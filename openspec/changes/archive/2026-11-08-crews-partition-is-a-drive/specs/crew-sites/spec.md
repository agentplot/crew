## MODIFIED Requirements

### Requirement: Sites are listed by bolt, with no server for a started bolt's work
`crew sites [<label>] [--json]` SHALL list, for each of the drive's hosts, its main level's and each its runners answer on, each bolt in flight there, as the runner that took its work reported. A started bolt SHALL be listed with no place and no dev server, saying its work runs in Flume's places, whose servers crew does not show yet, until the runner reports a place's addresses. A host that does not answer SHALL be named, with its bolts from the plan.

#### Scenario: A started bolt's work shows no server
- **WHEN** `an-installs-apex-is-its-own-zone` is a unit of started bolt `apex-zones`, and `devurl-serve` runs in a worktree of its kit on the box
- **THEN** `crew sites wldn` lists `apex-zones` under the box saying its work runs in Flume's places, whose servers crew does not show yet, with no URL

#### Scenario: A host that does not answer
- **WHEN** the box does not answer
- **THEN** `crew sites wldn` names the box as not answering, with `apex-zones` from the plan, and lists every other host's bolts
