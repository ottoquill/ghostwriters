#!/usr/bin/env bash
#
# PreToolUse hook: makes "never edit these" structural instead of advisory.
# A PreToolUse deny fires before any permission-mode check, so it holds under
# auto mode and --dangerously-skip-permissions alike.
#
#   ~/.claude/  outside source control. Config goes in the repo's .claude/,
#               memory in memory/. (Generic; keep this guard in any repo.)
#   sources/    the record of what the book says, verbatim. A wrong split is
#               fixed in scripts/fetch.py and re-run; the text is never edited.
#               (This repo's guard; swap the path for another repo's.)
#
# Fail-open: no jq, or no file path in the input, means allow.
set -uo pipefail

command -v jq >/dev/null 2>&1 || exit 0

input=$(cat)
file=$(printf '%s' "$input" | jq -r '.tool_input.file_path // .tool_input.notebook_path // empty' 2>/dev/null)
[ -z "$file" ] && exit 0

deny() {
  jq -nc --arg r "$1" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: $r
    }
  }'
  exit 0
}

case "$file" in
  "$HOME"/.claude/*)
    deny "$file is outside source control. Put project config in the repo's .claude/ and memory in memory/, so the change is reviewable and revertible."
    ;;
esac

root="${CLAUDE_PROJECT_DIR:-$PWD}"
case "$file" in
  "$root"/*) rel="${file#"$root"/}" ;;
  /*)        exit 0 ;;   # elsewhere on disk (a scratchpad) -- not ours
  *)         rel="$file" ;;
esac

case "$rel" in
  sources/*)
    deny "$rel is a source text and is never edited by hand. If the chapter split is wrong, fix CHAPTER_RE or is_subtitle in scripts/fetch.py and run it again."
    ;;
esac

exit 0
