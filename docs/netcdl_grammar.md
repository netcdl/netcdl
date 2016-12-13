#NETCDL Language Grammar
This file describes the NETCDL language with a Context Free Grammar

##Grammar

```
#Document Structure
<document> ::= <line> | <line> <document>
<line> ::= <definition> | <statement> | "\n" | "#..."
<statement> ::= <dhcp-statement> | <link-statement> | <packet-statement> | <connectivity-statement>

#Host and Network Defines
<definition> ::= "define" <definition-specifier> "as" <defined-name>
<definition-specifier> :: = "host" <IP-addr> | "network" <network-range>
<defined-name> ::= 'letters and numbers and underscores'
<IP-addr> :: = <ipv4> | <ipv6>
<network-range> ::= <ipv4-range> | <ipv6-range>
<network-entity> ::= <network-range> | <IP-addr> | <defined-name>


#DHCP Statements
<dhcp-statement> ::= "dhcp" "server" "should" <existence-expr> | <dhcp-dns-statement> | <dhcp-addr-range-statement> | <dhcp-addr-statement>
<dhcp-dns-statement> ::= "dhcp" "dns" "server" <should-expr> "be" <IP-addr>
<dhcp-address-statement> ::= "dhcp" "address" <should-expr> "be" <IP-addr>

#Links Statements
<link-statement> ::= "link" <should-expr> "be" <link-property>
<link-property> ::= <speed> | <duplex> | <power>
<duplex> ::= "full" "duplex" | "half" "duplex"
<speed> ::= "10Mb" | "100Mb" | "1000Mb" | "1Gb" | "gigabit"
<power> ::= <voltage> "poe"
<voltage> ::= "any" | "class" <poe-class>
<poe-class> ::= "0" | "1" | "2" | "3" | "4"

#Connectivity Statements
<connectivity-statement> ::= <network-entity> <should-expr> respond <response-expr>
<response-expr> ::= <to-protocol> | <on-port>
<to-protocol ::= to <protocol>
<protocol> ::= "http" | "ping" | "ssh" | "ftp"
<on-port> ::= "on" <transport> port <port-number>
<transport> ::= "tcp" | "udp"
<port-number ::= 0 - 65535


#Packet Statements
<packet-statement> ::= <packet-sighting-statement> 
<packet-sighting-statement> ::= <datagram-term> from <network-entity> <should-expr> be seen
<datagram-term> ::= "packets" | "frames" | "traffic"

#expressions
<should-expr> ::= "should" | "should" "not"
<existence-expr> ::= "exist" | "not" "exist"

```
