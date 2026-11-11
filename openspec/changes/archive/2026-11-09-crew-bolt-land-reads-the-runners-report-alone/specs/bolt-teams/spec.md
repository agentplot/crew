## MODIFIED Requirements

### Requirement: A landing records the commit main holds
The act that reads a started bolt's base place landed ("A landing is recorded by the first act that reads it in the runner's report") SHALL close the bolt in main-level ops's name by one `bolt.land` entry. The entry SHALL name the kit the bolt landed on and, as its `Head`, the commit Flume's status names the base place landed at, as the runner carries it, the record Flume holds for the runner after it tidies the base place among them. Its `Age` and `Split` SHALL be those the bolt's time gives from the run record, none read from sluice (`plan.20`). The close SHALL take the bolt and its work out of the plan and close its kit's landings card naming that commit and the fleet's timer. It SHALL delete no branch and remove no worktree. `crew bolt land` on a started bolt SHALL close it the same way. It SHALL be refused, recording nothing, while its base place does not read landed with its commit, naming its landing as the runner's report has it. No landing commit on its kit's main SHALL be read for it.

#### Scenario: The landing's commit
- **WHEN** the runner carries the base place of switchboard-kit's bolt `y` over, landed at `9c1e4b7`, and the raise of switchboard-kit's landings card reads `y`
- **THEN** the run record holds a `bolt.land` on `bolt/y` in ops's name naming switchboard-kit and `9c1e4b7` as its head, `y` and its work are gone from the plan, and no branch is deleted and no worktree removed

#### Scenario: Its time from the run record
- **WHEN** `y`'s close is recorded
- **THEN** its `Age` and `Split` are those its row shows from the run record, and no sluice history is read

#### Scenario: Closed by hand before it landed
- **WHEN** `crew bolt land y` runs while the runner carries `y`'s base place with its submission `#412` under test
- **THEN** it is refused, saying `y`'s landing is `#412` under test, and nothing is recorded

#### Scenario: A base place held for the runner
- **WHEN** Flume landed `z`'s base place on main at `4acecf0` and tidied it, holding its record for the runner, which carries it as the base place's status, GitHub has deleted `bolt/z`, and ops runs `crew bolt land z`
- **THEN** `z` and its chore leave the plan, and the landing's entry names the kit and `4acecf0` in ops's name

#### Scenario: A landing main holds that the runner does not report
- **WHEN** `z`'s kit's main holds a landing naming `bolt/z` in its `Sluice-From`, the runner carries no status of `z`'s base place, and ops runs `crew bolt land z`
- **THEN** it is refused, naming `z`'s landing as the runner's report has it, no kit is read, and nothing is recorded

### Requirement: A bolt started before bolts were base places lands under the crew that started it
crew SHALL read a started bolt with no launch of `bolt/<bolt>` in `requests.rec` as one whose branch sluice made before bolts were base places: `crew bolts` SHALL say it lands under the crew that started it, and its row SHALL have no box (rail-cards). No land SHALL be posted for it, and `crew bolt land` SHALL refuse it in those words, recording nothing and reading no landing commit on its kit's main. A drop of it SHALL drop its pieces' launches still standing and ask nothing for its branch, which SHALL stay, named in the drop's words, the user's.

#### Scenario: crew bolts says so
- **WHEN** started bolt `y` has its units' launches in `requests.rec` and no launch of `bolt/y`
- **THEN** `crew bolts` says `y` was started before bolts were base places and lands under the crew that started it

#### Scenario: No land is posted
- **WHEN** the raise of `y`'s kit's landings card reads a send that ticked `y`
- **THEN** no land is posted for `y`

#### Scenario: crew bolt land refuses it
- **WHEN** ops runs `crew bolt land y`
- **THEN** it is refused, saying `y` was started before bolts were base places and lands under the crew that started it, no kit is read, and nothing is recorded

#### Scenario: A drop of it
- **WHEN** the user approves dropping `y`, its unit `a`'s launch standing
- **THEN** the drop's commit appends a drop of `a`'s launch and no request for `bolt/y`, and the drop says `bolt/y` stays, the user's to keep or delete

### Requirement: A bolt's proof is its verification
A bolt SHALL be proven by its verification alone: its head is the landing of its work, as the runner reports it (merge-gate "A bolt's verification is its work's landing at its head, as the runner reports it alone"). Nobody SHALL deploy the bolt or work a list from its changes to prove it. Ops SHALL prove and deploy nothing. crew SHALL offer the bolt for landing, as its row on its kit's landings card, once every unit and chore of it has merged and its verification is green.

#### Scenario: Ready to land
- **WHEN** every unit of a bolt has merged and `crew bolts` shows its verification green
- **THEN** the bolt is a row of its kit's landings card, in main-level ops's name, and no one is asked to prove it

#### Scenario: Not yet green
- **WHEN** every unit of a bolt has merged and its head is no landing of its work that the runner reports
- **THEN** the bolt is not offered for landing, and `crew bolts` says what its verification is
