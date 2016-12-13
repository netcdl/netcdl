import test_helpers
import FrameTypeTest


def test_ctor():
    statement = test_helpers.O()
    statement.should = 'should not'
    statement.value = '0xFF'
    ftt = FrameTypeTest.FrameTypeTest(statement)

    assert ftt.should_pass is False
    assert ftt.value == 255


def test_run_success():
    statement = test_helpers.O()
    statement.should = 'should'
    statement.value = '0xFF'
    ftt = FrameTypeTest.FrameTypeTest(statement)

    packets = [{'fields': {'type': 0}}, {'fields': {'type': 255}}]
    result = ftt.run(packets)

    assert result.passed is True


def test_run_successful_failure():
    statement = test_helpers.O()
    statement.should = 'should not'
    statement.value = '0xFF'
    ftt = FrameTypeTest.FrameTypeTest(statement)

    packets = [{'fields': {'type': 10}}, {'fields': {'type': 253}}]
    result = ftt.run(packets)

    assert result.passed is True

def test_run_did_not_find():
    statement = test_helpers.O()
    statement.should = 'should'
    statement.value = '0xFF'
    ftt = FrameTypeTest.FrameTypeTest(statement)

    packets = [{'fields': {'type': 10}}, {'fields': {'type': 253}}]
    result = ftt.run(packets)

    assert result.passed is False

def test_run_found_but_shouldnt():
    statement = test_helpers.O()
    statement.should = 'should not'
    statement.value = '0xFF'
    ftt = FrameTypeTest.FrameTypeTest(statement)

    packets = [{'fields': {'type': 255}}, {'fields': {'type': 253}}]
    result = ftt.run(packets)

    assert result.passed is False
