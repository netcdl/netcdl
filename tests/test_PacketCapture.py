import test_helpers
import PacketCapture
import scapy

import multiprocessing as mp


def test_ctor():
    q = test_helpers.Q()
    pc = PacketCapture.PacketCapture('eth1', q)

    assert pc.iface == 'eth1'
    assert len(pc.packets) == 0


def test_start(mocker):
    q = test_helpers.Q()
    fake_process = test_helpers.O()
    fake_process.start = lambda: 'run'
    mocker.patch('multiprocessing.Process')
    mp.Process.return_value = fake_process

    pc = PacketCapture.PacketCapture('eth1', q)

    res = pc.start()
    assert res == 'run'


def test_end(mocker):
    q = test_helpers.Q()
    fake_process = test_helpers.O()
    fake_process.join = lambda: 'joined'
    mocker.patch('multiprocessing.Process')
    mp.Process.return_value = fake_process

    pc = PacketCapture.PacketCapture('eth1', q)

    res = pc.end()
    assert res == 'joined'


def test_capture(mocker):
    q = test_helpers.Q()

    packets = test_helpers.O()
    packets.res = [1, 2]
    mocker.patch('scapy.all.sniff')
    mocker.patch('PacketCapture.PacketCapture.trim_packet')
    PacketCapture.PacketCapture.trim_packet.return_value = 'abc'
    scapy.all.sniff.return_value = packets

    pc = PacketCapture.PacketCapture('eth1', q)

    pc.capture(q)
    assert q.what_was_put[0] == 'abc'
    assert q.what_was_put[1] == 'abc'


def test_trim_packet(mocker):
    input_packet = test_helpers.O()
    input_packet.name = 'IP'
    input_packet.fields = 'IPfields'

    inner_packet = test_helpers.O()
    inner_packet.name = 'BOOTP'
    inner_packet.fields = 'innerfields'
    inner_packet.payload = test_helpers.O()
    inner_packet.payload.name = 'otherprotocol'

    input_packet.payload = inner_packet

    out = PacketCapture.PacketCapture.trim_packet(input_packet)

    assert out['fields'] == 'IPfields'
    assert out['name'] == 'IP'
    assert out['payload']['name'] == 'BOOTP'
    assert out['payload']['fields'] == 'innerfields'
    assert out['payload']['payload'] is None

def test_trim_packet_exception(mocker):
    assert PacketCapture.PacketCapture.trim_packet({}) is None



