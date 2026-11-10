## ADDED Requirements

### Requirement: A standing operator comes up and goes down with its main level
The drive's operator, `<label>-operator`, SHALL be a role of its main level: while it stands, `crew main up <label>` SHALL start it in an `operator` tab of the `<label>` workspace, beside the design agent, the planner and ops, and greet it once it is up as it greets them; `crew main down <label>` SHALL end it; `crew revive` SHALL bring it back as it brings them back.

#### Scenario: The main level comes up with its operator
- **WHEN** `crew main up wldn` runs
- **THEN** `wldn-operator` starts in the `wldn` workspace's `operator` tab and is greeted once, beside `wldn-design`, `wldn-planner` and `wldn-ops`

### Requirement: An operator its drive runs as its kind runs on an ask
While its drive runs the operator as its kind, the operator SHALL run as a role's run does, on an ask, and none of `crew main up <label>`, `crew main down <label>` and `crew revive` SHALL start it.

#### Scenario: The operator runs as its kind
- **WHEN** madswan's `flume` names a stream for its operator and `crew main up madswan` runs
- **THEN** no `operator` tab is opened and no operator is started, and a tell to `madswan-operator` is an ask of its role

### Requirement: Every brief names the drive's one operator
Every brief SHALL name `<label>-operator` as the drive's operator, and crew SHALL start no other operator agent for the drive.

#### Scenario: A conductor waits on the user with no card
- **WHEN** a conductor of wldn stops on a question asked only in its pane
- **THEN** its brief has it tell `wldn-operator`, the drive's one operator

### Requirement: A send reaches the operator of the drive it names, marked as a tell
`crew send <drive> "<text>"` SHALL deliver the text to the operator of the drive it names by its label, `<label>-operator`, wherever that agent runs. The text SHALL arrive marked as every tell is, `[crew tell from <sender>]`, the sender being the agent that ran the command or `<user>@<host>`, followed by `(sent to <drive>)`, then the text.

#### Scenario: An agent sends to another drive
- **WHEN** `swancloud-planner` runs `crew send wldn "The zone check fails on tenants with no region"`
- **THEN** `wldn-operator` is prompted with `[crew tell from swancloud-planner] (sent to wldn) The zone check fails on tenants with no region`

#### Scenario: A drive by its label
- **WHEN** the user, at a shell on mac-studio, runs `crew send wldn "<text>"`
- **THEN** `wldn-operator` is prompted with `[crew tell from <user>@mac-studio] (sent to wldn) <text>`

### Requirement: A send to no drive or to the operator's own drive is refused
A name that is no drive's label SHALL be refused by `crew send`, naming the drives there are. A send by the operator to its own drive SHALL be refused, saying it carries with `crew tell`.

#### Scenario: A name crew does not know
- **WHEN** an agent runs `crew send swb-1 "<text>"`, a team's name from before teams left
- **THEN** nothing is sent, and crew says it sends to a drive by its label, naming each

#### Scenario: The door sends to itself
- **WHEN** `wldn-operator` runs `crew send wldn "<text>"`
- **THEN** nothing is sent, and crew says it is wldn's door and carries with `crew tell`

### Requirement: A send types nothing to an operator that cannot take it
An operator that is not up, or waits on a question in its pane, SHALL get nothing typed by `crew send`, and the send SHALL fail saying so, as a tell does. To a drive that runs its operator as its kind, with no standing operator up, the send SHALL be written as an ask of the operator from the sender, carrying whom it was sent to and the text, and SHALL not fail for the operator not being up.

#### Scenario: The operator waits on a question
- **WHEN** an agent sends to wldn while `wldn-operator` waits on a question in its pane
- **THEN** nothing is typed, and the send fails saying the operator waits on a question and to send again once it is answered

#### Scenario: An operator that runs as its kind
- **WHEN** madswan runs its operator as its kind, no standing operator of it is up, and swancloud-planner runs `crew send madswan "<text>"`
- **THEN** an ask of madswan's operator from swancloud-planner holds `(sent to madswan)` and the text, and nothing is typed

### Requirement: The operator carries what is sent to it in the sender's words
The operator SHALL carry what reaches it by `crew send` on to the agent whose job it is, in the sender's words and naming the sender: a finding becomes a signal it records, quoting the words as sent; a design question goes to the design agent; work to build, or a message about a bolt's work, to the planner; a landing, a deploy or an operation to main-level ops. It SHALL NOT answer it in the sender's place or reason it out itself.

#### Scenario: A message about a bolt's work
- **WHEN** `wldn-operator` receives `[crew tell from swancloud-planner] (sent to wldn) <text about a wldn bolt>`
- **THEN** it tells `wldn-planner` the text, saying it is from `swancloud-planner`

#### Scenario: A finding
- **WHEN** what is sent reports a defect, with no request
- **THEN** the operator records it as a signal, its excerpt the words as sent

### Requirement: An operator on a box sends a teams change to a drive on a Mac
A request to change the teams file, from an operator whose main level runs on a box, SHALL be sent with `crew send` to a drive whose main level runs on a Mac that keeps swancloud's checkout.

#### Scenario: A teams change from a box
- **WHEN** the operator's brief prints for wldn, whose main level runs on the box
- **THEN** its *Changing the drives* says a request to change the teams file is sent with `crew send <label> "<the request>"` to one of `madswan` and `swancloud`, which reaches that drive's operator

## REMOVED Requirements

### Requirement: The operator is a main-level role
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A standing operator comes up and goes down with its main level", "An operator its drive runs as its kind runs on an ask" and "Every brief names the drive's one operator".

### Requirement: Anything sent to another drive reaches its operator
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A send reaches the operator of the drive it names, marked as a tell", "A send to no drive or to the operator's own drive is refused" and "A send types nothing to an operator that cannot take it".

### Requirement: The operator carries what is sent to it to the role whose job it is
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "The operator carries what is sent to it in the sender's words" and "An operator on a box sends a teams change to a drive on a Mac".
