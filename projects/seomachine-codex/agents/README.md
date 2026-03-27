# Codex Agents

This directory contains project-local specialized agent definitions for Codex-oriented workflows.

## Status

These definitions are project configuration artifacts, not application code. They are intended to make specialized work easier to route inside this repository:

- content analysis
- SEO optimization
- landing page CRO review
- growth strategy review

## Format

Each agent is stored as a `.toml` file with:

- `name`
- `description`
- `model`
- `reasoning_effort`
- `instructions`

The instructions are written to match this repository's structure and conventions.

## Current Agents

- `content-analyst.toml`
- `seo-optimizer.toml`
- `landing-cro-analyst.toml`
- `growth-strategist.toml`
- `priorities-analyst.toml`
- `keyword-researcher.toml`
- `content-editor.toml`
- `publishing-qa.toml`

## Notes

- These are repository-scoped definitions, not runtime wrappers.
- Deterministic automation still lives under `scripts/`.
- If your Codex environment expects a different on-disk schema for project-local agents, treat these files as canonical prompt sources and adapt the loader rather than rewriting the prompts from scratch.
