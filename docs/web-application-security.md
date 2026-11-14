---
layout: doc
title: "Web Application Security: XSS, SQL Injection & Burp Suite"
description: "Learn web application security fundamentals: HTTP, Burp Suite, XSS, SQL injection, DVWA, SQLMap, jSQL, sqlsus, Wireshark and the OWASP Top 10."
permalink: /docs/web-application-security/
eyebrow: "Documentation"
last_modified: 2026-11-14
---

## The web is the largest attack surface

Most organizations expose a web application to the internet. That makes web security the highest-value module in the course — and the easiest place to cross a legal line. Testing a public site without permission is unauthorized access, even if you only send a harmless-looking payload.

This guide explains the concepts behind the web chapters. Practise against DVWA, OWASP Juice Shop or another deliberately vulnerable app on your own machine.

<div class="notice notice-legal"><p><strong>Use a target you own.</strong> A reflected XSS payload or SQL injection string sent to a live third-party site can be a crime. Keep the lab isolated and never test a public site "just to see".</p></div>

## HTTP refresher

A web interaction is a request and a response. Important request parts:

- **Method** — GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD.
- **URL and query string** — path plus parameters.
- **Headers** — cookies, content type, authorization, user agent.
- **Body** — form data, JSON, multipart uploads.

Important response parts:

- **Status code** — 200, 301, 302, 400, 401, 403, 404, 500.
- **Headers** — content type, caching, cookies, security headers.
- **Body** — HTML, JSON, files.

Useful inspection commands:

```bash
curl -I http://192.168.56.10/
curl -v http://192.168.56.10/login
curl -s -o /dev/null -w "%{http_code}\n" http://192.168.56.10/
```

## Cookies and sessions

A session cookie identifies an authenticated user. If an attacker steals it, they may be able to act as that user without knowing the password.

Cookie protections:

| Attribute | Effect |
| --- | --- |
| `HttpOnly` | JavaScript cannot read the cookie |
| `Secure` | Cookie is sent only over HTTPS |
| `SameSite=Lax` / `Strict` | Reduces cross-site request forgery |
| `Path` | Limits where the cookie is sent |
| Expiry | Limits the window of theft |

`HttpOnly` reduces the impact of XSS but does not fix it. XSS can still perform actions in the page, read data from the DOM and steal non-HttpOnly tokens.

## Burp Suite

Burp Suite is an intercepting proxy. It sits between the browser and the target so you can inspect and modify requests.

Basic setup:

1. Start Burp and confirm the proxy listener, usually `127.0.0.1:8080`.
2. Configure the browser to use that proxy for the lab target.
3. Install Burp's CA certificate in the browser so HTTPS interception works.
4. Browse the lab app with the proxy on.
5. Use **Proxy → HTTP history** to inspect requests.
6. Use **Repeater** to modify and resend a single request.
7. Use **Intruder** only in a lab and with rate limits; it generates many requests.

Burp Community has limitations, but the core proxy, Repeater and decoder are enough for learning. The official [Burp documentation](https://portswigger.net/burp/documentation) is the primary reference.

## Cross-site scripting (XSS)

XSS occurs when untrusted input is rendered as executable content in a victim's browser.

| Type | Where the payload lives | Example |
| --- | --- | --- |
| Reflected | In the request, reflected in the response | Search parameter echoed into HTML |
| Stored | Saved by the app, served to other users | Comment field rendered without encoding |
| DOM-based | Processed by client-side JavaScript | `innerHTML` with a URL fragment |

A harmless lab payload used in DVWA might be:

```html
<script>alert('lab')</script>
```

That is a test marker, not a real attack. In a real finding, demonstrate impact with the minimum proof required, and never target a real user.

### Why it works

- Output is inserted into HTML without context-aware encoding.
- Input is placed inside an attribute or script block where escaping differs.
- Client-side code writes untrusted data into `innerHTML`, `document.write` or similar sinks.
- A Content Security Policy is missing or too permissive.

### How to fix it

- Encode output for the correct context (HTML, attribute, JavaScript, URL, CSS).
- Use templating engines with auto-escaping and avoid raw HTML sinks.
- Validate input on the server, but do not rely on validation alone.
- Add a strict Content Security Policy as defence in depth.
- Set cookies `HttpOnly`, `Secure` and `SameSite`.
- Test with a browser and a proxy, not just a scanner.

## SQL injection

SQL injection occurs when user input changes the structure of a database query.

| Type | Signal |
| --- | --- |
| In-band / union | Query results are returned in the page |
| Error-based | Database errors reveal structure |
| Boolean-based blind | Page changes true/false |
| Time-based blind | Response time changes with a condition |
| Out-of-band | Data leaves through DNS or HTTP |

A lab test might add a quote to a parameter and observe an error or a change in results. The goal is to prove that input reaches the query unsafely, then show impact with minimal data access.

### SQLMap

SQLMap automates detection and exploitation of SQL injection.

```bash
sqlmap -u "http://192.168.56.10/vulnerabilities/sqli/?id=1&Submit=Submit" --batch
sqlmap -r request.txt --batch
sqlmap -u "<lab-url>" --dbs
```

Use it only against DVWA or another lab target. SQLMap can extract entire databases, write files and attempt command execution. Those features are dangerous and unnecessary for a beginner exercise.

Start with detection and database enumeration, then stop. Read the official [sqlmap wiki](https://github.com/sqlmapproject/sqlmap/wiki) before using advanced options.

### jSQL Injection

jSQL is a graphical, Java-based SQL injection tool. It provides a visual way to test parameters, enumerate databases and extract data. The same legal boundary applies: lab only.

### sqlsus

sqlsus is a MySQL-focused injection tool with an interactive shell and configuration file. It is useful for understanding MySQL-specific workflows, and it reinforces why parameterized queries matter.

### How to fix SQL injection

- Use parameterized queries / prepared statements.
- Use an ORM correctly, without string concatenation.
- Apply least-privilege database accounts.
- Validate and constrain input types.
- Avoid detailed database errors in production.
- Add a WAF as defence in depth, not as the primary fix.

## Wireshark and traffic analysis

Wireshark captures and inspects packets. For web work it helps you see what actually left the browser: headers, cookies, redirects, TLS handshakes and timing.

Useful filters:

```text
http
http.request.method == "POST"
tls.handshake.type == 1
dns.qry.name contains "example"
ip.addr == 192.168.56.10
```

Capture only your own lab traffic. On a shared network, capturing other users' traffic can violate privacy law. See the official [Wireshark user's guide](https://www.wireshark.org/docs/wsug_html_chunked/).

## OWASP Top 10 as a map

The OWASP Top 10 is an awareness document, not a checklist. It groups common categories such as broken access control, cryptographic failures, injection, insecure design, security misconfiguration, vulnerable components, identification and authentication failures, software and data integrity failures, logging failures and SSRF.

Use it to organize findings, then read the detailed OWASP pages for the specific issue.

## Secure development habits

- Threat-model the feature before writing code.
- Treat all input as untrusted.
- Prefer well-maintained libraries and patch them.
- Use secure defaults and fail closed.
- Log security events without logging secrets.
- Test authorization on every endpoint, not just authentication.
- Add automated tests for injection and access control.
- Run dependency and container scans in CI.

## Practice exercises

1. Configure Burp and capture a login request in DVWA.
2. Identify a reflected XSS in DVWA and write the context-aware fix.
3. Use SQLMap against DVWA to list databases, then stop.
4. Compare a vulnerable query with a parameterized version.
5. Capture a DVWA request in Wireshark and identify the HTTP method and cookie.
6. Map three DVWA findings to OWASP Top 10 categories.
7. Write a remediation ticket for one finding, including a test plan.

## Next steps

- Review the web chapters starting at [Chapter 41]({{ '/lessons/lesson-041/' | relative_url }}).
- Read [Vulnerability analysis]({{ '/docs/vulnerability-analysis/' | relative_url }}) for reporting.
- Keep the [lab checklist]({{ '/resources/lab-checklist/' | relative_url }}) beside you.
