## ADDED Requirements

### Requirement: A capture and a bolt's landing are asks
A signal captured through crew SHALL be an ask of a design agent that runs as its kind, one per signal, keyed by the signal's id. A bolt's landing, as crew's read of the runner's report records it, SHALL be an ask of a planner and of a design agent that run as their kinds, keyed by the bolt.

#### Scenario: A landing
- **WHEN** the runner reports a swancloud bolt's base place landed and crew's read records the landing, while swancloud's planner and design agent run as their kinds
- **THEN** that write holds an ask of the planner and one of the design agent, each naming the bolt

### Requirement: A landing refused or stopped is an ask of ops
A landing crew's read records refused or stopped SHALL be an ask of a main-level ops that runs as its kind, with Flume's or the runner's words, keyed by the land's request, so an outcome read twice asks once (record 0056 point 4).

#### Scenario: A landing that conflicts
- **WHEN** ops runs as its kind, the user's send of bolt `y` was carried to the runner as land request 57, and the runner reports `y`'s base place refused for a conflict with main
- **THEN** crew's read writes one ask of ops naming `bolt/y` with Flume's words, keyed by request 57, however often the outcome is read, and ops's next run takes it

#### Scenario: A land the runner refused
- **WHEN** ops runs as its kind, and the runner answers `y`'s land request 57 refused, a place on `bolt/y` still live
- **THEN** crew's read records `y`'s landing stopped and writes one ask of ops naming `bolt/y` with the runner's words, keyed by request 57

### Requirement: A run's start prints its brief's path, then what it took in order
`crew role start` SHALL write the role's brief, filled for its drive as `crew-role` fills it, to a file on the host, and print the file's path to read whole first, then each ask it took, oldest first, with who asked, what, the record it names and its words, then each place that waits on the role, with its work, its place and its words, then the ends it took, and last the role's answered cards, read in the role's own Pending You name, each with its key and the answer.

#### Scenario: What the planner's run reads
- **WHEN** the planner's start took an ask from the design agent and a card's answer
- **THEN** it prints the brief's path, then the design agent's words, then the card's ask, then the card's key and the user's answer, read in madswan-planner's name

### Requirement: A run's start prints a line for each launch whose ends it took
`crew role start` SHALL print the ends it took that Flume holds for the role, one line for each launch, with its work, its place, its request and each end's key, an expired end marked so, saying they are confirmed when the turn ends.

#### Scenario: The ends it took
- **WHEN** the planner's start took an ask and unit `a`'s construct's and code's ends of request 12, the code's expired
- **THEN** after the ask it prints one line for unit `a` naming its place and request 12, `stage/construct/1/delivered` and `stage/code/1/delivered` marked expired, and that they are confirmed when the turn ends

## REMOVED Requirements

### Requirement: A capture and a landing are asks
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A capture and a bolt's landing are asks" and "A landing refused or stopped is an ask of ops".

### Requirement: A run's start gives its brief and what it took
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A run's start prints its brief's path, then what it took in order" and "A run's start prints a line for each launch whose ends it took".
