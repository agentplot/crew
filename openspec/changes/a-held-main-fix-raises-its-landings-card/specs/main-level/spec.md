## MODIFIED Requirements

### Requirement: A fix of main lands on the user's send
Once a fix of main's code has delivered and its submission waits held, the kit's landings row and the kit's landings card SHALL carry it; `crew main fix <kit> <name> --send`, ops's on the user's send and read as a landing's words are, SHALL append the retry of its submission, and nothing else SHALL submit it. `crew card read land/<kit>` SHALL give each fix the user ticked, on the card read or on an earlier send while it waits held, as that command, ahead of the submit of the bolts the send lands.

#### Scenario: The user's send
- **WHEN** the runner's record shows `main--a-test-reads-its-fixture`'s code delivered and its submission held, and the user sends the kit's landings card with it ticked
- **THEN** ops's `crew main fix crew a-test-reads-its-fixture --send` appends a retry of its submission

#### Scenario: The read of the send
- **WHEN** the user approves `land/sluice`, whose one row is `main--handed-over-wait-holds-steady`
- **THEN** ops's `crew card read land/sluice` prints `crew main fix sluice handed-over-wait-holds-steady --send` as the command that sends it, and no `crew bolt submit`

#### Scenario: Beside a bolt
- **WHEN** the user sends `land/crew` with `main--a-test-reads-its-fixture` and `y` ticked
- **THEN** the read prints the fix's `crew main fix crew a-test-reads-its-fixture --send` and then `crew bolt submit y`
