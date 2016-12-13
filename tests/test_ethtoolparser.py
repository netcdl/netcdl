
import EthtoolParser


ethtool_output = """
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

def test_parse(mocker):
    res = EthtoolParser.parse('eth0')
    assert res['speed'] is not None
    assert res['duplex'] is not None

def test_parse_speed():
    assert  EthtoolParser.parse_speed(ethtool_output) == '1000Mb/s'

def test_parse_duplex():
    assert  EthtoolParser.parse_duplex(ethtool_output) == 'Full'
