# seomachine-codex For Codex

这是从 `seomachine-codex` 提取出的 Codex 迁移资产包。

## 工作方式

- 把 `skills/` 当作主入口
- 把 `scripts/` 当作确定性执行层
- 把 `commands/` / `prompts/` 当作原 `.claude/commands` 的 Codex 替代物
- 把 `agents/` 当作项目级多 agent 角色定义

## 使用约束

1. 先读相关 `context/` 文件，再写内容
2. 内容产出后优先跑现有 Python 脚本，不要只给主观建议
3. 这套资产依赖项目上下文，不建议直接当作全局通用技能包
