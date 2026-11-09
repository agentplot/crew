# bolt-teams Specification

## Purpose
A bolt team builds one bolt at a time and holds at most one more that waits to land: a standing conductor and ops, and units built stage by stage by fresh agents. The bolt is a branch that moves only through sluice, and lands on main once its verification is green.

## Requirements

### Requirement: A landing records the commit main holds
The act that reads a started bolt's base place landed ("A landing is recorded by the first act that reads it in the runner's report") SHALL close the bolt in main-level ops's name by one `bolt.land` entry. The entry SHALL name the kit the bolt landed on and, as its `Head`, the commit Flume's status names the base place landed at, as the runner carries it. Its `Age` and `Split` SHALL be those the bolt's time gives from the run record, none read from sluice (`plan.20`). The close SHALL take the bolt and its work out of the plan and close its kit's landings card naming that commit and the fleet's timer. It SHALL delete no branch and remove no worktree. `crew bolt land` on a started bolt SHALL close it the same way, or at the landing its kit's main holds ("A bolt whose landing main holds closes whatever the runner carried of its places"). It SHALL be refused, recording nothing, while its base place does not read landed with its commit and its kit's main holds no landing of it, naming its landing as the runner's report has it.

#### Scenario: The landing's commit
- **WHEN** the runner carries the base place of switchboard-kit's bolt `y` over, landed at `9c1e4b7`, and the raise of switchboard-kit's landings card reads `y`
- **THEN** the run record holds a `bolt.land` on `bolt/y` in ops's name naming switchboard-kit and `9c1e4b7` as its head, `y` and its work are gone from the plan, and no branch is deleted and no worktree removed

#### Scenario: Its time from the run record
- **WHEN** `y`'s close is recorded
- **THEN** its `Age` and `Split` are those its row shows from the run record, and no sluice history is read

#### Scenario: Closed by hand before it landed
- **WHEN** `crew bolt land y` runs while the runner carries `y`'s base place with its submission `#412` under test, and switchboard-kit's main holds no landing of `y`
- **THEN** it is refused, saying `y`'s landing is `#412` under test, and nothing is recorded

### Requirement: A bolt's proof is its verification
A bolt SHALL be proven by its verification alone: its head is the landing of its work, as the runner reports it (merge-gate "A bolt's verification is its work's landing at its head, as the runner reports it"). Nobody SHALL deploy the bolt or work a list from its changes to prove it. Ops SHALL prove and deploy nothing. crew SHALL offer the bolt for landing, as its row on its kit's landings card, once every unit and chore of it has merged and its verification is green.

#### Scenario: Ready to land
- **WHEN** every unit of a bolt has merged and `crew bolts` shows its verification green
- **THEN** the bolt is a row of its kit's landings card, in main-level ops's name, and no one is asked to prove it

#### Scenario: Not yet green
- **WHEN** every unit of a bolt has merged and its head is no landing of its work that the runner reports
- **THEN** the bolt is not offered for landing, and `crew bolts` says what its verification is

### Requirement: A crew change's tasks each name their check
crew's `openspec/config.yaml` SHALL hand crew's construct, as rules for `tasks`, that each task is one sentence naming the check in crew's tiers that proves it, with a pointer to its reasoning; that no task is a deploy, a step on a live host or the user's, or work done after the landing; and that the tasks end with the tests the change affects, not the whole suite, which the merge gate runs. Its apply guidance SHALL tell crew's coder to tick a task only once the check it names passes.

#### Scenario: A crew construct asks for the tasks' instructions
- **WHEN** a construct in crew runs `/opsx:propose` and OpenSpec gives it the instructions for `tasks`
- **THEN** their rules say each task names the check that proves it, the tasks end with the tests the change affects, and no task is a deploy or work after the landing

#### Scenario: A crew coder ticks a task
- **WHEN** a crew coder runs `/opsx:apply` on a change
- **THEN** the guidance OpenSpec hands it says to tick a task only once the check the task names passes

#### Scenario: Another kit's agents
- **WHEN** a construct or coder works a change of another kit
- **THEN** OpenSpec hands it that kit's config, and nothing of crew's conventions reaches it

### Requirement: A crew change holds no proof list
crew's `openspec/config.yaml` SHALL hand crew's construct, as rules for `design`, that a task's full brief goes under *Task notes*, headed by the task's number; that a design holds no proof list of any name; and that *After deploy* lists only the steps no check can be code, each saying why, with its environments and its doer. As a rule for `specs`, it SHALL say that a scenario no check proves is a check the change adds (`docs.6`).

#### Scenario: A scenario no check proves
- **WHEN** a crew construct writes a scenario that no existing check proves
- **THEN** its tasks add the check that proves it, and its design lists no hand step for it

#### Scenario: Nothing to do after a deploy
- **WHEN** a crew change has no step that only a person or a live host can do
- **THEN** its design's *After deploy* says none and why, and it has no *Proof in dev* or *Proof on real work* section

### Requirement: A landing that did not land is the bolt's only for its own content
When the runner's report has a started bolt's landing refused by Flume's verdict, crew SHALL judge it the bolt's by the verdict alone, never by its words: a verdict `failed`, whatever check its words name or none, and a verdict `conflict`, with the files and main's revision Flume's words name. Flume's failed verdict carries sluice's words alone, with no mark of a check that never ran, so every failed verdict is the bolt's (record 0056; this departs from `plan.18`'s reading of 2026-10-24). The bolt's SHALL be recorded refused at its head. crew's words on the bolt's head line SHALL say what comes next and name no team or conductor: a conflict is taken in by the take-main fix crew launches on the bolt, ops starting nothing, and a failed check is a fix on the bolt that ops starts with Flume's words. Any other end with the bolt not on main SHALL be a stop ("A landing stopped by nothing of the bolt's is recorded stopped, and its send is spent").

#### Scenario: A conflict is the bolt's
- **WHEN** the runner carries `z`'s base place with the verdict conflict on `README.md`
- **THEN** the run record's `bolt.submit` for `z` carries `Refused` and its head, and `crew bolts` says the conflict is the bolt's and that crew launches the fix that takes main into it, naming no team or conductor

#### Scenario: A check that ran and failed
- **WHEN** the runner carries `z`'s base place with the verdict failed, Flume's words naming `tests:logic` as failing
- **THEN** the landing is the bolt's and recorded refused, as for a conflict, and crew's words tell ops to start a fix on the bolt with Flume's words, `crew fix z <name> "<Flume's words>"`

#### Scenario: A failed verdict that names no check that ran
- **WHEN** the runner carries `z`'s base place with the verdict failed, Flume's words naming a check the host could not run
- **THEN** the landing is the bolt's and recorded refused, not stopped

### Requirement: A submission's number is on its bolt's row from the submit
crew SHALL show each piece's sluice submission and the bolt's landing on the bolt's row in `crew bolts`, text and JSON. It SHALL show them from the first read after the submit or the land, whoever made it:

- **A piece's submission.** While a unit's, chore's or fix's submission stands, its line SHALL show the submission's number, `submitted #<n>`, from Flume's status of the piece's place as the runner carried it (`runner.stage_of`).
- **The bolt's landing.** The bolt's head line SHALL show its landing as the runner's report and the run record give it (`runner.landing_of`, `plan.landing_phase`): `landing asked, request <n>` while its land is unanswered, `landing #<n>` with the entry's state while Flume's submission of it waits or is under test, `landed at <commit>`, or refused or stopped in its words.

crew SHALL read neither from sluice's queue. It SHALL run no `sluice overview` for a bolt's row. Its JSON SHALL give no line a `submission`, and no bolt a `landing` or a `submissions_error`, read from sluice.

#### Scenario: A unit's merge under test
- **WHEN** the runner carries the place of unit `a` with its submission `#41` under test on `bolt/y`
- **THEN** the next `crew bolts` shows `a`'s line with `submitted #41`, its JSON gives `a`'s stage as `submitted` with submission `41`, and no sluice command is run

#### Scenario: A bolt's landing asked
- **WHEN** the user's send has posted request 57, a land of `y`'s launch, and the runner has not answered it
- **THEN** `crew bolts` shows `y`'s head line saying `landing asked, request 57`

#### Scenario: A bolt's landing queued on main
- **WHEN** the runner carries `y`'s base place with its submission `#412` under test on main
- **THEN** `crew bolts` shows `y`'s head line saying `landing #412 under test`, and no sluice command is run

#### Scenario: Read again after the session that submitted it ended
- **WHEN** the session in unit `a`'s place has ended, and the runner still carries `a`'s submission `#41` waiting on `bolt/y`
- **THEN** `crew bolts` still shows `a`'s line with `submitted #41`

#### Scenario: Decided
- **WHEN** sluice lands `#41` on `bolt/y`, and the runner carries `a`'s place landed
- **THEN** `a`'s line shows no submission, and reads its stage as merged

#### Scenario: sluice's record can't be read
- **WHEN** `sluice overview --json` would fail on the kit's host, while the runner carries `a`'s submission `#41` waiting on `bolt/y`
- **THEN** `crew bolts` runs no sluice command, shows `a`'s line with `submitted #41`, and says nothing of sluice's queue on the bolt's head line

#### Scenario: A runner that can't be read
- **WHEN** the branch of the runner that took `a`'s launch can't be read
- **THEN** `crew bolts` names that runner as one that can't be read, the stages of its work unknown, no line shows a number, and no sluice command is run

### Requirement: A close crew refuses is said on the bolt's row and in the run record until it is lifted
When a landed bolt's close is refused, crew SHALL record a `bolt.land` entry on the bolt carrying the refusal in crew's words, and SHALL say the same words on standard error. While the plan still holds the bolt, each later read SHALL try the close again. A read SHALL record a new refused entry only when the words differ from the bolt's last refused `bolt.land` since its landing. The bolt's head line SHALL say it landed on main and was not closed, with the words of its last refused close, until a close succeeds.

#### Scenario: A chore still at ready
- **WHEN** `z` lands on main while its chore `tidy-z` is still at ready in the plan
- **THEN** the run record holds a refused `bolt.land` on `bolt/z` saying `tidy-z` has not landed on main, and `z`'s head line says it landed on main and was not closed, with those words

#### Scenario: The same refusal is recorded once
- **WHEN** three of the rail's sweeps in a row find `z`'s close refused for the same reason
- **THEN** the run record holds one refused `bolt.land` for it

#### Scenario: Lifted
- **WHEN** the planner drops `tidy-z` from the plan and the rail sweeps again on the kit's host
- **THEN** the read closes `z`, the run record holds its `bolt.land`, and no head line for `z` remains

### Requirement: A started bolt's work is launched whole
`crew bolt start <bolt>` SHALL make one plan write, `bolt.start`, refused for a bolt started already, but as "A start run again launches a bolt whose launch the runner refused" has it, and while no runner answers for the partition. It SHALL read no host, make no branch, and read neither the kit's policy nor any host's sluice. Its write SHALL set `Path: flume` on the bolt, and no `Team`, and append the bolt's own launch ("A start launches the bolt's base place before its pieces"), then a launch for each of its units and chores in the file's order, cut from `bolt/<bolt>`, in the kit's repository and naming no host or stream, for a runner whose configuration names the repository to take. It SHALL start, restart and greet no agent.

#### Scenario: A bolt of three
- **WHEN** `crew bolt start x` runs, `x` holding units `a` and `b`, `b` after `a`, and chore `c`, and a runner answers for madswan
- **THEN** the plan marks `x` `Path: flume` with no `Team`, `requests.rec` holds a launch of `crew/bolt` for `bolt/x` and after it three launches of `change`, `change` and `chore` on `bolt/x`, each in crew's repository and naming no host or stream, and no agent starts

#### Scenario: No runner on the host
- **WHEN** `crew bolt start x` runs and madswan's state repository holds no runner's branch
- **THEN** the start is refused naming that no runner answers for madswan, and the plan and `requests.rec` are unchanged

#### Scenario: A host that keeps no checkout of the kit
- **WHEN** `crew bolt start x` runs while madswan's main-level host keeps no checkout of `x`'s kit, and a runner answers for madswan
- **THEN** `x` is started as any bolt is, and nothing is read or run on that host

### Requirement: A launch carries its repository, priority, intent and recipient
Each launch of a started bolt's work SHALL name the kit's repository as the plan names it and no host or stream, a runner whose configuration names the repository taking it, in the stream its host's Flume configuration maps the repository to, the intent `<label>/<bolt>`, the recipient `<label>/planner`, a priority from its bolt's place in the plan, the highest first, and its brief, the work's own words as crew's prompts give them. A write that starts or reorders bolts SHALL append a priority for each launched place whose priority the plan's order changed.

#### Scenario: Two bolts in order
- **WHEN** `x` and then `y` are started, `x` above `y` in the plan
- **THEN** `x`'s launches carry a higher priority than `y`'s, each names crew's repository and no host or stream, intent `madswan/<bolt>` and recipient `madswan/planner`

#### Scenario: A reorder
- **WHEN** `crew bolt order` puts `y` above `x`
- **THEN** `requests.rec` gains a priority for each launched place of `x` and `y` whose priority changed, and none for another

### Requirement: A dependent launches once its After work has landed
A launch of work whose `After` names other work SHALL name those launches, and the runner SHALL launch it only once each of their places has landed on the bolt, answering it held meanwhile, so its place is cut from a bolt that holds their work.

#### Scenario: A dependent held
- **WHEN** `x` is started, `b` after `a`
- **THEN** `b`'s launch names `a`'s as its After, and `b` reads waiting on `a` until `a`'s place has landed on `bolt/x`

### Requirement: Plan writes reach a started bolt's places
Each as the write's own act, in its own commit: a unit or chore added to or moved into a started bolt SHALL be launched as the start launches it; an approved amendment of a unit whose place is launched SHALL be a retry of its construct with the amendment's words, and of one whose launch is held or unanswered a drop of that launch and a new launch carrying the amendment; a unit, chore or bolt dropped SHALL drop each of its launches still standing.

#### Scenario: An amendment of a unit in code
- **WHEN** the user approves an amendment of `a`, whose place on deneb's runner is in code
- **THEN** `requests.rec` gains a retry of `a`'s construct with the amendment's words, in the approval's commit

#### Scenario: A unit dropped
- **WHEN** the user approves dropping `c`, launched on started `x`
- **THEN** `requests.rec` gains a drop of `c`'s launch, in the approval's commit

### Requirement: Launched work keeps its bolt and order
A move out of a started bolt, a split, or a change of `After` on work whose launch is written SHALL be refused, naming its place and drop then add as the way on, since a place's base and order are fixed at its launch.

#### Scenario: A move of launched work
- **WHEN** a proposal moves `a`, launched on started `x`, to bolt `y`
- **THEN** the proposal is refused naming `a`'s place and that it is dropped and added again

### Requirement: A place is answered by a retry
`crew answer <work> "<words>"`, the planner's, the design agent's or main-level ops's, SHALL append a retry of the stage the work's place stopped short on or waits on, carrying the words, its agent kept open for the answer or not, and past its kind's bound or not, whatever stage it last delivered; or of its submission where that waits on its caller unheld. It SHALL be refused naming the place's stage when the place neither stopped short nor waits on its caller. For a live place, the refusal SHALL name that stage as the runner carried it, with the runner's host and when it carried it, and say that a wait Flume has told of since reaches crew with that runner's next carry. It SHALL be refused naming what crew could not read when it can't tell whether the place waits. It SHALL never say that a live place has nothing to answer.

#### Scenario: A construct that asked
- **WHEN** the runner's record shows `a`'s construct stopped short asking "Which partition's rail?", and the planner runs `crew answer a "madswan's"`
- **THEN** `requests.rec` gains a retry of `a`'s construct with the words `madswan's`

#### Scenario: A stop-short whose agent is kept open
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place, its code ended short needing an answer with its agent kept open, and the planner runs `crew answer a "Wait for the releases; retry once they land."`
- **THEN** `requests.rec` gains a retry of `a`'s code with those words, and nothing is refused

#### Scenario: A place past its bound
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place waiting on its caller to retry code past its bound, its verify delivered, and the planner runs `crew answer a "Take the bolt in and resolve the conflict."`
- **THEN** `requests.rec` gains a retry of `a`'s code with those words

#### Scenario: A submission that waits on its retry
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place waiting on its caller to retry its submission, which the merge queue refused, and the planner runs `crew answer a "Submit it again."`
- **THEN** `requests.rec` gains a retry of `a`'s submission with those words

#### Scenario: Nothing to answer
- **WHEN** deneb's runner last carried `a`'s place in code with no question, Flume may since have told the planner the place waits on its caller, and the planner runs `crew answer a "yes"`
- **THEN** it is refused naming `a`'s stage as code when deneb's runner carried it, at the time it carried it, and saying that a wait Flume has told of since reaches crew with that runner's next carry, never that there is nothing to answer, and `requests.rec` gains nothing

#### Scenario: A place the runner has not carried
- **WHEN** `a`, naming no `After`, is answered held with the runner's claim, or launched at a place whose status the runner has not carried, and `crew answer a "yes"` runs
- **THEN** it is refused saying crew can't tell whether `a`'s place waits on an answer, with the runner's words or that no status of the place is carried, and never that it is held for its After work

#### Scenario: Work that is over
- **WHEN** the runner's record shows `a`'s place landed on its bolt, and `crew answer a "yes"` runs
- **THEN** it is refused naming `a` merged, with nothing to answer

### Requirement: A fix is a fix place on its bolt
`crew fix <bolt> <name> "<words>"` SHALL append a launch of the fix kind on `bolt/<bolt>`, in its kit's repository and naming no host or stream, with nothing held; `--drop` SHALL drop it, and `--merge`, `--wait` and `--bolt` SHALL be no options it has. A fix in flight SHALL hold its bolt's landing.

#### Scenario: A review note marked fix
- **WHEN** the planner runs `crew fix x rail-word "Say 'land' for a started bolt"` on a batch's note
- **THEN** `requests.rec` gains a launch of `fix` named `x--rail-word` on `bolt/x`, and `x`'s landing row says it lands once that fix has merged or been dropped

### Requirement: A landing that conflicts with main takes main in by a fix place
When the runner's report has a started bolt's landing refused by Flume's verdict conflict, and its base place names no landing fix, the first act of crew's that reads it SHALL append a launch of a fix on the bolt named `take-main-<main's revision, seven>`, in its kit's repository and naming no host or stream, its brief saying to take `origin/main` into the bolt with Flume's words of the conflict, unless a fix of that name already stands. Where the base place names a landing fix, Flume's landing fix SHALL take main in and crew SHALL append nothing. The bolt's row SHALL say it takes main first.

#### Scenario: A landing refused for a conflict
- **WHEN** a raise of the kit's landings card reads the runner carrying `x`'s base place, naming no landing fix, with the verdict conflict against main at `4d3d9be`
- **THEN** `requests.rec` gains one launch of `fix` named `x--take-main-4d3d9be` with Flume's words of the conflict, and `x`'s row says it takes main first

#### Scenario: Read twice
- **WHEN** a later read of the same verdict finds `x--take-main-4d3d9be` standing
- **THEN** no second launch is appended

#### Scenario: Refused with Flume's landing fix
- **WHEN** a raise reads `x`'s base place with the verdict conflict against main at `4d3d9be` and its landing fix `x-1` live
- **THEN** `requests.rec` gains no launch, and `x`'s row says it takes main first, naming `x-1`

### Requirement: A bolt whose work is on main lands by its close alone
`crew bolt land` SHALL land a bolt never started, with no base place and no launch of its work, on the user's word, once its kit's main holds each of its units' changes, open or archived, and each of its chores. It SHALL read them in the checkout the partition's main-level host keeps of its kit, since no runner took any of its work. It SHALL record in its `bolt.land` entry the kit and the commit that main holds. It SHALL merge, submit and post nothing for it, and run no sluice. It SHALL be refused for such a bolt with no units or chores, whose kit that host keeps no checkout of, or while any unit's change is not on main.

#### Scenario: A bolt built outside its branch
- **WHEN** the plan holds the bolt `deploys-go-through-crew`, never started, and each of its units' changes is archived on crew's main
- **THEN** `crew bolt land deploys-go-through-crew` removes it and its units from the plan, the landing's entry names crew and the commit its main holds, and nothing is asked of the runner

#### Scenario: A unit not yet on main
- **WHEN** one unit of such a bolt has no change on its kit's main
- **THEN** `crew bolt land` is refused, naming the unit and its stage

### Requirement: A crew agent carries its name for sluice
Every agent crew starts SHALL have `SLUICE_AGENT` in its environment, the same as its `CREW_AGENT`, from its start and again when herdr resumes it where crew gives it its identity back; a main level's agent herdr resumes off its main level's host SHALL have neither (`main-level`).

#### Scenario: A main-level agent starts
- **WHEN** crew starts `wldn-ops`
- **THEN** its environment holds `CREW_AGENT=wldn-ops` and `SLUICE_AGENT=wldn-ops`

#### Scenario: herdr resumes an agent
- **WHEN** herdr resumes `wldn-planner`'s session on wldn's main-level host without crew's environment
- **THEN** its commands see `SLUICE_AGENT` back, the same as its `CREW_AGENT`

#### Scenario: herdr resumes a main level's agent on another host
- **WHEN** herdr resumes `swancloud-planner`'s session on a host the teams file does not name for swancloud's main level
- **THEN** its commands see neither `CREW_AGENT` nor `SLUICE_AGENT`

### Requirement: No brief names a proof list
No brief crew gives an agent SHALL name a proof list, a task's shape or a design's sections, and the results section every brief carries SHALL name no proof list.

#### Scenario: The planner's brief
- **WHEN** the planner's brief, or any brief's results section, is printed
- **THEN** it names no *Proof in dev* list, no *Task notes* section and no shape for a task

### Requirement: A landing queued holds its bolt's work
crew SHALL read a bolt's landing from the run record as one of four states, each its own. **Queued** runs from the `bolt.submit` that records a land of the bolt asked until an entry records that land's outcome. **Rejected** holds once the newest land's outcome is recorded refused, for the bolt's own content, a failed check or a conflict, with its head, until a land is asked again. **Landing again** is queued once more after a rejection. **None** is a bolt never asked to land, landed, or stopped by nothing of the bolt's.

While a bolt's landing is queued or landing again, these SHALL be refused, naming the landing with its request or, once Flume names one, its merge queue entry, with nothing written or launched: `crew unit add` and `crew chore add` into the bolt, `crew unit move` and `crew chore move` into it, and `crew fix <bolt> <name>`. That holds whether they run directly or as a proposal's commands, at the proposal's check and at its approval. Each SHALL read the state from the run record at the tip its write is applied to. Once the bolt's landing is rejected, or with none, they SHALL go on as for any started bolt. `crew fix <bolt> <name> --drop`, the take-main fix crew launches on reading a conflict, and a proposal's card as it is drawn SHALL read no state.

`crew bolts`, text and JSON, the rail's line under land and the board's head line SHALL each say the state in words of their own. A landing queued is said with its request, or with its merge queue entry and its state once Flume names one. A landing again is said so, with the entry Flume's verdict refused before it. A rejection is said, while the bolt's head is the one refused, as the landing refused and the bolt open for work, in Flume's words. The rail SHALL leave a bolt whose landing is queued or landing again out of the bolts that can land.

#### Scenario: A unit added while the landing is queued
- **WHEN** the user's send has posted request 57, a land of `z`'s launch, the runner has not decided it, and the user approves the planner's proposal adding unit `b` to `z`
- **THEN** the approval is refused, saying `z`'s landing is asked of the runner as request 57, so unit `b` does not join it until the landing is decided, and to put it on another bolt; `requests.rec` gains nothing

#### Scenario: A fix while the landing is queued
- **WHEN** the runner carries `z`'s base place with its submission `#412` under test, and main-level ops runs `crew fix z logic "Fix tests:logic."`
- **THEN** it is refused naming `#412`, and no fix is launched

#### Scenario: A rejection opens the bolt for work
- **WHEN** the runner's report has `#412`'s verdict failed, Flume's words naming `tests:logic`, and the read records it
- **THEN** `crew bolts`, the rail and the board say `z`'s landing `#412` was refused at its head and the bolt is open for work, in Flume's words, and ops's `crew fix z logic "<Flume's words>"` is launched

#### Scenario: Landing again
- **WHEN** the fix has merged into `z`, the user's send has posted a land of `z` again, and the runner carries it as `#415` under test
- **THEN** `crew bolts`, the rail and the board say `z` is landing again as `#415`, after `#412` was refused; a unit added to `z` is refused naming both; and the rail leaves `z` out of the bolts that can land

#### Scenario: A wait sluice itself failed on
- **WHEN** Flume's wait on sluice's record of `z`'s submission `#412` fails, and the runner carries the base place with Flume's words that it could not read the submission
- **THEN** `z`'s landing still reads queued as `#412`, and its work is held until a read records `#412`'s outcome

#### Scenario: Another bolt's landing
- **WHEN** `y`'s landing is queued and the user adds a unit to `z`
- **THEN** the unit is added to `z` and launched

### Requirement: crew bolts says a bolt carries another bolt's work
`crew bolts` SHALL say under a bolt whose kit's read says it carries another bolt's work that main lacks that its landing is held, naming that bolt and its landings, and SHALL give it in its JSON as `carries`, or why it can't be read as `carries_error`. A kit's read SHALL leave out a bolt's ref another command removed while it read, and SHALL name a line git can't list.

#### Scenario: crew bolts shows a bolt carrying another's work
- **WHEN** the kit's read says bolt `y` carries bolt `x`'s landing `f5e67f35`
- **THEN** `crew bolts` shows under `y` "landing: held: carries bolt x's work, its landing f5e67f3, which main lacks", and its JSON gives `carries`

#### Scenario: A bolt's ref goes while the kit is read
- **WHEN** a fetch removes `origin/bolt/gone` while a kit's read lists the bolts' lines
- **THEN** `gone` is left out of the lines, and no bolt is read as unreadable for it

### Requirement: A bolt is a base place of crew's kind
A started bolt SHALL be a Flume base place of crew's kind `crew/bolt@1`, which lands with no stages, its package in crew's kinds folder (flume-source; record 0056). Its branch `bolt/<bolt>` SHALL be made from main by sluice at the launch, landed by Flume on the runner's land, and ended by sluice once the place has landed or been dropped. crew SHALL make, move, submit and delete no bolt branch, and SHALL make no worktree on one.

#### Scenario: A bolt's launch names crew's kind
- **WHEN** `crew bolt start x` runs and a runner answers for madswan
- **THEN** its launch of `bolt/x` names `Kind: crew/bolt`, and crew makes no `bolt/x` branch and no worktree

#### Scenario: A landed bolt's branch is Flume's and sluice's
- **WHEN** the runner carries `x`'s base place landed, and crew's next read closes `x`
- **THEN** crew deletes no branch and removes no worktree for `x`

### Requirement: A start launches the bolt's base place before its pieces
`crew bolt start`'s write SHALL append the bolt's own launch first, on `Base: main`, with the `Priority` of its place in the plan, `Intent: <label>/<bolt>` and `Recipient: <label>/ops`, naming no host or stream, with no `Brief`, since a base place runs no agent, and no `After`. Each unit's and chore's launch SHALL follow it in the file, on `Base: bolt/<bolt>`, naming no `After` on the bolt's launch, since a base place lands only after every place on its branch.

#### Scenario: The bolt's own launch
- **WHEN** `crew bolt start x` runs in madswan and a runner answers for madswan
- **THEN** the first request the write appends is a launch of `bolt/x` with `Kind: crew/bolt`, `Name: x`, `Base: main`, `Intent: madswan/x`, `Recipient: madswan/ops` and `x`'s priority, naming no host or stream and carrying no `Brief` or `After`

#### Scenario: Its pieces after it
- **WHEN** `crew bolt start x` runs, `x` holding unit `a`, and unit `b` after `a`
- **THEN** `a`'s and `b`'s launches follow `x`'s in `requests.rec` on `Base: bolt/x`, `b`'s `After` names `a`'s launch, and neither names `x`'s

### Requirement: A bolt's launch, its pieces' and its land are checked before they are appended
crew SHALL refuse, naming the field, a launch of `bolt/<bolt>` that names a kind but `crew/bolt`, a base but `main`, a `Brief` or an `After`. It SHALL refuse a launch of other work that names `Kind: crew/bolt`. It SHALL refuse a `land` whose `Of` names no launch of a bolt or a fix of main, or whose `Work` is not that launch's.

#### Scenario: A fix on a bolt started before bolts were base places
- **WHEN** a fix's launch on `Base: bolt/y` is to be appended and `requests.rec` holds no launch of `bolt/y`
- **THEN** it is appended

#### Scenario: A bolt's launch with a brief
- **WHEN** a launch of `bolt/y` names a `Brief`
- **THEN** it is refused, naming `Brief`, and nothing is appended

#### Scenario: A land of a unit's launch
- **WHEN** a land whose `Of` names a unit's launch is to be appended
- **THEN** it is refused, naming the launch, and nothing is appended

#### Scenario: The requests file holds a bolt's launch and its land
- **WHEN** `requests.rec` holds a launch of `Kind: crew/bolt` and a land of it
- **THEN** `recfix --check` passes on it

### Requirement: A start run again launches a bolt whose launch the runner refused
A started bolt whose own launch the runner answered refused, as Flume refuses it while its host has not locked `crew/bolt@1`, SHALL stay started with nothing made for it, and `crew bolts` SHALL show it unlaunched in the runner's words (`read.1`). No read SHALL launch it again. `crew bolt start` run again on it SHALL drop each of its pieces' launches not yet launched, then launch the bolt anew and those pieces after it, in one write. Any other started bolt's start SHALL be refused.

#### Scenario: A kind its host has not locked
- **WHEN** `x` is started and the runner answers `x`'s launch refused, in Flume's words naming the lock `crew/bolt@1` lacks on its host
- **THEN** `x` stays started, `crew bolts` shows `x` unlaunched in those words, and no read of `x` appends a request

#### Scenario: Started again
- **WHEN** `crew bolt start x` runs on that `x`, its unit `a`'s launch not yet launched
- **THEN** one write appends a drop of `a`'s launch, then a launch of `bolt/x` and a launch of `a` after it

#### Scenario: A bolt whose launch is launched
- **WHEN** `x`'s base place is launched and `crew bolt start x` runs
- **THEN** it is refused, saying `x` is started already, and the plan and `requests.rec` are unchanged

### Requirement: A landing's outcome is read from the runner's report
crew SHALL read a started bolt's landing from its launch, the lands of it in `requests.rec`, and Flume's status of its base place as the runner that took the launch carries it, and from nothing else, as one outcome: unlaunched, none, asked, submitted, landed, refused for a failed check or a conflict, stopped, dropped, or unknown, naming why (`runner.landing_of`, `code.7`). Each fact SHALL be guarded, so a field the status lacks becomes no text (`read.2`).

#### Scenario: Unlaunched
- **WHEN** the runner has not answered `z`'s launch, or answered it held or refused
- **THEN** `z`'s landing reads unlaunched, in the runner's words where it gave any

#### Scenario: None
- **WHEN** `z`'s base place is launched and no land of it stands
- **THEN** `z`'s landing reads none

#### Scenario: Asked
- **WHEN** a land of `z`'s launch is posted as request 57 and the runner has not answered it
- **THEN** `z`'s landing reads asked, with request 57

#### Scenario: Under test
- **WHEN** the runner carries Flume 0.17.0's status of `z`'s base place with its submission `#412` under test
- **THEN** `z`'s landing reads submitted, with entry 412 under test

#### Scenario: Landed
- **WHEN** the runner carries `z`'s base place over, landed at `5d1a9e0`
- **THEN** `z`'s landing reads landed, with `5d1a9e0`

#### Scenario: A failed check
- **WHEN** the runner carries `z`'s base place waiting on its caller with the verdict failed and Flume's words
- **THEN** `z`'s landing reads refused, the bolt's, in those words

#### Scenario: A conflict
- **WHEN** the runner carries `z`'s base place with the verdict conflict on `README.md` against main at `4d3d9be`
- **THEN** `z`'s landing reads refused for a conflict, naming `README.md` and `4d3d9be`

#### Scenario: Withdrawn
- **WHEN** the runner carries `z`'s base place waiting on its caller with the verdict withdrawn
- **THEN** `z`'s landing reads stopped, in Flume's words

#### Scenario: A land the runner refused
- **WHEN** the runner answers `z`'s land refused, Flume's words saying a place on `bolt/z` is live
- **THEN** `z`'s landing reads stopped, in those words

#### Scenario: Dropped
- **WHEN** the runner carries `z`'s base place over, dropped
- **THEN** `z`'s landing reads dropped

#### Scenario: Flume could not read the submission
- **WHEN** the runner carries `z`'s base place with Flume's words that it could not read the submission
- **THEN** `z`'s landing reads unknown, in those words, and is read as no other outcome

#### Scenario: A runner that can't be read
- **WHEN** the branch of the runner that took `z`'s launch can't be read
- **THEN** `z`'s landing reads unknown, naming that runner, and is read as no other outcome

### Requirement: A landing is recorded by the first act that reads it in the runner's report
The first act on any host to read a bolt whose landing is decided SHALL record it: its kit's card's raise, the follower's sweep, a kit's read, or `crew bolt land` (`plan.21`); `crew bolts`, a view, SHALL write nothing (`state.4`). It SHALL write one `bolt.submit`, decided at its write's tip, with the outcome, the head, Flume's entry as `Submission` where it names one, and a refusal's or stop's words; nothing while it is asked, submitted or unknown.

#### Scenario: Nobody runs anything
- **WHEN** a land of `z` is posted, no agent of the partition runs a command, and the runner's branch then carries `z`'s base place landed at `5d1a9e0`
- **THEN** the next raise of `z`'s kit's landings card records `z`'s `bolt.submit` landed and its `bolt.land` at `5d1a9e0`, and closes `z`

#### Scenario: Two reads at once
- **WHEN** two reads of `z` find its base place landed, and the second's write is applied to a tip that holds the first's
- **THEN** the run record holds one `bolt.submit` outcome and one `bolt.land` for `z`, the second read writing nothing and recording no refused close

#### Scenario: crew bolts reads it
- **WHEN** `crew bolts` runs while the runner's report has `z`'s base place landed and no read has recorded it
- **THEN** `crew bolts` says `z` landed at Flume's commit and writes nothing, and the next raise of its kit's card or the follower's sweep records it

#### Scenario: Still under test
- **WHEN** a read finds `z`'s base place with its submission `#412` under test
- **THEN** nothing is recorded, and `z`'s last `bolt.submit` stays asked

#### Scenario: A conflict recorded by a later read
- **WHEN** the runner's report has `z`'s submission `#412` with the verdict conflict
- **THEN** the next read records `z`'s landing refused at its head in Flume's words, appends its take-main fix, and raises its kit's landings card with `z`'s row saying it takes main first

#### Scenario: A runner that can't be read
- **WHEN** the branch of the runner that took `z`'s launch can't be read
- **THEN** the read records nothing for `z`, and names that runner as one it could not read

### Requirement: A landing's record rests on the state repository alone
A read of a bolt's landing SHALL take its outcome from the runners' branches in the partition's state repository and reach no host over ssh for it (`read.5`). It SHALL rest nothing on Flume's notice of the end to `<label>/ops`, and SHALL record the outcome whether ops runs or not (`roles.6`).

#### Scenario: Read away from the kit's host
- **WHEN** `z`'s kit is kept by deneb's runner, and a read of `z` on mac-studio finds its base place landed on deneb's runner's branch
- **THEN** the read records `z` landed and closes it, and runs no ssh to deneb

#### Scenario: Ops is not running
- **WHEN** `z`'s base place reads landed while no session of `<label>/ops` runs
- **THEN** the next raise of `z`'s kit's landings card records `z` landed and closes it

### Requirement: A landing stopped by nothing of the bolt's is recorded stopped, and its send is spent
When the runner answers a bolt's land refused, or Flume's verdict on its submission is withdrawn or refused, crew SHALL record the landing stopped at the bolt's head, in the runner's or Flume's words, with no refusal, and SHALL hold nothing of the bolt for it. The send that ticked the bolt SHALL be spent: a land of it SHALL be posted again only on a new send of the user's. Its row keeps its box, as rail-cards has it.

#### Scenario: A place on the branch is live
- **WHEN** the runner answers `z`'s land refused, Flume's words saying a place on `bolt/z` is live
- **THEN** the run record's `bolt.submit` for `z` carries no `Refused`, its `Outcome` stopped, its `Why` those words and its `Head`, and `crew bolts` says `z`'s landing stopped in those words

#### Scenario: No land again on the same send
- **WHEN** `z`'s landing is recorded stopped and its kit's landings card is raised again on the send that ticked it
- **THEN** no land of `z` is posted, and once the user sends the card again with `z` ticked, one land of `z` is posted

### Requirement: A bolt lands on the user's send alone, carried to the runner as a land
A started bolt whose verification is green SHALL land only by a `land` of its launch that crew posts on the user's send of its row on its kit's landings card (rail-cards). The runner SHALL carry it out with Flume, which submits the base place's branch through sluice onto GitHub's main as a merge commit (record 0056; `plan.8`, `plan.16`). No agent SHALL run anything to land a bolt. Each bolt's land SHALL be its own, one refused or stopped holding no other. A landing SHALL deploy nothing.

#### Scenario: The bolt lands
- **WHEN** bolt `x` reads proven and the user sends its kit's landings card with `x` ticked
- **THEN** `requests.rec` gains one land of `x`'s launch; once the runner's branch carries `x`'s base place landed at a commit, the next raise of the card records `x` landed at that commit and closes it, with no agent's command run between

#### Scenario: Three bolts on one send
- **WHEN** the user's send ticks `y`, `z` and `w` in that order, and the runner's report then carries `z`'s verdict conflict
- **THEN** lands of `y`, `z` and `w` are posted in that order, `y` and `w` land and are closed, and `z` reads refused for its conflict, its take-main fix launched

### Requirement: crew bolt submit lands nothing
`crew bolt submit`, run with any arguments but `-h` or `--help`, SHALL refuse at once, before it reads anything, saying it lands nothing and that a bolt lands on the user's send of its row on its kit's landings card, which crew carries to the runner as a land. It SHALL append and record nothing. With `-h` or `--help` among its arguments it SHALL print its usage and exit 0 (`code.11`).

#### Scenario: Ops runs it
- **WHEN** main-level ops runs `crew bolt submit y`
- **THEN** it is refused at once, before it reads the plan or any host, saying it lands nothing and that `y` lands on the user's send of its row on its kit's landings card, which crew carries to the runner as a land; nothing is appended or recorded

#### Scenario: Its help
- **WHEN** anyone runs `crew bolt submit --help`
- **THEN** it prints its usage and exits 0

### Requirement: A bolt's drop drops its base place last
A drop of a started bolt SHALL append, in the drop's commit, a drop of each of its pieces' launches still standing, then a drop of the bolt's own launch, the last. crew SHALL delete no branch for a drop. A dropped bolt's branch that holds work main lacks is kept by sluice and named in Flume's answer, which the runner carries; it SHALL be the user's to keep or delete (record 0003), and crew SHALL ask nothing for it.

#### Scenario: A drop's requests in order
- **WHEN** the user approves dropping started `x`, whose units `a` and `b` are launched
- **THEN** the drop's commit appends drops of `a`'s and `b`'s launches, then a drop of `x`'s launch, and no branch is deleted

#### Scenario: A dropped bolt's branch holds work main lacks
- **WHEN** the runner carries `x`'s base place dropped, Flume's answer naming `bolt/x` kept for work main lacks
- **THEN** crew appends no request for it and deletes nothing

### Requirement: A base place's drop the runner refused is asked again once nothing on its branch is live
Where the runner answered a bolt's drop refused, as Flume refuses it while a place on the bolt's branch is live, the next plan write that finds the bolt gone from the plan, its launch standing, no piece of it live and no landing fix of its base place live SHALL ask the drop again, once for each refusal (`runner.base_drop_due`).

#### Scenario: A refused drop asked again
- **WHEN** the runner answered `x`'s drop refused while `a`'s place was live, and a later plan write finds `x` gone from the plan, its launch standing and no place of its pieces live
- **THEN** that write appends one drop of `x`'s launch, and a write after it, while that drop is unanswered, appends none

#### Scenario: Not while a piece is live
- **WHEN** the runner answered `x`'s drop refused and `a`'s place is still live
- **THEN** no plan write asks the drop again

#### Scenario: Not while a landing fix is live
- **WHEN** the runner answered `x`'s drop refused and `x`'s base place lists its landing fix `x-1` live
- **THEN** no plan write asks the drop again, and the first write after `x-1` has ended appends one

### Requirement: A bolt started before bolts were base places lands under the crew that started it
crew SHALL read a started bolt with no launch of `bolt/<bolt>` in `requests.rec` as one whose branch sluice made before bolts were base places: `crew bolts` SHALL say it lands under the crew that started it, and its row SHALL have no box (rail-cards). No land SHALL be posted for it. A drop of it SHALL drop its pieces' launches still standing and ask nothing for its branch, which SHALL stay, named in the drop's words, the user's.

#### Scenario: crew bolts says so
- **WHEN** started bolt `y` has its units' launches in `requests.rec` and no launch of `bolt/y`
- **THEN** `crew bolts` says `y` was started before bolts were base places and lands under the crew that started it

#### Scenario: No land is posted
- **WHEN** the raise of `y`'s kit's landings card reads a send that ticked `y`
- **THEN** no land is posted for `y`

#### Scenario: A drop of it
- **WHEN** the user approves dropping `y`, its unit `a`'s launch standing
- **THEN** the drop's commit appends a drop of `a`'s launch and no request for `bolt/y`, and the drop says `bolt/y` stays, the user's to keep or delete

### Requirement: No crew command runs sluice, wt or gh for a bolt, or moves a checkout
No crew command SHALL run a `sluice`, `wt` or `gh` command for a bolt's start, branch, landing, close or drop, or for the tidy of its kit (record 0056; `state.5`). crew's only sluice commands SHALL be a card's preview's: `sluice preview`, `sluice previews` and `sluice release` of a preview. No crew command SHALL write a checkout's `HEAD`, index or refs, but the remote-tracking refs a fetch writes: crew levels no checkout and moves no anchor (`plan.18`).

#### Scenario: crew's code names no such command
- **WHEN** `plugin/lib/plan.py`, `gather.py`, `kit.py`, `board.py`, `runner.py` and `plugin/bin/crew` are read as text
- **THEN** none holds a `sluice` command, `wt submit`, `wt merge`, `wt remove`, a `gh` command or `read-tree` outside the functions that bring up, list or release a card's preview and the scripts only they run

#### Scenario: A bolt from its start to its close
- **WHEN** a bolt runs from `crew bolt start` to its close on the stubs
- **THEN** the stubs' log holds no `sluice`, `wt` or `gh` call, and each kit's `HEAD`, index and refs are as they were before the start, but its remote-tracking refs

### Requirement: crew removes no worktree, and names a landing's left from before
crew SHALL remove no worktree and delete no branch of a kit. Its tidy SHALL run no sluice and no `wt`, and SHALL name each `<kit>/places/land-<bolt>` and `<kit>/bolts/<bolt>` it finds, with the commands that remove it, `sluice release --worktree <path>` then `wt remove`, as the user's to run (record 0056). It SHALL leave every other worktree as it is: the main checkout, a place of Flume's, one the user made, one on no branch.

#### Scenario: A landing's worktree from before
- **WHEN** a kit checkout holds `places/land-y` on `bolt/y`, left by a landing an older crew made
- **THEN** the tidy leaves it, names it with `sluice release --worktree <path>` then `wt remove` as the user's to run, and runs neither

#### Scenario: A bolt's worktree from before record 0026
- **WHEN** a kit checkout holds `bolts/z`
- **THEN** the tidy leaves it and names it with the same commands, the user's to run

#### Scenario: A worktree made by hand
- **WHEN** a kit checkout has a worktree beside `main` that the user made, on a branch of their own
- **THEN** crew leaves it as it is

#### Scenario: A place of Flume's
- **WHEN** a kit checkout has `places/change--x` on `change/x`, a place Flume made
- **THEN** crew neither removes it nor makes it ready

#### Scenario: A merge partway through its rebase
- **WHEN** a place is on no branch because a rebase stopped partway
- **THEN** crew leaves it as it is

### Requirement: A bolt carrying another bolt's work is asked no land
Another bolt's work is a commit on that bolt's first-parent line beyond main, as the kit's read holds the branches. crew SHALL post no land for a bolt whose head holds such a commit that main lacks, off its own first-parent line, whatever the user's send ticked, its row held naming each bolt and its landings (rail-cards). The bolt whose work was carried SHALL NOT be held for it. No land SHALL be posted for a bolt whose carried work can't be read, its row saying why.

#### Scenario: A bolt built on another bolt's landing posts no land
- **WHEN** bolt `popover`'s branch holds bolt `deleting`'s landing `f5e67f35`, which main lacks, and a raise of its kit's landings card reads a send that ticked `popover`
- **THEN** no land of `popover` is posted, and its row is held naming bolt `deleting` and its landing `f5e67f3`

#### Scenario: The bolt whose work was carried lands
- **WHEN** `popover` carries `deleting`'s landing, and the send ticked `deleting`
- **THEN** a land of `deleting` is posted, since it holds nothing on `popover`'s first-parent line

#### Scenario: Main holds the carried work
- **WHEN** `deleting` has landed on main and its branch is gone, and the send ticked `popover`
- **THEN** `popover` carries nothing main lacks, and its land is posted as any bolt's is

#### Scenario: What a head carries can't be read
- **WHEN** the kit's read could not list a bolt's own commits beyond main, and the send ticked `popover`
- **THEN** no land of `popover` is posted, and its row says why

### Requirement: A landing Flume's verdict sent back is the bolt's fix
A landing whose verdict Flume gives as failed or conflict SHALL be the bolt's fix until a fix moves its head. crew SHALL name what failed in Flume's words and give the way on. Where the base place names a landing fix within its bound, the way on is Flume's landing fix. Where it names none, it is the take-main fix crew launches for a conflict, or the `crew fix` ops starts for a failed check. Past the bound, it is the fix ops starts. No land SHALL be posted at the head sent back. Once a fix has moved the head and the bolt reads proven, a land SHALL be posted again only as rail-cards has the send stand. No word SHALL name a team or a conductor.

#### Scenario: A check fails
- **WHEN** the runner carries `z`'s base place, as Flume 0.17.0 gives it, with `#7`'s verdict failed, Flume's words naming `tests:logic`, tested on main at `db8bc25`
- **THEN** `crew bolts` says `z` did not land, that a failed check is the bolt's, in Flume's words, and that ops starts `crew fix z <name> "<Flume's words>"`, naming no team or conductor

#### Scenario: A check fails with Flume's landing fix
- **WHEN** the runner carries `z`'s base place with `#7`'s verdict failed and its landing fix `z-1` for `#7` live
- **THEN** `crew bolts` says `z` did not land, in Flume's words, and that Flume's landing fix `z-1` makes the failed checks pass, naming no command for ops

#### Scenario: Read again at the head sent back
- **WHEN** the send that ticked `z` is read again while `z`'s head is still the one `#7` sent back
- **THEN** no land of `z` is posted, and `z` stays held on its row for its fix

#### Scenario: A conflict read again before its fix merged
- **WHEN** `z`'s landing was sent back for a conflict with main on `README.md`, its take-main fix was launched, crew's or Flume's, and the kit's landings card is raised again before that fix has merged
- **THEN** no land of `z` is posted and no second take-main fix is launched, its row saying it takes main first

#### Scenario: The take-main fix moves the head
- **WHEN** `z`'s take-main fix, crew's or Flume's, has merged and `z` reads proven at its new head
- **THEN** the next raise of its kit's landings card posts one land of `z` on the send that ticked it, asking the user nothing

### Requirement: A bolt's landing fix is read from its base place's status
crew SHALL read a started bolt's landing fix from Flume's status of its base place as the runner carries it, and from nothing else: the fix kind, the bound, and each fix Flume launched, with its cause and how it ended. Each fact SHALL be guarded, and a fix crew can't read whole SHALL be named, never guessed (`read.1`, `read.2`). A status that names no fix kind SHALL read as a base place whose landing fix Flume does not launch (`runner.landing_fix`, `code.7`).

#### Scenario: A host whose Flume names no fix kind
- **WHEN** the runner carries `y`'s base place as Flume 0.17.0 gives it, verdict failed
- **THEN** `y`'s landing reads refused for a failed check, its way on crew's

#### Scenario: A landing fix live
- **WHEN** the runner carries `y`'s base place with verdict conflict on `#412`, fix kind `flume/fix@1`, bound 3, and fix `y-1` for `#412` live
- **THEN** `y`'s landing reads refused for a conflict, its way on Flume's, with `y-1` live

#### Scenario: A landing fix due
- **WHEN** the runner carries `y`'s base place with verdict failed on `#412`, fix kind `flume/fix@1`, bound 3, and no fix
- **THEN** `y`'s landing reads refused, its way on Flume's, its landing fix due

#### Scenario: The bound spent
- **WHEN** the runner carries `y`'s base place with verdict failed on `#415`, bound 3, and three fixes, none for `#415`
- **THEN** `y`'s landing reads refused, its way on its caller's, naming three landing fixes run

#### Scenario: A fix dropped
- **WHEN** the runner carries `y`'s base place with verdict conflict on `#412` and fix `y-1` for `#412` dropped
- **THEN** `y`'s landing reads refused, its way on its caller's, naming `y-1` dropped

#### Scenario: A fix crew can't read
- **WHEN** a fix in `y`'s base place's status gives an end crew does not read
- **THEN** that fix is named as unread and counted toward no outcome

### Requirement: crew launches no fix and asks for none where Flume launches the landing fix
Where a refused landing's way on is Flume's, its landing fix live, landed or due within its bound, the first act of crew's that reads it SHALL record the refusal as before, and SHALL launch no take-main fix and ask main-level ops nothing.

#### Scenario: Flume's fix takes main in
- **WHEN** a raise of `land/crew` reads `y`'s landing refused for a conflict with `y-1` live
- **THEN** the run record gains `y`'s `bolt.submit` refused, `requests.rec` gains no launch, and ops is asked nothing

#### Scenario: Flume's fix due
- **WHEN** a raise reads `y`'s landing refused for a failed check, its landing fix due
- **THEN** no launch is appended and ops is asked nothing

### Requirement: A landing past its landing fixes is ops's
Where a refused landing's way on is its caller's, Flume's bound of landing fixes spent or its fix for the refusal dropped or not launched, the first act of crew's that reads it SHALL ask main-level ops once, keyed by the land's request, in Flume's words, naming how many landing fixes ran or how the fix ended, and SHALL launch no take-main fix.

#### Scenario: Past the bound
- **WHEN** a raise reads `y`'s landing refused with its three landing fixes run
- **THEN** ops is asked once, its words naming three landing fixes and Flume's words, and no launch is appended

#### Scenario: Read twice past the bound
- **WHEN** a later read finds the same refusal past the bound
- **THEN** ops is not asked again

### Requirement: A live landing fix holds its bolt
A live landing fix of a bolt's base place SHALL be a fix in flight on the bolt: its row SHALL have no box, no land of the bolt SHALL be posted while it is live, and a drop of the bolt the runner refused SHALL not be asked again until it has ended. Its note SHALL take main in for a forecast or a conflict, so the row takes main first and the send that ticked it stands through it, and SHALL name the failed checks for a failed submission.

#### Scenario: No land while it runs
- **WHEN** the user's send stands for `y` and `y-1` is live
- **THEN** no land of `y` is posted

#### Scenario: Taken main in
- **WHEN** `y-1`, which took main in, has landed and `y` reads proven at its new head with its own work unchanged
- **THEN** the next raise posts one land of `y` on the send that ticked it, asking the user nothing

#### Scenario: A drop while it runs
- **WHEN** the runner answered `y`'s drop refused and `y-1` is live
- **THEN** no plan write asks the drop again until `y-1` has ended

### Requirement: A landed bolt closes on its pieces' ends as the runner reports them
`crew bolt land`, and the landing's read that closes a landed bolt, SHALL close a started bolt once each of its units and chores reads merged, as the runner reports its place's end, at a commit its kit's main holds, its branch standing or not. No landing commit SHALL be read for it. A bolt with a piece that does not read so SHALL be refused, naming that piece and its stage, and nothing is removed.

#### Scenario: A landed bolt whose branch and places are gone
- **WHEN** `x` landed on main, GitHub has deleted `bolt/x`, Flume has tidied each of `x`'s places, and deneb's runner carries the record Flume holds for it of each, landed on `bolt/x` at a commit main holds
- **THEN** each of `x`'s units reads merged at the commit its record names, and `x`'s close is refused for none of them

#### Scenario: A piece whose end the runner never carried
- **WHEN** main holds `x`'s landing, the runner last carried `x`'s unit `b`'s place at submitted, Flume having tidied it holding no record for the runner, and a landing commit on `bolt/x` names `change/b` in its `Sluice-From`
- **THEN** `x`'s close is refused, naming `b` and that it has not merged into `bolt/x`: it is submitted
