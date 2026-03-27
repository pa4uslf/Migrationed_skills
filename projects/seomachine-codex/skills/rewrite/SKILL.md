---
name: rewrite
description: Use when the user wants to refresh or substantially rewrite an existing article in this repository. This skill preserves useful material, updates outdated sections, saves the new draft, and then runs the Codex post-write pipeline.
---

# Rewrite

Update an existing article without losing the parts that still work.

## Inputs

- Existing article file or rewrite brief
- Optional analysis report from `research/`
- Optional new keyword angle or updated CTA

## Read First

- `context/brand-voice.md`
- `context/style-guide.md`
- `context/seo-guidelines.md`
- `context/internal-links-map.md`
- The original article
- Any matching file in `research/analysis-*.md`

## Rewrite Rules

- Keep effective sections that still match current intent
- Update stats, examples, links, and outdated claims
- Expand thin sections where competitors now go deeper
- Preserve or improve metadata
- Save to `rewrites/<topic-slug>-rewrite-<YYYY-MM-DD>.md`

## After Saving

Run:

```bash
.venv/bin/python scripts/run_postwrite_pipeline.py rewrites/<rewrite-file>.md
```

Then address the generated quality and analysis reports before publishing.
