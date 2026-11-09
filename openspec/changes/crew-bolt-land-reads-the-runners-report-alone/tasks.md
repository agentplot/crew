# Tasks

Each check is a moon task run through `tests/suite`. Submit nothing: Flume submits the place once its last stage delivers.

## 1. crew bolt land reads the runner's report alone

- [ ] 1.1 `crew bolt land` closes a started bolt only once the runner reports its base place landed, a record held for the runner among them, reads no kit, and refuses a bolt started before bolts were base places (design, Decisions 1 and 2; Task notes 1.1). Verify `tests/suite logic` ends with "0 failed".
- [ ] 1.2 A bolt whose branch GitHub deleted and whose places Flume tidied closes at Flume's commit from the records Flume holds for the runner (design, Decision 1; Task notes 1.2). Verify `tests/suite t-journey-land` ends with "0 failed".
- [ ] 1.3 merge-gate's verification cases cite "A head only a landing commit names" and the requirement's new name (design, Decision 3; Task notes 1.3). Verify `tests/suite logic` ends with "0 failed".
- [ ] 1.4 README, the skill and `crew`'s usage say `crew bolt land` reads no landing commit on main and refuses a bolt started before bolts were base places (design, Decisions 1 and 2; Task notes 1.4). Verify `tests/suite t-docs` ends with "0 failed".
- [ ] 1.5 Verify `tests/suite --affected` ends with "0 failed".
