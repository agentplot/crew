## RENAMED Requirements

- FROM: `### Requirement: The user's own words are their decision`
- TO: `### Requirement: A record states the user's decisions in its own words`

## ADDED Requirements

### Requirement: A decision record holds only how a tool is built or behaves
The design agent SHALL write and amend decision records only of how a tool is built or how it behaves, and a unit SHALL cite as its sources only such records. A proposed record or amendment that holds only a plan matter SHALL raise no card: the design agent SHALL take it out of the kit's main and tell the planner, or main-level ops for a live system.

#### Scenario: A talk settles how a tool behaves
- **WHEN** the user settles in the design agent's pane that a bolt lands only on their send of its row on the landings card
- **THEN** the design agent records it in crew's `docs/adr/`, states the decision in the record's own words, and tells the user the record's number and commit

#### Scenario: A unit's sources
- **WHEN** the design agent or the planner names the sources of a unit whose work a freeze on fixes held back
- **THEN** its `--source` names the records of how the tool is built, and nothing of the freeze

#### Scenario: A proposed amendment that is a plan matter
- **WHEN** the design agent starts and finds a proposed amendment on a kit's main, with no card open, that only freezes fixes on main until a rebuild lands
- **THEN** it raises no card for it, takes the amendment out in a commit submitted through sluice, and tells the planner the freeze in one line

### Requirement: A plan matter goes to the planner, or to ops for a live system, with no record
An order of work, a priority, a freeze, a schedule or a trial, which bolt or unit carries something, and how a one-off move, rename or carry-over is carried out SHALL be the plan's, whoever settles it, the user included. The design agent SHALL tell it to the planner, or to main-level ops when it moves a live system, naming the signal of the user's words when they settled it, and SHALL write no record or amendment of it and raise no card for it.

#### Scenario: The user freezes fixes in the design talk
- **WHEN** the user tells the design agent in its pane that no fixes go on sluice's main until the rebuild lands
- **THEN** the design agent records the user's words as a signal, tells the planner in one line naming the signal, and writes no decision record or amendment and raises no card

#### Scenario: A carry-over on a live system
- **WHEN** the user tells the design agent how a repository's old address is carried over to its new one on the hosts
- **THEN** the design agent records the user's words as a signal, tells main-level ops in one line naming the signal, and records no decision

#### Scenario: A question that is a plan matter
- **WHEN** a question asks the design agent which bolt should carry a fix
- **THEN** the design agent tells whoever brought it that it is the planner's, and records nothing

#### Scenario: The planner carries a plan matter
- **WHEN** the design agent tells the planner of a priority the user set
- **THEN** the planner carries it in the plan, by a proposal where it changes the plan, and asks for no decision record of it

## MODIFIED Requirements

### Requirement: A decision record is accepted only on the user's yes
Every decision record the design agent writes, and every amendment it makes to one, SHALL be committed as proposed. A record or an amendment SHALL become accepted only on the user's yes, recorded in the record with the date and where they gave it: in the pane where the record was settled with them, or on the one card crew raises for it through `crew record` when it was not. Until the yes, a rule drawn from the record SHALL be written marked as proposed, and no unit SHALL be queued from it.

#### Scenario: A new record
- **WHEN** the design agent writes record 0021 in crew's `docs/adr/` from the signals, with the user not in its pane
- **THEN** it commits the record with the status proposed and runs `crew record crew 21 --proposed`, which raises one card asking the user to accept it, in the record's words, and queues no unit from it yet

#### Scenario: The user says yes
- **WHEN** the user approves the card for record 0021
- **THEN** the design agent commits the record as accepted by the user on that date, on their card, takes the proposed mark off each rule drawn from it, runs `crew record crew 21 --accepted`, which closes the card, and only then queues the units it calls for

#### Scenario: An amendment to an accepted record
- **WHEN** the design agent amends record 0005, which is accepted, with the user not in its pane
- **THEN** the amendment is marked proposed in the record, the card crew raises carries the amendment's words, and the amendment is accepted only on the user's yes

### Requirement: A record states the user's decisions in its own words
What the user settled in the design talk SHALL be stated in the record in the record's own words, its deciders line naming the user and where and when they settled it, never their words quoted as the decision. When a card is raised for the record, it SHALL say which part is the user's, and when the user settled the whole record in the pane, their yes there SHALL be recorded and no card raised.

#### Scenario: The user's own words
- **WHEN** the user said in the design talk "the landing still needs my yes", and the record rests on it
- **THEN** the record states in its own words that a landing waits on the user's yes, its deciders line names the user in the design talk on that date and quotes none of their words, and the card, when one is raised, says that part is the user's

#### Scenario: The user's yes in the pane is crew's evidence, not the record's
- **WHEN** the user says "Yes, accept 31 as written" in the design agent's pane, and the design agent runs `crew record crew 31 --proposed --settled-in-pane --excerpt "Yes, accept 31 as written"`
- **THEN** crew reads those words in the design agent's transcript as the user's, and the record says it was accepted by the user in the design agent's pane on that date, quoting none of their words
