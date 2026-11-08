## ADDED Requirements

### Requirement: A landing sluice sent back is the bolt's fix
A landing sluice sent back for the bolt's own content SHALL be the bolt's fix until a fix moves its head. crew SHALL name what failed from sluice's record, never a check's words, and give the way on: the take-main fix crew launches for a conflict with main, or the `crew fix` ops starts for a failed check. crew SHALL NOT submit it again at that head, but for a conflict only with a submission queued ahead, and a submit there that submitted nothing SHALL leave it the bolt's fix.

#### Scenario: A check fails
- **WHEN** `crew bolt submit z` waits on `#7` and sluice's record has it failed with `tests:logic`, which ran and failed, tested on main at `db8bc25`
- **THEN** the command fails, saying `z` did not land, that a failed check is the bolt's, `#7 failed tests:logic, tested on main at db8bc25`, and that ops starts `crew fix z landing-7 "Mend what sluice sent bolt/z's landing back for: #7 failed tests:logic, tested on main at db8bc25"`, after which the bolt's row asks the user again

#### Scenario: Submitted again at the head sluice sent back
- **WHEN** ops runs `crew bolt submit z` again while `z`'s head is still the one sluice sent back as `#7`
- **THEN** crew reads sluice's record of `#7` on the kit's host and submits nothing, runs no `wt submit` and leaves the pull request a draft, refusing in words that name what failed and the way on, saying it is the bolt's fix, not a stop, and `z` stays held on its row

#### Scenario: A conflict sent back, submitted again at the same head
- **WHEN** sluice sent `z`'s landing back in conflict with main on `README.md`, crew launched its take-main fix, and ops runs `crew bolt submit z` again before that fix has merged
- **THEN** crew submits nothing, saying the conflict is the bolt's and the fix crew launches on reading the refusal takes main into it, so ops starts nothing, and that once that fix has merged, `crew bolt submit z` submits the landing again at its new head

#### Scenario: A conflict only with a submission queued ahead
- **WHEN** sluice sent `z`'s landing back in conflict only with `#12`, queued on main ahead of it, and ops runs `crew bolt submit z` again at the same head
- **THEN** crew submits it as any landing, the bolt having waited that submission out

#### Scenario: A submit that submitted nothing
- **WHEN** `z`'s landing was refused at `977138a` and a later `crew bolt submit z` at `977138a` ends with sluice's driver submitting nothing, recorded stopped with no submission
- **THEN** `z` reads as held for its fix at `977138a`, on its kit's landings card, the rail and `crew bolts`, its landing rejected and open for work, and no reader says it was stopped or that ops submits it again as it is

#### Scenario: The fix moves the head
- **WHEN** a fix on `z` has merged and `z`'s head is no longer the one sluice sent back
- **THEN** `crew bolt submit z` submits it at its new head as any landing, asking sluice's record of `#7` nothing

#### Scenario: sluice's record can't be read
- **WHEN** `crew bolt submit z` finds `z`'s landing refused at its head and `sluice status 7 --json` fails
- **THEN** it submits nothing, saying the words the refusal was recorded with and why the record can't be read, and gives the way on with no fix's words of crew's

#### Scenario: No team is named
- **WHEN** any of the words above are said, on this line where crew runs no team
- **THEN** none names a team or a conductor
