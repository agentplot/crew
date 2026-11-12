## MODIFIED Requirements

### Requirement: A row that can land is a box, ticked as crew proposes
With two or more rows, a landings card SHALL be one list of at most five boxes in the rows' order. Each box SHALL be ticked as crew proposes but a row taking main first, which SHALL be unticked, and labelled with its row's place and its bolt, its detail what the row carries, its consequence its forecast. Clearing a box SHALL leave that bolt waiting. The face SHALL say one send lands the ticked bolts in the order shown and a note may move one.

#### Scenario: Three bolts
- **WHEN** `y`, `z` and `w` of crew read proven in that order
- **THEN** `land/crew` is one list of three ticked boxes, `1. y`, `2. z`, `3. w`, and its summary says the send lands the ticked ones in that order

#### Scenario: Seven bolts
- **WHEN** seven bolts of crew, `b1` to `b7`, read proven in that order
- **THEN** `land/crew` is one list of five ticked boxes, `1. b1` to `5. b5`, and `b6` and `b7` are on its face with no box

## REMOVED Requirements

### Requirement: A landings card of two or more rows is a list carrying highStakes
**Reason**: Pending You refuses a card of questions whose questions carry `highStakes`, as it refused boomdrive's landings card on deneb from 2026-11-11T23:09Z, so a landings card is never lists of questions.
**Migration**: "A landings card of two or more rows is one list carrying highStakes on the card".

### Requirement: A card of questions carries highStakes on each question
**Reason**: A kit's landings card no longer asks questions, so the requirement holds for a deploy's card alone.
**Migration**: "A deploy's card of questions carries highStakes on each question".

## ADDED Requirements

### Requirement: A landings card of two or more rows is one list carrying highStakes on the card
With two or more rows, those that can land and those beside them taking main first, a kit's landings card SHALL be one list of boxes carrying `highStakes` on the card, which Pending You takes on a list as the same test as risk high, whatever the number of rows. It SHALL ask no questions, since Pending You refuses a card of questions that carries `highStakes`, on the card or on its questions.

#### Scenario: A list of three bolts
- **WHEN** crew raises `land/crew` with three rows that can land
- **THEN** the card is one list of three boxes with `highStakes` set, and no `approve` block

#### Scenario: One that can land beside one taking main first
- **WHEN** crew raises `land/crew` with `y`, which can land, and `z`, which takes main first
- **THEN** the card is one list of two boxes with `highStakes` set, `y` ticked and `z` unticked

#### Scenario: Eight bolts, one list marked
- **WHEN** crew raises `land/crew` with eight rows that can land
- **THEN** the card is one list of five boxes with `highStakes` set on the card, and it asks no questions

### Requirement: A deploy's card of questions carries highStakes on each question
A deploy's card that asks questions SHALL carry `highStakes` on each question whose answer is high stakes and SHALL NOT carry it on the card, which Pending You refuses beside questions: "With questions, each question carries its own highStakes; leave the card's highStakes out." A card of one list SHALL carry it on the card.

#### Scenario: A deploy waiting on five steps
- **WHEN** a deploy waits on five steps of the user's, none done
- **THEN** its card asks two lists, each with `highStakes` set, and the card carries none

### Requirement: A landings card holds five boxes and the rest of its rows wait on its face
A landings card of more than five rows SHALL give boxes to five: first the rows crew would tick, then the others, each in the rows' order. Every other row SHALL stay on the card's face in its place, marked as waiting for a box, and its post or change SHALL record it as having none. A row with no box SHALL be no word to land. The summary SHALL say how many rows wait for a box and that the card that follows the send asks for them.

#### Scenario: Eight bolts, and Pending You refuses questions carrying highStakes
- **WHEN** eight bolts of crew, `b1` to `b8`, read proven in that order, and Pending You refuses a card of questions carrying `highStakes` anywhere
- **THEN** `land/crew` is posted as one list of five boxes, `1. b1` to `5. b5`, `b6`, `b7` and `b8` are on its face marked as waiting for a box, and its post is recorded with nothing refused, its `Heads` marking `b6`, `b7` and `b8` `:next`

#### Scenario: A left row and one taking main first among seven
- **WHEN** crew's seven rows are `b1`, which the user left, `b2`, which takes main first, and `b3` to `b7`, which can land
- **THEN** the boxes are `3. b3` to `7. b7`, all ticked, and `b1` and `b2` are on the face in their places with no box

#### Scenario: Twenty-one bolts
- **WHEN** twenty-one bolts of crew read proven
- **THEN** `land/crew` is one list of five boxes, sixteen rows wait on its face, and the card is posted

### Requirement: A row coming to a box or losing one changes the waiting landings card in place
While a landings card waits, a row coming to have a box or losing one, as rows join, leave or are left, SHALL change the card in place with a note naming the row, and SHALL NOT follow it while it stays one list.

#### Scenario: A boxed row is held for a fix
- **WHEN** `land/crew` waits with eight rows, `b6` to `b8` with no box, and `b2` is held for a fix
- **THEN** the card is changed in place, its note saying `b6` has a box now, its boxes `b1`, `b3`, `b4`, `b5` and `b6`, and no card is posted

#### Scenario: A row waiting for a box moves its head
- **WHEN** `land/crew` waits with `b7` on its face with no box, and a fix's merge moves `b7`'s head to `def5678`
- **THEN** the card is changed in place, its note saying `b7`'s head is now `def5678`, and `b7` still has no box

### Requirement: A send with rows waiting for a box is followed at once by a card asking for them
When the user sends a landings card that had rows waiting for a box, crew SHALL close it at once, naming those rows as having had no box, and post the card that follows, its rows those the send does not land. A row that waited for a box SHALL NOT be counted among the rows the user left. A row the user left SHALL stay left while it waits for a box. The card that follows SHALL say which of its rows had no box on the last card.

#### Scenario: Five ticked, three waiting
- **WHEN** the user sends `land/crew` with `b1` to `b5` ticked and `b6` to `b8` waiting for a box
- **THEN** the card is closed saying the send lands `b1` to `b5` and `b6`, `b7` and `b8` had no box, a card asking for `b6`, `b7` and `b8` as ticked boxes follows it at once, its summary saying they had no box on the last card, and none of them is recorded left

#### Scenario: A left row that waited for a box
- **WHEN** the user left `b1` on an earlier send, `b1` waits on the face of `land/crew` with no box, and the user sends it with `b2` to `b6` ticked
- **THEN** `b1` stays left, unticked on the card that follows
