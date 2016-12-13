#Targeted Use Cases for NETCDL v1.0

##Key Tests and behaviors to verify
- Power Over ethernet voltage
- Opening TCP ports
- Opening UDP ports
- doing an HTTP Get to a web server
- Resolving a name with a DNS server
- asserting link speed
- asserting link duplex
- asserting correct VLAN id
- verifying DHCP operation
    - verify dhcp server addr
    - verify ip addr that is handed out, in the right network
    - verify that dns server is correct
- Pinging an IP address.
- Traceroute, ensure that it looks correct, as expected. (order of hops)
- Packet/frame capturing
    - verify source IP address should/should not be seen
    - verify traffic to a destination UDP port should/should not be seen
    - verify traffic from a destination UDP port should/should not be seen
    - verify traffic to a destination TCP port should/should not be seen
    - verify traffic from a destination TCP port should/should not be seen
    - verify ethertype seen/not seen
        - https://en.wikipedia.org/wiki/EtherType
    - verify ip protocol header value seen/not seen
        - https://en.wikipedia.org/wiki/List_of_IP_protocol_numbers 

##Meta features

- comments with # sign
- 'negations' for certain statements (server should not be reachable on port 80)
- named aliases for hostnames and network address ranges.

