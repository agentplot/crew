## ADDED Requirements

### Requirement: A proven bolt not marked to stay lands on proof, its land posted by the card's raise
Each raise of a kit's landings card SHALL post, by one plan write in main-level ops's name after its sends' lands, a `land` of each bolt that can land, its forecast made and clear of main, not marked to stay, not left by the user, with no land posted at its head now and no hold on its drive or kit at the write's tip, in the plan's order, at any hour (record 0067, `plan.16`). Such a bolt SHALL be no row of the card, and no agent SHALL run anything for it.

#### Scenario: Proven at night
- **WHEN** bolt `y` of crew, not marked to stay, reads proven at `abc1234` at 03:10, every unit's latest change having been in a batch the user answered, and the raise of `land/crew` forecasts it clear of main
- **THEN** that raise appends one land of `y`'s launch to `requests.rec`, recorded in the run record as asked on proof, no card asks for `y`, and no agent is told to run anything

#### Scenario: Read again
- **WHEN** a later raise reads `y` at `abc1234`, its land on proof posted and not answered
- **THEN** it posts no land

#### Scenario: Forecast to conflict with main
- **WHEN** the raise's forecast finds `y` in conflict with main at `abc1234`
- **THEN** no land of `y` is posted, the conflict is recorded, `y` takes main first, and once it reads proven at a new head forecast clear of main, the next raise posts its land on proof

#### Scenario: A forecast not made
- **WHEN** the raise of `land/crew` cannot make `y`'s forecast against main, git not telling
- **THEN** no land of `y` is posted, the raise says the forecast could not be made and why, and the next raise once a forecast finds `y` clear of main posts its land on proof

#### Scenario: Beside a bolt marked to stay
- **WHEN** bolts `y` and `z` of crew read proven, `z` marked to stay, both forecast clear of main
- **THEN** the raise posts `y`'s land on proof, and `land/crew` asks for `z` alone

#### Scenario: Beside a send
- **WHEN** the user sent `land/crew` ticking `z`, marked to stay, and `y`, not marked, reads proven
- **THEN** one raise posts `z`'s land on the send and then `y`'s on proof, in one plan write each

### Requirement: The rail's read raises a kit whose proven bolt is due a land on proof
On the main level's host, each rail read SHALL raise once each kit whose land row holds a bolt that can land, not marked to stay, not left by the user, with no land posted at its head now, and no hold on its drive or kit. A kit holding none SHALL be raised by none of this.

#### Scenario: Proven since the last read
- **WHEN** bolt `y` of crew, not marked to stay, reads proven on the main level's host, no card of crew open
- **THEN** that rail read raises `land/crew`, whose raise posts `y`'s land on proof, and the next read raises none for `y`

#### Scenario: Proven while a card asks for a bolt marked to stay
- **WHEN** `land/crew` waits on the user with `z`, marked to stay, and `y`, not marked, reads proven
- **THEN** the rail read raises `land/crew`, which posts `y`'s land on proof and leaves the card's rows as they stand

#### Scenario: Under a hold
- **WHEN** a hold on crew stands and `y` reads proven
- **THEN** no rail read raises `land/crew` for `y`

### Requirement: A landings card asks only about the rows a send must land
A kit's landings card SHALL ask only about bolts marked to stay, bolts the user left, bolts whose land on proof at their head was stopped, and fixes of main, each with the rows taking main first beside them as this spec has it. Each requirement of this spec on a landings card's row SHALL hold of those rows alone, and a bolt that lands on proof SHALL be no row of it.

#### Scenario: A bolt not marked beside one marked
- **WHEN** bolts `y` and `z` of crew read proven, `z` marked to stay
- **THEN** `land/crew` is an approve naming `z` alone, and `y` is no row of it

#### Scenario: A land on proof stopped
- **WHEN** crew posted `y`'s land on proof at `abc1234` and the runner answered it refused, a place on `bolt/y` being live
- **THEN** `land/crew` asks for `y` with its box, its row saying its land on proof at `abc1234` was stopped, in the runner's words, nothing of the bolt's, no raise posts another land of `y` at that head, and the user's send lands it, a stop of crew's land on proof spending no send of theirs

#### Scenario: A bolt the user left
- **WHEN** the user left `y`, not marked to stay, on their send of an earlier card, and `y` reads proven
- **THEN** `land/crew` shows `y` unticked, and no land on proof is posted for `y` while it is left

#### Scenario: Taking main first
- **WHEN** `y`, not marked to stay, is forecast to conflict with main, and `z`, marked, can land
- **THEN** `land/crew` asks for `z` alone, and `y` is no row of it

### Requirement: A bolt that landed on proof is told on its kit's landings card
Each bolt that landed on proof SHALL be told on its kit's landings card, naming it and the commit its kit's main holds after it, until the user answers or taps a card that told it. With no row to ask about, the card SHALL be a one-tap notice that asks nothing. With rows, the told bolts SHALL open the card's face. A told bolt SHALL hold the card open by itself.

#### Scenario: A notice
- **WHEN** `y` landed on proof, crew's main holding `9f1c2ab` after it, and no row of crew waits
- **THEN** `land/crew` is a notice in swancloud-ops's name that asks nothing, naming `y` and `9f1c2ab`

#### Scenario: Another lands while the notice is open
- **WHEN** the notice naming `y` is open and `w` lands on proof
- **THEN** the notice is changed in place, naming `y` and then `w`

#### Scenario: The user taps it
- **WHEN** the user taps the notice naming `y` and `w`
- **THEN** it is closed, and no later card tells `y` or `w`

#### Scenario: A bolt marked to stay reads proven while the notice is open
- **WHEN** the notice naming `y` is open and `z`, marked to stay, reads proven
- **THEN** a card following the notice asks for `z`, and its face opens naming `y` as landed on proof

#### Scenario: Followed before the user saw it
- **WHEN** a card telling `y` is followed or withdrawn before the user answered or tapped it
- **THEN** the next card of crew's landings still tells `y`

### Requirement: A hold on the drive or the kit posts no land
While a hold the user put on a drive or a kit stands (bolt-plan), crew SHALL post no land of its bolts or its fixes of main, on proof or on a send. A send made meanwhile SHALL stand. Its lands, and each land due on proof, SHALL be posted by the first raise after the hold is lifted.

#### Scenario: Proven under a hold
- **WHEN** the user put a hold on crew, saying "Cutover", and `y`, not marked to stay, reads proven
- **THEN** no land of `y` is posted, and `y`'s land line says the hold on crew holds it, "Cutover"

#### Scenario: A send under a hold
- **WHEN** a hold on crew stands and the user sends `land/crew` ticking `z`
- **THEN** no land of `z` is posted, and `crew card read land/crew` says the send stands and lands `z` once the hold on crew is lifted

#### Scenario: The hold lifted
- **WHEN** the user runs `crew plan go --repo crew --label swancloud`, `y` still proven and the send ticking `z` standing
- **THEN** the raise of `land/crew` that the lift hands posts `z`'s land on the send and then `y`'s on proof

#### Scenario: The drive's hold outlasts the kit's
- **WHEN** holds on the drive swancloud and on its kit crew stand, and the user lifts crew's
- **THEN** no land of crew's bolts is posted while the drive's hold stands

#### Scenario: A card followed under a hold
- **WHEN** a hold on crew stands, the user sent `land/crew` ticking `z`, and `w`, marked to stay, reads proven since
- **THEN** the card is closed saying the user's send stands for `z`, no land asked while the hold stands, and a card following it asks for `w`

#### Scenario: A hold put while a raise posts
- **WHEN** the user puts a hold on crew while a raise of `land/crew` is posting `y`'s land on proof
- **THEN** the raise's write, applied to a tip that holds the hold, posts no land

## RENAMED Requirements

- FROM: `### Requirement: A landings card is open only while a row can land`
- TO: `### Requirement: A landings card is open only while a row can land or a landing on proof is untold`

## MODIFIED Requirements

### Requirement: Each kit has one landings card in main-level ops's name, its rows in plan order
crew SHALL keep one landings card for each kit with a row it asks about waiting on its main, or a bolt landed on proof to tell, keyed `land/<kit>`, in the name of the drive's main-level ops, posted on the drive's main host. Rows SHALL be in the plan's order. The card SHALL ask only for the landing.

#### Scenario: Sluice's pull request
- **WHEN** sluice's submission at `y`'s head has pull request #23 on the kit's GitHub
- **THEN** `y`'s row links it, titled as sluice's pull request for `y`'s landing, on the card's face and in its details

#### Scenario: No pull request
- **WHEN** the kit's sluice opens no pull request for a submission
- **THEN** the row carries no link, and says nothing of one

#### Scenario: Two green bolts of one kit
- **WHEN** bolts `y` and `z` of crew, both marked to stay, read proven, `y` first in the plan
- **THEN** one card keyed `land/crew` is open in swancloud-ops's name, its rows `y` then `z`, and no card is open under `land/y` or `land/z`

#### Scenario: Bolts of two kits
- **WHEN** bolt `y` of crew and bolt `w` of swancloud, both marked to stay, read proven
- **THEN** `land/crew` holds `y`, `land/swancloud` holds `w`, and each is its own card

#### Scenario: A row carries what the bolt's card carried
- **WHEN** bolt `y` of swc-1, marked to stay, holding units `a` and `b` read in batch 7 and chore `c`, reads proven at `abc1234`, the landing of its work there made at 10:02, with pull request #23, main moved two landings since `y` was cut
- **THEN** `y`'s row names swc-1-conductor, `a`, `b` and `c (chore)`, batch 7, `abc1234` green since 10:02, two landings, pull request #23 linked, and `y`'s reading's link

#### Scenario: A second bolt is proven while the card waits
- **WHEN** `land/crew` waits on the user with one row, `y`, and bolt `z` of crew, marked to stay, reads proven
- **THEN** the card becomes a list of `y` and `z`, posted following the one it replaces since a card's kind does not change in place, with a change note naming `z`

#### Scenario: A row's head moves while the card waits
- **WHEN** `land/crew` waits on the user as a list of `y` and `z`, and a fix's merge moves `z`'s head to `def5678`
- **THEN** the card is changed in place, its note saying `z`'s head is now `def5678`, and `z`'s row carries its reading of `def5678` and `bolt/z` at `def5678` as what brings its preview up

#### Scenario: A yes frees the team for its next bolt
- **WHEN** swc-1's bolt `y` is a row of `land/crew`, and the last unit of swc-1's other bolt `z`, marked to stay, merges with sluice green at its head, and `d` is the next planned bolt of swc-1's kit
- **THEN** `y`'s row says a yes frees swc-1 for `d`

#### Scenario: Only bolts landed on proof
- **WHEN** no bolt of crew waits to land, and `y` landed on proof, unseen by the user
- **THEN** `land/crew` is open in swancloud-ops's name as a notice telling `y`, asking nothing

### Requirement: A bolt is a row that can land once its work is merged, read and verified
A bolt SHALL be a row that can land once every unit and chore of it has merged, every unit's latest change has been in a batch whose card the user has answered, its verification is green, its head the landing of its work as the runner reports it (merge-gate "A bolt's verification is its work's landing at its head, as the runner reports it alone"), and no fix of it is in flight.

#### Scenario: A green bolt
- **WHEN** every unit and chore of bolt `y` of crew, marked to stay, has merged, each unit's latest change has been in a batch the user has answered, `y`'s head `abc1234` is the landing of its last unit as the runner reports it, and no other bolt of crew can land
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

#### Scenario: Not marked to stay
- **WHEN** `y`, not marked to stay, reads proven as in "A green bolt"
- **THEN** no card asks for `y`: its land is posted on proof

### Requirement: A landings card is open only while a row can land or a landing on proof is untold
A send ticking none SHALL close the landings card, landing nothing. With no row that can land and no bolt landed on proof left to tell, no card SHALL be open, and the next row the card asks about, or the next bolt landed on proof, SHALL raise one, following nothing.

#### Scenario: The next proven bolt
- **WHEN** no landings card of crew is open and bolt `w`, marked to stay, reads proven
- **THEN** `land/crew` is posted with `w` as its one row, following no card

#### Scenario: The next landing on proof
- **WHEN** no landings card of crew is open and `y` lands on proof
- **THEN** `land/crew` is posted as a notice telling `y`, following no card

#### Scenario: Nothing to ask and nothing to tell
- **WHEN** `land/crew` waits on the user with `z`, marked to stay, the user lifts `z`'s mark, `z` lands on proof, and the user taps the notice that tells it
- **THEN** no card of crew's landings is open

### Requirement: A landings row is due one land for each send and head
A row of a kit's landings card SHALL be due a land when its box was ticked on a send that stands for it at its head now, it can land, and no land of its launch stands undecided or was posted at that head, but a land stopped there on proof or on another send, which bars no send. A send read twice SHALL post once, and a send that stands through a take-main fix SHALL post again once the bolt reads proven at its new head. A write replayed on a tip that already holds the lands SHALL write nothing.

#### Scenario: The send read again
- **WHEN** a later raise reads the user's send on `land/crew` with `y` and `z` still at the heads they were ticked at, their lands posted
- **THEN** it posts no land

#### Scenario: A ticked bolt taking main in
- **WHEN** the user ticked `z` at `abc1234`, Flume refused `z`'s landing in conflict with main, and `z`'s take-main fix merged, so `z` reads proven at `def5678` with its own work unchanged
- **THEN** no land of `z` is posted while it takes main in, and the first raise after it reads proven at `def5678` posts one land of `z` on that send

#### Scenario: A stopped row on the same send
- **WHEN** the runner answered `z`'s land on the user's send refused
- **THEN** no raise posts another land of `z` on that send

#### Scenario: A send at the head of a stopped land on proof
- **WHEN** crew's land on proof of `y` at `abc1234` was stopped by the runner, and the user sends `land/crew` ticking `y`, still at `abc1234`
- **THEN** the next raise posts one land of `y` at `abc1234` on that send

#### Scenario: A later card at the head of a stopped land
- **WHEN** `z`'s land on the user's send of one card was stopped at `abc1234`, and they send the card that follows it ticking `z`, still at `abc1234`
- **THEN** the next raise posts one land of `z` at `abc1234` on that later send

#### Scenario: A write replayed
- **WHEN** the plan write posting `y`'s land is applied again to a tip that already holds that land
- **THEN** it writes nothing
