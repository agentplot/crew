## ADDED Requirements

### Requirement: A fix of main is a box of its kit's landings card
Each fix of a kit's main whose code has delivered and whose submission waits held for the user's send SHALL be a row of the kit's landings card ahead of its bolts, `fix main--<name>`, ticked as crew proposes, saying the failure's first line and that ticked, ops sends it with `crew main fix <kit> <name> --send`, and forecast against nothing. crew SHALL raise the card for it though no bolt can land beside it, a lone fix the card's one row, an approval. A fix sent already SHALL be no row.

#### Scenario: A fix with no bolt beside it
- **WHEN** sluice's `main--handed-over-wait-holds-steady` has delivered and its submission waits held, and no bolt of sluice can land
- **THEN** `land/sluice` is raised in agentplot-ops's name, the fix its one row, an approval that says approving sends it with `crew main fix sluice handed-over-wait-holds-steady --send`

#### Scenario: A fix beside a bolt
- **WHEN** crew's `main--a-test-reads-its-fixture` waits held and crew's bolt `y` can land
- **THEN** `land/crew` is one list, `1. fix main--a-test-reads-its-fixture` then `2. y`, both ticked, and only `y` is forecast

### Requirement: A ticked fix of main stands on the send while it waits held
A fix of main the user ticked SHALL be still to land on their send while it waits held, sent or not, and the card's close, once it no longer does, SHALL say whether it was sent on their word for its runner to submit or dropped. A fix they cleared SHALL be left, unticked on the card that follows. A fix an earlier send ticked SHALL be no row of a later card while it waits held at that launch. An answered card that ticked a fix SHALL wait on ops until its send or drop is recorded.

#### Scenario: Ticked and sent
- **WHEN** the user sent `land/crew` with the fix ticked, and ops's `crew main fix crew a-test-reads-its-fixture --send` appended its retry
- **THEN** the card is left until the fix no longer waits held, then closed saying it was sent on the user's word for its runner to submit to main through sluice

#### Scenario: Cleared on the send
- **WHEN** the user sent `land/crew` with `y` ticked and the fix cleared, and `y` lands
- **THEN** the card is closed saying `y` landed and the fix was left, and a new card follows it with the fix unticked

#### Scenario: ops's send ends the wait
- **WHEN** the user's answer on `land/crew` ticked the fix and `y`, and ops's send of the fix is recorded since
- **THEN** the card waits on ops for `y` alone
