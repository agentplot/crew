## MODIFIED Requirements

### Requirement: A role record names its run
`roles.rec` on the drive's branch SHALL hold one record for each role its drive runs as its kind, naming its address, `<label>/<role>`; its run's name, `<label>-<role>`; the main level's host; the drive's first blueprints repository as the teams file names it; crew's kinds and the kind `crew-<role>`; the place's name, `<label>`; the stream, the drive's own, named by its label; the priority 0; the intent `<label>-<role>`; and the role's model and effort.

#### Scenario: The planner's record
- **WHEN** madswan runs its planner as its kind and its record is written
- **THEN** it names `madswan/planner`, `madswan-planner`, deneb, `afterthought/blueprints`, `crew-planner`, the place's name `madswan`, the stream `madswan`, the intent `madswan-planner` and Opus 5.5

### Requirement: Role records follow the teams file
crew SHALL write `roles.rec` to match the teams file at `crew main up` and in the commit of an ask whose role's record is missing or differs, and SHALL remove the record of a role the teams file no longer runs as its kind.

#### Scenario: The planner moves
- **WHEN** madswan's teams entry's `runs` names its planner `on-demand`, and `crew main up madswan` runs
- **THEN** `roles.rec` on `madswan/main` holds the planner's record

#### Scenario: An ask before main up
- **WHEN** the teams entry's `runs` names the planner `on-demand`, no record of it is on the branch, and a tell to the planner writes an ask
- **THEN** the ask's commit holds the planner's record too

#### Scenario: The planner stands again
- **WHEN** madswan's teams entry's `runs` names the planner `standing` again, and `crew main up madswan` runs
- **THEN** `roles.rec` holds no record of the planner

### Requirement: A role's work that lands is a place it launches
`crew role land <repo> <name> --brief-file <file>`, run in a role's run, SHALL launch through the runner a place of Flume's own chore kind in that repository, on its default branch, its brief the file's text whole, the run's address its recipient and the drive's own stream, named by its label, its stream. A repository neither the teams file nor the plan names SHALL be refused, and so SHALL a run outside a role's run. No role's run SHALL submit to sluice.

#### Scenario: The design agent's records
- **WHEN** madswan's design run writes the text of a record and its rule's amendment to a file and runs `crew role land afterthought/crew record-0053 --brief-file <file>`
- **THEN** a chore launch in `afterthought/crew` on its default branch is written for the runner, with the file's text as its brief, `madswan/design` as its recipient and `madswan` as its stream
