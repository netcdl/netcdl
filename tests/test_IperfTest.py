import test_helpers
import IperfTest
import pytest
import json
import subprocess


def test_ctor():
    statement = test_helpers.O()
    statement.direction = 'download from'
    statement.comparison = 'least'
    statement.bitrate = '100mbps'
    statement.server = '10.0.0.1'

    ipt = IperfTest.IperfTest(statement)

    assert ipt.direction == 'download from'
    assert ipt.bitrate == 100000000
    assert statement.server == '10.0.0.1'
    assert statement.comparison == 'least'


def test_parse_bitrate():
    assert IperfTest.IperfTest.parse_bitrate('100bps') == 100
    assert IperfTest.IperfTest.parse_bitrate('100kbps') == 100000
    assert IperfTest.IperfTest.parse_bitrate('100mbps') == 100000000
    assert IperfTest.IperfTest.parse_bitrate('100gbps') == 100000000000
    with pytest.raises(Exception):
        IperfTest.IperfTest.parse_bitrate('badstring')


def test_run_error(mocker):
    mocker.patch('json.loads')
    mocker.patch('subprocess.Popen')
    json.loads.return_value = {'error': 'it failed'}

    statement = test_helpers.O()
    statement.direction = 'download from'
    statement.comparison = 'least'
    statement.bitrate = '100mbps'
    statement.server = '10.0.0.1'

    q = test_helpers.Q()
    ipt = IperfTest.IperfTest(statement)
    ipt.run(q)
    assert q.what_was_put.passed is False


def test_run_success(mocker):
    mocker.patch('json.loads')
    mocker.patch('subprocess.Popen')
    json.loads.return_value = {
        'end': {'streams': [{'receiver': {'bits_per_second': 101}, 'sender': {'bits_per_second': 101}}]}}

    statement = test_helpers.O()
    statement.direction = 'download from'
    statement.comparison = 'least'
    statement.bitrate = '100bps'
    statement.server = '10.0.0.1'

    q = test_helpers.Q()
    ipt = IperfTest.IperfTest(statement)
    ipt.run(q)
    assert q.what_was_put.passed is True


def test_compare_bandwidth_downloadfrom_least():
    statement = test_helpers.O()
    statement.server = '10.0.0.1'
    statement.bitrate = '100bps'

    statement.direction = 'download from'
    statement.comparison = 'least'

    ipt = IperfTest.IperfTest(statement)

    ipt.download_bandwidth = 1000
    ipt.compare_bandwidth()
    assert ipt.success is True
    ipt.download_bandwidth = 10
    ipt.compare_bandwidth()
    assert ipt.success is False


def test_compare_bandwidth_downloadfrom_most():
    statement = test_helpers.O()
    statement.server = '10.0.0.1'
    statement.bitrate = '100bps'

    statement.direction = 'download from'
    statement.comparison = 'most'

    ipt = IperfTest.IperfTest(statement)

    ipt.download_bandwidth = 1000
    ipt.compare_bandwidth()
    assert ipt.success is False
    ipt.download_bandwidth = 10
    ipt.compare_bandwidth()
    assert ipt.success is True


def test_compare_bandwidth_uploadto_least():
    statement = test_helpers.O()
    statement.server = '10.0.0.1'
    statement.bitrate = '100bps'

    statement.direction = 'upload to'
    statement.comparison = 'least'

    ipt = IperfTest.IperfTest(statement)

    ipt.upload_bandwidth = 1000
    ipt.compare_bandwidth()
    assert ipt.success is True
    ipt.upload_bandwidth = 10
    ipt.compare_bandwidth()
    assert ipt.success is False


def test_compare_bandwidth_uploadto_most():
    statement = test_helpers.O()
    statement.server = '10.0.0.1'
    statement.bitrate = '100bps'

    statement.direction = 'upload to'
    statement.comparison = 'most'

    ipt = IperfTest.IperfTest(statement)

    ipt.upload_bandwidth = 1000
    ipt.compare_bandwidth()
    assert ipt.success is False
    ipt.upload_bandwidth = 10
    ipt.compare_bandwidth()
    assert ipt.success is True
