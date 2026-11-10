## ADDED Requirements

### Requirement: A landed bolt is closed in ops's name and leaves the plan
The act that reads a started bolt's base place landed ("A landing is recorded by the first act that reads it in the runner's report") SHALL close the bolt in main-level ops's name by one `bolt.land` entry. The close SHALL take the bolt and its work out of the plan and close its kit's landings card naming the commit its base place landed at and the fleet's timer. It SHALL delete no branch and remove no worktree.

#### Scenario: The landing's commit
- **WHEN** the runner carries the base place of switchboard-kit's bolt `y` over, landed at `9c1e4b7`, and the raise of switchboard-kit's landings card reads `y`
- **THEN** the run record holds a `bolt.land` on `bolt/y` in ops's name naming switchboard-kit and `9c1e4b7` as its head, `y` and its work are gone from the plan, and no branch is deleted and no worktree removed

### Requirement: A landing's entry names its kit, its head and its time
A landed bolt's `bolt.land` entry SHALL name the kit the bolt landed on and, as its `Head`, the commit Flume's status names the base place landed at, as the runner carries it, the record Flume holds for the runner after it tidies the base place among them. Its `Age` and `Split` SHALL be those the bolt's time gives from the run record, none read from sluice (`plan.20`).

#### Scenario: Its time from the run record
- **WHEN** `y`'s close is recorded
- **THEN** its `Age` and `Split` are those its row shows from the run record, and no sluice history is read

### Requirement: crew bolt land closes a started bolt only once its base place reads landed
`crew bolt land` on a started bolt SHALL close it the same way as the act that reads its base place landed. It SHALL be refused, recording nothing, while its base place does not read landed with its commit, naming its landing as the runner's report has it. No landing commit on its kit's main SHALL be read for it.

#### Scenario: Closed by hand before it landed
- **WHEN** `crew bolt land y` runs while the runner carries `y`'s base place with its submission `#412` under test
- **THEN** it is refused, saying `y`'s landing is `#412` under test, and nothing is recorded

#### Scenario: A base place held for the runner
- **WHEN** Flume landed `z`'s base place on main at `4acecf0` and tidied it, holding its record for the runner, which carries it as the base place's status, GitHub has deleted `bolt/z`, and ops runs `crew bolt land z`
- **THEN** `z` and its chore leave the plan, and the landing's entry names the kit and `4acecf0` in ops's name

#### Scenario: A landing main holds that the runner does not report
- **WHEN** `z`'s kit's main holds a landing naming `bolt/z` in its `Sluice-From`, the runner carries no status of `z`'s base place, and ops runs `crew bolt land z`
- **THEN** it is refused, naming `z`'s landing as the runner's report has it, no kit is read, and nothing is recorded

### Requirement: A landing refused by Flume's verdict is the bolt's
When the runner's report has a started bolt's landing refused by Flume's verdict, crew SHALL judge it the bolt's by the verdict alone, never by its words: a verdict `failed`, whatever check its words name or none, and a verdict `conflict`, with the files and main's revision Flume's words name. The bolt's SHALL be recorded refused at its head.

#### Scenario: A conflict is the bolt's
- **WHEN** the runner carries `z`'s base place with the verdict conflict on `README.md`
- **THEN** the run record's `bolt.submit` for `z` carries `Refused` and its head, and `crew bolts` says the conflict is the bolt's and that crew launches the fix that takes main into it, naming no team or conductor

### Requirement: Every failed verdict is the bolt's, and any other end is a stop
Flume's failed verdict carries sluice's words alone, with no mark of a check that never ran, so every failed verdict is the bolt's (record 0056; this departs from `plan.18`'s reading of 2026-10-24). Any end but a verdict `failed` or `conflict` with the bolt not on main SHALL be a stop ("A landing stopped by nothing of the bolt's is recorded stopped, and its send is spent").

#### Scenario: A failed verdict that names no check that ran
- **WHEN** the runner carries `z`'s base place with the verdict failed, Flume's words naming a check the host could not run
- **THEN** the landing is the bolt's and recorded refused, not stopped

### Requirement: A landing that is the bolt's says what comes next on its head line
For a landing that is the bolt's, crew's words on the bolt's head line SHALL say what comes next and name no team or conductor: a conflict is taken in by the take-main fix crew launches on the bolt, ops starting nothing, and a failed check is a fix on the bolt that ops starts with Flume's words.

#### Scenario: A check that ran and failed
- **WHEN** the runner carries `z`'s base place with the verdict failed, Flume's words naming `tests:logic` as failing
- **THEN** the landing is the bolt's and recorded refused, as for a conflict, and crew's words tell ops to start a fix on the bolt with Flume's words, `crew fix z <name> "<Flume's words>"`

### Requirement: A piece's line shows its submission's number from the runner's report
crew SHALL show each piece's sluice submission on the bolt's row in `crew bolts`, text and JSON, from the first read after the submit, whoever made it. While a unit's, chore's or fix's submission stands, its line SHALL show the submission's number, `submitted #<n>`, from Flume's status of the piece's place as the runner carried it (`runner.stage_of`).

#### Scenario: A unit's merge under test
- **WHEN** the runner carries the place of unit `a` with its submission `#41` under test on `bolt/y`
- **THEN** the next `crew bolts` shows `a`'s line with `submitted #41`, its JSON gives `a`'s stage as `submitted` with submission `41`, and no sluice command is run

#### Scenario: Read again after the session that submitted it ended
- **WHEN** the session in unit `a`'s place has ended, and the runner still carries `a`'s submission `#41` waiting on `bolt/y`
- **THEN** `crew bolts` still shows `a`'s line with `submitted #41`

#### Scenario: Decided
- **WHEN** sluice lands `#41` on `bolt/y`, and the runner carries `a`'s place landed
- **THEN** `a`'s line shows no submission, and reads its stage as merged

### Requirement: A bolt's head line shows its landing from the runner's report
crew SHALL show a bolt's landing in `crew bolts`, text and JSON, from the first read after the land, whoever made it. The bolt's head line SHALL show its landing as the runner's report and the run record give it (`runner.landing_of`, `plan.landing_phase`): `landing asked, request <n>` while its land is unanswered, `landing #<n>` with the entry's state while Flume's submission of it waits or is under test, `landed at <commit>`, or refused or stopped in its words.

#### Scenario: A bolt's landing asked
- **WHEN** the user's send has posted request 57, a land of `y`'s launch, and the runner has not answered it
- **THEN** `crew bolts` shows `y`'s head line saying `landing asked, request 57`

#### Scenario: A bolt's landing queued on main
- **WHEN** the runner carries `y`'s base place with its submission `#412` under test on main
- **THEN** `crew bolts` shows `y`'s head line saying `landing #412 under test`, and no sluice command is run

### Requirement: A bolt's row reads nothing from sluice's queue
crew SHALL read neither a piece's submission nor a bolt's landing from sluice's queue. It SHALL run no `sluice overview` for a bolt's row. The JSON of `crew bolts` SHALL give no line a `submission`, and no bolt a `landing` or a `submissions_error`, read from sluice.

#### Scenario: sluice's record can't be read
- **WHEN** `sluice overview --json` would fail on the kit's host, while the runner carries `a`'s submission `#41` waiting on `bolt/y`
- **THEN** `crew bolts` runs no sluice command, shows `a`'s line with `submitted #41`, and says nothing of sluice's queue on the bolt's head line

#### Scenario: A runner that can't be read
- **WHEN** the branch of the runner that took `a`'s launch can't be read
- **THEN** `crew bolts` names that runner as one that can't be read, the stages of its work unknown, no line shows a number, and no sluice command is run

### Requirement: A refused close is recorded and said on the bolt's head line
When a landed bolt's close is refused, crew SHALL record a `bolt.land` entry on the bolt carrying the refusal in crew's words, and SHALL say the same words on standard error. The bolt's head line SHALL say it landed on main and was not closed, with the words of its last refused close, until a close succeeds.

#### Scenario: A chore still at ready
- **WHEN** `z` lands on main while its chore `tidy-z` is still at ready in the plan
- **THEN** the run record holds a refused `bolt.land` on `bolt/z` saying `tidy-z` has not landed on main, and `z`'s head line says it landed on main and was not closed, with those words

### Requirement: Each read tries a refused close again and records only new words
While the plan still holds a landed bolt whose close was refused, each later read SHALL try the close again. A read SHALL record a new refused entry only when the words differ from the bolt's last refused `bolt.land` since its landing.

#### Scenario: The same refusal is recorded once
- **WHEN** three of the rail's sweeps in a row find `z`'s close refused for the same reason
- **THEN** the run record holds one refused `bolt.land` for it

#### Scenario: Lifted
- **WHEN** the planner drops `tidy-z` from the plan and the rail sweeps again on the kit's host
- **THEN** the read closes `z`, the run record holds its `bolt.land`, and no head line for `z` remains

### Requirement: A bolt's start is one plan write that reads no host
`crew bolt start <bolt>` SHALL make one plan write, `bolt.start`, refused for a bolt started already, but as "A start run again launches a bolt whose launch the runner refused" has it, and while no runner answers for the drive. It SHALL read no host, make no branch, and read neither the kit's policy nor any host's sluice.

#### Scenario: No runner on the host
- **WHEN** `crew bolt start x` runs and madswan's state repository holds no runner's branch
- **THEN** the start is refused naming that no runner answers for madswan, and the plan and `requests.rec` are unchanged

#### Scenario: A host that keeps no checkout of the kit
- **WHEN** `crew bolt start x` runs while madswan's main-level host keeps no checkout of `x`'s kit, and a runner answers for madswan
- **THEN** `x` is started as any bolt is, and nothing is read or run on that host

### Requirement: A start marks the bolt Flume's and launches its pieces in order
`crew bolt start`'s write SHALL set `Path: flume` on the bolt, and no `Team`, and append the bolt's own launch ("A start launches the bolt's base place before its pieces"), then a launch for each of its units and chores in the file's order, cut from `bolt/<bolt>`, in the kit's repository and naming no host or stream, for a runner whose configuration names the repository to take. `crew bolt start` SHALL start, restart and greet no agent.

#### Scenario: A bolt of three
- **WHEN** `crew bolt start x` runs, `x` holding units `a` and `b`, `b` after `a`, and chore `c`, and a runner answers for madswan
- **THEN** the plan marks `x` `Path: flume` with no `Team`, `requests.rec` holds a launch of `crew/bolt` for `bolt/x` and after it three launches of `change`, `change` and `chore` on `bolt/x`, each in crew's repository and naming no host or stream, and no agent starts

### Requirement: A launch names its repository, intent, recipient, priority and brief
Each launch of a started bolt's work SHALL name the kit's repository as the plan names it and no host or stream, a runner whose configuration names the repository taking it, in the stream its host's Flume configuration maps the repository to, the intent `<label>/<bolt>`, the recipient `<label>/planner`, a priority from its bolt's place in the plan, the highest first, and its brief, the work's own words as crew's prompts give them.

#### Scenario: Two bolts in order
- **WHEN** `x` and then `y` are started, `x` above `y` in the plan
- **THEN** `x`'s launches carry a higher priority than `y`'s, each names crew's repository and no host or stream, intent `madswan/<bolt>` and recipient `madswan/planner`

### Requirement: A start or a reorder appends each priority it changed
A write that starts or reorders bolts SHALL append a priority for each launched place whose priority the plan's order changed.

#### Scenario: A reorder
- **WHEN** `crew bolt order` puts `y` above `x`
- **THEN** `requests.rec` gains a priority for each launched place of `x` and `y` whose priority changed, and none for another

### Requirement: An answer retries the stage or the submission its place waits on
`crew answer <work> "<words>"`, the planner's, the design agent's or main-level ops's, SHALL append a retry of the stage the work's place stopped short on or waits on, carrying the words, its agent kept open for the answer or not, and past its kind's bound or not, whatever stage it last delivered; or of its submission where that waits on its caller unheld.

#### Scenario: A construct that asked
- **WHEN** the runner's record shows `a`'s construct stopped short asking "Which drive's rail?", and the planner runs `crew answer a "madswan's"`
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

### Requirement: An answer to a place that does not wait is refused naming its stage
`crew answer` SHALL be refused naming the place's stage when the place neither stopped short nor waits on its caller. For a live place, the refusal SHALL name that stage as the runner carried it, with the runner's host and when it carried it, and say that a wait Flume has told of since reaches crew with that runner's next carry. `crew answer` SHALL never say that a live place has nothing to answer.

#### Scenario: Nothing to answer
- **WHEN** deneb's runner last carried `a`'s place in code with no question, Flume may since have told the planner the place waits on its caller, and the planner runs `crew answer a "yes"`
- **THEN** it is refused naming `a`'s stage as code when deneb's runner carried it, at the time it carried it, and saying that a wait Flume has told of since reaches crew with that runner's next carry, never that there is nothing to answer, and `requests.rec` gains nothing

#### Scenario: Work that is over
- **WHEN** the runner's record shows `a`'s place landed on its bolt, and `crew answer a "yes"` runs
- **THEN** it is refused naming `a` merged, with nothing to answer

### Requirement: An answer is refused where crew can't tell whether the place waits
`crew answer` SHALL be refused naming what crew could not read when it can't tell whether the place waits.

#### Scenario: A place the runner has not carried
- **WHEN** `a`, naming no `After`, is answered held with the runner's claim, or launched at a place whose status the runner has not carried, and `crew answer a "yes"` runs
- **THEN** it is refused saying crew can't tell whether `a`'s place waits on an answer, with the runner's words or that no status of the place is carried, and never that it is held for its After work

### Requirement: A conflict with no landing fix launches crew's take-main fix
When the runner's report has a started bolt's landing refused by Flume's verdict conflict, and its base place names no landing fix, the first act of crew's that reads it SHALL append a launch of a fix on the bolt named `take-main-<main's revision, seven>`, in its kit's repository and naming no host or stream, its brief saying to take `origin/main` into the bolt with Flume's words of the conflict, unless a fix of that name already stands.

#### Scenario: A landing refused for a conflict
- **WHEN** a raise of the kit's landings card reads the runner carrying `x`'s base place, naming no landing fix, with the verdict conflict against main at `4d3d9be`
- **THEN** `requests.rec` gains one launch of `fix` named `x--take-main-4d3d9be` with Flume's words of the conflict, and `x`'s row says it takes main first

#### Scenario: Read twice
- **WHEN** a later read of the same verdict finds `x--take-main-4d3d9be` standing
- **THEN** no second launch is appended

### Requirement: Flume's landing fix takes main in where the base place names one
Where the base place of a bolt whose landing conflicts with main names a landing fix, Flume's landing fix SHALL take main in and crew SHALL append nothing. The row of a bolt whose landing conflicts with main SHALL say it takes main first.

#### Scenario: Refused with Flume's landing fix
- **WHEN** a raise reads `x`'s base place with the verdict conflict against main at `4d3d9be` and its landing fix `x-1` live
- **THEN** `requests.rec` gains no launch, and `x`'s row says it takes main first, naming `x-1`

### Requirement: A bolt never started lands by its close once main holds its work
`crew bolt land` SHALL land a bolt never started, with no base place and no launch of its work, on the user's word, once its kit's main holds each of its units' changes, open or archived, and each of its chores. It SHALL read them in the checkout the drive's main-level host keeps of its kit, since no runner took any of its work. It SHALL record in its `bolt.land` entry the kit and the commit that main holds. It SHALL merge, submit and post nothing for it, and run no sluice.

#### Scenario: A bolt built outside its branch
- **WHEN** the plan holds the bolt `deploys-go-through-crew`, never started, and each of its units' changes is archived on crew's main
- **THEN** `crew bolt land deploys-go-through-crew` removes it and its units from the plan, the landing's entry names crew and the commit its main holds, and nothing is asked of the runner

### Requirement: A bolt never started is refused its close until main holds its work
`crew bolt land` SHALL be refused for a bolt never started with no units or chores, whose kit the drive's main-level host keeps no checkout of, or while any unit's change is not on main.

#### Scenario: A unit not yet on main
- **WHEN** one unit of such a bolt has no change on its kit's main
- **THEN** `crew bolt land` is refused, naming the unit and its stage

### Requirement: A bolt's landing reads queued, rejected or landing again from the run record
crew SHALL read a bolt's landing from the run record as one of four states, each its own. **Queued** runs from the `bolt.submit` that records a land of the bolt asked until an entry records that land's outcome. **Rejected** holds once the newest land's outcome is recorded refused, for the bolt's own content, a failed check or a conflict, with its head, until a land is asked again. **Landing again** is queued once more after a rejection.

#### Scenario: A wait sluice itself failed on
- **WHEN** Flume's wait on sluice's record of `z`'s submission `#412` fails, and the runner carries the base place with Flume's words that it could not read the submission
- **THEN** `z`'s landing still reads queued as `#412`, and its work is held until a read records `#412`'s outcome

### Requirement: Work into a bolt whose landing is queued is refused
While a bolt's landing is queued or landing again, these SHALL be refused, naming the landing with its request or, once Flume names one, its merge queue entry, with nothing written or launched: `crew unit add` and `crew chore add` into the bolt, `crew unit move` and `crew chore move` into it, and `crew fix <bolt> <name>`. That holds whether they run directly or as a proposal's commands, at the proposal's check and at its approval.

#### Scenario: A unit added while the landing is queued
- **WHEN** the user's send has posted request 57, a land of `z`'s launch, the runner has not decided it, and the user approves the planner's proposal adding unit `b` to `z`
- **THEN** the approval is refused, saying `z`'s landing is asked of the runner as request 57, so unit `b` does not join it until the landing is decided, and to put it on another bolt; `requests.rec` gains nothing

#### Scenario: A fix while the landing is queued
- **WHEN** the runner carries `z`'s base place with its submission `#412` under test, and main-level ops runs `crew fix z logic "Fix tests:logic."`
- **THEN** it is refused naming `#412`, and no fix is launched

### Requirement: A bolt's work goes on unless its own landing is queued
**None** is a bolt never asked to land, landed, or stopped by nothing of the bolt's. Each command a landing queued or landing again refuses SHALL read the state from the run record at the tip its write is applied to. Once a bolt's landing is rejected, or with none, those commands SHALL go on as for any started bolt. `crew fix <bolt> <name> --drop`, the take-main fix crew launches on reading a conflict, and a proposal's card as it is drawn SHALL read no state.

#### Scenario: Another bolt's landing
- **WHEN** `y`'s landing is queued and the user adds a unit to `z`
- **THEN** the unit is added to `z` and launched

### Requirement: The views say a queued landing and leave it out of the bolts that can land
`crew bolts`, text and JSON, the rail's line under land and the board's head line SHALL each say the state in words of their own. A landing queued is said with its request, or with its merge queue entry and its state once Flume names one. A landing again is said so, with the entry Flume's verdict refused before it. The rail SHALL leave a bolt whose landing is queued or landing again out of the bolts that can land.

#### Scenario: Landing again
- **WHEN** the fix has merged into `z`, the user's send has posted a land of `z` again, and the runner carries it as `#415` under test
- **THEN** `crew bolts`, the rail and the board say `z` is landing again as `#415`, after `#412` was refused; a unit added to `z` is refused naming both; and the rail leaves `z` out of the bolts that can land

### Requirement: The views say a rejected landing as refused and the bolt open for work
`crew bolts`, text and JSON, the rail's line under land and the board's head line SHALL each say a landing's rejection. A rejection is said, while the bolt's head is the one refused, as the landing refused and the bolt open for work, in Flume's words.

#### Scenario: A rejection opens the bolt for work
- **WHEN** the runner's report has `#412`'s verdict failed, Flume's words naming `tests:logic`, and the read records it
- **THEN** `crew bolts`, the rail and the board say `z`'s landing `#412` was refused at its head and the bolt is open for work, in Flume's words, and ops's `crew fix z logic "<Flume's words>"` is launched

### Requirement: A bolt with no launch of its own lands under the crew that started it
crew SHALL read a started bolt with no launch of `bolt/<bolt>` in `requests.rec` as one whose branch sluice made before bolts were base places: `crew bolts` SHALL say it lands under the crew that started it, and its row SHALL have no box (rail-cards). No land SHALL be posted for it, and `crew bolt land` SHALL refuse it in those words, recording nothing and reading no landing commit on its kit's main.

#### Scenario: crew bolts says so
- **WHEN** started bolt `y` has its units' launches in `requests.rec` and no launch of `bolt/y`
- **THEN** `crew bolts` says `y` was started before bolts were base places and lands under the crew that started it

#### Scenario: No land is posted
- **WHEN** the raise of `y`'s kit's landings card reads a send that ticked `y`
- **THEN** no land is posted for `y`

#### Scenario: crew bolt land refuses it
- **WHEN** ops runs `crew bolt land y`
- **THEN** it is refused, saying `y` was started before bolts were base places and lands under the crew that started it, no kit is read, and nothing is recorded

### Requirement: A drop of a bolt started before bolts were base places leaves its branch to the user
A drop of a bolt started before bolts were base places SHALL drop its pieces' launches still standing and ask nothing for its branch, which SHALL stay, named in the drop's words, the user's.

#### Scenario: A drop of it
- **WHEN** the user approves dropping `y`, its unit `a`'s launch standing
- **THEN** the drop's commit appends a drop of `a`'s launch and no request for `bolt/y`, and the drop says `bolt/y` stays, the user's to keep or delete

### Requirement: A landing sent back names what failed and the way on
A landing whose verdict Flume gives as failed or conflict SHALL be the bolt's fix until a fix moves its head. crew SHALL name what failed in Flume's words and give the way on. Where the base place names a landing fix within its bound, the way on is Flume's landing fix. Where it names none, it is the take-main fix crew launches for a conflict, or the `crew fix` ops starts for a failed check. Past the bound, it is the fix ops starts. No word SHALL name a team or a conductor.

#### Scenario: A check fails
- **WHEN** the runner carries `z`'s base place, as Flume 0.17.0 gives it, with `#7`'s verdict failed, Flume's words naming `tests:logic`, tested on main at `db8bc25`
- **THEN** `crew bolts` says `z` did not land, that a failed check is the bolt's, in Flume's words, and that ops starts `crew fix z <name> "<Flume's words>"`, naming no team or conductor

#### Scenario: A check fails with Flume's landing fix
- **WHEN** the runner carries `z`'s base place with `#7`'s verdict failed and its landing fix `z-1` for `#7` live
- **THEN** `crew bolts` says `z` did not land, in Flume's words, and that Flume's landing fix `z-1` makes the failed checks pass, naming no command for ops

### Requirement: No land is posted again until a fix moves the head sent back
No land SHALL be posted at the head sent back. Once a fix has moved the head and the bolt reads proven, a land SHALL be posted again only as rail-cards has the send stand.

#### Scenario: Read again at the head sent back
- **WHEN** the send that ticked `z` is read again while `z`'s head is still the one `#7` sent back
- **THEN** no land of `z` is posted, and `z` stays held on its row for its fix

#### Scenario: A conflict read again before its fix merged
- **WHEN** `z`'s landing was sent back for a conflict with main on `README.md`, its take-main fix was launched, crew's or Flume's, and the kit's landings card is raised again before that fix has merged
- **THEN** no land of `z` is posted and no second take-main fix is launched, its row saying it takes main first

#### Scenario: The take-main fix moves the head
- **WHEN** `z`'s take-main fix, crew's or Flume's, has merged and `z` reads proven at its new head
- **THEN** the next raise of its kit's landings card posts one land of `z` on the send that ticked it, asking the user nothing

## REMOVED Requirements

### Requirement: A landing records the commit main holds
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A landed bolt is closed in ops's name and leaves the plan", "A landing's entry names its kit, its head and its time" and "crew bolt land closes a started bolt only once its base place reads landed".

### Requirement: A landing that did not land is the bolt's only for its own content
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A landing refused by Flume's verdict is the bolt's", "Every failed verdict is the bolt's, and any other end is a stop" and "A landing that is the bolt's says what comes next on its head line".

### Requirement: A submission's number is on its bolt's row from the submit
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A piece's line shows its submission's number from the runner's report", "A bolt's head line shows its landing from the runner's report" and "A bolt's row reads nothing from sluice's queue".

### Requirement: A close crew refuses is said on the bolt's row and in the run record until it is lifted
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A refused close is recorded and said on the bolt's head line" and "Each read tries a refused close again and records only new words".

### Requirement: A started bolt's work is launched whole
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A bolt's start is one plan write that reads no host" and "A start marks the bolt Flume's and launches its pieces in order".

### Requirement: A launch carries its repository, priority, intent and recipient
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A launch names its repository, intent, recipient, priority and brief" and "A start or a reorder appends each priority it changed".

### Requirement: A place is answered by a retry
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "An answer retries the stage or the submission its place waits on", "An answer to a place that does not wait is refused naming its stage" and "An answer is refused where crew can't tell whether the place waits".

### Requirement: A landing that conflicts with main takes main in by a fix place
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A conflict with no landing fix launches crew's take-main fix" and "Flume's landing fix takes main in where the base place names one".

### Requirement: A bolt whose work is on main lands by its close alone
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A bolt never started lands by its close once main holds its work" and "A bolt never started is refused its close until main holds its work".

### Requirement: A landing queued holds its bolt's work
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A bolt's landing reads queued, rejected or landing again from the run record", "Work into a bolt whose landing is queued is refused", "A bolt's work goes on unless its own landing is queued", "The views say a queued landing and leave it out of the bolts that can land" and "The views say a rejected landing as refused and the bolt open for work".

### Requirement: A bolt started before bolts were base places lands under the crew that started it
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A bolt with no launch of its own lands under the crew that started it" and "A drop of a bolt started before bolts were base places leaves its branch to the user".

### Requirement: A landing Flume's verdict sent back is the bolt's fix
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A landing sent back names what failed and the way on" and "No land is posted again until a fix moves the head sent back".
