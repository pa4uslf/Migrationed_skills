# Skills Index

This repository now exposes two classes of Codex-usable skills:

- **Codex-native workflow skills**: created or rewritten specifically for the migration
- **Migrated marketing skills**: copied from the original Claude workspace and kept compatible through shared paths and references

## Codex-Native Workflow Skills

### Content Pipeline

- `research`
- `write`
- `rewrite`
- `article`
- `optimize`
- `content-analysis`
- `analyze-existing`
- `publish-draft`

### Research And Prioritization

- `priorities`
- `performance-review`
- `research-quick-wins`
- `research-gaps`
- `research-performance`
- `research-topics`
- `research-trending`
- `research-serp`
- `cluster`

### Landing Pages

- `landing-research`
- `landing-write`
- `landing-audit`
- `landing-competitor`
- `landing-publish`

## Migrated Marketing Skills

These were copied from `.claude/skills/` into `.agents/skills/` and can now be discovered by Codex.

### Copy And Messaging

- `copywriting`
- `copy-editing`
- `content-strategy`
- `marketing-ideas`
- `marketing-psychology`
- `growth-lead`

### CRO And Funnel Optimization

- `page-cro`
- `form-cro`
- `popup-cro`
- `onboarding-cro`
- `signup-flow-cro`
- `paywall-upgrade-cro`

### SEO And Content Systems

- `seo-audit`
- `schema-markup`
- `programmatic-seo`
- `competitor-alternatives`
- `free-tool-strategy`

### Demand Gen And Lifecycle

- `email-sequence`
- `social-content`
- `paid-ads`
- `referral-program`
- `launch-strategy`
- `pricing-strategy`
- `ab-test-setup`
- `analytics-tracking`

### Shared Marketing Context

- `product-marketing-context`

Canonical shared context file:

- `.agents/product-marketing-context.md`

Compatibility alias:

- `.claude/product-marketing-context.md` -> symlink to the Codex-side file

## Notes

- Most migrated skills now resolve correctly through Codex-side paths and copied reference files.
- A small number still mention legacy Claude conventions in explanatory prose, but their working file references are intact.
- For deterministic automation, prefer the Codex-native scripts under `scripts/` over prose-only legacy workflows.

## Refined Migrated Skills

These high-traffic marketing skills were explicitly adjusted for the Codex migration and now point directly at `.agents/product-marketing-context.md`:

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
