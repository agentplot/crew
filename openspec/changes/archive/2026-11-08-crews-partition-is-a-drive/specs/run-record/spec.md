## RENAMED Requirements

- FROM: `### Requirement: A send is one entry in the receiving partition's record`
- TO: `### Requirement: A send is one entry in the receiving drive's record`


## MODIFIED Requirements

### Requirement: Every command that moves work leaves an entry
Every crew command that changes the plan, a signal or its move, a unit's approval or stage, a fix, or an agent's or a team's sessions, and every `crew tell`, SHALL append one entry for each such act to the run record of the drive it acts for, after the act is done. A command that only reads SHALL append nothing. An entry SHALL give its id, the time in UTC, the host crew ran on, who asked, the act, and the objects it acted on.

#### Scenario: A plan write
- **WHEN** the planner adds a unit to the queue
- **THEN** the run record gains one entry whose act is `unit.add`, naming the unit and the queue it went to

#### Scenario: A command that does several things
- **WHEN** `crew bolt give swb-1` writes the plan, restarts the team's conductor and ops, and greets the conductor
- **THEN** the run record gains an entry for the give, one for each restart and one for the greeting

#### Scenario: A command that only reads
- **WHEN** `crew bolts`, `crew status` or `crew sites` runs
- **THEN** no entry is written

### Requirement: Entries can be followed as they are written
`crew events --follow` SHALL print each entry of the drive as it reaches the drive's branch, one line per entry, until it is interrupted. It SHALL read the branch as this host's cache holds it, read it again only when the cache's tip moves, and read again only the run-record files whose content changed. The branch SHALL be fetched once a minute, never faster: by the host's follower for a drive it follows, else by the follow itself. It SHALL ask no host for entries.

#### Scenario: Following a bolt team
- **WHEN** `crew events --follow --label wldn` is running and a conductor starts a stage on the box
- **THEN** that entry's line appears once its commit is on `wldn/main` and this host has fetched it, within a minute, without the command being run again

#### Scenario: A host is asleep
- **WHEN** `crew events --follow --label wldn` starts while macbook-pro does not answer
- **THEN** it follows the branch as before, and starts nothing on macbook-pro

#### Scenario: Nothing moves
- **WHEN** `crew events --follow --label wldn` runs on a host where no follower follows wldn, and nothing reaches wldn's branch
- **THEN** it fetches the branch once a minute and starts no other process

#### Scenario: The host's follower fetches
- **WHEN** `crew events --follow --label wldn` runs on mac-studio while mac-studio's follower follows wldn
- **THEN** the follow fetches nothing itself, and prints each entry once the follower's fetch, or a write on mac-studio, has moved the cache

### Requirement: A send is one entry in the receiving drive's record
Each `crew send` that reaches its operator SHALL append one entry, act `send`, to the run record of the drive it was sent to, on the host the command ran on. Its `By` SHALL be the sender, its `On` the operator, `agent/<label>-operator`, and the team, `team/<team>`, when a team was named; its `Why` SHALL be `send <team or drive>`; and its `Chars` the length of the text. It SHALL hold no part of the text, and no separate tell entry SHALL be written for it. A send that types nothing SHALL write no entry, as a tell that types nothing writes none.

#### Scenario: A send to a team
- **WHEN** `crw-5-unit-1` sends 46 characters to `swb-1`, a team of wldn
- **THEN** wldn's run record gains one entry: act `send`, `By: crw-5-unit-1`, `On: agent/wldn-operator`, `On: team/swb-1`, `Why: send swb-1`, `Chars: 46`, and the text appears nowhere in it

#### Scenario: A send that is refused
- **WHEN** a send fails because `wldn-operator` is not up
- **THEN** no entry is written

### Requirement: Every entry reaches the branch as it is written
Once crew appends an entry to the host's run record, the same command SHALL push it to `runs/<host>/<day>.rec` on the drive's branch of its state repository, as its own commit from that host, by the procedure every write to the branch takes. The commit SHALL change that day's file alone, adding the entry to what the branch holds. Only a host SHALL write its own files, entries SHALL be added and never removed, and pushing an entry the branch holds SHALL change nothing.

#### Scenario: A tell
- **WHEN** an agent on the box tells another agent
- **THEN** before the command returns, `wldn/main` has a commit from the box adding the tell's entry to `runs/chuck-herdr-alpha/<day>.rec`, and no other file

#### Scenario: A plan write
- **WHEN** the planner adds a unit to the queue on mac-studio
- **THEN** the write's commit changes the plan alone, and the next commit on the branch adds its `unit.add` entry, which names the write's commit

#### Scenario: Two hosts at once
- **WHEN** mac-studio and the box each push an entry of wldn at the same moment
- **THEN** both entries are on `wldn/main`, each in its host's file, the one whose push was refused replayed on the new tip

#### Scenario: A host is rebuilt
- **WHEN** a host loses its local run record
- **THEN** every entry it wrote before is still on the branch, and its next entry is added beside them

### Requirement: An entry that did not reach the branch goes with the host's next
When an entry cannot be pushed, crew SHALL say so once on standard error, naming the entry, the branch and why, and the command SHALL do its work and exit as it would have. The entry SHALL stay in the host's file. The host's next push of the drive's record, by its next entry or by `crew events --push`, SHALL first push each of the host's entries the branch lacks, each as its own commit, oldest first. `crew events --push` SHALL say when the branch already holds every entry the host has.

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

### Requirement: Entries are read from the drive's branch alone
`crew events [--label <label>] [--about <object>] [--since <time>] [--json]` and `crew trace <object>` SHALL read the run record from the drive's branch of its state repository, and SHALL ask no host for it. When the branch cannot be read they SHALL say so, naming the branch.

#### Scenario: A host is asleep
- **WHEN** macbook-pro, which wrote entries of wldn and pushed them, does not answer
- **THEN** `crew events --label wldn` prints its entries with the other hosts' in time order, and names no host

#### Scenario: Two hosts
- **WHEN** `crew events --label wldn` runs on mac-studio while wldn's teams run on the box
- **THEN** the box's entries and mac-studio's are printed together in time order, and no ssh is made for them

#### Scenario: One object
- **WHEN** `crew events --about unit/<unit>` runs
- **THEN** only entries naming that unit in `On` or `From` are printed

#### Scenario: The branch cannot be read
- **WHEN** `crew events --label wldn` runs while the state repository cannot be fetched
- **THEN** it names `wldn/main` as not read, and why

### Requirement: An ask and a turn are entries
Each ask crew writes SHALL be one `ask` entry in the asked drive's record, naming the role's run and the record the ask names, with the length of its words and never their text. A run's start SHALL be one `turn.begin` entry naming the run and how many it took, and its end one `turn.end` entry. `crew trace agent/<label>-<role>` SHALL list them with the rest of the role's entries.

#### Scenario: A tell that is an ask
- **WHEN** `crew tell madswan-planner "<forty characters>"` is written as an ask
- **THEN** madswan's record holds an `ask` entry on `agent/madswan-planner` with `Chars: 40` and not the text

#### Scenario: A turn traced
- **WHEN** the planner's run took two asks and ended
- **THEN** `crew trace agent/madswan-planner` lists the two asks, the `turn.begin` taking two and the `turn.end`

### Requirement: A kit's rename is one entry naming both its names
`crew kit rename` SHALL leave one `kit.rename` entry per act, done or refused. The entry SHALL name the repository by its new name, `On: kit/<new>`, and by the name it had, `From: kit/<old>`, with `proposal/<n>` beside it when a proposal's approval applies the rename. Its `Repo` SHALL be the new name and its `Count` the number of records the rename renamed, all files together. The rename's commit SHALL name the entry in its `Crew-Entry`, and the entry SHALL reach the branch as the commit after. It SHALL hold no text anyone typed. The entry SHALL be the record of the act alone: no `kit.rename` entry, done or refused, SHALL rename anything crew reads, a later rename SHALL leave it as written, and `crew events` and `crew trace` SHALL print it as written. An entry already written SHALL stay valid under the run record's descriptor, so a branch holding one takes every write.

#### Scenario: The entry of a rename
- **WHEN** the user runs `crew kit rename tailrace timber --label madswan`, renaming a Source, two requests and five entries
- **THEN** madswan's run record holds one `kit.rename` entry with `On: kit/timber`, `From: kit/tailrace`, `Repo: timber` and `Count: 8`, its commit's `Crew-Entry` naming it, and the day file holding it passes `recfix --check`

#### Scenario: A refused rename renames nothing
- **WHEN** a rename of `tailrace` to `timber` is refused because deneb's runner still keeps `agentplot/tailrace`
- **THEN** its entry is a refusal, and every record that named `tailrace` still does

#### Scenario: A rename's entry renames nothing
- **WHEN** a tip's run record holds a `bolt.land` under `tailrace` and, after it, a done `kit.rename` entry of `tailrace` to `timber` that a rename made before this change left
- **THEN** the landings at that tip are that one `bolt.land`, read in one read of the run record, and the drive's kits name `tailrace` as written

#### Scenario: A later rename leaves it
- **WHEN** the run record holds a `kit.rename` of `tailrace` to `timber`, and the user later renames `timber` to `trc`
- **THEN** the first entry still says `On: kit/timber`, `From: kit/tailrace` and `Repo: timber`
