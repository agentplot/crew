## RENAMED Requirements

- FROM: `### Requirement: The design agent is the partition's one design role`
- TO: `### Requirement: The design agent is the drive's one design role`


## MODIFIED Requirements

### Requirement: The teams file overrides a role's model or effort
A drive's main level in `teams.json` MAY set `roles.<role>.model` or `roles.<role>.effort` for its design agent, planner, main-level ops, operator or reviewer. crew SHALL start that role there with the override instead of its definition's value. An override naming a role or an effort level that does not exist SHALL be refused with a message naming it.

#### Scenario: One partition's planner
- **WHEN** wldn's drive entry sets `roles.planner.effort` to `max`
- **THEN** wldn's planner starts at max, and madswan's at its definition's xhigh

#### Scenario: A dispatcher's override
- **WHEN** a drive's entry sets `roles.dispatcher.effort`
- **THEN** crew refuses to load the teams file, naming the role it has no definition for

### Requirement: The design agent is the drive's one design role
No role SHALL be called fable. The design agent at the main level SHALL take over what fable did, and SHALL be the drive's one design role.

#### Scenario: The main level's one design role
- **WHEN** `crew main up wldn` runs
- **THEN** `wldn-design` is the one design agent it starts, and nothing named fable starts
