## ADDED Requirements

### Requirement: A proposal is one open record that is never changed
`crew plan propose <file>` SHALL write one Proposal record to `proposals.rec` on the drive's branch: its number, the planner's case, the plan commands it would run in order, who wrote it and when, and its state, `open`. A number SHALL be given once and never reused, and a proposal SHALL never be removed or its commands changed.

#### Scenario: A new bolt with two units
- **WHEN** the planner proposes `bolt new cfn-checks …`, `unit add cfn-nag-security-check … --bolt cfn-checks` and `unit move retire-suite-cfn-lint cfn-checks`, with its case
- **THEN** proposal N holds the case and those three commands in that order, in state `open`, and the plan is unchanged

#### Scenario: Someone other than the planner
- **WHEN** a conductor runs `crew plan propose`
- **THEN** it is refused; only the drive's planner and the user write proposals

### Requirement: A proposal holds only commands that change bolts, units and chores
A proposal's commands SHALL be among `bolt new`, `bolt order`, `bolt drop`, `unit add`, `unit amend`, `unit move`, `unit split`, `unit order`, `unit after`, `unit drop`, `chore add`, `chore move`, `chore order`, `chore after` and `chore drop`.

#### Scenario: A command a proposal cannot hold
- **WHEN** a proposal file holds `bolt give swb-1`
- **THEN** the proposal is refused, naming the command, and nothing is written

#### Scenario: An amendment to a unit in flight
- **WHEN** the planner proposes `unit amend <unit> "<new intent>"` for a unit in code in a bolt a team holds
- **THEN** the proposal is written, the unit's intent is unchanged, and that bolt's conductor is told

#### Scenario: A chore's words changed
- **WHEN** the planner proposes `chore drop bump-biome "…"` then `chore add bump-biome "<new words>" --bolt tooling`
- **THEN** the proposal is written; a chore has no amendment, so its words change by a drop and an add

### Requirement: Approval applies a proposal's commands in one commit or not at all
`crew plan approve <n>` SHALL apply the proposal's commands in order to the plan at the branch's tip and close the proposal as `approved`, in one commit. When any command would now be refused, the approval SHALL be refused, naming the command and the reason, and the plan and the proposal SHALL be unchanged. What follows a direct command SHALL follow the approval.

#### Scenario: A proposal is approved
- **WHEN** the user approves proposal N, which creates a bolt and adds a unit to it
- **THEN** one commit adds the bolt and the unit and marks the proposal approved, and no reader sees the bolt without the unit

#### Scenario: The plan moved since
- **WHEN** a unit the proposal moves was dropped after the proposal was written
- **THEN** the approval is refused, naming that command, and the proposal stays open

#### Scenario: A unit with a worktree is moved
- **WHEN** an approved proposal moves unit `a`, launched as a Flume place on started `x`, to bolt `y`
- **THEN** the approval is refused, naming `a`'s place and that it is dropped and added again as the way on, crew rebases nothing, and the plan and the proposal are unchanged

#### Scenario: A unit from a signal
- **WHEN** an approved proposal holds `unit add … --signal <id>`
- **THEN** the same commit adds the unit and the signal's `route` move

### Requirement: An approval leaves out the new units the user cleared
`crew plan approve <n> --clear <unit>...` SHALL apply the commands the user kept: each cleared unit SHALL be one the proposal adds or moves into a bolt, every command that names only cleared units SHALL be left out, and when a command left in names a cleared unit the approval SHALL be refused, naming that command and the unit, with nothing changed. The approved proposal SHALL record each cleared unit.

#### Scenario: A new unit left out
- **WHEN** proposal N drops `a`, adds `b` and `c` to bolt `y`, and orders `c` first, and the user approves it with `c` cleared
- **THEN** one commit drops `a`, adds `b`, makes no unit `c`, runs no order of `c`, marks the proposal approved and records `c` as cleared

#### Scenario: A unit moved in from the queue left out
- **WHEN** proposal N moves queued unit `q` into bolt `y` and the user clears `q`
- **THEN** the approval applies the rest, and `q` stays in the queue as it was

#### Scenario: A kept command names a cleared unit
- **WHEN** proposal N adds `b` and `c` to bolt `y`, `c` with `--after b`, and the user clears `b` and keeps `c`
- **THEN** the approval is refused, naming the `unit add c` command and `b`, the plan and the proposal are unchanged, and the planner writes the proposal again without `b`

#### Scenario: A unit that is not new is cleared
- **WHEN** `crew plan approve N --clear a` names a unit proposal N only amends
- **THEN** the approval is refused, naming `a` and the units the proposal adds or moves in, and nothing changes

### Requirement: A dropped proposal applies nothing and its card is withdrawn with the reason
`crew plan drop <n> "<reason>"` SHALL close an open proposal as `dropped` with the reason, applying nothing, withdraw its chain's card with the reason, and tell the planner when someone else dropped it.

#### Scenario: The user rejects a proposal
- **WHEN** the user drops proposal N with a reason
- **THEN** the proposal is `dropped`, the plan is unchanged, its card is withdrawn with the reason, and the planner is told the reason

### Requirement: A replacing proposal drops the one it replaces and changes the chain's card to it
`crew plan propose <file> --replaces <n>` SHALL drop proposal n and write its successor in one commit, the successor naming the one it replaces, and SHALL change the chain's card to the successor with the note "Rewritten as proposal <successor> after your note", in place while it waits on the user, and once the user's note answered it as a new version following the card they answered.

#### Scenario: The planner revises
- **WHEN** the planner proposes again with `--replaces N` after the user asked for a different placement
- **THEN** proposal N is `dropped`, proposal N+1 is `open` and names N, agreements given to N do not carry over, and the card keyed `proposal/N` shows N+1 with the change note

### Requirement: A replaced card Pending You cannot change in place is withdrawn and followed
A replaced proposal's card that asks its rows as questions, its rows filling more than one list, or whose form the successor changes, a hold-to-approve, a choice, one list or lists, SHALL be withdrawn with the rewrite's note while it waits and the successor's posted following it, since Pending You changes no card's questions or kind in place. The chain's card SHALL stay keyed by its first proposal, and the rail's row for the successor SHALL carry it.

#### Scenario: A rewrite that moves its card to another form
- **WHEN** proposal N's card, one list of three new units, waits on the user, and the planner proposes again with `--replaces N`, its six new units filling two lists
- **THEN** the card is not changed in place: it is withdrawn with the note "Rewritten as proposal N+1 after your note", and N+1's card, keyed by the chain's first proposal, is posted following it with its rows as questions

### Requirement: crew plan propose raises the proposal's card itself
`crew plan propose` SHALL, once a proposal is accepted into the plan, raise its card itself in the planner's name, keyed `proposal/<n>`, drawn from the plan and the proposal as record 0018 has it.

#### Scenario: A proposal with three new units
- **WHEN** the planner's proposal adding three units to a bolt is accepted as number 4
- **THEN** its card is open, titled "Plan change to <bolt>: 3 new", with the case, the change drawn and in text, a paragraph per unit, and one list of the three units ticked

### Requirement: An agent shows a proposal as crew plan proposed prints it
Any agent that puts one of the planner's proposals before the user in a pane, the planner, a conductor or the operator agent, SHALL show what `crew plan proposed <n>` prints, in its own pane or opened beside it, and SHALL NOT name the proposal by its number alone; the number SHALL follow the words, as a reference.

#### Scenario: The planner proposes
- **WHEN** the planner has written proposal N and `crew plan propose` accepts it
- **THEN** its card is open, and when the user is in the planner's pane the planner shows what `crew plan proposed N` prints and asks them to approve it or say what to change

#### Scenario: The user asks what waits on them
- **WHEN** the operator agent answers where things stand and proposal N is open
- **THEN** its answer shows what `crew plan proposed N` prints, not only that proposal N is open

### Requirement: An agent asks for the user's answer in words and acts only on it
An agent that puts one of the planner's proposals before the user SHALL ask for the user's answer in words, SHALL NOT recite a command for the user to answer with, and SHALL run the answering command only on the user's word.

#### Scenario: The user says yes
- **WHEN** the user tells the agent showing proposal N to approve it
- **THEN** that agent runs `crew plan approve N`, which closes the card with what was applied

### Requirement: A proposal opens in plannotator as crew plan proposed prints it
`crew plan proposed <n> [--label L] --open` SHALL write the proposal, exactly as `crew plan proposed <n>` prints it, to a file on the host it runs on, and open that file in plannotator for the user to read and annotate: beside the caller with `plannotator-tui herdr open` when it runs in herdr, inline with `plannotator-tui` otherwise. It SHALL read only the drive's branch, so it works from any host. It SHALL write nothing to the branch or the run record.

#### Scenario: Opened from the rail's shell
- **WHEN** the user runs `crew plan proposed 3 --label wldn --open` in a herdr pane
- **THEN** plannotator opens beside it with the same text `crew plan proposed 3 --label wldn` prints

### Requirement: Opening a proposal needs its number and no JSON
The `--open` of `crew plan proposed` SHALL be refused without `<n>` and with `--json`.

#### Scenario: Without a number
- **WHEN** `crew plan proposed --open` is run
- **THEN** it is refused, saying `--open` needs a proposal's number

### Requirement: A proposal's card is built from the drive's branch alone
When crew raises or changes a proposal's card it SHALL read only the drive's branch and build every part of the card: its title "Plan change to <bolt or queue>: <counts>", no question and no proposal number; its summary, a sentence of what the planner proposes and why from the case; its background; its boxes and its artifacts.

#### Scenario: A closed proposal
- **WHEN** a proposal is approved or dropped
- **THEN** its card is closed or withdrawn, and crew draws no card for it again

### Requirement: A proposal's card has a paragraph for each new and dropped unit
When crew raises or changes a proposal's card it SHALL build a paragraph per new unit and per dropped unit as inline Markdown on its face, the intent and a "Direction" line from the proposal's `Do` line and case, a dropped unit's with its why.

#### Scenario: A proposal that drops, amends and adds
- **WHEN** crew raises the card for a proposal that drops one unit of bolt `y`, amends one and adds two
- **THEN** its title is "Plan change to y: 1 dropped, 1 amended, 2 new", its summary says what the planner proposes in a sentence, its face holds a paragraph for each new unit and the dropped one, and its picture is a PNG 1560 pixels wide

### Requirement: crew draws a proposal card's picture itself
When crew raises or changes a proposal's card it SHALL draw the card's picture, a PNG 1560 pixels wide at twice a phone's pixel density so it is sharp on a Retina screen, itself, with no browser, no other program and no agent.

#### Scenario: Run on a host with no browser
- **WHEN** crew raises a proposal's card on a host where no browser and no image tool is installed
- **THEN** it draws the picture all the same

### Requirement: A card asks only for its new units, in one ticked list
When proposal n makes units or chores new to a bolt or to a kit's queue, its card SHALL ask only those: one `multi` list and nothing else to tap, a box per new unit or chore, ticked, each with its intent as its detail and what clearing it does as its consequence; its intent SHALL be `decide`. No approve block SHALL sit inside the card and no question SHALL ask for words.

#### Scenario: One dropped, three new
- **WHEN** crew raises the card for a proposal that drops `a` and adds `b`, `c` and `d`
- **THEN** the card is one list of three boxes, `b`, `c` and `d`, every one ticked, with no box for `a`; its face holds a paragraph for `a`'s drop; and sending it as it stands applies the proposal whole, `a` dropped

#### Scenario: A move alone
- **WHEN** the proposal moves bolt `y` first and changes no unit
- **THEN** the card is a hold-to-approve of risk low

### Requirement: What else a proposal changes applies with its new units
What else a proposal that makes new units or chores changes, a drop, an amendment, a move, an order or a new bolt, SHALL be drawn on the card's face, its picture and its text and SHALL apply with it, and SHALL NOT be a box, and the card's summary SHALL say so. Send SHALL apply the change with the boxes as they stand, a new unit cleared left out, and the planner told which.

#### Scenario: How to object to a drop
- **WHEN** the card of a proposal that drops `a` and adds `b`, `c` and `d` is raised
- **THEN** its summary says that what it drops or amends applies with it, and no box on it keeps `a`

#### Scenario: A new unit left out beside an amendment
- **WHEN** the proposal amends `x` and adds `b` and `c`, and the user clears `c` and sends
- **THEN** `x`'s amendment and `b` are applied, `c` is left out, and the planner is told `c` was left out

### Requirement: A card of one new unit is the choice of adding it
A proposal of one new unit or chore SHALL be the choice of adding it or leaving it out instead of a list, adding it recommended, since a Pending You list holds two at least.

#### Scenario: One new unit
- **WHEN** the proposal adds one unit `c` and nothing else
- **THEN** the card is the choice of adding `c` or leaving it out, adding `c` recommended, and Send applies the side picked

#### Scenario: One new unit beside a drop
- **WHEN** the proposal drops `a` and adds `c`
- **THEN** the card is the choice of adding `c` or leaving it out, and `a`'s drop applies whichever side is sent

### Requirement: A card of more than five new units asks them five at a time
A proposal of more than five new units or chores SHALL be grouped into `questions` of at most five boxes each, in the plan's order.

#### Scenario: Seven new units
- **WHEN** crew raises the card for a proposal that adds seven units
- **THEN** the card has two questions of four and three boxes, every one ticked

### Requirement: A proposal with no new unit, or more than fifteen, has a hold-to-approve card
When proposal n makes no unit or chore new to a bolt or the queue, whether it drops, amends, moves or orders units or makes or orders bolts, alone or in any mix, or when it makes more than fifteen new, its card SHALL be a hold-to-approve of low risk, reversible, with no boxes and its change drawn on its face, its picture and its text. The card of more than fifteen SHALL say it links the proposal's plannotator session.

#### Scenario: No new unit
- **WHEN** the proposal only orders a unit first
- **THEN** the card is a hold-to-approve with no boxes, and approving it applies it whole

#### Scenario: Sixteen new units
- **WHEN** the proposal adds sixteen units
- **THEN** the card is a hold-to-approve with no boxes, and says it links the proposal's plannotator session

### Requirement: A plain approval applies whole or not at all
Approving a proposal's hold-to-approve SHALL apply it whole; declining it SHALL apply nothing. The card of a proposal that drops or amends SHALL say that declining with a note keeps what it drops or amends.

#### Scenario: Drops alone
- **WHEN** the proposal drops `a`, `b` and `c` and nothing else
- **THEN** the card is a hold-to-approve with no boxes, its face holds a paragraph for each dropped unit with its why, its summary says declining with a note keeps what it drops, and approving it drops all three

#### Scenario: Drops with an amendment and an order
- **WHEN** the proposal drops `a`, amends `x` and orders `d` first
- **THEN** the card is a hold-to-approve with no boxes, and approving it applies all three

#### Scenario: Keeping a dropped unit
- **WHEN** the user declines a drops-alone card with the note "keep b", and the planner runs `crew plan answer N plan decline --note "keep b"`
- **THEN** nothing is applied, and crew says the user's note is the planner's to act on, writing the proposal again or dropping it

### Requirement: Each answer is recorded as the proposal's card asks it
`crew plan answer <n> <question> <answer>...` SHALL record one question's answer of open proposal n's card on the host it runs on, checked against the card crew builds for the proposal: `rows-<k>` with the ids of the boxes the user left ticked, `rows-1` for a card of one list, and for a lone new unit the side picked; or, for a hold-to-approve, `plan` with `approve` or `decline`.

#### Scenario: Declined
- **WHEN** the planner runs `crew plan answer N plan decline` for a hold-to-approve
- **THEN** nothing is applied, the gathered answers are discarded, and crew says the user's note is theirs to act on, writing the proposal again or dropping it

#### Scenario: A box the card no longer asks
- **WHEN** the planner runs `crew plan answer N rows-1 keep:a add:b` for a proposal that drops `a` and adds `b` and `c`
- **THEN** it is refused, naming the boxes `rows-1` holds, `add:b` or `add:c`, and nothing is recorded

### Requirement: A card's change is applied once every question is answered
Once `crew plan answer` holds every question's answer of a proposal's card, it SHALL apply the change with the boxes as they stand, each new unit unticked cleared as `crew plan approve <n> --clear` clears it, the approved proposal recording each of those units as cleared, and crew SHALL close the card with what was applied; until then it SHALL apply nothing and name the questions it waits on.

#### Scenario: A card the user split
- **WHEN** proposal N adds seven units, the user sends the card's first list, and the planner runs `crew plan answer N rows-1` with its four boxes
- **THEN** nothing is applied and crew says it waits on `rows-2`; when the planner then runs `crew plan answer N rows-2` with two of its three boxes, the change is applied with the third unit left out

### Requirement: Work a bolt in flight needs is proposed into it, marked as unblocking it
Landing SHALL be part of every bolt's goal. A unit that a bolt in flight needs before it can be proven or land SHALL be proposed into that bolt, ordered ahead of the units that wait on it, and marked with the bolt it unblocks (`--unblocks <bolt>` on the `crew unit add` or `crew unit move` the proposal runs). The planner's brief SHALL say this, and SHALL say to fold into a bolt in flight the units a planned bolt holds that only serve it.

#### Scenario: A bolt can't land without new work
- **WHEN** a stage stops short telling the planner its bolt can't land until two pins agree
- **THEN** the planner's proposal adds the unit to that bolt, ahead of the units waiting on it, marked as unblocking that bolt, and the user reads the mark on the proposal

#### Scenario: The planner's brief on unblocking work
- **WHEN** the planner's brief is printed
- **THEN** it says to propose work a bolt in flight needs into that bolt, marked `--unblocks`, and to fold into it the units of a planned bolt that only serve it

### Requirement: Unblocking work is refused outside its bolt and marked on the proposal
crew SHALL refuse a proposal that marks a unit as unblocking a bolt in flight but places it in the queue or in another bolt. `crew plan proposed <n>` SHALL show the mark beside the unit.

#### Scenario: Unblocking work placed elsewhere
- **WHEN** a proposal marks a unit `--unblocks biome-follows-the-shell` but adds it to the queue or to a new bolt
- **THEN** writing the proposal is refused, naming the bolt in flight

### Requirement: crew plan proposed lists the open proposals from any host
`crew plan proposed` SHALL list the open proposals from any host, each with its number, who wrote it, when, the first line of its case and what it waits on.

#### Scenario: Nothing open
- **WHEN** no proposal is open
- **THEN** `crew plan proposed` says so

### Requirement: A proposal's page gives each change in plain words over its command
`crew plan proposed <n>` SHALL print the case and then each change in plain words: a new unit's intent beside the sources it rests on and the goal of the bolt it would join, a move's bolts with their goals, a new bolt's goal, a drop's reason. Under each change's plain words it SHALL print the command approval will run for that change, so the sequence of adds, moves and drops reads as the plan commands it is.

#### Scenario: A unit for an existing bolt
- **WHEN** proposal N adds a unit to a bolt in flight
- **THEN** `crew plan proposed N` shows the unit's intent and the bolt's goal beside it, and names no agreement it waits on

#### Scenario: Each change shows its command
- **WHEN** proposal N creates a bolt, adds a unit to it and moves a queued unit into it
- **THEN** `crew plan proposed N` prints under each of the three changes, in order, the `crew` command approval will run for it

### Requirement: An open proposal's page says in words that it waits on the user
For an open proposal `crew plan proposed <n>` SHALL then name, in words, that it waits on the user, without the commands that answer it. `crew plan proposed --json` SHALL give the same as its text.

#### Scenario: Waiting on, in words
- **WHEN** proposal N is open
- **THEN** `crew plan proposed N` names the user and what they would do, and prints no `crew plan approve` or `crew plan drop` command

### Requirement: A kit's rename is drawn on a proposal's card as a block of its own
A proposal holding `kit rename <old> <new>` SHALL draw it on its card as a block of its own. The block SHALL name the old name and the new, and say that the repository's work is finished and that its launches, landings and decision-record sources are renamed. Since a rename stands with no bolt or unit of the repository, the block SHALL name none, and the card's picture SHALL draw no section for it.

#### Scenario: madswan's renames proposed
- **WHEN** madswan-planner proposes `kit rename flywheel-cloud boomdrive-cloud` and `kit rename tailrace timber`, once each repository's work is finished
- **THEN** its card draws two rename blocks, each naming its two names and no bolt or unit, its picture draws nothing for either, and the card is a plain approval

### Requirement: A rename asks no question of its own
A proposal whose changes add no unit SHALL stay a plain approval, with the rename asking no question of its own.

#### Scenario: Renames alone
- **WHEN** crew builds the card of a proposal holding only `kit rename flywheel-cloud boomdrive-cloud` and `kit rename tailrace timber`
- **THEN** the card is a hold-to-approve of low risk with no boxes and no options, and its summary says to hold to apply it whole

## REMOVED Requirements

### Requirement: A proposal is a case and the commands it would run
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A proposal is one open record that is never changed" and "A proposal holds only commands that change bolts, units and chores".

### Requirement: Approval applies a proposal exactly as it was read
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "Approval applies a proposal's commands in one commit or not at all" and "An approval leaves out the new units the user cleared".

### Requirement: A proposal is dropped with a reason, or replaced
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A dropped proposal applies nothing and its card is withdrawn with the reason", "A replacing proposal drops the one it replaces and changes the chain's card to it" and "A replaced card Pending You cannot change in place is withdrawn and followed".

### Requirement: A proposal is put before the user whole
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "crew plan propose raises the proposal's card itself", "An agent shows a proposal as crew plan proposed prints it" and "An agent asks for the user's answer in words and acts only on it".

### Requirement: A proposal can be opened in plannotator
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A proposal opens in plannotator as crew plan proposed prints it" and "Opening a proposal needs its number and no JSON".

### Requirement: A proposal's card is drawn from the plan and the proposal
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A proposal's card is built from the drive's branch alone", "A proposal's card has a paragraph for each new and dropped unit" and "crew draws a proposal card's picture itself".

### Requirement: The card's questions are the approval and the new units
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A card asks only for its new units, in one ticked list", "What else a proposal changes applies with its new units", "A card of one new unit is the choice of adding it" and "A card of more than five new units asks them five at a time".

### Requirement: A card with no new unit, or more than fifteen, is a plain approval
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A proposal with no new unit, or more than fifteen, has a hold-to-approve card" and "A plain approval applies whole or not at all".

### Requirement: A card's answers are gathered before the approval
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "Each answer is recorded as the proposal's card asks it" and "A card's change is applied once every question is answered".

### Requirement: Work a bolt in flight needs goes into that bolt
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "Work a bolt in flight needs is proposed into it, marked as unblocking it" and "Unblocking work is refused outside its bolt and marked on the proposal".

### Requirement: A proposal is read as the user would read it, waiting on the user alone
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "crew plan proposed lists the open proposals from any host", "A proposal's page gives each change in plain words over its command" and "An open proposal's page says in words that it waits on the user".

### Requirement: A proposal's card draws a kit's rename
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A kit's rename is drawn on a proposal's card as a block of its own" and "A rename asks no question of its own".
