## RENAMED Requirements

- FROM: `### Requirement: A partition is never renamed`
- TO: `### Requirement: A drive is never renamed`


## MODIFIED Requirements

### Requirement: A drive's state is one branch of its state repository
Each drive SHALL name one state repository in the teams file, as `state`. The drive SHALL keep its state as files on the branch `<label>/main` of that repository. The branch SHALL hold no other drive's files and SHALL share no history with another drive's branch.

#### Scenario: Willdan's drive
- **WHEN** the `wldn` drive names `WilldanGroup/crew-state` as its state repository
- **THEN** its plan, moves and run record are files on the branch `wldn/main` of that repository

#### Scenario: Two drives of one organisation
- **WHEN** `madswan` and `swancloud` both name `afterthought/crew-state`
- **THEN** each has its own branch, `madswan/main` and `swancloud/main`, and neither branch holds a commit of the other's

### Requirement: A drive's branch is created, and adopts what it had
`crew state init <label>` SHALL create `<label>/main` in the drive's state repository with an empty plan and an empty moves file. Where a blueprints repo of the drive holds `plan/<label>`, the branch SHALL start from that plan's history, and the moves in the first blueprints repo's `signals/moves.rec` SHALL be copied with the commit they were read at. Run again, it SHALL change nothing.

#### Scenario: Willdan's plan is adopted
- **WHEN** `crew state init wldn` runs while willdan-blueprints holds `plan/wldn` and two moves
- **THEN** `wldn/main` holds the same bolts and units, its history reaches back to the plan's first commit, and `moves.rec` holds both moves

#### Scenario: A drive with two plans
- **WHEN** `crew state init madswan` runs while afterthought/blueprints and agentplot/blueprints each hold `plan/madswan`
- **THEN** `madswan/main` holds one plan with the bolts and units of both, the second plan's records added in one commit that names where they came from

#### Scenario: Two plans share a name
- **WHEN** the two plans being joined both hold a bolt or a unit of the same name
- **THEN** init is refused, naming it, and nothing is written

#### Scenario: Run twice
- **WHEN** `crew state init wldn` runs again
- **THEN** nothing is written, and it says the branch exists and at which commit

### Requirement: crew reads each host's runner from that runner's own branch
crew SHALL read a host's runner from `<label>/runner/<host>` of the drive's state repository, fetched with `<label>/main` in one fetch, and SHALL never write it. The branch holds four files:
- `runner.rec` says a runner serves the drive there;
- `answers.rec` says where each request stands;
- `places.rec` holds Flume's status of each place, as Flume gave it;
- `repositories.rec` holds each repository the runner keeps on its host, by its forge address with the folder of its clone.

A `repositories.rec` that recfix refuses, or that holds a record with no address or one address twice, SHALL make that host's runner unreadable, as the other files do. A branch with no `repositories.rec` SHALL be read as a runner that reports no repositories.

#### Scenario: One fetch
- **WHEN** a command reads the plan and the runners
- **THEN** it fetches the state repository once, `<label>/main` and `<label>/runner/*` together

#### Scenario: The repositories a runner keeps
- **WHEN** `madswan/runner/deneb` holds a `repositories.rec` naming `agentplot/boomdrive-cloud` at `/r/boomdrive-cloud`
- **THEN** crew reads that deneb's runner keeps `agentplot/boomdrive-cloud` in `/r/boomdrive-cloud`

#### Scenario: A runner that reports no repositories
- **WHEN** `madswan/runner/deneb` holds no `repositories.rec`
- **THEN** deneb's runner is read as before, reporting no repositories

#### Scenario: A repositories file crew can't read
- **WHEN** deneb's `repositories.rec` names `agentplot/boomdrive-cloud` twice
- **THEN** deneb's runner can't be read, naming the file, and only the work no runner crew read has taken reads unknown

### Requirement: What comes before a runner takes a kit's work is done on the main-level host
Some of what crew does on a kit comes before any runner has taken the work in hand:
- a start's `sluice branch create`, and its read of the kit's policy and its host's sluice;
- a new unit's or chore's name, checked against the kit's main;
- a bolt never started, landed by its close alone;
- the design agent's records, and a proposal's records, read in the kit;
- the board's explorations on the kit's main;
- the main level's folders of the drive's kits.

That work SHALL be done in the checkout the drive's main-level host keeps of the kit, found by the kit's forge address or, for a kit the plan names by its name alone, by that name. Where the main-level host is the host crew runs on and its teams file names the repository among its `repositories`, the kit's checkout SHALL be that entry's `checkout` and its folder that entry's `dir`, whether or not a session's space lists the repository. Otherwise they SHALL be the checkout and folder that host's spaces in the hosts file keep, `<session dir>/<name>/main` and `<session dir>/<name>`. Nothing SHALL be asked of a runner for it. It SHALL be refused, naming the host and the kit, where that host keeps none or keeps two repositories by the kit's name, counting those its teams file names with those its spaces keep. A refusal for a kit the host keeps none of SHALL also name `crew kit rename <kit> <new>` as the way on for a kit renamed on its host.

#### Scenario: A kit's first bolt is started
- **WHEN** `crew bolt start x` runs for crew's first bolt, no runner has taken any of crew's work, and deneb, madswan's main-level host, keeps `afterthought/crew` at `/d/madswan/crew/main`
- **THEN** sluice makes `bolt/x` from main in `/d/madswan/crew/main` on deneb, the policy there is read, and the start goes on as any start

#### Scenario: A kit the main-level host keeps no checkout of
- **WHEN** `crew bolt start x` runs and deneb's spaces keep no checkout of crew
- **THEN** it is refused naming deneb and crew, the plan is unchanged and no branch is made

#### Scenario: A kit renamed on its host before the plan
- **WHEN** deneb's spaces keep `agentplot/timber` and nothing by `tailrace`, and `crew bolt start x` runs for a bolt whose `Repo` is `tailrace`, with no rename
- **THEN** it is refused naming deneb, `tailrace` and `crew kit rename tailrace <new>`, and nothing is made

#### Scenario: A unit's name and a record
- **WHEN** the planner adds unit `a` to crew and the design agent runs `crew record crew 53 --proposed`
- **THEN** `a`'s name is checked against crew's main, and record 0053 read, in `/d/madswan/crew/main` on deneb

#### Scenario: The main level's kit folders
- **WHEN** madswan's plan names crew and sluice, deneb keeps both and a role of madswan's main level starts there
- **THEN** it may reach deneb's checkouts of crew and sluice, and a kit its plan names that deneb keeps none of is left out

#### Scenario: A kit in the runner's copy
- **WHEN** crew runs on deneb, madswan's main-level host, and deneb's teams file names `agentplot/crew` with `dir` `/r/agentplot/crew` and `checkout` `/v/agentplot/crew`, while a session's space also keeps `agentplot/crew` at `/d/agentplot`
- **THEN** crew is read and acted on before any runner takes its work in `/v/agentplot/crew`, its folder `/r/agentplot/crew`, by the name `crew` or the address `agentplot/crew`, and a role of madswan's main level may reach `/v/agentplot/crew`

#### Scenario: A repository the file names and no space keeps
- **WHEN** crew runs on deneb, deneb's teams file names `agentplot/weir`, and no session's space on deneb keeps it
- **THEN** weir is a kit deneb keeps, at the file's `checkout` and `dir`

#### Scenario: Another host's kit
- **WHEN** crew runs on deneb, its teams file names `WilldanGroup/atlas-kit`, and wldn's main level runs on chuck-herdr-alpha, whose spaces keep atlas-kit at `/workspace`
- **THEN** wldn's atlas-kit is read in `/workspace/atlas-kit/main` on chuck-herdr-alpha, since deneb's file names deneb's repositories alone

#### Scenario: One name, two repositories
- **WHEN** crew runs on deneb, its teams file names `agentplot/blueprints`, and a session's space on deneb keeps `afterthought/blueprints`
- **THEN** a kit named `blueprints` alone is refused naming both, and `agentplot/blueprints` is the file's checkout

### Requirement: A drive is never renamed
A drive's label SHALL be fixed once it is made, and no crew command SHALL rename one; `crew kit rename` renames a repository within the one drive it runs as. A label that changes in the teams file SHALL be read as one drive removed and another added: the new label's state is its own branch, `<new label>/main`, nothing of the old label's branch is read as the new drive's, and a command naming the old label is refused as naming no drive.

#### Scenario: A label changed in the teams file
- **WHEN** the teams file names `afterthought` where it named `swancloud`
- **THEN** crew reads afterthought's state from `afterthought/main` of its state repository, and a command run with `--label swancloud` is refused naming the drives the teams file has
