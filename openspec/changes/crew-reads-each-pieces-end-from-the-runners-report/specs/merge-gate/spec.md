## MODIFIED Requirements

### Requirement: A bolt's verification is its work's landing at its head, as the runner reports it
A bolt's verification SHALL be green when its head, read where the bolt lives, is the commit at which one of its units, chores or fixes reads merged or landed as the runner reports it, a record Flume holds for the runner after its tidy among them; none when the head is no such commit; and unknown with no head to read. Its words SHALL name the head and the work. crew SHALL read no `Sluice-Result` or `Sluice-From` trailer and run no sluice command for it.

#### Scenario: A bolt after its last unit's landing
- **WHEN** the runner carries unit `a`'s place on `bolt/b` landed at `e25fea4`, and `bolt/b`'s head is `e25fea4`
- **THEN** `crew bolts` shows the bolt's verification green, naming `e25fea4` and `a`

#### Scenario: A landing held for the runner
- **WHEN** Flume landed unit `a`'s place on `bolt/b` at its head and tidied it, holding its record for the runner, and the runner carries that record as `a`'s status, tidied and landed at the head
- **THEN** the bolt's verification is green, naming the head and `a`, as the runner reports it

#### Scenario: A landing read from the bolt's own landings
- **WHEN** unit `a`'s place was tidied before the runner carried its end, the runner last carrying it at submitted, and the landing commit at `bolt/b`'s head names `a`'s branch in its `Sluice-From`
- **THEN** crew reads no such landing: the bolt's verification reads none, and the bolt is not offered for landing

#### Scenario: A take-main fix landed beside the queue
- **WHEN** every unit of `bolt/b` has merged, and the runner carries the place of `b`'s take-main fix landed at the bolt's head, which sluice landed beside its queue with nothing run
- **THEN** the bolt's verification is green, naming the fix, and `b` is a row of its kit's landings card that can land

#### Scenario: A head that is no landing of the bolt's work
- **WHEN** `bolt/b`'s head is a commit at which none of its units, chores or fixes reads merged or landed
- **THEN** its verification reads none, saying its head is no landing of its work that the runner reports, and the bolt is not offered for landing

#### Scenario: No head
- **WHEN** crew can't read `bolt/b`'s head where it lives
- **THEN** its verification reads unknown, and the bolt is not offered for landing

#### Scenario: Nothing of sluice's is read
- **WHEN** a kit holding `bolt/b`, whose first-parent line holds sluice's landing commits, each naming a place's branch in its `Sluice-From`, and whose head is a landing beside the queue, is gathered, with a `sluice` on the path that records every call
- **THEN** the gather runs no `sluice` command, and its answer carries no `verdict`, `beside`, `landings`, `landed`, `landings_error` or `landed_error` for `b`
