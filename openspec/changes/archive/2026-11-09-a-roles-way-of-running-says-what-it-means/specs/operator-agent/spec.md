## MODIFIED Requirements

### Requirement: The operator is a main-level role
The drive's operator, `<label>-operator`, SHALL be a role of its main level: while it stands, `crew main up <label>` SHALL start it in an `operator` tab of the `<label>` workspace, beside the design agent, the planner and ops, and greet it once it is up as it greets them; `crew main down <label>` SHALL end it; `crew revive` SHALL bring it back as it brings them back. While its drive's `runs` names it `on-demand`, so that it runs as its kind, it SHALL run as a role's run does, on an ask, and none of these SHALL start it. Every brief SHALL name it as the drive's operator, and crew SHALL start no other operator agent for the drive.

#### Scenario: The main level comes up with its operator
- **WHEN** `crew main up wldn` runs
- **THEN** `wldn-operator` starts in the `wldn` workspace's `operator` tab and is greeted once, beside `wldn-design`, `wldn-planner` and `wldn-ops`

#### Scenario: A conductor waits on the user with no card
- **WHEN** a conductor of wldn stops on a question asked only in its pane
- **THEN** its brief has it tell `wldn-operator`, the drive's one operator

#### Scenario: The operator runs as its kind
- **WHEN** madswan's `runs` names its operator `on-demand` and `crew main up madswan` runs
- **THEN** no `operator` tab is opened and no operator is started, and a tell to `madswan-operator` is an ask of its role

### Requirement: The operator's brief says who changes the drives on its host
The operator's brief SHALL say that where its host's `~/.config/crew/teams.json` is a file and not a link into the Nix store, as Boomdrive's setup leaves a person's Mac, a drive is added or changed through Boomdrive's setup on the user's word, which gives crew the drive's entry with `crew drive set`, and that the operator edits no teams file by hand; it SHALL name no drive's removal there. Its steps through swancloud's `lib/crew-teams.nix` SHALL be said for a teams file that is such a link. Among what a drive's entry says, the brief SHALL name how each of its roles runs, `runs`, `standing` or `on-demand`, and its batch setting, `review`, by `after_changes` and `after_hours`, and SHALL name no `flume` as a key of the teams file.

#### Scenario: The operator's brief
- **WHEN** a drive's operator brief is built
- **THEN** its *Changing the drives* says a drive on a host whose teams file is no link into the Nix store is added or changed through Boomdrive's setup, which writes crew's entry with `crew drive set`, never by a hand edit, and says the swancloud steps for a teams file that is such a link

#### Scenario: No removal through setup
- **WHEN** a drive's operator brief is built
- **THEN** its *Changing the drives* names no drive removed through Boomdrive's setup

#### Scenario: What a drive's entry says
- **WHEN** a drive's operator brief is built
- **THEN** its *Changing the drives* names `runs`, `standing`, `on-demand`, `after_changes` and `after_hours`, and no `` `flume` ``
