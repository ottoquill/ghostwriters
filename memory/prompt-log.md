# Permission prompt log

Appended by the `PermissionRequest` hook in `.claude/settings.json`, one line
per dialog shown, so a prompt is captured even when a session forgets it. This
is the queue [permissions.md](../.claude/rules/permissions.md) drains: for each
`pending` line, add the exact `allow:` entry that ends it, then mark the line
resolved or delete it. Empty is the goal.

Format: `- <date> | <tool>(<target>) | fix: | pending`

<!-- entries are appended below -->
