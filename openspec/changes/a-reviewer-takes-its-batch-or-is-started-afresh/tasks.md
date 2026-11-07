# Tasks

## 1. A reviewer takes its batch or is started afresh

- [x] 1.1 `crew review <label>` sends the standing reviewer its batch through `crew.send_taken`, and a batch taken at neither sending leaves nothing typed, its start recorded refused, the command refused naming `crew review <label>`, the next start taking its number and `--wait` refused after it (design, Decisions 1 and 2; Task notes 1.1). Verify `tests/suite t-journey-review` ends with "0 failed".
- [x] 1.2 `crew review <label>` ends a reviewer up, idle or done, at no question, that took no batch and wrote no summary since its last start, records the end, says so and starts the batch's reviewer afresh, refuses one at work, at a question, that took its batch or whose taking it can't read, and `--wait` on one that took no batch refuses naming `crew review <label>` (design, Decision 3; Task notes 1.2). Passes `tests/py/test_review.py` (`tests/suite logic`), and verify `tests/suite t-journey-review` ends with "0 failed".

## 2. The docs and the change's tests

- [x] 2.1 README, the crew skill and `crew`'s usage header say the batch is taken or sent again and an idle reviewer that took no batch is started afresh (`docs.2`; Task notes 1.3). Verify `tests/suite t-docs` ends with "0 failed".
- [ ] 2.2 The tests the change affects pass. Verify `tests/suite --affected` ends with "0 failed".
