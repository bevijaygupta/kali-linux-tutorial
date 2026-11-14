---
layout: doc
title: "Wireless Security: Wi-Fi Terms, Aircrack-ng & Defense"
description: "Understand 802.11 security, WEP, WPA2, WPA3, monitor mode, Aircrack-ng workflows and practical ways to protect a wireless network."
permalink: /docs/wireless-security/
eyebrow: "Documentation"
last_modified: 2026-11-14
---

## Wireless is a radio problem first

Wi-Fi attacks are constrained by physics and law. You need a compatible adapter, proximity to the signal, and authorization to test the network. Capturing frames from a network you do not own can violate wiretapping and privacy laws even if you never crack a password.

This guide explains the concepts behind the wireless module. It does not provide a step-by-step attack against a neighbour's network.

<div class="notice notice-legal"><p><strong>Radio interception is regulated.</strong> Monitoring, capturing and injecting frames on a network you do not own can be illegal. Test only your own equipment in an isolated lab, and check local radio regulations before changing adapter behaviour.</p></div>

## 802.11 terms

| Term | Meaning |
| --- | --- |
| SSID | Network name |
| BSSID | MAC address of an access point |
| Channel | Frequency slice used by the network |
| Band | 2.4 GHz, 5 GHz or 6 GHz |
| Beacon | Periodic management frame advertising the network |
| Probe request | Client searching for a network |
| Association | Client joining an access point |
| Handshake | Authentication and key negotiation exchange |
| PMF | Protected Management Frames |
| Monitor mode | Capture all frames on a channel, not just those addressed to you |
| Packet injection | Transmit crafted frames; requires adapter and driver support |

Wireless security is not only about the password. It also includes rogue access points, evil twins, deauthentication, captive portals, WPS and client-side attacks.

## WEP, WPA, WPA2 and WPA3

### WEP

Wired Equivalent Privacy used RC4 with short, weak initialization vectors. It is broken and should not be used. A WEP key can be recovered from captured traffic in minutes with the right hardware. The lesson is historical: never rely on an obsolete protocol because it is convenient.

### WPA

Wi-Fi Protected Access introduced TKIP as an interim fix. It is deprecated and should be disabled.

### WPA2

WPA2 uses AES-CCMP and a 4-way handshake. In personal mode (WPA2-PSK), a shared passphrase derives the pairwise key. Capture of a handshake allows an offline dictionary attack against a weak passphrase. WPA2-Enterprise uses 802.1X and a RADIUS server, which changes the attack surface.

### WPA3

WPA3-Personal uses SAE (Simultaneous Authentication of Equals), which resists offline dictionary attacks against captured handshakes. WPA3 also mandates PMF in many configurations. It is not immune to all attacks, but it removes a major weakness of WPA2-PSK.

Older devices may fall back to WPA2 or use transition mode. A network is only as strong as its weakest permitted configuration.

## Hardware and drivers

Not every adapter supports monitor mode and injection, especially on Windows hosts. A common setup is a USB adapter passed through to a Kali VM, with a chipset supported by Linux.

Check interfaces:

```bash
iw dev
ip link
```

Check capabilities:

```bash
iw list | grep -A 8 "Supported interface modes"
```

Look for `monitor` and, if you plan to inject, confirm the driver supports it. Virtual machines add another layer: USB passthrough must work reliably, and the hypervisor must not block the adapter.

Changing an interface to monitor mode:

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
```

To return to managed mode:

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type managed
sudo ip link set wlan0 up
```

Interface names vary. Confirm with `iw dev` before running these commands, and do this only on your own adapter.

## The Aircrack-ng suite

| Tool | Purpose |
| --- | --- |
| `airmon-ng` | Manage monitor-mode interfaces |
| `airodump-ng` | Capture and display wireless frames |
| `aireplay-ng` | Inject frames for testing |
| `aircrack-ng` | Analyze captures and test keys |
| `airdecap-ng` | Decrypt captured traffic with a known key |

A safe lab workflow looks like this:

1. Confirm you own the access point and the client.
2. Put the adapter in monitor mode on the correct channel.
3. Capture beacon and handshake frames from your own network.
4. Test the passphrase offline with a small wordlist you generated.
5. Restore managed mode and delete captures.

```bash
sudo airmon-ng start wlan0
sudo airodump-ng wlan0mon
sudo airodump-ng -c 6 --bssid <your-ap-mac> -w lab wlan0mon
```

Do not run deauthentication or injection against devices you do not own. Deauth frames disconnect users and can disrupt emergency or business traffic.

## Fern WiFi Cracker

Fern is a graphical front end for wireless testing. It wraps scanning, capture and cracking workflows. A GUI makes the steps look simple, which is exactly why you should understand what it is doing before clicking.

Use it only against your own lab access point. A GUI does not change the legal boundary.

## Reading wireless results

- A captured handshake does not mean the password is weak.
- A strong passphrase may never fall to a dictionary attack.
- A WEP result demonstrates a broken protocol, not a modern network.
- A "hidden" SSID is not a security control; the name appears in management frames.
- MAC filtering is trivial to bypass and should not be your only control.

## Defending a wireless network

| Control | Why it helps |
| --- | --- |
| WPA3 or WPA2-AES | Removes WEP/TKIP weaknesses |
| Long random passphrase | Makes offline guessing impractical |
| Disable WPS | WPS PINs have a history of weaknesses |
| Firmware updates | Patches known AP vulnerabilities |
| PMF | Protects management frames |
| Strong admin credentials | Prevents router takeover |
| Guest network isolation | Limits lateral movement |
| Monitoring / WIDS | Detects rogue APs and deauth floods |
| 802.1X for business | Centralized identity and revocation |
| Disable unused services | Reduces attack surface |

For a home network, the practical list is: WPA3 if supported, a long unique passphrase, updated firmware, WPS off, a separate guest network for IoT devices, and no remote administration from the internet.

## Practice exercises

1. List the wireless interfaces on your own machine and their supported modes.
2. Explain why WEP is broken and why WPA2-PSK is still common.
3. Draw the WPA2 4-way handshake at a high level.
4. Capture beacons from your own AP and identify the channel, BSSID and security flags.
5. Compare WPA2-PSK and WPA3-SAE in one paragraph.
6. Write a wireless hardening checklist for a small office.

## Next steps

- Continue to [Web application security]({{ '/docs/web-application-security/' | relative_url }}).
- Review the wireless chapters starting at [Chapter 67]({{ '/lessons/lesson-067/' | relative_url }}).
- Confirm hardware and legal limits with the [lab checklist]({{ '/resources/lab-checklist/' | relative_url }}).
