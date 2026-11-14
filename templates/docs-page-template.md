---
layout: doc
title: "<Topic>: <specific promise, not a generic label>"
description: "<unique 70–175 character summary of what the reader can do after this page>"
permalink: /docs/<slug>/
eyebrow: "Documentation"
last_modified: "<YYYY-MM-DD>"
---

<!--
Documentation page template.

A docs page explains a concept or workflow that spans several chapters. It is
not a transcript, a command dump or a replacement for vendor documentation.
Every page should:
  * solve one clear problem;
  * link to the relevant lessons and primary sources;
  * distinguish verified facts from lab-specific examples;
  * include an authorized-use reminder when the topic is intrusive.
-->

## <Why this matters>

<Open with the problem the reader is trying to solve. Two short paragraphs at most. Explain where this guide sits in the course and what it assumes.>

<div class="notice notice-legal"><p><strong>Authorized use only.</strong> <Adapt this notice if the page discusses scanning, exploitation, credential access, spoofing or wireless capture. Otherwise use a normal informational notice.></p></div>

## <Core concept>

<Explain the mental model. Use a short analogy only if it is accurate. Define terms the first time they appear and link to the [glossary]({{ '/resources/glossary/' | relative_url }}).>

### <Subtopic>

<Details, examples or a table. Prefer small tables over long bullet lists when comparing options.>

| Option | When to use it | Risk or limitation |
| --- | --- | --- |
| <Option A> | <Use case> | <Limitation> |
| <Option B> | <Use case> | <Limitation> |

## <Workflow or lab example>

<Describe the safe lab version. Name the scope, the expected observation and the rollback step. Avoid commands that target public systems.>

```bash
# Lab-only example. Replace the placeholder target with your own VM.
<command> <lab-target>
```

<div class="notice notice-warning"><p><strong>Watch the blast radius:</strong> <What can this command change? What should the reader check first? When should they stop?></p></div>

## <Common mistakes>

- **<Mistake>** — <Why it happens and how to avoid it.>
- **<Mistake>** — <Why it happens and how to avoid it.>
- **<Mistake>** — <Why it happens and how to avoid it.>

## <Defensive perspective>

<Explain how a defender detects, prevents or limits the issue. This section is mandatory for offensive topics: it keeps the page balanced and useful.>

## Related lessons and guides

- [Chapter <n>: <title>]({{ '/lessons/lesson-<n>/' | relative_url }})
- [<Related docs page>]({{ '/docs/<slug>/' | relative_url }})
- [<Resource>]({{ '/resources/<slug>/' | relative_url }})

## Primary sources

- [<Official documentation>](https://<official-source>)
- [<Standard or specification>](https://<official-source>)

## Continue learning

<One or two sentences pointing to the next logical guide or module. Use a Liquid `relative_url` link.>
