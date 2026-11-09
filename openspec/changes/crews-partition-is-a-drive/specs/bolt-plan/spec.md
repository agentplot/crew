## MODIFIED Requirements

### Requirement: What is in flight can be read from anywhere
`crew bolts [<bolt>] [--json]` SHALL list each of the drive's bolts with its repo, its kit's host and its state, each unit's and chore's stage and place, the fixes in flight on it, and the queue. Bolts with no work started, and queued work, SHALL be listed without reaching any host. Each host holding a bolt's work SHALL be read once. No line SHALL name a team.

#### Scenario: A host is unreachable
- **WHEN** the box is asleep
- **THEN** its bolts are listed from the plan, with every stage shown as unknown and the host named

### Requirement: Work is queued from a signal
`crew unit add … --signal <id>` SHALL queue the unit with the signal as its source, `signals/<id>`, and SHALL record the signal's one move, `route`, targeting the unit, in `moves.rec` on the drive's branch, in the same commit as the unit. A signal that is missing from the drive's first blueprints repo, already moved, or whose move would fail `recfix --check` SHALL be refused, and nothing written.

#### Scenario: A signal routed to work
- **WHEN** the planner queues a unit from a signal
- **THEN** one commit on the drive's branch adds the unit with `Source: signals/<id>` and a `route` move for that signal

#### Scenario: A signal in another blueprints repo
- **WHEN** madswan's planner queues a flywheel-next unit, whose design is in agentplot/blueprints, from a signal in afterthought/blueprints, the drive's first blueprints repo
- **THEN** the unit's `Source` is `signals/<id>`, which names that signal in afterthought/blueprints, and the route move is in `moves.rec` on `madswan/main`, in the same commit as the unit

#### Scenario: A signal already moved
- **WHEN** the signal named already has its move
- **THEN** the command is refused, naming the move it has, and the plan is unchanged

### Requirement: A drive keeps one plan in its state repository
Each drive SHALL keep one plan, the recutils file `plan.rec` on its branch of its state repository, for all of its kits. The plan SHALL hold only Bolt and Unit records. A Bolt has its name, repo, goal and sources. A Unit has its name, repo, bolt, intent, sources and dependencies (`After`); a Unit record marked `Kind: chore` is a chore, whose intent is its words. The plan SHALL hold what is meant to be built and any hold on it, never how far the work has got. A Bolt record that still carries a `Team` field, written before teams left, SHALL be read as any bolt, the field read by nothing; a new branch's schema SHALL allow no `Team`.

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

#### Scenario: A bolt given before teams left
- **WHEN** `plan.rec` holds a Bolt record with `Team: swb-1`, and its branch's schema allows the field
- **THEN** `recfix --check` passes, `crew bolts` shows the bolt with no team, and the next write leaves the field as it is

#### Scenario: A new branch
- **WHEN** `crew state init` starts a drive's branch
- **THEN** its `plan.rec` declares no `Team` field and its `proposals.rec` no `Agreed` field

### Requirement: A launched place's stage is where Flume's status has it
Once launched, a unit, chore or fix SHALL read queued while Flume waits for room; construct, code with its ticked tasks of all, or verify while a stage runs; needing an answer with the agent's question when it stopped short asking; its stage, sent back, with sluice's words when a submission failed or conflicted; submitted with sluice's number; waiting on its caller, with Flume's words and the stage it waits to retry or its submission, whenever Flume's status says it waits on its caller for a retry, past its kind's bound among them, whatever stage it last delivered; stalled once Flume's status says it is stalled; merged once it has landed on its bolt and landed once its bolt has; or dropped.

#### Scenario: A unit in code
- **WHEN** deneb's runner record for `a`'s launch carries Flume's status of its place in code with three of seven tasks ticked
- **THEN** `crew bolts` shows `a` at `code 3/7`

#### Scenario: A construct that asked
- **WHEN** the runner's record shows `a`'s construct stopped short with "Which drive's rail?"
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

### Requirement: A command reads each kit and the plan once, and fetches again only when refused
A crew command SHALL read each kit once and fetch the state branch once on each host it runs on, however many steps it has. A step that makes or removes a worktree in a kit SHALL leave the next step to read that kit again. A plan write SHALL start from the tip the command holds and fetch again only when its push is refused. The host's follower and `crew events --follow` SHALL check at each look whether what they read has moved, and read again only what has.

#### Scenario: Bolts with three units in flight
- **WHEN** `crew bolts` runs for a drive whose one bolt has three units in flight on one host
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

### Requirement: A bolt's work starts by crew bolt start
`crew bolt start <bolt>` SHALL make `bolt/<bolt>` through sluice from the kit's main, in the checkout the drive's main-level host keeps of the kit, mark the bolt `Path: flume` and request a launch of each unit and chore of it in its repository, with its `After` and priority and naming no host or stream, for a runner whose configuration names the repository to take, in one plan write, starting no agent, and record `bolt.start`. A proposal MAY hold it; the user runs it directly; no other agent SHALL. It SHALL be refused, with the plan unchanged and no branch made, while that host keeps no checkout of the kit or is held, or no runner answers for the drive.

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
`crew fix <bolt> <name> "<words>"` SHALL request a fix place on `bolt/<bolt>`, and `crew main fix <kit> <name> "<words>"` one on the kit's main, each in the kit's repository and naming no host or stream, for a runner whose configuration names it to take, in the stream its host maps it to. Neither SHALL take a team; `--drop` SHALL drop either's launch, and `crew fix` SHALL take no `--merge`, `--wait` or `--bolt`. A fix of main where no runner answers for the drive SHALL be refused, naming it.

#### Scenario: A fix on a bolt
- **WHEN** wldn-planner runs `crew fix b zone-check "the zone check fails on tenants with no region"`
- **THEN** a launch request of a fix on `bolt/b` names its kit's repository and the words and no host or stream, and no slot or agent of crew's is involved

#### Scenario: A team's name where the bolt goes
- **WHEN** an agent runs `crew fix swb-1 zone-check "<words>"` and no bolt is named `swb-1`
- **THEN** it is refused, naming no bolt `swb-1`, and nothing is requested

### Requirement: A unit whose work its bolt's branch holds is built
crew SHALL read a started bolt's unit or chore as `merged`, at the landing's commit and time, once a landing sluice made on the bolt's first-parent line names its place's branch, `change/<unit>` or `chore/<chore>`, in its `Sluice-From`. This holds whatever the runner reports of the place and whichever drive's launch made it, mapping no drive onto another. Where crew can't read the bolt's landings, the runner's reading SHALL stand.

#### Scenario: A place landed and tidied
- **WHEN** `a`'s place was never carried by the runner and `b`'s was last carried at submitted, Flume having tidied both after they landed, and `bolt/x` holds sluice's landings of `change/a` and `change/b`
- **THEN** `a` and `b` read `merged` at their landings, a batch reads each at its landing, and `a` reads `landed` once main holds its change

#### Scenario: A launch refused for a change the bolt holds
- **WHEN** `a`'s place ran as another drive's launch and landed on `bolt/x`, and the runner refused this drive's launch of `a` because the base bolt already holds a change named `a`
- **THEN** `a` reads `merged` at its landing, nothing waits on it, and `crew bolts` shows `a` merged, naming `change/a` and the landing's commit

#### Scenario: Read once main holds the bolt
- **WHEN** `x` has landed on main and main has moved on since
- **THEN** `bolt/x`'s landings of `change/a` and `chore/c` still read, at the same commits, so its close finds main holding each

#### Scenario: Built with no launch here
- **WHEN** this drive holds no launch of `a`, and `bolt/x` holds a landing naming `change/a`
- **THEN** `a` reads `merged`, and a landing naming any other branch builds nothing

#### Scenario: Proven from its landings
- **WHEN** every piece of `x` reads merged from its landings and sluice passed the landing at `x`'s head
- **THEN** `x` waits to land

#### Scenario: Landings crew can't read
- **WHEN** git can't list the landings on `bolt/x`
- **THEN** each piece of `x` reads as the runner's records give it

### Requirement: crew reads each kit by the name its record gives it
crew SHALL read a kit by the name each of its records gives it: a `Repo` in the plan, `requests.rec` or the run record; the kit in a fix of main's work or a card key; and the repository a source names. No reader SHALL map one kit's name to another's, through `kit.rename` entries or any list of former names. A drive's kits SHALL be the names its plan and its landings give, each once.

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

### Requirement: A rename waits until no host keeps the old name
`crew kit rename <old> <new>` SHALL be refused while any host still keeps `<old>`, naming the host and what keeps it. The hosts read SHALL be each host with a runner branch of the drive, and the drive's main-level host. A host's keeping SHALL be its runner's `repositories.rec` where that runner reports one, and otherwise the host's spaces in the hosts file. Where crew can't read something this depends on, it SHALL be refused naming what it could not read. No host needs to keep `<new>`.

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
`crew kit rename <old> <new>` SHALL be refused, with nothing written, where `<old>` and `<new>` name one repository, where `<new>` is the name of one of the drive's bolts, since `land/<new>` would name the bolt, and where no record of the drive names `<old>`.

#### Scenario: No record names it
- **WHEN** no record of madswan names `rocs-kit`
- **THEN** `crew kit rename rocs-kit rocs --label madswan` is refused saying no record names `rocs-kit`

#### Scenario: One repository, or a bolt's name
- **WHEN** the user runs `crew kit rename tailrace agentplot/tailrace`, or `crew kit rename tailrace crew-bolt` where `crew-bolt` is a bolt of madswan
- **THEN** the first is refused as two names of one repository and the second naming the bolt, and nothing is written
