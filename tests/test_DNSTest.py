import test_helpers as th
import DNSTest
import dns.resolver


def test_ctor(mocker):
    statement = th.O()
    statement.should = 'should not'
    statement.server = 'myserver'
    statement.resolve_to = '10.0.0.200'
    statement.domain = 'example.com'
    t = DNSTest.DNSTest(statement)
    assert t.server == 'myserver'
    assert t.server == 'myserver'
    assert t.domain == 'example.com'
    assert t.resolve_to == '10.0.0.200'


def test_run_success(mocker):

    mocker.patch('dns.resolver.query')
    ans = th.O()
    ans.response = th.O()
    ans.response.answer = [th.O()]
    ans.response.answer[0].items = ['10.0.0.200']
    dns.resolver.query.return_value = ans

    statement = th.O()
    statement.should = 'should'
    statement.server = 'myserver'
    statement.resolve_to = '10.0.0.200'
    statement.domain = 'example.com'
    t = DNSTest.DNSTest(statement)
    q = th.Q()
    t.run(q)
    dns.resolver.query.assert_called()
    assert q.what_was_put.passed is True

def test_run_success_no_resolve_to(mocker):

    mocker.patch('dns.resolver.query')
    ans = th.O()
    ans.response = th.O()
    ans.response.answer = [th.O()]
    ans.response.answer[0].items = ['10.0.0.200']
    dns.resolver.query.return_value = ans

    statement = th.O()
    statement.should = 'should'
    statement.server = 'myserver'
    statement.resolve_to = None
    statement.domain = 'example.com'
    t = DNSTest.DNSTest(statement)
    q = th.Q()
    t.run(q)
    dns.resolver.query.assert_called()
    assert q.what_was_put.passed is True

def test_run_successful_fail(mocker):
    mocker.patch('dns.resolver.query')
    ans = th.O()
    ans.response = th.O()
    ans.response.answer = [th.O()]
    ans.response.answer[0].items = ['10.0.0.200']
    dns.resolver.query.return_value = ans

    statement = th.O()
    statement.should = 'should not'
    statement.server = 'myserver'
    statement.resolve_to = '10.0.0.201'
    statement.domain = 'example.com'
    t = DNSTest.DNSTest(statement)
    q = th.Q()
    t.run(q)
    dns.resolver.query.assert_called()
    assert q.what_was_put.passed is True

def test_run_successful_fail2(mocker):

    mocker.patch('dns.resolver.query')
    ans = th.O()
    ans.response = th.O()
    ans.response.answer = [th.O()]
    ans.response.answer[0].items = []
    dns.resolver.query.return_value = ans

    statement = th.O()
    statement.should = 'should not'
    statement.server = 'myserver'
    statement.resolve_to = None
    statement.domain = 'example.com'
    t = DNSTest.DNSTest(statement)
    q = th.Q()
    t.run(q)
    dns.resolver.query.assert_called()
    assert q.what_was_put.passed is True


