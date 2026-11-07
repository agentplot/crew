## ADDED Requirements

### Requirement: A failed deploy's card closes naming what the user does
A deploy's card closed by its end recorded failed SHALL name the step that failed and its log, then the words of what the user does that the deployer handed that end with `--does <words>`, as it wrote them. `crew ops record` SHALL take `--does` on every act and keep the words on its entry. Handed no words, or ending well, the card SHALL close as it did before.

#### Scenario: A deploy fails naming what the user does
- **WHEN** the deployer records the end of srv's deploy of `abc1234` failed, its `guests` step failed, with `--does "run clan vars generate srv, land vars/ on main, then ask ops to offer this deploy again"`
- **THEN** `deploy/srv`'s card is closed "The deploy of abc1234 to srv failed at guests; its log: <its log>. What you do: run clan vars generate srv, land vars/ on main, then ask ops to offer this deploy again.", and the run record's end entry holds the words as its `Does`

#### Scenario: A deployer's record handed what the user does is never refused for it
- **WHEN** the deployer runs `crew ops record srv --act end --outcome failed --does <words>`
- **THEN** crew records the end, refusing nothing for `--does`

#### Scenario: A failed deploy handed no words
- **WHEN** the deployer records the end of srv's deploy of `abc1234` failed, its `guests` step failed, with no `--does`
- **THEN** `deploy/srv`'s card is closed "The deploy of abc1234 to srv failed at guests; its log: <its log>."

#### Scenario: A deploy that ends well is handed words
- **WHEN** the deployer records the end of srv's deploy done, every step ok, with `--does <words>`
- **THEN** `deploy/srv`'s card is closed with each step's outcome, naming no words of what the user does
