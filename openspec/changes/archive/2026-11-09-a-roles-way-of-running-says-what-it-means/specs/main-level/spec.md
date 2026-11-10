## MODIFIED Requirements

### Requirement: Drives are declared in the teams file
`teams.json` SHALL list each drive with a main level, under `drives`, and SHALL give every fact crew reads of a host's drives and of the hosts that serve them. crew SHALL read no other file for them, swancloud's `~/.config/swancloud/herdr-hosts.json` among them, and SHALL start with no such file present.

Each drive's entry gives:
- its label (`wldn`, `madswan`, `agentplot`), which is its one name;
- its blueprints repos, the first being the one its signals and elaboration go to by default;
- its state repository (`state`, as `<owner>/<name>`);
- the machine and session its main level runs in;
- `folder`, the absolute folder of its herdr session on its machine;
- `repos`, the repositories that folder keeps on its machine, each by its address, `<owner>/<name>`;
- `accounts`, naming each of its five main-level roles, `design`, `planner`, `reviewer`, `ops` and `operator`, with the Claude account it runs under, a name crew accepts;
- `runs`, naming each of the same five roles with how it runs: `standing`, crew keeping the role's agent running in its pane on the drive's machine, or `on-demand`, the host's runner having Flume run the role in the drive's own stream, the one its label names, while something is pending for it, each run ending when its work is done;
- `review`, its batch setting, `after_changes` and `after_hours` (review-batches, "A batch spans the drive's bolts").

Every refusal of the file SHALL name as its fix the teams file's writer: crew's own module, `services.crew`, `crew drive set`, or the machine's configuration that writes the file. A host with no teams file SHALL be refused naming the same writers, and a file that is no JSON naming the file and why, each with nothing done. No refusal of the file SHALL name a module of another repository's as its fix.

A drive's first blueprints repo SHALL be kept on its machine: among its `repos`, or named in `repositories` where its machine is the host the file is written on. A drive whose entry lacks `state`, `folder`, `repos`, `accounts`, `review` or `runs` SHALL be an error naming the drive, the field and the teams file's writer as the fix, never a default. So SHALL a `folder` that is not absolute, a `repos` entry that is no `<owner>/<name>`, an `accounts` or a `runs` that leaves a role out or names another key, an account that is no name crew accepts, a `runs` role given anything but `standing` or `on-demand`, a `review` that lacks `after_changes` or `after_hours` or names another key, an `after_changes` that is no whole number of at least 1, an `after_hours` that is no number above 0, and two roles that run in one session and name two accounts, since a herdr session runs under one.

A drive's entry that names `flume`, or a `review` that names `every` or `hours`, SHALL be refused naming the drive and the key, saying the file names how each role runs under `runs` and the batch setting by `after_changes` and `after_hours`, with the teams file's writer as the fix, whatever else the entry gives. crew SHALL read no `flume`, `every` or `hours`, and SHALL name no stream for a role: a role that runs on demand runs in the stream its drive's label names.

The file's `hosts` SHALL name each host crew reaches or reads, by the name `hostname -s` gives it, each giving exactly its `ssh` name and its `kind`, `darwin` or `nixos`. A file with no `hosts`, a drive whose `machine` it does not name, a host name crew does not accept, and an entry that lacks either key, gives another, or gives a `kind` that is neither SHALL be refused, naming the file, the host and the fix, with nothing done.

crew SHALL read version 6 of the file alone. A file at any other version, version 5 and its `partitions` among them, or one holding `teams`, SHALL be refused naming the teams file's writer as the fix, with nothing done. crew SHALL read no `partitions` key and no entry's `partition`. A drive's `roles.<role>` MAY name a `session` of the main level's machine where that role runs while it stands. crew SHALL check it against no list of sessions: herdr runs the session the file names.

The host's kept repositories, where the file names them, SHALL be its `repositories`. That is an object keyed by each repository's address, `<owner>/<name>`, each giving exactly its `dir`, the folder crew names as the kit's, and its `checkout`, the working tree crew names as the kit's checkout, each an absolute path. crew SHALL check every entry when it loads the file, before any is used. A `repositories` that is no object, a key that is no `<owner>/<name>`, or an entry that lacks `dir` or `checkout`, gives another key, or gives a path that is not absolute SHALL be refused, naming the file, the repository and the teams file's writer as the fix, with nothing done. A file with no `repositories` SHALL load, naming no repository.

Where a host keeps a repository SHALL be read from the file alone: the `repositories` entry, where the file names the repository and the host is the one the file is written on; otherwise `<folder>/<name>` and its checkout `<folder>/<name>/main`, in the folder of the first drive, in the file's order, whose machine is that host and whose `repos` lists the repository. A host keeps no other repository.

The file's `consoles` MAY name, for the host it is written on, each drive whose console that host opens, by its label, with the absolute folder the console's tabs open in. A label the file lists no drive by and a folder that is not absolute SHALL be refused, naming the file and the fix. A file with no `consoles` SHALL load, naming no console.

#### Scenario: clients/willdan
- **WHEN** `teams.json` lists the drive `wldn` with willdan-blueprints and `WilldanGroup/crew-state`, running on chuck-herdr-alpha in `wldn-2`, its folder `/workspace` and its `repos` naming willdan-blueprints, and `hosts` names chuck-herdr-alpha
- **THEN** `crew main up wldn` starts its main level in `wldn-2` on chuck-herdr-alpha, in `/workspace/willdan-blueprints/main`, and wldn's plan is read from `wldn/main` of `WilldanGroup/crew-state`

#### Scenario: No hosts file
- **WHEN** a host has a teams file giving every key and no `~/.config/swancloud/herdr-hosts.json`
- **THEN** crew loads the teams file and its commands run as they would with one

#### Scenario: A session's `partition` in the hosts file
- **WHEN** a host's `~/.config/swancloud/herdr-hosts.json` gives wldn's session `wldn-2` a `partition`, a folder, an account or an ssh name the teams file does not give
- **THEN** crew loads the teams file the same as with no hosts file, and reads nothing of it

#### Scenario: A drive with no state repository
- **WHEN** a drive's entry has no `state`
- **THEN** crew refuses to load the teams file, naming the drive and the missing field

#### Scenario: A drive with no folder, repos or accounts
- **WHEN** a drive's entry has no `folder`, no `repos` or no `accounts`
- **THEN** crew refuses to load the teams file, naming the drive, the missing field and the teams file's writer, and does nothing

#### Scenario: A relative folder
- **WHEN** a drive's `folder` is `work/willdan`
- **THEN** crew refuses to load the teams file, naming the drive and its `folder`

#### Scenario: An account left out
- **WHEN** wldn's `accounts` names `design`, `planner`, `ops` and `operator`, and no `reviewer`
- **THEN** crew refuses to load the teams file, naming wldn and the reviewer

#### Scenario: Two accounts in one session
- **WHEN** wldn's design agent and ops run in `wldn-2`, and its `accounts` gives the design agent `willdan-alex` and ops `credits`
- **THEN** crew refuses to load the teams file, naming wldn, `wldn-2` and both accounts

#### Scenario: A blueprints repo its machine does not keep
- **WHEN** wldn's `repos` does not list `WilldanGroup/willdan-blueprints`, and chuck-herdr-alpha's teams file does not name it in `repositories`
- **THEN** crew refuses to load the teams file, naming wldn, chuck-herdr-alpha and the repository

#### Scenario: A machine the file gives no host for
- **WHEN** wldn's `machine` is `chuck-herdr-alpha` and `hosts` names only `deneb`
- **THEN** crew refuses to load the teams file, naming wldn, chuck-herdr-alpha and `hosts`

#### Scenario: No hosts
- **WHEN** `teams.json` gives no `hosts`
- **THEN** crew refuses to load the teams file, naming `hosts` and the teams file's writer, and does nothing

#### Scenario: A host named wrongly
- **WHEN** `hosts` gives deneb no `ssh`, gives it a `kind` of `macos`, or gives it a `home` beside its `ssh` and `kind`
- **THEN** crew refuses to load the teams file, naming deneb and the key

#### Scenario: The planner in a session of its own
- **WHEN** wldn's entry names `roles.planner.session` as `wldn-1`
- **THEN** `wldn-planner` runs in `wldn-1` and its other main-level roles in the main level's session

#### Scenario: A session of another drive
- **WHEN** wldn's `roles.planner.session` names `madswan`, another drive's session
- **THEN** crew loads the teams file, and `wldn-planner` runs in the session `madswan` on chuck-herdr-alpha, as the file names it

#### Scenario: A drive with no flume
- **WHEN** a drive's entry has no `flume` and gives `runs`, naming each of its five roles `standing` or `on-demand`
- **THEN** crew loads the teams file

#### Scenario: A drive with no runs
- **WHEN** a drive's entry has no `runs`
- **THEN** crew refuses to load the teams file, naming the drive, the field and the teams file's writer

#### Scenario: A role crew has no kind for
- **WHEN** madswan's `runs` names `dispatcher`, leaves out `operator`, or gives `planner` the value `false`, `true` or `madswan`
- **THEN** crew refuses to load the teams file, naming the drive and the role

#### Scenario: Each role standing or on demand
- **WHEN** madswan's `runs` names its planner and its reviewer `on-demand` and its design agent, ops and operator `standing`
- **THEN** crew loads the teams file, madswan's planner and reviewer run on demand in the stream `madswan`, and its design agent, ops and operator stand

#### Scenario: A drive that names flume
- **WHEN** the file is at version 6 and madswan's entry names `flume`, beside a `runs` or with none
- **THEN** crew refuses to load it, naming madswan and `flume`, saying the file names how each role runs under `runs`, and naming the teams file's writer, and does nothing

#### Scenario: A batch setting by its former names
- **WHEN** the file is at version 6 and wldn's `review` gives `every` 5 and `hours` 4
- **THEN** crew refuses to load it, naming wldn and `review.every`, saying the batch setting is `after_changes` and `after_hours`, and naming the teams file's writer, and does nothing

#### Scenario: A batch setting out of range
- **WHEN** wldn's `review` gives `after_changes` 0, or `after_hours` 0
- **THEN** crew refuses to load the teams file, naming wldn and the key, with its unit and range

#### Scenario: The file before version 4
- **WHEN** `teams.json` is at version 3
- **THEN** crew refuses to load it, naming its version and the teams file's writer, and does nothing

#### Scenario: The file before version 5
- **WHEN** `teams.json` is at version 4, its `teams` listing a team for each kit
- **THEN** crew refuses to load it, naming its version and the teams file's writer, and does nothing

#### Scenario: The file at version 5
- **WHEN** `teams.json` is at version 5, its `partitions` each naming its `partition`, as deneb's file held them on 2026-11-08
- **THEN** crew refuses to load it, naming its version, that crew reads only version 6, and the teams file's writer, and does nothing

#### Scenario: The box's file at version 2
- **WHEN** `teams.json` is at version 2, its `partitions` and its `teams` as chuck-herdr-alpha's file holds them for wldn's teams
- **THEN** crew refuses to load it, naming its version, that crew reads only version 6, and the teams file's writer, and does nothing

#### Scenario: A version-5 file that lists teams
- **WHEN** `teams.json` is at version 5 and holds a `teams` key beside its `partitions`
- **THEN** crew refuses to load it, naming its version, that crew reads only version 6, and the teams file's writer, and does nothing

#### Scenario: A version-6 file that lists teams
- **WHEN** `teams.json` is at version 6 and holds a `teams` key beside its `drives`
- **THEN** crew refuses to load it, saying version 6 has no place for teams since crew runs none, naming the teams file's writer, and does nothing

#### Scenario: A version-6 file whose drives are under `partitions`
- **WHEN** `teams.json` is at version 6 and lists its drives under `partitions`, with no `drives`
- **THEN** crew refuses to load it, saying it lists no drives, naming the teams file's writer, and does nothing

#### Scenario: Every refusal of the file names crew's own fix
- **WHEN** crew refuses `teams.json` for being missing, for its version, for a `teams` key, for listing no drives, for a drive's `state`, `review`, `runs`, `flume`, `folder`, `repos` or `accounts`, for its `hosts`, for a kept repository named wrongly, or for its `consoles`
- **THEN** the refusal names crew's own module, `services.crew`, `crew drive set`, or the machine's configuration that writes the file as the fix, and no module of swancloud's or of any other repository's

#### Scenario: No teams file
- **WHEN** a host has no `~/.config/crew/teams.json` and `crew bolts` runs there
- **THEN** it is refused naming the file and `crew drive set` among its writers, and does nothing

#### Scenario: A file that is no JSON
- **WHEN** `~/.config/crew/teams.json` holds text that is no JSON
- **THEN** crew refuses to load it, naming the file and the parser's words, with no traceback, and does nothing

#### Scenario: A runner host's kept repositories
- **WHEN** deneb's `teams.json` gives `repositories` naming `agentplot/crew` with `dir` `/Users/chuck/.local/share/flywheel/repositories/agentplot/crew` and `checkout` `/Users/chuck/Code/boomdrive/agentplot/crew`
- **THEN** crew loads the file, and on deneb names that folder and that checkout as crew's

#### Scenario: A kept repository named wrongly
- **WHEN** `repositories` names `crew` with no owner, or names `agentplot/crew` with no `checkout`, with a `dir` of `repositories/agentplot/crew`, or with a `view` beside its `dir` and `checkout`
- **THEN** crew refuses to load the teams file, naming the file, the repository and the teams file's writer, and does nothing

#### Scenario: A file that names no repository
- **WHEN** `teams.json` gives no `repositories`, and madswan runs on mac-studio with its `folder` `/w/madswan` and its `repos` naming `agentplot/crew`
- **THEN** crew loads it, and names crew's folder on mac-studio `/w/madswan/crew` and its checkout `/w/madswan/crew/main`

#### Scenario: A repository no drive of the host lists
- **WHEN** mac-studio's teams file names no `WilldanGroup/atlas-kit` in `repositories`, and no drive whose machine is mac-studio lists it in `repos`
- **THEN** mac-studio keeps no atlas-kit, whatever folder on it holds one

#### Scenario: The consoles of the host
- **WHEN** deneb's teams file gives `consoles` naming `wldn` with `/Users/chuck/Code/clients/github_willdan` and `agentplot` with `/Users/chuck/Code/github_agentplot`
- **THEN** crew loads it, and deneb opens the consoles of wldn and agentplot

#### Scenario: A console of no drive
- **WHEN** `consoles` names `swancloud`, and the file lists no drive `swancloud`
- **THEN** crew refuses to load the teams file, naming `swancloud` and `consoles`

### Requirement: The main level is one herdr workspace
`crew main up <label>` SHALL open a herdr workspace named `<label>` in the main level's session. It SHALL hold a `design` tab with the design agent, a `planner` tab with the planner, an `ops` tab with the main-level ops and an `operator` tab with the drive's operator, each only while it stands, and start each, and nothing else. A role its drive's `runs` names `on-demand`, which runs as its kind, SHALL get no tab and no start: `crew main up` SHALL instead write its role record to match the teams file, and SHALL end a standing agent of it still running once that agent is not working, leaving one working and saying so.

Every agent crew starts, the main level's standing roles, SHALL be greeted once it is up, exactly once per start: told to read where the drive stands and carry on with what is its role's. The greeting SHALL be marked as crew's. An agent brought back by `crew revive` or `crew main up` after the main level was taken down SHALL be greeted the same way, so none sits idle until someone tells it what to do. `crew revive` SHALL bring back no role its drive runs as its kind.

#### Scenario: The main level comes up
- **WHEN** `crew main up wldn` runs and wldn's `runs` names every role `standing`
- **THEN** `wldn-design`, `wldn-planner`, `wldn-ops` and `wldn-operator` start in the `wldn` workspace, each is greeted once it is up, and no dispatcher starts on any host

#### Scenario: Two roles run as their kinds
- **WHEN** madswan's `runs` names its reviewer and its planner `on-demand`, and `crew main up madswan` runs
- **THEN** the `madswan` workspace has no `planner` tab and no planner is started or greeted, `roles.rec` on `madswan/main` holds the planner's and the reviewer's records, and the design agent, ops and the operator start as today

#### Scenario: A standing planner from before
- **WHEN** madswan's `runs` has just come to name its planner `on-demand`, `madswan-planner` still stands idle in its tab, and `crew main up madswan` runs
- **THEN** `madswan-planner`'s standing agent is ended and the command says so; had it been working, it would be left and named

#### Scenario: The main level comes back
- **WHEN** the user runs `crew main down swancloud` and then `crew main up swancloud`
- **THEN** each of its standing agents starts and is greeted, and picks up its role from the rail and the bolts without the user or the operator telling it to

#### Scenario: Brought up again while it is up
- **WHEN** `crew main up wldn` runs while its agents are up
- **THEN** none is started and none is greeted

#### Scenario: Revived after a restart
- **WHEN** a host restarts, `wldn-design`'s pane comes back with no agent in it, and `crew revive` runs there
- **THEN** `wldn-design` is brought back and greeted once, and no agent that came back by itself is greeted

#### Scenario: An agent waiting on a question
- **WHEN** `crew main up wldn` starts `wldn-planner` stopped on a question in its pane
- **THEN** the design agent and ops are greeted without waiting on it, the command says `wldn-planner` waits on a question and will be greeted once it is answered, and it is greeted once, after the answer

#### Scenario: An agent that never settles
- **WHEN** an agent `crew main up` started is still not ready to greet when crew stops waiting for it
- **THEN** the command says so, names the `crew tell` that would greet it, and still succeeds

### Requirement: A role that runs as its kind is not started by crew-role
`crew-role <label> <role>`, fresh or with `resume`, SHALL refuse a role its drive runs as its kind, naming `crew role open <role> --label <label>`, and start no Claude. `crew main status <label>` SHALL say of each such role that it runs as its kind, whether the runner's records show a run of it standing, and how many asks wait for it since when, naming as its stream the drive's label.

#### Scenario: The planner started by hand
- **WHEN** madswan's planner runs as its kind and `crew-role madswan planner` runs
- **THEN** it refuses, saying madswan's planner runs as its kind and is opened with `crew role open planner --label madswan`, and no Claude starts

#### Scenario: Main status
- **WHEN** madswan's planner runs as its kind, two asks of it wait and no run of it stands, and `crew main status madswan` runs
- **THEN** it says the planner runs as its kind in stream `madswan`, that no run stands, and that two asks wait, with the oldest's age
