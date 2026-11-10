## ADDED Requirements

### Requirement: A drive's block names its hosts, and under each the sessions its agents run in with their account
A drive's block SHALL name each host the board asked for it, its main level's and its runners', one that did not answer marked so, and its main level's host, marked not asked where the board did not ask it; and under each host each herdr session an agent of the drive runs in: its main-level agents in it (design agent, planner, ops, operator), and the Claude account the drive's `accounts` gives the roles in that session. A session no agent of the drive runs in SHALL not be shown.

#### Scenario: Two sessions of one main level
- **WHEN** swancloud's design agent, planner and ops run in deneb's session swancloud and its operator in deneb's session swancloud-3, and swancloud's `accounts` gives the first three madswan and its operator madswan-2
- **THEN** swancloud's block shows deneb with session swancloud, its design agent, planner and ops, account madswan, and session swancloud-3, its operator, account madswan-2

#### Scenario: A runner's host
- **WHEN** wldn's runner on chuck-herdr-alpha takes its work and its main level runs on mac-studio, which the board did not ask
- **THEN** wldn's block shows chuck-herdr-alpha answered with no session under it, and mac-studio not asked with session wldn and its main-level agents

### Requirement: A drive's block names no team
A drive's block SHALL name no team.

#### Scenario: A drive's block with no team
- **WHEN** the fleet page is made for madswan, swancloud and wldn
- **THEN** no drive's block names a team

### Requirement: Each drive lists its kits once, with each one's last landing and what is queued for its main
A drive's block SHALL list each of its kits, the repositories its plan and its landings name, once; the last landing on its main in the run record's window, its bolt, the commit main held after it, when and who landed it, or that none is in the window; and what is queued for that main: the bolts of that kit that wait to land, with whether their landing card is open, the bolts of it in construction, and how many bolts of it are planned and units of it are queued.

#### Scenario: A kit with a landing and a bolt waiting
- **WHEN** crew's main last took bolt a at 3f2c1d0 two days ago, bolt w of crew waits to land with its card open, and one unit of crew is queued
- **THEN** crew's line says it last landed a at 3f2c1d0 with when and who landed it, that w waits to land with its card open, and that one unit is queued, and names no team

#### Scenario: A kit with no landing in the window
- **WHEN** swancloud has had no landing in the run record's window
- **THEN** swancloud's line says no landing is in the window, never a blank

### Requirement: No kit names a team that builds it
No kit SHALL name a team that builds it.

#### Scenario: Kits with no team
- **WHEN** swancloud's plan and landings name crew and swancloud
- **THEN** swancloud's block lists crew and swancloud, and neither names a team

## REMOVED Requirements

### Requirement: Each drive shows where its main level runs and on which account
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A drive's block names its hosts, and under each the sessions its agents run in with their account" and "A drive's block names no team".

### Requirement: Each drive shows the kits its plan and landings name, and their mains
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "Each drive lists its kits once, with each one's last landing and what is queued for its main" and "No kit names a team that builds it".
