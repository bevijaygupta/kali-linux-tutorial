---
layout: doc
title: "Kali Linux Study Roadmap: 8-Week Learning Plan"
description: "A realistic eight-week plan for the Kali Linux course, with weekly goals, lab deliverables, review checkpoints and a portfolio project."
permalink: /docs/study-roadmap/
eyebrow: "Documentation"
last_modified: 2026-11-14
---

## How to use this roadmap

This plan assumes **6–8 hours per week** and no prior Linux experience. If you have more time, keep the order and add practice; do not skip the fundamentals to reach the "exciting" modules faster. People who rush to exploitation usually end up copying commands they cannot explain.

The plan covers the **published** chapters. Scheduled chapters are marked on their lesson pages; add them to the matching week when they are released.

<div class="notice notice-info"><p><strong>Before week 1:</strong> complete the <a href="{{ '/docs/installation/' | relative_url }}">installation guide</a> and the <a href="{{ '/resources/lab-checklist/' | relative_url }}">lab checklist</a>. Do not start scanning until your lab is isolated and snapshotted.</p></div>

## The eight weeks at a glance

| Week | Focus | Chapters | Deliverable |
| --- | --- | --- | --- |
| 1 | Orientation, install, first Linux steps | 1–4 | Working Kali VM with a clean snapshot |
| 2 | Linux fundamentals | 5–12 | A personal command cheat sheet |
| 3 | Permissions, users, shortcuts | 13–19 | A permissions troubleshooting note |
| 4 | Networking, anonymity, traffic routing | 20–31 | A network diagram of your lab |
| 5 | Reconnaissance and Nmap | 32–41 | A recon report with no vulnerability claims |
| 6 | Vulnerability analysis and web tools | 42–48 | Two verified findings with evidence |
| 7 | Passwords, sniffing, wireless | 49–70 | A defence checklist for each topic |
| 8 | Exploitation, honeypots, review | 71–76 | A portfolio project and a gap review |

## Week 1 — Orientation and installation

**Chapters:** 1–4

**Goals**

- Explain why Kali exists and how it differs from Ubuntu.
- Download the official ISO and verify its checksum.
- Install VirtualBox or VMware and create a Kali VM.
- Update the system, install Guest Additions and take a snapshot.

**Practice**

- Rebuild the VM once without following along.
- Record the VM settings, network mode and snapshot name in a lab log.
- Write five questions you still have about Linux.

**Checkpoint:** you can restore the snapshot and explain what it contains.

## Week 2 — Linux fundamentals

**Chapters:** 5–12

**Goals**

- Navigate the file system without a GUI.
- Use `ls`, `cd`, `cp`, `mv`, `rm`, `find`, `locate`, `sort`, `zip` and `history`.
- Read command output and recognize errors.
- Use pipes and redirection safely.

**Practice**

- Create a directory tree and practise copying, moving and deleting.
- Build a 20-command cheat sheet in your own words.
- Explain the difference between `locate` and `find`.

**Checkpoint:** you can perform a file-management task from memory and explain each command.

## Week 3 — Permissions, users and terminal fluency

**Chapters:** 13–19

**Goals**

- Read and change numeric and symbolic permissions.
- Create users, change passwords and use `su`/`sudo`.
- Diagnose "Permission denied".
- Use Tab completion, `Ctrl+R` and other shortcuts.

**Practice**

- Create a test user and a shared directory with group permissions.
- Break a permission deliberately, then fix it.
- Write a one-page troubleshooting guide for common permission errors.

**Checkpoint:** you can explain `750`, `644` and `777` without looking them up.

## Week 4 — Networking and traffic routing

**Chapters:** 20–31

**Goals**

- Explain IP addresses, subnets, ports and DNS.
- Distinguish TCP from UDP.
- Explain proxy vs VPN vs Tor, including their limits.
- Change a MAC address in a lab and explain what it does not hide.
- Map your lab network and its boundary.

**Practice**

- Draw the lab: host, hypervisor, Kali, target, virtual switch, route to the internet.
- Capture five DNS packets and explain the query/response.
- Test what a proxy hides and what it leaks.

**Checkpoint:** you can trace a packet from Kali to the lab target and explain each hop.

## Week 5 — Reconnaissance and Nmap

**Chapters:** 32–41

**Goals**

- Distinguish passive and active reconnaissance.
- Use `dig`, `dnsenum`, `dnsmap` and `dnstracer` on a lab domain.
- Discover hosts with Nmap.
- Compare TCP connect, SYN and UDP scans.
- Identify services with `-sV` and save output.

**Practice**

- Scan your lab subnet and document every live host.
- Run a top-100 scan and a full TCP scan; compare time and results.
- Write a recon report that makes no vulnerability claims.

**Checkpoint:** you can explain `open`, `closed`, `filtered` and `open|filtered`.

## Week 6 — Vulnerability analysis and web tools

**Chapters:** 42–48

**Goals**

- Use Searchsploit to find candidate exploits and assess applicability.
- Run Nikto against a lab web server and verify findings manually.
- Use WhatWeb, Whois and Dirb within scope.
- Understand XSS and SQL injection at a conceptual level.
- Use SQLMap, jSQL and sqlsus only in a lab.

**Practice**

- Verify two Nikto findings with `curl`.
- Map two DVWA findings to OWASP categories.
- Write a finding with evidence, impact and remediation.

**Checkpoint:** you can distinguish a scanner claim from a verified finding.

## Week 7 — Passwords, sniffing and wireless

**Chapters:** 49–70

This is a large week. Split it across two weeks if needed.

**Goals**

- Explain hashing, salting and key stretching.
- Build a small custom wordlist with CEWL and Crunch.
- Crack a generated lab hash with John or Hashcat.
- Explain online vs offline attacks and the defences for each.
- Capture and read lab traffic with Wireshark.
- Explain ARP/DNS spoofing and why it is dangerous.
- Explain WEP, WPA2 and WPA3 differences.
- Describe a safe wireless lab and its legal limits.

**Practice**

- Write a password policy for a small organisation.
- Capture a lab HTTP request and identify the cookie.
- List five wireless hardening controls.

**Checkpoint:** you can explain why WPA3-SAE resists offline dictionary attacks.

## Week 8 — Exploitation, honeypots and review

**Chapters:** 71–76

**Goals**

- Explain Metasploit modules, payloads, sessions and handlers.
- Describe the buffer overflow workflow at a high level.
- Explain what a honeypot is and why it is not a perfect defence.
- Explain the limits of browser exploitation with BeEF.
- Review the whole course and identify weak areas.

**Practice**

- Inspect three Metasploit modules without running them.
- Write a cleanup checklist for an exploitation exercise.
- Design a small honeypot deployment for a lab.
- Build a portfolio project: a lab report with scope, method, findings, evidence and remediation.

**Checkpoint:** you can explain the difference between a proof of impact and real-world harm.

## If you only have three hours a week

Stretch the plan to 12–16 weeks. Keep the sequence:

1. Install and Linux basics.
2. Permissions and users.
3. Networking.
4. Recon.
5. Web and vulnerability analysis.
6. Passwords.
7. Sniffing and wireless.
8. Exploitation and review.

Do not skip weeks 1–4. They are the foundation for everything else.

## Portfolio project

A good beginner portfolio is not a collection of screenshots. It is a small, honest lab report:

- **Scope** — what you tested, what you excluded and why.
- **Environment** — VM names, network diagram, snapshots.
- **Method** — the commands and tools, with versions.
- **Findings** — verified issues, evidence and impact.
- **Remediation** — specific fixes and verification steps.
- **Reflection** — what you would do differently.

Redact credentials and personal data. Do not publish another organization's information. If you test a public lab platform, follow its rules for sharing write-ups.

## What comes after the course

- Build a home lab with a deliberately vulnerable app and a defender VM.
- Practise on legal platforms such as TryHackMe or Hack The Box.
- Study networking and operating-system fundamentals more deeply.
- Learn a scripting language for automation.
- Read vendor documentation and security advisories regularly.
- Consider an entry-level certification only when you can explain the material, not just pass a practice test.

No course guarantees a job. A portfolio, clear writing and verifiable lab work matter more than a certificate count.

## Review checklist

- [ ] I can install Kali and restore a snapshot.
- [ ] I can navigate Linux and fix common permission errors.
- [ ] I can explain IP, ports, DNS, TCP and UDP.
- [ ] I can scan a lab network and interpret the output.
- [ ] I can distinguish a vulnerability claim from a verified finding.
- [ ] I can explain hashing and why MFA matters.
- [ ] I can capture and read lab traffic responsibly.
- [ ] I can explain WPA2 vs WPA3.
- [ ] I can describe Metasploit concepts without running an attack.
- [ ] I have a written lab report with scope and remediation.
- [ ] I have not tested any system without authorization.

## Next steps

- Return to the [lesson index]({{ '/lessons/' | relative_url }}) and fill any gaps.
- Use the [cheat sheet]({{ '/resources/cheat-sheet/' | relative_url }}) for daily practice.
- Read the [official links]({{ '/resources/official-links/' | relative_url }}) for primary sources.
