# Tasks

Each check is a moon task of the `tests` project, run through `tests/suite`: `logic` is `tests:logic`, `contract` is `tests:contract`. Build the groups in order. Submit nothing: Flume submits the place once its last stage delivers.

## 1. A refused write waits longer before each replay

- [x] 1.1 `plan.replay_wait` gives each replay's wait from `REPLAY_WAITS`, growing from half a second to eight, each drawn over its upper half, and no more than 23.5 seconds in all (design Decisions 2 and 3; Task notes 1.1). Passes `tests/py/test_record.py` (`tests/suite logic`).
- [x] 1.2 `plan.land` waits before each replay's fresh fetch but the last, a branch that keeps moving is refused naming the attempts and the wait, and `record.reach` keeps that entry for the host's next push, which carries it once the branch takes it (design Decisions 1 and 4; Task notes 1.2). Passes `tests/py/test_record.py` (`tests/suite logic`).

## 2. Against git

- [x] 2.1 A branch another clone moves before each of a write's first three pushes is outwaited, each wait longer than the last and made before a fresh fetch, and the write lands on top of the other clone's last commit (design Decision 1; Task notes 2.1). Passes `tests/contract/test_record.py` (`tests/suite contract`).

## 3. README and the tests the change affects

- [x] 3.1 README's State section says a refused push is applied again after a growing wait, up to six times (Task notes 3.1). Verify `tests/suite t-docs` ends with "0 failed".
- [x] 3.2 Verify `tests/suite --affected` ends with "0 failed".
