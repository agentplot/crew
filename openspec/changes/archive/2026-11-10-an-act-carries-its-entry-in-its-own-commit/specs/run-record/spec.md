## MODIFIED Requirements

### Requirement: Every command that moves work leaves an entry
Every crew command that changes the plan, a signal or its move, a unit's approval or stage, a fix, or an agent's or a team's sessions, and every `crew tell`, SHALL append one entry for each such act to its drive's run record. The entry SHALL be in the act's own commit where the act writes the drive's branch, else appended once the act is done. A command that only reads SHALL append nothing. An entry SHALL give its id, the UTC time, the host, who asked, the act and the objects acted on.

#### Scenario: A plan write
- **WHEN** the planner adds a unit to the queue
- **THEN** the run record gains one entry whose act is `unit.add`, naming the unit and the queue it went to, in the write's own commit

#### Scenario: A command that does several things
- **WHEN** `crew bolt give swb-1` writes the plan, restarts the team's conductor and ops, and greets the conductor
- **THEN** the run record gains an entry for the give, one for each restart and one for the greeting

#### Scenario: A command that only reads
- **WHEN** `crew bolts`, `crew status` or `crew sites` runs
- **THEN** no entry is written

### Requirement: An entry names the commit it wrote
When an act writes a commit outside the drive's branch, such as the kit's commit for an approval, its entry SHALL name it as `<owner>/<name>@<sha>`. An act whose write is a commit crew makes on the drive's branch SHALL name no commit of its own, since that commit carries its entry. A state init that adopts another branch's history SHALL name the tip it adopted. An act that wrote no commit SHALL carry none.

#### Scenario: An approval
- **WHEN** `crew unit approve` records the review on `unit/<unit>`
- **THEN** the entry names the kit and that commit

#### Scenario: A plan write
- **WHEN** the planner adds a bolt to the plan
- **THEN** its `bolt.new` entry names no `Commit`, and the write's commit on the drive's branch adds it

#### Scenario: A tell
- **WHEN** `crew tell` prompts an agent
- **THEN** the entry carries no commit

### Requirement: Every entry reaches the branch as it is written
An entry of an act that writes the drive's branch SHALL reach the branch in that act's commit. The same command SHALL push any other entry to `runs/<host>/<day>.rec` on the branch as its own commit from that host. That push SHALL follow the procedure every write to the branch takes and change that day's file alone. Only a host SHALL write its own files. Entries SHALL be added and never removed, and pushing an entry the branch holds SHALL change nothing.

#### Scenario: A tell
- **WHEN** an agent on the box tells another agent
- **THEN** before the command returns, `wldn/main` has a commit from the box adding the tell's entry to `runs/chuck-herdr-alpha/<day>.rec`, and no other file

#### Scenario: A plan write
- **WHEN** the planner adds a unit to the queue on mac-studio
- **THEN** the write's one commit changes the plan and adds its `unit.add` entry to `runs/mac-studio/<day>.rec`, and no commit follows it for that entry

#### Scenario: Two hosts at once
- **WHEN** mac-studio and the box each push an entry of wldn at the same moment
- **THEN** both entries are on `wldn/main`, each in its host's file, the one whose push was refused replayed on the new tip

#### Scenario: A host is rebuilt
- **WHEN** a host loses its local run record
- **THEN** every entry it wrote before is still on the branch, and its next entry is added beside them

### Requirement: An entry that did not reach the branch goes with the host's next
When an entry can't be pushed, crew SHALL say so once on standard error, naming the entry, the branch and why, and the command SHALL do its work and exit as it would have. The entry SHALL stay in the host's file. The host's next push of the record SHALL push each entry the branch lacks, each as its own commit, oldest first, whether that push is its next entry's, its next write's or `crew events --push`'s. `crew events --push` SHALL say when the branch holds every entry the host has.

#### Scenario: GitHub out of reach
- **WHEN** a conductor on the box starts a stage while github.com cannot be reached
- **THEN** the stage starts, the command says once that its entry did not reach `wldn/main` and why, and the entry is in the box's file

#### Scenario: A branch too busy to take the entry
- **WHEN** the branch moves before every push of an entry, through its last replay
- **THEN** the command says once that the entry did not reach the branch because it kept moving, the entry stays in the host's file, and the host's next push, once the branch takes it, pushes it

#### Scenario: The next entry
- **WHEN** the box's next entry of wldn is pushed once github.com answers again
- **THEN** `wldn/main` gains the missed entry's commit, then the new entry's, and nothing is pushed twice

#### Scenario: The next write
- **WHEN** mac-studio writes the plan after a tell whose entry did not reach `wldn/main`
- **THEN** the write's commit adds the write's entry and not the tell's, the tell's entry follows as a commit of its own, and nothing is pushed twice

#### Scenario: By hand
- **WHEN** `crew events --push --label wldn` runs on the box after a missed push
- **THEN** each entry the branch lacks is pushed as its own commit, and run again it says there is nothing left to push

#### Scenario: An entry that fails its check
- **WHEN** an entry in the host's file is cut short, so the day's file would fail `recfix --check`
- **THEN** nothing of the record is pushed, the command names the file and why on standard error, and the act it recorded stands

#### Scenario: A write after an entry that fails its check
- **WHEN** the host's file holds an entry cut short and the host then writes the plan
- **THEN** the write lands with its own entry in its commit, and the command names the file and why on standard error

### Requirement: A rename's entry reaches the branch and stands there as written
The rename's commit SHALL add the `kit.rename` entry to the run record as its rewrite left it, and SHALL name the entry in its `Crew-Entry`. The entry SHALL be the record of the act alone. No `kit.rename` entry, done or refused, SHALL rename anything crew reads, and a later rename SHALL leave it as written. `crew events` and `crew trace` SHALL print it as written. An entry already written SHALL stay valid under the run record's descriptor, so a branch holding one takes every write.

#### Scenario: The rename's one commit
- **WHEN** the user renames `tailrace` to `timber` while the host's day file on the branch holds a `bolt.land` entry under `tailrace`
- **THEN** one commit renames that entry's `Repo` to `timber` and adds the `kit.rename` entry beside it, with `From: kit/tailrace` as written

#### Scenario: A rename's entry renames nothing
- **WHEN** a tip's run record holds a `bolt.land` under `tailrace` and, after it, a done `kit.rename` entry of `tailrace` to `timber` that a rename made before this change left
- **THEN** the landings at that tip are that one `bolt.land`, read in one read of the run record, and the drive's kits name `tailrace` as written

#### Scenario: A later rename leaves it
- **WHEN** the run record holds a `kit.rename` of `tailrace` to `timber`, and the user later renames `timber` to `trc`
- **THEN** the first entry still says `On: kit/timber`, `From: kit/tailrace` and `Repo: timber`
