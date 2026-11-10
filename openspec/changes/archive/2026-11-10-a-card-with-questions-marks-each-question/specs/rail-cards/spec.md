## ADDED Requirements

### Requirement: A card of questions carries highStakes on each question
A card of crew's that asks questions SHALL carry `highStakes` on each question whose answer is high stakes and SHALL NOT carry it on the card, which Pending You refuses beside questions: "With questions, each question carries its own highStakes; leave the card's highStakes out." A card of one list SHALL carry it on the card.

#### Scenario: Six bolts to land
- **WHEN** six bolts of crew read proven and Pending You refuses a card of questions carrying the card's `highStakes`
- **THEN** `land/crew` is posted as two lists of three, each with `highStakes` set and the card with none, and its post is recorded with nothing refused

#### Scenario: A deploy waiting on five steps
- **WHEN** a deploy waits on five steps of the user's, none done
- **THEN** its card asks two lists, each with `highStakes` set, and the card carries none

## MODIFIED Requirements

### Requirement: A landings card of two or more rows is a list carrying highStakes
With two or more rows, those that can land and those beside them taking main first, a kit's landings card SHALL be boxes carrying `highStakes`, which Pending You takes on a list as the same test as risk high: on the card when it is one list, and on each list and never on the card when it is lists of questions, as "A card of questions carries highStakes on each question" has it.

#### Scenario: A list of three bolts
- **WHEN** crew raises `land/crew` with three rows that can land
- **THEN** the card is one list of three boxes with `highStakes` set, and no `approve` block

#### Scenario: One that can land beside one taking main first
- **WHEN** crew raises `land/crew` with `y`, which can land, and `z`, which takes main first
- **THEN** the card is one list of two boxes with `highStakes` set, `y` ticked and `z` unticked

#### Scenario: Seven bolts, each list marked
- **WHEN** crew raises `land/crew` with seven rows that can land
- **THEN** the card is two lists, of four and three, each with `highStakes` set, and the card carries no `highStakes`
