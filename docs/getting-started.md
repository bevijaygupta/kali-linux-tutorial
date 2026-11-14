---
layout: doc
title: "Getting Started with the Kali Linux Course"
description: "A practical orientation to the Kali Linux course: prerequisites, the right learning order, how to take notes, and the first three things to do before Chapter 1."
permalink: /docs/getting-started/
eyebrow: "Documentation"
last_modified: 2026-11-14
---

## Start with the right expectations

Kali Linux is a specialist operating system for security work, not a shortcut to becoming a hacker. It bundles hundreds of tools, but tools do not supply judgement. This course is structured so that you learn the operating system, the network and the methodology before you run anything intrusive.

You can finish the published chapters in a few weekends of passive watching. Actually learning the material takes longer, because every module needs lab time. Plan for **two to four hours of practice for every hour of video**.

<div class="notice notice-legal"><p><strong>Legal boundary.</strong> Use every technique only on machines you own or have explicit written permission to test. "I was just practising" is not a legal defence. The course notes always assume an isolated lab.</p></div>

## What you need before Chapter 1

- A 64-bit computer with virtualization enabled in the BIOS/UEFI.
- 8 GB of RAM minimum; 16 GB is comfortable if you also run a target VM.
- 40–80 GB of free disk space.
- VirtualBox or VMware Workstation Player.
- A wired or stable internet connection for downloads and videos.
- A notebook — physical or digital — for commands, outputs and questions.

You do not need a second computer, a paid course, a certification voucher or an "ethical hacking" distro collection. One Kali VM and one deliberately vulnerable target VM are enough for most of the course.

## The teaching order versus the playlist order

YouTube shows the newest chapter at the top of the playlist. If you press play from the top, you will start near the end of the course. Use one of these instead:

1. Open the [lesson index]({{ '/lessons/' | relative_url }}) and start at Chapter 1.
2. Use the **Previous lesson** and **Next lesson** links at the bottom of each chapter page.
3. Bookmark the playlist and select Chapter 1 manually from the playlist menu.

The lesson pages preserve the original playlist position as metadata, so you can always find the video in the playlist without pretending the order is something it is not.

## A realistic first week

| Day | Task | Time |
| --- | --- | --- |
| 1 | Read this page and the [lab checklist]({{ '/resources/lab-checklist/' | relative_url }}) | 30 min |
| 2 | Download and verify the Kali ISO | 45 min |
| 3 | Install VirtualBox and create the Kali VM | 60 min |
| 4 | Complete the Kali installer and first boot | 60 min |
| 5 | Update the system inside the VM and take a snapshot | 45 min |
| 6 | Watch Chapters 1–4 and write notes | 90 min |
| 7 | Rebuild the VM from scratch without following along | 90 min |

Rebuilding from scratch is the most valuable step. It exposes what you only thought you understood.

## How to take notes that help later

A useful note for a security command contains five things:

- **Purpose** — what question the command answers.
- **Exact syntax** — the command you ran, with placeholders clearly marked.
- **Input context** — target, interface, wordlist or credentials file.
- **Output interpretation** — what the result means and what it does not mean.
- **Safety note** — whether it changes state, generates traffic, or could break something.

Avoid copying entire terminal transcripts. Summarise the decision, not the scrollback.

## Study habits that prevent wasted months

### Watch once, practise twice

Watch a chapter without pausing to copy commands. Then rewatch the practical section with the VM open. Finally, repeat the exercise from memory with the video closed.

### Keep a lab log

Record the date, the VM snapshot name, the target, the command, the result and the cleanup step. If you later break something, the log tells you where to restart.

### Do not collect tools

Installing every tool in the Kali repository feels productive and teaches almost nothing. Learn one tool per module deeply enough to explain its output to another person.

### Stop when you are guessing

If you cannot explain why a scan returned a result, stop and read the official documentation. Running more commands on top of a misunderstood result creates false confidence.

## What to skip for now

- Wireless testing until you have a compatible adapter and understand the legal limits.
- Exploitation modules until your lab is isolated and snapshotted.
- Password cracking until you understand hashing and wordlists.
- Any "full course in 24 hours" video that promises a job.

## Common beginner mistakes

| Mistake | Better approach |
| --- | --- |
| Installing Kali on bare metal first | Use a VM with snapshots |
| Using the host network for scans | Use host-only or isolated networking |
| Testing a public website "just to see" | Use DVWA, Metasploitable or a legal platform |
| Copying commands without reading options | Run `man <tool>` and check each flag |
| Skipping Linux fundamentals | Complete Chapters 5–19 before scanners |
| Chasing certifications too early | Build one solid lab project first |

## Next steps

1. Read [Installation]({{ '/docs/installation/' | relative_url }}) and verify the ISO from the official Kali site.
2. Follow [Lab setup]({{ '/docs/lab-setup/' | relative_url }}) to isolate the VM.
3. Open [Chapter 1]({{ '/lessons/lesson-001/' | relative_url }}) and begin.
4. Choose a schedule from the [study roadmap]({{ '/docs/study-roadmap/' | relative_url }}).

If you get stuck, check the chapter FAQ first, then the official documentation linked at the bottom of the lesson. When a link or command is wrong, open an issue in the repository with the source that proves it.
