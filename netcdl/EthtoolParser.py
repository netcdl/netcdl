import subprocess
import re

"""
Example output
$ ethtool eth0
Settings for eth0:
        Supported ports: [ TP ]
        Supported link modes:   10baseT/Half 10baseT/Full
                                100baseT/Half 100baseT/Full
                                1000baseT/Half 1000baseT/Full
        Supported pause frame use: No
        Supports auto-negotiation: Yes
        Advertised link modes:  10baseT/Half 10baseT/Full
                                100baseT/Half 100baseT/Full
                                1000baseT/Half 1000baseT/Full
        Advertised pause frame use: No
        Advertised auto-negotiation: No
        Speed: 1000Mb/s
        Duplex: Full
        Port: Twisted Pair
        PHYAD: 0
        Transceiver: internal
        Auto-negotiation: on
        MDI-X: Unknown
Cannot get wake-on-lan settings: Operation not permitted
        Current message level: 0x000000ff (255)
                               drv probe link timer ifdown ifup rx_err tx_err
        Link detected: yes
"""


def parse(iface):
    output = subprocess.Popen("ethtool " + iface, shell=True, stdout=subprocess.PIPE).stdout.read()
    results = {}
    results['speed'] = parse_speed(output)
    results['duplex'] = parse_duplex(output)
    return results


def parse_speed(ethtool_output):
    m = re.search('Speed: (\d+.*?)\n', ethtool_output)
    speed = m.group(1)
    return speed

def parse_duplex(ethtool_output):
    m = re.search('Duplex: (.*)', ethtool_output)
    duplex = m.group(1)
    return duplex

