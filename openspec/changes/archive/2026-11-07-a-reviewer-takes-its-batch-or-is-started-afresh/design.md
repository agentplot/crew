# Design: a reviewer takes its batch or is started afresh

## Context

The proposal gives madswan's cases of 2026-10-26. Rules this change relies on: `teams.15`, under which every first message, the reviewer's batch among them, is sent once the agent accepts input, read back, sent once more and reported not taken when the second sending is not taken either; `teams.2`, under which a working agent is ended only with `--force`; `teams.7`, under which the reviewer's batch is its one first message; `read.1`, under which what crew cannot read is refused, never guessed; `code.7`, which makes the decision a function of facts; `roles.4`, whose details already leave a stage's prompt unmarked, as the batch is today; `docs.2`; `tests.4`, `tests.11` and `tests.12`, which put each decision in the logic tier and the wiring in one end-to-end case per command. It touches the areas of `plan.md` (`plugin/lib/plan.py`), `teams.md` (`plugin/bin/crew`), `briefs.md` (`plugin/skills/`), `tests.md` (`tests/`) and `docs.md` (`README.md`, `openspec/`). It departs from no rule, and edits no rule page: `teams.15` already names the reviewer's batch and the chore that builds it.

The family: Flume runs a role's run as a place and owns its delivery when a partition runs its reviewer as its kind (`review_asked`), so nothing here reaches that path; the standing reviewer is crew's alone until the move that retires it (`roles.5`). The way a first message is sent has one owner in crew, `crew.send_taken`, which this change calls and does not copy.

## Decisions

### Decision 1: the batch goes through `send_taken`, and its outcome is the start's

`review_cmd` calls `crew.send_taken(fleet, "<label>-reviewer", <batch>)` in place of `herdr agent prompt`. Its three outcomes:

- **taken**: `review.start` recorded as today, and "is reviewing batch N".
- **never** (not taken twice, or never ready, nothing typed): `send_taken` has cleared the input with Ctrl+C; `review.start` is recorded with `Refused` in `untaken_said`'s words ("<label>-reviewer did not take batch N, sent twice; nothing is left typed"), and the command refuses with those words and the way on, "once it is idle, crew review <label> ends it and starts the batch's reviewer afresh" (Decision 3). The reviewer is left up: ending it is the next start's, which reads it afresh.
- **unread** (crew cannot tell whether it took it): nothing more is sent. `review.start` is recorded, since a reviewer that did take it writes its summary, which `--wait` must find; the command says what it could not read and that the next `crew review` starts afresh a reviewer that sits idle having taken none. Recording it refused would lose a batch the reviewer took; recording nothing would leave `--wait` waiting on the batch before.

Considered: a second sending path in `plan.py` with its own read-back, which the brief rules out, and marking the batch `[crew]`, which `teams.7` and the journey's case that the reviewer is not greeted leave unmarked.

### Decision 2: a refused start is no batch

`review_start` numbers a batch past every start and batch recorded, now leaving out a refused start, so the start that follows takes the same number and no batch number is spent on a batch nobody read. `review_wait` reads the newest start, refused or not: a refused one refuses the wait, naming `crew review <label>`, where it would otherwise return the batch before.

### Decision 3: whether an up reviewer is started afresh is a decision of facts

`reviewer_up_said(label, agent, status, asking, took, written)` decides, starting nothing (`code.7`):

- **afresh** when herdr reads it idle or done, no question is open, its session received no batch, and no summary was written since its last start: nothing of a batch is lost by ending it.
- **refused, waiting on a question** when herdr reads it blocked, or crew's question mark is open.
- **refused, still reviewing** when it is at work, took its batch, or a summary is written since its last start: the wait ends it at its summary. `crew review` takes no `--force`, so a working reviewer is never ended by it (`teams.2`).
- **refused, can't tell** when whether it took a batch is unread (`read.1`).

`reviewer_up` reads the facts: herdr's status and the question mark through `crew.Pane.reading`, as `send_taken` reads them; whether its session took a batch from its transcript, `crew.Pane.received(<session>, 0, "Review batch")`, the words every batch opens with (`REVIEW_OPENS`, which `review_prompt` uses), since a standing reviewer is started fresh for each batch and its batch is its one prompt (`teams.7`); and whether the batch file of its last start on this host, refused or not, was written since that start (`batch_written`). A session crew finds no id for is unread. Reading the transcript rather than the run record covers a reviewer started by a crew that recorded its start unread, or before this change, as madswan's batch 28 was.

`review_cmd` decides before the main level's check and the batch's reading, and ends an afresh reviewer only once `review_start` has found a batch due, so a refused command ends nothing. The end is `Agents.stop`, which fails rather than lies (`teams.2`), recorded as `review.end` on the reviewer and said in the decision's words; the reviewer is then started in the same pane. `--wait` on an afresh reviewer refuses, naming `crew review <label>`, and ends nothing.

## After deploy

None. Every case is held by the logic tier and by `t-journey-review` on the stubs; what deneb runs is swancloud's pin of `teamless/deneb`, not a step of this change.

## Task notes

**1.1** `plugin/lib/plan.py` `review_cmd`: `crew.send_taken` in place of `herdr agent prompt`; `untaken_said` for the refusal; `review.start` with `refused`. `review_start`: a refused start left out of the numbering. `review_wait`: the newest start, refused, refuses. End to end: `tests/t-journey-review.sh` at batch 3, the stub's `stub leave wldn-reviewer 2` with `CREW_TAKEN_WITHIN=1`: the refusal's words, two sendings and two Ctrl+Cs, nothing left typed, the refused entry, and `--wait` refused; batch 1's sent once.

**1.2** `plugin/lib/plan.py` `reviewer_up_said`, `reviewer_up`, `REVIEW_OPENS`, `review_prompt`. Logic: `tests/py/test_review.py` `TestAReviewerUp`: idle and done afresh; at work, took its batch, a summary written: still reviewing; blocked or a question open; unread; the prompt's opening. End to end: `t-journey-review` at batch 3 after the refusal, `stub leave wldn-reviewer 1`: crew review ends the reviewer by `/exit`, says so, records `review.end`, starts it afresh and sends batch 3 twice, taken at the second.

**1.3** README's batches paragraph, the crew skill's main-level paragraph and `crew`'s usage header for `crew review`.
