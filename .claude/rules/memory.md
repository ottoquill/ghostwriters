# Memory

What a later session needs to know lives in `memory/` at the repo root, under
git. `autoMemoryDirectory` in `.claude/settings.json` points the auto-memory
system there. Never write memory under `~/.claude/` or `.claude/` instead: the
first is outside source control, and the second prompts on every write, which
no allowlist entry can suppress.

- `memory/where-we-are.md` is loaded into every session: the arc, the decisions
  in force, the live defects, what is parked — dated. When a decision is made or
  the direction moves, update it in the same turn and bump the date. Before
  acting on a specific it states — a count, a path, whether a script runs —
  check the disk; specifics go stale first.
- `memory/MEMORY.md` is the index, one line per file. Each memory is one file
  with `name`, `description` and `type` frontmatter, a **Why** and a **How to
  apply**; link related ones with `[[name]]`. Prefix the filename by scope:
  `global-` for any project, `project-` for this one, `topic-` for one subject.
- Paraphrase feedback and do not name the user. The repo is public.
- Do not record what the repo, its history, or a rule already says.
