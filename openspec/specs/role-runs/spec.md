# role-runs Specification

## Purpose
Runs a main-level role its drive names a Flume stream for as a kind crew's release carries, on demand rather than standing all day: whatever names the role is an ask on the drive's branch, the host's runner keeps one run of it while anything is pending, and the run takes everything pending at its start, acts on it, and ends its turn with a report, its work that lands a place it launches.

## Requirements

### Requirement: crew's release carries a kind for each main-level role
crew's plugin SHALL carry a Flume declaration, `plugin/flume/kinds.toml`, of five kinds, `crew-design`, `crew-planner`, `crew-reviewer`, `crew-ops` and `crew-operator`, each landing nothing, its branches prefixed by its name, and holding one stage, `turn`, whose prompt is `plugin/flume/turn.md` beside it and whose one deliverable is a report in the place's own folder, `report:{{state}}/turn.md`. The declaration SHALL name no model, no instructions and no environment.

#### Scenario: The declaration as Flume reads it
- **WHEN** `plugin/flume/kinds.toml` is read as TOML
- **THEN** it holds the five kinds, each with `lands` false, one stage named `turn` with `report:{{state}}/turn.md` as its one deliverable and `turn.md` as its prompt, and no `model`, `instructions` or `env` in any table

### Requirement: A turn's prompt starts and ends the turn
`plugin/flume/turn.md` SHALL say the run is of a role its drive's `runs` names `on-demand`, never that it runs as its kind. It SHALL have the run start with `crew role start` and end with `crew role end`, writing its report at `{{report}}`, saying the end asks the runners to confirm to Flume each end the turn took. It SHALL place `{{needs}}` in a sentence saying the run asks the user only on a card and stops short only when `crew role start` refuses. It SHALL ask for no `{{brief}}`.

#### Scenario: The prompt's parts
- **WHEN** `plugin/flume/turn.md` is read
- **THEN** every part in double braces is one Flume fills for a stage with a report deliverable and no `makes`, `{{needs}}` among them, and `{{brief}}` is not among them

#### Scenario: The end confirms
- **WHEN** `plugin/flume/turn.md` is read
- **THEN** its step that runs `crew role end` says the end asks the runners to confirm each end the turn took

#### Scenario: The role's way of running
- **WHEN** `plugin/flume/turn.md` is read
- **THEN** it says the run is of a role its drive's `runs` names `on-demand`, and says nowhere that the role runs as its kind

### Requirement: An ask is a record naming a role
An ask SHALL be a record of `asks.rec` on the drive's branch, written through crew as every write there is: its number, the role it asks, who or what asks, what kind of ask it is, the record it names where it names one, its key where it must be written once, the words it carries where it carries any, and when it was written.

#### Scenario: A malformed ask
- **WHEN** a write would add an ask with no role
- **THEN** `recfix --check` refuses it and nothing is committed

### Requirement: An ask with a key is written once
An ask whose key `asks.rec` already holds SHALL write nothing and say so, on the tip it was first tried on and on any tip a refused push is applied again to.

#### Scenario: One answer seen twice
- **WHEN** Pending You's notice of the answer on madswan's proposal 12's card, at its version 3, reaches deneb's follower twice, while madswan's planner runs as its kind
- **THEN** `asks.rec` on `madswan/main` holds one ask of the planner keyed by that card's request and version 3, and the second write says the ask is there

### Requirement: An ask is written with the act that makes it
An ask SHALL be written in the same commit as the act that makes it, where that act writes to the drive's branch, and in a commit of its own where it does not.

#### Scenario: A capture
- **WHEN** an agent captures a signal through crew in madswan, whose design agent runs as its kind
- **THEN** the capture's commit holds an ask of the design agent keyed by the signal's id

### Requirement: A tell, a notice or a send to a role that runs as its kind is an ask
A `crew tell` to a role its drive runs as its kind, by an agent or the user, and every notice crew sends it, SHALL be written as an ask of the role from the sender, `crew` for a notice, carrying the text; a `crew send` to the drive SHALL be an ask of its operator carrying whom it was sent to and the text. Nothing SHALL be typed into any pane for it.

#### Scenario: A tell to the planner
- **WHEN** madswan's planner runs as its kind, no standing agent of it is up, and madswan-design runs `crew tell madswan-planner "record 0053 is accepted"`
- **THEN** an ask of the planner from madswan-design holds those words, nothing is typed into any pane, and the command says it asked madswan-planner

#### Scenario: crew's own notice
- **WHEN** a proposal of madswan's is approved and the planner runs as its kind
- **THEN** an ask of the planner from crew says the proposal was approved, where today the planner is told

### Requirement: A card's answer, an opening and a batch are asks
A change on a card in the name of a role that runs as its kind, the user's answer among them, as Pending You's notice names it to the host's follower, SHALL be an ask of that role, keyed by the card's request and version; the follower SHALL read nothing of the card, and SHALL write nothing for a card in any other name. The user opening a role SHALL be an ask of it. A batch from `crew review` SHALL be an ask of a reviewer that runs as its kind, and a batch delivered an ask of the planner.

#### Scenario: A deploy approved from the phone
- **WHEN** swancloud's ops runs as its kind and the user approves `deploy/deneb` on the phone
- **THEN** the host's follower, told by Pending You's notice, writes one ask of ops naming the card's request, and reads nothing of the card

#### Scenario: A standing agent's card
- **WHEN** Pending You's notice names an answer on a card in wldn-planner's name, and wldn's planner stands
- **THEN** the follower writes no ask, and the card's answer wakes wldn-planner as today

### Requirement: The follower hears Pending You's notice while a role here runs as its kind
The host's follower SHALL run Pending You's notice of changes on the host's cards, `pendingyou watch`, while a drive whose main level runs on its host runs a role as its kind, and only then.

#### Scenario: A role here runs as its kind
- **WHEN** madswan's main level runs on deneb and its planner runs as its kind
- **THEN** deneb's follower runs `pendingyou watch` for as long as it holds the host's follower lock

#### Scenario: No role here runs as its kind
- **WHEN** no drive whose main level runs on deneb runs a role as its kind
- **THEN** deneb's follower runs no `pendingyou watch`

### Requirement: A role that stands is asked nothing
For a role its drive does not run as its kind, no tell, notice, send, capture, landing, card's answer, opening or batch SHALL write an ask: each SHALL do what it does today.

#### Scenario: A role still standing
- **WHEN** wldn's planner stands, and `crew tell wldn-planner "<text>"` runs
- **THEN** the text is typed into wldn-planner's pane as today, and no ask is written

### Requirement: A tell finds a standing agent of the role first
A tell to a role its drive runs as its kind SHALL be typed into a standing agent of it that is still up, as a tell is today, and written as an ask only once crew has read that none is up. When crew cannot read whether one is up, the tell SHALL refuse, naming what it could not read, and write nothing.

#### Scenario: The standing agent not yet stopped
- **WHEN** madswan's planner was named to run as its kind a minute ago, its standing agent is still up and idle, and the design agent tells it
- **THEN** the text is typed into the standing agent's pane, and no ask is written

### Requirement: A place that waits on a role is pending for the role
A place the runner's records show waiting on its caller, stopped short asking or having found work, past its send-back bound, lost, stalled, or holding its submission for a word, whose launch request names `<label>/<role>` as its recipient, SHALL be pending for that role as an unanswered ask is, keyed by its request and when that wait began, with no ask written for it. A place whose stage delivers while its kind runs through SHALL be pending for no role. The role's next run SHALL take each.

#### Scenario: A stage asks the planner
- **WHEN** a construct in a place crew launched for madswan stops short asking which bolt a finding belongs in, its request's recipient `madswan/planner`, and the runner's records show it waiting
- **THEN** the planner's next run takes it with its work, its place and its words

#### Scenario: A stage that delivers
- **WHEN** a unit's construct delivers and its code stage starts
- **THEN** nothing is pending for the planner from it

### Requirement: A role's landed work is pending for the role
A place `crew role land` launched for a role SHALL be pending for that role once the runner's records show it landed, keyed by its request, so the role's next run reads what landed.

#### Scenario: A record lands
- **WHEN** the chore madswan's design run launched for record 0053 lands on crew's main
- **THEN** the design agent's next run takes it, and records the record's status with `crew record`

### Requirement: A role record names its run
`roles.rec` on the drive's branch SHALL hold one record for each role its drive runs as its kind, naming its address, `<label>/<role>`; its run's name, `<label>-<role>`; the main level's host; the drive's first blueprints repository as the teams file names it; crew's kinds and the kind `crew-<role>`; the place's name, `<label>`; the stream, the drive's own, named by its label; the priority 0; the intent `<label>-<role>`; and the role's model and effort.

#### Scenario: The planner's record
- **WHEN** madswan runs its planner as its kind and its record is written
- **THEN** it names `madswan/planner`, `madswan-planner`, deneb, `afterthought/blueprints`, `crew-planner`, the place's name `madswan`, the stream `madswan`, the intent `madswan-planner` and Opus 5.5

### Requirement: Role records follow the teams file
crew SHALL write `roles.rec` to match the teams file at `crew main up` and in the commit of an ask whose role's record is missing or differs, and SHALL remove the record of a role the teams file no longer runs as its kind.

#### Scenario: The planner moves
- **WHEN** madswan's teams entry's `runs` names its planner `on-demand`, and `crew main up madswan` runs
- **THEN** `roles.rec` on `madswan/main` holds the planner's record

#### Scenario: An ask before main up
- **WHEN** the teams entry's `runs` names the planner `on-demand`, no record of it is on the branch, and a tell to the planner writes an ask
- **THEN** the ask's commit holds the planner's record too

#### Scenario: The planner stands again
- **WHEN** madswan's teams entry's `runs` names the planner `standing` again, and `crew main up madswan` runs
- **THEN** `roles.rec` holds no record of the planner

### Requirement: A role has at most one run, wanted while anything is pending
What is pending for a role SHALL be each of its asks and each place that waits on it that no turn ended by `crew role end` took. The role SHALL be wanted while anything is pending, and the runner on its record's host SHALL keep at most one run of it, so asks written during a run wait for the next and a burst of them is one run.

#### Scenario: A burst
- **WHEN** three asks of madswan's planner are written within a minute and no run of it stands
- **THEN** one run of the planner takes all three

#### Scenario: An ask during a run
- **WHEN** the planner's run has taken two asks, and a third is written before it ends
- **THEN** the third is still pending once the run's turn ends, and the planner is wanted again

#### Scenario: Nothing pending
- **WHEN** every ask of the planner has been taken by a turn that ended
- **THEN** the planner is not wanted

### Requirement: A run's start takes everything pending
`crew role start`, run in a role's run, SHALL take everything pending for the role and record, in one commit, the turn that took it. With nothing pending, it SHALL record no turn and say so. Run anywhere but a role's run, it SHALL refuse, naming where it runs, and write nothing.

#### Scenario: Two asks waiting
- **WHEN** the planner's run starts with an ask from the design agent and a card's answer pending
- **THEN** `crew role start` records a turn taking both

#### Scenario: Nothing waiting
- **WHEN** the planner's run starts with nothing pending
- **THEN** `crew role start` records no turn and says nothing waits, so the run ends its turn

#### Scenario: Not a run
- **WHEN** `crew role start` runs in a change's place
- **THEN** it refuses, saying it runs only in a run of a crew role, and writes nothing

### Requirement: A start takes again what a lost run took
A turn of the role still open when a run starts SHALL be recorded superseded by the new turn, which takes its asks again; a superseded turn SHALL answer nothing.

#### Scenario: A run that was lost
- **WHEN** the planner's earlier run took an ask and was lost before its end, and its run is retried
- **THEN** the new start records the earlier turn superseded and takes that ask again

### Requirement: A run's end answers what it took
`crew role end --report <path> "<what was done>"` SHALL record the run's open turn ended with those words, in one commit, and write the report at the path, naming the turn, what it took and what was done. With no open turn of the run, it SHALL write the report saying no turn was taken, record nothing on the branch, and say so, so every run delivers its stage. Run anywhere but a role's run, it SHALL refuse and write nothing.

#### Scenario: A turn ends
- **WHEN** the planner's run has acted on what it took and runs `crew role end --report <path> "proposed the fix bolt"`
- **THEN** the turn is recorded ended, the asks it took are no longer pending, and the report is written at the path

#### Scenario: No turn open
- **WHEN** a run that found nothing pending runs `crew role end --report <path> "nothing waited"`
- **THEN** the report is written at the path saying no turn was taken, the branch is unchanged, and the command says so

### Requirement: A run is named as its role
A run SHALL be named `<label>-<role>`, `<label>-ops` for main-level ops, read from the place it runs in, `crew-<role>--<label>`, the place its role record named, for a role its drive runs as its kind. Every crew command the run makes SHALL take that name and drive as a standing agent's `CREW_AGENT` and `CREW_LABEL` give them: the plan's role table, the cards' owners and the run record's entries SHALL treat the run as the role, and a command forwarded to another host SHALL carry them.

#### Scenario: The planner's run proposes
- **WHEN** the planner's run runs `crew plan propose <file>`
- **THEN** the proposal is the planner's, its card is raised in madswan-planner's name, and a direct plan write by the run is refused as the planner's is

#### Scenario: A place of another kind
- **WHEN** a crew command runs in a fix's place with no `CREW_AGENT`
- **THEN** it names no role as its caller

### Requirement: A run's brief says how a turn goes
A role's brief SHALL say the word its drive's `runs` names it by, `standing` or `on-demand`, never that it runs as its kind. An on-demand role's SHALL say its turn starts with `crew role start`, acts on what that took, and ends with `crew role end`; that it waits in its session on nothing, what it would have waited for reaching its next run as an ask; and that it asks the user only on a card in its own name. A standing role's SHALL say its work reaches it as tells and cards in its pane.

#### Scenario: Every brief filled
- **WHEN** each of the five briefs prints for a drive whose `runs` names all five `on-demand`
- **THEN** each says its drive's `runs` names it `on-demand`, holds the turn's words, says nowhere that it runs as its kind, and leaves no token unfilled

#### Scenario: Every brief of a standing role
- **WHEN** each of the five briefs prints for a drive whose `runs` names all five `standing`
- **THEN** each says its drive's `runs` names it `standing` and that its work reaches it in its pane, and none holds the turn's words

### Requirement: A role's work that lands is a place it launches
`crew role land <repo> <name> --brief-file <file>`, run in a role's run, SHALL launch through the runner a place of Flume's own chore kind in that repository, on its default branch, its brief the file's text whole, the run's address its recipient and the drive's own stream, named by its label, its stream. A repository neither the teams file nor the plan names SHALL be refused, and so SHALL a run outside a role's run. No role's run SHALL submit to sluice.

#### Scenario: The design agent's records
- **WHEN** madswan's design run writes the text of a record and its rule's amendment to a file and runs `crew role land afterthought/crew record-0053 --brief-file <file>`
- **THEN** a chore launch in `afterthought/crew` on its default branch is written for the runner, with the file's text as its brief, `madswan/design` as its recipient and `madswan` as its stream

### Requirement: The user opens a role to talk
`crew role open <role> [--label L]` SHALL write an ask from the user to open the role, and say that its run opens as the place `crew-<role>--<label>` on the main level's host. Where the runner's records on the role's host show a run of the role live, it SHALL write nothing and name that run's place. Where those records cannot be read, it SHALL refuse, naming what it could not read.

#### Scenario: No run live
- **WHEN** no run of madswan's design agent stands and the user runs `crew role open design --label madswan`
- **THEN** an open ask of the design agent from the user is written, and the command names `crew-design--madswan` on deneb

#### Scenario: A run live
- **WHEN** a run of madswan's design agent is live and the user runs `crew role open design --label madswan`
- **THEN** nothing is written, and the command names the live run's place to talk to now

### Requirement: A turn the user opened lasts their conversation
A turn that took an open ask SHALL greet the user in its pane and keep the conversation there until the user says they are done, and then end.

#### Scenario: Talking a design through
- **WHEN** the design agent's run took the user's open ask and the user talks a design through in its pane
- **THEN** the run's turn goes on until the user says they are done, and then it runs `crew role end`

### Requirement: A run's model is its definition's
A role record SHALL name the model and the effort of the role's definition after the teams file's `roles.<role>` override, the runner's launch SHALL pass the model, and the kinds file SHALL name neither.

#### Scenario: An override
- **WHEN** wldn's teams entry sets `roles.planner.model` and wldn's planner runs as its kind
- **THEN** wldn's planner's role record names that model, and madswan's names the definition's

### Requirement: Main-level ops's run lands nothing
Main-level ops's run SHALL land, submit and wait on nothing for a bolt or a fix of main: the user's send of a row on a kit's landings card is carried to the runner by crew's own act, whether or not a run of ops stands (record 0056 point 5), and each landing's end SHALL reach ops's next run only as the ask crew's read of the runner's report writes for it. Ops's brief, for a drive that runs ops as its kind, SHALL say so in its turn's words and SHALL name no `crew bolt submit`.

#### Scenario: The turn's words
- **WHEN** main-level ops's brief prints for a drive that runs ops as its kind
- **THEN** its turn's words say that a landing's end reaches ops's next run as an ask when it does not land, and the planner's and the design agent's when it does, and it names no `crew bolt submit`

#### Scenario: A send while no run of ops stands
- **WHEN** ops runs as its kind, no run of it stands, and the user sends `land/crew` with `y` ticked
- **THEN** `y`'s land is posted by crew's raise of the card, which waits on no run of ops

### Requirement: A run's start takes every end Flume holds for its role
`crew role start` SHALL take into its turn, beside the asks and the places that wait on the role, each end that a place's status in the runners' records gives as owed to the role's address `<label>/<role>`, by its delivery key.

#### Scenario: A unit's ends taken with an ask
- **WHEN** madswan's planner run starts with an ask from the design agent pending, and the runner's records carry unit `a`'s place, launched by request 12, whose status gives its construct's and its code's ends each owed to `madswan/planner` with its delivery key
- **THEN** the turn takes the ask and both ends, each recorded in the turn by request 12 and its delivery key

#### Scenario: An end owed to another role
- **WHEN** unit `a`'s status gives an end owed to `madswan/operator` and not to `madswan/planner`
- **THEN** the planner's start does not take it

### Requirement: An end a confirm names is not taken again
A start SHALL take no end that a `confirm` of the role's address in `requests.rec` already names, whatever the runner answered that confirm.

#### Scenario: An end already asked confirmed
- **WHEN** an ended turn took unit `a`'s construct's end and its confirm is in `requests.rec`, and the runner's records still carry that end owed to `madswan/planner`
- **THEN** the next start does not take it

#### Scenario: A refused confirm
- **WHEN** the runner answered that confirm `refused`, and its end is still carried owed to `madswan/planner`
- **THEN** the next start does not take it

### Requirement: An owed end makes no role wanted
An end owed to a role's address SHALL NOT make the role wanted: with no ask and no place waiting on the role, its run's start SHALL record no turn and take no end.

#### Scenario: Ends alone start no turn
- **WHEN** the planner's run starts with no ask and no place waiting on it, and unit `a`'s delivered ends are owed to `madswan/planner`
- **THEN** no turn is recorded, no end is taken, and the start says nothing waits

### Requirement: An end crew cannot read is not taken
A start SHALL take no end whose status gives no delivery key or no `owed` crew can read, and SHALL leave the ends on a host whose runner can't be read for the role's next run, as its waits are.

#### Scenario: A status with no delivery keys
- **WHEN** the runner carried unit `a`'s status from a Flume whose ends give no `delivery` and no `owed`
- **THEN** the start takes no end of it, and still takes what waits on the role

### Requirement: A run's end asks the runners to confirm each end its turn took
`crew role end` SHALL append to `requests.rec`, in the commit that ends the turn, one `confirm` for each launch whose ends the turn took, oldest first, naming the launch as its `Of`, the launch's work, the role's address as its `Recipient`, and one `Delivery` for each of those ends' keys in the order taken. A turn that took no end SHALL append none.

#### Scenario: Two places' ends
- **WHEN** the planner's turn took two ends of request 12's place and one of request 14's, and the run runs `crew role end --report <path> "acted on the stop-short"`
- **THEN** the commit that records the turn ended appends a confirm of request 12 naming `madswan/planner` and its two delivery keys, then a confirm of request 14 naming its one

#### Scenario: A turn with no ends
- **WHEN** the planner's turn took one ask and no end, and the run ends its turn
- **THEN** `requests.rec` is unchanged by the end

### Requirement: A lost run confirms nothing
A run that ends taking no turn, and a turn superseded before its end, SHALL append no confirm, so the next run takes those ends again.

#### Scenario: A lost run
- **WHEN** the planner's run took an end and was lost before its end, and its run is retried
- **THEN** no confirm names the end, and the new start takes it again

### Requirement: A turn's report counts its ends
The report `crew role end` writes SHALL say how many ends the turn took, of which launches, and that their confirmation was asked of the runners.

#### Scenario: Three ends of two places
- **WHEN** the planner's turn took two ends of request 12's place and one of request 14's, and its run ends the turn
- **THEN** the report says three ends of requests 12 and 14 were taken and their confirmation asked of the runners

### Requirement: A capture and a bolt's landing are asks
A signal captured through crew SHALL be an ask of a design agent that runs as its kind, one per signal, keyed by the signal's id. A bolt's landing, as crew's read of the runner's report records it, SHALL be an ask of a planner and of a design agent that run as their kinds, keyed by the bolt.

#### Scenario: A landing
- **WHEN** the runner reports a swancloud bolt's base place landed and crew's read records the landing, while swancloud's planner and design agent run as their kinds
- **THEN** that write holds an ask of the planner and one of the design agent, each naming the bolt

### Requirement: A landing refused or stopped is an ask of ops
A landing crew's read records refused or stopped SHALL be an ask of a main-level ops that runs as its kind, with Flume's or the runner's words, keyed by the land's request, so an outcome read twice asks once (record 0056 point 4).

#### Scenario: A landing that conflicts
- **WHEN** ops runs as its kind, the user's send of bolt `y` was carried to the runner as land request 57, and the runner reports `y`'s base place refused for a conflict with main
- **THEN** crew's read writes one ask of ops naming `bolt/y` with Flume's words, keyed by request 57, however often the outcome is read, and ops's next run takes it

#### Scenario: A land the runner refused
- **WHEN** ops runs as its kind, and the runner answers `y`'s land request 57 refused, a place on `bolt/y` still live
- **THEN** crew's read records `y`'s landing stopped and writes one ask of ops naming `bolt/y` with the runner's words, keyed by request 57

### Requirement: A run's start prints its brief's path, then what it took in order
`crew role start` SHALL write the role's brief, filled for its drive as `crew-role` fills it, to a file on the host, and print the file's path to read whole first, then each ask it took, oldest first, with who asked, what, the record it names and its words, then each place that waits on the role, with its work, its place and its words, then the ends it took, and last the role's answered cards, read in the role's own Pending You name, each with its key and the answer.

#### Scenario: What the planner's run reads
- **WHEN** the planner's start took an ask from the design agent and a card's answer
- **THEN** it prints the brief's path, then the design agent's words, then the card's ask, then the card's key and the user's answer, read in madswan-planner's name

### Requirement: A run's start prints a line for each launch whose ends it took
`crew role start` SHALL print the ends it took that Flume holds for the role, one line for each launch, with its work, its place, its request and each end's key, an expired end marked so, saying they are confirmed when the turn ends.

#### Scenario: The ends it took
- **WHEN** the planner's start took an ask and unit `a`'s construct's and code's ends of request 12, the code's expired
- **THEN** after the ask it prints one line for unit `a` naming its place and request 12, `stage/construct/1/delivered` and `stage/code/1/delivered` marked expired, and that they are confirmed when the turn ends
