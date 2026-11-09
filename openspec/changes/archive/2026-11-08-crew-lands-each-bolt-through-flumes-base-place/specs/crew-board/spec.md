## MODIFIED Requirements

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
