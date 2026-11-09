# drive-state Specification

## Purpose
Keeps each drive's own records (its plan, its moves, its run record, and what later capabilities add) in a state repository apart from the design, on a branch of its own, written only through crew, so that several drives can share one repository without meeting.

## Requirements

### Requirement: A drive's state is one branch of its state repository
Each drive SHALL name one state repository in the teams file, as `state`. The drive SHALL keep its state as files on the branch `<label>/main` of that repository. The branch SHALL hold no other drive's files and SHALL share no history with another drive's branch.

#### Scenario: Willdan's drive
- **WHEN** the `wldn` drive names `WilldanGroup/crew-state` as its state repository
- **THEN** its plan, moves and run record are files on the branch `wldn/main` of that repository

#### Scenario: Two drives of one organisation
- **WHEN** `madswan` and `swancloud` both name `afterthought/crew-state`
- **THEN** each has its own branch, `madswan/main` and `swancloud/main`, and neither branch holds a commit of the other's

### Requirement: The state is written only through crew, one commit a write
Every write to a drive's branch SHALL be made by a crew command. It SHALL fetch the branch over https into crew's own bare cache, apply itself to the tip, check each file it changed, commit without touching any working tree, and push without force. A push rejected because the branch moved SHALL have the write applied again to the new tip, up to six times, after a growing wait before each replay's fetch, 23.5 seconds in all at most. A write that changes several files SHALL be one commit.

#### Scenario: Two hosts write at once
- **WHEN** a write from the box and a write from mac-studio reach the same drive's branch together
- **THEN** both land, one after the other, and nothing is merged

#### Scenario: Each replay waits longer
- **WHEN** a write's push is refused for the nth time and a replay follows
- **THEN** it waits between half and all of the nth of 0.5, 1, 2, 4, 8 and 8 seconds, drawn afresh, before it fetches the branch again, so writers refused at one moment replay apart

#### Scenario: A busy branch is outwaited
- **WHEN** another writer moves the branch before each of a write's first three pushes
- **THEN** the write waits before each fresh fetch, each wait longer than the one before, and lands on its fourth push on top of the other writer's last commit

#### Scenario: A branch that will not take the write
- **WHEN** the branch moves before every one of a write's pushes
- **THEN** the write is applied seven times, waits before each fresh fetch but the last, no more than 23.5 seconds in all, and is refused saying the branch kept moving, how many times the write was applied and how long it waited

#### Scenario: A write of two files
- **WHEN** a command changes the plan and appends a move
- **THEN** one commit holds both, and no reader sees the plan change without the move

#### Scenario: A file that fails its check
- **WHEN** a write would leave a recutils file that fails `recfix --check` or crew's rules
- **THEN** nothing is pushed, and the command says which file and why

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

### Requirement: Drives in one repository never meet
crew SHALL fetch and push only the branch of the drive a command acts for. A write to one drive SHALL never be refused, delayed or replayed because another drive wrote.

#### Scenario: Two drives write at the same moment
- **WHEN** `madswan` and `swancloud` each write their plan at the same moment
- **THEN** each write's first push succeeds

#### Scenario: Reading one drive
- **WHEN** a command reads wldn's plan
- **THEN** crew fetches `wldn/main` and no other branch

### Requirement: A drive's branch is created, and adopts what it had
`crew state init <label>` SHALL create `<label>/main` in the drive's state repository with an empty plan and an empty moves file. Where a blueprints repo of the drive holds `plan/<label>`, the branch SHALL start from that plan's history, and the moves in the first blueprints repo's `signals/moves.rec` SHALL be copied with the commit they were read at. Run again, it SHALL change nothing.

#### Scenario: Willdan's plan is adopted
- **WHEN** `crew state init wldn` runs while willdan-blueprints holds `plan/wldn` and two moves
- **THEN** `wldn/main` holds the same bolts and units, its history reaches back to the plan's first commit, and `moves.rec` holds both moves

#### Scenario: A drive with two plans
- **WHEN** `crew state init madswan` runs while afterthought/blueprints and agentplot/blueprints each hold `plan/madswan`
- **THEN** `madswan/main` holds one plan with the bolts and units of both, the second plan's records added in one commit that names where they came from

#### Scenario: Two plans share a name
- **WHEN** the two plans being joined both hold a bolt or a unit of the same name
- **THEN** init is refused, naming it, and nothing is written

#### Scenario: Run twice
- **WHEN** `crew state init wldn` runs again
- **THEN** nothing is written, and it says the branch exists and at which commit

### Requirement: A drive's state is plain files anyone with access can read
A clone of a drive's branch SHALL be recutils files that `recsel` and `recfix` read with no crew command, and each commit's subject SHALL say what the write did and who asked.

#### Scenario: Reading with recutils
- **WHEN** the user clones the branch `wldn/main` and runs `recsel -t Unit plan.rec`
- **THEN** the plan's units are printed

### Requirement: crew asks a host's runner for work by requests on the drive's branch
crew SHALL write every request for a host's runner as a record of `requests.rec` on the drive's branch: a launch of a place, or a retry, drop, priority or land of one it launched, or a confirm, for a role's address, of ends of a place it launched, or a preview of a branch at a revision on the host where the work it serves runs, brought up or, marked done, put away. Each SHALL be numbered once, appended by a crew command in the commit of the plan write that occasions it, and checked by `recfix --check` and crew's own rules. A request SHALL never be removed. It SHALL never be changed, except by `crew kit rename`, which renames a repository's name in a request's `Repo` and in a fix of its main's `Work`, in the rename's one commit. Any other write that changes a request SHALL be refused.

#### Scenario: Never renumbered
- **WHEN** `requests.rec` holds requests 1 to 7 and a drop is written
- **THEN** it is request 8, and requests 1 to 7 are as they were

#### Scenario: A land is a request
- **WHEN** `requests.rec` holds requests 1 to 7, request 1 the launch of `bolt/x`, and the user's send of `x`'s row is carried to the runner
- **THEN** request 8 is a land of request 1, and requests 1 to 7 are as they were

#### Scenario: A preview and its done
- **WHEN** `requests.rec` holds requests 1 to 7, a preview is asked from a card, and later the user is done with it
- **THEN** the preview is request 8 and its done request 9, each in a commit of its own, and requests 1 to 8 are as they were when 9 is written

#### Scenario: A confirm in a turn's end
- **WHEN** `requests.rec` holds requests 1 to 7, request 3 a launch of unit `a`, and the planner's run ends a turn that took two ends of `a`'s place
- **THEN** request 8 is a confirm of request 3 for `madswan/planner` with two `Delivery` lines, in the commit that ends the turn, and it passes `recfix --check`

#### Scenario: A rename's write changes a request's repository
- **WHEN** the user renames `flywheel-cloud` to `boomdrive-cloud` and request 3 has `Repo: flywheel-cloud`
- **THEN** the write passes crew's append check with request 3's `Repo` renamed and nothing else of it changed

#### Scenario: Any other write that changes a request
- **WHEN** a write other than a rename would change request 3's `Repo`
- **THEN** it is refused, saying a request is never changed or removed, and nothing is pushed

### Requirement: A launch names everything the runner passes to Flume
A launch of a kit's work SHALL name the work it serves, its repository as the plan names it, its kind, name and base, its priority, intent and recipient, and its brief, and SHALL name no host or stream, a runner whose configuration names its repository taking it, in the stream its host's Flume configuration maps the repository to; a launch of a role's work SHALL also name the host and stream its role runs in. A bolt's own launch, of `bolt/<bolt>`, SHALL name the kind `crew/bolt` and the base `main`, and no brief and no launch to land first, since its base place runs no agent; and any other launch SHALL NOT name the kind `crew/bolt` (record 0056 point 2). A start SHALL append the bolt's launch before its pieces' (bolt-teams), and a launch on the base `bolt/<bolt>` SHALL be taken with no launch of `bolt/<bolt>` before it, as a fix on a bolt started before bolts were base places is. A launch MAY name launches that must land first and a held submission. A retry, drop, priority, land or confirm SHALL name the launch it acts on and no host, and a land SHALL name a launch of a bolt or of a fix of main, its work the same as that launch's. A confirm SHALL name as its recipient the address of one of crew's five roles, `<label>/<role>`, and at least one delivery key, for the runner that holds the launch to confirm to Flume as that recipient. crew's rules SHALL refuse a request that lacks what its act needs or names what its act does not take.

#### Scenario: A launch with no stream
- **WHEN** a bolt's start appends a launch of a kit's work naming no `Stream`
- **THEN** it is appended, a runner whose configuration names the kit's repository giving its stream

#### Scenario: A kit's launch naming a host
- **WHEN** a bolt's start would append a launch naming a `Host` or a `Stream`
- **THEN** the write is refused by crew's rules and the branch is unchanged

#### Scenario: A retry of nothing
- **WHEN** a retry would name request 9, which is no launch
- **THEN** the write is refused naming request 9

#### Scenario: A bolt's own launch
- **WHEN** a bolt's start appends a launch of `bolt/x` of the kind `crew/bolt` on the base `main`, with no brief and no launch to land first
- **THEN** it is appended; had it named a brief, a launch to land first, another kind or another base, the write would be refused naming the field

#### Scenario: A fix on a bolt with no launch of its own
- **WHEN** a write would append a fix's launch on the base `bolt/x`, and `requests.rec` holds `x`'s units' launches and no launch of `bolt/x`
- **THEN** it is appended

#### Scenario: A land of a unit
- **WHEN** a land would name request 4, the launch of unit `a` on `bolt/x`
- **THEN** the write is refused naming request 4, since a land names a bolt's or a fix of main's launch

#### Scenario: A confirm with no key, or for no role
- **WHEN** a confirm of request 3 would name no `Delivery`, or name `madswan/coder` as its `Recipient`
- **THEN** the write is refused by crew's rules, naming what the confirm lacks or the recipient, and the branch is unchanged

### Requirement: crew reads each host's runner from that runner's own branch
crew SHALL read a host's runner from `<label>/runner/<host>` of the drive's state repository, fetched with `<label>/main` in one fetch, and SHALL never write it. The branch holds five files:
- `runner.rec` says a runner serves the drive there;
- `answers.rec` says where each request stands;
- `places.rec` holds Flume's status of each place, as Flume gave it;
- `repositories.rec` holds each repository the runner keeps on its host, by its forge address with the folder of its clone;
- `previews.rec` holds what the runner answered of each preview request, by its request's number: its outcome, `held`, `done` or `refused`; sluice's answer and sluice's listing of the preview, each as the runner carried it; whether sluice's last listing held it; the runner's words; and when.

crew SHALL hold `previews.rec`'s descriptor byte for byte as the runner writes it. A `repositories.rec` or a `previews.rec` that recfix refuses, or that holds a record with no address or no request's number, or one address or one request twice, SHALL make that host's runner unreadable, as the other files do. A branch with no `repositories.rec` SHALL be read as a runner that reports no repositories, and one with no `previews.rec` as a runner that has answered no preview. A preview's answer or listing that is no JSON object crew reads SHALL mark that preview alone as unread, naming it.

#### Scenario: One fetch
- **WHEN** a command reads the plan and the runners
- **THEN** it fetches the state repository once, `<label>/main` and `<label>/runner/*` together

#### Scenario: The repositories a runner keeps
- **WHEN** `madswan/runner/deneb` holds a `repositories.rec` naming `agentplot/boomdrive-cloud` at `/r/boomdrive-cloud`
- **THEN** crew reads that deneb's runner keeps `agentplot/boomdrive-cloud` in `/r/boomdrive-cloud`

#### Scenario: A runner that reports no repositories
- **WHEN** `madswan/runner/deneb` holds no `repositories.rec`
- **THEN** deneb's runner is read as before, reporting no repositories

#### Scenario: A repositories file crew can't read
- **WHEN** deneb's `repositories.rec` names `agentplot/boomdrive-cloud` twice
- **THEN** deneb's runner can't be read, naming the file, and only the work no runner crew read has taken reads unknown

#### Scenario: A preview the runner answered
- **WHEN** `madswan/runner/deneb` holds a `previews.rec` whose `Preview` for request 12 says `Outcome: done`, `Listed: yes`, and a `Status` that is sluice's listing of the preview `up` at `web`
- **THEN** crew reads request 12's preview as brought up and up, at sluice's address for `web`

#### Scenario: A runner that has answered no preview
- **WHEN** `madswan/runner/deneb` holds no `previews.rec`
- **THEN** deneb's runner is read as before, answering no preview

#### Scenario: A previews file crew can't read
- **WHEN** deneb's `previews.rec` holds request 12 twice
- **THEN** deneb's runner can't be read, naming the file

#### Scenario: A preview's listing that is no JSON
- **WHEN** request 12's `Status` in deneb's `previews.rec` is no JSON object
- **THEN** request 12's preview reads unread, naming deneb's file, and every other answer of deneb's reads as it stands

### Requirement: A runner's branch that can't be read hides only the work no runner crew read has taken
A host whose runner branch recfix refuses, or crew can't read, SHALL hide only the work no runner crew read has taken, which reads unknown, naming that runner; work a runner crew read has taken SHALL read as it stands. A host with no runner branch is no runner, and hides nothing.

#### Scenario: Two hosts, one silent
- **WHEN** `madswan/runner/deneb` holds an answer and a place for request 3, and `madswan/runner/alpha` can't be read
- **THEN** request 3's work reads its stage from deneb's place, and work deneb has not taken reads unknown, naming alpha's runner

### Requirement: A kit's work is taken by a runner whose configuration names its repository
crew SHALL record a kit's work against its repository and look up no kit's host. A runner whose configuration names the repository takes the work, under a lease and while its host's stream has room, and launches it there, in the stream its host's Flume configuration maps the repository to.

crew SHALL read a launched piece's stage from the runner whose answers hold its launch, and read it as launching while none does. Where two runners hold it, or none crew read holds it and a runner could not be read, the piece SHALL read unknown, naming them.

Where crew must act on or say where a bolt's work runs, it SHALL read what the runner reported for the work it took. This covers the bolt's landing, its reads of the bolt and its kit, its reading and preview, the sweep after a landing or a drop, its site row, and its ledger's host and stream.
- The host is the one whose runner took the newest of the bolt's launches taken. While no runner has taken any of the bolt's own work, it is the host whose runner took its kit's newest work taken.
- The kit's folder there is the one that runner's `repositories.rec` names for the kit's repository, by the name or forge address the plan gives the kit. crew SHALL never read the folder from Flume's status of a place that runner carried, whether of the bolt's work or of the kit's other work.
- The stream is the one Flume's status of that runner's newest place of the work names, and none while it carries no such place.

The kit SHALL be named as unread, nothing of it landed and every other bolt read as it stands, in each of these cases:
- the runner reports no repositories. The refusal names the host and says its runner reports no repositories it keeps;
- a runner that reports its repositories names none by the kit's name. The refusal names the host, the repositories it keeps and `crew kit rename`;
- no runner has reported the bolt or the kit;
- the runner that took it reports two repositories by the kit's name, and the plan names the kit by its name alone;
- two runners took the bolt's newest launch.

#### Scenario: The runner that took the work
- **WHEN** deneb's runner answers launch 1 of crew's unit `a` on `bolt/x` and carries Flume's status of its place, naming its stream `madswan`, and its `repositories.rec` names `afterthought/crew` at `/w/crew`
- **THEN** `a`'s stage is read from deneb's records, and `x` is read and landed on deneb in `/w/crew`, its ledger saying deneb and `madswan`

#### Scenario: A runner that reports no repositories
- **WHEN** deneb's runner answers launch 1 of `x`'s unit `a` and carries Flume's status of its place, naming its repository `/w/crew`, and its branch holds no `repositories.rec`
- **THEN** crew can't tell where `x`'s kit is kept on deneb, saying deneb's runner reports no repositories it keeps, and nothing of `x` is read in `/w/crew` or landed

#### Scenario: A bolt none of whose own work is taken
- **WHEN** `x` is started and no runner has taken its launches, and deneb's runner took crew's work on another bolt and its `repositories.rec` names `afterthought/crew` at `/w/crew`
- **THEN** `x` is read and landed on deneb in `/w/crew`

#### Scenario: A bolt whose every launch was refused
- **WHEN** deneb's runner refused launch 1 of `x`'s unit `a`, the base bolt already holding its change, carries no place of crew's work, and its `repositories.rec` names `afterthought/crew` at `/w/crew`
- **THEN** `x` is read and landed on deneb in `/w/crew`, and `crew bolts` says where it runs; with no `repositories.rec` on deneb's branch, crew could not tell where `x`'s kit is kept there, whatever another place of crew's work names

#### Scenario: A bolt whose places the runner no longer carries
- **WHEN** deneb's runner answered every launch of `x` launched, carries no place of any of them nor of crew's other work, and its `repositories.rec` names `afterthought/crew` at `/w/crew`
- **THEN** `x` is read and landed on deneb in `/w/crew`, and `crew bolts` says where it runs

#### Scenario: Taken by two runners
- **WHEN** deneb's and chuck-herdr-alpha's runners both answer launch 1
- **THEN** its piece reads unknown naming both, and crew can't tell where `x` runs, landing nothing of it

#### Scenario: No runner has reported the kit
- **WHEN** no runner has taken any launch of crew's work
- **THEN** a landing of `x` is refused naming that no runner has reported taking its work, and a piece of it reads launching

#### Scenario: A kit renamed under its place
- **WHEN** deneb's runner carries request 1's place, Flume's status naming its repository `/r/flywheel-cloud`, its `repositories.rec` names `agentplot/boomdrive-cloud` at `/r/boomdrive-cloud`, and the bolt's kit is `boomdrive-cloud`, as the plan gives it
- **THEN** the bolt is read and landed on deneb in `/r/boomdrive-cloud`

#### Scenario: A runner that does not keep the kit
- **WHEN** deneb's `repositories.rec` names only `agentplot/boomdrive-cloud`, and the bolt's kit is `flywheel-cloud`, as the plan gives it
- **THEN** its landing is refused naming deneb, `flywheel-cloud`, the repositories deneb's runner keeps and `crew kit rename`, and nothing is landed

### Requirement: What comes before a runner takes a kit's work is done on the main-level host
Some of what crew does on a kit comes before any runner has taken the work in hand:
- a new unit's or chore's name, checked against the kit's main;
- a bolt never started, landed by its close alone;
- the design agent's records, and a proposal's records, read in the kit;
- the board's explorations on the kit's main;
- the main level's folders of the drive's kits.

That work SHALL be done in the checkout the drive's main-level host keeps of the kit, found by the kit's forge address or, for a kit the plan names by its name alone, by that name. Where the main-level host is the host crew runs on and its teams file names the repository among its `repositories`, the kit's checkout SHALL be that entry's `checkout` and its folder that entry's `dir`, whether or not a drive's `repos` lists the repository. Otherwise they SHALL be `<folder>/<name>/main` and `<folder>/<name>` in the folder of the first drive whose machine is that host and whose `repos` lists the repository, as the teams file gives them. Nothing SHALL be asked of a runner for it, and no file but the teams file SHALL be read for it. It SHALL be refused, naming the host and the kit, where that host keeps none or keeps two repositories by the kit's name, counting those its teams file names with those its drives' `repos` list. A refusal for a kit the host keeps none of SHALL also name `crew kit rename <kit> <new>` as the way on for a kit renamed on its host.

A bolt's start SHALL be none of that work: it SHALL read no host's checkout, make no branch and run nothing on any host, and SHALL read neither the kit's policy nor any host's sluice, the bolt's base place and its pieces asked of the runner by requests on the drive's branch alone (record 0056 point 2).

#### Scenario: A kit's first bolt is started
- **WHEN** `crew bolt start x` runs for crew's first bolt, no runner has taken any of crew's work, and deneb, madswan's main-level host, keeps `afterthought/crew` at `/d/madswan/crew/main`, madswan's folder being `/d/madswan` and its `repos` listing `afterthought/crew`
- **THEN** `requests.rec` gains `x`'s base place's launch and then its pieces' launches, no branch is made, and nothing is read or run in `/d/madswan/crew/main` or anywhere on deneb

#### Scenario: A start where the main-level host keeps no checkout of the kit
- **WHEN** `crew bolt start x` runs, deneb's teams file names no crew in `repositories`, and no drive whose machine is deneb lists crew in its `repos`
- **THEN** the start is not refused for it, and `x`'s launches are appended as for any start

#### Scenario: A kit the main-level host keeps no checkout of
- **WHEN** the planner adds unit `a` to crew, deneb's teams file names no crew in `repositories`, and no drive whose machine is deneb lists crew in its `repos`
- **THEN** it is refused naming deneb and crew, and the plan is unchanged

#### Scenario: A kit renamed on its host before the plan
- **WHEN** deneb's drives' `repos` list `agentplot/timber` and nothing by `tailrace`, and the planner adds unit `a` to `tailrace`, with no rename
- **THEN** it is refused naming deneb, `tailrace` and `crew kit rename tailrace <new>`, and nothing is written

#### Scenario: A unit's name and a record
- **WHEN** the planner adds unit `a` to crew and the design agent runs `crew record crew 53 --proposed`
- **THEN** `a`'s name is checked against crew's main, and record 0053 read, in `/d/madswan/crew/main` on deneb

#### Scenario: The main level's kit folders
- **WHEN** madswan's plan names crew and sluice, deneb keeps both and a role of madswan's main level starts there
- **THEN** it may reach deneb's checkouts of crew and sluice, and a kit its plan names that deneb keeps none of is left out

#### Scenario: A kit in the runner's copy
- **WHEN** crew runs on deneb, madswan's main-level host, and deneb's teams file names `agentplot/crew` with `dir` `/r/agentplot/crew` and `checkout` `/v/agentplot/crew`, while agentplot's `repos` also lists `agentplot/crew` in its folder `/d/agentplot`
- **THEN** crew is read and acted on before any runner takes its work in `/v/agentplot/crew`, its folder `/r/agentplot/crew`, by the name `crew` or the address `agentplot/crew`, and a role of madswan's main level may reach `/v/agentplot/crew`

#### Scenario: A repository the file names and no space keeps
- **WHEN** crew runs on deneb, deneb's teams file names `agentplot/weir` in `repositories`, and no drive's `repos` lists it
- **THEN** weir is a kit deneb keeps, at the file's `checkout` and `dir`

#### Scenario: Another host's kit
- **WHEN** crew runs on deneb, its teams file names `WilldanGroup/atlas-kit` in `repositories`, and wldn's main level runs on chuck-herdr-alpha, wldn's folder being `/workspace` and its `repos` listing atlas-kit
- **THEN** wldn's atlas-kit is read in `/workspace/atlas-kit/main` on chuck-herdr-alpha, since deneb's file names deneb's repositories alone

#### Scenario: One name, two repositories
- **WHEN** crew runs on deneb, its teams file names `agentplot/blueprints` in `repositories`, and a drive on deneb lists `afterthought/blueprints` in its `repos`
- **THEN** a kit named `blueprints` alone is refused naming both, and `agentplot/blueprints` is the file's checkout

### Requirement: A started bolt's host is named before its place is carried
`crew bolts`, the board's ledger and the page SHALL name a started bolt's host as the one whose runner took its newest launch taken, while the runner has carried no place of its work, and never say where it runs can't be told for work a runner has taken. Whatever acts in the bolt's kit SHALL still wait until the kit's folder there is read.

#### Scenario: A place not carried yet
- **WHEN** deneb's runner answers `a`'s launch on `bolt/x` held with its claim, or launched at its place, and carries no status of the place, and reports no repositories
- **THEN** `crew bolts` names `x` at deneb and the board's ledger says on deneb, neither saying where it runs can't be told, and nothing of `x`'s kit is read or landed

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

### Requirement: A drive is never renamed
A drive's label SHALL be fixed once it is made, and no crew command SHALL rename one; `crew kit rename` renames a repository within the one drive it runs as. A label that changes in the teams file SHALL be read as one drive removed and another added: the new label's state is its own branch, `<new label>/main`, nothing of the old label's branch is read as the new drive's, and a command naming the old label is refused as naming no drive.

#### Scenario: A label changed in the teams file
- **WHEN** the teams file names `afterthought` where it named `swancloud`
- **THEN** crew reads afterthought's state from `afterthought/main` of its state repository, and a command run with `--label swancloud` is refused naming the drives the teams file has

### Requirement: A preview names its host, its work, its repository, its branch and its revision
A preview request SHALL name the host whose runner reported the work it serves (the requirement "A kit's work is taken by a runner whose configuration names its repository"), since only that runner brings it up; the work it serves, `bolt/<bolt>` for a landings row's bolt or `unit/<unit>` for a batch line; its repository as the plan names it; the branch and the revision; and, to put it away, `Done: yes`. It SHALL name nothing else ("A bolt's work is its base place's and its preview's").

#### Scenario: A preview of a landings row's bolt
- **WHEN** `crew card preview land/crew y` appends a preview naming `Host: deneb`, `Work: bolt/y`, `Repo: crew`, `Branch: bolt/y` and `Revision: abc1234`
- **THEN** the write passes crew's rules and recfix

#### Scenario: A preview naming no host
- **WHEN** a write would append a preview naming no `Host`
- **THEN** it is refused by crew's rules, saying a preview names the host whose runner brings it up, and the branch is unchanged

#### Scenario: A preview carrying what it does not take
- **WHEN** a write would append a preview naming a `Kind` or a `Stream`
- **THEN** it is refused by crew's rules, naming the fields, and the branch is unchanged

#### Scenario: A bolt's work on any other request
- **WHEN** a write would append a launch serving `bolt/y` of the kind `change`
- **THEN** it is refused by crew's rules, saying a bolt's base place is of crew's kind `crew/bolt`

### Requirement: A preview is read from the runner on the host it names
crew SHALL read a preview request's answer from the runner on the host it names alone: from that runner's `previews.rec`, or from its `answers.rec` where that runner refused the request there, as a runner that cannot read it does. It SHALL read as asked while that runner has answered it neither way. crew SHALL read the previews of one host, repository and revision as one, and its ask as standing while the newest preview request naming all three is a bring-up that runner has not refused.

#### Scenario: A runner before previews
- **WHEN** deneb's runner, of a release that reads no preview, answers request 12 refused in `answers.rec` with the words `its Act preview, which crew's implementation does not read`
- **THEN** crew reads request 12's preview as refused, in the runner's words

#### Scenario: Put away, then asked again
- **WHEN** request 12 asks for `bolt/y` at `abc1234` on deneb, request 13 is its done, and request 14 asks for it again
- **THEN** crew reads the ask of `abc1234` on deneb as standing at request 14

### Requirement: A bolt's work is its base place's and its preview's
`bolt/<bolt>` SHALL be the work of the bolt's base place, its launch of crew's kind `crew/bolt` and the retry, drop, priority, land and confirm of it ("A launch names everything the runner passes to Flume"), and of a landings row's preview, and of no other request. A retry, drop, priority, land or confirm SHALL name a launch by `Of`, never a preview.

#### Scenario: A preview and a land of one bolt
- **WHEN** `requests.rec` holds `bolt/y`'s base place's launch as request 1 and a preview of `bolt/y` as request 2, and a write would append a land of `bolt/y` naming request 1
- **THEN** the write passes crew's rules, and a land naming request 2 is refused, saying request 2 is no launch

#### Scenario: A retry or drop naming a preview
- **WHEN** `requests.rec` holds a preview of `bolt/y` as request 1, and a write would append a retry or a drop of `bolt/y` naming request 1
- **THEN** it is refused by crew's rules, saying request 1 is no launch
