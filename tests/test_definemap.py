import DefineMap


class TestDefineMap:
    def test_host_mapping(self):
        DefineMap.add_host('testhost', '10.0.0.1')
        assert DefineMap.lookup_host('testhost') == '10.0.0.1'
        assert DefineMap.lookup_host('missingHost') == 'missingHost'
        assert DefineMap.lookup_network('testhost') != '10.0.0.1'

    def test_network_mapping(selfs):
        DefineMap.add_network('testnetwork', '10.0.0.0/8')
        assert DefineMap.lookup_network('testnetwork') == '10.0.0.0/8'
        assert DefineMap.lookup_network('unknownNetwork') == 'unknownNetwork'
        assert DefineMap.lookup_host('testnetwork') != '10.0.0.0/8'
