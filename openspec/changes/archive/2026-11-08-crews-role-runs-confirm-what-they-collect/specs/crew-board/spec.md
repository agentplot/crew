## MODIFIED Requirements

### Requirement: A role that runs as its kind has its view
Each role its partition runs as its kind SHALL have a view among the agents' views under its run's name, `<label>-<role>`, drawn above its run's prompt by crew's mod where crew's plugin loads: what its turn took, each ask and waiting place on a line of its own and the ends Flume held for the role counted on its head line, never listed, and how many asks wait for the role and since when.

#### Scenario: A run with an ask waiting
- **WHEN** madswan's planner run took two asks and a third has waited four minutes
- **THEN** madswan-planner's view shows the two it took and one waiting for four minutes

#### Scenario: Nothing waiting
- **WHEN** madswan's planner run took one ask and nothing else waits
- **THEN** madswan-planner's view shows the one it took and says nothing waits

#### Scenario: Ends counted
- **WHEN** madswan's planner run took one ask and nine ends of three places
- **THEN** madswan-planner's head line says its turn took one and nine ends, and its view has one line for the ask and none for an end
