# Design

## Context

This section records what was read on deneb (18 cores, Darwin 27) on 2026-11-07, so the decisions below rest on it. The host carried its own work throughout, about five cores busy with no test of crew's running.

**Each test alone.** Every end-to-end test was run alone through `tests/run`, its processes' CPU taken from their resource use and set beside its wall time:
- the 25 tests took 612 s of wall time and 584 s of CPU;
- each kept 0.8 to 1.0 cores busy, except the few that mostly wait (`t-slot`, `t-session-hook`), and about half of every test's CPU was the kernel's;
- the longest were `t-journey-land` (194 s, 180 s of CPU, 101 s of it the kernel's), `t-cards` (65 s), `t-journey-review` (58 s), `t-journey-plan` (56 s) and `t-journey-board` (52 s).

**What a test starts.** `t-journey-land`, run with a shim on each command that logged its start, started 23,684 processes:
- 10,013 `git`, 1,054 `recfix` and 578 `python3`;
- 131 of the `python3` were `plan.py`, crew's commands, about 77 `git` each;
- 431 runs of the stub sluice, 229 of them `sluice wait`.

**Side by side.** `t-journey-cross` (11.5 s alone) was run in groups side by side, in a slot folder of its own, while `iostat` read the host's busy cores each second:

| side by side | CPU per run | wall per run | host cores the group added |
|---|---|---|---|
| 1 | 10.8 s (5.2 kernel) | 11.5 s | within the host's own swing |
| 4 | 12.6 s (6.9) | 13.5 s | 3.75, for 3.73 of their own |
| 8 | 14.0 s (7.9) | 15.1 s | 8.76, for 7.41 of their own |
| 16 | 15.7 s (9.2) | 22.9 s | 12.72, for 10.87; the host 17.88 of 18 busy |

With sixteen, `top` read 0.5% idle and 57% of the CPU the kernel's, and about 22 processes were runnable at each look. Beside others, a run's processes take more CPU than alone, and the host spends about a sixth again outside them. So one test costs the host its CPU per run, times that sixth, over its wall time alone: 14.0 × 1.18 / 11.5 = 1.44 cores at eight, and 15.7 × 1.17 / 11.5 = 1.60 at sixteen.

**The stub sluice's pause.** The stub paused with `read -rt 0.2 _ <> <(:)`. On deneb that answers "/dev/fd/63: Permission denied" in a millisecond: macOS refuses a read-write open of a pipe's `/dev/fd`. So a wait on a submission a test holds undecided exited 5 at once. crew's landing waiter calls `sluice wait` again on 5, so it spun for as long as the test held the decision. A fifo opened read-write does pause: `read -t 0.3` on one took 0.37 s.

**A test's own waits.** `until_ok` ran its command, then the real `sleep 0.1`, until the command succeeded, up to ten minutes. Many of its commands start processes: `field`, a Python and a `jq`; `plan`, a `git` and a `recsel`. `t-journey-main` waited for the other roles' greetings with a loop of its own: three `grep` and a `sleep` every tenth of a second.

**After this change.** Run alone again, `t-journey-land` took 181 s and 162.5 s of CPU (from 194 s and 180 s), `t-journey-board` 49.3 s of CPU (from 51.7 s) and `t-hold` 29.0 s (from 31.8 s).

**What is not the tests'.** Most of what a test starts is crew's own commands: each runs about 77 `git`. Each `python3 plan.py` also compiles plan.py's 15,755 lines afresh, 0.13 s of CPU, since Python caches the bytecode of a module it imports and never of the script it runs. That cost is crew's command core's. Lightening a command is crew's own work and no part of this fix, which changes no file under `plugin/`.

**The family.** A test's slot is crew's own: record 0021 and `tests.9` built it, and no tool of the family runs or bounds crew's tests. sluice bounds its own runs per branch, and a bound across every kit's runs on a host is sluice's, as record 0037 named, so there is nothing to reconcile here.

**Area pages this change touches:** `tests.md` (`tests.2`, `tests.8`, `tests.9`, `tests.10`, `tests.11`) and `docs.md` (`docs.2`, `docs.4`, `docs.6`). From `core.md`: `code.7`, since no decision of crew's changes. No rule changes, so no page is edited (`docs.7`).

## Goals / Non-Goals

**Goals:**

- The tests running at once on a host keep its cores less two busy and no more (`tests.9`).
- No wait in the tests starts a process ten times a second, and none spins.

**Non-Goals:**

- A lighter crew command. Its `git` and the compile of `plan.py` are crew's command core's (Context).
- A bound across every kit's runs on a host. That is sluice's (record 0037's finding).
- Moving end-to-end cases to the logic tier (`tests.11`, `tests.12`). That is done test by test, slowest first, by its own changes.

## Decisions

### Decision 1: The host's slots come from what one test costs it

`tests/slot` holds `TEST_CORES = 1.5`: what one test costs the host beside others, in cores, read as in Context. A host has as many slots as its cores less two hold at that cost, and at least one. That is ten on deneb's 18 cores, nine on the box's 16 and five on ten. `CREW_TEST_SLOTS` still names a count, and a count that is not one is still refused. Each test still holds one slot, so `crew ops quiet` still counts held slots as running tests.

The two cores left are the agents' and the user's, as before. The tests at once then keep the rest busy at the speed each runs alone. One suite's wall time hardly moves: it is `t-journey-land`'s, about three minutes, while the other 24 tests' CPU, spread over ten slots, takes about a minute.

The floor is one where it was two. A host's cores less two hold fewer than two tests only below five cores, and no host of the fleet has fewer than ten.

*Departs from* record 0021's consequence as amended on 2026-10-12, on the user's word, that a host's slots are its cores less two. The brief of this fix replaces it: "The number that run at once comes from what each test starts, not from the cores less two". `tests.9` stands as written. Its details still say the slots are the cores less two; they are the design agent's to read again after the landing (`docs.7`).

*Not taken:*
- A weight per test, a `# Cores:` line the slot takes that many slots for. Every test measured alike alone (0.8 to 1.0 cores), so the weight would be one number written 25 times, kept true by hand.
- The slots read from the host's load at each test's start: record 0037, which the user rejected ("This is terrible. I don't like the decision").
- Half the host's cores, record 0021's first amendment: a count with no reading behind it, which the user replaced on 2026-10-12.
- The cores less two, kept: sixteen side by side filled deneb (Context).

### Decision 2: A test's wait looks less often the longer it waits, and pauses with no process

`tests/lib.sh` makes `$T/.pause`, a fifo nothing writes, and holds it open read-write on fd 9. `nap <seconds>` is a `read -t` on it: a pause that starts no process, on macOS as anywhere.

`until_ok` looks at once. Then it pauses a tenth of a second, and each pause after is twice the last, up to a second. A wait that is over at once costs no pause. A wait of a few seconds runs its command a handful of times rather than ten a second. The limit stays ten minutes (`tests.8`), and a looser host only lengthens each pause, so it looks fewer times, never more.

*Not taken:*
- A fixed, slower look. A short wait would pay its whole first pause.
- The real `sleep` for the pause. It is a process per pause.

### Decision 3: The stub sluice pauses on the test's fifo, and a held wait takes a second

The stub's `pause` reads the same fifo, making it should it be missing, so it pauses on every host. A wait on a submission held undecided returns after a second, looking every tenth whether the hold is lifted and returning then. It still reads the hold once, so a hold lifted in that moment still exits 5 for that call, as before. A landing's waiter on a held submission then calls about once a second, where on macOS it called as fast as the host let it. The stub's other pause, while another wait lands the submission, uses `pause` too.

*Not taken:*
- The real `sleep` in the stub. It is a process per pause, and the stub cannot see `lib.sh`'s.
- The two tenths of a second the stub meant. Five calls a second, each a `bash`, a `git` and a `jq` or two, is still more than the case needs.

### Decision 4: t-journey-main waits with until_ok

The background wait for the design agent's and ops's greetings and the planner's read becomes `until_ok` on one function, `others_greeted`. Its ten-minute limit and the planner's answer after it are unchanged.

## Risks / Trade-offs

- **Fewer slots.** Several suites side by side on one host queue longer. sluice's twenty minutes for crew's checks hold a suite queued behind two others: each is about three minutes alone.
- **A later last look.** A wait may end up to a second after its condition holds.
- **One host's reading.** `TEST_CORES` was read on deneb. A host whose kernel starts processes more cheaply, such as the box, may cost less per test, and its count is still the same formula. The number is read again when the tests' weight changes.

## After deploy

None. This changes crew's test harness alone, which sluice runs on every submission. Nothing is deployed to a host.

## Task notes

**1.1** `tests/slot`: `TEST_CORES = 1.5` beside `GRACE`, with the reading it rests on. `count(cores=None)`: `CREW_TEST_SLOTS` as before, else `max(1, int(((cores or os.cpu_count() or 4) - 2) / TEST_CORES))`. The module's docstring says where the count comes from. `tests/t-slot.sh`: `count 18 16 10 4 2` gives `10 9 5 1 1`, and `count` with no cores gives this host's.

**2.1** `tests/lib.sh`: after `zzz`, `mkfifo "$T/.pause"; exec 9<>"$T/.pause"` and `nap() { read -rt "$1" -u 9 _ || true; }`. `until_ok`: `gap` in tenths of a second, starting at 1, `nap "$((gap / 10)).$((gap % 10))"`, then doubled up to 10. `tests/t-waits.sh`, new:
- `nap 0.3` with `PATH` an empty folder succeeds and takes at least 0.3 s, timed with `EPOCHREALTIME`;
- `until_ok` on a command that succeeds runs it once;
- `until_ok` on a command that succeeds once three seconds have passed runs it at most seven times.

**2.2** `tests/stubs/sluice`: `pause <seconds>`, a `read -rt` on `$CREW_TEST_ROOT/.pause`, made with `mkfifo` when it is not a fifo. In the held wait: up to ten pauses of a tenth, ending when `sluice-wait-holds` is gone. The wait for another wait's landing uses `pause 0.1`. Its header says a held wait takes a second or until the hold is lifted. `tests/t-waits.sh`: a submission record written in a scratch repository's common dir, as the stub's own submit writes it; held, `sluice wait 7` exits 5 with state `testing` after at least 0.9 s; once the hold is lifted it exits 0 with state `landed`.

**2.3** `tests/t-journey-main.sh`: `others_greeted`, the three `grep`s, and `answer() { until_ok others_greeted || true; as $box herdr --session wldn-3 stub status wldn-planner idle; }`.

**3.1** README's sentence on the test slots and CLAUDE.md's Tests bullet say how many slots a host has. CLAUDE.md also says that a test's waits start little. `tests/moon.yml` gains `t-waits`'s task from `tests/moon-tasks`.
