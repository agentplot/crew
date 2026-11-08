## ADDED Requirements

### Requirement: A repository is renamed by one explicit command
`crew kit rename <old> <new>` SHALL rename a repository in crew's records as one act: one commit with one `kit.rename` entry. Nothing SHALL rename a repository on its own. The rename SHALL append no request and SHALL launch, retry or drop nothing. A proposal MAY hold it, applied as any of its commands, and the user MAY run it at a shell. The planner's direct run SHALL be refused naming `crew plan propose`, and any other agent crew started SHALL be refused naming the planner.

#### Scenario: The user renames tailrace once its work is finished
- **WHEN** madswan's plan holds no bolt, unit or chore in `tailrace`, its run record holds two `bolt.land` entries with `Repo: tailrace`, no card, batch or open proposal names it, deneb's runner reports `agentplot/timber` and not `agentplot/tailrace` in `repositories.rec`, and the user runs `crew kit rename tailrace timber --label madswan`
- **THEN** one commit renames its records, no request is appended, and the run record holds one `kit.rename` entry naming both names

#### Scenario: A proposal holds it
- **WHEN** madswan-planner proposes `kit rename tailrace timber` and the user approves it
- **THEN** the approval's one commit renames the records, and its entry's `From` names `proposal/<n>` beside `kit/tailrace`

#### Scenario: The planner and the other agents
- **WHEN** madswan-planner runs `crew kit rename tailrace timber`, and madswan-ops runs the same
- **THEN** the planner's run is refused naming `crew plan propose`, and ops's naming the planner

### Requirement: A rename waits until the repository's work is finished
`crew kit rename <old> <new>` SHALL be refused, with nothing written, naming all that stands, while `<old>`'s work stands, matched by name or address:
- a bolt, unit or chore of the plan;
- a fix of its main or a role's work in it, not landed or dropped;
- a place Flume holds live;
- a card open under `land/<old>` or `record/<old>/<n>`;
- an unanswered batch holding its work that still waits;
- an open proposal, but the one applying it, whose `Do` names it.

#### Scenario: A bolt not landed
- **WHEN** madswan's plan holds bolt `trc-1` with `Repo: tailrace`
- **THEN** `crew kit rename tailrace timber` is refused naming `trc-1` as not landed, and nothing is written

#### Scenario: A fix of main not landed
- **WHEN** request 9 launched `fix/main/tailrace/cargo-lock` with no drop, and deneb's runner carries its place at code
- **THEN** the rename is refused naming the fix and its stage

#### Scenario: A place Flume holds live
- **WHEN** deneb's runner carries Flume's status of request 4's place, launched with `Repo: tailrace`, its phase live
- **THEN** the rename is refused naming the place and deneb

#### Scenario: An open card
- **WHEN** madswan-ops holds a card open under `land/tailrace`, or its last card there was closed as lost to its owner
- **THEN** the rename is refused naming `land/tailrace` and madswan-ops

#### Scenario: An unanswered batch
- **WHEN** batch 12 holds a unit of a landed `tailrace` bolt beside a unit of another kit that still waits, and the user has not answered it
- **THEN** the rename is refused naming batch 12

#### Scenario: An open proposal names it
- **WHEN** proposal 170 is open and one of its `Do` lines holds `--repo tailrace`, an object built on `tailrace` or a source `agentplot/tailrace:docs/adr/0017`
- **THEN** the rename is refused naming proposal 170, while a goal whose words mention tailrace names nothing

#### Scenario: Several things stand
- **WHEN** bolt `trc-1` has not landed and madswan-ops holds a card open under `land/tailrace`
- **THEN** the one refusal names both

### Requirement: A rename waits until no host keeps the old name
`crew kit rename <old> <new>` SHALL be refused while any host still keeps `<old>`, naming the host and what keeps it. The hosts read SHALL be each host with a runner branch of the partition, and the partition's main-level host. A host's keeping SHALL be its runner's `repositories.rec` where that runner reports one, and otherwise the host's spaces in the hosts file. Where crew can't read something this depends on, it SHALL be refused naming what it could not read. No host needs to keep `<new>`.

#### Scenario: A host still keeps it
- **WHEN** deneb's runner reports `agentplot/tailrace` among its repositories
- **THEN** the rename is refused naming deneb's runner and `agentplot/tailrace`

#### Scenario: A runner that reports no repositories
- **WHEN** deneb's runner branch holds no `repositories.rec` and deneb's spaces in the hosts file keep `agentplot/tailrace`
- **THEN** the rename is refused naming deneb's spaces and `agentplot/tailrace`

#### Scenario: What crew can't read
- **WHEN** deneb's runner branch can't be read, or a runner's host is neither reporting its repositories nor listed in the hosts file
- **THEN** the rename is refused naming that host and why, and nothing is written

#### Scenario: The new name kept by no host
- **WHEN** no host keeps `timber` or `tailrace`, and nothing else stands
- **THEN** `crew kit rename tailrace timber` renames the records

### Requirement: A rename takes only a name some record holds, and a new name of its own
`crew kit rename <old> <new>` SHALL be refused, with nothing written, where `<old>` and `<new>` name one repository, where `<new>` is the name of one of the partition's bolts, since `land/<new>` would name the bolt, and where no record of the partition names `<old>`.

#### Scenario: No record names it
- **WHEN** no record of madswan names `rocs-kit`
- **THEN** `crew kit rename rocs-kit rocs --label madswan` is refused saying no record names `rocs-kit`

#### Scenario: One repository, or a bolt's name
- **WHEN** the user runs `crew kit rename tailrace agentplot/tailrace`, or `crew kit rename tailrace crew-bolt` where `crew-bolt` is a bolt of madswan
- **THEN** the first is refused as two names of one repository and the second naming the bolt, and nothing is written

### Requirement: A rename renames every record a reader matches the repository by
In its one commit, `crew kit rename <old> <new>` SHALL rename `<old>` to `<new>` in each plan Source naming a decision record in `<old>`'s repository; each request's `Repo`, and a fix of its main's `Work`; and each run-record entry on the branch, its `Repo` and the objects of its `On` and `From` built on the name. A field keeps its form: a name becomes `<new>`'s, an address `<owner>/<old>` becomes `<owner>/<new>` unless `<new>` is an address, and an object takes `<new>`'s name.

#### Scenario: A request, a landing, a card and a source
- **WHEN** request 3 has `Repo: flywheel-cloud` and `Work: fix/main/flywheel-cloud/one-seam`, a `bolt.land` entry has `Repo: flywheel-cloud`, a closed landings card's `card.post` has `On: kit/flywheel-cloud` and `Key: land/flywheel-cloud`, a crew unit's Source names `agentplot/flywheel-cloud:docs/adr/0017`, and the user renames `flywheel-cloud` to `boomdrive-cloud`
- **THEN** the request's `Repo` is `boomdrive-cloud` and its `Work` `fix/main/boomdrive-cloud/one-seam`, the landing's `Repo` is `boomdrive-cloud`, the `card.post` has `On: kit/boomdrive-cloud` and keeps `Key: land/flywheel-cloud`, the Source names `agentplot/boomdrive-cloud:docs/adr/0017`, and the entry's `Count` is 4

#### Scenario: Every object built on the name
- **WHEN** entries name `kit/tailrace`, `land/tailrace`, `queue/tailrace`, `record/tailrace/0017` and `fix/main/tailrace/cargo-lock` in their `On` or `From`, and the user renames `tailrace` to `timber`
- **THEN** each names `timber` in its place, and an object of another repository, `kit/tailrace-web`, is as it was

#### Scenario: A forge address keeps its owner
- **WHEN** a request has `Repo: agentplot/flywheel-cloud` and the user renames `flywheel-cloud` to `boomdrive-cloud`
- **THEN** its `Repo` is `agentplot/boomdrive-cloud`

### Requirement: A rename leaves what no reader looks a repository up from
`crew kit rename` SHALL leave as written the plan's Goals and Intents, a Source naming no decision record, `proposals.rec`, signals, `moves.rec`, `asks.rec`, `roles.rec`, an entry's `Key`, `Why` and `Refused`, every `kit.rename` entry, the runners' branches and each host's own run-record files. It SHALL rewrite a file record by record, its descriptor, comments and order kept, and SHALL leave a file in which it renames no record byte for byte.

#### Scenario: What stays as written
- **WHEN** a bolt's Goal says "tailrace", a closed proposal's `Do` holds `--repo tailrace`, an earlier `kit.rename` entry has `From: kit/tailrace`, and the user renames `tailrace` to `timber`
- **THEN** each is as it was, and a run-record file naming no `tailrace` is unchanged byte for byte

### Requirement: A rename run again renames what an earlier one left
`<old>` MAY be any name a record still holds, so running `crew kit rename <old> <new>` again renames whatever an earlier rename left under `<old>`, writing its own entry. Before it reads the branch, the rename SHALL push the entries its own host kept unpushed, so they are renamed with the rest.

#### Scenario: Run again over what an earlier rename left
- **WHEN** madswan's plan names `boomdrive-cloud` while request 3 and two landings still name `flywheel-cloud`, and the user runs `crew kit rename flywheel-cloud boomdrive-cloud --label madswan`
- **THEN** request 3 and both landings name `boomdrive-cloud`, the entry's `Count` is 3, and the earlier `kit.rename` entry is as it was

#### Scenario: The host's kept entries go first
- **WHEN** deneb kept a `bolt.land` entry under `tailrace` unpushed, and the user runs the rename on deneb
- **THEN** crew pushes that entry before it reads the branch, and the rename's commit renames it with the others

## REMOVED Requirements

### Requirement: A kit renamed on its host is renamed across the plan in one act
**Reason**: Record 0060, accepted by the user on 2026-11-07, together with `plan.22`. A repository is renamed by one explicit command once its work is finished, and never while it stands. Its records are renamed wherever a reader matches it, not in the plan alone. The command no longer waits for the host to keep `<new>`, since the repository is added back under `<new>` after the rename.
**Migration**: The requirements added here replace it, from "A repository is renamed by one explicit command" to "A rename run again renames what an earlier one left". A started bolt's repository is renamed once the bolt has landed or been dropped.
