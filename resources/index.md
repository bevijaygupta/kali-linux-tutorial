---
layout: page
hide_title: true
title: "Kali Linux Resources: Cheat Sheet, Lab Checklist & Glossary"
description: "Practical resources for the Kali Linux course: a safe command cheat sheet, lab pre-flight checklist, official documentation links and a plain-language glossary."
permalink: /resources/
breadcrumbs: false
---

# Resources

These are the working documents for the course. They are designed to be printed, bookmarked or copied into your lab notes — not read once and forgotten.

<div class="notice notice-legal"><p><strong>Authorized use only.</strong> Every command in these resources is for systems you own or have explicit written permission to test. The cheat sheet is a syntax reference, not a target list.</p></div>

<div class="doc-grid">
  <a class="doc-card" href="{{ '/resources/cheat-sheet/' | relative_url }}">
    <h3>Command cheat sheet</h3>
    <p>Linux, networking, reconnaissance, web, password and wireless commands — with the safety notes that matter.</p>
    <span class="doc-card-more">Open the cheat sheet →</span>
  </a>
  <a class="doc-card" href="{{ '/resources/lab-checklist/' | relative_url }}">
    <h3>Lab checklist</h3>
    <p>A repeatable pre-flight, in-flight and cleanup checklist for every practice session, plus a scope template.</p>
    <span class="doc-card-more">Open the checklist →</span>
  </a>
  <a class="doc-card" href="{{ '/resources/official-links/' | relative_url }}">
    <h3>Official links</h3>
    <p>Kali, Nmap, Metasploit, Wireshark, OWASP and other primary documentation sources, plus acceptable-use rules.</p>
    <span class="doc-card-more">See the links →</span>
  </a>
  <a class="doc-card" href="{{ '/resources/glossary/' | relative_url }}">
    <h3>Glossary</h3>
    <p>Plain-language definitions of the terms used across the course, from ARP to XSS.</p>
    <span class="doc-card-more">Read the glossary →</span>
  </a>
</div>

## How to use these resources

1. **Before a session:** open the [lab checklist]({{ '/resources/lab-checklist/' | relative_url }}) and confirm scope, snapshots and network isolation.
2. **During a session:** use the [cheat sheet]({{ '/resources/cheat-sheet/' | relative_url }}) for syntax, then read `man <tool>` for the full option list.
3. **When a term is unclear:** check the [glossary]({{ '/resources/glossary/' | relative_url }}).
4. **When you need the primary source:** use [official links]({{ '/resources/official-links/' | relative_url }}). Prefer vendor documentation over random tutorials.
5. **After a session:** record what you ran, restore snapshots and clean up.

## What is not here

- No exploit payloads aimed at real systems.
- No credential dumps, hashes or personal data.
- No video files, transcripts or copied chapter descriptions.
- No "one weird trick" shortcuts that skip the fundamentals.

The course videos live on [YouTube]({{ site.playlist_url }}). The written notes live in the [lesson index]({{ '/lessons/' | relative_url }}). These resources support both.
