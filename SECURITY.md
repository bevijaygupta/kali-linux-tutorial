# Security policy

## Scope

This policy covers the **repository and website**:

- Python scripts, GitHub Actions workflows and automation.
- Jekyll layouts, includes, CSS, JavaScript and generated site output.
- Supply-chain, secret-handling and deployment configuration.
- Content that could cause harm, such as dangerous instructions, leaked credentials or missing safety warnings.

It does **not** cover the YouTube videos, the EINITIAL24 Academy channel, Kali Linux, OffSec or any third-party tool. Report issues in those products to their respective owners.

## Reporting a vulnerability

Please do **not** open a public issue for:

- A leaked secret, token or credential.
- A vulnerability in the site or automation that could be exploited.
- A safety problem that could lead someone to damage a system or break the law.
- Personal data that should not be public.

Use GitHub's **private vulnerability reporting** for this repository:

1. Open the repository's **Security** tab.
2. Choose **Advisories → Report a vulnerability**.
3. Describe the issue, the affected file or URL, and the impact.
4. Include reproduction steps only if they are safe and do not target a third party.

If private reporting is unavailable, contact a repository maintainer directly on GitHub and ask for a private channel. Do not include secrets in the first public message.

## What to include

A useful report contains:

- A clear description of the problem and why it matters.
- The affected path, URL, workflow or commit.
- Safe reproduction steps or a proof of concept that does not harm a real system.
- The potential impact and any preconditions.
- Whether the issue is already public.
- A suggested fix, if you have one.

Do not access, modify or exfiltrate data that is not yours. Do not test against third-party systems. If you encounter a real secret, stop, do not copy it, and report its location.

## Response process

This is a volunteer-maintained educational project. Reports are reviewed on a best-effort basis; no response time or bounty is promised.

When a report is received, maintainers will:

1. Acknowledge the report when possible.
2. Assess scope and impact.
3. Remove or rotate exposed secrets and fix the issue.
4. Coordinate disclosure with the reporter when appropriate.
5. Credit the reporter if they want credit.

Please allow reasonable time for a fix before public disclosure.

## Safe harbour

We support good-faith security research on this repository. We will not pursue action against researchers who:

- test only their own copy or a local deployment;
- avoid privacy violations, data destruction and service disruption;
- report findings privately and give maintainers time to respond;
- do not use the research to harm others.

This safe harbour applies to this repository only. It does not authorize testing of YouTube, GitHub, OffSec or any third-party service.

## Content safety reports

If a lesson or resource contains a command that could cause harm without adequate warning, or if a page encourages unauthorized activity, report it. Include the page URL and the specific sentence or command. Safety corrections are treated as high priority.

## Secrets and credentials

Never commit real API keys, passwords, tokens, private keys or personal data. Use `.env` locally and GitHub Actions secrets in CI. If a secret is exposed:

1. Revoke or rotate it immediately at the provider.
2. Remove it from the current tree.
3. Report the exposure privately.
4. Assume the value is compromised even if the commit is later rewritten.

## Supported versions

This repository is a continuously updated educational project. Fixes are applied to the `main` branch. There are no long-term support branches.
