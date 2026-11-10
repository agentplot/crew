## MODIFIED Requirements

### Requirement: A place is answered by a retry
`crew answer <work> "<words>"`, the planner's, the design agent's or main-level ops's, SHALL append a retry of the stage the work's place stopped short on or waits on, carrying the words, its agent kept open for the answer or not, and past its kind's bound or not, whatever stage it last delivered; or of its submission where that waits on its caller unheld. It SHALL be refused naming the place's stage when the place neither stopped short nor waits on its caller. For a live place, the refusal SHALL name that stage as the runner carried it, with the runner's host and when it carried it, and say that a wait Flume has told of since reaches crew with that runner's next carry. It SHALL be refused naming what crew could not read when it can't tell whether the place waits. It SHALL never say that a live place has nothing to answer.

#### Scenario: A construct that asked
- **WHEN** the runner's record shows `a`'s construct stopped short asking "Which partition's rail?", and the planner runs `crew answer a "madswan's"`
- **THEN** `requests.rec` gains a retry of `a`'s construct with the words `madswan's`

#### Scenario: A stop-short whose agent is kept open
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place, its code ended short needing an answer with its agent kept open, and the planner runs `crew answer a "Wait for the releases; retry once they land."`
- **THEN** `requests.rec` gains a retry of `a`'s code with those words, and nothing is refused

#### Scenario: A place past its bound
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place waiting on its caller to retry code past its bound, its verify delivered, and the planner runs `crew answer a "Take the bolt in and resolve the conflict."`
- **THEN** `requests.rec` gains a retry of `a`'s code with those words

#### Scenario: A submission that waits on its retry
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place waiting on its caller to retry its submission, which the merge queue refused, and the planner runs `crew answer a "Submit it again."`
- **THEN** `requests.rec` gains a retry of `a`'s submission with those words

#### Scenario: Nothing to answer
- **WHEN** deneb's runner last carried `a`'s place in code with no question, Flume may since have told the planner the place waits on its caller, and the planner runs `crew answer a "yes"`
- **THEN** it is refused naming `a`'s stage as code when deneb's runner carried it, at the time it carried it, and saying that a wait Flume has told of since reaches crew with that runner's next carry, never that there is nothing to answer, and `requests.rec` gains nothing

#### Scenario: A place the runner has not carried
- **WHEN** `a`, naming no `After`, is answered held with the runner's claim, or launched at a place whose status the runner has not carried, and `crew answer a "yes"` runs
- **THEN** it is refused saying crew can't tell whether `a`'s place waits on an answer, with the runner's words or that no status of the place is carried, and never that it is held for its After work

#### Scenario: Work that is over
- **WHEN** the runner's record shows `a`'s place landed on its bolt, and `crew answer a "yes"` runs
- **THEN** it is refused naming `a` merged, with nothing to answer
