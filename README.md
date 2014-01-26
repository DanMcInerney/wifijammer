wifijammer
==========

Continuously jam all wifi clients within range.

Requires: airmon-ng, python 2.7, scapy, a wireless card capable of injection


All options:

```shell
python wifijammer.py [-c CHANNEL] [-i INTERFACE] [-m MAXIMUM] [-s SKIP] [-t TIME INTERVAL]
```

Usage
-----


``` shell
python wifijammer.py
```

This will find the monitor mode interface if one is up and if one isn't up it will find the most powerful wireless interface and turn on monitor mode. It will then start hopping channels sequentially identifying all wireless communication between clients and access points and deauthenticate every client/AP combo it comes across until you tell it to stop.

By default it sends 2 deauth packets to each client/AP combo every 1 second. 
