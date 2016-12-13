__author__ = 'codyhanson'

from Test import Test


class PacketTypeTest(Test):
    def __init__(self, statement):
        self.should_pass = statement.should == "should"
        #Since hex string values have 0x in front of them python automatically does the correct thing
        self.value = int(statement.value, 0)
        should_str = 'should' if self.should_pass else 'should not'
        self.display_str = 'packets with type{0} {1} be seen'.format(self.value, should_str)
        super(PacketTypeTest, self).__init__(statement)

    def run(self, packets):
        self.success = not self.should_pass
        for p in packets:
            try:
                proto_number = p['payload']['fields']['proto']
            except:
                continue
            if proto_number == self.value:
                self.success = self.should_pass
                break

        return self.create_result()
