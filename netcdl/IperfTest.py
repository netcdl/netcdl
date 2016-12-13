import re

from ActiveTest import ActiveTest
import DefineMap
import subprocess
import json

"""
Example Iperf3 Output: Client
{
        "start":        {
                "connected":    [{
                                "socket":       4,
                                "local_host":   "192.168.1.17",
                                "local_port":   33822,
                                "remote_host":  "192.168.1.144",
                                "remote_port":  5201
                        }],
                "version":      "iperf 3.0.7",
                "system_info":  "Linux mint 3.19.0-32-generic #37~14.04.1-Ubuntu SMP Thu Oct 22 09:41:40 UTC 2015 x86_64 x86_64 x86_64 GNU/Linux\n",
                "timestamp":    {
                        "time": "Tue, 09 Aug 2016 02:51:27 GMT",
                        "timesecs":     1470711087
                },
                "connecting_to":        {
                        "host": "ent.local",
                        "port": 5201
                },
                "cookie":       "mint.1470711087.808386.2d235a2012f71",
                "tcp_mss_default":      1448,
                "test_start":   {
                        "protocol":     "TCP",
                        "num_streams":  1,
                        "blksize":      131072,
                        "omit": 0,
                        "duration":     10,
                        "bytes":        0,
                        "blocks":       0,
                        "reverse":      0
                }
        },
        "end":  {
                "streams":      [{
                                "sender":       {
                                        "socket":       4,
                                        "start":        0,
                                        "end":  10.0001,
                                        "seconds":      10.0001,
                                        "bytes":        118899624,
                                        "bits_per_second":      9.5119e+07,
                                        "retransmits":  0
                                },
                                "receiver":     {
                                        "socket":       4,
                                        "start":        0,
                                        "end":  10.0001,
                                        "seconds":      10.0001,
                                        "bytes":        117886024,
                                        "bits_per_second":      9.43081e+07
                                }
                        }],
                "sum_sent":     {
                        "start":        0,
                        "end":  10.0001,
                        "seconds":      10.0001,
                        "bytes":        118899624,
                        "bits_per_second":      9.5119e+07,
                        "retransmits":  0
                },
                "sum_received": {
                        "start":        0,
                        "end":  10.0001,
                        "seconds":      10.0001,
                        "bytes":        117886024,
                        "bits_per_second":      9.43081e+07
                },
                "cpu_utilization_percent":      {
                        "host_total":   0.69204,
                        "host_user":    0.0793772,
                        "host_system":  0.635017,
                        "remote_total": 4.14278,
                        "remote_user":  0.474529,
                        "remote_system":        3.66381
                }
        }
}

"""


class IperfTest(ActiveTest):
    def __init__(self, statement):
        self.direction = statement.direction
        self.comparison = statement.comparison
        self.bitrate = IperfTest.parse_bitrate(statement.bitrate)
        self.bitrate_display = statement.bitrate
        self.server = DefineMap.lookup_host(statement.server)
        self.display_str = "iperf {0} {1} should be at {2} {3}".format(self.direction, self.server, self.comparison,
                                                                       self.bitrate_display)
        super(IperfTest, self).__init__(statement)

    # returns an integer representing bits per second
    @staticmethod
    def parse_bitrate(bitrate):
        multipliers = {'bps': 1, 'kbps': 1000, 'mbps': 1000000, 'gbps': 1000000000}
        # bitrate looks like number[bps|kbps|mbps|gbps]
        m = re.match('(\d+)(bps|kbps|mbps|gbps)', bitrate.lower())
        if m is None:
            raise Exception('Bad Iperf Bitrate')
        return int(m.group(1)) * multipliers[m.group(2)]

    def run(self, q):
        iperf_output = json.loads(subprocess.Popen("iperf3 -c {0} -f m -J -t 2".format(self.server), shell=True,
                                                   stdout=subprocess.PIPE).stdout.read())
        if iperf_output.get("error", False):
            # problem with iperf test
            self.success = False
            self.result_detail = iperf_output['error']
        else:
            self.upload_bandwidth = iperf_output['end']['streams'][0]['receiver']['bits_per_second']
            self.download_bandwidth = iperf_output['end']['streams'][0]['sender']['bits_per_second']
            self.compare_bandwidth()
        return q.put(self.create_result())

    def compare_bandwidth(self):
        if self.direction == 'download from':
            if self.comparison == 'least':
                self.success = self.bitrate < self.download_bandwidth
            else:
                self.success = self.bitrate > self.download_bandwidth
        else:
            if self.comparison == 'least':
                self.success = self.bitrate < self.upload_bandwidth
            else:
                self.success = self.bitrate > self.upload_bandwidth
