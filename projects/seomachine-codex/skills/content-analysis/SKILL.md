---
name: content-analysis
description: Use when the user wants a deterministic SEO content analysis report for an article in this repository. This skill runs the Codex report script and then interprets the findings.
---

# Content Analysis

Generate and interpret a deterministic SEO analysis report for a local article.

## Command

```bash
.venv/bin/python scripts/run_content_analysis.py <article-file>
```

Optional inputs:

- `--site-url https://example.com`
- `--serp-json path/to/serp-results.json`
- `--output custom-report-path.md`

## What The Script Produces

- Search intent summary
- Keyword placement and density analysis
- Readability metrics
- SEO quality score
- Optional content-length comparison if SERP data is supplied
- Priority action list

## What Codex Should Add

After the script runs:

- Translate the report into a practical editing plan
- Apply fixes directly if the user asked for changes
- Call out missing metadata or missing SERP data instead of guessing
