## ADDED Requirements

### Requirement: A bolt marked to stay is marked in the bands, and each hold opens them
In the planner's and main-level ops's bands, a started bolt marked to stay SHALL say so on its line, beside its name. While a hold stands on the drive or a kit of it, those bands SHALL open with a line for each hold: the drive or the kit it holds, its words, and that no land is posted until the user lifts it with `crew plan go` (`code.8`).

#### Scenario: A bolt marked to stay
- **WHEN** wldn's started bolt `console-pages` is marked to stay
- **THEN** its line in wldn-planner's and wldn-ops's bands says it stays, beside its name

#### Scenario: A kit held
- **WHEN** the user put a hold on switchboard-kit, saying "Cutover"
- **THEN** wldn-planner's and wldn-ops's bands open with a line naming switchboard-kit, "Cutover", and that no land is posted until the user lifts it with `crew plan go`

#### Scenario: No hold and no mark
- **WHEN** no hold stands on wldn and no bolt of it is marked to stay
- **THEN** the bands draw neither
