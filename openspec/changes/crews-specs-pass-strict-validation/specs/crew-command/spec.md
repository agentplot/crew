## ADDED Requirements

### Requirement: crew reaches another host by its ssh name and runs the checkout that host keeps of crew
When a crew command runs crew on another host, as a tell, a send, an ops act or a command forwarded to a main level's host does, it SHALL reach the host by the `ssh` name the teams file's `hosts` gives it, and SHALL run the crew in the checkout that host keeps of the repository crew is, found where the teams file keeps it there: in the folder of a drive whose machine is that host and whose `repos` lists the repository.

#### Scenario: A send reaches another host's drive
- **WHEN** crew is `agentplot/crew`, the teams file gives wldn the machine chuck-herdr-alpha, the folder `/workspace` and `repos` listing `agentplot/crew`, gives chuck-herdr-alpha the `ssh` name `box`, and the user runs `crew send wldn "<text>"` on deneb
- **THEN** crew runs `/workspace/crew/main/plugin/bin/crew` on chuck-herdr-alpha over `ssh box`, and wldn-operator receives the text

### Requirement: crew is run on no host that keeps no checkout of it or has no ssh name
Where the teams file keeps no checkout of the repository crew is on a host, or gives the host no `ssh` name, a command that runs crew there SHALL be refused, naming the host and what crew looked for, and nothing SHALL be run there. No former address of crew's SHALL be followed.

#### Scenario: A host that keeps no checkout of crew
- **WHEN** no drive whose machine is chuck-herdr-alpha lists `agentplot/crew` in its `repos`, and a command on deneb runs crew there
- **THEN** it is refused saying chuck-herdr-alpha keeps no checkout of agentplot/crew, the repository crew is, as the teams file gives it, so crew can't run there, and nothing is run on chuck-herdr-alpha

#### Scenario: A checkout kept under crew's former address
- **WHEN** wldn's `repos` lists `afterthought/crew` and nothing by `agentplot/crew`, and a command on deneb runs crew on chuck-herdr-alpha
- **THEN** it is refused the same way, naming `agentplot/crew`

#### Scenario: A host the file gives no ssh name
- **WHEN** a command on deneb runs crew on a host the teams file's `hosts` does not name
- **THEN** it is refused naming the host and the teams file's `hosts`, and no ssh is run

## REMOVED Requirements

### Requirement: crew runs itself on another host from the checkout of the repository it is
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "crew reaches another host by its ssh name and runs the checkout that host keeps of crew" and "crew is run on no host that keeps no checkout of it or has no ssh name".
