#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE_DIR="${SOURCE_DIR:-/Users/frank_zhang/codex/migration-sources/seomachine-codex}"

COMMANDS_SRC="$SOURCE_DIR/.claude/commands"
COMMANDS_DEST="$ROOT_DIR/commands"
PROMPTS_DEST="$ROOT_DIR/prompts"
DOCS_DEST="$ROOT_DIR/docs"

render_command_prompt() {
  local src="$1"
  local dest="$2"
  local name="$3"

  {
    printf '# %s\n\n' "$name"
    printf '> 迁移来源：`seomachine-codex/.claude/commands/%s.md`\n\n' "$name"
    printf '> 用法：在 Codex 中把这份文件当作工作流模板使用，而不是当作 slash command。\n\n'
    printf '> 额外建议：优先结合本目录下的 `skills/`、`scripts/` 和 `context/`，不要只照搬文案流程。\n\n'
    awk '
      BEGIN { frontmatter = 0 }
      NR == 1 && $0 == "---" { frontmatter = 1; next }
      frontmatter == 1 && $0 == "---" { frontmatter = 0; next }
      frontmatter == 1 { next }
      { print }
    ' "$src"
  } > "$dest"
}

write_inventory() {
  {
    printf '# Commands Inventory\n\n'
    printf '| Command | Prompt File |\n'
    printf '| --- | --- |\n'
    for file in "$COMMANDS_DEST"/*.md; do
      [[ -f "$file" ]] || continue
      name="$(basename "$file")"
      printf '| `%s` | `%s` |\n' "${name%.md}" "$name"
    done
  } > "$DOCS_DEST/commands-inventory.md"
}

if [[ ! -d "$COMMANDS_SRC" ]]; then
  printf 'Missing source commands: %s\n' "$COMMANDS_SRC" >&2
  exit 1
fi

mkdir -p "$COMMANDS_DEST" "$PROMPTS_DEST" "$DOCS_DEST"
find "$COMMANDS_DEST" -mindepth 1 -maxdepth 1 -type f -name '*.md' -exec rm -f {} +
find "$PROMPTS_DEST" -mindepth 1 -maxdepth 1 -type f -name '*.md' -exec rm -f {} +

for src in "$COMMANDS_SRC"/*.md; do
  [[ -f "$src" ]] || continue
  name="$(basename "$src" .md)"
  render_command_prompt "$src" "$COMMANDS_DEST/$name.md" "$name"
  cp "$COMMANDS_DEST/$name.md" "$PROMPTS_DEST/$name.md"
done

write_inventory

printf 'commands=%s\n' "$(find "$COMMANDS_DEST" -mindepth 1 -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')"
