---
layout: doc
title: "Install Kali Linux Safely: ISO Verification & VirtualBox"
description: "Download Kali Linux from the official source, verify the ISO, and install it in VirtualBox or VMware with the right disk, memory and network settings."
permalink: /docs/installation/
eyebrow: "Documentation"
last_modified: 2026-11-14
---

## Only download from the official source

Kali Linux ISOs are published at [kali.org/get-kali](https://www.kali.org/get-kali/). Search results, YouTube descriptions and "pre-configured hacking VM" downloads are common vectors for malware. A tampered ISO can include a backdoor, a miner or credential-stealing code before you ever open a terminal.

Use the official **Installer** image for a virtual machine. The live image is useful for testing hardware, but it is not the best base for a persistent lab.

<div class="notice notice-warning"><p><strong>Do not use third-party images.</strong> A VM image from a random site can contain anything. Build your own from the official ISO and verify it.</p></div>

## Verify the ISO before you install

Kali publishes SHA-256 sums and a signing key. Verification proves that the file you downloaded matches the file the project published and that the checksum itself was signed by Kali.

### 1. Compare the SHA-256 sum

Download the `SHA256SUMS` file from the same official directory as the ISO, then run:

```bash
sha256sum kali-linux-*.iso
```

Compare the output with the matching line in `SHA256SUMS`. The two long hexadecimal strings must match exactly. A single different character means the download is corrupt or tampered with — delete it and download again.

### 2. Verify the signed checksum file (recommended)

Import the Kali signing key and verify `SHA256SUMS`:

```bash
gpg --keyserver hkps://keyserver.ubuntu.com --recv-key 44C6513A8E4FB3D30875F758ED444FF07D8D0BF6
gpg --verify SHA256SUMS.gpg SHA256SUMS
```

The fingerprint above is the public Kali repository key published by OffSec. Confirm it on the official Kali documentation before trusting a copy from any other source. A good signature does **not** prove the ISO is good by itself; it proves the checksum file is authentic, and the checksum then proves the ISO matches.

<div class="notice notice-info"><p><strong>Why this matters:</strong> verification is the first security habit in the course. If you skip it here, you will skip it when it matters more.</p></div>

## Create the virtual machine

The exact menus differ between VirtualBox versions, but the decisions are the same.

### VirtualBox settings

| Setting | Recommendation | Why |
| --- | --- | --- |
| Type / Version | Linux / Debian (64-bit) | Kali is Debian-based |
| Memory | 4096 MB minimum | 2048 MB is slow with a browser open |
| CPUs | 2–4 | More than the host has causes contention |
| Disk | 40 GB dynamically allocated | Enough for tools and snapshots |
| Network adapter | NAT while installing | Internet access for updates |
| Shared clipboard | Bidirectional (Guest Additions) | Convenient, but treat the host as trusted |
| USB | USB 3.0 controller | Needed for wireless adapters later |

If your host has 8 GB of RAM, do not give the VM more than 4 GB if you also plan to run a target VM. Two VMs plus the host will exhaust memory quickly.

### VMware settings

Use a Debian 12.x 64-bit guest profile, 4 GB RAM, 2 CPUs and a 40 GB disk. Set the network adapter to **NAT** for installation. Do not enable "Accelerate 3D graphics" on a headless host; it causes unnecessary instability.

## Install Kali

1. Attach the verified ISO to the VM's optical drive and boot.
2. Choose **Graphical Install**.
3. Select your language, location and keyboard layout.
4. Set a hostname such as `kali-lab` and a domain such as `lab.local` if you want one.
5. Create a **standard user** and a strong password. Do not rely on the default `kali/kali` credentials.
6. Partition the virtual disk using the guided method — the whole disk, one partition, no encryption is fine for a lab. Encryption adds a recovery risk if you forget the passphrase.
7. Let the installer finish, remove the ISO from the virtual drive, and reboot.

On first boot, open a terminal and confirm the basics:

```bash
whoami
ip address
df -h
```

## Update the fresh install

```bash
sudo apt update
sudo apt full-upgrade -y
sudo reboot
```

`full-upgrade` can remove packages when dependencies change. Read the prompt before confirming, especially on a system you have customised. For routine updates, `sudo apt upgrade` is the more conservative choice.

Check the release version:

```bash
cat /etc/os-release
```

## Take a clean snapshot immediately

Before installing extra tools, snapshot the VM and name it `clean-install`. A snapshot is not a backup of your host files, and it is not a substitute for external backups, but it is the fastest way to recover a broken lab.

VirtualBox: **Machine → Take Snapshot**. VMware: **VM → Snapshot → Take Snapshot**.

## Install Guest Additions or VMware Tools

Guest Additions enable clipboard sharing, shared folders, better display resolution and time sync.

```bash
sudo apt install -y virtualbox-guest-x11
```

On some Kali releases the package name or kernel modules differ. Use the official [Kali VirtualBox documentation](https://www.kali.org/docs/virtualization/install-virtualbox-guest-additions/) and reboot after installation. If the display breaks, restore the snapshot rather than debugging for an hour.

## Troubleshooting

### The VM boots to a black screen

Check that virtualization (VT-x/AMD-V) is enabled in the firmware. On Windows, Hyper-V can also block VirtualBox; disable it or use the Hyper-V backend deliberately.

### The installer cannot see the disk

Confirm the virtual disk is attached to the correct controller and that you did not accidentally create an ISO-only VM.

### No network after install

Check the adapter is attached and set to NAT. Inside Kali, run `ip address`. If the interface has no address, restart the network service or reboot the VM.

### The screen is tiny

Install Guest Additions, then set the display scaling in the VM settings. Do not install random display drivers from the internet.

### Updates fail with a signature error

Check the system clock. An incorrect date breaks TLS and package signature validation. Then re-check that your `sources.list` points to the official Kali repository.

## Next steps

- Harden the lab network with [Lab setup]({{ '/docs/lab-setup/' | relative_url }}).
- Learn the terminal with [Linux fundamentals]({{ '/docs/linux-fundamentals/' | relative_url }}).
- Start the course at [Chapter 1]({{ '/lessons/lesson-001/' | relative_url }}).

<div class="notice notice-legal"><p><strong>Reminder:</strong> installing Kali is legal. Using its tools against systems without authorization is not. Keep the VM isolated and document your scope before scanning anything.</p></div>
