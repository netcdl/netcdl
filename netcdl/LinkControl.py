from scapy import all as s

class LinkControl:
    def __init__(self, iface):
        # This is the link name
        self.iface = iface

    # Send DHCP packets in order to elicit a response which we will capture in the packet capture
    def dhcp(self):
        packet = (s.Ether(dst="ff:ff:ff:ff:ff:ff") /
                  s.IP(src="0.0.0.0", dst="255.255.255.255") /
                  s.UDP(sport=68, dport=67) /
                  s.BOOTP(chaddr=s.RandString(12, 'acbedf1032547698')) /
                  s.DHCP(options=[("message-type", "discover"), "end"])
                  )

        s.sendp(packet, iface=self.iface, count=1)
