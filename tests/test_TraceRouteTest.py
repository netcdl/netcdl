import test_helpers
import TraceRouteTest
import scapy


def test_constructor(mocker):
    s = test_helpers.O()
    s.host = 'host'
    s.routers = ['a', 'b', 'c']
    t = TraceRouteTest.TraceRouteTest(s)
    assert t.host == 'host'
    assert t.routers == ['a', 'b', 'c']


def test_run_success(mocker):
    s = test_helpers.O()
    s.host = 'example.com'
    s.routers = ['a', 'b']

    mocker.patch('scapy.all.sr')
    p1 = test_helpers.O()
    p2 = test_helpers.O()
    p1.fields = {'src': 'a'}
    p2.fields = {'src': 'b'}
    scapy.all.sr.return_value = [[(None, p1), (None, p2)], None]

    t = TraceRouteTest.TraceRouteTest(s)
    q = test_helpers.Q()
    t.run(q)
    assert q.what_was_put.passed is True


def test_run_failure(mocker):
    s = test_helpers.O()
    s.host = 'example.com'
    s.routers = ['a', 'b']

    mocker.patch('scapy.all.sr')
    p1 = test_helpers.O()
    p2 = test_helpers.O()
    p1.fields = {'src': 'b'}
    p2.fields = {'src': 'a'}
    scapy.all.sr.return_value = [[(None, p1), (None, p2)], None]

    t = TraceRouteTest.TraceRouteTest(s)
    q = test_helpers.Q()
    t.run(q)
    assert q.what_was_put.passed is False

def test_run_unknown_host(mocker):
    s = test_helpers.O()
    s.host = 'notarealdomainname.comxyz'
    s.routers = ['a', 'b']

    mocker.patch('scapy.all.sr')
    p1 = test_helpers.O()
    p2 = test_helpers.O()
    p1.fields = {'src': 'b'}
    p2.fields = {'src': 'a'}
    scapy.all.sr.return_value = [[(None, p1), (None, p2)], None]

    t = TraceRouteTest.TraceRouteTest(s)
    q = test_helpers.Q()
    t.run(q)
    assert q.what_was_put.passed is False
