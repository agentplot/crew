## ADDED Requirements

### Requirement: crew reads each kit by the name its record gives it
crew SHALL read a kit by the name each of its records gives it: a `Repo` in the plan, `requests.rec` or the run record; the kit in a fix of main's work or a card key; and the repository a source names. No reader SHALL map one kit's name to another's, through `kit.rename` entries or any list of former names. A partition's kits SHALL be the names its plan and its landings give, each once.

#### Scenario: Landings under another name
- **WHEN** madswan's plan names `timber`, and its run record holds a `bolt.land` with `Repo: tailrace` and, after it, a `kit.rename` entry of `tailrace` to `timber`
- **THEN** madswan's kits are `tailrace` and `timber`, each once, on the board too, and the agents' views keep the keys the mod reads

#### Scenario: A launch read as written
- **WHEN** request 1 launched `one-seam-turns-every-credential-into-a-principal` with `Repo: flywheel-cloud`, and the run record holds a `kit.rename` entry of `flywheel-cloud` to `boomdrive-cloud`
- **THEN** crew reads request 1 as `flywheel-cloud`'s launch, and no runner is read as having taken `boomdrive-cloud`'s work from it

#### Scenario: A fix of main read as written
- **WHEN** the fix of main `x` was launched as `fix/main/tailrace/x`, its code delivered and its submission held, and the run record holds a `kit.rename` entry of `tailrace` to `timber`
- **THEN** it is shown on `tailrace`'s landings row, and `crew main fix timber x --send` is refused as no launch of `fix/main/timber/x` standing

#### Scenario: A source read as written
- **WHEN** a unit's source names `WilldanGroup/old-board:docs/adr/0017`, and the work's kit is `switchboard-kit`
- **THEN** a proposal resting on it reads record 0017 of `WilldanGroup/old-board`, as the source names it

### Requirement: requests.rec and the run record are only appended to
crew SHALL write `requests.rec` and the run record only by appending a record, and SHALL rewrite no record of either, `crew kit rename` among its writes.

#### Scenario: A rename appends only its entry
- **WHEN** the user runs `crew kit rename flywheel-cloud boomdrive-cloud` while request 1 stands under `flywheel-cloud`
- **THEN** the rename's commit holds `plan.rec` alone, `requests.rec` is as it was with request 1 under `flywheel-cloud`, and the run record gains only the rename's entry

### Requirement: A command given a kit writes it as given
A plan command given a kit by `--repo`, `bolt new`, `unit add` and `chore add` among them, SHALL write the kit as it was given. It SHALL read the kit through no rename and say nothing of one. A unit or chore given `--repo` with `--bolt` SHALL be refused unless `--repo` names the bolt's kit as the plan writes it.

#### Scenario: A kit given by --repo is written as given
- **WHEN** the run record holds a `kit.rename` entry of `tailrace` to `timber`, and the user runs `crew bolt new y "…" --repo tailrace`
- **THEN** bolt `y` is written with `Repo: tailrace`, and its answer says nothing of a rename

#### Scenario: A chore given another name of its bolt's kit
- **WHEN** bolt `trc-1` is in `timber`, the run record holds a `kit.rename` entry of `tailrace` to `timber`, and the planner adds `chore add bump "…" --bolt trc-1 --repo tailrace`
- **THEN** it is refused naming `trc-1` as in `timber`, not `tailrace`, and the plan is unchanged

## MODIFIED Requirements

### Requirement: A kit renamed on its host is renamed across the plan in one act
`crew kit rename <old> <new>` SHALL rewrite the `Repo` of every Bolt and Unit record of the partition's plan that names `<old>`, by its name or its forge address, to `<new>` as given. The rewrite SHALL be one commit with one `kit.rename` entry, and SHALL change nothing else of the plan: no Goal, Intent or Source, and no record added, removed or moved. It SHALL append no request for a runner, and launch, retry or drop nothing. It SHALL rewrite no other file: `requests.rec`, the run record, `proposals.rec`, signals and `moves.rec` stay as written, and what they name under `<old>` is read as `<old>`'s. It SHALL be refused, with nothing written, in any of these cases:
- `<old>` is no kit of the partition, neither its plan's nor its landings'. A name an earlier rename renamed is judged as written, as any name is;
- the partition's main-level host keeps no repository by `<new>` in its spaces, or still keeps one by `<old>`. The refusal names the host and what its spaces keep;
- `<new>` is the name of one of the partition's bolts;
- the plan it leaves fails `recfix --check` or crew's own rules;
- the hosts file can't be read.

A proposal MAY hold it, applied as any of its commands, and the user MAY run it at a shell. The planner's direct run SHALL be refused naming `crew plan propose`, and any other agent crew started SHALL be refused naming the planner.

#### Scenario: The user renames tailrace
- **WHEN** madswan's plan names `tailrace` in 21 records and `flywheel-cloud` in 2, deneb's spaces keep `agentplot/timber` and nothing by `tailrace`, and the user runs `crew kit rename tailrace timber`
- **THEN** the 21 records name `timber`, the other 2 still name `flywheel-cloud`, every other field of every record is as it was, and one commit holds the change

#### Scenario: Not renamed on its host
- **WHEN** deneb's spaces still keep `agentplot/tailrace` and the user runs `crew kit rename tailrace timber`
- **THEN** it is refused naming deneb and `agentplot/tailrace`, and the plan is unchanged

#### Scenario: A new name the host does not keep
- **WHEN** deneb's spaces keep no repository by `timber`
- **THEN** `crew kit rename tailrace timber` is refused naming deneb and `timber`, and the plan is unchanged

#### Scenario: The new name is a bolt's
- **WHEN** madswan's plan holds a bolt named `timber`
- **THEN** `crew kit rename tailrace timber` is refused naming the bolt, and the plan is unchanged

#### Scenario: A kit only its landings name
- **WHEN** madswan's plan names no `tailrace` record and its run record holds a `bolt.land` of `tailrace`
- **THEN** `crew kit rename tailrace timber` renames no record and writes its `kit.rename` entry, and madswan's kits still name `tailrace`, by its landing as written

#### Scenario: A name an earlier rename renamed
- **WHEN** madswan's plan names `timber` and no `tailrace`, no landing names `tailrace`, and the run record holds a `kit.rename` entry of `tailrace` to `timber`
- **THEN** `crew kit rename tailrace trc` is refused as naming no kit of madswan, the refusal naming no rename, and the plan is unchanged

#### Scenario: The planner proposes it
- **WHEN** madswan-planner runs `crew kit rename tailrace timber`
- **THEN** it is refused naming `crew plan propose`, and a proposal holding `kit rename tailrace timber` is checked and, on the user's approval, renames the records in the approval's commit

#### Scenario: Another agent runs it
- **WHEN** madswan-ops runs `crew kit rename tailrace timber`
- **THEN** it is refused naming the planner, and the plan is unchanged

#### Scenario: A started bolt's kit
- **WHEN** `you-sign-in-to-staging` is started, its unit `one-seam-turns-every-credential-into-a-principal` has merged into its branch, and the user renames `flywheel-cloud` to `boomdrive-cloud`
- **THEN** the bolt and its unit name `boomdrive-cloud`, the bolt keeps `Path: flume`, `requests.rec` is unchanged with no request appended, and the unit reads merged as the runner carried it

#### Scenario: A started bolt renamed lands in its kit's clone
- **WHEN** `you-sign-in-to-staging` is renamed into `boomdrive-cloud`, request 1 launched its unit under `flywheel-cloud`, and deneb's runner took it and reports keeping `agentplot/boomdrive-cloud`
- **THEN** request 1 reads as written, its unit reads merged from deneb's place, and the bolt is read and landed in the clone deneb reports for `boomdrive-cloud`, a row of `land/boomdrive-cloud`

#### Scenario: The command at a shell
- **WHEN** the user runs `crew kit rename` on the stubs, and the planner proposes a rename the user then approves
- **THEN** the user's run writes one commit and its entry, the planner's direct run is refused, and the proposal's approval renames the records

## REMOVED Requirements

### Requirement: What crew recorded under a kit's former name is read under its name now
**Reason**: The user ruled out any reader's workaround for a kit's former name on 2026-11-06 (signal `2026-11-06-agentplot-planner-230ee466/01`: "I don't want you to be building fucking custom workaround shit"). Record 0060, accepted on 2026-11-07, has `plan.22` rule out "a reader through `kit_now` or the run record's `kit.rename` entries".
**Migration**: Each kit is read by the name its record gives it, as "crew reads each kit by the name its record gives it" says. madswan's landings under `tailrace` and its launches under `flywheel-cloud` read under those names, as its landings under `flywheel-web` already did.

### Requirement: A command given a kit's former name writes its name now
**Reason**: Writing a former name under the name now read it through the partition's renames, which no reader does (`plan.22`).
**Migration**: `bolt new`, `unit add` and `chore add` write the kit as given, as "A command given a kit writes it as given" says.
