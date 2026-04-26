# yichen-skills Codex Migration

来源：`https://github.com/mcncarl/yichen-skills.git`

本目录只保存适合当前 Codex 环境的整理后资产。上游原始仓库保存在：

`/Users/frank_zhang/codex/migration-sources/yichen-skills`

## 迁移结论

已迁入并适配：

- `x-article-publisher`：将 Markdown / Obsidian 文章整理到 X Articles 编辑器并保存为草稿。

暂不迁入全局技能：

- `summary`：和本机 `note` / `recall` 能力重叠，并且上游写死 Windows Obsidian 示例路径。
- `wechat-daily`：会安装 frida、codesign 微信副本并解密本机微信数据库；属于高敏感本地数据工作流，先保留为 source 参考，不默认启用。

## 安装

```bash
mkdir -p ~/.codex/skills
cp -R Migrationed_skills/projects/yichen-skills/skills/x-article-publisher ~/.codex/skills/x-article-publisher
```

安装后重开 Codex 会话，使用自然语言触发：

- `把这篇 Markdown 发成 X Article 草稿`
- `发布到 X Articles`
- `把 Obsidian 文章整理到 X 长文编辑器`

## 安全边界

- 只保存草稿，不自动点击最终发布按钮。
- `cookies.json` 只允许保存在本机，不提交到 Git。
- 如果用户已有真实 Chrome 登录态，优先按 `~/.codex/BROWSER.md` 选择 `browser-harness` / `bb-browser` 复用登录态；不要默认要求用户复制 X cookie。
- X 平台条款、账号风险和最终发布内容由用户确认。

