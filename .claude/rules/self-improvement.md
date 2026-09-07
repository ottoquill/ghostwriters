# Self-improvement

Friction is a request repeated or rephrased, an assumption corrected, a tool
call overridden, a prompt denied, output at the wrong length or level. When it
happens, write one file to `memory/friction/` with the hypothesised cause and
enough context to judge it later, prefixed by scope, and index it.

Friction consolidates upward, like a generational collector:

1. `memory/friction/` — one observation per file. Cheap; expected to be pruned.
2. `memory/patterns/` — when two or three observations share a theme, merge
   them into one pattern that names the recurring issue and the emerging rule,
   and delete the files it consumed.
3. `.claude/rules/` — when a pattern has held across several conversations,
   propose it as a rule. Rules are checked in and bind every later session:
   ask before adding or changing one. A `global-` pattern belongs somewhere
   shared across projects; propose where.

At the start of a conversation scan `memory/friction/` and consolidate what is
ready; at the end of a substantial one, ask whether an observation is due.

Not friction: a one-off cleared up at once, a tool or network fault, anything a
rule already covers, or a permission prompt — that is a settings bug, see
[permissions.md](permissions.md).
