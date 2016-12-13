
from LinkSpeedTest import LinkSpeedTest
import EthtoolParser

class statement:
    pass


def test_DuplexTest_constructor(mocker):
    s = statement()
    s.speed = '1000Mbps'
    s.should = 'should not'
    l = LinkSpeedTest(s, 'eth0')
    assert l.iface == 'eth0'
    assert l.speed == '1000mbps'
    assert l.should_pass is False


def test_DuplexTest_run_passing_pos(mocker):
    parse_output = {'speed': '1000MBPS'}
    mocker.patch.object(EthtoolParser, 'parse')
    EthtoolParser.parse.return_value = parse_output

    s = statement()
    s.speed = '1000mbps'
    s.should = 'should'

    l = LinkSpeedTest(s, 'eth0')
    res = l.run()
    assert res.passed is True

def test_DuplexTest_run_passing_neg(mocker):
    parse_output = {'speed': '1000MBPS'}
    mocker.patch.object(EthtoolParser, 'parse')
    EthtoolParser.parse.return_value = parse_output

    s = statement()
    s.speed = '100mbps'
    s.should = 'should not'

    l = LinkSpeedTest(s, 'eth0')
    res = l.run()
    assert res.passed is True

def test_DuplexTest_run_not_passing(mocker):
    parse_output = {'speed': '1000MBPS'}
    mocker.patch.object(EthtoolParser, 'parse')
    EthtoolParser.parse.return_value = parse_output

    s = statement()
    s.speed = '100mbps'
    s.should = 'should'

    l = LinkSpeedTest(s, 'eth0')
    res = l.run()
    assert res.passed is False
