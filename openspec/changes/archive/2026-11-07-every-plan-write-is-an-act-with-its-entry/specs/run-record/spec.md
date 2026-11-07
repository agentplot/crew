## MODIFIED Requirements

### Requirement: Every command that moves work leaves an entry
Every crew command that changes the plan, a signal or its move, a unit's approval or stage, a fix, or an agent's or a team's sessions, and every `crew tell`, SHALL append one entry for each such act to the run record of the partition it acts for, after the act is done. A command that only reads SHALL append nothing. An entry SHALL give its id, the time in UTC, the host crew ran on, who asked, the act, and the objects it acted on.

#### Scenario: A plan write
- **WHEN** the planner adds a unit to the queue
- **THEN** the run record gains one entry whose act is `unit.add`, naming the unit and the queue it went to

#### Scenario: A command that does several things
- **WHEN** `crew bolt give swb-1` writes the plan, restarts the team's conductor and ops, and greets the conductor
- **THEN** the run record gains an entry for the give, one for each restart and one for the greeting

#### Scenario: A command that only reads
- **WHEN** `crew bolts`, `crew status` or `crew sites` runs
- **THEN** no entry is written

#### Scenario: A construct run again on a committed change
- **WHEN** construct runs again on a unit whose change is committed, marking the unit amended at its head, and that construct then delivers
- **THEN** the run record gains a `unit.mark` entry naming the unit, its bolt and the head, which the mark's commit names; the construct's `stage.start` says it marked the unit and names that commit; and clearing the mark is a `unit.unmark` entry naming the unit and the mark, which its own commit names
