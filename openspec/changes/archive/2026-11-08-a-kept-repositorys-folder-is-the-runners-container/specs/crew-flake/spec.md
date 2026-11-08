## MODIFIED Requirements

### Requirement: The module writes crew's teams file from options named as the file names them
With `services.crew.enable`, the module SHALL write crew's teams file from `services.crew.settings`, each key named as the file names it: `partitions`; `repositories`, where the host gives its kept repositories; and `version`, which the module SHALL set to the version `plugin/lib/crew.py` reads and which no host SHALL set. The file SHALL be the settings as JSON with every unset key left out, so that for the same partitions and repositories it holds the same bytes the fleet's writer gives.

#### Scenario: deneb's partitions
- **WHEN** `services.crew.settings.partitions` lists afterthought, agentplot and madswan on deneb and wldn on chuck-herdr-alpha, with its planner in `wldn-1`, as deneb's teams file held them on 2026-11-07
- **THEN** the module's file holds, byte for byte, `nix/tests/files/deneb.json`, the bytes of deneb's `~/.config/crew/teams.json` read that day, and a partition that gives no `roles` has no `roles` key, and the file has no `repositories` key

#### Scenario: A runner host's kept repositories
- **WHEN** `services.crew.settings` gives deneb's partitions and `repositories` naming `agentplot/crew` and `afterthought/swancloud`, each with its runner's container as `dir` and its runner's view as `checkout`
- **THEN** the module's file holds, byte for byte, `nix/tests/files/runner.json`

#### Scenario: crew reads the file the module writes
- **WHEN** crew loads `nix/tests/files/deneb.json` as its teams file, beside a hosts file naming those sessions
- **THEN** it loads four partitions, afterthought, agentplot, madswan and wldn, wldn's planner and reviewer in `wldn-1`, and every role of every partition standing

#### Scenario: crew reads the kept repositories the module writes
- **WHEN** crew loads `nix/tests/files/runner.json` as its teams file on deneb, beside the same hosts file
- **THEN** it loads the four partitions, and names crew's and swancloud's folder and checkout on deneb as the file's `dir` and `checkout`

#### Scenario: The version is crew's
- **WHEN** a host's settings set `version`
- **THEN** evaluation fails, and the version the module writes is the one `plugin/lib/crew.py` reads

## ADDED Requirements

### Requirement: A kept repository is named by its address with its folder and checkout
The module SHALL declare `services.crew.settings.repositories` as an attribute set keyed by each repository's address, `<owner>/<name>`, each giving exactly `dir` and `checkout`, each an absolute path, with no default for either. It SHALL fail evaluation for a key that is no `<owner>/<name>`, an entry that lacks `dir` or `checkout` or gives another key, and a path that is not absolute. Where a host gives no `repositories`, the file SHALL have no such key.

#### Scenario: An entry with no checkout
- **WHEN** `services.crew.settings.repositories."agentplot/crew"` gives `dir` alone
- **THEN** evaluation fails

#### Scenario: A relative folder
- **WHEN** an entry's `dir` is `repositories/agentplot/crew`
- **THEN** evaluation fails

#### Scenario: A repository named with no owner
- **WHEN** `services.crew.settings.repositories` names `crew`
- **THEN** evaluation fails

#### Scenario: A key crew has no place for
- **WHEN** an entry gives `view` beside its `dir` and `checkout`
- **THEN** evaluation fails
