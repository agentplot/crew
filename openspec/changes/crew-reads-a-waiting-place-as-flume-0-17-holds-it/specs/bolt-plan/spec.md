## MODIFIED Requirements

### Requirement: A started bolt's work reads its stage from the runner's records
For every unit, chore and fix of a bolt marked `Path: flume`, a bolt started by `crew bolt start`, crew SHALL read its stage from its newest launch not dropped, that launch's answer and its place's record on the runner's branch, never from a place in the kit: unknown where its host was not read or it has no launch, launching before an answer, waiting while the runner holds a launch whose `After` names work, refused with the runner's words. A launch the runner holds whose `After` names no work SHALL read launching, with the runner's words, and never waiting on After work, since the runner answers held as well for its claim of a launch and for a stream with no room. `crew bolts` and every decision that reads a stage SHALL read the same.

#### Scenario: A dependent waits
- **WHEN** `b`'s launch is answered held, `a`'s place not yet landed
- **THEN** `crew bolts` shows `b` waiting on `a`

#### Scenario: A claimed launch is not held for After work
- **WHEN** deneb's runner answers the launch of `a`, which names no `After`, held with the words `claimed by deneb's runner; launching once no other runner has claimed it`
- **THEN** `a` reads launching, and `crew bolts`, the board and the planner's band show it launching with the runner's words, never waiting on After work

#### Scenario: The runner's host is silent
- **WHEN** deneb's runner branch can't be read
- **THEN** every piece launched on deneb reads unknown, and `crew bolts` names deneb

### Requirement: A launched place's stage is where Flume's status has it
Once launched, a unit, chore or fix SHALL read queued while Flume waits for room; construct, code with its ticked tasks of all, or verify while a stage runs; needing an answer with the agent's question when it stopped short asking, whether or not Flume keeps its agent open for the answer; its stage, sent back, with sluice's words when a submission failed or conflicted; submitted with sluice's number; waiting on its caller with Flume's words past its bound; stalled; merged once it has landed on its bolt and landed once its bolt has; or dropped. crew SHALL read each from Flume's status as the Flume the host runs gives it.

#### Scenario: A unit in code
- **WHEN** deneb's runner record for `a`'s launch carries Flume's status of its place in code with three of seven tasks ticked
- **THEN** `crew bolts` shows `a` at `code 3/7`

#### Scenario: A construct that asked
- **WHEN** the runner's record shows `a`'s construct stopped short with "Which partition's rail?"
- **THEN** `crew bolts` shows `a` as needing an answer, with the question

#### Scenario: A stop-short whose agent is kept open
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place, its code ended short needing an answer, its agent kept open for it until `open_until`, its end keyed `stage/code/1/ended-short`
- **THEN** `a` reads needing an answer at code, with the agent's words, and `crew bolts` shows it so

#### Scenario: Sent back by sluice
- **WHEN** the runner's record shows `b`'s place back in code after sluice found its submission in conflict on `plugin/lib/plan.py`
- **THEN** `crew bolts` shows `b` in code, sent back, with sluice's words

#### Scenario: Landed on the bolt
- **WHEN** the runner's record shows `a`'s place landed on `bolt/x`, and `x` has not landed
- **THEN** `crew bolts` shows `a` merged
