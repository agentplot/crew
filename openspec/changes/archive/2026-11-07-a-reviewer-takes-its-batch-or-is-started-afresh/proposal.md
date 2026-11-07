# A reviewer takes its batch or is started afresh

## Why

On 2026-10-26 madswan's batches 17 and 19 sat with the reviewer's prompt typed in its pane and never submitted, until the planner pressed Enter (signal `afterthought/crew-state:swancloud/main signals/2026-10-26-swancloud-operator-24752329/01-reviewer-prompt-typed-but-not-submitted`). `review_cmd` sends the reviewer its batch with `herdr agent prompt` and reads nothing back (`plugin/lib/plan.py` at `teamless/deneb` edad39a0), where every other first message goes through `crew.send_taken`; `teams.15`, amended that day, already names the reviewer's batch among the first messages that are taken or sent again.

The same day madswan's batch 28 reviewer sat idle with an empty input box, and `crew review madswan` refused twice, "madswan-reviewer is still reviewing a batch: crew review madswan --wait waits for its summary", until the pane was closed by hand (signals `afterthought/crew-state:swancloud/main signals/2026-10-26-swancloud-operator-58c1aadc/01-crew-review-force-does-not-end-a-promptless-reviewer` and `afterthought/crew-state:madswan/main signals/2026-10-26-madswan-planner-d7b6d29c/01-crew-review-force-does-not-end-a-promptless-reviewer`). `review_cmd` refuses whenever herdr reads the reviewer up, whatever it is doing, so a reviewer that never took its batch blocks every batch after it.

This fix carries the planner's two chores `a-reviewers-prompt-is-taken-or-sent-again` and `crew-review-ends-an-idle-reviewer-that-took-no-batch`, both `review_cmd`'s start of the reviewer.

## What Changes

- **The batch is taken or sent again.** `crew review <label>` sends the standing reviewer its batch through `crew.send_taken`, as every other first message is sent: once the reviewer accepts input, read back from its transcript, sent once more when not taken. Taken at neither sending, what was left typed is cleared, the start is recorded refused (`review.start` with `Refused`) and the command refuses, naming `crew review <label>` as the way on. A sending crew cannot read is recorded started and said, nothing more typed.
- **A refused start is no batch.** The next start takes its number, and `crew review <label> --wait` after it refuses, naming `crew review <label>`.
- **An idle reviewer that took no batch is started afresh.** `crew review <label>` that finds the reviewer up, idle or done, at no question, its session holding no batch and no summary written since its last start, ends it, records the end (`review.end`), says so and starts the batch's reviewer afresh. One at work, at a question, or that took its batch is refused as today; one crew cannot read is refused naming what it could not read. `crew review <label> --wait` on a reviewer that took no batch refuses, naming `crew review <label>`.
- README, the crew skill and `crew`'s usage header say this (`docs.2`).

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `review-batches`: "The planner starts the partition's reviewer" gains the batch taken or sent again and the idle reviewer that took no batch started afresh.

## Impact

- `plugin/lib/plan.py`: `review_cmd`, `reviewer_up_said`, `reviewer_up`, `REVIEW_OPENS`; `review_start`'s numbering; `review_prompt`'s opening; `review_wait`'s refused start.
- README, `plugin/skills/crew/SKILL.md`, `plugin/bin/crew`'s usage header.
- Tests: `tests/py/test_review.py` (`TestAReviewerUp`); `tests/t-journey-review.sh`.
- Nothing crew models changes: `review.end` is a run-record act no view reads, so the board, the views and the mod are untouched (`code.8` not reached). No new module or import (`code.1`).

## Touches

```
plugin/lib/plan.py
plugin/bin/crew
README.md
plugin/skills/crew/SKILL.md
tests/py/test_review.py
tests/t-journey-review.sh
```
