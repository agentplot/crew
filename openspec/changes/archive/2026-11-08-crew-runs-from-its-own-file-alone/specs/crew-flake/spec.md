## MODIFIED Requirements

### Requirement: The module writes crew's teams file from options named as the file names them
With `services.crew.enable`, the module SHALL write crew's teams file from `services.crew.settings`, each key named as the file names it: `drives`, given as an attribute set keyed by each drive's label and written as the file's list of drives in the order of their labels, each with its `label`; `hosts`; `consoles`, where the host gives the consoles it opens; `repositories`, where the host gives its kept repositories; and `version`, which the module SHALL set to the version `plugin/lib/crew.py` reads and which no host SHALL set. The file SHALL be the settings as JSON with every unset key left out, so that for the same drives, listed in the order of their labels, and the same hosts, consoles and repositories it holds the same bytes the fleet's writer gives.

#### Scenario: deneb's drives
- **WHEN** `services.crew.settings.drives` names afterthought, agentplot and madswan on deneb and wldn on chuck-herdr-alpha, with its planner in `wldn-1`, as deneb's teams file held them on 2026-11-07, each with the folder, repositories and accounts deneb's hosts file gave its sessions on 2026-11-09; `hosts` names deneb and chuck-herdr-alpha with their ssh names and kinds; and `consoles` names the four drives with deneb's folder for each
- **THEN** the module's file holds, byte for byte, `nix/tests/files/deneb.json`, its drives listed under `drives` in the order of their labels, each with its `label`, `folder`, `repos` and `accounts` and none naming a `partition`, a drive that gives no `roles` having no `roles` key, and the file has `hosts` and `consoles` and no `repositories` key

#### Scenario: A runner host's kept repositories
- **WHEN** `services.crew.settings` gives deneb's drives, hosts and consoles, and `repositories` naming `agentplot/crew` and `afterthought/swancloud`, each with its runner's container as `dir` and its runner's view as `checkout`
- **THEN** the module's file holds, byte for byte, `nix/tests/files/runner.json`

#### Scenario: crew reads the file the module writes
- **WHEN** crew loads `nix/tests/files/deneb.json` as its teams file on deneb, with no hosts file
- **THEN** it loads four drives, afterthought, agentplot, madswan and wldn, wldn's planner and reviewer in `wldn-1` on account ia and its other roles on willdan-alex, every role of every drive standing, and the consoles of the four drives on deneb

#### Scenario: crew reads the kept repositories the module writes
- **WHEN** crew loads `nix/tests/files/runner.json` as its teams file on deneb, with no hosts file
- **THEN** it loads the four drives, and names crew's and swancloud's folder and checkout on deneb as the file's `dir` and `checkout`

#### Scenario: The version is crew's
- **WHEN** a host's settings set `version`
- **THEN** evaluation fails, and the version the module writes is the one `plugin/lib/crew.py` reads

### Requirement: Another module gives a drive its machine and its state repository
A drive's `machine` and `state` SHALL each be written once: by the host's own settings, or by another module that gives them under the drive's label in `services.crew.settings.drives`, the drive's other keys staying in the host's settings under that label. Where either is written more than once at the same priority, the values equal or not, evaluation SHALL fail.

#### Scenario: deneb's drives from two modules
- **WHEN** one module gives each of deneb's four drives its `machine` and its `state`, and the host's settings give each drive its `blueprints`, `session`, `folder`, `repos`, `accounts`, `review` and `flume`, and wldn its `roles`, and give `hosts` and `consoles`, and neither gives a key the other gives
- **THEN** the module's file holds, byte for byte, `nix/tests/files/deneb.json`, and no assertion fails

#### Scenario: A machine written twice
- **WHEN** another module gives agentplot its `machine` `deneb`, and the host's settings also give agentplot the `machine` `deneb`
- **THEN** evaluation fails

#### Scenario: A state repository written twice
- **WHEN** another module gives agentplot its `state` `afterthought/crew-state`, and the host's settings also give agentplot the `state` `afterthought/crew-state`
- **THEN** evaluation fails

### Requirement: Every drive gives every key crew requires
The module SHALL give no default for a key crew requires of a drive (`blueprints`, `state`, `machine`, `session`, `folder`, `repos`, `accounts`, `review` and `flume`) and SHALL declare no `partition` option for a drive. It SHALL fail evaluation for a drive that lacks one of those keys, a `folder` that is not an absolute path, a `repos` entry that is no `<owner>/<name>`, an `accounts` that leaves out one of the five main-level roles, names another, or gives an account that is no name crew accepts, and a `flume` that names a role crew has no kind for or gives a role neither `false` nor a stream's name, and SHALL fail evaluation, saying so, for a `teams` key, which the version crew reads has no place for.

#### Scenario: A drive with no state repository
- **WHEN** a drive under `services.crew.settings.drives` gives no `state`, and no other module gives it one
- **THEN** evaluation fails

#### Scenario: A drive with no machine
- **WHEN** a drive under `services.crew.settings.drives` gives no `machine`, and no other module gives it one
- **THEN** evaluation fails

#### Scenario: A drive with no folder, repos or accounts
- **WHEN** a drive under `services.crew.settings.drives` gives no `folder`, no `repos` or no `accounts`
- **THEN** evaluation fails

#### Scenario: A relative folder
- **WHEN** a drive's `folder` is `work/madswan`
- **THEN** evaluation fails

#### Scenario: An account left out
- **WHEN** a drive's `accounts` gives `design`, `planner`, `ops` and `operator`, and no `reviewer`
- **THEN** evaluation fails

#### Scenario: A role crew has no kind for
- **WHEN** a drive's `flume` names `dispatcher`, or gives `planner` the value `true`
- **THEN** evaluation fails

#### Scenario: Teams
- **WHEN** `services.crew.settings` gives `teams`
- **THEN** evaluation fails, saying the teams file crew reads has no place for teams

## ADDED Requirements

### Requirement: The module names the hosts crew reaches, each by its ssh name and kind
The module SHALL declare `services.crew.settings.hosts` as an attribute set keyed by each host's name, a name crew accepts, each giving exactly `ssh`, a name that is not empty, and `kind`, `darwin` or `nixos`, with no default for `hosts` or for either key. It SHALL fail evaluation for settings that give no `hosts`, a host's name crew does not accept, an entry that lacks `ssh` or `kind` or gives another key, and a `kind` that is neither.

#### Scenario: No hosts
- **WHEN** `services.crew.settings` gives deneb's drives and no `hosts`
- **THEN** evaluation fails

#### Scenario: A kind crew does not read
- **WHEN** `services.crew.settings.hosts.deneb.kind` is `macos`
- **THEN** evaluation fails

#### Scenario: A key crew has no place for
- **WHEN** `services.crew.settings.hosts.deneb` gives `home` beside its `ssh` and `kind`
- **THEN** evaluation fails

### Requirement: The module names the consoles of the host
The module SHALL declare `services.crew.settings.consoles` as an attribute set keyed by a drive's label, each an absolute path, with no default for an entry. It SHALL fail evaluation for a path that is not absolute. Where a host gives no `consoles`, the file SHALL have no such key.

#### Scenario: A relative console folder
- **WHEN** `services.crew.settings.consoles.wldn` is `Code/clients/github_willdan`
- **THEN** evaluation fails

#### Scenario: No consoles
- **WHEN** a host gives no `services.crew.settings.consoles`
- **THEN** the module's file has no `consoles` key
