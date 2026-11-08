# A held fix of main raises its kit's landings card

## Why

crew-rail's "A fix of main waits to land on its kit's row" has a fix of main whose code has delivered and whose submission waits held be a line of the kit's landings row, "ticked and sent as a bolt is", and main-level's "A fix of main lands on the user's send" has the user send it from the kit's landings card. The rail built the line; the card never carried it. On 2026-11-08 sluice's fix `main--handed-over-wait-holds-steady` was such a line, with "can land: agentplot-ops sends it with crew main fix sluice handed-over-wait-holds-steady --send", while the rail read "card:   land/sluice, none open" and no landings card was raised, since the card's rows were the kit's proven bolts alone and no bolt of sluice could land beside the fix (signal 2026-11-08-agentplot-ops-de90f199/01). The sweep asked the kit's raise for the row's card and the raise posted nothing, so the user had no card to send, and `crew card read land/sluice` had no way to say the fix's send.

## What Changes

- **A held fix of main is a box of its kit's landings card.** Each fix of the kit's main whose code has delivered and whose submission waits held for the user's send is a row of the card ahead of the bolts, `fix main--<name>`, ticked as crew proposes, saying what it is in the failure's first line and what its send does, forecast against nothing. The card is raised for it though no bolt can land beside it; a fix alone is the card's one row, an approval as a lone bolt's is.
- **Its send stands until its runner takes it.** A fix the user ticked is still to land on their send while it waits held, sent or not; the card is closed once it no longer does, saying it was sent on their word for its runner to submit, or dropped. A fix they cleared is left, shown unticked on the card that follows, and one an earlier send ticked is no row of a card that follows while it waits held at the same launch.
- **The read gives its command.** `crew card read land/<kit>` gives each fix the user ticked, on the card or on an earlier send while it waits held, as `crew main fix <kit> <name> --send`, ops's command for it, ahead of the bolts' submit.
- **ops's wait ends at its send.** An answered card that ticked a fix waits on main-level ops until its send or its drop is recorded, so the sweep closes it once its row is gone.
- README, the crew skill, `crew`'s usage header and ops's brief say the card carries the fix (`docs.2`).

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `rail-cards`: "A fix of main is a box of its kit's landings card" and "A ticked fix of main stands on the send while it waits held", added.
- `main-level`: "A fix of main lands on the user's send" says the read of the card gives its command.

## Impact

- `plugin/lib/plan.py`: `FIX_HEAD`, `fix_head`, `fix_rows`, `fix_send`, `item_named`, `fixes_went`, `fixes_shown`; `card_heads` reads a fix's head; `landings_raised`, `landings_step`, `landings_since`, `rows_unsent`, `landing_lines`, `landings_earlier`, `landings_unopened`, `card_read`, `send_waits`, `answered_waits`, `rows_previewed`, `main_fix_line`.
- `plugin/lib/runner.py`: `main_fixes_waiting` gives each fix's launch number; `main_fix_gone`.
- `plugin/lib/cards.py`: `fix_said`, `fix_then`, `fix_paragraph`, `fix_card`; `landings_card` draws a fix's row.
- README, `plugin/skills/crew/SKILL.md`, `plugin/bin/crew`'s usage header, `plugin/roles/main-ops.md`, `tests/t-briefs.sh`.
- Tests: `tests/py/test_landings.py`, `tests/py/test_card_commands.py`.
- The views keep their shape: ops's band lists the card among its cards as any, and its fixes in flight as before (`code.8` not reached). Nothing outside the standard library is imported (`code.1`).
