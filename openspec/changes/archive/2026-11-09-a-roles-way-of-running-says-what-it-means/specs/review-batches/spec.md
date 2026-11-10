## MODIFIED Requirements

### Requirement: A batch spans the drive's bolts
A batch SHALL hold the changes due across every bolt of a drive. A drive SHALL have a batch setting, read from its entry in the teams file as `review`: `after_changes`, a count of changes, a whole number of at least 1, and `after_hours`, a number of hours above 0. A batch SHALL be due, at the rail's sweep on the drive's main-level host, once `after_changes` changes are due across its bolts, or once `after_hours` hours have passed since the drive's last batch and at least one change is due, whichever comes first. What crew says of a batch made due SHALL name the setting it reached in those units.

#### Scenario: Changes from several bolts
- **WHEN** a drive's `review` gives `after_changes` 5 and `after_hours` 4, and two units of bolt `x` and three of bolt `y` have been constructed since its last batch
- **THEN** a batch is due at the rail's next sweep on the main level's host, holding those five changes, and crew says five changes are due and a batch is due after 5

#### Scenario: The time is reached
- **WHEN** the drive's `after_hours` is 4, and two changes have been constructed across the drive's bolts since its last batch, four hours ago
- **THEN** a batch is due, holding those two, and crew says 4 hours have passed since the last batch

#### Scenario: Nothing due
- **WHEN** four hours have passed since the last batch and no change has been constructed since
- **THEN** no batch is due

#### Scenario: Swept on another host
- **WHEN** the rail's sweep runs on a host that is not wldn's main-level host
- **THEN** it reckons no batch for wldn
