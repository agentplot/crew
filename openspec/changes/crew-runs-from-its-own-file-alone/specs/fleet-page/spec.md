## MODIFIED Requirements

### Requirement: The fleet page shows every Claude subscription
The fleet page SHALL hold a section of Claude subscriptions, one for each account a drive's `accounts` in the teams file gives a role and each account a host published a reading for, by name, apart from the drives' blocks.

#### Scenario: Accounts from sessions and from readings
- **WHEN** the teams file gives the drives' roles the accounts madswan, madswan-2 and ia, and deneb has published a reading for madswan and for fable-test, which no role's account names
- **THEN** the subscriptions section holds fable-test, ia, madswan and madswan-2, in that order

### Requirement: A reading a host could not make is marked
A reading a host published as not made SHALL be marked so on its subscription with the host's words for why and when it tried. A subscription with no reading made SHALL say its use could not be read; one no host published for SHALL say no host has published its use.

#### Scenario: Only a failed reading
- **WHEN** deneb published for credits that it could not read its use, "the usage endpoint answered 401", and no other host published for credits
- **THEN** credits shows no figures, says its use could not be read, and names deneb with "the usage endpoint answered 401" and when it tried

#### Scenario: Nothing published
- **WHEN** wldn's `accounts` gives its planner ia and no host published a reading for ia
- **THEN** ia says no host has published its use

### Requirement: Each drive shows where its main level runs and on which account
A drive's block SHALL name each host the board asked for it, its main level's and its runners', one that did not answer marked so, and its main level's host, marked not asked where the board did not ask it; and under each host each herdr session an agent of the drive runs in: its main-level agents in it (design agent, planner, ops, operator), and the Claude account the drive's `accounts` gives the roles in that session. A session no agent of the drive runs in SHALL not be shown, and no team SHALL be named.

#### Scenario: Two sessions of one main level
- **WHEN** swancloud's design agent, planner and ops run in deneb's session swancloud and its operator in deneb's session swancloud-3, and swancloud's `accounts` gives the first three madswan and its operator madswan-2
- **THEN** swancloud's block shows deneb with session swancloud, its design agent, planner and ops, account madswan, and session swancloud-3, its operator, account madswan-2

#### Scenario: A runner's host
- **WHEN** wldn's runner on chuck-herdr-alpha takes its work and its main level runs on mac-studio, which the board did not ask
- **THEN** wldn's block shows chuck-herdr-alpha answered with no session under it, and mac-studio not asked with session wldn and its main-level agents

### Requirement: A subscription shows the main levels' sessions and drives on it beside its use
A subscription SHALL list each session a drive's main-level role runs in under its account, as the drive's `accounts` gives it, by host, with crew's agents in it, the main levels' roles, and SHALL name the drives whose agents run in those sessions. Nothing SHALL be computed from the use and the work together, and no team or slot SHALL be named.

#### Scenario: Two main levels on one subscription
- **WHEN** madswan's main level runs in deneb's session madswan and swancloud's design agent, planner and ops in deneb's session swancloud, every one of those roles on account madswan
- **THEN** madswan lists deneb's sessions madswan, with madswan's design agent, planner, ops and operator, and swancloud, with swancloud's design agent, planner and ops, and names the drives madswan and swancloud

#### Scenario: A main-level session that runs nothing
- **WHEN** deneb's herdr runs a session agentplot-2, which no drive's role runs in, and madswan is the account of every role of madswan's main level
- **THEN** madswan lists madswan's sessions alone, and no subscription lists agentplot-2
