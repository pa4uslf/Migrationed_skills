# Upstream Notes

## Source

- Repo: `https://github.com/mcncarl/yichen-skills.git`
- Local source clone: `/Users/frank_zhang/codex/migration-sources/yichen-skills`
- Reviewed commit: `eedff17`
- Review date: `2026-04-26`

## Upstream Contents

- `summary/skill.md`: conversation-to-Obsidian summary workflow.
- `x-publisher/x-article-publisher/skill.md`: X Articles Markdown publishing workflow.
- `wechat-daily/SKILL.md`: macOS WeChat local database daily digest workflow.

## Codex Adaptation

- Renamed `skill.md` to `SKILL.md` for Codex loading.
- Replaced Claude-specific `~/.claude/skills/x-publisher/...` paths with `{{SKILL_DIR}}/...`.
- Kept `cookies.template.json`; do not store real `cookies.json` in Git.
- Added draft-only and login-state boundary notes.
- Left `summary` and `wechat-daily` out of the active install set.

