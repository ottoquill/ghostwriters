# Permissions

A prompt for a routine command is a bug in `.claude/settings.json`, not
something to route around or remember. When one fires, propose the `allow:`
entry matching the shape that fired: `Bash(cmd:*)` covers bare `cmd` and
`cmd args`; an inner `*` between literal segments matches nothing. A hook
appends every prompt to `memory/prompt-log.md`; drain it before a long
unattended run.

Never widen your own permissions or install a hook silently. Build and test
the mechanism, then show the settings diff for the user to apply. A prompt on
a write under `.claude/` is correct and stays.

Keep bare `Edit` and `Write` in the allow list: the session mode drifts off
`acceptEdits`, and they are the safety net.
