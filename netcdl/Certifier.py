__author__ = 'codyhanson'

import time
import logging

from DNSTest import DNSTest
from FileFetchTest import FileFetchTest
from LinkDuplexTest import LinkDuplexTest
from LinkSpeedTest import LinkSpeedTest
from PacketTypeTest import PacketTypeTest
from FrameTypeTest import FrameTypeTest
from PacketPortTest import PacketPortTest
from PacketFromTest import PacketFromTest
from PingTest import PingTest
from IperfTest import IperfTest
from ActiveTest import ActiveTest
from PortOpenTest import PortOpenTest
from TraceRouteTest import TraceRouteTest

import DefineMap
from LinkControl import LinkControl
from PacketCapture import PacketCapture
from Report import Report
from DHCPTest import DHCPTest
from multiprocessing import Queue


class Certifier:
    def __init__(self, document, iface):
        self.logger = logging.getLogger(__name__)
        self.document = document
        self.active_tests = list()
        self.link_tests = list()
        self.dhcp_tests = list()
        self.packet_tests = list()
        self.exit_code = 0
        self.report = Report()

        self.iface = iface

        self.link = LinkControl(self.iface)

        self.packet_queue = Queue()
        self.packet_capture = PacketCapture(iface, self.packet_queue)

        self.finished = False
        self.passed = False
        self.load_document(document)

    def load_document(self, document):
        for statement in document.statements:
            # TODO a better way of marshaling the types?
            type_name = type(statement).__name__
            if type_name == "HostDefineStatement":
                DefineMap.add_host(statement.name, statement.value)
            elif type_name == "NetworkDefineStatement":
                DefineMap.add_network(statement.name, statement.value)
            elif type_name == "LinkDuplexStatement":
                self.link_tests.append(LinkDuplexTest(statement, self.iface))
            elif type_name == "LinkSpeedStatement":
                self.link_tests.append(LinkSpeedTest(statement, self.iface))
            elif type_name == "PortOpenStatement":
                self.active_tests.append(PortOpenTest(statement))
            elif type_name == "IperfStatement":
                self.active_tests.append(IperfTest(statement))
            elif type_name == "PingStatement":
                self.active_tests.append(PingTest(statement))
            elif type_name == "TraceRouteStatement":
                self.active_tests.append(TraceRouteTest(statement))
            elif type_name == "FileFetchStatement":
                self.active_tests.append(FileFetchTest(statement))
            elif type_name == "DHCPStatement":
                self.dhcp_tests.append(DHCPTest(statement))
            elif type_name == "DNSStatement":
                self.active_tests.append(DNSTest(statement))
            elif type_name == "PacketFromStatement":
                self.packet_tests.append(PacketFromTest(statement))
            elif type_name == "PacketTypeStatement":
                self.packet_tests.append(PacketTypeTest(statement))
            elif type_name == "FrameTypeStatement":
                self.packet_tests.append(FrameTypeTest(statement))
            elif type_name == "PacketPortStatement":
                self.packet_tests.append(PacketPortTest(statement))

    def log_report(self):
        self.report.log()

    def run(self):

        # start packet capture
        self.packet_capture.start()

        # give the packet capture time to spin up
        time.sleep(2)

        # elicit DHCP responses
        self.link.dhcp()

        # make link assertions
        for test in self.link_tests:
            self.report.record_result(test.run())

        # perform active tests
        active_tests = []
        for test in self.active_tests:
            active_tests.append(test.start())

        # wait for active tests to complete
        num_active_results = 0
        while num_active_results < len(active_tests):
            self.report.record_result(ActiveTest.get_from_queue())
            num_active_results += 1
            print "{0} of {1} active tests finished".format(num_active_results, len(active_tests))
        for t in active_tests:
            t.join()
        print "Active Tests Joined"
        self.packets = self.packet_queue.get()
        self.packet_capture.end()

        # make dhcp assertions
        for test in self.dhcp_tests:
            self.report.record_result(test.run(self.packets))

        for test in self.packet_tests:
            self.report.record_result(test.run(self.packets))
