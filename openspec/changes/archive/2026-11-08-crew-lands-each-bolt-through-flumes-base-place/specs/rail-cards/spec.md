## ADDED Requirements

### Requirement: The user's send on a kit's landings card posts one land for each row it lands
When an act of crew's that raises a kit's landings card reads the user's send on it, the raise SHALL post one `land` request for each row the send lands, a bolt's or a fix of main's, of that row's launch, in the card's order with the fixes of main first, by one plan write before it acts on the card, each land recorded in the run record as asked with its request (record 0056 points 3 and 6). No agent SHALL run anything for the landing (record 0056 point 5).

#### Scenario: Two bolts sent
- **WHEN** the user sends `land/crew` with `y` and `z` ticked, `y` first, and crew's next raise of `land/crew` reads the send
- **THEN** that raise appends to `requests.rec`, in one plan write, a land of `y`'s launch and then one of `z`'s, each recorded in the run record as asked with its request, and no agent is told to run anything

#### Scenario: A fix of main beside a bolt
- **WHEN** the user sends `land/crew` with `y` and `fix main--a-test-reads-its-fixture` ticked
- **THEN** the raise posts the fix's land first, of the fix's launch, and then `y`'s

### Requirement: A landings row is due one land for each send and head
A row of a kit's landings card SHALL be due a land when its box was ticked on a send that stands for it at its head now, it can land, and no land of its launch was posted at that head nor stands undecided. A send read twice SHALL post once, and a send that stands through a take-main fix SHALL post again once the bolt reads proven at its new head. A write replayed on a tip that already holds the lands SHALL write nothing.

#### Scenario: The send read again
- **WHEN** a later raise reads the user's send on `land/crew` with `y` and `z` still at the heads they were ticked at, their lands posted
- **THEN** it posts no land

#### Scenario: A ticked bolt taking main in
- **WHEN** the user ticked `z` at `abc1234`, Flume refused `z`'s landing in conflict with main, and `z`'s take-main fix merged, so `z` reads proven at `def5678` with its own work unchanged
- **THEN** no land of `z` is posted while it takes main in, and the first raise after it reads proven at `def5678` posts one land of `z` on that send

#### Scenario: A stopped row on the same send
- **WHEN** the runner answered `z`'s land on the user's send refused
- **THEN** no raise posts another land of `z` on that send

#### Scenario: A write replayed
- **WHEN** the plan write posting `y`'s land is applied again to a tip that already holds that land
- **THEN** it writes nothing

### Requirement: A send's lands are posted by the first act that reads it
The lands of a send SHALL be posted by whichever act of crew's first reads it: the host's follower, `crew card read land/<kit>` or any act that raises the card, so nothing waits on an agent's session (`roles.6`, `teams.24`).

#### Scenario: Read by the card's read
- **WHEN** the user sent `land/crew` with `y` ticked, no raise has read the send, and main-level ops runs `crew card read land/crew`
- **THEN** that read posts `y`'s land and prints it with its request

#### Scenario: Read with no session of ops's running
- **WHEN** the user sends `land/crew` with two rows ticked, no session of main-level ops runs, and a rail read on the main level's host raises the card
- **THEN** that raise posts the two lands in the card's order, and a second raise posts none

### Requirement: The landings card's read prints the lands crew posted
`crew card read land/<kit>`, once the user has sent the card, SHALL print the rows the send lands in the card's order, those an earlier send still lands first, each with the land crew posted for it and its request, or why none is posted: it takes main first, its land was stopped, or it landed or left the plan since. A send ticking no row SHALL print that nothing lands. The read SHALL print no command for any agent to run (record 0056 point 5).

#### Scenario: Two bolts sent
- **WHEN** the user sent `land/crew` with `a` and `c` ticked and `b` cleared, and crew's raise posted `a`'s land as request 57 and `c`'s as request 58
- **THEN** `crew card read land/crew` prints `a` then `c`, each with its request, and no `crew bolt submit` or other command

#### Scenario: A ticked bolt taking main first
- **WHEN** the user ticked `z` on `land/crew`, and the run record holds `z` forecast to conflict with main at the head the card showed
- **THEN** the read says `z` takes main first and the user's send stands for it, and names no land of `z`

#### Scenario: Nothing ticked
- **WHEN** the user sent `land/crew` with no box ticked
- **THEN** the read says nothing lands, and no land is posted

### Requirement: A bolt started before bolts were base places has no box
A started bolt with no launch of `bolt/<bolt>` in the drive's requests SHALL land under the crew that started it. Once it reads proven, its row on its kit's landings card SHALL have no box and SHALL say it was started before bolts were base places and lands under the crew that started it, and crew SHALL post no land for it (record 0056).

#### Scenario: Beside a bolt that can land
- **WHEN** crew's bolts `y` and `w` read proven, `y` launched as a base place and `w` started by an older crew, with no launch of `bolt/w`
- **THEN** `land/crew` shows `y` ticked and `w` with no box, `w`'s row saying it was started before bolts were base places and lands under the crew that started it, and no raise posts a land of `w`

### Requirement: A landing the runner or Flume stopped keeps its box
A bolt whose land the runner answered refused, or whose submission Flume reports withdrawn or refused and waiting on its caller, as the runner's report carries it, SHALL keep its box (record 0056 decision 6). Its row SHALL say what stopped its landing at that head, in the runner's or Flume's words, nothing of the bolt's. The send that ticked it SHALL be spent: crew SHALL post no land of it again on that send.

#### Scenario: The runner refuses the land
- **WHEN** the user sent `land/crew` with `z` ticked, crew posted `z`'s land, and the runner answered it refused, a place on `bolt/z` being live
- **THEN** `z` keeps its box, its row says its landing at that head was stopped, in the runner's words, nothing of the bolt's, and no raise posts another land of `z` on that send

#### Scenario: Flume's submission withdrawn
- **WHEN** the runner's report carries `z`'s base place with its submission withdrawn, waiting on its caller
- **THEN** `z` keeps its box, and its row says its landing was stopped, in Flume's words, nothing of the bolt's

#### Scenario: A new card while it is stopped
- **WHEN** `z`'s landing was stopped and a card of crew's landings follows the one the user answered
- **THEN** the closed card's outcome names `z` as stopped, with what stopped it, and the card that follows has `z` as a row with its box, ticked as crew proposes, saying what stopped its last landing

#### Scenario: The head moves
- **WHEN** `z`'s landing was stopped at `abc1234` and `z`'s head moves to a new head that reads proven
- **THEN** `z`'s row says nothing of the stop

## MODIFIED Requirements

### Requirement: An answer wakes the owner, which acts on the user's word
An answer on a crew card SHALL be acted on by the role whose row it is, woken in its session by the card it adopted, and by no other: the planner applies or rewrites the proposal, and reads a batch's answer with `crew card read batch/<n>`; main-level ops passes a note on a kit's landings card naming a defect in a bolt to that bolt's conductor, who starts a fix on it; main-level ops runs the deploy's approval or the step's state; the design agent sets the record's status. No role SHALL land the bolts and fixes of main the user ticked on a kit's landings card: crew's own raise of the card posts their lands, as "The user's send on a kit's landings card posts one land for each row it lands" has it. crew SHALL then close the card at that act's event. No process of crew's SHALL wait on a card's answer. Where the role runs as its kind, the host's follower SHALL write an ask of the role for each change Pending You's notice names on a card in the role's name, once per version of the card, reading nothing of the card, and the role's next run SHALL read the card in the role's own name and act on it as the woken session would.

#### Scenario: A proposal approved from the phone
- **WHEN** the user approves the card for proposal 4 on the phone
- **THEN** the planner is woken, runs `crew plan answer` and `crew plan approve 4`, which closes the card with what was applied, and the rail's proposal row is gone

#### Scenario: Changes asked for on a review card
- **WHEN** the user writes a note on a batch's card asking for changes to unit `x`
- **THEN** the planner is woken, `crew card read batch/<n>` prints the note and closes the card, the conductor runs construct again with its words, and no approval is asked

#### Scenario: Landing approved
- **WHEN** the user leaves `a` and `c` ticked on `land/crew`, clears `b`, and sends
- **THEN** crew's next raise of `land/crew` posts a land of `a` and then one of `c`, `crew card read land/crew` prints them with their requests and no command, and no agent is asked to land or pass anything on

#### Scenario: A defect noted on a row
- **WHEN** the user's note on `land/crew` names a defect in bolt `b`
- **THEN** swancloud-ops tells `b`'s conductor the note's words, the conductor starts a fix on `b`, and `b`'s row is held for the fix

#### Scenario: A proposal approved while the planner runs as its kind
- **WHEN** madswan's planner runs as its kind, no run of it is live, and the user approves proposal 12's card on the phone
- **THEN** the host's follower, told by Pending You's notice, writes one ask of the planner naming the card's request, and the planner's next run reads the card in madswan-planner's name and runs `crew plan answer` and `crew plan approve 12`

### Requirement: A card is closed by crew at the event that ends it
crew SHALL close each of its cards at the event that ends what it asks, with a one-line outcome, and SHALL withdraw a row's card whose row is gone on the next rail read, with the reason. A declined approval SHALL be closed with the user's words when its owner reads it with `crew card read`. The outcome or reason crew sends with a close SHALL be cut to Pending You's 200 characters, and the run record SHALL keep it whole.

#### Scenario: An outcome longer than Pending You takes
- **WHEN** an approval's outcome, naming every unit it added and every one the user left out, runs past 200 characters
- **THEN** the card is acked with the outcome cut to 200 characters, ending with …, and the run record's close holds it whole

#### Scenario: A proposal approved from the phone
- **WHEN** the user approves `proposal/4` on the phone with its new unit `c` unticked, and the planner runs `crew plan answer 4 rows-1 b`
- **THEN** crew applies the proposal with `c` left out and closes the card "Applied: added b. Left out on your word: c.", and the rail's proposal row is gone

#### Scenario: A proposal dropped
- **WHEN** the planner runs `crew plan drop 4 "the user: not this quarter"`
- **THEN** the card is withdrawn with those words

#### Scenario: A bolt landed
- **WHEN** `y` is the one bolt the user ticked on `land/crew`, the runner's report carries `y`'s base place landed at its commit, and crew's next raise of `land/crew` reads it
- **THEN** `y` is closed in main-level ops's name, and `land/crew`'s card is closed naming `y` landed on GitHub's main at that commit and that every host's folder follows by swancloud's timer within minutes

#### Scenario: A deploy fails
- **WHEN** the deployer records the end of srv's deploy of `abc1234` with its `guests` step failed
- **THEN** `deploy/srv`'s card is closed "The deploy of abc1234 to srv failed at guests; its log: <its log>."

#### Scenario: A step done
- **WHEN** the user answers `op/srv/1` Done and main-level ops runs `crew ops step srv --key <key> --state done`
- **THEN** the card is closed "Done."

#### Scenario: A landing declined
- **WHEN** the user declines `land/y` with "not before the demo" and the conductor runs `crew card read land/y`
- **THEN** the command prints the decline and its words, and the card is closed with them

#### Scenario: A row gone under an open card
- **WHEN** `proposal/4`'s card is open and the proposal is dropped without its card closing
- **THEN** the next rail read withdraws the card, "its proposal was dropped", and says so

### Requirement: A card carries what the user reads and the row's answers
A proposal's card SHALL hold the proposal whole, picture, text and case, linking a reading session only when it holds more than fifteen new units. A batch's card SHALL link its one session. A landing's card SHALL link its one session, on what the bolt brings to main, first in its details and among its links, saying the reading lands nothing. A deploy's, a step's and a record's card SHALL link no session: each holds what the user decides from.

#### Scenario: A review card's options
- **WHEN** a unit's change is due for a batch
- **THEN** no review card offers its approval; the batch's card asks nothing and its notes go to the unit's team

#### Scenario: A review card's link
- **WHEN** a unit's change is read in batch 3
- **THEN** the batch's card carries the one link to batch 3's session, and no card carries a link to the unit alone

#### Scenario: Answered in the session rather than on the card
- **WHEN** the user annotates a unit's change in the batch's session and sends the annotations
- **THEN** the rail's refresh tells the planner to read batch 3, its `crew card read batch/3` prints them, they go to the unit's conductor as the user's words, and the batch's card is closed

#### Scenario: A proposal's card holds the proposal whole
- **WHEN** crew raises the card for proposal 4, which adds two units
- **THEN** the card carries the picture, the text and the case, and no session link

#### Scenario: A landing card links its reading
- **WHEN** crew raises bolt `y`'s landing card
- **THEN** it names the units and chores that land, sluice's verdict and when, and how far main has moved, as before; its details open with the link to `land/y`'s session and say the reading lands nothing; the link is among its links, after which sluice's pull request when it has one; and it is an approval of risk high, the approval being the word to land

#### Scenario: A landing approved without opening its reading
- **WHEN** the user approves `land/crew`'s card, its one row `y`, without opening `y`'s reading
- **THEN** crew's raise posts `y`'s land on that approval as on any send, and nothing waits on the reading

### Requirement: A refused landing is held on its row
A bolt whose landing Flume refused for its own content, its verdict at that head failed or in conflict as the runner's report carries it, SHALL be held on its row at that head with no box, in Flume's words, while the bolts after it go on (record 0056 point 4). A failed check's row SHALL say its landing was refused and the bolt is open for work, and that it waits for a fix on the bolt, which main-level ops starts with Flume's words. A conflict's row SHALL say it takes main first, its take-main fix launched once however often the refusal is read (bolt-teams "A landing that conflicts with main takes main in by a fix place"). crew SHALL post no land of it again at that head. Once its head moves and it reads proven, crew SHALL post its land on the user's send that ticked it when that send still stands for its work, and it SHALL otherwise have a box again. A landing whose outcome crew can't tell from the runner's report SHALL hold nothing: its row SHALL say its landing can't be told and why, and crew SHALL post no land of it again at that head (`read.1`). A landing that did not land for any other cause SHALL NOT hold its row. No row SHALL name a team.

#### Scenario: The second of three is refused
- **WHEN** the user sends `land/crew` with `y`, `z` and `w` ticked, and Flume's verdict on `z`'s submission is a conflict with main on `plugin/lib/plan.py`
- **THEN** `y` and `w` land, `z` stays on crew's landing row held with no box, saying in Flume's words that its landing was refused in conflict and that it takes main first, its take-main fix is launched once, and the next landings card raised carries `z` held with no box

#### Scenario: A check fails
- **WHEN** Flume's verdict on `z`'s submission is failed, waiting on its caller, its words naming `tests:logic`
- **THEN** `z` is held on its row with no box, saying its landing was refused and the bolt is open for work, in Flume's words, and that it waits for a fix on the bolt

#### Scenario: Submitted again with nothing submitted
- **WHEN** `z` was refused for a failed check at `977138a`, and later raises read the runner's report with `z` still at `977138a`
- **THEN** crew posts no land of `z` again, so nothing of it is submitted, and `z` is still held on its row with no box for a fix on the bolt, its row saying nothing of a stop

#### Scenario: The fix merges
- **WHEN** a fix taking main in, launched on `z`, merges into `z` and `z` reads proven at its new head, its own work unchanged since the user's send
- **THEN** `z` has no box on any landings card, and crew posts its land on that send

#### Scenario: A fix that changes the bolt's work merges
- **WHEN** `z` was refused for a failed check, and a fix on `z` commits a change and merges, and `z` reads proven at its new head
- **THEN** `z` has a box on `land/crew` again, its note naming the fix's commit

#### Scenario: A bolt the user left
- **WHEN** the user cleared `z` on their send of `land/crew`, and main then lands a change `z` also makes
- **THEN** `z` keeps its box on the card that follows, unticked, and is not held taking main first

#### Scenario: An outcome crew can't tell
- **WHEN** crew posted `z`'s land, and the branch of the runner that took `z`'s work can't be read
- **THEN** `z` is not held, its row says its landing can't be told and why, and no land of `z` is posted again at that head

### Requirement: The landings card closes when nothing waits
A landings card the user has answered SHALL be left as it is until every bolt they ticked has landed, been held or been stopped, then closed naming what landed and where GitHub's main holds it, what was held and why, what was stopped and in whose words, and what was left; a new card SHALL follow it while rows can land. The close SHALL keep the user's send for each ticked bolt that was held and still stands for its work, saying so. A send ticking none SHALL close it, landing nothing. With no row that can land, no card SHALL be open, and the next proven bolt SHALL raise one, following nothing.

#### Scenario: Everything ticked lands
- **WHEN** the user sent `land/crew` with `y` and `z` ticked and both land
- **THEN** the card is closed saying `y` and `z` landed and where GitHub's main holds them, and no landings card of crew is open

#### Scenario: One left out
- **WHEN** the user sent `land/crew` with `y` ticked and `z` cleared, and `y` lands
- **THEN** the card is closed saying `y` landed and `z` was left, and a new card follows it with `z` as its one row

#### Scenario: The next proven bolt
- **WHEN** no landings card of crew is open and bolt `w` reads proven
- **THEN** `land/crew` is posted with `w` as its one row, following no card

#### Scenario: A ticked bolt held at the close
- **WHEN** the user sent `land/crew` with `y` and `z` ticked, `y` lands and Flume refuses `z` for a failed check
- **THEN** the card is closed saying `y` landed and `z` was held and why, and that the send stands for `z` while its own work is unchanged

#### Scenario: A ticked bolt stopped at the close
- **WHEN** the user sent `land/crew` with `y` and `z` ticked, `y` lands and the runner answers `z`'s land refused
- **THEN** the card is closed saying `y` landed and `z` was stopped, in the runner's words, and a new card follows it with `z` as a row with its box

### Requirement: A ticked bolt's approval stands while its own work is unchanged
The user's send on a kit's landings card SHALL stand for each bolt they ticked, at any later head whose own work is the same as at the head they ticked. A bolt's own work SHALL be the non-merge commits its head holds that GitHub's main does not. A bolt whose send stands SHALL be no row of any later landings card, and crew SHALL post its land on that send once it reads proven at its new head, with no card asking for it.

#### Scenario: A refused bolt takes main in
- **WHEN** the user sent `land/crew` with `z` ticked at `abc1234`, Flume refused `z`'s landing in conflict with main, and `z`'s take-main fix, resolving the conflict in its merge, merged into `z`, which reads proven at `def5678`
- **THEN** no landings card asks for `z`, crew posts `z`'s land at `def5678` on that send, and `crew card read land/crew` names `z` among the bolts the user's earlier send lands, with that land's request

#### Scenario: The head moves by taking main in before the landing
- **WHEN** the user sent `land/crew` with `y` and `z` ticked, `y` is landing, and a take-main fix moves `z`'s head before crew posts its land
- **THEN** the card is left as it is, and once `z` reads proven at its new head crew posts its land on the same send

#### Scenario: The host's copy is brought level
- **WHEN** the user ticked `z` at the host copy's head `abc1234`, and the copy is brought level with GitHub's `def5678`, whose merges bring in only main's commits
- **THEN** the send stands for `z` at `def5678`

#### Scenario: Two take-main fixes in a row
- **WHEN** the user ticked `z` at `abc1234`, and two take-main fixes later `z` reads proven at `0a1b2c3`, holding the same commits of its own as at `abc1234`
- **THEN** the send stands for `z` at `0a1b2c3`

### Requirement: A card that follows one the user answered says so first
Every card crew posts that follows a card the user answered SHALL open its summary, and its details, with one paragraph saying that the user answered the earlier card, when the earlier card was posted and by when crew recorded their answer, what they answered, and what has changed since, before anything else the card says, so a card asked again is never read as a repeat. A card the user answered is one the run record shows closed after their answer, declined among them, and one whose follow-on crew withheld (below). What they answered SHALL be the answer crew recorded at the earlier card's close; where the run record holds none, the paragraph SHALL say crew holds no record of what they answered. What changed SHALL be the sentences the event that raised the card gives: a record's new commit; a proposal's rewrite read against the proposal it replaces; a deploy's newer head; a step's place after the card it follows; what the user's send on a kit's landings card landed, held, stopped and left, and the bolts proven or moved since.

#### Scenario: A record revised after the user's note
- **WHEN** the user answered record 0019's card `req_1`, posted 2026-10-23 13:10 UTC, with a note, crew recorded it by 14:02 UTC, and the design agent revises the record at `4be21c0`
- **THEN** the card that follows `req_1` opens "You answered the card before this one, posted 2026-10-23 13:10 UTC, by 14:02 UTC: declined, with a note. Since then: revised at 4be21c0", with the commit's subject, before the record's own opening

#### Scenario: A proposal rewritten after the user's note
- **WHEN** the user answered proposal 239's card with a note and the planner rewrites it as proposal 241, which adds unit `x` and no longer adds unit `y`
- **THEN** the card that follows says first what the user answered and that proposal 241 adds `x` and no longer adds `y`

#### Scenario: A deploy offered again after the user declined it
- **WHEN** the user declined deneb's deploy of `ddcf2cb` and the deployer offers deneb `e104bcf`
- **THEN** the new deploy card follows the declined one and opens saying the user declined `ddcf2cb`, when, and that the offer is now `e104bcf`

#### Scenario: The landings card after a send that left a bolt
- **WHEN** the user sent `land/crew` with `y` ticked and `z` cleared, and `y` lands
- **THEN** the card that follows opens saying the user sent the earlier card, when, ticking `y` and leaving `z`, and that `y` landed and `z`, which they left, waits on this card

#### Scenario: The landings card after a send whose bolt was stopped
- **WHEN** the user sent `land/crew` with `z` ticked, and the runner answered `z`'s land refused
- **THEN** the card that follows opens saying the user sent the earlier card, when, ticking `z`, and that `z`'s landing was stopped, in the runner's words, so `z` waits on this card

#### Scenario: An answer crew holds no record of
- **WHEN** a card that follows one the user answered is posted, and the run record's close of the earlier card holds no answer, as a close made before crew recorded answers
- **THEN** its opening says the user answered the earlier card, when, that crew holds no record of what they answered, and what changed since

### Requirement: A send stands for a ticked bolt taking main in
When the user has sent a landings card with a bolt ticked, and that bolt then takes main first, by a forecast or a take-main fix in flight, or they ticked it while its row took main first, crew SHALL keep the send standing for it: the card SHALL be left, and SHALL NOT be closed counting that bolt as held, while it takes main in. crew SHALL post no land of such a bolt while it still stands at the head the card showed or the run record holds a conflict at its head now, read where the bolt lives; once its take-main fix has moved it, its own work unchanged, and it reads proven, the next raise SHALL post its land on that send, and `crew card read land/<kit>` SHALL name it with that land's request.

#### Scenario: Ticked, then forecast to conflict
- **WHEN** the user sent `land/crew` with `y` ticked, and main moves so that `y` is forecast to conflict with it before a raise posts `y`'s land
- **THEN** `land/crew` is left as it is, its send still standing for `y`, no land of `y` is posted, and no agent is told

#### Scenario: Ticked beside one that lands
- **WHEN** the user sent `land/crew` with `y` and `z` ticked, `z` lands, and `y` takes main first
- **THEN** `land/crew` is left as it is while `y` takes main in, and is not closed saying `y` was held

#### Scenario: Ticked while taking main in
- **WHEN** the user sends `land/crew` with `y` ticked and `z`, shown taking main first, ticked too
- **THEN** `y` lands, the card is left while `z` takes main in, and `z` lands on that send once it reads proven, its own work unchanged

#### Scenario: Read after the take-main fix
- **WHEN** the run record holds `z` forecast to conflict with main at `abc1234`, the head the card showed, the user ticked `z`, and `z`'s take-main fix has moved it to `def5678`, with no conflict recorded there, and `z` reads proven
- **THEN** the next raise posts a land of `z` on that send, and `crew card read land/crew` names `z` with that land's request

### Requirement: A bolt the user left stays left until they tick it
A bolt SHALL be left when the user cleared it on their send of its kit's landings card, or when main-level ops recorded the user's words in its pane stopping its landing. It SHALL stay left, shown unticked on each card that follows, until the user ticks it on a later send, or until its head moves. crew SHALL move no left bolt's head: it starts no take-main fix for it while it is left.

#### Scenario: Cleared on a send
- **WHEN** the user sends `land/swancloud` with `x` ticked and `builds-reach-the-phone` cleared
- **THEN** `builds-reach-the-phone` is left, and the card that follows shows it unticked

#### Scenario: Left again
- **WHEN** the user sends the card that follows with `builds-reach-the-phone` cleared again
- **THEN** it stays left, unticked on the next card

#### Scenario: Main moves under it many times
- **WHEN** main moves five times while `builds-reach-the-phone` is left, each move conflicting with it
- **THEN** no take-main fix is started for it, its head stays where it was, and it stays left on the card, asked for no more than any other row

#### Scenario: Its head moves
- **WHEN** a fix its conductor started for a defect merges into a left bolt and it reads proven at the new head
- **THEN** it is no longer left, and the card asks for it as a row at its new head

### Requirement: A bolt stopped in ops's pane is shown as left
A bolt whose landing main-level ops recorded the user's words stopping SHALL be shown on its kit's landings card unticked, as a bolt the user left, at the head it had when the stop was recorded, and SHALL be treated as left until the user ticks it on a send.

#### Scenario: Stopped, then the card is raised
- **WHEN** ops records the user's words stopping `z`'s landing, and `land/crew` is raised
- **THEN** `z`'s row is unticked, the card's note says `z` was stopped on the user's words, and no take-main fix is started for it

#### Scenario: Ticked after a stop
- **WHEN** the user then ticks `z` on a send of `land/crew`
- **THEN** `z` is no longer left, and lands on that send or takes main first as any ticked bolt

### Requirement: A landing row carries what brings its bolt's preview up
Where the kit's policy at a bolt's head declares `[preview]`, the bolt's row on its kit's landings card SHALL carry what brings the preview up, the bolt's branch and its head, and SHALL say that the preview comes up only when the user asks for it on the card and goes when they are done. Where the policy declares none, the row SHALL say "no preview". crew SHALL ask sluice for nothing when it posts or changes the row.

#### Scenario: A kit that declares a preview
- **WHEN** bolt `y` reads proven at head `abc1234` in a kit whose policy at `abc1234` declares `[preview]`
- **THEN** `y`'s row on `land/crew` names `bolt/y` at `abc1234` as what brings its preview up, says to write on the card to bring it up, and sluice on the team's host lists no preview of `abc1234`

#### Scenario: A kit that declares none
- **WHEN** bolt `y` reads proven in a kit whose policy at its head has no `[preview]` table
- **THEN** `y`'s row says "no preview", and sluice is asked for nothing

#### Scenario: The policy can't be read
- **WHEN** the kit's policy at `y`'s head can't be read on the team's host
- **THEN** `y`'s row says its preview can't be told and why, and `y` keeps its box

#### Scenario: Approved without a preview
- **WHEN** the user sends `land/crew` with `y` ticked and never asked for its preview
- **THEN** crew posts `y`'s land as for any ticked row, and no preview of `y` was made

### Requirement: A row forecast to conflict with main takes main first until a fix takes main in
A row whose bolt is forecast to conflict with what the kit's main holds, by the card's forecast or by one the run record holds at the bolt's present head, SHALL take main first, saying so, the files, and that it does until a fix taking main in moves its head. The raise that first finds the conflict at a bolt head and revision of main SHALL record it once, as a `forecast` on the bolt, and SHALL tell no agent and start nothing: a fix taking main in is launched when Flume refuses the bolt's landing in conflict with main, as the runner's report carries it and "A landing that conflicts with main takes main in by a fix place" has it, or by a fix launched on the bolt by hand. It SHALL NOT be ticked or offered to land while it conflicts: beside a row that can land it SHALL stay on the card as an unticked box, as "A row taking main first changes the card in place" has it, and with none that can land it SHALL be held, no card raised for it. It SHALL be ticked as crew proposes again once the bolt reads proven at a new head with no conflict forecast. A conflict only with a bolt above it holds nothing. A row whose bolt the user left SHALL NOT take main first so: it keeps its box and says it would take main first, as "A row the user left says whether it would take main first" has it.

#### Scenario: Main landed a change the bolt also made
- **WHEN** `x` and `y` read proven, and main has landed a change to `openspec/specs/artifact-buckets/spec.md` that `y`'s own archive also changed
- **THEN** `land/crew` shows `y` unticked, saying `y` takes main first, forecast to conflict with main on `openspec/specs/artifact-buckets/spec.md`, until a fix taking main in moves its head, and `x` ticked; the run record gains one `forecast` on `bolt/y` at `y`'s head and main's revision; and no agent is told

#### Scenario: Raised again at the same heads
- **WHEN** the run record holds `y`'s forecast at `y`'s present head, and the card's own forecast against main could not be made
- **THEN** `y` still takes main first, in the recorded files, and nothing more is recorded

#### Scenario: Only a bolt above it
- **WHEN** `z` is forecast to conflict with `y`, the row above it, and with nothing on main
- **THEN** `z` is ticked, its row naming the conflict with `y`

#### Scenario: The fix merges
- **WHEN** a fix taking main in merges into `y` and `y` reads proven at its new head with no conflict forecast against main
- **THEN** `y` is ticked on `land/crew` again

#### Scenario: A bolt the user left
- **WHEN** the user cleared `z` on their send of `land/crew`, and main then lands a change `z` also makes
- **THEN** `z` keeps its box on the card that follows, unticked, and does not take main first

### Requirement: The sweep leaves an answered landings card while a bolt it ticked waits to land
The rail's sweep SHALL NOT close a kit's landings card the user answered while a bolt they ticked on it has neither landed nor been dropped, even when the kit's row is gone from the read. It SHALL leave the card, saying it waits on the runner to land what was ticked. The event that ends the send closes it.

#### Scenario: The row is gone for a moment
- **WHEN** the user approved `land/sluice`'s card ticking `a`, `a` has no `bolt.land` or `bolt.drop` since, and the rail's read finds no `land/sluice` row
- **THEN** the sweep leaves the card open and says it waits on the runner to land `a`; nothing is withdrawn

#### Scenario: The ticked bolt landed
- **WHEN** `a` has landed and no other ticked bolt waits, and the read finds no `land/sluice` row
- **THEN** the sweep closes the card as answered, saying `a` landed

## REMOVED Requirements

### Requirement: A landing sluice or its host stopped keeps its box
**Reason**: crew reads no record of sluice's and runs no landing (record 0056 points 1 and 5). A stop is read from the runner's report alone, and the send that ticked the bolt is spent, where this requirement kept it for main-level ops to submit again; a check that never ran carries no mark in Flume's verdict, which is the bolt's.
**Migration**: "A landing the runner or Flume stopped keeps its box" says what a stop does to its row and its send; a failed verdict is held as "A refused landing is held on its row" has it.
