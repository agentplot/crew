## MODIFIED Requirements

### Requirement: A session is started for a card's row by its key
crew SHALL start a plannotator reading session when it raises a batch's card, on the batch's folder, the reviewer's summary whole and every unit's whole change as read at its commit, given as one review, on the drive's main level's host; when it raises the card of a proposal with more than fifteen new units, on the proposal's page; and when it raises a bolt's landing card, on what the bolt brings to main, on the team's host; it SHALL put the session's link in the card's words first and among its links. The session SHALL offer an Approve button and SHALL NOT open a browser on the host. `crew card session <key>` SHALL print the running session's link for such a key again, and SHALL refuse any other key, saying that card has nothing to read. A batch card posted before one card per batch was built, keyed `batch/<n>-<k>`, SHALL keep its sessions as they were until its card closes.

#### Scenario: A batch card's session
- **WHEN** crew raises batch 3's card on the main level's host, for a batch of `x` and `z` from two teams' hosts
- **THEN** one plannotator session is running there on the batch's summary and both units' changes, no browser has opened, and the card carries a link of the form `http://<host's tailnet name>:<port>`

#### Scenario: A unit named with a batch's key
- **WHEN** the planner runs `crew card session batch/3 x`
- **THEN** it is refused, saying a batch has one reading session, on the whole batch, and no session is started

#### Scenario: A batch card posted under an old key
- **WHEN** the planner runs `crew card session batch/2-2 x` for an open card of batch 2 posted under that key before this change, and `x` is among its units
- **THEN** the session on `x`'s change runs as before on `x`'s team's host, and its link is printed

#### Scenario: A proposal card's session
- **WHEN** crew raises the card of proposal 4, which adds sixteen units
- **THEN** a session is running on proposal 4's page as `crew plan proposed 4` prints it, and the card carries its link

#### Scenario: A review card's session
- **WHEN** swb-1-conductor runs `crew card session review/x/abc1234`
- **THEN** it is refused as not a card key, since there is no review row, and no session is started

#### Scenario: A verify report's key
- **WHEN** swb-1-conductor runs `crew card session verify/x/20261013-1200`
- **THEN** it is refused, saying no row of the rail has that key, and no session is started

#### Scenario: A landing card
- **WHEN** crew raises bolt `y`'s landing card on swb-1's host, mac-studio, once `y` reads proven
- **THEN** one plannotator session is running there on what `y` brings to main, no browser has opened, and the card carries a link of the form `http://<host's tailnet name>:<port>`

#### Scenario: A landing card's session asked for again
- **WHEN** swb-1-conductor runs `crew card session land/y` while that session runs
- **THEN** the command prints the same link, one session runs for `land/y`, and its files are not written again

### Requirement: A session is started only where its link can be answered
crew SHALL start no session, and SHALL say why, when the key is no row's or the row has nothing to read, when the batch's session would run on any host but the main level's, when a landing's session would run on any host but the one its bolt's work runs on, as the runner that took it reported, when a landing's bolt is not started or does not read proven, when the document is not on the host the session would run on or crew cannot read it whole, and when plannotator gives a link that names the host only for itself (`localhost` or a loopback address), ending that session.

#### Scenario: A key whose row is gone
- **WHEN** the planner runs `crew card session batch/3` after batch 3's card was closed
- **THEN** it is refused as a key with no row, and no session is started

#### Scenario: A batch's session on another host
- **WHEN** wldn-ops on the box runs `crew card session batch/3 --label wldn`, and the drive's main level is on mac-studio
- **THEN** it is refused, naming mac-studio, and no session is started

#### Scenario: A landing's session on another host
- **WHEN** the planner on mac-studio runs `crew card session land/y --label wldn`, and the runner that took `y`'s work runs on the box
- **THEN** it is refused, naming the box as where `land/y`'s reading runs, and no session is started

#### Scenario: A landing card
- **WHEN** wldn-ops runs `crew card session land/y` while unit `b` of `y` has not merged
- **THEN** it is refused, saying `y` does not read proven and why, so its landing card is not raised and has no session

### Requirement: A session whose card is closed or whose row is gone is ended on every rail read
Each time `crew rail` runs, and each time the host's follower refreshes after a state tip or a kit it read has moved, whether swancloud's job or a rail tab runs it, crew SHALL end, on every host of each drive read, each session it started for a card key whose row is gone, or whose card the run record holds as closed with no card open under the key. A refresh after no state tip and no kit moved SHALL sweep sessions only on a host whose card readings folder moved since its last read, as the follower's check last asked it, or that the last refresh could not check, and on no other host. It SHALL end only sessions it recorded, and only a process plannotator lists as serving the recorded document.

#### Scenario: A verify card's session from before
- **WHEN** the session crew started for `verify/x/20261009-1412`, before a verify report had no row, still runs on chuck-herdr-alpha
- **THEN** the next `crew rail`, run on mac-studio, ends that session, since no row has its key, and its link no longer opens

#### Scenario: A proposal approved in the app
- **WHEN** the user approves proposal 4 on its card, the planner runs `crew plan approve 4` but its session lost Pending You's tools before it closed the card
- **THEN** the next rail read ends the session for `proposal/4`, since its row is gone

#### Scenario: A card closed while its row stays
- **WHEN** the planner closed card `proposal/4` with `ack_answer`, its hook could not end the session, and proposal 4 is still open
- **THEN** the next rail read ends that session

#### Scenario: A row with no card yet
- **WHEN** the planner started the session for `proposal/4` and has not yet posted its card
- **THEN** a rail read leaves the session running

#### Scenario: A session crew did not start
- **WHEN** the user runs plannotator by hand on a closed proposal's page on mac-studio
- **THEN** no rail read ends it

#### Scenario: A batch card's sessions on another host
- **WHEN** the planner closed card `batch/3-1` on mac-studio, and the session for its unit `y` still runs on chuck-herdr-alpha
- **THEN** the next rail read ends `y`'s session there

#### Scenario: Swept with no tab open
- **WHEN** the planner closed card `proposal/4` and its session still runs, and the host's follower runs as swancloud's job with no rail tab open
- **THEN** the follower's next refresh ends that session

#### Scenario: A host the last sweep missed
- **WHEN** the follower's last refresh could not check chuck-herdr-alpha's sessions, and nothing has moved since
- **THEN** the next refresh asks chuck-herdr-alpha alone to end its sessions, and asks no other host

#### Scenario: A reading sent on one host
- **WHEN** the user sends back a reading on chuck-herdr-alpha, and nothing else has moved since mac-studio's follower last read
- **THEN** the follower's next refresh that asks chuck-herdr-alpha, at the next move there or within ten minutes, asks chuck-herdr-alpha alone to sweep its card sessions, and asks no other host

### Requirement: The rail says which sessions it ended
After its groups and its open cards with no row, `crew rail` SHALL list each session it ended on that read, with its card key, the unit for a batch card's, its drive, its host and whether its card was closed or its row gone, and SHALL name each host whose sessions it could not check, with why. When it ended nothing and checked every host, it SHALL print nothing about sessions.

#### Scenario: Two sessions ended
- **WHEN** a rail read ends the sessions of `proposal/4` and `batch/3`
- **THEN** the rail lists both, each with its host and why it was ended

#### Scenario: Nothing to end
- **WHEN** every recorded session's row and card are open
- **THEN** the rail says nothing about sessions

### Requirement: A session crew can't judge is kept
A rail read SHALL end no session whose row or card it cannot tell: none on a host that does not answer, which it names; no session for a card closed, and no batch card's, while the drive's run record cannot be read from its branch; and no session started less than two minutes before its host is checked, which a later read judges. A host that does not answer SHALL keep only the sessions on it: a card it posted or closed SHALL be judged from the branch like any other.

#### Scenario: The team's host is asleep
- **WHEN** chuck-herdr-alpha does not answer
- **THEN** the rail ends no session there, names chuck-herdr-alpha as not checked, and ends what it can judge elsewhere

#### Scenario: The record is read in part
- **WHEN** the drive's branch cannot be read
- **THEN** the rail ends no session for a card closed and no batch card's session, and still ends a session whose proposal's row is gone

#### Scenario: The host that closed a card is asleep
- **WHEN** a card the planner closed on macbook-pro is on `wldn/main` as closed, its session runs on mac-studio, and macbook-pro does not answer
- **THEN** the rail ends that session on mac-studio, its card read as closed

#### Scenario: A session just started
- **WHEN** the planner starts a session for a proposal opened after the rail's read began
- **THEN** that read leaves it running
