---
layout: page
title: "Kali Linux Course – Free Notes, Labs & Study Roadmap"
description: "Study the EINITIAL24 Academy Kali Linux course with 76 chapter notes, a safe lab checklist, command cheat sheet and official documentation links. Free and beginner friendly."
image: "https://bevijaygupta.github.io/kali-linux-tutorial/assets/images/social-preview.png"
hide_title: true
breadcrumbs: false
permalink: /
---

<section class="hero">
  <div class="container hero-grid">
    <div class="hero-copy">
      <div class="hero-badges">
        <span>{{ site.data.course.total }} chapters</span>
        <span>{{ site.data.course.published }} published</span>
        <span>Free forever</span>
        <span>Beginner friendly</span>
      </div>
      <h1>Learn Kali Linux.<br><span class="accent">Learn it safely.</span></h1>
      <p class="hero-lede">A complete, chapter-by-chapter companion to the free EINITIAL24 Academy Kali Linux course. Written notes, lawful lab guidance and official documentation — built for people starting from zero.</p>
      <div class="hero-actions">
        <a class="button button-primary" href="{{ '/lessons/lesson-001/' | relative_url }}">Start with Chapter 1</a>
        <a class="button button-secondary" href="{{ site.playlist_url }}" target="_blank" rel="noopener noreferrer">Watch the playlist</a>
      </div>
      <p class="hero-note">No sign-up. No paywall. No transcripts or re-uploaded videos — every lesson links to the original YouTube chapter.</p>
    </div>
    <div class="hero-media">
      <img src="{{ '/assets/images/kali-linux-course-banner.png' | relative_url }}" alt="Kali Linux Complete Course banner showing the course title, 76 chapters and EINITIAL24 Academy branding" width="1280" height="640" fetchpriority="high">
    </div>
  </div>
  <div class="container">
    <div class="stat-row">
      <div class="stat"><strong>{{ site.data.course.total }}</strong><span>Chapters mapped</span></div>
      <div class="stat"><strong>{{ site.data.course.published }}</strong><span>Published videos</span></div>
      <div class="stat"><strong>{{ site.data.course.modules.size }}</strong><span>Learning modules</span></div>
      <div class="stat"><strong>0</strong><span>Videos re-hosted</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">What this is</p>
      <h2>A study companion, not a replacement for the course</h2>
      <p>The YouTube playlist teaches the material. This site gives you the structure around it: what each chapter covers, which commands are safe to practise, what to read next, and how to avoid the legal and technical mistakes beginners make.</p>
    </div>
    <ol class="steps">
      <li>
        <strong>Watch the chapter in order</strong>
        <p>The playlist is newest-first, so use <a href="{{ '/lessons/' | relative_url }}">the lesson index</a> or the chapter pages to follow the intended teaching order from Chapter 1 to Chapter 76.</p>
      </li>
      <li>
        <strong>Practise in an isolated lab</strong>
        <p>Install Kali in a virtual machine, take a snapshot, and keep the network isolated. The <a href="{{ '/resources/lab-checklist/' | relative_url }}">lab checklist</a> covers the pre-flight checks.</p>
      </li>
      <li>
        <strong>Read the notes and official docs</strong>
        <p>Each lesson adds context, safety warnings, official links and a FAQ. Written notes are not transcripts; they explain concepts and point to primary sources.</p>
      </li>
    </ol>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">Curriculum</p>
      <h2>Nine modules, {{ site.data.course.total }} chapters</h2>
      <p>Start at Module 1 and work forward. Each module builds on the previous one, from installing Kali to analysing web traffic, wireless security and exploitation concepts.</p>
    </div>
    <div class="module-grid">
      {%- for module in site.data.course.modules %}
      <a class="module-card" href="{{ module.url | relative_url }}">
        <span class="module-num">Module {{ module.number }}</span>
        <h3>{{ module.name | split: ": " | last }}</h3>
        <p>{{ module.blurb }}</p>
        <span class="module-count">Chapters {{ module.start }}–{{ module.end }} · {{ module.count }} lessons · {{ module.published }} published</span>
      </a>
      {%- endfor %}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">Start here</p>
      <h2>Your first hour</h2>
      <p>Do not install tools at random. Follow this order and you will have a working, legal practice environment before you touch a scanner.</p>
    </div>
    <div class="doc-grid">
      <a class="doc-card" href="{{ '/docs/installation/' | relative_url }}">
        <h3>1. Download and install Kali</h3>
        <p>Verify the ISO from the official source, then install it in VirtualBox or VMware. Avoid third-party "pre-hacked" images.</p>
        <span class="doc-card-more">Read the installation guide →</span>
      </a>
      <a class="doc-card" href="{{ '/docs/lab-setup/' | relative_url }}">
        <h3>2. Build an isolated lab</h3>
        <p>Host-only networking, snapshots, a target VM and a written scope. This is what makes practice legal and recoverable.</p>
        <span class="doc-card-more">Set up the lab →</span>
      </a>
      <a class="doc-card" href="{{ '/lessons/lesson-001/' | relative_url }}">
        <h3>3. Watch Chapter 1</h3>
        <p>Understand what Kali is, where it came from and why it is not a daily-driver operating system.</p>
        <span class="doc-card-more">Open Chapter 1 →</span>
      </a>
      <a class="doc-card" href="{{ '/docs/study-roadmap/' | relative_url }}">
        <h3>4. Pick a schedule</h3>
        <p>A realistic eight-week plan for finishing the course while working or studying full time.</p>
        <span class="doc-card-more">See the roadmap →</span>
      </a>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">Documentation</p>
      <h2>Reference material that stays useful</h2>
      <p>These guides explain the concepts behind the chapters, not just the clicks. Use them when a video moves too fast.</p>
    </div>
    <div class="doc-grid">
      <a class="doc-card" href="{{ '/docs/linux-fundamentals/' | relative_url }}">
        <h3>Linux fundamentals</h3>
        <p>Files, permissions, users, processes and the terminal habits that make every later chapter easier.</p>
        <span class="doc-card-more">Read the guide →</span>
      </a>
      <a class="doc-card" href="{{ '/docs/networking-basics/' | relative_url }}">
        <h3>Networking basics</h3>
        <p>Addresses, ports, DNS, HTTP and the difference between a proxy, a VPN and Tor.</p>
        <span class="doc-card-more">Read the guide →</span>
      </a>
      <a class="doc-card" href="{{ '/docs/reconnaissance/' | relative_url }}">
        <h3>Reconnaissance</h3>
        <p>Passive research, DNS enumeration and Nmap scans — with scope and rate limits in mind.</p>
        <span class="doc-card-more">Read the guide →</span>
      </a>
      <a class="doc-card" href="{{ '/docs/web-application-security/' | relative_url }}">
        <h3>Web application security</h3>
        <p>XSS, SQL injection, Burp Suite and Wireshark explained without hype.</p>
        <span class="doc-card-more">Read the guide →</span>
      </a>
      <a class="doc-card" href="{{ '/resources/cheat-sheet/' | relative_url }}">
        <h3>Command cheat sheet</h3>
        <p>A compact reference for the Linux, network and security commands used in the course.</p>
        <span class="doc-card-more">Open the cheat sheet →</span>
      </a>
      <a class="doc-card" href="{{ '/resources/official-links/' | relative_url }}">
        <h3>Official links</h3>
        <p>Kali docs, vendor manuals and the acceptable-use rules that apply to every lesson.</p>
        <span class="doc-card-more">See the links →</span>
      </a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">FAQ</p>
      <h2>Common questions</h2>
    </div>
    <div class="prose">
      <h3>Is this course really free?</h3>
      <p>Yes. The videos are free on YouTube and these written notes are free to read. There is no account, paywall or upsell.</p>

      <h3>Do I need to know Linux first?</h3>
      <p>No. Module 2 starts from the terminal and assumes no prior experience. If you already know Linux, you can move faster through Chapters 5–19.</p>

      <h3>Which chapters are published right now?</h3>
      <p>{{ site.data.course.published }} of {{ site.data.course.total }} chapters are published. The remaining {{ site.data.course.scheduled }} are scheduled on YouTube; their lesson pages are clearly labelled and contain no invented video details.</p>

      <h3>Can I practise on any website or network?</h3>
      <p>No. Only test systems you own or have explicit written permission to test. Use a local lab or a legal practice platform. Unauthorized access is a crime in most jurisdictions.</p>

      <h3>Why do some lessons have no video yet?</h3>
      <p>The channel has scheduled future chapters. Their pages are based on the official chapter descriptions, not video footage, and the site does not publish a duration or publish date it cannot verify.</p>

      <h3>How often is the playlist data updated?</h3>
      <p>A GitHub Actions workflow checks the playlist weekly and opens a pull request when metadata changes. It never pushes to the main branch directly.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="cta-band">
      <div>
        <h2>Ready for Chapter 1?</h2>
        <p>Start with why Kali exists, then install it safely. The whole course is waiting — no sign-up required.</p>
      </div>
      <a class="button button-primary" href="{{ '/lessons/lesson-001/' | relative_url }}">Begin the course</a>
    </div>
  </div>
</section>
