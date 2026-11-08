## MODIFIED Requirements

### Requirement: Partitions are declared in the teams file
`teams.json` SHALL list each partition with a main level. Beside its partitions it MAY name, for the host it is written on, each repository that host keeps, and nothing else. Each partition's entry gives the partition's label (`wldn`, `madswan`, `swancloud`), its swancloud name, its blueprints repos, its state repository (`state`, as `<owner>/<name>`), the machine and session its main level runs in, and `flume`, naming each of its five main-level roles, `design`, `planner`, `reviewer`, `ops` and `operator`, as `false` while it stands or as the Flume stream its runs run in on the main level's host. The first blueprints repo listed SHALL be the one the partition's signals and elaboration go to by default. A partition with no `state` or no `flume` SHALL be an error naming the field and the machine's configuration as the fix, never a default, and so SHALL a `flume` that leaves a role out, names another key, or gives a role anything but `false` or a stream's name. crew SHALL read version 5 of the file alone: a file at any other version, or one holding `teams`, SHALL be refused naming swancloud's `lib/crew-teams.nix` as the fix, with nothing done. A partition's `roles.<role>` MAY name a `session` for a main-level role, a session of the main level's machine in the partition, where that role runs while it stands; any other session SHALL be an error naming it.

The host's kept repositories, where the file names them, SHALL be its `repositories`. That is an object keyed by each repository's address, `<owner>/<name>`, each giving exactly its `dir`, the folder crew names as the kit's, and its `checkout`, the working tree crew names as the kit's checkout, each an absolute path. crew SHALL check every entry when it loads the file, before any is used. A `repositories` that is no object, a key that is no `<owner>/<name>`, or an entry that lacks `dir` or `checkout`, gives another key, or gives a path that is not absolute SHALL be refused, naming the file, the repository and the machine's configuration as the fix, with nothing done. A file with no `repositories` SHALL load as before, naming no repository.

#### Scenario: clients/willdan
- **WHEN** `teams.json` lists `wldn` as `clients/willdan` with willdan-blueprints and `WilldanGroup/crew-state`, running on the box in `wldn-2`
- **THEN** `crew main up wldn` starts its main level in `wldn-2` on the box, and wldn's plan is read from `wldn/main` of `WilldanGroup/crew-state`

#### Scenario: A partition with no state repository
- **WHEN** a partition's entry has no `state`
- **THEN** crew refuses to load the teams file, naming the partition and the missing field

#### Scenario: The planner in a session of its own
- **WHEN** swancloud's entry names `roles.planner.session` as `swancloud-2`, a session of deneb in partition personal
- **THEN** `swancloud-planner` runs in `swancloud-2` and its other main-level roles in the main level's session

#### Scenario: A session of another partition
- **WHEN** swancloud's `roles.planner.session` names `madswan-1`, a session of partition business
- **THEN** crew refuses to load the teams file, naming the planner, the session and its partition

#### Scenario: A partition with no flume
- **WHEN** a partition's entry has no `flume`
- **THEN** crew refuses to load the teams file, naming the partition, the field and swancloud's `lib/crew-teams.nix`

#### Scenario: A role crew has no kind for
- **WHEN** madswan's `flume` names `dispatcher`, leaves out `operator`, or gives `planner` the value `true`
- **THEN** crew refuses to load the teams file, naming the partition and the role

#### Scenario: The file before version 4
- **WHEN** `teams.json` is at version 3
- **THEN** crew refuses to load it, naming its version and swancloud's `lib/crew-teams.nix`, and does nothing

#### Scenario: The file before version 5
- **WHEN** `teams.json` is at version 4, its `teams` listing a team for each kit
- **THEN** crew refuses to load it, naming its version and swancloud's `lib/crew-teams.nix`, and does nothing

#### Scenario: The box's file at version 2
- **WHEN** `teams.json` is at version 2, its `partitions` and its `teams` as chuck-herdr-alpha's file holds them for wldn's teams
- **THEN** crew refuses to load it, naming its version, that crew reads only version 5, and swancloud's `lib/crew-teams.nix`, and does nothing

#### Scenario: A version-5 file that lists teams
- **WHEN** `teams.json` is at version 5 and holds a `teams` key beside its `partitions`
- **THEN** crew refuses to load it, saying version 5 has no place for teams since crew runs none, naming swancloud's `lib/crew-teams.nix`, and does nothing

#### Scenario: A runner host's kept repositories
- **WHEN** deneb's `teams.json` gives `repositories` naming `agentplot/crew` with `dir` `/Users/chuck/.local/share/flywheel/repositories/agentplot/crew` and `checkout` `/Users/chuck/Code/boomdrive/agentplot/crew`
- **THEN** crew loads the file, and on deneb names that folder and that checkout as crew's

#### Scenario: A kept repository named wrongly
- **WHEN** `repositories` names `crew` with no owner, or names `agentplot/crew` with no `checkout`, with a `dir` of `repositories/agentplot/crew`, or with a `view` beside its `dir` and `checkout`
- **THEN** crew refuses to load the teams file, naming the file, the repository and the machine's configuration, and does nothing

#### Scenario: A file that names no repository
- **WHEN** `teams.json` gives no `repositories`
- **THEN** crew loads it, and names every kit's folder and checkout as the sessions in the hosts file keep it, `<session dir>/<name>` and `<session dir>/<name>/main`

## ADDED Requirements

### Requirement: The design agent's brief names each kept repository's checkout and folder as its host keeps them
The design agent's brief SHALL name its default blueprints repository's checkout and folder, and each kit's checkout with its folder, where its worktrees are cut. Each SHALL be the teams file's `checkout` and `dir` where it names the repository on the host crew runs on, and otherwise `<session dir>/<name>/main` and `<session dir>/<name>`. It SHALL say a checkout is moved only by its host: the fleet's timer, or the runner on a runner host.

#### Scenario: The design brief on a runner host
- **WHEN** deneb's teams file names `agentplot/blueprints` and `agentplot/crew` with their containers and views, and agentplot's design agent's brief is built on deneb
- **THEN** it names the blueprints view as its checkout with the blueprints container as its folder, and crew's view as crew's checkout with crew's container as its folder

#### Scenario: The design brief where the file names none
- **WHEN** the teams file gives no `repositories`, and deneb's agentplot session at `/Users/chuck/Code/github_agentplot` keeps `agentplot/crew`
- **THEN** the design brief names `/Users/chuck/Code/github_agentplot/crew/main` as crew's checkout, in the folder `/Users/chuck/Code/github_agentplot/crew`

### Requirement: The operator's brief names swancloud's checkout and folder as its host keeps them
The operator's brief SHALL name swancloud's checkout and folder as its main level's host keeps `afterthought/swancloud`, found as the design agent's are, for its fetch, its worktree under `<folder>/places/` and that worktree's removal. Where that host keeps none, the brief SHALL say so in words, never leaving a token blank.

#### Scenario: The operator's swancloud on a runner host
- **WHEN** deneb's teams file names `afterthought/swancloud` with its container and its view, and afterthought's operator's brief is built on deneb
- **THEN** it fetches in swancloud's view and cuts its `crew-teams-<label>` worktree under the container's `places/`, naming no `~/Code/github_afterthought/swancloud`

#### Scenario: A box's operator
- **WHEN** wldn's main level runs on the box, whose spaces and file keep no `afterthought/swancloud`
- **THEN** the operator's brief builds with every token filled, saying the host keeps no checkout of swancloud, and sends a change to the teams to a partition whose main level keeps one
