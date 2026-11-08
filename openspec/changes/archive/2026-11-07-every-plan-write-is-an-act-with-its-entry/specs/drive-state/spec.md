## MODIFIED Requirements

### Requirement: A commit names its run-record entry
Each commit crew makes on a drive's branch SHALL carry, in its message, the id of a run-record entry as a `Crew-Entry:` trailer. A commit that is an act's, such as a plan write, SHALL name the entry that describes it, and that entry SHALL name the commit. A commit that adds an entry to the run record SHALL name the entry it adds, and SHALL change nothing but that entry's day file. Every plan write SHALL be an act: the write SHALL record the entry its commit names and push that entry's commit before it returns, and crew SHALL refuse a write that names no act, before it reads or pushes anything, since its commit would name an entry nothing writes.

#### Scenario: From a commit to its entry
- **WHEN** a plan write's commit on `wldn/main` is read
- **THEN** its `Crew-Entry` id is the `Id` of one run-record entry, whose `Commit` is that commit

#### Scenario: An entry's own commit
- **WHEN** the commit that follows a plan write on `wldn/main` is read
- **THEN** its `Crew-Entry` id is the `Id` of the entry it adds to `runs/<host>/<day>.rec`, its subject ends with ` (<agent>)`, and it changes no other file

#### Scenario: Once a write returns
- **WHEN** a plan write on `wldn/main` returns, its push accepted
- **THEN** the branch's tip is the commit adding the write's entry, whose parent is the write's commit, and a decision then reads the branch at that tip

#### Scenario: A write that names no act
- **WHEN** crew is asked to write the plan with no act
- **THEN** it refuses, naming the write, and the branch is where it was

## ADDED Requirements

### Requirement: A decision reads an act whole and says when it read below the tip
A decision SHALL read a drive's branch at its tip, or, while one of its newest twenty first-parent commits names a run-record entry the tip lacks, at the parent of the oldest such commit. A command that read the branch below its tip SHALL say so, naming the commit it read at, the tip, the write it waits on and that write's agent, on the line before its refusal and on standard error after its answer.

#### Scenario: A write whose entry has not arrived
- **WHEN** `wldn/main` holds a write by `swb-1-conductor` whose entry the branch lacks, and the planner's proposal 6 was written after it
- **THEN** `crew plan proposed 6` refuses, its line before the refusal saying `wldn/main was read at <the write's parent>, below its tip <the tip>: the write <the write> by swb-1-conductor is on the branch without its run-record entry yet, so nothing from <the write> on was read (read.5)`, and its last line `no proposal 6 in wldn/main`

#### Scenario: An answer read below the tip
- **WHEN** a command that read the branch below its tip answers without refusing
- **THEN** it says on standard error where it read the branch and the write it waits on, and nothing of it on standard output

#### Scenario: The entry arrives
- **WHEN** the write's entry reaches the branch
- **THEN** `crew plan proposed 6` reads the tip, prints proposal 6, and says nothing of a read below the tip
