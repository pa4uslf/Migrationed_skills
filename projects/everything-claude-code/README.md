# Everything Claude Code -> Codex Migration Pack

这个目录是把 `everything-claude-code` 按 Codex 可直接消费的形式重新整理后的结果。

## 目录结构

- `backup/`：上游仓库的原始备份
- `skills/`：从上游 `.agents/skills/` 提取出的 Codex 技能
- `agents/`：Codex 多 agent 角色配置
- `commands/`：把上游 slash command 改写成可直接引用的提示词文档
- `prompts/`：和 `commands/` 同步的提示词副本，方便直接复制到 `~/.codex/prompts`
- `hooks/`：不能等价迁移的能力说明
- `docs/`：迁移报告、能力映射、清单
- `scripts/`：重建迁移产物的脚本

## 用法

1. 如需重建迁移结果，执行：

```bash
bash Migrationed_skills/projects/everything-claude-code/scripts/rebuild_from_backup.sh
```

2. 如需把它接到 Codex：

```bash
cp Migrationed_skills/projects/everything-claude-code/AGENTS.md ~/.codex/AGENTS.md
cp Migrationed_skills/projects/everything-claude-code/config.toml ~/.codex/config.toml
cp -R Migrationed_skills/projects/everything-claude-code/skills ~/.codex/
cp -R Migrationed_skills/projects/everything-claude-code/agents ~/.codex/
cp -R Migrationed_skills/projects/everything-claude-code/prompts ~/.codex/
```

## 迁移原则

- 保留技能与知识资产
- 将命令降级为“提示词模板”
- 将 Claude 风格 agent 定义重写为 Codex `agents/*.toml`
- 将 hooks 改成文档化约束，而不是假装可以 1:1 运行
