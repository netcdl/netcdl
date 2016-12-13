import test_helpers
import FileFetchTest
import requests


def test_ctor():
    statement = test_helpers.O()
    statement.protocol = 'HTTP'
    statement.target = 'example.com'
    statement.should = 'should not'
    statement.filename = 'afile.txt'
    statement.port = 8080
    fft = FileFetchTest.FileFetchTest(statement)

    assert fft.protocol == 'HTTP'
    assert fft.target == 'example.com'
    assert fft.should_pass is False
    assert fft.port == 8080
    assert fft.filename == 'afile.txt'


def test_parse_port():
    assert FileFetchTest.FileFetchTest.parse_port('http', 111) == 111
    assert FileFetchTest.FileFetchTest.parse_port('ftp', 111) == 111
    assert FileFetchTest.FileFetchTest.parse_port('tftp', 111) == 111
    assert FileFetchTest.FileFetchTest.parse_port('http', 0) == 80
    assert FileFetchTest.FileFetchTest.parse_port('ftp', 0) == 21
    assert FileFetchTest.FileFetchTest.parse_port('tftp', 0) == 69


def test_run_http_success(mocker):
    mocker.patch('requests.get')
    requests.get.return_value = test_helpers.O()
    requests.get.return_value.status_code = 200
    statement = test_helpers.O()
    statement.protocol = 'http'
    statement.target = 'www.google.com'
    statement.should = 'should'
    statement.filename = 'index.html'
    statement.port = 80
    fft = FileFetchTest.FileFetchTest(statement)
    q = test_helpers.Q()
    fft.run(q)

    assert q.what_was_put.passed is True

def test_run_http_failure(mocker):
    statement = test_helpers.O()
    statement.protocol = 'http'
    statement.target = 'example.com'
    statement.should = 'should'
    statement.filename = 'index.html'
    statement.port = 80111
    fft = FileFetchTest.FileFetchTest(statement)
    q = test_helpers.Q()
    fft.run(q)

    assert q.what_was_put.passed is False

def test_run_ftp_success(mocker):
    statement = test_helpers.O()
    statement.protocol = 'ftp'
    statement.target = 'speedtest.tele2.net'
    statement.should = 'should'
    statement.filename = '1KB.zip'
    statement.port = 21
    fft = FileFetchTest.FileFetchTest(statement)
    q = test_helpers.Q()
    fft.run(q)

    assert q.what_was_put.passed is True

def test_run_ftp_failure(mocker):
    statement = test_helpers.O()
    statement.protocol = 'ftp'
    statement.target = 'fakespeedtest.example.come'
    statement.should = 'should'
    statement.filename = '1KB.zip'
    statement.port = 21
    fft = FileFetchTest.FileFetchTest(statement)
    q = test_helpers.Q()
    fft.run(q)

    assert q.what_was_put.passed is False


def test_run_tftp_success(mocker):
    mocker.patch('tftpy.TftpClient.download')
    statement = test_helpers.O()
    statement.protocol = 'tftp'
    statement.target = 'tftp.example.com'
    statement.should = 'should'
    statement.filename = '1KB.zip'
    statement.port = 0
    fft = FileFetchTest.FileFetchTest(statement)
    q = test_helpers.Q()
    fft.run(q)

    assert q.what_was_put.passed is True

def test_run_tftp_failure(mocker):
    statement = test_helpers.O()
    statement.protocol = 'tftp'
    statement.target = 'example.com'
    statement.should = 'should'
    statement.filename = '1KB.zip'
    statement.port = 0
    fft = FileFetchTest.FileFetchTest(statement)
    q = test_helpers.Q()
    fft.run(q)

    assert q.what_was_put.passed is False

