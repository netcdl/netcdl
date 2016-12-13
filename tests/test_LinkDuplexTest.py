import mock
from pytest_mock import mocker
import pytest

from LinkDuplexTest import LinkDuplexTest
import EthtoolParser

class statement:
    pass


def test_DuplexTest_constructor(mocker):
    s = statement()
    s.duplex = 'full'
    s.should = 'should not'
    l = LinkDuplexTest(s, 'eth0')
    assert l.iface == 'eth0'
    assert l.duplex == 'full'
    assert l.should_pass is False


def test_DuplexTest_run_passing_pos(mocker):
    parse_output = {'duplex': 'FULL'}
    mocker.patch.object(EthtoolParser, 'parse')
    EthtoolParser.parse.return_value = parse_output

    s = statement()
    s.duplex = 'full'
    s.should = 'should'

    l = LinkDuplexTest(s, 'eth0')
    res = l.run()
    assert res.passed is True

def test_DuplexTest_run_passing_neg(mocker):
    parse_output = {'duplex': 'half'}
    mocker.patch.object(EthtoolParser, 'parse')
    EthtoolParser.parse.return_value = parse_output

    s = statement()
    s.duplex = 'full'
    s.should = 'should not'

    l = LinkDuplexTest(s, 'eth0')
    res = l.run()
    assert res.passed is True

def test_DuplexTest_run_not_passing(mocker):
    parse_output = {'duplex': 'HALF'}
    mocker.patch.object(EthtoolParser, 'parse')
    EthtoolParser.parse.return_value = parse_output

    s = statement()
    s.duplex = 'full'
    s.should = 'should'

    l = LinkDuplexTest(s, 'eth0')
    res = l.run()
    assert res.passed is False
