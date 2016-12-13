
from Test import Test
import EthtoolParser


class LinkDuplexTest(Test):

    def __init__(self, statement, iface):
        self.iface = iface
        self.duplex = statement.duplex
        self.should_pass = statement.should == "should"
        should_str = "should" if self.should_pass else "should not"
        self.display_str = "link duplex {0} be {1}".format(should_str, self.duplex)
        super(LinkDuplexTest, self).__init__(statement)

    def run(self):
        reported_duplex = EthtoolParser.parse(self.iface)['duplex'].lower()
        if self.duplex == reported_duplex and self.should_pass:
            self.success = True
        elif self.duplex != reported_duplex and not self.should_pass:
            self.success = True
        else:
            self.success = False
        return self.create_result()
