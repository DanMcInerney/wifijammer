#!/usr/bin/env python2
from setuptools import setup, find_packages

setup(
    name = "wifijammer",
    version = "0.1",
    author = "Dan McInerney",
    author_email = "andrewjcarter@gmail.com",
    description = "Continuously jam all wifi clients and access points within range.",
    # license = "GPL",
    keywords = "WiFi 802.11 jammer deauth",
    url = "https://github.com/DanMcInerney/wifijammer",
    packages=find_packages(),
    entry_points={
        'console_scripts':
        ['wifijammer = wifijammer:main']
    },
    install_requires=['scapy'],
    long_description="""Continuously jam all wifi clients and access points within range. The effectiveness of this script is constrained by your wireless card. Alfa cards seem to effectively jam within about a block radius with heavy access point saturation.
                   Granularity is given in the options for more effective targeting.""",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
)
