# Catalog Index

## Projects

### `everything-claude-code`

位置：
`projects/everything-claude-code/`

特点：
- 通用工程型技能为主
- 多 agent 协作、代码审查、TDD、验证链路较完整
- 上游含较多 Claude / plugin / hook 历史包袱，已做显式降级

推荐优先安装：
- `tdd-workflow`
- `verification-loop`
- `coding-standards`
- `backend-patterns`
- `frontend-patterns`
- `e2e-testing`
- `eval-harness`
- `strategic-compact`
- `api-design`
- `documentation-lookup`

高价值提示模板：
- `plan`
- `tdd`
- `verify`
- `code-review`
- `build-fix`
- `update-docs`

### `seomachine-codex`

位置：
`projects/seomachine-codex/`

特点：
- SEO / 内容 / CRO / 选题 / 落地页工作流更完整
- 已经有较成熟的 Codex 迁移层
- 强依赖仓库内脚本和上下文文档，适合项目内使用

推荐优先参考：
- `research`
- `write`
- `rewrite`
- `optimize`
- `analyze-existing`
- `landing-audit`
- `priorities`

## 安装策略

全局安装时，优先装 `everything-claude-code` 的工程型技能和提示模板。

`seomachine-codex` 的技能更适合按项目引入，因为它们依赖项目本身的：
- `context/`
- `scripts/`
- `data_sources/`
- `wordpress/`

### `social-push`

位置：
`projects/social-push/`

特点：
- 轻量
- 已有 Codex 使用说明
- 适合按需安装到全局技能目录
- 依赖浏览器远程调试与平台登录态

推荐使用方式：
- 只在确实需要社媒发布自动化时安装
- 把 `social-push` 和 `agent-browser` 一起使用
