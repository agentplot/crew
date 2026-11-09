# Verify: crew-lands-each-bolt-through-flumes-base-place

Read 2026-11-08 on `change/crew-lands-each-bolt-through-flumes-base-place` at `95d7d475`. **Verdict: not ready to archive.** The whole checks pass and every requirement name the deltas cite resolves. But crew's code and tests still cite six requirements that this change removes. Once archived, each of those citations names a requirement no spec holds. The change goes back to its code stage with what follows.

## The whole checks

`tests/suite` was run once from the worktree's root. It runs every project's `check-full` tasks, as sluice selects them. Result: **33 passed (33 replayed), 0 failed**, exit 0.

Each task was replayed from an earlier passing run on identical inputs: `contract`, `logic`, `mod`, `nix:format`, `nix:lint`, `nix:test`, `nix:typecheck`, `t-briefs`, `t-cards`, `t-docs`, `t-flume-source`, `t-help`, `t-hold`, `t-journey-board`, `t-journey-cross`, `t-journey-land`, `t-journey-main`, `t-journey-main-fix`, `t-journey-ops`, `t-journey-plan`, `t-journey-review`, `t-journey-roles`, `t-journey-signals`, `t-journey-state`, `t-roles`, `t-runner`, `t-session-hook`, `t-slot`, `t-sluice`, `t-stage-facts`, `t-suite`, `t-teams`, `t-waits`. The one commit since the last verify (`95d7d475`) changes only `specs/run-record/spec.md` and `tasks.md`, which no task takes as an input.

## Tasks

All 40 tasks in `tasks.md` are ticked. `openspec validate crew-lands-each-bolt-through-flumes-base-place --strict` passes.

Task 9.5's check holds. run-record's "A landing's Submission is the merge queue's entry Flume names" now cites bolt-teams "A landing is recorded by the first act that reads it in the runner's report", and the task's grep prints 0.

## Words in the delta

Every quoted `<capability> "<requirement>"` citation in the deltas, `design.md`, `proposal.md` and `tasks.md` was checked against the requirements each capability holds once the change is applied. That set is the main specs, plus each delta's ADDED and MODIFIED names, less its REMOVED ones. All 8 citations resolve.

## Requirements the code still cites after their removal

crew's convention is that a function or case names the requirement it serves, so the case reads as its spec's scenario. The deltas remove 27 requirements, and each REMOVED entry's Migration names what replaces it. Six of those removed names are still cited in `plugin/lib/plan.py` and `tests/py/`. After `openspec archive`, every citation below names a requirement no spec holds.

Task 5.9 has "the docstrings and usage lines naming crew's sluice landing go". The leftovers the first verify named are gone. These citations, and the sluice-landing wording around them, remain:

| Removed requirement | Its Migration | Cited at |
|---|---|---|
| bolt-teams "A landing sluice sent back is the bolt's fix" | "A landing Flume's verdict sent back is the bolt's fix" | `plan.py:2591-2592` (`sent_back`); `test_landing.py:53`; `test_landings.py:137-138` |
| rail-cards "A landing sluice or its host stopped keeps its box" | "A landing the runner or Flume stopped keeps its box"; a failed verdict as "A refused landing is held on its row" | `plan.py:2625-2626` (`stops`), `2721` (`landing_rows`); `test_landings.py:161`, `316`; `test_cards.py:1626` |
| main-level "Ops lands a bolt on a send that still stands" | crew's own raise carries a standing send; what `crew card read land/<kit>` prints is rail-cards' ("The landings card's read prints the lands crew posted") | `plan.py:11623`, `11627-11628` (the card's read), `11726-11727` (`landings_unopened`); `test_landings.py:948`, `1000`; `test_card_commands.py:1260` |
| main-level "A landing stopped in ops's pane is recorded as the user's words" | main-level "A stop said in ops's pane is read as the user's words", "A stop crew cannot read as the user's words is refused", "A stop is recorded holding none of the user's words" | `plan.py:3958` (`leave_word_refusal`), `4397-4398` (`crew bolt leave`); `test_pane_landing.py:64`; `test_parser.py:40` |
| role-runs "Main-level ops's landing from a run does not wait" | role-runs "A capture and a landing are asks" and "Main-level ops's run lands nothing" | `test_landing.py:599` (`TestTheLandingsAsks`) |

The same docstrings still describe crew's own sluice landing as current:

- `sent_back` (`plan.py:2589-2600`): "sluice's number for the submission", and a stop from "a `wt submit` that read nothing and submitted nothing".
- `refusals` and `stops` (`plan.py:2616-2631`): "sluice refused", "sluice or its host stopped".
- `landing_rows` (`plan.py:2716-2724`): "sluice refused", "sluice's rejection of its landing".
- `landing_phase` (`plan.py:4068-4080`): "sluice queued", "sluice refused in its answer, standing through a later submit that submitted nothing at its head".
- The card's read (`plan.py:11620-11628`): "the submit lands them before this card's".
- `TestTheLandingsAsks` (`test_landing.py:597-599`): "asks main-level ops with sluice's words, keyed by the submission".
- `test_landing.py:52-56` and `test_landings.py:136-140`: "a later crew bolt submit at the head sluice sent back".

The delta now reads a refusal or a stop from Flume's verdict as the runner reports it. `crew bolt submit` lands nothing.

No behaviour is wrong: the cases pass, and the functions still serve live requirements under their new names. Each citation should name the requirement its Migration gives, and each docstring should say the landing as the runner reports it. A check that proves this, written to run as it stands:

```
grep -rnE "sent back is the bolt's fix|pane is recorded as the|host stopped keeps its box|send that still stands\"|landing from a run does not|^ *bolt's fix\"" plugin tests
```

The fragments are chosen so that a citation wrapped across two lines is still caught. The check prints 19 lines at `95d7d475` and nothing once the work is done. `docs/architecture/` and `docs/adr/` are the design agent's (`docs.7`) and are left out of it.

## What holds

Apart from the citations above, the work holds against the delta:

- The whole checks pass.
- Every task is ticked.
- The deltas' citations resolve.
- The leftovers the first verify named are gone from `plugin/`: `landing_ended`, `landing_not_landed`, `land_delete`, `landing_split`, `LAND_COPIES`, plan.py's `LANDINGS`, and the card's sluice words. gather.py's `LANDINGS` is a different thing: it reads sluice's merges into a bolt.
- `crew bolt submit`'s usage line says it refuses at once.
- The pieces spot-checked against the delta are where it says they are:
  - `plugin/flume/kinds/bolt@1/kind.toml` lands with no stages on `bolt` branches.
  - `tests/py/test_no_tool_for_a_bolt.py` pins that no command runs a tool for a bolt.
  - The start's and landing's sluice scripts and `kit.policy_said` are gone.
