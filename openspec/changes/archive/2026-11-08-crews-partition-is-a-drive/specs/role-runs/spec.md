## MODIFIED Requirements

### Requirement: An ask is a record naming a role
An ask SHALL be a record of `asks.rec` on the drive's branch, written through crew as every write there is: its number, the role it asks, who or what asks, what kind of ask it is, the record it names where it names one, its key where it must be written once, the words it carries where it carries any, and when it was written.

#### Scenario: A malformed ask
- **WHEN** a write would add an ask with no role
- **THEN** `recfix --check` refuses it and nothing is committed

### Requirement: A tell, a notice or a send to a role that runs as its kind is an ask
A `crew tell` to a role its drive runs as its kind, by an agent or the user, and every notice crew sends it, SHALL be written as an ask of the role from the sender, `crew` for a notice, carrying the text; a `crew send` to the drive SHALL be an ask of its operator carrying whom it was sent to and the text. Nothing SHALL be typed into any pane for it.

#### Scenario: A tell to the planner
- **WHEN** madswan's planner runs as its kind, no standing agent of it is up, and madswan-design runs `crew tell madswan-planner "record 0053 is accepted"`
- **THEN** an ask of the planner from madswan-design holds those words, nothing is typed into any pane, and the command says it asked madswan-planner

#### Scenario: crew's own notice
- **WHEN** a proposal of madswan's is approved and the planner runs as its kind
- **THEN** an ask of the planner from crew says the proposal was approved, where today the planner is told

### Requirement: The follower hears Pending You's notice while a role here runs as its kind
The host's follower SHALL run Pending You's notice of changes on the host's cards, `pendingyou watch`, while a drive whose main level runs on its host runs a role as its kind, and only then.

#### Scenario: A role here runs as its kind
- **WHEN** madswan's main level runs on deneb and its planner runs as its kind
- **THEN** deneb's follower runs `pendingyou watch` for as long as it holds the host's follower lock

#### Scenario: No role here runs as its kind
- **WHEN** no drive whose main level runs on deneb runs a role as its kind
- **THEN** deneb's follower runs no `pendingyou watch`

### Requirement: A role that stands is asked nothing
For a role its drive does not run as its kind, no tell, notice, send, capture, landing, card's answer, opening or batch SHALL write an ask: each SHALL do what it does today.

#### Scenario: A role still standing
- **WHEN** wldn's planner stands, and `crew tell wldn-planner "<text>"` runs
- **THEN** the text is typed into wldn-planner's pane as today, and no ask is written

### Requirement: A tell finds a standing agent of the role first
A tell to a role its drive runs as its kind SHALL be typed into a standing agent of it that is still up, as a tell is today, and written as an ask only once crew has read that none is up. When crew cannot read whether one is up, the tell SHALL refuse, naming what it could not read, and write nothing.

#### Scenario: The standing agent not yet stopped
- **WHEN** madswan's planner was named to run as its kind a minute ago, its standing agent is still up and idle, and the design agent tells it
- **THEN** the text is typed into the standing agent's pane, and no ask is written

### Requirement: A role record names its run
`roles.rec` on the drive's branch SHALL hold one record for each role its drive runs as its kind, naming its address, `<label>/<role>`; its run's name, `<label>-<role>`; the main level's host; the drive's first blueprints repository as the teams file names it; crew's kinds and the kind `crew-<role>`; the place's name, `<label>`; the stream the drive's `flume` names for the role; the priority 0; the intent `<label>-<role>`; and the role's model and effort.

#### Scenario: The planner's record
- **WHEN** madswan runs its planner as its kind and its record is written
- **THEN** it names `madswan/planner`, `madswan-planner`, deneb, `afterthought/blueprints`, `crew-planner`, `madswan`, the intent `madswan-planner` and Opus 5.5

### Requirement: A run's start gives its brief and what it took
`crew role start` SHALL write the role's brief, filled for its drive as `crew-role` fills it, to a file on the host, and print the file's path to read whole first, then each ask it took, oldest first, with who asked, what, the record it names and its words, then each place that waits on the role, with its work, its place and its words, and last the role's answered cards, read in the role's own Pending You name, each with its key and the answer.

#### Scenario: What the planner's run reads
- **WHEN** the planner's start took an ask from the design agent and a card's answer
- **THEN** it prints the brief's path, then the design agent's words, then the card's ask, then the card's key and the user's answer, read in madswan-planner's name

### Requirement: A run is named as its role
A run SHALL be named `<label>-<role>`, `<label>-ops` for main-level ops, read from the place it runs in, `crew-<role>--<label>`, the place its role record named, for a role its drive runs as its kind. Every crew command the run makes SHALL take that name and drive as a standing agent's `CREW_AGENT` and `CREW_LABEL` give them: the plan's role table, the cards' owners and the run record's entries SHALL treat the run as the role, and a command forwarded to another host SHALL carry them.

#### Scenario: The planner's run proposes
- **WHEN** the planner's run runs `crew plan propose <file>`
- **THEN** the proposal is the planner's, its card is raised in madswan-planner's name, and a direct plan write by the run is refused as the planner's is

#### Scenario: A place of another kind
- **WHEN** a crew command runs in a fix's place with no `CREW_AGENT`
- **THEN** it names no role as its caller

### Requirement: A run's brief says how a turn goes
A role's brief SHALL say, for a role that runs as its kind, that its turn starts with `crew role start`, acts on what that took, and ends with `crew role end`; that it waits in its session on nothing, and that what it would have waited for, an answer, a submission, a review or a tell, reaches its next run as an ask; and that it asks the user only on a card in its own name. For a standing role it SHALL say that its work reaches it as tells and cards in its pane.

#### Scenario: Every brief filled
- **WHEN** each of the five briefs prints for a drive that runs all five as their kinds
- **THEN** each holds the turn's words, and no token is left unfilled
