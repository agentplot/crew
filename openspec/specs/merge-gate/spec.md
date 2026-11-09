# merge-gate Specification

## Purpose
Every merge into a bolt and every landing on main is a submission sluice tests on the checks the kit's policy requires and lands only when they pass; a bolt's verification is its work's landing at its head, as the runner reports it, and crew's own policy requires its whole suite.

## Requirements

### Requirement: Every merge into a bolt or onto main is a submission sluice gates
Every merge into a bolt, every landing on main, and every commit that reaches a kit's main, the user's and the design agent's among them, SHALL be a submission to sluice from a branch, landed as a merge commit only when the checks the kit's policy requires of the target pass with it merged, and otherwise landing nothing. Nothing of crew's SHALL move a bolt's branch or main by git, or run a merge gate or verification of its own.

#### Scenario: A red check refuses a unit's merge
- **WHEN** a unit's place holds a change under which a required check fails, and its merge stage runs `sluice submit bolt/<bolt> --no-wait --json`
- **THEN** its agent's `sluice wait` exits 1 naming the check, and `bolt/<bolt>` is at the commit it was at before

#### Scenario: A green submission lands
- **WHEN** every required check passes on the bolt with the unit merged
- **THEN** `bolt/<bolt>` is a merge commit sluice made, holding the unit's commits

#### Scenario: The design agent's record
- **WHEN** the design agent writes a decision record for a kit
- **THEN** it commits the record on a branch in a worktree of its own, submits it with `sluice submit main --no-wait --json` and waits on it with `sluice wait`, and the kit's main holds it only once sluice lands it, when the agent removes the worktree and its branch

#### Scenario: A landing is gated the same way
- **WHEN** main-level ops runs `crew bolt submit <bolt>` and a required check of main fails on main with the bolt merged
- **THEN** nothing lands, and main is at the commit it was at before

#### Scenario: A submission is never read from a listing
- **WHEN** an agent waits on its submission to a kit's main or a bolt
- **THEN** it reads the outcome from `sluice wait`'s exit and record, never from `sluice status <branch>`'s listing, which a decided submission leaves

### Requirement: crew's own policy gates its bolts and main on its whole suite
crew's `.config/sluice.toml` SHALL require the `check-full` tasks of every `bolt/*` branch and of `main`, run open on the host, and SHALL accept no replayed task for either, so every submission runs every test afresh. The live test SHALL be no task.

#### Scenario: crew's policy
- **WHEN** crew's `.config/sluice.toml` is read
- **THEN** `[branches."bolt/*"]` and `[branches.main]` each require `#check-full` and trust `open` alone, and its executor is `open`

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
