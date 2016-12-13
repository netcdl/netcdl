from ActiveTest import ActiveTest
from ftplib import FTP
import requests
import tftpy
import DefineMap


class FileFetchTest(ActiveTest):
    def __init__(self, statement):
        self.protocol = statement.protocol
        self.target = str(DefineMap.lookup_host(statement.target))
        self.should_pass = statement.should == 'should'
        self.filename = str(statement.filename)
        self.port = FileFetchTest.parse_port(self.protocol, statement.port)
        self.display_string = ""
        should_pass_str = "should" if self.should_pass else "should not"
        self.display_str = "{0} server at {1} {2} serve {3} on port {4}".format(self.protocol, self.target,
                                                                                should_pass_str, self.filename,
                                                                                self.port)
        super(FileFetchTest, self).__init__(statement)

    @staticmethod
    def parse_port(protocol, port):
        default_ports = {'http': 80, 'ftp': 21, 'tftp': 69}
        if port == 0:  # no port specified
            return default_ports[protocol]
        else:
            return port

    def run(self, q):

        if self.protocol == 'http':
            self.http_test()
        elif self.protocol == 'tftp':
            self.tftp_test()
        elif self.protocol == 'ftp':
            self.ftp_test()
        return q.put(self.create_result())

    def http_test(self):
        target_url = "http://{0}:{1}{2}".format(self.target, self.port, self.filename)
        try:
            r = requests.get(target_url, timeout=5)
            if r.status_code == 200 and self.should_pass:
                self.success = True
        except:
            self.success = not self.should_pass

    def tftp_test(self):
        try:
            client = tftpy.TftpClient(self.target, self.port)
            res = client.download(self.filename, 'tftpout', timeout=3)
            self.success = self.should_pass
        except:
            self.success = not self.should_pass

    def ftp_test(self):
        try:
            ftp = FTP(self.target)  # connect to host, default port
            ftp.login()
            ftp.retrbinary('RETR {0}'.format(self.filename), open('/tmp/{0}'.format(self.filename), 'wb').write)
            self.success = self.should_pass
        except:
            self.success = not self.should_pass
