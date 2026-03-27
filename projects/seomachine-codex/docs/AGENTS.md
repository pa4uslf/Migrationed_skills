# AGENTS.md

This repository now supports a Codex-native workflow in addition to the original Claude-oriented assets.

## Operating Model

- Treat `.claude/` as legacy reference material. Do not add new Codex logic there.
- Treat `.agents/skills/` as the primary Codex entry point for workflow guidance.
- Treat `scripts/` as the source of truth for deterministic post-write automation.
- Keep using `context/`, `data_sources/`, `config/`, and `wordpress/` as shared infrastructure.
- Use `.agents/product-marketing-context.md` as the canonical shared marketing context file. A legacy alias exists at `.claude/product-marketing-context.md`.

## Codex Workflow Map

Use these skills when the user asks for the corresponding workflow:

- `write` -> create a draft in `drafts/`, then run `.venv/bin/python scripts/run_postwrite_pipeline.py <draft>`
- `rewrite` -> create an updated draft in `rewrites/`, then run `.venv/bin/python scripts/run_postwrite_pipeline.py <rewrite>`
- `article` -> follow a research-first article workflow, then run `.venv/bin/python scripts/run_postwrite_pipeline.py <draft>`
- `research` -> create a research brief in `research/`
- `research-quick-wins` -> run `.venv/bin/python research_quick_wins.py`
- `research-gaps` -> run `.venv/bin/python research_competitor_gaps.py`
- `research-performance` -> run `.venv/bin/python research_performance_matrix.py`
- `research-topics` -> run `.venv/bin/python research_topic_clusters.py`
- `research-trending` -> run `.venv/bin/python research_trending.py`
- `research-serp` -> run `.venv/bin/python research_serp_analysis.py "<keyword>"`
- `cluster` -> create a topic cluster strategy in `research/`
- `optimize` -> run `.venv/bin/python scripts/run_optimize_pipeline.py <draft>`
- `performance-review` -> generate an analytics-driven queue with `.venv/bin/python scripts/run_performance_review.py`
- `priorities` -> orchestrate multi-report prioritization with `.venv/bin/python scripts/run_priorities.py`
- `analyze-existing` -> audit an existing URL or local article and save the report in `research/`
- `publish-draft` -> publish a prepared draft with `.venv/bin/python data_sources/modules/wordpress_publisher.py <draft>`
- `content-analysis` -> generate a deterministic SEO analysis report with `.venv/bin/python scripts/run_content_analysis.py <draft>`
- `landing-write` -> create a landing page in `landing-pages/`, then run `.venv/bin/python scripts/run_landing_audit.py <file>`
- `landing-audit` -> audit a local landing page with `.venv/bin/python scripts/run_landing_audit.py <file>`
- `landing-research` -> create a landing-page brief in `research/`
- `landing-competitor` -> analyze a competitor landing page into `research/`
- `landing-publish` -> publish a landing page draft with `.venv/bin/python data_sources/modules/wordpress_publisher.py <file> --type page`

## File Conventions

- New draft articles go in `drafts/`.
- Rewrite outputs go in `rewrites/`.
- Research briefs and audits go in `research/`.
- Landing pages go in `landing-pages/`.
- Articles that still need human intervention can be parked in `review-required/`.
- Keep report files close to their related article unless the user asks otherwise.

## Post-Write Automation

The Codex workflow does not rely on implicit slash-command chaining.

After saving a draft:

1. Run `scripts/run_postwrite_pipeline.py`
   Recommended: `.venv/bin/python scripts/run_postwrite_pipeline.py <draft>`
2. Review the generated quality and analysis reports
3. Fix the article directly if the score is below threshold
4. Re-run the pipeline until the article is publishable

## Context Expectations

Before writing or rewriting content, read the relevant files from `context/`:

- `brand-voice.md`
- `writing-examples.md`
- `style-guide.md`
- `seo-guidelines.md`
- `target-keywords.md`
- `internal-links-map.md`
- `features.md`
- `competitor-analysis.md`

If those files are still templates, say so explicitly and continue with the best available assumptions.

## Notes

- The Python analysis modules are reusable and should be preferred over re-implementing the same logic in prompts.
- If a workflow needs live SERP or analytics data, use the configured integrations when credentials are available. Otherwise, report the limitation clearly.
- Keep prompts and scripts aligned. If you change one, update the other.
