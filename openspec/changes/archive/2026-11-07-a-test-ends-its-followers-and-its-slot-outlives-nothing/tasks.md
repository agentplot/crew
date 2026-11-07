# Tasks

Each check is a moon task of the `tests` project, run through `tests/suite`. Build the groups in order. Submit nothing, and never run `wt submit --help`.

## 1. A test's slot and what it leaves running

- [x] 1.1 `tests/slot` holds the slot in its own process alone, runs the test under a keeper in a process group of its own, frees the slot once the test has ended, ends what is left of the group (SIGTERM, then SIGKILL after five seconds), passes a signal to the group, exits as the test did, and takes the test with it when killed (design Decisions 1 and 2; Task notes 1.1). Verify `tests/suite t-slot` ends with "0 failed".
- [x] 1.2 A card's plannotator session, started in a session of its own, ends once its test's shell has ended, `tests/lib.sh` exporting `CREW_TEST_PID` (design Decision 3; Task notes 1.2). Verify `tests/suite t-slot` ends with "0 failed".

## 2. A quiet tick counted from its own first read

- [x] 2.1 `t-journey-board` waits for each of the follower's ticks until every frame is new since the tick's fetch of wldn's state branch, and counts the tick's reads from that fetch on (design Decision 4; Task notes 1.3). Verify `tests/suite t-journey-board` ends with "0 failed".

## 3. What a slot holds, said

- [x] 3.1 `tests/run` and README say a test holds its slot only while it runs and that what it leaves running is ended with it (Task notes 1.4). Verify `tests/suite t-docs` ends with "0 failed".
- [x] 3.2 `t-briefs` judges a main-level brief's words with crew's checkout path left out, so a place whose folder names a gone word fails nothing (design Decision 5; Task notes 1.5). Verify `tests/suite t-briefs` ends with "0 failed".

## 4. The tests the change affects

- [x] 4.1 Verify `tests/suite --affected` ends with "0 failed".
