---
layout: doc
title: "Networking Basics for Ethical Hackers"
description: "Understand IP addresses, ports, TCP and UDP, DNS, HTTP, NAT, proxies, VPNs and Tor — the network concepts behind every Kali Linux chapter."
permalink: /docs/networking-basics/
eyebrow: "Documentation"
last_modified: 2026-11-14
---

## Why networking comes before scanning

A scanner is only useful if you can interpret what it finds. An open port is not automatically a vulnerability. A DNS record is not automatically a subdomain takeover. A proxy is not automatically anonymity. This guide covers the mental model you need before Chapter 20.

## Addresses and subnets

An IPv4 address is 32 bits, written as four octets, for example `192.168.56.10`. A subnet mask decides which part identifies the network and which part identifies the host. CIDR notation combines the address and mask:

| CIDR | Mask | Addresses | Typical use |
| --- | --- | --- | --- |
| `/32` | 255.255.255.255 | 1 | A single host route |
| `/24` | 255.255.255.0 | 256 | A small lab network |
| `/16` | 255.255.0.0 | 65,536 | A large private network |
| `/8` | 255.0.0.0 | 16,777,216 | Very large networks |

Private IPv4 ranges are defined by RFC 1918:

- `10.0.0.0/8`
- `172.16.0.0/12`
- `192.168.0.0/16`

Loopback is `127.0.0.0/8`. Link-local is `169.254.0.0/16`; an address in that range often means DHCP failed.

IPv6 addresses are 128 bits. `::1` is loopback and `fe80::/10` is link-local. Many tools support IPv6, but most beginner labs use IPv4.

### Inspect your interfaces

```bash
ip address
ip route
ip neigh
```

`ip route` is the most important command before a scan. It tells you which interface will be used for a destination. If the target is on your home LAN instead of the lab network, stop.

## Ports and protocols

A port identifies a service on a host. The first 1024 ports are "well known" and usually require elevated privileges to bind.

| Port | Service | Notes |
| --- | --- | --- |
| 22 | SSH | Encrypted remote shell |
| 25 | SMTP | Mail transfer |
| 53 | DNS | Name resolution, TCP and UDP |
| 80 | HTTP | Plain web traffic |
| 123 | NTP | Time sync; important for TLS and logs |
| 443 | HTTPS | HTTP over TLS |
| 445 | SMB | Windows file sharing |
| 3306 | MySQL | Database |
| 3389 | RDP | Remote Desktop |
| 8080 | HTTP proxy / alternate web | Common development port |

### TCP versus UDP

TCP is connection-oriented: it performs a handshake (SYN, SYN-ACK, ACK), retransmits lost data and provides ordered delivery. UDP is connectionless: it sends datagrams without a handshake and is used by DNS, DHCP, VoIP and many VPNs.

This difference shapes scanning. A TCP connect scan completes the handshake; a SYN scan sends SYN and evaluates the response without completing it. UDP scans are slow and ambiguous because a lack of response can mean "closed", "filtered" or "packet lost".

## DNS

DNS maps names to records:

| Record | Meaning |
| --- | --- |
| `A` | IPv4 address |
| `AAAA` | IPv6 address |
| `CNAME` | Alias to another name |
| `MX` | Mail server |
| `NS` | Authoritative name server |
| `TXT` | Arbitrary text, often verification or policy |
| `SOA` | Zone authority information |
| `PTR` | Reverse lookup |

```bash
dig example.com A
dig example.com MX
dig +short example.com
nslookup example.com
```

Use only domains you own or are authorized to enumerate. Querying public DNS is generally low risk, but automated enumeration of a third party's infrastructure can violate policy even when it is technically "passive".

## HTTP in one page

An HTTP request has a method, a path, headers and an optional body:

```http
GET /login HTTP/1.1
Host: lab.example
User-Agent: Mozilla/5.0
Accept: text/html
```

A response has a status code, headers and a body:

```http
HTTP/1.1 200 OK
Content-Type: text/html
Set-Cookie: session=abc123; HttpOnly; Secure
```

Status families:

- `2xx` success
- `3xx` redirect
- `4xx` client error (401 unauthenticated, 403 forbidden, 404 not found)
- `5xx` server error

Useful commands:

```bash
curl -I https://example.com
curl -v https://example.com
```

`curl -I` sends a HEAD request and prints headers. `-v` shows the TLS and HTTP conversation. Never send credentials to a system you do not control.

## NAT, routing and the lab boundary

Network Address Translation lets many private addresses share one public address. Your home router performs NAT. A virtual machine on NAT can reach the internet, but inbound connections are blocked unless you explicitly forward a port.

For a lab:

- NAT is convenient for updates.
- Host-only or internal networking isolates the practice network.
- Bridged networking exposes the VM to your real LAN and should be avoided for offensive testing.

Check the boundary:

```bash
ip route get 192.168.56.10
traceroute -n 192.168.56.10
```

If the route leaves through your Wi-Fi adapter, the target is not isolated.

## Proxy, VPN and Tor are not the same

| Technology | What it hides | What it does not hide | Typical use |
| --- | --- | --- | --- |
| HTTP proxy | Your source IP from the destination, for proxied traffic | DNS leaks, browser fingerprints, the proxy operator | Web debugging, corporate egress |
| VPN | Traffic between you and the VPN server | The VPN provider, destinations you authenticate to | Remote access, trusted network extension |
| Tor | Source and destination from each other, via three relays | Correlation by a global adversary, your own logins | Anonymity research, censorship circumvention |

All three can leak. A proxy misconfigured for DNS still reveals the domains you visit. A VPN does not make you anonymous to the websites where you log in. Tor does not protect you if you sign into a personal account or install a tracking extension.

<div class="notice notice-warning"><p><strong>Anonymity is not a get-out-of-jail card.</strong> Using Tor does not make unauthorized access legal. Authorization comes from the system owner, not from your routing path.</p></div>

## MAC addresses and ARP

A MAC address is a link-layer identifier assigned to a network interface. ARP resolves an IPv4 address to a MAC address on the local network. ARP has no authentication, which is why ARP spoofing exists. That is a local-network attack and belongs in an isolated lab.

```bash
ip link show
ip neigh
```

Changing your MAC address may be useful for privacy on a network you own. It does not hide you from the switch, the router or the ISP, and it can break DHCP leases.

## Capture traffic responsibly

```bash
sudo tcpdump -i eth0 -c 20
sudo tcpdump -i eth0 port 53 -w dns.pcap
```

Packet capture records other people's traffic if the interface sees it. On a shared network, that can violate privacy law. Capture only your own lab traffic or traffic you are authorized to inspect.

## Practice exercises

1. Draw your lab network: host, Kali, target, virtual switch and the route to the internet.
2. Run `ip route` and explain which interface reaches the lab target.
3. Use `dig` to query an A, MX and TXT record for a domain you own.
4. Capture five DNS packets in your lab and identify the query and response.
5. Explain why a VPN does not make you anonymous to a website where you log in.
6. List three signs that a VM is not isolated from your home LAN.

## Next steps

- Apply the model in [Reconnaissance]({{ '/docs/reconnaissance/' | relative_url }}).
- Review the networking chapters starting at [Chapter 20]({{ '/lessons/lesson-020/' | relative_url }}).
- Keep the [lab checklist]({{ '/resources/lab-checklist/' | relative_url }}) next to you.
