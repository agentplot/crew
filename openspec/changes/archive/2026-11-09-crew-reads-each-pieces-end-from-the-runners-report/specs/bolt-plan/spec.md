## MODIFIED Requirements

### Requirement: A launched place's stage is where Flume's status has it
Once launched, a unit, chore or fix SHALL read queued while Flume waits for room; construct, code with its ticked tasks of all, or verify while a stage runs; needing an answer with the agent's question when it stopped short asking; its stage, sent back, with sluice's words when a submission failed or conflicted; submitted with sluice's number; waiting on its caller, with Flume's words and the stage it waits to retry or its submission, whenever Flume's status says it waits on its caller for a retry, past its kind's bound among them, whatever stage it last delivered; stalled once Flume's status says it is stalled; merged once it has landed on its bolt and landed once its bolt has; or dropped. A place Flume has tidied SHALL read as the record Flume holds of it for the runner, which the runner carries as its status until its report holds it: merged or landed at the commit it landed at, or dropped. Where the runner carries no such record, the place SHALL read as the status the runner last carried. Nothing else SHALL be read for a place's end.

#### Scenario: A unit in code
- **WHEN** deneb's runner record for `a`'s launch carries Flume's status of its place in code with three of seven tasks ticked
- **THEN** `crew bolts` shows `a` at `code 3/7`

#### Scenario: A construct that asked
- **WHEN** the runner's record shows `a`'s construct stopped short with "Which partition's rail?"
- **THEN** `crew bolts` shows `a` as needing an answer, with the question

#### Scenario: A stop-short whose agent is kept open
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place, its code ended short needing an answer, its agent kept open for it until `open_until`, its end keyed `stage/code/1/ended-short`
- **THEN** `a` reads needing an answer at code, with the agent's words, and `crew bolts` shows it so

#### Scenario: A place past its bound
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place after its fourth verify delivered and its submission conflicted, the place having gone back as often as its kind allows, so Flume says it waits on its caller to retry code past its bound
- **THEN** `a` reads waiting on its caller at code with Flume's words, never at verify, and `crew bolts`, the board's ledger and the planner's band show it so

#### Scenario: A submission that waits on its retry
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place, its last stage delivered and its submission refused by the merge queue, so Flume says it waits on its caller to retry its submission
- **THEN** `a` reads waiting on its caller at its submission with Flume's words, and `crew bolts` shows it so

#### Scenario: Sent back by sluice
- **WHEN** the runner's record shows `b`'s place back in code after sluice found its submission in conflict on `plugin/lib/plan.py`
- **THEN** `crew bolts` shows `b` in code, sent back, with sluice's words

#### Scenario: Landed on the bolt
- **WHEN** the runner's record shows `a`'s place landed on `bolt/x`, and `x` has not landed
- **THEN** `crew bolts` shows `a` merged

#### Scenario: A landing held for the runner
- **WHEN** Flume landed `a`'s place on `bolt/x` and tidied it, holding its record for the runner, and deneb's runner carries that record as `a`'s status, Flume 0.20.0's tidied phase, its work over and landed at `d185a87`, pending for `boomdrive`
- **THEN** `a` reads merged at `d185a87`, and landed once main holds its change

#### Scenario: A drop held for the runner
- **WHEN** `a`'s place was dropped and Flume tidied it, holding its record for the runner, and deneb's runner carries that record as `a`'s status, its work over and dropped
- **THEN** `a` reads dropped

#### Scenario: A place tidied before the runner carried its end
- **WHEN** the runner last carried `b`'s place at submitted, Flume tidied it holding no record for the runner, and `bolt/x` holds a landing commit naming `change/b` in its `Sluice-From`
- **THEN** `b` reads submitted, as the runner last carried it, and no landing commit is read for it

### Requirement: A unit's stage is read from the runner, or from the plan before its bolt starts
crew SHALL read each unit's and chore's stage from the plan and the runner's records alone, never from a place in the kit or a landing commit on its bolt or on main: `queued` while it has no bolt; for a bolt not started, `ready`, or `waiting` while it names `After` work, which builds only once the bolt starts; for a started bolt, as "A started bolt's work reads its stage from the runner's records" and "A launched place's stage is where Flume's status has it" give it, `landed` once main holds its change, open or archived, or a chore's trailer; and `unknown`, naming why, where crew cannot read what it rests on. Nothing SHALL be kept by hand to say how far work has got.

#### Scenario: Queued work
- **WHEN** a unit has no bolt
- **THEN** its stage is `queued`

#### Scenario: A bolt not started
- **WHEN** bolt `y` is planned and not started, unit `a` names no `After` and `b` has `After: a`
- **THEN** `a` reads `ready` and `b` `waiting`, and nothing of a runner or a place in the kit is read for them

#### Scenario: Nothing kept by hand
- **WHEN** `x` is started and deneb's runner reports `a`'s place in code with 6 of 26 tasks ticked
- **THEN** `crew bolts` shows `a` at `code 6/26`, and no file was edited to say so

#### Scenario: A worktree of crew's from before
- **WHEN** a `unit/a` worktree from before teams left stands under the kit's `places/` with every task ticked, and `x` is started
- **THEN** `a`'s stage is the runner's, and nothing of that worktree is read for it

#### Scenario: A launch refused for a change the bolt holds
- **WHEN** the runner refused this partition's launch of `a` because the base `bolt/x` already holds a change named `a`, and `bolt/x` holds a landing commit naming `change/a`
- **THEN** `a` reads refused, in the runner's words, and nothing of `bolt/x`'s landing commits is read for it

## REMOVED Requirements

### Requirement: A unit whose work its bolt's branch holds is built
**Reason**: Record 0062's stopgap, the reading of a landing commit's `Sluice-From` on the bolt's first-parent line, goes now that the runner carries each place's end before Flume tidies it (agentplot/boomdrive `the-runner-carries-each-places-end`, Boomdrive record 0030). crew reads a piece's end from the runner's report alone (record 0056 point 4; `roles.5`, `roles.9`).
**Migration**: A unit or chore reads merged once the runner carries its place landed on the bolt, the record Flume holds for the runner after its tidy among them, and landed once main holds it ("A launched place's stage is where Flume's status has it"). A launch the runner refused because the bolt already holds the change reads refused, in the runner's words ("A unit's stage is read from the runner, or from the plan before its bolt starts").

### Requirement: A fix whose place's landing its bolt's branch holds is merged
**Reason**: Record 0062's stopgap, `a-bolts-landed-fix-reads-merged`, goes with the others: the runner carries the fix's place's end before Flume tidies it.
**Migration**: A fix reads merged once the runner reports its place landed on its bolt ("A fix the runner reports merged holds nothing"). A fix launched again under a dropped launch's name reads its own place's stage, since no landing is matched to it by name.

### Requirement: A bolt's landing is read from its kit's main
**Reason**: Record 0062's stopgap, `a-bolts-landing-on-main-reads-landed` (its Decision 2), read sluice's landing commits on main. crew reads nothing the runner's report does not carry (record 0056 point 4).
**Migration**: A landed bolt's pieces read landed from the runner's report and main's tree, and the bolt closes on them (bolt-teams "A landed bolt closes on its pieces' ends as the runner reports them").

### Requirement: A landed bolt's pieces are read from its landing
**Reason**: Record 0062's stopgap, Decision 3 of `a-bolts-landing-on-main-reads-landed`, read each piece from the landing commits on the bolt's landing line on main.
**Migration**: Each piece reads its stage from the runner's report, landed once main holds it, its bolt's branch standing or not ("A launched place's stage is where Flume's status has it").

### Requirement: A fix read merged from its bolt's landing holds nothing
**Reason**: It read a fix merged from its bolt's landing commits, record 0062's stopgap, which goes.
**Migration**: A fix is read from the runner's report as any piece is, and one the runner reports merged holds nothing ("A fix the runner reports merged holds nothing").

## ADDED Requirements

### Requirement: A fix the runner reports merged holds nothing
`crew bolts`, the board, the bolt's landing and `crew fix <bolt> <name> --drop` SHALL read a fix on a started bolt from the runner's records alike. A fix the runner reports merged, a record Flume holds for the runner among them, SHALL hold its bolt's landing no longer, and its drop SHALL be refused as any merged fix's is. A fix at any other stage SHALL read that stage, whatever its bolt's landing commits name.

#### Scenario: A landed fix holds its bolt's landing no longer
- **WHEN** every unit of `x` has merged, the runner reports `x`'s head as `a`'s landing, and it carries the record Flume holds for it of fix `x--tidy`'s place, tidied and landed on `bolt/x`
- **THEN** `fix/x/tidy` reads merged, no fix is in flight on `x`, and `x` reads proven

#### Scenario: A landed fix is not dropped
- **WHEN** the runner carries `fix/x/tidy`'s place landed on `bolt/x`, and the planner runs `crew fix x tidy --drop`
- **THEN** it is refused, saying the fix has merged into `bolt/x`, and nothing is appended to `requests.rec`

#### Scenario: A fix the runner last carried at submitted
- **WHEN** the runner last carried `fix/x/tidy`'s place at submitted, and `bolt/x` holds a landing commit naming `fix/x--tidy` in its `Sluice-From`
- **THEN** `fix/x/tidy` reads submitted and is in flight on `x`, holding its landing, and `crew fix x tidy --drop` appends its drop
