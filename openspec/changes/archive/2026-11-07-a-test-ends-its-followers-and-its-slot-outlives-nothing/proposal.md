# A test ends its followers, and its slot outlives nothing

## Why

On deneb, on 2026-10-29, `crew ops quiet` said "4 of crew's tests are running on deneb" with no test running, and deneb's deploy waited on it. Four `board.py _follow` processes left by crew's tests were still running, orphaned to launchd. One was eight hours old, from a removed place. Each held a test slot's lock, so the host read as busy with tests forever. swancloud-ops killed them by hand to let the deploy through (signal `afterthought/crew-state:swancloud/main signals/2026-10-29-swancloud-ops-1626e009/01-crew-tests-leak-board-followers-holding-test-slots`).

The cause is in `tests/slot`. It took the slot's lock, made the lock's file inheritable and exec'd into the test, so every process the test started held the slot's file too. A test that starts crew's board follower in the background, as `t-journey-board` does, ends it only on its success path. A failure in between left the follower running, its overview watches with it, all holding the slot.

The same day `t-journey-board` failed under host load with "expected 1 0 0 0 1, got 1 1 0 0 1": the follower's tick with nothing moved counted one git read (signal `afterthought/crew-state:swancloud/main signals/2026-10-29-crw-4-conductor-f4ad7861/01-t-journey-board-follower-race`). The read was the first refresh's own, landing after the test had emptied its reads log. f481fbff made the test wait for every frame of the first refresh, which removes that read. The count still takes whatever reaches the log between the clear and the tick as the tick's.

## What Changes

- **A slot is held by `tests/slot` alone.** It runs the test as a child, the lock's file open in no process the test starts, so the slot is free once the test has ended, whatever it left running.
- **What a test leaves running ends with it.** The test runs in a process group of its own. When it ends, passed or failed, what is left of the group is sent SIGTERM, then SIGKILL after five seconds. A signal sent to `tests/slot` is passed to the group. A keeper leads the group and kills it should `tests/slot` itself be killed.
- **A card's session ends with its test's shell.** crew starts a card's plannotator in a session of its own, out of the group's reach. The stub plannotator ends once the test's shell, `CREW_TEST_PID`, has ended.
- **`t-journey-board` counts a tick's reads from the tick's own fetch.** The tick's first read is the clock's fetch of wldn's state branch, and the git shim marks it there. The tick is waited for until every frame is new since that fetch, so nothing an earlier round read is counted as the tick's.
- **`t-briefs` judges a brief's words, not crew's path.** A printed brief names crew's checkout path. In a place whose folder holds `slot`, as this one does, the check that no brief names a slot failed on the path alone.
- `tests/run`'s header and README say a test holds its slot only while it runs and what it leaves is ended with it.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `test-suite`: a test's slot is held by its runner alone and is free once the test has ended. What a test leaves running is ended with it, passed, failed, or with its runner stopped or killed. A card's session ends once the test's shell has. A follower's tick is counted from its own first read.

## Impact

- `tests/slot`: the runner, its keeper and the end of the test's group.
- `tests/lib.sh`: exports `CREW_TEST_PID`.
- `tests/stubs/plannotator`: ends once `CREW_TEST_PID` has ended.
- `tests/t-slot.sh`: the cases; `tests/moon.yml`, t-slot's task naming the stub.
- `tests/t-journey-board.sh`: the tick's count.
- `tests/t-briefs.sh`: the gone words looked for with crew's path left out.
- `tests/run`, `README.md`: what a slot holds.
- No change to `plugin/`: `crew ops quiet` and the hold read a held slot as a running test, which it now always is.
