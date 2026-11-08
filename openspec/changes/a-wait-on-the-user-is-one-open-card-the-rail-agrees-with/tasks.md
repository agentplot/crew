# Tasks

Each pytest check runs from `tests/.venv`, synced by `devenv shell -- moon run tests:venv` (design, *Task notes*).

## 1. The user's answer is a recorded card act

- [x] 1.1 crew records one `card.answer` per card, on its object in its owner's name, with `Card`, `Key`, `Answer` in crew's words and, for a kit's landings card, `Heads` of the ticked bolts, and `record.py`'s docstring names the act (design, Decision 1; Task notes 1.1). Verify `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_card_commands.py` passes.
- [ ] 1.2 A landings card's raise and `crew card read` record the answer when they read the card answered, once (design, Decision 1; Task notes 1.2). Verify `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_landings.py tests/py/test_card_commands.py` passes.
- [ ] 1.3 The rail's sweep reads each owner's pending list in its one bridge, open record cards among what it asks after, and records the answer of each card it finds answered (design, Decision 2; Task notes 1.3). Verify `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_rail.py` passes.

## 2. An answered card is closed and keeps its send

- [ ] 2.1 A card the user answered is acked and recorded closed whether its close gives an outcome or only a reason, and a card still waiting is withdrawn as before (design, Decision 4; Task notes 2.1). Verify `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_cards.py` passes.
- [ ] 2.2 Every close of an answered kit's landings card carries the ticked bolts as `Heads`, and a raise that reads its card ended in Pending You records it closed with its answer and send and posts with no row for a bolt the send still lands (design, Decision 4; Task notes 2.2). Verify `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_landings.py` passes.
- [ ] 2.3 The sweep leaves an answered landings card open, said as waiting on ops, while a bolt it ticked has neither landed nor been dropped, though the kit's row is gone (design, Decision 5; Task notes 2.3). Verify `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_rail.py` passes.

## 3. A closed card leaves the rail

- [ ] 3.1 A card the sweep finds ended in Pending You is recorded closed or withdrawn on that read, sending Pending You nothing, and a row that still waits is then a row with none (design, Decision 5; Task notes 3.1). Verify `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_rail.py` passes.
- [ ] 3.2 A card Pending You refuses to its recorded owner as another assistant's is lost to that owner, posted again in the owner's name while its row waits and by nobody once its row is gone (design, Decision 6; Task notes 3.2). Verify `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_cards.py tests/py/test_rail.py` passes.
- [ ] 3.3 A row's card line names the one card open in the row owner's name, each other card under its key is named apart as not the row's, and a stray card whose close was refused is listed with the refusal's words (design, Decision 7; Task notes 3.3). Verify `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_rail.py` passes.

## 4. The rail says what each card waits on

- [ ] 4.1 A row's answered card says when and what was answered and the owner's act it waits on, and answered questions, record cards and left landings cards are listed under answered cards waiting on their askers, not among what waits on the user (design, Decision 3; Task notes 4.1). Verify `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_rail.py` passes.
- [ ] 4.2 Each bolt's line on a kit's land row says whether its card carries, holds or follows it, and a bolt that can't land and is no row of the card says nothing of it (design, Decision 8; Task notes 4.2). Verify `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_rail.py` passes.
- [ ] 4.3 On the stub pendingyou, `crew rail`'s sweep records a steered answer once and the row's card line says it waits on the planner, with one `list_pending` in the planner's name, and `t-cards.sh`'s other expectations follow the new reads (design, Decisions 2 and 3; Task notes 4.3). Verify `tests/suite t-cards` ends with "0 failed".

## 5. A bolt's time and the agents' bands

- [ ] 5.1 A card holds a bolt for the user only until its answer or close, a kit's landings card only while its rows name the bolt, and a main-level question only when its post names the bolt or its work (design, Decision 8; Task notes 5.1). Verify `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_bolt_time.py` passes.
- [ ] 5.2 The board's cards and markers carry the answer, an agent's band says an answered card is answered and theirs to act on, and ops's land line says the landing is its own (design, Decision 3; Task notes 5.2). Verify `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_board.py` passes.
- [ ] 5.3 crew's mod draws an answered card's line above ops's view as the views give it (design, Decision 3; Task notes 5.3). Verify `tests/suite mod` ends with "0 failed".

## 6. The command's words

- [ ] 6.1 README's *Operations*, the crew skill's `crew rail` row and `crew`'s usage header say what the rail now says of answered cards, one card per row and each bolt's card stand, and that the sweep records answers and ended cards (`docs.2`; Task notes 6.1). Verify `tests/suite t-docs` ends with "0 failed".
