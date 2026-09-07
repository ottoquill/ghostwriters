# Session memory and workflow rules — design

2026-09-07. Approved in conversation before implementation.

## The ask

Make the repo remember more between sessions, support the owner's working
preferences, and write the rules generically enough to reuse elsewhere.

## Evidence

Read in full: `uniteum/ai`, the `.claude/` trees and CLAUDE.md of
`bitsy-services/wiki`, `gyrealm`, `interdotbox/interbox`, `uniteum/promo`,
`ottoquill/desk`, `gargantis`; `peatyscot` and `tinarex` CLAUDE.md; the three
`uniteum/ai` consumers' wiring; eight projects' uncommitted harness memory;
`~/.claude/hooks`; this repo's log. Counts by checksum and `ls`. The owner's
rule: two repos is not a pattern.

| Finding | Repos |
|---|---|
| Memory in the repo under git, never `~/.claude` | 11 |
| …and not under `.claude/`: writes there prompt and no allowlist suppresses it (gargantis `65a0f0a`) | 3 |
| Memory loaded by `@` import from CLAUDE.md | 2 (the newest two) |
| A dated orientation note — arc, decisions, defects — updated the turn a decision is made | 3 |
| Friction → pattern → rule ladder; `global-`/`project-`/`topic-` prefixes | 3 |
| Bash: no compound statements; irreversible-action tiers | 10+ |
| A recurring permission prompt is a settings bug; hook logs prompts to a file | 3 (+2) |
| No trailing "want me to?"; one decision at a time, never a quiz | 5 |
| A script is the definition of done, run by a Stop hook, never weakened | 4 |
| Claude commits, bodies carry the reasoning | 2 + this repo |
| Reuse: `uniteum/ai` submodule 3 (all uniteum) vs copy-and-adapt 6 (all ottoquill/wiki) | — |

## Decision

Portable files in this repo, not the `uniteum/ai` submodule: no ottoquill repo
vendors it, its `autonomy.md` contradicts practice here (auto-memory off,
`git add` denied, no `AskUserQuestion`), and its changes break three consumers.
File names match `uniteum/ai` where content overlaps so lifting is a copy.

## Design

**Memory, `memory/` at the root.** `where-we-are.md` in desk's shape, imported
by `.claude/CLAUDE.md` (`@../memory/where-we-are.md`; relative imports resolve
against the importing file). `MEMORY.md` index, `friction/`, `patterns/`,
`prompt-log.md`. Feedback paraphrased, no names: the repo is public.

**Rules, six generic files under `.claude/rules/`:** `memory.md`,
`self-improvement.md`, `working.md`, `commit-messages.md`, `permissions.md`,
`gate.md`. No `paths` frontmatter: the docs say a rule with no `paths` loads at
launch, while a `paths` pattern — `**` included — makes it load when a matching
file is read. The wiki family's `paths: ["**"]` is therefore not carried over.
Budget: about 100 always-on lines across the six.

**Gate.** `scripts/check.py`, stdlib, tests in `scripts/tests/`. Checks what a
script can prove: `do_not_name` absent from voice bodies and everything under
`out/`; nothing under `out/` for a source whose `pd_status.us` is not `true`;
draft H1 equals the source chapter's; assembled book only once every chapter
has a draft; voice frontmatter complete and `name` equal to the filename;
source chapters open on an H1. The per-voice Checklist stays with `/retell`.

**Hooks.** `verify.sh` (Stop; blocks while the check is red; honours
`stop_hook_active`) and `guard-write.sh` (PreToolUse deny on `sources/**` and
`~/.claude/**`). Both fail open without `jq`.

**Settings.** `.claude/settings.json`: an explicit allowlist of what the repo
runs, `ask` on `git push`, the three hook wirings, and `autoMemoryDirectory:
"~/git/ottoquill/ghostwriters/memory"` — the documented way to point the
harness's auto-memory at a directory, in place of `uniteum/ai`'s symlink
script. It must be absolute or `~/`-relative, so it is the one per-project
line; every repo here lives at `~/git/<org>/<name>`.

## Testing

Unit tests for the check, written first and watched to fail. Hooks fed JSON on
stdin: a `sources/` edit is denied, a `voices/` edit allowed; the Stop hook is
silent on a clean tree and blocks with the check's output on a planted
violation. A fresh `claude -p` session quotes the imported note back and names
its memory directory.

## Out of scope

Vendoring `uniteum/ai`; a `backlog/` directory; the harness memory symlink;
any rule found in fewer than three repos.
