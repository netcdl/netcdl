__author__ = 'codyhanson'

from Test import Test
import iptools
import DefineMap


class DHCPTest(Test):
    def __init__(self, statement):
        self.type = statement.type
        self.should_pass = statement.should == "should"

        if self.type == 'network':
            self.value = DefineMap.lookup_network(statement.value)
        elif self.type in ['dns', 'gateway', 'server']:
            self.value = DefineMap.lookup_host(statement.value)

        should_str = "should" if self.should_pass else "should not"
        self.display_str = 'dhcp {0} {1} be {2}'.format(self.type, should_str, self.value)
        super(DHCPTest, self).__init__(statement)

    def run(self, packets):
        dhcp_packets = []
        for p in packets:
            try:
                # gather the DHCP response packets sent back to us.
                if p['payload']['payload']['name'] == 'UDP':
                    if p['payload']['payload']['fields']['dport'] == 68:
                        dhcp_packets.append(p)
            except:
                continue

        # TODO what if we get more than one response?
        if len(dhcp_packets) == 0:
            #didn't get anything
            self.success = False
            return self.create_result()

        dhcp_packet = dhcp_packets[0]['payload']['payload']['payload']['payload']['fields']

        self.dhcp_info = {}
        for option in dhcp_packet['options']:
            if option[0] == 'server_id':
                self.dhcp_info['server'] = option[1]
            elif option[0] == 'name_server':
                self.dhcp_info['dns'] = option[1]
            elif option[0] == 'router':
                self.dhcp_info['gateway'] = option[1]

        if self.type == 'server':
            self.check_server()
        elif self.type == 'dns':
            self.check_dns()
        elif self.type == 'network':
            self.check_network()
        elif self.type == 'gateway':
            self.check_gateway()
        return self.create_result()

    def check_server(self):
        if self.should_pass and self.dhcp_info['server'] == self.value:
            self.success = True
        elif not self.should_pass and self.dhcp_info['server'] != self.value:
            self.success = True
        else:
            self.success = False

    def check_dns(self):
        if self.should_pass and self.dhcp_info['dns'] == self.value:
            self.success = True
        elif not self.should_pass and self.dhcp_info['dns'] != self.value:
            self.success = True
        else:
            self.success = False

    def check_network(self):
        if self.should_pass and self.dhcp_info['gateway'] in iptools.IpRange(self.value):
            self.success = True
        elif not self.should_pass and self.dhcp_info['gateway'] not in iptools.IpRange(self.value):
            self.success = True
        else:
            self.success = False

    def check_gateway(self):
        if self.should_pass and self.dhcp_info['gateway'] == self.value:
            self.success = True
        elif not self.should_pass and self.dhcp_info['gateway'] != self.value:
            self.success = True
        else:
            self.success = False
