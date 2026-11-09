## ADDED Requirements

### Requirement: A land crew posts is one entry naming its request
Each `land` crew posts on the user's send of a kit's landings card SHALL be recorded as one entry for each row it lands: `bolt.submit` on `bolt/<bolt>` for a bolt's row, and `fix.merge` on `fix/main/<kit>/<name>` for a fix of main's. Each SHALL carry `Outcome: asked`, the card's id as `Card`, the head the send ticked as `Head`, the land's number in `requests.rec` as `Request` (record 0056), and no `Submission`. A land SHALL be recorded once, however often its send is read.

#### Scenario: Two rows sent
- **WHEN** the user's send of `land/crew` ticks `y` at `abc1234` and `z` at `def5678`, and the card's raise posts lands 57 and 58 of their launches
- **THEN** the run record holds a `bolt.submit` on `bolt/y` with `Outcome: asked`, the card's id as `Card`, `Head` `abc1234`'s commit and `Request: 57`, and one on `bolt/z` with `Request: 58`; neither carries a `Submission`

#### Scenario: A fix of main's row sent
- **WHEN** the user's send of `land/tailrace` ticks the fix of main `cargo-lock`, and the raise posts land 61 of its launch
- **THEN** the run record holds a `fix.merge` on `fix/main/tailrace/cargo-lock` with `Outcome: asked`, the card's id as `Card`, the head the send ticked as `Head` and `Request: 61`

#### Scenario: The send read again
- **WHEN** the card's raise runs again on the same send, `y`'s head unchanged and its land 57 not answered
- **THEN** no land is posted and no entry is written

### Requirement: A landing's Submission is the merge queue's entry Flume names
A `bolt.submit` entry's `Submission` SHALL be only the merge queue's entry that Flume's status of the bolt's base place names, as the runner carries it. The outcome of a land, recorded as bolt-teams "A landing is recorded by the first act that reads it in the runner's report" has it, SHALL carry that entry where Flume names one, and none where it names none. crew SHALL write no `Submission` it made or read from anything but Flume's status.

#### Scenario: A landing whose entry Flume names
- **WHEN** the runner carries `y`'s base place over, landed at `9f1c2ab`, its submission entry 412, and crew records `y`'s land landed
- **THEN** that `bolt.submit` on `bolt/y` carries `Submission: 412`

#### Scenario: A land the runner refused
- **WHEN** the runner answered land 57 of `y` refused because a place on `bolt/y` is live, Flume naming no submission, and crew records it stopped
- **THEN** that `bolt.submit` on `bolt/y` carries no `Submission`

### Requirement: The run record's descriptor allows a land's request
The run record's descriptor SHALL allow `Request`. A day's file begun under a descriptor without it SHALL take the field all the same, its entries reaching the branch under the descriptor that allows it. A `bolt.submit` an older crew wrote, queued with sluice's number among them, SHALL be read as it was written.

#### Scenario: A day's file an older crew began
- **WHEN** the host's day file was begun under a descriptor that allows no `Request`, and crew records an asked `bolt.submit` with `Request: 57` in it
- **THEN** `recsel` reads `Request: 57` from the file, and the day's file pushed to the branch carries the descriptor that allows it and passes `recfix --check`

#### Scenario: An entry an older crew wrote
- **WHEN** the run record holds a `bolt.submit` of `x` an older crew wrote, `Outcome: queued` and `Submission: 355`
- **THEN** `crew events` prints it as written, `Submission: 355` among it

### Requirement: A bolt's landing entry records its time by holder from the run record
Every `bolt.land` entry crew writes SHALL record the bolt's age in whole minutes, from its newest `bolt.start`, or an older crew's `bolt.give`, to the entry's own time, as `Age`, and the minutes each holder held, as `Split`, in the order team, kit, team-or-kit, user, hold, nobody, each named with its minutes. The split SHALL be the board's head line's, from the run record alone, summing to `Age`. With no start to read, the entry SHALL carry neither field, and the landing SHALL close.

#### Scenario: A bolt lands
- **WHEN** crew closes the landing of `b`, started 6h 10m before it records `b` landed, with its work holding it 3h 45m, the user 2h 05m, a hold 0 and nobody 20m
- **THEN** its `bolt.land` entry holds `Age: 370` and `Split: team 225, kit 0, team-or-kit 0, user 125, hold 0, nobody 20`

#### Scenario: No record of sluice's is read
- **WHEN** `b`'s landing is recorded, and the runner carried its unit `a`'s submission `#41` under test for seventeen minutes of its age
- **THEN** no sluice process starts and no host is asked, those minutes are placed as the board's head line places them, by no submission, and `Split` sums to `Age`

#### Scenario: The start can't be read
- **WHEN** the run record holds no start of `b` within the days crew reads as `b`'s landing is recorded
- **THEN** the `bolt.land` entry is written without `Age` and `Split`, and the landing is closed

## REMOVED Requirements

### Requirement: A bolt's landing entry records its time by holder
**Reason**: Its split read sluice's record of the bolt's submissions on the kit's host when the entry was written, and its landing was the moment sluice's record decided the bolt's submission. crew reads no record of sluice's and runs no command on a kit's host for a landing (record 0056 points 1 and 4).
**Migration**: The `bolt.land` entry records the same `Age` and `Split`, split as the board's head line splits them, from the run record alone, to the entry's own time (requirement "A bolt's landing entry records its time by holder from the run record"). An entry an older crew wrote stays as it was written.
