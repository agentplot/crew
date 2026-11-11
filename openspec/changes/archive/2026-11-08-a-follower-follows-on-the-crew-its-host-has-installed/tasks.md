# Tasks

## 1. A follower follows on the crew its host has installed

- [x] 1.1 A follower that runs a crew other than the one its host has installed starts again through the installed command before it reads, at its first refresh as at any later one, asking the installed crew once for each real path, never on a lag it can't read, and only once for a lag that survives its start (design, Decisions 1 to 3; Task notes 1.1). Passes `tests/py/test_board.py` (`tests/suite logic`).
- [x] 1.2 README, the crew skill and the usage of `crew _follow` and `crew _rail` say a follower follows only on the installed crew (`docs.2`; Task notes 1.2). Verify `tests/suite t-docs` ends with "0 failed".
- [x] 1.3 The tests the change affects pass. Verify `tests/suite --affected` ends with "0 failed".
