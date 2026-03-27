#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE_DIR="$ROOT_DIR/backup/everything-claude-code"

SKILLS_SRC="$SOURCE_DIR/.agents/skills"
AGENTS_SRC="$SOURCE_DIR/.codex/agents"
COMMANDS_SRC="$SOURCE_DIR/commands"

SKILLS_DEST="$ROOT_DIR/skills"
AGENTS_DEST="$ROOT_DIR/agents"
COMMANDS_DEST="$ROOT_DIR/commands"
PROMPTS_DEST="$ROOT_DIR/prompts"
DOCS_DEST="$ROOT_DIR/docs"

log() {
  printf '[migration] %s\n' "$*"
}

require_dir() {
  local path="$1"
  if [[ ! -d "$path" ]]; then
    printf 'Missing required directory: %s\n' "$path" >&2
    exit 1
  fi
}

render_command_prompt() {
  local src="$1"
  local dest="$2"
  local name="$3"

  {
    printf '# %s\n\n' "$name"
    printf '> 迁移来源：`everything-claude-code/commands/%s.md`\n\n' "$name"
    printf '> 用途：Codex 中没有原生 Claude 式 slash command，这里保留为可直接引用的工作流提示词。\n\n'
    printf '> 使用建议：优先把本文档当成执行模板；如果文中提到 Claude 风格 agent，优先改用本目录下 `agents/` 里的对应角色。\n\n'
    awk '
      BEGIN { frontmatter = 0; started = 0 }
      NR == 1 && $0 == "---" { frontmatter = 1; next }
      frontmatter == 1 && $0 == "---" { frontmatter = 0; started = 1; next }
      frontmatter == 1 { next }
      { print }
    ' "$src"
  } > "$dest"
}

write_inventory() {
  local skills_doc="$DOCS_DEST/skills-inventory.md"
  local commands_doc="$DOCS_DEST/commands-inventory.md"

  {
    printf '# Skills Inventory\n\n'
    printf '| Skill | Files |\n'
    printf '| --- | --- |\n'
    for skill_dir in "$SKILLS_DEST"/*; do
      [[ -d "$skill_dir" ]] || continue
      skill_name="$(basename "$skill_dir")"
      file_count="$(find "$skill_dir" -type f | wc -l | tr -d ' ')"
      printf '| `%s` | %s |\n' "$skill_name" "$file_count"
    done
  } > "$skills_doc"

  {
    printf '# Commands Inventory\n\n'
    printf '| Command | Prompt File |\n'
    printf '| --- | --- |\n'
    for command_file in "$COMMANDS_DEST"/*.md; do
      [[ -f "$command_file" ]] || continue
      command_name="$(basename "$command_file" .md)"
      printf '| `%s` | `%s.md` |\n' "$command_name" "$command_name"
    done
  } > "$commands_doc"
}

require_dir "$SOURCE_DIR"
require_dir "$SKILLS_SRC"
require_dir "$AGENTS_SRC"
require_dir "$COMMANDS_SRC"

log "Syncing skills"
mkdir -p "$SKILLS_DEST"
find "$SKILLS_DEST" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
cp -R "$SKILLS_SRC"/. "$SKILLS_DEST"/

log "Syncing upstream Codex agent configs"
mkdir -p "$AGENTS_DEST"
cp -R "$AGENTS_SRC"/. "$AGENTS_DEST"/

log "Generating command prompts"
mkdir -p "$COMMANDS_DEST" "$PROMPTS_DEST"
find "$COMMANDS_DEST" -mindepth 1 -maxdepth 1 -type f -name '*.md' -exec rm -f {} +
find "$PROMPTS_DEST" -mindepth 1 -maxdepth 1 -type f -name '*.md' -exec rm -f {} +

for src in "$COMMANDS_SRC"/*.md; do
  [[ -f "$src" ]] || continue
  name="$(basename "$src" .md)"
  render_command_prompt "$src" "$COMMANDS_DEST/$name.md" "$name"
  cp "$COMMANDS_DEST/$name.md" "$PROMPTS_DEST/$name.md"
done

log "Writing inventories"
mkdir -p "$DOCS_DEST"
write_inventory

skill_count="$(find "$SKILLS_DEST" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"
agent_count="$(find "$AGENTS_DEST" -mindepth 1 -maxdepth 1 -type f -name '*.toml' | wc -l | tr -d ' ')"
command_count="$(find "$COMMANDS_DEST" -mindepth 1 -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')"

log "Done"
printf 'skills=%s agents=%s commands=%s\n' "$skill_count" "$agent_count" "$command_count"
