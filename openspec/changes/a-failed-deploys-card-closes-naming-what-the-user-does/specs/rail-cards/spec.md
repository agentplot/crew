## MODIFIED Requirements

### Requirement: A card is closed by crew at the event that ends it
crew SHALL close each of its cards at the event that ends what it asks, with a one-line outcome, and SHALL withdraw a row's card whose row is gone on the next rail read, with the reason. A declined approval SHALL be closed with the user's words when its owner reads it with `crew card read`. The outcome or reason crew sends with a close SHALL be cut to Pending You's 200 characters, and the run record SHALL keep it whole.

A deploy's card closed by its end recorded failed SHALL name the step that failed and its log, and after them the words of what the user does that the deployer handed that end with `crew ops record --does <words>`, as the deployer wrote them. `crew ops record` SHALL take `--does` on every act and keep the words on its entry; a deploy whose end was handed no such words SHALL close naming the step and its log alone, and a deploy that ends well SHALL close with each step's outcome whatever words it was handed.

#### Scenario: An outcome longer than Pending You takes
- **WHEN** an approval's outcome, naming every unit it added and every one the user left out, runs past 200 characters
- **THEN** the card is acked with the outcome cut to 200 characters, ending with …, and the run record's close holds it whole

#### Scenario: A proposal approved from the phone
- **WHEN** the user approves `proposal/4` on the phone with its new unit `c` unticked, and the planner runs `crew plan answer 4 rows-1 b`
- **THEN** crew applies the proposal with `c` left out and closes the card "Applied: added b. Left out on your word: c.", and the rail's proposal row is gone

#### Scenario: A proposal dropped
- **WHEN** the planner runs `crew plan drop 4 "the user: not this quarter"`
- **THEN** the card is withdrawn with those words

#### Scenario: A bolt landed
- **WHEN** main-level ops runs `crew bolt land y` after the landing's submission
- **THEN** `land/y`'s card is closed "landed on GitHub's main at <its commit>; every host's folder follows by swancloud's timer within minutes"

#### Scenario: A deploy fails
- **WHEN** the deployer records the end of srv's deploy of `abc1234` with its `guests` step failed, and hands the end no words of what the user does
- **THEN** `deploy/srv`'s card is closed "The deploy of abc1234 to srv failed at guests; its log: <its log>."

#### Scenario: A deploy fails naming what the user does
- **WHEN** the deployer records the end of srv's deploy of `abc1234` failed, its `guests` step failed, with `--does "run clan vars generate srv, land vars/ on main, then ask ops to offer this deploy again"`
- **THEN** `deploy/srv`'s card is closed "The deploy of abc1234 to srv failed at guests; its log: <its log>. What you do: run clan vars generate srv, land vars/ on main, then ask ops to offer this deploy again.", and the run record's end entry holds the words as its `Does`

#### Scenario: A deployer's record handed what the user does is never refused for it
- **WHEN** the deployer runs `crew ops record srv --act end --outcome failed --does <words>`
- **THEN** crew records the end, refusing nothing for `--does`

#### Scenario: A deploy that ends well is handed words
- **WHEN** the deployer records the end of srv's deploy done, every step ok, with `--does <words>`
- **THEN** `deploy/srv`'s card is closed with each step's outcome, naming no words of what the user does

#### Scenario: A step done
- **WHEN** the user answers `op/srv/1` Done and main-level ops runs `crew ops step srv --key <key> --state done`
- **THEN** the card is closed "Done."

#### Scenario: A landing declined
- **WHEN** the user declines `land/y` with "not before the demo" and the conductor runs `crew card read land/y`
- **THEN** the command prints the decline and its words, and the card is closed with them

#### Scenario: A row gone under an open card
- **WHEN** `proposal/4`'s card is open and the proposal is dropped without its card closing
- **THEN** the next rail read withdraws the card, "its proposal was dropped", and says so
