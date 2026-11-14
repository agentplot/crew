# run-record Specification

## Purpose
Keeps a record of every act of crew's that moves work, written where the act happened, so that a person can read what happened to a bolt, a unit or a signal, who did it and what it led to, without asking an agent.

## Requirements

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

### Requirement: An entry names who asked and the session behind it
An entry's `By` SHALL be the name of the agent crew started that ran the command, else `<user>@<host>`. Its `Session` SHALL be the host and the Claude session id herdr reports for that agent when the command runs, and SHALL be absent for the user at a shell or when herdr reports none. A command crew runs again on another host SHALL carry both there, so the entry names the one who asked and not the host that did the work.

#### Scenario: A conductor's command
- **WHEN** `swb-2-conductor` on the box starts a unit's construct stage
- **THEN** the entry's `By` is `swb-2-conductor` and its `Session` is the box and that conductor's Claude session id

#### Scenario: The user at a shell
- **WHEN** the user runs `crew unit approve` in a terminal on mac-studio
- **THEN** the entry's `By` is `chuck@mac-studio` and it has no `Session`

#### Scenario: A command run on another host
- **WHEN** the operator agent on mac-studio runs `crew unit run` for a team on the box
- **THEN** the entry is written on the box, its `Host` is the box, and its `By` and `Session` name the operator agent and its session on mac-studio

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

### Requirement: An entry names what it acted on and what that came from
An entry's `On` fields SHALL name each object the act touched, and its `From` fields each object the act came from, as typed names: `unit/<unit>`, `chore/<chore>`, `bolt/<bolt>`, `queue/<kit>`, `signals/<id>`, `team/<team>`, `agent/<name>`, `stage/<unit or chore>/<stage>`, `fix/<bolt>/<name>`.

#### Scenario: A unit queued from a signal
- **WHEN** a unit is added with `--signal <id>`
- **THEN** the `unit.add` entry has `On: unit/<unit>` and `From: signals/<id>`, and the route move's entry has `On: signals/<id>` and `On: unit/<unit>`

#### Scenario: A stage
- **WHEN** a unit's code stage starts in slot 2 of swb-1
- **THEN** the entry has `On: stage/<unit>/code`, `On: unit/<unit>` and `On: agent/swb-1-unit-2`

#### Scenario: A chore's stage
- **WHEN** a chore's verify starts in slot 1 of swb-1
- **THEN** the entry has `On: stage/<chore>/verify`, `On: chore/<chore>` and `On: agent/swb-1-unit-1`

### Requirement: A refusal is an entry
When crew refuses a command that would have moved work, it SHALL append an entry with the act refused, the objects named and crew's reason in `Refused`.

#### Scenario: Code before review
- **WHEN** `crew unit run <unit> code` is refused because the unit is in review
- **THEN** the run record gains an entry with act `stage.start`, `On: unit/<unit>`, and the refusal's words in `Refused`

### Requirement: An entry holds no text anyone typed
An entry's `Why` SHALL be the subject crew itself composes from the names of things. An entry SHALL NOT hold the text of a tell, the words given to a stage, an intent, a goal, a reason or an excerpt. A tell's entry SHALL record the sender, the recipient and the length of the text.

#### Scenario: A tell
- **WHEN** a conductor tells the design agent a question in the user's words
- **THEN** the entry names both agents and the number of characters sent, and the question appears nowhere in the run record

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

### Requirement: One object's history is read from the entries alone
`crew trace <object>` SHALL print, in time order, every entry that names the object, and every entry of the objects it came from and the objects that came from it, each line giving the time, the act, who asked, the host, the commit, and the session to open. It SHALL read only the run record. An object no entry names SHALL be reported as such with a non-zero exit.

#### Scenario: A unit from a signal
- **WHEN** `crew trace unit/<unit>` runs for a unit queued from a signal and since merged
- **THEN** it prints the signal's capture, its route, the unit's add, each stage's start and end, the approval and the merge, in order

#### Scenario: A signal
- **WHEN** `crew trace signals/<id>` runs
- **THEN** it prints the same chain, starting from the signal

#### Scenario: Nothing recorded
- **WHEN** `crew trace unit/<unit>` names a unit no entry mentions
- **THEN** it says so and exits non-zero

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

### Requirement: A land crew posts is one entry naming its request
Each `land` crew posts on the user's send of a kit's landings card SHALL be recorded as one entry for each row it lands: `bolt.submit` on `bolt/<bolt>` for a bolt's row, and `fix.merge` on `fix/main/<kit>/<name>` for a fix of main's. Each SHALL carry `Outcome: asked`, the card's id as `Card`, the head the send ticked as `Head`, the land's number in `requests.rec` as `Request` (record 0056), and no `Submission`. A land SHALL be recorded once, however often its send is read.

#### Scenario: Two rows sent
- **WHEN** the user's send of `land/crew` ticks `y` at `abc1234` and `z` at `def5678`, and the card's raise posts lands 57 and 58 of their launches
- **THEN** the run record holds a `bolt.submit` on `bolt/y` with `Outcome: asked`, the card's id as `Card`, `Head` `abc1234`'s commit and `Request: 57`, and one on `bolt/z` with `Request: 58`; neither carries a `Submission`

#### Scenario: A fix of main's row sent
- **WHEN** the user's send of `land/tailrace` ticks the fix of main `cargo-lock`, and the raise posts land 61 of its launch
- **THEN** the run record holds a `fix.merge` on `fix/main/tailrace/cargo-lock` with `Outcome: asked`, the card's id as `Card`, the head the send ticked as `Head` and `Request: 61`

#### Scenario: The send read again
- **WHEN** the card's raise runs again on the same send, `y`'s head unchanged and its land 57 not answered
- **THEN** no land is posted and no entry is written

### Requirement: A landing's Submission is the merge queue's entry Flume names
A `bolt.submit` entry's `Submission` SHALL be only the merge queue's entry that Flume's status of the bolt's base place names, as the runner carries it. The outcome of a land, recorded as bolt-teams "A landing is recorded by the first act that reads it in the runner's report" has it, SHALL carry that entry where Flume names one, and none where it names none. crew SHALL write no `Submission` it made or read from anything but Flume's status.

#### Scenario: A landing whose entry Flume names
- **WHEN** the runner carries `y`'s base place over, landed at `9f1c2ab`, its submission entry 412, and crew records `y`'s land landed
- **THEN** that `bolt.submit` on `bolt/y` carries `Submission: 412`

#### Scenario: A land the runner refused
- **WHEN** the runner answered land 57 of `y` refused because a place on `bolt/y` is live, Flume naming no submission, and crew records it stopped
- **THEN** that `bolt.submit` on `bolt/y` carries no `Submission`

### Requirement: The run record's descriptor allows a land's request
The run record's descriptor SHALL allow `Request`. A day's file begun under a descriptor without it SHALL take the field all the same, its entries reaching the branch under the descriptor that allows it. A `bolt.submit` an older crew wrote, queued with sluice's number among them, SHALL be read as it was written.

#### Scenario: A day's file an older crew began
- **WHEN** the host's day file was begun under a descriptor that allows no `Request`, and crew records an asked `bolt.submit` with `Request: 57` in it
- **THEN** `recsel` reads `Request: 57` from the file, and the day's file pushed to the branch carries the descriptor that allows it and passes `recfix --check`

#### Scenario: An entry an older crew wrote
- **WHEN** the run record holds a `bolt.submit` of `x` an older crew wrote, `Outcome: queued` and `Submission: 355`
- **THEN** `crew events` prints it as written, `Submission: 355` among it

### Requirement: A bolt's landing entry records its time by holder from the run record
Every `bolt.land` entry crew writes SHALL record the bolt's age in whole minutes, from its newest `bolt.start`, or an older crew's `bolt.give`, to the entry's own time, as `Age`, and the minutes each holder held, as `Split`, in the order team, kit, team-or-kit, user, hold, nobody, each named with its minutes. The split SHALL be the board's head line's, from the run record alone, summing to `Age`. With no start to read, the entry SHALL carry neither field, and the landing SHALL close.

#### Scenario: A bolt lands
- **WHEN** crew closes the landing of `b`, started 6h 10m before it records `b` landed, with its work holding it 3h 45m, the user 2h 05m, a hold 0 and nobody 20m
- **THEN** its `bolt.land` entry holds `Age: 370` and `Split: team 225, kit 0, team-or-kit 0, user 125, hold 0, nobody 20`

#### Scenario: No record of sluice's is read
- **WHEN** `b`'s landing is recorded, and the runner carried its unit `a`'s submission `#41` under test for seventeen minutes of its age
- **THEN** no sluice process starts and no host is asked, those minutes are placed as the board's head line places them, by no submission, and `Split` sums to `Age`

#### Scenario: The start can't be read
- **WHEN** the run record holds no start of `b` within the days crew reads as `b`'s landing is recorded
- **THEN** the `bolt.land` entry is written without `Age` and `Split`, and the landing is closed

### Requirement: A host's run record is recutils files it appends to and never rewrites
Entries SHALL be recutils records in `~/.local/state/crew/<label>/runs/<host>/<date>.rec` on the host where the command ran, one file per UTC day, each append one write. crew SHALL never rewrite or remove an entry in a host's file. A failed append SHALL be reported on standard error and SHALL NOT change the command's result or exit status.

#### Scenario: After a restart
- **WHEN** a host restarts
- **THEN** every entry written before it is still in its file

#### Scenario: The record cannot be written
- **WHEN** the run record's directory cannot be written
- **THEN** the command does its work and exits as it would have, with one line on standard error saying the entry was not recorded

#### Scenario: Read with recutils alone
- **WHEN** `recsel -e "On = 'unit/<unit>'"` is run over a host's run-record files
- **THEN** it prints that unit's entries, with no crew command involved

### Requirement: Only a kit's rename rewrites the branch's copy of an entry
The drive's branch's copy of an entry SHALL be rewritten only by `crew kit rename`, and only to rename a repository's name, in the rename's one commit, which holds what each entry said before.

#### Scenario: A rename's rewrite
- **WHEN** the user renames `tailrace` to `timber` and the branch's run record holds a `bolt.land` entry with `Repo: tailrace`
- **THEN** the rename's commit changes that entry's `Repo` to `timber` and its parent holds it as it was, and the file on the host that wrote it still says `tailrace`

### Requirement: A send that reaches its operator appends one entry naming the sender and the operator
Each `crew send` that reaches its operator SHALL append one entry, act `send`, to the run record of the drive it was sent to, on the host the command ran on. Its `By` SHALL be the sender, its `On` the operator, `agent/<label>-operator`, and the team, `team/<team>`, when a team was named; its `Why` SHALL be `send <team or drive>`; and its `Chars` the length of the text. It SHALL hold no part of the text, and no separate tell entry SHALL be written for it.

#### Scenario: A send to a team
- **WHEN** `crw-5-unit-1` sends 46 characters to `swb-1`, a team of wldn
- **THEN** wldn's run record gains one entry: act `send`, `By: crw-5-unit-1`, `On: agent/wldn-operator`, `On: team/swb-1`, `Why: send swb-1`, `Chars: 46`, and the text appears nowhere in it

### Requirement: A send that types nothing writes no entry
A `crew send` that types nothing SHALL write no entry, as a tell that types nothing writes none.

#### Scenario: A send that is refused
- **WHEN** a send fails because `wldn-operator` is not up
- **THEN** no entry is written

### Requirement: A kit's rename leaves one entry naming its new and old names
`crew kit rename` SHALL leave one `kit.rename` entry per act, done or refused. The entry SHALL name the repository by its new name, `On: kit/<new>`, and by the name it had, `From: kit/<old>`, with `proposal/<n>` beside it when a proposal's approval applies the rename. Its `Repo` SHALL be the new name and its `Count` the number of records the rename renamed, all files together. It SHALL hold no text anyone typed.

#### Scenario: The entry of a rename
- **WHEN** the user runs `crew kit rename tailrace timber --label madswan`, renaming a Source, two requests and five entries
- **THEN** madswan's run record holds one `kit.rename` entry with `On: kit/timber`, `From: kit/tailrace`, `Repo: timber` and `Count: 8`, its commit's `Crew-Entry` naming it, and the day file holding it passes `recfix --check`

#### Scenario: A refused rename renames nothing
- **WHEN** a rename of `tailrace` to `timber` is refused because deneb's runner still keeps `agentplot/tailrace`
- **THEN** its entry is a refusal, and every record that named `tailrace` still does

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

### Requirement: A land crew posts on proof is one entry marked as on proof
Each `land` crew posts on proof SHALL be recorded as one `bolt.submit` on `bolt/<bolt>` carrying `Outcome: asked`, `Form: proof`, the head it was posted at as `Head` and the land's number in `requests.rec` as `Request`, with no `Card` and no `Submission`. A land SHALL be recorded once, however often the bolt is read proven at that head.

#### Scenario: A land on proof
- **WHEN** the raise of `land/crew` posts land 63 of `y`'s launch on proof at `abc1234`
- **THEN** the run record holds a `bolt.submit` on `bolt/y` with `Outcome: asked`, `Form: proof`, `Head` `abc1234`'s commit and `Request: 63`, and no `Card` or `Submission`

#### Scenario: Read proven again
- **WHEN** a later raise reads `y` proven at `abc1234`, land 63 not answered
- **THEN** no land is posted and no entry is written

### Requirement: The mark's lift and the holds each leave one entry holding none of their words
`crew bolt unstay` SHALL leave one `bolt.unstay` entry on `bolt/<bolt>`. `crew plan hold` and `crew plan go` SHALL each leave one entry, `plan.hold` or `plan.go`, on `kit/<kit>` for a kit's hold and on `plan/<label>` for the drive's. None SHALL hold the hold's words or the user's (`record.3`).

#### Scenario: A hold and its lift
- **WHEN** the user runs `crew plan hold "Cutover" --repo crew --label swancloud` and later `crew plan go --repo crew --label swancloud`
- **THEN** the run record holds a `plan.hold` and then a `plan.go`, each on `kit/crew`, and neither holds the word "Cutover"

### Requirement: A send's entry is pushed from the sending host
The entry of a `crew send` SHALL be appended to the sending host's own file of the receiving drive's record, and pushed from that host, with its own sign-in, as its own commit on the receiving drive's branch. A push that is refused SHALL keep the entry in that file, said once, and SHALL leave the send reported as made.

#### Scenario: A send from a box
- **WHEN** `wldn-planner` on chuck-herdr-alpha sends to swancloud, whose operator runs on mac-studio
- **THEN** chuck-herdr-alpha's own file of swancloud's record holds the `send` entry, mac-studio's holds none, and swancloud's branch gains it as the commit `runs(chuck-herdr-alpha): send agent/swancloud-operator (wldn-planner)`

#### Scenario: A refused push
- **WHEN** a send is typed into its operator and the push of its entry is refused
- **THEN** the entry stays in the sending host's file, the refusal is said once, and `crew send` reports the send made
