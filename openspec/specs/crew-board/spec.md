# crew-board Specification

## Purpose
The board of a partition's flow: four lanes, Inception, Bolt plan, Construction and Operation, each object on one line with the rail's decisions as markers on it, read from crew's state and writing nothing, as text in the terminal and as JSON for the page; and each crew agent's view of it.

## Requirements

### Requirement: Operation shows each environment's deploys and the operations waiting
After the bolts landed in the last seven days, the Operation lane SHALL show each environment's deploys that moved in those seven days or are still open, newest first, each on one line with the commit and the one it comes from, where it stands, whose word it was deployed on and the bolts it carried, or the commit the record can't place when no landing in it left main there; then each operation on that environment whose latest state is waiting, handed or failed. A deploy waiting on the user's word and an operation waiting on the user SHALL carry their rail row's marker. All of it SHALL be read from the run record's `ops.*` entries of the main level's host and its landings, and `crew board --json` SHALL give it as each partition's `environments`.

#### Scenario: A deploy done and a newer one offered
- **WHEN** wldn-ops approved the deploy of mac-studio to a landing's commit, the deployer recorded it done, and a deploy of the next landing's commit is offered
- **THEN** Operation shows the offer first, with ✓, waiting on the user's word and carrying the newer landing's bolt, then the deploy, done, approved by wldn-ops and carrying its bolt

#### Scenario: A deploy whose commit no landing left main at
- **WHEN** a deploy of mac-studio is recorded to a commit no landing in the record left main at
- **THEN** its line says that commit is no landing's commit in the record, and names no bolt

#### Scenario: Operations waiting
- **WHEN** a step after a deploy is handed to the dispatcher and a step on its own waits on the user
- **THEN** Operation shows the first handed to the dispatcher and the second with ✓ and its card, and not a step marked done

### Requirement: Main-level ops's view shows the operations
Main-level ops (`<label>-ops`) SHALL have a view among the agents' views, drawn above its prompt by crew's mod: a head counting the deploys waiting on the user's word, those running and the operations waiting, then, environment by environment, each deploy waiting on the word with its card, each approved and not yet deployed, each running, and each operation step waiting, handed or failed with the deploy it comes after and its doer.

#### Scenario: A deploy offered and a step handed
- **WHEN** a deploy of mac-studio waits on the user's word with wldn-ops's card open, and a step after the last deploy is handed to the dispatcher
- **THEN** wldn-ops's view counts one deploy waiting on the word and one operation, and shows the deploy with ✓ and its card, and the step as handed with the dispatcher as its doer

#### Scenario: A deploy whose card was refused
- **WHEN** a deploy of deneb waits on the user's word and Pending You refused the last post of its card
- **THEN** swancloud-ops's view shows the deploy with ✓ and says it has no card open, its post refused

### Requirement: The board prints four lanes in order
`crew board [--label L]` SHALL print, for each partition read (the one named, else the caller's, else every partition), a header naming the partition, the time it was read and the hosts that answered, then four lanes in this order: Inception, Bolt plan, Construction, Operation, then the attention line. Each object SHALL be one line. A lane with nothing in it SHALL say none.

#### Scenario: Nothing in flight
- **WHEN** `crew board --label wldn` runs on a partition whose plan holds no bolt, no queued unit and no open proposal
- **THEN** it prints wldn's header and the four lanes in order, each saying none

#### Scenario: Every partition
- **WHEN** `crew board` runs with no label outside any agent
- **THEN** it prints one board per partition in the teams file, one after another

### Requirement: Inception shows the signals no move has taken and the explorations
The Inception lane SHALL list every signal, on the drive's branch or on main of the partition's first blueprints repo, that has no move in `moves.rec`, grouped by who captured it, each group with how many it holds and how old its oldest is, each signal with its kind and its first words. It SHALL then list each exploration folder on main of each kit the partition's teams build, with the first line of its first file.

#### Scenario: A moved signal leaves
- **WHEN** a signal captured by wldn-planner is routed to a unit
- **THEN** the next board no longer lists it, and wldn-planner's group counts one fewer

#### Scenario: An exploration
- **WHEN** the kit's main holds `openspec/explorations/command-cost/reading.md` whose first line says it is a reading
- **THEN** Inception lists `command-cost` with that line

### Requirement: Bolt plan shows the proposals, the planned bolts and the queue
The Bolt plan lane SHALL list each open proposal with its number, who proposed it and the first line of its case; each bolt no team holds, with its repository, its goal and its units with their stages; and the queue, by repository, each unit with its sources.

#### Scenario: A planned bolt
- **WHEN** the plan holds bolt apex-zones with no team and unit zone-one in it
- **THEN** Bolt plan lists apex-zones with its repository and goal, and zone-one under it as ready

### Requirement: Operation shows the bolts landed in the last seven days
The Operation lane SHALL list each bolt landed in the last seven days, newest first, from the `bolt.land` entries of the partition's run record that were not refused, with when it landed, who landed it and its units.

#### Scenario: A landing
- **WHEN** wldn-ops landed bolt apex-zones two days ago
- **THEN** Operation lists apex-zones with that time, wldn-ops and zone-one

#### Scenario: Past the window
- **WHEN** a bolt landed eight days ago
- **THEN** Operation does not list it

### Requirement: Each rail row is a marker on its object
Every row `crew rail` would list for the partition SHALL appear on the board as a marker on the line of its object, and never as a line of its own: ✓ on a proposal's line for an open proposal, ✓ on a unit's line for a unit in review, ✎ on a unit's line for a verify report the user has not answered, and ✓ on a ledger's head line for a bolt waiting to land. Each marker SHALL say whether that row's card is open and who asked it, and, when none is open and the last post under the row's key was refused, that the row owes its card because Pending You refused its post.

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
- **WHEN** `crew board` runs on a partition with a proposal open, a unit in review and a bolt to land
- **THEN** its output holds no `crew plan approve`, `crew unit approve` or `crew tell`, the drive's branch has the same tip, and the run record has no new entry

### Requirement: The attention line names what is wrong
The board SHALL end with an attention line, each item marked !, naming each host that did not answer for its kits, never for its run record, which is read from the partition's branch; each plan or signals home it could not read, with why, the branch among them when its run record could not be read; and each bolt a team holds whose every unit has landed but which is still in the plan. A ledger whose bolt is in that state SHALL also carry ! on its head line. With nothing to name, the attention line SHALL say none.

#### Scenario: A host down
- **WHEN** the box holding swb-1 does not answer
- **THEN** the attention line names the box and why, and swb-1's ledger shows its units from the plan with their stages unknown

#### Scenario: An operator host asleep
- **WHEN** macbook-pro, which holds a wldn operator session and runs no team, does not answer
- **THEN** the attention line does not name macbook-pro, and the landings, batches and cards read from `wldn/main` are drawn whole

#### Scenario: Landed but still in the plan
- **WHEN** every unit of a held bolt has landed on main, the runner's report carrying its base place landed, and no act of crew's has yet recorded the landing and closed the bolt
- **THEN** its ledger's head carries ! and the attention line names the bolt as landed and still in the plan

### Requirement: The board prints its lanes as JSON
`crew board --json` SHALL print the same board as JSON: for each partition, its lanes as lists of objects, each object with its partition, its team where it has one, and its markers, each marker with its rail group, its card key, when its row began to wait, its card, and, when no card is open, the words of Pending You's refusal of the last post under its key, or none, and the attention items; and the hosts that did not answer and the plans not read.

#### Scenario: The page's input
- **WHEN** `crew board --label wldn --json` runs while unit a is in review
- **THEN** the JSON's Construction lane holds tenant-environments with team swb-1, and unit a with a marker of group review and its card key

### Requirement: The rail and the board come from one read
When the host's follower refreshes, crew SHALL read the plan, the kits and the run record once for both the rail and the board, and once for every partition with an operator session on the host, each kit read once however many of those partitions it serves: it SHALL write each partition's rail, what `crew rail` prints, as that partition's rail frame, and its board's data as its board frame; the rail tab SHALL draw the rail's frame and the board tab SHALL draw the board from that same read at its own width. When the follower has not refreshed a frame for more than three of its periods, its tab SHALL say how old it is; when none was ever written, the tab SHALL say so and that the host's follower writes it.

#### Scenario: One refresh
- **WHEN** the host's follower refreshes for a partition with three units in flight on one host
- **THEN** that host's kits are read once and the state branch fetched once for both frames

#### Scenario: Two partitions on one host
- **WHEN** the host's follower on mac-studio, which holds operator sessions of wldn and swancloud, makes its first refresh, and both partitions' teams build kits on the box
- **THEN** the box's kits are gathered once for both partitions, and wldn's and swancloud's rail frames, board frames and agents' views are each written from that one read

#### Scenario: The loop has stopped
- **WHEN** the host's follower has not run for five minutes
- **THEN** the board tab still shows its last board, and the rail tab its last rail, each headed with how long ago it was read

#### Scenario: Never written
- **WHEN** the board tab opens on a host where no follower has written wldn's frame
- **THEN** it says there is no board for wldn yet and that the host's follower writes it

### Requirement: The host's follower runs with no tab
`crew _follow` SHALL be the host's follower with no tab, the command a job of the host's runs: once a minute on its clock, and whenever this host's cache of a partition's state branch moves, for every partition with an operator session on the host, it SHALL make the refresh the rail tab's loop makes. crew SHALL run no service of its own for it.

#### Scenario: The host's job follows
- **WHEN** swancloud's job runs `crew _follow` on mac-studio, which holds operator sessions of wldn and swancloud, and no console tab is open
- **THEN** both partitions' board frames, rail frames and agents' views are written each period, the card sessions of closed cards are ended, and due restarts are handed out

### Requirement: A host has one follower
Whoever follows on a host, `crew _follow` or a rail tab's loop, SHALL hold the host's follower lock while it follows, saying which it is. A `crew _follow` started while another holds it SHALL wait for it, reading nothing; a rail tab that cannot take it SHALL draw the frames and try again.

#### Scenario: A second follower
- **WHEN** a rail tab's loop holds mac-studio's follower lock and `crew _follow` starts
- **THEN** `crew _follow` reads nothing until the rail tab is closed, and then follows

#### Scenario: The job is followed by a tab
- **WHEN** `crew _follow` holds the lock and the user opens wldn's rail tab
- **THEN** the rail tab draws the follower's frames and reads nothing itself

### Requirement: A refresh after nothing moved reads nothing
Before it reads, the host's follower SHALL check whether anything the refresh acts on has moved since its last read: each partition's state branch, its runners' branches and blueprints main as this host's caches hold them; each kit's refs, worktrees, places' changes and slots files, on every host it reads; each of those hosts' card readings folder, where a reading the user sent back lands; the cards as Pending You last answered for them; crew's checkout; and the teams file. It SHALL stamp this host's kits and readings in its own process at each refresh, starting nothing, and SHALL ask another host for its kits' and readings' stamps only when something there could have moved: when the drive's branch of a partition with work on that host moved, when that host's runner's branch moved, when the host did not answer the last time it was asked, and otherwise once in ten minutes; a host not asked SHALL count as unmoved. When nothing has moved, the follower SHALL start no read and no process, and at a tick of its clock none beyond its fetches, and SHALL write each partition's rail frame, board frame and agents' views again from its last read, as of the check.

#### Scenario: An idle host
- **WHEN** the host's follower on mac-studio ticks, every card it acts on answered at an earlier ask, and nothing it read has moved since its last refresh
- **THEN** it fetches each repository once and starts no other process: no git besides, no gather, no ssh, no sluice, no Pending You bridge, no herdr and no portless; it asks the box nothing, and writes wldn's frames again from its last read, each saying the time of this refresh

#### Scenario: The box asked when something there could have moved
- **WHEN** the box runs wldn's runner and holds a kit of wldn's, and the box's runner reports, or wldn's branch moves
- **THEN** the follower's next refresh asks the box for its kits' and readings' stamps in one ssh, and the refresh after it, with nothing moved since, asks the box nothing

#### Scenario: A partition with nothing on the box moves
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
When something has moved, the host's follower SHALL read again only what rests on what moved: a moved state tip, that partition's plan, proposals and run record at the new tip; a moved blueprints tip, its signals; a moved kit, that kit alone, on its host; a moved runner's branch, that partition's runners' records at the new tip, each piece's stage and submission among them, and no kit gathered whose stamp did not move; a moved readings folder, that host's card sessions swept and nothing read; cards whose answers moved, the card sweep run and nothing read. What did not move SHALL be taken from the follower's last read, which crew SHALL never read as a fact once what it was read at has moved, and keep in the follower's process alone, writing none of it.

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
The host's follower SHALL fetch once a minute on its own clock, never faster, each repository it reads once, carrying every branch it reads of that repository in the one fetch: each partition's state branch with its runners' branches, and its blueprints main. It SHALL never fetch because an entry arrived. A branch a repository does not have yet SHALL cost that repository's fetch no more than one fetch again without it. Between its clock's ticks it SHALL look at this host's caches with no process, refreshing within a few seconds when a write on this host moves one; it SHALL start no `crew events --follow` to wake on.

#### Scenario: An entry from another host
- **WHEN** a place's runner on the box reports, or an agent on the box writes an entry, and wldn's branch gains it
- **THEN** mac-studio's follower shows it at its clock's next fetch, within a minute, and fetched nothing in between

#### Scenario: Two partitions in one state repository
- **WHEN** the follower follows madswan and swancloud, whose branches are both in afterthought/crew-state
- **THEN** each tick fetches afterthought/crew-state once, both partitions' branches and their runners' in that one fetch

#### Scenario: An entry written on this host
- **WHEN** the user approves a unit from the rail tab's shell on mac-studio
- **THEN** the follower refreshes within a few seconds, without fetching

### Requirement: The follower asks Pending You about cards on its clock
The host's follower SHALL ask Pending You about the cards its sweep acts on, and herdr about their askers' panes, only at its clock's tick, in one bridge, and only when something there could have moved: a card or asker its last ask did not answer for, a last ask whose bridge failed or whose listing could not read an asker, or ten minutes since its last ask. It SHALL ask nothing when there is no card or asker to ask about. Its sweeps between asks SHALL judge the cards as the last ask answered, and a card its last sweep left SHALL count the cards as moved at the next ask, not at every tick.

#### Scenario: A card lost between ticks
- **WHEN** Pending You no longer finds wldn's card for proposal 4, whose row is still on the rail, and nothing else moves
- **THEN** the follower asks Pending You nothing until its next ask, within ten minutes, and then takes the cards as moved and its card sweep posts the card again

#### Scenario: No card to ask about
- **WHEN** the follower's clock ticks and its last read names no card its sweep would act on
- **THEN** it starts no Pending You bridge at that tick

#### Scenario: Every card answered
- **WHEN** the follower's clock ticks and Pending You answered every card its sweep acts on at an ask less than ten minutes ago
- **THEN** it starts no Pending You bridge and no herdr listing at that tick

#### Scenario: A card the sweep left
- **WHEN** Pending You refused the close of a card whose row is gone, and nothing else moves
- **THEN** the cards count as moved again at the follower's next ask, not at each tick before it

### Requirement: What no stamp sees is read on the follower's clock
At a tick of its clock that asks a host (the requirement *A refresh after nothing moved reads nothing* says when), the host's follower SHALL read again that host's dev servers as portless lists them, and at a tick that asks Pending You (the requirement *The follower asks Pending You about cards on its clock*), herdr's listing of each card's asker its card sweep acts on; it SHALL take a change in either as moved, drawing the frames again and sweeping the cards with it, with nothing gathered. At every refresh, whether or not anything moved, it SHALL work out from the run record's times and the time now whether a batch is due by hours, and tell the partition's planner once when one is.

#### Scenario: A dev server started by hand
- **WHEN** a dev server is started by hand on the box, and nothing else moves
- **THEN** the board shows it after the follower's next tick that asks the box, within ten minutes, and no kit is gathered

#### Scenario: An asker's agent gone
- **WHEN** the agent that asked a question on a card leaves its pane, and nothing else moves
- **THEN** at the follower's next ask, within ten minutes, herdr's listing shows the pane empty, and the card sweep withdraws the question, naming the asker

#### Scenario: A batch made due by the hours
- **WHEN** wldn's last batch was delivered as many hours ago as its setting, one change is due, and nothing moves
- **THEN** the follower's next refresh tells wldn's planner the batch is due, reading nothing to find it, and the refresh after reads the entry and tells nothing again

### Requirement: A held bolt's head line shows its age and who held its time
Each held bolt's head line SHALL show, in the Construction lane, in the board's JSON and in every agent's band that draws it, the bolt's age since its newest give and the minutes of that age each holder held, leaving out a holder that held none. Minutes crew can't split between the team and the kit SHALL be shown as the team's or the kit's, with why, never added to either. It SHALL also show who holds the bolt now and since when; for a hold, what the hold is for. Once nobody has held the bolt for five minutes, the line SHALL say it is stalled. When the give, the stages or the submissions can't be read, the line SHALL say the age or the split can't be told and why, and SHALL never show a guessed share. No card SHALL be raised and no one told because of a bolt's age.

#### Scenario: The bands
- **WHEN** the follower writes swb-1-conductor's view and the planner's
- **THEN** each draws `b`'s head line with its age, its shares and who holds it now, as the lane does

#### Scenario: Stalled
- **WHEN** nothing of `b` has run, stood in sluice, had a card open or been held for seven minutes
- **THEN** those seven minutes are nobody's, and the line says `b` is stalled since they began

#### Scenario: Nobody for a moment
- **WHEN** a stage of `b` ended two minutes ago and nothing has started since
- **THEN** the line says nobody holds `b` since then, and does not say it is stalled

#### Scenario: A give that can't be read
- **WHEN** the run record holds no give of `b` in the days the board reads
- **THEN** `b`'s head line says its age can't be told and why, and shows no share

#### Scenario: Minutes that can't be split
- **WHEN** twelve minutes of `b`'s age were a decided merge's stay in sluice whose checks' start crew does not hold
- **THEN** the line shows `team or kit 12m` among its shares, says that sluice's record of the merge keeps no start of its checks, and counts those minutes in neither the team's share nor the kit's

### Requirement: Each minute of a bolt's life goes to one holder
Each minute of a held bolt's life SHALL go to exactly one holder, the first of these that applies:

1. the team, while a stage of the bolt's units, chores or fixes runs other than a merge;
2. the kit, while one of the bolt's submissions (a merge into its branch, or its landing on its kit's main) is under test in sluice, from the start of its checks to its decision;
3. the team or the kit, unsplit, while one of the bolt's submissions is in sluice, from its submit to its decision, and crew holds no start of its checks; and for the whole run of a merge stage that ended when crew holds no submit of that merge's work within it;
4. the team, while a merge stage of the bolt's runs, or one of its submissions stands in sluice not under test, or a decided submission stood from its submit to the start of its checks;
5. the user, while a card of the bolt's is open;
6. a hold, while one is recorded on the bolt;
7. nobody.

The team's share of a merge SHALL end at its submit unless the submission stands queued, and no minute between a submit and its decision SHALL go to the team under its merge stage when crew can't tell queued from under test.

#### Scenario: A team at work
- **WHEN** bolt `b` was given to swb-1 three hours ago, a code stage ran for two hours, a batch card holding its unit was open for forty minutes with nothing running, and nothing held it for twenty minutes
- **THEN** `b`'s head line in the lane says `3h 00m`, team `2h 00m`, user `40m`, nobody `20m`, and names no kit, hold or team-or-kit share

#### Scenario: A merge under test
- **WHEN** unit `a`'s merge `#41` into `bolt/b` stood queued for five minutes and then under test for twelve, while `a`'s merge stage ran throughout and no other stage ran
- **THEN** the five minutes are the team's and the twelve the kit's, and while `#41` is under test the line says the kit holds `b` since the start of its checks

#### Scenario: A stage beside a merge under test
- **WHEN** unit `c`'s code stage runs while unit `a`'s merge `#41` is under test
- **THEN** those minutes are the team's

#### Scenario: A decided merge with its checks' start
- **WHEN** `#41`, landed, was submitted at 14:00, its checks began at 14:05 as the follower saw while it stood, and it was decided at 14:17
- **THEN** 14:00 to 14:05 are the team's, 14:05 to 14:17 the kit's, and no minute of it is team-or-kit

#### Scenario: A decided merge whose checks' start is not kept
- **WHEN** `#41`, landed, was submitted at 14:00 and decided at 14:17, and neither the overview the follower kept nor sluice's record gives when its checks began
- **THEN** 14:00 to 14:17 are team-or-kit, though `a`'s merge stage ran throughout, and none of them is the team's or the kit's

#### Scenario: A merge that ended before the follower saw it
- **WHEN** the follower started after `a`'s merge stage of 13:50 to 14:20 and its merge's submission were over, so it holds no submit of `a`'s merge
- **THEN** 13:50 to 14:20 are team-or-kit

### Requirement: Each holder is read from what crew already keeps
Every holder of a bolt's time SHALL be read from what crew already keeps, and nothing SHALL be recorded to make the reading:

- **Stages**: the run record's stage starts and ends for the bolt's work since the give.
- **Submissions**: none. The runner's report carries a piece's submission and a bolt's landing, but no time of either, and crew reads no queue or record of sluice's, so the lane, the rail, the bands and a landing's entry place no minute by a submission; a landing's entry records the split the views give (`plan.20`).
- **Cards**: the run record's card posts, changes, answers and closes. A card holds the bolt for the user from its post until the user's answer on it or its close, whichever comes first. A card is the bolt's when:
  - it is under the bolt's own key, `land/<bolt>`;
  - it is a batch's card holding work of the bolt's;
  - it is a proposal's card whose changes name the bolt or its work;
  - it is the kit's landings card while its last post or change names the bolt among its rows, from the later of that post or change and the end of the bolt's last merge;
  - it is a question an agent of the bolt's team asked the user while the team held the bolt;
  - or its post names the bolt or its work.
  A question of a main-level role's that names neither the bolt nor its work is no card of the bolt's.
- **Holds**: the run record's hold of the team's host, from its hold to its go.

#### Scenario: The user's card
- **WHEN** every unit of `b` has merged, nothing runs, and its kit's landings card has been open for an hour
- **THEN** that hour is the user's, and the line says the user holds `b` since the card's post, naming its key

#### Scenario: A question from the team
- **WHEN** swb-4's unit stopped short and swb-4-conductor's question to the user is open, with nothing of its bolt running
- **THEN** the minutes since its post are the user's

#### Scenario: A held host
- **WHEN** nothing of `b` runs and no card of it is open, while its team's host was held by the user at 14:02 and not yet let go
- **THEN** the minutes since 14:02 are the hold's, and the line says `b` is held since 14:02 because its host is held, naming who held it

#### Scenario: A row drawn from the overview
- **WHEN** sluice's overview of switchboard-kit would hold `b`'s merge `#41` under test since 14:05 and recent events naming `#40` landed at 13:58
- **THEN** `b`'s head line reads nothing of the overview, starts no sluice process, and counts neither `#41` nor `#40` among its shares

#### Scenario: A submission the runner reports
- **WHEN** the runner carries `b`'s unit `a` with its submission `#41` under test, and since 14:05 no stage of `b`'s has run, no card of it has been open and no hold has been on it
- **THEN** `b`'s head line counts none of the minutes since 14:05 the kit's or the team's, says nobody holds `b` since 14:05, and no sluice process is started

#### Scenario: A landing by pull request
- **WHEN** the runner's report carries `b`'s base place landed after its submission `#52`, from `pull/9`, stood under test, and crew's read records `b`'s landing
- **THEN** the landing's entry records the age and split `b`'s head line gives from the run record, and none of `#52`'s minutes is the kit's

#### Scenario: The user answered the landings card
- **WHEN** `b`'s kit's landings card, posted at 14:00 with `b` among its rows, was answered by the user at 14:40, and `b` has not landed
- **THEN** 14:00 to 14:40 are the user's, the minutes after 14:40 are nobody's, and the line does not say the user holds `b`

#### Scenario: A landings card that no longer carries the bolt
- **WHEN** `b`'s kit's landings card was changed at 15:00 to rows that no longer name `b`
- **THEN** the minutes after 15:00 are not the user's for that card

#### Scenario: A main-level question about something else
- **WHEN** agentplot-design's question `ask/agentplot-design/sluice-who-claims` has been open since 19:01, its post naming the asker alone, and nothing of flume's bolt `f` runs
- **THEN** none of `f`'s minutes since 19:01 are the user's for that question, and `f`'s line names no such question

### Requirement: The planner's and ops's bands show what places wait on them for
`board.agent_views` SHALL give the planner's band each launched place that stopped short asking or waits on its caller, past its kind's bound among them whatever stage it last delivered, with its question or Flume's words and the stage it waits to retry or its submission. It SHALL give main-level ops's band each fix of main and each take-main fix in flight with its stage. crew's mod SHALL draw both above the agent's prompt.

#### Scenario: A question in the planner's band
- **WHEN** `a`'s construct stopped short asking "Which partition's rail?"
- **THEN** madswan-planner's view lists `a` with that question, and the mod draws it

#### Scenario: A place past its bound in the planner's band
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place waiting on its caller to retry code past its bound, its verify delivered
- **THEN** madswan-planner's view counts one place waiting on an answer and lists `a` waiting on its caller at code with Flume's words, and the mod draws it

#### Scenario: A fix of main in ops's band
- **WHEN** `main--a-test-reads-its-fixture` is in code
- **THEN** madswan-ops's view lists it at code, and the mod draws it

### Requirement: A role that runs as its kind has its view
Each role its partition runs as its kind SHALL have a view among the agents' views under its run's name, `<label>-<role>`, drawn above its run's prompt by crew's mod where crew's plugin loads: what its turn took, each ask and waiting place on a line of its own and the ends Flume held for the role counted on its head line, never listed, and how many asks wait for the role and since when.

#### Scenario: A run with an ask waiting
- **WHEN** madswan's planner run took two asks and a third has waited four minutes
- **THEN** madswan-planner's view shows the two it took and one waiting for four minutes

#### Scenario: Nothing waiting
- **WHEN** madswan's planner run took one ask and nothing else waits
- **THEN** madswan-planner's view shows the one it took and says nothing waits

#### Scenario: Ends counted
- **WHEN** madswan's planner run took one ask and nine ends of three places
- **THEN** madswan-planner's head line says its turn took one and nine ends, and its view has one line for the ask and none for an end

### Requirement: The attention line names a role's run that waits
The board's attention line SHALL name each run of a role that the runner's records show stopped short, with its words, or lost, with its place and host, and SHALL print no command for it.

#### Scenario: A lost run
- **WHEN** the runner's records show madswan's design run `crew-design--madswan` on deneb lost
- **THEN** the attention line names madswan's design run as lost, with its place and deneb, and prints no command

### Requirement: Construction shows a started bolt from the runner's records
The Construction lane SHALL show each started bolt as a ledger of its units, chores and fixes with the stages the runner's records give, its head line naming the host and the stream its work runs in, as the runner that took it reported them, and no slot. The board's JSON SHALL give each such ledger its host and stream.

#### Scenario: A started bolt's ledger
- **WHEN** `x` is started, deneb's runner keeping its kit with the stream `madswan`, `a` at `code 3/7` and `b` waiting on `a`
- **THEN** the board's Construction lane shows `x` on deneb in stream `madswan`, `a` at code 3/7 and `b` waiting on `a`, and no slot line

### Requirement: Construction shows each bolt in flight as a ledger, with no server for a started bolt's work
The Construction lane SHALL show each bolt in flight as a ledger: its head line with its repository and its kit's host, and, once every unit and chore of it has merged and its verification is green while not every one has landed, that it waits to land; then its landing as the runner's report gives it, each state its own (record 0056 point 4): while crew's land of it is posted and the runner has not answered it, that its landing is asked, with the land's request; while the runner reports its base place's submission in the merge queue, that, with the entry's number and its state as Flume names them; once Flume has refused it at its head, in Flume's words, that its landing was refused and the bolt is open for work, for a failed check, or that it takes main first, for a conflict; once the runner has refused its land or Flume reports its submission withdrawn or refused, that its landing was stopped at that head, in their words; once the runner reports it landed, that it landed at Flume's commit, and once it has landed on main and its close was refused, that it landed and was not closed, with the words of its last refused close; where crew can't tell its landing from the runner's report, that and why; and for a started bolt with no launch of `bolt/<bolt>`, that it was started before bolts were base places and lands under the crew that started it. The ledger SHALL then show each unit in plan order with its stage, its tasks done and total in code or verify, and its submission's number while one stands, as Flume's status of its place gives it and the runner carried it; and each fix of the bolt with whether it has merged, and its submission's number while one stands, read the same way. A started bolt's ledger SHALL show no dev server for the bolt or any of its work, whose places are Flume's, until the runner reports a place's addresses. The planner's band SHALL draw each bolt in flight as this ledger, its head line as the lane's, since ordering within a bolt, batches and amendments are the planner's; main-level ops's band SHALL draw each landing asked or in the merge queue, with its request or the queue's entry, the head line of each bolt started before bolts were base places, and the head line of each bolt whose close was refused.

#### Scenario: A unit in code
- **WHEN** unit a of bolt tenant-environments is in code with 1 of 2 tasks ticked, 
- **THEN** tenant-environments' ledger has a line for a saying code 1/2, and names no slot

#### Scenario: A started bolt's work shows no server
- **WHEN** `tenant-environments` is started, and a dev server runs in a worktree of its kit named for it
- **THEN** its ledger shows no URL for the bolt, its units or its fixes, and no note about one

#### Scenario: A bolt waiting to land beside the one being built
- **WHEN** `doctor-rows` has every unit merged and its verification green, and `ssh-fix` of the same kit has a unit in code
- **THEN** the lane shows `doctor-rows`'s head line saying it waits to land, and `ssh-fix`'s ledger beside it

#### Scenario: A merge standing in sluice
- **WHEN** the runner carries unit a of bolt tenant-environments with its submission `#41` under test on `bolt/tenant-environments`
- **THEN** a's line in the lane says `submitted #41`, once

#### Scenario: A landing asked
- **WHEN** crew posted `doctor-rows`'s land as request 57, and the runner has not answered it
- **THEN** `doctor-rows`'s head line, in the lane and in main-level ops's band, says `landing asked, request 57`

#### Scenario: A landing standing in sluice
- **WHEN** the runner's report carries `doctor-rows`'s base place with its submission `#412` under test in the merge queue
- **THEN** `doctor-rows`'s head line, in the lane and in main-level ops's band, says `landing #412 under test`

#### Scenario: A landing recorded queued that sluice no longer has standing
- **WHEN** the run record's last `bolt.submit` on `doctor-rows` is its land asked as request 57, and the runner's report carries its base place over and landed at `1a2b3c4`, no submission of it standing, while the plan still holds `doctor-rows`
- **THEN** `doctor-rows`'s head line says `landed at 1a2b3c4`, from the runner's report, and nothing of sluice's queue is read

#### Scenario: A queue that can't be read
- **WHEN** sluice's record of the queue could not be read on swb-1's host, and crew posted tenant-environments' land as request 57, which the runner has not answered
- **THEN** nothing of it is said: crew reads no queue of sluice's, tenant-environments' head line says `landing asked, request 57`, and each line shows its submission as the runner carries it

#### Scenario: A runner that can't be read
- **WHEN** the branch of the runner that took tenant-environments' work can't be read, and crew posted tenant-environments' land as request 57
- **THEN** the lane names that runner as one that can't be read, no line of the bolt's work shows a number, and its head line says its landing can't be told, and why

#### Scenario: A landing rejected
- **WHEN** the runner's report carries Flume's verdict on `doctor-rows`'s submission at its present head failed, waiting on its caller, its words naming `tests:logic`
- **THEN** `doctor-rows`'s head line, on the lane and in the planner's band, says its landing was refused at that head and the bolt is open for work, with Flume's words

#### Scenario: Landing again
- **WHEN** `doctor-rows`'s landing was refused in conflict with main at its old head, its take-main fix merged, it reads proven at its new head, and crew posted its land again on the standing send as request 63
- **THEN** its head line says `landing asked, request 63`, and nothing of the refusal at its old head

#### Scenario: A landing refused in conflict
- **WHEN** the runner's report carries Flume's verdict on `doctor-rows`'s submission at its present head a conflict with main on `README.md`
- **THEN** `doctor-rows`'s head line says its landing was refused in conflict, with Flume's words, and that it takes main first

#### Scenario: A landing stopped
- **WHEN** the runner answered `doctor-rows`'s land refused, a place on `bolt/doctor-rows` being live
- **THEN** `doctor-rows`'s head line says its landing was stopped at that head, in the runner's words

#### Scenario: A bolt started before bolts were base places
- **WHEN** started `doctor-rows` has no launch of `bolt/doctor-rows` in `requests.rec`
- **THEN** `doctor-rows`'s head line, in the lane and in main-level ops's band, says it was started before bolts were base places and lands under the crew that started it

#### Scenario: A close refused
- **WHEN** `doctor-rows` has landed on main and the run record's last `bolt.land` on it since then is refused, saying chore `tidy-rows` has not landed on main
- **THEN** `doctor-rows`'s head line, on the lane and in main-level ops's band, says it landed on main and was not closed, with those words, in the attention gutter

### Requirement: An agent's band says which of its cards the user answered
Among the cards `board.agent_views` gives an agent's band, a card whose answer the run record holds SHALL say it was answered and how long ago, and that it is the agent's to act on, in place of how long it has been open. Main-level ops's band SHALL say on a kit's landing line that its card is answered and that crew asks the runner to land what the user ticked. crew's mod SHALL draw both as the views give them.

#### Scenario: The planner's answered proposal card
- **WHEN** `proposal/57`'s card is wldn-planner's, open, and the run record holds the user's answer on it from five minutes ago
- **THEN** wldn-planner's band shows `proposal/57` answered 5m ago, yours to act on, and not open

#### Scenario: Ops's answered landings card
- **WHEN** `land/sluice`'s card is agentplot-ops's and the run record holds the user's answer on it
- **THEN** agentplot-ops's band shows the card answered, and its `land/sluice` line says crew asks the runner to land what the user ticked

#### Scenario: The mod draws an answered card
- **WHEN** the views give agentplot-ops a card line saying `land/sluice` was answered 5m ago, its to act on
- **THEN** crew's mod draws that line above ops's view as given

### Requirement: The follower runs no sluice
The host's follower SHALL start no sluice process: no `sluice overview --watch`, no `sluice overview` at its clock's tick, and no `sluice status`. It SHALL keep no submission of its own. It SHALL learn that a piece's submission moved from the partition's runner's branch, which it looks at with no process and fetches on its clock. crew SHALL read and name no folder of sluice's.

#### Scenario: A merge moves in sluice's queue
- **WHEN** a unit's merge into a bolt of switchboard-kit on the box is queued in sluice, and the box's runner has not reported since
- **THEN** the follower's next refresh shows no change on the unit's line, and starts no sluice

#### Scenario: The runner reports the merge
- **WHEN** the box's runner then reports the unit's place submitted as `#41`
- **THEN** the follower's refresh after its clock's next fetch shows `submitted #41` on the unit's line, gathering no kit whose stamp did not move

#### Scenario: A follower's life
- **WHEN** the follower on mac-studio reads two partitions whose bolts are in switchboard-kit on the box, through a read, ticks with nothing moved, a runner's report and a gather of the kit
- **THEN** it starts no `sluice` process on either host and opens no ssh for a sluice command

### Requirement: A gather runs no sluice
A gather of a kit SHALL run no sluice command. A request to it SHALL hand in no queue. Its answer SHALL carry no `submissions`, `decided`, `overview`, `overviews`, `verdict` or `beside`.

#### Scenario: A gather of a kit with a held bolt
- **WHEN** a kit is gathered while bolt `b` is held there, with a merge of it decided, one standing, and a head landed beside the queue, and a `sluice` on the path that records every call
- **THEN** the gather runs no `sluice` command, and its answer carries no `submissions`, `decided`, `overview`, `verdict` or `beside`

### Requirement: Ops's band lists each landing fix Flume runs on a bolt
Main-level ops's band SHALL list each live landing fix of a started bolt's base place among its fixes in flight, after the take-main fixes, with its kit, its name, that it is a landing fix, and what it does, and its head line SHALL count it among the fixes in flight. The mod SHALL draw the band's lines as the views give them (`code.8`).

#### Scenario: A landing fix in ops's band
- **WHEN** `y`'s base place lists `y-1`, for a conflict, live
- **THEN** ops's band lists `fix y-1`, a landing fix taking main in, and its head line counts one fix in flight

#### Scenario: The mod draws it
- **WHEN** the views file gives ops's view with `y-1`'s line
- **THEN** the mod draws that line above ops's prompt as given

### Requirement: A bolt's head line names its landing fix
A bolt's head line and its line in `crew bolts` SHALL end its landing's words with its landing fix: which fix takes main in or makes the failed checks pass, that Flume launches it, or that Flume ran its landing fixes and the bolt waits on ops.

#### Scenario: A landing fix taking main in
- **WHEN** `y`'s landing was refused for a conflict and its base place lists `y-1` live
- **THEN** `y`'s head line ends saying Flume's landing fix `y-1` takes main in

#### Scenario: The bound spent on the head line
- **WHEN** `y`'s landing was refused with its three landing fixes run
- **THEN** `y`'s head line ends saying Flume ran its 3 landing fixes, and it waits on ops
