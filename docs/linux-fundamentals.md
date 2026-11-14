---
layout: doc
title: "Linux Fundamentals for Ethical Hackers"
description: "Learn the Linux skills the Kali course depends on: navigation, files, permissions, users, processes, packages, pipes and safe command-line habits."
permalink: /docs/linux-fundamentals/
eyebrow: "Documentation"
last_modified: 2026-11-14
---

## The terminal is the job

Security tools are usually command-line programs. They produce text, accept options and expect you to understand paths, permissions and processes. That is why the course spends fifteen chapters on Linux before it introduces a scanner.

This guide is a compact reference for those chapters. It is not a complete Linux course, but it covers the concepts you will use every day.

<div class="notice notice-warning"><p><strong>Destructive commands:</strong> <code>rm</code>, <code>dd</code>, <code>mkfs</code> and redirections can destroy data instantly. Read the path twice, use a lab VM, and keep a snapshot.</p></div>

## The file system

Linux arranges everything under a single root, `/`. There are no drive letters.

| Path | Purpose |
| --- | --- |
| `/` | Root of the file system |
| `/home/<user>` | Your personal files |
| `/root` | Home directory of the root user |
| `/etc` | System configuration |
| `/var` | Logs, caches and variable data |
| `/tmp` | Temporary files, often cleared on reboot |
| `/usr/bin` | Most installed programs |
| `/bin` | Essential user binaries |
| `/sbin` | System administration binaries |
| `/opt` | Optional third-party software |
| `/dev` | Device files |
| `/proc` | Kernel and process information |

### Navigation

```bash
pwd                 # print the current directory
ls -la              # list all files, including hidden ones, with details
cd /etc             # change to an absolute path
cd ..               # go to the parent directory
cd ~                # go to your home directory
cd -                # return to the previous directory
```

### Files and directories

```bash
mkdir -p lab/notes          # create nested directories
touch notes.txt             # create an empty file or update its timestamp
cp file.txt backup.txt      # copy a file
cp -r lab lab-backup        # copy a directory recursively
mv old.txt new.txt          # rename or move
rm notes.txt                # delete a file
rmdir empty-dir             # remove an empty directory
```

`rm` does not use a recycle bin. `rm -rf` is recursive and forced: it deletes a directory tree without prompts and ignores missing files. Never combine it with an unchecked variable, a wildcard or `/`.

### Finding things

```bash
find /var/log -name "*.log" -type f
locate nmap
sudo updatedb
grep -R "PermitRootLogin" /etc/ssh/
```

`locate` uses a database and is fast but can be stale; `find` walks the file system live and is slower but accurate.

## Viewing and filtering text

```bash
cat /etc/hosts
less /var/log/syslog
head -n 20 file.txt
tail -f /var/log/auth.log
wc -l file.txt
```

Pipes connect programs:

```bash
cat /etc/passwd | cut -d: -f1 | sort
grep -i "failed" /var/log/auth.log | tail -n 20
ps aux | grep ssh | grep -v grep
```

Redirection writes output to a file:

```bash
command > output.txt      # overwrite
command >> output.txt     # append
command 2> error.txt      # redirect stderr
command > all.txt 2>&1    # redirect both
```

Be careful with `>`: it truncates the target before the command runs. If you type the wrong filename, you can empty a file.

## Permissions

Every file has an owner, a group and three permission sets: user, group and other. `ls -l` shows them:

```text
-rwxr-x---  1 alice analysts 1234 Nov 14 10:00 scan.sh
```

The ten characters are:

| Position | Meaning |
| --- | --- |
| 1 | File type (`-` file, `d` directory, `l` symlink) |
| 2–4 | Owner: read, write, execute |
| 5–7 | Group: read, write, execute |
| 8–10 | Other: read, write, execute |

Numeric permissions add read (4), write (2) and execute (1):

```bash
chmod 750 scan.sh      # owner rwx, group r-x, other none
chmod u+x scan.sh      # add execute for the owner
chmod g-w scan.sh      # remove write from the group
chmod o=r scan.sh      # set other to read only
```

Change ownership:

```bash
sudo chown alice:analysts scan.sh
```

`chmod 777` gives everyone read, write and execute. It is almost always the wrong fix. If a service cannot read a file, grant the minimum permission the service account needs.

### Why "Permission denied" happens

- You are not the owner and the group/other bits do not allow the action.
- You are trying to execute a file without execute permission.
- The directory path itself lacks execute permission, so you cannot traverse it.
- A security module (AppArmor, SELinux) or a mount option is blocking access.

Read the error and check the full path, not just the final file.

## Users and groups

```bash
whoami
id
sudo adduser analyst
sudo usermod -aG sudo analyst
su - analyst
sudo passwd analyst
```

`su -` starts a login shell as another user. `sudo` runs a single command with elevated privileges. Prefer `sudo` over a permanent root shell, and never run a graphical browser as root.

The sudoers file controls who may use `sudo`:

```bash
sudo visudo
```

Edit it with `visudo`, which validates syntax before saving. A broken sudoers file can lock you out.

## Processes and services

```bash
ps aux
top
pgrep -a firefox
kill <pid>
sudo systemctl status ssh
sudo systemctl restart ssh
sudo systemctl enable --now ssh
```

Signals matter: `kill` sends TERM by default, which asks a process to stop. `kill -9` forces it and can leave files or services in a bad state. Try TERM first.

Check listening services:

```bash
ss -tulpn
```

This shows TCP and UDP listeners, the numeric ports and the owning process. It is one of the first commands to run on an unfamiliar system.

## Packages

Kali is Debian-based, so it uses `apt` and `dpkg`.

```bash
sudo apt update
apt search nmap
apt show nmap
sudo apt install nmap
sudo apt remove nmap
sudo apt full-upgrade
dpkg -l | grep nmap
```

Install only what you need. Every extra package expands the attack surface and the time you spend maintaining it.

## Shell shortcuts

| Shortcut | Action |
| --- | --- |
| `Tab` | Complete a command, path or option |
| `Ctrl+R` | Search command history |
| `Ctrl+C` | Interrupt the foreground process |
| `Ctrl+Z` | Suspend the foreground process |
| `Ctrl+L` | Clear the screen |
| `Ctrl+A` / `Ctrl+E` | Jump to start / end of the line |
| `!!` | Repeat the last command |
| `history` | Show command history |

Tab completion is a safety feature. It reduces typos in paths that you are about to modify.

## A first script

```bash
#!/usr/bin/env bash
set -euo pipefail

target="${1:-127.0.0.1}"
echo "Checking ${target}"
ping -c 2 "${target}"
```

Save it as `check.sh`, make it executable with `chmod +x check.sh`, and run `./check.sh 192.168.56.10`. `set -euo pipefail` stops on errors, undefined variables and failed pipes.

## Practice exercises

1. Create `~/lab/notes`, add three text files, then list them with sizes.
2. Change a file to `640` and explain who can read and write it.
3. Create a user, add them to a group and test access with `id`.
4. Find the five largest files under `/var/log`.
5. Show all listening TCP ports and identify one service.
6. Write a script that accepts a host and prints its route.

## Next steps

- Continue to [Networking basics]({{ '/docs/networking-basics/' | relative_url }}).
- Use the [cheat sheet]({{ '/resources/cheat-sheet/' | relative_url }}) while practising.
- Review the Linux chapters starting at [Chapter 5]({{ '/lessons/lesson-005/' | relative_url }}).
