# social-push Curated Package

这个子目录收录 `social-push` 项目里最适合纳入 `Migrationed_skills` 的部分。

## 判断结论

`social-push` 适合纳入，但它更像“已经支持 Codex 的独立技能包”，而不是传统意义上的迁移项目。

原因：
- 体量很小，核心内容集中在 `skills/`
- README 已经明确支持 OpenAI Codex
- 没有复杂的 Claude-only orchestration 层
- 主要价值是可复用的浏览器自动化与社媒发布流程

## 包含内容

- `skills/agent-browser/`
- `skills/social-push/`
- `docs/README.md`
- `docs/README_EN.md`
- `docs/UPSTREAM.md`

## 适用方式

这套内容适合：
- 按需复制到 `~/.codex/skills/`
- 作为平台发布技能模板参考
- 与现有浏览器自动化能力结合使用

这套内容不适合：
- 直接替代全局浏览器技能
- 在没有登录态、浏览器远程调试、平台 workflow 的情况下盲跑
