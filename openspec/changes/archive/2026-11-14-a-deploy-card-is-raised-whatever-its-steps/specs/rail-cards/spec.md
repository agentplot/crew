## ADDED Requirements

### Requirement: A deploy's card waiting on steps is one list of at most five boxes
While a step the deploy waits on is open, the deploy's card SHALL be one list of at most five boxes, the deploy's box last, carrying `highStakes` and what follows a yes on the card, whatever the number of steps. It SHALL ask no questions, since Pending You refuses a card of questions carrying `highStakes`, on the card or on any question.

#### Scenario: Seven steps the deploy waits on, and Pending You refuses questions carrying highStakes
- **WHEN** swancloud-srv's offer of `bbbbbbb` waits on seven steps of the user's, none done, and Pending You refuses a card of questions carrying `highStakes` anywhere
- **THEN** `deploy/swancloud-srv` is posted as one list of five boxes with `highStakes` set on the card, none ticked, the deploy's box last, it asks no questions, and its post is recorded with nothing refused and the form `boxes`

#### Scenario: Four steps the deploy waits on
- **WHEN** the deploy waits on four steps of the user's, none done
- **THEN** its card is one list of five boxes, `before:1` to `before:4` and `deploy`, each step with a box of its own

### Requirement: Past four open steps a deploy's fourth box holds the rest
With more than four open steps, the first three SHALL each have a box, and the fourth box SHALL hold every other open step, its id `before:` and their numbers joined by `-`, its label naming their numbers. Every step SHALL stay on the face with its why, and the summary SHALL say which steps share the fourth box. The word SHALL be the send with every box ticked, `crew ops approve --ticked` naming each step of each ticked box, and SHALL be refused naming any step it leaves out.

#### Scenario: Seven steps share four boxes
- **WHEN** the deploy waits on seven steps of the user's, none done
- **THEN** its boxes are `before:1`, `before:2`, `before:3`, `before:4-5-6-7` labelled "Done: steps 4, 5, 6 and 7", and `deploy`, its face lists all seven with their whys, and its summary says steps 4, 5, 6 and 7 share the fourth box

#### Scenario: A step done among six
- **WHEN** the deploy waits on six steps of the user's and step 2 is done
- **THEN** its boxes are `before:1`, `before:3`, `before:4`, `before:5-6` and `deploy`, and its face lists step 2 done

#### Scenario: A step recorded done while the card of a shared box waits
- **WHEN** the card of seven open steps is open and step 5 is recorded done
- **THEN** the card is changed in place, not followed, its boxes `before:1` to `before:3`, `before:4-6-7` and `deploy`

#### Scenario: The send's shared box named as one step
- **WHEN** the user sends that card with every box ticked and main-level ops runs `crew ops approve swancloud-srv --to bbbbbbb --ticked 1,2,3,4`
- **THEN** it is refused naming steps 5, 6 and 7, each with its words, and no word is given; `--ticked 1,2,3,4,5,6,7` is refused nothing

## REMOVED Requirements

### Requirement: A deploy's card of questions carries highStakes on each question
**Reason**: Pending You refuses a card of questions carrying `highStakes`, on the card or on any question, as it refused boomdrive's landings card on deneb from 2026-11-11T23:09Z, so a deploy's card no longer asks questions and no card of crew's does with `highStakes`.
**Migration**: "A deploy's card waiting on steps is one list of at most five boxes" and "Past four open steps a deploy's fourth box holds the rest".
