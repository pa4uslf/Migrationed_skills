---
name: optimize
description: Use when the user wants a final SEO optimization pass on an article in this repository. This skill runs the Codex analysis pipeline, reviews the reports, and then applies fixes directly in the article.
---

# Optimize

Run a final audit for a draft or rewrite and then apply the highest-leverage fixes.

## Inputs

- A local article file, usually from `drafts/` or `rewrites/`
- Optional `site_url` or SERP data path if available

## Required Actions

1. Run:

```bash
.venv/bin/python scripts/run_optimize_pipeline.py <article-file>
```

2. Read the generated report:

- `drafts/optimization-report-<article>.md` or the same directory equivalent

3. Apply the important fixes directly to the article
4. Re-run the optimize pipeline if the changes are substantial

## Optimization Priorities

- Missing or weak keyword placement
- Meta title / description quality
- Readability problems
- Thin sections
- Missing links
- Structure issues
- Low composite quality score

## Codex-Specific Notes

- Do not depend on implicit agent execution from the Claude version.
- The script provides deterministic analysis; Codex should provide the judgment and rewriting.
