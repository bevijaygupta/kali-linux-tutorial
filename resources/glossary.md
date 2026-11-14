---
layout: page
hide_title: true
title: "Cybersecurity & Kali Linux Glossary for Beginners"
description: "Plain-language definitions of the networking, Linux and security terms used in the Kali Linux course, from ARP and hashes to XSS and zero-day."
permalink: /resources/glossary/
section: "Resources"
section_url: "/resources/"
last_modified: 2026-11-14
---

# Glossary

Security writing is full of shorthand. This glossary explains the terms used across the course in plain language. Definitions are deliberately short; follow the links to the relevant guide for context.

<div class="notice notice-legal"><p><strong>Authorized use only.</strong> Understanding an attack technique is not permission to use it. Practise only on systems you own or have explicit written authorization to test.</p></div>

## A–C

**Access control** — The rules that decide who can read, change or use a resource. Authentication proves identity; authorization decides what that identity may do.

**ARP (Address Resolution Protocol)** — The protocol that maps an IPv4 address to a MAC address on a local network. ARP has no built-in authentication, which is why ARP spoofing is possible on a local segment.

**Attack surface** — Everything an attacker can interact with: exposed services, input fields, APIs, accounts, physical access and people. Reducing the attack surface is a core defensive goal.

**Authentication** — Proving an identity, usually with a password, key, certificate or second factor. It answers "who are you?".

**Authorization** — Permission to perform an action. In security testing it also means the written approval that defines what you may test. The two meanings are related but distinct.

**Banner grabbing** — Collecting the identifying text a service returns when connected to, such as a server version. Banners can help fingerprint a service but may be inaccurate or deliberately misleading.

**BSSID (Basic Service Set Identifier)** — The MAC address of a wireless access point's radio. It identifies the specific access point, while the SSID is the network name.

**Buffer overflow** — A bug where a program writes more data into a memory buffer than it can hold, potentially overwriting adjacent memory. Exploiting it can crash a process or change its control flow.

**CIA triad** — Confidentiality, integrity and availability: the three broad goals used to describe information security.

**CVE (Common Vulnerabilities and Exposures)** — A public identifier for a specific vulnerability, maintained through the CVE Program. A CVE entry is not the same as a CVSS score or a working exploit.

**CVSS (Common Vulnerability Scoring System)** — A specification for describing vulnerability severity. A score is only one input to risk; context and exploitability matter.

**Credential stuffing** — Trying username/password pairs leaked from one service against another, exploiting password reuse. It is an online attack and can trigger account lockouts.

## D–F

**DHCP (Dynamic Host Configuration Protocol)** — Automatically assigns IP addresses and network settings to hosts. Rogue DHCP servers can misconfigure or redirect clients.

**DNS (Domain Name System)** — Translates names such as `example.com` into IP addresses and other records. DNS enumeration discovers names, mail servers, name servers and related infrastructure.

**DNS enumeration** — Systematically discovering DNS records and subdomains. It is a reconnaissance activity and should respect the target's scope and rate limits.

**Domain** — A named part of the DNS hierarchy, such as `example.com`. Do not confuse it with a Windows Active Directory domain, which is a different concept.

**Exploit** — Code or a technique that takes advantage of a vulnerability to produce an unintended effect, such as executing code or reading protected data.

**Exploit-DB** — A public archive of exploits and proof-of-concept code. SearchSploit provides an offline copy in Kali.

**Firewall** — A control that filters network traffic according to rules. A firewall reduces exposure but does not fix a vulnerable application that is allowed through.

**Footprinting** — Collecting information about an organization and its systems before testing: domains, IP ranges, technologies, public documents and people. Also called reconnaissance or information gathering.

## G–L

**Hash** — A fixed-length value produced by a hash function from input data. Hashes are used for integrity checks and password storage. A hash is not encryption because it is not designed to be reversed.

**Hash function** — A one-way function that maps data of any size to a fixed-size output. Good password hashing uses a slow, salted algorithm such as Argon2, bcrypt or scrypt.

**Honeypot** — A decoy system or service designed to attract and observe unauthorized activity. Honeypots can provide early warning but add operational and legal complexity.

**HTTP (Hypertext Transfer Protocol)** — The application protocol used by the web. HTTP is stateless; cookies and tokens carry state between requests.

**HTTPS** — HTTP protected by TLS. It encrypts traffic in transit but does not make an application secure by itself.

**IP address** — A numeric address used to route packets on a network. IPv4 addresses are 32-bit; IPv6 addresses are 128-bit.

**Kali Linux** — A Debian-based distribution maintained by OffSec that bundles security tools for authorized testing, forensics and research. It is not a magic hacking system and is not intended as a daily-driver OS.

**LAN (Local Area Network)** — A network covering a limited area, such as a home or lab. Most ARP and local discovery activity happens on a LAN.

**Least privilege** — The principle that a user, process or service should have only the permissions needed for its task. It limits the damage from mistakes and compromise.

## M–P

**MAC address** — A hardware address assigned to a network interface, usually 48 bits. It is used on the local link, not for end-to-end internet routing, and can often be changed in software.

**Metasploit Framework** — A modular exploitation and testing framework. It provides modules, payloads, encoders and session management, usually through `msfconsole`.

**MITM (Man-in-the-middle)** — A position where an attacker can observe or alter traffic between two parties. ARP spoofing is one way to attempt this on a local network.

**Monitor mode** — A wireless interface mode that captures 802.11 frames without associating to a network. It requires compatible hardware and authorization.

**NAT (Network Address Translation)** — Rewrites addresses as traffic crosses a router. Home networks commonly use NAT to share one public IPv4 address.

**Nmap** — A network discovery and port-scanning tool. It can identify hosts, open ports, service versions and, with NSE, additional information.

**Offline attack** — Password guessing performed against captured or extracted hashes without contacting the authentication service. It does not trigger account lockouts but still requires authorization.

**Online attack** — Password guessing against a live authentication service, such as SSH or a web login. It can lock accounts, generate alerts and is easy to detect.

**OSINT (Open Source Intelligence)** — Information gathered from publicly available sources. It includes websites, public records, social media and technical data, but does not include unauthorized access.

**Packet** — A unit of data carried on a network. Capturing packets is useful for troubleshooting and analysis, but can expose sensitive information.

**Payload** — The part of an exploit that runs after a vulnerability is triggered, such as a shell or a command. Payload choice affects reliability, detection and impact.

**Penetration test** — An authorized assessment that attempts to find and demonstrate security weaknesses, usually within a defined scope and rules of engagement.

**Port** — A numeric identifier for a service endpoint on a host. Common examples are 22 (SSH), 80 (HTTP) and 443 (HTTPS).

**Privilege escalation** — Gaining a higher level of access than initially available, such as moving from a normal user to root or administrator.

**Proxy** — An intermediary that forwards requests. A proxy can hide the client's address from the destination, but it does not provide authorization or guarantee anonymity.

## R–S

**Rainbow table** — A precomputed table for reversing hashes. Salting and slow password hashing make rainbow tables much less effective.

**Reconnaissance** — The information-gathering phase of a test. It can be passive (public sources) or active (sending traffic to a target), and active work must stay in scope.

**Reverse shell** — A shell where the target connects back to the tester's listener. It is often used after exploitation, but is a high-impact action that requires explicit authorization.

**Root** — The superuser account on Linux with unrestricted permissions. Working as root all the time increases the impact of mistakes.

**Salt** — Random data added to a password before hashing so identical passwords produce different hashes and precomputed attacks are harder.

**Scope** — The defined boundary of an authorized test: systems, addresses, applications, techniques, time window and exclusions.

**SearchSploit** — A command-line interface to a local copy of Exploit-DB, used to search for public exploits and papers.

**Shell** — A command interpreter. A "shell" can also mean an interactive session on a compromised host, which is why context matters.

**Sniffing** — Capturing network traffic. On switched networks, visibility is limited unless the tester controls a tap, span port or an authorized interception position.

**Spoofing** — Falsifying an identity or address, such as an IP address, MAC address or DNS response. Spoofing can disrupt services and is illegal without authorization.

**SQL injection (SQLi)** — A vulnerability where untrusted input changes the structure of a database query. It can lead to data disclosure, modification or authentication bypass.

**SSID (Service Set Identifier)** — The name of a wireless network. It is not a security control and can be hidden or duplicated.

## T–Z

**TCP (Transmission Control Protocol)** — A connection-oriented transport protocol that provides ordered, reliable delivery. Many service scans target TCP ports.

**Tor** — An anonymity network that routes traffic through multiple relays. It reduces the chance that one relay knows both who you are and where you are going, but it does not make an action lawful or risk-free.

**UDP (User Datagram Protocol)** — A connectionless transport protocol with no delivery guarantee. DNS, DHCP and many real-time services use UDP.

**VPN (Virtual Private Network)** — An encrypted tunnel between a client and a VPN server. It protects traffic on untrusted networks and changes the apparent source address, but it is not the same as Tor and does not provide authorization.

**Vulnerability** — A weakness that can be exploited to affect confidentiality, integrity or availability. Not every weakness is exploitable in every context.

**WEP (Wired Equivalent Privacy)** — An obsolete wireless encryption protocol with fundamental design flaws. It should not be used for protection.

**WPA/WPA2/WPA3** — Successive Wi-Fi security standards. WPA2 and WPA3 are the relevant modern options; configuration and passphrase strength still matter.

**Wordlist** — A list of candidate passwords, usernames or paths used in testing. A targeted wordlist is often more effective than a huge generic one.

**XSS (Cross-site scripting)** — A vulnerability where attacker-controlled script runs in another user's browser in the context of a trusted site. It can steal sessions, modify pages or perform actions as the victim.

**Zero-day** — A vulnerability with no vendor fix available at the time of discovery. The term describes the fix status, not the severity.

## Related resources

- [Kali Linux command cheat sheet]({{ '/resources/cheat-sheet/' | relative_url }})
- [Networking basics]({{ '/docs/networking-basics/' | relative_url }})
- [Web application security]({{ '/docs/web-application-security/' | relative_url }})
- [Lab checklist]({{ '/resources/lab-checklist/' | relative_url }})
- [Official links]({{ '/resources/official-links/' | relative_url }})

## FAQ

### Is a hash the same as encryption?

No. Encryption is reversible with the right key. A cryptographic hash is designed to be one-way. Password storage uses hashing with a salt and a deliberately slow algorithm.

### Does Kali Linux make someone a hacker?

No. Kali is a collection of tools. Skills in Linux, networking, methodology, reporting and ethics determine whether someone can use those tools effectively and lawfully.

### What does "in scope" mean?

It means the system, address, application or technique is explicitly included in written authorization. Anything not listed is out of scope until the owner confirms otherwise.
