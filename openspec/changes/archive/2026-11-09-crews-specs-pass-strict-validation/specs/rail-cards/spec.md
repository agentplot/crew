## ADDED Requirements

### Requirement: Each rail row has a card key for its thing, not its version
Each rail row SHALL have one card key, the thing's and not its version's: `proposal/<n>` for a proposal chain, `n` its first proposal; `batch/<n>` for review batch n; `land/<bolt>` for a bolt proven; `deploy/<env>` for a `manual` environment's open offer; `op/<env>/<n>` for a step that waits on the user; `record/<kit>/<number>` for a record proposed. A question's card has no row and a key of its asker's own. There SHALL be no review row and no verify row.

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

### Requirement: A row's card is posted under its key, filled out to eight characters
crew SHALL post the row's card with its card key as its idempotency key, filled out at its end with `_` to Pending You's eight characters when it is shorter, the same on every post of it, and SHALL record the post under the row's key.

#### Scenario: A key shorter than Pending You takes
- **WHEN** crew raises review batch 7's card, `batch/7` being seven characters, and raises it again after its first post had no answer within a minute
- **THEN** both posts are under `batch/7_`, so Pending You gives the second the card the first made, and the run record holds it under `batch/7`

### Requirement: A batch's row lasts until its card closes or it waits on nothing
A batch's row SHALL last until its card closes or the batch waits on nothing (`review-batches`). A batch whose cards were posted under `batch/<n>-<k>` before one card per batch was built SHALL keep a row for each of those keys until its card closes or the units it holds wait on nothing, and SHALL have no `batch/<n>` row.

#### Scenario: A batch of seven
- **WHEN** review batch 3 holds seven changes and no card has been posted for it
- **THEN** the rail has one batch row for it, keyed `batch/3`, holding all seven units

#### Scenario: A batch posted as two cards before
- **WHEN** the run record holds the planner's posts of batch 2's cards under `batch/2-1` and `batch/2-2` from before one card per batch, and `batch/2-1` has closed
- **THEN** the rail has one row for batch 2, keyed `batch/2-2`, holding its units as before, until its card closes

#### Scenario: An old batch card whose units have landed
- **WHEN** batch 2's cards were posted under `batch/2-1` and `batch/2-2`, neither has closed, and every unit `batch/2-2` holds has landed while one unit of `batch/2-1` has not
- **THEN** the rail has one row for batch 2, keyed `batch/2-1`, and the sweep withdraws `batch/2-2`'s card, saying its units have landed

### Requirement: A card is asked in the name of the role whose row it is
crew SHALL ask each card in the name of the role whose row it is, with the host as the session's machine and the kit's checkout as its folder; a question's card SHALL be asked in its asker's crew name by the asker's session. A card's title SHALL be the question, read cold, naming the thing.

#### Scenario: A review card
- **WHEN** a unit's change is due for a batch
- **THEN** no review card is asked for it; the batch's card, asked in the planner's name, names the unit and its team

#### Scenario: A landing card
- **WHEN** crew raises bolt `y`'s landing card for swb-1's team in switchboard-kit
- **THEN** the card is asked as `swb-1-conductor` on the team's host, sits in switchboard-kit's area in the `wldn` group, and its title asks whether to land bolt `y` on the kit's main

### Requirement: A card is filed in its kit's area, in its drive's group
A card SHALL be filed in the area of its kit, found by the kit's git remote, in the group named for its drive; crew SHALL create a kit's area that does not exist with the key `create-area:<owner>/<kit>`, and an agent SHALL create one under no other key and never a group.

#### Scenario: The first card in a kit
- **WHEN** crew raises the first card in switchboard-kit and Pending You matches no area to its remote
- **THEN** crew makes the area under `create-area:WilldanGroup/switchboard-kit`, named `switchboard-kit`, in the drive's group, and files the card there

### Requirement: A landings card of one row is approved only by holding the button
A kit's landings card SHALL never be landed from a key in Herdr's popup. With one row, a bolt that can land, it SHALL be an `approve` of risk high, not reversible, approved by holding the button in the Pending You app, and SHALL NOT carry the `highStakes` flag, which Pending You refuses on an approval.

#### Scenario: Landing from the popup
- **WHEN** the user presses the approve key on a landings card of one row in Herdr's popup
- **THEN** Pending You refuses it as high risk, and the bolt does not land

### Requirement: A landings card of two or more rows is a list carrying highStakes
With two or more rows, those that can land and those beside them taking main first, a kit's landings card SHALL be a list of boxes carrying `highStakes`, which Pending You takes on a list as the same test as risk high.

#### Scenario: A list of three bolts
- **WHEN** crew raises `land/crew` with three rows that can land
- **THEN** the card is one list of three boxes with `highStakes` set, and no `approve` block

#### Scenario: One that can land beside one taking main first
- **WHEN** crew raises `land/crew` with `y`, which can land, and `z`, which takes main first
- **THEN** the card is one list of two boxes with `highStakes` set, `y` ticked and `z` unticked

### Requirement: An answer on a crew card is acted on by its row's role alone
An answer on a crew card SHALL be acted on by the role whose row it is, woken in its session by the card it adopted, and by no other: the planner applies or rewrites the proposal, and reads a batch's answer with `crew card read batch/<n>`; main-level ops passes a note on a kit's landings card naming a defect in a bolt to that bolt's conductor, who starts a fix on it; main-level ops runs the deploy's approval or the step's state; the design agent sets the record's status.

#### Scenario: A proposal approved from the phone
- **WHEN** the user approves the card for proposal 4 on the phone
- **THEN** the planner is woken, runs `crew plan answer` and `crew plan approve 4`, which closes the card with what was applied, and the rail's proposal row is gone

#### Scenario: Changes asked for on a review card
- **WHEN** the user writes a note on a batch's card asking for changes to unit `x`
- **THEN** the planner is woken, `crew card read batch/<n>` prints the note and closes the card, the conductor runs construct again with its words, and no approval is asked

#### Scenario: A defect noted on a row
- **WHEN** the user's note on `land/crew` names a defect in bolt `b`
- **THEN** swancloud-ops tells `b`'s conductor the note's words, the conductor starts a fix on `b`, and `b`'s row is held for the fix

### Requirement: No role lands what the user ticked, and no process of crew's waits on an answer
No role SHALL land the bolts and fixes of main the user ticked on a kit's landings card: crew's own raise of the card posts their lands, as "The user's send on a kit's landings card posts one land for each row it lands" has it. crew SHALL then close the card at that act's event. No process of crew's SHALL wait on a card's answer.

#### Scenario: Landing approved
- **WHEN** the user leaves `a` and `c` ticked on `land/crew`, clears `b`, and sends
- **THEN** crew's next raise of `land/crew` posts a land of `a` and then one of `c`, `crew card read land/crew` prints them with their requests and no command, and no agent is asked to land or pass anything on

### Requirement: A role running as its kind is asked to act on its card's answer
Where the role runs as its kind, the host's follower SHALL write an ask of the role for each change Pending You's notice names on a card in the role's name, once per version of the card, reading nothing of the card, and the role's next run SHALL read the card in the role's own name and act on it as the woken session would.

#### Scenario: A proposal approved while the planner runs as its kind
- **WHEN** madswan's planner runs as its kind, no run of it is live, and the user approves proposal 12's card on the phone
- **THEN** the host's follower, told by Pending You's notice, writes one ask of the planner naming the card's request, and the planner's next run reads the card in madswan-planner's name and runs `crew plan answer` and `crew plan approve 12`

### Requirement: An agent adopts crew's card by get_request and runs no pendingyou command
An agent crew started SHALL adopt a card crew posted by calling Pending You's `get_request` with the card's id under its own name, as the line crew prints or tells it says, from which the fleet's wake mod adopts the card and wakes the agent's session once the card is answered and the session is idle; it SHALL run no `pendingyou` command, `hold` and `watch` among them, none through `npx`, and wait on no hold.

#### Scenario: A brief that asks the user forbids Pending You from npm
- **WHEN** the planner's, main-level ops's or the design agent's brief is printed for wldn
- **THEN** it says never to run `npx pendingyou` or `pendingyou hold`

### Requirement: An agent adopts its open cards from the rail after a fresh start
After a fresh start an agent crew started SHALL read `crew rail` for its open cards and adopt each by calling Pending You's `get_request` with the card's id under its own name.

#### Scenario: Restarted with an answered card
- **WHEN** a conductor restarts while the user has answered its landing card
- **THEN** at its start `crew rail` names the card and its id, the conductor adopts it and acts on the answer

### Requirement: Each card act is an entry in the run record naming its card and key
Each card crew posts, changes, withdraws or closes, each answer of the user's on one of them that crew reads, and each card a crew agent posts, changes or closes through Pending You's tools, SHALL be an entry in the drive's run record naming the row's object or the asker, the card's id in `Card` and the key in `Key`, crew's read from Pending You's own reply, an agent's from the tool's result. An entry SHALL NOT hold a card's title, summary or other text.

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

### Requirement: An agent's card act whose result names no card is recorded unread
An agent's act whose result names no card SHALL be recorded on the agent with `State: unread`, and `crew rail` SHALL list each such act of the last 14 days with its agent, its act and its time.

#### Scenario: A question whose reply names no card
- **WHEN** swb-1-conductor's `post_request` under `ask/swb-1-conductor/hold-the-macs` returns a result that names no card
- **THEN** the run record has a `card.post` entry on swb-1-conductor with that key and `State: unread`, and `crew rail` lists it with swb-1-conductor, the act and its time

### Requirement: The rail prints each row's card under it and the open questions after
`crew rail` SHALL print, under each row, the row's card key, whether a card with that key is open, its id and whose it is, and whether the user has answered it, and after the groups the open question cards, each with its key, which names it, its asker and its age, and the open record cards apart.

#### Scenario: A row with its card
- **WHEN** bolt `y` reads proven and crew's card `req_l1` under `land/y` is open
- **THEN** the row's card line names `land/y` as open, `req_l1`, the conductor's

#### Scenario: A row without a card
- **WHEN** a proposal is open and its card's post was refused
- **THEN** the row's card line names `proposal/<n>` with no card open and the refusal's words

#### Scenario: A row with its card and a question open
- **WHEN** `proposal/4`'s card `req_p4` is open and swb-1-conductor's question `req_q1` is open
- **THEN** the proposal row's card line names `proposal/4`, open, `req_p4`, the planner's; and after the groups `req_q1` is listed with its key, swb-1-conductor and its age

#### Scenario: A row's card the user answered
- **WHEN** `land/crew`'s card `req_l2` is open and the run record holds the user's answer on it
- **THEN** the row's card line names `land/crew`, `req_l2`, answered, with when and what, and whose act it waits on

### Requirement: A row's card is the one open in its owner's name, others named apart
A card is open from its `card.post` entry until a `card.close` entry for the same card, or until a later `card.post` under the same key names another card, which is then the row's card while the older is taken as lost. A row's card is the one open in the row owner's name; another card open under its key, in another name, SHALL be named apart on the row as a copy that is not the row's, with whose it is.

#### Scenario: A card posted again under its row's key
- **WHEN** crew's card `req_1` under `proposal/17` read not found after the host signed in again, and the rail read posted `req_2` under `proposal/17`
- **THEN** the row's card line names `req_2` as its open card, and `req_1` is listed as lost

#### Scenario: Two cards open under one row's key
- **WHEN** afterthought's `proposal/508` row is the planner's, afterthought-planner's card `req_51` is open under it, and swancloud-planner's card `req_69` is open under it too
- **THEN** the row's card line names `req_51`, afterthought-planner's, as its card, and the row names `req_69` apart, swancloud-planner's, as a copy that is not the row's

### Requirement: A card's words are prose the phone wraps, in the document's own words
A crew card's words SHALL be prose the phone wraps, in short paragraphs, cut at whole sentences to Pending You's budget, with nothing the user has to read as raw Markdown; where a card speaks for a document, a proposal's case, a unit's opening paragraph, a record's opening sentences, it SHALL use the document's own words, never reworded.

#### Scenario: A review card
- **WHEN** unit `x`'s change is read in batch 3
- **THEN** the batch's card carries `x`'s reviewer paragraph in the reviewer's words, and no card carries `x`'s Why alone

#### Scenario: A verify card
- **WHEN** a unit's verify saves a report that raised two warnings
- **THEN** no card carries it: a verify report waits on no one, and its findings are fixed in one round

#### Scenario: A change too long for the summary
- **WHEN** a batch's paragraphs run past what the summary holds
- **THEN** the summary ends at the last whole sentence that fits, and the background holds every paragraph

#### Scenario: A proposal card
- **WHEN** crew raises the card for proposal 4
- **THEN** its title, summary, background, questions and artifacts are built from the plan and the proposal, the case and each change in the proposal's words

#### Scenario: A batch card's summary
- **WHEN** crew raises batch 7's card for four units
- **THEN** each unit's paragraph is the reviewer's opening paragraph as prose in its summary and details, with no code block in its words, the reviewer's summary rides its face as inline Markdown, and the card wraps on the phone

### Requirement: A list the user scans is an artifact on the card's face
A list the user scans, the units that land, a deploy's steps, a proposal's change, SHALL be an artifact on the card's face, one thing a line and no line over forty characters, never a comma run in the summary or the background; the background SHALL hold only what is read when the face is not enough. A path SHALL appear only inside a step's command or a deploy's log name.

#### Scenario: Six units on a landing card
- **WHEN** crew raises the landing card of a bolt of six units
- **THEN** the six names are a text artifact on the face, one a line, and the background names none of them

#### Scenario: A card follows the card its thing follows
- **WHEN** crew raises the card of srv's first step for the user after swancloud-ops's deploy card for srv
- **THEN** the step's card follows that deploy card, and the phone shows it in that card's thread

### Requirement: Each kit has one landings card in main-level ops's name, its rows in plan order
crew SHALL keep one landings card for each kit with a proven bolt waiting on its main, keyed `land/<kit>`, in the name of the drive's main-level ops, posted on the drive's main host. Rows SHALL be in the plan's order. The card SHALL ask only for the landing.

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
- **THEN** the card is changed in place, its note saying `z`'s head is now `def5678`, and `z`'s row carries its reading of `def5678` and `bolt/z` at `def5678` as what brings its preview up

#### Scenario: A yes frees the team for its next bolt
- **WHEN** swc-1's bolt `y` is a row of `land/crew`, and the last unit of swc-1's other bolt `z` merges with sluice green at its head, and `d` is the next planned bolt of swc-1's kit
- **THEN** `y`'s row says a yes frees swc-1 for `d`

### Requirement: A bolt is a row that can land once its work is merged, read and verified
A bolt SHALL be a row that can land once every unit and chore of it has merged, every unit's latest change has been in a batch whose card the user has answered, its verification is green, its head the landing of its work as the runner reports it (merge-gate "A bolt's verification is its work's landing at its head, as the runner reports it alone"), and no fix of it is in flight.

#### Scenario: A green bolt
- **WHEN** every unit and chore of bolt `y` of crew has merged, each unit's latest change has been in a batch the user has answered, `y`'s head `abc1234` is the landing of its last unit as the runner reports it, and no other bolt of crew can land
- **THEN** one card keyed `land/crew` is open in swancloud-ops's name, an approve of risk high, naming `y`, its units and chores and `abc1234` green

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

### Requirement: A batch's card is a notice that asks nothing, the reviewer's summary on its face
A batch's card, keyed `batch/<n>`, SHALL be a Pending You notice (`fyi`) crew raises when the reviewer delivers the batch's summary, that asks nothing: no options, no question, no approval and no steps. The reviewer's summary SHALL ride the face as inline Markdown, a paragraph per unit under its name and team.

#### Scenario: A card of six units
- **WHEN** crew raises the card for batch 2 holding six units
- **THEN** the card is one `fyi` titled with batch 2, whose summary opens "6 changes to read, nothing to approve", whose words say the units go on building, whose face and background name all six units with their teams and paragraphs, and whose one link opens the batch's session

### Requirement: A batch's card's title and words say what it is about and where notes go
A batch's card's title SHALL say what the batch is about, drawn from its units' subjects, with the batch's number after; its summary SHALL say first "N changes to read, nothing to approve", since the batch before it when there is one; its words SHALL say where notes go, the reading session or the card's own note, that each reaches its unit's team as the user's words, and that the units go on building whatever the user does with the card.

#### Scenario: A batch's title and the opening of its summary
- **WHEN** crew builds batch 7's card for four units, batch 6 the batch before it
- **THEN** its title says what the four units are about, with "(batch 7)" after, and its summary opens "4 changes to read, nothing to approve, since batch 6."

### Requirement: A card carries a document's substance as inline Markdown, never a file
A document's substance shown on a crew card beyond its words SHALL be inline Markdown, an artifact of kind `code` with lang `markdown` and the text as its lines, never an uploaded file or HTML: a record's card carries the record whole so, a proposal's its new units' paragraphs, a batch's the reviewer's summary, a deploy's the kit's release notes.

#### Scenario: A document's substance on a card
- **WHEN** crew raises record 32's card
- **THEN** its one artifact is the record as Markdown, its lines the record's text, and no file is attached

### Requirement: A crew card carries only a picture, Markdown, text lists, links and steps
The only artifacts a crew card carries SHALL be an uploaded picture, inline Markdown, a list as text (a landing's units, a deploy's steps, a proposal's change), a link as a `url` artifact (sluice's pull request, a batch's reading), and a step's commands as action steps.

#### Scenario: A card with nothing to show
- **WHEN** crew raises a landing card
- **THEN** its artifacts are the units that land as text and, when sluice opened one, the pull request's link, and it carries no reading session

### Requirement: A record's card is an approval of risk low carrying the record whole
A record's card SHALL be an `approve` of risk low, reversible, with no options and no steps, titled "Accept record <number> in <kit>: <title>", its summary the record's opening sentences, its background the record's decision and, when the record quotes the user's words from the design talk, "Your own words, recorded as your decision:" and the quote, and one artifact, the record whole as Markdown; it SHALL link no reading session.

#### Scenario: A record card marked high risk
- **WHEN** crew raises record 21's card with no alternatives file
- **THEN** it is an approval of risk low, reversible true, with the record's opening sentences and the Markdown, and no options

### Requirement: A record a rule decided between alternatives is carded as a choice
When the design agent runs `crew record … --proposed --alternatives <file>`, because a rule of the user's decided the record between alternatives, the record's card SHALL be, instead of an approval, a choice asked once: loosen the rules as drafted and take the other path, accept the record as ruled, or send it back with a note. crew builds both, so no other form arises.

#### Scenario: A record card as a choice
- **WHEN** the design agent runs `crew record switchboard-kit 32 --proposed --alternatives alternatives.md`, the file naming two ways, `ops.3` and `ops.7` as the rules that chose, and each loosened
- **THEN** the card is a choice of loosen, as ruled, or send back, with the file's Markdown on its face before the record, and the user's answer reaches the design agent as the record's status

### Requirement: A record's choice carries its alternatives before the record and recommends the user's own path
The choice's face SHALL carry the alternatives file as inline Markdown, the alternatives, the rules that decided and each rule as it would read loosened, before the record whole, and the recommended option SHALL be the one the user's own quoted words point to, else accepting as ruled.

#### Scenario: An alternatives file crew cannot read
- **WHEN** `--alternatives` names a file that is not there
- **THEN** the command refuses, naming the file, and raises nothing

### Requirement: crew changes its card in place while it waits on the user
When crew changes one of its own cards because its thing changed, it SHALL change the card in place while the card waits on the user.

#### Scenario: A card waiting on the user
- **WHEN** crew changes its card `req_1` under `land/b1`, which waits on the user
- **THEN** `req_1` is changed in place with the change note

### Requirement: An answered card is acked with the change note and followed by a new card
Once the user has answered a card crew changes, which Pending You no longer changes, crew SHALL ack it with the change note as its outcome and post the new version as a new card that follows it, in the same owner's name, saying first that the user answered the earlier card, when and with what, and what changed since, as every card that follows one the user answered says it. The run record SHALL hold the answered card's close, with the answer, and the new card's post, both under the row's key.

#### Scenario: A card the user answered
- **WHEN** crew changes its card `req_1` under `land/b1` after the user has answered it
- **THEN** `req_1` is acked with the change note, and a new card following `req_1` is posted, its summary opening with what the user answered on `req_1` and what changed. The run record has `req_1`'s close, with the answer, and the new card's post under `land/b1`, and `crew card read land/b1` finds the new card

### Requirement: A card posted under a key whose last card closed takes the key's revision
Every card crew posts under a row's key after a card of the owner's under that key has closed SHALL take the key with its revision, `<key>:<n>`, as its idempotency key, so Pending You never gives the closed card back.

#### Scenario: A card raised again after its last card closed
- **WHEN** crew raises b1's landing card after the user declined the last one under `land/b1`, or follows an answered one with its new version
- **THEN** it is posted under `land/b1:2` as a new card

### Requirement: A card still open under its key keeps its key and is recorded once
A card still open under a row's key SHALL keep its own key, so posting it again gives it back, and the run record SHALL hold one post of it: a post Pending You answers with the card this host's record already holds open under the key and owner is that card, printed with the line that adopts it and recorded no second time.

#### Scenario: A card posted again while it is open
- **WHEN** crew posts its card under `land/b1` again while `req_1` is open there
- **THEN** it is posted under the key its first post took, `land/b1_`, and Pending You gives `req_1` back

#### Scenario: Two rail reads raise a row's card at once
- **WHEN** two rail reads on mac-studio, from two agents' starts, sweep at once, each posts `op/srv/1`'s card, and Pending You gives both `req_1`
- **THEN** the run record holds one `card.post` of `req_1` under `op/srv/1`, written by the read that recorded it first, and the other read prints `req_1` and `call get_request (requestId req_1, name <role>)`

### Requirement: A user's step is a do card, and an agent's own step has none
A step whose doer is the user SHALL be a `do` card with the step's words, where it is done, each command whole as an action step, what is seen when it worked, and the options Done, Skip and Later. A step an agent runs on its own SHALL have no card.

#### Scenario: A password only the user can rotate
- **WHEN** the deployer records a step with doer user and two commands
- **THEN** the card keyed `op/srv/1` is a `do` with both commands whole, where to run them, when it is done, and Done, Skip and Later

#### Scenario: A step an agent runs on its own
- **WHEN** the deployer records a step with doer main-ops, when quiet, not held
- **THEN** no card is raised, and the step runs at the quiet moment

### Requirement: A deploy's steps for the user are carded one at a time
When a deploy ends with more than one step for a card, crew SHALL raise one card at a time: the first following the deploy's card, each next one following the one before, raised when crew closes it. Only another step's open card SHALL hold a step's card back: a step recorded again while its own card is open changes that card, as a row's card changes when its thing changes.

#### Scenario: Two steps after one deploy
- **WHEN** srv's deploy ends with a step that is the user's and a step held for the user's word
- **THEN** one card is open, following the deploy's card, and the second is raised following the first when the first is closed

### Requirement: A row's card is changed in place with a note the user sees
When what a row's card asks changes while it is open, crew SHALL change the one card in place with a change note the user sees, and SHALL post no second card under a new key. A proposal chain's card SHALL be the first proposal's, and the rail's row for the replacing proposal SHALL carry it.

#### Scenario: A proposal rewritten while its card waits
- **WHEN** proposal 4's card, its rows in one list, is open and unanswered, and the planner runs `crew plan propose <file> --replaces 4` and proposal 5 is accepted
- **THEN** the card keyed `proposal/4` is changed in place to proposal 5's, with the change note "Rewritten as proposal 5 after your note", and the rail's row for proposal 5 names it as its card

#### Scenario: A merge moves a bolt with an open landing card
- **WHEN** the landing card `land/y` is open and unanswered, and a merge into bolt `y` moves its head to `def5678`
- **THEN** crew changes the card in place, "Its head is now def5678", and posts no second card

#### Scenario: A newer head offered
- **WHEN** `deploy/srv`'s card is open for `abc1234` and the deployer offers `def5678`
- **THEN** the same card is changed to `def5678`, with the change note "Now offering def5678, which includes abc1234"

#### Scenario: A conductor agrees
- **WHEN** `proposal/4`'s card says it waits on crw-2's conductor and that conductor runs `crew plan agree 4`
- **THEN** the card is changed in place, "No longer waits on crw-2-conductor"

#### Scenario: A step recorded again with new words
- **WHEN** `op/srv/1`'s card is open, raised from the deployer's text for its step, and main-level ops records that step again waiting on the user with new words
- **THEN** the same card is changed in place, "Recorded again: its words changed", and the command prints its id and `call get_request (requestId <id>, name <role>)`; recorded again with the words the card shows, the card is not changed and the command prints the same line

### Requirement: A card that asks questions is withdrawn and followed, never changed in place
A card that asks questions, a proposal's whose rows fill more than one list, SHALL never be changed in place, since Pending You's `update_request` changes no card's questions: while it waits crew SHALL withdraw it with the change note and post its new version following it, under the key's next revision.

#### Scenario: A proposal whose rows fill more than one list rewritten while its card waits
- **WHEN** proposal 4's card asks its seven rows as `rows-1` and `rows-2`, is open and unanswered, and the planner runs `crew plan propose <file> --replaces 4` and proposal 5 is accepted
- **THEN** the card is withdrawn, "Rewritten as proposal 5 after your note", and proposal 5's card, asking proposal 5's rows, is posted under `proposal/4:2` following it, since Pending You changes no card's questions in place; the rail's row for proposal 5 names the new card

### Requirement: A card whose form changes is withdrawn and followed
A rewrite that moves a proposal's card to another form, a hold-to-approve, a choice, one list or lists, read from the replaced proposal's commands, SHALL be followed the same way as a card that asks questions, since Pending You changes no card's kind in place.

#### Scenario: A rewrite that moves a proposal's card to another form while it waits
- **WHEN** proposal 4's card asks its seven rows as `rows-1` and `rows-2`, is open and unanswered, and proposal 5, which replaces it, has three rows, one list
- **THEN** the card is withdrawn, "Rewritten as proposal 5 after your note", and proposal 5's one list is posted under `proposal/4:2` following it; so is a hold-to-approve rewritten to a list, or a list to lists

#### Scenario: A step's card that changes in kind
- **WHEN** `op/srv/1`'s card, the user's `do`, is open and its step is recorded again with main-level ops its doer, held for the user's word
- **THEN** the card is withdrawn, "Recorded again: its doer and its hold changed", and the step's choice is posted under `op/srv/1:2` following it, since Pending You changes no card's kind in place

### Requirement: A preview refused or not there yet is said on its row and holds nothing
A preview the runner refuses, in its own words or in sluice's as it carried them, or one crew cannot ask for or cannot read in the runner's report, SHALL be said on its row or line with that reason, the card changed in place while it waits on the user. A preview the runner has not answered yet, or has answered held, SHALL be said as asked and not there yet, naming the host whose runner brings it up. No preview refused, not there yet, failed or no longer listed SHALL hold the landing.

#### Scenario: The runner refuses the preview
- **WHEN** swancloud-ops has run `crew card preview land/crew y`, writing request 12, and deneb's runner, where `y`'s work runs, answers request 12 refused with the words `its Act preview, which crew's implementation does not read`
- **THEN** at the rail's next read on the drive's main machine `land/crew` is changed in place, `y`'s row saying its preview could not be brought up, in the runner's words, listing no addresses, and `y` keeps its box

#### Scenario: The host's sluice has no preview command
- **WHEN** deneb's runner runs a sluice that refuses `sluice preview`, and answers request 12 refused, carrying sluice's words
- **THEN** `land/crew` is changed in place, `y`'s row saying its preview could not be brought up, in sluice's words, listing no addresses, and `y` keeps its box

#### Scenario: A kit that declares no preview
- **WHEN** deneb's runner answers request 12 refused with sluice's words that the kit's policy at `y`'s head declares no preview
- **THEN** `y`'s row says its preview could not be brought up, in sluice's words, and `y` keeps its box

#### Scenario: A line naming a branch sluice does not land
- **WHEN** the planner has run `crew card preview batch/7 a/demo` for a line naming `unit/a` at `abc1234`, and the runner answers it refused with sluice's words that no `[branches]` table names `unit/a`
- **THEN** batch 7's card is changed in place, saying under `a` that `demo` could not be brought up, in sluice's words

#### Scenario: Not answered yet
- **WHEN** request 12 is written and deneb's runner has not answered it
- **THEN** `y`'s row says its preview of `abc1234` is asked of the runner on deneb and is not there yet, and that nothing waits on it

### Requirement: A card changes in place when its preview fails, goes or comes up
A preview whose addresses were listed and that sluice's listing, as the runner carried it, then shows failed SHALL change the card in place to say it did not come up, its addresses no longer listed; one sluice no longer lists SHALL change the card in place to say so; one that comes up after the card said it was not there yet SHALL change the card in place to list its addresses. A card the user has answered SHALL be left as it is.

#### Scenario: The stack fails to come up
- **WHEN** `y`'s row lists a preview's addresses and deneb's runner then carries sluice's listing of it as failed
- **THEN** the card is changed in place with a note that `y`'s preview did not come up, the row says so and lists no addresses, and `y` keeps its box

#### Scenario: The host is busy when the card is raised
- **WHEN** deneb's runner answers request 12 held, and at a later pass answers it done with sluice's listing of it up
- **THEN** the row says its preview waits for room on deneb, and the card is then changed in place with a note that `y`'s preview is up, listing its addresses

#### Scenario: A preview sluice no longer lists
- **WHEN** `y`'s row lists a preview's addresses and deneb's runner then carries it as no longer listed by sluice
- **THEN** the card is changed in place with a note that `y`'s preview is gone, the row saying sluice on deneb no longer lists it and listing no addresses

### Requirement: A card belongs to its host's sign-in and is asked after only from there
A card belongs to the Pending You sign-in of the host it was posted from, and each row's card is raised and waited on only where its owner runs: a proposal's, a batch's, a deploy's, a step's and a kit's landings card on the drive's main level's host. crew SHALL neither ask after nor close the older copy from a host whose sign-in does not reach it.

#### Scenario: Read on another host
- **WHEN** the rail is read on a host where the row's owner does not run while its card is held on mac-studio
- **THEN** that read posts no card for the row

### Requirement: A row's card held on another host is posted again on its owner's host
When the owner's newest card under a row's key was posted from another host and no close ends it, or its last close is as lost to the owner on any host, and no newer card of the owner's is under the key, the rail's next read on the owner's host SHALL post the row's card again there under the row's key, through its kind's raise, its summary opening with the words that say an older copy was lost and to dismiss it in the app, while the row still waits on its card.

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

### Requirement: The rail takes a card posted again as the row's, and posts none for a row that no longer waits
The rail SHALL take the new card posted again on the owner's host as the row's. A row that no longer waits SHALL have no card posted again, and the rail's read SHALL say its raise posted none.

#### Scenario: The batch no longer waits
- **WHEN** batch 13's card is held on mac-studio and every unit batch 13 holds has landed
- **THEN** no card of batch 13 is posted on deneb

#### Scenario: The proposal no longer waits
- **WHEN** proposal 13's card is held on mac-studio and proposal 13 was approved since
- **THEN** no card of proposal 13 is posted on deneb

### Requirement: A stranded record's card is posted again on the main level's host while it is proposed
When the design agent's newest card under a record's key was posted from another host and no close ends it, or was lost to it on any host, no newer card of the design agent's is under the key, and the record's last status crew recorded is proposed and not settled in the pane, the rail's next read on the main level's host SHALL post the record's card again there under `record/<kit>/<number>`.

#### Scenario: A record settled since
- **WHEN** record 21's card is held on mac-studio and `crew record atlas-kit 21 --accepted` was recorded since
- **THEN** no card of record 21 is posted on deneb

### Requirement: A record's card posted again is built from the record on the kit's main
A decision record's card has no rail row and is raised in the design agent's name on the main level's host. The record's card posted again SHALL be built from the record as the kit's main holds it, its summary opening with the words that say an older copy was lost.

#### Scenario: A record's card left on the host the main level left
- **WHEN** record 21 in atlas-kit was raised from mac-studio with no alternatives, is still proposed, the main level now runs on deneb, and the rail is read on deneb
- **THEN** crew posts record 21's card again on deneb under `record/atlas-kit/0021` in wldn-design's name, built from the record on atlas-kit's main, its summary opening with the words that say an older copy was lost, and the rail lists the new card under the decision records

### Requirement: A record's status records whether its card offered alternatives
`crew record --proposed` SHALL record on its `record.proposed` entry whether the card it raised offered alternatives, keeping none of the file's words.

#### Scenario: A record's status says its card offered alternatives
- **WHEN** the design agent runs `crew record switchboard-kit 33 --proposed --alternatives alternatives.md`, after record 32 was proposed with no alternatives file
- **THEN** record 33's `record.proposed` entry records that its card offered alternatives, and record 32's records none

### Requirement: A stranded record card with alternatives is raised again only by its command
A stranded record card raised with alternatives SHALL NOT be posted again by the rail's read, since crew keeps no copy of the alternatives file: the read SHALL say so, naming `crew record <kit> <number> --proposed --alternatives <file>` for the design agent; and `crew record --proposed`, run while its record's card is stranded so, SHALL post the card saying an older copy was lost.

#### Scenario: A record raised with alternatives
- **WHEN** record 32's card was raised from mac-studio with `--alternatives`, the main level now runs on deneb, and the rail is read on deneb
- **THEN** no card is posted, and the read names `crew record switchboard-kit 32 --proposed --alternatives <file>` for wldn-design

#### Scenario: The command raises it
- **WHEN** wldn-design then runs `crew record switchboard-kit 32 --proposed --alternatives alternatives.md` on deneb
- **THEN** the card is posted on deneb as a choice, its summary opening with the words that say an older copy was lost

### Requirement: Each landings row carries its forecast conflicts, or why none could be made
Each row of a kit's landings card SHALL carry the conflicts crew forecasts when its bolt is merged onto the kit's main and onto each bolt above it on the card, from their merge base, naming the files and the bolt or main each is with, or saying none is forecast. A forecast crew cannot make SHALL be said on its row with why, and SHALL hold nothing.

#### Scenario: Two bolts touch one file
- **WHEN** `y` and `z` of crew are rows in that order, and both change `plugin/lib/plan.py`'s same lines
- **THEN** `z`'s row says it is forecast to conflict with `y` on `plugin/lib/plan.py`, and `y`'s row says no conflict is forecast

#### Scenario: A bolt behind main
- **WHEN** main has landed a change to `README.md` that bolt `y` also changes
- **THEN** `y`'s row says it takes main first, forecast to conflict with main on `README.md`

#### Scenario: A bolt branch crew cannot read
- **WHEN** bolt `y` was made before gives went through sluice and its branch is on no host crew can read it from
- **THEN** `y`'s row says its forecast could not be made and why, and `y` keeps its box

### Requirement: Forecasts are made again when the card is raised or changed or main moves
Forecasts SHALL be made again whenever the card is raised or changed, and whenever the kit's main moves while the card is open, against GitHub's main after a fetch and each bolt where it lives.

#### Scenario: Main moves under an open card
- **WHEN** `land/crew` is open with `y` as a row forecast against main at `a1b2c3d`, and the rail is read on the main level's host once crew's checkout of the kit reads GitHub's main, as last fetched, at `e4f5a6b`
- **THEN** crew raises `land/crew` again, fetching GitHub's main and forecasting `y` against `e4f5a6b`

#### Scenario: Main has not moved
- **WHEN** `land/crew` is open with its rows forecast against `a1b2c3d`, and the rail is read with GitHub's main still at `a1b2c3d`
- **THEN** the read raises no landings card and fetches nothing for it

### Requirement: A bolt whose landing Flume refused is held at that head with no box
A bolt whose landing Flume refused for its own content, its verdict at that head failed or in conflict as the runner's report carries it, SHALL be held on its row at that head with no box, in Flume's words, while the bolts after it go on (record 0056 point 4). crew SHALL post no land of it again at that head.

#### Scenario: The second of three is refused
- **WHEN** the user sends `land/crew` with `y`, `z` and `w` ticked, and Flume's verdict on `z`'s submission is a conflict with main on `plugin/lib/plan.py`
- **THEN** `y` and `w` land, `z` stays on crew's landing row held with no box, saying in Flume's words that its landing was refused in conflict and that it takes main first, its take-main fix is launched once, and the next landings card raised carries `z` held with no box

#### Scenario: Submitted again with nothing submitted
- **WHEN** `z` was refused for a failed check at `977138a`, and later raises read the runner's report with `z` still at `977138a`
- **THEN** crew posts no land of `z` again, so nothing of it is submitted, and `z` is still held on its row with no box for a fix on the bolt, its row saying nothing of a stop

### Requirement: A refused row says whether it waits for a fix or takes main first
A failed check's row SHALL say its landing was refused and the bolt is open for work, and that it waits for a fix on the bolt, which main-level ops starts with Flume's words. A conflict's row SHALL say it takes main first, its take-main fix launched once however often the refusal is read (bolt-teams "A conflict with no landing fix launches crew's take-main fix"). No row SHALL name a team.

#### Scenario: A check fails
- **WHEN** Flume's verdict on `z`'s submission is failed, waiting on its caller, its words naming `tests:logic`
- **THEN** `z` is held on its row with no box, saying its landing was refused and the bolt is open for work, in Flume's words, and that it waits for a fix on the bolt

### Requirement: A refused bolt proven at a new head lands on its send or has a box again
Once a refused bolt's head moves and it reads proven, crew SHALL post its land on the user's send that ticked it when that send still stands for its work, and it SHALL otherwise have a box again.

#### Scenario: The fix merges
- **WHEN** a fix taking main in, launched on `z`, merges into `z` and `z` reads proven at its new head, its own work unchanged since the user's send
- **THEN** `z` has no box on any landings card, and crew posts its land on that send

#### Scenario: A fix that changes the bolt's work merges
- **WHEN** `z` was refused for a failed check, and a fix on `z` commits a change and merges, and `z` reads proven at its new head
- **THEN** `z` has a box on `land/crew` again, its note naming the fix's commit

### Requirement: A landing whose outcome crew can't tell holds nothing
A landing whose outcome crew can't tell from the runner's report SHALL hold nothing: its row SHALL say its landing can't be told and why, and crew SHALL post no land of it again at that head (`read.1`). A landing that did not land for any other cause SHALL NOT hold its row.

#### Scenario: An outcome crew can't tell
- **WHEN** crew posted `z`'s land, and the branch of the runner that took `z`'s work can't be read
- **THEN** `z` is not held, its row says its landing can't be told and why, and no land of `z` is posted again at that head

#### Scenario: A bolt the user left
- **WHEN** the user cleared `z` on their send of `land/crew`, and main then lands a change `z` also makes
- **THEN** `z` keeps its box on the card that follows, unticked, and is not held taking main first

### Requirement: An answered landings card closes once each bolt it ticked has landed, been held or stopped
A landings card the user has answered SHALL be left as it is until every bolt they ticked has landed, been held or been stopped, then closed naming what landed and where GitHub's main holds it, what was held and why, what was stopped and in whose words, and what was left; a new card SHALL follow it while rows can land. The close SHALL keep the user's send for each ticked bolt that was held and still stands for its work, saying so.

#### Scenario: Everything ticked lands
- **WHEN** the user sent `land/crew` with `y` and `z` ticked and both land
- **THEN** the card is closed saying `y` and `z` landed and where GitHub's main holds them, and no landings card of crew is open

#### Scenario: One left out
- **WHEN** the user sent `land/crew` with `y` ticked and `z` cleared, and `y` lands
- **THEN** the card is closed saying `y` landed and `z` was left, and a new card follows it with `z` as its one row

#### Scenario: A ticked bolt held at the close
- **WHEN** the user sent `land/crew` with `y` and `z` ticked, `y` lands and Flume refuses `z` for a failed check
- **THEN** the card is closed saying `y` landed and `z` was held and why, and that the send stands for `z` while its own work is unchanged

#### Scenario: A ticked bolt stopped at the close
- **WHEN** the user sent `land/crew` with `y` and `z` ticked, `y` lands and the runner answers `z`'s land refused
- **THEN** the card is closed saying `y` landed and `z` was stopped, in the runner's words, and a new card follows it with `z` as a row with its box

### Requirement: A landings card is open only while a row can land
A send ticking none SHALL close the landings card, landing nothing. With no row that can land, no card SHALL be open, and the next proven bolt SHALL raise one, following nothing.

#### Scenario: The next proven bolt
- **WHEN** no landings card of crew is open and bolt `w` reads proven
- **THEN** `land/crew` is posted with `w` as its one row, following no card

### Requirement: A follow-on card opens with one paragraph on the user's answer and what changed
Every card crew posts that follows a card the user answered SHALL open its summary, and its details, with one paragraph saying that the user answered the earlier card, when the earlier card was posted and by when crew recorded their answer, what they answered, and what has changed since, before anything else the card says, so a card asked again is never read as a repeat.

#### Scenario: A record revised after the user's note
- **WHEN** the user answered record 0019's card `req_1`, posted 2026-10-23 13:10 UTC, with a note, crew recorded it by 14:02 UTC, and the design agent revises the record at `4be21c0`
- **THEN** the card that follows `req_1` opens "You answered the card before this one, posted 2026-10-23 13:10 UTC, by 14:02 UTC: declined, with a note. Since then: revised at 4be21c0", with the commit's subject, before the record's own opening

### Requirement: A follow-on card gives the answer crew recorded at the earlier card's close
A card the user answered is one the run record shows closed after their answer, declined among them, and one whose follow-on crew withheld (below). What the user answered on the earlier card SHALL be the answer crew recorded at the earlier card's close; where the run record holds none, the opening paragraph SHALL say crew holds no record of what they answered.

#### Scenario: A deploy offered again after the user declined it
- **WHEN** the user declined deneb's deploy of `ddcf2cb` and the deployer offers deneb `e104bcf`
- **THEN** the new deploy card follows the declined one and opens saying the user declined `ddcf2cb`, when, and that the offer is now `e104bcf`

#### Scenario: An answer crew holds no record of
- **WHEN** a card that follows one the user answered is posted, and the run record's close of the earlier card holds no answer, as a close made before crew recorded answers
- **THEN** its opening says the user answered the earlier card, when, that crew holds no record of what they answered, and what changed since

### Requirement: A follow-on card says what changed in the words its event gives
What changed since the user answered SHALL be the sentences the event that raised the card gives: a record's new commit; a proposal's rewrite read against the proposal it replaces; a deploy's newer head; a step's place after the card it follows; what the user's send on a kit's landings card landed, held, stopped and left, and the bolts proven or moved since.

#### Scenario: A proposal rewritten after the user's note
- **WHEN** the user answered proposal 239's card with a note and the planner rewrites it as proposal 241, which adds unit `x` and no longer adds unit `y`
- **THEN** the card that follows says first what the user answered and that proposal 241 adds `x` and no longer adds `y`

#### Scenario: The landings card after a send that left a bolt
- **WHEN** the user sent `land/crew` with `y` ticked and `z` cleared, and `y` lands
- **THEN** the card that follows opens saying the user sent the earlier card, when, ticking `y` and leaving `z`, and that `y` landed and `z`, which they left, waits on this card

#### Scenario: The landings card after a send whose bolt was stopped
- **WHEN** the user sent `land/crew` with `z` ticked, and the runner answered `z`'s land refused
- **THEN** the card that follows opens saying the user sent the earlier card, when, ticking `z`, and that `z`'s landing was stopped, in the runner's words, so `z` waits on this card

### Requirement: A follow-on with nothing changed is recorded as standing, not posted
A card that follows one the user answered, for which the event that raised it gives nothing changed since the answer, SHALL NOT be posted: crew SHALL record it as a `card.post` under the row's key in its owner's name, refused in crew's own words naming the earlier card and saying its answer stands, with that card's id and the state `stands`, and SHALL refuse nothing of the event.

#### Scenario: A proposal rewritten with nothing changed
- **WHEN** the user answered proposal 239's card and the planner rewrites it as proposal 240 with the same commands and the same case
- **THEN** no card is posted for proposal 240; the run record has a `card.post` under the proposal's key, refused in crew's words naming 239's card and saying its answer stands, state `stands`; and `crew rail` shows the row with those words

#### Scenario: A deploy offered again at the head the user declined
- **WHEN** the user declined deneb's deploy of `ddcf2cb` and the deployer offers deneb `ddcf2cb` again with the same notes and steps
- **THEN** no card is posted, and the decline stands

### Requirement: A withheld follow-on is shown on the rail and posted only once something changes
The rail's card line SHALL show a withheld follow-on's words, and the rail's sweep SHALL NOT raise that row's card again; the next post under the row's key SHALL follow the card whose answer stands and SHALL be posted only when its event gives what changed since.

#### Scenario: The sweep meets a withheld card
- **WHEN** proposal 240's card was withheld and the rail is read on the planner's host
- **THEN** the sweep raises no card for proposal 240's row, and records nothing more

#### Scenario: Something changes after a withheld card
- **WHEN** proposal 240's card was withheld and the planner rewrites it as proposal 242, which adds unit `w`
- **THEN** proposal 242's card is posted following 239's card, opening with what the user answered on it and that proposal 242 adds `w`

### Requirement: An answered card's close records what the user answered from names alone
When crew closes one of its own cards that the user answered, it SHALL record on the close's entry what they answered as `Answer`, in crew's own words made from names alone: approved or declined; the options they picked, by the bolt, unit or choice each names; done, a failed step, or that they will handle it themselves; and "with a note" when they wrote one, never the note's words (`record.3`).

#### Scenario: A landings card sent with ticks
- **WHEN** the user sends `land/crew` with `land:y` ticked, `land:z` cleared and a note, and crew closes it
- **THEN** the close's entry holds `Answer: ticked y, left z, with a note`, and none of the note's words

#### Scenario: A deploy declined
- **WHEN** the user declines deneb's deploy card with the words "not tonight" and crew closes it
- **THEN** the close's entry holds `Answer: declined, with a note`

### Requirement: A card answered in a pane records that it was
A card answered in a conversation, closed as answered there, SHALL record that it was answered in a pane.

#### Scenario: A card closed as answered in its owner's pane
- **WHEN** crew closes `land/b1`'s card, waiting on the user, as answered in wldn-ops's pane
- **THEN** the close's entry holds the state closed and `Answer: answered in wldn-ops's pane`

### Requirement: A row taking main first stays on the landings card as an unticked box
While any row of a kit's landings card can land, each row taking main first, forecast to conflict with main or with only take-main fixes in flight, SHALL stay on the card as a box, unticked, its detail saying it takes main first and why, its consequence that ticked it lands once a fix on it has taken main in and sluice has proven it, the user's send standing through it; a row taking main first that an earlier send still lands SHALL be held with no box.

#### Scenario: One of two
- **WHEN** `land/crew` waits with `y` and `z` as ticked boxes, and main moves so that `z` is forecast to conflict with it
- **THEN** the card is changed in place, its change note saying `z` takes main first and why, `y` still ticked and `z` unticked, saying why

### Requirement: A row coming to take main first, or back, changes the waiting card in place
When a row comes to take main first while its card waits on the user, or comes back from it, crew SHALL change the card in place saying so, and SHALL NOT withdraw it and post it again: a bolt taking main in keeps the card's rows and so its form. A card left with no row that can land SHALL be withdrawn saying why.

#### Scenario: One of three
- **WHEN** `land/crew` waits with `y`, `z` and `w` as boxes, and main moves so that `w` is forecast to conflict with it
- **THEN** the card is changed in place, its change note saying `w` takes main first and why, `y` and `z` still ticked and `w` unticked

#### Scenario: Back from taking main in
- **WHEN** `land/crew` waits with `y` ticked and `z` unticked taking main first, and `z`'s take-main fix merges and `z` reads proven at `def5678`
- **THEN** the card is changed in place, its change note saying `z`'s head is now `def5678` and `z` can land again, both ticked

#### Scenario: Taking main in and back, one card
- **WHEN** `land/crew` waits with `y` and `z`, main moves under `z`, `z`'s take-main fix runs and merges, and main moves under `z` again, as switchboard-kit's identity-and-access did beside a-deploy-row on 2026-11-06
- **THEN** one card is open throughout, posted once and changed in place at each move, and none is withdrawn and posted again

#### Scenario: Nothing else can land
- **WHEN** `y` lands from `land/crew` and `z` still takes main first
- **THEN** no landings card of crew is open until `z` can land

### Requirement: A landings card is followed only when its form must change
A landings card's form SHALL be read from every row it shows. crew SHALL follow the card, instead of changing it in place, only when its form must change, as when a second bolt joins a card of one row, since Pending You changes no card's kind in place and takes no list of fewer than two boxes.

#### Scenario: Joining a card of one
- **WHEN** `land/crew` waits with `y` alone, and `z`, proven, is forecast to conflict with main
- **THEN** the card is followed by a list of `y` ticked and `z` unticked, taking main first, since a card of one row is an approval

### Requirement: A row taking main first that the user leaves unticked is not a bolt they left
A row the card showed taking main first that the user leaves unticked on their send SHALL NOT be a bolt they left: once it can land, a card asks for it, ticked as crew proposes.

#### Scenario: Unticked on the send
- **WHEN** the user sends `land/crew` with `y` ticked and `z`, shown taking main first, unticked, and `z` then reads proven
- **THEN** `z` is not left: the close names no bolt left, and the card that follows asks for `z` ticked

### Requirement: A send stands for a ticked bolt that takes main first, its card left
When the user has sent a landings card with a bolt ticked, and that bolt then takes main first, by a forecast or a take-main fix in flight, or they ticked it while its row took main first, crew SHALL keep the send standing for it: the card SHALL be left, and SHALL NOT be closed counting that bolt as held, while it takes main in.

#### Scenario: Ticked beside one that lands
- **WHEN** the user sent `land/crew` with `y` and `z` ticked, `z` lands, and `y` takes main first
- **THEN** `land/crew` is left as it is while `y` takes main in, and is not closed saying `y` was held

#### Scenario: Ticked while taking main in
- **WHEN** the user sends `land/crew` with `y` ticked and `z`, shown taking main first, ticked too
- **THEN** `y` lands, the card is left while `z` takes main in, and `z` lands on that send once it reads proven, its own work unchanged

### Requirement: A ticked bolt taking main in lands on its send once it reads proven at a new head
crew SHALL post no land of a ticked bolt taking main in while it still stands at the head the card showed or the run record holds a conflict at its head now, read where the bolt lives; once its take-main fix has moved it, its own work unchanged, and it reads proven, the next raise SHALL post its land on that send, and `crew card read land/<kit>` SHALL name it with that land's request.

#### Scenario: Ticked, then forecast to conflict
- **WHEN** the user sent `land/crew` with `y` ticked, and main moves so that `y` is forecast to conflict with it before a raise posts `y`'s land
- **THEN** `land/crew` is left as it is, its send still standing for `y`, no land of `y` is posted, and no agent is told

#### Scenario: Read after the take-main fix
- **WHEN** the run record holds `z` forecast to conflict with main at `abc1234`, the head the card showed, the user ticked `z`, and `z`'s take-main fix has moved it to `def5678`, with no conflict recorded there, and `z` reads proven
- **THEN** the next raise posts a land of `z` on that send, and `crew card read land/crew` names `z` with that land's request

### Requirement: A row the user left keeps its box and says whether it would take main first
Each row of a bolt the user left SHALL be forecast against main whenever the card is raised, as every row is, and SHALL keep its box. When its forecast against main finds a conflict, the row SHALL say it would take main first if ticked, on which files and at which revision of main, and that once it is ticked it waits for a fix taking main in, the user's send standing through it; otherwise it SHALL say it lands clean.

#### Scenario: Left and clean
- **WHEN** `z` is left and its forecast against main finds no conflict
- **THEN** its row says no conflict is forecast

### Requirement: A left row's first conflict with main changes the card in place once
When a left row's forecast first finds a conflict with main at the bolt's head and main's revision while a card waits on the user, crew SHALL change the card in place saying so; the same forecast SHALL NOT change the card again.

#### Scenario: Left, and main conflicts with it
- **WHEN** `z` is left on `land/crew`, waiting on the user, and main moves to `e4f5a6b`, landing a change to `README.md` that `z` also makes
- **THEN** `land/crew` is changed in place, its note saying `z`, which they left, would take main first, forecast to conflict with main on `README.md` at `e4f5a6b`; `z` keeps its box, its row saying it would take main first once ticked; and no agent is told

#### Scenario: Raised again at the same heads
- **WHEN** the card is raised again and neither `z` nor main has moved
- **THEN** the card is not changed for it

### Requirement: crew card preview asks the runner by one request, running nothing of sluice's
`crew card preview` SHALL ask for the thing's preview by one request on the drive's branch: a `preview` naming the host whose runner reported the thing's work, the work it serves, its repository as the plan names it, and the branch and revision the row or line names (drive-state "A preview names its host, its work, its repository, its branch and its revision"). crew SHALL run no sluice command and read no file of sluice's for it.

#### Scenario: Asked
- **WHEN** swancloud-ops runs `crew card preview land/crew y` with `y`'s row at `abc1234`, and deneb's runner took `y`'s work
- **THEN** `requests.rec` gains one request saying `Act: preview`, `Host: deneb`, `Work: bolt/y`, `Repo: crew`, `Branch: bolt/y` and `Revision: abc1234`, with no `Done`; `land/crew` is changed in place, its note saying `y`'s preview of `abc1234` is asked of the runner on deneb; and no sluice command is run

### Requirement: crew card preview answers once its request is written and asks a standing preview no twice
`crew card preview` SHALL answer once the request is written, and change the card in place saying the preview is asked of that host's runner. Asked again while crew's ask of that revision on that host stands, and the runner has neither refused it nor carried it failed or no longer listed, crew SHALL write no second request and give back what the runner reports.

#### Scenario: Asked twice
- **WHEN** `crew card preview land/crew y` is run again while deneb's runner reports `y`'s preview of `abc1234` up
- **THEN** `requests.rec` gains no request, and `y`'s row lists the same addresses

#### Scenario: Asked again after a refusal
- **WHEN** `crew card preview land/crew y` is run again after deneb's runner refused the first request
- **THEN** `requests.rec` gains a second `preview` of `bolt/y` at `abc1234`, and the card says it is asked

### Requirement: A preview brought up is listed on the card while sluice lists it
Once the runner reports the preview brought up, crew SHALL list on the card, while sluice lists it waiting, starting or up as the runner carried that listing, each address sluice named, under the name sluice gave it.

#### Scenario: Brought up
- **WHEN** deneb's runner then answers that request done, with sluice's listing of its preview up at addresses `web` and `api`
- **THEN** at the rail's next read on the drive's main machine `land/crew` is changed in place, its note saying `y`'s preview is up, `y`'s row listing `web` and `api` with sluice's addresses and saying a preview lands nothing

### Requirement: A preview is put away on the user's done and when its row leaves the landings card
crew SHALL put away a preview it asked for from a card by one request on the drive's branch, the same `preview` marked `Done: yes`: when the owner runs `--done` on the user's word; when the bolt's row is held for a fix, lands, is dropped or otherwise leaves its kit's landings card, at that card's raise. The card, while it waits, SHALL say it was put away.

#### Scenario: The user is done
- **WHEN** the user writes "done with y's preview" on `land/crew` and swancloud-ops runs `crew card preview land/crew y --done`
- **THEN** `requests.rec` gains a `preview` naming deneb, `bolt/y`, `crew`, `bolt/y` and `abc1234` with `Done: yes`, and `y`'s row again names `bolt/y` at its head and says to write on the card to bring it up

#### Scenario: The bolt lands with its preview up
- **WHEN** `crew bolt land y` closes `y` while crew's ask of its preview stands
- **THEN** the raise of `land/crew` that follows writes its done, and the close says nothing of a preview

#### Scenario: A fix holds the landing
- **WHEN** a fix started on bolt `y` holds its row while crew's ask of its preview stands
- **THEN** the raise of `land/crew` writes its done, and no preview is asked when `y` reads proven again

### Requirement: A preview is put away when its batch's card closes or its card or row is gone
crew SHALL put away a preview it asked for from a card by one request on the drive's branch, the same `preview` marked `Done: yes`, when a batch's card closes, for its lines no other open card carries; and at a rail read on the drive's main machine, for one whose card is closed or whose row is gone, once its ask is two minutes old.

#### Scenario: A card closed elsewhere
- **WHEN** batch 7's card is closed with no crew command closing it while crew's ask of `a/demo`'s preview stands, and no other open card holds `a`, and the rail is read on the drive's main machine more than two minutes after the ask
- **THEN** the rail's read writes its done, and says so

#### Scenario: A row gone with no raise of its card
- **WHEN** `y` leaves the plan by a write that raises no landings card while crew's ask of its preview stands, and the rail is read on the drive's main machine more than two minutes after the ask
- **THEN** the rail's read writes its done, and says so

### Requirement: crew puts away only a standing preview it asked for
crew SHALL put away only a preview it asked for and has not put away, SHALL write no done for one the runner refused, and SHALL run no sluice command for it.

#### Scenario: Done with none asked
- **WHEN** `crew card preview land/crew y --done` is run and crew's last ask of `y`'s preview at its head was put away already
- **THEN** crew says it asked for no preview of `y` that stands, and writes no request

#### Scenario: A preview crew did not ask for
- **WHEN** a person brought up a preview of an earlier revision of `bolt/y` themselves, and `y` later lands
- **THEN** crew writes a done only for the revision it asked for, and none for the person's

#### Scenario: A preview the runner refused
- **WHEN** deneb's runner refused crew's ask of `y`'s preview, and `y` lands
- **THEN** no done is written for it

### Requirement: A row forecast to conflict with main takes main first, recorded once and telling no one
A row whose bolt is forecast to conflict with what the kit's main holds, by the card's forecast or by one the run record holds at the bolt's present head, SHALL take main first, saying so, the files, and that it does until a fix taking main in moves its head. The raise that first finds the conflict at a bolt head and revision of main SHALL record it once, as a `forecast` on the bolt, and SHALL tell no agent and start nothing. A conflict only with a bolt above it holds nothing.

#### Scenario: Main landed a change the bolt also made
- **WHEN** `x` and `y` read proven, and main has landed a change to `openspec/specs/artifact-buckets/spec.md` that `y`'s own archive also changed
- **THEN** `land/crew` shows `y` unticked, saying `y` takes main first, forecast to conflict with main on `openspec/specs/artifact-buckets/spec.md`, until a fix taking main in moves its head, and `x` ticked; the run record gains one `forecast` on `bolt/y` at `y`'s head and main's revision; and no agent is told

#### Scenario: Raised again at the same heads
- **WHEN** the run record holds `y`'s forecast at `y`'s present head, and the card's own forecast against main could not be made
- **THEN** `y` still takes main first, in the recorded files, and nothing more is recorded

#### Scenario: Only a bolt above it
- **WHEN** `z` is forecast to conflict with `y`, the row above it, and with nothing on main
- **THEN** `z` is ticked, its row naming the conflict with `y`

### Requirement: A fix taking main in is launched by Flume, by crew or by hand
A fix taking main in SHALL be launched in one of three ways:
- by Flume, as the bolt's landing fix, on Flume's own forecast or on its refusal of the bolt's landing, where the bolt's base place names a landing fix;
- by crew, when Flume refuses the bolt's landing in conflict with main and the base place names none, as the runner's report carries it and "A conflict with no landing fix launches crew's take-main fix" has it;
- by a fix launched on the bolt by hand.

#### Scenario: Flume's forecast fix
- **WHEN** `y` is forecast to conflict with main and its base place lists `y-1`, for a forecast, live
- **THEN** `y` takes main first, naming `y-1` taking main in, and crew appends no launch for it

### Requirement: A row taking main first is offered to land again once proven with no conflict
A row taking main first SHALL NOT be ticked or offered to land while it conflicts. Beside a row that can land it SHALL stay on the card as an unticked box, as "A row taking main first stays on the landings card as an unticked box" has it. With none that can land it SHALL be held, and no card raised for it. It SHALL be ticked as crew proposes again once the bolt reads proven at a new head with no conflict forecast.

#### Scenario: The fix merges
- **WHEN** a fix taking main in merges into `y` and `y` reads proven at its new head with no conflict forecast against main
- **THEN** `y` is ticked on `land/crew` again

### Requirement: A row whose bolt the user left does not take main first
A row whose bolt the user left SHALL NOT take main first so: it keeps its box and says it would take main first, as "A row the user left keeps its box and says whether it would take main first" has it.

#### Scenario: A bolt the user left
- **WHEN** the user cleared `z` on their send of `land/crew`, and main then lands a change `z` also makes
- **THEN** `z` keeps its box on the card that follows, unticked, and does not take main first

## REMOVED Requirements

### Requirement: Each rail row has a card key
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "Each rail row has a card key for its thing, not its version", "A row's card is posted under its key, filled out to eight characters" and "A batch's row lasts until its card closes or it waits on nothing".

### Requirement: A card says whose it is and where it belongs
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A card is asked in the name of the role whose row it is" and "A card is filed in its kit's area, in its drive's group".

### Requirement: Landing is approved only by holding the button
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A landings card of one row is approved only by holding the button" and "A landings card of two or more rows is a list carrying highStakes".

### Requirement: An answer wakes the owner, which acts on the user's word
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "An answer on a crew card is acted on by its row's role alone", "No role lands what the user ticked, and no process of crew's waits on an answer" and "A role running as its kind is asked to act on its card's answer".

### Requirement: An agent never runs Pending You from npm or waits on a hold
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "An agent adopts crew's card by get_request and runs no pendingyou command" and "An agent adopts its open cards from the rail after a fresh start".

### Requirement: A crew agent's card acts are in the run record
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "Each card act is an entry in the run record naming its card and key" and "An agent's card act whose result names no card is recorded unread".

### Requirement: The rail shows each row's card
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "The rail prints each row's card under it and the open questions after" and "A row's card is the one open in its owner's name, others named apart".

### Requirement: A card's words are the document's own
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A card's words are prose the phone wraps, in the document's own words" and "A list the user scans is an artifact on the card's face".

### Requirement: The landing card is posted once the bolt's verification is green
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "Each kit has one landings card in main-level ops's name, its rows in plan order" and "A bolt is a row that can land once its work is merged, read and verified".

### Requirement: A batch's card is a notice naming every unit
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A batch's card is a notice that asks nothing, the reviewer's summary on its face" and "A batch's card's title and words say what it is about and where notes go".

### Requirement: A card's document is inline Markdown
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A card carries a document's substance as inline Markdown, never a file" and "A crew card carries only a picture, Markdown, text lists, links and steps".

### Requirement: A record's card is an approval
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A record's card is an approval of risk low carrying the record whole", "A record a rule decided between alternatives is carded as a choice" and "A record's choice carries its alternatives before the record and recommends the user's own path".

### Requirement: A card the user answered is followed by its new version
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "crew changes its card in place while it waits on the user" and "An answered card is acked with the change note and followed by a new card".

### Requirement: A card posted after a closed one takes its key's revision
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A card posted under a key whose last card closed takes the key's revision" and "A card still open under its key keeps its key and is recorded once".

### Requirement: A step's card is the user's do
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A user's step is a do card, and an agent's own step has none" and "A deploy's steps for the user are carded one at a time".

### Requirement: A row's card is changed in place when its thing changes
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A row's card is changed in place with a note the user sees", "A card that asks questions is withdrawn and followed, never changed in place" and "A card whose form changes is withdrawn and followed".

### Requirement: A preview that fails is said on the card and holds nothing
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A preview refused or not there yet is said on its row and holds nothing" and "A card changes in place when its preview fails, goes or comes up".

### Requirement: A row's card its owner's host can't reach is raised again there
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A card belongs to its host's sign-in and is asked after only from there", "A row's card held on another host is posted again on its owner's host" and "The rail takes a card posted again as the row's, and posts none for a row that no longer waits".

### Requirement: A record's card its owner's host can't reach is raised again there
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A stranded record's card is posted again on the main level's host while it is proposed" and "A record's card posted again is built from the record on the kit's main".

### Requirement: A record raised with alternatives is raised again by its command
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A record's status records whether its card offered alternatives" and "A stranded record card with alternatives is raised again only by its command".

### Requirement: The landings card forecasts each row's conflicts
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "Each landings row carries its forecast conflicts, or why none could be made" and "Forecasts are made again when the card is raised or changed or main moves".

### Requirement: A refused landing is held on its row
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A bolt whose landing Flume refused is held at that head with no box", "A refused row says whether it waits for a fix or takes main first", "A refused bolt proven at a new head lands on its send or has a box again" and "A landing whose outcome crew can't tell holds nothing".

### Requirement: The landings card closes when nothing waits
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "An answered landings card closes once each bolt it ticked has landed, been held or stopped" and "A landings card is open only while a row can land".

### Requirement: A card that follows one the user answered says so first
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A follow-on card opens with one paragraph on the user's answer and what changed", "A follow-on card gives the answer crew recorded at the earlier card's close" and "A follow-on card says what changed in the words its event gives".

### Requirement: A follow-on with nothing changed is not posted, the earlier answer standing
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A follow-on with nothing changed is recorded as standing, not posted" and "A withheld follow-on is shown on the rail and posted only once something changes".

### Requirement: The close of an answered card records the answer
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "An answered card's close records what the user answered from names alone" and "A card answered in a pane records that it was".

### Requirement: A row taking main first changes the card in place
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A row taking main first stays on the landings card as an unticked box", "A row coming to take main first, or back, changes the waiting card in place", "A landings card is followed only when its form must change" and "A row taking main first that the user leaves unticked is not a bolt they left".

### Requirement: A send stands for a ticked bolt taking main in
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A send stands for a ticked bolt that takes main first, its card left" and "A ticked bolt taking main in lands on its send once it reads proven at a new head".

### Requirement: A row the user left says whether it would take main first
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A row the user left keeps its box and says whether it would take main first" and "A left row's first conflict with main changes the card in place once".

### Requirement: A preview asked for from a card is asked of the runner and listed while it is up
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "crew card preview asks the runner by one request, running nothing of sluice's", "crew card preview answers once its request is written and asks a standing preview no twice" and "A preview brought up is listed on the card while sluice lists it".

### Requirement: A preview is released on the user's done and when its card or row ends
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A preview is put away on the user's done and when its row leaves the landings card", "A preview is put away when its batch's card closes or its card or row is gone" and "crew puts away only a standing preview it asked for".

### Requirement: A row forecast to conflict with main takes main first until a fix takes main in
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A row forecast to conflict with main takes main first, recorded once and telling no one", "A fix taking main in is launched by Flume, by crew or by hand", "A row taking main first is offered to land again once proven with no conflict" and "A row whose bolt the user left does not take main first".
