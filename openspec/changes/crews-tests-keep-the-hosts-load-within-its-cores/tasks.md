# Tasks

Each check is a moon task of the `tests` project, run through `tests/suite`. Build the groups in order. Submit nothing, and never run `wt submit --help`.

## 1. The host's slots

- [x] 1.1 `tests/slot` counts a host's slots as many tests as its cores less two hold at `TEST_CORES`, a core and a half each, at least one, `CREW_TEST_SLOTS` still naming a count (design Decision 1; Task notes 1.1). Verify `tests/suite t-slot` ends with "0 failed".

## 2. A test's waits

- [x] 2.1 `tests/lib.sh`'s `nap` pauses on a fifo with no process, and `until_ok` looks at once, then at pauses doubling from a tenth of a second up to a second (design Decision 2; Task notes 2.1). Verify `tests/suite t-waits` ends with "0 failed".
- [x] 2.2 The stub sluice pauses on the test's fifo, and its wait on a held submission exits 5 after a second or once the hold is lifted (design Decision 3; Task notes 2.2). Verify `tests/suite t-waits t-journey-land t-sluice` ends with "0 failed".
- [x] 2.3 `t-journey-main` waits for the other roles' greetings with `until_ok` (design Decision 4; Task notes 2.3). Verify `tests/suite t-journey-main` ends with "0 failed".

## 3. What is said

- [x] 3.1 README and CLAUDE.md say how many slots a host has and that a test's waits start little, and `tests/moon.yml` holds `t-waits`'s task (Task notes 3.1). Verify `tests/suite t-docs` ends with "0 failed".

## 4. The tests the change affects

- [x] 4.1 Verify `tests/suite --affected` ends with "0 failed".
