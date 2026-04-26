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

### `frontend_slides`

位置：
`frontend_slides/`

特点：
- 聚焦“网页原生演示稿”这一单一任务
- 已完成 Codex 化入口改写，适合直接复制到全局技能目录
- 保留上游风格预设、PPT 提取、部署与导出脚本
- 适合需要高质量 pitch deck、讲稿 slides、PPT 转 HTML 的场景

推荐使用方式：
- 需要做演示稿时按需安装到 `~/.codex/skills/frontend-slides`
- 先读 `skills/frontend-slides/SKILL.md`
- 生成正式 deck 前再按需读取 `STYLE_PRESETS.md`、`viewport-base.css`、`html-template.md`

### `xiaohu-wechat-format`

位置：
`projects/xiaohu-wechat-format/`

特点：
- 面向中文创作者的公众号排版技能
- 上游脚本成熟，迁移重点在 Codex 入口与可维护性
- 既能只排版，也能扩展到封面与草稿箱

推荐使用方式：
- 按需安装到 `~/.codex/skills/xiaohu-wechat-format`
- 默认先执行 `format.py --gallery`
- 只有需要发草稿箱时再补公众号凭证

### `yichen-skills`

位置：
`projects/yichen-skills/`

特点：
- 只迁入上游的 `x-article-publisher`
- 用于把 Markdown / Obsidian 文章整理到 X Articles 编辑器并保存为草稿
- 已把 Claude 路径改成 Codex `{{SKILL_DIR}}` 路径
- 上游 `summary` 与本机 `note` / `recall` 重叠，未安装
- 上游 `wechat-daily` 需要 frida、codesign 和微信本地数据库解密，默认不启用

推荐使用方式：
- 按需安装到 `~/.codex/skills/x-article-publisher`
- 只保存草稿，最终发布由用户手动确认
- 优先按 `~/.codex/BROWSER.md` 复用真实浏览器登录态；只有需要独立上下文时再配置 `cookies.json`

## 快速安装示例

### 安装 `frontend-slides`

```bash
mkdir -p ~/.codex/skills
cp -R Migrationed_skills/frontend_slides/skills/frontend-slides ~/.codex/skills/frontend-slides
```

### 安装 `social-push`

```bash
mkdir -p ~/.codex/skills
cp -R Migrationed_skills/projects/social-push/skills/social-push ~/.codex/skills/social-push
cp -R Migrationed_skills/projects/social-push/skills/agent-browser ~/.codex/skills/agent-browser
```

### 安装 `xiaohu-wechat-format`

```bash
mkdir -p ~/.codex/skills
cp -R Migrationed_skills/projects/xiaohu-wechat-format/skills/xiaohu-wechat-format ~/.codex/skills/xiaohu-wechat-format
python3 -m venv ~/.codex/skills/xiaohu-wechat-format/.venv
~/.codex/skills/xiaohu-wechat-format/.venv/bin/python3 -m pip install -r ~/.codex/skills/xiaohu-wechat-format/requirements.txt
```

### 安装 `x-article-publisher`

```bash
mkdir -p ~/.codex/skills
cp -R Migrationed_skills/projects/yichen-skills/skills/x-article-publisher ~/.codex/skills/x-article-publisher
```

### 按需参考项目型资产

项目型迁移包通常不建议整包直接复制到全局目录，比如：

- `projects/seomachine-codex/`
- `projects/everything-claude-code/`

更适合做法是：

- 先读项目内 `README.md`
- 按需复制具体 `skills/`、`agents/`、`prompts/` 或脚本
- 避免把强依赖项目上下文的内容一次性全局安装

## Source Repos

原始源项目位置见：
`catalog/SOURCES.md`
