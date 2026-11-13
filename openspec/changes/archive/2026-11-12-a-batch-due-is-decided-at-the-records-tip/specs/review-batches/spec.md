## ADDED Requirements

### Requirement: A batch due is decided at the run record's tip as the planner is told
Before crew tells a drive's planner a batch is due, it SHALL decide again from the run record at the tip of the drive's branch, fetched then, so a batch delivered since the read it reckoned from leaves nothing due that the batch held. When the tip cannot be read, crew SHALL tell nothing, say why, and try again at the follower's next tick. A `batch.due` entry SHALL name each change it tells of, as `<unit>:<bolt>@<commit>`.

#### Scenario: A batch delivered between the read and the tell
- **WHEN** the follower's read finds five of wldn's changes due, and batch 7, holding those five, reaches wldn's branch before the planner is told
- **THEN** wldn's planner is not told and no `batch.due` is recorded, and once later changes make a batch due, the planner is told of them

#### Scenario: The tip cannot be read
- **WHEN** the follower's read finds a batch of wldn's due and `wldn/main` cannot be fetched
- **THEN** the planner is not told, crew says why, and the follower reckons wldn's batch again at its clock's next tick

### Requirement: A tell keeps the next one back only while its changes are due
A `batch.due` entry after a drive's last batch SHALL keep the next tell back only while a change it names is still due. An entry naming only changes a batch has since held, or that are no longer due, SHALL keep nothing back. An entry written before a `batch.due` named its changes SHALL be judged by the units it names.

#### Scenario: A tell that stands
- **WHEN** wldn's planner was told of five due changes and no batch has been delivered since
- **THEN** the planner is not told again while one of those five is still due

#### Scenario: An entry naming only changes a batch held
- **WHEN** wldn's record holds, after batch 7, a `batch.due` naming only changes batch 7 held, and five changes made since are due
- **THEN** wldn's planner is told a batch of the five is due
