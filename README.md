wifijammer
==========

Continuously jam all wifi clients within range.


The effectiveness of this script is constrained by your wireless card. Granularity is given in the options so you can more effectively jam. The more clients in the deauth list the less packets/second are going to reach each client/AP. I have found on my Alfa card that more than about 6 in the list and you won't get good consistency in killing their connection. The most consistent connection loss seems to be when you just focus on one channel with the -c <num> option.


Requires: airmon-ng, python 2.7, scapy, a wireless card capable of injection


All options:

```shell
python wifijammer.py [-c CHANNEL] [-i INTERFACE] [-m MAXIMUM] [-p PACKETS] [-s SKIP] [-t TIME INTERVAL]
```


Usage
-----


### Simple
``` shell
python wifijammer.py
```

This will find the monitor mode interface if one is up and if one isn't up it will find the most powerful wireless interface and turn on monitor mode. It will then start hopping channels and identifying all wireless communication between clients and access points. Once it's identified a client/AP combo, it will constantly send deauthentication packets to them.


By default this simple usage has no set interval time between packets being sent and will go down its list of clients/APs sending 1 packet to the client from the AP, and 1 packet from the AP to the client before moving on to the next client/AP connection. You can adjust both these options with the -t and -p options respectively.


### Advanced
```shell
python wifijammer.py -c 1 -p 5 -t .00001 -s DL:3D:8D:JJ:39:52
```

Set the monitor mode interface to only listen on channel 1, send 5 packets to the client from the AP and 5 packets from the AP to the client, set a time interval of .00001 seconds between sending each deauth (try this if you get a scapy error like 'no buffer space'), and do not deauth the MAC DL:3D:8D:JJ:39:52.


### Walking/driving around
```shell
python wifijammer.py -m 10
```
The -m option sets a max number of client/AP combos that the script will attempt to deauth. When the max number is reached, it clears and repopulates its list based on what traffic it sniffs in the area. This allows you to constantly update the deauth list with client/AP combos who have the strongest signal in case you were not stationary. 


### My favorite
```shell
python wifijammer.py -c 1 -s 11:22:33:44:55:EE:77
```

This is handy in case you want to tempt people to join your access point (using LANs.py or a Pineapple would be good examples). It will only listen for client/AP combos on channel 1 and it will not deauth any connections to or from 11:22:33:44:55:EE:77 which we will pretend is our own access point's MAC address. I find the best consistency in killing connections when you focus the script on one channel. Initial evidence seems to suggest that keeping the consecutive number of packets send as the default 1 to
client, 1 to AP is the best as well. 


