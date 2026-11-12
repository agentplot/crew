## MODIFIED Requirements

### Requirement: A bolt started before bolts were base places has no box
A started bolt with no launch of `bolt/<bolt>` in the drive's requests SHALL land under the crew that started it. Once it reads proven, and while its kit's main does not hold its work, its row on its kit's landings card SHALL have no box and SHALL say it was started before bolts were base places and lands under the crew that started it, and crew SHALL post no land for it (record 0056). Once main holds its work, it is no row (bolt-teams).

#### Scenario: Beside a bolt that can land
- **WHEN** crew's bolts `y` and `w` read proven, `y` launched as a base place and `w` started by an older crew, with no launch of `bolt/w`, and crew's main does not hold `w`'s work
- **THEN** `land/crew` shows `y` ticked and `w` with no box, `w`'s row saying it was started before bolts were base places and lands under the crew that started it, and no raise posts a land of `w`

#### Scenario: Landed by the crew that started it
- **WHEN** `w`'s landing by an older crew has landed, and GitHub's main holds `w`'s work
- **THEN** `land/crew` shows `y` ticked and no row for `w`

### Requirement: A landing the runner or Flume stopped keeps its box
A bolt whose land the runner answered refused, or whose submission Flume reports withdrawn or refused and waiting on its caller, as the runner's report carries it, SHALL keep its box while its kit's main does not hold its work (record 0056 decision 6). Its row SHALL say what stopped its landing at that head, in the runner's or Flume's words, nothing of the bolt's. The send that ticked it SHALL be spent: crew SHALL post no land of it again on that send.

#### Scenario: The runner refuses the land
- **WHEN** the user sent `land/crew` with `z` ticked, crew posted `z`'s land, and the runner answered it refused, a place on `bolt/z` being live
- **THEN** `z` keeps its box, its row says its landing at that head was stopped, in the runner's words, nothing of the bolt's, and no raise posts another land of `z` on that send

#### Scenario: Flume's submission withdrawn
- **WHEN** the runner's report carries `z`'s base place with its submission withdrawn, waiting on its caller
- **THEN** `z` keeps its box, and its row says its landing was stopped, in Flume's words, nothing of the bolt's

#### Scenario: A new card while it is stopped
- **WHEN** `z`'s landing was stopped and a card of crew's landings follows the one the user answered
- **THEN** the closed card's outcome names `z` as stopped, with what stopped it, and the card that follows has `z` as a row with its box, ticked as crew proposes, saying what stopped its last landing

#### Scenario: The head moves
- **WHEN** `z`'s landing was stopped at `abc1234` and `z`'s head moves to a new head that reads proven
- **THEN** `z`'s row says nothing of the stop

#### Scenario: A stopped landing that landed
- **WHEN** `z`'s landing was stopped at `abc1234`, and GitHub's main holds `abc1234` and the commit each of `z`'s units landed at on `bolt/z`
- **THEN** `land/crew` has no row for `z`, and no word of the stop is said on the card
