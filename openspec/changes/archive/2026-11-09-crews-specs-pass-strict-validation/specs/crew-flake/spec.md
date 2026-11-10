## ADDED Requirements

### Requirement: The flake gives one crew package holding crew's plugin for each of three systems
crew's flake SHALL give `packages.<system>.crew` and `packages.<system>.default`, one derivation whose main program is `crew`, for `aarch64-darwin`, `aarch64-linux` and `x86_64-linux`, and no other system. The package SHALL hold crew's plugin folder from the flake's tree under `plugin/`, and `bin/crew`, which runs the plugin's own `bin/crew`.

#### Scenario: Every system's package
- **WHEN** the flake's outputs are evaluated
- **THEN** `packages` gives `aarch64-darwin`, `aarch64-linux` and `x86_64-linux`, each giving `crew` and `default` and nothing else, each a derivation that evaluates, `default` the same derivation as `crew`, its `meta.mainProgram` `crew`

### Requirement: A package built from a commit holds a release file naming it
Where the flake knows the commit it is built from, the package SHALL also hold `plugin/release.json`, naming that commit as `commit` and the package's version as `version`, and nothing else; built from a tree with no commit of its own, as one with uncommitted changes, it SHALL hold no release file. The package's `release` SHALL give what the file names, or null where it holds none.

#### Scenario: A build from a commit
- **WHEN** the flake's outputs are evaluated with `self.rev` `fcedc22e6df6380f1f640efac5f796416b1fb4c9`
- **THEN** each system's `crew.release` is that commit with the package's version, and its install writes them to `plugin/release.json`

#### Scenario: A build from a tree with no commit
- **WHEN** the flake's outputs are evaluated with no `self.rev`
- **THEN** each system's `crew.release` is null, and its install writes no `plugin/release.json`

### Requirement: The module writes each key of crew's teams file from the setting of that name
With `services.crew.enable`, the module SHALL write crew's teams file from `services.crew.settings`, each key named as the file names it: `drives`, given as an attribute set keyed by each drive's label and written as the file's list of drives in the order of their labels, each with its `label`; `hosts`; `consoles`, where the host gives the consoles it opens; `repositories`, where the host gives its kept repositories; and `version`.

#### Scenario: deneb's drives
- **WHEN** `services.crew.settings.drives` names afterthought, agentplot and madswan on deneb and wldn on chuck-herdr-alpha, with its planner in `wldn-1`, as deneb's teams file held them on 2026-11-07, each with the folder, repositories and accounts deneb's hosts file gave its sessions on 2026-11-09; `hosts` names deneb and chuck-herdr-alpha with their ssh names and kinds; and `consoles` names the four drives with deneb's folder for each
- **THEN** the module's file holds, byte for byte, `nix/tests/files/deneb.json`, its drives listed under `drives` in the order of their labels, each with its `label`, `folder`, `repos` and `accounts` and none naming a `partition`, a drive that gives no `roles` having no `roles` key, and the file has `hosts` and `consoles` and no `repositories` key

#### Scenario: A runner host's kept repositories
- **WHEN** `services.crew.settings` gives deneb's drives, hosts and consoles, and `repositories` naming `agentplot/crew` and `afterthought/swancloud`, each with its runner's container as `dir` and its runner's view as `checkout`
- **THEN** the module's file holds, byte for byte, `nix/tests/files/runner.json`

### Requirement: The module's file is the settings as JSON at the version crew reads
The module SHALL set `version`, which no host SHALL set, to the version `plugin/lib/crew.py` reads. The file SHALL be the settings as JSON with every unset key left out, so that for the same drives, listed in the order of their labels, and the same hosts, consoles and repositories it holds the same bytes the fleet's writer gives.

#### Scenario: crew reads the file the module writes
- **WHEN** crew loads `nix/tests/files/deneb.json` as its teams file on deneb, with no hosts file
- **THEN** it loads four drives, afterthought, agentplot, madswan and wldn, wldn's planner and reviewer in `wldn-1` on account ia and its other roles on willdan-alex, every role of every drive standing, and the consoles of the four drives on deneb

#### Scenario: crew reads the kept repositories the module writes
- **WHEN** crew loads `nix/tests/files/runner.json` as its teams file on deneb, with no hosts file
- **THEN** it loads the four drives, and names crew's and swancloud's folder and checkout on deneb as the file's `dir` and `checkout`

#### Scenario: The version is crew's
- **WHEN** a host's settings set `version`
- **THEN** evaluation fails, and the version the module writes is the one `plugin/lib/crew.py` reads

### Requirement: A drive that lacks a key crew requires fails evaluation, with no default for it
The module SHALL give no default for a key crew requires of a drive (`blueprints`, `state`, `machine`, `session`, `folder`, `repos`, `accounts`, `review` and `flume`) and SHALL declare no `partition` option for a drive. The module SHALL fail evaluation for a drive that lacks one of those keys.

#### Scenario: A drive with no state repository
- **WHEN** a drive under `services.crew.settings.drives` gives no `state`, and no other module gives it one
- **THEN** evaluation fails

#### Scenario: A drive with no machine
- **WHEN** a drive under `services.crew.settings.drives` gives no `machine`, and no other module gives it one
- **THEN** evaluation fails

#### Scenario: A drive with no folder, repos or accounts
- **WHEN** a drive under `services.crew.settings.drives` gives no `folder`, no `repos` or no `accounts`
- **THEN** evaluation fails

### Requirement: A drive's key crew cannot read, or a teams key, fails evaluation
The module SHALL fail evaluation for a `folder` that is not an absolute path, a `repos` entry that is no `<owner>/<name>`, an `accounts` that leaves out one of the five main-level roles, names another, or gives an account that is no name crew accepts, and a `flume` that names a role crew has no kind for or gives a role neither `false` nor a stream's name, and SHALL fail evaluation, saying so, for a `teams` key, which the version crew reads has no place for.

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

## REMOVED Requirements

### Requirement: The flake gives crew's package for each system
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "The flake gives one crew package holding crew's plugin for each of three systems" and "A package built from a commit holds a release file naming it".

### Requirement: The module writes crew's teams file from options named as the file names them
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "The module writes each key of crew's teams file from the setting of that name" and "The module's file is the settings as JSON at the version crew reads".

### Requirement: Every drive gives every key crew requires
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A drive that lacks a key crew requires fails evaluation, with no default for it" and "A drive's key crew cannot read, or a teams key, fails evaluation".
