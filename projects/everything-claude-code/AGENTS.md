# Migrated ECC For Codex

这个目录是从 `everything-claude-code` 提取出的 Codex-first 工作包。

## 工作方式

- 优先使用 `skills/` 里的技能，而不是依赖 Claude 插件机制
- 需要工作流时，优先参考 `commands/` 或 `prompts/` 里的提示词模板
- 多 agent 协作使用 `agents/` 目录下的角色配置
- `hooks/` 里的内容只是迁移说明，不代表 Codex CLI 会自动执行这些钩子

## 默认工程准则

1. 复杂需求先规划，再修改代码
2. 新功能和缺陷修复优先走 TDD
3. 变更后优先做代码审查和安全审查
4. 不要假设 Claude 的 slash commands、plugin hooks、自动内存都会存在
5. 对于不支持的能力，改用文档、脚本、提示词和多 agent 角色组合替代

## 技能

技能来自 `skills/`。如果你要显式触发某个技能，直接引用技能名或对应目录。

## 命令迁移规则

上游 `/plan`、`/verify`、`/code-review` 之类的命令，在这里被迁移为 `commands/*.md` 和 `prompts/*.md`。

使用方式：

- 先打开对应文件
- 把里面的流程当作当前任务的执行模板
- 若文件提到了上游 agent，优先用 `agents/` 中的同名或近似角色替代

## 重要限制

- Codex CLI 不等价支持 Claude Code 的 hooks 体系
- 因此自动记忆写入、自动安全门禁、自动停止总结等逻辑只能降级为显式流程
- 真正需要强约束时，应该用仓库脚本、CI、pre-commit 或 Git hook 实现
