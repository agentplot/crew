## RENAMED Requirements

- FROM: `### Requirement: The planner starts the partition's reviewer`
- TO: `### Requirement: The planner starts the drive's reviewer`

- FROM: `### Requirement: A batch spans the partition's bolts`
- TO: `### Requirement: A batch spans the drive's bolts`

- FROM: `### Requirement: A batch is reckoned from the partition's branch, never a host`
- TO: `### Requirement: A batch is reckoned from the drive's branch, never a host`


## MODIFIED Requirements

### Requirement: The planner starts the drive's reviewer
When a batch is due, crew SHALL tell the drive's planner once, and the planner SHALL start the reviewer: a main-level role, run fresh for each batch in its own tab of the main level's workspace, beside the planner, on the main level's host. Where the drive runs its reviewer as its kind, `crew review <label>` SHALL instead write an ask of the reviewer carrying the batch, as the reviewer's first message carries it today, open no tab and start no agent, and `crew review <label> --wait` SHALL refuse, saying the batch's delivery reaches the planner as an ask.

A standing reviewer SHALL be sent its batch taken or sent again: only once it accepts input, read back from its transcript within a short time, and sent once more when it is not there. When the second sending is not taken either, crew SHALL clear what was left typed in its input, record the start refused, and refuse, naming `crew review <label>` as the way on; a refused start SHALL be no batch, its number taken by the next start, and `crew review <label> --wait` after it SHALL refuse. When `crew review <label>` finds the reviewer up, idle or done with no question open, its session holding no batch and no summary written since its last start, crew SHALL end it, record the end, say so, and start the batch's reviewer afresh, ending nothing when no batch is due. A reviewer at work, at a question, or that took its batch SHALL be refused, and one whose taking crew cannot read SHALL be refused naming what it could not read. `crew review <label> --wait` on a reviewer that took no batch SHALL refuse, naming `crew review <label>`, and end nothing.

#### Scenario: A batch is due
- **WHEN** a conductor's wait finds a batch due in the wldn drive
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

### Requirement: A batch that waits on nothing is closed by crew
A batch SHALL wait on nothing once each of its units has landed, has been dropped from the plan since the batch was made, or is held by a later batch. crew SHALL read such a batch closed from the run record at every read of the rail and the board, so it is no row and crew raises no card for it; the rail's sweep SHALL record crew's close once, in the planner's name, saying why, and SHALL withdraw a card open under its key with the same words. A batch with any other unit SHALL stay a row until its card closes.

#### Scenario: Every unit has landed
- **WHEN** batch 3 holds `x1` and `x2`, no card of it was ever closed, and the bolt holding both has landed
- **THEN** the rail and the board have no row for batch 3, no card is posted for it, and the next rail read on the drive's main-level host records crew's close of `batch/3` in the planner's name, "its batch waits on nothing: x1 and x2 have landed"

#### Scenario: A later batch holds the unit
- **WHEN** batch 5 holds `x1`, the user's notes on it were given in the planner's pane, `x1` was constructed again, and batch 7 holds its new change
- **THEN** batch 5 is no row, crew's close of `batch/5` says "its batch waits on nothing: batch 7 holds a newer change of x1", and batch 7 is a row until its own card closes

#### Scenario: One unit landed and another held again
- **WHEN** batch 6 holds `x1`, which has landed, and `y1`, which batch 8 holds again
- **THEN** batch 6 is no row, and crew's close says "its batch waits on nothing: x1 has landed; batch 8 holds a newer change of y1"

#### Scenario: A unit dropped
- **WHEN** batch 4 holds `x1` and `x2`, `x1` has landed, and `x2` is dropped from the plan after batch 4 was made, by `crew unit drop`, by a proposal the user approved, or with its bolt
- **THEN** batch 4 is no row, and crew's close says "its batch waits on nothing: x1 has landed; x2 was dropped"

#### Scenario: A unit dropped and added again before the batch
- **WHEN** unit `x1` was dropped, a unit of the same name was added again and constructed, and batch 10 then holds its change
- **THEN** the earlier drop does not close batch 10, which stays a row until its card closes, or until `x1` lands, is dropped again or a later batch holds it

#### Scenario: A bolt dropped with its units queued
- **WHEN** batch 11 holds `x1`, and `x1`'s bolt is dropped with `--requeue`, so `x1` goes back to the queue
- **THEN** `x1` was not dropped, and batch 11 stays a row until its card closes or a later batch holds `x1`

#### Scenario: One unit still waits on the user
- **WHEN** batch 9 holds `x1`, which has landed, and `y1`, which has not landed, has not been dropped and no later batch holds
- **THEN** batch 9 is a row as it is today, and its card is raised and closed as before

#### Scenario: Its card is already open
- **WHEN** crew posted `batch/12`'s card in the planner's name on the main-level host, and every unit of batch 12 has landed
- **THEN** the next rail read there withdraws the card "its batch waits on nothing: …" with the words of crew's close, records both, and says so in its sweep's lines

#### Scenario: The unit moves on again
- **WHEN** batch 7 held `x1` again after batch 5, and `x1` is then constructed a third time, its newest change in no batch yet
- **THEN** batch 5 stays closed and is no row, and `x1`'s newest change is due for the next batch

#### Scenario: Read again after the close
- **WHEN** crew's close of `batch/3` is recorded and the rail is read again
- **THEN** no second close is recorded, and nothing is posted under `batch/3`

#### Scenario: crew's close is not the user's answer
- **WHEN** batch 5 is closed by crew because batch 7 holds `x1`'s newer change, and batch 7's card is unanswered
- **THEN** `x1`'s bolt's landing row says it lands once you have answered batch 7, as before

#### Scenario: The record did not answer whole
- **WHEN** the drive's branch cannot be read, so its run record cannot be
- **THEN** the sweep records no close for any batch, says the drive was not swept, and names the branch

#### Scenario: A host does not answer
- **WHEN** macbook-pro, which holds a wldn operator session, does not answer a rail read
- **THEN** each batch is closed as far as the entries on `wldn/main` show it, as when every host answers

### Requirement: A batch is answered by the user's own words in a main-level pane
A batch SHALL also be answered by the user's own words in the planner's pane or the operator's pane of its drive. The agent in that pane SHALL run `crew card answer batch/<n> --excerpt "<the user's words>"`. crew SHALL record the batch answered only when it finds the words in that agent's own live session transcript, on the host where the command runs, in a record the session received and that crew reads as the user's under `signals.5`. That is typing in the pane, or a `crew tell` from `<user>@<host>`. A later echo of the same words, in a tool's output or a tell, SHALL NOT hide the user's record. crew SHALL refuse the command, recording no answer, in each of these cases:
- the words are not in the transcript, or are only in what the agent wrote itself;
- the record holding them is a tool's output, crew's own message, or another agent's tell;
- crew cannot read the transcript, or cannot tell that it is the live session's;
- the caller is not that drive's planner or operator;
- the run record holds no batch `n`;
- the batch was already answered, by a tap, its reading session's send, or a pane;
- the batch waits on nothing.

The answer SHALL be one run-record entry, `batch.answer`, on `batch/<n>`. It names the batch, the caller, its session, the transcript record the words were read from, and the words' length, and holds none of the words (`record.3`). The answer SHALL close every card key of batch `n` for good: a card posted under one of those keys afterwards does not open the batch again. Answering several batches in one sentence SHALL take one command per batch.

#### Scenario: Typed in the planner's pane
- **WHEN** the user types "Batch 13 is fine, approve it" in swancloud-planner's pane, and the planner runs `crew card answer batch/13 --excerpt "Batch 13 is fine, approve it"`
- **THEN** batch 13 is recorded answered, with no words in the run record, and the rail and the board have no row for it

#### Scenario: Through the rail's answer command
- **WHEN** the user runs `crew tell swancloud-planner "On batch 14: fine"` at a shell, and the planner runs `crew card answer batch/14 --excerpt "On batch 14: fine"`
- **THEN** batch 14 is recorded answered, since a tell from `<user>@<host>` is the user's

#### Scenario: The agent's own words
- **WHEN** the planner writes "the user approved batch 15" in its own reply and runs `crew card answer batch/15 --excerpt "the user approved batch 15"`
- **THEN** the command is refused, saying the words are not in a record the session received, and batch 15 is not answered

#### Scenario: Words another agent passed on
- **WHEN** swancloud-operator tells the planner "The user says batch 15 is fine", and the planner runs the command with those words
- **THEN** the command is refused, naming swancloud-operator as the one who said them, and batch 15 is not answered

#### Scenario: Already answered on its card
- **WHEN** the user tapped batch 13's card, and then the planner runs `crew card answer batch/13` with the user's words in its pane
- **THEN** the command is refused, saying batch 13 was answered already, and nothing is recorded

#### Scenario: Three batches in one sentence
- **WHEN** the user writes, in the planner's pane, one sentence approving batches 13, 14 and 15
- **THEN** the planner runs the command once for each batch with that sentence, and each batch is recorded answered on its own

### Requirement: A unit is batched once its change has landed on its bolt
A unit of a started bolt SHALL become due for review when the runner's records read it merged, its change read archived on GitHub's bolt after a fetch, and SHALL be named in its batch with its bolt at the commit of the bolt that holds it, `<unit>:<bolt>@<commit>`, its reading opening its archived folder. A note the user marks fix on such a unit SHALL reach its bolt as a fix place, by the planner's `crew fix`.

#### Scenario: Merged, then batched
- **WHEN** `a` of started `x` lands on `bolt/x` at `9f1c2ab`, its change archived there
- **THEN** `a` counts toward the drive's next batch, named `a:x@9f1c2ab`

#### Scenario: Constructed but not landed
- **WHEN** `b`'s construct has delivered and its place is in code
- **THEN** `b` is not yet due for review

### Requirement: A batch spans the drive's bolts
A batch SHALL hold the changes due across every bolt of a drive. A drive SHALL have a batch setting, a count N and a number of hours T, read from its entry in the teams file. A batch SHALL be due, at the rail's sweep on the drive's main-level host, when N changes are due across its bolts, or when T hours have passed since the drive's last batch and at least one change is due, whichever comes first.

#### Scenario: Changes from several bolts
- **WHEN** a drive's setting is 5 and 4 hours, and two units of bolt `x` and three of bolt `y` have been constructed since its last batch
- **THEN** a batch is due at the rail's next sweep on the main level's host, holding those five changes

#### Scenario: The time is reached
- **WHEN** two changes have been constructed across the drive's bolts since its last batch, four hours ago
- **THEN** a batch is due, holding those two

#### Scenario: Nothing due
- **WHEN** four hours have passed since the last batch and no change has been constructed since
- **THEN** no batch is due

#### Scenario: Swept on another host
- **WHEN** the rail's sweep runs on a host that is not wldn's main-level host
- **THEN** it reckons no batch for wldn

### Requirement: A batch is reckoned from the drive's branch, never a host
Whether a batch is due, what a review holds, and whether every unit's latest change of a bolt has been in a batch, SHALL be read from the run record on the drive's branch alone, asking no host for it. A host that does not answer SHALL hold none of them. When the branch cannot be read, each SHALL be refused naming the branch, as crew can't tell then which changes have been in a batch.

#### Scenario: The laptop asleep at the rail's sweep
- **WHEN** the rail's sweep on chuck-herdr-alpha, wldn's main-level host, runs while macbook-pro, which holds a wldn operator session, does not answer, and five changes are due
- **THEN** the sweep finds the batch due and the planner is told, and macbook-pro is not asked

#### Scenario: A review while the laptop is asleep
- **WHEN** the planner runs `crew review wldn` while macbook-pro does not answer and a batch is due
- **THEN** the reviewer is started on the batch's due changes, and no earlier batch's summary is returned in its place

#### Scenario: A landing while the laptop is off
- **WHEN** `crew bolt land` runs on mac-studio for a bolt whose every unit's latest change has been in a batch the user answered, while macbook-pro is off the tailnet
- **THEN** the bolt is closed as landed, and nothing names macbook-pro

#### Scenario: The branch cannot be read
- **WHEN** the rail's sweep runs while `wldn/main` cannot be fetched
- **THEN** whether a batch is due is not reckoned, and the sweep says crew can't tell which changes have been in a batch, naming `wldn/main` and why
