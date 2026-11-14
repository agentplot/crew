## ADDED Requirements

### Requirement: A send to another host's drive runs on the sender's host
`crew send <drive>` SHALL run on the host it is invoked on, never forwarded, for every drive that host's teams file names, whichever machine runs it. Where the drive's operator runs on another machine, crew SHALL type the send there through `ssh -o BatchMode=yes` and herdr, and SHALL run no crew command there while herdr lists the operator by its name.

#### Scenario: A send from a box to a Mac's drive
- **WHEN** chuck-herdr-alpha's teams file names swancloud, whose main level runs on mac-studio, with no console for it, and `wldn-planner` runs `crew send swancloud "<text>"` on chuck-herdr-alpha
- **THEN** `swancloud-operator` on mac-studio is prompted with `[crew tell from wldn-planner] (sent to swancloud) <text>` through ssh from chuck-herdr-alpha and herdr on mac-studio, and no crew command runs on mac-studio

## MODIFIED Requirements

### Requirement: Every brief names one way to send to another drive
Every brief SHALL say in one line, beside its roster, that anything for another drive is sent with `crew send <drive> "<text>"`, run on the agent's own host and never over ssh, which reaches that drive's operator wherever it runs, and that it is sent nowhere else. A main level's brief SHALL count every drive but its own. No brief SHALL tell an agent to tell another drive's operator by name.

#### Scenario: The planner's brief
- **WHEN** `crew brief wldn planner` prints
- **THEN** it says beside the roster that anything for another drive goes with `crew send`, run on its own host and never over ssh, and names no team

#### Scenario: The operator's brief on a box
- **WHEN** the operator's brief prints for a drive whose main level runs on a box
- **THEN** its request to change the teams file goes with `crew send` to a drive named by its label, not with `crew tell` to another operator

### Requirement: A send to no drive or to the operator's own drive is refused
A name that is no drive's label in the host's teams file SHALL be refused by `crew send`, naming the drives the file names and saying that a drive another host runs is sent to once that file on this host names it, never by `crew send` run on that host over ssh, and that nothing was sent. A send by the operator to its own drive SHALL be refused, saying it carries with `crew tell`.

#### Scenario: A name crew does not know
- **WHEN** an agent runs `crew send swb-1 "<text>"`, a team's name from before teams left
- **THEN** nothing is sent, and crew says it sends to a drive by its label, naming each

#### Scenario: A drive the host's teams file does not name
- **WHEN** chuck-herdr-alpha's teams file names wldn alone, and `wldn-planner` runs `crew send afterthought "<text>"` there
- **THEN** nothing is sent, and crew names wldn, the teams file on chuck-herdr-alpha, and that a drive another host runs is sent to once that file names it, never by `crew send` run on that host over ssh

#### Scenario: The door sends to itself
- **WHEN** `wldn-operator` runs `crew send wldn "<text>"`
- **THEN** nothing is sent, and crew says it is wldn's door and carries with `crew tell`
