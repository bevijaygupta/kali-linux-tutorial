---
layout: page
hide_title: true
title: "Kali Linux Command Cheat Sheet (Safe Lab Reference)"
description: "A compact Kali Linux cheat sheet: file navigation, permissions, networking, Nmap, web tools, password tools and wireless commands for authorized labs."
permalink: /resources/cheat-sheet/
section: "Resources"
section_url: "/resources/"
last_modified: 2026-11-14
---

# Kali Linux command cheat sheet

A syntax reference for the commands used in the course. It is deliberately conservative: destructive options are marked, and nothing here is a target list.

<div class="notice notice-warning"><p><strong>Read before running:</strong> commands that change state are marked <strong>⚠</strong>. Run them only in a snapshot-backed lab VM. When in doubt, run <code>man &lt;tool&gt;</code> and read the options first.</p></div>

## Navigation and files

| Command | Purpose |
| --- | --- |
| `pwd` | Print the working directory |
| `ls -la` | List all files, including hidden, with details |
| `cd /path` | Change directory |
| `cd ..` / `cd ~` / `cd -` | Parent / home / previous directory |
| `mkdir -p a/b/c` | Create nested directories |
| `touch file` | Create an empty file |
| `cp file copy` | Copy a file |
| `cp -r dir copy` | Copy a directory recursively |
| `mv old new` | Move or rename |
| `rm file` | Delete a file ⚠ |
| `rm -ri dir` | Recursive delete with prompts ⚠ |
| `rm -rf dir` | Recursive forced delete — irreversible ⚠⚠ |
| `find /path -name "*.log"` | Find files by name |
| `locate name` | Search the locate database |
| `sudo updatedb` | Refresh the locate database |
| `du -sh dir` | Directory size |
| `df -h` | Disk usage by file system |
| `tree -L 2` | Directory tree (if installed) |

## Text and pipelines

| Command | Purpose |
| --- | --- |
| `cat file` | Print a file |
| `less file` | Page through a file |
| `head -n 20 file` | First 20 lines |
| `tail -f log` | Follow a growing log |
| `grep -i "text" file` | Case-insensitive search |
| `grep -R "text" dir` | Recursive search |
| `wc -l file` | Count lines |
| `sort file` | Sort lines |
| `sort -n` / `sort -r` / `sort -u` | Numeric / reverse / unique |
| `uniq -c` | Count repeated adjacent lines |
| `cut -d: -f1` | Cut fields by delimiter |
| `awk '{print $1}'` | Print a column |
| `cmd > file` | Overwrite redirect ⚠ |
| `cmd >> file` | Append redirect |
| `cmd 2>&1` | Merge stderr into stdout |
| `cmd1 \| cmd2` | Pipe output |

## Permissions and users

| Command | Purpose |
| --- | --- |
| `ls -l` | Show owner, group and mode |
| `chmod 750 file` | Set numeric permissions ⚠ |
| `chmod u+x file` | Add execute for the owner ⚠ |
| `chmod g-w file` | Remove group write ⚠ |
| `chown user:group file` | Change ownership ⚠ |
| `umask` | Show the default permission mask |
| `whoami` / `id` | Current user and groups |
| `sudo adduser name` | Create a user ⚠ |
| `sudo usermod -aG sudo name` | Add a user to sudo ⚠ |
| `sudo passwd name` | Change a password ⚠ |
| `su - name` | Start a login shell as another user |
| `sudo -l` | List allowed sudo commands |
| `sudo visudo` | Edit sudoers safely ⚠ |

## Processes and services

| Command | Purpose |
| --- | --- |
| `ps aux` | List processes |
| `top` / `htop` | Live process view |
| `pgrep -a name` | Find a process by name |
| `kill PID` | Send TERM to a process ⚠ |
| `kill -9 PID` | Force kill — last resort ⚠ |
| `systemctl status ssh` | Service status |
| `sudo systemctl restart ssh` | Restart a service ⚠ |
| `systemctl list-units --type=service` | List services |
| `ss -tulpn` | Listening TCP/UDP ports |
| `lsof -i :80` | Process using a port |

## Packages

| Command | Purpose |
| --- | --- |
| `sudo apt update` | Refresh package indexes ⚠ |
| `apt search name` | Search packages |
| `apt show name` | Package details |
| `sudo apt install name` | Install a package ⚠ |
| `sudo apt remove name` | Remove a package ⚠ |
| `sudo apt full-upgrade` | Upgrade with dependency changes ⚠ |
| `dpkg -l` | List installed packages |
| `dpkg -S /path/file` | Which package owns a file |

## Networking

| Command | Purpose |
| --- | --- |
| `ip address` | Show interfaces and addresses |
| `ip route` | Show the routing table |
| `ip neigh` | Show the ARP/neighbour table |
| `ping -c 3 host` | Test reachability |
| `traceroute host` | Trace the route |
| `ss -tulpn` | Listening ports |
| `dig example.com A` | DNS A record |
| `dig +short example.com` | Short DNS answer |
| `nslookup example.com` | Query DNS |
| `curl -I https://host` | Fetch headers only |
| `curl -v https://host` | Verbose request |
| `wget URL` | Download a file |
| `nc -zv host port` | Test a TCP port |
| `sudo tcpdump -i eth0 -c 20` | Capture 20 packets ⚠ |
| `sudo tcpdump -i eth0 port 53 -w dns.pcap` | Capture DNS to a file ⚠ |

## Anonymity and routing (concepts)

| Command | Purpose |
| --- | --- |
| `proxychains4 command` | Run a command through configured proxies |
| `sudo systemctl status tor` | Check the Tor service |
| `curl --socks5-hostname 127.0.0.1:9050 URL` | Request through a local SOCKS proxy |
| `macchanger -s eth0` | Show the current MAC |
| `sudo macchanger -r eth0` | Randomize the MAC in a lab ⚠ |
| `openvpn --config file.ovpn` | Connect a VPN ⚠ |

A proxy, VPN or Tor circuit does not create authorization and does not guarantee anonymity. See [Networking basics]({{ '/docs/networking-basics/' | relative_url }}).

## Reconnaissance

| Command | Purpose |
| --- | --- |
| `whois example.com` | Registration data (often redacted) |
| `dig example.com NS` | Name servers |
| `dig example.com MX` | Mail servers |
| `dnsenum example.com` | DNS enumeration |
| `dnsmap example.com -w wordlist` | Subdomain wordlist scan |
| `dnstracer example.com` | Trace DNS delegation |
| `whatweb http://lab/` | Web technology fingerprint |
| `dirb http://lab/ wordlist` | Web path brute force ⚠ |
| `nmap -sn 192.168.56.0/24` | Host discovery |
| `nmap -sT 192.168.56.10` | TCP connect scan |
| `sudo nmap -sS 192.168.56.10` | SYN scan |
| `sudo nmap -sU --top-ports 20 host` | UDP top ports |
| `nmap -sV -p 22,80,443 host` | Service versions |
| `nmap -sC -sV host` | Default scripts + versions |
| `nmap -A host` | Aggressive scan ⚠ |
| `nmap -p- host` | All TCP ports (slow) |
| `nmap -oA name host` | Save normal, XML and grepable output |

Only scan lab targets or systems covered by written authorization.

## Web and vulnerability analysis

| Command | Purpose |
| --- | --- |
| `nikto -h http://lab/` | Web server checks |
| `searchsploit apache 2.4` | Search Exploit-DB locally |
| `searchsploit -m ID` | Copy an exploit for study ⚠ |
| `sudo lynis audit system` | Linux hardening audit |
| `sqlmap -u "http://lab/?id=1" --batch` | SQL injection test (lab only) ⚠ |
| `curl -I http://lab/` | Inspect headers |
| `curl -s http://lab/robots.txt` | Fetch robots.txt |

## Password tools (lab only)

| Command | Purpose |
| --- | --- |
| `hash-identifier` | Guess a hash type |
| `cewl https://lab/ -w words.txt` | Build a wordlist from a site |
| `crunch 8 10 -t pass%%%% -o list.txt` | Pattern wordlist |
| `john --wordlist=list.txt hashes.txt` | Offline crack ⚠ |
| `john --show hashes.txt` | Show recovered passwords |
| `hashcat -m 0 -a 0 hashes.txt list.txt` | GPU dictionary attack ⚠ |
| `hydra -L users.txt -P list.txt ssh://lab` | Online SSH test (lab only) ⚠ |
| `medusa -h lab -U users.txt -P list.txt -M ssh` | Online test (lab only) ⚠ |

Never run online password attacks against accounts you do not own. They can lock out real users and are illegal without authorization.

## Wireless (own equipment only)

| Command | Purpose |
| --- | --- |
| `iw dev` | List wireless interfaces |
| `iw list` | Show supported modes |
| `sudo airmon-ng start wlan0` | Start monitor mode ⚠ |
| `sudo airodump-ng wlan0mon` | Capture wireless frames ⚠ |
| `sudo airmon-ng stop wlan0mon` | Stop monitor mode |
| `sudo ip link set wlan0 down` | Bring an interface down ⚠ |
| `sudo iw dev wlan0 set type managed` | Return to managed mode ⚠ |

Radio interception is regulated. Capture only your own lab network.

## Getting help

| Command | Purpose |
| --- | --- |
| `man tool` | Full manual |
| `tool --help` | Quick usage |
| `apropos keyword` | Find manuals by keyword |
| `info tool` | GNU info pages |
| `history \| grep tool` | Find a previous command |

Official documentation is preferred. See [official links]({{ '/resources/official-links/' | relative_url }}).

## Related guides

- [Linux fundamentals]({{ '/docs/linux-fundamentals/' | relative_url }})
- [Networking basics]({{ '/docs/networking-basics/' | relative_url }})
- [Reconnaissance]({{ '/docs/reconnaissance/' | relative_url }})
- [Web application security]({{ '/docs/web-application-security/' | relative_url }})
- [Lab checklist]({{ '/resources/lab-checklist/' | relative_url }})
