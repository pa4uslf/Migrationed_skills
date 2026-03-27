# Migration Report

## 目标

把 `everything-claude-code` 里能被 Codex 消费的部分提取出来，整理成一个不依赖 Claude 插件运行时的工作包。

## 已完成

- 建立本地备份目录：`backup/everything-claude-code`
- 提取 Codex 技能目录目标：`skills/`
- 建立 Codex 多 agent 目录：`agents/`
- 将上游 `commands/*.md` 改造成可直接引用的提示词文档
- 提供最小稳定的 `config.toml`
- 提供 Codex 版 `AGENTS.md`
- 文档化 hooks 降级策略

## 迁移策略

### 直接迁移

- `.agents/skills/*`
- `.codex/agents/*`
- 上游命令文档主体内容

### 结构性改写

- Claude slash commands -> `commands/*.md` / `prompts/*.md`
- Claude agent markdown -> Codex `agents/*.toml`
- Claude hook enforcement -> 文档约束 + 脚本/CI 替代

### 不做 1:1 兼容

- Claude 插件生命周期
- 依赖专有 hook 事件的自动化
- “安装即拥有全部行为”的错觉

## 结果判定

这个目录现在更接近“Codex-first 资产包”，而不是“Claude 仓库的兼容壳”。
