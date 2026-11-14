---
layout: doc
title: "Password Attacks Explained: Hashing, Wordlists & Defense"
description: "Learn how password attacks work: hashing and salts, wordlists, John the Ripper, Hashcat, Hydra and Medusa, plus practical account protection."
permalink: /docs/password-attacks/
eyebrow: "Documentation"
last_modified: 2026-11-14
---

## Why passwords still matter

Passwords remain a common initial access path because people reuse them, choose predictable patterns and store them in insecure places. Understanding password attacks helps you defend accounts, design authentication and evaluate risk — not just run a cracker.

This guide covers the concepts in the password module. It does not include real credential dumps, hashes or target lists.

<div class="notice notice-legal"><p><strong>Authorized testing only.</strong> Online password attacks against accounts you do not own are illegal and can lock out real users. Offline cracking of hashes you do not own may also violate law and policy. Use generated lab hashes and your own test accounts.</p></div>

## Authentication, hashing and encryption

- **Hashing** is a one-way transformation. The same input produces the same output, but you cannot reverse the output to recover the input.
- **Encryption** is reversible with a key. It protects confidentiality, not password verification.
- **Salting** adds unique random data to each password before hashing, so identical passwords produce different hashes.
- **Key stretching** deliberately makes each hash computation slow (bcrypt, scrypt, Argon2) to raise the cost of guessing.

A password hash is not "encrypted password". If a website can email you your password, it is storing it reversibly or in plaintext — a serious design flaw.

## Common hash formats

| Format | Typical prefix / shape | Notes |
| --- | --- | --- |
| MD5 | 32 hex characters | Fast, obsolete for passwords |
| SHA-1 | 40 hex characters | Fast, deprecated for passwords |
| SHA-256 | 64 hex characters | Fast, not ideal for passwords |
| bcrypt | `$2a$`, `$2b$`, `$2y$` | Slow, salted |
| scrypt | `$scrypt$` | Memory-hard |
| Argon2 | `$argon2id$` | Modern password hashing |
| SHA-512 crypt | `$6$` | Common on Linux |
| NetNTLM | 32 hex characters | Windows challenge-response, not a password hash in the same sense |

`hash-identifier` guesses the likely type from the format. It is a heuristic, not proof. Verify against the source system or documentation.

```bash
hash-identifier
```

Paste a generated lab hash interactively. Do not paste real user hashes into a third-party service.

## How cracking works

A cracker guesses a password, hashes it with the same algorithm and parameters, and compares the result with the target hash.

| Attack | How it works | Defence |
| --- | --- | --- |
| Dictionary | Tries words from a list | Long unique passphrases, rate limits |
| Rule-based | Applies mutations (`P@ssw0rd!`) | Avoid predictable substitutions |
| Brute force | Tries every combination | Length and slow hashing |
| Mask | Limits the character set and pattern | Same, plus MFA |
| Hybrid | Wordlist plus mutations | Same |
| Credential stuffing | Reuses leaked passwords | Unique passwords, breach monitoring |
| Password spraying | Tries a few common passwords across many accounts | Lockout policy, MFA, anomaly detection |

Offline cracking is limited by hash algorithm, password entropy and hardware. Online attacks are limited by network latency, lockouts and monitoring. Both are expensive at scale when defences are correct.

## Wordlists

A wordlist is only useful if it matches the target's language, culture and patterns. The course covers CEWL (custom words from a website) and Crunch (pattern generation).

```bash
cewl https://lab.example -d 2 -m 5 -w custom.txt
crunch 8 10 -t pass%%%% -o patterns.txt
```

- `cewl` crawls a site you are authorized to crawl. It can generate a large list and cause load.
- `crunch` can generate enormous files. Estimate the size before writing millions of candidates:

```bash
crunch 8 8 -t pass%%%% -c 100000
```

`-c` counts lines without writing the file. A full 8-character lowercase keyspace is 208 billion combinations; that is not a practical wordlist.

Kali includes wordlists under `/usr/share/wordlists/`, but check the licence and contents before use. Do not redistribute lists that contain personal data.

## John the Ripper

John is a versatile offline cracker with format detection and rule support.

```bash
john --list=formats
john --wordlist=custom.txt hashes.txt
john --show hashes.txt
```

For a specific format:

```bash
john --format=raw-sha256 --wordlist=custom.txt hashes.txt
```

Use a generated hash in a lab. John can also apply rules:

```bash
john --wordlist=custom.txt --rules hashes.txt
```

Rules multiply the candidate count. Start small and measure the cracking rate before committing to a long run.

## Hashcat

Hashcat is GPU-accelerated and supports a very large set of hash modes.

```bash
hashcat -m 0 -a 0 hashes.txt custom.txt
hashcat -m 0 -a 0 hashes.txt custom.txt --show
hashcat -m 0 -a 3 hashes.txt ?a?a?a?a
```

- `-m` selects the hash mode; `0` is MD5, used here only as an example.
- `-a 0` is a straight dictionary attack; `-a 3` is brute force/mask.
- `?a` is all printable ASCII, which grows extremely fast.

Always confirm the mode with the official hashcat example hashes. A wrong mode wastes time or produces false results.

Run cracking only on hardware you own and in a lab. GPU cracking can heat a laptop and consume significant power.

## Online attacks: Hydra and Medusa

Online tools try credentials against a live service such as SSH, FTP or a web login.

```bash
hydra -L users.txt -P passwords.txt ssh://192.168.56.10
medusa -h 192.168.56.10 -U users.txt -P passwords.txt -M ssh
```

These commands should only be run against a lab VM with test accounts. Against a real service they can:

- Lock out legitimate users.
- Trigger alarms and incident response.
- Violate terms of service and law.
- Cause availability problems.

Rate limits matter. A fast attack is noisy; a slow attack is still unauthorized without permission. The right use of these tools is to test your own authentication defences and measure detection.

## Defending accounts

| Control | Effect |
| --- | --- |
| Unique passphrases | Stops credential stuffing |
| Password manager | Makes unique passwords practical |
| MFA / passkeys | Reduces the value of a stolen password |
| Argon2id or bcrypt | Makes offline cracking expensive |
| Rate limiting and lockout | Slows online guessing |
| Breach monitoring | Detects leaked credentials |
| Anomaly detection | Catches spraying and impossible travel |
| Least privilege | Limits what a compromised account can do |
| No password reuse | Breaks cascading compromise |

A password policy that forces `P@ssw0rd1!` every 60 days is worse than a long passphrase with MFA. Modern guidance favours length, uniqueness and breach checks over arbitrary rotation.

## Extracting hashes (lab only)

The course demonstrates Windows SAM and Linux shadow files, and password-protected archives. These exercises require administrative access to a system you own.

- SAM: the Windows account database; extracting it usually requires administrator or offline access.
- `/etc/shadow`: readable only by root on Linux.
- ZIP/RAR: encrypted archives require a dedicated extraction tool before cracking.

Never copy real hashes into a public repository, chat or third-party website. Treat them as credentials.

## Practice exercises

1. Generate a SHA-256 hash of a test password and identify the format.
2. Create a 50-word custom list and crack one generated hash with John.
3. Compare the cracking speed of a fast hash and bcrypt on the same hardware.
4. Explain why salting defeats precomputed rainbow tables.
5. Test a lab SSH account with Hydra at a low rate, then enable rate limiting and observe the difference.
6. Write a one-page password policy for a small organisation.

## Next steps

- Continue to [Wireless security]({{ '/docs/wireless-security/' | relative_url }}).
- Review the password chapters starting at [Chapter 49]({{ '/lessons/lesson-049/' | relative_url }}).
- Use the [cheat sheet]({{ '/resources/cheat-sheet/' | relative_url }}) for syntax, not for targets.
