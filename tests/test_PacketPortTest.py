import test_helpers
import PacketPortTest


def test_ctor():
    statement = test_helpers.O()
    statement.should = 'should not'
    statement.protocol = 'TCP'
    statement.port = 80
    statement.direction = 'source'
    ppt = PacketPortTest.PacketPortTest(statement)

    assert ppt.should_pass is False
    assert ppt.port == 80
    assert ppt.direction == 'source'


def test_run_success():
    statement = test_helpers.O()
    statement.should = 'should'
    statement.protocol = 'TCP'
    statement.port = 80
    statement.direction = 'source'
    ppt = PacketPortTest.PacketPortTest(statement)

    packets = [
        {},
        {'payload': {'payload': {'name': 'UDP', 'fields': {'sport': 80, 'dport': 1000}}}},
        {'payload': {'payload': {'name': 'TCP', 'fields': {'sport': 80, 'dport': 1001}}}}
    ]
    result = ppt.run(packets)

    assert result.passed is True


def test_run_failure():
    statement = test_helpers.O()
    statement.should = 'should not'
    statement.protocol = 'TCP'
    statement.port = 80
    statement.direction = 'destination'
    ppt = PacketPortTest.PacketPortTest(statement)

    packets = [
        {},
        {'payload': {'payload': {'name': 'UDP', 'fields': {'sport': 800, 'dport': 80}}}},
        {'payload': {'payload': {'name': 'TCP', 'fields': {'sport': 800, 'dport': 80}}}}
    ]
    result = ppt.run(packets)

    assert result.passed is False
