---
layout: doc
title: "Reconnaissance & Nmap for Beginners"
description: "Learn authorized reconnaissance: passive OSINT, DNS enumeration, host discovery, port scanning with Nmap, and how to document findings without overstepping scope."
permalink: /docs/reconnaissance/
eyebrow: "Documentation"
last_modified: 2026-11-14
---

## Reconnaissance is information gathering, not attacking

Reconnaissance answers three questions:

1. What exists?
2. What is exposed?
3. What is worth investigating next?

It does not prove a vulnerability. A port scan shows that a service is reachable; it does not show that the service is exploitable. Keep those claims separate in your notes.

<div class="notice notice-legal"><p><strong>Authorization check.</strong> Active scanning sends packets to the target and can be logged, rate-limited or treated as hostile. Scan only lab VMs or systems covered by written permission. Passive research can still violate privacy or platform policy if you collect personal data.</p></div>

## Passive reconnaissance

Passive work uses public information without touching the target directly.

| Source | What it can reveal | Caution |
| --- | --- | --- |
| Search engines | Public pages, documents, job posts | Do not collect personal data without a reason |
| WHOIS | Registrar, dates, sometimes contacts | Redacted for privacy; do not scrape personal records |
| DNS records | Mail servers, verification tokens, subdomains | Public DNS is not automatically fair game for mass enumeration |
| Certificate transparency | Historical subdomains | Can reveal internal naming conventions |
| Technology fingerprints | CMS, frameworks, headers | Public pages only |
| Job listings | Technology stack and team structure | Avoid social engineering |

A simple, authorized lookup:

```bash
whois example.com
dig example.com NS
dig example.com MX
```

`whois` output varies by registry and is often redacted. Do not assume a missing contact means the domain is abandoned.

## DNS enumeration

DNS enumeration discovers names that point at the same organization. The course covers `dig`, `nslookup`, `dnsenum`, `dnsmap` and `dnstracer`.

```bash
dig example.com ANY
dig +short example.com
dig @1.1.1.1 example.com A
```

`ANY` queries are often refused or minimized by modern DNS servers. Use specific record types instead.

### dnsenum

```bash
dnsenum example.com
```

`dnsenum` combines record lookups, zone transfer attempts and subdomain brute force. A zone transfer (`AXFR`) should fail on a correctly configured server. If it succeeds, that is a configuration finding, not a vulnerability you should exploit beyond documentation.

### dnsmap

```bash
dnsmap example.com -w /usr/share/wordlists/dnsmap.txt
```

`dnsmap` tests a wordlist against a domain. Wordlist-based enumeration can generate a lot of traffic. Run it only against your lab domain or an authorized target, and rate-limit if the tool supports it.

### dnstracer

```bash
dnstracer example.com
```

`dnstracer` follows the delegation chain from the root to the authoritative server. It is useful for understanding DNS architecture, not for finding vulnerabilities by itself.

## Host discovery

Before scanning ports, find live hosts:

```bash
nmap -sn 192.168.56.0/24
```

`-sn` performs host discovery and skips port scanning. In a lab, it quickly shows which VMs are up. On a network with strict filtering, hosts may appear down even when they are up; `-Pn` skips discovery but assumes every target is alive, which is slower and noisier.

```bash
nmap -sn 192.168.56.0/24 -oA lab-discovery
```

`-oA` writes normal, XML and grepable output. Keep the XML if you want to parse results later.

## Port scanning

The course covers connect, SYN, UDP, ACK, FIN, Xmas, version detection and the NSE scripting engine.

### TCP connect scan

```bash
nmap -sT 192.168.56.10
```

A full TCP handshake per port. It works without root and is easy to detect. Good for understanding the mechanics.

### SYN scan

```bash
sudo nmap -sS 192.168.56.10
```

Sends SYN and evaluates SYN-ACK, RST or no response without completing the handshake. Requires raw sockets and elevated privileges. Often called a "half-open" scan.

### UDP scan

```bash
sudo nmap -sU --top-ports 20 192.168.56.10
```

Slow and ambiguous. UDP services may not reply at all. Use a small port list and expect false negatives.

### Service and version detection

```bash
nmap -sV -p 22,80,443 192.168.56.10
nmap -sV --version-intensity 5 192.168.56.10
```

`-sV` probes open ports to identify the service and version. The result is a fingerprint, not proof. A banner can be spoofed or generic.

### Default scripts

```bash
nmap -sC -sV -p 80,443 192.168.56.10
```

`-sC` runs the default NSE script set. Scripts can be intrusive. Read what a script does before running it against anything you do not own.

### Aggressive scan

```bash
sudo nmap -A 192.168.56.10
```

`-A` enables OS detection, version detection, script scanning and traceroute. It is noisy and can take a long time. In a lab it is convenient; on a real engagement it needs explicit approval.

### Port ranges and timing

```bash
nmap -p 1-1000 192.168.56.10
nmap -p- --min-rate 500 192.168.56.10
nmap -T3 192.168.56.10
```

`-p-` scans all 65,535 TCP ports and can take a long time. `--min-rate` increases speed at the cost of accuracy and stealth. `-T4` is common in labs; `-T5` can miss results on lossy networks. Never use aggressive timing on a network you do not own.

## Reading Nmap output

Typical states:

| State | Meaning |
| --- | --- |
| `open` | A service accepted the probe |
| `closed` | The host responded but no service is listening |
| `filtered` | A firewall or filter prevented a definite answer |
| `unfiltered` | Reachable, but open/closed could not be determined |
| `open|filtered` | Ambiguous, common with UDP and some scan types |

An `open` port is an exposure, not a vulnerability. The next step is to identify the service, version and configuration, then compare it with known issues — in a lab.

## Documenting a scan

For every scan, record:

- Date and time, including timezone.
- Source interface and IP.
- Target scope and authorization reference.
- Exact command.
- Output file name.
- Key findings and uncertainty.
- Follow-up actions.

Nmap output changes. A screenshot is not evidence; keep the raw output file and the command.

## Common mistakes

| Mistake | Consequence |
| --- | --- |
| Scanning the home LAN by accident | Unauthorized traffic to real devices |
| Treating an open port as a vulnerability | False findings and bad reports |
| Using `-T5` or `--min-rate` on a shared network | Packet loss, alerts, service disruption |
| Running NSE scripts without reading them | Unintended exploitation or crashes |
| Skipping `ip route` | Scanning outside the lab |
| Not saving output | Findings cannot be reproduced |

## Practice exercises

1. Discover live hosts on your lab subnet with `-sn`.
2. Compare `-sT` and `-sS` against the same lab target and explain the difference.
3. Scan the top 100 ports and save all output formats.
4. Identify one service with `-sV` and find its official documentation.
5. Explain why a `filtered` result is not the same as `closed`.
6. Write a one-page recon report for your lab target with no vulnerability claims.

## Next steps

- Interpret results in [Vulnerability analysis]({{ '/docs/vulnerability-analysis/' | relative_url }}).
- Review the recon chapters starting at [Chapter 32]({{ '/lessons/lesson-032/' | relative_url }}).
- Confirm scope with the [lab checklist]({{ '/resources/lab-checklist/' | relative_url }}).
