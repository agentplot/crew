# Design

## Context

This section records what was read on 2026-11-08 at this change's base, `2ae95617`, so the decisions below rest on it. The proposal's *Why* says what the change is for.

**What the runner's report holds.** A runner answers on `<label>/runner/<host>` with three files, in crew's formats (boomdrive `crew-control-plane`, "The runner's branch holds crew's three files in crew's formats"; `runner.PLACES`):

- `runner.rec`;
- `answers.rec`;
- `places.rec`: one `Place` per launched request. Its `Status` is `flume status --json <place>`'s answer, byte for byte.

crew reads that status through `runner.flume_facts`. Of a place's submission it reads:

- the entry's number and state (`submission.read.found.submission`, `waiting`, `under_test`, `landed`);
- how often the place was submitted and sent back;
- the last verdict, with its words;
- whether the submission is held;
- once the place is over and landed, the commit it landed (`phase.*.over.landed.commit`).

Flume 0.3.6's fixtures show what the status lacks (`tests/py/flume-0.3.6/`). Its `submission` holds no time: `read`, `submits`, `send_backs`, `verdict`, `waiting` and `held` only. A tidied place, `landed.json`, carries `submission: null` and keeps its landed commit.

**The family.** sluice holds the queue and its verdicts. Flume submits a place and reads its submission's entry. The runner carries Flume's status of each place to the control plane. In the hosted implementation, it also carries sluice's entry for each submission Flume names (boomdrive `tool-records`, "Each submission Flume names is carried from sluice's own answer"). crew's implementation of the control plane writes only the three files above. So everything crew may know of a submission is what Flume's status of the place says. crew becomes one more reader of the runner's report, beside the hosted control plane, and keeps no second path to sluice.

**Where crew runs sluice today** (`grep -n sluice plugin/lib/*.py plugin/bin/*`), sorted by who takes each:

| Where | What it runs or reads | Taken by |
|---|---|---|
| `gather.kit`: `overview`, `queue`, `submissions_of`, `decided_in` | `sluice overview --json`, a kit's queue for the bolts' rows and for a bolt's time | this change |
| `gather.landing_read` | the `Sluice-Result`, `Sluice-Submission` and `Sluice-Tested` trailers at a bolt's head, and `sluice status <n> --json` for a head landed beside the queue | this change |
| `board.Watches`, `Follower`, `stamps_now`, `gather.read`'s stamp `overview` | `sluice overview --json --watch` on each kit, and the overview asked at the clock's tick | this change |
| `plan.py`: `BOLT_CREATE`, `GIVE_READ`, `kit.sluice_refusal` | `sluice branch create`, `sluice --version` at a start | `crew-lands-each-bolt-through-flumes-base-place` (record 0056 point 2) |
| `plan.py`: `SUBMIT`, `QUEUE`, `WAIT`, `SUBMISSION_STATUS`, `HISTORY`, `SUBMISSIONS`, `landing_read`, `_landing-read`, `landing_time` | crew's own landing: `wt submit main`, `sluice overview`, `sluice wait`, `sluice status` | the same unit (record 0056 points 3 to 5) |
| `plan.py`: `BOLT_DELETE`, `tidy`'s `sluice_read(main, "overview")` and `release --worktree` | `sluice branch delete`, the landing places' runs and release | the same unit (record 0056 point 5) |
| `plan.land_facts`, `pull_of` | the pull request a landing's `Sluice-From` names | the same unit |
| `gather.bolt_landings`, `ops.py` `RANGE`, `runner.built_on_bolt` | `Sluice-From` on the landing commits of a bolt and of main | `crew-reads-each-pieces-end-from-the-runners-report` (record 0062) |
| `plan.previews_of`, `_preview`, `preview_release` | `sluice previews`, `sluice preview … --wait`, `sluice release <target>` | none yet: Decision 1 |

crew runs no `flume` command anywhere. Its Flume reads are the runner's carried status alone (`runner.flume_facts`, `asks.py`).

**Area pages this change touches:**

- `core.md`: `roles.5`, `roles.9`, `read.1`, `read.2`, `state.4`, `code.7`, `code.8`;
- `plan.md`: `plan.12`, `plan.16`, `plan.20`, for `gather.py`, `plan.py` and `kit.py`;
- `tests.md`: `tests.4`, `tests.5`, `tests.11`;
- `briefs.md`: main-level ops's brief;
- `docs.md`: `docs.2`, `docs.6`, `docs.7`.

Under `docs.7`, no rule page or record is edited here. The departures below are the design agent's to amend after the landing.

## Goals / Non-Goals

**Goals:**

- No gather of a kit and no follower runs a sluice command. Nothing crew shows of a bolt's queue or its verification is read from sluice.
- What crew read from sluice, it reads from the runner's report where the report carries it, and does without where it does not (the unit's intent).
- A bolt reads proven, and its landings row can land, exactly when it did before for every bolt whose work is built through Flume.

**Non-Goals:**

- crew's own landing of a bolt, and the sluice commands it runs. Record 0056 point 7 keeps that landing as it is until the landing unit's release.
- The `Sluice-From` readings, which are record 0062's stopgap.
- Card previews.
- Any change to the runner, Flume or sluice.

## Decisions

### Decision 1: What this change takes, and what it leaves

It takes the reads that record 0056's *Consequences* name outside a bolt's landing:

- the gather's queue and verdict;
- the follower's watch;
- what the views draw from them.

It leaves three things:

- **crew's own landing.** `crew bolt submit`, its wait, read and history, the start's and the land's branch commands, and the landing places' release. These are record 0056 points 1 to 5 for a bolt, built by `crew-lands-each-bolt-through-flumes-base-place`. Until that unit ships, crew lands as today (point 7), and taking the landing's reads away first would leave crew unable to land.
- **The `Sluice-From` readings.** These are the one named stopgap (record 0062), which `crew-reads-each-pieces-end-from-the-runners-report` retires.
- **Card previews.** A preview is an ask of sluice for an environment, on a card of a batch or a landing, live in swancloud's and switchboard-kit's policies (`[preview]`). It reads no landing and no queue, and the runner's report carries no preview to read in its stead.

Path not taken: doing without previews now. That would take previews off those kits' cards until the runner carried them. That loss is not this unit's intent, and leaving previews in place is cheap to undo later.

### Decision 2: A piece's submission and a bolt's landing come from the runner and the run record

Every started bolt's work is a Flume place (`plan.started`: `Path: flume`). Each piece's line already says its submission through `runner.piece_said`: `submitted #41`, or its stage with sluice's words once it is sent back. That is read from Flume's status of the piece's place as the runner carried it. The overview's `submission` beside it, `#41 under test`, repeats it, so it goes.

A bolt's landing on its head line is what the run record holds (`plan.landing_phase`): queued as #n, landing again, or rejected at its head. `phase_said` names the number always. Its `live` argument goes: it hid the number while sluice's queue showed the landing standing. `submission_rows`, `standing_said` and `queue_read` stay for crew's own landing (`landing_standing`), which still reads sluice's queue before it submits. No view calls them.

"Submissions can't be read" goes with the read it said. A runner that can't be read is already named, and the stages of its work read unknown (`Stages.unread`, `runners_unread`). Nothing is read from a default (`read.1`).

### Decision 3: The follower learns from the runner's branch

The follower already looks at each partition's runners' branches with no process (`board.look`, `plan.runner_tips`). It fetches them with the partition's branch on its clock (`fetches`), and takes a host as moved when its runner's branch moves (`host_basis`). A submission's move reaches crew in a runner's report, so that is how the follower learns of it.

These go:

- the overview watches (`Watches`) and the clock's overview ask;
- the queue stamps;
- the submissions the follower kept;
- the seeding of a new watch from a gather;
- every argument and key that carried them.

`crew _follow --once` still makes one tick and ends; it no longer says "with no watch".

Trade-off: a submission's move reached the board within seconds through the watch. Now it reaches the board at the runner's next report and the follower's next fetch, within about a minute plus the runner's pass. That is the record's design: crew knows what the runner reports.

### Decision 4: A bolt's verification is its work's landing at its head, as the runner reports it

`runner.verification(head, pieces)` decides it, as a function of plain facts (`code.7`):

- `head` is the bolt's head, read where the bolt lives (`gather.bolt_read`, git).
- `pieces` is each unit, chore and fix of the bolt, with its stage as `Stages` gives it: `runner.stage_of`, or `runner.built_on_bolt` for record 0062's stopgap.

It returns:

- **green**, naming the head and the work, when some piece reads `merged` or `landed` with a `commit` equal to the head;
- **none**, saying the head is no landing of its work that the runner reports, otherwise;
- **unknown** when there is no head.

`kit.verification`, `kit.covering` and `kit.VERDICT` go, and `gather.landing_read` with them.

This keeps record 0025 point 4, the kit's checks green at the bolt's head. Every piece lands on the bolt through a submission sluice decides (`teams.5`). sluice lands only once the checks its policy requires pass, or beside its queue when none of them reads the submission's changes (sluice clause 140). So a head that is a piece's landing is a head the kit's checks passed. A landing beside, a take-main fix's among them, reads green like any landing of the bolt's work. That drops merge-gate's covering-verdict read, which needed sluice's record (`sluice status <n>`).

Paths not taken:

- **Read the verdict in Flume's status of the landed place.** A tidied place carries `submission: null` (flume 0.3.6 `landed.json`), so most bolts would read unknown and never be offered for landing.
- **Do without a verification, proven once every piece merged.** That would offer a bolt whose head is no landing of its work, such as a commit pushed by hand, and it departs further from record 0025 than the record needs.

The commits compare whole. Flume's landed commit and `bolt_landings`' `%H` are full shas, and so is the head from `rev-parse`. A piece whose commit is missing matches nothing (`read.2`).

**Departs from `tests.5`.** That rule reads the verification "from the landing commit", its `Sluice-Result`. It is now read from the runner's report of the commit the bolt's work landed at, for record 0056 points 1 and 4. The rule's outcome, that the bolt's proof is the kit's checks at its head, stands. `plan.16`'s "verification is green at its head" stands as written.

### Decision 5: A bolt's time in the views reads no submission

`held_time` gives `bolt_facts` no submissions and no decided ones: `([], None)` for both. So the board, the rail and the bands place no minute by a submission.

The runner's report carries no time of one. Its status's `submission` holds none, and `places.rec`'s `At` is the time of the runner's pass, not of sluice's events. `bolt_time`, `bolt_facts`' signature and `landing_split` stay. A landing's entry still records the split, from sluice's record read once at `crew bolt land` (`landing_time`, `HISTORY`), which is crew's own landing (Decision 1) and leaves with it.

**Departs from `plan.20`.** In the live rows, the team's share of "a submission in a gate" and the kit's share of "a gate's checks running" are no longer read. Those minutes go to whatever else holds the bolt, else nobody. The rule's "the bolt's own work as the runner reports it running" was not built before this change either.

Path not taken: rebuild a place's times from the history of the runner's branch. That would be a reading crew has nowhere else, and its times would be the runner's passes, not sluice's.

### Decision 6: The gather runs no sluice

These go from `gather.py`:

- `overview`, `queue`, `sluice_ran`, `SLUICE_ANSWER`, `decided_in`, `landing_read`, `LANDING_TRAILERS` and `BESIDE_FIELDS`;
- the request's `queued`, `decided` and `overview`, and the stamp request's `overview`;
- the answer's `submissions`, `decided`, `submissions_error`, `decided_error`, `overview`, `overviews`, `verdict` and `beside`.

`submissions_of`, `status_read` and `sluice_said` stay. They start no process, and crew's own landing calls them (`queue_read`, `history_read`). On the plan's side, `survey`'s gather requests hand in no queue (`plan.py` near 1396). `Kept` loses `queued` and `decided`, and `stamped` loses its `overview` argument.

The gather still reads the kit's `.config/sluice.toml` as text (`policy`), for a start's checks. That is crew's own landing of a bolt (`plan.19`), and it runs no process.

### Decision 7: Where each scenario is proved

These scenarios are decisions on plain facts (`tests.11`), proved in the logic tier:

- the verification;
- the lines;
- the head line;
- the time split;
- the follower's refresh plans and stamps.

That "the gather runs no sluice" is proved in the contract tier. A scratch kit holds a bolt whose head is a landing beside the queue, and a `sluice` first on the path appends every call it gets to a file. The gather's answer and the empty file are asserted (`tests.4`).

The follower's whole life, read, tick, report and gather, is proved end to end by `t-journey-board`, whose log names every `sluice` the stubs ran. The bolt's verification read from the runner's report is proved by `t-sluice` and `t-journey-land`. The stub `sluice` keeps its `overview` and `--watch`, since crew's own landing still asks the overview.

### Decision 8: The words

The following say where the queue and the verification come from:

- `crew bolts`' lines in `plugin/bin/crew`'s usage, README and `plugin/skills/crew/SKILL.md` (`docs.2`);
- the follower's lines in `crew`'s usage and `board.py`'s;
- `plugin/roles/main-ops.md`'s first paragraph;
- CLAUDE.md's *Proving and landing a bolt*.

The mod draws the rows the views give, so nothing it draws changes (`code.8`). Its comment on when the views are written loses the overview watch.

## Risks / Trade-offs

- **[A bolt whose last piece's landing is in no report and named by no landing commit reads none.]** → Every Flume landing on a bolt names its place's branch in `Sluice-From`, which record 0062's stopgap reads. Once the Boomdrive unit `the-runner-carries-each-places-end` ships, the report carries every end. A bolt that reads none is not offered, and is never offered wrongly (`read.1`).
- **[A submission shows on the board up to a minute later than through the watch.]** → Decision 3. The rail and the board already wait on the runner's report for every other stage.
- **[Fixtures across the logic tier made a bolt green with `verdict: passed …`.]** → `facts.crew_read`'s default head becomes the commit of `tests/py/flume-0.3.6/landed.json`'s place. A bolt whose pieces stand landed then reads green, and a case of a head that is no landing sets its own head (Task notes 1.2).
- **[crew still runs sluice for its own landing and for previews.]** → The specs and the words claim "no sluice" only for the gather, the follower and the views. Decision 1 names who takes the rest.

## Migration Plan

Nothing to migrate. No file crew writes changes shape: the run record, the plan and the frames carry nothing of the queue. A follower that starts on the new crew opens no watch. A watch left from the old one ends with the process that held it.

## After deploy

None. Every scenario is proved by a check in crew's tiers, and nothing of a host's needs a step once the release reaches it (`docs.6`).

## Task notes

**1.1** In `plugin/lib/runner.py`, beside `built_on_bolt`, add `verification(head, pieces)`:

- `pieces` is `[(work, s)]`: `work` as requests name it (`unit/<u>`, `chore/<c>`, `fix/<bolt>/<f>`), and `s` as `stage_of` or `built_on_bolt` gives it.
- It returns `("unknown", "no head crew can read")` with no head.
- It returns `("green", f"its head {head[:7]} is {bare(work)}'s landing, as the runner reports it")` for the first piece in the order given whose `s["stage"]` is `merged` or `landed` and whose `s.get("commit") == head`. Use the words "as its landing on the bolt names it" when `s.get("on") == "bolt"`.
- Otherwise it returns `("none", f"its head {head[:7]} is no landing of its work that the runner reports")`.

Cases go in `tests/py/test_runner.py`, a class `TestVerification`:

- a unit landed at the head;
- a chore;
- a fix landed beside, which reads the same;
- one read from the bolt (`on: bolt`);
- a piece merged at another commit;
- a piece with no commit;
- no pieces;
- no head.

**1.2** Switch every reader of the old verification to `runner.verification`:

- `plan.Stages.bolt_state`;
- `plan.landing_unready`: its signature becomes `(work, verified, fixes)`, where `verified` is the `(state, words)` pair;
- `plan.land_facts`;
- `plan.bolts_data`: its `verification`;
- `plan.rail_rows`'s landings row, near `plan.py` 11587.

Each builds `pieces` from `st.of(u.name())["flume"]` for the bolt's units and chores, and `st.fixes(b)` for its fixes. Delete `kit.verification`, `kit.covering` and `kit.VERDICT`, and the docstrings that cite them, `Stages.bolt_state`'s "sluice is green at its head" among them.

In `tests/py/test_kit.py`, `TestVerification` and `TestLandedBeside` go. In `tests/py/facts.py`:

- `crew_read`'s default bolt head becomes `LANDED`, the commit `flume-0.3.6/landed.json` landed (`d185a879b51dba33555c036392b50443f4dfc5e8`), and its `"verdict"` goes;
- `landed_beside`, `BESIDE_HEAD`, `COVERING`, `BESIDE_OLD` and `BESIDE_NEW` go once nothing uses them.

Every case that made a bolt green by a `verdict` makes it green by its head being a merged piece's commit. Every case of a bolt "not green" sets a head that no piece landed at. Those cases are in these files:

- `tests/py/test_rail.py`, `test_landing.py`, `test_landings.py`, `test_pane_landing.py`, `test_stages.py`;
- `test_bolt_commands.py`, `test_batch_answer.py`, `test_board.py`, `test_cards.py`, `test_ops.py`, `test_kit_rename.py`.

A `verdict` that is crew's own landing's outcome, `crew bolt submit`'s, stays as it is (Decision 1).

**1.3** In `plugin/lib/gather.py`, `kit()` no longer spreads `landing_read` into a bolt's read. `landing_read`, `LANDING_TRAILERS` and `BESIDE_FIELDS` go, and the module's docstring loses "each bolt's verdict …". In `tests/contract/test_gather.py`, `test_a_head_landed_beside_the_queue_is_read_with_sluices_record_of_its_submission` becomes a case where the gather reads such a head with no `sluice` run and no `verdict` or `beside` in its answer. The recording `sluice` is a script in `tmp_path` that appends its arguments to a file, first on `PATH` by `monkeypatch`.

**2.1** Make these changes in `plugin/lib/plan.py`:

- `bolts_data` drops `submission_rows`, the units' and fixes' `submission`, and the bolt's `landing` and `submissions_error`;
- `bolts_text` drops the `landing #…` it added after `record_said`, the "submissions: can't be read" line, and the `standing_said` of a unit or fix line;
- `phase_said` loses `live` and always names the number;
- `standing_said` and `submission_rows` stay for `landing_standing` alone, their docstrings saying so.

Make these changes in `plugin/lib/board.py`:

- `board_data` (near 285) drops `submission_rows`, `submission`, `landing` and `submissions_error`;
- `merge_said`, `landing_said` and `queue_said` go from every row;
- `head_said` calls `phase_said(record, head)`.

`ops_view`'s rows near 835 name a landing from `b["record"]`: queued or again, through `plan.phase_said`, for each bolt whose record has one. That is the band's "each landing the run record holds queued or landing again, with its number".

Cases:

- `tests/py/test_bolt_submissions.py`'s `crew bolts` cases (from 312) assert the line from the runner's status and the head line from the run record. The case for a queue that can't be read becomes "sluice's record can't be read", in which nothing is said of it. The overview parsing cases of `submissions_of` and `status_read` stay. The `decided_in` cases go with it, in task 3.2.
- `tests/py/test_board.py` `TestSubmissions` and `TestViews`, and `tests/py/test_rail.py`, follow.

**2.2** `plan.held_time` passes `([], None)` for both the submissions and the decided to `bolt_facts`, and its `pair` helper goes. `bolt_facts`' docstring says that the views hand it none and `landing_split` hands it sluice's record. In `tests/py/test_board.py`, `TestTime`, a case shows a runner-reported submission under test placing no minute (crew-board "A submission the runner reports"). `tests/py/test_bolt_time.py` and `test_landing.py`'s `TestAgeAndSplit` stand unchanged.

**3.1** In `plugin/lib/board.py`, these go:

- `Watches`, `queue_key`, `queue_moved`, `queue_stamp`, `queue_of`, `kept_submissions`, `decided_kept`, `queue_kits`, `watch_plan`, `watch_key` and `watch_refused`;
- `host_basis`'s `queues`;
- `moved`'s `queues`, and `any` no longer counts them;
- `refresh_plan`'s "a kit's queue" from its sweep;
- `stamps_now`'s `overviews`;
- in `Follower`: `watch`, `watches`, `subs`, `requeue`, the method that remade the kept submissions, the seeding in `check` and `read`, and `queues` in its stamps and `seen`.

`main` builds `Follower(lock, period)`, and `--once` still ticks once. The follower's usage at the top of `board.py` drops the overview watch.

In `tests/py/test_board.py`, `TestWatches` and `TestKept` go. `TestMoved`, `TestRefresh`, `TestAsking` and `TestFollower` lose their queue cases, and gain one where a moved runner's branch is the host's move with no queue in its basis.

**3.2** In `plugin/lib/gather.py`, these go:

- `SLUICE_ANSWER`, `overview`, `sluice_ran`, `queue` and `decided_in`;
- in `kit()`: the block that read the queue (`req.get("queued")`, `overview(main)`, `out["submissions"]`, `out["decided"]` and their errors) and the `stamped` overview;
- in `read()`: the stamp's `overviews`;
- in the docstring: the request's `queued`, `decided` and `overview`, and "and sluice" from what it reads with.

In `plugin/lib/plan.py`:

- `stamped` loses its `overview` argument and the request key;
- `survey`'s kit requests near 1396 hand in no `queued` or `decided`;
- `Kept` loses `queued` and `decided`.

In `tests/contract/test_gather.py`, these become one case: the gather of a kit with a held bolt, a merge decided, one standing and a head landed beside, with the recording `sluice`, asserting no call and none of those keys. They replace the two queue cases:

- `test_a_kits_queue_handed_in_is_its_submissions_and_sluice_is_not_run`;
- `test_a_kits_gather_reads_sluice_only_through_one_overview_and_with_its_queue_handed_in_starts_no_sluice`.

`TestStamp` loses its overview cases.

**3.3** In `tests/t-journey-board.sh`, the section from line 198 that waits for the overview watches becomes this:

1. The follower's first read and its ticks run no `sluice` on either host: `grep ' sluice ' "$CREW_TEST_LOG"` counts 0.
2. `runner_writes` (`tests/lib.sh`) moves the box's runner's branch to carry unit `a`'s place submitted as `#41`, its status `tests/py/flume-0.3.6/code.json`'s with a submission found under test.
3. The next refresh after the follower's fetch draws `submitted #41` on `a`'s line in the board's frame.

The opening comment's line 11 says so. If the test reads a file it did not name, its `# Reads:` line gains it, and `tests/moon-tasks` is run and `tests/moon.yml` committed (`tests.10`).

**3.4** In `tests/t-sluice.sh` (line 56) and `tests/t-journey-land.sh` (line 118), the bolt's verification is asserted as `green, its head <h> is <work>'s landing, as …`. Each test's opening comment says the verification is read from the runner's report. The `sluice-overview.json` that `t-journey-land` writes for crew's own landing (line 769) stays.

**4.1** The words, as Decision 8 lists them:

- In `plugin/bin/crew`'s usage, `crew bolts`' lines 53 to 55 say each held bolt's verification, whether its head is its work's landing as the runner reports it, and each piece's submission as the runner carries it. They no longer say "sluice's queue".
- `crew _follow`'s lines 335 and 336 drop the overview watch.
- README's paragraph at line 63 says the same, with `--json`'s keys as they now are, and README's other mentions of the queue follow.
- `plugin/skills/crew/SKILL.md` lines 24, 31 and 40 follow.
- `plugin/roles/main-ops.md` line 13 says "A bolt's proof is its verification, its head the landing of its work as the runner reports it". `t-briefs.sh`'s phrase "shows every unit merged and the bolt's verification green" stays true.
- CLAUDE.md's *Proving and landing a bolt* first bullet says the verification is the landing of the bolt's work at its head, as the runner reports it, which `crew bolts` shows (record 0025, record 0056).
- `plugin/hooks/status.js` line 13 says the follower writes the views within seconds of a write on this host, and at its clock's fetch of a runner's report.
