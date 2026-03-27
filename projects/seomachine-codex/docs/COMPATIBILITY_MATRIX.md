# Compatibility Matrix

## 可以直接用于 Codex

- `skills/`
- `scripts/`
- `context/product-marketing-context.md`
- `docs/CODEX-MIGRATION.md`
- `docs/CODEX-STATUS.md`

## 已改写为 Codex 形式

- `.codex/agents/*.toml` 的旧格式，已整理为更接近当前 Codex 的 agent 文件
- `.claude/commands/*.md` 已转成 `commands/` 与 `prompts/`

## 仍然保留项目依赖

这些能力离开原项目上下文后会明显降级：

- 内容写作与改写
- 优化与内容分析
- 落地页审计
- 发布前 QA

原因：
- 依赖 `scripts/`
- 依赖 `context/`
- 依赖 `data_sources/` 与 `wordpress/`
