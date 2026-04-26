# Migrationed Skills

这是一个“从 Claude Code 迁移到 Codex”的技能与工作流资产总仓库。

## 结构

- `catalog/`：总览、索引、安装建议
- `frontend_slides/`：从 `zarazhangrui/frontend-slides` 提取并改写的 Codex 演示稿技能包
- `projects/xiaohu-wechat-format/`：从 `xiaohuailabs/xiaohu-wechat-format` 提取并适配的公众号排版技能包
- `projects/everything-claude-code/`：从 `everything-claude-code` 提取并重构的 Codex 资产包
- `projects/seomachine-codex/`：从 `seomachine-codex` 提取并整理的 Codex 资产包
- `projects/social-push/`：已支持 Codex 的社媒发布技能包归档
- `projects/yichen-skills/`：从 `mcncarl/yichen-skills` 提取并适配的 X Articles 草稿发布技能包

原始源项目统一放在：
- `/Users/frank_zhang/codex/migration-sources/`

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
- `frontend_slides`
  - 1 个 Codex 化演示稿技能
  - 保留上游完整备份与辅助脚本
  - 适合按需复制到 `~/.codex/skills/frontend-slides`
- `xiaohu-wechat-format`
  - 1 个公众号排版 Codex 技能
  - 保留主题、模板、封面与发布脚本
  - 适合按需复制到 `~/.codex/skills/xiaohu-wechat-format`
- `yichen-skills`
  - 1 个 X Articles 草稿发布 Codex 技能
  - 只迁入 `x-article-publisher`
  - `summary` 与本机笔记/记忆能力重叠，`wechat-daily` 涉及微信本地数据库解密，暂不默认启用

## 使用原则

1. 不追求 Claude Code 功能 1:1 复刻。
2. 优先保留能被 Codex 直接消费的技能、提示模板、agent 配置和脚本。
3. 对 hooks、slash commands、自动链式执行等能力，统一做显式降级。
4. 安装到 `~/.codex` 时，优先补“当前环境里没有、但复用价值高”的内容。
5. 总仓库只保存整理后的资产，不直接承载上游源项目仓库。
