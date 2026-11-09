# Verify: crew-lands-each-bolt-through-flumes-base-place

Read 2026-11-08 on `change/crew-lands-each-bolt-through-flumes-base-place` at `8f062e3c`. **Verdict: not ready to archive.** The whole checks fail in the contract tier. The change goes back to its code stage with what follows.

## The whole checks

`tests/suite` was run once from the worktree's root. It runs every project's `check-full` tasks, as sluice selects them. Result: **32 passed (18 replayed), 1 failed**, exit 1.

Passed: `logic`, `mod`, `nix:format`, `nix:lint`, `nix:test`, `nix:typecheck`, `t-briefs`, `t-cards`, `t-docs`, `t-flume-source`, `t-help`, `t-hold`, `t-journey-board`, `t-journey-cross`, `t-journey-land`, `t-journey-main`, `t-journey-main-fix`, `t-journey-ops`, `t-journey-plan`, `t-journey-review`, `t-journey-roles`, `t-journey-signals`, `t-journey-state`, `t-roles`, `t-runner`, `t-session-hook`, `t-slot`, `t-sluice`, `t-stage-facts`, `t-suite`, `t-teams`, `t-waits`.

Failed:

- **`contract`**: 3 failed, 94 passed.
  - `tests/contract/test_git.py::test_a_kits_policy_is_read_from_mains_commit` (line 199): `AttributeError: module 'kit' has no attribute 'policy_said'`.
  - `tests/contract/test_git.py::test_a_kits_policy_is_read_from_githubs_main_ahead_of_the_hosts_own` (line 218): `AttributeError: module 'kit' has no attribute 'policy_said'`.
  - `tests/contract/test_kit.py::test_the_remote_a_bolt_lives_on_is_read_from_the_policy_main_holds` (line 14): `AttributeError: module 'plan' has no attribute 'POLICY'`.

  Cause: `88388624` removed the start's policy script, `plan.POLICY`, and its parse, `kit.policy_said`, because bolt-teams "A started bolt's work is launched whole" says the start reads no kit policy. These three contract cases still pin what was removed. No task's check runs the contract tier: 3.3, 5.5 and 5.6 name logic files only. So the code stage never saw the failures.

  What is left for the code stage: each case goes with the script it pinned, or pins something crew still runs. `test_kit.py`'s case reads `kit.bolt_remote` through `plan.POLICY`. `bolt_remote` is still reached through `kit.bolt_home`.

## Tasks

All 37 tasks in `tasks.md` are ticked. `openspec validate crew-lands-each-bolt-through-flumes-base-place --strict` passes.

## The last verify's findings, read again

Each finding of the verify at `d4adecfc` was checked against the code and tests as they stand.

**Requirements not met.** All 14 are met now, and each has a case:

1. A landed `bolt.submit` carries `Submission` (`runner.landing_of`'s landed branch gives `entry`; `test_landing.py:706`).
2. A failed check's words name `crew fix <bolt> <name> "<words>"` (`runner.landing_said`; `test_board.py:2130`, `test_rail.py:245`).
3. A bolt's drop asks no host (`op_bolt_drop`'s `after`).
4. Two reads at once record once (`landing_record`, `closed_already`; `test_landing.py:784`).
5. The spec now names `crew bolts` a view that writes nothing (`state.4`), and `crew bolt land` records the outcome in its close's commit (`started_land`; `test_bolt_commands.py`).
6. A drop of a bolt started before base places says its branch stays, the user's (`legacy_drop_said`; `test_cross.py:226`).
7. "Landing again" is drawn, and work joining is refused naming both entries (`test_board.py:2165`, `test_cross.py:275`).
8. The follower raises a kit's card whose answer its sweep recorded (`landings_answered`; `test_rail.py:2184`).
9. A bolt started before base places has no box (`test_landings.py:1980`).
10. A conflict is said as taking main first (`landing_said`).
11. Those words show in ops's band (`test_board.py:2201`).
12. A failed check's head line names its head and "open for work", and a stop names its head (`landing_said`).
13. The refusals' words name the bolts given, and the fix with its card (`submit_refused`, `send_refused`).
14. `crew events` prints `Outcome`, `Request` and `Submission` (`test_record.py:335-339`).

**Scenarios no check proved.** Each now has a case, as task 8.4 lists them.

**Words and code left behind.** The card text naming ops's sluice landing is gone. So are the pane outcomes, the `LANDINGS` record and the docstrings. The stub `gh` refuses every call, and the stub `sluice` answers only what crew and the tests still run (tasks 5.9, 7.3 and 9.3).

## Words in the delta

bolt-plan's delta cites two bolt-teams requirements by names the bolt-teams delta does not have:

- In "A bolt's work starts by crew bolt start", it cites "A bolt is a base place of crew's kind, launched before its pieces". bolt-teams has "A bolt is a base place of crew's kind" and "A start launches the bolt's base place before its pieces".
- In "A bolt is created and dropped through crew" and in its REMOVED migration, it cites "A bolt's drop drops its base place last, and asks it again after a refusal". bolt-teams has "A bolt's drop drops its base place last" and "A base place's drop the runner refused is asked again once nothing on its branch is live".

`openspec validate` passes, since it does not check names inside quotes. These two citations should name the requirements as they stand.

## What holds

Apart from the contract tier and the two citations above, the work holds against the delta. The logic tier, the mod's cases, the flake's checks and every end-to-end test pass. The last verify's findings are met, each with its case.
