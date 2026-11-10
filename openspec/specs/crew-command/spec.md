# crew-command Specification

## Purpose
What the `crew` command, and `crew-role` beside it, do with what they are given, whatever the command: the rules every command holds to at its entry point, before it reads, records, starts or forwards anything (`code.11`).

## Requirements

### Requirement: A help flag shows a command's usage and acts on nothing
Every crew command SHALL answer `-h` or `--help` among its own arguments by printing its usage and exiting 0, before it reads the teams file, records, asks, launches, starts, tells or sends anything to another host. Its usage SHALL be the one text its entry point already prints. An argument that is not exactly `-h` or `--help` SHALL be read as it was before.

#### Scenario: A tell's usage
- **WHEN** the design agent runs `crew tell wldn-planner --help`, or `crew tell wldn-planner -h`, where the planner runs as its kind
- **THEN** crew prints `crew tell`'s lines of its usage and exits 0; nothing is asked of the planner, nothing is typed into a pane and no entry is written

#### Scenario: A fix's usage
- **WHEN** ops runs `crew fix tenant-environments tidy --help`, or `crew fix tenant-environments tidy "The banner flickers." -h`
- **THEN** crew prints the usage of `crew fix` and exits 0, and no fix is launched: no request and no entry

#### Scenario: Every command
- **WHEN** any command crew dispatches is run with arguments of its own shape and `--help` or `-h` among them, the internal `_` commands, `crew hold <host> "<why>" --help`, `crew send <drive> "<text>" --help`, `crew main up <label> --help` and `crew revive --help` among them
- **THEN** it prints its usage and exits 0, with no call to herdr, ssh, sluice or any other tool, no agent started, no entry on any host and no write to the state branch; a command `crew` reads itself prints its own lines of `crew`'s usage header, and a command `crew` hands to a Python parser prints that parser's usage

#### Scenario: crew's own usage
- **WHEN** the user runs `crew --help`, `crew -h` or `crew-role wldn planner --help`
- **THEN** each prints its whole usage and exits 0, starting nothing

#### Scenario: A command a Python parser reads
- **WHEN** an agent runs `crew bolt start tenant-environments --help`, or `crew plan approve three --help`, where `three` is no proposal's number
- **THEN** crew prints the usage of `crew bolt start`, or of `crew plan approve`, and exits 0, before it checks for recutils or reads the teams file

#### Scenario: A word that is not the flag
- **WHEN** the design agent runs `crew tell wldn-planner "--help with which table holds tenants"`, where the planner runs as its kind
- **THEN** the words are asked of the planner, as any tell to a role that runs as its kind is

### Requirement: crew reads the repository it is from its own manifest
crew SHALL read the repository it is from the `repository` of its own manifest, `plugin/.claude-plugin/plugin.json`, a GitHub address, and never from a name written in its code. Where the manifest cannot be read or names no GitHub repository, a command that runs crew on another host SHALL be refused naming the file, and nothing SHALL be run there. A command run for this host SHALL read no manifest.

#### Scenario: crew's manifest names its current address
- **WHEN** crew's manifest is read
- **THEN** its `repository`, `https://github.com/agentplot/crew`, gives `agentplot/crew`

#### Scenario: A manifest that names no repository
- **WHEN** crew's manifest has no `repository`, or names one that is no GitHub address, and a command runs crew on another host
- **THEN** it is refused naming the manifest, and nothing is run on the other host

#### Scenario: crew's code names no address of its own
- **WHEN** the modules under `plugin/lib/` and the commands under `plugin/bin/` are read
- **THEN** none names the repository crew's manifest names

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
