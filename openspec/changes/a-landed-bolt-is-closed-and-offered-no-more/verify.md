# Verify: a-landed-bolt-is-closed-and-offered-no-more

Verified on `change/a-landed-bolt-is-closed-and-offered-no-more` at `5c5a229e`, 2026-11-11.

**Verdict: does not hold. The whole checks fail, so the change is not archived and goes back to its code stage.**

## The whole checks

`tests/suite --affected` (CLAUDE.md, *Tests*), run once against the merge-base with `main`: **30 passed (1 replayed), 2 failed**, exit 1.

### 1. `logic`: `tests/py/test_rail.py::TestCrossedLandings::test_a_fix_in_flight_on_it_holds_its_landing`

```
>       assert self.rows({1: "landed", 2: "landed", 3: "landed", 4: "landed"}, extra=[fix])[0]["bolts"][0]["can"] is True
E       IndexError: list index out of range
tests/py/test_rail.py:2411
1 failed, 3594 passed in 20.54s
```

Cause: in this case's fixture, request 4 is `bolt/x`'s base place (`facts.launched` gives `unit/a` 1, `unit/b` 2, `chore/c` 3, `bolt/x` 4). The extra fix launch the case adds is also numbered 4. So `{4: "landed"}` makes the runner report the base place landed. Under this change's requirement "A bolt read landed on main is offered no more", a bolt whose landing reads landed has no line under *land* (`rail_rows`' new `continue`). So `x` has no row, and the case's second assertion still expects the old behaviour.

The code is as the spec asks. The case is what has to change: give the fix a request number of its own (5, with `{…, 5: "landed"}`), so the case proves what it names, a fix in flight holding the landing, and no longer pins a landed bolt to the rail.

### 2. `t-journey-board`

```
FAIL: expected '1 4', got '1 6'
```

This is at `tests/t-journey-board.sh:242`, the follower's quiet tick counted by its fetches. The tick now fetches six other repositories, not four. The two extra are the mains of the started bolts' kits, which Decision 7 adds to the clock's fetch (`board.fetches(fleet, labels, self.kits)`, `kit_mains`). The behaviour is the design's. The test, its count and the comment above it (lines 238–241, "one fetch of each repository: …") were not updated to say so. Task 5.1 named only `tests/py/test_board.py`, so the end-to-end test that pins the tick's fetches was left behind.

The kept scratch is `/private/tmp/crew-test.soRF6K`.

## The change against its specs and tasks

- **Tasks:** all 14 are ticked (`tasks.md` 1.1–6.1). Each task's named test class exists: `TestLandingHead`, `TestOnMain`, `TestMainTip`, `TestMainHolds`, `TestABoltWhoseWorkIsOnMain`, `TestALandingReadOnMainIsRecorded`, `TestALandingReadOnMainCloses`, `TestCrewBoltLandOfAStartedBolt`, `TestTheSweepClosesABoltOnMain`, `TestABoltOnMainIsNoRow`, `TestABoltOnMainHasNoLandLine` and `TestTheFollowerFetchesEachKitsMain`. The logic and contract tiers ran them all and passed them. Only the one case above failed. `t-docs` passed.
- **`openspec validate a-landed-bolt-is-closed-and-offered-no-more --strict`:** valid.
- **bolt-teams, added requirements:**
  - "A bolt whose work is on its kit's main reads landed" is met by `main_asks`, `on_main`, `landing_head`, `main_tip`, `main_holds`, `landed_by` and `Stages.main_landing`. They read GitHub's main in crew's cache, read no trailer and reach no host. Main that can't be read gives the report's outcome.
  - "… is recorded and closed by the first act that reads it" is met by `landing_entry`'s `by: "main"` branch, which records once since the newest start, `landing_read` with `landing_on_main`, `started_land`, and `landings_judged` and `reap_judged`, which list a bolt under the main-level host where its host can't be told.
  - "… is offered no more" is met by `land_facts` returning no row for a landed bolt and `rail_rows` skipping it under *land*.
- **bolt-teams, modified requirements:**
  - "A landing's outcome is read from the runner's report": the report first, main beside it.
  - "A landing's entry names its kit, its head and its time": `Head` is `landed_by`'s commit, and the contract case pins the merge rather than main's tip.
  - "crew bolt land closes a started bolt only once its base place reads landed": refused naming both readings, or closed at main's commit.
  - "A bolt with no launch of its own lands under the crew that started it": legacy until main holds its work.
  - All four are met in code.
- **rail-cards, modified requirements:** "A bolt started before bolts were base places has no box" and "A landing the runner or Flume stopped keeps its box" are met by `land_facts` and `rail_rows`, holding while main lacks the bolt's work.
- **Docs (`docs.2`):** README, `plugin/skills/crew/SKILL.md` and `plugin/bin/crew`'s usage header each say it, and `t-docs` passed.
- **A note, not a failure:** Task note 5.1 has `look` add the kit mains under `"kits"`. The code names the key `"mains"`, because a refresh's stamps already hold its kits' answers under `kits` (`board.look`'s docstring). The design's note can follow the code when the code stage next touches it.

## What goes back to the code stage

1. Renumber the fix launch in `TestCrossedLandings.test_a_fix_in_flight_on_it_holds_its_landing` so it no longer shares request 4 with `bolt/x`'s base place.
2. Update `tests/t-journey-board.sh`'s quiet-tick fetch count, now `1 6`, and the comment above it, naming the started bolts' kits' mains the clock fetches (Decision 7).

Then `tests/suite --affected` ends with "0 failed".
