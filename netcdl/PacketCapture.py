__author__ = 'codyhanson'

from scapy import all as s
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

import multiprocessing as mp


class PacketCapture:
    def __init__(self, iface, q):
        self.iface = iface
        self.packets = list()
        self.p = mp.Process(target=self.capture, args=(q,))

    def start(self):
        return self.p.start()

    #TODO continue capturing as many packets as possible, until the signal comes that all other tests have finished
    def capture(self, q):
        self.packets = s.sniff(count=1500, iface=self.iface)
        processed_packets = map(PacketCapture.trim_packet, self.packets.res)
        return q.put(processed_packets)

    # This is a hack to trim down the scapy packets so that we can pickle them and put them
    # into the IPC queue. Ideally we could pass back more of the raw packet data.
    # Instead I just loaded the fields that i am using into dicts.
    @staticmethod
    def trim_packet(p):
        try:
            if p.name in ['IP', 'Ethernet', 'TCP', 'UDP', 'BOOTP', 'DHCP options', 'DHCP']:
                return {'fields': p.fields, 'payload': PacketCapture.trim_packet(p.payload), 'name': p.name}
            else:
                return None
        except:
            return None

    def end(self):
        return self.p.join()
