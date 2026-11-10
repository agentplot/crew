## ADDED Requirements

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

## REMOVED Requirements

### Requirement: crew reads the repository it is from its own manifest
**Reason**: crew read its own address only to find its checkout on another host. It now runs the crew that host installed, by its name, so nothing reads the address.
**Migration**: The manifest keeps its `repository` for Claude Code and crew's release. The check that crew's code names no address of its own is now a scenario of "crew reaches another host by its ssh name and runs the crew that host has installed".

### Requirement: crew reaches another host by its ssh name and runs the checkout that host keeps of crew
**Reason**: A host keeps crew's checkout only where a drive's `repos` lists crew, and a released host runs its release rather than that checkout, so a send between the box and deneb was refused in both directions (2026-11-10).
**Migration**: "crew reaches another host by its ssh name and runs the crew that host has installed": crew runs `crew` by its name on the host's login path, over ssh to the same `ssh` name.

### Requirement: crew is run on no host that keeps no checkout of it or has no ssh name
**Reason**: crew looks for no checkout of itself on another host, so a host that keeps none, or keeps one under a former address, is no longer a refusal of its own.
**Migration**: "crew is run on no host that has no ssh name or no crew on its login path": a host `hosts` does not name is refused as before, and a host whose login path finds no crew fails naming the host.
