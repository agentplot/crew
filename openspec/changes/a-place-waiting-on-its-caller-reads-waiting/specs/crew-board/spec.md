## MODIFIED Requirements

### Requirement: The planner's and ops's bands show what places wait on them for
`board.agent_views` SHALL give the planner's band each launched place that stopped short asking or waits on its caller, past its kind's bound among them whatever stage it last delivered, with its question or Flume's words and the stage it waits to retry or its submission. It SHALL give main-level ops's band each fix of main and each take-main fix in flight with its stage. crew's mod SHALL draw both above the agent's prompt.

#### Scenario: A question in the planner's band
- **WHEN** `a`'s construct stopped short asking "Which partition's rail?"
- **THEN** madswan-planner's view lists `a` with that question, and the mod draws it

#### Scenario: A place past its bound in the planner's band
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place waiting on its caller to retry code past its bound, its verify delivered
- **THEN** madswan-planner's view counts one place waiting on an answer and lists `a` waiting on its caller at code with Flume's words, and the mod draws it

#### Scenario: A fix of main in ops's band
- **WHEN** `main--a-test-reads-its-fixture` is in code
- **THEN** madswan-ops's view lists it at code, and the mod draws it
