## MODIFIED Requirements

### Requirement: A bolt's proof is its verification
A bolt SHALL be proven by its verification alone: its head is the landing of its work, as the runner reports it (merge-gate "A bolt's verification is its work's landing at its head, as the runner reports it"). Nobody SHALL deploy the bolt or work a list from its changes to prove it. Ops SHALL prove and deploy nothing. crew SHALL offer the bolt for landing, as its row on its kit's landings card, once every unit and chore of it has merged and its verification is green.

#### Scenario: Ready to land
- **WHEN** every unit of a bolt has merged and `crew bolts` shows its verification green
- **THEN** the bolt is a row of its kit's landings card, in main-level ops's name, and no one is asked to prove it

#### Scenario: Not yet green
- **WHEN** every unit of a bolt has merged and its head is no landing of its work that the runner reports
- **THEN** the bolt is not offered for landing, and `crew bolts` says what its verification is

### Requirement: A submission's number is on its bolt's row from the submit
crew SHALL show each piece's sluice submission and the bolt's landing on the bolt's row in `crew bolts`, text and JSON. It SHALL show them from the first read after the submit, whoever made it:

- **A piece's submission.** While a unit's, chore's or fix's submission stands, its line SHALL show the submission's number, `submitted #<n>`, from Flume's status of the piece's place as the runner carried it (`runner.stage_of`).
- **The bolt's landing.** The bolt's head line SHALL show its landing as the run record holds it: queued as #n, landing again, or rejected (`plan.landing_phase`).

crew SHALL read neither from sluice's queue. It SHALL run no `sluice overview` for a bolt's row. Its JSON SHALL give no line a `submission`, and no bolt a `landing` or a `submissions_error`, read from sluice.

#### Scenario: A unit's merge under test
- **WHEN** the runner carries the place of unit `a` with its submission `#41` under test on `bolt/y`
- **THEN** the next `crew bolts` shows `a`'s line with `submitted #41`, its JSON gives `a`'s stage as `submitted` with submission `41`, and no sluice command is run

#### Scenario: A bolt's landing queued on main
- **WHEN** main-level ops's `crew bolt submit y` has been answered `#355`, and the run record holds the landing queued with no outcome
- **THEN** `crew bolts` shows `y`'s head line saying `landing queued as #355`

#### Scenario: Read again after the session that submitted it ended
- **WHEN** the session in unit `a`'s place has ended, and the runner still carries `a`'s submission `#41` waiting on `bolt/y`
- **THEN** `crew bolts` still shows `a`'s line with `submitted #41`

#### Scenario: Decided
- **WHEN** sluice lands `#41` on `bolt/y`, and the runner carries `a`'s place landed
- **THEN** `a`'s line shows no submission, and reads its stage as merged

#### Scenario: sluice's record can't be read
- **WHEN** `sluice overview --json` would fail on the kit's host, while the runner carries `a`'s submission `#41` waiting on `bolt/y`
- **THEN** `crew bolts` runs no sluice command, shows `a`'s line with `submitted #41`, and says nothing of sluice's queue on the bolt's head line

#### Scenario: A runner that can't be read
- **WHEN** the branch of the runner that took `a`'s launch can't be read
- **THEN** `crew bolts` names that runner as one that can't be read, the stages of its work unknown, no line shows a number, and no sluice command is run
