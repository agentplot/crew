# Design

## Context

This section records what was read on 2026-11-07 on deneb, so the decisions below rest on it.

**How a slot was held.** `tests/slot` took the slot's lock with flock and called `os.set_inheritable` on its file. Then it `execvp`'d into the test, so the test's shell held the file, and so did every process the shell started. A flock is let go only when the last descriptor of its open file closes. So the slot stayed held while anything the test started still ran.

**What a test leaves running.**
- `t-journey-board` starts `crew _follow` in the background with a clock of an hour, and kills it only on its success path. The follower opens one `sluice overview --json --watch` per kit: the stub's watch loops until a write to its reader fails, and it writes only when its document changes.
- On a deliberate failure placed after the follower's first tick, the follower and both watches were still running after `tests/run` had reported the failure. Their process group was the shell's that ran `tests/run`.
- `t-journey-main`, `t-journey-land`, `t-journey-state` and `t-journey-ops` also start processes in the background and end them on their own paths. Two of them use an EXIT trap.

**What leaves a test's process group.** crew starts three processes in a session of their own, so that they outlive the command that started them:
- a card's plannotator session (`plan.py`, the card session's start);
- `crew _preview` (`preview_hand`);
- `crew _renew` (`hold.hand`).

The stub plannotator waits up to five minutes for a decision, and ends early only when its registry folder goes, which `tests/run` removes only for a passed test. `_preview` and `_renew` end with their work.

**Reading another process's environment.** `ps -wwE` on deneb (Darwin 27) printed no environment for a child of the reading shell. So a test's processes cannot be found by a marker in their environment.

**The follower's tick.**
- The follower is one process doing one thing at a time. A tick is a fetch of each partition's state branch and blueprints main (wldn's state branch first), the ask of the cards, then a refresh that ends by writing each partition's frames.
- In a traced run, the first refresh's last git read was `git describe` for swancloud's agents' view (`board.here_read`), written before swancloud's board and agents' frames.
- The three runs the signal names (sluice candidates 8b7a788, a4d314f4, 276430e0) all held the version of the test before f481fbff, which waited on wldn's rail frame alone.

**The family.** sluice ends what a worktree's runs left running when it releases the worktree (`plan.9`). That works at a worktree's scale, when the worktree goes. A test's slot is crew's own: record 0021 and `tests.9` built it, and no tool of the family runs or bounds crew's tests. So the two owners are not one mechanism to reconcile. Each ends what was started within its own scope.

**Area pages this change touches:** `tests.md` (`tests.1`, `tests.4`, `tests.8`, `tests.9`, `tests.10`, `tests.11`) and `docs.md` (the spec, `docs.4`, `docs.6`). From `core.md`: `code.7`, since no decision of crew's changes. No rule changes, so no page is edited (`docs.7`).

## Goals / Non-Goals

**Goals:**

- A slot is held while its test runs and no longer, whatever the test leaves running (`tests.9`).
- What a test starts ends with it, passed or failed, or with its runner stopped or killed.
- `t-journey-board`'s count of a quiet tick fails only when the tick itself reads.

**Non-Goals:**

- `crew _preview` and `crew _renew` in tests. Each ends with its work, and neither holds a slot once the slot is no longer inherited.
- A change to `crew ops quiet` or the hold's count of tests. Each reads a held slot as a running test, which this change makes true.
- How many slots a host has. `tests.9`'s bound stands as record 0021 left it.

## Decisions

### Decision 1: The slot's file is open in `tests/slot` alone

`tests/slot` no longer execs. It holds the lock in its own process, through a file `os.open` makes non-inheritable, and runs the test as a child: `subprocess` closes every other descriptor in the child. It lets the slot go as soon as the test has ended, before it ends what the test left. If `tests/slot` is killed, the system lets the slot go, since no other process holds the file.

*Not taken:* keeping the exec and having the test's shell close the file for its children. bash cannot mark a descriptor close-on-exec, so every test would have to do it by hand, and none that forgot would be caught.

### Decision 2: The test runs in a process group of its own, which ends with it

- **The group.** The test runs under a keeper, `tests/slot --keeper`, started in a session of its own. The keeper is the group's leader and the test's parent. When the test ends, the keeper exits as the test did. Then `tests/slot` sends SIGTERM to whatever is left of the group, and SIGKILL to anything still there five seconds later (`GRACE`).
- **Exit status.** `tests/slot` exits as the test did, 128 and the signal's number when a signal ended it.
- **Signals.** SIGTERM, SIGINT and SIGHUP sent to `tests/slot` are passed to the group.
- **When `tests/slot` is killed.** The keeper holds the read end of a pipe whose write end only `tests/slot` holds. Should `tests/slot` end without ending the group, as on a SIGKILL to the runner's process group, the pipe reaches its end and the keeper kills the whole group. So a test never outlives its runner, as it could not when `tests/slot` exec'd into it.
- **macOS.** macOS answers EPERM for a group that holds only processes that have ended and wait to be reaped. That is taken as nothing left.
- **Nested runs.** A test started inside another's slot (`CREW_TEST_SLOT`) takes no lock, and its own group is ended all the same.

*Not taken:*
- An EXIT trap in `lib.sh`. Two tests set their own EXIT trap, which would replace it. A trap does not run on SIGKILL. And a trap reaches only the shell's own jobs, not a follower's watches.
- Finding a test's processes by a marker in their environment. That cannot be read on macOS (Context).
- A subreaper. Linux has one and macOS has none.
- The test in a group of its own with no keeper. A SIGKILL to the runner's group would then leave the test running alone.
- The slot's process leading the group itself. It would have to pass outside signals into a group that holds itself, and enumerate the group to end everyone but itself.

### Decision 3: A card's session ends once its test's shell has

`lib.sh` exports `CREW_TEST_PID`, the test's own shell. The stub plannotator ends, writing no result, once that process is gone. Its registry and five-minute ends stay.

This is the one test process left out of the group that waits on something only the test would give it. crew starts it in a session of its own by design, so that it outlives the command that asked for it, and the tests keep that (`tests.4`: the stub is started as crew starts plannotator). Ending with the test's shell is the stub's own housekeeping, like its registry end, and nothing crew reads.

*Not taken:* crew starting card sessions in the caller's group under test. That would test a crew that does not run on any host.

### Decision 4: A quiet tick's reads are counted from its own first read

- **Where a tick begins.** The tick's first read is the clock's fetch of wldn's state branch. At that fetch the follower's git shim writes two marks: each frame's file as the tick found it, in `tick-began`, and a `mac-studio tick` line in the calls log.
- **Waiting for the tick.** `tick` clears the logs, signals the follower, and waits until every frame is new since `tick-began` (`ticked`).
- **Counting.** `tick_reads` counts the reads log from the tick's fetch on, and `only_stamps` counts both logs from the tick's marks on.
- **Why nothing earlier is counted.** The follower does one thing at a time. A tick cannot begin while an earlier round, or a refresh that followed it, is still reading. So nothing such a round read under load reaches the count. A git read inside the tick still does, and fails the check.
- The first round and the tick after sluice's write are waited for and counted the same way.

*Not taken:*
- Waiting for the follower to be quiet for a while. That is the clock deciding an outcome (`tests.8`).
- Timestamps on each read compared with the frames' times. crew's own count of a gather has no timestamp, and a file's time on Linux is taken from a coarse clock.

## Risks / Trade-offs

- **A second process per test.** Each test now has a keeper, one more Python start, about a twentieth of a second.
- **A process that left the group lives on.** It holds no slot. Of crew's, only a card's session waits on the test, and it ends by Decision 3.
- **A SIGKILL to `tests/slot` in the moment after its test ended.** The keeper has exited by then, so whatever the test left lives on, holding no slot.

## After deploy

None. This changes crew's test harness alone, which sluice runs on every submission. Nothing is deployed to a host.

## Task notes

**1.1** `tests/slot`: `take` returns a non-inheritable file and nothing marks it inheritable. `main` runs `[sys.executable, tests/slot, --keeper, <r>, *argv]` with `pass_fds=(r,)` and `start_new_session=True`. It passes SIGTERM, SIGINT and SIGHUP to the group (`sent`), waits, closes the slot's file, ends the group (`end`: SIGTERM, then SIGKILL after `GRACE`, EPERM and ESRCH both taken as nothing left), and exits with `status`. `keeper`: `Popen(argv)`, a daemon thread that reads the pipe to its end and then kills its own group, then exits as the command did. `tests/t-slot.sh`:
- a leftover reports whether any open descriptor of its own is slot-0's file, and reports none;
- the slot is free once the test exits 3, the exit is 3, and the leftover ends;
- a leftover that ignores SIGTERM ends;
- SIGTERM to the slot exits 143 and ends the test and its leftover;
- after a SIGKILL to the slot, a new test takes the slot, and the killed test and its leftover end.

**1.2** `tests/lib.sh` exports `CREW_TEST_PID=$$` beside `CREW_TEST_ROOT`. In `tests/stubs/plannotator`'s wait loop, `alive(CREW_TEST_PID)` false ends it. `tests/t-slot.sh`: a test started under the slot, exporting its own shell as `CREW_TEST_PID`, starts `plannotator annotate` in a session of its own and waits until `plannotator sessions` lists it. Once the test ends, the session ends with no result file. t-slot's `# Reads:` names `tests/stubs/plannotator`, and `tests/moon.yml` is rewritten by `tests/moon-tasks`.

**1.3** `tests/t-journey-board.sh`:
- `$T/written`, a script, prints the six frames' inodes. The git shim's first line runs it into `tick-began` at a fetch of `refs/crew/wldn/main` and appends `mac-studio tick` to the calls log.
- `ticked` is `rewritten` against `tick-began`. `tick <words>` clears both logs, removes `tick-began`, sends SIGUSR1 and waits for `ticked`.
- `tick_reads` counts from the first `mac-studio fetch` line on. `only_stamps` counts the box's reads from the fetch on and its ssh calls from the `mac-studio tick` line on.
- The running follower's first round, its quiet tick and the tick after sluice's write use them.

**1.4** `tests/run`'s header and its slot comment, and README's sentence on the test slots, say a test holds its slot only while it runs and that what it leaves running is ended with it.
