## ADDED Requirements

### Requirement: The teams file is the one file crew reads of a host's drives and hosts
`teams.json` SHALL list each drive with a main level, under `drives`, and SHALL give every fact crew reads of a host's drives and of the hosts that serve them. crew SHALL read no other file for them, swancloud's `~/.config/swancloud/herdr-hosts.json` among them, and SHALL start with no such file present.

#### Scenario: No hosts file
- **WHEN** a host has a teams file giving every key and no `~/.config/swancloud/herdr-hosts.json`
- **THEN** crew loads the teams file and its commands run as they would with one

#### Scenario: A session's `partition` in the hosts file
- **WHEN** a host's `~/.config/swancloud/herdr-hosts.json` gives wldn's session `wldn-2` a `partition`, a folder, an account or an ssh name the teams file does not give
- **THEN** crew loads the teams file the same as with no hosts file, and reads nothing of it

### Requirement: Each drive's entry names its label, its repositories and where its main level runs
Each drive's entry SHALL give:
- its label (`wldn`, `madswan`, `agentplot`), which is its one name;
- its blueprints repos, the first being the one its signals and elaboration go to by default;
- its state repository (`state`, as `<owner>/<name>`);
- the machine and session its main level runs in;
- `folder`, the absolute folder of its herdr session on its machine;
- `repos`, the repositories that folder keeps on its machine, each by its address, `<owner>/<name>`.

#### Scenario: clients/willdan
- **WHEN** `teams.json` lists the drive `wldn` with willdan-blueprints and `WilldanGroup/crew-state`, running on chuck-herdr-alpha in `wldn-2`, its folder `/workspace` and its `repos` naming willdan-blueprints, and `hosts` names chuck-herdr-alpha
- **THEN** `crew main up wldn` starts its main level in `wldn-2` on chuck-herdr-alpha, in `/workspace/willdan-blueprints/main`, and wldn's plan is read from `wldn/main` of `WilldanGroup/crew-state`

### Requirement: Each drive's entry names the account and the running of each main-level role
Each drive's entry SHALL also give:
- `accounts`, naming each of its five main-level roles, `design`, `planner`, `reviewer`, `ops` and `operator`, with the Claude account it runs under, a name crew accepts;
- `flume`, naming each of the same five roles as `false` while it stands or as the Flume stream its runs run in on the main level's host.

#### Scenario: An account left out
- **WHEN** wldn's `accounts` names `design`, `planner`, `ops` and `operator`, and no `reviewer`
- **THEN** crew refuses to load the teams file, naming wldn and the reviewer

#### Scenario: A role crew has no kind for
- **WHEN** madswan's `flume` names `dispatcher`, leaves out `operator`, or gives `planner` the value `true`
- **THEN** crew refuses to load the teams file, naming the drive and the role

### Requirement: Every refusal of the teams file names its writer as the fix
Every refusal of the file SHALL name as its fix the teams file's writer: crew's own module, `services.crew`, `crew drive set`, or the machine's configuration that writes the file. A host with no teams file SHALL be refused naming the same writers, and a file that is no JSON naming the file and why, each with nothing done. No refusal of the file SHALL name a module of another repository's as its fix.

#### Scenario: Every refusal of the file names crew's own fix
- **WHEN** crew refuses `teams.json` for being missing, for its version, for a `teams` key, for listing no drives, for a drive's `state`, `review`, `flume`, `folder`, `repos` or `accounts`, for its `hosts`, for a kept repository named wrongly, or for its `consoles`
- **THEN** the refusal names crew's own module, `services.crew`, `crew drive set`, or the machine's configuration that writes the file as the fix, and no module of swancloud's or of any other repository's

#### Scenario: No teams file
- **WHEN** a host has no `~/.config/crew/teams.json` and `crew bolts` runs there
- **THEN** it is refused naming the file and `crew drive set` among its writers, and does nothing

#### Scenario: A file that is no JSON
- **WHEN** `~/.config/crew/teams.json` holds text that is no JSON
- **THEN** crew refuses to load it, naming the file and the parser's words, with no traceback, and does nothing

### Requirement: A drive's first blueprints repo is kept on its machine
A drive's first blueprints repo SHALL be kept on its machine: among its `repos`, or named in `repositories` where its machine is the host the file is written on.

#### Scenario: A blueprints repo its machine does not keep
- **WHEN** wldn's `repos` does not list `WilldanGroup/willdan-blueprints`, and chuck-herdr-alpha's teams file does not name it in `repositories`
- **THEN** crew refuses to load the teams file, naming wldn, chuck-herdr-alpha and the repository

### Requirement: A drive's entry that lacks a field crew requires is an error, never a default
A drive whose entry lacks `state`, `folder`, `repos`, `accounts` or `flume` SHALL be an error naming the drive, the field and the teams file's writer as the fix, never a default.

#### Scenario: A drive with no state repository
- **WHEN** a drive's entry has no `state`
- **THEN** crew refuses to load the teams file, naming the drive and the missing field

#### Scenario: A drive with no folder, repos or accounts
- **WHEN** a drive's entry has no `folder`, no `repos` or no `accounts`
- **THEN** crew refuses to load the teams file, naming the drive, the missing field and the teams file's writer, and does nothing

#### Scenario: A drive with no flume
- **WHEN** a drive's entry has no `flume`
- **THEN** crew refuses to load the teams file, naming the drive, the field and the teams file's writer

### Requirement: A drive's entry with a field crew does not accept is an error
Each of these SHALL be an error naming the drive, the field and the teams file's writer as the fix, never a default: a `folder` that is not absolute, a `repos` entry that is no `<owner>/<name>`, an `accounts` or a `flume` that leaves a role out or names another key, an account that is no name crew accepts, a `flume` role given anything but `false` or a stream's name, and two roles that run in one session and name two accounts, since a herdr session runs under one.

#### Scenario: A relative folder
- **WHEN** a drive's `folder` is `work/willdan`
- **THEN** crew refuses to load the teams file, naming the drive and its `folder`

#### Scenario: Two accounts in one session
- **WHEN** wldn's design agent and ops run in `wldn-2`, and its `accounts` gives the design agent `willdan-alex` and ops `credits`
- **THEN** crew refuses to load the teams file, naming wldn, `wldn-2` and both accounts

### Requirement: The teams file names each host crew reaches by its ssh name and kind
The file's `hosts` SHALL name each host crew reaches or reads, by the name `hostname -s` gives it, each giving exactly its `ssh` name and its `kind`, `darwin` or `nixos`. A file with no `hosts`, a drive whose `machine` it does not name, a host name crew does not accept, and an entry that lacks either key, gives another, or gives a `kind` that is neither SHALL be refused, naming the file, the host and the fix, with nothing done.

#### Scenario: A machine the file gives no host for
- **WHEN** wldn's `machine` is `chuck-herdr-alpha` and `hosts` names only `deneb`
- **THEN** crew refuses to load the teams file, naming wldn, chuck-herdr-alpha and `hosts`

#### Scenario: No hosts
- **WHEN** `teams.json` gives no `hosts`
- **THEN** crew refuses to load the teams file, naming `hosts` and the teams file's writer, and does nothing

#### Scenario: A host named wrongly
- **WHEN** `hosts` gives deneb no `ssh`, gives it a `kind` of `macos`, or gives it a `home` beside its `ssh` and `kind`
- **THEN** crew refuses to load the teams file, naming deneb and the key

### Requirement: crew reads version 6 of the teams file alone
crew SHALL read version 6 of the file alone. A file at any other version, version 5 and its `partitions` among them, or one holding `teams`, SHALL be refused naming the teams file's writer as the fix, with nothing done. crew SHALL read no `partitions` key and no entry's `partition`.

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

### Requirement: A role runs in the session the teams file names for it
A drive's `roles.<role>` MAY name a `session` of the main level's machine where that role runs while it stands. crew SHALL check it against no list of sessions: herdr runs the session the file names.

#### Scenario: The planner in a session of its own
- **WHEN** wldn's entry names `roles.planner.session` as `wldn-1`
- **THEN** `wldn-planner` runs in `wldn-1` and its other main-level roles in the main level's session

#### Scenario: A session of another drive
- **WHEN** wldn's `roles.planner.session` names `madswan`, another drive's session
- **THEN** crew loads the teams file, and `wldn-planner` runs in the session `madswan` on chuck-herdr-alpha, as the file names it

### Requirement: A host's kept repositories are named in the teams file with their folder and checkout
The host's kept repositories, where the file names them, SHALL be its `repositories`. That is an object keyed by each repository's address, `<owner>/<name>`, each giving exactly its `dir`, the folder crew names as the kit's, and its `checkout`, the working tree crew names as the kit's checkout, each an absolute path. crew SHALL check every entry when it loads the file, before any is used. A file with no `repositories` SHALL load, naming no repository.

#### Scenario: A runner host's kept repositories
- **WHEN** deneb's `teams.json` gives `repositories` naming `agentplot/crew` with `dir` `/Users/chuck/.local/share/flywheel/repositories/agentplot/crew` and `checkout` `/Users/chuck/Code/boomdrive/agentplot/crew`
- **THEN** crew loads the file, and on deneb names that folder and that checkout as crew's

### Requirement: A kept repository the teams file names wrongly is refused
A `repositories` that is no object, a key that is no `<owner>/<name>`, or an entry that lacks `dir` or `checkout`, gives another key, or gives a path that is not absolute SHALL be refused, naming the file, the repository and the teams file's writer as the fix, with nothing done.

#### Scenario: A kept repository named wrongly
- **WHEN** `repositories` names `crew` with no owner, or names `agentplot/crew` with no `checkout`, with a `dir` of `repositories/agentplot/crew`, or with a `view` beside its `dir` and `checkout`
- **THEN** crew refuses to load the teams file, naming the file, the repository and the teams file's writer, and does nothing

### Requirement: Where a host keeps a repository is read from the teams file alone
Where a host keeps a repository SHALL be read from the file alone: the `repositories` entry, where the file names the repository and the host is the one the file is written on; otherwise `<folder>/<name>` and its checkout `<folder>/<name>/main`, in the folder of the first drive, in the file's order, whose machine is that host and whose `repos` lists the repository. A host keeps no other repository.

#### Scenario: A file that names no repository
- **WHEN** `teams.json` gives no `repositories`, and madswan runs on mac-studio with its `folder` `/w/madswan` and its `repos` naming `agentplot/crew`
- **THEN** crew loads it, and names crew's folder on mac-studio `/w/madswan/crew` and its checkout `/w/madswan/crew/main`

#### Scenario: A repository no drive of the host lists
- **WHEN** mac-studio's teams file names no `WilldanGroup/atlas-kit` in `repositories`, and no drive whose machine is mac-studio lists it in `repos`
- **THEN** mac-studio keeps no atlas-kit, whatever folder on it holds one

### Requirement: The teams file names the consoles its host opens
The file's `consoles` MAY name, for the host it is written on, each drive whose console that host opens, by its label, with the absolute folder the console's tabs open in. A label the file lists no drive by and a folder that is not absolute SHALL be refused, naming the file and the fix. A file with no `consoles` SHALL load, naming no console.

#### Scenario: The consoles of the host
- **WHEN** deneb's teams file gives `consoles` naming `wldn` with `/Users/chuck/Code/clients/github_willdan` and `agentplot` with `/Users/chuck/Code/github_agentplot`
- **THEN** crew loads it, and deneb opens the consoles of wldn and agentplot

#### Scenario: A console of no drive
- **WHEN** `consoles` names `swancloud`, and the file lists no drive `swancloud`
- **THEN** crew refuses to load the teams file, naming `swancloud` and `consoles`

### Requirement: crew main up opens the main level's workspace with a tab for each standing role
`crew main up <label>` SHALL open a herdr workspace named `<label>` in the main level's session. It SHALL hold a `design` tab with the design agent, a `planner` tab with the planner, an `ops` tab with the main-level ops and an `operator` tab with the drive's operator, each only while it stands, and start each, and nothing else.

#### Scenario: The main level comes up
- **WHEN** `crew main up wldn` runs and wldn's `flume` names every role `false`
- **THEN** `wldn-design`, `wldn-planner`, `wldn-ops` and `wldn-operator` start in the `wldn` workspace, each is greeted once it is up, and no dispatcher starts on any host

### Requirement: A role that runs as its kind gets no tab, no start and no revive
A role that runs as its kind SHALL get no tab and no start: `crew main up` SHALL instead write its role record to match the teams file, and SHALL end a standing agent of it still running once that agent is not working, leaving one working and saying so. `crew revive` SHALL bring back no role its drive runs as its kind.

#### Scenario: Two roles run as their kinds
- **WHEN** madswan's `flume` names a stream for its reviewer and its planner, and `crew main up madswan` runs
- **THEN** the `madswan` workspace has no `planner` tab and no planner is started or greeted, `roles.rec` on `madswan/main` holds the planner's and the reviewer's records, and the design agent, ops and the operator start as today

#### Scenario: A standing planner from before
- **WHEN** madswan's `flume` has just come to name a stream for its planner, `madswan-planner` still stands idle in its tab, and `crew main up madswan` runs
- **THEN** `madswan-planner`'s standing agent is ended and the command says so; had it been working, it would be left and named

### Requirement: Every agent crew starts is greeted once per start
Every agent crew starts, the main level's standing roles, SHALL be greeted once it is up, exactly once per start: told to read where the drive stands and carry on with what is its role's. The greeting SHALL be marked as crew's. An agent brought back by `crew revive` or `crew main up` after the main level was taken down SHALL be greeted the same way, so none sits idle until someone tells it what to do.

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

### Requirement: The design agent keeps the design true on main and answers the questions brought to it
The design agent SHALL keep the drive's design true on main: the books, specs and constitution in its blueprints repos and kits, the decision records, and the curation of signals with the moves `attach`, `challenge`, `new-territory`, `answered` and `drop`, each written only through `crew signal move`. It SHALL answer a design question a stage, the planner or ops brings it. A construct's linked questions SHALL be answered together, in one answer, after reading.

#### Scenario: Linked questions
- **WHEN** three questions from one construct about the same stack reach the design agent together
- **THEN** the design agent reads what they turn on and answers all three in one message

### Requirement: Work the design agent's elaboration calls for is queued as units
Work the design agent's elaboration calls for SHALL be queued as units, never put into a bolt by the design agent, each with an intent that names the outcome and sources that name the records governing it, never the mechanism.

#### Scenario: Elaboration produces work
- **WHEN** the design agent records a decision that needs building
- **THEN** it queues a unit whose intent says what becomes true and whose source is the decision's page, and tells the planner

### Requirement: A ruling names what it rests on, read by the design agent itself
A ruling the design agent gives about how a service or a system behaves SHALL name, in the message that carries it, the documentation page or the reading it rests on. Before ruling about something that exists, the design agent SHALL read it itself with the credentials it has: the live configuration, the stack, the policy, the code on main.

#### Scenario: A question about a live service
- **WHEN** a question reaches the design agent asking whether an existing CloudFormation stack can take over a resource, and the design agent can read the stack with its credentials
- **THEN** it reads the stack and the service's documentation before answering, and its answer names the page and the reading it rests on

### Requirement: A ruling waits for its reading and leaves the steps to the construct
Where the design agent has neither documentation nor a reading, it SHALL say so and ask for the reading, and SHALL give no ruling on that point until the reading is back. A ruling SHALL say what must be true and what must not change, and SHALL leave the steps to the construct.

#### Scenario: Nothing to rest a ruling on
- **WHEN** a question turns on how a service behaves, and the design agent can neither find the documentation nor read the thing itself
- **THEN** it says so, names the reading it needs and asks for it, and rules on that point only once the reading is back

#### Scenario: A sequence is asked for
- **WHEN** a construct asks in what order to take over an AWS boundary
- **THEN** the design agent answers with what must be true when the takeover is done and what must not change along the way, and the construct works out the steps from its own reading

### Requirement: A kit's deployer asks crew for each deploy with its release notes and steps
A kit's deployer SHALL ask crew for each deploy of a `manual` environment with `crew ops offer <env> --to <sha> --from <sha|none> [--notes <file>] [--steps <file>]`, the notes file the kit's release notes for the range from the environment's last deployed commit to the offered one as the kit's changelog tool writes them, the steps file the range's after-deploy steps one a line as the deployer gathers them (`step <n> <doer> <when> <environments> <why> <text>`).

#### Scenario: A deploy offered with its notes and steps
- **WHEN** the deployer runs `crew ops offer mac-studio` with `--notes` naming the range's release notes and `--steps` naming its steps file
- **THEN** crew raises the deploy's card, keyed `deploy/mac-studio`, in main-level ops's name with the notes and the steps on its face

### Requirement: An offer raises one card for its deploy in main-level ops's name
`crew ops offer` SHALL raise the deploy's card in main-level ops's name, keyed `deploy/<env>`, with the notes and the steps on its face and nothing of them written by crew, change it when a newer head is offered, post it again when the commit already offered is offered again with the same files and main-level ops holds no card open under `deploy/<env>`, writing no second offer, and tell main-level ops the line that adopts it, `call get_request (requestId <id>, name <role>)`.

#### Scenario: The same commit offered again after its card was refused
- **WHEN** Pending You refused deneb's deploy card for `ddcf2cb`, and the deployer offers deneb `ddcf2cb` again with the same notes and steps
- **THEN** crew posts deneb's deploy card under `deploy/deneb`, the run record gains no second `ops.offer` for it, and main-level ops is told the line that adopts the card

#### Scenario: The same commit offered again while its card is open
- **WHEN** swancloud-ops's card for deneb's offer of `ddcf2cb` is open, and the deployer offers deneb `ddcf2cb` again with the same notes and steps
- **THEN** nothing is written, posted or changed

### Requirement: The user's word holds the deploy's card, and the deploy's end closes it
The user's word SHALL be holding the deploy's card, recorded with `crew ops approve`. `crew ops record --act end` SHALL close the card with the deploy's outcome when that end spends the user's word, naming the deploy and the commit the user approved when the deploy is a newer one.

#### Scenario: A deploy offered and approved
- **WHEN** the deployer offers mac-studio a deploy of main's head and the user holds its card
- **THEN** main-level ops runs `crew ops approve`, the row leaves the rail, `crew ops word mac-studio` prints the commit until the deploy's end is recorded, and `crew ops record mac-studio --act end` closes the card with each step's outcome

#### Scenario: An approval for another commit
- **WHEN** `crew ops approve` names a commit other than the open offer's
- **THEN** it is refused, recorded as refused, and no word is given

### Requirement: A step the user is to take, or held for their word, has a card until it is marked
`crew ops step` SHALL raise a step's card, keyed `op/<env>/<n>`, when the step's doer is the user or the step is marked held for the user's word, SHALL change it when the step is recorded again while it is open with other words, another doer or another hold, printing the line that adopts it whether it changed it or not, and SHALL close it when the step is recorded done or declined.

#### Scenario: An operation the user is to take
- **WHEN** the deployer records a step whose doer is the user as waiting, after a deploy or on its own
- **THEN** the rail shows it under operations with its `do` card until it is recorded done or declined, and `crew ops steps` gives its latest state

#### Scenario: A held step
- **WHEN** the deployer records a step whose doer is main-ops and marked held, after mac-studio's deploy
- **THEN** the rail shows it under operations with a card asking now, when quiet or skip, and the step runs when the user answers

### Requirement: The word stands for its commit until that deploy or a newer one ends
`crew ops word` SHALL give the commit the word is for until the end is recorded of that deploy or of a newer deploy of the environment, one whose start is recorded after the word was given, whatever its outcome; the end of a deploy running when the word was given, or of one whose start the record lacks, SHALL leave the word standing. Every `crew ops` command SHALL run where the drive's main level runs.

#### Scenario: A newer deploy ends before the deploy approved
- **WHEN** the user's word for mac-studio is for `3b12e8f`, and the deployer then starts and ends a deploy of `8651be6` there
- **THEN** `crew ops word mac-studio` gives no commit, `deploy/mac-studio`'s card is closed "Deployed 8651be6 to mac-studio, newer than the 3b12e8f you approved: …", and the board says `3b12e8f` was approved, then the deploy of `8651be6` ended first

#### Scenario: A deploy running when the word was given ends
- **WHEN** a deploy of `8651be6` to mac-studio started before the user's word for `3b12e8f`, and it ends
- **THEN** `crew ops word mac-studio` still gives `3b12e8f`, and its card stays open for that deploy

### Requirement: A record the user asks to change is revised, still proposed
On a note asking for changes, the design agent SHALL revise the record, still proposed, commit it and run `crew record … --proposed` again, which closes the card the user answered with the new commit named and puts the revised record on a new card that follows it; a record revised while its card still waits on the user changes the card in place with the new commit named.

#### Scenario: The user asks for changes
- **WHEN** the user answers the card with a note asking for a change
- **THEN** the design agent revises the record, commits it still proposed, and the card the user answered is closed, "Revised at …", naming the new commit, with a new card for the revised record following it

### Requirement: A record the user says no to is rejected in their words
On a no, the design agent SHALL mark the record rejected, in the user's words, take out the rules drawn from it, and run `crew record … --rejected`, which closes the card.

#### Scenario: The user says no
- **WHEN** the user rejects the card
- **THEN** the record's status becomes rejected with the user's words, every rule drawn from it is taken out, and the card is closed with the commit

### Requirement: A red main's fix is launched on main for a runner to take, its submission held
`crew main fix <kit> <name> "<the failure's words>"`, main-level ops's or the user's on reading the kit's main red after a landing, SHALL append a launch of the fix kind on `main`, named `main--<name>`, its brief the failure's words, its submission held and its recipient `<label>/ops`, in the kit's repository as the drive's kits name it and naming no host or stream, for a runner whose configuration names the repository to take, in the stream its host maps it to.

#### Scenario: Main red after a landing
- **WHEN** crew's main fails its checks after a landing and ops runs `crew main fix crew a-test-reads-its-fixture "<the check's words>"`
- **THEN** `requests.rec` gains a launch of `fix` named `main--a-test-reads-its-fixture` on `main` in crew, its submission held, recipient `madswan/ops`, naming no host or stream

### Requirement: A fix of main takes no team, and its drop drops its launch
`crew main fix` SHALL take no `--team`. `--drop` SHALL drop its launch.

#### Scenario: A fix of main dropped
- **WHEN** `crew main fix crew red "<the failure's words>"` has appended its launch, and `crew main fix crew red --drop` runs
- **THEN** `requests.rec` gains a drop of `fix/main/crew/red` naming that launch

### Requirement: A fix of main's land is carried to the runner on the user's send of its row
Once a fix of main's code has delivered and its submission waits held, the kit's landings row SHALL carry it, and the user's send of that row SHALL be the one word that lands it: crew SHALL carry the send to the runner as a land of the fix's launch, by its own act and in ops's name, with no agent running anything, and the runner submits the fix's place (record 0056 decision 6).

#### Scenario: The user's send
- **WHEN** the runner's record shows `main--a-test-reads-its-fixture`'s code delivered and its submission held, and the user sends crew's landings card with it ticked
- **THEN** crew's next raise of the card appends one land of the fix's launch to `requests.rec`, ahead of the lands of the bolts the same send ticked, and a raise after it appends none

### Requirement: A fix of main sent by hand is refused, and nothing else submits it
`crew main fix <kit> <name> --send`, with or without `--excerpt`, SHALL refuse at once, before it reads anything, saying a fix of main lands on the user's send of its row on the kit's landings card, which crew carries to the runner, and SHALL append nothing. Nothing else SHALL submit it.

#### Scenario: Sent by hand
- **WHEN** ops runs `crew main fix crew a-test-reads-its-fixture --send`, or the same with `--excerpt "<the user's words>"`
- **THEN** it is refused before anything is read, naming the send of the fix's row on crew's landings card as the way, and `requests.rec` is as it was

### Requirement: The planner alone proposes bolts, and changes the plan only by a proposal the user approves
The planner SHALL be the only agent that proposes bolts, the placing of units into bolts, and their splitting, ordering or moving between bolts, and SHALL change the plan only through a proposal the user approves. It SHALL route signals to work. A change to a bolt in flight SHALL wait on the user's approval alone. The planner SHALL NOT start a unit's stage.

#### Scenario: A finding mid-bolt
- **WHEN** a stage stops short reporting that a unit needs work outside its bolt's goal
- **THEN** the planner proposes queuing that work or adding it to another bolt, and the bolt keeps its goal

#### Scenario: New work beside a bolt in flight
- **WHEN** the planner judges that new work belongs in a bolt in flight
- **THEN** it proposes the unit for that bolt, no agent's agreement is asked, and the unit is in the bolt only once the user has approved the proposal

### Requirement: An intent the planner writes names the outcome, never the mechanism
An intent the planner writes SHALL name the outcome, and the unit's sources SHALL name the records that govern it; the intent SHALL NOT name the mechanism.

#### Scenario: A changed mechanism
- **WHEN** a construct finds that the way a unit's sources describe doing something won't work, and the records are amended
- **THEN** the unit's intent still holds, and the planner proposes no amendment for it

### Requirement: Corrections to a unit in construct are proposed as one amendment once it settles
Corrections to a unit whose construct is still running SHALL be held and proposed as one amendment once that construct has settled, unless one of them blocks the bolt's work now, which SHALL be proposed at once with the others held so far.

#### Scenario: Corrections arrive during construct
- **WHEN** two corrections to a unit arrive while its construct is still running, and neither stops the bolt's work
- **THEN** the planner holds both, and once the construct has settled proposes one `unit amend` that carries both

#### Scenario: A correction that blocks the bolt's work
- **WHEN** a correction arrives without which the unit's construct, or another unit, cannot go on
- **THEN** the planner proposes the amendment at once, with any other corrections it holds for that unit

### Requirement: A tell prompts an agent by its name, and fails for one not up or waiting on a question
`crew tell <agent> "<text>"` SHALL prompt any agent crew starts, by its name alone, in the host and session where it runs. An agent that is not up SHALL be reported and the command SHALL fail, with nothing sent. An agent waiting on a question in its pane SHALL be reported the same way, naming the wait, and nothing SHALL be typed into the question: a tell is delivered as a prompt the agent receives, never as text that lands in a dialog and is lost.

#### Scenario: The planner asks the design agent
- **WHEN** `wldn-planner` on the box runs `crew tell wldn-design "<question>"`
- **THEN** the design agent in `wldn-2` receives the question

#### Scenario: The agent is waiting on a question
- **WHEN** `crew tell wldn-ops "<text>"` runs while wldn-ops has a question open in its pane
- **THEN** the command fails, says wldn-ops is waiting on a question in its pane, and nothing is typed there; the sender tells it again once the question is answered

#### Scenario: The question is answered
- **WHEN** the user answers or dismisses wldn-ops' question, and `crew tell wldn-ops "<text>"` runs again
- **THEN** wldn-ops receives the text as a prompt

#### Scenario: A pane crew cannot find
- **WHEN** herdr on the agent's host lists no agent named wldn-planner in its session
- **THEN** `crew tell wldn-planner "<text>"` fails saying it is not up, and nothing is sent

### Requirement: An agent waits on a question while a question it opened has no answer
An agent is waiting on a question when herdr reports it blocked, or when it has opened a question or a plan for the user's answer in Claude Code and that call has no answer yet in its session, however the dialog looks on screen. crew's greetings and notices SHALL be delivered on the same terms as a tell.

#### Scenario: A question herdr does not see
- **WHEN** wldn-ops has a question open in its pane that herdr reports as idle, and `crew tell wldn-ops "<text>"` runs
- **THEN** the command fails the same way, and nothing is typed there

#### Scenario: An agent greeted while it waits on a question
- **WHEN** crew greets `wldn-ops` while it has a question open which herdr reports as idle
- **THEN** the greeting waits until the question is answered, as it does for one herdr reports blocked, and is then sent once

### Requirement: A tell reads the agent's session from herdr or from crew's record
The agent's session is the one herdr names for its pane, or, when herdr names none, the newest session crew recorded of that agent starting in that pane. When neither names a session, herdr's reading of the pane alone SHALL guard the tell, and a missing session SHALL NOT refuse it.

#### Scenario: A main-level agent herdr names no session for
- **WHEN** wldn-planner sits idle in `wldn-2` after herdr's own restore resumed its pane, herdr names no Claude session for that pane, and the design agent runs `crew tell wldn-planner "<text>"`
- **THEN** wldn-planner receives the text as a prompt, marked with who sent it

#### Scenario: A question open in a pane herdr names no session for
- **WHEN** herdr names no Claude session for wldn-planner's pane and reports it idle, crew's record names the session that last started in that pane, that session has a question open, and `crew tell wldn-planner "<text>"` runs
- **THEN** the command fails, says wldn-planner is waiting on a question in its pane, and nothing is typed there

#### Scenario: Neither herdr nor crew names a session
- **WHEN** herdr names no Claude session for wldn-planner's pane and crew holds no record of a session of wldn-planner starting in that pane
- **THEN** `crew tell wldn-planner "<text>"` is typed unless herdr reports the agent blocked, and herdr's own refusal of a blocked agent at the moment of typing still fails it with nothing typed

### Requirement: A tell crew cannot guard is refused, naming what crew could not read
When crew cannot read whether the agent is waiting on a question, it SHALL refuse the tell as it does one to an agent waiting on a question, naming what it could not read, and type nothing.

#### Scenario: crew cannot read whether a question is open
- **WHEN** wldn-ops opened a question and crew cannot read its session to learn whether it has been answered
- **THEN** `crew tell wldn-ops "<text>"` fails naming what it could not read, and nothing is typed there

### Requirement: A tell to a role that runs as its kind is written as an ask of the role
A tell to a role its drive runs as its kind, `<label>-<role>`, whose standing agent is not up, SHALL NOT fail for it: it SHALL be written as an ask of the role, from the sender, `crew` for crew's own notice, carrying the text, and the command SHALL say it asked the role and type nothing. A standing agent of that role still up SHALL be told as today.

#### Scenario: A role that runs as its kind
- **WHEN** madswan's planner runs as its kind, herdr lists no agent named madswan-planner, and madswan-design runs `crew tell madswan-planner "<text>"`
- **THEN** an ask of the planner from madswan-design holds the text, nothing is typed, and the command says it asked madswan-planner

### Requirement: The operator's brief names where its host keeps swancloud, or says it keeps none
The operator's brief SHALL name swancloud's checkout and folder as its main level's host keeps `afterthought/swancloud`, found as the design agent's are, for its worktree under `<folder>/places/`, cut from `origin/main`, and that worktree's removal. Where that host keeps none, the brief SHALL say so in words, never leaving a token blank.

#### Scenario: A box's operator
- **WHEN** wldn's main level runs on the box, whose spaces and file keep no `afterthought/swancloud`
- **THEN** the operator's brief builds with every token filled, saying the host keeps no checkout of swancloud, and sends a change to the teams to a drive whose main level keeps one

### Requirement: The operator's brief fetches swancloud first unless its checkout is the runner's clone
The operator's brief SHALL fetch swancloud's checkout first, but where that checkout is the runner's clone, where it SHALL fetch nothing and cut from `origin/main` as the runner last fetched it.

#### Scenario: The operator's swancloud on a runner host
- **WHEN** deneb's teams file names `afterthought/swancloud` with its container and its view, and afterthought's operator's brief is built on deneb
- **THEN** it cuts its `crew-teams-<label>` worktree from swancloud's view under the container's `places/` with no fetch, from `origin/main` as the runner last fetched it, naming no `~/Code/github_afterthought/swancloud` and no `fetch -q origin`

#### Scenario: The operator's swancloud on a Mac with no runner's clone
- **WHEN** mac-studio's spaces keep `afterthought/swancloud` and its teams file names none
- **THEN** the operator's brief fetches in swancloud's checkout first and cuts its worktree from `origin/main`, as before

### Requirement: Main-level ops answers a landing that does not land from the runner's report alone
What follows a landing that does not land SHALL be main-level ops's, read from the runner's report alone (record 0056 decision 5). A landing fix that asks reaches ops as its recipient, and ops SHALL tell the user it waits and on what.

#### Scenario: A landing fix that asks
- **WHEN** main-level ops's brief is read
- **THEN** it says crew cannot answer a fix it did not launch, so ops tells the user in one line that it waits and on what

### Requirement: Main-level ops starts no fix that Flume's landing fix covers
Where the bolt's row says Flume's landing fix covers it, whether that fix takes main in, makes a failed check pass, or is still to be launched, ops SHALL start nothing and tell the user in one line. Where crew asks ops because Flume ran its bound of landing fixes, or its fix was dropped or not launched, ops SHALL start a fix on the bolt with Flume's words, or tell the planner and the user in one line where the bolt should not land.

#### Scenario: Flume's landing fix
- **WHEN** main-level ops's brief is read
- **THEN** it says that where the bolt's row says Flume's landing fix takes main in, makes the failed checks pass, or is launched by Flume, ops starts nothing and tells the user in one line, and that where crew asks it after Flume ran its landing fixes, ops starts a fix by hand with Flume's words or tells the planner and the user

### Requirement: Main-level ops starts the fix a failed check or a forecast conflict needs, and records a stop as a signal
Where the bolt's row names no landing fix of Flume's: for a check that failed, ops SHALL start a fix on the bolt with Flume's words; for a conflict, whose take-main fix crew's read launches, ops SHALL start nothing; and for a forecast conflict, ops SHALL start the take-main fix. A landing the runner or Flume stopped, nothing of the bolt's, ops SHALL record as a signal and tell the planner of in one line, the bolt landing again only on the user's next send.

#### Scenario: What follows a landing that does not land
- **WHEN** main-level ops's brief is read
- **THEN** it says a check that failed is a fix on the bolt ops starts with `crew fix <bolt> <name> "<Flume's words>"`, that a conflict's take-main fix is crew's to launch and ops starts nothing for it, and that a stop is recorded as a signal and told to the planner, the bolt landing again on the user's next send

## REMOVED Requirements

### Requirement: Drives are declared in the teams file
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "The teams file is the one file crew reads of a host's drives and hosts", "Each drive's entry names its label, its repositories and where its main level runs", "Each drive's entry names the account and the running of each main-level role", "Every refusal of the teams file names its writer as the fix", "A drive's first blueprints repo is kept on its machine", "A drive's entry that lacks a field crew requires is an error, never a default", "A drive's entry with a field crew does not accept is an error", "The teams file names each host crew reaches by its ssh name and kind", "crew reads version 6 of the teams file alone", "A role runs in the session the teams file names for it", "A host's kept repositories are named in the teams file with their folder and checkout", "A kept repository the teams file names wrongly is refused", "Where a host keeps a repository is read from the teams file alone" and "The teams file names the consoles its host opens".

### Requirement: The main level is one herdr workspace
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "crew main up opens the main level's workspace with a tab for each standing role", "A role that runs as its kind gets no tab, no start and no revive" and "Every agent crew starts is greeted once per start".

### Requirement: The design agent elaborates on main
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "The design agent keeps the design true on main and answers the questions brought to it", "Work the design agent's elaboration calls for is queued as units", "A ruling names what it rests on, read by the design agent itself" and "A ruling waits for its reading and leaves the steps to the construct".

### Requirement: A deploy and every operation are approved and recorded through crew
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A kit's deployer asks crew for each deploy with its release notes and steps", "An offer raises one card for its deploy in main-level ops's name", "The user's word holds the deploy's card, and the deploy's end closes it", "A step the user is to take, or held for their word, has a card until it is marked" and "The word stands for its commit until that deploy or a newer one ends".

### Requirement: A record the user does not accept is revised or rejected
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A record the user asks to change is revised, still proposed" and "A record the user says no to is rejected in their words".

### Requirement: A red main's fix is a fix place on main in the kit's repository
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A red main's fix is launched on main for a runner to take, its submission held" and "A fix of main takes no team, and its drop drops its launch".

### Requirement: A fix of main lands on the user's send
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A fix of main's land is carried to the runner on the user's send of its row" and "A fix of main sent by hand is refused, and nothing else submits it".

### Requirement: The planner plans across bolts by proposal alone
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "The planner alone proposes bolts, and changes the plan only by a proposal the user approves", "An intent the planner writes names the outcome, never the mechanism" and "Corrections to a unit in construct are proposed as one amendment once it settles".

### Requirement: Any agent crew starts is reached by its name
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A tell prompts an agent by its name, and fails for one not up or waiting on a question", "An agent waits on a question while a question it opened has no answer", "A tell reads the agent's session from herdr or from crew's record", "A tell crew cannot guard is refused, naming what crew could not read" and "A tell to a role that runs as its kind is written as an ask of the role".

### Requirement: The operator's brief names swancloud's checkout and folder as its host keeps them
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "The operator's brief names where its host keeps swancloud, or says it keeps none" and "The operator's brief fetches swancloud first unless its checkout is the runner's clone".

### Requirement: Main-level ops answers a landing that does not land
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "Main-level ops answers a landing that does not land from the runner's report alone", "Main-level ops starts no fix that Flume's landing fix covers" and "Main-level ops starts the fix a failed check or a forecast conflict needs, and records a stop as a signal".
