## MODIFIED Requirements

### Requirement: The module writes crew's teams file from options named as the file names them
With `services.crew.enable`, the module SHALL write crew's teams file from `services.crew.settings`, each key named as the file names it: `drives`, given as an attribute set keyed by each drive's label and written as the file's list of drives in the order of their labels, each with its `label`; `repositories`, where the host gives its kept repositories; and `version`, which the module SHALL set to the version `plugin/lib/crew.py` reads and which no host SHALL set. The file SHALL be the settings as JSON with every unset key left out, so that for the same drives, listed in the order of their labels, and the same repositories it holds the same bytes the fleet's writer gives.

#### Scenario: deneb's drives
- **WHEN** `services.crew.settings.drives` names afterthought, agentplot and madswan on deneb and wldn on chuck-herdr-alpha, with its planner in `wldn-1`, as deneb's teams file held them on 2026-11-07
- **THEN** the module's file holds, byte for byte, `nix/tests/files/deneb.json`, the bytes of deneb's `~/.config/crew/teams.json` read that day as version 6 holds them, its drives listed under `drives` in the order of their labels, each with its `label` and none naming a `partition`, and a drive that gives no `roles` has no `roles` key, and the file has no `repositories` key

#### Scenario: A runner host's kept repositories
- **WHEN** `services.crew.settings` gives deneb's drives and `repositories` naming `agentplot/crew` and `afterthought/swancloud`, each with its runner's container as `dir` and its runner's view as `checkout`
- **THEN** the module's file holds, byte for byte, `nix/tests/files/runner.json`

#### Scenario: crew reads the file the module writes
- **WHEN** crew loads `nix/tests/files/deneb.json` as its teams file, beside a hosts file naming those sessions
- **THEN** it loads four drives, afterthought, agentplot, madswan and wldn, wldn's planner and reviewer in `wldn-1`, and every role of every drive standing

#### Scenario: crew reads the kept repositories the module writes
- **WHEN** crew loads `nix/tests/files/runner.json` as its teams file on deneb, beside the same hosts file
- **THEN** it loads the four drives, and names crew's and swancloud's folder and checkout on deneb as the file's `dir` and `checkout`

#### Scenario: The version is crew's
- **WHEN** a host's settings set `version`
- **THEN** evaluation fails, and the version the module writes is the one `plugin/lib/crew.py` reads

## REMOVED Requirements

### Requirement: Every drive is listed once, with every key crew requires
**Reason**: The drives are keyed by label (design, Decision 1), so a label cannot be listed twice, and the list's own failures, a label twice among them, no longer apply. Another module now gives a drive's `machine` and `state` by its label (agentplot/boomdrive record 0032).
**Migration**: Requirement "Every drive gives every key crew requires" keeps every key crew requires without a default and the `flume` and `teams` failures; requirement "Every drive is named once, by its label" keeps the `partitions` failure and adds the keyed drives' own. A host lists its drives under `services.crew.settings.drives.<label>`, each without a `label`.

## ADDED Requirements

### Requirement: Another module gives a drive its machine and its state repository
A drive's `machine` and `state` SHALL each be written once: by the host's own settings, or by another module that gives them under the drive's label in `services.crew.settings.drives`, the drive's other keys staying in the host's settings under that label. Where either is written more than once at the same priority, the values equal or not, evaluation SHALL fail.

#### Scenario: deneb's drives from two modules
- **WHEN** one module gives each of deneb's four drives its `machine` and its `state`, and the host's settings give each drive its `blueprints`, `session`, `review` and `flume`, and wldn its `roles`, and neither gives a key the other gives
- **THEN** the module's file holds, byte for byte, `nix/tests/files/deneb.json`, and no assertion fails

#### Scenario: A machine written twice
- **WHEN** another module gives agentplot its `machine` `deneb`, and the host's settings also give agentplot the `machine` `deneb`
- **THEN** evaluation fails

#### Scenario: A state repository written twice
- **WHEN** another module gives agentplot its `state` `afterthought/crew-state`, and the host's settings also give agentplot the `state` `afterthought/crew-state`
- **THEN** evaluation fails

### Requirement: A drive another module gives is configured in the host's settings
A drive that another module gives its `machine` and `state`, for which the host's settings give none of crew's own keys, SHALL fail evaluation, as a drive that lacks a key crew requires.

#### Scenario: A drive given and not configured
- **WHEN** another module gives a drive `extra` its `machine` and its `state`, and the host's settings name no drive `extra`
- **THEN** evaluation fails

### Requirement: Every drive is named once, by its label
The module SHALL take the drives under `services.crew.settings.drives` alone, as an attribute set keyed by each drive's label, and SHALL take a drive's `label` from its name, which no host SHALL set. It SHALL fail evaluation for a drive's name that is not a name crew accepts, a `label` the host sets, drives given as a list, and drives under `partitions` with no `drives`, and SHALL fail evaluation, naming `services.crew.settings.drives`, where it names no drive.

#### Scenario: A label the host sets
- **WHEN** the host's settings give the drive `madswan` the `label` `madswan`
- **THEN** evaluation fails

#### Scenario: A name crew does not accept
- **WHEN** `services.crew.settings.drives` names a drive `Madswan`
- **THEN** evaluation fails

#### Scenario: Drives as a list
- **WHEN** `services.crew.settings.drives` is a list of deneb's drives, each with its `label`
- **THEN** evaluation fails

#### Scenario: Drives under `partitions`
- **WHEN** `services.crew.settings` lists the drives under `partitions` and gives no `drives`
- **THEN** evaluation fails

#### Scenario: No drive
- **WHEN** `services.crew.settings.drives` names no drive
- **THEN** evaluation fails, naming `services.crew.settings.drives`

### Requirement: Every drive gives every key crew requires
The module SHALL give no default for a key crew requires of a drive (`blueprints`, `state`, `machine`, `session`, `review` and `flume`) and SHALL declare no `partition` option for a drive. It SHALL fail evaluation for a drive that lacks one of those keys and for a `flume` that names a role crew has no kind for or gives a role neither `false` nor a stream's name, and SHALL fail evaluation, saying so, for a `teams` key, which the version crew reads has no place for.

#### Scenario: A drive with no state repository
- **WHEN** a drive under `services.crew.settings.drives` gives no `state`, and no other module gives it one
- **THEN** evaluation fails

#### Scenario: A drive with no machine
- **WHEN** a drive under `services.crew.settings.drives` gives no `machine`, and no other module gives it one
- **THEN** evaluation fails

#### Scenario: A role crew has no kind for
- **WHEN** a drive's `flume` names `dispatcher`, or gives `planner` the value `true`
- **THEN** evaluation fails

#### Scenario: Teams
- **WHEN** `services.crew.settings` gives `teams`
- **THEN** evaluation fails, saying the teams file crew reads has no place for teams
