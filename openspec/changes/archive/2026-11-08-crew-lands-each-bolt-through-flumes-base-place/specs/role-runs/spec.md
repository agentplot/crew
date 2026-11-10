## ADDED Requirements

### Requirement: Main-level ops's run lands nothing
Main-level ops's run SHALL land, submit and wait on nothing for a bolt or a fix of main: the user's send of a row on a kit's landings card is carried to the runner by crew's own act, whether or not a run of ops stands (record 0056 point 5), and each landing's end SHALL reach ops's next run only as the ask crew's read of the runner's report writes for it. Ops's brief, for a partition that runs ops as its kind, SHALL say so in its turn's words and SHALL name no `crew bolt submit`.

#### Scenario: The turn's words
- **WHEN** main-level ops's brief prints for a partition that runs ops as its kind
- **THEN** its turn's words say that a landing's end reaches ops's next run as an ask when it does not land, and the planner's and the design agent's when it does, and it names no `crew bolt submit`

#### Scenario: A send while no run of ops stands
- **WHEN** ops runs as its kind, no run of it stands, and the user sends `land/crew` with `y` ticked
- **THEN** `y`'s land is posted by crew's raise of the card, which waits on no run of ops

## MODIFIED Requirements

### Requirement: A capture and a landing are asks
A signal captured through crew SHALL be an ask of a design agent that runs as its kind, one per signal, keyed by the signal's id. A bolt's landing, as crew's read of the runner's report records it, SHALL be an ask of a planner and of a design agent that run as their kinds, keyed by the bolt. A landing crew's read records refused or stopped SHALL be an ask of a main-level ops that runs as its kind, with Flume's or the runner's words, keyed by the land's request, so an outcome read twice asks once (record 0056 point 4).

#### Scenario: A landing
- **WHEN** the runner reports a swancloud bolt's base place landed and crew's read records the landing, while swancloud's planner and design agent run as their kinds
- **THEN** that write holds an ask of the planner and one of the design agent, each naming the bolt

#### Scenario: A landing that conflicts
- **WHEN** ops runs as its kind, the user's send of bolt `y` was carried to the runner as land request 57, and the runner reports `y`'s base place refused for a conflict with main
- **THEN** crew's read writes one ask of ops naming `bolt/y` with Flume's words, keyed by request 57, however often the outcome is read, and ops's next run takes it

#### Scenario: A land the runner refused
- **WHEN** ops runs as its kind, and the runner answers `y`'s land request 57 refused, a place on `bolt/y` still live
- **THEN** crew's read records `y`'s landing stopped and writes one ask of ops naming `bolt/y` with the runner's words, keyed by request 57

## REMOVED Requirements

### Requirement: Main-level ops's landing from a run does not wait
**Reason**: Main-level ops's run lands nothing: `crew bolt submit` refuses whatever it is given, and crew leaves no landing's waiter on any host (record 0056 points 1 and 5; design Decisions 1 and 4).
**Migration**: A landing's end reaches ops's next run as the ask crew's read of the runner's report writes (requirement "A capture and a landing are asks"), and the run's brief says ops lands nothing (requirement "Main-level ops's run lands nothing").
