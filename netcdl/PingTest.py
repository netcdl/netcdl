__author__ = 'Cody'

from scapy import all as s
from ActiveTest import ActiveTest
import DefineMap

class PingTest(ActiveTest):
    def __init__(self, statement):
        self.target = DefineMap.lookup_host(statement.reachable.host)
        self.should_pass = statement.reachable.should == 'should'
        self.display_str = "ping to {0} should succeed:{1}".format(self.target, self.should_pass)
        super(PingTest, self).__init__(statement)

    def run(self, q):
        ans, unans = s.sr(s.IP(dst=self.target) / s.ICMP(), retry=1, timeout=3)
        if len(ans.res) > 0 and self.should_pass:
            self.success = True
        elif len(ans.res) == 0 and not self.should_pass:
            self.success = True
        else:
            self.success = False

        self.result_detail = 'ping detail'
        return q.put(self.create_result())
