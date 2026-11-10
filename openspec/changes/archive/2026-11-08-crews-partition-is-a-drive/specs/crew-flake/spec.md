## RENAMED Requirements

- FROM: `### Requirement: Every partition is listed once, with every key crew requires`
- TO: `### Requirement: Every drive is listed once, with every key crew requires`


## MODIFIED Requirements

### Requirement: The module writes crew's teams file from options named as the file names them
With `services.crew.enable`, the module SHALL write crew's teams file from `services.crew.settings`, each key named as the file names it: `drives`; `repositories`, where the host gives its kept repositories; and `version`, which the module SHALL set to the version `plugin/lib/crew.py` reads and which no host SHALL set. The file SHALL be the settings as JSON with every unset key left out, so that for the same drives and repositories it holds the same bytes the fleet's writer gives.

#### Scenario: deneb's drives
- **WHEN** `services.crew.settings.drives` lists afterthought, agentplot and madswan on deneb and wldn on chuck-herdr-alpha, with its planner in `wldn-1`, as deneb's teams file held them on 2026-11-07
- **THEN** the module's file holds, byte for byte, `nix/tests/files/deneb.json`, the bytes of deneb's `~/.config/crew/teams.json` read that day as version 6 holds them, its drives under `drives` and none naming a `partition`, and a drive that gives no `roles` has no `roles` key, and the file has no `repositories` key

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

### Requirement: Every drive is listed once, with every key crew requires
The module SHALL give no default for a key crew requires of a drive (`label`, `blueprints`, `state`, `machine`, `session`, `review` and `flume`), SHALL declare no `partition` option for a drive, and SHALL list the drives under `drives` alone, and SHALL fail evaluation, naming what is wrong, for a drive that lacks one, a label listed twice, a `flume` that names a role crew has no kind for or gives a role neither `false` nor a stream's name, and a `teams` key, which the version crew reads has no place for.

#### Scenario: A drive with no state repository
- **WHEN** a drive in `services.crew.settings.drives` gives no `state`
- **THEN** evaluation fails, naming `state`

#### Scenario: A label twice
- **WHEN** `services.crew.settings.drives` lists `madswan` twice
- **THEN** evaluation fails, naming `services.crew.settings.drives` and `madswan`

#### Scenario: A role crew has no kind for
- **WHEN** a drive's `flume` names `dispatcher`, or gives `planner` the value `true`
- **THEN** evaluation fails

#### Scenario: Drives under `partitions`
- **WHEN** `services.crew.settings` lists the drives under `partitions` and gives no `drives`
- **THEN** evaluation fails, naming `services.crew.settings.drives` as used but not defined

#### Scenario: Teams
- **WHEN** `services.crew.settings` gives `teams`
- **THEN** evaluation fails, saying the teams file crew reads has no place for teams

### Requirement: services.crew.host names the host
`services.crew.host` SHALL name this host as `hostname -s` names it, the name the drives' `machine` gives a host. It SHALL NOT be written into the teams file. The module's activation SHALL be given it, and SHALL say, naming both, when the host's own name is not it, linking the file all the same.

#### Scenario: The activation is given the host
- **WHEN** a system enables `services.crew` with `host = "host-a"`
- **THEN** its activation runs crew's link with the module's file and `host-a`, and the teams file holds no `host`

#### Scenario: A host whose name is not services.crew.host
- **WHEN** crew's link runs with `host-a` on a host whose name, read as `hostname -s` gives it, is `host-b`
- **THEN** it links the file and says a line naming `host-a` and `host-b`
