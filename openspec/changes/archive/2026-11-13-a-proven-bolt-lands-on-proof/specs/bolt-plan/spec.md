## RENAMED Requirements

- FROM: `### Requirement: A drive's one plan holds only Bolt and Unit records of what is meant to be built`
- TO: `### Requirement: A drive's one plan holds only Bolt, Unit and Hold records of what is meant to be built`

## MODIFIED Requirements

### Requirement: A drive's one plan holds only Bolt, Unit and Hold records of what is meant to be built
Each drive SHALL keep one plan, the recutils file `plan.rec` on its branch of its state repository, for all of its kits. The plan SHALL hold only Bolt, Unit and Hold records. A Bolt has its name, repo, goal, sources and its mark to stay. A Unit has its name, repo, bolt, intent, sources and `After`; one marked `Kind: chore` is a chore. A Hold names a kit, or none for the whole drive, with its words. The plan SHALL never hold how far the work has got.

#### Scenario: Business and agentplot work
- **WHEN** the drive `madswan` builds kits whose design is in afterthought/blueprints and kits whose design is in agentplot/blueprints
- **THEN** its bolts and units for both are in one `plan.rec` on `madswan/main`, and afterthought's plan is `plan.rec` on `afterthought/main`

#### Scenario: A plan that fails its schema
- **WHEN** a hand edit leaves a duplicated key or a field the schema does not allow
- **THEN** crew refuses to read that plan, and names the commit and `recfix --check`'s message

#### Scenario: A source in a blueprints repo
- **WHEN** a unit's source is a page of the drive's first blueprints repo
- **THEN** its `Source` is that page's path, and a page of another repo is `<owner>/<name>:<path>`

#### Scenario: A chore among the units
- **WHEN** a bolt holds two units and a chore between them
- **THEN** `plan.rec` holds the chore's Unit record, marked `Kind: chore`, between the two units' records, and the file's order is their build order

#### Scenario: A bolt marked to stay and a hold
- **WHEN** bolt `console-pages` of switchboard-kit is marked to stay, and the user put a hold on switchboard-kit, saying "Cutover"
- **THEN** `plan.rec` holds `console-pages`'s Bolt record with `Stays: yes`, and a Hold record naming `Kit: switchboard-kit` with `Why: Cutover`

#### Scenario: Two holds on one kit
- **WHEN** a hand edit leaves two Hold records naming switchboard-kit, or two naming no kit
- **THEN** crew refuses to read that plan, naming the holds

#### Scenario: A branch from before the mark and the holds
- **WHEN** a drive's `plan.rec` was written before Bolt allowed `Stays` and before the Hold record set
- **THEN** it is read as it stands, and its next write brings its descriptors in step, allowing both

### Requirement: A rename renames every record a reader matches the repository by
In its one commit, `crew kit rename <old> <new>` SHALL rename `<old>` to `<new>` in each plan Source naming a decision record in `<old>`'s repository, and each Hold's `Kit`; each request's `Repo`, and a fix of its main's `Work`; and each run-record entry, its `Repo` and the objects of its `On` and `From` built on the name. A field keeps its form: a name becomes `<new>`'s, an address `<owner>/<old>` becomes `<owner>/<new>` unless `<new>` is an address, and an object takes `<new>`'s name.

#### Scenario: A request, a landing, a card and a source
- **WHEN** request 3 has `Repo: flywheel-cloud` and `Work: fix/main/flywheel-cloud/one-seam`, a `bolt.land` entry has `Repo: flywheel-cloud`, a closed landings card's `card.post` has `On: kit/flywheel-cloud` and `Key: land/flywheel-cloud`, a crew unit's Source names `agentplot/flywheel-cloud:docs/adr/0017`, and the user renames `flywheel-cloud` to `boomdrive-cloud`
- **THEN** the request's `Repo` is `boomdrive-cloud` and its `Work` `fix/main/boomdrive-cloud/one-seam`, the landing's `Repo` is `boomdrive-cloud`, the `card.post` has `On: kit/boomdrive-cloud` and keeps `Key: land/flywheel-cloud`, the Source names `agentplot/boomdrive-cloud:docs/adr/0017`, and the entry's `Count` is 4

#### Scenario: Every object built on the name
- **WHEN** entries name `kit/tailrace`, `land/tailrace`, `queue/tailrace`, `record/tailrace/0017` and `fix/main/tailrace/cargo-lock` in their `On` or `From`, and the user renames `tailrace` to `timber`
- **THEN** each names `timber` in its place, and an object of another repository, `kit/tailrace-web`, is as it was

#### Scenario: A forge address keeps its owner
- **WHEN** a request has `Repo: agentplot/flywheel-cloud` and the user renames `flywheel-cloud` to `boomdrive-cloud`
- **THEN** its `Repo` is `agentplot/boomdrive-cloud`

#### Scenario: A hold on the kit
- **WHEN** a hold on flywheel-cloud stands, saying "Cutover", and the user renames `flywheel-cloud` to `boomdrive-cloud`
- **THEN** the Hold names `Kit: boomdrive-cloud` with the words "Cutover", and no land of boomdrive-cloud's is posted while it stands

## ADDED Requirements

### Requirement: A bolt is marked to stay only when it is planned or started
`crew bolt new … --stays` and `crew bolt start <bolt> --stays` SHALL mark the bolt `Stays: yes`, in the same write that plans or starts it, by the hands that may run each, a proposal's among them (record 0067). No other command SHALL set the mark, so it is set ahead of time and never after the bolt is proven.

#### Scenario: Planned to stay
- **WHEN** the user approves a proposal holding `crew bolt new console-pages "Console pages" --repo switchboard-kit --stays`
- **THEN** `console-pages` is in the plan marked `Stays: yes`, and the run record's `bolt.new` names it

#### Scenario: Started to stay
- **WHEN** the user runs `crew bolt start console-pages --stays --label wldn`, and a runner answers for wldn
- **THEN** the start's one write marks `console-pages` `Path: flume` and `Stays: yes`, and requests its launches as any start does

#### Scenario: No mark later
- **WHEN** anyone runs `crew bolt stay console-pages`
- **THEN** crew refuses it as no command it has, and the plan is unchanged

### Requirement: The user lifts a bolt's mark to stay
`crew bolt unstay <bolt>` SHALL lift a bolt's mark to stay, in one write recording `bolt.unstay`. The user SHALL run it, or approve a proposal holding it; any agent running it directly SHALL be refused, naming the planner. It SHALL be refused for a bolt not marked, naming it. Once a started bolt's mark is lifted, crew SHALL hand a raise of its kit's landings card to the main level's host, and the bolt lands on its next proof.

#### Scenario: Lifted
- **WHEN** `console-pages`, marked to stay, reads proven as a row of `land/switchboard-kit`, and the user runs `crew bolt unstay console-pages --label wldn`
- **THEN** its mark is gone from the plan, and the raise the lift hands posts its land on proof, the card no longer asking for it

#### Scenario: An agent lifts it
- **WHEN** wldn-ops runs `crew bolt unstay console-pages`
- **THEN** it is refused, naming wldn-planner, who proposes it, and the plan is unchanged

#### Scenario: Not marked
- **WHEN** the user runs `crew bolt unstay apex-zones`, which is not marked to stay
- **THEN** it is refused, saying `apex-zones` is not marked to stay, and nothing is written

### Requirement: A hold on a drive or a kit is put and lifted through crew
`crew plan hold "<why>" [--repo <kit>]` SHALL put a hold on the drive's landings, or one kit's, with its words, as one Hold record, a second on the same kit or drive changing its words. `crew plan go [--repo <kit>]` SHALL lift it, refused where none stands, and hand a raise of each landings card it held to the main level's host. Each SHALL be the user's, ops's hold only as main-level has it; the planner and the design agent are refused.

#### Scenario: A kit held
- **WHEN** the user runs `crew plan hold "Cutover" --repo switchboard-kit --label wldn`
- **THEN** the plan holds a Hold naming switchboard-kit with the words "Cutover", the run record holds a `plan.hold` on `kit/switchboard-kit` with none of the words, and no land of switchboard-kit's is posted while it stands

#### Scenario: The drive held
- **WHEN** the user runs `crew plan hold "Cutover" --label wldn`
- **THEN** the plan holds a Hold naming no kit, and no land of any of wldn's kits is posted while it stands

#### Scenario: Lifted
- **WHEN** the user runs `crew plan go --repo switchboard-kit --label wldn`
- **THEN** the Hold is gone from the plan, the run record holds a `plan.go` on `kit/switchboard-kit`, and a raise of `land/switchboard-kit` is handed to wldn's main level's host

#### Scenario: The drive's hold lifted
- **WHEN** a hold on the drive wldn and one on breadboard-kit stand, atlas-kit's card holds only a fix of main, and the user runs `crew plan go --label wldn`
- **THEN** the drive's Hold is gone from the plan, and a raise of the landings card of each of wldn's kits is handed to its main level's host, atlas-kit's among them, but breadboard-kit's, which its own hold still holds

#### Scenario: Nothing to lift
- **WHEN** the user runs `crew plan go --repo atlas-kit --label wldn` and no hold names atlas-kit
- **THEN** it is refused, saying no hold names atlas-kit and naming the drive's hold where one stands, and nothing is written

#### Scenario: The planner holds
- **WHEN** wldn-planner runs `crew plan hold "Cutover" --label wldn`
- **THEN** it is refused, naming the user and wldn-ops, and the plan is unchanged
