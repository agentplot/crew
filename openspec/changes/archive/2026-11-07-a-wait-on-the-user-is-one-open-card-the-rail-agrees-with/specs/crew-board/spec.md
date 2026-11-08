## MODIFIED Requirements

### Requirement: Each holder is read from what crew already keeps
Every holder of a bolt's time SHALL be read from what crew already keeps, and nothing SHALL be recorded to make the reading:

- **Stages**: the run record's stage starts and ends for the bolt's work since the give.
- **Submissions**: sluice's overview, as the follower's watch or one ask of it printed it, and what the follower kept of each submission from it: the number and where it came from, when it was submitted, when its checks began where a candidate testing it gave that, and when it was decided, from the recent events of the line that no longer held it. A landing on main is the bolt's when it came from `bolt/<bolt>`, from a pull request opened from it, or when its number is the one the run record's queued `bolt.submit` of the bolt names. No gather SHALL read sluice's record of a branch's submissions; a read made once at an act, as the landing's, MAY.
- **Cards**: the run record's card posts, changes, answers and closes. A card holds the bolt for the user from its post until the user's answer on it or its close, whichever comes first. A card is the bolt's when:
  - it is under the bolt's own key, `land/<bolt>`;
  - it is a batch's card holding work of the bolt's;
  - it is a proposal's card whose changes name the bolt or its work;
  - it is the kit's landings card while its last post or change names the bolt among its rows, from the later of that post or change and the end of the bolt's last merge;
  - it is a question an agent of the bolt's team asked the user while the team held the bolt;
  - or its post names the bolt or its work.
  A question of a main-level role's that names neither the bolt nor its work is no card of the bolt's.
- **Holds**: the run record's hold of the team's host, from its hold to its go.

#### Scenario: The user's card
- **WHEN** every unit of `b` has merged, nothing runs, and its kit's landings card has been open for an hour
- **THEN** that hour is the user's, and the line says the user holds `b` since the card's post, naming its key

#### Scenario: A question from the team
- **WHEN** swb-4's unit stopped short and swb-4-conductor's question to the user is open, with nothing of its bolt running
- **THEN** the minutes since its post are the user's

#### Scenario: A held host
- **WHEN** nothing of `b` runs and no card of it is open, while its team's host was held by the user at 14:02 and not yet let go
- **THEN** the minutes since 14:02 are the hold's, and the line says `b` is held since 14:02 because its host is held, naming who held it

#### Scenario: A row drawn from the overview
- **WHEN** the follower's watch of switchboard-kit prints a line holding `b`'s merge `#41` under test since 14:05 and recent events naming `#40` landed at 13:58
- **THEN** `b`'s head line counts `#41` the kit's since 14:05 and `#40` decided at 13:58, read from that line and what the follower kept, with no sluice process started

#### Scenario: A landing by pull request
- **WHEN** main's recent events name `#52`, from `pull/9`, landed, and the run record's queued `bolt.submit` of `b` names `#52`
- **THEN** `#52` is `b`'s landing

#### Scenario: The user answered the landings card
- **WHEN** `b`'s kit's landings card, posted at 14:00 with `b` among its rows, was answered by the user at 14:40, and ops has not yet submitted `b`
- **THEN** 14:00 to 14:40 are the user's, the minutes after 14:40 are nobody's, and the line does not say the user holds `b`

#### Scenario: A landings card that no longer carries the bolt
- **WHEN** `b`'s kit's landings card was changed at 15:00 to rows that no longer name `b`
- **THEN** the minutes after 15:00 are not the user's for that card

#### Scenario: A main-level question about something else
- **WHEN** agentplot-design's question `ask/agentplot-design/sluice-who-claims` has been open since 19:01, its post naming the asker alone, and nothing of flume's bolt `f` runs
- **THEN** none of `f`'s minutes since 19:01 are the user's for that question, and `f`'s line names no such question

## ADDED Requirements

### Requirement: An agent's band says which of its cards the user answered
Among the cards `board.agent_views` gives an agent's band, a card whose answer the run record holds SHALL say it was answered and how long ago, and that it is the agent's to act on, in place of how long it has been open. Main-level ops's band SHALL say on a kit's landing line that its card is answered and the landing is ops's. crew's mod SHALL draw both as the views give them.

#### Scenario: The planner's answered proposal card
- **WHEN** `proposal/57`'s card is wldn-planner's, open, and the run record holds the user's answer on it from five minutes ago
- **THEN** wldn-planner's band shows `proposal/57` answered 5m ago, yours to act on, and not open

#### Scenario: Ops's answered landings card
- **WHEN** `land/sluice`'s card is agentplot-ops's and the run record holds the user's answer on it
- **THEN** agentplot-ops's band shows the card answered, and its `land/sluice` line says the landing is ops's

#### Scenario: The mod draws an answered card
- **WHEN** the views give agentplot-ops a card line saying `land/sluice` was answered 5m ago, its to act on
- **THEN** crew's mod draws that line above ops's view as given
