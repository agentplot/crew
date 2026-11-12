## ADDED Requirements

### Requirement: The rail's read raises a landings card that does not show a row as it stands
On the main level's host, the rail's read SHALL raise each kit's landings card open in main-level ops's name whose land row holds a row that can land, held by no send, that the card shows on no row, at another head, taking main first, or, once answered, with no box. It SHALL raise none for a card that shows every such row as it stands.

#### Scenario: A bolt proven between a send and its landing
- **WHEN** the user sent `land/crew` ticking `y`, whose land the runner has not answered, main has not moved, and `z` reads proven, on no row of that card
- **THEN** the rail's read raises `land/crew` in the same sweep: the card they sent is closed keeping their send for `y`, and a card following it asks for `z`

#### Scenario: A bolt proven while the card waits
- **WHEN** `land/crew` waits on the user with `y`, main has not moved, and `z` reads proven
- **THEN** the rail's read raises `land/crew` for `z`, and the read after it, the card showing `z` at its head, raises none

#### Scenario: A bolt the user left beside a send still landing
- **WHEN** the user sent `land/crew` ticking `y` and leaving `z`, `y` has not landed, and `z` stands at the head the card showed
- **THEN** the rail's read raises no landings card

#### Scenario: The rail names the card it raised
- **WHEN** the rail's read raised `land/switchboard-kit` for `apex-zones`
- **THEN** `crew rail` says so under the landings cards raised for rows they did not offer as they stand, naming `apex-zones` and the card, or the raise's refusal in its words

### Requirement: A bolt proven while an answered landings card waits on its landings is offered at once
A row that can land and that a kit's answered landings card did not offer as it now stands SHALL be offered at once. crew SHALL close the answered card, keeping the user's send for each bolt it still lands, which lands on that send, and post a card following it that asks for the row, as for a send's rows that waited for a box.

#### Scenario: Proven since the send
- **WHEN** the user sent `land/crew` ticking `y`, `y` has not landed, `z` reads proven, on no row of that card, and crew raises `land/crew`
- **THEN** the card is closed saying the runner was asked to land `y` and that `z` reads proven since, keeping `y` at the head it showed as the send; a card following it asks for `z`; and `y` is no row of that card while its head stands

## MODIFIED Requirements

### Requirement: An answered landings card closes once each bolt it ticked has landed, been held or stopped
A landings card the user has answered SHALL be left as it is until every bolt they ticked has landed, been held or been stopped, then closed naming what landed and where GitHub's main holds it, what was held and why, what was stopped and in whose words, and what was left; a new card SHALL follow it while rows can land. A row proven meanwhile SHALL close it sooner, its send kept. The close SHALL keep the user's send for each ticked bolt held whose send still stands, saying so.

#### Scenario: Everything ticked lands
- **WHEN** the user sent `land/crew` with `y` and `z` ticked and both land
- **THEN** the card is closed saying `y` and `z` landed and where GitHub's main holds them, and no landings card of crew is open

#### Scenario: One left out
- **WHEN** the user sent `land/crew` with `y` ticked and `z` cleared, and `y` lands
- **THEN** the card is closed saying `y` landed and `z` was left, and a new card follows it with `z` as its one row

#### Scenario: A ticked bolt held at the close
- **WHEN** the user sent `land/crew` with `y` and `z` ticked, `y` lands and Flume refuses `z` for a failed check
- **THEN** the card is closed saying `y` landed and `z` was held and why, and that the send stands for `z` while its own work is unchanged

#### Scenario: A ticked bolt stopped at the close
- **WHEN** the user sent `land/crew` with `y` and `z` ticked, `y` lands and the runner answers `z`'s land refused
- **THEN** the card is closed saying `y` landed and `z` was stopped, in the runner's words, and a new card follows it with `z` as a row with its box
