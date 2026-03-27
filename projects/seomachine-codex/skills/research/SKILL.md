---
name: research
description: Use when the user wants a content research brief, keyword framing, competitor gap analysis, or article outline for this repository. Save the result to research/ and use the project context files as grounding.
---

# Research

Create a research brief for a new article or content opportunity.

## Read First

- `context/target-keywords.md`
- `context/competitor-analysis.md`
- `context/internal-links-map.md`
- `context/features.md`
- `config/competitors.example.json`

If the repository has client-specific files filled in, prefer those over the generic examples.

## Brief Contents

Each brief should include:

- Primary keyword
- Secondary keywords
- Search intent
- Audience pain points
- Competitor observations
- Content gaps or differentiation angles
- Recommended H2/H3 outline
- Internal link opportunities
- Suggested CTA

## Output

Save the brief to:

`research/brief-<topic-slug>-<YYYY-MM-DD>.md`

## Codex-Specific Notes

- Claude slash commands are not the execution model here.
- Treat `.claude/commands/research*.md` as reference material only.
- If live web research is needed, do it explicitly and cite the sources in the brief.
