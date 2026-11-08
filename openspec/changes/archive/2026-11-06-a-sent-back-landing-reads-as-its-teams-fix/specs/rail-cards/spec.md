## MODIFIED Requirements

### Requirement: A refused landing is held on its row
A bolt whose landing sluice refused for its own content, its submission in conflict or blamed for a check that ran and failed, SHALL be held on its row at that head, with no box, the row saying its landing was rejected and the bolt is open for work, sluice's words, and that it waits for a fix on the bolt, while the bolts after it go on. A later submit at that head that submitted nothing SHALL leave it held. Once its head moves and it reads proven, it SHALL land on the user's send that ticked it when that send still stands for its work, and SHALL otherwise have a box again. A landing that did not land for any other cause SHALL NOT hold its row. No row SHALL name a team.

#### Scenario: The second of three is refused
- **WHEN** the user sends `land/crew` with `y`, `z` and `w` ticked, and sluice refuses `z` for a conflict on `plugin/lib/plan.py`
- **THEN** `y` and `w` land, `z` stays on crew's landing row held with no box, saying its landing was rejected and the bolt is open for work, with sluice's words, and that it waits for a fix on the bolt, and the next landings card raised carries `z` held with no box

#### Scenario: A check fails
- **WHEN** sluice blames `z`'s landing for `tests:logic`, which ran and failed
- **THEN** `z` is held on its row with no box, saying its landing was rejected and the bolt is open for work, with sluice's words, and that it waits for a fix on the bolt

#### Scenario: Submitted again with nothing submitted
- **WHEN** `z` was refused at `977138a`, and a later `crew bolt submit z` at `977138a` is recorded stopped with no submission of sluice's
- **THEN** `z` is still held on its row with no box for a fix on the bolt, and the row says nothing of a stop

#### Scenario: The fix merges
- **WHEN** a fix taking main in, launched on `z`, merges into `z` and `z` reads proven at its new head, its own work unchanged since the user's send
- **THEN** `z` has no box on any landings card and lands on that send

#### Scenario: A fix that changes the bolt's work merges
- **WHEN** `z` was refused for a failed check, and a fix on `z` commits a change and merges, and `z` reads proven at its new head
- **THEN** `z` has a box on `land/crew` again, its note naming the fix's commit

#### Scenario: A bolt the user left
- **WHEN** the user cleared `z` on their send of `land/crew`, and main then lands a change `z` also makes
- **THEN** `z` keeps its box on the card that follows, unticked, and is not held taking main first
