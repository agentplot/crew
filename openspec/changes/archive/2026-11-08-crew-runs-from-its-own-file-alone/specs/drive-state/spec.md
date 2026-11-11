## MODIFIED Requirements

### Requirement: What comes before a runner takes a kit's work is done on the main-level host
Some of what crew does on a kit comes before any runner has taken the work in hand:
- a start's `sluice branch create`, and its read of the kit's policy and its host's sluice;
- a new unit's or chore's name, checked against the kit's main;
- a bolt never started, landed by its close alone;
- the design agent's records, and a proposal's records, read in the kit;
- the board's explorations on the kit's main;
- the main level's folders of the drive's kits.

That work SHALL be done in the checkout the drive's main-level host keeps of the kit, found by the kit's forge address or, for a kit the plan names by its name alone, by that name. Where the main-level host is the host crew runs on and its teams file names the repository among its `repositories`, the kit's checkout SHALL be that entry's `checkout` and its folder that entry's `dir`, whether or not a drive's `repos` lists the repository. Otherwise they SHALL be `<folder>/<name>/main` and `<folder>/<name>` in the folder of the first drive whose machine is that host and whose `repos` lists the repository, as the teams file gives them. Nothing SHALL be asked of a runner for it, and no file but the teams file SHALL be read for it. It SHALL be refused, naming the host and the kit, where that host keeps none or keeps two repositories by the kit's name, counting those its teams file names with those its drives' `repos` list. A refusal for a kit the host keeps none of SHALL also name `crew kit rename <kit> <new>` as the way on for a kit renamed on its host.

#### Scenario: A kit's first bolt is started
- **WHEN** `crew bolt start x` runs for crew's first bolt, no runner has taken any of crew's work, and deneb, madswan's main-level host, keeps `afterthought/crew` at `/d/madswan/crew/main`, madswan's folder being `/d/madswan` and its `repos` listing `afterthought/crew`
- **THEN** sluice makes `bolt/x` from main in `/d/madswan/crew/main` on deneb, the policy there is read, and the start goes on as any start

#### Scenario: A kit the main-level host keeps no checkout of
- **WHEN** `crew bolt start x` runs, deneb's teams file names no crew in `repositories`, and no drive whose machine is deneb lists crew in its `repos`
- **THEN** it is refused naming deneb and crew, the plan is unchanged and no branch is made

#### Scenario: A kit renamed on its host before the plan
- **WHEN** deneb's drives' `repos` list `agentplot/timber` and nothing by `tailrace`, and `crew bolt start x` runs for a bolt whose `Repo` is `tailrace`, with no rename
- **THEN** it is refused naming deneb, `tailrace` and `crew kit rename tailrace <new>`, and nothing is made

#### Scenario: A unit's name and a record
- **WHEN** the planner adds unit `a` to crew and the design agent runs `crew record crew 53 --proposed`
- **THEN** `a`'s name is checked against crew's main, and record 0053 read, in `/d/madswan/crew/main` on deneb

#### Scenario: The main level's kit folders
- **WHEN** madswan's plan names crew and sluice, deneb keeps both and a role of madswan's main level starts there
- **THEN** it may reach deneb's checkouts of crew and sluice, and a kit its plan names that deneb keeps none of is left out

#### Scenario: A kit in the runner's copy
- **WHEN** crew runs on deneb, madswan's main-level host, and deneb's teams file names `agentplot/crew` with `dir` `/r/agentplot/crew` and `checkout` `/v/agentplot/crew`, while agentplot's `repos` also lists `agentplot/crew` in its folder `/d/agentplot`
- **THEN** crew is read and acted on before any runner takes its work in `/v/agentplot/crew`, its folder `/r/agentplot/crew`, by the name `crew` or the address `agentplot/crew`, and a role of madswan's main level may reach `/v/agentplot/crew`

#### Scenario: A repository the file names and no space keeps
- **WHEN** crew runs on deneb, deneb's teams file names `agentplot/weir` in `repositories`, and no drive's `repos` lists it
- **THEN** weir is a kit deneb keeps, at the file's `checkout` and `dir`

#### Scenario: Another host's kit
- **WHEN** crew runs on deneb, its teams file names `WilldanGroup/atlas-kit` in `repositories`, and wldn's main level runs on chuck-herdr-alpha, wldn's folder being `/workspace` and its `repos` listing atlas-kit
- **THEN** wldn's atlas-kit is read in `/workspace/atlas-kit/main` on chuck-herdr-alpha, since deneb's file names deneb's repositories alone

#### Scenario: One name, two repositories
- **WHEN** crew runs on deneb, its teams file names `agentplot/blueprints` in `repositories`, and a drive on deneb lists `afterthought/blueprints` in its `repos`
- **THEN** a kit named `blueprints` alone is refused naming both, and `agentplot/blueprints` is the file's checkout
