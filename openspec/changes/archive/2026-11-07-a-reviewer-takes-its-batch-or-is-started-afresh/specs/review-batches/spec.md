## MODIFIED Requirements

### Requirement: The planner starts the partition's reviewer
When a batch is due, crew SHALL tell the partition's planner once, and the planner SHALL start the reviewer: a main-level role, run fresh for each batch in its own tab of the main level's workspace, beside the planner, on the main level's host. Where the partition runs its reviewer as its kind, `crew review <label>` SHALL instead write an ask of the reviewer carrying the batch, as the reviewer's first message carries it today, open no tab and start no agent, and `crew review <label> --wait` SHALL refuse, saying the batch's delivery reaches the planner as an ask.

A standing reviewer SHALL be sent its batch taken or sent again: only once it accepts input, read back from its transcript within a short time, and sent once more when it is not there. When the second sending is not taken either, crew SHALL clear what was left typed in its input, record the start refused, and refuse, naming `crew review <label>` as the way on; a refused start SHALL be no batch, its number taken by the next start, and `crew review <label> --wait` after it SHALL refuse. When `crew review <label>` finds the reviewer up, idle or done with no question open, its session holding no batch and no summary written since its last start, crew SHALL end it, record the end, say so, and start the batch's reviewer afresh, ending nothing when no batch is due. A reviewer at work, at a question, or that took its batch SHALL be refused, and one whose taking crew cannot read SHALL be refused naming what it could not read. `crew review <label> --wait` on a reviewer that took no batch SHALL refuse, naming `crew review <label>`, and end nothing.

#### Scenario: A batch is due
- **WHEN** a conductor's wait finds a batch due in the wldn partition
- **THEN** wldn-planner is told once, and starts `wldn-reviewer` in the `wldn` workspace

#### Scenario: A reviewer that runs as its kind
- **WHEN** madswan runs its reviewer as its kind and the planner's run runs `crew review madswan`
- **THEN** an ask of the reviewer holds the batch's changes, how to read each and the file to write, no tab is opened, and no reviewer is started by crew

#### Scenario: Waiting on a reviewer that runs as its kind
- **WHEN** madswan runs its reviewer as its kind and `crew review madswan --wait` runs
- **THEN** it refuses, saying the batch's delivery reaches the planner as an ask, and waits on nothing

#### Scenario: A batch taken at once
- **WHEN** the planner runs `crew review wldn` and wldn-reviewer's transcript shows its batch received moments after crew sent it
- **THEN** crew sent it once, records the start, and says wldn-reviewer is reviewing the batch

#### Scenario: A batch taken at neither sending
- **WHEN** the planner runs `crew review wldn` and wldn-reviewer's transcript shows batch 3 received after neither sending, while it sits idle
- **THEN** crew cleared its input after each sending, nothing is left typed, the start is recorded refused, and the command refuses, saying wldn-reviewer did not take batch 3 and that `crew review wldn` ends it and starts the batch's reviewer afresh

#### Scenario: Waiting on a reviewer that took no batch
- **WHEN** wldn-reviewer is up and idle having taken no batch and `crew review wldn --wait` runs
- **THEN** it refuses, naming `crew review wldn`, and ends nothing

#### Scenario: An idle reviewer that took no batch
- **WHEN** the planner runs `crew review wldn` while wldn-reviewer is up and idle, its session holding no batch and no summary written since its last start
- **THEN** crew ends it, records the end, says so, starts wldn-reviewer afresh and sends it the batch, taken or sent again

#### Scenario: A reviewer still reviewing
- **WHEN** the planner runs `crew review wldn` while herdr reads wldn-reviewer working, or its session holds its batch, or its summary is written
- **THEN** crew refuses, saying wldn-reviewer is still reviewing a batch and that `crew review wldn --wait` waits for its summary, and ends nothing

#### Scenario: A reviewer at a question or not read
- **WHEN** the planner runs `crew review wldn` while wldn-reviewer waits on a question in its pane, or crew cannot read whether its session holds a batch
- **THEN** crew refuses, saying which, and ends nothing
