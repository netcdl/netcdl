__author__ = 'codyhanson'

from Test import Test
import DefineMap


class PacketPortTest(Test):
    def __init__(self, statement):
        self.should_pass = statement.should == "should"
        self.port = statement.port
        self.protocol = statement.protocol
        self.direction = statement.direction
        should_str = 'should' if self.should_pass else 'should not'
        self.display_str = 'packets with {0} {1} port {2} {3} be seen'.format(self.protocol, self.direction, self.port,
                                                                              should_str)
        super(PacketPortTest, self).__init__(statement)

    def run(self, packets):
        self.success = not self.should_pass
        for p in packets:
            try:
                if p['payload']['payload']['name'] != self.protocol:
                    # be sure that we match TCP or UDP appropriately
                    continue
                s_port = p['payload']['payload']['fields']['sport']
                d_port = p['payload']['payload']['fields']['dport']
            except:
                continue
            if self.direction == 'source' and s_port == self.port:
                self.success = self.should_pass
                break
            elif self.direction == 'destination' and d_port == self.port:
                self.success = self.should_pass
                break
        return self.create_result()
