# seomachine-codex Migration Pack

这个子目录收纳 `seomachine-codex` 中与 Codex 迁移直接相关的资产，而不是整个业务项目本体。

## 包含内容

- `skills/`：48 个 Codex 可发现技能
- `agents/`：8 个项目级 agent 配置，已整理为更接近当前 Codex 的格式
- `commands/`：由旧 `.claude/commands` 转成的提示模板
- `prompts/`：命令模板副本，方便复制到 `~/.codex/prompts`
- `scripts/`：确定性内容分析与优化脚本
- `context/`：共享营销上下文的核心文件
- `docs/`：迁移状态、技能索引、兼容性说明
- `backup/`：保留原始 Claude 命令与技能目录

## 适用场景

这套资产更适合“项目内使用”，不适合无脑全局安装。原因是很多技能和 agent 都假设以下目录存在：

- `context/`
- `scripts/`
- `data_sources/`
- `drafts/`
- `research/`
- `landing-pages/`

## 重建

```bash
bash Migrationed_skills/projects/seomachine-codex/scripts/rebuild_from_source.sh
```
