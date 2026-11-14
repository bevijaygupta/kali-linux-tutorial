---
layout: doc
title: "Build an Isolated Kali Linux Lab for Safe Practice"
description: "Design a legal, snapshot-backed cybersecurity lab: host-only networking, target VMs, scope documents, isolation checks and a clean shutdown routine."
permalink: /docs/lab-setup/
eyebrow: "Documentation"
last_modified: 2026-11-14
---

## Why the lab matters

Most beginner mistakes are not technical. They are environmental: scanning a home router, attacking a university network, or running a password attack against a live account. An isolated lab removes the temptation and the risk. It also lets you break things without consequences, which is how you actually learn.

The goal is simple:

> One Kali VM, one deliberately vulnerable target VM, a private virtual network between them, and no route from that network to the internet or your real LAN.

<div class="notice notice-legal"><p><strong>Scope first.</strong> Write down what you are allowed to test before you boot the lab. If a target is not in your scope document and not owned by you, do not touch it.</p></div>

## Lab architecture

| Component | Role | Example |
| --- | --- | --- |
| Host machine | Runs the hypervisor | Your everyday laptop |
| Kali VM | Attacker workstation | Kali rolling, 4 GB RAM |
| Target VM | Deliberately vulnerable server | Metasploitable 2, DVWA, OWASP Juice Shop |
| Virtual network | Private link between VMs | Host-only adapter or internal network |
| Snapshot | Recovery point | `clean-install`, `pre-module-5` |
| Lab log | Evidence and cleanup | Markdown file on the host |

A second target VM is useful later, but start with one. More VMs increase memory pressure and configuration mistakes.

## Network modes, and when to use them

### NAT

The VM can reach the internet through the host, but the host and LAN cannot initiate connections to the VM. Use NAT for installation, updates and watching videos.

### Host-only

A private virtual network shared by the host and selected VMs. Use it for scanning and exploitation practice. The VMs can talk to each other but should not reach the internet.

### Internal network

VMs can talk only to other VMs on the same named internal network. This is the strongest isolation for a two-VM lab. The host cannot reach the VMs unless you add another adapter.

### Bridged

The VM appears as a separate device on your real LAN. **Avoid this for offensive testing.** A bridged VM can reach your router, printer, NAS and neighbours' devices, which turns a lab exercise into unauthorized testing.

<div class="notice notice-warning"><p><strong>Check before every scan.</strong> Run <code>ip route</code> and confirm the target address is on the isolated lab subnet, not your home or office network.</p></div>

## Step-by-step setup

### 1. Create the private network

In VirtualBox, open **File → Host Network Manager**, create a host-only adapter, and note its subnet, for example `192.168.56.0/24`. Disable the DHCP server if you want to assign addresses manually; leaving it enabled is fine for a small lab.

In VMware, use **Virtual Network Editor** to create a host-only VMnet and disable its NAT and DHCP if you prefer static addressing.

### 2. Attach Kali to the lab network

Add a second adapter to the Kali VM, set it to the host-only network, and keep the first adapter on NAT for updates. Inside Kali:

```bash
ip address
ip route
```

Identify the lab interface, for example `eth1`, and confirm it has an address on the lab subnet.

### 3. Attach the target VM

Set the target's adapter to the same host-only network. Boot it and note its address. If it uses DHCP, check the console or the hypervisor's lease list.

### 4. Verify isolation before testing

From Kali, test the target and then test the boundary:

```bash
ping -c 3 <target-ip>
ip route get <target-ip>
curl -I --max-time 5 http://<target-ip>/
```

The target should respond. A public website should not be reachable through the lab interface if you have truly isolated it. If the target is reachable and the internet is also reachable through the same interface, your isolation is incomplete.

### 5. Snapshot both VMs

Take a snapshot of Kali named `clean-install` and one of the target named `fresh-target`. Snapshot again before each destructive module: exploitation, password attacks, sniffing and wireless.

### 6. Write the scope document

Create a file on the host with these fields:

```text
Lab name:
Owner:
Date:
Kali IP / interface:
Target IP / hostname:
Allowed tests:
Excluded systems:
Network boundary:
Start snapshot:
End snapshot:
Cleanup steps:
```

Keep it short enough that you will actually fill it in. The value is the habit, not the paperwork.

## Choosing a target

Use an intentionally vulnerable application or VM:

- **DVWA** — a PHP/MySQL web app with adjustable difficulty, ideal for XSS and SQL injection chapters.
- **OWASP Juice Shop** — a modern JavaScript web app with a large set of guided challenges.
- **Metasploitable 2** — an older Linux VM built for exploitation practice.
- **VulnHub / OWASP VMs** — downloadable lab images; verify the source and run them isolated.
- **TryHackMe / Hack The Box** — hosted legal environments when you want guided or competitive practice.

Do not use a production server, a friend's website, a school network or a public IP address as a target. "It was only a scan" can still violate law and policy.

## Snapshot strategy

| When | Snapshot name | Why |
| --- | --- | --- |
| After install and updates | `clean-install` | Fast return to a known-good system |
| Before installing a tool stack | `pre-<tool>` | Undo dependency conflicts |
| Before exploitation | `pre-exploit` | Recover from a compromised VM |
| Before wireless tests | `pre-wireless` | Undo driver and monitor-mode changes |
| After a completed module | `module-N-done` | Reuse a working configuration |

Delete old snapshots when disk space becomes tight. Snapshots grow as the VM changes; they are not free.

## Housekeeping and cleanup

After each session:

1. Stop scans and close tools.
2. Revert the target VM to its fresh snapshot if it was compromised.
3. Revert Kali if you changed network or driver settings.
4. Update the lab log with what you ran and what you observed.
5. Confirm no scan is still running in the background.

Before you close the laptop, check for stray processes:

```bash
ps aux | grep -E 'nmap|msf|hydra|aircrack' | grep -v grep
```

Do not leave a password attack or a packet capture running unattended.

## Legal and ethical checklist

- The target is owned by you or covered by written permission.
- The target is on a private virtual network.
- The scope document names the target and the allowed tests.
- No public IP, employer network or shared Wi-Fi is in scope.
- You have a snapshot to restore.
- You will not publish another person's data, credentials or personal information.
- You will report a real vulnerability responsibly if you accidentally find one.

If any line is false, stop and fix it before continuing. The [lab checklist]({{ '/resources/lab-checklist/' | relative_url }}) turns this into a repeatable pre-flight list.

## Next steps

- Learn the command line with [Linux fundamentals]({{ '/docs/linux-fundamentals/' | relative_url }}).
- Understand the network with [Networking basics]({{ '/docs/networking-basics/' | relative_url }}).
- Start scanning in [Reconnaissance]({{ '/docs/reconnaissance/' | relative_url }}), only inside the lab.
