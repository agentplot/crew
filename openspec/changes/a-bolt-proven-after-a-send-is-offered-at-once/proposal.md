# A bolt proven after a send is offered at once

## Why

On wldn's drive, switchboard-kit bolts proven overnight waited 400 to 1055 minutes for a landings card (signal `2026-11-12-agentplot-planner-237b59c7/01` on afterthought/crew-state `agentplot/main`, from the landing timings read on chuck-herdr-alpha). One cause is a stale `batch.due` silencing the planner, which the fix `a-batch-due-is-decided-at-the-records-tip` takes. This is the other: a bolt that reads proven while its kit's landings card is open is offered by nothing.

What a raise of the card does with such a bolt is already decided. `plan.landings_step` closes an answered card, keeping the user's send for the bolts it still lands, and posts a card following it that asks for the new bolt; on a card that waits on the user it changes the card in place. But nothing raises the card when a bolt reads proven:
- No act of crew's is a bolt's proof. The rail reads it from the runner's report.
- The rail's read raises an open landings card only when main has moved under it (`landings_moved`) or when its sweep recorded the user's answer in that read (`landings_answered`).
- Otherwise a row with an open card is only asked after in Pending You (`sweep_judged`'s `held`).

So a bolt proven between the user's send and its landing waits until a bolt they ticked lands or main moves. One proven while the card waits on the user waits the same way, though its land line says the card that follows carries it.

## What Changes

- **The rail's read raises a landings card that does not show a row as it stands.** On the main level's host, each kit's landings card open in main-level ops's name is raised when its land row holds a row that can land, held by no send, that the card shows:
  - on no row;
  - at another head;
  - taking main first;
  - or, once answered, with no box.
- **A bolt proven since the user's send is offered in the same read**, on a card following theirs, as a send's rows that waited for a box are. The card they sent is closed keeping their send, which still lands what they ticked. A bolt proven while the card waits joins it.
- **A card that shows every row as it stands is raised by none of this.** A bolt the user left, at the head the card showed, is one such row. So an answered card with nothing proven since waits on its own landings, as before.
- **A land row's bolts carry their head now**, by which the read tells a row the card shows at another head.
- **`crew rail` names each card it raised so**, with its rows.
- **README, the crew skill and `crew rail`'s usage say so.**

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `rail-cards`: the rail's read raises a kit's landings card that does not show a row that can land as it stands. A bolt proven while an answered landings card waits on its landings is offered at once, on a card following it, the send kept.

## Impact

- `plugin/lib/plan.py`: `rail_rows` (each bolt's head on its land row), a new decision `unoffered`, a new `landings_unoffered`, `sweep_moved`, `rail_text`.
- `tests/py/test_landings.py`, `tests/py/test_rail.py`, `tests/py/test_kit_rename.py`: the cases.
- `README.md`, `plugin/skills/crew/SKILL.md`, `plugin/bin/crew`'s usage of `crew rail` (`docs.2`).
- No change to the views or crew's mod (`code.8`). The rail's land row gains its bolts' heads, which neither `board.agent_views` nor `status.js` reads. No bolt, unit, stage, card key or card changes shape.
