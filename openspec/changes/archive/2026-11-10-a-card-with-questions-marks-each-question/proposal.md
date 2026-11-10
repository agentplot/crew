# A card with questions marks each question

## Why

On the Willdan box, on 2026-11-10, crew 0.41.11 could not post `land/<kit>` for six proven Switchboard bolts. Pending You refused every post: "With questions, each question carries its own highStakes; leave the card's highStakes out." The six bolts waited about nine hours with no card (signals `2026-11-10-wldn-ops-6352d0d6/01` and `2026-11-10-wldn-operator-9599d7fa/01` on WilldanGroup/crew-state `wldn/main`).

The cause is in `plugin/lib/cards.py`. Past `BOXES`, five rows, `landings_card` asks its rows as lists, each a question, and still passes `highStakes=True` to `built`, which puts it on the card beside the questions. Rows taking main first count toward the six. `deploy_card` does the same once a deploy waits on five or more open steps, five boxes and the deploy's. `tests/py/test_cards.py` asserted a seven-row card carries both, which locked the defect in, and the stub Pending You took such a card.

## What Changes

- **A card of questions carries `highStakes` on each question and none on the card.** The landings card of six or more rows and the deploy's card of more than five boxes each mark every list. A card of one list carries it on the card, as before.
- **The tests assert it.** The seven-row case asserts each list carries `highStakes` and the card none, the five-step deploy case the same, and a raise of six proven bolts posts through a Pending You fake that refuses a card's `highStakes` beside questions in its words.
- **The stub Pending You refuses such a post** in Pending You's words (`tests.4`).

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `rail-cards`: a card of questions carries `highStakes` on each question and none on the card; a landings card of six or more rows is lists, each carrying it.

## Impact

- `plugin/lib/cards.py`: `landings_card`, `deploy_card`, and their docstrings and `landings_form`'s.
- `tests/py/test_cards.py`, `tests/py/test_ops.py`, `tests/py/test_landings.py`: the cases.
- `tests/stubs/pendingyou`: refuses a post of questions carrying the card's `highStakes`.
- No change to the views or crew's mod (`code.8`): no bolt, unit, stage, card key or rail row changes shape.
