## ADDED Requirements

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

## MODIFIED Requirements

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

### Requirement: Each holder is read from what crew already keeps
Every holder of a bolt's time SHALL be read from what crew already keeps, and nothing SHALL be recorded to make the reading:

- **Stages**: the run record's stage starts and ends for the bolt's work since the give.
- **Submissions**: none in the views. The runner's report carries a piece's submission, but no time of it, and crew reads no queue of sluice's, so the lane, the rail and the bands place no minute by a submission. A read made once at an act MAY place them: the landing's own read of sluice's record, as crew's landing makes it, whose split the landing's entry records. There, a landing on main is the bolt's when it came from `bolt/<bolt>`, from a pull request opened from it, or when its number is the one the run record's queued `bolt.submit` of the bolt names.
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
- **WHEN** sluice's record read at `b`'s landing names `#52`, from `pull/9`, landed, and the run record's queued `bolt.submit` of `b` names `#52`
- **THEN** `#52` is `b`'s landing in the split its landing's entry records

#### Scenario: The user answered the landings card
- **WHEN** `b`'s kit's landings card, posted at 14:00 with `b` among its rows, was answered by the user at 14:40, and ops has not yet submitted `b`
- **THEN** 14:00 to 14:40 are the user's, the minutes after 14:40 are nobody's, and the line does not say the user holds `b`

#### Scenario: A landings card that no longer carries the bolt
- **WHEN** `b`'s kit's landings card was changed at 15:00 to rows that no longer name `b`
- **THEN** the minutes after 15:00 are not the user's for that card

#### Scenario: A main-level question about something else
- **WHEN** agentplot-design's question `ask/agentplot-design/sluice-who-claims` has been open since 19:01, its post naming the asker alone, and nothing of flume's bolt `f` runs
- **THEN** none of `f`'s minutes since 19:01 are the user's for that question, and `f`'s line names no such question

### Requirement: Construction shows each bolt in flight as a ledger, with no server for a started bolt's work
The Construction lane SHALL show each bolt in flight as a ledger: its head line with its repository and its kit's host, and, once every unit and chore of it has merged and its verification is green while not every one has landed, that it waits to land; while the run record has its landing queued, that its landing is queued, with the number the run record holds; while it is landing again, that, with the submission sluice rejected before it; while sluice's rejection of its landing is at its head, that its landing was rejected and the bolt is open for work, with sluice's words, each state its own (bolt-teams "A landing queued holds its bolt's work"); once it has landed on main and its close was refused, that it landed and was not closed, with the words of its last refused close; each unit in plan order with its stage, its tasks done and total in code or verify, and its submission's number while one stands, as Flume's status of its place gives it and the runner carried it; and each fix of the bolt with whether it has merged, and its submission's number while one stands, read the same way. A started bolt's ledger SHALL show no dev server for the bolt or any of its work, whose places are Flume's, until the runner reports a place's addresses. The planner's band SHALL draw each bolt in flight as this ledger, its head line as the lane's, since ordering within a bolt, batches and amendments are the planner's; main-level ops's band SHALL draw each landing the run record holds queued or landing again, with its number, and the head line of each bolt whose close was refused.

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

#### Scenario: A landing standing in sluice
- **WHEN** the run record's last `bolt.submit` on `doctor-rows` is queued as submission 355, with no outcome
- **THEN** `doctor-rows`'s head line, in the lane and in main-level ops's band, says `landing queued as #355`

#### Scenario: A landing recorded queued that sluice no longer has standing
- **WHEN** the run record's last `bolt.submit` on `doctor-rows` is queued as submission 412, and sluice's queue on its kit's host would show no landing of it standing
- **THEN** `doctor-rows`'s head line, on the lane and in the planner's band, says its landing is queued as #412, and nothing of sluice's queue is read

#### Scenario: A queue that can't be read
- **WHEN** sluice's record of the queue could not be read on swb-1's host, and the run record has tenant-environments' landing queued as #412
- **THEN** nothing of it is said: crew reads no queue of sluice's, tenant-environments' head line says `landing queued as #412`, and each line shows its submission as the runner carries it

#### Scenario: A runner that can't be read
- **WHEN** the branch of the runner that took tenant-environments' work can't be read, and the run record has its landing queued as #412
- **THEN** the lane names that runner as one that can't be read, no line of the bolt's work shows a number, and its head line says `landing queued as #412`

#### Scenario: A landing rejected
- **WHEN** the run record has `doctor-rows`'s landing #412 refused at its present head for a conflict on `README.md`
- **THEN** `doctor-rows`'s head line, on the lane and in the planner's band, says its landing #412 was rejected at that head and the bolt is open for work, with sluice's words

#### Scenario: Landing again
- **WHEN** `doctor-rows`, rejected as #412, is queued again as #415
- **THEN** its head line says it is landing again as #415, after #412 was rejected

#### Scenario: A close refused
- **WHEN** `doctor-rows` has landed on main and the run record's last `bolt.land` on it since then is refused, saying chore `tidy-rows` has not landed on main
- **THEN** `doctor-rows`'s head line, on the lane and in main-level ops's band, says it landed on main and was not closed, with those words, in the attention gutter

## REMOVED Requirements

### Requirement: The follower follows each kit's queue through sluice's overview
**Reason**: crew calls no sluice and reads no record of sluice's (record 0056 point 1). A kit's queue, as sluice's overview prints it, is a record that the runner's report does not carry (point 4). What the bolt's rows drew from the queue, each piece's submission, the runner's report already carries, in Flume's status of the piece's place. So does the move of a submission: the runner reports it, and its branch moves.
**Migration**: The follower learns that a submission moved from the runner's branch, and a piece's line shows its submission from Flume's status of its place (requirement "The follower runs no sluice"; bolt-teams "A submission's number is on its bolt's row from the submit"). A bolt's landing is read from the run record. The time a submission stood in sluice is placed only by the landing's own read at its act (requirement "Each holder is read from what crew already keeps").
