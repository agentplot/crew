## RENAMED Requirements

- FROM: `### Requirement: The page opens on the partition's board`
- TO: `### Requirement: The page opens on the drive's board`

- FROM: `### Requirement: The header names every partition and links to its page`
- TO: `### Requirement: The header names every drive and links to its page`


## MODIFIED Requirements

### Requirement: The page opens on the drive's board
`crew page <label>` SHALL embed the board of that one drive, as `crew board --label <label> --json` reads it, and the page SHALL open on a board view of it. The lineage view SHALL be one switch away in the page's header. The board SHALL come from the same read the page is made from, and the page SHALL say when that read was made.

#### Scenario: Opening the page
- **WHEN** the user opens the page `crew page swancloud` wrote
- **THEN** it shows swancloud's board, with the time it was read in its header and a switch to the lineage view

#### Scenario: A host did not answer
- **WHEN** the page is made while a host of the drive does not answer
- **THEN** the board's attention strip names that host, and the bolts on it show their units with their stages unknown

### Requirement: The board view draws four lanes in the mockup's forms
The board view SHALL draw the lanes Inception, Bolt plan, Construction and Operation, in that order, each object in the form the mockup's phases view gives its kind: a signal as a quote, a proposal as a sheet, a queued unit as a slip, a bolt as a ledger and a landed bolt as a record. Bolt plan SHALL be drawn as the hatched gate and Operation marked as observed. No object SHALL carry the name of its lane, and a lane with nothing in it SHALL say so.

#### Scenario: Nothing waiting in the plan
- **WHEN** the drive has no open proposal, no planned bolt and no queued unit
- **THEN** the Bolt plan lane is drawn as the gate and says it holds nothing

### Requirement: The page stays one self-contained file
With the board view and the dock, the page SHALL still be one file that holds its own data, style and script and loads nothing: no font, script, style or image from anywhere. The one request it SHALL make is a dock's word, posted to the page's own address when the user sends it. It SHALL hold none of the mockup's sample data. Every text it shows from the state, in the lanes and in a dock, and every answer to a word, SHALL be set as text, never as markup.

#### Scenario: Offline
- **WHEN** the page is opened from disk with the network off
- **THEN** the board view and the lineage view draw in full and the browser makes no request

#### Scenario: A dock of typed words
- **WHEN** a signal's assertion holds `</script><b>here</b>` and the user opens its dock
- **THEN** the dock shows those characters as they are, and the page's data block is not ended by them

#### Scenario: Only the word is posted
- **WHEN** the served page is opened, a dock is opened, and a word is sent
- **THEN** the page's only request is one post to its own address's `word`, carrying the drive, key, agent and text

### Requirement: The header names every drive and links to its page
The page's header SHALL name every drive in the teams file, in its order, with the page's own drive marked as current. Each other drive SHALL be a link to that drive's page in the layout of this page's own file: `<label>.html` beside it when this page's file is named for its drive, `../<label>/` with the same file name when this page's folder is named for its drive, both when both are. When neither names its drive, the other drives SHALL be named and not linked, and `crew page` SHALL say so. Before the drives the header SHALL link to the fleet page in the same layout: `index.html` beside a page whose file alone is named for its drive, as the board is served, and `../page.html` from a page written as `page.html` in a folder named for its drive, as crew writes them; a page in any other layout SHALL have no link to the fleet page, since crew cannot tell where the fleet page is.

#### Scenario: Three drives
- **WHEN** the teams file holds madswan, swancloud and wldn and `crew page swancloud` writes `~/.local/state/crew/swancloud/page.html`
- **THEN** the header links to the fleet page at `../page.html`, then shows madswan, swancloud marked as current, and wldn, and madswan links to `../madswan/page.html` and wldn to `../wldn/page.html`

#### Scenario: Pages written side by side as they are served
- **WHEN** `crew page swancloud --out <folder>/swancloud.html` writes the page, as swancloud's board asks for it
- **THEN** the header links to the fleet page at `index.html`, madswan links to `madswan.html` and wldn to `wldn.html`, so on the board served as `<label>.html` side by side each link opens that drive's page

#### Scenario: A folder and a file both named for the drive
- **WHEN** the page is written to `<folder>/wldn/wldn.html`
- **THEN** madswan links to `../madswan/madswan.html`, and the header has no link to the fleet page

#### Scenario: A page written where its layout names no drive
- **WHEN** `crew page wldn --out <folder>/board.html` writes the page
- **THEN** the header has no link to the fleet page and names madswan and swancloud without linking them, and `crew page` prints a line saying the other drives are not linked because the page's file and folder are not named for wldn

### Requirement: Every item on the board opens its dock
A click on an item of the board view, or Enter on it, SHALL open that item's dock: a signal's quote, a proposal's sheet, a planned or started bolt's ledger, a unit's or chore's link in a chain or its queued slip, a fix's row, a landing's record, a deploy's record and a waiting operation's record. Each deploy of the deploys view SHALL open the same dock as its record on the board. Every item the page draws SHALL have a dock, and no team SHALL have one.

#### Scenario: A unit being built
- **WHEN** the user clicks unit a in tenant-environments' ledger
- **THEN** a dock opens titled a, saying it is a unit of bolt tenant-environments in code at 1 of 2 tasks, naming no slot

#### Scenario: Every item has its dock
- **WHEN** the page is written for a drive with a signal, a proposal, a planned bolt, a started bolt with a unit and a fix, a queued unit, a landing, a deploy and a waiting operation
- **THEN** every one of them carries the key of a dock the page holds, and no dock is a team's

#### Scenario: A deploy from either view
- **WHEN** the user opens the deploy of mac-studio from the Operation lane, and then from the deploys view
- **THEN** both open the same dock

### Requirement: Every dock takes a word to its item's agent
Every dock SHALL end with a one-line field for a word to the item's agent, a Send control, and a line naming the agent it goes to and saying that a card is answered on the rail. A word SHALL be at most 1000 characters. A dock opened from a page read from disk SHALL say that a word is sent only from the served board, and SHALL send nothing.

#### Scenario: A unit's dock
- **WHEN** the user opens unit a's dock, a in started bolt tenant-environments
- **THEN** the dock ends with a field and Send, naming the drive's planner as who the word goes to and saying that a card is answered on the rail

#### Scenario: Opened from disk
- **WHEN** the page is opened from a file on disk and the user opens a dock
- **THEN** the dock says a word is sent only from the served board, and its field sends nothing

### Requirement: A word goes to the agent its item's kind names
The agent a dock's word goes to SHALL be decided from the item's kind: a bolt, a unit or chore, a fix, a proposal or a batch to the drive's planner; a signal or a record to its design agent; a landing, a deploy or an operation to its main-level ops; and a subscription or a drive to the drive's operator.

#### Scenario: Each kind's agent
- **WHEN** the page is written for wldn with a bolt in flight with a unit and a fix, a planned bolt, a proposal, a signal, a landing, a deploy, an operation and a subscription
- **THEN** the bolt, unit, fix, planned bolt and proposal go to wldn-planner, the signal to wldn-design, the landing, deploy and operation to wldn-ops, and the subscription to wldn-operator

### Requirement: A word reaches its agent as the user's tell from the board, naming the item
Sending a word SHALL post it, with the drive, the item's key and the agent, to the page's own address, whose listener hands it to `crew tell --board` on its standard input. crew SHALL check it and tell the agent `[crew tell from <user>@board] (on <kind> <name>) <text>`, `<user>` being the user the listener runs as, and record the tell with its length and never its text. On delivery it SHALL print `sent to <agent>` and exit zero.

#### Scenario: A word on a unit
- **WHEN** the listener running as chuck pipes `{"label": "wldn", "key": "unit:a", "to": "swb-1-conductor", "text": "Keep the zone check"}` to `crew tell --board`
- **THEN** swb-1-conductor is prompted with `[crew tell from chuck@board] (on unit a) Keep the zone check`, the command prints `sent to swb-1-conductor`, and the run record holds a tell of 31 characters, the length of what was typed after the mark, and not the words

#### Scenario: The agent reads it as the user's
- **WHEN** the conductor's transcript holds that word and it captures a signal from its words
- **THEN** the signal is asserted by the user

### Requirement: A word not of the board's form is refused
`crew tell --board` SHALL type nothing and exit non-zero, saying why on standard error, when the posted word is not one JSON object holding the drive, key, agent and text as strings; names no drive crew knows; has a key of no kind a dock has; names an agent its item's kind does not go to in that drive; or has a text that is empty, longer than 1000 characters or more than one line.

#### Scenario: An agent the kind does not go to
- **WHEN** a word on `proposal:4` is posted for swb-1-conductor
- **THEN** nothing is typed, and the command exits non-zero saying a word on a proposal goes to wldn-planner

#### Scenario: A word of two lines
- **WHEN** the posted text holds a line break
- **THEN** nothing is typed, and the command exits non-zero saying a word from the board is one line

### Requirement: A subscription's dock lists the main level's sessions on it
The Claude account a session of the drive's main level runs on SHALL have a dock on the drive's page, opened from the fleet page's subscription by the drive's link, which SHALL list the drive's sessions on that account, as the hosts file names them: each main-level agent on it, with its host and session. A session whose entry names no account SHALL have no such dock.

#### Scenario: One account for three roles
- **WHEN** wldn's design agent, planner and reviewer run in mac-studio's session wldn on account madswan-2, and its ops in session ops on account willdan
- **THEN** madswan-2's dock lists wldn-design, wldn-planner and wldn-reviewer with mac-studio and session wldn, and willdan's lists wldn-ops
