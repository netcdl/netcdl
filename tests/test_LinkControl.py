

import scapy
import LinkControl


def test_link_control_dhcp(mocker):
    mocker.patch('scapy.all.sendp')
    lc = LinkControl.LinkControl('eth0')
    assert lc.iface == 'eth0'
    lc.dhcp()
    scapy.all.sendp.assert_called()
