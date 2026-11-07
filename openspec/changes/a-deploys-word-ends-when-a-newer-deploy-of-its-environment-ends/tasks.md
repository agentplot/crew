# Tasks

Each check is a moon task of the `tests` project, run through `tests/suite`: `logic` is `tests:logic`. Submit nothing, and never run `wt submit --help`.

## 1. A word ends at its own deploy's end or a newer one's

- [x] 1.1 A deploy's word ends at the end of its own deploy or of a newer one, started after the word was given, whatever its outcome, and stands through the end of a deploy running when it was given or one with no start (design Decisions 1 and 2; Task notes 1.1). Passes `tests/py/test_ops.py` (`tests/suite logic`).
- [x] 1.2 An approved deploy not started whose word a newer deploy's end spent is `replaced`, `spent` naming that deploy, as `state` reads the word at every point (design Decision 4; Task notes 1.2). Passes `tests/py/test_ops.py` (`tests/suite logic`).
- [x] 1.3 The end that spends a word closes its `deploy/<env>` card, naming the newer deploy and the head the user approved, and an end that spends none closes nothing (design Decision 3; Task notes 1.3). Passes `tests/py/test_ops.py` (`tests/suite logic`).
- [x] 1.4 The board, the page and the rail's sweep follow the spent word: the board and the page name the newer deploy, main-level ops's view leaves the deploy out, and the sweep no longer leaves the card (design Decision 4; Task notes 1.4). Passes `tests/py/test_board.py`, `tests/py/test_page.py` and `tests/py/test_rail.py` (`tests/suite logic`).

## 2. The tests the change affects

- [x] 2.1 Verify `tests/suite --affected` ends with "0 failed".
