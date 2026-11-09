## RENAMED Requirements

- FROM: `### Requirement: The fleet page shows every partition at once`
- TO: `### Requirement: The fleet page shows every drive at once`

- FROM: `### Requirement: Each partition shows what needs attention`
- TO: `### Requirement: Each drive shows what needs attention`

- FROM: `### Requirement: The fleet page is written beside the partitions' pages`
- TO: `### Requirement: The fleet page is written beside the drives' pages`

- FROM: `### Requirement: Each partition shows where its main level runs and on which account`
- TO: `### Requirement: Each drive shows where its main level runs and on which account`

- FROM: `### Requirement: Each partition shows the kits its plan and landings name, and their mains`
- TO: `### Requirement: Each drive shows the kits its plan and landings name, and their mains`

- FROM: `### Requirement: Each partition's page is a link away, and a subscription's dock on it`
- TO: `### Requirement: Each drive's page is a link away, and a subscription's dock on it`

- FROM: `### Requirement: A subscription shows the main levels' sessions and partitions on it beside its use`
- TO: `### Requirement: A subscription shows the main levels' sessions and drives on it beside its use`


## MODIFIED Requirements

### Requirement: The fleet page shows every drive at once
`crew page --fleet` SHALL write one page holding every drive in the teams file, in its order, each as a block of its own, from one read of all of them that is the read `crew board` makes. The page SHALL say when that read was made and, for each drive, the commit of its plan it was read at. A host that did not answer, or a plan that could not be read, SHALL be named in its drive's block and in what the command prints, and everything else SHALL still be shown.

#### Scenario: Three drives
- **WHEN** the teams file holds madswan, swancloud and wldn and `crew page --fleet` is run
- **THEN** the page holds a block for madswan, then swancloud, then wldn, and says as of when and which commit of each plan

#### Scenario: A host that does not answer
- **WHEN** one of wldn's hosts does not answer as the fleet page is made
- **THEN** wldn's block names that host as not answering, the command prints it, and the other drives and wldn's other hosts are shown in full

### Requirement: Each drive shows what needs attention
A drive's block SHALL show its attention items in the words the board uses for them, and how many of its cards are open, or that nothing needs attention.

#### Scenario: A bolt still in the plan once landed
- **WHEN** a bolt of swancloud has every unit landed and is still in the plan
- **THEN** swancloud's block carries the board's attention line for that bolt

### Requirement: The fleet page is written beside the drives' pages
Written with no `--out`, the fleet page SHALL be `page.html` in crew's state folder, beside each drive's folder.

#### Scenario: Crew's own layout
- **WHEN** `crew page --fleet` is run with no `--out`
- **THEN** it writes `~/.local/state/crew/page.html` and prints that path, and wldn's name links to `wldn/page.html`

### Requirement: The fleet page is one self-contained file that answers nothing
The fleet page SHALL be one file that holds its own data, style and script and fetches nothing, light and dark as the viewer prefers, its blocks side by side on a desktop and stacked under 760 px. Every text it shows from the state SHALL be set as text, never as markup. It SHALL hold no control that answers a card or moves anything, and making it SHALL write nothing to any drive's state.

#### Scenario: Offline
- **WHEN** the fleet page is opened from disk with the network off
- **THEN** every block draws in full and the browser makes no request

#### Scenario: Typed words
- **WHEN** the words of an attention item, a host's error as it was read, hold `</script><b>here</b>`
- **THEN** the page shows those characters as they are, and its data block is not ended by them

### Requirement: The fleet page shows every Claude subscription
The fleet page SHALL hold a section of Claude subscriptions, one for each account the hosts file gives a session and each account a host published a reading for, by name, apart from the drives' blocks.

#### Scenario: Accounts from sessions and from readings
- **WHEN** the hosts file gives sessions the accounts madswan, madswan-2 and ia, and deneb has published a reading for madswan and for fable-test, which no session names
- **THEN** the subscriptions section holds fable-test, ia, madswan and madswan-2, in that order

### Requirement: Each drive shows where its main level runs and on which account
A drive's block SHALL name each host the board asked for it, its main level's and its runners', one that did not answer marked so, and its main level's host, marked not asked where the board did not ask it; and under each host each herdr session an agent of the drive runs in: its main-level agents in it (design agent, planner, ops, operator), and the Claude account the hosts file gives the session. A session whose entry names no account SHALL say so, never be shown blank. A session no agent of the drive runs in SHALL not be shown, and no team SHALL be named.

#### Scenario: Two sessions of one main level
- **WHEN** swancloud's design agent, planner and ops run in deneb's session swancloud on account madswan, and its operator in deneb's session swancloud-3, which names no account
- **THEN** swancloud's block shows deneb with session swancloud, its design agent, planner and ops, account madswan, and session swancloud-3, its operator, saying no account is named for it in the hosts file

#### Scenario: A runner's host
- **WHEN** wldn's runner on chuck-herdr-alpha takes its work and its main level runs on mac-studio, which the board did not ask
- **THEN** wldn's block shows chuck-herdr-alpha answered with no session under it, and mac-studio not asked with session wldn and its main-level agents

### Requirement: Each drive shows the kits its plan and landings name, and their mains
A drive's block SHALL list each of its kits, the repositories its plan and its landings name, once; the last landing on its main in the run record's window, its bolt, the commit main held after it, when and who landed it, or that none is in the window; and what is queued for that main: the bolts of that kit that wait to land, with whether their landing card is open, the bolts of it in construction, and how many bolts of it are planned and units of it are queued. No kit SHALL name a team that builds it.

#### Scenario: A kit with a landing and a bolt waiting
- **WHEN** crew's main last took bolt a at 3f2c1d0 two days ago, bolt w of crew waits to land with its card open, and one unit of crew is queued
- **THEN** crew's line says it last landed a at 3f2c1d0 with when and who landed it, that w waits to land with its card open, and that one unit is queued, and names no team

#### Scenario: A kit with no landing in the window
- **WHEN** swancloud has had no landing in the run record's window
- **THEN** swancloud's line says no landing is in the window, never a blank

### Requirement: Each drive's page is a link away, and a subscription's dock on it
Each drive's name on the fleet page SHALL link to that drive's page, and each drive a subscription names to that page with the subscription's dock open, in the layout of the fleet page's own file: `<label>.html` beside it when the fleet page's file is `index.html`, as the board is served; `<label>/page.html` beside it when its file is `page.html`, crew's own layout. For any other name the drives SHALL be named and not linked, and the command SHALL say so.

#### Scenario: Served beside the drives' pages
- **WHEN** `crew page --fleet --out <folder>/index.html` writes the page
- **THEN** wldn's name links to `wldn.html`, and swancloud under the madswan subscription to swancloud's page with madswan's dock open

#### Scenario: A name that says no layout
- **WHEN** `crew page --fleet --out <folder>/fleet.html` writes the page
- **THEN** the drives are named and not linked, and the command prints a line saying so

### Requirement: A subscription shows the main levels' sessions and drives on it beside its use
A subscription SHALL list each session the hosts file gives its account, by host, with crew's agents in it, the main levels' roles, and SHALL name the drives whose agents run in those sessions. A session no crew agent runs in SHALL be listed as running none. Nothing SHALL be computed from the use and the work together, and no team or slot SHALL be named.

#### Scenario: Two main levels on one subscription
- **WHEN** madswan's main level runs in deneb's session madswan and swancloud's design agent, planner and ops in deneb's session swancloud, both on account madswan
- **THEN** madswan lists deneb's sessions madswan, with madswan's design agent, planner, ops and operator, and swancloud, with swancloud's design agent, planner and ops, and names the drives madswan and swancloud

#### Scenario: A main-level session that runs nothing
- **WHEN** deneb's session agentplot-2 is on account madswan and no agent of any drive runs there
- **THEN** madswan lists deneb's agentplot-2 as running no crew agent
