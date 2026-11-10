# crew-flake Specification

## Purpose
crew's own flake (agentplot/boomdrive record 0023): crew's package and its `services.crew` module for nix-darwin and NixOS, which writes crew's teams file from options named as the file names them and no other tool's file, so a host configures crew through the module alone and the Boomdrive flake re-exports it (record 0058, `flake.1` to `flake.3`).

## Requirements

### Requirement: The module is given for nix-darwin and NixOS
The flake SHALL give `darwinModules.crew` and `nixosModules.crew`, each also as `default`, declaring `services.crew`. A system of each platform with `services.crew` enabled SHALL evaluate.

#### Scenario: A nix-darwin system
- **WHEN** a nix-darwin system of `aarch64-darwin` imports `darwinModules.default` and enables `services.crew` for its primary user
- **THEN** the system's derivation evaluates

#### Scenario: A NixOS system
- **WHEN** a NixOS system of `x86_64-linux` imports `nixosModules.default` and enables `services.crew` for a normal user
- **THEN** the system's toplevel evaluates

### Requirement: services.crew.host names the host
`services.crew.host` SHALL name this host as `hostname -s` names it, the name the drives' `machine` gives a host. It SHALL NOT be written into the teams file. The module's activation SHALL be given it, and SHALL say, naming both, when the host's own name is not it, linking the file all the same.

#### Scenario: The activation is given the host
- **WHEN** a system enables `services.crew` with `host = "host-a"`
- **THEN** its activation runs crew's link with the module's file and `host-a`, and the teams file holds no `host`

#### Scenario: A host whose name is not services.crew.host
- **WHEN** crew's link runs with `host-a` on a host whose name, read as `hostname -s` gives it, is `host-b`
- **THEN** it links the file and says a line naming `host-a` and `host-b`

### Requirement: The file is linked for the user who runs crew
The module's activation SHALL link crew's teams file as nix-darwin's primary user under their home, or, on NixOS, as `services.crew.user` alone. A primary user with no home, and a `services.crew.user` the system does not declare, SHALL fail evaluation, naming the option to set.

#### Scenario: On nix-darwin
- **WHEN** a nix-darwin system whose primary user is alice, at `/Users/alice`, enables `services.crew`
- **THEN** its activation runs crew's link as alice with `HOME=/Users/alice`, given the module's file and the host

#### Scenario: A primary user with no home
- **WHEN** alice's `users.users.alice.home` is not set
- **THEN** evaluation fails, naming `alice` and `users.users.alice.home`

#### Scenario: On NixOS
- **WHEN** a NixOS system whose normal users are alice and bob enables `services.crew` with `user = "alice"`
- **THEN** its user activation runs crew's link only when the user running it is alice, given the module's file and the host

#### Scenario: A user the system does not declare
- **WHEN** `services.crew.user` is `carol`, whom `users.users` does not declare
- **THEN** evaluation fails, naming `services.crew.user` and `users.users.carol`

### Requirement: crew's link replaces only a link
crew's link SHALL make `~/.config/crew/teams.json` a link to the module's file, replacing a link there. A file there that is no link SHALL be moved aside once, to `teams.json.before-nix`, both paths named; where that path is taken already, the link SHALL change neither, name both and fail, stopping nothing else of the system's activation.

#### Scenario: Nothing there
- **WHEN** crew's link runs in a home with no `~/.config/crew`
- **THEN** it makes the folder and links `teams.json` to the file

#### Scenario: A link there
- **WHEN** `~/.config/crew/teams.json` is a link to another file
- **THEN** it is linked to the module's file, and nothing is moved aside

#### Scenario: A file there
- **WHEN** `~/.config/crew/teams.json` is a file that is no link
- **THEN** it is moved to `teams.json.before-nix`, the link is made, and both paths are named

#### Scenario: A file there and one aside already
- **WHEN** `~/.config/crew/teams.json` is a file that is no link and `teams.json.before-nix` is there
- **THEN** neither changes, both are named, and the link exits non-zero

### Requirement: The package is the flake's unless the host gives its own
The module SHALL install `services.crew.package` in the system profile, the flake's crew for the host's system unless the host gives its own, and SHALL install no other package of crew's.

#### Scenario: The flake's crew
- **WHEN** a system of either platform enables `services.crew` and gives no package
- **THEN** the system profile holds the flake's crew for that system

#### Scenario: A host's own crew
- **WHEN** a system gives `services.crew.package` a crew of its own
- **THEN** the system profile holds that crew and not the flake's, and the module's file is unchanged

### Requirement: The module writes no other tool's file
The module SHALL write crew's teams file alone, and run no service: it SHALL add no file under `/etc`, no launchd agent or daemon, and no systemd unit, and its activation SHALL link only `~/.config/crew/teams.json`.

#### Scenario: Nothing else on the host
- **WHEN** a system of either platform enables `services.crew`, beside the same system with it not enabled
- **THEN** both have the same files under `environment.etc`, the same launchd agents and daemons or the same systemd units, and the same users, and the enabled system's activation adds only crew's link

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
