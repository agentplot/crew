# Tasks

## 1. Another host asked only when something there could have moved

- [x] 1.1 The follower stamps this host's kits and readings in its own process at each refresh and asks another host only when a branch of a partition with work there or that host's runner's branch moved, a watch of its kit printed or ended, it did not answer last, or ten minutes passed, a host not asked counting as unmoved, and asks a host's routes and its unwatched overviews only at a tick that asks it (design, Decision 1; Task notes 1.1); passes `tests/py/test_board.py`, `tests/suite logic` ending with "0 failed".

## 2. Pending You and herdr asked only when the cards could have moved

- [x] 2.1 At a tick the follower asks Pending You after the cards and herdr after their askers only for one it has not answered, a failed bridge or unread asker, or ten minutes on, never with none to ask, and a card its sweep left counts the cards as moved at the next ask and not at each tick (design, Decision 2; Task notes 2.1); passes `tests/py/test_board.py`, `tests/suite logic` ending with "0 failed".

## 3. One fetch for each repository

- [x] 3.1 The clock fetches each repository once with every branch it reads of it, a branch not yet made costing one fetch more (design, Decision 3; Task notes 3.1); passes `tests/py/test_board.py` and `tests/contract/test_git.py`, `tests/suite logic contract` ending with "0 failed".

## 4. One overview watch for each repository

- [x] 4.1 The follower keeps one overview watch for each repository on a host, two checkouts of one repository on this host sharing it, its line and its end each kit's of it (design, Decision 4; Task notes 4.1); passes `tests/py/test_board.py`, `tests/suite logic` ending with "0 failed".

## 5. A runner's report is a move

- [x] 5.1 The look stamps each partition's runners' branches, and one moved, made or gone reads that partition again (design, Decision 5; Task notes 5.1); passes `tests/py/test_board.py`, `tests/suite logic` ending with "0 failed".

## 6. The quiet tick, and the words

- [x] 6.1 A tick after nothing moved, every card answered, starts nothing but one fetch of each repository: no other git, no gather, no ssh, no sluice, no Pending You, no herdr and no portless (design, Decisions 1 to 3; Task notes 6.1); passes `tests/py/test_board.py` and `tests/suite t-journey-board` ending with "0 failed".
- [x] 6.2 README, the crew skill, crew's usage and `board.py`'s header say the follower fetches each repository once, asks another host, Pending You or herdr only when something there could have moved, and follows each repository's queue through one watch (design, Task notes 6.2); passes `tests/suite t-docs` ending with "0 failed".
- [x] 6.3 The tests the change affects pass: `tests/suite --affected` ends with "0 failed".
