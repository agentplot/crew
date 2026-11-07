## Purpose
crew's own flake (agentplot/boomdrive record 0023): crew's package and its `services.crew` module for nix-darwin and NixOS, which writes crew's teams file from options named as the file names them and no other tool's file, so a host configures crew through the module alone and the Boomdrive flake re-exports it (record 0058, `flake.1` to `flake.3`).

## ADDED Requirements

### Requirement: The flake gives crew's package for each system
crew's flake SHALL give `packages.<system>.crew` and `packages.<system>.default`, one derivation whose main program is `crew`, for `aarch64-darwin`, `aarch64-linux` and `x86_64-linux`, and no other system. The package SHALL hold crew's plugin folder from the flake's tree under `plugin/`, and `bin/crew`, which runs the plugin's own `bin/crew`.

#### Scenario: Every system's package
- **WHEN** the flake's outputs are evaluated
- **THEN** `packages` gives `aarch64-darwin`, `aarch64-linux` and `x86_64-linux`, each giving `crew` and `default` and nothing else, each a derivation that evaluates, `default` the same derivation as `crew`, its `meta.mainProgram` `crew`

### Requirement: The module is given for nix-darwin and NixOS
The flake SHALL give `darwinModules.crew` and `nixosModules.crew`, each also as `default`, declaring `services.crew`. A system of each platform with `services.crew` enabled SHALL evaluate.

#### Scenario: A nix-darwin system
- **WHEN** a nix-darwin system of `aarch64-darwin` imports `darwinModules.default` and enables `services.crew` for its primary user
- **THEN** the system's derivation evaluates

#### Scenario: A NixOS system
- **WHEN** a NixOS system of `x86_64-linux` imports `nixosModules.default` and enables `services.crew` for a normal user
- **THEN** the system's toplevel evaluates

### Requirement: The module writes crew's teams file from options named as the file names them
With `services.crew.enable`, the module SHALL write crew's teams file from `services.crew.settings`, each key named as the file names it: `partitions`, and `version`, which the module SHALL set to the version `plugin/lib/crew.py` reads and which no host SHALL set. The file SHALL be the settings as JSON with every unset key left out, so that for the same partitions it holds the same bytes the fleet's writer gives today.

#### Scenario: deneb's partitions
- **WHEN** `services.crew.settings.partitions` lists afterthought, agentplot and madswan on deneb and wldn on chuck-herdr-alpha, with its planner in `wldn-1`, as deneb's teams file held them on 2026-11-07
- **THEN** the module's file holds, byte for byte, `nix/tests/files/deneb.json`, the bytes of deneb's `~/.config/crew/teams.json` read that day, and a partition that gives no `roles` has no `roles` key

#### Scenario: crew reads the file the module writes
- **WHEN** crew loads `nix/tests/files/deneb.json` as its teams file, beside a hosts file naming those sessions
- **THEN** it loads four partitions, afterthought, agentplot, madswan and wldn, wldn's planner and reviewer in `wldn-1`, and every role of every partition standing

#### Scenario: The version is crew's
- **WHEN** a host's settings set `version`
- **THEN** evaluation fails, and the version the module writes is the one `plugin/lib/crew.py` reads

### Requirement: Every partition is listed once, with every key crew requires
The module SHALL give no default for a key crew requires of a partition (`label`, `partition`, `blueprints`, `state`, `machine`, `session`, `review` and `flume`), and SHALL fail evaluation, naming what is wrong, for a partition that lacks one, a label listed twice, a `flume` that names a role crew has no kind for or gives a role neither `false` nor a stream's name, and a `teams` key, which the version crew reads has no place for.

#### Scenario: A partition with no state repository
- **WHEN** a partition in `services.crew.settings.partitions` gives no `state`
- **THEN** evaluation fails, naming `state`

#### Scenario: A label twice
- **WHEN** `services.crew.settings.partitions` lists `madswan` twice
- **THEN** evaluation fails, naming `services.crew.settings.partitions` and `madswan`

#### Scenario: A role crew has no kind for
- **WHEN** a partition's `flume` names `dispatcher`, or gives `planner` the value `true`
- **THEN** evaluation fails

#### Scenario: Teams
- **WHEN** `services.crew.settings` gives `teams`
- **THEN** evaluation fails, saying the teams file crew reads has no place for teams

### Requirement: services.crew.host names the host
`services.crew.host` SHALL name this host as `hostname -s` names it, the name the partitions' `machine` gives a host. It SHALL NOT be written into the teams file. The module's activation SHALL be given it, and SHALL say, naming both, when the host's own name is not it, linking the file all the same.

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
