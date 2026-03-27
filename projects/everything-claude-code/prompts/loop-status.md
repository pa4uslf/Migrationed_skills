# loop-status

> 迁移来源：`everything-claude-code/commands/loop-status.md`

> 用途：Codex 中没有原生 Claude 式 slash command，这里保留为可直接引用的工作流提示词。

> 使用建议：优先把本文档当成执行模板；如果文中提到 Claude 风格 agent，优先改用本目录下 `agents/` 里的对应角色。

# Loop Status Command

Inspect active loop state, progress, and failure signals.

## Usage

`/loop-status [--watch]`

## What to Report

- active loop pattern
- current phase and last successful checkpoint
- failing checks (if any)
- estimated time/cost drift
- recommended intervention (continue/pause/stop)

## Watch Mode

When `--watch` is present, refresh status periodically and surface state changes.

## Arguments

$ARGUMENTS:
- `--watch` optional
