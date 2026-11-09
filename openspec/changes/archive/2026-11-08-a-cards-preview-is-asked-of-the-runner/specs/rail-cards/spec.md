## MODIFIED Requirements

### Requirement: The landing card is posted once the bolt's verification is green
crew SHALL keep one landings card for each kit with a proven bolt waiting on its main, keyed `land/<kit>`, in the name of the partition's main-level ops, posted on the partition's main host. A bolt SHALL be a row that can land once every unit and chore of it has merged, every unit's latest change has been in a batch whose card the user has answered, its verification is green, its head the landing of its work as the runner reports it (merge-gate "A bolt's verification is its work's landing at its head, as the runner reports it"), and no fix of it is in flight. Rows SHALL be in the plan's order. The card SHALL ask only for the landing.

#### Scenario: A green bolt
- **WHEN** every unit and chore of bolt `y` of crew has merged, each unit's latest change has been in a batch the user has answered, `y`'s head `abc1234` is the landing of its last unit as the runner reports it, and no other bolt of crew can land
- **THEN** one card keyed `land/crew` is open in swancloud-ops's name, an approve of risk high, naming `y`, its units and chores and `abc1234` green

#### Scenario: Sluice's pull request
- **WHEN** sluice's submission at `y`'s head has pull request #23 on the kit's GitHub
- **THEN** `y`'s row links it, titled as sluice's pull request for `y`'s landing, on the card's face and in its details

#### Scenario: No pull request
- **WHEN** the kit's sluice opens no pull request for a submission
- **THEN** the row carries no link, and says nothing of one

#### Scenario: Two green bolts of one kit
- **WHEN** bolts `y` and `z` of crew both read proven, `y` first in the plan
- **THEN** one card keyed `land/crew` is open in swancloud-ops's name, its rows `y` then `z`, and no card is open under `land/y` or `land/z`

#### Scenario: Bolts of two kits
- **WHEN** bolt `y` of crew and bolt `w` of swancloud both read proven
- **THEN** `land/crew` holds `y`, `land/swancloud` holds `w`, and each is its own card

#### Scenario: A row carries what the bolt's card carried
- **WHEN** bolt `y` of swc-1, holding units `a` and `b` read in batch 7 and chore `c`, reads proven at `abc1234`, the landing of its work there made at 10:02, with pull request #23, main moved two landings since `y` was cut
- **THEN** `y`'s row names swc-1-conductor, `a`, `b` and `c (chore)`, batch 7, `abc1234` green since 10:02, two landings, pull request #23 linked, and `y`'s reading's link

#### Scenario: A second bolt is proven while the card waits
- **WHEN** `land/crew` waits on the user with one row, `y`, and bolt `z` of crew reads proven
- **THEN** the card becomes a list of `y` and `z`, posted following the one it replaces since a card's kind does not change in place, with a change note naming `z`

#### Scenario: A row's head moves while the card waits
- **WHEN** `land/crew` waits on the user as a list of `y` and `z`, and a fix's merge moves `z`'s head to `def5678`
- **THEN** the card is changed in place, its note saying `z`'s head is now `def5678`, and `z`'s row carries its reading of `def5678` and `bolt/z` at `def5678` as what brings its preview up

#### Scenario: A yes frees the team for its next bolt
- **WHEN** swc-1's bolt `y` is a row of `land/crew`, and the last unit of swc-1's other bolt `z` merges with sluice green at its head, and `d` is the next planned bolt of swc-1's kit
- **THEN** `y`'s row says a yes frees swc-1 for `d`

#### Scenario: A fix in flight holds the card
- **WHEN** bolt `y` would read proven, but `fix/y/gap`, started on `y`, has neither merged nor been dropped
- **THEN** `y` has no box on `land/crew`, its row on the card's face says it is held for `fix/y/gap`, and it has a box again once the fix has merged and `y` reads proven

#### Scenario: A landing row before the bolt reads proven
- **WHEN** every unit of bolt `y` has merged and one unit's latest change has not been in a batch
- **THEN** the rail's landing row for crew names `y`, saying it lands once that unit has been in a batch, and `y` is no row of `land/crew`

#### Scenario: A landing row while a batch card waits on the user
- **WHEN** every unit of bolt `y` has merged, its verification is green, and batch 7, whose card the user has not answered, holds a unit's latest change
- **THEN** the rail's landing row for crew names `y`, saying it lands once you have answered batch 7, and `y` is no row of `land/crew` until the user has answered batch 7's card

#### Scenario: A defect noted on the card
- **WHEN** the user sends `land/crew` with a note naming a defect in `y`, and `y`'s conductor runs `crew fix` on `y` in the note's words
- **THEN** `y` loses its box and its row says "held for a fix: <the note>", and it has a box again once `y` reads proven again

### Requirement: A preview that fails is said on the card and holds nothing
A preview the runner refuses, in its own words or in sluice's as it carried them, or one crew cannot ask for or cannot read in the runner's report, SHALL be said on its row or line with that reason, the card changed in place while it waits on the user. A preview the runner has not answered yet, or has answered held, SHALL be said as asked and not there yet, naming the host whose runner brings it up. A preview whose addresses were listed and that sluice's listing, as the runner carried it, then shows failed SHALL change the card in place to say it did not come up, its addresses no longer listed; one sluice no longer lists SHALL change the card in place to say so; one that comes up after the card said it was not there yet SHALL change the card in place to list its addresses. A card the user has answered SHALL be left as it is. None of this SHALL hold the landing.

#### Scenario: The runner refuses the preview
- **WHEN** swancloud-ops has run `crew card preview land/crew y`, writing request 12, and deneb's runner, where `y`'s work runs, answers request 12 refused with the words `its Act preview, which crew's implementation does not read`
- **THEN** at the rail's next read on the partition's main machine `land/crew` is changed in place, `y`'s row saying its preview could not be brought up, in the runner's words, listing no addresses, and `y` keeps its box

#### Scenario: The host's sluice has no preview command
- **WHEN** deneb's runner runs a sluice that refuses `sluice preview`, and answers request 12 refused, carrying sluice's words
- **THEN** `land/crew` is changed in place, `y`'s row saying its preview could not be brought up, in sluice's words, listing no addresses, and `y` keeps its box

#### Scenario: A kit that declares no preview
- **WHEN** deneb's runner answers request 12 refused with sluice's words that the kit's policy at `y`'s head declares no preview
- **THEN** `y`'s row says its preview could not be brought up, in sluice's words, and `y` keeps its box

#### Scenario: A line naming a branch sluice does not land
- **WHEN** the planner has run `crew card preview batch/7 a/demo` for a line naming `unit/a` at `abc1234`, and the runner answers it refused with sluice's words that no `[branches]` table names `unit/a`
- **THEN** batch 7's card is changed in place, saying under `a` that `demo` could not be brought up, in sluice's words

#### Scenario: Not answered yet
- **WHEN** request 12 is written and deneb's runner has not answered it
- **THEN** `y`'s row says its preview of `abc1234` is asked of the runner on deneb and is not there yet, and that nothing waits on it

#### Scenario: The stack fails to come up
- **WHEN** `y`'s row lists a preview's addresses and deneb's runner then carries sluice's listing of it as failed
- **THEN** the card is changed in place with a note that `y`'s preview did not come up, the row says so and lists no addresses, and `y` keeps its box

#### Scenario: The host is busy when the card is raised
- **WHEN** deneb's runner answers request 12 held, and at a later pass answers it done with sluice's listing of it up
- **THEN** the row says its preview waits for room on deneb, and the card is then changed in place with a note that `y`'s preview is up, listing its addresses

#### Scenario: A preview sluice no longer lists
- **WHEN** `y`'s row lists a preview's addresses and deneb's runner then carries it as no longer listed by sluice
- **THEN** the card is changed in place with a note that `y`'s preview is gone, the row saying sluice on deneb no longer lists it and listing no addresses

### Requirement: A landing row carries what brings its bolt's preview up
Each bolt's row on its kit's landings card that can land SHALL carry what brings a preview of its head up, the bolt's branch and its head, and SHALL say that the preview comes up only when the user asks for it on the card and goes when they are done. crew SHALL read no file of the kit's to tell whether the kit declares a preview: a kit that declares none answers in sluice's words when the preview is asked for. crew SHALL write no request when it posts or changes the row.

#### Scenario: A kit that declares a preview
- **WHEN** bolt `y` reads proven at head `abc1234` in a kit whose policy at `abc1234` declares `[preview]`
- **THEN** `y`'s row on `land/crew` names `bolt/y` at `abc1234` as what brings its preview up and says to write on the card to bring it up, `requests.rec` gains no request, and crew reads no `.config/sluice.toml` for it

#### Scenario: A kit that declares none
- **WHEN** bolt `y` reads proven in a kit whose policy at its head has no `[preview]` table
- **THEN** `y`'s row carries what brings its preview up as any row does, nothing is asked until the user asks for it, and the runner's answer then says, in sluice's words, that there is none

#### Scenario: The policy can't be read
- **WHEN** the kit's policy at `y`'s head can't be read on the host where `y`'s work runs
- **THEN** `y`'s row carries what brings its preview up as any row does, since crew reads no policy for it, and `y` keeps its box

#### Scenario: Approved without a preview
- **WHEN** the user sends `land/crew` with `y` ticked and never asked for its preview
- **THEN** main-level ops lands `y` as for any ticked row, and `requests.rec` holds no preview of `y`

### Requirement: The user asks for a preview by writing on the card
A card that carries a thing that must run SHALL say, in its words, that the user brings it up by writing on the card naming it, and puts it away by writing that they are done. The card's owner, woken by the user's words, SHALL run `crew card preview <key> <thing>` to ask for it and `crew card preview <key> <thing> --done` to put it away, `<thing>` a landings row's bolt or a batch line's `<unit>/<name>`. No card SHALL ask the user to run a command.

#### Scenario: The user asks on the landings card
- **WHEN** the user writes "bring up y's preview" on `land/crew` while it waits on them
- **THEN** swancloud-ops is woken, runs `crew card preview land/crew y`, and the card stays open waiting on the user's send

#### Scenario: A thing the card does not carry
- **WHEN** `crew card preview land/crew w` is run and `w` is no row of `land/crew`
- **THEN** crew refuses, naming the rows that carry a preview, and writes no request

#### Scenario: Asked by anyone but the owner
- **WHEN** a conductor runs `crew card preview land/crew y`
- **THEN** crew refuses, naming swancloud-ops as the card's owner, and writes no request

### Requirement: A preview asked for from a card is asked of the runner and listed while it is up
`crew card preview` SHALL ask for the thing's preview by one request on the drive's branch: a `preview` naming the host whose runner reported the thing's work, the work it serves, its repository as the plan names it, and the branch and revision the row or line names (drive-state "A preview names its host, its work, its repository, its branch and its revision"). It SHALL answer once the request is written, and change the card in place saying the preview is asked of that host's runner. crew SHALL run no sluice command and read no file of sluice's for it. Once the runner reports the preview brought up, crew SHALL list on the card, while sluice lists it waiting, starting or up as the runner carried that listing, each address sluice named, under the name sluice gave it. Asked again while crew's ask of that revision on that host stands, and the runner has neither refused it nor carried it failed or no longer listed, crew SHALL write no second request and give back what the runner reports.

#### Scenario: Asked
- **WHEN** swancloud-ops runs `crew card preview land/crew y` with `y`'s row at `abc1234`, and deneb's runner took `y`'s work
- **THEN** `requests.rec` gains one request saying `Act: preview`, `Host: deneb`, `Work: bolt/y`, `Repo: crew`, `Branch: bolt/y` and `Revision: abc1234`, with no `Done`; `land/crew` is changed in place, its note saying `y`'s preview of `abc1234` is asked of the runner on deneb; and no sluice command is run

#### Scenario: Brought up
- **WHEN** deneb's runner then answers that request done, with sluice's listing of its preview up at addresses `web` and `api`
- **THEN** at the rail's next read on the partition's main machine `land/crew` is changed in place, its note saying `y`'s preview is up, `y`'s row listing `web` and `api` with sluice's addresses and saying a preview lands nothing

#### Scenario: Asked twice
- **WHEN** `crew card preview land/crew y` is run again while deneb's runner reports `y`'s preview of `abc1234` up
- **THEN** `requests.rec` gains no request, and `y`'s row lists the same addresses

#### Scenario: Asked again after a refusal
- **WHEN** `crew card preview land/crew y` is run again after deneb's runner refused the first request
- **THEN** `requests.rec` gains a second `preview` of `bolt/y` at `abc1234`, and the card says it is asked

### Requirement: A preview is released on the user's done and when its card or row ends
crew SHALL put away a preview it asked for from a card by one request on the drive's branch, the same `preview` marked `Done: yes`: when the owner runs `--done` on the user's word; when the bolt's row is held for a fix, lands, is dropped or otherwise leaves its kit's landings card, at that card's raise; when a batch's card closes, for its lines no other open card carries; and at a rail read on the partition's main machine, for one whose card is closed or whose row is gone, once its ask is two minutes old. The card, while it waits, SHALL say it was put away. crew SHALL put away only a preview it asked for and has not put away, SHALL write no done for one the runner refused, and SHALL run no sluice command for it.

#### Scenario: The user is done
- **WHEN** the user writes "done with y's preview" on `land/crew` and swancloud-ops runs `crew card preview land/crew y --done`
- **THEN** `requests.rec` gains a `preview` naming deneb, `bolt/y`, `crew`, `bolt/y` and `abc1234` with `Done: yes`, and `y`'s row again names `bolt/y` at its head and says to write on the card to bring it up

#### Scenario: Done with none asked
- **WHEN** `crew card preview land/crew y --done` is run and crew's last ask of `y`'s preview at its head was put away already
- **THEN** crew says it asked for no preview of `y` that stands, and writes no request

#### Scenario: The bolt lands with its preview up
- **WHEN** `crew bolt land y` closes `y` while crew's ask of its preview stands
- **THEN** the raise of `land/crew` that follows writes its done, and the close says nothing of a preview

#### Scenario: A fix holds the landing
- **WHEN** a fix started on bolt `y` holds its row while crew's ask of its preview stands
- **THEN** the raise of `land/crew` writes its done, and no preview is asked when `y` reads proven again

#### Scenario: A preview crew did not ask for
- **WHEN** a person brought up a preview of an earlier revision of `bolt/y` themselves, and `y` later lands
- **THEN** crew writes a done only for the revision it asked for, and none for the person's

#### Scenario: A preview the runner refused
- **WHEN** deneb's runner refused crew's ask of `y`'s preview, and `y` lands
- **THEN** no done is written for it

#### Scenario: A card closed elsewhere
- **WHEN** batch 7's card is closed with no crew command closing it while crew's ask of `a/demo`'s preview stands, and no other open card holds `a`, and the rail is read on the partition's main machine more than two minutes after the ask
- **THEN** the rail's read writes its done, and says so

#### Scenario: A row gone with no raise of its card
- **WHEN** `y` leaves the plan by a write that raises no landings card while crew's ask of its preview stands, and the rail is read on the partition's main machine more than two minutes after the ask
- **THEN** the rail's read writes its done, and says so

### Requirement: A moved head releases the preview of the old one and asks for none
When a merge moves a bolt's head while it is a row of its kit's landings card, crew SHALL change the row in place to name the new head as what brings the preview up, SHALL put away, by its done, a preview it asked for at the old head, and SHALL say so on the row; it SHALL ask for no preview at the new head until the user asks again.

#### Scenario: The head moves with a preview up
- **WHEN** a fix's merge moves bolt `y`'s head from `abc1234` to `def5678` while crew's ask of `y`'s preview of `abc1234` stands
- **THEN** the raise of `land/crew` writes the done of `abc1234`'s preview, `y`'s row names `bolt/y` at `def5678` and says its preview of `abc1234` was released as the head moved, and `requests.rec` holds no preview of `def5678`

## ADDED Requirements

### Requirement: A card is changed in place when the runner reports its preview anew
At each rail read on the partition's main machine, a card there that waits on the user and carries a standing ask SHALL be changed in place when the runner's report changes what the card says of that preview, its note naming the thing and what the preview now is. crew SHALL keep on that host what it last told each card of each preview, a cache whose loss costs one more change, and SHALL change no card for a report that changes nothing it says. A card the user has answered SHALL be left as it is.

#### Scenario: The runner reports a preview brought up
- **WHEN** `land/crew` waits on the user saying `y`'s preview is asked, and deneb's runner reports it up
- **THEN** the rail's read changes `land/crew` in place once, its note saying `y`'s preview is up, and the next read, with the report unchanged, changes nothing

#### Scenario: A report that changes nothing the card says
- **WHEN** deneb's runner carries sluice's listing of `y`'s preview again, up at the same addresses, at a later time
- **THEN** the rail's read leaves `land/crew` as it is

#### Scenario: The user answered the card
- **WHEN** the user has sent `land/crew`, and deneb's runner then reports `y`'s preview failed
- **THEN** the rail's read leaves `land/crew` as the user answered it

#### Scenario: What was told is lost
- **WHEN** the main machine's record of what `land/crew` was told of `y`'s preview is gone, and the rail is read
- **THEN** `land/crew` is changed in place once, saying what the runner now reports, and the record is kept again

## RENAMED Requirements

- FROM: `### Requirement: A preview asked for from a card is brought up through sluice and listed while it is up`
- TO: `### Requirement: A preview asked for from a card is asked of the runner and listed while it is up`
