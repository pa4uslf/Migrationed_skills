---
name: write
description: Use when the user wants a long-form SEO article drafted in this repository. This skill reads the project context, writes the draft to drafts/, and then runs the Codex post-write pipeline instead of relying on Claude-specific auto-triggered commands.
---

# Write

Create a long-form SEO article that fits the project's context files and then run the deterministic Codex pipeline.

## Inputs

- Topic, keyword, or an existing research brief
- Optional audience, CTA, angle, or desired article type

## Required Context

Read these files before drafting:

- `context/brand-voice.md`
- `context/writing-examples.md`
- `context/style-guide.md`
- `context/seo-guidelines.md`
- `context/target-keywords.md`
- `context/internal-links-map.md`
- `context/features.md`

If the user already gave a research brief, use it. Otherwise check `research/` for a matching brief first.

## Output Rules

- Save the article to `drafts/<topic-slug>-<YYYY-MM-DD>.md`
- Prefer simple frontmatter or metadata block with at least:
  - `Primary Keyword`
  - `Secondary Keywords`
  - `Meta Title`
  - `Meta Description`
- Keep the body in Markdown
- Include a real H1, strong intro, internal links, external links, and a clear CTA

## After Saving The Draft

Run:

```bash
.venv/bin/python scripts/run_postwrite_pipeline.py drafts/<article-file>.md
```

Then review:

- `drafts/quality-report-<article>.md`
- `drafts/content-analysis-<article>.md`

If the draft scores below threshold, improve the article instead of declaring success.

## Codex-Specific Notes

- Do not rely on `.claude/commands/write.md` auto-trigger behavior.
- Use `scripts/run_postwrite_pipeline.py` as the Codex replacement for scrub + score + analyze.
- If the user wants deeper editorial or meta copy refinement, do that explicitly in the session after the pipeline runs.
