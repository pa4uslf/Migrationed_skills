# Compatibility Matrix

## 可以直接用于 Codex

| 上游能力 | 迁移结果 | 位置 |
| --- | --- | --- |
| `.agents/skills/*` | 直接提取 | `skills/` |
| `.codex/agents/*` | 直接提取 | `agents/` |
| Codex 基础配置 | 重新整理 | `config.toml` |
| Codex 项目指令 | 重新整理 | `AGENTS.md` |

## 需要改写后使用

| 上游能力 | Codex 形态 | 位置 |
| --- | --- | --- |
| `commands/*.md` | 提示词模板 | `commands/` |
| slash commands | 手动引用文档执行 | `commands/` / `prompts/` |
| Claude agent markdown | Codex TOML 角色 | `agents/*.toml` |

## 不能 1:1 迁移

| 上游能力 | 原因 | 替代方案 |
| --- | --- | --- |
| Claude hooks | Codex CLI 无等价事件系统 | Git hooks / CI / 脚本 |
| 自动记忆注入 | 依赖上游运行时 | 明确写入 `AGENTS.md` / 项目文档 |
| 插件生命周期 | Codex 不走 Claude plugin 机制 | 项目级目录 + `config.toml` |
| 原生命令注册 | Codex 不按 Claude slash command 注册 | 提示词模板 |

## 建议使用顺序

1. 先把 `AGENTS.md` 和 `config.toml` 放到 `~/.codex/`
2. 再把 `skills/`、`agents/`、`prompts/` 复制到 `~/.codex/`
3. 最后按任务类型引用 `commands/*.md` 中的工作流模板
