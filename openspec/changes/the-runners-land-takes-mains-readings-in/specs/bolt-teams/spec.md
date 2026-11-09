## MODIFIED Requirements

### Requirement: A landing records the commit main holds
The act that reads a started bolt's base place landed ("A landing is recorded by the first act that reads it in the runner's report") SHALL close the bolt in main-level ops's name by one `bolt.land` entry. The entry SHALL name the kit the bolt landed on and, as its `Head`, the commit Flume's status names the base place landed at, as the runner carries it. Its `Age` and `Split` SHALL be those the bolt's time gives from the run record, none read from sluice (`plan.20`). The close SHALL take the bolt and its work out of the plan and close its kit's landings card naming that commit and the fleet's timer. It SHALL delete no branch and remove no worktree. `crew bolt land` on a started bolt SHALL close it the same way, or at the landing its kit's main holds ("A bolt whose landing main holds closes whatever the runner carried of its places"). It SHALL be refused, recording nothing, while its base place does not read landed with its commit and its kit's main holds no landing of it, naming its landing as the runner's report has it.

#### Scenario: The landing's commit
- **WHEN** the runner carries the base place of switchboard-kit's bolt `y` over, landed at `9c1e4b7`, and the raise of switchboard-kit's landings card reads `y`
- **THEN** the run record holds a `bolt.land` on `bolt/y` in ops's name naming switchboard-kit and `9c1e4b7` as its head, `y` and its work are gone from the plan, and no branch is deleted and no worktree removed

#### Scenario: Its time from the run record
- **WHEN** `y`'s close is recorded
- **THEN** its `Age` and `Split` are those its row shows from the run record, and no sluice history is read

#### Scenario: Closed by hand before it landed
- **WHEN** `crew bolt land y` runs while the runner carries `y`'s base place with its submission `#412` under test, and switchboard-kit's main holds no landing of `y`
- **THEN** it is refused, saying `y`'s landing is `#412` under test, and nothing is recorded

### Requirement: A bolt whose landing main holds closes whatever the runner carried of its places
`crew bolt land`, and the landing's read that closes a landed bolt, SHALL close a started bolt whose landing its kit's main holds once each of its units and chores reads landed through that landing ("A landed bolt's pieces are read from its landing"), whether or not its branch still stands and whatever the runner last carried of its places. This SHALL hold for a bolt whose base place the runner does not read landed, and for a bolt started before bolts were base places, which the crew that started it landed. The close SHALL name the landing's commit as its `Head` and record no outcome of the runner's. A bolt with a piece that does not read landed SHALL be refused, naming that piece and its stage, and nothing is removed.

#### Scenario: A landed bolt whose branch and places are gone
- **WHEN** `x` landed on main through `crew bolt submit`, GitHub has deleted `bolt/x`, deneb's runner carries no place of `x`'s work, its `repositories.rec` names the kit, and ops runs `crew bolt land x`
- **THEN** `x` and its units leave the plan, and the landing's entry names the kit and the commit its main holds

#### Scenario: A base place the runner no longer carries
- **WHEN** Flume landed `z`'s base place on main at `4acecf0`, its landing naming `bolt/z`, GitHub has deleted `bolt/z`, the runner carries no place of `z`'s work, so its report reads `z`'s land asked, and ops runs `crew bolt land z`
- **THEN** `z` and its chore leave the plan, the landing's entry names the kit and `4acecf0` in ops's name, and no `bolt.submit` outcome is recorded

#### Scenario: A piece its landing does not hold
- **WHEN** main holds `x`'s landing, and `x`'s unit `b` is named by no landing on that landing's line, and the runner reads `b` at code
- **THEN** `crew bolt land x` is refused, naming `b` and that it has not landed, and the plan is unchanged
