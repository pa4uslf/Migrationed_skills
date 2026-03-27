# Migrationed Skills

这是一个“从 Claude Code 迁移到 Codex”的技能与工作流资产总仓库。

## 结构

- `catalog/`：总览、索引、安装建议
- `projects/everything-claude-code/`：从 `everything-claude-code` 提取并重构的 Codex 资产包
- `projects/seomachine-codex/`：从 `seomachine-codex` 提取并整理的 Codex 资产包
- `projects/social-push/`：已支持 Codex 的社媒发布技能包归档

## 当前收录

- `everything-claude-code`
  - 29 个技能
  - 13 个 agent 配置
  - 60 个命令提示模板
- `seomachine-codex`
  - 48 个技能
  - 8 个 agent 配置
  - 22 个命令提示模板
  - 7 个确定性脚本
- `social-push`
  - 2 个技能
  - 已有 Codex 使用说明
  - 适合作为独立技能包按需安装

## 使用原则

1. 不追求 Claude Code 功能 1:1 复刻。
2. 优先保留能被 Codex 直接消费的技能、提示模板、agent 配置和脚本。
3. 对 hooks、slash commands、自动链式执行等能力，统一做显式降级。
4. 安装到 `~/.codex` 时，优先补“当前环境里没有、但复用价值高”的内容。
