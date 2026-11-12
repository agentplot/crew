# Tasks

Each check is a moon task of the `tests` project, run through `tests/suite`: `logic` is `tests:logic`. Submit nothing, and never run `wt submit --help`.

## 1. The rail's read raises a landings card that does not show a row as it stands

- [ ] 1.1 Each bolt on a kit's land row carries its head now (design Decision 3; Task notes 1.1). Passes `tests/py/test_rail.py` and `tests/py/test_kit_rename.py` (`tests/suite logic`).
- [ ] 1.2 `plan.unoffered` gives the rows that can land, held by no send, that the open card shows on no row, at another head, taking main first, or, once answered, with no box (design Decision 1; Task notes 1.2). Passes `tests/py/test_landings.py` (`tests/suite logic`).
- [ ] 1.3 The rail's read raises each landings card that does not show a row as it stands, once, so a bolt proven between a send and its landing gets its card in the same sweep, and a card showing every row as it stands is raised by none (design Decisions 1 and 2; Task notes 1.3). Passes `tests/py/test_landings.py` and `tests/py/test_rail.py` (`tests/suite logic`).
- [ ] 1.4 `crew rail` names each card it raised for rows it did not offer, with the rows, or its raise's refusal (design Decision 1; Task notes 1.4). Passes `tests/py/test_rail.py` (`tests/suite logic`).

## 2. The words

- [ ] 2.1 README, the crew skill and `crew rail`'s usage say the rail's read raises a landings card that does not show a row as it stands, a bolt proven since the user's send offered at once on a card following theirs (`docs.2`; Task notes 2.1). Verify `tests/suite t-docs` ends with "0 failed".

## 3. The tests the change affects

- [ ] 3.1 Verify `tests/suite --affected` ends with "0 failed".
