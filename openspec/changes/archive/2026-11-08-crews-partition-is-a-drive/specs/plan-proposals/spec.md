## MODIFIED Requirements

### Requirement: The planner changes the plan only by a proposal
A command that would write the plan, run by a drive's planner, SHALL be refused with a message naming `crew plan propose`. The planner SHALL change the plan only by writing a proposal, which changes nothing until it is approved.

#### Scenario: The planner adds a unit directly
- **WHEN** `wldn-planner` runs `crew unit add <unit> "<intent>" --repo switchboard-kit`
- **THEN** it is refused, the plan is unchanged, and the message names `crew plan propose`

#### Scenario: The planner creates a bolt directly
- **WHEN** `wldn-planner` runs `crew bolt new <bolt> "<goal>" --repo switchboard-kit`
- **THEN** it is refused in the same way

### Requirement: A proposal is a case and the commands it would run
`crew plan propose <file>` SHALL write one Proposal record to `proposals.rec` on the drive's branch: its number, the planner's case, the plan commands it would run in order, who wrote it and when, and its state, `open`. The commands SHALL be among `bolt new`, `bolt order`, `bolt drop`, `unit add`, `unit amend`, `unit move`, `unit split`, `unit order`, `unit after`, `unit drop`, `chore add`, `chore move`, `chore order`, `chore after` and `chore drop`. A number SHALL be given once and never reused, and a proposal SHALL never be removed or its commands changed.

#### Scenario: A new bolt with two units
- **WHEN** the planner proposes `bolt new cfn-checks …`, `unit add cfn-nag-security-check … --bolt cfn-checks` and `unit move retire-suite-cfn-lint cfn-checks`, with its case
- **THEN** proposal N holds the case and those three commands in that order, in state `open`, and the plan is unchanged

#### Scenario: A command a proposal cannot hold
- **WHEN** a proposal file holds `bolt give swb-1`
- **THEN** the proposal is refused, naming the command, and nothing is written

#### Scenario: Someone other than the planner
- **WHEN** a conductor runs `crew plan propose`
- **THEN** it is refused; only the drive's planner and the user write proposals

#### Scenario: An amendment to a unit in flight
- **WHEN** the planner proposes `unit amend <unit> "<new intent>"` for a unit in code in a bolt a team holds
- **THEN** the proposal is written, the unit's intent is unchanged, and that bolt's conductor is told

#### Scenario: A chore's words changed
- **WHEN** the planner proposes `chore drop bump-biome "…"` then `chore add bump-biome "<new words>" --bolt tooling`
- **THEN** the proposal is written; a chore has no amendment, so its words change by a drop and an add
