## ADDED Requirements

### Requirement: A bolt's verification is its work's landing at its head, as the runner reports it
A bolt's verification SHALL be green when its head, read where the bolt lives, is the commit at which one of its units, chores or fixes reads merged or landed, as the runner reports it or as record 0062's stopgap reads it; none when the head is no such commit; and unknown with no head to read. Its words SHALL name the head and the work. crew SHALL read no `Sluice-Result` trailer and run no sluice command for it.

#### Scenario: A bolt after its last unit's landing
- **WHEN** the runner carries unit `a`'s place on `bolt/b` landed at `e25fea4`, and `bolt/b`'s head is `e25fea4`
- **THEN** `crew bolts` shows the bolt's verification green, naming `e25fea4` and `a`

#### Scenario: A landing read from the bolt's own landings
- **WHEN** unit `a`'s place was tidied before the runner carried its landing, and the landing commit at `bolt/b`'s head names `a`'s branch in its `Sluice-From`
- **THEN** the bolt's verification is green, naming the head and `a`

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
- **WHEN** a kit holding `bolt/b`, whose head is a landing beside the queue, is gathered, with a `sluice` on the path that records every call
- **THEN** the gather runs no `sluice` command, and its answer carries no `verdict` and no `beside` for `b`

## REMOVED Requirements

### Requirement: A bolt's verification is sluice's verdict on its last landing
**Reason**: crew reads no record of sluice's, and nothing that the runner's report does not carry (record 0056 points 1 and 4). The `Sluice-Result` trailer at a bolt's head is sluice's record of its landing. The runner's report already says the same thing: it carries the landing of each piece of the bolt's work, at its commit.
**Migration**: A bolt's verification is read from the runner's report (requirement "A bolt's verification is its work's landing at its head, as the runner reports it"). A bolt whose head is a piece's landing reads green as before. A head that is no landing of its work reads none, as a head that was no landing of sluice's read before.

### Requirement: A landing beside reads as the verdict that covers it
**Reason**: The covering verdict was read from sluice's record of the submission, with `sluice status <n> --json`. That is a sluice command, and a record of sluice's that the runner's report does not carry (record 0056 points 1 and 4).
**Migration**: A landing beside the queue that lands a piece of the bolt's work reads green, as any landing of its work does. sluice lands a submission beside its queue only when no check its policy requires reads the submission's changes (sluice clause 140), so the kit's checks stand passed at that head.
