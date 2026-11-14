---
layout: page
hide_title: true
title: "Official Cybersecurity Documentation & Legal Links"
description: "Primary documentation for Kali Linux, Nmap, Metasploit, Wireshark, OWASP, password tools, wireless security and Tor, plus legal and ethics references."
permalink: /resources/official-links/
section: "Resources"
section_url: "/resources/"
last_modified: 2026-11-14
---

# Official links and primary sources

Tool tutorials age quickly. Vendor documentation, project repositories and standards bodies are the sources to trust when a command, option or default changes. This page collects the primary sources used across the course.

<div class="notice notice-legal"><p><strong>Authorized use only.</strong> Documentation explains capability, not permission. Use these tools only on systems you own or have explicit written authorization to test.</p></div>

## How to judge a source

1. **Prefer the project itself.** The official manual, repository or documentation site beats a reposted tutorial.
2. **Check the date and version.** A 2016 walkthrough may describe flags that no longer exist.
3. **Look for evidence.** Good security writing distinguishes a verified finding from a guess.
4. **Cross-check vulnerabilities.** Use CVE/NVD records, vendor advisories and the original research.
5. **Do not copy commands blindly.** Read the option list and understand the target before running anything.

## Kali Linux and Debian

| Resource | Why it matters |
| --- | --- |
| [Kali Linux documentation](https://www.kali.org/docs/) | Installation, configuration, troubleshooting and tool usage from the maintainers |
| [Get Kali](https://www.kali.org/get-kali/) | Official images and download verification information |
| [Kali tools directory](https://www.kali.org/tools/) | Package descriptions and upstream project links |
| [Kali blog](https://www.kali.org/blog/) | Release notes and platform changes |
| [Debian documentation](https://www.debian.org/doc/) | The base distribution's manuals and policy |
| [Linux man-pages project](https://man7.org/linux/man-pages/) | Manual pages for core Linux commands |

Kali Linux is maintained by OffSec. This repository is an independent study companion and is not affiliated with OffSec or the Kali project.

## Virtualisation

| Resource | Why it matters |
| --- | --- |
| [VirtualBox manual](https://www.virtualbox.org/manual/) | Network modes, snapshots, shared folders and guest additions |
| [VMware Workstation documentation](https://docs.vmware.com/en/VMware-Workstation-Pro/index.html) | Virtual networking and snapshot behaviour for VMware users |
| [Proxmox documentation](https://pve.proxmox.com/pve-docs/) | Alternative lab platform for dedicated hardware |

Read the network-mode section before you connect a lab VM to anything. A bridged adapter changes the blast radius of every command.

## Networking, DNS and packet analysis

| Resource | Why it matters |
| --- | --- |
| [Nmap reference guide](https://nmap.org/book/man.html) | Authoritative explanation of scan types and options |
| [Nmap NSE documentation](https://nmap.org/nsedoc/) | Script categories and individual script behaviour |
| [Wireshark user's guide](https://www.wireshark.org/docs/wsug_html_chunked/) | Capture, display filters and protocol analysis |
| [tcpdump manual](https://www.tcpdump.org/manpages/tcpdump.1.html) | Command-line packet capture |
| [Scapy documentation](https://scapy.readthedocs.io/) | Packet crafting and inspection in Python |
| [BIND 9 documentation](https://bind9.readthedocs.io/) | DNS server and query tool reference, including `dig` |
| [IANA root servers](https://www.iana.org/domains/root/servers) | DNS root server operators and addresses |
| [Cloudflare Learning Center: DNS](https://www.cloudflare.com/learning/dns/what-is-dns/) | Accessible DNS primer from a network operator |

Only capture traffic on networks you own or are authorized to monitor. Packet capture can expose credentials and personal data.

## Web application security

| Resource | Why it matters |
| --- | --- |
| [OWASP Top 10](https://owasp.org/www-project-top-ten/) | The most widely used web risk awareness list |
| [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) | Structured testing methodology |
| [OWASP: Cross Site Scripting](https://owasp.org/www-community/attacks/xss/) | How XSS works and how to prevent it |
| [OWASP: SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection) | Injection concepts and defences |
| [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) | Deliberately vulnerable application for legal practice |
| [DVWA](https://dvwa.co.uk/) | Classic deliberately vulnerable PHP application |
| [PortSwigger Web Security Academy](https://portswigger.net/web-security) | Free labs and explanations from the Burp Suite team |
| [Burp Suite documentation](https://portswigger.net/burp/documentation) | Proxy, repeater, intruder and scanner reference |

Use DVWA, Juice Shop or another application explicitly designed for training. A public website is not a practice target.

## Exploitation and vulnerability research

| Resource | Why it matters |
| --- | --- |
| [Metasploit documentation](https://docs.metasploit.com/) | Framework concepts, modules and usage |
| [Exploit-DB](https://www.exploit-db.com/) | Public exploit and proof-of-concept archive |
| [SearchSploit manual](https://www.exploit-db.com/searchsploit) | Offline command-line access to Exploit-DB |
| [BeEF project](https://beefproject.com/) | Browser exploitation framework documentation |
| [CVE Program](https://www.cve.org/) | Canonical vulnerability identifiers |
| [NVD](https://nvd.nist.gov/) | CVE enrichment, severity and references |
| [FIRST CVSS](https://www.first.org/cvss/) | Severity scoring specification |
| [MITRE ATT&CK](https://attack.mitre.org/) | Adversary tactics and techniques knowledge base |

An exploit database entry is not proof that a target is vulnerable. Verify the version, prerequisites and impact in a lab before making a claim.

## Passwords and authentication

| Resource | Why it matters |
| --- | --- |
| [John the Ripper](https://www.openwall.com/john/) | Project home and release information |
| [John the Ripper documentation](https://www.openwall.com/john/doc/) | Modes, formats and options |
| [Hashcat wiki](https://hashcat.net/wiki/) | Hash modes, attack modes and performance guidance |
| [THC Hydra](https://github.com/vanhauser-thc/thc-hydra) | Online password testing tool and documentation |
| [Medusa](https://www.kali.org/tools/medusa/) | Kali package notes for the online testing tool |
| [CeWL](https://github.com/digininja/CeWL) | Custom wordlist generation |
| [Crunch](https://www.kali.org/tools/crunch/) | Pattern-based wordlist generation |
| [Hash-Identifier](https://www.kali.org/tools/hash-identifier/) | Hash type identification helper |

Online guessing can lock real accounts and is illegal without authorization. Use lab accounts and rate limits. Offline cracking should use hashes you created or are authorized to assess.

## Wireless security

| Resource | Why it matters |
| --- | --- |
| [Aircrack-ng documentation](https://www.aircrack-ng.org/doku.php) | Monitor mode, capture and cracking suite reference |
| [Wi-Fi Alliance](https://www.wi-fi.org/) | Wireless standards and certification information |
| [Wireshark wireless analysis](https://www.wireshark.org/docs/wsug_html_chunked/) | 802.11 capture and display filters |
| [Kali wireless docs](https://www.kali.org/docs/) | Adapter and driver guidance from the Kali project |

Radio interception is regulated in many countries. Test only your own equipment and network, and check local rules before capturing frames.

## Privacy, anonymity and Tor

| Resource | Why it matters |
| --- | --- |
| [Tor Project](https://www.torproject.org/) | How Tor works and how to use it |
| [Tor support portal](https://support.torproject.org/) | Configuration and troubleshooting |
| [EFF Surveillance Self-Defense](https://ssd.eff.org/) | Practical privacy and threat-model guidance |
| [EFF](https://www.eff.org/) | Digital rights research and policy context |

A proxy, VPN or Tor circuit does not create authorization and does not guarantee anonymity. It changes where traffic appears to come from, not whether an action is lawful.

## Law, ethics and incident reporting

| Resource | Why it matters |
| --- | --- |
| [UK Computer Misuse Act 1990](https://www.legislation.gov.uk/ukpga/1990/18/contents) | Primary legislation on unauthorized access in the UK |
| [US DOJ Computer Crime and Intellectual Property Section](https://www.justice.gov/criminal-ccips) | US computer crime policy and guidance |
| [CISA](https://www.cisa.gov/) | US cybersecurity agency guidance and advisories |
| [NCSC](https://www.ncsc.gov.uk/) | UK cybersecurity guidance |
| [ENISA](https://www.enisa.europa.eu/) | EU cybersecurity agency publications |

This list is for orientation, not legal advice. Laws differ by jurisdiction and by the network or data involved. If you are unsure whether an action is authorized, do not run it.

## Practice platforms

| Resource | Why it matters |
| --- | --- |
| [TryHackMe](https://tryhackme.com/) | Guided, browser-based security labs |
| [Hack The Box](https://www.hackthebox.com/) | Challenge and lab platform with scoped targets |
| [VulnHub](https://www.vulnhub.com/) | Downloadable vulnerable virtual machines for local labs |
| [PortSwigger Web Security Academy](https://portswigger.net/web-security) | Free web security labs and learning material |

Platform terms still apply. Stay inside the targets the platform provides, and never use a lab skill against a system outside it.

## Related resources

- [Kali Linux command cheat sheet]({{ '/resources/cheat-sheet/' | relative_url }})
- [Lab checklist]({{ '/resources/lab-checklist/' | relative_url }})
- [Glossary]({{ '/resources/glossary/' | relative_url }})
- [Reconnaissance guide]({{ '/docs/reconnaissance/' | relative_url }})
- [Web application security guide]({{ '/docs/web-application-security/' | relative_url }})
- [Security policy]({{ site.repository_url }}/blob/main/SECURITY.md)

## FAQ

### Why are some tools missing from this list?

The list focuses on tools covered by the course and on primary sources that change slowly. A missing tool is not a judgement about its quality; add a suggestion through the issue tracker if a stable official link is missing.

### Is documentation enough to make a tool safe to run?

No. Documentation explains the options. Authorization, scope, a snapshot and a rollback plan determine whether running it is acceptable.

### What should I do if a link is broken?

Open an issue with the page URL and the link that failed. Prefer the project's current documentation home page over a deep link that may have moved.
