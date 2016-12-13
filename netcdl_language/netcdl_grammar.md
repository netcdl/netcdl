#NETCDL Language Grammar
This file describes the NETCDL language with a Context Free Grammar in Extended Backus-Naur Form

##Grammar

```
#Document Structure
<document> ::= <line> | <line> <document>
<line> ::= <definition> | <statement> | <blank-line> | <comment>
<comment> ::= <whitespace> "#.*"
<whitespace> ::= " " <whitespace> | "\t" <whitespace> | ""
<blank-line> ::= <whitespace> "\n"
<nonwhitespace> :: = <nonwhitespace><nonwhitespace> | "a-z" | "A-Z" | ".~!@$%^&*()_-"
<statement> ::= <dhcp-statement> | <link-statement> | <packet-statement> | <port-open-statement> |
               <ping-statement> | <traceroute-statement> | <vlan-statement> | <dns-statement> | 
               <iperf-statement> | <file-fetch-statement>

#Host and Network Defines
<definition> ::= "define" <definition-type>  <nonwhitespace> "as" <nonwhitespace>
<definition-type> :: = "host" | "network" 

#DHCP Statements
<dhcp-statement> ::= "dhcp" "server" "should" <existence-expr> | <dhcp-dns-statement> | <dhcp-addr-range-statement> | <dhcp-addr-statement>
<dhcp-dns-statement> ::= "dhcp" "dns" "server" <should-expr> "be" <IP-addr>
<dhcp-address-statement> ::= "dhcp" "address" <should-expr> "be" <IP-addr>

#Link Statements
<link-statement> ::= <link-speed> | <link-duplex> 
<link-speed> ::= "link speed" <should-expr> "be" <speed>
<link-speed> ::= "link duplex" <should-expr> "be" <duplex>
<duplex> ::= "full" | "half"
<speed> ::= "10Mb" | "100Mb" | "1000Mb" | "1Gb" | "gigabit"

<port-open-statement> <reachable> "on" <transport> "port" <port-number>

<ping-statement> ::= <reachable> "by ping"

<traceroute-statement> ::= "traceroute to" <nonwhitespace> "should traverse [" <routers> "]"
<routers> ::= <routers><nonwhitespace> | ""

<vlan-statement> ::= "access vlan" <should-expr> "be" <integer>

<dns-statement> ::= "domain name" <nonwhitespace> <should-expr>  "resolve" <resolve-target> "using server" <nonwhitespace>
<resolve-target> ::= "" | "to" <nonwhitespace>

<file-fetch-statement> ::= <fetch-protocol> "server at" <nonwhitespace> <should-expr> "serve" <nonwhitespace> <fetch-port>
<fetch-port> ::= "" | "on port" <port-number>
<fetch-protocol> ::= "http" | "tftp" | "ftp"
<on-port> ::= "on" <transport> port <port-number>
<transport> ::= "tcp" | "udp"
<port-number> ::= 0 - 65535


#iperf statement
<iperf-statement> ::= "iperf" <iperf-direction> <nonwhitespace> 'should be at' <iperf-comparison> <nonwhitespace>
<iperf-direction> ::= "upload to" | "download from"
<iperf-comparison ::= "most" | "least"


#Packet Statements
<packet-statement> ::= <packet-from-statement> | <packet-port-statement> | <packet-type-statement> | <frame-type-statement>
<packet-from-statement> ::= "packets from" <packet-from-type> <nonwhitespace> <should-expr> "be seen"
<packet-from-type> ::= "host" | "network"
<packet-port-statement> ::= "packets with" <protocol> <packet-direction> "port" <port-number> <should-expr> "be seen" 
<packet-type-statement> ::= "packets with type" <packet-from-type> <nonwhitespace> <should-expr> "be seen"
<frame-type-statement> ::= "frames with ethertype" <nonwhitespace> <should-expr> "be seen"

#expressions
<should-expr> ::= "should" | "should not"
<reachable> ::= <nonwhitespace> <should-expr> "be reachable"

#primitives
<integer> ::= 0|1|2|3|4|5|6|8|9|0|<integer><integer>
```

