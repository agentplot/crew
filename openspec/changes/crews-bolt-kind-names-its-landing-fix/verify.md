# Verify: crews-bolt-kind-names-its-landing-fix

Verified on `change/crews-bolt-kind-names-its-landing-fix` at `589ec3a6`, cut from `bolt/crew-lands-through-the-runners-land-message`, on 2026-11-08.

**Verdict: the whole checks pass and the work holds. The change is archived.**

## The whole checks

`tests/suite --affected`, run once as CLAUDE.md names it for a change that is done: **31 passed (5 replayed), 0 failed**, exit 0.

| Tier or project | Tasks |
|---|---|
| Logic, contract | `logic`, `contract` |
| Mod | `mod` (replayed) |
| Flake | `nix:test`, `nix:typecheck` (replayed) |
| End to end | `t-briefs` (replayed), `t-cards`, `t-docs` (replayed), `t-flume-source`, `t-help`, `t-hold`, `t-journey-board`, `t-journey-cross`, `t-journey-land`, `t-journey-main`, `t-journey-main-fix`, `t-journey-ops`, `t-journey-plan`, `t-journey-review`, `t-journey-roles`, `t-journey-signals`, `t-journey-state`, `t-roles`, `t-runner`, `t-session-hook`, `t-slot`, `t-sluice`, `t-stage-facts`, `t-suite`, `t-teams`, `t-waits` |

`openspec validate crews-bolt-kind-names-its-landing-fix --strict`: valid.

## Tasks

All 11 tasks in `tasks.md` are ticked, from 1.1 to 6.2.

## Requirements and scenarios

### flume-source

| Requirement | Where it holds |
|---|---|
| crew's bolt kind is a base place, and a version of it never changes | `plugin/flume/kinds/bolt@1/kind.toml` holds `landing_fix = "flume/fix@1"` and `max_landing_fixes = 3` and no other new key. *The package's bytes*: `tests/py/test_source.py` pins the bytes (`BOLT_KIND`) and the parsed table. *The landing fix is named by identity*: `test_the_landing_fix_is_named_by_identity_and_bounded`. |

### bolt-teams

| Requirement | Where it holds |
|---|---|
| A bolt's landing fix is read from its base place's status | `runner.flume_facts` reads `fix_kind`, `fix_limit`, `fixes` and `fixes_unread`, each field guarded (`fix_facts`, `count`). `runner.landing_fix` and `landing_way` decide whose the way on is, from plain facts (`code.7`). Each scenario has a case in `TestBasePlaceFixes` and `TestLandingFix` (`tests/py/test_runner.py`), on new fixtures in `tests/py/flume-0.19.0/`: *A host whose Flume names no fix kind* is `test_a_status_naming_no_fix_kind_leaves_the_way_on_crews` and `test_flume_0_17_names_no_fix_kind_and_no_fixes`; *A landing fix live* is `test_a_conflict_whose_landing_fix_is_live_is_flumes`; *A landing fix due* is `test_a_failure_with_no_fix_yet_is_flumes_and_due`; *The bound spent* is `test_a_failure_past_the_bound_is_its_callers`; *A fix dropped* is `test_a_fix_dropped_is_its_callers_naming_the_drop`; *A fix crew can't read* is `test_a_fix_crew_cant_read_whole_is_left_out_and_named`, where the fix is named in `fixes_unread`, kept out of `ran` and so counted toward no outcome. |
| crew launches no fix and asks for none where Flume launches the landing fix | `plan.landing_read` launches and asks nothing when `by` is `flume`. *Flume's fix takes main in* and *Flume's fix due* are cases in `tests/py/test_landing.py`. |
| A landing past its landing fixes is ops's | `plan.landing_read` asks ops once, in `runner.caller_said`'s words, and launches nothing when `by` is `caller`. *Past the bound* and *Read twice past the bound* are `test_past_the_bound_ops_is_asked_once_in_flumes_words_and_nothing_taken`. The dropped fix is `test_a_landing_fix_dropped_asks_ops_once_naming_the_drop_and_nothing_taken`. |
| A live landing fix holds its bolt | `runner.fixes_in_flight` adds the live landing fix under Flume's name, with its note (`landing_fix_note`). `base_drop_due` skips a base place whose landing fix is live. *No land while it runs* and *Taken main in* are `test_no_land_is_posted_while_it_runs_and_one_once_the_fix_that_took_main_in_has_landed` (`tests/py/test_landings.py`). *A drop while it runs* is `test_not_while_a_landing_fix_is_live_and_once_it_has_ended`. |
| A landing Flume's verdict sent back is the bolt's fix (modified) | `runner.landing_said` ends a refusal's words with `fix_clause` in place of crew's or ops's way on. *A check fails* with Flume 0.17.0 still gives the `crew fix` command (`test_a_status_naming_no_fix_kind_leaves_the_way_on_crews`). *A check fails with Flume's landing fix* is `test_a_failed_checks_landing_fix_names_no_command_for_ops`. The read-again, conflict-again and moved-head scenarios, with Flume's fix, are cases in `TestALiveLandingFixHoldsItsRow`. |
| A landing that conflicts with main takes main in by a fix place (modified) | `take_main_launch` runs only when `by` is `crew`. *Refused with Flume's landing fix* is the conflict case in `test_landing.py`, which appends no launch, and the row case in `test_landings.py`, which takes main first naming `y-1`. The earlier cases still hold on Flume 0.17.0. |
| A base place's drop the runner refused is asked again once nothing on its branch is live (modified) | `runner.base_drop_due`. *Not while a landing fix is live* is `test_not_while_a_landing_fix_is_live_and_once_it_has_ended`. |

### main-level

| Requirement | Where it holds |
|---|---|
| Main-level ops answers a landing that does not land (modified) | `plugin/roles/main-ops.md` says to start nothing where the row says Flume's landing fix covers it, and to start the fix only where the row names none or the bound is spent. Past the bound, ops starts a fix by hand or tells the planner and the user. A landing fix that asks is told to the user. `tests/t-briefs.sh` pins each of these phrases and the earlier ones, so both scenarios hold. |

### rail-cards

| Requirement | Where it holds |
|---|---|
| A row held by Flume's landing fix says so | `TestALiveLandingFixHoldsItsRow` in `tests/py/test_landings.py` has a case per scenario: *Taking main in by Flume's fix*, *A failed check's fix* and *Due*. |
| A row forecast to conflict with main takes main first until a fix takes main in (modified) | The note of a forecast's live landing fix begins as `plan.TAKE_MAIN` does, so the row takes main first. *Flume's forecast fix* is `test_a_forecasts_live_landing_fix_takes_main_first_and_the_raise_appends_no_request`. The earlier scenarios are unchanged and pass. |

### crew-board

| Requirement | Where it holds |
|---|---|
| Ops's band lists each landing fix Flume runs on a bolt | `board.flume_waits` adds each live landing fix after the take-main fixes, with the stage `landing fix`. *A landing fix in ops's band* is `test_a_landing_fix_in_ops_band` (`tests/py/test_board.py`). *The mod draws it* is the new case in `plugin/tests/status.test.ts`, run by the `mod` task (`code.8`). |
| A bolt's head line names its landing fix | `plan.landing_line` and `runner.landing_said` end the words with `fix_clause`. *A landing fix taking main in* and *The bound spent on the head line* are cases in `TestALandingFromTheRunnersReport`. |

## Notes

- The proposal's Impact lists `tests/t-docs.sh`, but the change leaves it as it was. No requirement asks it to pin the new README or skill words, and `t-docs` passes on them, as task 6.2 asks.
- Nothing in this change waits on a person, so no decision is open.
