## ADDED Requirements

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

### Requirement: Main-level ops answers a landing that does not land
What follows a landing that does not land SHALL be main-level ops's, read from the runner's report alone (record 0056 decision 5): for a check that failed, ops SHALL start a fix on the bolt with Flume's words; for a conflict, whose take-main fix crew's read launches, ops SHALL start nothing; and a landing the runner or Flume stopped, nothing of the bolt's, ops SHALL record as a signal and tell the planner of in one line, the bolt landing again only on the user's next send.

#### Scenario: What follows a landing that does not land
- **WHEN** main-level ops's brief is read
- **THEN** it says a check that failed is a fix on the bolt ops starts with `crew fix <bolt> <name> "<Flume's words>"`, that a conflict's take-main fix is crew's to launch and ops starts nothing for it, and that a stop is recorded as a signal and told to the planner, the bolt landing again on the user's next send

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

## MODIFIED Requirements

### Requirement: A fix of main lands on the user's send
Once a fix of main's code has delivered and its submission waits held, the kit's landings row SHALL carry it, and the user's send of that row SHALL be the one word that lands it: crew SHALL carry the send to the runner as a land of the fix's launch, by its own act and in ops's name, with no agent running anything, and the runner submits the fix's place (record 0056 decision 6). `crew main fix <kit> <name> --send`, with or without `--excerpt`, SHALL refuse at once, before it reads anything, saying a fix of main lands on the user's send of its row on the kit's landings card, which crew carries to the runner, and SHALL append nothing. Nothing else SHALL submit it.

#### Scenario: The user's send
- **WHEN** the runner's record shows `main--a-test-reads-its-fixture`'s code delivered and its submission held, and the user sends crew's landings card with it ticked
- **THEN** crew's next raise of the card appends one land of the fix's launch to `requests.rec`, ahead of the lands of the bolts the same send ticked, and a raise after it appends none

#### Scenario: Sent by hand
- **WHEN** ops runs `crew main fix crew a-test-reads-its-fixture --send`, or the same with `--excerpt "<the user's words>"`
- **THEN** it is refused before anything is read, naming the send of the fix's row on crew's landings card as the way, and `requests.rec` is as it was

## REMOVED Requirements

### Requirement: Main-level ops lands bolts by one procedure
**Reason**: Main-level ops submits nothing (record 0056 points 1 and 5): crew carries the user's send to the runner itself, so ops runs no `crew bolt submit`, a note on the send moves no landing of ops's, and a stopped landing lands again only on a new send (design Decisions 4 and 7).
**Migration**: The procedure is requirement "A bolt lands on the user's send, carried in ops's name"; what ops does not run, requirement "Main-level ops runs no landing"; what ops does when a landing does not land, requirement "Main-level ops answers a landing that does not land"; and the deploy and the fix after a landing, requirement "A landing deploys nothing".

### Requirement: A landing said in ops's pane is checked as the user's words before it is submitted
**Reason**: The user's words in ops's pane are no word to land (record 0056 decision 5): main-level ops asks for nothing at a landing, and `crew bolt submit` lands nothing with any arguments, `--excerpt` among them (design Decisions 1 and 4).
**Migration**: The user lands a bolt by their send of its row on the kit's landings card (requirement "A bolt lands on the user's send, carried in ops's name"), and ops answers their words in its pane by pointing them to the card (requirement "The user's words in ops's pane are no word to land"). crew's reading of the user's words in ops's transcript stays for `crew bolt leave` (requirement "A stop said in ops's pane is read as the user's words"). A `bolt.submit` entry an older crew wrote naming a transcript record is read as it was.

### Requirement: A landing said in ops's pane closes its card naming the user's words
**Reason**: No landing is made on the user's words in ops's pane (record 0056 decision 5), so no landings card closes naming them, and no close reads words kept on a host.
**Migration**: A landed bolt's kit's landings card closes as any landings card the user answered, naming the commit the runner reports and the fleet's timer, as the rail-cards spec has it.

### Requirement: Ops lands a bolt on a send that still stands
**Reason**: crew posts the land itself on a send that still stands, once the bolt reads proven at its new head (design Decision 4), so main-level ops lands nothing on it, and `crew card read land/<kit>` prints no command for ops to run (design Decision 10).
**Migration**: A standing send is carried to the runner by crew's own raise of the kit's landings card. What `crew card read land/<kit>` prints of it, the lands posted with their requests and a bolt whose head crew cannot read, is the rail-cards spec's.

### Requirement: A landing stopped in ops's pane is recorded as the user's words
**Reason**: Its scenario of a stop ended by a landing on the user's words in ops's pane goes with that landing (record 0056 decision 5), and the cases it refused in were named by reference to a landing said in the pane, a requirement this change removes.
**Migration**: `crew bolt leave` reads and records the stop as before, by requirements "A stop said in ops's pane is read as the user's words", "A stop crew cannot read as the user's words is refused" and "A stop is recorded holding none of the user's words"; a stop ends when the user ticks the bolt on a send, or when its head moves.
