## MODIFIED Requirements

### Requirement: A bolt lands only once every unit's latest change has been in a batch the user has answered
A bolt SHALL be offered for landing only once every unit's latest change, the commit its last construct left, has been in a batch the user has answered. A batch is answered when its card was sent back with a tap or closed in Pending You, as crew records the card's close, when its reading session was sent, as crew records the card's close or, with no card closed, the batch's, or when the user answered it in their own words in a main-level pane, as crew records from that session's transcript. When a bolt is otherwise ready to land and some unit's latest change has not been in a batch, a batch SHALL be due at once for those units, and the bolt's landing row SHALL name them. While a batch holding a unit's latest change waits on the user's answer, the landing row SHALL name that batch. No landing card SHALL be raised, the row SHALL carry no word to land, and crew SHALL post no `land` of the bolt's launch, whatever send of its kit's landings card stands, until every unit's latest change has been in a batch the user has answered. `crew bolt land` SHALL be refused while any unit's latest change remains outside a batch. A card Pending You lost to its owner SHALL be no answer, and neither SHALL an agent's own words or another agent's tell of what the user said. A chore SHALL be in no batch and SHALL hold no landing.

#### Scenario: A late amendment
- **WHEN** every unit of a bolt has merged and its verification is green, and one unit's change was constructed again after the last batch
- **THEN** a batch holding that unit is due at once, the landing row names the unit, and no landing card is raised until the batch's card has been answered

#### Scenario: A batch card unanswered
- **WHEN** every unit of bolt `y` has merged and its verification is green, and batch 7, whose card the user has not answered, holds one unit's latest change
- **THEN** `y`'s landing row says it lands once you have answered batch 7, carries no command, and no landing card is raised for `y`

#### Scenario: No land while a batch waits
- **WHEN** the user's send on `y`'s kit's landings card stands at `y`'s head, and one of `y`'s units' latest change is in batch 7, which the user has not answered
- **THEN** the card's raise posts no `land` of `y`'s launch, and `y`'s landing row says it lands once you have answered batch 7

#### Scenario: The batch card answered
- **WHEN** the user sends batch 7's card back with no notes
- **THEN** the next rail read on `y`'s team's host raises `y`'s landing card, and its row carries the word to land

#### Scenario: The batch answered in a pane
- **WHEN** the user answers batch 7 in their own words in the planner's pane, and the planner records it with `crew card answer batch/7`
- **THEN** the next rail read on `y`'s team's host raises `y`'s landing card, and its row carries the word to land

#### Scenario: The batch's session sent with no card held
- **WHEN** batch 7's card is held on a host the main level has left, and the user sends batch 7's reading session on the main level's host
- **THEN** crew records batch 7 read, and the next rail read on `y`'s team's host raises `y`'s landing card

#### Scenario: Notes send a unit back
- **WHEN** the user's notes on batch 7 send one of `y`'s units back to construct, and its new change is in no batch yet
- **THEN** `y`'s landing row names that unit as due a batch, and no landing card is raised until the batch that holds its new change has been answered
