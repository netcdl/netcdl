__author__ = 'codyhanson'

from Test import Test


class FrameTypeTest(Test):
    def __init__(self, statement):
        self.should_pass = statement.should == "should"
        #Since hex string values have 0x in front of them python automatically does the correct thing
        self.value = int(statement.value, 0)
        should_str = 'should' if self.should_pass else 'should not'
        self.display_str = 'frames with ethertype {0} {1} be seen'.format(self.value, should_str)
        super(FrameTypeTest, self).__init__(statement)

    def run(self, packets):
        self.success = not self.should_pass
        for p in packets:
            ethertype = p['fields']['type']
            if ethertype == self.value:
                self.success = self.should_pass
                break

        return self.create_result()
