wifijammer
==========

Continuously jam all wifi clients and access points within range. The effectiveness of this script is constrained by your wireless card. Alfa cards seem to effectively jam within about a block radius with heavy access point saturation. Granularity is given in the options for more effective targeting. 


Requires: python 2.7, python-scapy, a wireless card capable of injection


Usage
-----


### Simple
``` shell
python wifijammer.py
```

This will find the most powerful wireless interface and turn on monitor mode. If a monitor mode interface is already up it will use the first one it finds instead. It will then start sequentially hopping channels 1 per second from channel 1 to 11 identifying all access points and clients connected to those access points. On the first pass through all the wireless channels it is only identifying targets. After that the 1sec per channel time limit is eliminated and channels are hopped as soon as the deauth packets finish sending. Note that it will still add clients and APs as it finds them after the first pass through.

Upon hopping to a new channel it will identify targets that are on that channel and send 1 deauth packet to the client from the AP, 1 deauth to the AP from the client, and 1 deauth to the AP destined for the broadcast address to deauth all clients connected to the AP. Many APs ignore deauths to broadcast addresses.

```shell
python wifijammer.py -a 00:0E:DA:DE:24:8E -c 2
```

Deauthenticate all devices with which 00:0E:DA:DE:24:8E communicates and skips channel hopping by setting the channel to the target AP's channel (2 in this case). This would mainly be an access point's MAC so all clients associated with that AP would be deauthenticated, but you can also put a client MAC here to target that one client and any other devices that communicate with it.


### Advanced
```shell
python wifijammer.py -c 1 -p 5 -t .00001 -s DL:3D:8D:JJ:39:52 -d --world
```

* `-c`, Set the monitor mode interface to only listen and deauth clients or APs on channel 1

* `-p`, Send 5 packets to the client from the AP and 5 packets to the AP from the client along with 5 packets to the broadcast address of the AP

* `-t`, Set a time interval of .00001 seconds between sending each deauth (try this if you get a scapy error like 'no buffer space')

* `-s`, Do not deauth the MAC DL:3D:8D:JJ:39:52. Ignoring a certain MAC address is handy in case you want to tempt people to join your access point in cases of wanting to use LANs.py or a Pineapple on them.

* `-d`, Do not send deauths to access points' broadcast address; this will speed up the deauths to the clients that are found

* `--world`, Set the max channel to 13. In N. America the max channel standard is 11, but the rest of the world uses 13 channels so use this option if you're not in N. America


### Walking/driving around
```shell
python wifijammer.py -m 10
```
The `-m` option sets a max number of client/AP combos that the script will attempt to deauth. When the max number is reached, it clears and repopulates its list based on what traffic it sniffs in the area. This allows you to constantly update the deauth list with client/AP combos who have the strongest signal in case you were not stationary. If you want to set a max and not have the deauth list clear itself when the max is hit, just add the -n option like: `-m 10 -n`


All options:

```shell
python wifijammer.py [-a AP MAC] [-c CHANNEL] [-d] [-i INTERFACE] [-m MAXIMUM] [-n] [-p PACKETS] [-s SKIP] [-t TIME INTERVAL]
```

Technical breakdown
-------
[How to kick everyone around you off wifi with python](http://danmcinerney.org/how-to-kick-everyone-around-you-off-wifi-with-python/)


License
-------

Copyright (c) 2014, Dan McInerney
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
* Neither the name of Dan McInerney nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

***
* [danmcinerney.org](http://danmcinerney.org)
* [![Flattr this](http://api.flattr.com/button/flattr-badge-large.png)](https://flattr.com/submit/auto?user_id=DanMcInerney&url=https://github.com/DanMcInerney/wifijammer&title=wifijammer&language=&tags=github&category=software) 
* [![Analytics](https://ga-beacon.appspot.com/UA-46613304-3/wifijammer/README.md)](https://github.com/igrigorik/ga-beacon)
