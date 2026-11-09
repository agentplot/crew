# Verify: crew-lands-each-bolt-through-flumes-base-place

Read 2026-11-08 on `change/crew-lands-each-bolt-through-flumes-base-place` at `98144f4d`. **Verdict: not ready to archive.** The whole checks pass, every task is ticked, and no function or case cites a requirement this change removes. But 18 lines in `plugin/` and `tests/` cite, by name, a requirement or scenario that no spec holds, before this change is archived or after. Every one of them was added on this change's branch. The change goes back to its code stage with what follows.

## The whole checks

`tests/suite` was run once from the worktree's root. It runs every project's `check-full` tasks, as sluice selects them. Result: **33 passed (5 replayed), 0 failed**, exit 0.

Run afresh: `contract`, `logic`, and every end-to-end test (`t-briefs`, `t-cards`, `t-docs`, `t-flume-source`, `t-help`, `t-hold`, `t-journey-board`, `t-journey-cross`, `t-journey-land`, `t-journey-main`, `t-journey-main-fix`, `t-journey-ops`, `t-journey-plan`, `t-journey-review`, `t-journey-roles`, `t-journey-signals`, `t-journey-state`, `t-roles`, `t-runner`, `t-session-hook`, `t-slot`, `t-sluice`, `t-stage-facts`, `t-suite`, `t-teams`, `t-waits`). Replayed from an earlier passing run on identical inputs: `mod`, `nix:format`, `nix:lint`, `nix:test`, `nix:typecheck`.

## Tasks

All 41 tasks in `tasks.md` are ticked. `openspec validate crew-lands-each-bolt-through-flumes-base-place --strict` passes.

Task 5.11's check holds. Its grep prints nothing. The six files its pytest names are in the logic tier, which passed.

The one commit since the last verify (`98144f4d`) changes only docstrings and comments. Each changed Python file parses to the same syntax tree as at `95d7d475` once docstrings are blanked.

## How the citations were checked

crew's convention is that a function or case names the requirement or scenario it serves, as `<capability> "<name>"`, so a case reads as its spec's scenario.

Every such citation in `plugin/`, `tests/` and the change's own documents was read, including the later names of a list (`"A", "B" and "C"`) and a citation wrapped across lines. Each was checked against the names its capability holds once the change is applied: requirements and scenarios. That set is the main specs, less each delta's REMOVED requirements, with its ADDED and MODIFIED requirements and their scenarios in their place.

The same check was run on the branch's base (`4b813f18`) against the specs there, and only the citations new on this branch are reported. The base already held unresolved citations, mostly shorthand. They are not this change's and are left out.

- **No citation names a requirement this change removes.**
- **The deltas, `design.md`, `proposal.md` and `tasks.md` cite only names that resolve.**
- **18 lines added on this branch cite names that resolve nowhere.**

## Citations that name nothing in any spec

Each cited name below is in no spec, main or delta, under any capability. The functions and cases are right, and their behaviour matches the scenario they mean. Only the name is wrong. Each should cite the name its spec holds:

| Cited at | Cites | The spec's name |
|---|---|---|
| `plugin/lib/plan.py:4172`, `4193`; `tests/py/test_landing.py:682` | bolt-teams "A fix while the landing is under test" | Scenario "A fix while the landing is queued", of requirement "A landing queued holds its bolt's work" |
| `tests/py/test_landing.py:870` | bolt-teams "A landing asked holds its bolt's work" | "A landing queued holds its bolt's work" |
| `tests/py/test_landing.py:737` | bolt-teams "The first read after a landing's outcome records it and acts on it" | "A landing is recorded by the first act that reads it in the runner's report" |
| `tests/py/test_landings.py:2098` | bolt-teams "Read from any host" | "A landing's record rests on the state repository alone", whose scenario is "Read away from the kit's host" |
| `plugin/lib/runner.py:1165`; `tests/py/test_runner.py:934` | bolt-teams "A bolt's drop drops its base place last, and asks it again after a refusal" | Two requirements: "A bolt's drop drops its base place last" and "A base place's drop the runner refused is asked again once nothing on its branch is live" |
| `tests/py/test_tidy.py:17` | bolt-teams "crew deletes no bolt branch and removes no landing worktree" | "crew removes no worktree, and names a landing's left from before" |
| `plugin/tests/status.test.ts:100`; `tests/py/test_board.py:2112` | crew-board "A bolt's landing on its head line and in the bands" | No crew-board requirement or scenario has this name. The head line's landing is in crew-board "Construction shows each bolt in flight as a ledger, with no server for a started bolt's work" (scenarios "A landing asked", "A landing standing in sluice"). The code stage names the one each case proves. |
| `tests/py/test_board_word.py:108` | board-page "A word from the board lands nothing" | "A word from the board answers nothing" |
| `tests/py/test_rail.py:217` | crew-rail "A landing asked" and "A landing in the merge queue" | crew-rail's scenarios "A land asked" and "A landing queued". The third name on the line, "A landing crew can't tell", resolves. |
| `tests/py/test_rail.py:240` | crew-rail "A landing refused for a failed check" | crew-rail's scenario "A refused landing". The second name on the line, "A landing refused in conflict", resolves. |
| `tests/py/test_record.py:61` | run-record "A land's entry names its request" | "A land crew posts is one entry naming its request" |

Three more lines added on this branch cite a requirement by the start of its name only. Task 5.11 counts a shorthand as something to fix:

| Cited at | Cites | The spec's name |
|---|---|---|
| `tests/py/test_bolt_commands.py:92` | drive-state "What comes before a runner takes a kit's work" | "What comes before a runner takes a kit's work is done on the main-level host" |
| `tests/py/test_landings.py:117` | rail-cards "A bolt started before bolts were base places" | "A bolt started before bolts were base places has no box", which line 1983 of the same file cites whole |
| `tests/py/test_runner.py:542-543` | merge-gate "A bolt's verification is its work's landing at its head" | "A bolt's verification is its work's landing at its head, as the runner reports it" |

A check that proves the fix, written to run as it stands. It prints these 18 lines at `98144f4d` and nothing once the work is done:

```
grep -rnE 'landing is under test"|asks it again after a refusal"|head line and in the bands"|board lands nothing"|A landing asked holds|records it and acts on it"|"Read from any host"|crew-rail "A landing asked"|"A landing in the merge queue"|refused for a failed check"|entry names its request"|removes no landing worktree"|"What comes before a runner takes a kit.s work"|rail-cards "A bolt started before bolts were base places"|^ *verification is its work.s landing at its head"' plugin tests
```

## What holds

Apart from the citations above, the work holds against the delta:

- The whole checks pass.
- Every task is ticked, and task 5.11's check prints nothing.
- No code or case cites a removed requirement.
- The deltas' own citations resolve.
- The last verify's spot checks still stand, since the only commit since then changes docstrings alone:
  - The leftovers of crew's own sluice landing are gone from `plugin/`.
  - `crew bolt submit`'s usage says it refuses at once.
  - `plugin/flume/kinds/bolt@1/kind.toml` lands with no stages on `bolt` branches.
  - `tests/py/test_no_tool_for_a_bolt.py` pins that no command runs a tool for a bolt.
  - The start's and landing's sluice scripts and `kit.policy_said` are gone.
