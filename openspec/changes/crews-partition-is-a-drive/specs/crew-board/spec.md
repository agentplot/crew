## MODIFIED Requirements

### Requirement: Operation shows each environment's deploys and the operations waiting
After the bolts landed in the last seven days, the Operation lane SHALL show each environment's deploys that moved in those seven days or are still open, newest first, each on one line with the commit and the one it comes from, where it stands, whose word it was deployed on and the bolts it carried, or the commit the record can't place when no landing in it left main there; then each operation on that environment whose latest state is waiting, handed or failed. A deploy waiting on the user's word and an operation waiting on the user SHALL carry their rail row's marker. All of it SHALL be read from the run record's `ops.*` entries of the main level's host and its landings, and `crew board --json` SHALL give it as each drive's `environments`.

#### Scenario: A deploy done and a newer one offered
- **WHEN** wldn-ops approved the deploy of mac-studio to a landing's commit, the deployer recorded it done, and a deploy of the next landing's commit is offered
- **THEN** Operation shows the offer first, with ✓, waiting on the user's word and carrying the newer landing's bolt, then the deploy, done, approved by wldn-ops and carrying its bolt

#### Scenario: A deploy whose commit no landing left main at
- **WHEN** a deploy of mac-studio is recorded to a commit no landing in the record left main at
- **THEN** its line says that commit is no landing's commit in the record, and names no bolt

#### Scenario: Operations waiting
- **WHEN** a step after a deploy is handed to the dispatcher and a step on its own waits on the user
- **THEN** Operation shows the first handed to the dispatcher and the second with ✓ and its card, and not a step marked done

### Requirement: The board prints four lanes in order
`crew board [--label L]` SHALL print, for each drive read (the one named, else the caller's, else every drive), a header naming the drive, the time it was read and the hosts that answered, then four lanes in this order: Inception, Bolt plan, Construction, Operation, then the attention line. Each object SHALL be one line. A lane with nothing in it SHALL say none.

#### Scenario: Nothing in flight
- **WHEN** `crew board --label wldn` runs on a drive whose plan holds no bolt, no queued unit and no open proposal
- **THEN** it prints wldn's header and the four lanes in order, each saying none

#### Scenario: Every drive
- **WHEN** `crew board` runs with no label outside any agent
- **THEN** it prints one board per drive in the teams file, one after another

### Requirement: Inception shows the signals no move has taken and the explorations
The Inception lane SHALL list every signal, on the drive's branch or on main of the drive's first blueprints repo, that has no move in `moves.rec`, grouped by who captured it, each group with how many it holds and how old its oldest is, each signal with its kind and its first words. It SHALL then list each exploration folder on main of each kit the drive's teams build, with the first line of its first file.

#### Scenario: A moved signal leaves
- **WHEN** a signal captured by wldn-planner is routed to a unit
- **THEN** the next board no longer lists it, and wldn-planner's group counts one fewer

#### Scenario: An exploration
- **WHEN** the kit's main holds `openspec/explorations/command-cost/reading.md` whose first line says it is a reading
- **THEN** Inception lists `command-cost` with that line

### Requirement: Operation shows the bolts landed in the last seven days
The Operation lane SHALL list each bolt landed in the last seven days, newest first, from the `bolt.land` entries of the drive's run record that were not refused, with when it landed, who landed it and its units.

#### Scenario: A landing
- **WHEN** wldn-ops landed bolt apex-zones two days ago
- **THEN** Operation lists apex-zones with that time, wldn-ops and zone-one

#### Scenario: Past the window
- **WHEN** a bolt landed eight days ago
- **THEN** Operation does not list it

### Requirement: Each rail row is a marker on its object
Every row `crew rail` would list for the drive SHALL appear on the board as a marker on the line of its object, and never as a line of its own: ✓ on a proposal's line for an open proposal, ✓ on a unit's line for a unit in review, ✎ on a unit's line for a verify report the user has not answered, and ✓ on a ledger's head line for a bolt waiting to land. Each marker SHALL say whether that row's card is open and who asked it, and, when none is open and the last post under the row's key was refused, that the row owes its card because Pending You refused its post.

#### Scenario: A unit in review
- **WHEN** unit a is in review and swb-1-conductor has a card open under its key
- **THEN** a's line in its ledger carries ✓ and says the card is open, asked by swb-1-conductor, and no other line names a's review

#### Scenario: A bolt to land
- **WHEN** every unit of tenant-environments has merged and none has landed
- **THEN** its ledger's head line carries ✓ and says whether a card is open for it

#### Scenario: A row whose card post was refused
- **WHEN** a deploy of deneb waits on the user's word, no card is open under `deploy/deneb`, and the last post under that key was refused
- **THEN** its line in Operation carries ✓ and says it has no card open, its post refused, and the JSON's marker carries the refusal's words

### Requirement: The board answers nothing
The board SHALL print no command that answers or moves anything, and SHALL write nothing: no commit, no run-record entry, no file in a kit or a blueprints repo.

#### Scenario: Read only
- **WHEN** `crew board` runs on a drive with a proposal open, a unit in review and a bolt to land
- **THEN** its output holds no `crew plan approve`, `crew unit approve` or `crew tell`, the drive's branch has the same tip, and the run record has no new entry

### Requirement: The attention line names what is wrong
The board SHALL end with an attention line, each item marked !, naming each host that did not answer for its kits, never for its run record, which is read from the drive's branch; each plan or signals home it could not read, with why, the branch among them when its run record could not be read; and each bolt a team holds whose every unit has landed but which is still in the plan. A ledger whose bolt is in that state SHALL also carry ! on its head line. With nothing to name, the attention line SHALL say none.

#### Scenario: A host down
- **WHEN** the box holding swb-1 does not answer
- **THEN** the attention line names the box and why, and swb-1's ledger shows its units from the plan with their stages unknown

#### Scenario: An operator host asleep
- **WHEN** macbook-pro, which holds a wldn operator session and runs no team, does not answer
- **THEN** the attention line does not name macbook-pro, and the landings, batches and cards read from `wldn/main` are drawn whole

#### Scenario: Landed but still in the plan
- **WHEN** every unit of a held bolt has landed on main and `crew bolt land` has not run
- **THEN** its ledger's head carries ! and the attention line names the bolt as landed and still in the plan

### Requirement: The board prints its lanes as JSON
`crew board --json` SHALL print the same board as JSON: for each drive, its lanes as lists of objects, each object with its drive, its team where it has one, and its markers, each marker with its rail group, its card key, when its row began to wait, its card, and, when no card is open, the words of Pending You's refusal of the last post under its key, or none, and the attention items; and the hosts that did not answer and the plans not read.

#### Scenario: The page's input
- **WHEN** `crew board --label wldn --json` runs while unit a is in review
- **THEN** the JSON's Construction lane holds tenant-environments with team swb-1, and unit a with a marker of group review and its card key

### Requirement: The rail and the board come from one read
When the host's follower refreshes, crew SHALL read the plan, the kits and the run record once for both the rail and the board, and once for every drive with an operator session on the host, each kit read once however many of those drives it serves: it SHALL write each drive's rail, what `crew rail` prints, as that drive's rail frame, and its board's data as its board frame; the rail tab SHALL draw the rail's frame and the board tab SHALL draw the board from that same read at its own width. When the follower has not refreshed a frame for more than three of its periods, its tab SHALL say how old it is; when none was ever written, the tab SHALL say so and that the host's follower writes it.

#### Scenario: One refresh
- **WHEN** the host's follower refreshes for a drive with three units in flight on one host
- **THEN** that host's kits are read once and the state branch fetched once for both frames

#### Scenario: Two drives on one host
- **WHEN** the host's follower on mac-studio, which holds operator sessions of wldn and swancloud, makes its first refresh, and both drives' teams build kits on the box
- **THEN** the box's kits are gathered once for both drives, and wldn's and swancloud's rail frames, board frames and agents' views are each written from that one read

#### Scenario: The loop has stopped
- **WHEN** the host's follower has not run for five minutes
- **THEN** the board tab still shows its last board, and the rail tab its last rail, each headed with how long ago it was read

#### Scenario: Never written
- **WHEN** the board tab opens on a host where no follower has written wldn's frame
- **THEN** it says there is no board for wldn yet and that the host's follower writes it

### Requirement: The host's follower runs with no tab
`crew _follow` SHALL be the host's follower with no tab, the command a job of the host's runs: once a minute on its clock, and whenever this host's cache of a drive's state branch moves, for every drive with an operator session on the host, it SHALL make the refresh the rail tab's loop makes. crew SHALL run no service of its own for it.

#### Scenario: The host's job follows
- **WHEN** swancloud's job runs `crew _follow` on mac-studio, which holds operator sessions of wldn and swancloud, and no console tab is open
- **THEN** both drives' board frames, rail frames and agents' views are written each period, the card sessions of closed cards are ended, and due restarts are handed out

### Requirement: A refresh after nothing moved reads nothing
Before it reads, the host's follower SHALL check whether anything the refresh acts on has moved since its last read: each drive's state branch, its runners' branches and blueprints main as this host's caches hold them; each kit's refs, worktrees, places' changes and slots files, on every host it reads; each of those hosts' card readings folder, where a reading the user sent back lands; the cards as Pending You last answered for them; crew's checkout; and the teams file. It SHALL stamp this host's kits and readings in its own process at each refresh, starting nothing, and SHALL ask another host for its kits' and readings' stamps only when something there could have moved: when the branch of a drive with work on that host moved, when that host's runner's branch moved, when the host did not answer the last time it was asked, and otherwise once in ten minutes; a host not asked SHALL count as unmoved. When nothing has moved, the follower SHALL start no read and no process, and at a tick of its clock none beyond its fetches, and SHALL write each drive's rail frame, board frame and agents' views again from its last read, as of the check.

#### Scenario: An idle host
- **WHEN** the host's follower on mac-studio ticks, every card it acts on answered at an earlier ask, and nothing it read has moved since its last refresh
- **THEN** it fetches each repository once and starts no other process: no git besides, no gather, no ssh, no sluice, no Pending You bridge, no herdr and no portless; it asks the box nothing, and writes wldn's frames again from its last read, each saying the time of this refresh

#### Scenario: The box asked when something there could have moved
- **WHEN** the box runs wldn's runner and holds a kit of wldn's, and the box's runner reports, or wldn's branch moves
- **THEN** the follower's next refresh asks the box for its kits' and readings' stamps in one ssh, and the refresh after it, with nothing moved since, asks the box nothing

#### Scenario: A drive with nothing on the box moves
- **WHEN** swancloud's branch moves, and no kit, runner or card session of swancloud's is on the box
- **THEN** the follower's next refresh asks the box nothing

#### Scenario: Ten minutes with nothing moved
- **WHEN** nothing has said the box could have moved for ten minutes
- **THEN** the follower's next refresh asks the box once, and a tick that does asks its dev servers in the same ssh

#### Scenario: What it can't check
- **WHEN** the follower cannot read whether a kit on the box has moved, because the box does not answer
- **THEN** it does not take the kit as unmoved: it reads again what rests on the box, names the box as it does today, and asks the box again at its next refresh

#### Scenario: A runner's report
- **WHEN** the box's runner pushes a report of the places it runs to its branch, and wldn's own branch does not move
- **THEN** the follower's next refresh after its clock's fetch brings it reads wldn again at its tips, and gathers no kit whose stamp did not move

#### Scenario: A reading sent back
- **WHEN** the user sends back a batch's reading on mac-studio, and plannotator writes its result into the card's readings folder there, with nothing else moved
- **THEN** the follower's next refresh, within a few seconds, takes mac-studio's readings as moved and sweeps its card sessions there, which is where the reading's owner is told, and gathers no kit and reads no state branch

#### Scenario: sluice's folder moves
- **WHEN** sluice writes its records and logs in switchboard-kit's git folder on the box, and the box's runner has not reported since
- **THEN** the follower takes the kit as unmoved, having read nothing of that folder

#### Scenario: A task ticked with nothing committed
- **WHEN** a coder on mac-studio ticks a task in its place's tasks.md and commits nothing
- **THEN** the follower's next refresh on its clock takes the kit as moved and gathers it again

### Requirement: A refresh after a change reads only what moved
When something has moved, the host's follower SHALL read again only what rests on what moved: a moved state tip, that drive's plan, proposals and run record at the new tip; a moved blueprints tip, its signals; a moved kit, that kit alone, on its host; a moved runner's branch, that drive's runners' records at the new tip, each piece's stage and submission among them, and no kit gathered whose stamp did not move; a moved readings folder, that host's card sessions swept and nothing read; cards whose answers moved, the card sweep run and nothing read. What did not move SHALL be taken from the follower's last read, which crew SHALL never read as a fact once what it was read at has moved, and keep in the follower's process alone, writing none of it.

#### Scenario: The plan moved and no kit did
- **WHEN** the user approves a proposal on mac-studio, moving wldn's state branch there, and no kit has moved
- **THEN** the follower's refresh fetches nothing, reads wldn's plan and run record once at the new tip, and gathers no kit

#### Scenario: One kit moved
- **WHEN** a coder commits in a place of switchboard-kit on the box, and nothing else has moved
- **THEN** the follower's next refresh gathers switchboard-kit on the box alone, and reads no state branch again

#### Scenario: A submission moved
- **WHEN** the box's runner reports unit `a`'s place with its submission `#41` under test, and nothing else has moved
- **THEN** the follower's refresh after its clock's fetch brings the report shows `submitted #41` on `a`'s line, gathers no kit and starts no sluice

### Requirement: The follower fetches on a one-minute clock
The host's follower SHALL fetch once a minute on its own clock, never faster, each repository it reads once, carrying every branch it reads of that repository in the one fetch: each drive's state branch with its runners' branches, and its blueprints main. It SHALL never fetch because an entry arrived. A branch a repository does not have yet SHALL cost that repository's fetch no more than one fetch again without it. Between its clock's ticks it SHALL look at this host's caches with no process, refreshing within a few seconds when a write on this host moves one; it SHALL start no `crew events --follow` to wake on.

#### Scenario: An entry from another host
- **WHEN** a place's runner on the box reports, or an agent on the box writes an entry, and wldn's branch gains it
- **THEN** mac-studio's follower shows it at its clock's next fetch, within a minute, and fetched nothing in between

#### Scenario: Two drives in one state repository
- **WHEN** the follower follows madswan and swancloud, whose branches are both in afterthought/crew-state
- **THEN** each tick fetches afterthought/crew-state once, both drives' branches and their runners' in that one fetch

#### Scenario: An entry written on this host
- **WHEN** the user approves a unit from the rail tab's shell on mac-studio
- **THEN** the follower refreshes within a few seconds, without fetching

### Requirement: What no stamp sees is read on the follower's clock
At a tick of its clock that asks a host (the requirement *A refresh after nothing moved reads nothing* says when), the host's follower SHALL read again that host's dev servers as portless lists them, and at a tick that asks Pending You (the requirement *The follower asks Pending You about cards on its clock*), herdr's listing of each card's asker its card sweep acts on; it SHALL take a change in either as moved, drawing the frames again and sweeping the cards with it, with nothing gathered. At every refresh, whether or not anything moved, it SHALL work out from the run record's times and the time now whether a batch is due by hours, and tell the drive's planner once when one is.

#### Scenario: A dev server started by hand
- **WHEN** a dev server is started by hand on the box, and nothing else moves
- **THEN** the board shows it after the follower's next tick that asks the box, within ten minutes, and no kit is gathered

#### Scenario: An asker's agent gone
- **WHEN** the agent that asked a question on a card leaves its pane, and nothing else moves
- **THEN** at the follower's next ask, within ten minutes, herdr's listing shows the pane empty, and the card sweep withdraws the question, naming the asker

#### Scenario: A batch made due by the hours
- **WHEN** wldn's last batch was delivered as many hours ago as its setting, one change is due, and nothing moves
- **THEN** the follower's next refresh tells wldn's planner the batch is due, reading nothing to find it, and the refresh after reads the entry and tells nothing again

### Requirement: The planner's and ops's bands show what places wait on them for
`board.agent_views` SHALL give the planner's band each launched place that stopped short asking or waits on its caller, past its kind's bound among them whatever stage it last delivered, with its question or Flume's words and the stage it waits to retry or its submission. It SHALL give main-level ops's band each fix of main and each take-main fix in flight with its stage. crew's mod SHALL draw both above the agent's prompt.

#### Scenario: A question in the planner's band
- **WHEN** `a`'s construct stopped short asking "Which drive's rail?"
- **THEN** madswan-planner's view lists `a` with that question, and the mod draws it

#### Scenario: A place past its bound in the planner's band
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place waiting on its caller to retry code past its bound, its verify delivered
- **THEN** madswan-planner's view counts one place waiting on an answer and lists `a` waiting on its caller at code with Flume's words, and the mod draws it

#### Scenario: A fix of main in ops's band
- **WHEN** `main--a-test-reads-its-fixture` is in code
- **THEN** madswan-ops's view lists it at code, and the mod draws it

### Requirement: A role that runs as its kind has its view
Each role its drive runs as its kind SHALL have a view among the agents' views under its run's name, `<label>-<role>`, drawn above its run's prompt by crew's mod where crew's plugin loads: what its turn took, and how many asks wait for the role and since when.

#### Scenario: A run with an ask waiting
- **WHEN** madswan's planner run took two asks and a third has waited four minutes
- **THEN** madswan-planner's view shows the two it took and one waiting for four minutes

#### Scenario: Nothing waiting
- **WHEN** madswan's planner run took one ask and nothing else waits
- **THEN** madswan-planner's view shows the one it took and says nothing waits

### Requirement: The follower runs no sluice
The host's follower SHALL start no sluice process: no `sluice overview --watch`, no `sluice overview` at its clock's tick, and no `sluice status`. It SHALL keep no submission of its own. It SHALL learn that a piece's submission moved from the drive's runner's branch, which it looks at with no process and fetches on its clock. crew SHALL read and name no folder of sluice's.

#### Scenario: A merge moves in sluice's queue
- **WHEN** a unit's merge into a bolt of switchboard-kit on the box is queued in sluice, and the box's runner has not reported since
- **THEN** the follower's next refresh shows no change on the unit's line, and starts no sluice

#### Scenario: The runner reports the merge
- **WHEN** the box's runner then reports the unit's place submitted as `#41`
- **THEN** the follower's refresh after its clock's next fetch shows `submitted #41` on the unit's line, gathering no kit whose stamp did not move

#### Scenario: A follower's life
- **WHEN** the follower on mac-studio reads two drives whose bolts are in switchboard-kit on the box, through a read, ticks with nothing moved, a runner's report and a gather of the kit
- **THEN** it starts no `sluice` process on either host and opens no ssh for a sluice command
