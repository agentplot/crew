## ADDED Requirements

### Requirement: A row held by Flume's landing fix says so
A row whose bolt's base place has a landing fix live SHALL be held with no box, saying which fix and what it does: taking main in for a forecast or a conflict, the row taking main first, or making the failed checks pass for a failed submission, in Flume's words. A row whose landing was refused and whose landing fix is due SHALL be held at the refused head, saying Flume launches its landing fix. A row past the bound SHALL be held, saying Flume ran its landing fixes and the bolt waits on ops.

#### Scenario: Taking main in by Flume's fix
- **WHEN** `y`'s base place lists `y-1`, for a conflict, live, and `x` can land
- **THEN** `land/crew` shows `y` unticked, taking main first, naming `y-1` taking main in, and `x` ticked

#### Scenario: A failed check's fix
- **WHEN** `y`'s base place lists `y-1`, for a failed check, live
- **THEN** `y`'s row has no box and says it is held for Flume's landing fix `y-1`, which makes the failed checks pass, in Flume's words

#### Scenario: Due
- **WHEN** `y`'s landing was refused for a failed check at its head and its landing fix is due
- **THEN** `y`'s row has no box and says Flume launches its landing fix

## MODIFIED Requirements

### Requirement: A row forecast to conflict with main takes main first until a fix takes main in
A row whose bolt is forecast to conflict with what the kit's main holds, by the card's forecast or by one the run record holds at the bolt's present head, SHALL take main first, saying so, the files, and that it does until a fix taking main in moves its head. The raise that first finds the conflict at a bolt head and revision of main SHALL record it once, as a `forecast` on the bolt, and SHALL tell no agent and start nothing. A fix taking main in is launched in one of three ways:
- by Flume, as the bolt's landing fix, on Flume's own forecast or on its refusal of the bolt's landing, where the bolt's base place names a landing fix;
- by crew, when Flume refuses the bolt's landing in conflict with main and the base place names none, as the runner's report carries it and "A landing that conflicts with main takes main in by a fix place" has it;
- by a fix launched on the bolt by hand.

The row SHALL NOT be ticked or offered to land while it conflicts. Beside a row that can land it SHALL stay on the card as an unticked box, as "A row taking main first changes the card in place" has it. With none that can land it SHALL be held, and no card raised for it. It SHALL be ticked as crew proposes again once the bolt reads proven at a new head with no conflict forecast. A conflict only with a bolt above it holds nothing. A row whose bolt the user left SHALL NOT take main first so: it keeps its box and says it would take main first, as "A row the user left says whether it would take main first" has it.

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

#### Scenario: Flume's forecast fix
- **WHEN** `y` is forecast to conflict with main and its base place lists `y-1`, for a forecast, live
- **THEN** `y` takes main first, naming `y-1` taking main in, and crew appends no launch for it

#### Scenario: A bolt the user left
- **WHEN** the user cleared `z` on their send of `land/crew`, and main then lands a change `z` also makes
- **THEN** `z` keeps its box on the card that follows, unticked, and does not take main first
