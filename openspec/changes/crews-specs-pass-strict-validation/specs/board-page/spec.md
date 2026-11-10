## ADDED Requirements

### Requirement: The deploys view draws each environment's deploys as a timeline with the user's word on each
The page SHALL have a deploys view, one switch from the board and the flow, kept in its address, that draws each environment as a timeline of its deploys over the record's window, oldest first, each with the commit it moved from and to, the user's word on it as its card's answer recorded it (approved by whom and when, waiting, or replaced unanswered), its steps, the suite's checks and its outcome; then the operations waiting on it.

#### Scenario: The sequence of words
- **WHEN** one deploy of mac-studio was approved and done and a newer offer waits
- **THEN** the deploys view shows the approved one above the waiting one, each with its word

### Requirement: The deploys view shows what each deploy carried, read from the run record alone
The deploys view SHALL draw each deploy with the bolts it carried with the proposals the lineage joins to each as its release notes, and the after-deploy steps of its commit with their doers and states. The deploys view SHALL be read from the run record alone, and the page SHALL stay one self-contained file.

#### Scenario: What a deploy carried
- **WHEN** the deploy of mac-studio carried bolt b, whose unit came from proposal 3
- **THEN** the deploys view lists b under it with proposal 3 and the first line of its case

### Requirement: Every decision is drawn on its object's form, and nothing on the board answers it
Every marker the board's read gives SHALL be drawn on its object's form, never as a form of its own: ✓ for an approval (an open proposal, a bolt to land), ✎ for an answer (a verify report not yet answered), ! for attention (a held bolt every unit of which has landed). The board view SHALL hold no button, link or command that answers or moves anything.

#### Scenario: A proposal waiting
- **WHEN** proposal 4 is open and wldn-planner has its card open
- **THEN** proposal 4's sheet carries ✓ and says its card is open, asked by wldn-planner, and nothing on the page approves it

### Requirement: A marker says whether its card is open, who asked it, and that its post was refused
Each marker SHALL say whether its card is open and who asked it, and, when none is open and its last post was refused, that its post was refused, with Pending You's words where the marker is pointed at.

#### Scenario: A deploy whose card was refused
- **WHEN** a deploy of deneb waits on the user's word and Pending You refused its card's last post
- **THEN** the deploy's marker says it has no card, its post refused, and pointing at it shows Pending You's words

### Requirement: The header names every drive and links each other drive in the page's own layout
The page's header SHALL name every drive in the teams file, in its order, with the page's own drive marked as current. Each other drive SHALL be a link to that drive's page in the layout of this page's own file: `<label>.html` beside it when this page's file is named for its drive, `../<label>/` with the same file name when this page's folder is named for its drive, both when both are.

#### Scenario: Three drives
- **WHEN** the teams file holds madswan, swancloud and wldn and `crew page swancloud` writes `~/.local/state/crew/swancloud/page.html`
- **THEN** the header links to the fleet page at `../page.html`, then shows madswan, swancloud marked as current, and wldn, and madswan links to `../madswan/page.html` and wldn to `../wldn/page.html`

#### Scenario: A folder and a file both named for the drive
- **WHEN** the page is written to `<folder>/wldn/wldn.html`
- **THEN** madswan links to `../madswan/madswan.html`, and the header has no link to the fleet page

### Requirement: A page whose layout names no drive names the other drives without linking them
When neither this page's file nor its folder names its drive, the other drives SHALL be named and not linked, and `crew page` SHALL say so.

#### Scenario: A page written where its layout names no drive
- **WHEN** `crew page wldn --out <folder>/board.html` writes the page
- **THEN** the header has no link to the fleet page and names madswan and swancloud without linking them, and `crew page` prints a line saying the other drives are not linked because the page's file and folder are not named for wldn

### Requirement: The header links to the fleet page where the page's layout tells where it is
Before the drives the header SHALL link to the fleet page in the same layout as this page's own file: `index.html` beside a page whose file alone is named for its drive, as the board is served, and `../page.html` from a page written as `page.html` in a folder named for its drive, as crew writes them; a page in any other layout SHALL have no link to the fleet page, since crew cannot tell where the fleet page is.

#### Scenario: Pages written side by side as they are served
- **WHEN** `crew page swancloud --out <folder>/swancloud.html` writes the page, as swancloud's board asks for it
- **THEN** the header links to the fleet page at `index.html`, madswan links to `madswan.html` and wldn to `wldn.html`, so on the board served as `<label>.html` side by side each link opens that drive's page

### Requirement: Words from the board are not the user's answer to a batch or a record
Words that reached an agent only in a tell from `<user>@board` SHALL NOT be taken as the user's words for answering a batch or settling a record in a pane. crew SHALL refuse each, recording nothing, and say the words came from the board, which answers nothing, and where the user answers instead. The same words typed in the pane, or told from `<user>@<host>`, SHALL still be the user's.

#### Scenario: A batch answered from the board
- **WHEN** the user sends "Batch 14 is fine" from a dock, and the planner runs `crew card answer batch/14 --excerpt "Batch 14 is fine"`
- **THEN** batch 14 is not answered, and the command says the words came from the board

#### Scenario: Typed in the pane after the board
- **WHEN** the user sent "Batch 14 is fine" from a dock and then typed the same words in the planner's pane
- **THEN** `crew card answer batch/14 --excerpt "Batch 14 is fine"` records batch 14 answered

### Requirement: No words, from the board or a pane, land a bolt
No words, from the board or typed in a pane, SHALL land a bolt: a bolt lands only on the user's send of its row on its kit's landings card, which crew carries to the runner (record 0056 point 5).

#### Scenario: A landing asked from the board
- **WHEN** the user sends "Land bolt y" from bolt y's landing dock, and swancloud-ops runs `crew bolt submit y --excerpt "Land bolt y"`
- **THEN** nothing is submitted or posted, and the command says a bolt lands on the user's send of its row on its kit's landings card, which crew carries to the runner

## REMOVED Requirements

### Requirement: The deploys view
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "The deploys view draws each environment's deploys as a timeline with the user's word on each" and "The deploys view shows what each deploy carried, read from the run record alone".

### Requirement: Every decision is a marker on its object
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "Every decision is drawn on its object's form, and nothing on the board answers it" and "A marker says whether its card is open, who asked it, and that its post was refused".

### Requirement: The header names every drive and links to its page
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "The header names every drive and links each other drive in the page's own layout", "A page whose layout names no drive names the other drives without linking them" and "The header links to the fleet page where the page's layout tells where it is".

### Requirement: A word from the board answers nothing
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "Words from the board are not the user's answer to a batch or a record" and "No words, from the board or a pane, land a bolt".
