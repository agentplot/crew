## ADDED Requirements

### Requirement: Every merge into a bolt or onto main lands only through sluice, never by crew's git
Every merge into a bolt, every landing on main, and every commit that reaches a kit's main, the user's and the design agent's among them, SHALL be a submission to sluice from a branch, landed as a merge commit only when the checks the kit's policy requires of the target pass with it merged, and otherwise landing nothing.
Nothing of crew's SHALL move a bolt's branch or main by git, or run a merge gate or verification of its own.

#### Scenario: A red check refuses a unit's merge
- **WHEN** a unit's place holds a change under which a required check fails, and its merge stage runs `sluice submit bolt/<bolt> --no-wait --json`
- **THEN** its agent's `sluice wait` exits 1 naming the check, and `bolt/<bolt>` is at the commit it was at before

#### Scenario: A green submission lands
- **WHEN** every required check passes on the bolt with the unit merged
- **THEN** `bolt/<bolt>` is a merge commit sluice made, holding the unit's commits

#### Scenario: The design agent's record
- **WHEN** the design agent writes a decision record for a kit
- **THEN** it commits the record on a branch in a worktree of its own, submits it with `sluice submit main --no-wait --json` and waits on it with `sluice wait`, and the kit's main holds it only once sluice lands it, when the agent removes the worktree and its branch

#### Scenario: A submission is never read from a listing
- **WHEN** an agent waits on its submission to a kit's main or a bolt
- **THEN** it reads the outcome from `sluice wait`'s exit and record, never from `sluice status <branch>`'s listing, which a decided submission leaves

### Requirement: A bolt's landing on main is the runner's submission through Flume, and crew submits nothing for it
A bolt's landing on main SHALL be the runner's submission of the bolt's base place through Flume, `sluice submit main --head bolt/<bolt>`, and a fix of main's the runner's submission of the fix's place, each on the land crew posts for the user's send (record 0056 points 3 and 5); crew SHALL submit nothing to sluice for either, and run no sluice, `wt` or `gh` command for a landing.

#### Scenario: A landing is gated the same way
- **WHEN** crew has posted the land of bolt `b` on the user's send, and the runner reports `b`'s base place refused, a required check of main failing on main with the bolt merged
- **THEN** nothing lands, main is at the commit it was at before, and crew reads `b`'s landing refused in Flume's words

#### Scenario: crew submits nothing for a landing
- **WHEN** a bolt runs on the stubs from its start to its close, its land posted on the user's send and its base place reported landed by the runner
- **THEN** the stubs' log holds no `sluice`, `wt` or `gh` call, and no scratch kit's `HEAD`, index or refs moved but its remotes'

## REMOVED Requirements

### Requirement: Every merge into a bolt or onto main is a submission sluice gates
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "Every merge into a bolt or onto main lands only through sluice, never by crew's git" and "A bolt's landing on main is the runner's submission through Flume, and crew submits nothing for it".
