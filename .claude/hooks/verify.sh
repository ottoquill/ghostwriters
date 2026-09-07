#!/usr/bin/env bash
#
# Stop hook: closes the verification loop.
#
# Rules in .claude/rules/ are advisory -- the model may or may not follow them.
# This makes the checkable subset deterministic: the turn cannot end while
# scripts/check.py is red. Without it, "looks done" is the only completion
# signal and the human becomes the verification loop.
#
# Generic apart from the one command below; swap it for another repo's gate.
set -uo pipefail

command -v jq >/dev/null 2>&1 || exit 0

input=$(cat)

# Claude is already continuing because of this hook -- let it stop, or we spin.
if [ "$(printf '%s' "$input" | jq -r '.stop_hook_active // false' 2>/dev/null)" = "true" ]; then
  exit 0
fi

root="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"

if out=$(python3 "$root/scripts/check.py" --root "$root" 2>&1); then
  exit 0
fi

jq -nc --arg out "$out" '{
  decision: "block",
  reason: ("scripts/check.py is failing, so this work is not done. Fix every problem below and re-run it -- do not stop while it is red.\n\n" + $out)
}'
exit 0
