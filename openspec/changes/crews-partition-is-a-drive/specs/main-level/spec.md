## RENAMED Requirements

- FROM: `### Requirement: Partitions are declared in the teams file`
- TO: `### Requirement: Drives are declared in the teams file`

- FROM: `### Requirement: A red main's fix stays a bolt of one chore where no runner answers for the partition`
- TO: `### Requirement: A red main's fix stays a bolt of one chore where no runner answers for the drive`


## MODIFIED Requirements

### Requirement: Drives are declared in the teams file
`teams.json` SHALL list each drive with a main level, under `drives`. Beside its drives it MAY name, for the host it is written on, each repository that host keeps, and nothing else. Each drive's entry gives the drive's label (`wldn`, `madswan`, `agentplot`), which is its one name, its blueprints repos, its state repository (`state`, as `<owner>/<name>`), the machine and session its main level runs in, and `flume`, naming each of its five main-level roles, `design`, `planner`, `reviewer`, `ops` and `operator`, as `false` while it stands or as the Flume stream its runs run in on the main level's host. The first blueprints repo listed SHALL be the one the drive's signals and elaboration go to by default. A drive with no `state` or no `flume` SHALL be an error naming the field and the machine's configuration as the fix, never a default, and so SHALL a `flume` that leaves a role out, names another key, or gives a role anything but `false` or a stream's name. crew SHALL read version 6 of the file alone: a file at any other version, version 5 and its `partitions` among them, or one holding `teams`, SHALL be refused naming swancloud's `lib/crew-teams.nix` as the fix, with nothing done; crew SHALL read no `partitions` key and no entry's `partition`. A drive's `roles.<role>` MAY name a `session` for a main-level role, a session the hosts file lists on the main level's machine, where that role runs while it stands; any other session SHALL be an error naming it. crew SHALL read no session's `partition` in the hosts file: the drive names its sessions, and the fleet's configuration checks what it writes there.

The host's kept repositories, where the file names them, SHALL be its `repositories`. That is an object keyed by each repository's address, `<owner>/<name>`, each giving exactly its `dir`, the folder crew names as the kit's, and its `checkout`, the working tree crew names as the kit's checkout, each an absolute path. crew SHALL check every entry when it loads the file, before any is used. A `repositories` that is no object, a key that is no `<owner>/<name>`, or an entry that lacks `dir` or `checkout`, gives another key, or gives a path that is not absolute SHALL be refused, naming the file, the repository and the machine's configuration as the fix, with nothing done. A file with no `repositories` SHALL load as before, naming no repository.

#### Scenario: clients/willdan
- **WHEN** `teams.json` lists the drive `wldn` with willdan-blueprints and `WilldanGroup/crew-state`, running on the box in `wldn-2`, a session the hosts file puts in `clients/willdan`
- **THEN** `crew main up wldn` starts its main level in `wldn-2` on the box, and wldn's plan is read from `wldn/main` of `WilldanGroup/crew-state`

#### Scenario: A partition with no state repository
- **WHEN** a drive's entry has no `state`
- **THEN** crew refuses to load the teams file, naming the drive and the missing field

#### Scenario: The planner in a session of its own
- **WHEN** wldn's entry names `roles.planner.session` as `wldn-1`, a session the hosts file lists on chuck-herdr-alpha
- **THEN** `wldn-planner` runs in `wldn-1` and its other main-level roles in the main level's session

#### Scenario: A session of another partition
- **WHEN** wldn's `roles.planner.session` names `madswan`, another drive's session, which the hosts file lists on deneb and not on chuck-herdr-alpha
- **THEN** crew refuses to load the teams file, naming the planner, the session and the machine

#### Scenario: A session's `partition` in the hosts file
- **WHEN** the hosts file gives wldn's session `wldn-2` a `partition` of `clients/willdan`, of `business`, or none
- **THEN** crew loads the teams file the same each time, reading nothing of it

#### Scenario: A partition with no flume
- **WHEN** a drive's entry has no `flume`
- **THEN** crew refuses to load the teams file, naming the drive, the field and swancloud's `lib/crew-teams.nix`

#### Scenario: A role crew has no kind for
- **WHEN** madswan's `flume` names `dispatcher`, leaves out `operator`, or gives `planner` the value `true`
- **THEN** crew refuses to load the teams file, naming the drive and the role

#### Scenario: The file before version 4
- **WHEN** `teams.json` is at version 3
- **THEN** crew refuses to load it, naming its version and swancloud's `lib/crew-teams.nix`, and does nothing

#### Scenario: The file before version 5
- **WHEN** `teams.json` is at version 4, its `teams` listing a team for each kit
- **THEN** crew refuses to load it, naming its version and swancloud's `lib/crew-teams.nix`, and does nothing

#### Scenario: The file at version 5
- **WHEN** `teams.json` is at version 5, its `partitions` each naming its `partition`, as deneb's file held them on 2026-11-08
- **THEN** crew refuses to load it, naming its version, that crew reads only version 6, and swancloud's `lib/crew-teams.nix`, and does nothing

#### Scenario: The box's file at version 2
- **WHEN** `teams.json` is at version 2, its `partitions` and its `teams` as chuck-herdr-alpha's file holds them for wldn's teams
- **THEN** crew refuses to load it, naming its version, that crew reads only version 6, and swancloud's `lib/crew-teams.nix`, and does nothing

#### Scenario: A version-5 file that lists teams
- **WHEN** `teams.json` is at version 5 and holds a `teams` key beside its `partitions`
- **THEN** crew refuses to load it, naming its version, that crew reads only version 6, and swancloud's `lib/crew-teams.nix`, and does nothing

#### Scenario: A version-6 file that lists teams
- **WHEN** `teams.json` is at version 6 and holds a `teams` key beside its `drives`
- **THEN** crew refuses to load it, saying version 6 has no place for teams since crew runs none, naming swancloud's `lib/crew-teams.nix`, and does nothing

#### Scenario: A version-6 file whose drives are under `partitions`
- **WHEN** `teams.json` is at version 6 and lists its drives under `partitions`, with no `drives`
- **THEN** crew refuses to load it, saying it lists no drives, naming swancloud's `lib/crew-teams.nix`, and does nothing

#### Scenario: A runner host's kept repositories
- **WHEN** deneb's `teams.json` gives `repositories` naming `agentplot/crew` with `dir` `/Users/chuck/.local/share/flywheel/repositories/agentplot/crew` and `checkout` `/Users/chuck/Code/boomdrive/agentplot/crew`
- **THEN** crew loads the file, and on deneb names that folder and that checkout as crew's

#### Scenario: A kept repository named wrongly
- **WHEN** `repositories` names `crew` with no owner, or names `agentplot/crew` with no `checkout`, with a `dir` of `repositories/agentplot/crew`, or with a `view` beside its `dir` and `checkout`
- **THEN** crew refuses to load the teams file, naming the file, the repository and the machine's configuration, and does nothing

#### Scenario: A file that names no repository
- **WHEN** `teams.json` gives no `repositories`
- **THEN** crew loads it, and names every kit's folder and checkout as the sessions in the hosts file keep it, `<session dir>/<name>` and `<session dir>/<name>/main`

### Requirement: The main level is one herdr workspace
`crew main up <label>` SHALL open a herdr workspace named `<label>` in the main level's session. It SHALL hold a `design` tab with the design agent, a `planner` tab with the planner, an `ops` tab with the main-level ops and an `operator` tab with the drive's operator, each only while it stands, and start each, and nothing else. A role that runs as its kind SHALL get no tab and no start: `crew main up` SHALL instead write its role record to match the teams file, and SHALL end a standing agent of it still running once that agent is not working, leaving one working and saying so.

Every agent crew starts, the main level's standing roles, SHALL be greeted once it is up, exactly once per start: told to read where the drive stands and carry on with what is its role's. The greeting SHALL be marked as crew's. An agent brought back by `crew revive` or `crew main up` after the main level was taken down SHALL be greeted the same way, so none sits idle until someone tells it what to do. `crew revive` SHALL bring back no role its drive runs as its kind.

#### Scenario: The main level comes up
- **WHEN** `crew main up wldn` runs and wldn's `flume` names every role `false`
- **THEN** `wldn-design`, `wldn-planner`, `wldn-ops` and `wldn-operator` start in the `wldn` workspace, each is greeted once it is up, and no dispatcher starts on any host

#### Scenario: Two roles run as their kinds
- **WHEN** madswan's `flume` names a stream for its reviewer and its planner, and `crew main up madswan` runs
- **THEN** the `madswan` workspace has no `planner` tab and no planner is started or greeted, `roles.rec` on `madswan/main` holds the planner's and the reviewer's records, and the design agent, ops and the operator start as today

#### Scenario: A standing planner from before
- **WHEN** madswan's `flume` has just come to name a stream for its planner, `madswan-planner` still stands idle in its tab, and `crew main up madswan` runs
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

### Requirement: The design agent elaborates on main
The design agent SHALL keep the drive's design true on main: the books, specs and constitution in its blueprints repos and kits, the decision records, and the curation of signals with the moves `attach`, `challenge`, `new-territory`, `answered` and `drop`, each written only through `crew signal move`. It SHALL answer a design question a stage, the planner or ops brings it. Work its elaboration calls for SHALL be queued as units, never put into a bolt by the design agent, each with an intent that names the outcome and sources that name the records governing it, never the mechanism.

A ruling the design agent gives about how a service or a system behaves SHALL name, in the message that carries it, the documentation page or the reading it rests on. Before ruling about something that exists, the design agent SHALL read it itself with the credentials it has: the live configuration, the stack, the policy, the code on main. Where it has neither documentation nor a reading, it SHALL say so and ask for the reading, and SHALL give no ruling on that point until the reading is back. A ruling SHALL say what must be true and what must not change, and SHALL leave the steps to the construct. A construct's linked questions SHALL be answered together, in one answer, after reading.

#### Scenario: Elaboration produces work
- **WHEN** the design agent records a decision that needs building
- **THEN** it queues a unit whose intent says what becomes true and whose source is the decision's page, and tells the planner

#### Scenario: A question about a live service
- **WHEN** a question reaches the design agent asking whether an existing CloudFormation stack can take over a resource, and the design agent can read the stack with its credentials
- **THEN** it reads the stack and the service's documentation before answering, and its answer names the page and the reading it rests on

#### Scenario: Nothing to rest a ruling on
- **WHEN** a question turns on how a service behaves, and the design agent can neither find the documentation nor read the thing itself
- **THEN** it says so, names the reading it needs and asks for it, and rules on that point only once the reading is back

#### Scenario: A sequence is asked for
- **WHEN** a construct asks in what order to take over an AWS boundary
- **THEN** the design agent answers with what must be true when the takeover is done and what must not change along the way, and the construct works out the steps from its own reading

#### Scenario: Linked questions
- **WHEN** three questions from one construct about the same stack reach the design agent together
- **THEN** the design agent reads what they turn on and answers all three in one message

### Requirement: Signals reach the plan only through a route
Signals SHALL stay in the drive's first blueprints repo, in the signals model its `signals/README.md` gives. A bolt's agents SHALL record a finding outside their bolt as a signal there with `crew signal`. A signal SHALL become work only through a `route` move written by `crew unit add --signal`.

#### Scenario: A finding from a bolt
- **WHEN** ops on swb-1 finds a defect in a shared service the bolt does not own
- **THEN** it records a signal in willdan-blueprints, and the planner decides whether to route it

### Requirement: A deploy and every operation are approved and recorded through crew
A kit's deployer SHALL ask crew for each deploy of a `manual` environment with `crew ops offer <env> --to <sha> --from <sha|none> [--notes <file>] [--steps <file>]`, the notes file the kit's release notes for the range from the environment's last deployed commit to the offered one as the kit's changelog tool writes them, the steps file the range's after-deploy steps one a line as the deployer gathers them (`step <n> <doer> <when> <environments> <why> <text>`), which SHALL raise the deploy's card in main-level ops's name, keyed `deploy/<env>`, with the notes and the steps on its face and nothing of them written by crew, change it when a newer head is offered, post it again when the commit already offered is offered again with the same files and main-level ops holds no card open under `deploy/<env>`, writing no second offer, and tell main-level ops the line that adopts it, `call get_request (requestId <id>, name <role>)`; the user's word SHALL be holding that card, recorded with `crew ops approve`. `crew ops record --act end` SHALL close the card with the deploy's outcome when that end spends the user's word, naming the deploy and the commit the user approved when the deploy is a newer one. `crew ops step` SHALL raise a step's card, keyed `op/<env>/<n>`, when the step's doer is the user or the step is marked held for the user's word, SHALL change it when the step is recorded again while it is open with other words, another doer or another hold, printing the line that adopts it whether it changed it or not, and SHALL close it when the step is recorded done or declined. `crew ops word` SHALL give the commit the word is for until the end is recorded of that deploy or of a newer deploy of the environment, one whose start is recorded after the word was given, whatever its outcome; the end of a deploy running when the word was given, or of one whose start the record lacks, SHALL leave the word standing. Every `crew ops` command SHALL run where the drive's main level runs.

#### Scenario: A deploy offered and approved
- **WHEN** the deployer offers mac-studio a deploy of main's head and the user holds its card
- **THEN** main-level ops runs `crew ops approve`, the row leaves the rail, `crew ops word mac-studio` prints the commit until the deploy's end is recorded, and `crew ops record mac-studio --act end` closes the card with each step's outcome

#### Scenario: An approval for another commit
- **WHEN** `crew ops approve` names a commit other than the open offer's
- **THEN** it is refused, recorded as refused, and no word is given

#### Scenario: An operation the user is to take
- **WHEN** the deployer records a step whose doer is the user as waiting, after a deploy or on its own
- **THEN** the rail shows it under operations with its `do` card until it is recorded done or declined, and `crew ops steps` gives its latest state

#### Scenario: A held step
- **WHEN** the deployer records a step whose doer is main-ops and marked held, after mac-studio's deploy
- **THEN** the rail shows it under operations with a card asking now, when quiet or skip, and the step runs when the user answers

#### Scenario: The same commit offered again after its card was refused
- **WHEN** Pending You refused deneb's deploy card for `ddcf2cb`, and the deployer offers deneb `ddcf2cb` again with the same notes and steps
- **THEN** crew posts deneb's deploy card under `deploy/deneb`, the run record gains no second `ops.offer` for it, and main-level ops is told the line that adopts the card

#### Scenario: The same commit offered again while its card is open
- **WHEN** swancloud-ops's card for deneb's offer of `ddcf2cb` is open, and the deployer offers deneb `ddcf2cb` again with the same notes and steps
- **THEN** nothing is written, posted or changed

#### Scenario: A newer deploy ends before the deploy approved
- **WHEN** the user's word for mac-studio is for `3b12e8f`, and the deployer then starts and ends a deploy of `8651be6` there
- **THEN** `crew ops word mac-studio` gives no commit, `deploy/mac-studio`'s card is closed "Deployed 8651be6 to mac-studio, newer than the 3b12e8f you approved: …", and the board says `3b12e8f` was approved, then the deploy of `8651be6` ended first

#### Scenario: A deploy running when the word was given ends
- **WHEN** a deploy of `8651be6` to mac-studio started before the user's word for `3b12e8f`, and it ends
- **THEN** `crew ops word mac-studio` still gives `3b12e8f`, and its card stays open for that deploy

### Requirement: A main-level role starts only on its main level's host
`crew-role <label> design|planner|ops|operator|reviewer`, fresh or with `resume`, SHALL start its agent only on the host the teams file names for that drive's main level. On any other host it SHALL refuse, naming the agent, the main level's host and this host, and start no Claude.

#### Scenario: The planner started on the standby
- **WHEN** the teams file puts swancloud's main level on deneb and `crew-role swancloud planner` runs on mac-studio
- **THEN** it refuses, saying that swancloud's main level runs on deneb, not mac-studio, and that crew starts `swancloud-planner` only there, and no Claude is started

#### Scenario: On its host
- **WHEN** `crew-role swancloud planner` runs on deneb
- **THEN** the planner starts as it does today

### Requirement: A record settled in the pane takes the user's words, read as theirs
`crew record … --proposed --settled-in-pane` SHALL record the record settled in the pane only from the user's words, given with `--excerpt`, which crew reads in the caller's own session transcript on this host as the user's (`signals.5`), and only when the caller is the drive's design agent. Otherwise it SHALL refuse with the reason, record nothing and raise no card. Either flag without the other SHALL be refused.

#### Scenario: The design agent's own words
- **WHEN** the design agent runs `crew record crew 31 --proposed --settled-in-pane --excerpt "<words>"`, and the words are only in what the design agent wrote itself
- **THEN** crew refuses, saying only the user's own words in the pane settle a record and to run `crew record crew 31 --proposed` so the user answers on its card, and records nothing

#### Scenario: Another agent's tell of the user's yes
- **WHEN** the words are in the design agent's transcript only in a `[crew tell from swancloud-planner]` message
- **THEN** crew refuses, naming swancloud-planner as the one who said them, and records nothing

#### Scenario: Words crew cannot read as anyone's
- **WHEN** the words are only in crew's own message, in a tool's output, or in a record crew can't classify
- **THEN** crew refuses, saying which, and records nothing

#### Scenario: A transcript crew cannot read
- **WHEN** the caller's session has no transcript on this host, its transcript can't be read, or it has not been written for more than 15 minutes
- **THEN** crew refuses with that reason and records nothing

#### Scenario: Another caller
- **WHEN** an agent other than the drive's design agent, or the user at a terminal, runs `crew record … --proposed --settled-in-pane --excerpt "<words>"`
- **THEN** crew refuses, saying only the design agent records a record settled in its pane, and records nothing

#### Scenario: A flag without the other
- **WHEN** `--settled-in-pane` is given without `--excerpt`, or `--excerpt` without `--settled-in-pane`
- **THEN** crew refuses, naming the flag that is missing, and records nothing

### Requirement: A red main's fix is a fix place on main in the kit's repository
`crew main fix <kit> <name> "<the failure's words>"`, main-level ops's or the user's on reading the kit's main red after a landing, SHALL append a launch of the fix kind on `main`, named `main--<name>`, its brief the failure's words, its submission held and its recipient `<label>/ops`, in the kit's repository as the drive's kits name it and naming no host or stream, for a runner whose configuration names the repository to take, in the stream its host maps it to. It SHALL take no `--team`. `--drop` SHALL drop it.

#### Scenario: Main red after a landing
- **WHEN** crew's main fails its checks after a landing and ops runs `crew main fix crew a-test-reads-its-fixture "<the check's words>"`
- **THEN** `requests.rec` gains a launch of `fix` named `main--a-test-reads-its-fixture` on `main` in crew, its submission held, recipient `madswan/ops`, naming no host or stream

### Requirement: A role that runs as its kind is not started by crew-role
`crew-role <label> <role>`, fresh or with `resume`, SHALL refuse a role its drive runs as its kind, naming `crew role open <role> --label <label>`, and start no Claude. `crew main status <label>` SHALL say of each such role that it runs as its kind, whether the runner's records show a run of it standing, and how many asks wait for it since when.

#### Scenario: The planner started by hand
- **WHEN** madswan's planner runs as its kind and `crew-role madswan planner` runs
- **THEN** it refuses, saying madswan's planner runs as its kind and is opened with `crew role open planner --label madswan`, and no Claude starts

#### Scenario: Main status
- **WHEN** madswan's planner runs as its kind, two asks of it wait and no run of it stands, and `crew main status madswan` runs
- **THEN** it says the planner runs as its kind, that no run stands, and that two asks wait, with the oldest's age

### Requirement: Any agent crew starts is reached by its name
`crew tell <agent> "<text>"` SHALL prompt any agent crew starts, by its name alone, in the host and session where it runs. An agent that is not up SHALL be reported and the command SHALL fail, with nothing sent. An agent waiting on a question in its pane SHALL be reported the same way, naming the wait, and nothing SHALL be typed into the question: a tell is delivered as a prompt the agent receives, never as text that lands in a dialog and is lost. An agent is waiting on a question when herdr reports it blocked, or when it has opened a question or a plan for the user's answer in Claude Code and that call has no answer yet in its session, however the dialog looks on screen. The agent's session is the one herdr names for its pane, or, when herdr names none, the newest session crew recorded of that agent starting in that pane. When neither names a session, herdr's reading of the pane alone SHALL guard the tell, and a missing session SHALL NOT refuse it. When crew cannot read whether the agent is waiting on a question, it SHALL refuse the same way, naming what it could not read, and type nothing. crew's greetings and notices SHALL be delivered on the same terms.

A tell to a role its drive runs as its kind, `<label>-<role>`, whose standing agent is not up, SHALL NOT fail for it: it SHALL be written as an ask of the role, from the sender, `crew` for crew's own notice, carrying the text, and the command SHALL say it asked the role and type nothing. A standing agent of that role still up SHALL be told as today.

#### Scenario: The planner asks the design agent
- **WHEN** `wldn-planner` on the box runs `crew tell wldn-design "<question>"`
- **THEN** the design agent in `wldn-2` receives the question

#### Scenario: The agent is waiting on a question
- **WHEN** `crew tell wldn-ops "<text>"` runs while wldn-ops has a question open in its pane
- **THEN** the command fails, says wldn-ops is waiting on a question in its pane, and nothing is typed there; the sender tells it again once the question is answered

#### Scenario: A question herdr does not see
- **WHEN** wldn-ops has a question open in its pane that herdr reports as idle, and `crew tell wldn-ops "<text>"` runs
- **THEN** the command fails the same way, and nothing is typed there

#### Scenario: The question is answered
- **WHEN** the user answers or dismisses wldn-ops' question, and `crew tell wldn-ops "<text>"` runs again
- **THEN** wldn-ops receives the text as a prompt

#### Scenario: crew cannot read whether a question is open
- **WHEN** wldn-ops opened a question and crew cannot read its session to learn whether it has been answered
- **THEN** `crew tell wldn-ops "<text>"` fails naming what it could not read, and nothing is typed there

#### Scenario: An agent greeted while it waits on a question
- **WHEN** crew greets `wldn-ops` while it has a question open which herdr reports as idle
- **THEN** the greeting waits until the question is answered, as it does for one herdr reports blocked, and is then sent once

#### Scenario: A main-level agent herdr names no session for
- **WHEN** wldn-planner sits idle in `wldn-2` after herdr's own restore resumed its pane, herdr names no Claude session for that pane, and the design agent runs `crew tell wldn-planner "<text>"`
- **THEN** wldn-planner receives the text as a prompt, marked with who sent it

#### Scenario: A question open in a pane herdr names no session for
- **WHEN** herdr names no Claude session for wldn-planner's pane and reports it idle, crew's record names the session that last started in that pane, that session has a question open, and `crew tell wldn-planner "<text>"` runs
- **THEN** the command fails, says wldn-planner is waiting on a question in its pane, and nothing is typed there

#### Scenario: Neither herdr nor crew names a session
- **WHEN** herdr names no Claude session for wldn-planner's pane and crew holds no record of a session of wldn-planner starting in that pane
- **THEN** `crew tell wldn-planner "<text>"` is typed unless herdr reports the agent blocked, and herdr's own refusal of a blocked agent at the moment of typing still fails it with nothing typed

#### Scenario: A pane crew cannot find
- **WHEN** herdr on the agent's host lists no agent named wldn-planner in its session
- **THEN** `crew tell wldn-planner "<text>"` fails saying it is not up, and nothing is sent

#### Scenario: A role that runs as its kind
- **WHEN** madswan's planner runs as its kind, herdr lists no agent named madswan-planner, and madswan-design runs `crew tell madswan-planner "<text>"`
- **THEN** an ask of the planner from madswan-design holds the text, nothing is typed, and the command says it asked madswan-planner

### Requirement: A main-level agent resumed off its host is given no identity, and nothing else of crew's is
When herdr resumes a session without crew's environment and crew's record of it names a drive's design agent, planner, ops, operator or reviewer, crew SHALL give it its name, identity, pane name and brief back only on the host the teams file names for that main level. On any other host the session SHALL get none of them, its record SHALL be left as it was, and it SHALL be told at each start that it is no agent of crew's there, which host the main level runs on, and to do nothing of crew's.

#### Scenario: A replayed pane on the standby
- **WHEN** the teams file puts swancloud's main level on deneb, and herdr on mac-studio resumes a session whose record there names `swancloud-planner`
- **THEN** its commands see no `CREW_AGENT`, `CREW_LABEL` or `SLUICE_AGENT`, its pane is not named `swancloud-planner`, its record is unchanged, and it is told that swancloud's main level runs on deneb and that it is no agent of crew's on mac-studio

#### Scenario: Compacted on the standby
- **WHEN** that session on mac-studio is compacted
- **THEN** it is given no brief, and is told again that it is no agent of crew's there

#### Scenario: Resumed on its host
- **WHEN** herdr on deneb resumes a session whose record names `swancloud-planner`
- **THEN** it gets its name, identity and pane name back, and its brief at a compaction, as today

#### Scenario: The teams file can't be read
- **WHEN** herdr resumes a session whose record names `swancloud-planner` and crew can't read the teams file
- **THEN** it gets no identity, and is told that crew can't tell where swancloud's main level runs, and why

#### Scenario: A team's agent from before
- **WHEN** herdr resumes a session whose record names `crw-5-conductor` or `swancloud-dispatch-deneb`
- **THEN** it is given no name, identity or brief, crew modelling no such agent

### Requirement: A red main's fix stays a bolt of one chore where no runner answers for the drive
Where no runner answers for the drive, its state repository holding no `<label>/runner/<host>`, `crew main fix` SHALL be refused, naming the kit and a bolt of one chore, proposed first among the planned, as the way.

#### Scenario: No runner answers for the partition
- **WHEN** wldn's state repository holds no runner's branch and ops runs `crew main fix switchboard-kit gate-word "<words>"`
- **THEN** it is refused, naming switchboard-kit and a bolt of one chore proposed first among the planned

### Requirement: The operator's brief names swancloud's checkout and folder as its host keeps them
The operator's brief SHALL name swancloud's checkout and folder as its main level's host keeps `afterthought/swancloud`, found as the design agent's are, for its worktree under `<folder>/places/`, cut from `origin/main`, and that worktree's removal. It SHALL fetch swancloud's checkout first, but where that checkout is the runner's clone, where it SHALL fetch nothing and cut from `origin/main` as the runner last fetched it. Where that host keeps none, the brief SHALL say so in words, never leaving a token blank.

#### Scenario: The operator's swancloud on a runner host
- **WHEN** deneb's teams file names `afterthought/swancloud` with its container and its view, and afterthought's operator's brief is built on deneb
- **THEN** it cuts its `crew-teams-<label>` worktree from swancloud's view under the container's `places/` with no fetch, from `origin/main` as the runner last fetched it, naming no `~/Code/github_afterthought/swancloud` and no `fetch -q origin`

#### Scenario: The operator's swancloud on a Mac with no runner's clone
- **WHEN** mac-studio's spaces keep `afterthought/swancloud` and its teams file names none
- **THEN** the operator's brief fetches in swancloud's checkout first and cuts its worktree from `origin/main`, as before

#### Scenario: A box's operator
- **WHEN** wldn's main level runs on the box, whose spaces and file keep no `afterthought/swancloud`
- **THEN** the operator's brief builds with every token filled, saying the host keeps no checkout of swancloud, and sends a change to the teams to a drive whose main level keeps one
