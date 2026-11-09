## MODIFIED Requirements

### Requirement: A host can be held
`crew hold <host>|--all "<why>"` SHALL hold each host named, or every host crew runs agents on, the hosts of its drives' main levels: crew SHALL start no agent there until `crew go`, refusing with the hold's words every command that would, and SHALL tell every standing agent up there to finish the step it is in and start nothing new. With `--now` crew SHALL end every crew agent there at once. The run record SHALL name the host and never the why.

#### Scenario: Held
- **WHEN** the user runs `crew hold deneb "herdr 0.9.6"`
- **THEN** each main-level agent up on deneb is told the hold, and `crew main up swancloud` on deneb is refused naming who held it and why

#### Scenario: Held at once
- **WHEN** the user runs `crew hold --all "reboot" --now`
- **THEN** every crew agent on every host crew runs agents on is ended, and each is brought back by `crew go`

### Requirement: A standing agent of a role that now runs as its kind is ended at its next stop
A standing agent whose drive now runs its role as its kind SHALL be ended at its next stop, once herdr reads it idle with no question open and no background work of its own but crew's waits, told that its role now runs as its kind, and started again by nothing: no restart, no `crew revive`, no `crew update`. Nothing SHALL be ended on a held host.

#### Scenario: The planner moves
- **WHEN** madswan's teams entry comes to name a stream for its planner while `madswan-planner` stands, and it ends its turn
- **THEN** `madswan-planner` is ended, its pane is left with no agent started in it, and its log says its role now runs as its kind

#### Scenario: An update after the move
- **WHEN** `crew update` runs on deneb after madswan's planner has moved
- **THEN** no planner of madswan is restarted or started
