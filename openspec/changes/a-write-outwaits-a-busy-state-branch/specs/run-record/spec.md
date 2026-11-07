## MODIFIED Requirements

### Requirement: An entry that did not reach the branch goes with the host's next
When an entry cannot be pushed, crew SHALL say so once on standard error, naming the entry, the branch and why, and the command SHALL do its work and exit as it would have. An entry whose every replay is refused because the branch kept moving SHALL be treated so too. The entry SHALL stay in the host's file. The host's next push of the partition's record, by its next entry or by `crew events --push`, SHALL first push each of the host's entries the branch lacks, each as its own commit, oldest first. `crew events --push` SHALL say when the branch already holds every entry the host has.

#### Scenario: GitHub out of reach
- **WHEN** a conductor on the box starts a stage while github.com cannot be reached
- **THEN** the stage starts, the command says once that its entry did not reach `wldn/main` and why, and the entry is in the box's file

#### Scenario: A branch too busy to take the entry
- **WHEN** the branch moves before every push of an entry, through its last replay
- **THEN** the command says once that the entry did not reach the branch because it kept moving, the entry stays in the host's file, and the host's next push, once the branch takes it, pushes it

#### Scenario: The next entry
- **WHEN** the box's next entry of wldn is pushed once github.com answers again
- **THEN** `wldn/main` gains the missed entry's commit, then the new entry's, and nothing is pushed twice

#### Scenario: By hand
- **WHEN** `crew events --push --label wldn` runs on the box after a missed push
- **THEN** each entry the branch lacks is pushed as its own commit, and run again it says there is nothing left to push

#### Scenario: An entry that fails its check
- **WHEN** an entry in the host's file is cut short, so the day's file would fail `recfix --check`
- **THEN** nothing of the record is pushed, the command names the file and why on standard error, and the act it recorded stands
