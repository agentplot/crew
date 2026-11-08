## MODIFIED Requirements

### Requirement: A crew agent's card acts are in the run record
Each card crew posts, changes, withdraws or closes, each answer of the user's on one of them that crew reads, and each card a crew agent posts, changes or closes through Pending You's tools, SHALL be an entry in the partition's run record naming the row's object or the asker, the card's id in `Card` and the key in `Key`, crew's read from Pending You's own reply, an agent's from the tool's result; an agent's act whose result names no card SHALL be recorded on the agent with `State: unread`, and `crew rail` SHALL list each such act of the last 14 days with its agent, its act and its time. An entry SHALL NOT hold a card's title, summary or other text.

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

### Requirement: The rail shows each row's card
`crew rail` SHALL print, under each row, the row's card key, whether a card with that key is open, its id and whose it is, and whether the user has answered it, and after the groups the open question cards, each with its key, which names it, its asker and its age, and the open record cards apart. A card is open from its `card.post` entry until a `card.close` entry for the same card, or until a later `card.post` under the same key names another card, which is then the row's card while the older is taken as lost. A row's card is the one open in the row owner's name; another card open under its key, in another name, SHALL be named apart on the row as a copy that is not the row's, with whose it is.

#### Scenario: A row with its card
- **WHEN** bolt `y` reads proven and crew's card `req_l1` under `land/y` is open
- **THEN** the row's card line names `land/y` as open, `req_l1`, the conductor's

#### Scenario: A row without a card
- **WHEN** a proposal is open and its card's post was refused
- **THEN** the row's card line names `proposal/<n>` with no card open and the refusal's words

#### Scenario: A card posted again under its row's key
- **WHEN** crew's card `req_1` under `proposal/17` read not found after the host signed in again, and the rail read posted `req_2` under `proposal/17`
- **THEN** the row's card line names `req_2` as its open card, and `req_1` is listed as lost

#### Scenario: A row with its card and a question open
- **WHEN** `proposal/4`'s card `req_p4` is open and swb-1-conductor's question `req_q1` is open
- **THEN** the proposal row's card line names `proposal/4`, open, `req_p4`, the planner's; and after the groups `req_q1` is listed with its key, swb-1-conductor and its age

#### Scenario: Two cards open under one row's key
- **WHEN** afterthought's `proposal/508` row is the planner's, afterthought-planner's card `req_51` is open under it, and swancloud-planner's card `req_69` is open under it too
- **THEN** the row's card line names `req_51`, afterthought-planner's, as its card, and the row names `req_69` apart, swancloud-planner's, as a copy that is not the row's

#### Scenario: A row's card the user answered
- **WHEN** `land/crew`'s card `req_l2` is open and the run record holds the user's answer on it
- **THEN** the row's card line names `land/crew`, `req_l2`, answered, with when and what, and whose act it waits on

### Requirement: The rail names an open card whose row is gone
After its groups, `crew rail` SHALL list each card its sweep withdrew or closed on this read, with its key, its owner and why (its row is gone, its asker ended), and each card it posted again as lost. An open card whose row is gone that the sweep did not close SHALL be listed with what keeps it: the words of the refusal of its last close, where its last close was refused, else that a later rail read on its host closes it.

#### Scenario: A forgotten card
- **WHEN** proposal 4 was approved from the planner's pane and its card `proposal/4` is still open
- **THEN** the next rail read closes it with the approval's outcome and lists it, "closed: its proposal was applied"

#### Scenario: A withdrawn card
- **WHEN** bolt `y` was dropped while `land/y`'s card was open
- **THEN** the rail withdraws the card and lists it, "withdrawn: its bolt was dropped"

#### Scenario: A card whose close was refused
- **WHEN** `batch/40`'s card is open with its batch answered, and its last close was refused "Pending You refused the close: the service is down"
- **THEN** the rail lists `batch/40` among the open cards whose row is gone with those words, and does not say a later read closes it

## ADDED Requirements

### Requirement: crew records the user's answer the first time it reads it
When an act of crew's reads a card the run record holds open answered in Pending You, it SHALL record a `card.answer` entry on the card's object, in the card owner's name, with `Card`, `Key` and `Answer` in crew's words made from names alone, and for a kit's landings card `Heads`, the bolts ticked at the heads the card showed. It SHALL record one per card. Those acts are the rail's sweep, a landings card's raise and `crew card read`.

#### Scenario: The sweep finds a row's card answered
- **WHEN** the rail's sweep asks after `proposal/57`'s card `req_57`, which the run record holds open, and Pending You gives it answered, approved
- **THEN** the run record has one `card.answer` on `proposal/57` with `req_57`, `Key: proposal/57` and `Answer: approved`

#### Scenario: A landings card's raise reads it answered
- **WHEN** a raise of `land/sluice` reads its card `req_e9` answered with `land:a` ticked and `land:b` cleared, the card showing `a@1111111 b@2222222`
- **THEN** the run record has a `card.answer` on `kit/sluice` with `Answer: ticked a, left b` and `Heads: a@1111111`

#### Scenario: Read answered again
- **WHEN** a later read finds `req_57` answered again
- **THEN** nothing more is recorded

#### Scenario: A question answered
- **WHEN** the sweep asks after agentplot-design's question `req_q2` and Pending You gives it answered
- **THEN** the run record has a `card.answer` on `agent/agentplot-design` with `req_q2` and its key

### Requirement: A card the user answered is closed, never withdrawn
crew SHALL close a card the user answered by acking it with an outcome, its close's `State` closed and its `Answer` recorded, whatever ends it: an event's outcome, or, where the event gives only a reason, the reason as the outcome. crew SHALL NOT withdraw a card the user answered.

#### Scenario: A landings card answered whose row the sweep finds gone
- **WHEN** the user approved `land/sluice`'s card and the sweep closes it as its row is gone, the ticked bolt having been dropped
- **THEN** the card is acked with "nothing waits to land on sluice's main", its close's State is closed and its Answer approved, and no close of it is recorded withdrawn

#### Scenario: A card still waiting
- **WHEN** the sweep closes `land/sluice`'s card, which waits on the user, as its row is gone
- **THEN** it is withdrawn with the reason, as before

### Requirement: A kit's landings card's close keeps the user's send
Every close of a kit's landings card the user answered SHALL carry as `Heads` the bolts they ticked, at the heads the card showed. This holds whichever act closes it: the raise, the sweep, `crew bolt land`, or a read that finds it ended in Pending You. The card that follows then asks for no bolt the send still lands at a head whose own work is the same.

#### Scenario: The sweep closes an answered landings card
- **WHEN** the user ticked `a` at `1111111` on `land/sluice`'s card and the sweep closes it with `a` not landed
- **THEN** the close holds `Heads: a@1111111`

#### Scenario: The next card
- **WHEN** `land/sluice`'s next card is raised while `a` stands at `1111111`
- **THEN** it has no row for `a`, the send standing for it

#### Scenario: A send closed in Pending You by its owner
- **WHEN** ops's session acked `land/sluice`'s answered card in Pending You, and the next raise reads it resolved
- **THEN** crew records it closed as ended in Pending You already, with its Answer and `Heads: a@1111111`, and the card it posts has no row for `a`

### Requirement: The sweep leaves an answered landings card while a bolt it ticked waits to land
The rail's sweep SHALL NOT close a kit's landings card the user answered while a bolt they ticked on it has neither landed nor been dropped, even when the kit's row is gone from the read. It SHALL leave the card, saying it waits on main-level ops to land what was ticked. The event that ends the send closes it.

#### Scenario: The row is gone for a moment
- **WHEN** the user approved `land/sluice`'s card ticking `a`, `a` has no `bolt.land` or `bolt.drop` since, and the rail's read finds no `land/sluice` row
- **THEN** the sweep leaves the card open and says it waits on agentplot-ops to land `a`; nothing is withdrawn

#### Scenario: The ticked bolt landed
- **WHEN** `a` has landed and no other ticked bolt waits, and the read finds no `land/sluice` row
- **THEN** the sweep closes the card as answered, saying `a` landed

### Requirement: A card Pending You has ended is recorded on the read that finds it
When the rail's sweep asks Pending You after an open card of crew's and is told it is resolved, cancelled or expired, it SHALL record the card's close on that read: closed as ended in Pending You already when resolved, with what the user answered, and withdrawn when cancelled or expired. It SHALL send Pending You nothing for it. The card then leaves the rail, and a row that still waits is a row with none, raised as such.

#### Scenario: A card the user dismissed
- **WHEN** `proposal/57`'s card is open in the run record and the sweep's ask finds it cancelled
- **THEN** the run record holds its close, withdrawn, ended in Pending You already; the rail no longer names it open; and the sweep raises `proposal/57`'s card as a row with none

#### Scenario: A question its asker acked
- **WHEN** a question's card is open in the run record and the sweep's ask finds it resolved
- **THEN** the run record holds its close, closed, ended in Pending You already, and the rail lists it nowhere

### Requirement: A card Pending You holds in another assistant's name is lost to its owner
A card whose read, change or close in the name of the owner the run record gives Pending You refuses as another assistant's card SHALL be lost to that owner, as a card Pending You no longer finds is. Its row's card SHALL be posted again in the owner's name, saying the older copy is dead. With its row gone, it SHALL be recorded lost and posted by nobody. In either case it SHALL leave the rail's open cards.

#### Scenario: A batch card posted under another name
- **WHEN** madswan-planner's card `req_ea` under `batch/16` is open in the run record, its batch was answered in a pane, and the sweep's close is refused "This is swancloud-planner's card; leave it. You're "madswan-planner": act only on the cards you posted."
- **THEN** the card is recorded lost to madswan-planner, nobody posts it again, and the rail lists it no more among the open cards whose row is gone

#### Scenario: A row's card posted under another name
- **WHEN** `proposal/12`'s card is open in the run record in wldn-planner's name, and Pending You refuses the sweep's read of it in wldn-planner's name as swancloud-planner's card
- **THEN** the card is recorded lost, and `proposal/12`'s card is posted again in the planner's name, saying the older copy is dead
