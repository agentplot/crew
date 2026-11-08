# crew reads a bolt's queue and verification from the runner's report

## Why

Record 0056, as the user rewrote it and accepted it on 2026-11-08 (9c71cd16), makes crew the control plane. crew talks only to Boomdrive's runner. It never calls Flume or sluice, and it reads neither one's records (point 1). What the runner's report does not carry, crew does not read anywhere else (point 4).

The record names three places where crew still calls sluice outside a bolt's landing (*Consequences*):

- crew's plan reads a landing with a `sluice … --json` in a kit's main;
- the gather of a kit runs `sluice overview --json`, and `sluice status <n> --json` for a head landed beside the queue;
- the board's follower keeps a `sluice overview --json --watch` on every kit.

All three read sluice's queue, or its verdict on a bolt's head. The unit's intent is that each one comes from the runner's report, or crew does without it (agentplot/crew `plan.rec`, unit `crew-calls-no-tool-but-its-runner`).

The report already carries most of it. A runner's branch holds `places.rec`: Flume's status of each place it launched, as Flume gave it (boomdrive `crew-control-plane`, "The runner's branch holds crew's three files in crew's formats"). That status names the place's sluice submission, its number and state, and the commit it landed. crew already reads it to tell each piece's stage (`runner.stage_of`). So the queue and the verdict that crew reads from sluice repeat, by another way, what the runner reports.

## What Changes

- **The gather runs no sluice.** `gather.py` no longer runs `sluice overview --json` for a kit's queue. It also no longer runs `sluice status <n> --json` for a head landed beside the queue, and it no longer reads the `Sluice-Result` trailer at a bolt's head. A kit's answer carries no `submissions`, `decided`, `overview`, `verdict` or `beside`. A request carries no `queued`, `decided` or `overview`.
- **The follower keeps no sluice watch.** The board's follower opens no `sluice overview --json --watch` and asks no overview at its clock's tick. It keeps no submissions of its own. It learns that a piece's submission moved from the runner's branch: it already looks at that branch with no process, and fetches it on its clock.
- **A piece's submission is on its line from the runner's report.** A unit's, chore's or fix's line shows its sluice submission as Flume's status of its place gives it. That is already its stage, `submitted #41`, or sent back with sluice's words (`runner.piece_said`). The second number beside it, read from sluice's queue, goes. A bolt's landing on its head line is what the run record holds: queued as #n, landing again, or rejected (`plan.landing_phase`). The line "submissions can't be read" goes. A runner that can't be read already says that the stages of its work are unknown.
- **A bolt's verification is its work's landing at its head, as the runner reports it.** A bolt is green once its head is the commit at which one of its units, chores or fixes reads merged or landed. That commit is Flume's landed commit as the runner carried it, or the landing commit that record 0062's named stopgap reads. Otherwise the bolt's verification is none, and it is unknown with no head to read. Its proof, its landings row and its card follow, as before, from its verification. A landing beside the queue reads green like any other landing of its work.
- **A bolt's time on the board and the rail reads no submission.** The runner's report carries no time of a submission, so the live views place no minute by a submission. The split of a bolt's time at its landing is recorded once, at its own act, from sluice's record (`landing_time`). That split stays with crew's own landing, below.
- **The words follow.** The following say where the queue and the verification now come from: `crew bolts` in the usage header and in README, the crew skill, main-level ops's brief, CLAUDE.md's *Proving and landing a bolt*, the follower's usage in `board.py`, and the mod's comment on when the views are written.

Left as they are, each for its own change:

- **crew's own landing of a bolt**, and every sluice command it runs, stays. That covers:
  - the start's `branch create` and its `sluice --version`;
  - `crew bolt submit`'s queue read, wait, `sluice status <n>`, history and `_landing-read`;
  - the land's `branch delete`;
  - the landing places' `sluice overview` and `sluice release --worktree`;
  - the landing's pull request, read from `Sluice-From`.

  Record 0056 point 7 keeps crew landing as it does today until the release that carries its points 1 to 5 for a bolt. Those points are the unit `crew-lands-each-bolt-through-flumes-base-place`.
- **The `Sluice-From` readings stay.** These are the three readings of record 0062's named stopgap, which `crew-reads-each-pieces-end-from-the-runners-report` retires.
- **Card previews stay.** These are `sluice previews`, `sluice preview … --wait` and `sluice release <target>`. They ask sluice for an environment, and read no landing and no queue. The runner's report carries no preview.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `merge-gate`: a bolt's verification is the landing of its work at its head, as the runner reports it, and no longer sluice's trailer or its record of a landing beside.
- `bolt-teams`: a bolt's proof reads that verification. A piece's submission is on its line from Flume's status of its place, and a bolt's landing on its head line from the run record, no longer from sluice's queue.
- `bolt-plan`: a bolt on GitHub is read where it lives, its verification among what is read there, as the runner reports its work.
- `crew-rail`: a land row's line says what the verification is, as the runner reports it.
- `crew-board`: the follower runs no sluice and follows no queue. A refresh learns that a submission moved from the runner's branch. A bolt's time in the views is read from the run record and its cards and holds alone.
- `rail-cards`: the landings card's row can land once its verification is green, as the runner reports its work.

## Impact

- `plugin/lib/gather.py`: these go: `overview`, `queue`, `sluice_ran`, `decided_in`, `landing_read`, `LANDING_TRAILERS`, `BESIDE_FIELDS`, the request's `queued`, `decided` and `overview`, and the answer's `submissions`, `decided`, `*_error`, `overview`, `overviews`, `verdict` and `beside`. These stay, starting no process: `submissions_of`, `status_read` and `sluice_said`, which crew's own landing still calls.
- `plugin/lib/board.py`: these go: `Watches`, `queue_key`, `queue_moved`, `queue_stamp`, `queue_of`, `kept_submissions`, `decided_kept`, `queue_kits`, `watch_plan`, `watch_key` and `watch_refused`. The `Follower`'s watches, `subs`, `requeue` and seeding go. `host_basis` loses its queues, and `stamps_now` its overviews. The `merge_said`, `landing_said` and `queue_said` lines go. `board_data` gives no `submission`, `landing` or `submissions_error`.
- `plugin/lib/plan.py`: the following change:
  - `Stages.bolt_state`, `landing_unready`, `land_facts`, `bolts_data`, `bolts_text`, the landings row's read, `held_time` and `stamped` change;
  - `Kept` loses `queued` and `decided`;
  - the gather request no longer hands in a queue.
- `plugin/lib/runner.py`: gains `verification(head, pieces)`.
- `plugin/lib/kit.py`: loses `verification`, `covering` and `VERDICT`.
- `plugin/hooks/status.js`: its comment on when the views are written changes. Nothing it draws changes: it draws the rows the views give.
- `plugin/bin/crew`, `README.md`, `plugin/skills/crew/SKILL.md`, `plugin/roles/main-ops.md`, `CLAUDE.md`: their words on the queue and the verification change.
- Tests:
  - `tests/py/test_kit.py`, `tests/py/test_runner.py`, `tests/py/test_board.py`, `tests/py/test_bolt_submissions.py`, `tests/py/test_rail.py`, `tests/py/test_landing.py` and `tests/py/facts.py`;
  - `tests/contract/test_gather.py`;
  - `tests/t-journey-board.sh`, `tests/t-sluice.sh`, `tests/t-journey-land.sh` and `tests/t-docs.sh`.
- Nothing changes in the runner, Flume or sluice. The stub `sluice` keeps what crew's own landing and the previews still run.
