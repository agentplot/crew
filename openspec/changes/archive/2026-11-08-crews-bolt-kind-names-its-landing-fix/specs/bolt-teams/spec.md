## ADDED Requirements

### Requirement: A bolt's landing fix is read from its base place's status
crew SHALL read a started bolt's landing fix from Flume's status of its base place as the runner carries it, and from nothing else: the fix kind, the bound, and each fix Flume launched, with its cause and how it ended. Each fact SHALL be guarded, and a fix crew can't read whole SHALL be named, never guessed (`read.1`, `read.2`). A status that names no fix kind SHALL read as a base place whose landing fix Flume does not launch (`runner.landing_fix`, `code.7`).

#### Scenario: A host whose Flume names no fix kind
- **WHEN** the runner carries `y`'s base place as Flume 0.17.0 gives it, verdict failed
- **THEN** `y`'s landing reads refused for a failed check, its way on crew's

#### Scenario: A landing fix live
- **WHEN** the runner carries `y`'s base place with verdict conflict on `#412`, fix kind `flume/fix@1`, bound 3, and fix `y-1` for `#412` live
- **THEN** `y`'s landing reads refused for a conflict, its way on Flume's, with `y-1` live

#### Scenario: A landing fix due
- **WHEN** the runner carries `y`'s base place with verdict failed on `#412`, fix kind `flume/fix@1`, bound 3, and no fix
- **THEN** `y`'s landing reads refused, its way on Flume's, its landing fix due

#### Scenario: The bound spent
- **WHEN** the runner carries `y`'s base place with verdict failed on `#415`, bound 3, and three fixes, none for `#415`
- **THEN** `y`'s landing reads refused, its way on its caller's, naming three landing fixes run

#### Scenario: A fix dropped
- **WHEN** the runner carries `y`'s base place with verdict conflict on `#412` and fix `y-1` for `#412` dropped
- **THEN** `y`'s landing reads refused, its way on its caller's, naming `y-1` dropped

#### Scenario: A fix crew can't read
- **WHEN** a fix in `y`'s base place's status gives an end crew does not read
- **THEN** that fix is named as unread and counted toward no outcome

### Requirement: crew launches no fix and asks for none where Flume launches the landing fix
Where a refused landing's way on is Flume's, its landing fix live, landed or due within its bound, the first act of crew's that reads it SHALL record the refusal as before, and SHALL launch no take-main fix and ask main-level ops nothing.

#### Scenario: Flume's fix takes main in
- **WHEN** a raise of `land/crew` reads `y`'s landing refused for a conflict with `y-1` live
- **THEN** the run record gains `y`'s `bolt.submit` refused, `requests.rec` gains no launch, and ops is asked nothing

#### Scenario: Flume's fix due
- **WHEN** a raise reads `y`'s landing refused for a failed check, its landing fix due
- **THEN** no launch is appended and ops is asked nothing

### Requirement: A landing past its landing fixes is ops's
Where a refused landing's way on is its caller's, Flume's bound of landing fixes spent or its fix for the refusal dropped or not launched, the first act of crew's that reads it SHALL ask main-level ops once, keyed by the land's request, in Flume's words, naming how many landing fixes ran or how the fix ended, and SHALL launch no take-main fix.

#### Scenario: Past the bound
- **WHEN** a raise reads `y`'s landing refused with its three landing fixes run
- **THEN** ops is asked once, its words naming three landing fixes and Flume's words, and no launch is appended

#### Scenario: Read twice past the bound
- **WHEN** a later read finds the same refusal past the bound
- **THEN** ops is not asked again

### Requirement: A live landing fix holds its bolt
A live landing fix of a bolt's base place SHALL be a fix in flight on the bolt: its row SHALL have no box, no land of the bolt SHALL be posted while it is live, and a drop of the bolt the runner refused SHALL not be asked again until it has ended. Its note SHALL take main in for a forecast or a conflict, so the row takes main first and the send that ticked it stands through it, and SHALL name the failed checks for a failed submission.

#### Scenario: No land while it runs
- **WHEN** the user's send stands for `y` and `y-1` is live
- **THEN** no land of `y` is posted

#### Scenario: Taken main in
- **WHEN** `y-1`, which took main in, has landed and `y` reads proven at its new head with its own work unchanged
- **THEN** the next raise posts one land of `y` on the send that ticked it, asking the user nothing

#### Scenario: A drop while it runs
- **WHEN** the runner answered `y`'s drop refused and `y-1` is live
- **THEN** no plan write asks the drop again until `y-1` has ended

## MODIFIED Requirements

### Requirement: A landing Flume's verdict sent back is the bolt's fix
A landing whose verdict Flume gives as failed or conflict SHALL be the bolt's fix until a fix moves its head. crew SHALL name what failed in Flume's words and give the way on. Where the base place names a landing fix within its bound, the way on is Flume's landing fix. Where it names none, it is the take-main fix crew launches for a conflict, or the `crew fix` ops starts for a failed check. Past the bound, it is the fix ops starts. No land SHALL be posted at the head sent back. Once a fix has moved the head and the bolt reads proven, a land SHALL be posted again only as rail-cards has the send stand. No word SHALL name a team or a conductor.

#### Scenario: A check fails
- **WHEN** the runner carries `z`'s base place, as Flume 0.17.0 gives it, with `#7`'s verdict failed, Flume's words naming `tests:logic`, tested on main at `db8bc25`
- **THEN** `crew bolts` says `z` did not land, that a failed check is the bolt's, in Flume's words, and that ops starts `crew fix z <name> "<Flume's words>"`, naming no team or conductor

#### Scenario: A check fails with Flume's landing fix
- **WHEN** the runner carries `z`'s base place with `#7`'s verdict failed and its landing fix `z-1` for `#7` live
- **THEN** `crew bolts` says `z` did not land, in Flume's words, and that Flume's landing fix `z-1` makes the failed checks pass, naming no command for ops

#### Scenario: Read again at the head sent back
- **WHEN** the send that ticked `z` is read again while `z`'s head is still the one `#7` sent back
- **THEN** no land of `z` is posted, and `z` stays held on its row for its fix

#### Scenario: A conflict read again before its fix merged
- **WHEN** `z`'s landing was sent back for a conflict with main on `README.md`, its take-main fix was launched, crew's or Flume's, and the kit's landings card is raised again before that fix has merged
- **THEN** no land of `z` is posted and no second take-main fix is launched, its row saying it takes main first

#### Scenario: The take-main fix moves the head
- **WHEN** `z`'s take-main fix, crew's or Flume's, has merged and `z` reads proven at its new head
- **THEN** the next raise of its kit's landings card posts one land of `z` on the send that ticked it, asking the user nothing

### Requirement: A landing that conflicts with main takes main in by a fix place
When the runner's report has a started bolt's landing refused by Flume's verdict conflict, and its base place names no landing fix, the first act of crew's that reads it SHALL append a launch of a fix on the bolt named `take-main-<main's revision, seven>`, in its kit's repository and naming no host or stream, its brief saying to take `origin/main` into the bolt with Flume's words of the conflict, unless a fix of that name already stands. Where the base place names a landing fix, Flume's landing fix SHALL take main in and crew SHALL append nothing. The bolt's row SHALL say it takes main first.

#### Scenario: A landing refused for a conflict
- **WHEN** a raise of the kit's landings card reads the runner carrying `x`'s base place, naming no landing fix, with the verdict conflict against main at `4d3d9be`
- **THEN** `requests.rec` gains one launch of `fix` named `x--take-main-4d3d9be` with Flume's words of the conflict, and `x`'s row says it takes main first

#### Scenario: Read twice
- **WHEN** a later read of the same verdict finds `x--take-main-4d3d9be` standing
- **THEN** no second launch is appended

#### Scenario: Refused with Flume's landing fix
- **WHEN** a raise reads `x`'s base place with the verdict conflict against main at `4d3d9be` and its landing fix `x-1` live
- **THEN** `requests.rec` gains no launch, and `x`'s row says it takes main first, naming `x-1`

### Requirement: A base place's drop the runner refused is asked again once nothing on its branch is live
Where the runner answered a bolt's drop refused, as Flume refuses it while a place on the bolt's branch is live, the next plan write that finds the bolt gone from the plan, its launch standing, no piece of it live and no landing fix of its base place live SHALL ask the drop again, once for each refusal (`runner.base_drop_due`).

#### Scenario: A refused drop asked again
- **WHEN** the runner answered `x`'s drop refused while `a`'s place was live, and a later plan write finds `x` gone from the plan, its launch standing and no place of its pieces live
- **THEN** that write appends one drop of `x`'s launch, and a write after it, while that drop is unanswered, appends none

#### Scenario: Not while a piece is live
- **WHEN** the runner answered `x`'s drop refused and `a`'s place is still live
- **THEN** no plan write asks the drop again

#### Scenario: Not while a landing fix is live
- **WHEN** the runner answered `x`'s drop refused and `x`'s base place lists its landing fix `x-1` live
- **THEN** no plan write asks the drop again, and the first write after `x-1` has ended appends one
