## ADDED Requirements

### Requirement: A bolt whose work is on its kit's main reads landed
Where the runner's report does not read a started bolt landed, crew SHALL read it landed once its kit's main, as GitHub holds it in crew's own cache, holds the commit each of its units and chores landed at on the bolt, as the runner reports it, and the newest head a landing of it carried, where the run record holds one. A bolt with no base place SHALL be read so too. crew SHALL read no trailer, no record of sluice's or Flume's and no host's checkout for it.

#### Scenario: A bolt an older crew landed
- **WHEN** started bolt `y` has no launch of `bolt/y`, its unit `a`'s place landed on `bolt/y` at `896e642` as the runner reports it, the run record holds `y`'s landing queued as `#154` at `62d2f06` and then stopped at `62d2f06`, and GitHub's main holds `6cfc4ae`, whose second parent is `62d2f06`
- **THEN** `y`'s landing reads landed at `6cfc4ae`, and `crew bolts` says `y` landed at `6cfc4ae`, naming neither the stop nor the crew that started it

#### Scenario: A landing the runner reports stopped
- **WHEN** the runner answers `y`'s land refused, so its landing reads stopped at `62d2f06`, and GitHub's main holds `62d2f06` and the commit `y`'s unit `a` landed at on `bolt/y`
- **THEN** `y`'s landing reads landed at main's commit that landed `62d2f06`

#### Scenario: A host's checkout of main is gone
- **WHEN** the folder named for `y`'s kit on deneb is gone, deneb's copy of main lags GitHub's, and GitHub's main holds `y`'s work
- **THEN** `y`'s landing reads landed, and no host is read for it

#### Scenario: A unit main does not hold
- **WHEN** GitHub's main holds the head `y`'s landing carried, and `y`'s unit `b`'s place landed on `bolt/y` at a commit main does not hold
- **THEN** `y`'s landing reads as the runner's report gives it

#### Scenario: A unit not merged
- **WHEN** `y`'s unit `b` reads code
- **THEN** `y`'s landing reads as the runner's report gives it, and nothing of main is read for it

#### Scenario: A newer landing main does not hold
- **WHEN** `y`'s landing was stopped at `62d2f06`, a land of `y` asked at `a1b2c3d` stands since, and GitHub's main holds `62d2f06` and not `a1b2c3d`
- **THEN** `y`'s landing reads as the runner's report gives it

#### Scenario: A bolt with no work of its own
- **WHEN** started bolt `y` holds no unit or chore that has merged, and the run record holds no landing of it
- **THEN** `y`'s landing reads as the runner's report gives it, though main holds `bolt/y`'s head

#### Scenario: Main can't be read
- **WHEN** crew can't fetch `y`'s kit's main from GitHub, or git can't tell whether main holds a commit `y`'s reading asks
- **THEN** `y`'s landing reads as the runner's report gives it, and nothing is taken as landed

### Requirement: A bolt read landed on main is recorded and closed by the first act that reads it
The first act on any host to read a bolt landed on its kit's main SHALL record it, as it records a landing the runner reports: its kit's card's raise, the follower's sweep, a kit's read or `crew bolt land`, whether or not a land of it was posted (`plan.21`). It SHALL write one `bolt.submit` landed, naming the head and the landing still pending where there is one, and close the bolt by one `bolt.land` in main-level ops's name.

#### Scenario: Nobody runs anything
- **WHEN** `y`, with no launch of `bolt/y`, reads landed on main at `6cfc4ae`, and no agent of the drive runs a command
- **THEN** the follower's next sweep records `y`'s `bolt.submit` landed with `Submission: 154` and `Head: 62d2f06`, and its `bolt.land` at `6cfc4ae` in ops's name, and `y` and its unit leave the plan

#### Scenario: The stop and the queued landing end
- **WHEN** that `bolt.submit` is recorded
- **THEN** the run record reads `y`'s landing neither queued as `#154` nor stopped at `62d2f06`

#### Scenario: Two reads at once
- **WHEN** two reads find `y` landed on main, and the second's write is applied to a tip that holds the first's
- **THEN** the run record holds one landed `bolt.submit` and one `bolt.land` for `y`

#### Scenario: Its host can't be told
- **WHEN** `y` reads landed on main and crew can't tell which host's runner keeps `y`'s kit
- **THEN** the sweep on the drive's main-level host records `y` landed and closes it

### Requirement: A bolt read landed on main is offered no more
A bolt whose landing reads landed, from the runner's report or from its kit's main, SHALL be no row of its kit's landings card, SHALL have no line under *land* on the rail, and no land of it SHALL be posted on any send. Its head line SHALL say it landed at its commit, and nothing of a stop or of the crew that started it.

#### Scenario: Not on its kit's landings card
- **WHEN** the user's last send of `land/boomdrive` ticked `y`, its landing stopped, and `y` now reads landed on main
- **THEN** the next raise of `land/boomdrive` lists no row for `y`, and no land of `y` is posted

#### Scenario: Not under land on the rail
- **WHEN** `y` reads landed on main and its close has not been recorded yet
- **THEN** the rail's row under *land* for boomdrive holds no line for `y`

## MODIFIED Requirements

### Requirement: A landing's outcome is read from the runner's report
crew SHALL read a started bolt's landing from its launch, the lands of it in `requests.rec`, and Flume's status of its base place as the runner that took the launch carries it, as one outcome: unlaunched, none, asked, submitted, landed, refused for a failed check or a conflict, stopped, dropped, or unknown, naming why (`runner.landing_of`, `code.7`). Each fact SHALL be guarded (`read.2`). An outcome not landed is read against main ("A bolt whose work is on its kit's main reads landed").

#### Scenario: Unlaunched
- **WHEN** the runner has not answered `z`'s launch, or answered it held or refused
- **THEN** `z`'s landing reads unlaunched, in the runner's words where it gave any

#### Scenario: None
- **WHEN** `z`'s base place is launched and no land of it stands
- **THEN** `z`'s landing reads none

#### Scenario: Asked
- **WHEN** a land of `z`'s launch is posted as request 57 and the runner has not answered it
- **THEN** `z`'s landing reads asked, with request 57

#### Scenario: Under test
- **WHEN** the runner carries Flume 0.17.0's status of `z`'s base place with its submission `#412` under test
- **THEN** `z`'s landing reads submitted, with entry 412 under test

#### Scenario: Landed
- **WHEN** the runner carries `z`'s base place over, landed at `5d1a9e0`
- **THEN** `z`'s landing reads landed, with `5d1a9e0`

#### Scenario: A failed check
- **WHEN** the runner carries `z`'s base place waiting on its caller with the verdict failed and Flume's words
- **THEN** `z`'s landing reads refused, the bolt's, in those words

#### Scenario: A conflict
- **WHEN** the runner carries `z`'s base place with the verdict conflict on `README.md` against main at `4d3d9be`
- **THEN** `z`'s landing reads refused for a conflict, naming `README.md` and `4d3d9be`

#### Scenario: Withdrawn
- **WHEN** the runner carries `z`'s base place waiting on its caller with the verdict withdrawn
- **THEN** `z`'s landing reads stopped, in Flume's words

#### Scenario: A land the runner refused
- **WHEN** the runner answers `z`'s land refused, Flume's words saying a place on `bolt/z` is live
- **THEN** `z`'s landing reads stopped, in those words

#### Scenario: Dropped
- **WHEN** the runner carries `z`'s base place over, dropped
- **THEN** `z`'s landing reads dropped

#### Scenario: Flume could not read the submission
- **WHEN** the runner carries `z`'s base place with Flume's words that it could not read the submission
- **THEN** `z`'s landing reads unknown, in those words, and is read as no other outcome

#### Scenario: A runner that can't be read
- **WHEN** the branch of the runner that took `z`'s launch can't be read
- **THEN** `z`'s landing reads unknown, naming that runner, and is read as no other outcome

### Requirement: A landing's entry names its kit, its head and its time
A landed bolt's `bolt.land` entry SHALL name the kit the bolt landed on and, as its `Head`, the commit Flume's status names the base place landed at, as the runner carries it, the record Flume holds for the runner after it tidies the base place among them; or, for a bolt read landed on its kit's main, main's commit that landed it. Its `Age` and `Split` SHALL be those the bolt's time gives from the run record, none read from sluice (`plan.20`).

#### Scenario: Its time from the run record
- **WHEN** `y`'s close is recorded
- **THEN** its `Age` and `Split` are those its row shows from the run record, and no sluice history is read

#### Scenario: Its head read on main
- **WHEN** `y` reads landed on main, the oldest commit of main's first-parent line holding the head its landing carried being `6cfc4ae`, and three commits have landed on main after it
- **THEN** `y`'s `bolt.land` names `6cfc4ae` as its `Head`

### Requirement: crew bolt land closes a started bolt only once its base place reads landed
`crew bolt land` on a started bolt SHALL close it the same way as the act that reads it landed. It SHALL be refused, recording nothing, while its base place does not read landed with its commit and its kit's main does not hold its work ("A bolt whose work is on its kit's main reads landed"), naming its landing as the runner's report has it. No landing commit's trailer SHALL be read for it.

#### Scenario: Closed by hand before it landed
- **WHEN** `crew bolt land y` runs while the runner carries `y`'s base place with its submission `#412` under test, and `y`'s kit's main does not hold `y`'s head
- **THEN** it is refused, saying `y`'s landing is `#412` under test, and nothing is recorded

#### Scenario: A base place held for the runner
- **WHEN** Flume landed `z`'s base place on main at `4acecf0` and tidied it, holding its record for the runner, which carries it as the base place's status, GitHub has deleted `bolt/z`, and ops runs `crew bolt land z`
- **THEN** `z` and its chore leave the plan, and the landing's entry names the kit and `4acecf0` in ops's name

#### Scenario: A landing main holds that the runner does not report
- **WHEN** `z`'s kit's main holds a commit whose `Sluice-From` names `bolt/z`, but neither `z`'s head nor the commit `z`'s chore landed at on `bolt/z`, the runner carries no status of `z`'s base place, and ops runs `crew bolt land z`
- **THEN** it is refused, naming `z`'s landing as the runner's report has it, no host is read, and nothing is recorded

#### Scenario: A landing main holds
- **WHEN** the runner reports `z`'s landing stopped at `9c1e4b7`, GitHub's main holds `9c1e4b7` and the commit `z`'s chore landed at on `bolt/z`, and ops runs `crew bolt land z`
- **THEN** `z` and its chore leave the plan, and the landing's entry names the kit and main's commit that landed `9c1e4b7` in ops's name

### Requirement: A bolt with no launch of its own lands under the crew that started it
crew SHALL read a started bolt with no launch of `bolt/<bolt>` in `requests.rec` as one whose branch sluice made before bolts were base places: until its kit's main holds its work, `crew bolts` SHALL say it lands under the crew that started it, its row SHALL have no box (rail-cards), and `crew bolt land` SHALL refuse it in those words, recording nothing. No land SHALL be posted for it. Once main holds its work, it SHALL read landed and close as any bolt.

#### Scenario: crew bolts says so
- **WHEN** started bolt `y` has its units' launches in `requests.rec` and no launch of `bolt/y`, and its kit's main does not hold its work
- **THEN** `crew bolts` says `y` was started before bolts were base places and lands under the crew that started it

#### Scenario: No land is posted
- **WHEN** the raise of `y`'s kit's landings card reads a send that ticked `y`
- **THEN** no land is posted for `y`

#### Scenario: crew bolt land refuses it
- **WHEN** ops runs `crew bolt land y` while `y`'s kit's main does not hold its work
- **THEN** it is refused, saying `y` was started before bolts were base places and lands under the crew that started it and that its kit's main does not hold its work, no host is read, and nothing is recorded

#### Scenario: crew bolt land closes it once main holds its work
- **WHEN** ops runs `crew bolt land y` once GitHub's main holds `y`'s work, landed by an older crew at `6cfc4ae`
- **THEN** `y` and its units leave the plan, and the landing's entry names the kit and `6cfc4ae` in ops's name
