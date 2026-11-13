# A kit's landings card is raised whatever its rows

## Why

On deneb, from 2026-11-11T23:09Z to 2026-11-12T01:17Z, crew posted no landings card for boomdrive. Seven proven bolts, then eight, waited on boomdrive's main. Every post of `land/boomdrive` was refused, eleven minutes apart: "Pending You refused post_request: With questions, each question carries its own highStakes; leave the card’s highStakes out." The user had no card to send them on (signal `afterthought/crew-state:agentplot/main signals/2026-11-12-agentplot-ops-6907cc32/01-land-boomdrive-card-refused-by-pending-you`).

crew 0.59.0 already built the card as those words ask. `cards.landings_card` made more than five rows into lists of questions, each carrying its own `highStakes` and the card none (fix 6f6ff0fe, `tests/py/test_landings.py`). Pending You's guide (revision 2.60) documents that shape. Pending You refused it all the same.

What Pending You has taken, read from the run records of three drives:
- an approval of risk high, the landings card of one row, many times a day;
- one list of up to five boxes carrying `highStakes` on the card: boomdrive's two rows at 2026-11-11T21:25Z, switchboard-kit's four at 2026-11-10T19:40Z;
- a card of questions carrying no `highStakes` anywhere: agentplot-design's two questions at 2026-11-11T21:31Z.

No card of questions carrying `highStakes` has ever posted. The fix of 2026-11-10 was proven only against crew's stub, which refuses a card's own `highStakes` beside questions and takes it on each question. Pending You does not.

A landing cannot be undone, so its card must carry `highStakes` (record 0031 §5). Pending You takes that only on one list, and a list holds five boxes at most (`post_request`'s and `update_request`'s `options`, read 2026-11-12). Lists of questions also stop at four questions, twenty rows. So a card that gives every row a box cannot hold every count of rows in a form Pending You takes.

## What Changes

- **A kit's landings card asks no questions.** One row is the approval of risk high, as today. Two or more rows are one list of boxes carrying `highStakes` on the card, whatever their number. The lists form goes.
- **The list holds five boxes, and the rest wait on its face.** With more than five rows, five get boxes: first the rows crew would tick, then the others, each in the rows' order. Every row stays on the card's face in its place, each row's paragraph as before. A row without a box is marked as waiting for one. The summary says how many wait and that the card that follows the send asks for them.
- **A row without a box is recorded so.** The card's post and change record it in their `Heads` with the mark `:next`, beside `:main` and `:left`. So a raise reads which rows had boxes, and a row coming to a box or losing one changes the waiting card in place with a note naming it. The card is followed only when its form changes, between the approval and the list.
- **The send's card follows at once.** When the user sends a card that had rows waiting, crew closes it and posts the card that follows straight away, asking for every row the send does not land. A row that waited for a box is never counted among those the user left. A row the user left stays left when it waits for a box. The close names the rows that had no box, and the card that follows says they wait on it.
- **The stub Pending You and the logic tier's fake refuse what Pending You refused:** a card of questions carrying `highStakes`, on the card or on any question, in Pending You's words (`tests.4`).
- **main-level ops's brief and README say a row with no box waits for the card that follows the send.**

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `rail-cards`: a kit's landings card is always an approval or one list carrying `highStakes`, never questions. Its list holds five boxes, and the rest of its rows wait on its face, recorded as having none. A row coming to a box or losing one changes the waiting card in place. A send with rows waiting is followed at once by a card asking for them. A deploy's card is now the one crew card whose questions carry `highStakes`.

## Impact

- `plugin/lib/cards.py`: `BOXES`'s source, `landings_form`, a new decision `landings_boxed`, `landings_card`, `row_paragraph`.
- `plugin/lib/plan.py`: `card_heads`, `heads_taking`, a new `heads_next`, `offered_boxes`, `kit_card_state`, `landings_step`, `left_now`, `landings_since` and its caller.
- `tests/stubs/pendingyou`: refuses a card of questions carrying `highStakes` anywhere.
- `tests/py/test_cards.py`, `tests/py/test_landings.py`: the cases.
- `plugin/roles/main-ops.md` and `tests/t-briefs.sh`: one sentence and its pinned phrase.
- `README.md`: the landings card's form.
- No change to the views or crew's mod (`code.8`): no bolt, unit, stage, card key or rail row changes shape. A row's place on its card is the card's, not the row's.
