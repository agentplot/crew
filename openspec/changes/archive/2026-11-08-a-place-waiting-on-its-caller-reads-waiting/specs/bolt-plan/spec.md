## MODIFIED Requirements

### Requirement: A launched place's stage is where Flume's status has it
Once launched, a unit, chore or fix SHALL read queued while Flume waits for room; construct, code with its ticked tasks of all, or verify while a stage runs; needing an answer with the agent's question when it stopped short asking; its stage, sent back, with sluice's words when a submission failed or conflicted; submitted with sluice's number; waiting on its caller, with Flume's words and the stage it waits to retry or its submission, whenever Flume's status says it waits on its caller for a retry, past its kind's bound among them, whatever stage it last delivered; stalled once Flume's status says it is stalled; merged once it has landed on its bolt and landed once its bolt has; or dropped.

#### Scenario: A unit in code
- **WHEN** deneb's runner record for `a`'s launch carries Flume's status of its place in code with three of seven tasks ticked
- **THEN** `crew bolts` shows `a` at `code 3/7`

#### Scenario: A construct that asked
- **WHEN** the runner's record shows `a`'s construct stopped short with "Which partition's rail?"
- **THEN** `crew bolts` shows `a` as needing an answer, with the question

#### Scenario: A stop-short whose agent is kept open
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place, its code ended short needing an answer, its agent kept open for it until `open_until`, its end keyed `stage/code/1/ended-short`
- **THEN** `a` reads needing an answer at code, with the agent's words, and `crew bolts` shows it so

#### Scenario: A place past its bound
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place after its fourth verify delivered and its submission conflicted, the place having gone back as often as its kind allows, so Flume says it waits on its caller to retry code past its bound
- **THEN** `a` reads waiting on its caller at code with Flume's words, never at verify, and `crew bolts`, the board's ledger and the planner's band show it so

#### Scenario: A submission that waits on its retry
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place, its last stage delivered and its submission refused by the merge queue, so Flume says it waits on its caller to retry its submission
- **THEN** `a` reads waiting on its caller at its submission with Flume's words, and `crew bolts` shows it so

#### Scenario: Sent back by sluice
- **WHEN** the runner's record shows `b`'s place back in code after sluice found its submission in conflict on `plugin/lib/plan.py`
- **THEN** `crew bolts` shows `b` in code, sent back, with sluice's words

#### Scenario: Landed on the bolt
- **WHEN** the runner's record shows `a`'s place landed on `bolt/x`, and `x` has not landed
- **THEN** `crew bolts` shows `a` merged
