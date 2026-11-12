# Verify: a-landed-bolt-is-closed-and-offered-no-more

Verified on `change/a-landed-bolt-is-closed-and-offered-no-more` at `5f1d37ca`, 2026-11-11.

**Verdict: holds. The whole checks pass, every task is ticked, and every requirement and scenario of the specs is met. The change is archived with this report.**

## The whole checks

`tests/suite --affected` (CLAUDE.md, *Tests*), run once against the merge-base with `main`: **32 passed (31 replayed), 0 failed**, exit 0.

`logic` ran afresh. The other 31 replayed a pass on this host with identical inputs, `t-journey-board` among them at its current count of the quiet tick's fetches, `1 6`. Every task's inputs include crew's command core, so a replay means the same code and tests passed. The `check-full` run that sluice makes on the bolt with this work merged runs everything afresh.

## The change against its tasks

- All 16 tasks in `tasks.md` (1.1–6.1, with 4.3 and 5.2) are ticked.
- Each task's named check is in the tiers:
  - `TestLandingHead`, `TestOnMain` and `TestMainTip` are in `tests/py/test_landed_on_main.py`.
  - `TestMainHolds` is in `tests/contract/test_git.py`.
  - `TestABoltWhoseWorkIsOnMain` is in `tests/py/test_stages.py`.
  - `TestALandingReadOnMainIsRecorded`, `TestALandingReadOnMainCloses` and `TestCrewBoltLandOfAStartedBolt` are in `tests/py/test_landing.py`.
  - `TestTheSweepClosesABoltOnMain` and `TestABoltOnMainIsNoRow` are in `tests/py/test_landings.py`.
  - `TestABoltOnMainHasNoLandLine` and `TestCrossedLandings` are in `tests/py/test_rail.py`.
  - `TestTheFollowerFetchesEachKitsMain` is in `tests/py/test_board.py`.
  - The end-to-end checks are `t-journey-board` and `t-docs`.
- The logic, contract and end-to-end tiers above passed them all.
- `TestCrossedLandings.test_a_fix_in_flight_on_it_holds_its_landing` numbers its fix launch 5, a request of its own. So the case proves that a fix in flight holds the landing, and it no longer reads `bolt/x`'s base place landed (task 4.3).
- `t-journey-board`'s quiet tick counts `1 6`. Its comment names the mains of switchboard-kit and atlas-kit, which Decision 7 fetches (task 5.2).
- The design's note on `look` names the key `mains`, as the code does.

## The change against its specs

`openspec validate a-landed-bolt-is-closed-and-offered-no-more --strict`: valid. Each requirement's text above its first scenario is at most 491 characters, under `t-specs`' 500, the modified ones included.

### bolt-teams, added requirements

- **"A bolt whose work is on its kit's main reads landed"** is met by `plan.landing_head`, `main_asks`, `on_main`, `main_tip`, `main_holds`, `landed_by` and `Stages.main_landing`. They read GitHub's main in crew's cache only, and read no trailer and no host. The scenarios:
  - *An older crew landed* and *A host's checkout of main is gone*: `test_a_bolt_an_older_crew_landed_reads_landed_at_mains_commit`, which asks only the cache's tip of `afterthought/crew`.
  - *The runner reports stopped*: `test_a_base_place_the_runner_reports_stopped_reads_landed_once_main_holds_its_work`.
  - *A unit main does not hold*: `test_a_units_commit_main_does_not_hold_gives_unlanded_words`.
  - *A unit not merged*: `test_a_unit_in_code_*`, in both `TestOnMain` and `TestABoltWhoseWorkIsOnMain`, which ask git nothing.
  - *A newer landing main does not hold*: `TestLandingHead.test_a_land_asked_at_a_newer_head_after_a_stop_gives_that_head_and_its_request` with `test_the_head_main_does_not_hold_with_the_units_held_gives_the_heads_words`.
  - *A bolt with no work of its own*: `test_no_work_and_no_head_holds_no_work_on_main`.
  - *Main can't be read*: `test_main_that_cant_be_fetched_reads_the_reports_outcome` and `test_a_commit_git_cannot_tell_is_never_taken_as_landed`.
  - The contract cases pin git's answer for a merge, a fast-forward, a commit only another ref fetched, and one the cache never fetched.
- **"A bolt read landed on main is recorded and closed by the first act that reads it"** is met by `landing_entry`'s main branch, `landing_read`, `started_land` and the sweep's `landings_judged` and `reap_judged`. The scenarios:
  - *Nobody runs anything*: `TestALandingReadOnMainCloses.test_a_bolt_with_no_launch_of_its_own_on_main_is_recorded_and_closed` and `TestTheSweepClosesABoltOnMain.test_a_bolt_read_landed_on_main_with_nothing_posted_is_read`.
  - *The stop and the queued landing end*: `test_its_entry_ends_the_queued_landing_and_the_stop`.
  - *Two reads at once*: `test_the_same_read_again_records_nothing`.
  - *Its host can't be told*: `test_with_its_host_unknown_it_is_listed_under_the_main_level_host`.
  - The base place reported stopped is closed with ops asked nothing (`test_a_base_place_reported_stopped_on_main_is_closed_and_ops_asked_nothing`).
- **"A bolt read landed on main is offered no more"** is met by `land_read` returning no row and `rail_rows` skipping the bolt under *land*. The scenarios:
  - *Not on its kit's landings card*: `TestABoltOnMainIsNoRow.test_a_bolt_read_landed_on_main_is_no_row_and_no_land_of_it_is_posted`, where `lands_due` posts nothing for `y` or `z`.
  - *Not under land on the rail*: `TestABoltOnMainHasNoLandLine`.

### bolt-teams, modified requirements

- **"A landing's outcome is read from the runner's report"**: the report is read first, and an outcome not landed is read against main. The existing scenario cases pass, and `test_main_not_holding_it_leaves_todays_outcomes` pins that main lacking the work leaves each outcome as it was.
- **"A landing's entry names its kit, its head and its time"**:
  - *Its head read on main*: the head is `landed_by`'s commit. `test_a_bolt_merged_into_main_is_held_and_landed_by_its_merge_not_mains_tip` pins the merge `6cfc4ae` over main's tip, with two commits landed after it.
  - *Its time from the run record*: every close goes through `started_land`, the sweep's too (`landing_close` calls `bolt_land`). Its `bolt.land` takes `Age` and `Split` from `landing_spent`, which reads the run record alone, both for a bolt read landed on main and for one the report reads landed.
- **"crew bolt land closes a started bolt only once its base place reads landed"**, in `TestCrewBoltLandOfAStartedBolt`:
  - *Closed by hand before it landed*: `test_a_bolt_not_read_landed_is_refused_naming_its_outcome_and_records_nothing`.
  - *A base place held for the runner*: `test_a_base_place_held_for_the_runner_landed_closes_at_flumes_commit`.
  - *A landing main holds that the runner does not report*: `test_a_base_place_the_runner_no_longer_carries_is_refused_whatever_main_holds`.
  - *A landing main holds*: `test_a_stopped_base_place_closes_once_main_holds_its_head_and_its_chores_commit`.
- **"A bolt with no launch of its own lands under the crew that started it"**:
  - *crew bolts says so* and *No land is posted*: the legacy cases in `test_landing.py` and `test_landings.py`, which hold while main lacks the work.
  - *crew bolt land refuses it*: `test_a_bolt_started_before_bolts_were_base_places_is_refused_while_main_lacks_its_work`.
  - *crew bolt land closes it once main holds its work*: `test_a_bolt_started_before_bolts_were_base_places_closes_once_main_holds_its_work`.

### rail-cards, modified requirements

- **"A bolt started before bolts were base places has no box"**: a bolt with no launch of its own keeps its legacy row with no box while main lacks its work. Once main holds its work it has no row (*Landed by the crew that started it*), by the same `land_read` path, and `TestABoltOnMainHasNoLandLine` pins both sides.
- **"A landing the runner or Flume stopped keeps its box"**: `TestABoltOnMainIsNoRow.test_a_stopped_bolt_main_does_not_hold_keeps_its_box_and_its_stop` keeps the box and the stop while main lacks the head. *A stopped landing that landed* is no row, with no word of the stop. The existing cases for the runner's refusal, Flume's withdrawal, the next card and the head moving pass.

### Docs

`docs.2`: README, `plugin/skills/crew/SKILL.md` and `plugin/bin/crew`'s usage header each say that a started bolt whose work its kit's main holds reads landed, is closed whichever way it landed, and is offered on no landings card. `t-docs` passed.

`docs.7`: the change edits nothing under `docs/architecture/` or `docs/adr/`.
