---
name: cluster
description: Use when the user wants a topic cluster strategy with a pillar page, supporting articles, sequencing, and an internal-linking map. Save the strategy to research/.
---

# Cluster

Build a topic cluster strategy rather than a single article.

## Read First

- `context/target-keywords.md`
- `context/internal-links-map.md`
- `context/competitor-analysis.md`
- Existing files in `research/` that match the topic

## Output Requirements

Save to:

`research/cluster-strategy-<topic-slug>-<YYYY-MM-DD>.md`

Include:

- Pillar keyword and search intent
- Pillar page definition
- 8-12 supporting article ideas
- Priority score or sequencing logic
- Internal link map
- Copy-pastable next commands for research and writing

## Codex-Specific Notes

- Use `.claude/commands/cluster.md` and `.claude/agents/cluster-strategist.md` as reference only.
- If keyword APIs are unavailable, produce the cluster from local research plus explicit web research.
