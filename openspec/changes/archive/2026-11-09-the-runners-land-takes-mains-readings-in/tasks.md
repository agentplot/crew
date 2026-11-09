# Tasks

Each check is a moon task run through `tests/suite`. Submit nothing: Flume submits the place once its last stage delivers.

## 1. Both readings hold

- [x] 1.1 `crew bolt land` closes a started bolt once the runner reports it landed, or once its kit's main holds its landing with each piece read landed through it, and is refused otherwise, naming the runner's report or the piece (design, Decision 1; Task notes 1.1). Verify `tests/suite logic` ends with "0 failed".
- [x] 1.2 `bolt/<bolt>` serves the bolt's base place and a landings row's preview, a launch of it of any kind but `crew/bolt` refused (design, Decision 2; Task notes 1.2). Verify `tests/suite logic` ends with "0 failed".
- [x] 1.3 A bolt's run on the stubs asks its preview of the runner and closes a bolt at the landing main holds (design, Decisions 1 and 2; Task notes 1.3). Verify `tests/suite t-journey-land` ends with "0 failed".
- [x] 1.4 Verify `tests/suite --affected` ends with "0 failed".
