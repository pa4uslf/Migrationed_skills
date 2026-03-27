# Codex Migration Status

This file summarizes how far the repository has been adapted from the original Claude-oriented workspace into a Codex-friendly workspace.

## Current State

### Codex-Native

These areas now have explicit Codex entry points, scripts, or rewritten workflow guidance:

- Repository instructions via `AGENTS.md`
- Content pipeline
  - `research`
  - `write`
  - `rewrite`
  - `article`
  - `optimize`
  - `content-analysis`
  - `analyze-existing`
  - `publish-draft`
- Research and prioritization
  - `priorities`
  - `performance-review`
  - `research-quick-wins`
  - `research-gaps`
  - `research-performance`
  - `research-topics`
  - `research-trending`
  - `research-serp`
  - `cluster`
- Landing page workflows
  - `landing-research`
  - `landing-write`
  - `landing-audit`
  - `landing-competitor`
  - `landing-publish`
- Shared marketing context
  - `.agents/product-marketing-context.md`

### Migrated And Refined

These marketing skills were migrated from `.claude/skills/` and explicitly adjusted to use Codex-side shared context:

- `copywriting`
- `copy-editing`
- `content-strategy`
- `seo-audit`
- `programmatic-seo`
- `pricing-strategy`
- `paid-ads`
- `social-content`
- `page-cro`
- `email-sequence`
- `analytics-tracking`
- `marketing-ideas`
- `free-tool-strategy`
- `competitor-alternatives`
- `form-cro`
- `onboarding-cro`
- `popup-cro`
- `signup-flow-cro`
- `ab-test-setup`
- `launch-strategy`
- `marketing-psychology`
- `referral-program`
- `schema-markup`
- `paywall-upgrade-cro`

### Migrated With Compatibility Layer

The remaining migrated skills are usable in Codex because:

- they live under `.agents/skills/`
- referenced `references/` folders were copied over
- `.claude/product-marketing-context.md` points to the Codex-side canonical file

They may still mention legacy Claude phrasing in prose, but their working file paths are intact.

## Counts

- Total discoverable Codex skills: `48`
- Codex-native workflow skills: `22`
- Refined migrated marketing skills: `24`
- Project-local Codex agent definitions: `8`
- Shared marketing context files: `1` canonical + `1` compatibility alias

## Remaining Optional Work

These are improvements, not blockers:

1. Continue line-editing the few remaining migrated skills so their prose no longer mentions legacy Claude conventions.
2. Add more deterministic wrappers where pure skill prose is not enough.
3. Expand `.codex/agents` definitions if you want more explicit specialized sub-agent entry points.
4. Grow the current smoke test suite into deeper behavioral tests if this repository will be maintained as a long-lived internal tool.
