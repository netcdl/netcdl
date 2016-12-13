netcdl
======
The Network Certification Description Language - Reference Implementation.

Prototype software that implements a [NETCDL](http://netcdl.org) certifier.

This initial work was part of the Master's thesis by @codyhanson.

##Requirements to run:
- python2.7
- Linux system (tested with Ubuntu/Mint)
- iperf3 client installed

##Installation and running tests
```
pip install -r requirements.txt
(sudo) make test
```

##Running a certification

See [netcdl.org](http://netcdl.org) for more information on the NETCDL Language

##Permissions required to run
Because of the low level packet manipulation that the Scapy library does,
NETCDL requires super user privileges to run.
