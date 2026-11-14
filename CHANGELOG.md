# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html) for the automation and site tooling. Written lesson content may be corrected at any time without a version bump.

## [Unreleased]

### Planned

- Author full notes for scheduled chapters as they are published and reviewed.
- Add a captioned walkthrough for the local Jekyll preview.
- Expand the glossary with terms requested through issues.

## [1.0.0] — 2026-11-14

### Added

- Initial public study companion for the EINITIAL24 Academy **Kali Linux Complete Course**.
- Verified metadata for **76 chapters** in `data/playlist.json`, preserving the original newest-first playlist positions: **47 published** and **29 scheduled** at the time of extraction.
- Authored curriculum notes for all 76 chapters in `data/curriculum.json`, grouped into nine learning modules.
- Generated lesson pages in `lessons/` with Watch, About, What You Will Learn, Important Concepts, Practical Notes, Related Lessons, Additional Resources, FAQ and Continue Learning sections.
- Lesson index, README curriculum table, search index and `llms.txt` generators.
- Jekyll site with dark and light themes, orange `#E65616` accent, responsive layout, lesson search, breadcrumbs, table of contents, reading progress and YouTube call-to-action.
- 13 documentation pages covering getting started, installation, lab setup, Linux fundamentals, networking, reconnaissance, vulnerability analysis, exploitation basics, password attacks, wireless security, web application security and an eight-week study roadmap.
- Four resources: a command cheat sheet, a lab checklist with a scope template, a primary-source link collection and a glossary.
- Structured data for Organization, WebSite, Course, BreadcrumbList, Article and verified VideoObject entries.
- Static `sitemap.xml`, `robots.txt`, a no-indexed 404 page and canonical/Open Graph/Twitter metadata through `jekyll-seo-tag`.
- Python automation: playlist fetch, page generation, content generation, sitemap generation, validation and an update orchestrator.
- GitHub Actions workflows for validation, weekly playlist updates through pull requests, and GitHub Pages deployment.
- Issue templates, pull request template, contribution guide, code of conduct, security policy and dual MIT/CC BY 4.0 licensing.
- Generated banner, social preview, roadmap and logo assets.

### Security

- Scheduled chapters never receive a fabricated duration, publish date or `VideoObject`.
- Lesson pages include authorized-use notices and destructive-command warnings.
- The update workflow opens a pull request instead of pushing to `main`.
- Optional API keys are read from environment variables or GitHub Actions secrets; no credentials are committed.

### Known limitations

- The 29 scheduled chapters use their official descriptions and course outline for context; they will be reviewed when video footage is available.
- No video files, transcripts or full chapter descriptions are hosted in this repository.
- Local Jekyll preview requires Ruby and Bundler, which are separate from the Python tooling.
- GitHub Pages deployment requires the repository owner to enable Pages with **GitHub Actions** as the source.

[Unreleased]: https://github.com/bevijaygupta/kali-linux-tutorial/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/bevijaygupta/kali-linux-tutorial/releases/tag/v1.0.0
