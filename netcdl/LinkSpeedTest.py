
import EthtoolParser
from Test import Test

class LinkSpeedTest(Test):

    def __init__(self, statement, iface):
        self.iface = iface
        self.speed = statement.speed.lower()
        self.should_pass = statement.should == "should"
        should_str = "should" if self.should_pass else "should not"
        self.display_str = "link speed {0} be {1}".format(should_str, self.speed)
        super(LinkSpeedTest, self).__init__(statement)

    def run(self):
        reported_speed = EthtoolParser.parse(self.iface)['speed'].lower()
        if self.speed == reported_speed and self.should_pass:
            self.success = True
        elif self.speed != reported_speed and not self.should_pass:
            self.success = True
        else:
            self.success = False
        self.result_detail = "Reported Speed:{0}".format(reported_speed)
        return self.create_result()
