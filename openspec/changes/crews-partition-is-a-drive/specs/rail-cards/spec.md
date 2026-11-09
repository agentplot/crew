## MODIFIED Requirements

### Requirement: Each rail row has a card key
Each rail row SHALL have one card key, the thing's and not its version's: `proposal/<n>` for a proposal chain, `n` its first proposal; `batch/<n>` for review batch n; `land/<bolt>` for a bolt proven; `deploy/<env>` for a `manual` environment's open offer; `op/<env>/<n>` for a step that waits on the user; `record/<kit>/<number>` for a record proposed. crew SHALL post the row's card with that key as its idempotency key, filled out at its end with `_` to Pending You's eight characters when it is shorter, the same on every post of it, and SHALL record the post under the row's key. A question's card has no row and a key of its asker's own. There SHALL be no review row and no verify row. A batch's row SHALL last until its card closes or the batch waits on nothing (`review-batches`). A batch whose cards were posted under `batch/<n>-<k>` before one card per batch was built SHALL keep a row for each of those keys until its card closes or the units it holds wait on nothing, and SHALL have no `batch/<n>` row.

#### Scenario: A batch of seven
- **WHEN** review batch 3 holds seven changes and no card has been posted for it
- **THEN** the rail has one batch row for it, keyed `batch/3`, holding all seven units

#### Scenario: A key shorter than Pending You takes
- **WHEN** crew raises review batch 7's card, `batch/7` being seven characters, and raises it again after its first post had no answer within a minute
- **THEN** both posts are under `batch/7_`, so Pending You gives the second the card the first made, and the run record holds it under `batch/7`

#### Scenario: A batch posted as two cards before
- **WHEN** the run record holds the planner's posts of batch 2's cards under `batch/2-1` and `batch/2-2` from before one card per batch, and `batch/2-1` has closed
- **THEN** the rail has one row for batch 2, keyed `batch/2-2`, holding its units as before, until its card closes

#### Scenario: An old batch card whose units have landed
- **WHEN** batch 2's cards were posted under `batch/2-1` and `batch/2-2`, neither has closed, and every unit `batch/2-2` holds has landed while one unit of `batch/2-1` has not
- **THEN** the rail has one row for batch 2, keyed `batch/2-1`, and the sweep withdraws `batch/2-2`'s card, saying its units have landed

#### Scenario: A bolt proven again on a new head
- **WHEN** bolt `y` was ready to land at head `abc1234`, a note on its landing card named a defect, and a fix landed on the bolt at `def5678` with its verification green
- **THEN** its landing row's key is still `land/y`, and crew raises a new landing card under it, following the one the fix held

#### Scenario: A unit built again
- **WHEN** unit `u` was constructed at head `abc1234`, and construct runs again and commits `def5678`
- **THEN** no review row or key exists for either head; the unit's revised change is due for the drive's next batch, whose card's key is the batch's

#### Scenario: A verify report saved
- **WHEN** unit `u`'s verify saves its report `verify-u-20261013-1200.md`
- **THEN** the rail has no row for it, and a card keyed `verify/u/20261013-1200` belongs to no row

#### Scenario: A proposal replaced
- **WHEN** proposal 4 is replaced by proposal 5
- **THEN** the rail's row for proposal 5 has the key `proposal/4`, and its card is the chain's

### Requirement: A card says whose it is and where it belongs
crew SHALL ask each card in the name of the role whose row it is, with the host as the session's machine and the kit's checkout as its folder; a question's card SHALL be asked in its asker's crew name by the asker's session. A card SHALL be filed in the area of its kit, found by the kit's git remote, in the group named for its drive; crew SHALL create a kit's area that does not exist with the key `create-area:<owner>/<kit>`, and an agent SHALL create one under no other key and never a group. A card's title SHALL be the question, read cold, naming the thing.

#### Scenario: A review card
- **WHEN** a unit's change is due for a batch
- **THEN** no review card is asked for it; the batch's card, asked in the planner's name, names the unit and its team

#### Scenario: The first card in a kit
- **WHEN** crew raises the first card in switchboard-kit and Pending You matches no area to its remote
- **THEN** crew makes the area under `create-area:WilldanGroup/switchboard-kit`, named `switchboard-kit`, in the drive's group, and files the card there

#### Scenario: A landing card
- **WHEN** crew raises bolt `y`'s landing card for swb-1's team in switchboard-kit
- **THEN** the card is asked as `swb-1-conductor` on the team's host, sits in switchboard-kit's area in the `wldn` group, and its title asks whether to land bolt `y` on the kit's main

### Requirement: A crew agent's card acts are in the run record
Each card crew posts, changes, withdraws or closes, each answer of the user's on one of them that crew reads, and each card a crew agent posts, changes or closes through Pending You's tools, SHALL be an entry in the drive's run record naming the row's object or the asker, the card's id in `Card` and the key in `Key`, crew's read from Pending You's own reply, an agent's from the tool's result; an agent's act whose result names no card SHALL be recorded on the agent with `State: unread`, and `crew rail` SHALL list each such act of the last 14 days with its agent, its act and its time. An entry SHALL NOT hold a card's title, summary or other text.

#### Scenario: A card posted and closed
- **WHEN** crew raises `land/y`'s card `req_l1` and later closes it at the landing
- **THEN** the run record has a `card.post` entry on `bolt/y` with that key and `req_l1`, and a `card.close` entry with the same id

#### Scenario: A card posted through crew
- **WHEN** `crew ops offer srv --to abc1234` runs and Pending You answers with the card `req_d1`
- **THEN** the run record has a `card.post` entry on `env/srv` with the key `deploy/srv` and the card `req_d1`, and nothing written on the card

#### Scenario: A card the user answered
- **WHEN** crew reads `land/crew`'s card `req_l2` answered, ticking `y`
- **THEN** the run record has a `card.answer` entry on `kit/crew` with the key `land/crew`, `req_l2` and the answer in crew's words, and none of the user's own words

#### Scenario: The user's own sessions
- **WHEN** a Claude session crew did not start posts a Pending You card
- **THEN** nothing is written to crew's run record

#### Scenario: A question posted
- **WHEN** swb-1-conductor's `post_request` under `ask/swb-1-conductor/hold-the-macs` returns `req_q1`
- **THEN** the run record has a `card.post` entry on swb-1-conductor with that key and `req_q1`

#### Scenario: A question whose reply names no card
- **WHEN** swb-1-conductor's `post_request` under `ask/swb-1-conductor/hold-the-macs` returns a result that names no card
- **THEN** the run record has a `card.post` entry on swb-1-conductor with that key and `State: unread`, and `crew rail` lists it with swb-1-conductor, the act and its time

### Requirement: The check refuses what it cannot read, and only for crew's sessions
crew's hook SHALL run only in a session with `CREW_AGENT` set, and SHALL refuse a card's post, change or close, or an area's making, when it cannot read the agent's drive, the teams file, or crew's record of its cards, the run record on this host that holds the key of the card a change or close names, naming what it could not read and saying to try again later, never letting a call through on a guess. It SHALL read no plan and fetch no state branch. The user's own sessions SHALL be untouched.

#### Scenario: The plan cannot be read
- **WHEN** swb-1-conductor posts a question under `ask/swb-1-conductor/hold-the-macs` while the drive's state branch cannot be fetched
- **THEN** the call goes through: the hook reads no plan, and judges the key by its form alone

#### Scenario: crew's record of its cards cannot be read
- **WHEN** swb-1-conductor calls `cancel_request` for its card `req_q1` and the hook cannot read the drive's run record on this host
- **THEN** the call is refused, "crew could not check this card: <why>. Try it again later.", and nothing is closed

#### Scenario: The user's own session
- **WHEN** a session with no `CREW_AGENT` calls `post_request`
- **THEN** the hook does nothing, and the call goes through as Pending You ships it

#### Scenario: The agent's role cannot be read
- **WHEN** a crew session's `CREW_AGENT` names no role the teams file knows and the agent calls `post_request`
- **THEN** the call is refused, naming the agent and saying only a conductor, the planner, main-level ops and the design agent ask the user on a card, and nothing is posted

### Requirement: The landing card is posted once the bolt's verification is green
crew SHALL keep one landings card for each kit with a proven bolt waiting on its main, keyed `land/<kit>`, in the name of the drive's main-level ops, posted on the drive's main host. A bolt SHALL be a row that can land once every unit and chore of it has merged, every unit's latest change has been in a batch whose card the user has answered, its verification is green, its head the landing of its work as the runner reports it (merge-gate "A bolt's verification is its work's landing at its head, as the runner reports it"), and no fix of it is in flight. Rows SHALL be in the plan's order. The card SHALL ask only for the landing.

#### Scenario: A green bolt
- **WHEN** every unit and chore of bolt `y` of crew has merged, each unit's latest change has been in a batch the user has answered, `y`'s head `abc1234` is the landing of its last unit as the runner reports it, and no other bolt of crew can land
- **THEN** one card keyed `land/crew` is open in swancloud-ops's name, an approve of risk high, naming `y`, its units and chores and `abc1234` green

#### Scenario: Sluice's pull request
- **WHEN** sluice's submission at `y`'s head has pull request #23 on the kit's GitHub
- **THEN** `y`'s row links it, titled as sluice's pull request for `y`'s landing, on the card's face and in its details

#### Scenario: No pull request
- **WHEN** the kit's sluice opens no pull request for a submission
- **THEN** the row carries no link, and says nothing of one

#### Scenario: Two green bolts of one kit
- **WHEN** bolts `y` and `z` of crew both read proven, `y` first in the plan
- **THEN** one card keyed `land/crew` is open in swancloud-ops's name, its rows `y` then `z`, and no card is open under `land/y` or `land/z`

#### Scenario: Bolts of two kits
- **WHEN** bolt `y` of crew and bolt `w` of swancloud both read proven
- **THEN** `land/crew` holds `y`, `land/swancloud` holds `w`, and each is its own card

#### Scenario: A row carries what the bolt's card carried
- **WHEN** bolt `y` of swc-1, holding units `a` and `b` read in batch 7 and chore `c`, reads proven at `abc1234`, the landing of its work there made at 10:02, with pull request #23, main moved two landings since `y` was cut
- **THEN** `y`'s row names swc-1-conductor, `a`, `b` and `c (chore)`, batch 7, `abc1234` green since 10:02, two landings, pull request #23 linked, and `y`'s reading's link

#### Scenario: A second bolt is proven while the card waits
- **WHEN** `land/crew` waits on the user with one row, `y`, and bolt `z` of crew reads proven
- **THEN** the card becomes a list of `y` and `z`, posted following the one it replaces since a card's kind does not change in place, with a change note naming `z`

#### Scenario: A row's head moves while the card waits
- **WHEN** `land/crew` waits on the user as a list of `y` and `z`, and a fix's merge moves `z`'s head to `def5678`
- **THEN** the card is changed in place, its note saying `z`'s head is now `def5678`, and `z`'s row carries its reading of `def5678` and, where the kit's policy names a preview, `bolt/z` at `def5678` as what brings it up

#### Scenario: A yes frees the team for its next bolt
- **WHEN** swc-1's bolt `y` is a row of `land/crew`, and the last unit of swc-1's other bolt `z` merges with sluice green at its head, and `d` is the next planned bolt of swc-1's kit
- **THEN** `y`'s row says a yes frees swc-1 for `d`

#### Scenario: A fix in flight holds the card
- **WHEN** bolt `y` would read proven, but `fix/y/gap`, started on `y`, has neither merged nor been dropped
- **THEN** `y` has no box on `land/crew`, its row on the card's face says it is held for `fix/y/gap`, and it has a box again once the fix has merged and `y` reads proven

#### Scenario: A landing row before the bolt reads proven
- **WHEN** every unit of bolt `y` has merged and one unit's latest change has not been in a batch
- **THEN** the rail's landing row for crew names `y`, saying it lands once that unit has been in a batch, and `y` is no row of `land/crew`

#### Scenario: A landing row while a batch card waits on the user
- **WHEN** every unit of bolt `y` has merged, its verification is green, and batch 7, whose card the user has not answered, holds a unit's latest change
- **THEN** the rail's landing row for crew names `y`, saying it lands once you have answered batch 7, and `y` is no row of `land/crew` until the user has answered batch 7's card

#### Scenario: A defect noted on the card
- **WHEN** the user sends `land/crew` with a note naming a defect in `y`, and `y`'s conductor runs `crew fix` on `y` in the note's words
- **THEN** `y` loses its box and its row says "held for a fix: <the note>", and it has a box again once `y` reads proven again

### Requirement: The design agent posts a record's card under its record key
A record's card SHALL be raised by crew through `crew record <kit> <number> --proposed`, keyed `record/<kit>/<number>`, where `<kit>` is the name of a kit one of the drive's teams builds and `<number>` the record's four digits, in the design agent's name; the design agent SHALL post none itself, and no agent SHALL post under a record key. A kit that is not the drive's SHALL be refused naming the drive's kits.

#### Scenario: The design agent posts a record's card
- **WHEN** wldn-design runs `crew record atlas-kit 21 --proposed`, and atlas-kit is built by one of wldn's teams
- **THEN** one card keyed `record/atlas-kit/0021` is open in wldn-design's name, and the run record has a `card.post` entry on `record/atlas-kit/0021` with that key

#### Scenario: A kit outside the partition
- **WHEN** wldn-design runs `crew record flywheel-next 3 --proposed`, and no team of wldn builds flywheel-next
- **THEN** the command is refused, naming wldn's kits, and nothing is posted

#### Scenario: Another agent posts under a record key
- **WHEN** wldn-planner or a conductor calls `post_request` with a key `record/atlas-kit/0021`
- **THEN** the call is refused before it reaches Pending You, saying a record's card is crew's

#### Scenario: The design agent posts under any other key
- **WHEN** wldn-design calls `post_request` with the key `proposal/1`
- **THEN** the call is refused, saying a proposal's card is crew's; a key of its own for a question goes through

### Requirement: A row's card its owner's host can't reach is raised again there
A card belongs to the Pending You sign-in of the host it was posted from, and each row's card is raised and waited on only where its owner runs: a proposal's, a batch's, a deploy's, a step's and a kit's landings card on the drive's main level's host. When the owner's newest card under a row's key was posted from another host and no close ends it, or its last close is as lost to the owner on any host, and no newer card of the owner's is under the key, the rail's next read on the owner's host SHALL post the row's card again there under the row's key, through its kind's raise, its summary opening with the words that say an older copy was lost and to dismiss it in the app, while the row still waits on its card; and the rail SHALL take the new card as the row's. crew SHALL neither ask after nor close the older copy from a host whose sign-in does not reach it. A row that no longer waits SHALL have no card posted again, and the read SHALL say its raise posted none.

#### Scenario: The main level moved to another host
- **WHEN** batch 13's card was posted from mac-studio, the drive's main level now runs on deneb, the user has not answered the batch where crew can read it, and the rail is read on deneb
- **THEN** crew posts batch 13's card again on deneb under `batch/13` in the planner's name, its summary opening "An older copy of this card was lost: dismiss it in the app.", the rail shows the new card's id as the row's, and the read lists the older card as lost and the new one as posted

#### Scenario: A proposal's card left on the host the main level left
- **WHEN** proposal 13's card was posted from mac-studio in the planner's name, proposal 13 is still open, the main level now runs on deneb, and the rail is read on deneb
- **THEN** crew posts proposal 13's card again on deneb under `proposal/13`, in its form, its summary opening with the words that say an older copy was lost, and the rail shows the new card's id as the row's

#### Scenario: A deploy's and a step's card left behind
- **WHEN** `deploy/dev`'s card, or `op/dev/2`'s, was posted from mac-studio in main-level ops's name, the offer or the step still waits on the user among the operations recorded on deneb, and the rail is read on deneb
- **THEN** crew posts that card again on deneb in main-level ops's name, saying an older copy was lost

#### Scenario: A landings card left on the host the main level left
- **WHEN** `land/crew` was posted from mac-studio in swancloud-ops's name, the main level now runs on deneb, bolt `y` of crew still reads proven, and the rail is read on deneb
- **THEN** crew posts the landings card again on deneb under `land/crew`, with `y` as its row, saying an older copy was lost

#### Scenario: Lost to the planner on the host it was posted from
- **WHEN** batch 13's card was recorded lost to the planner on mac-studio, no card was posted under `batch/13` since, and the rail is read on deneb, the main level's host
- **THEN** crew posts batch 13's card on deneb, its summary saying an older copy was lost

#### Scenario: Read on another host
- **WHEN** the rail is read on a host where the row's owner does not run while its card is held on mac-studio
- **THEN** that read posts no card for the row

#### Scenario: The batch no longer waits
- **WHEN** batch 13's card is held on mac-studio and every unit batch 13 holds has landed
- **THEN** no card of batch 13 is posted on deneb

#### Scenario: The proposal no longer waits
- **WHEN** proposal 13's card is held on mac-studio and proposal 13 was approved since
- **THEN** no card of proposal 13 is posted on deneb

### Requirement: A bolt's own landing card gives way to its kit's
An open landing card under `land/<bolt>`, in a conductor's name, SHALL be withdrawn by the rail's sweep on the team's host, saying the bolt is now a row of its kit's landings card, and that card SHALL be raised for the bolt. crew SHALL raise no card under `land/<bolt>`. A bolt SHALL NOT be added to the plan under a name that is a kit's of its drive.

#### Scenario: A card from before
- **WHEN** swc-1-conductor holds an open card under `land/y`, raised before this change, and the rail is read on swc-1's host
- **THEN** that card is withdrawn saying `y` is now a row of crew's landings card, and `land/crew` holds `y`

#### Scenario: A bolt named as a kit
- **WHEN** a proposal adds a bolt named `crew` to swancloud's plan, whose teams build the kit crew
- **THEN** its approval is refused, naming the kit, and nothing is written

### Requirement: A card whose role left the fleet is withdrawn
On each rail read crew SHALL withdraw, in its owner's name, each open card of its own six posted on that host whose owner is `<label>-planner`, `<label>-ops` or `<label>-design` for a label no drive of the teams file has now, saying the owner left the fleet and how whoever holds the work now raises it again. The close SHALL be recorded, withdrawn, and the rail SHALL no longer show the card. Any other card SHALL keep the paths it has.

#### Scenario: A partition's label changed under an open deploy card
- **WHEN** the teams file labels the drive `wldn`, and its run record holds `deploy/dev`'s card posted on this host in `willdan-ops`'s name and open while the offer waits
- **THEN** the rail's read withdraws the card in `willdan-ops`'s name with "willdan-ops left the fleet, so an answer here reaches nobody. The deploy is offered again in the name of the ops of the drive that holds dev now.", records the close withdrawn with those words, and lists it among the cards it withdrew

#### Scenario: The partition stays
- **WHEN** the teams file labels the drive `wldn` and `deploy/dev`'s card is open in `wldn-ops`'s name while the offer waits
- **THEN** the rail's read leaves the card open and posts no other

#### Scenario: A deploy whose word stands
- **WHEN** `deploy/dev`'s card is open in `willdan-ops`'s name and the user's word on the deploy is recorded
- **THEN** the card is withdrawn with "willdan-ops left the fleet, so an answer here reaches nobody. Your word on dev's deploy stands, and the deploy goes on."

#### Scenario: A record's card in a former design agent's name
- **WHEN** `record/atlas-kit/0021`'s card is open in `willdan-design`'s name
- **THEN** it is withdrawn, saying "Record 0021 of atlas-kit is carded again with crew record by the design agent of the drive that holds it now."

#### Scenario: A question and a conductor's card are no partition role's
- **WHEN** a question card is open in `willdan-planner`'s name, and `land/y`'s card in `swb-1-conductor`'s
- **THEN** the sweep judges neither as a role that left the fleet: the question is judged by its asker's pane and the landing card by its row

### Requirement: A card in a former name cards no row
A card whose owner left the fleet SHALL card no row. A row whose only open card is such a card SHALL be posted through its kind's raise in its owner's name, as a row with no card open is. crew SHALL map no former name onto a new one, carry no card across, and take no drive as another's successor.

#### Scenario: The deploy row is carded in the standing ops's name
- **WHEN** `deploy/dev`'s card is open in `willdan-ops`'s name, the offer of dev's deploy still waits, and the teams file labels the drive `wldn`
- **THEN** the rail's read posts `deploy/dev`'s card through its raise in `wldn-ops`'s name, following no card
