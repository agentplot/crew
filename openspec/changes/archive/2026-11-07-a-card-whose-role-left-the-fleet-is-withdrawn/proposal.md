# A card whose role left the fleet is withdrawn

## Why

On 2026-11-07 swancloud's partition is labelled `afterthought` in deneb's teams file, and its state branch, `afterthought/main` of afterthought/crew-state, carries on from `swancloud/main`. Its run record still holds cards crew raised in the old roles' names, open: `proposal/508` and batches 62 and 63 in `swancloud-planner`'s, two deploy cards in `swancloud-ops`'s. The deploy card of swancloud-srv's offer of b851ee6, req_2061e578985d4c8f8fb0, stood in `swancloud-ops`'s name, and Pending You refuses afterthought-ops's `whoami` with `previousName` swancloud-ops, so the user's yes on it reached nobody (signal `2026-11-07-agentplot-planner-2909addd/01-a-renamed-roles-card-reaches-nobody` on agentplot/main of afterthought/crew-state).

crew reads a card by its owner's name alone (`cards.card_under`), which is right: nothing maps a former name. But the rail's sweep closes a card only when its row is gone, so a card whose row stands under a name no partition has now is held as the row's card. It is never closed, and the row is never carded in a name that reaches someone. Record 0031 §1 has crew close each card at the event that ends it. A role leaving the fleet is such an event, and nothing acts on it.

## What Changes

- **The rail's sweep withdraws a card whose role left the fleet.** On each rail read, a card of crew's six (a proposal's, a batch's, a landings card, a deploy's, a step's, a record's) posted on this host in the name crew raises it in, `<label>-planner`, `<label>-ops` or `<label>-design`, whose label no partition of the teams file has now, is withdrawn on Pending You in its owner's name. Its partition was removed, or its label changed, which is a partition removed and another added: there is no renaming (record 0055, rejected).
- **The withdrawal says why and how the work is asked again.** "<owner> left the fleet, so an answer here reaches nobody." and then, by kind, who raises it now: a deploy offered again in the name of the ops of the partition that holds it now; a step recorded again, its card in that ops's name; a landings card, a proposal or a batch carded by that partition's ops or planner; a record carded again with `crew record` by its design agent. A deploy whose word already stands says so and that the deploy goes on.
- **It is recorded and leaves the rail.** The withdrawal is a `card.close` in the run record, state `withdrawn`, its words whole. The rail no longer shows the card, and the read lists it among the cards it withdrew. A card Pending You no longer finds is recorded lost, as any card is.
- **The row is carded as any row with no card.** A card that reaches nobody cards no row: a row of the partition whose only open card is in a former name is posted through its kind's raise in its owner's name, as a row with none open is. crew maps no former name onto a new one, carries no card across, and takes no partition as another's successor.
- **Everything else is untouched.** A card of a role still in the fleet, a question (an agent's own card), and a card in any name crew does not mint for a partition's role, a conductor's among them, keep the paths they have.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `rail-cards`: the rail's sweep withdraws each of crew's cards whose owner is a role of a partition the teams file no longer has, saying how the work is asked again, and a card in a former name cards no row.

## Impact

- `plugin/lib/cards.py`: `role_left`, whether a card's owner is a partition role that left, and `left_said`, the withdrawal's words, both decisions (`code.7`).
- `plugin/lib/plan.py`: `sweep_judged` judges such cards, `sweep_judgments` hands it the teams file's labels, `cards_asked` and `sweep_cards` ask after and withdraw them.
- `README.md`: the rail read's sweep paragraph names the withdrawal.
- `tests/py/test_rail.py`: the cases.
- No change to the views or crew's mod (`code.8`): no bolt, unit, stage, card key or rail row changes shape, and `withdrawn` is a sweep outcome the rail already lists.
