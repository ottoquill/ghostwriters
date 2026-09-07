# The gate

`python3 scripts/check.py` is the definition of done. Run it before claiming a
change is finished; a `Stop` hook runs it anyway, and a red check blocks the
turn from ending. `.claude/CLAUDE.md` says what it checks.

Never weaken the check to make it pass — fix the content or the tool that made
it. When a rule is broken twice, the fix is a check, not a firmer rule. Before
claiming a new check closes a gap, plant a case known to be bad and confirm it
fails.
