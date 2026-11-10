## ADDED Requirements

### Requirement: Main status says a standing role is standing
`crew main status <label>` SHALL say `standing`, the word its drive's `runs` names it by, of each standing main-level role it lists, beside its agent's pane, session and status, `not up` where none runs.

#### Scenario: A standing role
- **WHEN** wldn's `runs` names its design agent `standing`, its agent is idle, and `crew main status wldn` runs
- **THEN** the design agent's line gives its pane and session and says `standing` and `idle`

## MODIFIED Requirements

### Requirement: A role that runs as its kind is not started by crew-role
`crew-role <label> <role>`, fresh or with `resume`, SHALL refuse a role its drive runs as its kind, naming `crew role open <role> --label <label>`, and start no Claude. `crew main status <label>` SHALL say of each such role that it is `on-demand`, the word its drive's `runs` names it by, and never that it runs as its kind; whether the runner's records show a run of it standing; and how many asks wait for it since when, naming as its stream the drive's label.

#### Scenario: The planner started by hand
- **WHEN** madswan's planner runs as its kind and `crew-role madswan planner` runs
- **THEN** it refuses, saying madswan's planner runs as its kind and is opened with `crew role open planner --label madswan`, and no Claude starts

#### Scenario: Main status
- **WHEN** madswan's `runs` names the planner `on-demand`, two asks of it wait and no run of it stands, and `crew main status madswan` runs
- **THEN** it says the planner is `on-demand` in stream `madswan`, that no run stands, and that two asks wait, with the oldest's age, and not that it runs as its kind
