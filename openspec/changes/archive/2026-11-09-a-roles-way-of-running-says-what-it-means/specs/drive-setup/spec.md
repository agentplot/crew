## MODIFIED Requirements

### Requirement: Every key is a flag, with no default
`crew drive set <label>` SHALL take every key crew's module writes for a drive, for the hosts it needs, and for this host's console and kept repositories of it, as a flag named as the file names the key. A flag for a key crew requires, and `--hosts`, SHALL be required; `--roles`, `--console` and `--repositories` SHALL be optional. No flag SHALL have a default.

#### Scenario: A person's Mac
- **WHEN** `crew drive set pat` runs on `pats-mac` with `--state pat/crew-state`, `--blueprints pat/blueprints`, `--machine pats-mac`, `--session pat`, `--folder /Users/pat/.local/share/herdr/pat`, `--repos pat/blueprints`, the account `pat` for each role, `--runs` `standing` for each role, `--review 5 4`, `--hosts pats-mac pats-mac darwin`, `--console /Users/pat/.local/share/herdr/pat` and `--repositories pat/blueprints` with the runner's container and view
- **THEN** the teams file names the drive `pat` with those keys, its `runs` naming every role `standing` and its `review` giving `after_changes` 5 and `after_hours` 4, `hosts` names `pats-mac`, `consoles` names `pat`, `repositories` names `pat/blueprints`, and crew loads the file

### Requirement: A flag crew does not accept is refused before anything is read
`--accounts` and `--runs` SHALL each be given once for each of the five main-level roles, `design`, `planner`, `reviewer`, `ops` and `operator`, and for no other, `--runs` giving each `standing` or `on-demand`. `--review` SHALL be given once, as `<after_changes> <after_hours>`, a whole number of at least 1 and a number above 0. `--flume` SHALL be refused as an argument crew does not take. A flag left out, given more often than its count, or given a value crew does not accept for its key SHALL be refused naming the flag, before anything is read or written.

#### Scenario: A flag left out
- **WHEN** `crew drive set pat` is given every flag but `--folder`
- **THEN** it is refused naming `--folder`, and nothing is read or written

#### Scenario: An account left out
- **WHEN** `crew drive set pat` gives `--accounts` for `design`, `planner`, `ops` and `operator`, and none for `reviewer`
- **THEN** it is refused naming `--accounts` and the reviewer, and nothing is written

#### Scenario: A way of running crew does not take
- **WHEN** `crew drive set pat` gives `--runs planner false`, or `--runs planner pat-work`
- **THEN** it is refused naming `--runs` and the planner, saying a role runs `standing` or `on-demand`, and nothing is read or written

#### Scenario: A batch setting out of range
- **WHEN** `crew drive set pat` gives `--review 0 4` or `--review 5 0`
- **THEN** it is refused naming `--review` and the value with its unit and range, and nothing is read or written

#### Scenario: The former flag
- **WHEN** `crew drive set pat` gives `--flume design false` beside every flag it takes
- **THEN** it is refused naming `--flume` as an argument crew does not take, and nothing is read or written
