# crew-rail Specification

## Purpose
One list of everything that waits on the user, read from the state crew already keeps, so the user can work down it and an answered item leaves it on its own.

## Requirements

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

### Requirement: Each row has its time, its age and the command that answers it
Each row SHALL name what waits, when it began to wait, how long ago that was, and the command that answers it, written to be pasted into a shell, with every path quoted. Within a group, rows SHALL be ordered oldest first. A row's time SHALL be read from the same state as the row itself, never from a record kept for the rail.

#### Scenario: Two units in review
- **WHEN** unit `a` has been in review since 09:00 and unit `b` since 11:00
- **THEN** `a`'s row comes before `b`'s, and each shows its time and its age

### Requirement: A unit in review is a row with the command that opens its whole change
Each unit whose stage is review SHALL be a row under review, naming its team and host. The row SHALL carry a command that opens the unit's whole change folder in plannotator, and the command that approves it (`crew unit approve <unit> --label <label>`). It SHALL have begun to wait at the time of the last commit on the unit's branch.

#### Scenario: Opened on the team's host
- **WHEN** `crew rail` runs on the host of the unit's team
- **THEN** the row carries `plannotator-tui herdr open <kit>/places/<unit>/openspec/changes/<unit>/`

#### Scenario: Opened from another host
- **WHEN** `crew rail` runs on a host other than the unit's team's host
- **THEN** the row carries `ssh -t <the team host's ssh name> plannotator-tui <the same folder>`

#### Scenario: Construct runs again
- **WHEN** the unit is sent back to construct
- **THEN** the next `crew rail` has no row for it until its change is in review again

### Requirement: Nothing is written to make or clear a row
`crew rail` SHALL read only the plan, the proposals, the kits and the run record, and SHALL write nothing to any of them. Every row SHALL leave the list when the state it was read from records its answer.

#### Scenario: A read leaves no trace
- **WHEN** `crew rail` runs
- **THEN** the drive's branch, the kits and the run record are unchanged

### Requirement: A host that does not answer is named
When a team's host does not answer, `crew rail` SHALL print the rows it could read and name that host, saying that its units and bolts may also wait on the user. It SHALL exit zero. When a drive's plan cannot be read, it SHALL name it and exit non-zero.

#### Scenario: The box is asleep
- **WHEN** chuck-herdr-alpha does not answer
- **THEN** `crew rail` still lists the open proposals and the rows of other hosts, and names chuck-herdr-alpha as not answering

### Requirement: A left bolt's land line says it would take main first once ticked
A bolt the user left on its kit's landings card, or stopped in their words to main-level ops, whose forecast against main the run record holds in conflict at its present head, SHALL be said on the kit's land row to be left by the user and to take main first once ticked, naming the files, and SHALL be none of the bolts that can land. A left bolt with no such conflict SHALL read as it does today.

#### Scenario: Left and forecast to conflict
- **WHEN** `z` is left on `land/crew`, reads proven, and the run record holds `z` forecast to conflict with main on `README.md` at its present head
- **THEN** crew's row under land says `z` was left by the user and takes main first once ticked, forecast to conflict with main on `README.md`, and `z` is none of the bolts that can land

#### Scenario: Ticked
- **WHEN** the user ticks `z` and its take-main fix is told
- **THEN** `z`'s line says it takes main first, until its team's take-main fix moves its head

### Requirement: A bolt's land line shows its age and who held its time
Each bolt's line on its kit's landings row SHALL end with the bolt's age since its newest give, the minutes of it each holder held, and who holds it now and since when. It SHALL read them as the board's head line does, by the same rule and from the same read, so the rail and the board never differ for one bolt. A bolt still being built has no line on the rail and is read on the board. The rail SHALL raise no card and add no row because of a bolt's age.

#### Scenario: A bolt waiting on the user's yes
- **WHEN** crew's bolt `b`, given to crw-6 five hours ago, has every unit merged, and its kit's landings card has been open for two hours
- **THEN** `b`'s line on the `land/crew` row says `5h 00m` with its shares, the user's `2h 00m` among them, and that the user holds it since the card's post

#### Scenario: The rail and the board agree
- **WHEN** the follower writes the rail's frame and the board's from one read
- **THEN** `b`'s age, shares and holder are the same on the land line and on the board's head line

### Requirement: An open proposal is a row until the user approves or drops it
Each open proposal on the drive's branch SHALL be a row under proposals. The row SHALL name the command that prints it (`crew plan proposed <n> --label <label>`), the command that opens it in plannotator for the user to read and annotate (`crew plan proposed <n> --label <label> --open`), and the command that approves it (`crew plan approve <n> --label <label>`). It SHALL have begun to wait at its `plan.propose` entry in the run record, or at its `Opened` date when no entry is found.

#### Scenario: An open proposal
- **WHEN** proposal 3 is open and touches a bolt in flight
- **THEN** its row names no agreement it needs and carries `crew plan proposed 3 --label wldn`, `crew plan proposed 3 --label wldn --open` and `crew plan approve 3 --label wldn`

#### Scenario: Approved
- **WHEN** proposal 3 is approved
- **THEN** the next `crew rail` has no row for it

### Requirement: A started bolt waits to land on its kit's row
A started bolt SHALL wait to land on its kit's landings row on the same terms as any bolt, every unit and chore merged and sluice green at its head, its pieces' stages read from the runner's records; its line SHALL name the host its work runs on, as the runner that took it reported, and no team or slot.

#### Scenario: A started bolt proven
- **WHEN** started `x` has `a`, `b` and `c` merged by the runner's records, deneb's runner having taken them, and sluice green at its head
- **THEN** the rail shows crew's landings row with `x`, on deneb, can land

### Requirement: A bolt carrying another bolt's work is held on its land line
A bolt whose kit's read says it carries another bolt's work that main lacks SHALL NOT be able to land on its kit's land row. Its line SHALL say it is held, naming each bolt whose work it carries and that bolt's landings, and that it lands once main holds that work. Once the kit's read finds nothing carried, the line SHALL say it can land.

#### Scenario: A bolt carrying another bolt's work
- **WHEN** bolt `apex-zones` reads proven and the kit's read says it carries bolt `tenant-environments`'s landing `f5e67f35`
- **THEN** its line says "held: carries bolt tenant-environments's work, its landing f5e67f3, which main lacks", and it is none of the bolts that can land

#### Scenario: Main holds the carried work
- **WHEN** the kit's read says `apex-zones` carries nothing
- **THEN** its line says it can land

### Requirement: A row whose card the user answered says whose act it waits on
When the run record holds the user's answer on a row's open card, the row's card line SHALL say the card was answered, when, what was answered in crew's words, and the act it now waits on, never that it is open and asked: for a kit's landings card, the runner's landing of what the user ticked, which crew's raise asks of it; for any other card, the act of the row's owner.

#### Scenario: A landings card the user sent
- **WHEN** `land/sluice`'s card `req_e9` is open and the run record holds the user's answer on it at 22:01, ticking `a` and `b`
- **THEN** the land row's card line says `land/sluice` was answered at 22:01, ticking `a` and `b`, and waits on the runner to land them, and does not say `open, asked by`

#### Scenario: A proposal's card approved on the phone
- **WHEN** `proposal/57`'s card is open and the run record holds the user's answer on it, approved
- **THEN** the proposal row's card line says it was answered, approved, and waits on the planner to apply it

#### Scenario: A batch's card tapped
- **WHEN** `batch/12`'s card is open and the run record holds the user's answer on it
- **THEN** the batch row's card line says it was answered and waits on the planner to hand on its notes

#### Scenario: A deploy whose word stands
- **WHEN** `deploy/srv`'s card is answered and ops has recorded the word, which stands
- **THEN** the operations row's card line says the user's word stands and the deploy's end closes the card

#### Scenario: A card not yet answered
- **WHEN** `proposal/57`'s card is open and the run record holds no answer on it
- **THEN** its card line names it open, asked by the planner, with its id, as before

### Requirement: An answered question or record card no longer waits on the user
An open question or decision record card whose answer the run record holds SHALL NOT be listed among the questions or records waiting on the user. It SHALL be listed apart, under answered cards waiting on their askers, with its key, its asker, when it was answered and what was answered.

#### Scenario: A question answered
- **WHEN** agentplot-design's question `ask/agentplot-design/sluice-who-claims` is open and the run record holds the user's answer on it
- **THEN** the rail lists it under the answered cards waiting on their askers, naming agentplot-design and when it was answered, and not under the questions waiting on the user

#### Scenario: A record card answered
- **WHEN** `record/weir/0004`'s card is open and the run record holds the user's answer on it, approved
- **THEN** the rail lists it under the answered cards waiting on their askers, naming agentplot-design, and not under the decision records waiting on the user

### Requirement: Each bolt's land line says whether its card carries, holds or follows it
Each bolt line on a kit's land row SHALL end what it waits on with how the kit's card stands for it: carried, when the open card waiting on the user shows it as a row; held, when the user's send stands for it at its head now; or following, when it can land and neither holds. A bolt that can't land and is no row of the card SHALL say nothing of the card.

#### Scenario: A bolt the open card carries
- **WHEN** `land/crew`'s card waits on the user and its last post shows `b` at its head now
- **THEN** `b`'s line says `land/crew` carries it, waiting on the user

#### Scenario: A bolt the card shows at an older head
- **WHEN** `land/crew`'s card waits on the user and shows `b` at `1111111`, and `b`'s head is now `2222222`
- **THEN** `b`'s line says `land/crew` carries it at `1111111`, its head now `2222222`

#### Scenario: A bolt the user's send holds
- **WHEN** the user answered `land/crew`'s card ticking `b` at its head now, and no land of `b` is posted yet
- **THEN** `b`'s line says the user's send on `land/crew` holds it and crew asks the runner to land it on that send

#### Scenario: A send kept on a closed card
- **WHEN** `land/crew`'s answered card closed keeping the user's send for `b`, held taking main in, and `b` reads proven again at a head whose own work is the same
- **THEN** `b`'s line says the user's send holds it

#### Scenario: A bolt proven since the send
- **WHEN** the user answered `land/crew`'s card ticking `b`, and `c` reads proven since, on no row of that card
- **THEN** `c`'s line says it follows: the card after `land/crew`'s answered one carries it

#### Scenario: A bolt no card carries yet
- **WHEN** `b` can land and no card is open under `land/crew`
- **THEN** `b`'s line says it follows: the next card under `land/crew` carries it

#### Scenario: A bolt waiting on its verification
- **WHEN** `b`'s line says it lands once its verification is green, and no card shows it
- **THEN** `b`'s line says nothing of the card

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

### Requirement: A bolt that can land says how it lands
Once a bolt can land, its line on its kit's row under land SHALL say how it lands: on proof, with its land and request once posted; on the user's send of `land/<kit>`'s card, for a bolt marked to stay, left by the user, or whose last land at its head was stopped, saying which and, for a stop, what stopped it in the runner's or Flume's words; or once the hold on its drive or kit is lifted, naming the hold and its words. It SHALL carry no command for main-level ops.

#### Scenario: The last unit merges
- **WHEN** the last unit of crew's bolt `b`, not marked to stay, merges into `bolt/b` through sluice, every unit's change has been in a batch the user has answered, and the runner carries that unit's place landed at `bolt/b`'s head
- **THEN** crew's row under land names `b` and `swancloud-ops`, saying `b` lands on proof, crew asking the runner to land it in swancloud-ops's name, and carries no `crew tell`

#### Scenario: Its land posted
- **WHEN** crew posted `b`'s land on proof as request 57, which the runner has not answered
- **THEN** `b`'s line says its land on proof is asked, request 57

#### Scenario: Marked to stay
- **WHEN** crew's bolt `b`, marked to stay, can land
- **THEN** `b`'s line says it stays, and lands on the user's send of `land/crew`

#### Scenario: A stopped landing
- **WHEN** the runner answered `b`'s land on proof at its head refused, a place on `bolt/b` being live
- **THEN** `b`'s line says it can land, that its last landing at that head was stopped, in the runner's words, nothing of the bolt's, and that it lands on the user's send of `land/crew`

#### Scenario: Under a hold
- **WHEN** the user put a hold on the drive swancloud, saying "Cutover", and `b` can land
- **THEN** `b`'s line says the hold on swancloud holds it, "Cutover", and that it lands once the hold is lifted

### Requirement: A bolt started before bolts were base places lands under the crew that started it
A bolt started before bolts were base places SHALL say it lands under the crew that started it, and SHALL be none of the bolts that can land.

#### Scenario: A bolt started before bolts were base places
- **WHEN** started bolt `b` has no launch of `bolt/b` in `requests.rec`, and reads proven
- **THEN** `b`'s line says it was started before bolts were base places and lands under the crew that started it, and `b` is none of the bolts that can land

### Requirement: A kit's row under land holds the bolts its card tells
A kit's row under land SHALL be raised while a bolt of the kit that landed on proof is still to be told on its landings card, as rail-cards "A bolt that landed on proof is told on its kit's landings card" has it, its line naming each such bolt with the commit its kit's main holds after it, until the user answers or taps a card that told it.

#### Scenario: Landed overnight
- **WHEN** `y` and `w` of crew landed on proof overnight, crew's main holding `9f1c2ab` after `y` and `4d5e6f7` after `w`, and no bolt of crew waits to land
- **THEN** crew's row under land names `y` at `9f1c2ab` and `w` at `4d5e6f7` as landed on proof, told on `land/crew`, and `crew rail` and the rail tab draw each on a line of its own, after the line of each bolt of crew that waits to land

#### Scenario: Tapped
- **WHEN** the user taps the notice telling `y` and `w`, and no bolt of crew waits to land
- **THEN** the rail has no row for crew under land
