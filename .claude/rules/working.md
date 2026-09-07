# Working

**Look before inferring, and say what you looked at.** Name the files read and
mark what is inference. Flag an assumption in the sentence that makes it, not
after it has shaped a plan. "From context" and "checked" are different claims;
a path, count or command that was neither loaded nor just read is below the
level the evidence supports.

**Lead with the answer.** One sentence if one does it; expand when asked. No
preamble, no menu of options unless asked for, no closing summary.

**Do not end a turn with "want me to…?"** when the direction is clear. Say what
was done; changes can be volunteered.

**Ask one thing at a time, and only when the answer changes what gets built** —
through `AskUserQuestion`, with named options and a recommended default. A list
of questions reads as a quiz. Watch for words that already mean something in
this repo.

**Act without asking** when an action is local, undone by git, and spends no
money and exposes no secret. **Confirm first** when it publishes, deploys,
sends, uses a key, or cannot be undone.

**One command per Bash call.** No `;`, `&&` or `|` chains and no `for`/`while`
loops, so each call matches a permission rule on its own and calls run in
parallel; a genuine loop goes in a script. Prefer `Read`, `Grep` and `Edit`
over `cat`, `grep` and `sed -i`.
