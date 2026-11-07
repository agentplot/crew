# Tasks

Each check is a moon task of the `tests` project, run through `tests/suite`: `logic` is `tests:logic`. Build the groups in order. Submit nothing, and never run `wt submit --help`.

## 1. A card whose role left the fleet is withdrawn

- [ ] 1.1 `cards.role_left` tells a card's owner that is a partition role whose label the teams file no longer has, and `cards.left_said` gives the withdrawal's words by the card's kind (design Decisions 1 and 3; Task notes 1.1). Passes `tests/py/test_rail.py` (`tests/suite logic`).
- [ ] 1.2 The rail's sweep judges each such card posted on this host, asks Pending You after it, withdraws it in its owner's name with those words and records the close, and a card in a former name cards no row, so the row is raised in its owner's name; a card of a standing role is left as it was (design Decisions 2 and 4; Task notes 1.2). Passes `tests/py/test_rail.py` (`tests/suite logic`).

## 2. The how-to

- [ ] 2.1 README's paragraph on the rail read's sweep names the withdrawal of a card whose role left the fleet (Task notes 2.1). Passes `tests/t-docs.sh` (`tests/suite t-docs`).

## 3. The tests the change affects

- [ ] 3.1 Verify `tests/suite --affected` ends with "0 failed".
