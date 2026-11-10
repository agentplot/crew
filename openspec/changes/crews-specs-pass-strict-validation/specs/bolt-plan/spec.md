## ADDED Requirements

### Requirement: The file's order is a bolt's build order, and a unit with no bolt is queued work
A bolt's units SHALL be ordered by the file: a bolt's launches SHALL take their priority from the order the bolts appear, and a unit is ahead of every unit after it in its bolt. A unit with no `Bolt` SHALL be queued work.

#### Scenario: Queued work
- **WHEN** a unit is added with no bolt
- **THEN** `crew bolts` lists it under the queue of its repo

### Requirement: A unit's After holds its launch until that work has landed on the bolt
A unit's `After` SHALL name units or chores of the same bolt that it builds on. Its launch SHALL be held by the runner until each of them has landed on the bolt, so its place is cut from a bolt that holds their work, as bolt-teams "A dependent launches once its After work has landed" has it.

#### Scenario: A dependency still in construct
- **WHEN** unit B of started bolt `x` has `After: A`, and A's construct has not committed
- **THEN** B's stage is `waiting` on A, and its launch is held

#### Scenario: A dependency constructed
- **WHEN** unit B has `After: A`, and A's change is committed while A is in code
- **THEN** B still waits on A, its launch held until A has landed on `bolt/x`

#### Scenario: A dependency not yet merged
- **WHEN** unit B has `After: A`, and A has not landed on `bolt/x`
- **THEN** no place of B's is launched, so nothing of B's merges into the bolt before A

### Requirement: A drive's one plan holds only Bolt and Unit records of what is meant to be built
Each drive SHALL keep one plan, the recutils file `plan.rec` on its branch of its state repository, for all of its kits. The plan SHALL hold only Bolt and Unit records. A Bolt has its name, repo, goal and sources. A Unit has its name, repo, bolt, intent, sources and dependencies (`After`); a Unit record marked `Kind: chore` is a chore, whose intent is its words. The plan SHALL hold what is meant to be built and any hold on it, never how far the work has got.

#### Scenario: Business and agentplot work
- **WHEN** the drive `madswan` builds kits whose design is in afterthought/blueprints and kits whose design is in agentplot/blueprints
- **THEN** its bolts and units for both are in one `plan.rec` on `madswan/main`, and afterthought's plan is `plan.rec` on `afterthought/main`

#### Scenario: A plan that fails its schema
- **WHEN** a hand edit leaves a duplicated key or a field the schema does not allow
- **THEN** crew refuses to read that plan, and names the commit and `recfix --check`'s message

#### Scenario: A source in a blueprints repo
- **WHEN** a unit's source is a page of the drive's first blueprints repo
- **THEN** its `Source` is that page's path, and a page of another repo is `<owner>/<name>:<path>`

#### Scenario: A chore among the units
- **WHEN** a bolt holds two units and a chore between them
- **THEN** `plan.rec` holds the chore's Unit record, marked `Kind: chore`, between the two units' records, and the file's order is their build order

### Requirement: A Bolt record's Team field is read by nothing, and a new branch allows none
A Bolt record that still carries a `Team` field, written before teams left, SHALL be read as any bolt, the field read by nothing; a new branch's schema SHALL allow no `Team`.

#### Scenario: A bolt given before teams left
- **WHEN** `plan.rec` holds a Bolt record with `Team: swb-1`, and its branch's schema allows the field
- **THEN** `recfix --check` passes, `crew bolts` shows the bolt with no team, and the next write leaves the field as it is

#### Scenario: A new branch
- **WHEN** `crew state init` starts a drive's branch
- **THEN** its `plan.rec` declares no `Team` field and its `proposals.rec` no `Agreed` field

### Requirement: crew reads a bolt at GitHub's copy where its policy names a remote, and else at the host's own
crew SHALL read a bolt at GitHub's copy of its branch, `origin/bolt/<bolt>`, when the host holds that copy and the policy in it names a remote for the bolt. Otherwise it SHALL read the bolt at the host's own `bolt/<bolt>`. crew SHALL never read a bolt on GitHub from the host's own `bolt/<bolt>`, which is sluice's copy, whether or not sluice has levelled it.

#### Scenario: A merge landed on GitHub while the host's copy stayed behind
- **WHEN** sluice lands a unit's merge and a chore's merge on GitHub's `bolt/b`, the host has fetched it, and the host's own `bolt/b` is still at the commit before them
- **THEN** the unit and the chore read `merged`, the bolt's head is GitHub's, and its verification is read at that head

#### Scenario: A bolt kept on its host
- **WHEN** a bolt was made before gives went through sluice, the policy at GitHub's copy of it names no remote for its bolts, and the host's own `bolt/b` holds merges GitHub's copy lacks
- **THEN** the bolt is read at the host's `bolt/b`, those merges counted

#### Scenario: A bolt GitHub's copy of which this host has not got
- **WHEN** the host holds no `origin/bolt/b`
- **THEN** the bolt is read at the host's `bolt/b`, the only copy the host has, and is missing when that is not there either

#### Scenario: A policy crew can't read
- **WHEN** the policy in GitHub's copy of the bolt is not TOML
- **THEN** the bolt's stages read `unknown`, naming the file and the bolt, and nothing is read from the host's `bolt/b`

### Requirement: A bolt's head, work, stages and verification come from the ref it is read at
A bolt's head, the changes and chores it holds, and every stage read from it SHALL come from the ref crew reads the bolt at. So SHALL its verification: whether that head is the landing of its work, as the runner reports it.

#### Scenario: A proven bolt whose copy lags
- **WHEN** every unit of a bolt on GitHub has merged, GitHub's head is the commit at which the runner carries the bolt's last unit landed, and the host's `bolt/b` is at an earlier landing
- **THEN** the bolt reads proven, and its row on its kit's landings card is offered

#### Scenario: A chore's place and a fix beside a bolt on GitHub
- **WHEN** a chore's place holds one commit of its own beyond GitHub's `bolt/b`, and a fix's tip is in GitHub's `bolt/b` but not in the host's
- **THEN** the chore reads `verify` and the fix reads merged

### Requirement: A launched place reads its stage up to its submission
Once launched, a unit, chore or fix SHALL read queued while Flume waits for room; construct, code with its ticked tasks of all, or verify while a stage runs; needing an answer with the agent's question when it stopped short asking; its stage, sent back, with sluice's words when a submission failed or conflicted; submitted with sluice's number.

#### Scenario: A unit in code
- **WHEN** deneb's runner record for `a`'s launch carries Flume's status of its place in code with three of seven tasks ticked
- **THEN** `crew bolts` shows `a` at `code 3/7`

#### Scenario: A construct that asked
- **WHEN** the runner's record shows `a`'s construct stopped short with "Which drive's rail?"
- **THEN** `crew bolts` shows `a` as needing an answer, with the question

#### Scenario: A stop-short whose agent is kept open
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place, its code ended short needing an answer, its agent kept open for it until `open_until`, its end keyed `stage/code/1/ended-short`
- **THEN** `a` reads needing an answer at code, with the agent's words, and `crew bolts` shows it so

#### Scenario: Sent back by sluice
- **WHEN** the runner's record shows `b`'s place back in code after sluice found its submission in conflict on `plugin/lib/plan.py`
- **THEN** `crew bolts` shows `b` in code, sent back, with sluice's words

### Requirement: A launched place reads waiting on its caller, stalled, or its end
Once launched, a unit, chore or fix SHALL read waiting on its caller, with Flume's words and the stage it waits to retry or its submission, whenever Flume's status says it waits on its caller for a retry, past its kind's bound among them, whatever stage it last delivered; stalled once Flume's status says it is stalled; merged once it has landed on its bolt and landed once its bolt has; or dropped.

#### Scenario: A place past its bound
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place after its fourth verify delivered and its submission conflicted, the place having gone back as often as its kind allows, so Flume says it waits on its caller to retry code past its bound
- **THEN** `a` reads waiting on its caller at code with Flume's words, never at verify, and `crew bolts`, the board's ledger and the planner's band show it so

#### Scenario: A submission that waits on its retry
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place, its last stage delivered and its submission refused by the merge queue, so Flume says it waits on its caller to retry its submission
- **THEN** `a` reads waiting on its caller at its submission with Flume's words, and `crew bolts` shows it so

#### Scenario: Landed on the bolt
- **WHEN** the runner's record shows `a`'s place landed on `bolt/x`, and `x` has not landed
- **THEN** `crew bolts` shows `a` merged

### Requirement: A tidied place reads as the record Flume holds of it for the runner
A place Flume has tidied SHALL read as the record Flume holds of it for the runner, which the runner carries as its status until its report holds it: merged or landed at the commit it landed at, or dropped. Where the runner carries no such record, the place SHALL read as the status the runner last carried. Nothing else SHALL be read for a place's end.

#### Scenario: A landing held for the runner
- **WHEN** Flume landed `a`'s place on `bolt/x` and tidied it, holding its record for the runner, and deneb's runner carries that record as `a`'s status, Flume 0.20.0's tidied phase, its work over and landed at `d185a87`, pending for `boomdrive`
- **THEN** `a` reads merged at `d185a87`, and landed once main holds its change

#### Scenario: A drop held for the runner
- **WHEN** `a`'s place was dropped and Flume tidied it, holding its record for the runner, and deneb's runner carries that record as `a`'s status, its work over and dropped
- **THEN** `a` reads dropped

#### Scenario: A place tidied before the runner carried its end
- **WHEN** the runner last carried `b`'s place at submitted, Flume tidied it holding no record for the runner, and `bolt/x` holds a landing commit naming `change/b` in its `Sluice-From`
- **THEN** `b` reads submitted, as the runner last carried it, and no landing commit is read for it

### Requirement: crew bolt start requests a bolt's base place and then its pieces in one plan write
`crew bolt start <bolt>` SHALL mark the bolt `Path: flume` and request, in one plan write that records `bolt.start`, the launch of the bolt's base place and after it a launch of each unit and chore of it on `bolt/<bolt>`, with its `After` and priority, as bolt-teams "A bolt is a base place of crew's kind" and "A start launches the bolt's base place before its pieces" give their fields (record 0056).

#### Scenario: A bolt is started
- **WHEN** the user approves a proposal holding `crew bolt start b`, a bolt of switchboard-kit with unit `a` and chore `c`, and a runner answers for wldn
- **THEN** `b` is marked `Path: flume`; `requests.rec` gains, in that one commit, the launch of `bolt/b`'s base place and then the launches of `a` and `c` on `bolt/b`, each naming switchboard-kit and no host or stream; no branch is made and no agent starts; and the run record has `bolt.start` on `bolt/b`

### Requirement: A start's launches name no host or stream, and a start reads no host
Each launch `crew bolt start <bolt>` requests SHALL be in the bolt's repository and name no host or stream, for a runner whose configuration names the repository to take. `crew bolt start` SHALL start no agent, make no branch and read no host.

#### Scenario: A start reads no host
- **WHEN** `crew bolt start console-pages` runs for wldn, where any read of a host fails the run
- **THEN** it requests the launch of `bolt/console-pages`'s base place, naming the bolt's repository, and reads no host

### Requirement: Only a proposal or the user starts a bolt
A proposal MAY hold `crew bolt start`; the user runs it directly; no other agent SHALL.

#### Scenario: An agent starts a bolt directly
- **WHEN** `wldn-ops` runs `crew bolt start b` outside a proposal
- **THEN** it is refused, naming the planner and the user, and the plan is unchanged

### Requirement: A start is refused while no runner answers or the bolt is started already
`crew bolt start <bolt>` SHALL be refused, with the plan unchanged and nothing requested, while no runner answers for the drive, and for a bolt started already, but one whose own launch the runner answered refused, which it launches anew as bolt-teams "A start run again launches a bolt whose launch the runner refused" has it.

#### Scenario: A drive no runner answers for
- **WHEN** `crew bolt start b` runs and wldn's state repository holds no runner's branch
- **THEN** it is refused, naming that no runner answers for wldn, the plan is unchanged and nothing is requested

#### Scenario: A bolt started before bolts were base places
- **WHEN** `b` is started, `requests.rec` holds its units' launches and no launch of `bolt/b`, and `crew bolt start b` runs
- **THEN** it is refused, saying `b` is started already, and nothing is written

### Requirement: A unit's stage is read from the plan before its bolt starts, never from the kit
crew SHALL read each unit's and chore's stage from the plan and the runner's records alone, never from a place in the kit or a landing commit on its bolt or on main: `queued` while it has no bolt; for a bolt not started, `ready`, or `waiting` while it names `After` work, which builds only once the bolt starts; and `unknown`, naming why, where crew cannot read what it rests on.

#### Scenario: Queued work
- **WHEN** a unit has no bolt
- **THEN** its stage is `queued`

#### Scenario: A bolt not started
- **WHEN** bolt `y` is planned and not started, unit `a` names no `After` and `b` has `After: a`
- **THEN** `a` reads `ready` and `b` `waiting`, and nothing of a runner or a place in the kit is read for them

#### Scenario: A worktree of crew's from before
- **WHEN** a `unit/a` worktree from before teams left stands under the kit's `places/` with every task ticked, and `x` is started
- **THEN** `a`'s stage is the runner's, and nothing of that worktree is read for it

### Requirement: A started bolt's unit reads its stage from the runner, and nothing is kept by hand
For a started bolt, crew SHALL read each unit's and chore's stage as "A started bolt's work reads its stage from the runner's records", "A launched place reads its stage up to its submission", "A launched place reads waiting on its caller, stalled, or its end" and "A tidied place reads as the record Flume holds of it for the runner" give it, `landed` once main holds its change, open or archived, or a chore's trailer. Nothing SHALL be kept by hand to say how far work has got.

#### Scenario: Nothing kept by hand
- **WHEN** `x` is started and deneb's runner reports `a`'s place in code with 6 of 26 tasks ticked
- **THEN** `crew bolts` shows `a` at `code 6/26`, and no file was edited to say so

#### Scenario: A launch refused for a change the bolt holds
- **WHEN** the runner refused this drive's launch of `a` because the base `bolt/x` already holds a change named `a`, and `bolt/x` holds a landing commit naming `change/a`
- **THEN** `a` reads refused, in the runner's words, and nothing of `bolt/x`'s landing commits is read for it

### Requirement: A rename is refused while a host of the drive keeps the old name
`crew kit rename <old> <new>` SHALL be refused while any host still keeps `<old>`, naming the host and what keeps it. The hosts read SHALL be each host with a runner branch of the drive, and the drive's main-level host. No host needs to keep `<new>`.

#### Scenario: A host still keeps it
- **WHEN** deneb's runner reports `agentplot/tailrace` among its repositories
- **THEN** the rename is refused naming deneb's runner and `agentplot/tailrace`

#### Scenario: The new name kept by no host
- **WHEN** no host keeps `timber` or `tailrace`, and nothing else stands
- **THEN** `crew kit rename tailrace timber` renames the records

### Requirement: A host's keeping is its runner's repositories, and otherwise the teams file's
A host's keeping SHALL be its runner's `repositories.rec` where that runner reports one, and otherwise what the teams file keeps there: its `repositories`, where the host is the one the file is written on, and the `repos` of each drive whose machine is the host.

#### Scenario: A runner that reports no repositories
- **WHEN** deneb's runner branch holds no `repositories.rec` and a drive whose machine is deneb lists `agentplot/tailrace` in its `repos`
- **THEN** the rename is refused naming deneb's teams file and `agentplot/tailrace`

### Requirement: A rename is refused where crew can't read a host's keeping
A host whose runner reports no repositories, that is not the host the file is written on, and that no drive of the file runs on is one whose keeping crew can't read. Where crew can't read something this depends on, `crew kit rename <old> <new>` SHALL be refused naming what it could not read.

#### Scenario: What crew can't read
- **WHEN** deneb's runner branch can't be read, or a runner's host reports no repositories, is not the host the rename runs on, and runs no drive of the teams file
- **THEN** the rename is refused naming that host and why, and nothing is written

## REMOVED Requirements

### Requirement: The file's order and dependencies are the plan
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "The file's order is a bolt's build order, and a unit with no bolt is queued work" and "A unit's After holds its launch until that work has landed on the bolt".

### Requirement: A drive keeps one plan in its state repository
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A drive's one plan holds only Bolt and Unit records of what is meant to be built" and "A Bolt record's Team field is read by nothing, and a new branch allows none".

### Requirement: A bolt on GitHub is read where it lives
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "crew reads a bolt at GitHub's copy where its policy names a remote, and else at the host's own" and "A bolt's head, work, stages and verification come from the ref it is read at".

### Requirement: A launched place's stage is where Flume's status has it
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A launched place reads its stage up to its submission", "A launched place reads waiting on its caller, stalled, or its end" and "A tidied place reads as the record Flume holds of it for the runner".

### Requirement: A bolt's work starts by crew bolt start
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "crew bolt start requests a bolt's base place and then its pieces in one plan write", "A start's launches name no host or stream, and a start reads no host", "Only a proposal or the user starts a bolt" and "A start is refused while no runner answers or the bolt is started already".

### Requirement: A unit's stage is read from the runner, or from the plan before its bolt starts
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A unit's stage is read from the plan before its bolt starts, never from the kit" and "A started bolt's unit reads its stage from the runner, and nothing is kept by hand".

### Requirement: A rename waits until no host keeps the old name
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A rename is refused while a host of the drive keeps the old name", "A host's keeping is its runner's repositories, and otherwise the teams file's" and "A rename is refused where crew can't read a host's keeping".
