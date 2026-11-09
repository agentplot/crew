# bolt-plan Specification

## Purpose
Keeps what a partition means to build, its bolts and their units, in one plain-text plan per blueprints repo. Every stage of the work is read from the kits rather than recorded by hand.

## Requirements

### Requirement: The file's order and dependencies are the plan
A bolt's units SHALL be ordered by the file: a bolt's launches SHALL take their priority from the order the bolts appear, and a unit is ahead of every unit after it in its bolt. A unit's `After` SHALL name units or chores of the same bolt that it builds on. Its launch SHALL be held by the runner until each of them has landed on the bolt, so its place is cut from a bolt that holds their work, as bolt-teams "A dependent launches once its After work has landed" has it. A unit with no `Bolt` SHALL be queued work.

#### Scenario: A dependency still in construct
- **WHEN** unit B of started bolt `x` has `After: A`, and A's construct has not committed
- **THEN** B's stage is `waiting` on A, and its launch is held

#### Scenario: A dependency constructed
- **WHEN** unit B has `After: A`, and A's change is committed while A is in code
- **THEN** B still waits on A, its launch held until A has landed on `bolt/x`

#### Scenario: A dependency not yet merged
- **WHEN** unit B has `After: A`, and A has not landed on `bolt/x`
- **THEN** no place of B's is launched, so nothing of B's merges into the bolt before A

#### Scenario: Queued work
- **WHEN** a unit is added with no bolt
- **THEN** `crew bolts` lists it under the queue of its repo

### Requirement: Writes go through crew and are never merged
Agents SHALL write the plan only through `crew bolt …` and `crew unit …`. Each write SHALL fetch the drive's branch of its state repository over https into crew's own bare cache of that repository, with no working tree, and apply the change to its tip. It SHALL then check the result with `recfix --check` and crew's own rules, commit it without touching any working tree, and push without force. A rejected push SHALL have its write replayed on the new tip after a growing wait.

#### Scenario: Two writes race
- **WHEN** the planner moves a unit while a conductor narrows the same unit's intent, from different hosts
- **THEN** both writes land, one after the other, and neither is merged

#### Scenario: The subject is gone
- **WHEN** a write names a unit that another write has just dropped
- **THEN** it is refused, naming the commit that dropped the unit

#### Scenario: No ssh on a Mac
- **WHEN** a write runs on a Mac
- **THEN** git reaches the state repository over https and never waits on 1Password

### Requirement: Units change while a bolt runs
`crew unit add` SHALL add a unit to a bolt, or to the queue, at the end or before a named unit. `crew unit split` SHALL narrow a unit and add the remainder right after it. `crew unit order` SHALL move a unit within its bolt. `crew unit after` SHALL set or clear a dependency, refusing a cycle or a unit of another bolt. `crew unit move` SHALL move a unit to another bolt of the same repo, or to the queue. `crew unit drop` SHALL remove a unit, with the reason in the commit.

#### Scenario: Splitting a unit in code
- **WHEN** `crew unit split` names a unit whose stage is code or later
- **THEN** it is refused; the remainder is added as a new unit instead

#### Scenario: Moving a unit with a worktree
- **WHEN** a unit in construct moves to another bolt in the same checkout
- **THEN** its branch is rebased onto the new bolt; a conflict aborts the move and leaves the plan unchanged

#### Scenario: Dropping merged work
- **WHEN** `crew unit drop` names a unit that has merged into its bolt
- **THEN** it is refused

### Requirement: What is in flight can be read from anywhere
`crew bolts [<bolt>] [--json]` SHALL list each of the partition's bolts with its repo, its kit's host and its state, each unit's and chore's stage and place, the fixes in flight on it, and the queue. Bolts with no work started, and queued work, SHALL be listed without reaching any host. Each host holding a bolt's work SHALL be read once. No line SHALL name a team.

#### Scenario: A host is unreachable
- **WHEN** the box is asleep
- **THEN** its bolts are listed from the plan, with every stage shown as unknown and the host named

### Requirement: Work is queued from a signal
`crew unit add … --signal <id>` SHALL queue the unit with the signal as its source, `signals/<id>`, and SHALL record the signal's one move, `route`, targeting the unit, in `moves.rec` on the drive's branch, in the same commit as the unit. A signal that is missing from the partition's first blueprints repo, already moved, or whose move would fail `recfix --check` SHALL be refused, and nothing written.

#### Scenario: A signal routed to work
- **WHEN** the planner queues a unit from a signal
- **THEN** one commit on the drive's branch adds the unit with `Source: signals/<id>` and a `route` move for that signal

#### Scenario: A signal in another blueprints repo
- **WHEN** madswan's planner queues a flywheel-next unit, whose design is in agentplot/blueprints, from a signal in afterthought/blueprints, the partition's first blueprints repo
- **THEN** the unit's `Source` is `signals/<id>`, which names that signal in afterthought/blueprints, and the route move is in `moves.rec` on `madswan/main`, in the same commit as the unit

#### Scenario: A signal already moved
- **WHEN** the signal named already has its move
- **THEN** the command is refused, naming the move it has, and the plan is unchanged

### Requirement: A drive keeps one plan in its state repository
Each drive SHALL keep one plan, the recutils file `plan.rec` on its branch of its state repository, for all of its kits. The plan SHALL hold only Bolt and Unit records. A Bolt has its name, repo, goal and sources. A Unit has its name, repo, bolt, intent, sources and dependencies (`After`); a Unit record marked `Kind: chore` is a chore, whose intent is its words. The plan SHALL hold what is meant to be built and any hold on it, never how far the work has got. A Bolt record that still carries a `Team` field, written before teams left, SHALL be read as any bolt, the field read by nothing; a new branch's schema SHALL allow no `Team`.

#### Scenario: Business and agentplot work
- **WHEN** the business partition (label `madswan`) builds kits whose design is in afterthought/blueprints and kits whose design is in agentplot/blueprints
- **THEN** its bolts and units for both are in one `plan.rec` on `madswan/main`, and personal's plan is `plan.rec` on `swancloud/main`

#### Scenario: A plan that fails its schema
- **WHEN** a hand edit leaves a duplicated key or a field the schema does not allow
- **THEN** crew refuses to read that plan, and names the commit and `recfix --check`'s message

#### Scenario: A source in a blueprints repo
- **WHEN** a unit's source is a page of the partition's first blueprints repo
- **THEN** its `Source` is that page's path, and a page of another repo is `<owner>/<name>:<path>`

#### Scenario: A chore among the units
- **WHEN** a bolt holds two units and a chore between them
- **THEN** `plan.rec` holds the chore's Unit record, marked `Kind: chore`, between the two units' records, and the file's order is their build order

#### Scenario: A bolt given before teams left
- **WHEN** `plan.rec` holds a Bolt record with `Team: swb-1`, and its branch's schema allows the field
- **THEN** `recfix --check` passes, `crew bolts` shows the bolt with no team, and the next write leaves the field as it is

#### Scenario: A new branch
- **WHEN** `crew state init` starts a drive's branch
- **THEN** its `plan.rec` declares no `Team` field and its `proposals.rec` no `Agreed` field

### Requirement: A bolt on GitHub is read where it lives
crew SHALL read a bolt at GitHub's copy of its branch, `origin/bolt/<bolt>`, when the host holds that copy and the policy in it names a remote for the bolt. Otherwise it SHALL read the bolt at the host's own `bolt/<bolt>`. The bolt's head, the changes and chores it holds, and every stage read from it SHALL come from that ref. So SHALL its verification: whether that head is the landing of its work, as the runner reports it. crew SHALL never read a bolt on GitHub from the host's own `bolt/<bolt>`, which is sluice's copy, whether or not sluice has levelled it.

#### Scenario: A merge landed on GitHub while the host's copy stayed behind
- **WHEN** sluice lands a unit's merge and a chore's merge on GitHub's `bolt/b`, the host has fetched it, and the host's own `bolt/b` is still at the commit before them
- **THEN** the unit and the chore read `merged`, the bolt's head is GitHub's, and its verification is read at that head

#### Scenario: A proven bolt whose copy lags
- **WHEN** every unit of a bolt on GitHub has merged, GitHub's head is the commit at which the runner carries the bolt's last unit landed, and the host's `bolt/b` is at an earlier landing
- **THEN** the bolt reads proven, and its row on its kit's landings card is offered

#### Scenario: A bolt kept on its host
- **WHEN** a bolt was made before gives went through sluice, the policy at GitHub's copy of it names no remote for its bolts, and the host's own `bolt/b` holds merges GitHub's copy lacks
- **THEN** the bolt is read at the host's `bolt/b`, those merges counted

#### Scenario: A bolt GitHub's copy of which this host has not got
- **WHEN** the host holds no `origin/bolt/b`
- **THEN** the bolt is read at the host's `bolt/b`, the only copy the host has, and is missing when that is not there either

#### Scenario: A policy crew can't read
- **WHEN** the policy in GitHub's copy of the bolt is not TOML
- **THEN** the bolt's stages read `unknown`, naming the file and the bolt, and nothing is read from the host's `bolt/b`

#### Scenario: A chore's place and a fix beside a bolt on GitHub
- **WHEN** a chore's place holds one commit of its own beyond GitHub's `bolt/b`, and a fix's tip is in GitHub's `bolt/b` but not in the host's
- **THEN** the chore reads `verify` and the fix reads merged

### Requirement: A started bolt's work reads its stage from the runner's records
For every unit, chore and fix of a bolt marked `Path: flume`, crew SHALL read its stage from its newest launch not dropped, its answer and its place's record on the runner's branch, never from the kit: unknown where its host was not read or it has no launch; launching before an answer; waiting while the runner holds it and its `After` names work, else launching with the runner's words; refused with the runner's words. `crew bolts` and every decision SHALL read the same.

#### Scenario: A dependent waits
- **WHEN** `b`'s launch is answered held, `a`'s place not yet landed
- **THEN** `crew bolts` shows `b` waiting on `a`

#### Scenario: A claimed launch is not held for After work
- **WHEN** deneb's runner answers the launch of `a`, which names no `After`, held with the words `claimed by deneb's runner; launching once no other runner has claimed it`
- **THEN** `a` reads launching, and `crew bolts`, the board and the planner's band show it launching with the runner's words, never waiting on After work

#### Scenario: The runner's host is silent
- **WHEN** deneb's runner branch can't be read
- **THEN** every piece launched on deneb reads unknown, and `crew bolts` names deneb

### Requirement: A launched place's stage is where Flume's status has it
Once launched, a unit, chore or fix SHALL read queued while Flume waits for room; construct, code with its ticked tasks of all, or verify while a stage runs; needing an answer with the agent's question when it stopped short asking; its stage, sent back, with sluice's words when a submission failed or conflicted; submitted with sluice's number; waiting on its caller, with Flume's words and the stage it waits to retry or its submission, whenever Flume's status says it waits on its caller for a retry, past its kind's bound among them, whatever stage it last delivered; stalled once Flume's status says it is stalled; merged once it has landed on its bolt and landed once its bolt has; or dropped.

#### Scenario: A unit in code
- **WHEN** deneb's runner record for `a`'s launch carries Flume's status of its place in code with three of seven tasks ticked
- **THEN** `crew bolts` shows `a` at `code 3/7`

#### Scenario: A construct that asked
- **WHEN** the runner's record shows `a`'s construct stopped short with "Which partition's rail?"
- **THEN** `crew bolts` shows `a` as needing an answer, with the question

#### Scenario: A stop-short whose agent is kept open
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place, its code ended short needing an answer, its agent kept open for it until `open_until`, its end keyed `stage/code/1/ended-short`
- **THEN** `a` reads needing an answer at code, with the agent's words, and `crew bolts` shows it so

#### Scenario: A place past its bound
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place after its fourth verify delivered and its submission conflicted, the place having gone back as often as its kind allows, so Flume says it waits on its caller to retry code past its bound
- **THEN** `a` reads waiting on its caller at code with Flume's words, never at verify, and `crew bolts`, the board's ledger and the planner's band show it so

#### Scenario: A submission that waits on its retry
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place, its last stage delivered and its submission refused by the merge queue, so Flume says it waits on its caller to retry its submission
- **THEN** `a` reads waiting on its caller at its submission with Flume's words, and `crew bolts` shows it so

#### Scenario: Sent back by sluice
- **WHEN** the runner's record shows `b`'s place back in code after sluice found its submission in conflict on `plugin/lib/plan.py`
- **THEN** `crew bolts` shows `b` in code, sent back, with sluice's words

#### Scenario: Landed on the bolt
- **WHEN** the runner's record shows `a`'s place landed on `bolt/x`, and `x` has not landed
- **THEN** `crew bolts` shows `a` merged

### Requirement: A bolt is created, dropped and landed through crew
`crew bolt new` SHALL add a bolt with its repo, goal and sources; `crew bolt order` moves it; `crew bolt drop` SHALL remove it and its units, or with `--requeue` queue them, and in either case SHALL drop each of the bolt's launches still standing in the drop's own commit, a requeued unit's among them, so a requeued unit is launched afresh once a bolt it is placed in is started. `crew bolt submit` SHALL submit its branch to its kit's main through sluice; `crew bolt land` SHALL remove a landed bolt and its units, and land and drop SHALL have sluice delete its branch, keeping and naming one holding work main lacks. No command SHALL give a bolt to a team.

#### Scenario: Landing too early
- **WHEN** `crew bolt land` runs while one of the bolt's units has not landed on main
- **THEN** it is refused, naming that unit

#### Scenario: The bolt's branch is deleted at its land
- **WHEN** `crew bolt land` runs for a landed bolt whose branch is on GitHub
- **THEN** the bolt leaves the plan, sluice deletes `bolt/<bolt>` from GitHub, and the branch is gone from the kit's host

#### Scenario: A delete sluice refuses
- **WHEN** `crew bolt land` runs and sluice refuses to delete `bolt/<bolt>` because a submission is still queued on it
- **THEN** the bolt leaves the plan, the branch stays on GitHub, and crew names it with sluice's words

#### Scenario: Dropping a bolt in flight
- **WHEN** the planner drops a bolt whose branch's tip main holds
- **THEN** the bolt and its units are gone from the plan, sluice deletes `bolt/<bolt>` from GitHub, and the branch is gone from the kit's host

#### Scenario: A dropped bolt holds work main lacks
- **WHEN** the planner drops a bolt into which a unit has merged that main does not hold
- **THEN** the bolt and its units are gone from the plan, sluice refuses the delete, the branch stays on GitHub and on the kit's host, and the drop names it as its unmerged work with sluice's words, the user's to keep or delete, and records it once

#### Scenario: The drop's host does not answer
- **WHEN** the planner drops a bolt while its kit's host does not answer
- **THEN** the drop names the host and the command, and the bolt is gone from the plan

#### Scenario: Requeuing a unit that has a place
- **WHEN** `crew bolt drop x "Later." --requeue` runs while unit `a` of started `x` has a launched place
- **THEN** `a` is in its repository's queue with no bolt or `After`, `x` is gone from the plan, and `requests.rec` gains a drop of `a`'s launch, in the drop's commit

#### Scenario: A give
- **WHEN** anyone runs `crew bolt give swb-1`
- **THEN** crew refuses it as no command it has, and the plan is unchanged

### Requirement: A unit's intent is amended through crew, its construct run again
`crew unit amend <unit> "<new intent>"` SHALL replace the unit's intent. A unit with a place SHALL also be marked amended, its construct run again with the new intent as the bolt's work is started, never handed to a team's host or told to a conductor. The command, direct or by an approval, SHALL answer once its write is made and wait on no agent (`code.9`). A unit merged into its bolt or landed SHALL be refused; run by the planner it SHALL be refused outside a proposal.

#### Scenario: A queued unit
- **WHEN** an amendment to a queued unit's intent is applied
- **THEN** the unit's intent is the new one, and nothing else changes

#### Scenario: A unit in code
- **WHEN** an amendment to a unit in code is applied
- **THEN** the unit's intent is the new one, the unit is marked amended, and the command answers once its write is made, naming no team, host or conductor

#### Scenario: A merged unit
- **WHEN** `crew unit amend` names a unit that has merged into its bolt
- **THEN** it is refused; what is needed is a fix or a new unit

### Requirement: A command reads each kit and the plan once, and fetches again only when refused
A crew command SHALL read each kit once and fetch the state branch once on each host it runs on, however many steps it has. A step that makes or removes a worktree in a kit SHALL leave the next step to read that kit again. A plan write SHALL start from the tip the command holds and fetch again only when its push is refused. The host's follower and `crew events --follow` SHALL check at each look whether what they read has moved, and read again only what has.

#### Scenario: Bolts with three units in flight
- **WHEN** `crew bolts` runs for a partition whose one bolt has three units in flight on one host
- **THEN** that host reads the kit once and fetches the state branch once, and `openspec` is not started

#### Scenario: A write after the plan moved
- **WHEN** another agent's write lands on the state branch after a command fetched it, and the command then writes
- **THEN** the command's push is refused, it fetches the new tip and applies its change there, as any write does

#### Scenario: Nothing is left behind
- **WHEN** a command ends, whether it succeeded or was refused
- **THEN** what it kept for its steps is gone, and the next command reads afresh

#### Scenario: A follower's look after nothing moved
- **WHEN** the host's follower looks again and nothing it read has moved
- **THEN** it reads no kit and fetches no branch at that look

### Requirement: A bolt on GitHub is fetched before crew bolts and a landing read it
As main is read (plan.18), crew SHALL read a bolt on GitHub as the host last fetched it on every read of a kit and every refresh of the rail and the board, fetching nothing. `crew bolts` and a landing's submission SHALL fetch the kit's origin first. A fetch that fails SHALL be named with git's words, never read past to the host's copy.

#### Scenario: crew bolts after a landing elsewhere
- **WHEN** a merge has landed on GitHub's `bolt/b` since the host last fetched, and `crew bolts` runs
- **THEN** it fetches the kit's origin once on the kit's host and shows the merged unit as `merged`

#### Scenario: The board does not fetch
- **WHEN** the rail's or the board's refresh reads the kit
- **THEN** no fetch is run, and the bolt is read at `origin/bolt/b` as the host last fetched it

#### Scenario: A fetch that fails
- **WHEN** `crew bolts` runs and the fetch of the kit's origin on the kit's host fails
- **THEN** the kit's stages read `unknown`, naming that GitHub could not be fetched and git's words, and nothing is read from the host's `bolt/b`

### Requirement: A bolt's work starts by crew bolt start
`crew bolt start <bolt>` SHALL make `bolt/<bolt>` through sluice from the kit's main, in the checkout the partition's main-level host keeps of the kit, mark the bolt `Path: flume` and request a launch of each unit and chore of it in its repository, with its `After` and priority and naming no host or stream, for a runner whose configuration names the repository to take, in one plan write, starting no agent, and record `bolt.start`. A proposal MAY hold it; the user runs it directly; no other agent SHALL. It SHALL be refused, with the plan unchanged and no branch made, while that host keeps no checkout of the kit or is held, or no runner answers for the partition.

#### Scenario: A bolt is started
- **WHEN** the user approves a proposal holding `crew bolt start b`, a bolt of switchboard-kit with two units, and a runner answers for wldn
- **THEN** `bolt/b` is made on GitHub by sluice, `b` is marked `Path: flume`, two launch requests name switchboard-kit and no host or stream, no agent starts, and the run record has `bolt.start` on `bolt/b`

#### Scenario: A partition no runner answers for
- **WHEN** `crew bolt start b` runs and wldn's state repository holds no runner's branch
- **THEN** it is refused, naming that no runner answers for wldn, the plan is unchanged and no branch is made

#### Scenario: An agent starts a bolt directly
- **WHEN** `wldn-ops` runs `crew bolt start b` outside a proposal
- **THEN** it is refused, naming the planner and the user, and the plan is unchanged

### Requirement: A fix names its bolt, and a fix of main its kit alone
`crew fix <bolt> <name> "<words>"` SHALL request a fix place on `bolt/<bolt>`, and `crew main fix <kit> <name> "<words>"` one on the kit's main, each in the kit's repository and naming no host or stream, for a runner whose configuration names it to take, in the stream its host maps it to. Neither SHALL take a team; `--drop` SHALL drop either's launch, and `crew fix` SHALL take no `--merge`, `--wait` or `--bolt`. A fix of main where no runner answers for the partition SHALL be refused, naming it.

#### Scenario: A fix on a bolt
- **WHEN** wldn-planner runs `crew fix b zone-check "the zone check fails on tenants with no region"`
- **THEN** a launch request of a fix on `bolt/b` names its kit's repository and the words and no host or stream, and no slot or agent of crew's is involved

#### Scenario: A team's name where the bolt goes
- **WHEN** an agent runs `crew fix swb-1 zone-check "<words>"` and no bolt is named `swb-1`
- **THEN** it is refused, naming no bolt `swb-1`, and nothing is requested

### Requirement: A unit's stage is read from the runner, or from the plan before its bolt starts
crew SHALL read each unit's and chore's stage from the plan, the runner's records and its bolt's landings alone, never from a place in the kit: `queued` while it has no bolt; for a bolt not started, `ready`, or `waiting` while it names `After` work, which builds only once the bolt starts; for a started bolt, as "A started bolt's work reads its stage from the runner's records", "A launched place's stage is where Flume's status has it" and "A unit whose work its bolt's branch holds is built" give it, `landed` once main holds its change, open or archived, or a chore's trailer; and `unknown`, naming why, where crew cannot read what it rests on. Nothing SHALL be kept by hand to say how far work has got.

#### Scenario: Queued work
- **WHEN** a unit has no bolt
- **THEN** its stage is `queued`

#### Scenario: A bolt not started
- **WHEN** bolt `y` is planned and not started, unit `a` names no `After` and `b` has `After: a`
- **THEN** `a` reads `ready` and `b` `waiting`, and nothing of a runner or a place in the kit is read for them

#### Scenario: Nothing kept by hand
- **WHEN** `x` is started and deneb's runner reports `a`'s place in code with 6 of 26 tasks ticked
- **THEN** `crew bolts` shows `a` at `code 6/26`, and no file was edited to say so

#### Scenario: A worktree of crew's from before
- **WHEN** a `unit/a` worktree from before teams left stands under the kit's `places/` with every task ticked, and `x` is started
- **THEN** `a`'s stage is the runner's, and nothing of that worktree is read for it

### Requirement: A unit whose work its bolt's branch holds is built
crew SHALL read a started bolt's unit or chore as `merged`, at the landing's commit and time, once a landing sluice made on the bolt's first-parent line names its place's branch, `change/<unit>` or `chore/<chore>`, in its `Sluice-From`. This holds whatever the runner reports of the place and whichever partition's launch made it, mapping no partition onto another. Where crew can't read the bolt's landings, the runner's reading SHALL stand.

#### Scenario: A place landed and tidied
- **WHEN** `a`'s place was never carried by the runner and `b`'s was last carried at submitted, Flume having tidied both after they landed, and `bolt/x` holds sluice's landings of `change/a` and `change/b`
- **THEN** `a` and `b` read `merged` at their landings, a batch reads each at its landing, and `a` reads `landed` once main holds its change

#### Scenario: A launch refused for a change the bolt holds
- **WHEN** `a`'s place ran as another partition's launch and landed on `bolt/x`, and the runner refused this partition's launch of `a` because the base bolt already holds a change named `a`
- **THEN** `a` reads `merged` at its landing, nothing waits on it, and `crew bolts` shows `a` merged, naming `change/a` and the landing's commit

#### Scenario: Read once main holds the bolt
- **WHEN** `x` has landed on main and main has moved on since
- **THEN** `bolt/x`'s landings of `change/a` and `chore/c` still read, at the same commits, so its close finds main holding each

#### Scenario: Built with no launch here
- **WHEN** this partition holds no launch of `a`, and `bolt/x` holds a landing naming `change/a`
- **THEN** `a` reads `merged`, and a landing naming any other branch builds nothing

#### Scenario: Proven from its landings
- **WHEN** every piece of `x` reads merged from its landings and sluice passed the landing at `x`'s head
- **THEN** `x` waits to land

#### Scenario: Landings crew can't read
- **WHEN** git can't list the landings on `bolt/x`
- **THEN** each piece of `x` reads as the runner's records give it

### Requirement: A fix whose place's landing its bolt's branch holds is merged
crew SHALL read a fix on a started bolt as `merged`, at the landing's commit and time, once a landing sluice made on the bolt's first-parent line names the fix's place's branch, `fix/<bolt>--<name>`, in its `Sluice-From`, whatever the runner last carried of its place. A landing whose time is before the fix's launch SHALL build nothing of that fix. A fix of a kit's main SHALL never be read from a bolt's landings. Where crew can't read the bolt's landings, the runner's reading SHALL stand.

#### Scenario: A landed fix whose place the runner last carried at submitted
- **WHEN** fix `x--tidy`'s place was last carried by the runner at submitted, Flume having tidied it after it landed, and `bolt/x` holds sluice's landing naming `fix/x--tidy`, made after the fix's launch
- **THEN** `fix/x/tidy` reads `merged` at that landing, and `crew bolts` shows it merged, naming `fix/x--tidy` and the landing's commit

#### Scenario: A fix launched again under a landed fix's name
- **WHEN** `bolt/x` holds a landing naming `fix/x--tidy` made before the standing launch of `fix/x/tidy`, an earlier launch of that name having been dropped after its place landed
- **THEN** `fix/x/tidy` reads its stage from the runner's records

#### Scenario: Landings crew can't read
- **WHEN** git can't list the landings on `bolt/x`, and the runner last carried `fix/x/tidy`'s place at submitted
- **THEN** `fix/x/tidy` reads submitted

### Requirement: A fix read merged from its bolt's landing holds nothing
`crew bolts`, the board, the bolt's landing and `crew fix <bolt> <name> --drop` SHALL read a fix through its bolt's landings alike. A fix read merged SHALL hold its bolt's landing no longer, and its drop SHALL be refused as any merged fix's is.

#### Scenario: A landed fix holds its bolt's landing no longer
- **WHEN** every unit of `x` has merged, sluice passed the landing at `x`'s head, and `fix/x/tidy` reads merged from its landing while the runner last carried it at submitted
- **THEN** no fix is in flight on `x`, and `x` reads proven

#### Scenario: A landed fix is not dropped
- **WHEN** `fix/x/tidy` reads merged from its landing on `bolt/x`, and the planner runs `crew fix x tidy --drop`
- **THEN** it is refused, saying the fix has merged into `bolt/x`, and nothing is appended to `requests.rec`

#### Scenario: A fix whose landings crew can't read still holds
- **WHEN** git can't list the landings on `bolt/x`, and the runner last carried `fix/x/tidy`'s place at submitted
- **THEN** `fix/x/tidy` is in flight on `x`, and holds its landing

### Requirement: A bolt's landing is read from its kit's main
crew SHALL read a started bolt's landing from its kit's main's first-parent line, branch standing or not: the newest merge there since the bolt's first launch whose `Sluice-From` names `bolt/<bolt>`, or whose second parent is a head crew submitted of the bolt or its branch's head. An older merge SHALL be no landing of it. Where git can't read main's line, the landing SHALL be unread, said so.

#### Scenario: A bolt landed through a pull request, its branch gone
- **WHEN** swancloud's main holds `4acecf09`, with `Sluice-From: afterthought-ops (pull/377)` and second parent `900527e9`, the head of `x`'s `bolt.submit`, and GitHub has deleted `bolt/x`
- **THEN** `x`'s landing reads `4acecf09`

#### Scenario: A landing that names the bolt's branch
- **WHEN** main holds a merge whose `Sluice-From` is `bolt/x (bolt/x)`, made after `x`'s first launch, and crew recorded no submission of `x`
- **THEN** `x`'s landing reads that merge

#### Scenario: An earlier bolt of the same name
- **WHEN** main holds a merge whose `Sluice-From` names `bolt/x`, made before the standing `x`'s first launch by an `x` that landed and left the plan
- **THEN** it is no landing of the standing `x`

#### Scenario: main's line can't be read
- **WHEN** git can't list main's first-parent line in `x`'s kit
- **THEN** `x`'s landing is unread, said so, and nothing of `x` reads landed from it

### Requirement: A landed bolt's pieces are read from its landing
Once main holds a started bolt's landing, crew SHALL read the bolt's landings, by the branches they name, from that landing's second parent back to its first parent. It SHALL read each unit, chore and fix of the bolt from them, as "A unit whose work its bolt's branch holds is built" and "A fix whose place's landing its bolt's branch holds is merged" have it, whatever the runner carried of its places. A bolt whose every piece reads landed SHALL read landed.

#### Scenario: The landed unit of a bolt whose branch and places are gone
- **WHEN** `x`'s landing on main is `4acecf09`, `900527e9`'s first-parent line holds sluice's landing naming `change/a`, GitHub has deleted `bolt/x`, and deneb's runner answered `a`'s launch `launched` and carries no place of it
- **THEN** `a` reads `landed`, and `x` reads landed in `crew bolts` and on the board

#### Scenario: A piece its landing does not name
- **WHEN** `x`'s landing on main holds a landing naming `change/a` and none naming `change/b`, and the runner reads `b` at code
- **THEN** `a` reads `landed`, `b` reads code, and `x` does not read landed

### Requirement: crew reads each kit by the name its record gives it
crew SHALL read a kit by the name each of its records gives it: a `Repo` in the plan, `requests.rec` or the run record; the kit in a fix of main's work or a card key; and the repository a source names. No reader SHALL map one kit's name to another's, through `kit.rename` entries or any list of former names. A partition's kits SHALL be the names its plan and its landings give, each once.

#### Scenario: Landings under another name
- **WHEN** madswan's plan names `timber`, and its run record holds a `bolt.land` with `Repo: tailrace` and, after it, a `kit.rename` entry of `tailrace` to `timber`
- **THEN** madswan's kits are `tailrace` and `timber`, each once, on the board too, and the agents' views keep the keys the mod reads

#### Scenario: A launch read as written
- **WHEN** request 1 launched `one-seam-turns-every-credential-into-a-principal` with `Repo: flywheel-cloud`, and the run record holds a `kit.rename` entry of `flywheel-cloud` to `boomdrive-cloud`
- **THEN** crew reads request 1 as `flywheel-cloud`'s launch, and no runner is read as having taken `boomdrive-cloud`'s work from it

#### Scenario: A fix of main read as written
- **WHEN** the fix of main `x` was launched as `fix/main/tailrace/x`, its code delivered and its submission held, and the run record holds a `kit.rename` entry of `tailrace` to `timber`
- **THEN** it is shown on `tailrace`'s landings row, and `crew main fix timber x --send` is refused as no launch of `fix/main/timber/x` standing

#### Scenario: A source read as written
- **WHEN** a unit's source names `WilldanGroup/old-board:docs/adr/0017`, and the work's kit is `switchboard-kit`
- **THEN** a proposal resting on it reads record 0017 of `WilldanGroup/old-board`, as the source names it

### Requirement: A command given a kit writes it as given
A plan command given a kit by `--repo`, `bolt new`, `unit add` and `chore add` among them, SHALL write the kit as it was given. It SHALL read the kit through no rename and say nothing of one. A unit or chore given `--repo` with `--bolt` SHALL be refused unless `--repo` names the bolt's kit as the plan writes it.

#### Scenario: A kit given by --repo is written as given
- **WHEN** the run record holds a `kit.rename` entry of `tailrace` to `timber`, and the user runs `crew bolt new y "…" --repo tailrace`
- **THEN** bolt `y` is written with `Repo: tailrace`, and its answer says nothing of a rename

#### Scenario: A chore given another name of its bolt's kit
- **WHEN** bolt `trc-1` is in `timber`, the run record holds a `kit.rename` entry of `tailrace` to `timber`, and the planner adds `chore add bump "…" --bolt trc-1 --repo tailrace`
- **THEN** it is refused naming `trc-1` as in `timber`, not `tailrace`, and the plan is unchanged

### Requirement: A repository is renamed by one explicit command
`crew kit rename <old> <new>` SHALL rename a repository in crew's records as one act: one commit with one `kit.rename` entry. Nothing SHALL rename a repository on its own. The rename SHALL append no request and SHALL launch, retry or drop nothing. A proposal MAY hold it, applied as any of its commands, and the user MAY run it at a shell. The planner's direct run SHALL be refused naming `crew plan propose`, and any other agent crew started SHALL be refused naming the planner.

#### Scenario: The user renames tailrace once its work is finished
- **WHEN** madswan's plan holds no bolt, unit or chore in `tailrace`, its run record holds two `bolt.land` entries with `Repo: tailrace`, no card, batch or open proposal names it, deneb's runner reports `agentplot/timber` and not `agentplot/tailrace` in `repositories.rec`, and the user runs `crew kit rename tailrace timber --label madswan`
- **THEN** one commit renames its records, no request is appended, and the run record holds one `kit.rename` entry naming both names

#### Scenario: A proposal holds it
- **WHEN** madswan-planner proposes `kit rename tailrace timber` and the user approves it
- **THEN** the approval's one commit renames the records, and its entry's `From` names `proposal/<n>` beside `kit/tailrace`

#### Scenario: The planner and the other agents
- **WHEN** madswan-planner runs `crew kit rename tailrace timber`, and madswan-ops runs the same
- **THEN** the planner's run is refused naming `crew plan propose`, and ops's naming the planner

### Requirement: A rename waits until the repository's work is finished
`crew kit rename <old> <new>` SHALL be refused, with nothing written, naming all that stands, while `<old>`'s work stands, matched by name or address:
- a bolt, unit or chore of the plan;
- a fix of its main or a role's work in it, not landed or dropped;
- a place Flume holds live;
- a card open under `land/<old>` or `record/<old>/<n>`;
- an unanswered batch holding its work that still waits;
- an open proposal, but the one applying it, whose `Do` names it.

#### Scenario: A bolt not landed
- **WHEN** madswan's plan holds bolt `trc-1` with `Repo: tailrace`
- **THEN** `crew kit rename tailrace timber` is refused naming `trc-1` as not landed, and nothing is written

#### Scenario: A fix of main not landed
- **WHEN** request 9 launched `fix/main/tailrace/cargo-lock` with no drop, and deneb's runner carries its place at code
- **THEN** the rename is refused naming the fix and its stage

#### Scenario: A place Flume holds live
- **WHEN** deneb's runner carries Flume's status of request 4's place, launched with `Repo: tailrace`, its phase live
- **THEN** the rename is refused naming the place and deneb

#### Scenario: An open card
- **WHEN** madswan-ops holds a card open under `land/tailrace`, or its last card there was closed as lost to its owner
- **THEN** the rename is refused naming `land/tailrace` and madswan-ops

#### Scenario: An unanswered batch
- **WHEN** batch 12 holds a unit of a landed `tailrace` bolt beside a unit of another kit that still waits, and the user has not answered it
- **THEN** the rename is refused naming batch 12

#### Scenario: An open proposal names it
- **WHEN** proposal 170 is open and one of its `Do` lines holds `--repo tailrace`, an object built on `tailrace` or a source `agentplot/tailrace:docs/adr/0017`
- **THEN** the rename is refused naming proposal 170, while a goal whose words mention tailrace names nothing

#### Scenario: Several things stand
- **WHEN** bolt `trc-1` has not landed and madswan-ops holds a card open under `land/tailrace`
- **THEN** the one refusal names both

### Requirement: A rename waits until no host keeps the old name
`crew kit rename <old> <new>` SHALL be refused while any host still keeps `<old>`, naming the host and what keeps it. The hosts read SHALL be each host with a runner branch of the partition, and the partition's main-level host. A host's keeping SHALL be its runner's `repositories.rec` where that runner reports one, and otherwise the host's spaces in the hosts file. Where crew can't read something this depends on, it SHALL be refused naming what it could not read. No host needs to keep `<new>`.

#### Scenario: A host still keeps it
- **WHEN** deneb's runner reports `agentplot/tailrace` among its repositories
- **THEN** the rename is refused naming deneb's runner and `agentplot/tailrace`

#### Scenario: A runner that reports no repositories
- **WHEN** deneb's runner branch holds no `repositories.rec` and deneb's spaces in the hosts file keep `agentplot/tailrace`
- **THEN** the rename is refused naming deneb's spaces and `agentplot/tailrace`

#### Scenario: What crew can't read
- **WHEN** deneb's runner branch can't be read, or a runner's host is neither reporting its repositories nor listed in the hosts file
- **THEN** the rename is refused naming that host and why, and nothing is written

#### Scenario: The new name kept by no host
- **WHEN** no host keeps `timber` or `tailrace`, and nothing else stands
- **THEN** `crew kit rename tailrace timber` renames the records

### Requirement: A rename takes only a name some record holds, and a new name of its own
`crew kit rename <old> <new>` SHALL be refused, with nothing written, where `<old>` and `<new>` name one repository, where `<new>` is the name of one of the partition's bolts, since `land/<new>` would name the bolt, and where no record of the partition names `<old>`.

#### Scenario: No record names it
- **WHEN** no record of madswan names `rocs-kit`
- **THEN** `crew kit rename rocs-kit rocs --label madswan` is refused saying no record names `rocs-kit`

#### Scenario: One repository, or a bolt's name
- **WHEN** the user runs `crew kit rename tailrace agentplot/tailrace`, or `crew kit rename tailrace crew-bolt` where `crew-bolt` is a bolt of madswan
- **THEN** the first is refused as two names of one repository and the second naming the bolt, and nothing is written

### Requirement: A rename renames every record a reader matches the repository by
In its one commit, `crew kit rename <old> <new>` SHALL rename `<old>` to `<new>` in each plan Source naming a decision record in `<old>`'s repository; each request's `Repo`, and a fix of its main's `Work`; and each run-record entry on the branch, its `Repo` and the objects of its `On` and `From` built on the name. A field keeps its form: a name becomes `<new>`'s, an address `<owner>/<old>` becomes `<owner>/<new>` unless `<new>` is an address, and an object takes `<new>`'s name.

#### Scenario: A request, a landing, a card and a source
- **WHEN** request 3 has `Repo: flywheel-cloud` and `Work: fix/main/flywheel-cloud/one-seam`, a `bolt.land` entry has `Repo: flywheel-cloud`, a closed landings card's `card.post` has `On: kit/flywheel-cloud` and `Key: land/flywheel-cloud`, a crew unit's Source names `agentplot/flywheel-cloud:docs/adr/0017`, and the user renames `flywheel-cloud` to `boomdrive-cloud`
- **THEN** the request's `Repo` is `boomdrive-cloud` and its `Work` `fix/main/boomdrive-cloud/one-seam`, the landing's `Repo` is `boomdrive-cloud`, the `card.post` has `On: kit/boomdrive-cloud` and keeps `Key: land/flywheel-cloud`, the Source names `agentplot/boomdrive-cloud:docs/adr/0017`, and the entry's `Count` is 4

#### Scenario: Every object built on the name
- **WHEN** entries name `kit/tailrace`, `land/tailrace`, `queue/tailrace`, `record/tailrace/0017` and `fix/main/tailrace/cargo-lock` in their `On` or `From`, and the user renames `tailrace` to `timber`
- **THEN** each names `timber` in its place, and an object of another repository, `kit/tailrace-web`, is as it was

#### Scenario: A forge address keeps its owner
- **WHEN** a request has `Repo: agentplot/flywheel-cloud` and the user renames `flywheel-cloud` to `boomdrive-cloud`
- **THEN** its `Repo` is `agentplot/boomdrive-cloud`

### Requirement: A rename leaves what no reader looks a repository up from
`crew kit rename` SHALL leave as written the plan's Goals and Intents, a Source naming no decision record, `proposals.rec`, signals, `moves.rec`, `asks.rec`, `roles.rec`, an entry's `Key`, `Why` and `Refused`, every `kit.rename` entry, the runners' branches and each host's own run-record files. It SHALL rewrite a file record by record, its descriptor, comments and order kept, and SHALL leave a file in which it renames no record byte for byte.

#### Scenario: What stays as written
- **WHEN** a bolt's Goal says "tailrace", a closed proposal's `Do` holds `--repo tailrace`, an earlier `kit.rename` entry has `From: kit/tailrace`, and the user renames `tailrace` to `timber`
- **THEN** each is as it was, and a run-record file naming no `tailrace` is unchanged byte for byte

### Requirement: A rename run again renames what an earlier one left
`<old>` MAY be any name a record still holds, so running `crew kit rename <old> <new>` again renames whatever an earlier rename left under `<old>`, writing its own entry. Before it reads the branch, the rename SHALL push the entries its own host kept unpushed, so they are renamed with the rest.

#### Scenario: Run again over what an earlier rename left
- **WHEN** madswan's plan names `boomdrive-cloud` while request 3 and two landings still name `flywheel-cloud`, and the user runs `crew kit rename flywheel-cloud boomdrive-cloud --label madswan`
- **THEN** request 3 and both landings name `boomdrive-cloud`, the entry's `Count` is 3, and the earlier `kit.rename` entry is as it was

#### Scenario: The host's kept entries go first
- **WHEN** deneb kept a `bolt.land` entry under `tailrace` unpushed, and the user runs the rename on deneb
- **THEN** crew pushes that entry before it reads the branch, and the rename's commit renames it with the others
