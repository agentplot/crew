## MODIFIED Requirements

### Requirement: The state is written only through crew, one commit a write
Every write to a drive's branch SHALL be made by a crew command. It SHALL fetch the branch over https into crew's own bare cache, apply itself to the tip, check each file it changed, commit without touching any working tree, and push without force. A push rejected because the branch moved SHALL have the write applied again to the new tip, up to six times, after a growing wait before each replay's fetch, 23.5 seconds in all at most. A write that changes several files SHALL be one commit.

#### Scenario: Two hosts write at once
- **WHEN** a write from the box and a write from mac-studio reach the same drive's branch together
- **THEN** both land, one after the other, and nothing is merged

#### Scenario: Each replay waits longer
- **WHEN** a write's push is refused for the nth time and a replay follows
- **THEN** it waits between half and all of the nth of 0.5, 1, 2, 4, 8 and 8 seconds, drawn afresh, before it fetches the branch again, so writers refused at one moment replay apart

#### Scenario: A busy branch is outwaited
- **WHEN** another writer moves the branch before each of a write's first three pushes
- **THEN** the write waits before each fresh fetch, each wait longer than the one before, and lands on its fourth push on top of the other writer's last commit

#### Scenario: A branch that will not take the write
- **WHEN** the branch moves before every one of a write's pushes
- **THEN** the write is applied seven times, waits before each fresh fetch but the last, no more than 23.5 seconds in all, and is refused saying the branch kept moving, how many times the write was applied and how long it waited

#### Scenario: A write of two files
- **WHEN** a command changes the plan and appends a move
- **THEN** one commit holds both, and no reader sees the plan change without the move

#### Scenario: A file that fails its check
- **WHEN** a write would leave a recutils file that fails `recfix --check` or crew's rules
- **THEN** nothing is pushed, and the command says which file and why
