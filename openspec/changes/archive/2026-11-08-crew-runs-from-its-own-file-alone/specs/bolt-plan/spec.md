## MODIFIED Requirements

### Requirement: A rename waits until no host keeps the old name
`crew kit rename <old> <new>` SHALL be refused while any host still keeps `<old>`, naming the host and what keeps it. The hosts read SHALL be each host with a runner branch of the drive, and the drive's main-level host. A host's keeping SHALL be its runner's `repositories.rec` where that runner reports one, and otherwise what the teams file keeps there: its `repositories`, where the host is the one the file is written on, and the `repos` of each drive whose machine is the host. A host whose runner reports no repositories, that is not the host the file is written on, and that no drive of the file runs on is one whose keeping crew can't read. Where crew can't read something this depends on, it SHALL be refused naming what it could not read. No host needs to keep `<new>`.

#### Scenario: A host still keeps it
- **WHEN** deneb's runner reports `agentplot/tailrace` among its repositories
- **THEN** the rename is refused naming deneb's runner and `agentplot/tailrace`

#### Scenario: A runner that reports no repositories
- **WHEN** deneb's runner branch holds no `repositories.rec` and a drive whose machine is deneb lists `agentplot/tailrace` in its `repos`
- **THEN** the rename is refused naming deneb's teams file and `agentplot/tailrace`

#### Scenario: What crew can't read
- **WHEN** deneb's runner branch can't be read, or a runner's host reports no repositories, is not the host the rename runs on, and runs no drive of the teams file
- **THEN** the rename is refused naming that host and why, and nothing is written

#### Scenario: The new name kept by no host
- **WHEN** no host keeps `timber` or `tailrace`, and nothing else stands
- **THEN** `crew kit rename tailrace timber` renames the records
