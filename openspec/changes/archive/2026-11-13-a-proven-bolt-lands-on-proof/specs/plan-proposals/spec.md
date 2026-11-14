## MODIFIED Requirements

### Requirement: A proposal holds only commands that change bolts, units and chores
A proposal's commands SHALL be among `bolt new`, `bolt start`, `bolt unstay`, `bolt order`, `bolt drop`, `unit add`, `unit amend`, `unit move`, `unit split`, `unit order`, `unit after`, `unit drop`, `chore add`, `chore move`, `chore order`, `chore after`, `chore drop` and `kit rename`. A proposal SHALL hold no hold of a drive or a kit. Its card SHALL say of each bolt a command of it marks to stay that the bolt stays unlanded until the user's send.

#### Scenario: A command a proposal cannot hold
- **WHEN** a proposal file holds `bolt give swb-1`
- **THEN** the proposal is refused, naming the command, and nothing is written

#### Scenario: A hold in a proposal
- **WHEN** a proposal file holds `plan hold "Cutover" --repo switchboard-kit`
- **THEN** the proposal is refused, naming the command, and nothing is written

#### Scenario: A bolt planned to stay
- **WHEN** the planner proposes `bolt new console-pages "Console pages" --repo switchboard-kit --stays`
- **THEN** the proposal's card names `console-pages` and says it stays unlanded until the user's send

#### Scenario: An amendment to a unit in flight
- **WHEN** the planner proposes `unit amend <unit> "<new intent>"` for a unit in code in a bolt a team holds
- **THEN** the proposal is written, the unit's intent is unchanged, and that bolt's conductor is told

#### Scenario: A chore's words changed
- **WHEN** the planner proposes `chore drop bump-biome "…"` then `chore add bump-biome "<new words>" --bolt tooling`
- **THEN** the proposal is written; a chore has no amendment, so its words change by a drop and an add
