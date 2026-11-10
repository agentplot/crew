## ADDED Requirements

### Requirement: A delivered fix of main is a line of its kit's landings row, sent as a bolt's is
A fix of the kit's main whose code has delivered and whose submission waits held SHALL be a line of the kit's landings row, `fix main--<name>`, with the first line of its brief, ticked and sent on the kit's landings card as a bolt's row is, crew's raise of the card posting its land on the user's send (rail-cards "The user's send on a kit's landings card posts one land for each row it lands"). The line SHALL name no command for main-level ops.

#### Scenario: A fix of main waits beside a bolt
- **WHEN** `main--a-test-reads-its-fixture`'s code has delivered and its submission waits held
- **THEN** crew's landings row has a line `fix main--a-test-reads-its-fixture` with the failure's first line, saying it can land on the user's send of `land/crew`, and names no `crew main fix` command

### Requirement: A sent fix of main's line names its land's request and the runner that submits it
Once a fix of main's land is posted, its line SHALL say it was sent on the user's word, with the land's request, and that the runner on its host submits it.

#### Scenario: A fix of main sent
- **WHEN** the user sent `land/crew` with `fix main--a-test-reads-its-fixture` ticked, and crew's raise posted its land as request 61
- **THEN** the fix's line says it was sent on the user's word, request 61, and that the runner on its host submits it

### Requirement: A kit's bolts whose units have all merged and not all landed are one row under land
Each kit with a bolt in flight whose units have all merged and not all landed SHALL be one row under land, keyed `land/<kit>`, naming the drive's main-level ops and, in the plan's order, each such bolt with what it waits on. The row SHALL have begun to wait at the time of the earliest last commit among its bolts' branches.

#### Scenario: Two bolts of one kit
- **WHEN** crew's bolts `b` and `c` can both land, `b` first in the plan
- **THEN** there is one row, `land/crew`, naming `b` then `c`, each able to land

#### Scenario: It lands
- **WHEN** the bolt is landed and closed in the plan
- **THEN** the next `crew rail` names it on no row

### Requirement: A bolt not yet proven says on its kit's row what it waits on
A bolt not yet proven SHALL say what it waits on: the verification as it reads, the units due a batch, the batches waiting on the user's answer, a fix in flight, a landing Flume refused at its head for a failed check, said as refused with the bolt open for work, in Flume's words, or that it takes main first, forecast at its present head to conflict with what main holds or refused there in conflict with it.

#### Scenario: A verification that is not green
- **WHEN** every unit of bolt `b` has merged and been in a batch the user has answered, and `bolt/b`'s head is no landing of its work that the runner reports
- **THEN** `b`'s line says it lands once its verification is green and what the verification is now, and `b` is none of the bolts that can land

#### Scenario: A batch that waits on the user
- **WHEN** every unit of bolt `b` has merged, its verification is green, and batches 8 and 9, whose cards the user has not answered, hold its units' latest changes
- **THEN** `b`'s line says it lands once you have answered batches 8 and 9, and `b` is none of the bolts that can land

#### Scenario: A refused landing
- **WHEN** the runner's report carries Flume's verdict on `b`'s submission at its head failed, waiting on its caller
- **THEN** `b`'s line says its landing was refused at that head and the bolt is open for work, and, in Flume's words, that it lands again once a fix moves its head

#### Scenario: A landing refused in conflict
- **WHEN** the runner's report carries Flume's verdict on `b`'s submission at its head a conflict with main on `README.md`
- **THEN** `b`'s line says it takes main first, in Flume's words, until a fix taking main in moves its head, and `b` is none of the bolts that can land

#### Scenario: A bolt taking main first
- **WHEN** `b` reads proven and the run record holds a `forecast` on `bolt/b` at `b`'s present head naming a conflict with main on `README.md`, and no land of `b` stands undecided
- **THEN** `b`'s line says it takes main first, forecast to conflict with main on `README.md`, until a fix taking main in moves its head, and `b` is none of the bolts that can land

#### Scenario: A conflict forecast at an older head
- **WHEN** the run record's `forecast` on `bolt/b` naming a conflict with main is at a head `b` has since moved from
- **THEN** that forecast holds nothing on `b`'s line

### Requirement: A bolt whose landing is asked or queued says how it stands and is none that can land
A bolt whose land crew has asked of the runner, or whose submission the runner reports in the merge queue, SHALL say so, with the land's request or the queue's entry and its state, and that no unit, chore or fix joins it until its outcome is read, and SHALL be none of the bolts that can land. A bolt whose landing crew can't tell from the runner's report SHALL say so and why.

#### Scenario: A land asked
- **WHEN** crew posted `b`'s land as request 57 and the runner has not answered it
- **THEN** `b`'s line says its landing is asked as request 57 and that no unit, chore or fix joins it until its outcome is read, and `b` is none of the bolts that can land

#### Scenario: A landing queued
- **WHEN** the runner's report carries `b`'s base place submitted, its merge queue entry #412 waiting
- **THEN** `b`'s line says its landing is #412, waiting, and that no unit, chore or fix joins it until its outcome is read, and `b` is none of the bolts that can land

#### Scenario: Landing again
- **WHEN** `b`'s landing was refused in conflict with main at its old head, its take-main fix merged, `b` reads proven at its new head, and crew posted its land again on the standing send as request 63
- **THEN** `b`'s line says its landing is asked as request 63, and `b` is none of the bolts that can land

#### Scenario: A landing crew can't tell
- **WHEN** crew posted `b`'s land and the branch of the runner that took `b`'s work can't be read
- **THEN** `b`'s line says its landing can't be told, and why

### Requirement: A bolt that can land lands on the user's send of its kit's card
Once a bolt can land, its kit's row under land SHALL say it lands on the user's send of `land/<kit>`'s card, and SHALL carry no command for main-level ops, since no word in a pane lands a bolt (record 0056 point 5). A bolt that can land whose last land at its head the runner or Flume stopped SHALL say, beside that it can land, what stopped it, in their words, nothing of the bolt's, and that it lands on the user's next send.

#### Scenario: The last unit merges
- **WHEN** the last unit of crew's bolt `b` merges into `bolt/b` through sluice, every unit's change has been in a batch the user has answered, and the runner carries that unit's place landed at `bolt/b`'s head
- **THEN** crew's row under land names `b` and `swancloud-ops`, saying `b` can land on the user's send of `land/crew`, and carries no `crew tell`

#### Scenario: A stopped landing
- **WHEN** the runner answered `b`'s land at its head refused, a place on `bolt/b` being live
- **THEN** `b`'s line says it can land, that its last landing at that head was stopped, in the runner's words, nothing of the bolt's, and that it lands on the user's next send

### Requirement: A bolt started before bolts were base places lands under the crew that started it
A bolt started before bolts were base places SHALL say it lands under the crew that started it, and SHALL be none of the bolts that can land.

#### Scenario: A bolt started before bolts were base places
- **WHEN** started bolt `b` has no launch of `bolt/b` in `requests.rec`, and reads proven
- **THEN** `b`'s line says it was started before bolts were base places and lands under the crew that started it, and `b` is none of the bolts that can land

## REMOVED Requirements

### Requirement: A fix of main waits to land on its kit's row
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A delivered fix of main is a line of its kit's landings row, sent as a bolt's is" and "A sent fix of main's line names its land's request and the runner that submits it".

### Requirement: A bolt whose every unit has merged and that has not landed is a row of its kit's
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A kit's bolts whose units have all merged and not all landed are one row under land", "A bolt not yet proven says on its kit's row what it waits on", "A bolt whose landing is asked or queued says how it stands and is none that can land", "A bolt that can land lands on the user's send of its kit's card" and "A bolt started before bolts were base places lands under the crew that started it".
