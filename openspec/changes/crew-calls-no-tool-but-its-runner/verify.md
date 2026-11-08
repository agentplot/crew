# Verify: crew-calls-no-tool-but-its-runner

Verified on 2026-11-08 at `82d7bfb1`, on `change/crew-calls-no-tool-but-its-runner`, cut from `bolt/crew-talks-only-to-its-runner` at `2ae95617`.

**Verdict: not ready to archive.** The whole checks fail in the logic tier. The change goes back to its code stage.

## The whole checks

`tests/suite` ran once: every project's `check-full` tasks, as `.config/sluice.toml` requires them of `bolt/*` and `main`.

**Outcome:** `32 passed (7 replayed), 1 failed`, exit 1.

- **Passed:**
  - every end-to-end test, among them `t-journey-board`, `t-sluice`, `t-journey-land`, `t-docs` and `t-briefs`;
  - `contract`;
  - `mod`;
  - `nix:format`, `nix:lint`, `nix:typecheck` and `nix:test`.
- **Failed:** `logic`, with `2 failed, 3436 passed`. Neither failing file is in the verify list of task 1.2, so the narrower checks the tasks name passed while the whole logic tier fails.

### Failure 1: `tests/py/test_fix.py:114`

`TestAFixOfAStartedBolt.test_a_fix_in_flight_holds_the_bolts_landing_until_it_has_merged_or_been_dropped`

```
>       assert plan.landing_unready([("a", "unit", "merged")], "h" * 40, "passed", ["fix/x/rail-word"]) == "fix/x/rail-word is in flight on it"
E       TypeError: landing_unready() takes 3 positional arguments but 4 were given
```

The case still calls `landing_unready` with the old signature `(work, head, verdict, fixes)`. Task 1.2 changed the signature to `(work, verified, fixes)`, where `verified` is the `(state, words)` pair. The case has to pass a verification pair.

### Failure 2: `tests/py/test_chores.py:170`

`TestStage.test_a_bolt_lands_once_every_unit_and_chore_has`

```
>       assert st.bolt_state(p.bolt("x")) == "active"
E       AssertionError: assert 'waits' == 'active'
```

The bolt is `x`, with unit `a` and chore `bump`, both read `landed` from the runner by `ran({1: "landed", 2: "landed"})`. `crew_read(main=["a"], bolts={"x": {}})` now gives `x` the default head `LANDED`, which is the commit those runner fixtures landed at. So `runner.verification` reads the bolt green, and `Stages.bolt_state` (`plan.py` 1608) returns `waits` where the case expects `active`.

The code stage decides which way this goes:

- **Keep `active`.** Set a head on `x` that no piece landed at, as task note 1.2 says for a bolt that is not green.
- **Expect `waits`.** A head that is a piece's landing now reads green, as merge-gate's new requirement says.

Whichever it is, the case's docstring has to say why.

## Tasks

All 12 tasks in `tasks.md` are ticked `[x]`. Each task's own verify check names a subset of the logic tier. `test_chores.py` and `test_fix.py` are in none of them, which is how the two failures above got through.

## Specs against the work

`openspec validate crew-calls-no-tool-but-its-runner --strict` reports the change valid.

Read against the code at `82d7bfb1`:

- **merge-gate.** "A bolt's verification is its work's landing at its head, as the runner reports it" is met:
  - `runner.verification` (`plugin/lib/runner.py` 670) gives green, none and unknown, with the words the design names;
  - `tests/py/test_runner.py` `TestVerification` holds the eight cases of task note 1.1;
  - `kit.verification`, `kit.covering` and `VERDICT` are gone;
  - the gather reads no `Sluice-Result`;
  - `tests/contract/test_gather.py` `test_a_gather_of_a_kit_with_a_held_bolt_runs_no_sluice` proves "Nothing of sluice's is read".
- **crew-board.** "The follower runs no sluice" and "A gather runs no sluice" are met:
  - `board.py` holds no `Watches`, queue stamps or kept submissions;
  - `gather.py` runs no sluice, and keeps `submissions_of`, `status_read` and `sluice_said` for crew's own landing alone;
  - `t-journey-board` asserts no `sluice` in its log and `submitted #41` after the runner's report.

  The time requirement is met: `held_time` hands `bolt_facts` no submissions, and `test_board.py` has "A submission the runner reports places no minute".
- **bolt-teams, bolt-plan, crew-rail and rail-cards.** Their verification and readiness readers all go through `Stages.verification`:
  - `bolt_state`;
  - `landing_unready`;
  - `land_facts`;
  - `bolts_data`;
  - the landings row.

  `phase_said` names the number always. `bolts_data` and `board_data` give no `submission`, `landing` or `submissions_error`. `t-sluice` and `t-journey-land` assert the verification's words, as the runner reports it.
- **The words.** The following say where the queue and the verification come from, and none says a view reads sluice's queue or verdict:
  - `plugin/bin/crew`'s usage;
  - README line 63;
  - `plugin/skills/crew/SKILL.md`;
  - `plugin/roles/main-ops.md` line 13;
  - CLAUDE.md's *Proving and landing a bolt*;
  - `status.js`.

  README's remaining mentions of sluice's queue are crew's own landing (`crew bolt submit`), which Decision 1 leaves.

The work meets its specs as far as reading shows. What holds the change back is the logic tier's two failing cases.

## What the code stage does

1. Fix `tests/py/test_fix.py:114` for `landing_unready(work, verified, fixes)`.
2. Settle `tests/py/test_chores.py:170` as Failure 2 says.
3. Run `tests/suite logic` until it says "0 failed".
