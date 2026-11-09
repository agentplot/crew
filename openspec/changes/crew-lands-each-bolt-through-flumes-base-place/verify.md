# Verify: crew-lands-each-bolt-through-flumes-base-place

Read 2026-11-08 on `change/crew-lands-each-bolt-through-flumes-base-place` at `d4adecfc`. **Verdict: not ready to archive.** The whole checks fail, and the specs are not fully met. The change goes back to its code stage with what follows.

## The whole checks

`tests/suite` was run once from the worktree's root. It runs every project's `check-full` tasks, as sluice selects them. Result: **27 passed (4 replayed), 6 failed**, exit 1.

Passed: `contract`, `mod`, `nix:format`, `nix:lint`, `nix:test`, `nix:typecheck`, `t-briefs`, `t-cards`, `t-docs`, `t-flume-source`, `t-help`, `t-hold`, `t-journey-land`, `t-journey-main`, `t-journey-main-fix`, `t-journey-ops`, `t-journey-roles`, `t-journey-signals`, `t-journey-state`, `t-roles`, `t-runner`, `t-session-hook`, `t-slot`, `t-stage-facts`, `t-suite`, `t-teams`, `t-waits`.

Failed:

- **`logic`**: 14 failed, 3143 passed.
  - `test_asks.py::TestLand` (3 cases: `test_the_design_agents_records_are_a_chore_launch_on_the_repositorys_default_branch`, `test_a_blueprints_repository_or_one_the_plan_names_is_named_and_requests_follow_those_held`, `test_a_name_in_use_a_name_crew_does_not_mint_and_a_brief_with_no_words_or_no_file_are_refused`). Each one starts a process: `git init -q --bare ~/.cache/crew/git/afterthought/madswan-state.git`. conftest refuses that ("a logic test starts no process").
  - `test_proposals.py::TestStartProposed` (`test_its_card_is_checked_reading_no_kit`, `test_one_naming_a_bolt_started_already_is_refused_whole`). Both start a process: `git init -q --bare ~/.cache/crew/git/None.git`. A proposal's `bolt start` now reaches the state cache.
  - `test_bolt_time.py` (5 cases: `test_the_bolts_submissions_standing_over_the_decided_and_none_of_another_bolts`, `test_a_flume_places_submissions_are_the_bolts`, `test_a_landing_by_pull_request_is_the_bolts_by_the_number_its_queued_submit_names`, `test_submissions_that_cant_be_read_keep_the_age_and_tell_no_share`, `test_a_decided_submission_with_no_time_it_was_decided_is_said`). `bolt_facts` no longer yields submissions or `unknown`. The cases still expect sluice-era submissions: `[] == ['#61', '#62', '#63']`, `KeyError: 'unknown'`.
  - `test_cross.py::TestReach::test_a_drop_no_runner_has_taken_work_of_is_swept_in_the_main_level_hosts_checkout`. `drop_at` gives `(None, None)` where the case expects the main level's host.
  - `test_kit_rename.py::TestTheStartedBoltLands::test_one_seam_reads_merged_and_the_bolt_lands_in_the_renamed_clone_on_land_boomdrive_cloud`. The row reads `can: False` where `True` is expected.
  - `test_kits.py::TestNoFetchInTheRunnersClone` (2 cases). One fails with `module 'plan' has no attribute 'LANDED'`. The other fails because `POLICY` is no longer passed to `told(...)`. The case still lists scripts this change removed.
- **`t-journey-board`**: `expected '1 1 1 0', got '2 1 1 1'` at `tests/t-journey-board.sh:161`. These are the fetch and gather counts on mac-studio and the box.
- **`t-journey-cross`**: the test expects `next is started: sluice made bolt/next on GitHub (origin) from switchboard-kit's main at`. The start now says the base place is asked of the runner.
- **`t-journey-plan`**: `fatal: ambiguous argument 'bolt/tenant-environments'`. The test reads a branch the start no longer makes.
- **`t-journey-review`**: `fatal: invalid reference: origin/bolt/d1`. Same cause.
- **`t-sluice`**: the test expects `crew bolt start tenant-environments` to fail, as the sluice-version refusal did. The start now goes on.

None of these tests was among the narrow checks the tasks named, so the code stage never ran them.

## Tasks

All 21 tasks in `tasks.md` are ticked. `openspec validate crew-lands-each-bolt-through-flumes-base-place --strict` passes. Each task's own check passes in the suite, apart from the logic tier as a whole.

## Requirements not met

Each item was found by reading the code and tests against the delta. The first two were read again by hand.

1. **run-record, "A landing whose entry Flume names".** The scenario says a landed `bolt.submit` carries `Submission: 412`. `runner.landing_of`'s landed branch returns only the commit (`runner.py:1232`), so no Submission is recorded. `test_landing.py:693` pins `Submission=None` against the `bolt-landed` fixture, which names entry 412.
2. **bolt-teams, "A check fails".** `crew bolts` should say a failed check is the bolt's and that ops starts `crew fix z <name> "<Flume's words>"`. The views say only `landing refused, a check failed: <words>` (`runner.py:1282`). For a conflict, nothing says crew launches the take-main fix.
3. **bolt-plan, "The drop's host does not answer".** The scenario says no host is asked. A drop of a started bolt with units still calls `sweep_on` (`plan.py:4704-4707`), which runs `crew _sweep` over ssh on the work's host. `test_bolt_commands.py:498` asserts that sweep. `test_cross.py`'s drop case fails, as listed above.
4. **bolt-teams, "Two reads at once".** `landing_read` records the outcome with `record.emit`, judged against entries read before the write rather than at the tip it lands on. Two concurrent reads can each record a `bolt.submit` outcome, and the second close records a refused `bolt.land`. No test covers it.
5. **bolt-teams, "First read records".** Not every act that reads the bolt records its outcome. `crew bolt land` (`started_land`) writes `bolt.land` but no `bolt.submit` outcome. `crew bolts` writes nothing. Only the card's raise, the rail sweep and a kit read record it.
6. **bolt-teams, "A drop of" a bolt started before this release.** Nothing says `bolt/y` stays and is the user's to keep or delete. No test drops such a bolt.
7. **bolt-teams, "A fix while the landing is under test" and "Landing again".** The refusal names only the request, never the queue entry (`#412`) once Flume names one. A second land has no "again" state: the views say `landing #415 under test` and nothing about the refusal before it. The "again" cases (`test_landing_state.py`, `test_rail.py:174`, `test_board.py:1494`) drive sluice-era `queued` entries only.
8. **rail-cards, "A send's lands are posted by the first act that reads it".** The host's follower is one of the acts named. The rail's sweep records the user's answer (`answer_seen`, `plan.py:13893-13903`) but raises an answered landings card only in some cases: main moved, the card was lost, or a reading reopened. So where the follower reads the send first, no land is posted until `crew card read` or another raise. The case for "Read with no session of ops's running" calls `raise_landings` directly and never goes through the rail.
9. **rail-cards, "A bolt started before bolts were base places", beside a bolt that can land.** `land_read` and `landing_rows` give such a bolt a box (`plan.py:3335-3345`). Only the rail and head lines say it lands under the crew that started it. `lands_due` skips it, so no land is posted. No test checks the card's row.
10. **crew-rail and crew-board, "A landing refused in conflict".** Neither the rail line nor the head line says the bolt takes main first, in Flume's words, until a fix taking main in moves its head. Before crew records the refusal they say `landing refused in conflict with main at …`. After, they say `landing … rejected at <head>, open for work: …` or `lands once fix/… has merged`. No test covers it.
11. **crew-board, "A bolt started before base places", in ops's band.** The scenario says the words show in the lane and in ops's band. `board.ops_view` (`board.py:796-829`) leaves them out of the band. `test_board.py:2140` tests the lane only.
12. **crew-board, "A landing rejected" and "A landing stopped".** The failed-check head line lacks the head and "open for work" until a write records it (`runner.py:1285`, pinned by `test_board.py:2132`). The stopped line names no head (`landing stopped, nothing of the bolt's: <words>`).
13. **main-level and bolt-teams, the refusals' words.** `SUBMIT_REFUSED` says "a bolt lands …" where the scenario has "`y` lands …". `SEND_REFUSED` names neither the fix nor its kit's card.
14. **run-record, "An entry an older crew wrote".** `crew events` should print `Submission: 355`. `record.line` prints neither Outcome nor Submission, and only `--json` carries them. No test covers it.

## Scenarios no check proves (`docs.6`)

- The landing's `Age` and `Split` from the run record (`landing_spent`, `plan.py:3948`). This covers bolt-plan's three "time by holder" scenarios and crew-board's "A landing by pull request". `TestAgeAndSplit` was deleted with nothing in its place.
- crew-board's "A runner that can't be read": no case asserts `can't tell its landing`.
- crew-rail's new runner lines: asked with request 57 or 63, `#412` waiting, can't tell, and a bolt started before this release. `test_rail.py:161-175` still drives sluice-era `Submission` entries.
- bolt-teams's "Kind its host has not locked": nothing asserts that no read appends a request.
- bolt-plan's "Requeuing a unit that has a place": the case's bolt has no base-place launch, so the drop of `bolt/x` on a requeue is never tested.
- bolt-teams's "Three bolts on one send" and landing one bolt beside a refused one: the journey has two bolts, both refused.
- rail-cards's card read with a posted land, "asked of the runner to land, request N", from this send or an earlier one. A stopped bolt's read also prints its old request as asked, since `posted` keeps the newest land whatever its outcome.
- rail-cards's "Two bolts sent", "no agent is told": `test_landings.py:2077` doesn't assert that nothing was told.
- review-batches's "No land while a batch waits": its `lands_due` case passes `rows=[]`, so it shows nothing of a bolt waiting on a batch.
- run-record's "A land the runner refused" carries no `Submission`, and "A day's file an older crew began" with `Request`: neither has a case of its own.

## Words and code the change leaves behind

None of this is reachable as behaviour, but it contradicts the specs' words or the design's removals:

- Card text still says ops lands through sluice and asks again: "wldn-ops submits it again once that is cleared" (`cards.py:922`); "main-level ops lands them through sluice" (`cards.py:794`, `1013`); "sluice has proven it" (`cards.py:880`, `1010`; `plan.py:3028`). These are pinned by `test_cards.py:1391`, `1606`, `1623` and `test_landings.py:688`.
- `crew _land-card --pane` and `raise_landings`' close for an answer in the pane (`plan.py:3549`, `3721-3723`, `14576-14580`). Also `left_marks` ending a stop on a pane-word `bolt.submit` (`plan.py:2810`, `2827`; pinned by `test_pane_landing.py:108`), and the unused `LANDINGS` constant (`plan.py:12540-12544`).
- Docstrings that describe the removed path:
  - `plan.py:59-69` (`crew bolt submit` as a sluice landing)
  - `kit_read` (`plan.py:7377-7385`: sluice deleting the bolt's branch, `land_delete`)
  - `bolt_facts` (`plan.py:8376-8381`: `landing_split`, sluice's submissions)
  - `landing_pending` and `landing_phase` (`landing_ended`, `landing_not_landed`)
  - `unlanded_ask` (`plan.py:5184`)
  - `landing_lines` (`plan.py:11508`: the removed "Checks that never ran")
  - `board.py:800` ("the landing is ops's")
  - `plan.py:2133` (`LAND_COPIES`)
- The stub `sluice` still answers `submit`, `wait` and `branch create`/`delete`, and `tests/stubs/gh` and `tests/stubs/wt-submit` remain. Task note 5.2 removes them only once no test calls them, and `tests/run`, `tests/lib.sh` and the failing tests above still reach them.

## What holds

These hold and are proven by passing checks:

- The bolt kind (`plugin/flume/kinds/bolt@1/kind.toml`, `source.keep`).
- `requests.rec`'s descriptor and refusals for a `crew/bolt` launch and a `land`.
- The start's launch order and its restart after a refusal.
- `lands_due` and the posting of lands on a raise, once per send and head.
- `landing_of`'s table.
- The close at Flume's commit, with no branch deleted.
- The take-main fix launched once on a conflict, and the failed check held.
- `crew bolt submit` and `crew main fix --send` refusing before any read, with `--help` still answered.
- The fix of main's land.
- The tidy naming old worktrees.
- `test_no_tool_for_a_bolt.py`, and the journey's empty tool log with the checkouts unmoved.
- The ops band's asked and under-test lines in the mod.
- The briefs and docs.

The REMOVED requirements' scripts and functions are gone from `plugin/lib` and `plugin/bin`, apart from the leftovers listed above.
