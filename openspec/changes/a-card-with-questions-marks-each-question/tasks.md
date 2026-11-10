# Tasks

Each check is a moon task of the `tests` project, run through `tests/suite`: `logic` is `tests:logic`. Submit nothing, and never run `wt submit --help`.

## 1. A card of questions marks each question

- [ ] 1.1 A kit's landings card of six or more rows and a deploy's card of more than five boxes carry `highStakes` on each question and none on the card, and a card of one list carries it on the card (design Decision 1; Task notes 1.1). Passes `tests/py/test_cards.py` and `tests/py/test_ops.py` (`tests/suite logic`).
- [ ] 1.2 Six proven bolts raised on a Pending You that refuses a card's `highStakes` beside questions post one card of two lists, each carrying it, and nothing is refused (design Decision 1; Task notes 1.2). Passes `tests/py/test_landings.py` (`tests/suite logic`).
- [ ] 1.3 The stub Pending You refuses a post of questions carrying the card's `highStakes` in Pending You's words (`tests.4`; design Decision 2; Task notes 1.3). Verify `tests/suite t-cards t-journey-land t-journey-ops` ends with "0 failed".

## 2. The tests the change affects

- [ ] 2.1 Verify `tests/suite --affected` ends with "0 failed".
