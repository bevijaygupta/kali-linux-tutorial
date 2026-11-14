---
layout: doc
title: "Kali Linux Course Documentation – Start Here"
description: "How to use the Kali Linux course notes: prerequisites, learning order, lab safety, study plan and links to every guide in the documentation set."
permalink: /docs/
eyebrow: "Documentation"
last_modified: 2026-11-14
---

## What this documentation is

This is the written reference layer for the **Kali Linux Complete Course** published by [EINITIAL24 ACADEMY](https://www.youtube.com/@EINITIAL24). The videos teach the material step by step. These pages explain the concepts behind each module, collect the official documentation, and describe how to practise without breaking a system or a law.

The repository is not a video mirror. It does not host video files, transcripts or full copies of chapter descriptions. Every lesson links to the original YouTube video, and every technical claim should be checked against the linked vendor documentation.

<div class="notice notice-legal"><p><strong>Authorized use only.</strong> Every command and technique discussed here is for systems you own or have explicit written permission to test. A personal virtual lab is the safest place to learn. Unauthorized access, interception or disruption is illegal in most jurisdictions.</p></div>

## Who this is for

- Complete beginners who want a structured path into Linux and security fundamentals.
- Students preparing for entry-level security certifications who need hands-on repetition.
- IT professionals who want to understand how attackers view a network.
- Anyone who prefers written notes alongside video.

You do **not** need programming experience. You do need a computer with enough RAM to run a virtual machine, and the patience to follow the chapters in order.

## The correct learning order

YouTube displays the playlist newest-first, so the top video is the most recent chapter, not Chapter 1. This site reorders the course into teaching order:

| Order | Module | Chapters |
| --- | --- | --- |
| 1 | Getting Started with Kali Linux | 1–4 |
| 2 | Linux Fundamentals for Ethical Hackers | 5–19 |
| 3 | Networking, Anonymity & Traffic Routing | 20–31 |
| 4 | Reconnaissance & Network Scanning | 32–41 |
| 5 | Web Application & Vulnerability Analysis | 42–48 |
| 6 | Password Attacks & Hash Cracking | 49–59 |
| 7 | Sniffing, Spoofing & Traffic Analysis | 60–66 |
| 8 | Wireless Network Security | 67–70 |
| 9 | Exploitation, Honeypots & Advanced Topics | 71–76 |

Use the [lesson index]({{ '/lessons/' | relative_url }}) for the full chapter-by-chapter table.

## Prerequisites

| Requirement | Minimum | Recommended |
| --- | --- | --- |
| RAM | 8 GB total | 16 GB total |
| Free disk | 40 GB | 80 GB SSD |
| CPU | 64-bit, virtualization enabled | 4 cores or more |
| Software | VirtualBox or VMware | VirtualBox with Extension Pack |
| Network | Internet for videos and updates | Separate host-only lab network |

Kali can run from a live USB, but a virtual machine is the better learning environment because you can snapshot it, break it and restore it. Bare-metal installation is covered in the course, but it is not necessary to follow along.

## How to use the site

1. Read [Getting started]({{ '/docs/getting-started/' | relative_url }}) for the course structure and study habits.
2. Follow [Installation]({{ '/docs/installation/' | relative_url }}) and [Lab setup]({{ '/docs/lab-setup/' | relative_url }}) before running any security tool.
3. Work through the [lessons]({{ '/lessons/' | relative_url }}) in chapter order.
4. Use the [Linux fundamentals]({{ '/docs/linux-fundamentals/' | relative_url }}) and [Networking basics]({{ '/docs/networking-basics/' | relative_url }}) guides when a video moves too fast.
5. Keep the [cheat sheet]({{ '/resources/cheat-sheet/' | relative_url }}) and [lab checklist]({{ '/resources/lab-checklist/' | relative_url }}) open while you practise.
6. Pick a schedule from the [study roadmap]({{ '/docs/study-roadmap/' | relative_url }}).

## What each lesson page contains

Every chapter page follows the same structure:

- **Watch the tutorial** — the original YouTube video, embedded privacy-first and linked directly.
- **About this chapter** — a written summary of the chapter's scope.
- **What you will learn** — concrete learning outcomes.
- **Important concepts** — the ideas that make the commands make sense.
- **Practical notes** — commands shown for study, with a safety warning.
- **Related lessons** — previous, next and same-module chapters.
- **Additional resources** — official documentation, not random tutorials.
- **FAQ** — common beginner questions.
- **Continue learning** — the next step in the course.

Scheduled chapters are labelled. Their notes are derived from the official chapter description and are revised when the video is published.

## Documentation map

| Guide | Use it when |
| --- | --- |
| [Getting started]({{ '/docs/getting-started/' | relative_url }}) | You are new and need a plan |
| [Installation]({{ '/docs/installation/' | relative_url }}) | You are downloading or installing Kali |
| [Lab setup]({{ '/docs/lab-setup/' | relative_url }}) | You need a safe place to practise |
| [Linux fundamentals]({{ '/docs/linux-fundamentals/' | relative_url }}) | Paths, permissions or users confuse you |
| [Networking basics]({{ '/docs/networking-basics/' | relative_url }}) | Addresses, ports or DNS are unclear |
| [Reconnaissance]({{ '/docs/reconnaissance/' | relative_url }}) | You are starting Nmap and OSINT |
| [Vulnerability analysis]({{ '/docs/vulnerability-analysis/' | relative_url }}) | You have scan output and need to interpret it |
| [Exploitation basics]({{ '/docs/exploitation-basics/' | relative_url }}) | You are opening Metasploit for the first time |
| [Password attacks]({{ '/docs/password-attacks/' | relative_url }}) | Hashes, wordlists or Hydra are new |
| [Wireless security]({{ '/docs/wireless-security/' | relative_url }}) | You are studying Wi-Fi security |
| [Web application security]({{ '/docs/web-application-security/' | relative_url }}) | You are testing a deliberately vulnerable app |
| [Study roadmap]({{ '/docs/study-roadmap/' | relative_url }}) | You need a week-by-week schedule |

## Editorial rules

This project follows five rules:

1. **Verify, do not invent.** Video titles, durations and dates come from YouTube metadata. Missing values are `null`, not guesses.
2. **Link, do not copy.** Videos and thumbnails remain on YouTube. No transcripts are published.
3. **Official sources first.** Tool documentation links point to vendor or project pages.
4. **Safety is part of the lesson.** Destructive commands and legal limits are called out next to the technique.
5. **Corrections are welcome.** If a command or link is wrong, open an issue with a source.

Ready? Continue with [Getting started]({{ '/docs/getting-started/' | relative_url }}).
