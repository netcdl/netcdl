import test_helpers
import PacketFromTest


def test_ctor_host():
    statement = test_helpers.O()
    statement.should = 'should not'
    statement.target = '10.0.0.1'
    statement.type = 'host'
    pft = PacketFromTest.PacketFromTest(statement)

    assert pft.should_pass is False
    assert pft.target == '10.0.0.1'
    assert pft.type == 'host'

def test_ctor_network():
    statement = test_helpers.O()
    statement.should = 'should not'
    statement.target = '10.0.0.0/8'
    statement.type = 'network'
    pft = PacketFromTest.PacketFromTest(statement)

    assert pft.should_pass is False
    assert pft.target == '10.0.0.0/8'
    assert pft.type == 'network'


def test_run_success_host():
    statement = test_helpers.O()
    statement.should = 'should'
    statement.target = '10.0.0.1'
    statement.type = 'host'
    pft = PacketFromTest.PacketFromTest(statement)

    packets = [{}, {'payload': {'fields': {'src': '10.0.0.1'}}}, {'payload': {'fields': {'src': 'abc'}}}]
    result = pft.run(packets)

    assert result.passed is True

def test_run_success_network():
    statement = test_helpers.O()
    statement.should = 'should'
    statement.target = '10.0.0.0/8'
    statement.type = 'network'
    pft = PacketFromTest.PacketFromTest(statement)

    packets = [{}, {'payload': {'fields': {'src': '10.1.2.1'}}}, {'payload': {'fields': {'src': 'abc'}}}]
    result = pft.run(packets)

    assert result.passed is True



def test_run_successful_failure_host():
    statement = test_helpers.O()
    statement.should = 'should not'
    statement.target = '10.0.0.1'
    statement.type = 'host'
    pft = PacketFromTest.PacketFromTest(statement)

    packets = [{}, {'payload': {'fields': {'src': '10.0.0.2'}}}, {'payload': {'fields': {'src': '192.168.1.1'}}}]
    result = pft.run(packets)

    assert result.passed is True

def test_run_successful_failure_network():
    statement = test_helpers.O()
    statement.should = 'should not'
    statement.target = '10.0.0.0/8'
    statement.type = 'network'
    pft = PacketFromTest.PacketFromTest(statement)

    packets = [{}, {'payload': {'fields': {'src': '11.0.0.2'}}}, {'payload': {'fields': {'src': '192.168.1.1'}}}]
    result = pft.run(packets)

    assert result.passed is True


def test_run_did_not_find():
    statement = test_helpers.O()
    statement.should = 'should'
    statement.target = '10.0.0.1'
    statement.type = 'host'
    pft = PacketFromTest.PacketFromTest(statement)

    packets = [{}, {'payload': {'fields': {'src': '10.0.0.2'}}}, {'payload': {'fields': {'src': '192.168.1.1'}}}]
    result = pft.run(packets)

    assert result.passed is False


def test_run_found_but_shouldnt():
    statement = test_helpers.O()
    statement.should = 'should not'
    statement.target = '10.0.0.1'
    statement.type = 'host'
    pft = PacketFromTest.PacketFromTest(statement)

    packets = [{}, {'payload': {'fields': {'src': '10.0.0.1'}}}, {'payload': {'fields': {'src': '192.168.1.1'}}}]
    result = pft.run(packets)

    assert result.passed is False
