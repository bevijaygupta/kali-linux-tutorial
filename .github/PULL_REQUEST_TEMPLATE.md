## Summary

<!-- What does this change and why? Link the issue if there is one. -->

## Type of change

- [ ] Bug fix
- [ ] Content correction
- [ ] New documentation or resource
- [ ] Site or accessibility improvement
- [ ] Automation or workflow change
- [ ] Metadata refresh

## Verification

<!-- List the checks you ran and their results. -->

```text
python scripts/generate_lesson_pages.py --check
python scripts/generate_content.py --check
python scripts/generate_sitemap.py --check
python scripts/validate_links.py --strict
```

- [ ] Generated files were regenerated with the scripts, not hand-edited.
- [ ] Internal links use Liquid `relative_url` in Jekyll pages.
- [ ] Facts, commands and claims have a primary source where possible.
- [ ] Scheduled chapters still have `duration: null`, `published_date: null` and no `VideoObject`.
- [ ] No transcript, re-hosted video, credential, secret, personal data or target list is included.
- [ ] Destructive or intrusive steps have a warning and an isolated-lab boundary.
- [ ] The change does not push directly to `main` or bypass review.

## Screenshots

<!-- For visual changes, add before/after screenshots. Remove this section if not applicable. -->

## Notes for reviewers

<!-- Anything risky, unverified or intentionally left out. -->
