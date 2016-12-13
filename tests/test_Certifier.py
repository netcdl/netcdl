from textx.metamodel import metamodel_from_file
import test_helpers
import Certifier
import DefineMap


def test_ctor(mocker):
    mocker.patch('Certifier.Certifier.load_document')

    c = Certifier.Certifier('doc', 'eth1')
    assert c.document == 'doc'
    assert c.iface == 'eth1'
    assert len(c.active_tests) == 0
    assert len(c.link_tests) == 0
    assert len(c.dhcp_tests) == 0
    assert len(c.packet_tests) == 0
    c.load_document.assert_called()


def test_load_document(mocker):
    # It is easier just to read a real netcdl doc to excercise some of the logic in the file.
    netcdl_mm = metamodel_from_file('./netcdl/textx/netcdl.tx')
    netcdl_doc = netcdl_mm.model_from_file('./tests/example_netcdldoc_for_unittests.netcdl')

    c = Certifier.Certifier(netcdl_doc, 'eth1')

    assert len(c.active_tests) == 6
    assert len(c.link_tests) == 2
    assert len(c.dhcp_tests) == 1
    assert len(c.packet_tests) == 4
    assert len(DefineMap.hosts.keys()) == 1
    assert len(DefineMap.networks.keys()) == 1


def test_log(mocker):
    mocker.patch('Certifier.Certifier.load_document')
    c = Certifier.Certifier([], 'eth1')
    c.log_report()


def test_run(mocker):
    pass
