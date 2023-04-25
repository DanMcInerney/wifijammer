#!/usr/bin/env python3
from setuptools import setup

setup(
    name = "wifijammer",
    version = "0.1",
    author = "Dan McInerney",
    description = "Continuously jam all wifi clients and access points within range.",
    keywords = "WiFi 802.11 jammer deauth",
    url = "https://github.com/DanMcInerney/wifijammer",
    scripts=['wifijammer'],
    # py_modules=['wifijammer'],
    install_requires=['scapy'],
    long_description="Continuously jam all wifi clients and access points within range.",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
)

)
