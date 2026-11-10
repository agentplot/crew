## RENAMED Requirements

- FROM: `### Requirement: A bolt's verification is its work's landing at its head, as the runner reports it alone`
- TO: `### Requirement: A bolt's verification is its work's landing, or sluice's passed landing, at its head`

## MODIFIED Requirements

### Requirement: A bolt's verification is its work's landing, or sluice's passed landing, at its head
A bolt's verification SHALL be green when its head, read where the bolt lives, is the commit at which one of its units, chores or fixes reads merged or landed as the runner reports it, or else a landing sluice made on the bolt beyond main whose one `Sluice-Result` reads passed, whoever submitted it; unknown with no head, or with that commit's trailers unread; else none. Its words SHALL name the head and the work or sluice's landing. crew SHALL run no sluice command for it.

#### Scenario: A bolt after its last unit's landing
- **WHEN** the runner carries unit `a`'s place on `bolt/b` landed at `e25fea4`, and `bolt/b`'s head is `e25fea4`
- **THEN** `crew bolts` shows the bolt's verification green, naming `e25fea4` and `a`

#### Scenario: A landing held for the runner
- **WHEN** Flume landed unit `a`'s place on `bolt/b` at its head and tidied it, holding its record for the runner, and the runner carries that record as `a`'s status, tidied and landed at the head
- **THEN** the bolt's verification is green, naming the head and `a`, as the runner reports it

#### Scenario: A passed landing at the head that no piece names
- **WHEN** every unit of `bolt/b` reads merged as the runner reports it, and then a record's fix landed straight onto `bolt/b` as sluice's #70 at `8df8e1d`, its commit naming `Sluice-Result: passed (3 run, 0 replayed)`, so no piece of `b` landed at its head
- **THEN** the bolt's verification is green, naming `8df8e1d` and sluice's landing #70, and `b` is a row of its kit's landings card that can land

#### Scenario: A head only a landing commit names
- **WHEN** unit `a`'s place was tidied before the runner carried its end, the runner last carrying it at submitted, and the landing commit at `bolt/b`'s head names `a`'s branch in its `Sluice-From` and a passed `Sluice-Result`
- **THEN** the bolt's verification is green as sluice's landing, no landing commit makes `a` merged, and the bolt is not offered for landing while `a` reads submitted

#### Scenario: A take-main fix landed beside the queue
- **WHEN** every unit of `bolt/b` has merged, and the runner carries the place of `b`'s take-main fix landed at the bolt's head, which sluice landed beside its queue with nothing run
- **THEN** the bolt's verification is green, naming the fix, and `b` is a row of its kit's landings card that can land

#### Scenario: A head that is no landing of the bolt's work
- **WHEN** `bolt/b`'s head is a commit at which none of its units, chores or fixes reads merged or landed, and the commit names no `Sluice-Result`, or one that does not read passed, or more than one
- **THEN** its verification reads none, saying its head is no landing of its work that the runner reports, and the bolt is not offered for landing

#### Scenario: A head main already holds
- **WHEN** `bolt/b` stands where its kit's main holds it, main's tip itself a landing sluice passed
- **THEN** the head is no landing on the bolt, and its verification reads none

#### Scenario: A head whose trailers can't be read
- **WHEN** no piece of `bolt/b` landed at its head, and git can't list the bolt's own line beyond main or read the head's trailers
- **THEN** its verification reads unknown, naming what could not be read, and the bolt is not offered for landing

#### Scenario: No head
- **WHEN** crew can't read `bolt/b`'s head where it lives
- **THEN** its verification reads unknown, and the bolt is not offered for landing

#### Scenario: Nothing of sluice's is read
- **WHEN** a kit holding `bolt/b`, whose first-parent line holds sluice's landing commits, each naming a place's branch in its `Sluice-From`, and whose head is a landing beside the queue, is gathered, with a `sluice` on the path that records every call
- **THEN** the gather runs no `sluice` command and reads none of sluice's records, its answer for `b` carries the head's `Sluice-Submission` and `Sluice-Result` values, and it carries no `verdict`, `beside`, `landings`, `landed`, `landings_error` or `landed_error` for `b`
