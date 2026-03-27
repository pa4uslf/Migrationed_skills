---
name: article
description: Use when the user wants a higher-rigor article workflow than the basic write flow. This skill enforces research, gap analysis, planning, and then drafting before the post-write pipeline runs.
---

# Article

Use this workflow for competitive or strategically important articles where a quick draft is not good enough.

## Required Sequence

1. Perform SERP research and save notes in `research/`
2. Perform social research if the topic benefits from Reddit, YouTube, or community language
3. Build a section-by-section plan
4. Draft the article
5. Run the post-write pipeline

## Recommended File Outputs

- `research/serp-analysis-<topic>-<date>.md`
- `research/social-research-<topic>-<date>.md`
- `research/article-plan-<topic>-<date>.md`
- `drafts/<topic>-<date>.md`

## After Drafting

```bash
.venv/bin/python scripts/run_postwrite_pipeline.py drafts/<article-file>.md
```

## When To Prefer This Skill

- High-value commercial topics
- Competitive SERPs
- Topics where generic AI drafts will lose
- Articles that need stronger differentiation than the `write` skill
