import scapy
import PingTest
import test_helpers as th



class PingStatement:
    def __init__(self, should):
        self.reachable = th.O()
        self.reachable.host = '8.8.8.8'
        self.reachable.should = should


def test_ctor(mocker):
    pst = PingStatement('should')
    pt = PingTest.PingTest(pst)
    assert pt.target == '8.8.8.8'
    assert pt.should_pass is True


def test_run_success(mocker):
    mocker.patch('scapy.all.sr')
    ans = th.O()
    ans.res = [1, 2, 3]
    scapy.all.sr.return_value = [ans, 'unans']
    pst = PingStatement('should')
    pt = PingTest.PingTest(pst)
    q = th.Q()
    pt.run(q)
    scapy.all.sr.assert_called()
    assert q.what_was_put.passed is True


def test_run_successful_fail(mocker):
    mocker.patch('scapy.all.sr')
    ans = th.O()
    ans.res = []
    scapy.all.sr.return_value = [ans, 'unans']
    pst = PingStatement('should not')
    pt = PingTest.PingTest(pst)
    q = th.Q()
    pt.run(q)
    scapy.all.sr.assert_called()
    assert q.what_was_put.passed is True


def test_run_fail1(mocker):
    mocker.patch('scapy.all.sr')
    ans = th.O()
    ans.res = []
    scapy.all.sr.return_value = [ans, 'unans']
    pst = PingStatement('should')
    pt = PingTest.PingTest(pst)
    q = th.Q()
    pt.run(q)
    scapy.all.sr.assert_called()
    assert q.what_was_put.passed is False


def test_run_fail2(mocker):
    mocker.patch('scapy.all.sr')
    ans = th.O()
    ans.res = [1, 2, 3]
    scapy.all.sr.return_value = [ans, 'unans']
    pst = PingStatement('should not')
    pt = PingTest.PingTest(pst)
    q = th.Q()
    pt.run(q)
    scapy.all.sr.assert_called()
    assert q.what_was_put.passed is False
