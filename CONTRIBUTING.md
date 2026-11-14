# Contributing

Thank you for improving the Kali Linux course companion. This project values accurate, verifiable and legally careful material over volume.

## Before you start

- Read the [README](README.md), [SECURITY.md](SECURITY.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- Check existing issues and pull requests so you do not duplicate work.
- For a large change, open an issue first and describe the scope.
- Do not include real credentials, personal data, private IP addresses from someone else's network, target lists or transcripts.

## What we accept

Good contributions include:

- Corrections to factual errors, broken links or outdated commands.
- Clearer explanations of a concept in a lesson or documentation page.
- New official documentation links that are stable and maintained.
- Accessibility, performance and responsive-layout improvements.
- Bug fixes in the Python automation, Jekyll templates or GitHub Actions workflows.
- Safer wording for destructive commands, legal boundaries and lab setup.

We do not accept:

- Transcripts, re-uploaded videos or copied YouTube descriptions.
- Requests or instructions to attack a real third party.
- Real password hashes, credential dumps, API keys or personal data.
- Invented metadata, durations, dates, ratings, view counts or testimonials.
- SEO keyword stuffing, hidden text or doorway pages.
- Changes that push directly to `main` or bypass validation.

## Content rules

1. **Verify before writing.** Prefer official project documentation, standards bodies and vendor advisories. Link the source.
2. **Separate fact from inference.** If a value is unknown, write `null` or say it is unverified. Never guess.
3. **Do not copy the video.** Lesson notes are original explanations. Summarise concepts; do not reproduce a transcript.
4. **Respect scheduled chapters.** A scheduled page must keep `status: "scheduled"`, `duration: null` and `published_date: null`. It must not receive a `VideoObject` or a fabricated publish date.
5. **Keep it lawful.** Every technique must be framed for systems the learner owns or has written permission to test.
6. **Warn about destructive actions.** Mark commands that delete data, change interfaces, spoof traffic, crack credentials or can lock accounts.
7. **Use plain language.** Define jargon on first use and link the [glossary](resources/glossary.md).
8. **Write unique metadata.** Page titles and descriptions must be specific to the page, not duplicated boilerplate.

## Local setup

The Python tooling requires Python 3.11 or newer and no third-party packages.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

For the Jekyll site, install Ruby and Bundler, then:

```bash
bundle install
bundle exec jekyll serve
```

See the README for the full local preview and deployment commands.

## Data and page generation

`data/playlist.json` and `data/curriculum.json` are the source of truth.

- `data/playlist.json` holds verified YouTube metadata and playlist order.
- `data/curriculum.json` holds the authored notes keyed by chapter number.
- `lessons/*.md`, `lessons/index.md`, the README curriculum table, `assets/data/lessons-index.json`, `_data/course.json`, `llms.txt` and `sitemap.xml` are generated.

Do not hand-edit generated lesson pages. Edit the data files and run:

```bash
python scripts/update_repository.py --skip-fetch
```

To refresh playlist metadata first, omit `--skip-fetch`. If YouTube adds a chapter that has no authored notes, the pipeline writes `data/curriculum-drafts.json` and generates a clearly labelled metadata-only page for review.

## Validation

Run the same checks as CI before opening a pull request:

```bash
python scripts/generate_lesson_pages.py --check
python scripts/generate_content.py --check
python scripts/generate_sitemap.py --check
python scripts/validate_links.py --strict
```

The validator checks JSON structure, chapter coverage, required sections, unique titles and descriptions, scheduled-metadata rules, internal links, assets, sitemap coverage and safety notices. A pull request that fails validation will not be merged.

## Pull request checklist

- [ ] The change is scoped and described.
- [ ] Facts and commands have a primary-source link where possible.
- [ ] No transcript, re-hosted video, credential, secret or personal data is included.
- [ ] Destructive or intrusive steps have a clear warning and a lab boundary.
- [ ] Internal links use Liquid `relative_url` in Jekyll pages.
- [ ] Generated files were regenerated, not hand-edited.
- [ ] `python scripts/validate_links.py --strict` passes.
- [ ] The PR template is complete.

## Commit messages

Use short, imperative messages. Examples:

```text
docs: clarify Nmap timing options
fix: correct scheduled lesson null metadata
feat: add lab scope template
chore: refresh playlist metadata
```

Group unrelated changes into separate pull requests when practical.

## Reporting a security problem

Do not open a public issue for a vulnerability in this repository, a leaked secret or a safety problem that could cause harm. Follow [SECURITY.md](SECURITY.md).

## Licence

By contributing, you agree that your code contribution is licensed under the MIT License and your written contribution is licensed under CC BY 4.0, as described in [LICENSE](LICENSE). You confirm that you have the right to submit the material and that it does not contain third-party content under an incompatible licence.
