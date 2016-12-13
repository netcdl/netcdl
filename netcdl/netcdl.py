#! /usr/bin/env python
"""netcdl.

Usage:
netcdl.py <specfile>...
netcdl.py [--interface=<iface>] <specfile>...
netcdl.py (-h | --help)
Options:
-h --help       Show this screen.
-i --interface=<iface>  Name of the network interface to run certification out
-s --spec       Path to the specification file to evaluate.
-d --debug      Enable debug logging.
"""

__author__ = 'Cody Hanson <chanson@uwalumni.com>'
__version__ = 'alpha'

from textx.exceptions import TextXSyntaxError
from textx.metamodel import metamodel_from_file
import sys
import time

import Certifier

import os
dir = os.path.dirname(__file__)
netcdl_definition_filename = os.path.join(dir, 'textx/netcdl.tx')


# PyPi libs
from docopt import docopt


def main(args):
    netcdl_mm = metamodel_from_file(netcdl_definition_filename)
    begin = time.time()
    print_logo()
    try:
        netcdl_doc = netcdl_mm.model_from_file(args['<specfile>'][0])
    except TextXSyntaxError as e:
        print "exception: {0}".format(e)
        return

    certifier = Certifier.Certifier(netcdl_doc, args.get('--interface', 'eth0'))
    certifier.run()

    # Certification work is now completed, or failed.
    certifier.log_report()
    end = time.time()
    print "Certification complete in about {0} seconds".format(int(end - begin))
    sys.exit(certifier.exit_code)


def print_logo():
    print """
    #     # ####### #######  #####  ######  #
    ##    # #          #    #     # #     # #
    # #   # #          #    #       #     # #
    #  #  # #####      #    #       #     # #
    #   # # #          #    #       #     # #
    #    ## #          #    #     # #     # #
    #     # #######    #     #####  ######  #######
    """


if __name__ == '__main__':
    arguments = docopt(__doc__, version='netcdl 0.0.1')
    main(arguments)
