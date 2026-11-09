# Verify: crew-lands-each-bolt-through-flumes-base-place

Read 2026-11-08 on `change/crew-lands-each-bolt-through-flumes-base-place` at `5a318f97`. **Verdict: ready to archive.** The whole checks pass. Every task is ticked, the change validates strictly, and every requirement or scenario named by a function or case this branch adds resolves to a name its spec holds once the change is applied.

## The whole checks

`tests/suite` was run once from the worktree's root. It runs every project's `check-full` tasks, as sluice selects them. Result: **33 passed (4 replayed), 0 failed**, exit 0.

Run afresh: `contract`, `logic`, `mod`, and every end-to-end test (`t-briefs`, `t-cards`, `t-docs`, `t-flume-source`, `t-help`, `t-hold`, `t-journey-board`, `t-journey-cross`, `t-journey-land`, `t-journey-main`, `t-journey-main-fix`, `t-journey-ops`, `t-journey-plan`, `t-journey-review`, `t-journey-roles`, `t-journey-signals`, `t-journey-state`, `t-roles`, `t-runner`, `t-session-hook`, `t-slot`, `t-sluice`, `t-stage-facts`, `t-suite`, `t-teams`, `t-waits`). Replayed from an earlier passing run on identical inputs: `nix:format`, `nix:lint`, `nix:test`, `nix:typecheck`.

## Tasks

All 42 tasks in `tasks.md` are ticked. `openspec validate crew-lands-each-bolt-through-flumes-base-place --strict` passes.

Task 5.12's check, the last verify's grep read with `-I`, prints nothing. Task 5.11's check still prints nothing.

## What changed since the last verify

The last verify read `98144f4d`. One commit came after it, `5a318f97`. It rewrites the 18 citations that verify found naming nothing in any spec, and adds task 5.12 recording the fix.

The commit changes only docstrings and comments:

- Each of its 11 Python files parses to the same syntax tree as at `98144f4d` once docstrings are blanked.
- Its one TypeScript change, `plugin/tests/status.test.ts:100`, is a line comment.

So the behaviour the last verify found meeting the delta is the behaviour on this branch now.

## The citations

crew's convention is that a function or case names the requirement or scenario it serves, as `<capability> "<name>"`, so a case reads as its spec's scenario.

Every such citation in `plugin/` and `tests/` was read, including the later names of a list (`"A", "B" and "C"`) and a citation wrapped across lines. Each was checked against the names its capability holds once the change is applied. That set is the main specs, less each delta's REMOVED requirements, with its ADDED and MODIFIED requirements and their scenarios in their place. The same check was run on the branch's base (`4b813f18`) against the specs there.

- **Every citation on a line this branch adds resolves.** Each of task 5.12's new names is a requirement or scenario its capability holds.
- **No citation names a requirement this change removes.** A citation that resolved at the base and resolves nowhere now would show as new; there is none.
- **The deltas, `design.md`, `proposal.md` and `tasks.md` cite only names that resolve.**

The base already held unresolved citations, mostly shorthand, such as rail-cards "A row taking main first stays on the card" at `plugin/lib/cards.py:883`. They are on lines this branch does not change, so they are not this change's and are left out.

## What holds

- The whole checks pass.
- Every task is ticked, and the checks of tasks 5.11 and 5.12 print nothing.
- Every citation this branch adds resolves, and none names a removed requirement.
- The last verify's findings still stand, since the only commit since then changes docstrings and comments alone:
  - The work meets the delta's requirements and scenarios.
  - The leftovers of crew's own sluice landing are gone from `plugin/`.
  - `crew bolt submit`'s usage says it refuses at once.
  - `plugin/flume/kinds/bolt@1/kind.toml` lands with no stages on `bolt` branches.
  - `tests/py/test_no_tool_for_a_bolt.py` pins that no command runs a tool for a bolt.
  - The start's and landing's sluice scripts and `kit.policy_said` are gone.
