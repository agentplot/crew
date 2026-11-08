# Tasks

## 1. A sent-back landing reads as the bolt's fix

- [x] 1.1 A refusal sluice made for the bolt's own content stands at its head through every later submit that submitted nothing there, and no reader says a stop over it (design, Decision 1; Task notes 1.1). Passes `tests/py/test_landing.py` and `tests/py/test_landings.py` (`tests/suite logic`).
- [x] 1.2 `crew bolt submit` submits nothing at a head sluice sent back, naming what failed from sluice's record and the way on, the take-main fix crew launches or a failed check's `crew fix` with its words (design, Decisions 2 and 3; Task notes 1.2). Passes `tests/py/test_landing.py` (`tests/suite logic`); verify `tests/suite t-journey-land` ends with "0 failed".
- [x] 1.3 A landing sluice sends back for a failed check tells ops the fix's command, named and worded from sluice's record, never to submit again as it is (design, Decision 3; Task notes 1.3). Passes `tests/py/test_landing.py` (`tests/suite logic`).
- [x] 1.4 The landings card's row, the rail's land line and `crew bolts` read the sent-back landing as rejected and open for work through a submit that submitted nothing, as `landing_phase` and `refusals` read it from `sent_back` (design, Decision 4; Task notes 1.4). Passes `tests/py/test_landings.py` and `tests/py/test_landing.py` (`tests/suite logic`).

## 2. The docs and the change's tests

- [x] 2.1 README, the crew skill and `crew`'s usage header say a sent-back landing is the bolt's fix (`docs.2`; Task notes 2.1). Verify `tests/suite t-docs` ends with "0 failed".
- [x] 2.2 The tests the change affects pass. Verify `tests/suite --affected` ends with "0 failed".
