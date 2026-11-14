---
layout: page
hide_title: true
title: "Kali Linux Lab Checklist: Safe Practice Before Every Session"
description: "A repeatable pre-flight, in-session and cleanup checklist for Kali Linux practice, plus a scope template, isolation checks and snapshot guidance."
permalink: /resources/lab-checklist/
section: "Resources"
section_url: "/resources/"
last_modified: 2026-11-14
---

# Kali Linux lab checklist

Most avoidable incidents in a beginner lab are environmental, not technical: the wrong network adapter, a missing snapshot, a test aimed at a live service, or a forgotten listener left running overnight. This checklist turns lab safety into a routine.

<div class="notice notice-legal"><p><strong>Authorized use only.</strong> A virtual machine does not create permission. Test only systems you own or have explicit written authorization to assess. Keep that authorization with your notes for the whole session.</p></div>

## Before you start

Work through this list before opening a terminal. If any item is false, stop and fix it first.

- [ ] **Scope is written down.** I know exactly which hosts, URLs, accounts and networks are in scope, and which are excluded.
- [ ] **Authorization is available.** For anything I do not personally own, I have written permission from someone entitled to grant it.
- [ ] **The lab is isolated.** Kali and the target use a host-only, internal or otherwise isolated network. Bridged mode is off unless the exercise explicitly requires it and the scope allows it.
- [ ] **A clean snapshot exists.** The VM is snapshotted before tools are installed, files are changed or a test begins.
- [ ] **The target is disposable.** The target VM or deliberately vulnerable application can be rebuilt from a snapshot or installer.
- [ ] **No production accounts are involved.** I am not using personal, work, university or shared credentials in the lab.
- [ ] **Test data is synthetic.** Any credentials, hashes, documents or databases are created for the exercise.
- [ ] **Logging is ready.** I have a place to record the date, scope, commands, results and cleanup steps.
- [ ] **Resources are sufficient.** There is enough disk space, RAM and battery for the session, and the host will not sleep mid-test.
- [ ] **Wireless testing is lawful.** If radio equipment is involved, I own the network and hardware, and I have checked local radio regulations.

## Write a scope statement

Even a solo lab benefits from a one-page scope. It forces you to name the boundary before you touch a scanner. Copy this template into your notes and fill it in honestly.

```text
Lab / engagement scope
----------------------
Owner:                 [name or "self"]
Authorized tester:     [name]
Authorization date:    [YYYY-MM-DD]
Authorization ref:     [ticket, email or document reference]

In scope:
  Hosts / IPs:         [e.g. 192.168.56.10]
  URLs:                [e.g. http://lab.local/]
  Applications:        [e.g. DVWA on the target VM]
  Accounts:            [lab-only accounts]

Out of scope:
  [production systems, home router, public websites, other students]

Allowed techniques:
  [e.g. port scanning, web crawling, authentication testing]

Prohibited techniques:
  [e.g. denial of service, destructive payloads, data exfiltration]

Test window:
  [start and end in UTC, including timezone]

Network location:
  [host-only / internal / isolated VLAN]

Emergency stop:
  [how to shut down the VM or disconnect the network]

Cleanup:
  [snapshot restore, listener shutdown, file deletion]
```

A scope is not a legal contract by itself. It is a record that you thought about authorization before acting. Real engagements need a signed agreement reviewed by someone qualified to approve it.

## Verify network isolation

Run these checks on Kali and on the target. You are looking for proof that traffic cannot reach systems outside the lab.

| Check | Command | What to confirm |
| --- | --- | --- |
| Interfaces | `ip -brief address` | Only the expected lab adapters are up |
| Routes | `ip route` | No unexpected default route to a live network |
| Neighbours | `ip neigh` | Only lab hosts appear in the ARP table |
| Target reachability | `ping -c 3 192.168.56.10` | The lab target answers |
| Internet isolation | `ping -c 1 1.1.1.1` | This should fail in an isolated lab |
| Listening services | `ss -tulpn` | Only services you intended to start are listening |

Replace `192.168.56.10` with your target address. If the internet test succeeds when it should not, stop. Check the VM network mode before continuing.

<div class="notice notice-warning"><p><strong>Do not "just test it quickly" on a bridged adapter.</strong> Bridged mode puts the VM on the same network as your host. A scan that was harmless in a host-only lab can reach a neighbour, a workplace network or a public service.</p></div>

## Snapshot routine

A snapshot is your rollback plan. Take one at each stable point, and label it clearly.

1. **Clean install** — immediately after installation and updates.
2. **Tool baseline** — after installing the tools needed for the module.
3. **Before a risky exercise** — before changing interfaces, firewall rules, services or target data.
4. **After a verified result** — when the lab is in a known-good state you want to reuse.

VirtualBox example (run on the host, not inside Kali):

```bash
VBoxManage list vms
VBoxManage snapshot "Kali Lab" take "before-module-4" --description "Clean lab before Nmap practice"
VBoxManage snapshot "Kali Lab" list
```

Names and syntax vary by version. If you use VMware, take the snapshot through the VM menu and confirm it completed before starting the exercise.

<div class="notice notice-warning"><p><strong>Snapshots are not backups.</strong> They live with the VM and can be corrupted or deleted. Keep installers and notes somewhere separate, and never store the only copy of important work inside a lab VM.</p></div>

## During the session

- Keep the scope visible. If a command targets something outside it, stop.
- Prefer read-only discovery before any state-changing action.
- Rate-limit scans and avoid aggressive options on shared hardware.
- Read the command before pressing Enter. Check the interface, target and output path.
- Record the exact command, time and result. Future you will not remember the flags.
- Do not paste credentials, tokens or personal data into notes, screenshots or chat.
- Stop and reassess if a service becomes unstable, a disk fills up or the network changes.
- Disconnect test listeners and reverse shells when you are finished with them.

## After the session

- [ ] Stop every listener, scanner, capture and background process you started.
- [ ] Save notes and evidence in the agreed location.
- [ ] Remove temporary wordlists, captures and extracted data that are no longer needed.
- [ ] Restore the snapshot if the lab was modified.
- [ ] Return interfaces to managed mode after wireless work.
- [ ] Shut down the target and Kali VMs cleanly.
- [ ] Disconnect VPNs, proxies and shared folders you enabled for the exercise.
- [ ] Note anything that needs review before the next session.

Useful checks:

```bash
ss -tulpn
ps aux | grep -E 'nmap|sqlmap|hydra|medusa|tcpdump|ettercap|aircrack'
ip -brief address
```

The process list is a prompt, not a complete audit. Review the output and stop anything you no longer need.

## Legal and ethical boundaries

- **Authorization must be explicit.** "It is on the internet" is not permission.
- **Stay inside scope.** A related domain, a shared host or a neighbouring IP is still out of scope unless it is listed.
- **Minimize impact.** Use the least intrusive technique that answers the question.
- **Protect data.** If you encounter real personal or sensitive data in a lab, stop and report it rather than copying it.
- **Do not hide activity.** Covert persistence, cleanup of audit logs and testing outside the window are not acceptable in a learning lab.
- **Report problems.** If you accidentally affect a system outside scope, tell the owner promptly and document what happened.

Laws differ by country and by network. The [official links]({{ '/resources/official-links/' | relative_url }}) page lists primary security resources and selected legal references, but it is not legal advice.

## Related resources

- [Kali Linux command cheat sheet]({{ '/resources/cheat-sheet/' | relative_url }})
- [Build an isolated lab]({{ '/docs/lab-setup/' | relative_url }})
- [Glossary]({{ '/resources/glossary/' | relative_url }})
- [Study roadmap]({{ '/docs/study-roadmap/' | relative_url }})
- [Lesson index]({{ '/lessons/' | relative_url }})

## FAQ

### Is a virtual machine enough to make testing legal?

No. A VM limits technical impact, but authorization still comes from the system owner. Use a VM to protect your own machine, not as a substitute for permission.

### Should I use NAT or host-only networking?

Host-only or an internal network is the safer default because it isolates the lab from your real network. NAT can be useful for updates, but it also gives the VM a route to the internet. Switch back to host-only before scanning.

### How often should I take snapshots?

Before every exercise that changes system state, and after every verified good state you want to reuse. Snapshots are cheap compared with rebuilding a corrupted lab.
