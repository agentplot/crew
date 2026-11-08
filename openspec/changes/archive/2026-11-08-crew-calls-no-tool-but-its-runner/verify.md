# Verify: crew-calls-no-tool-but-its-runner

Verified on 2026-11-08 at `0aede1d7`, on `change/crew-calls-no-tool-but-its-runner`, cut from `bolt/crew-talks-only-to-its-runner` at `2ae95617`.

**Verdict: ready to archive.** The whole checks pass, every task is ticked, and the work meets every requirement and scenario of the change's specs as far as reading the code and its cases shows.

## The whole checks

`tests/suite` ran once: every project's `check-full` tasks, as `.config/sluice.toml` requires them of `bolt/*` and `main`.

**Outcome:** `33 passed (33 replayed), 0 failed`, exit 0.

- `logic`, `contract` and `mod`;
- `nix:format`, `nix:lint`, `nix:typecheck` and `nix:test`;
- every end-to-end test, 26 of them, among them `t-journey-board`, `t-sluice`, `t-journey-land`, `t-docs` and `t-briefs`.

Every task was replayed: its inputs at `0aede1d7` are identical to a run that passed on this host, and moon replays no run that failed.

The first verify, at `82d7bfb1` (its report in `49c214ef`), found the logic tier failing in two cases: `tests/py/test_fix.py:114` (Failure 1), calling `landing_unready` with its old signature, and `tests/py/test_chores.py:170` (Failure 2), a bolt whose pieces all landed at its head expected `active`. `0aede1d7` settles both as task 1.4 says: `test_fix` hands `landing_unready` a `(state, words)` verification, and `test_chores`'s bolt reads `waits`, its verification green, its docstring saying why.

## Tasks

All 11 tasks in `tasks.md` are ticked `[x]`, and none is open. Task 1.4's check, `tests/suite logic`, is the `logic` task above.

## Specs against the work

`openspec validate crew-calls-no-tool-but-its-runner --strict` reports the change valid.

- **merge-gate.** "A bolt's verification is its work's landing at its head, as the runner reports it" is met:
  - `runner.verification` (`plugin/lib/runner.py` 670) gives green for a head that is a piece's merged or landed commit, naming the head and the work, none for any other head, and unknown with no head;
  - a landing read from the bolt's own landings commits, record 0062's stopgap, comes through `runner.built_on_bolt` (654) and is named "as its landing on the bolt names it";
  - `tests/py/test_runner.py` `TestVerification` holds the cases of task note 1.1;
  - `kit.verification`, `kit.covering`, `kit.VERDICT`, `gather.landing_read`, `LANDING_TRAILERS` and `BESIDE_FIELDS` are gone, and no file under `plugin/` reads `Sluice-Result`;
  - `tests/contract/test_gather.py` `test_a_gather_of_a_kit_with_a_held_bolt_runs_no_sluice` proves "Nothing of sluice's is read".

  The removed requirements, "sluice's verdict on its last landing" and "A landing beside reads as the verdict that covers it", have no reader left.
- **bolt-plan.** "A bolt on GitHub is read where it lives" reads the verification at the head `gather.bolt_read` gives, GitHub's copy where the policy names a remote.
- **bolt-teams.** "A bolt's proof is its verification" holds through `landing_unready` and `bolt_state`, which take `Stages.verification`. "A submission's number is on its bolt's row from the submit" holds: a piece's `submitted #<n>` comes from `runner.piece_said`, the bolt's landing from the run record (`plan.landing_phase`), and `merge_said`, `landing_said(b)` and `queue_said` are gone from the views. `t-sluice` and `t-journey-land` assert the verification's words as the runner reports it.
- **crew-board.** "The follower runs no sluice" and "A gather runs no sluice" are met:
  - `board.py` starts no `sluice` and keeps no watch or submission of its own;
  - `gather.py` runs no sluice, and keeps `submissions_of`, `status_read` and `sluice_said` for crew's own landing alone (`plan.queue_read`, `landing_standing`, `submission_rows`, which say no view calls them);
  - `t-journey-board` asserts no `sluice` on either host across the follower's ticks, and `submitted #41` on `a`'s row after the runner's report.

  "Each holder is read from what crew already keeps" places no minute by a submission (`test_board.py`, "A submission the runner reports places no minute").
- **crew-rail and rail-cards.** The landings row and card offer a bolt only once its verification is green, read through `Stages.verification`, and say what it is otherwise.
- **The words.** `plugin/bin/crew`'s usage, README, `plugin/skills/crew/SKILL.md`, `plugin/roles/main-ops.md`, CLAUDE.md's *Proving and landing a bolt*, `board.py`'s follower usage and `status.js` say where the queue and the verification come from, and none says a view reads sluice's queue or verdict. README's remaining mentions of sluice's queue are crew's own landing, `crew bolt submit`, which Decision 1 leaves.

## Outcome

The change is archived on `change/crew-calls-no-tool-but-its-runner`, with this report.
