## ADDED Requirements

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
The first crew act on any host to read a bolt whose landing's outcome is decided SHALL record it: the raise of its kit's landings card, `crew bolts`' plan write, `crew bolt land`, or any plan write that reads the bolt (`plan.21`). It SHALL write one `bolt.submit` entry with the outcome, the head, the merge queue's entry as `Submission` where Flume names one, and the words of a refusal or a stop. It SHALL record nothing while the landing is asked, submitted or unknown.

#### Scenario: Nobody runs anything
- **WHEN** a land of `z` is posted, no agent of the partition runs a command, and the runner's branch then carries `z`'s base place landed at `5d1a9e0`
- **THEN** the next raise of `z`'s kit's landings card records `z`'s `bolt.submit` landed and its `bolt.land` at `5d1a9e0`, and closes `z`

#### Scenario: Two reads at once
- **WHEN** two reads of `z` find its base place landed, and the second's write is applied to a tip that holds the first's
- **THEN** the run record holds one `bolt.submit` outcome and one `bolt.land` for `z`

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
Where the runner answered a bolt's drop refused, as Flume refuses it while a place on the bolt's branch is live, the next plan write that finds the bolt gone from the plan, its launch standing and no piece of it live SHALL ask the drop again, once for each refusal (`runner.base_drop_due`).

#### Scenario: A refused drop asked again
- **WHEN** the runner answered `x`'s drop refused while `a`'s place was live, and a later plan write finds `x` gone from the plan, its launch standing and no place of its pieces live
- **THEN** that write appends one drop of `x`'s launch, and a write after it, while that drop is unanswered, appends none

#### Scenario: Not while a piece is live
- **WHEN** the runner answered `x`'s drop refused and `a`'s place is still live
- **THEN** no plan write asks the drop again

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
A landing whose verdict Flume gives as failed or conflict SHALL be the bolt's fix until a fix moves its head. crew SHALL name what failed in Flume's words and give the way on: the take-main fix crew launches for a conflict, or the `crew fix` ops starts for a failed check. No land SHALL be posted at the head sent back. Once a fix has moved the head and the bolt reads proven, a land SHALL be posted again only as rail-cards has the send stand. No word SHALL name a team or a conductor.

#### Scenario: A check fails
- **WHEN** the runner carries `z`'s base place with `#7`'s verdict failed, Flume's words naming `tests:logic`, tested on main at `db8bc25`
- **THEN** `crew bolts` says `z` did not land, that a failed check is the bolt's, in Flume's words, and that ops starts `crew fix z <name> "<Flume's words>"`, naming no team or conductor

#### Scenario: Read again at the head sent back
- **WHEN** the send that ticked `z` is read again while `z`'s head is still the one `#7` sent back
- **THEN** no land of `z` is posted, and `z` stays held on its row for its fix

#### Scenario: A conflict read again before its fix merged
- **WHEN** `z`'s landing was sent back for a conflict with main on `README.md`, crew launched its take-main fix, and the kit's landings card is raised again before that fix has merged
- **THEN** no land of `z` is posted and no second take-main fix is launched, its row saying it takes main first

#### Scenario: The take-main fix moves the head
- **WHEN** `z`'s take-main fix has merged and `z` reads proven at its new head
- **THEN** the next raise of its kit's landings card posts one land of `z` on the send that ticked it, asking the user nothing

## MODIFIED Requirements

### Requirement: A landing records the commit main holds
The act that reads a started bolt's base place landed ("A landing is recorded by the first act that reads it in the runner's report") SHALL close the bolt in main-level ops's name by one `bolt.land` entry. The entry SHALL name the kit the bolt landed on and, as its `Head`, the commit Flume's status names the base place landed at, as the runner carries it. Its `Age` and `Split` SHALL be those the bolt's time gives from the run record, none read from sluice (`plan.20`). The close SHALL take the bolt and its work out of the plan and close its kit's landings card naming that commit and the fleet's timer. It SHALL delete no branch and remove no worktree. `crew bolt land` on a started bolt SHALL close it the same way, and SHALL be refused, recording nothing, while its base place does not read landed with its commit, naming its landing as the runner's report has it.

#### Scenario: The landing's commit
- **WHEN** the runner carries the base place of switchboard-kit's bolt `y` over, landed at `9c1e4b7`, and the raise of switchboard-kit's landings card reads `y`
- **THEN** the run record holds a `bolt.land` on `bolt/y` in ops's name naming switchboard-kit and `9c1e4b7` as its head, `y` and its work are gone from the plan, and no branch is deleted and no worktree removed

#### Scenario: Its time from the run record
- **WHEN** `y`'s close is recorded
- **THEN** its `Age` and `Split` are those its row shows from the run record, and no sluice history is read

#### Scenario: Closed by hand before it landed
- **WHEN** `crew bolt land y` runs while the runner carries `y`'s base place with its submission `#412` under test
- **THEN** it is refused, saying `y`'s landing is `#412` under test, and nothing is recorded

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

### Requirement: A landing that conflicts with main takes main in by a fix place
When the runner's report has a started bolt's landing refused by Flume's verdict conflict, the first act of crew's that reads it SHALL append a launch of a fix on the bolt named `take-main-<main's revision, seven>`, in its kit's repository and naming no host or stream, its brief saying to take `origin/main` into the bolt with Flume's words of the conflict, unless a fix of that name already stands. The bolt's row SHALL say it takes main first.

#### Scenario: A landing refused for a conflict
- **WHEN** a raise of the kit's landings card reads the runner carrying `x`'s base place with the verdict conflict against main at `4d3d9be`
- **THEN** `requests.rec` gains one launch of `fix` named `x--take-main-4d3d9be` with Flume's words of the conflict, and `x`'s row says it takes main first

#### Scenario: Read twice
- **WHEN** a later read of the same verdict finds `x--take-main-4d3d9be` standing
- **THEN** no second launch is appended

### Requirement: A bolt whose work is on main lands by its close alone
`crew bolt land` SHALL land a bolt never started, with no base place and no launch of its work, on the user's word, once its kit's main holds each of its units' changes, open or archived, and each of its chores. It SHALL read them in the checkout the partition's main-level host keeps of its kit, since no runner took any of its work. It SHALL record in its `bolt.land` entry the kit and the commit that main holds. It SHALL merge, submit and post nothing for it, and run no sluice. It SHALL be refused for such a bolt with no units or chores, whose kit that host keeps no checkout of, or while any unit's change is not on main.

#### Scenario: A bolt built outside its branch
- **WHEN** the plan holds the bolt `deploys-go-through-crew`, never started, and each of its units' changes is archived on crew's main
- **THEN** `crew bolt land deploys-go-through-crew` removes it and its units from the plan, the landing's entry names crew and the commit its main holds, and nothing is asked of the runner

#### Scenario: A unit not yet on main
- **WHEN** one unit of such a bolt has no change on its kit's main
- **THEN** `crew bolt land` is refused, naming the unit and its stage

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

## REMOVED Requirements

### Requirement: crew removes only its own worktrees
**Reason**: crew makes no landing worktree and deletes no bolt branch, so it has no worktree or branch of its own to remove (record 0056; departs from `plan.9`).
**Migration**: "crew removes no worktree, and names a landing's left from before" holds the tidy, which names a landing's or legacy bolt's worktree it finds with the commands the user runs to remove it.

### Requirement: A landing is read from GitHub's main
**Reason**: crew submits nothing and reads no landing from main or from sluice's exit; the runner carries the landing out with Flume and sluice (record 0056).
**Migration**: "A landing's outcome is read from the runner's report" reads a landing's outcome, and its landed commit, from Flume's status of the bolt's base place as the runner carries it.

### Requirement: The next landing on the user's word readies the pull request
**Reason**: crew runs no `gh` for a bolt and readies no pull request; Flume submits the base place's branch through sluice, which holds any pull request a kit's policy asks for (record 0056).
**Migration**: "No crew command runs sluice, wt or gh for a bolt, or moves a checkout".

### Requirement: A kit that takes no pull requests is asked nothing of GitHub
**Reason**: crew reads and marks no pull request for any kit's bolt, whatever its policy says of pull requests (record 0056).
**Migration**: "No crew command runs sluice, wt or gh for a bolt, or moves a checkout".

### Requirement: A landing submits the bolt where it lives
**Reason**: crew cuts no landing worktree, fetches or levels no copy of a bolt's branch and submits nothing; Flume submits the base place's branch as sluice holds it (record 0056; departs from `plan.19`).
**Migration**: "A bolt lands on the user's send alone, carried to the runner as a land".

### Requirement: A landing stopped by sluice or its host is recorded stopped
**Reason**: a stop is the runner's refusal of the land or Flume's verdict withdrawn or refused, read from the runner's report, and it spends the send rather than awaiting ops's submission again (record 0056).
**Migration**: "A landing stopped by nothing of the bolt's is recorded stopped, and its send is spent".

### Requirement: A landing standing in sluice is waited on again, not submitted again
**Reason**: crew submits and waits on nothing; a land standing undecided is not posted again (record 0056).
**Migration**: rail-cards has the raise of a kit's landings card post no land for a row whose land stands undecided; "A landing's outcome is read from the runner's report" reads it.

### Requirement: A landing's submission is recorded when sluice queues it
**Reason**: crew makes no submission; it records the land it posts on the user's send by its request, and the merge queue's entry only as Flume's status names it (record 0056).
**Migration**: run-record holds the land's `bolt.submit` entry, asked, with its request; "A landing is recorded by the first act that reads it in the runner's report" records the outcome with the entry Flume names.

### Requirement: A landing's waiter waits from the background a call at a time
**Reason**: crew leaves no waiter running and calls no `sluice wait`; the runner's report carries a landing's end, and the first act that reads the bolt records it (record 0056).
**Migration**: "A landing is recorded by the first act that reads it in the runner's report"; "A landing queued holds its bolt's work" holds the bolt's work while its land is undecided.

### Requirement: A bolt is a branch, and crew's one worktree is a landing's
**Reason**: a bolt is a Flume base place whose branch sluice makes and ends, and crew makes no worktree at all (record 0056; departs from `plan.18`).
**Migration**: "A bolt is a base place of crew's kind"; "crew removes no worktree, and names a landing's left from before" leaves a place of Flume's alone.

### Requirement: Main-level ops lands bolts on the user's word
**Reason**: no role runs a landing; the user's send of a bolt's row is one land, which crew posts and the runner carries out (record 0056; `plan.16` as it amends it).
**Migration**: "A bolt lands on the user's send alone, carried to the runner as a land" and "crew bolt submit lands nothing"; main-level holds what of a landing stays ops's.

### Requirement: A landed bolt's branch goes only once main holds its work
**Reason**: crew deletes and marks no bolt branch; Flume tidies the base place and sluice ends its branch, keeping and naming one that holds work main lacks (record 0056; departs from `plan.19`).
**Migration**: "A bolt is a base place of crew's kind"; "A bolt's drop drops its base place last".

### Requirement: A landing that does not land leaves its pull request a draft
**Reason**: crew runs no `gh` for a bolt and drafts no pull request (record 0056).
**Migration**: "No crew command runs sluice, wt or gh for a bolt, or moves a checkout".

### Requirement: A landing is recorded by the first act that reads the bolt after it
**Reason**: its reads were of sluice's record on the kit's host, by the landing's waiter and `crew bolt submit`'s end, none of which crew has; the outcome is read from the runner's report (record 0056).
**Migration**: "A landing is recorded by the first act that reads it in the runner's report" and "A landing's record rests on the state repository alone".

### Requirement: A bolt carrying another bolt's work does not land
**Reason**: it was a refusal of `crew bolt submit`, which lands nothing; the hold is on the land crew posts (record 0056).
**Migration**: "A bolt carrying another bolt's work is asked no land".

### Requirement: A landing sluice sent back is the bolt's fix
**Reason**: its cases were of `crew bolt submit` run again at a head sluice sent back; crew posts no land at such a head, reading Flume's verdict from the runner's report (record 0056).
**Migration**: "A landing Flume's verdict sent back is the bolt's fix".
