## MODIFIED Requirements

### Requirement: A place is answered by a retry
`crew answer <work> "<words>"`, the planner's, the design agent's or main-level ops's, SHALL append a retry of the stage the work's place stopped short on or waits on, carrying the words, a stop-short whose agent Flume keeps open for its answer among them, whose retry Flume hands that session as a tell answering it does. It SHALL be refused, naming the place's stage, when the place neither stopped short nor waits on its caller. Where crew can't tell whether the place waits on an answer, since no runner has answered its launch, the runner holds its launch, or the runner has carried none of Flume's status of its place yet, it SHALL be refused naming which, and never saying the place has nothing to answer.

#### Scenario: A construct that asked
- **WHEN** the runner's record shows `a`'s construct stopped short asking "Which partition's rail?", and the planner runs `crew answer a "madswan's"`
- **THEN** `requests.rec` gains a retry of `a`'s construct with the words `madswan's`

#### Scenario: A stop-short whose agent is kept open
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place, its code ended short needing an answer with its agent kept open, and the planner runs `crew answer a "Wait for the releases; retry once they land."`
- **THEN** `requests.rec` gains a retry of `a`'s code with those words, and nothing is refused

#### Scenario: A place the runner has not carried
- **WHEN** `a`, naming no `After`, is answered held with the runner's claim, or launched at a place whose status the runner has not carried, and `crew answer a "yes"` runs
- **THEN** it is refused saying crew can't tell whether `a`'s place waits on an answer, with the runner's words or that no status of the place is carried, and never that it is held for its After work

#### Scenario: Nothing to answer
- **WHEN** `a`'s place is in code with no question, and `crew answer a "yes"` runs
- **THEN** it is refused naming `a`'s stage as code
