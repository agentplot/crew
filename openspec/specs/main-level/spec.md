# main-level Specification

## Purpose
Above a drive's bolt teams: a design agent that elaborates on main, a planner across the bolts, a dispatcher on each host that runs them, and ops that lands them. Signals are what reaches them from outside.

## Requirements

### Requirement: Signals reach the plan only through a route
Signals SHALL stay in the drive's first blueprints repo, in the signals model its `signals/README.md` gives. A bolt's agents SHALL record a finding outside their bolt as a signal there with `crew signal`. A signal SHALL become work only through a `route` move written by `crew unit add --signal`.

#### Scenario: A finding from a bolt
- **WHEN** ops on swb-1 finds a defect in a shared service the bolt does not own
- **THEN** it records a signal in willdan-blueprints, and the planner decides whether to route it

### Requirement: Every move is written through crew and never merged
Every move SHALL be appended to `moves.rec` on the drive's branch of its state repository, through crew: `route` by `crew unit add --signal`, and `attach`, `challenge`, `new-territory`, `answered` and `drop` by `crew signal move <id> <move>`. Each SHALL be fetched over https, applied to the tip of the branch, checked with `recfix --check`, committed, and pushed without force, applied again to the new tip when the push is refused. A signal SHALL have one move; a second is refused.

#### Scenario: Moves from two hosts
- **WHEN** a route is written on the box while curation writes a drop on mac-studio, both through crew
- **THEN** both moves are in `moves.rec`, one after the other, nothing is merged, and the file passes `recfix --check`

#### Scenario: A signal moved twice
- **WHEN** `crew signal move` names a signal that already has its move
- **THEN** it is refused, naming the move it has

### Requirement: Main-level ops reports results as one glyph per line
Whenever the main-level ops reports the results of a landing's checks, of main's deploy or of any test or proof it ran, it SHALL list them first, before any prose, one bullet per suite, check or proof: ✅ passed, with its counts where the tool gave them; ❌ failed, with how many failed and one line on why; ⏳ not yet run, or still running. It SHALL NOT state a result only in a sentence, nor fold several into one bullet.

#### Scenario: A landing whose gate is still running
- **WHEN** the main-level ops reports a landing while the merge's checks still run
- **THEN** its message opens with a ⏳ bullet for those checks, and says the bolt has not landed yet

#### Scenario: A landing that went through
- **WHEN** the merge's checks passed and main was deployed and found healthy
- **THEN** its message opens with a ✅ bullet for the checks, with their counts, and one for main's deploy, before it says the bolt is closed

### Requirement: A decision record is accepted only on the user's yes
Every decision record the design agent writes, and every amendment it makes to one, SHALL be committed as proposed. A record or an amendment SHALL become accepted only on the user's yes, recorded in the record with the date and where they gave it: in the pane where the record was settled with them, or on the one card crew raises for it through `crew record` when it was not. Until the yes, a rule drawn from the record SHALL be written marked as proposed, and no unit SHALL be queued from it.

#### Scenario: A new record
- **WHEN** the design agent writes record 0021 in crew's `docs/adr/` from the signals, with the user not in its pane
- **THEN** it commits the record with the status proposed and runs `crew record crew 21 --proposed`, which raises one card asking the user to accept it, in the record's words, and queues no unit from it yet

#### Scenario: The user says yes
- **WHEN** the user approves the card for record 0021
- **THEN** the design agent commits the record as accepted by the user on that date, on their card, takes the proposed mark off each rule drawn from it, runs `crew record crew 21 --accepted`, which closes the card, and only then queues the units it calls for

#### Scenario: An amendment to an accepted record
- **WHEN** the design agent amends record 0005, which is accepted, with the user not in its pane
- **THEN** the amendment is marked proposed in the record, the card crew raises carries the amendment's words, and the amendment is accepted only on the user's yes

### Requirement: A record states the user's decisions in its own words
What the user settled in the design talk SHALL be stated in the record in the record's own words, its deciders line naming the user and where and when they settled it, never their words quoted as the decision. When a card is raised for the record, it SHALL say which part is the user's, and when the user settled the whole record in the pane, their yes there SHALL be recorded and no card raised.

#### Scenario: The user's own words
- **WHEN** the user said in the design talk "the landing still needs my yes", and the record rests on it
- **THEN** the record states in its own words that a landing waits on the user's yes, its deciders line names the user in the design talk on that date and quotes none of their words, and the card, when one is raised, says that part is the user's

#### Scenario: The user's yes in the pane is crew's evidence, not the record's
- **WHEN** the user says "Yes, accept 31 as written" in the design agent's pane, and the design agent runs `crew record crew 31 --proposed --settled-in-pane --excerpt "Yes, accept 31 as written"`
- **THEN** crew reads those words in the design agent's transcript as the user's, and the record says it was accepted by the user in the design agent's pane on that date, quoting none of their words

### Requirement: A record's status is recorded through crew
`crew record <kit> <number> --proposed|--accepted|--rejected` SHALL record the record's status with its commit in the run record, and SHALL refuse a status the record's file does not hold at that commit.

#### Scenario: A status the file does not hold
- **WHEN** the design agent runs `crew record crew 32 --accepted` while the file at HEAD still says proposed
- **THEN** the command refuses, naming the file's status, and records nothing

### Requirement: A record's card is raised unless it was settled in the pane
`crew record <kit> <number> --proposed` SHALL put the record at its commit on its card in the design agent's name, raising the card the first time and changing it in place at each new commit, unless `--settled-in-pane --excerpt "<words>"` says the user settled it in the pane; with `--alternatives <file>`, which hands the Markdown of the alternatives a rule of the user's decided between, the rules and each loosened, the card SHALL be a choice.

#### Scenario: A record a rule decided
- **WHEN** the design agent runs `crew record switchboard-kit 32 --proposed --alternatives docs/adr/0032-alternatives.md`
- **THEN** the card is a choice of loosening the rules as drafted, accepting as ruled, or sending back, with the file on its face, and the design agent is woken by the answer

#### Scenario: A record settled in the pane
- **WHEN** the user says "Yes, accept 31 as written" in the design agent's pane, and the design agent commits record 31 as proposed and runs `crew record crew 31 --proposed --settled-in-pane --excerpt "Yes, accept 31 as written"`
- **THEN** the status is recorded with the user's yes as given in the pane, naming the transcript record the words came from and not the words, and no card is raised

### Requirement: A record's card is closed with its accepted or rejected status
`crew record <kit> <number> --accepted` or `--rejected` SHALL close the record's card with the commit that holds the status.

#### Scenario: A record from the signals, accepted on its card
- **WHEN** the design agent runs `crew record crew 32 --proposed`, the user accepts the card, and the design agent commits it accepted and runs `crew record crew 32 --accepted`
- **THEN** the card was raised, and is closed with the accepting commit

### Requirement: A signal names where what its words point at lives
An agent recording a signal whose words point at something made elsewhere (another conversation, a page or prototype, an artifact, files in another repo, a spike) SHALL find it and name in the signal's sentence where it lives, in a form another agent can open: `<owner>/<repo>:<path>`, a branch, or an artifact's link. A conversation's id alone SHALL NOT stand for what the conversation made. The excerpt SHALL stay the words as said.

#### Scenario: The user pastes a conversation's id
- **WHEN** the user asks the planner for work and pastes the id of a conversation, held in another repo, that wrote the design pages and published the artifact the work rests on
- **THEN** the signal the planner records quotes the user's words, id and all, and its sentence names those pages by repo and path and the artifact by its link

### Requirement: A unit made from a signal names what the signal points at
A unit the planner proposes from a signal, or the design agent queues from one, SHALL name with `--source` what the signal points at, beside the signal itself.

#### Scenario: Work queued from a signal that names a page
- **WHEN** the planner proposes a unit from a signal whose sentence names a page in another repo
- **THEN** the unit's sources are the signal and that page, and the construct's prompt carries both

### Requirement: A greeting not taken is reported, with nothing left typed
When the second sending of a greeting is not taken either, crew SHALL leave nothing typed, record no greeting, and say the agent was not greeted, with the `crew tell` that would greet it. When crew cannot read whether the greeting was taken, it SHALL send nothing more and say what it could not read. A greeting that is not delivered SHALL fail nothing else the command does.

#### Scenario: A greeting never taken
- **WHEN** neither sending of wldn-design's greeting shows in its transcript within the time
- **THEN** its input is cleared, crew says wldn-design was not greeted and gives the `crew tell wldn-design "<greeting>"` that would greet it, no greeting is recorded, and `crew main up` goes on with its other agents

### Requirement: A deploy held at a gate whose reviewer is the user waits as the user's step
A deploy a hosted deployer holds at a gate whose reviewer is the user SHALL be recorded by whoever dispatched it as a step that is the user's, waiting, the gate's link its text and the deploy's commit its `--to` when known, with no offer posted for it. Its rail row, the board's Operation lane and main-level ops's view SHALL say the deploy waits at its gate for the user.

#### Scenario: A stand dispatched to dev's gate
- **WHEN** a crew agent dispatches a run that waits at dev's gate, whose one reviewer is the user, and records `crew ops step dev --to 4f2a9c1 --key gate-38612817613 --doer user --state waiting --text <file holding the run's link>`
- **THEN** the rail shows the row `op/dev/<n>` under operations, saying the deploy of 4f2a9c1 to dev waits at its gate for the user with the gate's link, its card is raised, and no deploy offer is made for that commit

#### Scenario: The gate in the views
- **WHEN** the gate's step waits on dev
- **THEN** the board's Operation lane says it waits at its gate for the user, and main-level ops's view names it the gate of 4f2a9c1, not a step after 4f2a9c1

### Requirement: A gate's step ends when the gate is passed or rejected
A gate's step SHALL be recorded done when the deployer's run shows the gate passed, by whoever dispatched it, or by main-level ops on the user's Done; and declined when the gate is rejected or on the user's Skip. Its card SHALL close with that state, as every step's card does.

#### Scenario: The gate passed
- **WHEN** the deployer's run shows it has passed the gate, and its dispatcher records the step done
- **THEN** the step's card is closed as done, and its row leaves the rail

#### Scenario: The user taps Done
- **WHEN** the user approves at the gate and taps Done on the card
- **THEN** main-level ops runs the row's done command, and the card closes

#### Scenario: The gate rejected
- **WHEN** the user rejects the deployment at the gate and taps Skip on the card
- **THEN** main-level ops runs the row's decline command, and the card closes as declined

### Requirement: The main level is a workspace in each of its sessions
`crew main up <label>` SHALL open a `<label>` workspace in each session the main level's roles run in, each role's tab in its session's, and start each role there; `crew main down`, `crew main status`, `crew review` and `crew revive` SHALL find each role in its session.

#### Scenario: Design and planner on two accounts
- **WHEN** swancloud's planner runs in `swancloud-2` and the rest of its main level in `swancloud-1`, and `crew main up swancloud` runs
- **THEN** `swancloud-planner` starts in the `swancloud` workspace of `swancloud-2`, and the design agent, ops and the operator in `swancloud-1`'s

### Requirement: A role is never started twice when its session changes
`crew main up` SHALL refuse while a role's agent still runs in a session it no longer stands in, naming it, and `crew main down` SHALL end it there. Panes a state folder recorded in another session than the one its agents run in now SHALL be set aside and said, never taken for that session's.

#### Scenario: A role moved while it runs
- **WHEN** wldn's teams file names a session for its planner while `wldn-planner` still runs in `wldn-2`, and `crew main up wldn` runs
- **THEN** it refuses, naming `wldn-planner`, its session and pane, and that `crew main down wldn` ends it

#### Scenario: Panes recorded in another session
- **WHEN** swancloud's main level moves from `swancloud-2` to `swancloud-1` and a main-level command runs
- **THEN** the panes recorded in `swancloud-2` are set aside and said, and no agent of `swancloud-1` at the same pane id is taken for one of the main level's

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

### Requirement: A role that runs as its kind is not started by crew-role
`crew-role <label> <role>`, fresh or with `resume`, SHALL refuse a role its drive runs as its kind, naming `crew role open <role> --label <label>`, and start no Claude. `crew main status <label>` SHALL say of each such role that it is `on-demand`, the word its drive's `runs` names it by, and never that it runs as its kind; whether the runner's records show a run of it standing; and how many asks wait for it since when, naming as its stream the drive's label.

#### Scenario: The planner started by hand
- **WHEN** madswan's planner runs as its kind and `crew-role madswan planner` runs
- **THEN** it refuses, saying madswan's planner runs as its kind and is opened with `crew role open planner --label madswan`, and no Claude starts

#### Scenario: Main status
- **WHEN** madswan's `runs` names the planner `on-demand`, two asks of it wait and no run of it stands, and `crew main status madswan` runs
- **THEN** it says the planner is `on-demand` in stream `madswan`, that no run stands, and that two asks wait, with the oldest's age, and not that it runs as its kind

### Requirement: A greeting to a main-level agent is taken or sent again
A greeting crew sends to any agent it starts SHALL be sent only once the agent is ready for input, and crew SHALL then read the agent's transcript to see that Claude received it within a short time. When it does not, and the agent sits idle or done, crew SHALL clear what was left typed in the agent's input and send the greeting once more. Exactly one greeting SHALL reach the agent per start.

#### Scenario: A greeting taken at once
- **WHEN** `crew main up wldn` starts `wldn-ops` and its transcript shows the greeting received moments after crew sent it
- **THEN** crew says wldn-ops was greeted, records one greeting, and sent it once

#### Scenario: A greeting left typed
- **WHEN** crew greets wldn-planner and the planner's transcript shows nothing received within the time, while it sits idle
- **THEN** crew clears the planner's input, sends the greeting once more, and says it was greeted once the transcript shows it

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

#### Scenario: No runner answers for the drive
- **WHEN** wldn's state repository holds no runner's branch and ops runs `crew main fix switchboard-kit gate-word "<words>"`
- **THEN** it is refused, naming switchboard-kit and a bolt of one chore proposed first among the planned

### Requirement: The design agent's brief names each kept repository's checkout and folder as its host keeps them
The design agent's brief SHALL name its default blueprints repository's checkout and folder, and each kit's checkout with its folder, where its worktrees are cut. Each SHALL be the teams file's `checkout` and `dir` where it names the repository on the host crew runs on, and otherwise `<session dir>/<name>/main` and `<session dir>/<name>`. It SHALL say a checkout is moved only by its host: the fleet's timer, or the runner on a runner host.

#### Scenario: The design brief on a runner host
- **WHEN** deneb's teams file names `agentplot/blueprints` and `agentplot/crew` with their containers and views, and agentplot's design agent's brief is built on deneb
- **THEN** it names the blueprints view as its checkout with the blueprints container as its folder, and crew's view as crew's checkout with crew's container as its folder

#### Scenario: The design brief where the file names none
- **WHEN** the teams file gives no `repositories`, and deneb's agentplot session at `/Users/chuck/Code/github_agentplot` keeps `agentplot/crew`
- **THEN** the design brief names `/Users/chuck/Code/github_agentplot/crew/main` as crew's checkout, in the folder `/Users/chuck/Code/github_agentplot/crew`

### Requirement: A bolt lands on the user's send, carried in ops's name
A bolt whose verification is green SHALL land by one procedure, main-level ops's (`plan.16` as record 0056 amends it): the user's send on its kit's landings card, which crew raises in ops's name, the word for every bolt they ticked, which crew itself carries to the runner as a land in ops's name, with no agent running anything (record 0056 points 3 and 5). Nothing else SHALL be a word to land: not the planner, not another agent, not a bolt's row appearing on the rail.

#### Scenario: Landing
- **WHEN** the user sends swb-1's bolt ticked on willdan's landings card
- **THEN** crew's next raise of the card posts the bolt's land to the runner, no agent running anything for it, and once the runner reports the bolt's base place landed, crew's read closes the bolt and the plan no longer holds it

#### Scenario: No word from the planner
- **WHEN** the planner tells the main-level ops that a bolt may land
- **THEN** ops runs nothing, no land is posted for the bolt, and it lands only once the user sends the kit's landings card with it ticked

### Requirement: Main-level ops runs no landing
Main-level ops SHALL run nothing for a landing: it SHALL submit no bolt and no fix of main, wait on no landing, push nothing, level no host's checkout, close no landed bolt by hand, and post, change or close no landings card, since crew carries the user's send to the runner itself and crew's read of the runner's report closes what landed (record 0056 points 1, 4 and 5).

#### Scenario: The brief names no landing of ops's
- **WHEN** main-level ops's brief is read
- **THEN** it says the word to land is the user's send on the kit's landings card, which crew carries to the runner, and that ops runs no landing, submits nothing and closes nothing by hand, and it names no `crew bolt submit`, `wt submit` or `sluice withdraw`

#### Scenario: A landing run from an older brief
- **WHEN** an agent whose brief predates this release runs `crew bolt submit y z --label swancloud`
- **THEN** it is refused before anything is read, saying a bolt lands on the user's send of its row on its kit's landings card, which crew carries to the runner, and `requests.rec` and the run record are as they were

### Requirement: A landing deploys nothing
A landing SHALL deploy nothing. Until a kit's deployer records its deploys through crew, the main-level ops SHALL deploy that kit's main only on the user's word for that deploy. A failure after landing SHALL be a fix on main.

#### Scenario: A landing deploys nothing
- **WHEN** a swancloud bolt lands
- **THEN** nothing is deployed by the landing, and main is deployed only by a later act on the user's word for that deploy

### Requirement: The user's words in ops's pane are no word to land
The user's own words in main-level ops's pane, typed there or told from their shell, SHALL be no word to land a bolt or a fix of main (record 0056 decision 5): ops SHALL land and post nothing on them, and SHALL answer them by telling the user that their send of the row on the kit's landings card lands it. `crew bolt submit` and `crew main fix --send` given `--excerpt` SHALL read no transcript and record no word to land.

#### Scenario: The brief points the user to the card
- **WHEN** main-level ops's brief is read
- **THEN** it says the user's words in its pane asking for a landing are no word to land, that ops answers them by telling the user that their send of the row on the kit's landings card lands it, and it gives no command that lands on those words

#### Scenario: The user's words quoted to land
- **WHEN** the user types "Land crw-5's bolt" in swancloud-ops's pane, and ops runs `crew bolt submit y --excerpt "Land crw-5's bolt"`
- **THEN** the command is refused before it reads anything, saying `y` lands on the user's send of its row on its kit's landings card, which crew carries to the runner; no transcript is read, no `bolt.submit` entry is recorded and no land is posted

### Requirement: A stop said in ops's pane is read as the user's words
When the user's own words in main-level ops's pane stop a bolt's landing, ops SHALL run `crew bolt leave <bolt>... --excerpt "<the user's words>"`. crew SHALL go on only once it finds the words in the caller's own live session transcript, on the host where the command runs, in a record the session received that it reads as the user's under `signals.5`: typed in the pane, or a `crew tell` from `<user>@<host>`. A later echo of the same words SHALL NOT hide the user's record.

#### Scenario: Typed in ops's pane
- **WHEN** the user types "Hold the phone bolt, don't land it yet" in swancloud-ops's pane, and ops runs `crew bolt leave builds-reach-the-phone --excerpt "Hold the phone bolt, don't land it yet"`
- **THEN** crew reads the words as the user's and records the stop

#### Scenario: Told from the user's shell
- **WHEN** the user runs `crew tell swancloud-ops "Hold bolt y."` at a shell, and ops runs `crew bolt leave y --excerpt "Hold bolt y."`
- **THEN** crew records the stop, since a tell from `<user>@<host>` is the user's

### Requirement: A stop crew cannot read as the user's words is refused
`crew bolt leave --excerpt` SHALL refuse, recording no stop, when the words are not in the caller's transcript or are only in what the agent wrote itself; when the record holding them is a tool's output, crew's own message or another agent's tell, which the refusal names; or when crew cannot read the transcript, or cannot tell that it is the live session's.

#### Scenario: Words that are not the user's
- **WHEN** ops runs `crew bolt leave builds-reach-the-phone --excerpt "<words>"` with words only another agent's tell holds
- **THEN** crew refuses, naming the tell, and records no stop

#### Scenario: Ops's own words
- **WHEN** ops writes "the user wants the phone bolt held" in its own reply and runs `crew bolt leave builds-reach-the-phone --excerpt "the user wants the phone bolt held"`
- **THEN** crew refuses, saying the words are not in a record the session received, and records no stop

#### Scenario: A transcript crew cannot read
- **WHEN** ops's session has no transcript on the host where `crew bolt leave` runs, or crew cannot tell that the transcript is the live session's
- **THEN** crew refuses, saying which, and records no stop

### Requirement: A stop is recorded holding none of the user's words
A stop SHALL be recorded on each bolt as a `bolt.leave` entry naming its head, the caller, its session, the transcript record the words were read from and the words' length, and holding none of the words (`record.3`), and crew SHALL raise the bolt's kit's landings card. A stop SHALL end when the user ticks the bolt on a send of that card, or when its head moves.

#### Scenario: Stopped in the pane
- **WHEN** ops runs `crew bolt leave builds-reach-the-phone --excerpt "Hold the phone bolt, don't land it yet"` on the user's words typed in its pane
- **THEN** a `bolt.leave` entry on `bolt/builds-reach-the-phone` is recorded with its head, the transcript record and the words' length, and none of the words, and `land/swancloud` is raised showing it unticked as left

#### Scenario: Asked in the pane after a stop
- **WHEN** the user later tells ops in its pane to land `builds-reach-the-phone`
- **THEN** nothing lands on those words, and the bolt stays left until the user ticks it on a send of `land/swancloud`

#### Scenario: Ticked on a later send
- **WHEN** the user later sends `land/swancloud` with `builds-reach-the-phone` ticked
- **THEN** the stop ends, and the bolt is no longer left

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
- `runs`, naming each of the same five roles with how it runs, `standing` or `on-demand`.

#### Scenario: An account left out
- **WHEN** wldn's `accounts` names `design`, `planner`, `ops` and `operator`, and no `reviewer`
- **THEN** crew refuses to load the teams file, naming wldn and the reviewer

#### Scenario: A role crew has no kind for
- **WHEN** madswan's `runs` names `dispatcher`, leaves out `operator`, or gives `planner` the value `false`, `true` or `madswan`
- **THEN** crew refuses to load the teams file, naming the drive and the role

### Requirement: A role runs standing or on demand, as its drive's runs names it
A role its drive's `runs` names `standing` SHALL be kept running by crew, its agent in its pane on the drive's machine. A role it names `on-demand` SHALL be run by the host's runner, which has Flume run the role in the drive's own stream, the one its label names, while something is pending for it, each run ending when its work is done.

#### Scenario: Each role standing or on demand
- **WHEN** madswan's `runs` names its planner and its reviewer `on-demand` and its design agent, ops and operator `standing`
- **THEN** crew loads the teams file, madswan's planner and reviewer run on demand in the stream `madswan`, and its design agent, ops and operator stand

### Requirement: Each drive's entry gives its batch setting
Each drive's entry SHALL also give `review`, its batch setting, `after_changes` and `after_hours` (review-batches, "A batch spans the drive's bolts"). A `review` that lacks `after_changes` or `after_hours` or names another key, an `after_changes` that is no whole number of at least 1, and an `after_hours` that is no number above 0 SHALL each be an error naming the drive, the key and the teams file's writer as the fix, never a default.

#### Scenario: A batch setting out of range
- **WHEN** wldn's `review` gives `after_changes` 0, or `after_hours` 0
- **THEN** crew refuses to load the teams file, naming wldn and the key, with its unit and range

### Requirement: Every refusal of the teams file names its writer as the fix
Every refusal of the file SHALL name as its fix the teams file's writer: crew's own module, `services.crew`, `crew drive set`, or the machine's configuration that writes the file. A host with no teams file SHALL be refused naming the same writers, and a file that is no JSON naming the file and why, each with nothing done. No refusal of the file SHALL name a module of another repository's as its fix.

#### Scenario: Every refusal of the file names crew's own fix
- **WHEN** crew refuses `teams.json` for being missing, for its version, for a `teams` key, for listing no drives, for a drive's `state`, `review`, `runs`, `flume`, `folder`, `repos` or `accounts`, for its `hosts`, for a kept repository named wrongly, or for its `consoles`
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
A drive whose entry lacks `state`, `folder`, `repos`, `accounts`, `review` or `runs` SHALL be an error naming the drive, the field and the teams file's writer as the fix, never a default.

#### Scenario: A drive with no state repository
- **WHEN** a drive's entry has no `state`
- **THEN** crew refuses to load the teams file, naming the drive and the missing field

#### Scenario: A drive with no folder, repos or accounts
- **WHEN** a drive's entry has no `folder`, no `repos` or no `accounts`
- **THEN** crew refuses to load the teams file, naming the drive, the missing field and the teams file's writer, and does nothing

#### Scenario: A drive with no flume
- **WHEN** a drive's entry has no `flume` and gives `runs`, naming each of its five roles `standing` or `on-demand`
- **THEN** crew loads the teams file

#### Scenario: A drive with no runs
- **WHEN** a drive's entry has no `runs`
- **THEN** crew refuses to load the teams file, naming the drive, the field and the teams file's writer

### Requirement: A drive's entry with a field crew does not accept is an error
Each of these SHALL be an error naming the drive, the field and the teams file's writer as the fix, never a default: a `folder` that is not absolute, a `repos` entry that is no `<owner>/<name>`, an `accounts` or a `runs` that leaves a role out or names another key, an account that is no name crew accepts, a `runs` role given anything but `standing` or `on-demand`, and two roles that run in one session and name two accounts, since a herdr session runs under one.

#### Scenario: A relative folder
- **WHEN** a drive's `folder` is `work/willdan`
- **THEN** crew refuses to load the teams file, naming the drive and its `folder`

#### Scenario: Two accounts in one session
- **WHEN** wldn's design agent and ops run in `wldn-2`, and its `accounts` gives the design agent `willdan-alex` and ops `credits`
- **THEN** crew refuses to load the teams file, naming wldn, `wldn-2` and both accounts

### Requirement: A drive's entry that names a former key is refused
A drive's entry that names `flume`, or a `review` that names `every` or `hours`, SHALL be refused naming the drive and the key, saying the file names how each role runs under `runs` and the batch setting by `after_changes` and `after_hours`, with the teams file's writer as the fix, whatever else the entry gives. crew SHALL read no `flume`, `every` or `hours`, and SHALL name no stream for a role: a role that runs on demand runs in the stream its drive's label names.

#### Scenario: A drive that names flume
- **WHEN** the file is at version 6 and madswan's entry names `flume`, beside a `runs` or with none
- **THEN** crew refuses to load it, naming madswan and `flume`, saying the file names how each role runs under `runs`, and naming the teams file's writer, and does nothing

#### Scenario: A batch setting by its former names
- **WHEN** the file is at version 6 and wldn's `review` gives `every` 5 and `hours` 4
- **THEN** crew refuses to load it, naming wldn and `review.every`, saying the batch setting is `after_changes` and `after_hours`, and naming the teams file's writer, and does nothing

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
- **WHEN** `crew main up wldn` runs and wldn's `runs` names every role `standing`
- **THEN** `wldn-design`, `wldn-planner`, `wldn-ops` and `wldn-operator` start in the `wldn` workspace, each is greeted once it is up, and no dispatcher starts on any host

### Requirement: A role that runs as its kind gets no tab, no start and no revive
A role its drive's `runs` names `on-demand`, which runs as its kind, SHALL get no tab and no start: `crew main up` SHALL instead write its role record to match the teams file, and SHALL end a standing agent of it still running once that agent is not working, leaving one working and saying so. `crew revive` SHALL bring back no role its drive runs as its kind.

#### Scenario: Two roles run as their kinds
- **WHEN** madswan's `runs` names its reviewer and its planner `on-demand`, and `crew main up madswan` runs
- **THEN** the `madswan` workspace has no `planner` tab and no planner is started or greeted, `roles.rec` on `madswan/main` holds the planner's and the reviewer's records, and the design agent, ops and the operator start as today

#### Scenario: A standing planner from before
- **WHEN** madswan's `runs` has just come to name its planner `on-demand`, `madswan-planner` still stands idle in its tab, and `crew main up madswan` runs
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

### Requirement: Main status says a standing role is standing
`crew main status <label>` SHALL say `standing`, the word its drive's `runs` names it by, of each standing main-level role it lists, beside its agent's pane, session and status, `not up` where none runs.

#### Scenario: A standing role
- **WHEN** wldn's `runs` names its design agent `standing`, its agent is idle, and `crew main status wldn` runs
- **THEN** the design agent's line gives its pane and session and says `standing` and `idle`

### Requirement: A decision record holds only how a tool is built or behaves
The design agent SHALL write and amend decision records only of how a tool is built or how it behaves, and a unit SHALL cite as its sources only such records. A proposed record or amendment that holds only a plan matter SHALL raise no card: the design agent SHALL take it out of the kit's main and tell the planner, or main-level ops for a live system.

#### Scenario: A talk settles how a tool behaves
- **WHEN** the user settles in the design agent's pane that a bolt lands only on their send of its row on the landings card
- **THEN** the design agent records it in crew's `docs/adr/`, states the decision in the record's own words, and tells the user the record's number and commit

#### Scenario: A unit's sources
- **WHEN** the design agent or the planner names the sources of a unit whose work a freeze on fixes held back
- **THEN** its `--source` names the records of how the tool is built, and nothing of the freeze

#### Scenario: A proposed amendment that is a plan matter
- **WHEN** the design agent starts and finds a proposed amendment on a kit's main, with no card open, that only freezes fixes on main until a rebuild lands
- **THEN** it raises no card for it, takes the amendment out in a commit submitted through sluice, and tells the planner the freeze in one line

### Requirement: A plan matter goes to the planner, or to ops for a live system, with no record
An order of work, a priority, a freeze, a schedule or a trial, which bolt or unit carries something, and how a one-off move, rename or carry-over is carried out SHALL be the plan's, whoever settles it, the user included. The design agent SHALL tell it to the planner, or to main-level ops when it moves a live system, naming the signal of the user's words when they settled it, and SHALL write no record or amendment of it and raise no card for it.

#### Scenario: The user freezes fixes in the design talk
- **WHEN** the user tells the design agent in its pane that no fixes go on sluice's main until the rebuild lands
- **THEN** the design agent records the user's words as a signal, tells the planner in one line naming the signal, and writes no decision record or amendment and raises no card

#### Scenario: A carry-over on a live system
- **WHEN** the user tells the design agent how a repository's old address is carried over to its new one on the hosts
- **THEN** the design agent records the user's words as a signal, tells main-level ops in one line naming the signal, and records no decision

#### Scenario: A question that is a plan matter
- **WHEN** a question asks the design agent which bolt should carry a fix
- **THEN** the design agent tells whoever brought it that it is the planner's, and records nothing

#### Scenario: The planner carries a plan matter
- **WHEN** the design agent tells the planner of a priority the user set
- **THEN** the planner carries it in the plan, by a proposal where it changes the plan, and asks for no decision record of it
