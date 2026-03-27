# Hooks Migration Notes

这里不直接放可执行 hook，因为上游很多能力依赖 Claude Code 的事件系统，Codex CLI 不能等价运行。

## 已降级的能力

- Session start / stop 自动摘要
- 自动记忆写入
- 命令前后拦截
- 自动安全扫描门禁
- 自动 compact / context budget 管理

## 建议替代

- 需要强制执行的检查：放到 Git hooks 或 CI
- 需要重复执行的流程：放到 `commands/` 或 `prompts/`
- 需要约束模型行为：放到 `AGENTS.md`
- 需要自动化同步：放到 `scripts/`

## 备份来源

原始 hook 逻辑在：

- `backup/everything-claude-code/hooks/`
- `backup/everything-claude-code/scripts/hooks/`
