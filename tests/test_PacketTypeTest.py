import test_helpers
import PacketTypeTest


def test_ctor():
    statement = test_helpers.O()
    statement.should = 'should not'
    statement.value = '0xFF'
    ptt = PacketTypeTest.PacketTypeTest(statement)

    assert ptt.should_pass is False
    assert ptt.value == 255


def test_run_success():
    statement = test_helpers.O()
    statement.should = 'should'
    statement.value = '0xFF'
    ptt = PacketTypeTest.PacketTypeTest(statement)

    packets = [{}, {'payload': {'fields': {'proto': 211}}}, {'payload': {'fields': {'proto': 255}}}]
    result = ptt.run(packets)

    assert result.passed is True


def test_run_successful_failure():
    statement = test_helpers.O()
    statement.should = 'should not'
    statement.value = '0xFF'
    ptt = PacketTypeTest.PacketTypeTest(statement)

    packets = [{}, {'payload': {'fields': {'proto': 211}}}, {'payload': {'fields': {'proto': 55}}}]
    result = ptt.run(packets)

    assert result.passed is True


def test_run_did_not_find():
    statement = test_helpers.O()
    statement.should = 'should'
    statement.value = '0xFF'
    ptt = PacketTypeTest.PacketTypeTest(statement)

    packets = [{}, {'payload': {'fields': {'proto': 211}}}, {'payload': {'fields': {'proto': 55}}}]
    result = ptt.run(packets)

    assert result.passed is False


def test_run_found_but_shouldnt():
    statement = test_helpers.O()
    statement.should = 'should not'
    statement.value = '0xFF'
    ptt = PacketTypeTest.PacketTypeTest(statement)

    packets = [{}, {'payload': {'fields': {'proto': 211}}}, {'payload': {'fields': {'proto': 255}}}]
    result = ptt.run(packets)

    assert result.passed is False
