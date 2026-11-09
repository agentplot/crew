## MODIFIED Requirements

### Requirement: Drives are declared in the teams file
`teams.json` SHALL list each drive with a main level, under `drives`. Beside its drives it MAY name, for the host it is written on, each repository that host keeps, and nothing else. Each drive's entry gives the drive's label (`wldn`, `madswan`, `agentplot`), which is its one name, its blueprints repos, its state repository (`state`, as `<owner>/<name>`), the machine and session its main level runs in, and `flume`, naming each of its five main-level roles, `design`, `planner`, `reviewer`, `ops` and `operator`, as `false` while it stands or as the Flume stream its runs run in on the main level's host. The first blueprints repo listed SHALL be the one the drive's signals and elaboration go to by default. A drive with no `state` or no `flume` SHALL be an error naming the field and the machine's configuration as the fix, never a default, and so SHALL a `flume` that leaves a role out, names another key, or gives a role anything but `false` or a stream's name. crew SHALL read version 6 of the file alone: a file at any other version, version 5 and its `partitions` among them, or one holding `teams`, SHALL be refused naming as the fix crew's own module, `services.crew`, or the machine's configuration that writes the file, with nothing done; no refusal of the file SHALL name a module of another repository's as its fix; crew SHALL read no `partitions` key and no entry's `partition`. A drive's `roles.<role>` MAY name a `session` for a main-level role, a session the hosts file lists on the main level's machine, where that role runs while it stands; any other session SHALL be an error naming it. crew SHALL read no session's `partition` in the hosts file: the drive names its sessions, and the fleet's configuration checks what it writes there.

The host's kept repositories, where the file names them, SHALL be its `repositories`. That is an object keyed by each repository's address, `<owner>/<name>`, each giving exactly its `dir`, the folder crew names as the kit's, and its `checkout`, the working tree crew names as the kit's checkout, each an absolute path. crew SHALL check every entry when it loads the file, before any is used. A `repositories` that is no object, a key that is no `<owner>/<name>`, or an entry that lacks `dir` or `checkout`, gives another key, or gives a path that is not absolute SHALL be refused, naming the file, the repository and the machine's configuration as the fix, with nothing done. A file with no `repositories` SHALL load as before, naming no repository.

#### Scenario: clients/willdan
- **WHEN** `teams.json` lists the drive `wldn` with willdan-blueprints and `WilldanGroup/crew-state`, running on the box in `wldn-2`, a session the hosts file puts in `clients/willdan`
- **THEN** `crew main up wldn` starts its main level in `wldn-2` on the box, and wldn's plan is read from `wldn/main` of `WilldanGroup/crew-state`

#### Scenario: A drive with no state repository
- **WHEN** a drive's entry has no `state`
- **THEN** crew refuses to load the teams file, naming the drive and the missing field

#### Scenario: The planner in a session of its own
- **WHEN** wldn's entry names `roles.planner.session` as `wldn-1`, a session the hosts file lists on chuck-herdr-alpha
- **THEN** `wldn-planner` runs in `wldn-1` and its other main-level roles in the main level's session

#### Scenario: A session of another drive
- **WHEN** wldn's `roles.planner.session` names `madswan`, another drive's session, which the hosts file lists on deneb and not on chuck-herdr-alpha
- **THEN** crew refuses to load the teams file, naming the planner, the session and the machine

#### Scenario: A session's `partition` in the hosts file
- **WHEN** the hosts file gives wldn's session `wldn-2` a `partition` of `clients/willdan`, of `business`, or none
- **THEN** crew loads the teams file the same each time, reading nothing of it

#### Scenario: A drive with no flume
- **WHEN** a drive's entry has no `flume`
- **THEN** crew refuses to load the teams file, naming the drive, the field and crew's own module, `services.crew`, or the machine's configuration that writes the file

#### Scenario: A role crew has no kind for
- **WHEN** madswan's `flume` names `dispatcher`, leaves out `operator`, or gives `planner` the value `true`
- **THEN** crew refuses to load the teams file, naming the drive and the role

#### Scenario: The file before version 4
- **WHEN** `teams.json` is at version 3
- **THEN** crew refuses to load it, naming its version and crew's own module, `services.crew`, or the machine's configuration that writes the file, and does nothing

#### Scenario: The file before version 5
- **WHEN** `teams.json` is at version 4, its `teams` listing a team for each kit
- **THEN** crew refuses to load it, naming its version and crew's own module, `services.crew`, or the machine's configuration that writes the file, and does nothing

#### Scenario: The file at version 5
- **WHEN** `teams.json` is at version 5, its `partitions` each naming its `partition`, as deneb's file held them on 2026-11-08
- **THEN** crew refuses to load it, naming its version, that crew reads only version 6, and crew's own module, `services.crew`, or the machine's configuration that writes the file, and does nothing

#### Scenario: The box's file at version 2
- **WHEN** `teams.json` is at version 2, its `partitions` and its `teams` as chuck-herdr-alpha's file holds them for wldn's teams
- **THEN** crew refuses to load it, naming its version, that crew reads only version 6, and crew's own module, `services.crew`, or the machine's configuration that writes the file, and does nothing

#### Scenario: A version-5 file that lists teams
- **WHEN** `teams.json` is at version 5 and holds a `teams` key beside its `partitions`
- **THEN** crew refuses to load it, naming its version, that crew reads only version 6, and crew's own module, `services.crew`, or the machine's configuration that writes the file, and does nothing

#### Scenario: A version-6 file that lists teams
- **WHEN** `teams.json` is at version 6 and holds a `teams` key beside its `drives`
- **THEN** crew refuses to load it, saying version 6 has no place for teams since crew runs none, naming crew's own module, `services.crew`, or the machine's configuration that writes the file, and does nothing

#### Scenario: A version-6 file whose drives are under `partitions`
- **WHEN** `teams.json` is at version 6 and lists its drives under `partitions`, with no `drives`
- **THEN** crew refuses to load it, saying it lists no drives, naming crew's own module, `services.crew`, or the machine's configuration that writes the file, and does nothing

#### Scenario: Every refusal of the file names crew's own fix
- **WHEN** crew refuses `teams.json` for its version, for a `teams` key, for listing no drives, for a drive's `state`, `review` or `flume`, or for a kept repository named wrongly
- **THEN** the refusal names crew's own module, `services.crew`, or the machine's configuration that writes the file as the fix, and no module of swancloud's or of any other repository's

#### Scenario: A runner host's kept repositories
- **WHEN** deneb's `teams.json` gives `repositories` naming `agentplot/crew` with `dir` `/Users/chuck/.local/share/flywheel/repositories/agentplot/crew` and `checkout` `/Users/chuck/Code/boomdrive/agentplot/crew`
- **THEN** crew loads the file, and on deneb names that folder and that checkout as crew's

#### Scenario: A kept repository named wrongly
- **WHEN** `repositories` names `crew` with no owner, or names `agentplot/crew` with no `checkout`, with a `dir` of `repositories/agentplot/crew`, or with a `view` beside its `dir` and `checkout`
- **THEN** crew refuses to load the teams file, naming the file, the repository and the machine's configuration, and does nothing

#### Scenario: A file that names no repository
- **WHEN** `teams.json` gives no `repositories`
- **THEN** crew loads it, and names every kit's folder and checkout as the sessions in the hosts file keep it, `<session dir>/<name>` and `<session dir>/<name>/main`
