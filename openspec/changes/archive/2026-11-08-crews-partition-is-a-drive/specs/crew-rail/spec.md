## MODIFIED Requirements

### Requirement: The rail lists what waits on the user in four groups
`crew rail [--label L]` SHALL print, from any host, what waits on the user in a drive, or in every drive when no label is given or known. It SHALL group the rows in this order: proposals, batches, land, operations. A verify report SHALL be no row: its findings are fixed in one round with no wait on the user (`teams.17`). Every group heading SHALL be printed, with `none` under a group that has no rows.

#### Scenario: Something waits in two groups
- **WHEN** a proposal is open and a deploy is offered, and nothing else waits
- **THEN** `crew rail --label swancloud` prints the four headings in order, one row under proposals, one under operations, and `none` under batches and land

#### Scenario: Run from another host
- **WHEN** `crew rail --label wldn` runs on a host that holds none of wldn's teams
- **THEN** it prints the same rows as it does on the teams' host

#### Scenario: A unit in verify with its report
- **WHEN** unit `x` is in verify and its report was written after the last commit on `unit/x`
- **THEN** `crew rail` has no row for `x`

### Requirement: A host that does not answer is named
When a team's host does not answer, `crew rail` SHALL print the rows it could read and name that host, saying that its units and bolts may also wait on the user. It SHALL exit zero. When a drive's plan cannot be read, it SHALL name it and exit non-zero.

#### Scenario: The box is asleep
- **WHEN** chuck-herdr-alpha does not answer
- **THEN** `crew rail` still lists the open proposals and the rows of other hosts, and names chuck-herdr-alpha as not answering

### Requirement: A bolt whose every unit has merged and that has not landed is a row of its kit's
Each kit with a bolt in flight whose units have all merged and not all landed SHALL be one row under land, keyed `land/<kit>`, naming the drive's main-level ops and, in the plan's order, each such bolt with what it waits on. A bolt not yet proven SHALL say what it waits on: the verification as it reads, the units due a batch, the batches waiting on the user's answer, a fix in flight, a landing sluice rejected at its head for the bolt's own content, said as rejected with the bolt open for work, or that it takes main first, forecast at its present head to conflict with what main holds. A bolt whose landing the run record has queued, or landing again, SHALL say so with its number and that no work joins it until sluice decides, and SHALL be none of the bolts that can land (bolt-teams "A landing queued holds its bolt's work"). A bolt that can land whose last landing at its head sluice or its host stopped SHALL say, beside that it can land, what stopped it and that main-level ops submits it again once that is cleared. Once a bolt can land, the row SHALL carry `crew tell <label>-ops "Land <bolts that can land, in order>."`. The row SHALL have begun to wait at the time of the earliest last commit among its bolts' branches.

#### Scenario: The last unit merges
- **WHEN** the last unit of crew's bolt `b` merges into `bolt/b` through sluice, every unit's change has been in a batch the user has answered, and the runner carries that unit's place landed at `bolt/b`'s head
- **THEN** crew's row under land names `b` and `swancloud-ops`, saying `b` waits to land, with the tell that lands it

#### Scenario: Two bolts of one kit
- **WHEN** crew's bolts `b` and `c` can both land, `b` first in the plan
- **THEN** there is one row, `land/crew`, naming `b` then `c`, its tell naming both in that order

#### Scenario: A verification that is not green
- **WHEN** every unit of bolt `b` has merged and been in a batch the user has answered, and `bolt/b`'s head is no landing of its work that the runner reports
- **THEN** `b`'s line says it lands once its verification is green and what the verification is now, and the row's tell leaves `b` out

#### Scenario: A batch that waits on the user
- **WHEN** every unit of bolt `b` has merged, its verification is green, and batches 8 and 9, whose cards the user has not answered, hold its units' latest changes
- **THEN** `b`'s line says it lands once you have answered batches 8 and 9, and the row carries no tell when no other bolt can land

#### Scenario: A refused landing
- **WHEN** sluice refused `b`'s landing at its head for a conflict
- **THEN** `b`'s line says its landing was rejected at that head and the bolt is open for work, and, in sluice's words, that it lands again once a fix moves its head

#### Scenario: A landing queued
- **WHEN** the run record has `b`'s landing queued on main as #412 with no outcome
- **THEN** `b`'s line says its landing is queued as #412 and that no unit, chore or fix joins it until sluice decides, and the row's tell leaves `b` out

#### Scenario: Landing again
- **WHEN** `b`, rejected as #412, is queued again as #415
- **THEN** `b`'s line says it is landing again as #415, after #412 was rejected, and the row's tell leaves `b` out

#### Scenario: A bolt taking main first
- **WHEN** `b` reads proven and the run record holds a `forecast` on `bolt/b` at `b`'s present head naming a conflict with main on `README.md` and no submission queued on main
- **THEN** `b`'s line says it takes main first, forecast to conflict with main on `README.md`, until a fix taking main in moves its head, and the row's tell leaves `b` out

#### Scenario: A conflict forecast at an older head
- **WHEN** the run record's `forecast` on `bolt/b` naming a conflict with main is at a head `b` has since moved from
- **THEN** that forecast holds nothing on `b`'s line

#### Scenario: A stopped landing
- **WHEN** `b`'s last landing at its head did not land because sluice itself failed
- **THEN** `b`'s line says it can land, that sluice itself failed at that head, in sluice's words, and that `swancloud-ops` submits it again once that is cleared, and the row's tell names `b`

#### Scenario: It lands
- **WHEN** the bolt is landed and closed in the plan
- **THEN** the next `crew rail` names it on no row
