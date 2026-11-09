# Verify: crew-reads-each-pieces-end-from-the-runners-report

Checked on `change/crew-reads-each-pieces-end-from-the-runners-report` at b5cf3481, cut from `bolt/crew-reads-every-end-from-the-runner`, merge-base with main 05ffe51e, on 2026-11-09.

## The whole checks

`tests/suite --affected`, run once, as CLAUDE.md names it for a change that is done: **28 passed (2 replayed), 0 failed**, exit 0.

- Ran: `logic`, `contract`, and every end-to-end test (`t-briefs`, `t-cards`, `t-flume-source`, `t-help`, `t-hold`, `t-journey-board`, `t-journey-cross`, `t-journey-main`, `t-journey-main-fix`, `t-journey-ops`, `t-journey-plan`, `t-journey-review`, `t-journey-roles`, `t-journey-signals`, `t-journey-state`, `t-roles`, `t-runner`, `t-session-hook`, `t-slot`, `t-sluice`, `t-stage-facts`, `t-suite`, `t-teams`, `t-waits`).
- Replayed: `t-docs` and `t-journey-land`, from passing runs on this host with identical inputs (the code stage ran both by name for tasks 3.1 and 3.2).
- Not affected: `mod`, since nothing under `plugin/hooks/` or `plugin/tests/` changed, and the `nix` project's tasks, since nothing of the flake changed.

`openspec validate crew-reads-each-pieces-end-from-the-runners-report --strict`: valid.

## Tasks

All 10 tasks in `tasks.md` are ticked. Each one's named check exists and passed in the run above:

| Task | Check | Where |
|---|---|---|
| 1.1 | `TestStageOf::test_a_landing_held_for_the_runner_is_merged_at_its_commit`, `test_a_drop_held_for_the_runner_is_dropped`; fixtures `landed-held.json`, `dropped-held.json`, `version.txt` and `README` | `tests/py/test_runner.py`; `tests/py/flume-0.20.0/` |
| 2.1 | `TestEndsHeldForTheRunner`'s place cases; `TestCrossed::test_a_crossed_bolts_fix_held_for_the_runner_reads_merged` | `tests/py/test_stages.py` |
| 2.2 | `TestVerification`; `test_a_head_held_for_the_runner_reads_green_and_one_only_a_landing_commit_names_reads_none` | `tests/py/test_runner.py`, `tests/py/test_stages.py` |
| 2.3 | `TestAFixTheRunnerReportsMerged`, `test_a_fix_held_for_the_runner_landed_is_not_dropped` | `tests/py/test_fix.py` |
| 2.4 | `test_a_landed_bolt_whose_places_are_held_for_the_runner_closes`, `test_a_piece_whose_end_the_runner_never_carried_keeps_the_bolt_open` | `tests/py/test_stages.py` |
| 2.5 | `test_stages_for_asks_the_survey_for_each_started_bolt_and_seeks_nothing`; `TestWhenABoltIsFetched`; `tests/py/test_main_landing.py` removed | `tests/py/test_stages.py`, `tests/py/test_bolt_commands.py` |
| 2.6 | `test_a_gather_of_a_kit_with_a_held_bolt_runs_no_sluice`; `test_kit.py`'s `TestLandedFrom` removed | `tests/contract/test_gather.py`, `tests/py/test_kit.py` |
| 2.7 | `TestCrewBoltsCrossed::test_a_bolt_whose_places_the_runner_holds_ended_reads_each_unit_merged`; `test_a_bolt_whose_head_is_its_take_main_fix_landed_beside_the_queue_can_land` | `tests/py/test_bolt_commands.py`, `tests/py/test_rail.py` |
| 3.1 | `t-docs` | `tests/t-docs.sh` |
| 3.2 | `t-journey-land` | `tests/t-journey-land.sh` |

## Requirements against the code

### bolt-plan

- **A launched place's stage is where Flume's status has it** (modified). `runner.stage_of` and `flume_facts` are unchanged. They already read a tidied entry at `<location>@<at>` and its `over` as merged at its commit on a bolt, landed on main, or dropped (design Decision 1).
  - "A landing held for the runner": `test_a_landing_held_for_the_runner_is_merged_at_its_commit` reads merged at `f564d22` on a bolt and landed for `Base: main`. `test_a_place_landed_and_tidied_reads_merged_from_the_record_held_for_the_runner` reads `a` merged, carried at the record's time, and landed once main holds it.
  - "A drop held for the runner": `test_a_drop_held_for_the_runner_is_dropped`.
  - "A place tidied before the runner carried its end": `b` reads submitted, and `crossed_changes` is empty, with a `landings` fact naming `change/b` that nothing reads.
  - The scenarios carried over unchanged keep their earlier cases, which passed.
- **A unit's stage is read from the runner, or from the plan before its bolt starts** (modified). `Stages.crossed` takes `stage_of`'s answer as given. The `built_on_bolt` call and the `carried` override are gone. "A launch refused for a change the bolt holds" reads refused in the runner's words, with the bolt's landing commits unread.
- **The removed requirements** have no code left behind:
  - "A unit whose work its bolt's branch holds is built"
  - "A fix whose place's landing its bolt's branch holds is merged"
  - "A bolt's landing is read from its kit's main"
  - "A landed bolt's pieces are read from its landing"
  - "A fix read merged from its bolt's landing holds nothing"

  The following are gone, and a grep of `plugin/` and `tests/` finds none of them:
  - `runner.built_on_bolt`, `Stages.landings`, `landing_sought`, `seek_answered`, `submits_read` and `submits_at`;
  - gather's `FROM`, `landed_from`, `LANDINGS`, `bolt_landings`, `LANDED` and `main_landing`;
  - `survey`'s `seek`.

  `runs_at` returns `{"landings"}` alone. `plan.LANDED` and `plan.LANDINGS`, which share those names, are the bolt's landing script and the card's state path, and are not gather's.
- **A fix the runner reports merged holds nothing** (added). `Stages.fixes` returns `runner.fixes_on`'s stage as it is. `fix_flume` has lost its `landings` parameter, and `crew fix --drop` reads no stages before its write.
  - "A landed fix holds its bolt's landing no longer": tidy is merged, `fixes_in_flight` is empty, and `landing_unready` is None.
  - "A landed fix is not dropped": refused with "has merged into bolt/x", and nothing is appended.
  - "A fix the runner last carried at submitted": submitted and in flight, and its drop goes.

### bolt-teams

- **A bolt whose landing main holds closes whatever the runner carried of its places** (removed). Nothing of it is left in `plan.py`.
- **A landed bolt closes on its pieces' ends as the runner reports them** (added). Both scenarios pass through `plan.land_refusal`, on top of `runner.unlanded`, which this change leaves alone (design Decision 6):
  - "A landed bolt whose branch and places are gone": refused for no piece, with `bolt/x` gone and each piece merged at the held record's commit.
  - "A piece whose end the runner never carried": refused with "unit b has not merged into bolt/x: it is submitted".

### merge-gate

- **A bolt's verification is its work's landing at its head, as the runner reports it** (modified). `runner.verification` lost its `how`. Green always says "as the runner reports it", and `piece_said` lost its "landed on its bolt" detail.
  - "A landing held for the runner" reads green.
  - "A landing read from the bolt's own landings" reads none and leaves the bolt `active`.
  - "A take-main fix landed beside the queue" reads green, naming the fix, and is a landings-card row that can land.
  - "Nothing of sluice's is read": the contract case runs no `sluice`, and the gather's answer for `te` carries none of `verdict`, `beside`, `landings`, `landed`, `landings_error` or `landed_error`.
  - "A head that is no landing of the bolt's work" and "No head" keep their earlier cases, which passed.

## Other checks

- `docs.2`: README, `plugin/skills/crew/SKILL.md` and `plugin/bin/crew`'s usage header each say a piece's end is the runner's report alone, a record held for the runner after Flume's tidy among them. Each also says a landed bolt closes once each piece reads landed so. None of them names `Sluice-From`, or a landing on the bolt or main, as what makes a piece merged. `t-docs` pins them.
- `docs.7`: the change edits nothing under `docs/architecture/` or `docs/adr/`. As the design says, after the landing the design agent lifts `tests.5`'s "or record 0062's stopgap reads it" and marks record 0062 retired.
- `code.8`: no view key changes. `status.js` reads none of `on`, `branch` or `landed`, so `mod` was not affected.
- `code.7`: `stage_of`, `verification`, `unlanded` and `fixes_in_flight` stay decisions on facts.
- Two citations of record 0062's other parts remain, and both are deliberate:
  - **Decision 1 of `a-bolts-landing-on-main-reads-landed`**, the kit's folder read from the runner's `repositories.rec`. It is cited in `tests/lib.sh`, `tests/py/facts.py`, `tests/py/test_board.py` and `tests/t-journey-cross.sh`. It is a reading of the runner's report and stays, as the design's non-goals say.
  - **The remaining `Sluice-From` readers**: `plan.pull_of`, the landing card's pull request, and `ops.RANGE`, a deploy's landings. They name what a landing or deploy carries, never a piece's end, as the design's non-goals say.
- Specs after the archive: see Findings.

## Findings

No finding blocks the change.

- `merge-gate` validates strict before the archive. `bolt-plan` and `bolt-teams` already fail strict on length warnings alone (7 and 11 requirements over 500 characters), as most of crew's specs do. The archive writes this change's requirements into all three. A rise in those warnings is a wording matter for a later change, as earlier verifies found.
- The reading is whole only on a host whose runner carries agentplot/boomdrive `76e0226` and whose Flume is 0.20.0 or later (design *Dependencies*). Elsewhere a place tidied after its landing reads as last carried, which is Decision 3's intended outcome.
- Decision 7, removing `started_land`'s fallback to `main_landed` once main is taken in, is for the bolt's take-main fix. This bolt does not hold that code.

The whole checks pass, and the work holds against every requirement and scenario of the change's three delta specs.
