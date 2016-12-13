__author__ = 'codyhanson'

from Test import Test
import DefineMap
import iptools


class PacketFromTest(Test):
    def __init__(self, statement):
        self.should_pass = statement.should == "should"
        self.type = statement.type

        if self.type == "network":
            self.target = DefineMap.lookup_network(statement.target)
        else:  # host
            self.target = DefineMap.lookup_host(statement.target)

        should_str = 'should' if self.should_pass else 'should not'
        self.display_str = 'packets from {0} {1} be seen'.format(self.target, should_str)
        super(PacketFromTest, self).__init__(statement)

    def run(self, packets):
        self.success = not self.should_pass
        for p in packets:
            try:
                src_ip = p['payload']['fields'].get('src', None)
                if self.type == "network" and src_ip in iptools.IpRange(self.target):
                    self.success = self.should_pass
                    break
                elif src_ip == self.target:
                    self.success = self.should_pass
                    break
            except:
                continue

        return self.create_result()
