## ADDED Requirements

### Requirement: A bolt on GitHub is fetched before crew bolts reads it
As main is read (plan.18), crew SHALL read a bolt on GitHub as the host last fetched it on every read of a kit and every refresh of the rail and the board, fetching nothing. `crew bolts` SHALL fetch the kit's origin first. A fetch that fails SHALL be named with git's words, never read past to the host's copy.

#### Scenario: crew bolts after a landing elsewhere
- **WHEN** a merge has landed on GitHub's `bolt/b` since the host last fetched, and `crew bolts` runs
- **THEN** it fetches the kit's origin once on the kit's host and shows the merged unit as `merged`

#### Scenario: The board does not fetch
- **WHEN** the rail's or the board's refresh reads the kit
- **THEN** no fetch is run, and the bolt is read at `origin/bolt/b` as the host last fetched it

#### Scenario: A fetch that fails
- **WHEN** `crew bolts` runs and the fetch of the kit's origin on the kit's host fails
- **THEN** the kit's stages read `unknown`, naming that GitHub could not be fetched and git's words, and nothing is read from the host's `bolt/b`

### Requirement: A bolt is created and dropped through crew
`crew bolt new` SHALL add a bolt with its repo, goal and sources; `crew bolt order` moves it; `crew bolt drop` SHALL remove it and its units, or with `--requeue` queue them. Either way the drop's own commit SHALL drop each of the bolt's launches still standing, a requeued unit's among them, as bolt-teams "A bolt's drop drops its base place last, and asks it again after a refusal" has it, and the drop SHALL ask nothing of a host. No command SHALL give a bolt to a team.

#### Scenario: The drop's host does not answer
- **WHEN** the planner drops started bolt `x`, whose unit `a`'s launch stands, while `x`'s kit's host does not answer
- **THEN** `x` and its units are gone from the plan, the drop's commit holds the drops of `a`'s and `bolt/x`'s launches, and no host is asked

#### Scenario: Requeuing a unit that has a place
- **WHEN** `crew bolt drop x "Later." --requeue` runs while unit `a` of started `x` has a launched place
- **THEN** `a` is in its repository's queue with no bolt or `After`, `x` is gone from the plan, and `requests.rec` gains a drop of `a`'s launch and then a drop of `bolt/x`'s launch, in the drop's commit, so `a` is launched afresh once a bolt it is placed in is started

#### Scenario: A give
- **WHEN** anyone runs `crew bolt give swb-1`
- **THEN** crew refuses it as no command it has, and the plan is unchanged

### Requirement: A landed bolt leaves the plan with its units
`crew bolt land` SHALL remove a landed bolt and its units from the plan, and SHALL be refused while one of its units has not landed on main. A bolt SHALL land only as bolt-teams "A bolt lands on the user's send alone, carried to the runner as a land" has it, and no plan command SHALL make, submit or delete its branch (record 0056).

#### Scenario: Landing too early
- **WHEN** `crew bolt land` runs while one of the bolt's units has not landed on main
- **THEN** it is refused, naming that unit

#### Scenario: A landed bolt's close deletes no branch
- **WHEN** the runner carries Flume's status of `b`'s base place over, landed at `9f1c2ab`, and `crew bolt land b` runs
- **THEN** `b` and its units leave the plan, no sluice, `wt` or `gh` command is run, and `bolt/b` is left to Flume's tidy and sluice

## MODIFIED Requirements

### Requirement: A bolt's work starts by crew bolt start
`crew bolt start <bolt>` SHALL mark the bolt `Path: flume` and request, in one plan write that records `bolt.start`, the launch of the bolt's base place and after it a launch of each unit and chore of it on `bolt/<bolt>`, with its `After` and priority, each in the bolt's repository and naming no host or stream, for a runner whose configuration names the repository to take, as bolt-teams "A bolt is a base place of crew's kind, launched before its pieces" gives their fields (record 0056). It SHALL start no agent, make no branch and read no host. A proposal MAY hold it; the user runs it directly; no other agent SHALL. It SHALL be refused, with the plan unchanged and nothing requested, while no runner answers for the partition, and for a bolt started already, but one whose own launch the runner answered refused, which it launches anew as bolt-teams "A start run again launches a bolt whose launch the runner refused" has it.

#### Scenario: A bolt is started
- **WHEN** the user approves a proposal holding `crew bolt start b`, a bolt of switchboard-kit with unit `a` and chore `c`, and a runner answers for wldn
- **THEN** `b` is marked `Path: flume`; `requests.rec` gains, in that one commit, the launch of `bolt/b`'s base place and then the launches of `a` and `c` on `bolt/b`, each naming switchboard-kit and no host or stream; no branch is made and no agent starts; and the run record has `bolt.start` on `bolt/b`

#### Scenario: A partition no runner answers for
- **WHEN** `crew bolt start b` runs and wldn's state repository holds no runner's branch
- **THEN** it is refused, naming that no runner answers for wldn, the plan is unchanged and nothing is requested

#### Scenario: A bolt started before bolts were base places
- **WHEN** `b` is started, `requests.rec` holds its units' launches and no launch of `bolt/b`, and `crew bolt start b` runs
- **THEN** it is refused, saying `b` is started already, and nothing is written

#### Scenario: An agent starts a bolt directly
- **WHEN** `wldn-ops` runs `crew bolt start b` outside a proposal
- **THEN** it is refused, naming the planner and the user, and the plan is unchanged

### Requirement: crew reads each kit by the name its record gives it
crew SHALL read a kit by the name each of its records gives it: a `Repo` in the plan, `requests.rec` or the run record; the kit in a fix of main's work or a card key; and the repository a source names. No reader SHALL map one kit's name to another's, through `kit.rename` entries or any list of former names. A partition's kits SHALL be the names its plan and its landings give, each once.

#### Scenario: Landings under another name
- **WHEN** madswan's plan names `timber`, and its run record holds a `bolt.land` with `Repo: tailrace` and, after it, a `kit.rename` entry of `tailrace` to `timber`
- **THEN** madswan's kits are `tailrace` and `timber`, each once, on the board too, and the agents' views keep the keys the mod reads

#### Scenario: A launch read as written
- **WHEN** request 1 launched `one-seam-turns-every-credential-into-a-principal` with `Repo: flywheel-cloud`, and the run record holds a `kit.rename` entry of `flywheel-cloud` to `boomdrive-cloud`
- **THEN** crew reads request 1 as `flywheel-cloud`'s launch, and no runner is read as having taken `boomdrive-cloud`'s work from it

#### Scenario: A fix of main read as written
- **WHEN** request 1 launched the fix of main `x` as `fix/main/tailrace/x`, its code delivered and its submission held, and the run record holds a `kit.rename` entry of `tailrace` to `timber`
- **THEN** it is shown on `tailrace`'s landings row, the user's send of that row posts a land with `Work: fix/main/tailrace/x` and `Of: 1`, and no land names `fix/main/timber/x`

#### Scenario: A source read as written
- **WHEN** a unit's source names `WilldanGroup/old-board:docs/adr/0017`, and the work's kit is `switchboard-kit`
- **THEN** a proposal resting on it reads record 0017 of `WilldanGroup/old-board`, as the source names it

## REMOVED Requirements

### Requirement: A bolt on GitHub is fetched before crew bolts and a landing read it
**Reason**: crew makes no landing submission and reads no bolt for one (record 0056 points 1 and 3). A bolt's landing is the user's send carried to the runner as a `land`, and Flume submits the bolt's branch as it stands on GitHub, so no landing of crew's fetches the kit's origin.
**Migration**: `crew bolts` still fetches the kit's origin first, and every other read reads the bolt as the host last fetched it (requirement "A bolt on GitHub is fetched before crew bolts reads it", whose scenarios are these, carried over).

### Requirement: A bolt is created, dropped and landed through crew
**Reason**: crew makes, submits and deletes no bolt branch, and runs no sluice command for one (record 0056 points 1 to 3). A bolt is a Flume base place that the runner launches at its start and lands on the user's send; Flume tidies its place and sluice ends its branch. So `crew bolt submit` lands nothing, and neither `crew bolt land` nor `crew bolt drop` asks sluice to delete the branch.
**Migration**: A bolt's creation and drop are in requirement "A bolt is created and dropped through crew", and its close in "A landed bolt leaves the plan with its units". bolt-teams holds the rest: the drop's requests and a refused drop asked again ("A bolt's drop drops its base place last, and asks it again after a refusal"), the landing and `crew bolt submit`'s refusal ("A bolt lands on the user's send alone, carried to the runner as a land"), and a bolt started before this release ("A bolt started before bolts were base places lands under the crew that started it"). A branch a drop leaves holding work main lacks stays the user's, as before.
