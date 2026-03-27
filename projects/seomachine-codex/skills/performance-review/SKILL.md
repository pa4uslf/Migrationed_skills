---
name: performance-review
description: Use when the user wants analytics-driven content priorities, quick wins, declining-content detection, or a monthly SEO performance queue. This skill uses the project's data integrations and emits a report in research/.
---

# Performance Review

Generate a prioritized content task queue from analytics and ranking data.

## Command

```bash
.venv/bin/python scripts/run_performance_review.py --days 30
```

Optional:

```bash
.venv/bin/python scripts/run_performance_review.py --days 90 --output research/performance-review-q1.md
```

## Expected Inputs

- Configured credentials in `data_sources/config/.env`
- GA4 access
- GSC access
- DataForSEO access if competitor/ranking data is required

## What To Do With The Report

- Turn quick wins into `optimize` or `analyze-existing` tasks
- Turn declining pages into `rewrite` tasks
- Turn trending topics into `research` and `write` tasks

## Codex-Specific Notes

- The original Claude command was largely orchestration around Python modules. In Codex, the script is the source of truth.
- If credentials are missing, the report should still be generated with clear gaps called out.
