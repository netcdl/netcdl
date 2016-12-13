import DHCPTest
import test_helpers

packets = [
    {},
    {'payload': {'payload': {'name': 'UDP', 'fields': {'dport': 68}, 'payload': {'payload': {'fields': {
        'options': [
            ('server_id', '1.1.1.1'), ('subnet_mask', '255.255.255.0'), ('name_server', '8.8.8.8'),
            ('router', '10.0.0.1')
        ]}}}}}}
]


def test_ctor():
    statement = test_helpers.O()
    statement.type = 'server'
    statement.value = 'example.com'
    statement.should = 'should not'
    dt = DHCPTest.DHCPTest(statement)

    assert dt.type == 'server'
    assert dt.value == 'example.com'
    assert dt.should_pass is False


def test_run_zeropackets():
    statement = test_helpers.O()
    statement.type = 'server'
    statement.value = '1.1.1.1'
    statement.should = 'should'
    dt = DHCPTest.DHCPTest(statement)
    result = dt.run([])
    assert result.passed is False


def test_run_success_server():
    statement = test_helpers.O()
    statement.type = 'server'
    statement.value = '1.1.1.1'
    statement.should = 'should'
    dt = DHCPTest.DHCPTest(statement)
    result = dt.run(packets)
    assert result.passed is True


def test_run_success_dns():
    statement = test_helpers.O()
    statement.type = 'dns'
    statement.value = '8.8.8.8'
    statement.should = 'should'
    dt = DHCPTest.DHCPTest(statement)
    result = dt.run(packets)
    assert result.passed is True


def test_run_success_network():
    statement = test_helpers.O()
    statement.type = 'network'
    statement.value = '10.0.0.0/24'
    statement.should = 'should'
    dt = DHCPTest.DHCPTest(statement)
    result = dt.run(packets)
    assert result.passed is True


def test_run_success_gateway():
    statement = test_helpers.O()
    statement.type = 'gateway'
    statement.value = '10.0.0.1'
    statement.should = 'should'
    dt = DHCPTest.DHCPTest(statement)
    result = dt.run(packets)
    assert result.passed is True


def test_check_gateway_successful_fail():
    statement = test_helpers.O()
    statement.type = 'gateway'
    statement.value = '10.0.0.1'
    statement.should = 'should not'
    dt = DHCPTest.DHCPTest(statement)
    dt.dhcp_info = {}
    dt.dhcp_info['gateway'] = '10.0.0.2'
    dt.check_gateway()
    assert dt.success is True


def test_check_gateway_fail():
    statement = test_helpers.O()
    statement.type = 'gateway'
    statement.value = '10.0.0.1'
    statement.should = 'should'
    dt = DHCPTest.DHCPTest(statement)
    dt.dhcp_info = {}
    dt.dhcp_info['gateway'] = '10.0.0.2'
    dt.check_gateway()
    assert dt.success is False


def test_check_server_successful_fail():
    statement = test_helpers.O()
    statement.type = 'server'
    statement.value = '10.0.0.1'
    statement.should = 'should not'
    dt = DHCPTest.DHCPTest(statement)
    dt.dhcp_info = {}
    dt.dhcp_info['server'] = '10.0.0.2'
    dt.check_server()
    assert dt.success is True


def test_check_server_fail():
    statement = test_helpers.O()
    statement.type = 'server'
    statement.value = '10.0.0.1'
    statement.should = 'should'
    dt = DHCPTest.DHCPTest(statement)
    dt.dhcp_info = {}
    dt.dhcp_info['server'] = '10.0.0.2'
    dt.check_server()
    assert dt.success is False


def test_check_dns_successful_fail():
    statement = test_helpers.O()
    statement.type = 'dns'
    statement.value = '10.0.0.1'
    statement.should = 'should not'
    dt = DHCPTest.DHCPTest(statement)
    dt.dhcp_info = {}
    dt.dhcp_info['dns'] = '10.0.0.2'
    dt.check_dns()
    assert dt.success is True


def test_check_dns_fail():
    statement = test_helpers.O()
    statement.type = 'dns'
    statement.value = '10.0.0.1'
    statement.should = 'should'
    dt = DHCPTest.DHCPTest(statement)
    dt.dhcp_info = {}
    dt.dhcp_info['dns'] = '10.0.0.2'
    dt.check_dns()
    assert dt.success is False


def test_check_network_successful_fail():
    statement = test_helpers.O()
    statement.type = 'network'
    statement.value = '10.0.0.0/24'
    statement.should = 'should not'
    dt = DHCPTest.DHCPTest(statement)
    dt.dhcp_info = {}
    dt.dhcp_info['gateway'] = '12.0.0.2'
    dt.check_network()
    assert dt.success is True


def test_check_network_fail():
    statement = test_helpers.O()
    statement.type = 'network'
    statement.value = '10.0.0.0/24'
    statement.should = 'should'
    dt = DHCPTest.DHCPTest(statement)
    dt.dhcp_info = {}
    dt.dhcp_info['gateway'] = '12.0.0.2'
    dt.check_network()
    assert dt.success is False
