# Tasks

## 1. A held fix of main on its kit's landings card

- [x] 1.1 Each fix of the kit's main whose code has delivered and whose submission waits held is a box of the kit's landings card ahead of its bolts, named by its place and shown at its launch's number, forecast against nothing, the card raised for it with no bolt beside it, a lone fix an approval (design, Decisions 1 and 5). Passes `tests/py/test_landings.py` (`tests/suite logic`).
- [x] 1.2 A ticked fix stands on the send while it waits held, sent or not, the close saying whether it was sent or dropped; a cleared one is left on the card that follows; one an earlier send ticked is no row of a card that follows while it waits held at that launch (design, Decision 2). Passes `tests/py/test_landings.py` (`tests/suite logic`).
- [x] 1.3 `crew card read land/<kit>` gives each ticked fix, on the card or on an earlier send, as `crew main fix <kit> <name> --send` ahead of the bolts' submit (design, Decision 3). Passes `tests/py/test_landings.py` and `tests/py/test_card_commands.py` (`tests/suite logic`).
- [x] 1.4 An answered card that ticked a fix waits on ops until the fix's send or drop is recorded (design, Decision 4). Passes `tests/py/test_landings.py` (`tests/suite logic`).

## 2. The docs and the change's tests

- [x] 2.1 README, the crew skill, `crew`'s usage header and ops's brief say the card carries a held fix of main and the read gives its command (`docs.2`, `tests.6`). Verify `tests/suite t-docs t-briefs` ends with "0 failed".
- [x] 2.2 The tests the change affects pass. Verify `tests/suite --affected` ends with "0 failed".
