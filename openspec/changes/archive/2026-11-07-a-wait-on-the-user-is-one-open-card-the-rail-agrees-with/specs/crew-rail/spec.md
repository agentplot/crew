## ADDED Requirements

### Requirement: A row whose card the user answered says whose act it waits on
When the run record holds the user's answer on a row's open card, the row's card line SHALL say the card was answered, when, what was answered in crew's words, and the act of the row owner's it now waits on, never that it is open and asked.

#### Scenario: A landings card the user sent
- **WHEN** `land/sluice`'s card `req_e9` is open and the run record holds the user's answer on it at 22:01, ticking `a` and `b`
- **THEN** the land row's card line says `land/sluice` was answered at 22:01, ticking `a` and `b`, and waits on agentplot-ops to land them, and does not say `open, asked by`

#### Scenario: A proposal's card approved on the phone
- **WHEN** `proposal/57`'s card is open and the run record holds the user's answer on it, approved
- **THEN** the proposal row's card line says it was answered, approved, and waits on the planner to apply it

#### Scenario: A batch's card tapped
- **WHEN** `batch/12`'s card is open and the run record holds the user's answer on it
- **THEN** the batch row's card line says it was answered and waits on the planner to hand on its notes

#### Scenario: A deploy whose word stands
- **WHEN** `deploy/srv`'s card is answered and ops has recorded the word, which stands
- **THEN** the operations row's card line says the user's word stands and the deploy's end closes the card

#### Scenario: A card not yet answered
- **WHEN** `proposal/57`'s card is open and the run record holds no answer on it
- **THEN** its card line names it open, asked by the planner, with its id, as before

### Requirement: An answered question or record card no longer waits on the user
An open question or decision record card whose answer the run record holds SHALL NOT be listed among the questions or records waiting on the user. It SHALL be listed apart, under answered cards waiting on their askers, with its key, its asker, when it was answered and what was answered.

#### Scenario: A question answered
- **WHEN** agentplot-design's question `ask/agentplot-design/sluice-who-claims` is open and the run record holds the user's answer on it
- **THEN** the rail lists it under the answered cards waiting on their askers, naming agentplot-design and when it was answered, and not under the questions waiting on the user

#### Scenario: A record card answered
- **WHEN** `record/weir/0004`'s card is open and the run record holds the user's answer on it, approved
- **THEN** the rail lists it under the answered cards waiting on their askers, naming agentplot-design, and not under the decision records waiting on the user

### Requirement: Each bolt's land line says whether its card carries, holds or follows it
Each bolt line on a kit's land row SHALL end what it waits on with how the kit's card stands for it: carried, when the open card waiting on the user shows it as a row; held, when the user's send stands for it at its head now; or following, when it can land and neither holds. A bolt that can't land and is no row of the card SHALL say nothing of the card.

#### Scenario: A bolt the open card carries
- **WHEN** `land/crew`'s card waits on the user and its last post shows `b` at its head now
- **THEN** `b`'s line says `land/crew` carries it, waiting on the user

#### Scenario: A bolt the card shows at an older head
- **WHEN** `land/crew`'s card waits on the user and shows `b` at `1111111`, and `b`'s head is now `2222222`
- **THEN** `b`'s line says `land/crew` carries it at `1111111`, its head now `2222222`

#### Scenario: A bolt the user's send holds
- **WHEN** the user answered `land/crew`'s card ticking `b` at its head now, and `b`'s landing is not yet queued
- **THEN** `b`'s line says the user's send on `land/crew` holds it and swancloud-ops lands it

#### Scenario: A send kept on a closed card
- **WHEN** `land/crew`'s answered card closed keeping the user's send for `b`, held taking main in, and `b` reads proven again at a head whose own work is the same
- **THEN** `b`'s line says the user's send holds it

#### Scenario: A bolt proven since the send
- **WHEN** the user answered `land/crew`'s card ticking `b`, and `c` reads proven since, on no row of that card
- **THEN** `c`'s line says it follows: the card after `land/crew`'s answered one carries it

#### Scenario: A bolt no card carries yet
- **WHEN** `b` can land and no card is open under `land/crew`
- **THEN** `b`'s line says it follows: the next card under `land/crew` carries it

#### Scenario: A bolt waiting on its verification
- **WHEN** `b`'s line says it lands once its verification is green, and no card shows it
- **THEN** `b`'s line says nothing of the card
