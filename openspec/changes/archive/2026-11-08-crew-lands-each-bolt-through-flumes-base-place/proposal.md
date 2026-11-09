# crew lands each bolt through Flume's base place

## Why

crew still drives a bolt's branch through sluice from start to end. `crew bolt start` makes it with `sluice branch create`. Main-level ops lands it with `crew bolt submit`, which cuts a worktree on the bolt's branch, levels the host's copy, readies the pull request, runs `wt submit main`, waits on `sluice wait` and reads sluice's records. `crew bolt land` then has sluice delete the branch, and the tidy releases crew's landing places through sluice (`plan.8`, `plan.16`, `plan.19`). So crew talks to sluice directly, an agent runs every landing, and two tools drive one landing. That path named a submission by a number that was not sluice's and read it from another queue (signal `2026-11-07-agentplot-ops-38152130/01`), and levelled a host's main checkout after a landing, which nothing of crew's may do (signal `2026-11-07-agentplot-ops-b785032d/01`). The user asked that the retrofit be planned (signal `2026-11-07-chuck-deneb-809395f6/01`).

Record 0056, rewritten and accepted by the user on 2026-11-08 ("Yes, that's it. Rewrite the record that way"), decides it: crew is the control plane and talks only to Boomdrive's runner; a bolt is work crew hands the runner; the user's send of a bolt's row is one message, `land`, which the runner carries out with Flume and sluice; crew learns what happened only from the runner's report; and nothing of crew's lands anything. The runner now takes `land` and carries a bolt as a launch (agentplot/boomdrive `bolt/the-runner-lands-on-a-land-message`, #53). This change builds record 0056's points 1 to 5 for a bolt, and its decision 6's `land` for a fix of main too.

## What Changes

- **crew ships a Flume kind, `crew/bolt@1`**: `plugin/flume/kinds/bolt@1/kind.toml`, a kind that lands with no stages, its branches `bolt/<bolt>`. crew's follower and a main-level start put it in crew's kinds folder.
- **`crew bolt start` launches the bolt's base place** to the runner, then each unit's and chore's launch on `bolt/<bolt>` as today. It makes no branch, reads no host and runs no sluice. Run again on a bolt whose launch the runner refused, it launches the bolt anew.
- **The user's send posts `land`.** The act of crew's that reads the user's send on a kit's landings card posts one `land` request for each row it lands, in the card's order, a fix of main's row among them, once per send and head, recorded with its request's number. No agent runs anything for it, and the user's words in ops's pane are no longer a word to land.
- **`crew bolt submit` and `crew main fix --send` land nothing.** Each refuses at once, naming the card's send as the way.
- **A landing's outcome comes from the runner's report.** The base place's status as the runner carries it says asked, submitted, landed with its commit, refused for a failed check or a conflict, or stopped. The first act of crew's that reads it records it: a landing closes the bolt; a failed check holds its row for ops's fix; a conflict launches the take-main fix, the send standing for it; a stop keeps the row's box.
- **crew deletes no bolt branch and removes no landing worktree.** A drop drops the pieces' launches, then the bolt's. Flume tidies the base place and sluice ends its branch. The tidy runs no sluice and names any landing worktree left from before.
- **A bolt started before this release** has no base place: its row says it lands under the crew that started it, and no land is posted for it.
- **A test pins** that no crew command runs sluice, `wt` or `gh` for a bolt, or moves a checkout.
- **Removed:** `GIVE_READ`, `BOLT_CREATE`, `BOLT_FOUND`, `BOLT_DELETE`, `SUBMIT`, `QUEUE`, `WAIT`, `LANDED`, `LANDED_MARK`, `SUBMISSIONS`, `HISTORY`, `SUBMISSION_STATUS`, `PULL`, `PULL_MARK`, `LAND_COPIES`, the landing's waiter, `crew _landing-read`, the bolt-branch marks, and the leftovers `crew-calls-no-tool-but-its-runner` kept for crew's own landing.
- Main-level ops's brief, the planner's, the usage, README, the crew skill and CLAUDE.md say so.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `bolt-teams`: a bolt is a base place; the send is a land; the landing's outcome, hold, stop and close come from the runner's report; no landing worktree, waiter, pull-request mark or branch delete.
- `bolt-plan`: a bolt started, dropped and landed through the runner.
- `main-level`: ops's landing procedure is the user's send alone; a fix of main lands on the same send.
- `rail-cards`: a row's land, refusal and stop in the runner's and Flume's words; the card's read prints the lands posted.
- `crew-rail`: a fix of main's row is sent as a bolt's is.
- `crew-board`: a bolt's landing on its head line and in the bands from the runner's report.
- `drive-state`: a start does nothing on a host.
- `role-runs`: ops's run lands nothing.
- `run-record`: a land's entry names its request.
- `flume-source`: crew's kinds folder holds its bolt kind.
- `merge-gate`: a bolt's landing on main is the runner's submission through Flume.
- `review-batches`: no land is posted while a bolt's units wait on a batch the user has not answered.
- `board-page`: a word from the board lands nothing.

## Impact

- `plugin/flume/kinds/bolt@1/kind.toml` (new); `plugin/lib/source.py`.
- `plugin/lib/runner.py`: `REQUESTS`, `WORK`, `ACTS`, `request_refusal`, `bolt_launch`, `restart`, `lands_due`, `landing_of`, `base_drop_due`; `send_refusal` and `sent_of` folded into `lands_due`.
- `plugin/lib/plan.py`: `op_bolt_start`, `op_bolt_drop`, `bolt_submit`, `bolt_land`, `main_fix`, the landings card's raise and read, the landing's reads and records, the tidy; the sluice landing path removed.
- `plugin/lib/gather.py`, `plugin/lib/kit.py`, `plugin/lib/board.py`, `plugin/lib/record.py`, `plugin/hooks/status.js`, `plugin/bin/crew`.
- `plugin/roles/main-ops.md`, `plugin/roles/planner.md`, `plugin/roles/operator.md`, `plugin/skills/crew/SKILL.md`, README, CLAUDE.md.
- Tests: `tests/py/` (`test_runner.py`, `test_source.py`, `test_made.py`, `test_bolt_commands.py`, `test_stages.py`, `test_landings.py`, `test_landing.py`, `test_landing_state.py`, `test_bolt_submissions.py`, `test_pane_landing.py`, `test_card_commands.py`, `test_main_fix.py`, `test_send.py`, `test_record.py`, `test_tidy.py`, `test_rail.py`, `test_board.py`, a new `test_no_tool_for_a_bolt.py`), `tests/contract/test_recfix.py`, `tests/t-journey-land.sh`, `t-journey-main-fix.sh`, `t-flume-source.sh`, `t-briefs.sh`, `t-docs.sh`, `t-help.sh`, the stubs, `tests/moon.yml`, `plugin/tests/status.test.ts`.
- Other tools: none changes. A host locks `crew/bolt@1` and runs a runner that takes `land` before its crew pin moves to this release (design, *After deploy*).
