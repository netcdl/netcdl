__author__ = 'Cody'

from ActiveTest import ActiveTest
import DefineMap
from scapy import all as s


class TraceRouteTest(ActiveTest):
    def __init__(self, statement):
        self.host = DefineMap.lookup_host(statement.host)
        self.routers = map(DefineMap.lookup_host, statement.routers)
        self.display_str = "traceroute to {0} should traverse {1}".format(self.host, ','.join(self.routers))
        super(TraceRouteTest, self).__init__(statement)

    def run(self, q):
        try:
            ans, unans = s.sr(s.IP(dst=str(self.host), ttl=(1, 30)) / s.TCP(sport=s.RandShort(), dport=80), retry=2,
                              timeout=5)
            self.success = True
            rtr_index = 0
            for snd, rcv in ans:
                if self.routers[rtr_index] == rcv.fields['src']:
                    # found the next router in our list
                    rtr_index += 1
                    if len(self.routers) == rtr_index:
                        # ran out of routers to look for, all done!
                        break
                else:
                    # found some router that didn't match
                    self.success = False
                    break
        except:
            self.success = False
        return q.put(self.create_result())
