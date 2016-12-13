__author__ = 'codyhanson'

from ActiveTest import ActiveTest
import dns.resolver
import DefineMap

class DNSTest(ActiveTest):

    def __init__(self, statement):
        self.server = DefineMap.lookup_host(statement.server)
        self.should_pass = statement.should == "should"
        self.resolve_to = statement.resolve_to
        self.domain = statement.domain
        should_str = "should" if self.should_pass else "should not"
        self.display_str = "domain name {0} {1} resolve using server {2}".format(self.domain, should_str, self.server)
        super(DNSTest, self).__init__(statement)

    def run(self, q):
        try:
            response = dns.resolver.query(self.domain)
            if self.resolve_to is not None:
                if self.resolve_to in response.response.answer[0].items and self.should_pass:
                    self.success = True
                elif self.resolve_to not in response.response.answer[0].items and not self.should_pass:
                    self.success = True
                else:
                    self.success = False
            else:
                if len(response.response.answer[0].items) > 0 and self.should_pass:
                    #it resolved to something, anything at all
                    self.success = True
                elif len(response.response.answer[0].items) == 0 and not self.should_pass:
                    self.success = True
                else:
                    self.success = False
        except Exception as e:
            self.success = False
        return q.put(self.create_result())
