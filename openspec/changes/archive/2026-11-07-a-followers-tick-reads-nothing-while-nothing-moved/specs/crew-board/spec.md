## MODIFIED Requirements

### Requirement: A refresh after nothing moved reads nothing
Before it reads, the host's follower SHALL check whether anything the refresh acts on has moved since its last read: each partition's state branch, its runners' branches and blueprints main as this host's caches hold them; each kit's refs, worktrees, places' changes and slots files, on every host it reads; each kit's queue, as sluice's overview last printed it; each of those hosts' card readings folder, where a reading the user sent back lands; the cards as Pending You last answered for them; crew's checkout; and the teams file. It SHALL stamp this host's kits and readings in its own process at each refresh, starting nothing, and SHALL ask another host for its kits' and readings' stamps only when something there could have moved: when the drive's branch of a partition with work on that host moved, when that host's runner's branch moved, when a watch of one of its kits printed a new line or ended, when the host did not answer the last time it was asked, and otherwise once in ten minutes; a host not asked SHALL count as unmoved. When nothing has moved, the follower SHALL start no read and no process, and at a tick of its clock none beyond its fetches, and SHALL write each partition's rail frame, board frame and agents' views again from its last read, as of the check.

#### Scenario: An idle host
- **WHEN** the host's follower on mac-studio ticks, every card it acts on answered at an earlier ask, and nothing it read has moved since its last refresh
- **THEN** it fetches each repository once and starts no other process: no git besides, no gather, no ssh, no sluice, no Pending You bridge, no herdr and no portless; it asks the box nothing, and writes wldn's frames again from its last read, each saying the time of this refresh

#### Scenario: The box asked when something there could have moved
- **WHEN** the box runs wldn's runner and holds a kit of wldn's, and the box's runner reports, or wldn's branch moves, or the watch of the kit on the box prints a new line
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
- **WHEN** sluice writes its records and logs in switchboard-kit's git folder on the box, and its overview prints no new line
- **THEN** the follower takes the kit as unmoved, having read nothing of that folder

#### Scenario: A task ticked with nothing committed
- **WHEN** a coder on mac-studio ticks a task in its place's tasks.md and commits nothing
- **THEN** the follower's next refresh on its clock takes the kit as moved and gathers it again

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

### Requirement: The follower follows each kit's queue through sluice's overview
The host's follower SHALL learn that a kit's merge queue moved from sluice's overview alone. It SHALL keep one `sluice overview --json --watch` running for each repository whose queue its read shows on a host, in a main checkout of it on that host, two checkouts of one repository on this host sharing one watch, take a line whose document differs from the last (its time aside) as the queue's move for each kit of that repository, and read the queue from that line. Where no watch can run, because the host's sluice has no watch or the kit's watch ended or could not start, it SHALL ask `sluice overview --json` once at a tick of its clock that asks that host, and open an ended watch again at the next tick. A gather of a kit SHALL start no sluice process while a watch's line gives the queue, and at most one `sluice overview --json` where none does; it SHALL run no `sluice status`, for a held bolt's branch or for the kit's main. The follower SHALL keep, for each kit, every submission of a held bolt it has seen stand, with when it was submitted and, once a candidate tested it, when its checks began, and SHALL keep it across later lines and gathers while the bolt is held. When a line no longer holds a kept submission, the follower SHALL take it as decided at the time that line's recent events give for it, or at that line's own time when they name it in no event, reading nothing else. crew SHALL read and name no folder of sluice's.

#### Scenario: A merge moves in sluice's queue
- **WHEN** a unit's merge into a bolt of switchboard-kit on the box is queued in sluice, and the kit's overview watch prints a new line
- **THEN** the follower's next refresh, within a few seconds, shows the submission's number on the unit's row, gathers no kit and starts no sluice

#### Scenario: One watch for each kit
- **WHEN** the follower on mac-studio reads two partitions whose bolts are both in switchboard-kit on the box, or two kits that are checkouts of one repository on mac-studio
- **THEN** it keeps one overview watch for that repository, over one ssh to the box or as one child on mac-studio, and a refresh that gathers a kit of it takes its queue from the watch's line and starts no sluice process

#### Scenario: A host whose sluice has no watch
- **WHEN** the box's sluice refuses `--watch`
- **THEN** the follower asks the box's kits' overviews once at each tick of its clock that asks the box, in that tick's one ssh to it, and not between ticks

#### Scenario: A watch ends
- **WHEN** the ssh holding switchboard-kit's watch drops
- **THEN** the kit's row says its queue can't be read and why until the next tick, which opens the watch again and asks the overview once

#### Scenario: A held bolt's decided merges
- **WHEN** the follower gathers switchboard-kit while bolts `b` and `c` are held there, with merges of both decided and one of `b`'s standing
- **THEN** the gather runs no `sluice status`, for `bolt/b`, `bolt/c` or main, and the rows of `b` and `c` are drawn from the overview the watch last printed and what the follower kept of each submission

#### Scenario: A merge decided between gathers
- **WHEN** `b`'s merge `#41`, kept since it was submitted at 14:00 and tested from 14:05, leaves the queue on a line whose recent events say it landed at 14:17
- **THEN** the follower keeps `#41` decided at 14:17, starts no process to learn it, and still holds it after the next gather of the kit

#### Scenario: A withdrawn merge
- **WHEN** a kept merge of `b` leaves the queue on a line printed at 14:20 whose recent events do not name it
- **THEN** the follower keeps it decided at 14:20

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
