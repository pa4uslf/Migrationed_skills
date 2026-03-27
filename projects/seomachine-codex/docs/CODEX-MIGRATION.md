# Codex Migration Guide

This repository started as a Claude Code workspace. The Codex adaptation keeps the analysis and publishing core, but replaces the orchestration layer.

## What Stayed the Same

- `context/` for brand, style, keyword, and linking guidance
- `data_sources/` for analytics, SEO scoring, and publishing integrations
- `wordpress/` for Yoast-compatible REST publishing support
- Existing content directories such as `drafts/`, `research/`, `published/`, and `rewrites/`

## What Changed

### Legacy Claude Layer

- `CLAUDE.md`
- `.claude/commands/*`
- `.claude/agents/*`
- `.claude/skills/*`

These files are preserved as reference material.

### Codex Layer

- `AGENTS.md` contains repository-level instructions for Codex
- `.agents/skills/*` contains Codex-friendly workflow skills
- `.agents/product-marketing-context.md` is the canonical shared marketing context file
- `docs/CODEX-STATUS.md` tracks current migration coverage
- `scripts/run_postwrite_pipeline.py` replaces implicit auto-trigger chains
- `scripts/run_content_analysis.py` creates deterministic analysis reports
- `scripts/run_optimize_pipeline.py` provides a final pre-publish audit path

## Mapping

| Claude asset | Codex replacement |
| --- | --- |
| `CLAUDE.md` | `AGENTS.md` |
| `.claude/commands/write.md` | `.agents/skills/write/SKILL.md` + `scripts/run_postwrite_pipeline.py` |
| `.claude/commands/rewrite.md` | `.agents/skills/rewrite/SKILL.md` + `scripts/run_postwrite_pipeline.py` |
| `.claude/commands/research.md` | `.agents/skills/research/SKILL.md` |
| `.claude/commands/research-serp.md` | `.agents/skills/research-serp/SKILL.md` |
| `.claude/commands/research-topics.md` | `.agents/skills/research-topics/SKILL.md` |
| `.claude/commands/research-trending.md` | `.agents/skills/research-trending/SKILL.md` |
| `.claude/commands/research-performance.md` | `.agents/skills/research-performance/SKILL.md` |
| `.claude/commands/research-gaps.md` | `.agents/skills/research-gaps/SKILL.md` |
| `.claude/commands/priorities.md` | `.agents/skills/priorities/SKILL.md` + `scripts/run_priorities.py` |
| `.claude/commands/article.md` | `.agents/skills/article/SKILL.md` |
| `.claude/commands/cluster.md` | `.agents/skills/cluster/SKILL.md` |
| `.claude/commands/optimize.md` | `.agents/skills/optimize/SKILL.md` + `scripts/run_optimize_pipeline.py` |
| `.claude/commands/analyze-existing.md` | `.agents/skills/analyze-existing/SKILL.md` |
| `.claude/commands/performance-review.md` | `.agents/skills/performance-review/SKILL.md` + `scripts/run_performance_review.py` |
| `.claude/commands/publish-draft.md` | `.agents/skills/publish-draft/SKILL.md` |
| `.claude/commands/landing-write.md` | `.agents/skills/landing-write/SKILL.md` |
| `.claude/commands/landing-audit.md` | `.agents/skills/landing-audit/SKILL.md` + `scripts/run_landing_audit.py` |
| `.claude/commands/landing-research.md` | `.agents/skills/landing-research/SKILL.md` |
| `.claude/commands/landing-competitor.md` | `.agents/skills/landing-competitor/SKILL.md` |
| `.claude/commands/landing-publish.md` | `.agents/skills/landing-publish/SKILL.md` |
| `.claude/agents/content-analyzer.md` | `.agents/skills/content-analysis/SKILL.md` + `scripts/run_content_analysis.py` |

## Recommended Codex Flow

### New Article

1. Ask Codex to use the `research` skill and create a brief in `research/`
2. Ask Codex to use the `write` skill and create a draft in `drafts/`
3. Run:

```bash
.venv/bin/python scripts/run_postwrite_pipeline.py drafts/<article>.md
```

4. Review:
- `drafts/quality-report-<article>.md`
- `drafts/content-analysis-<article>.md`

5. Iterate until the article is ready
6. Run:

```bash
.venv/bin/python scripts/run_optimize_pipeline.py drafts/<article>.md
```

### Existing Article

1. Ask Codex to use the `analyze-existing` skill
2. Save the audit in `research/`
3. Rewrite into `rewrites/` or `drafts/`
4. Run the same post-write pipeline

### Publishing

Once the draft has valid metadata and WordPress credentials are configured:

```bash
.venv/bin/python data_sources/modules/wordpress_publisher.py drafts/<article>.md
```

## Why the Codex Version Uses Scripts

The original Claude workflow depended on prompt-level auto-execution:

- save article
- run scrubber
- run scorer
- run multiple analysis agents

Codex works better when that chain is explicit, inspectable, and repeatable. The scripts in `scripts/` make the workflow deterministic and easy to rerun.
