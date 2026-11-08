# Design: a landing's close never waits on its own lock

## Context

The proposal gives the box's case. This change touches the areas of `plan.md` (`plugin/lib/plan.py`) and `tests.md` (`tests/`). Rules it relies on:

- `plan.21`: a landing is recorded by the first act of crew's that reads the bolt after it. The team's read is one such act, and so is a landing's own read.
- `read.5`: a decision reads the flywheel's branch at the newest commit whose entry has arrived. This is why a tidy can find a bolt still held after its close.
- `code.9`: a crew command answers within the time an agent's shell gives one command. A command that never answers breaks it.
- `tests.4`, `tests.8`, `tests.11`: the case goes in the logic tier, its wait has a limit, and it starts no process.

It departs from no rule.

### The path that waits on itself

Read in `plugin/lib/plan.py` at `23b3b3dc` on crew main, where the team's tidy ran it; on `teamless/deneb` the same path runs through the kit's read, read at `ddab9793`:

1. `landing_read` opens `landing_state(t)/landings/<bolt>.lock` and takes `flock(LOCK_EX)`. It holds the lock through the outcome's read, its record, the close, and the mark it keeps of what it said.
2. A bolt read landed that the plan still holds is closed: `landing_close` calls `bolt_land(by=<label>-ops)`. With `by` given, `bolt_land` reads no landing itself. It writes the plan and then asks for the kit's read after the landing (`sweep_on`).
3. `sweep_on` runs `kit_read` in its own process when the kit's host is this one, as it is, since a landing is read only on the host its work runs on; elsewhere it runs `crew _sweep <label> <kit> --landed <bolt> …` there through `crew.on_machine`, `subprocess.run` with no timeout.
4. `kit_read` ran `reap_landings` on every read. `reap_landings` reads the plan, and for each bolt whose work runs on the host and whose landing is due by `landing_read_due` it calls `landing_read`, which opens the lock's file afresh and waits on the lock from step 1: `flock` holds a lock per open file, so a second open in the same process waits on the first as another process would.

On crew main the close ran `crew _tidy --landed` and its `reap`; every way a holder of the lock reaches that lock again goes through this path. `landing_read` is called by `reap_landings`, by `landing_read_on` (from `bolt_land` with no `by`, and from `landing_ended`) and by `crew _landing-read`. Under the lock, `landing_close` calls `bolt_land` with `by` set, so it never reaches `landing_read_on`. `landing_close_out` and `landing_not_landed` run bash on the host (`LANDED`, `LANDED_MARK`, `SUBMISSIONS`) and hand the kit's card raise to `crew _land-card` (`land_hand`). Neither of those reads a landing. `land_delete` runs `BOLT_DELETE` in bash and takes no lock. So the only way back to the lock is the close's tidy reading landings.

The tidy finds the bolt due only when it reads a plan that still holds it. That is the plan below the close: its `bolt.land` entry is written after the plan's push and reaches the branch only once its own push is taken, so until then `decision_at` reads below the close (`read.5`). On a branch as busy as wldn's, the tidy can read the plan before that entry has arrived. A second shape needs no such lag. Two bolts of one team close at once, X and Y. X's read holds X's lock and waits on its tidy, and that tidy reads Y's landing, due because Y's units have all landed. Y's read holds Y's lock and waits on its own tidy, which reads X's. Each waits on the other for good.

## Decisions

### Decision 1: the read a landing's close runs reads no landing

On `teamless/deneb`, `kit_read(fleet, t, landed)` skips `reap_landings` when `landed` is given, as crew main's `reap(fleet, team, landed)` does; the rest of this decision is read from main's tidy, and holds for the kit's read the same way. `landed` is given only when `team_tidy` runs as `crew _tidy --landed <bolt>`, and only `bolt_land` asks for that, through `tidy_after`, once a landing is closed. The bolt it follows was read by the act that closed it: by `landing_read` under its lock, or by `bolt_land` run by hand, which reads a queued landing first (`landing_read_on`). The team's other bolts are read by the team's next read: the conductor's next command or wait, `crew status`, or a stage's start. A holder of any landing's lock then never waits on a command that takes one, so both shapes above go. The lock still covers the close and its tidy, as before, so a read that waited on it finds the tidy done and says what the first read said, its tidy's words among them (`landing_kept`).

Considered and not taken:

- **Run the tidy after the lock is let go.** `bolt_land` would hand its tidy back, and `landing_read` would run it once out of the lock. The tidy would still read landings. The bolt's own read would take the free lock, find the plan below the close still holding the bolt, and close it again. That second write is refused at the tip, which holds no bolt, so a refused `bolt.land` would be recorded on a bolt that landed and closed (`landing_close`, `close_refused_new`). It would also leave the tidy's words out of what the lock's mark keeps, and leave the cross shape of two bolts as it is.
- **Tell the tidy it already holds the lock.** An environment variable naming the held lock would let a read in the tidy skip that bolt. The tidy would still read the team's other bolts under the parent's lock, so the cross shape stays. It also asks the lock's meaning to cross a process boundary that `crew.on_machine` crosses over ssh for every other host.

### Decision 2: the other locks were read for the same shape, and none has it

Each was read for a holder that waits on a command, or reaches code in its own process, that takes the same lock:

- **`waits/<slot>.lock`.** `stage_wait` takes it non-blocking and refuses when it is held. `crew needs` (`stage_needs`) also takes it non-blocking, and gives up after six polls. Nothing ever blocks on it, so no holder can wait on itself.
- **`handed/.lock`.** `construct_handed` holds it while it runs a construct (`run_unit_stage`), and through `reap` that construct can read a landing and run its close and tidy. Only `construct_handed` takes this lock. It runs in a process `construct_hand` starts with `Popen(start_new_session=True)`, which nothing waits on. Nothing under the lock starts it.
- **The cards' `land/.<kit>.lock`.** `raise_landings` holds it and reads each bolt's row on its team's host, through `crew _land-row`, or in its own process when that host is this one (`land_row`). A row's read opens its reading and preview and ends a held row's reading. It raises no card and reads no landing: `land_row`, `land_read`, `land_facts`, `landing_opened`, `reading_open`, `row_card_close` and `row_card_change` reach neither `land_hand`, `raise_landings` nor `landing_read`. A landing's read may wait on this lock, through `land_hand`'s `crew _land-card`, but the raise never waits on a landing's lock, so the two never wait on each other.
- **The other `flock`s.** `stages_file`, `short_lock`, `preview_lock`, a card folder's `.lock`, a proposal's answers' `.lock`, `hold.crossing` and `_renew`'s lock hold no `crew` command they wait on.

## After deploy

None. What the fix does is proved by the logic tier. The box runs it once its crew moves to a commit that holds it, through swancloud's live worktree or its pin, and nothing about that can be checked by hand.

## Task notes

**1.1** On `teamless/deneb`: in `kit_read`, `reap_landings` runs only when `landed` is not given; the docstrings of `kit_read`, `kit_sweep` and `sweep_on`, and the comment on `landing_read`'s lock, say why. `tests/py/test_landing.py`, `TestTheLandingsRead`: the close (`bolt_land`) runs the real `sweep_on`, which runs the real `kit_read` in this process, and a landing read there reads `b` under a lock file opened afresh, as `reap_landings` does; the read runs in a thread joined with a one-minute bound, and before the fix fails at the bound. On crew main: in `reap`, `reap_landings(fleet, t)` runs only when `landed` is not given. The docstrings of `reap` and `team_tidy`, and the comment on `landing_read`'s lock, say why. `tests/py/test_landing.py`, `TestTheLandingsRead`: a case drives `landing_read` with the real lock in its team state. The close (`bolt_land`) calls the real `tidy_after`. `crew.on_machine` runs `crew _tidy` as the real `team_tidy`, parsed by crew's own parser, in a thread of its own, waited on to its end as `subprocess.run` waits. The tidy reads the plan still holding the bolt with every unit landed. The read runs in a thread joined with a one-minute bound. It must end, record one `bolt.submit` outcome, close the bolt once, and run the tidy with `landed` set. Before the fix the case fails at the bound, the read waiting on its own lock.

**2.1** `tests/suite --affected`, against the merge-base with main.
