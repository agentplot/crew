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

### Requirement: crew reaches another host by its ssh name and runs the crew that host has installed
When a crew command runs crew on another host, as a tell, a send, an ops act or a command forwarded to a main level's host does, it SHALL reach the host by the `ssh` name the teams file's `hosts` gives it, and SHALL run `crew` there by its name, the crew the host's login path finds, as the one asking. It SHALL look for no checkout of crew there and SHALL read no address of its own to find one.

#### Scenario: A command forwarded to a main level's host
- **WHEN** the user runs `crew main status wldn` on deneb, the teams file giving wldn the machine chuck-herdr-alpha and giving chuck-herdr-alpha the `ssh` name `box`, and no drive's `repos` lists crew's repository
- **THEN** crew runs `crew main status wldn` by the name `crew` over `ssh box`, with the asker's `CREW_AGENT`, `CREW_LABEL` and `CREW_SESSION`, and the crew installed on chuck-herdr-alpha answers it

#### Scenario: A send reaches another host's drive whatever the teams file keeps of crew there
- **WHEN** the user runs `crew send wldn "<text>"` on deneb, where wldn runs on chuck-herdr-alpha and no drive's `repos` lists crew's repository
- **THEN** wldn-operator receives the text, as it does where a drive's `repos` lists crew

#### Scenario: A tell finds an agent herdr names in no pane through the crew installed there
- **WHEN** a tell from deneb is for wldn-planner on chuck-herdr-alpha, whose name herdr dropped in the pane crew keeps for it
- **THEN** crew asks the crew installed on chuck-herdr-alpha, by its name, `crew _found wldn-planner`, which finds the agent there and gives its name back, and the tell reaches it

#### Scenario: crew's code names no address of its own
- **WHEN** the modules under `plugin/lib/` and the commands under `plugin/bin/` are read
- **THEN** none names the repository crew's manifest names

### Requirement: crew is run on no host that has no ssh name or no crew on its login path
Where the teams file's `hosts` does not name a host, a command that runs crew there SHALL be refused naming the host and `hosts`, and no ssh SHALL be run. Where the host's login path finds no `crew`, the command SHALL fail saying so of that host, and nothing else SHALL be run there. No other crew, a checkout among them, SHALL be tried in its place.

#### Scenario: A host that has installed no crew
- **WHEN** chuck-herdr-alpha's login path finds no `crew`, a drive there lists crew's repository in its `repos`, and the user runs `crew main status wldn` on deneb
- **THEN** it fails saying chuck-herdr-alpha has no crew on its login path, so crew can't run there, and no crew runs on chuck-herdr-alpha, the drive's checkout of crew among them

#### Scenario: A host the file gives no ssh name
- **WHEN** a command on deneb runs crew on a host the teams file's `hosts` does not name
- **THEN** it is refused naming the host and the teams file's `hosts`, and no ssh is run
