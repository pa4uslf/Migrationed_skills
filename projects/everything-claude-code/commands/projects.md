# projects

> 迁移来源：`everything-claude-code/commands/projects.md`

> 用途：Codex 中没有原生 Claude 式 slash command，这里保留为可直接引用的工作流提示词。

> 使用建议：优先把本文档当成执行模板；如果文中提到 Claude 风格 agent，优先改用本目录下 `agents/` 里的对应角色。


# Projects Command

List project registry entries and per-project instinct/observation counts for continuous-learning-v2.

## Implementation

Run the instinct CLI using the plugin root path:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" projects
```

Or if `CLAUDE_PLUGIN_ROOT` is not set (manual installation):

```bash
python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py projects
```

## Usage

```bash
/projects
```

## What to Do

1. Read `~/.claude/homunculus/projects.json`
2. For each project, display:
   - Project name, id, root, remote
   - Personal and inherited instinct counts
   - Observation event count
   - Last seen timestamp
3. Also display global instinct totals
