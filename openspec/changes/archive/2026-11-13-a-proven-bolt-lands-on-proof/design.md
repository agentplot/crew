# Design

## Context

**What lands a bolt today.** A started bolt lands only by a `land` of its launch that crew posts, and crew posts one only on the user's send of its row on its kit's landings card (`plan.16`, record 0056 point 3). The path:
- The rail reads a bolt that can land from the runner's report and the run record (`rail_rows`). It can land once every unit and chore has merged, every unit's latest change has been in a batch the user answered, its verification is green, no fix is in flight, and no refusal or conflict is recorded at its head.
- The raise of the kit's landings card (`raise_landings`, `landings_raised`) reads each started bolt's row on its host (`land_row`). It forecasts every row that can land against GitHub's main and records each conflict (`main_told`), so a row in conflict takes main first. It posts the lands the user's sends make due (`lands_post`, `lands_change`, `runner.lands_due`), by one plan write in main-level ops's name, each recorded as `bolt.submit` with `Card`, `Head`, `Request` and `Outcome: asked`. Then it decides what the card does (`landings_step`): post, change, follow, withdraw, leave or close.
- The raise runs on the main level's host, where ops's cards are. Events hand it there (`land_hand`): a bolt's close, a leave, a reading opened, a preview's change. The rail's read raises it too (`sweep_moved`), for a card main moved under, one whose answer the sweep recorded, and one that does not offer a row as it stands (`landings_unoffered`). The sweep raises a row with no card (`sweep_judged`).

Nothing of crew's makes a bolt proven: the rail reads the proof from the runner's report. So the rail's read is the first act that can see a proof on the main level's host.

**What it cost, and what the user decided.** Bolts proven overnight on wldn's switchboard-kit waited 400 to 1,055 minutes for a card and the user's send (record 0067's sources). The user decided on 2026-11-12 that a proven bolt lands on proof, and that a bolt they keep working on is marked ahead of time to stay (record 0067, accepted). agentplot-design chose the rest of record 0067: the card tells and asks only about marked bolts; the mark is the plan's and the user lifts it; every drive lands on proof, with no setting; and a hold the user put on the drive or the kit stops it. `plan.16`, `briefs.11` and `state.3` carry the amendment.

**What crew holds today of a hold.** Nothing at a drive's or a kit's level.
- `crew hold <host>` holds a host's agents, not a drive's landings, and a drive's kits run on several hosts.
- The code pause of 2026-11-12 was Flume holds of single places, put by agentplot-ops.
- The plan's spec already allows "any hold on it" (bolt-plan), and `state.2` names a `Hold` mark as not ruled out once built.

**The family.** The landing itself is the runner's and Flume's: crew posts `land`, the runner carries it, and Flume submits the base place through sluice (record 0056; `roles.5`). What decides when to post a land is crew's alone. Pending You resolves an answered card when a card follows it. A card's kind never changes in place (`cards.landings_form`).
- **Flume** holds a place's stage or submission and lets a caller hold the move a place waits on it for (clause 130, core.24). It holds nothing of a drive's or a repository's.
- **The runner** carries a land, a retry and a drop (`want.rs` `ActSort`) and keeps no hold of a repository's.

So the mark and the hold are crew's, kept in its plan (`state.2`, `roles.5`), and no other tool changes.

Record 0067's amendment of 2026-11-14 gives a proven bolt that waits on the user words that name what it waits on, carried to Flume as a hold of its base place's waiting move. That is a crew unit of its own, after Boomdrive's runner takes `hold`. This change neither builds nor blocks it: with landing on proof, fewer proven bolts wait on the user at all.

**Area pages this change touches:**
- `core.md`: `state.2`, `state.3`, `roles.1`, `roles.2`, `roles.3`, `roles.5`, `read.1`, `code.4`, `code.7`, `code.8`, `code.9`, `code.11`.
- `plan.md`: `plan.1`, `plan.3`, `plan.8`, `plan.16`, `plan.21`.
- `briefs.md`: `briefs.11`, `briefs.12`.
- `record.md`: `record.1`, `record.3`.
- `docs.md`: `docs.2`, `docs.6`, `docs.7`.
- `tests.md`: `tests.4`, `tests.11`.

No rule changes, so no page is edited (`docs.7`).

## Goals / Non-Goals

**Goals:**

- A proven bolt not marked to stay lands at the first rail read on the main level's host that reads it proven, at any hour, crew posting its land in ops's name with no agent and no user.
- A bolt the user means to keep working on is marked when it is planned or started, waits for their send, and lands on its next proof once they lift the mark.
- The landings card asks only about what a send must land, and tells the user each bolt that landed on proof.
- A hold the user puts on a drive or a kit stops every land, on proof and on a send, until they lift it.

**Non-Goals:**

- Words for a proven bolt that waits on the user, carried to Flume as a hold (record 0067's amendment of 2026-11-14): a unit of its own.
- A hold that stops anything but landings: launches, starts and stages go on under it. A later change may widen it, and its name leaves room.
- A setting per drive for landing on proof: record 0067 puts the choice on the bolt.
- A change to how a send lands a marked bolt or a fix of main: `lands_due` and `landings_step` keep their rules for the rows the card asks about.

## Decisions

### 1. The raise posts the land on proof, after the forecast and the sends' lands

A bolt is due a land on proof when its row can land, its forecast is clear of main, and every one of these holds:
- it is not marked to stay;
- the user has not left it;
- no land of it is posted at its head now, nor stands undecided or unknown;
- no land of it posted on proof at its head now was stopped;
- no hold stands on its drive or its kit.

The raise posts these lands, because the raise is where the forecast against GitHub's main is made (`plan.8`): a bolt's row reads clear of main only once that forecast found no conflict. A forecast against main that could not be made, git not telling, is no clear forecast (`read.1`): no land on proof is posted for that bolt, the raise says why, and the next read raises the kit again, the bolt being still due. The order in `landings_raised`:
1. Forecast every row that can land, as today, marked or not. A conflict found is recorded and the row takes main first, as today.
2. Post the sends' lands, as today.
3. Post the lands due on proof, in the plan's order, by one plan write in ops's name, the card's owner. Each is recorded as `bolt.submit` on `bolt/<bolt>` with `Outcome: asked`, `Form: proof`, `Head` and `Request`, and no `Card`. The write's subject is `plan(<kit>): land <bolts> on proof`.
4. Decide the card from the rows it asks about (Decision 3) and the bolts it tells (Decision 4).

`runner.lands_due` decides which proof lands are due, as it does a send's. The proof rows come to it as a send of their own, keyed by no card, so its rules hold: one land per head, none while one stands undecided or unknown, none once one at that head was stopped. Its stop rule reads the stopped land's head for proof: a stop at an old head holds nothing at a new one.

A stop holds no send of the user's at that head. Where a row's last land, stopped at its head now, was posted on proof or on another card's send, a send ticking the row there is due its land: the stop is nothing of the bolt's and no fix moves its head, so only a send lands it. The send that posted the stopped land is spent, at that head or any, as rail-cards "A landing the runner or Flume stopped keeps its box" has it. So the card that follows a spent send, which asks for the bolt again at the same head, lands it on its own send, and a stopped land on proof is landed by the first send that ticks it (rail-cards "A landings row is due one land for each send and head", modified here).

`lands_change` re-checks at the tip it is applied to (`plan.1`): a hold standing there on the kit or its drive posts nothing, on a send or on proof, and a land on proof is posted only for a bolt the plan there still holds and does not mark to stay.

`plan.lands_by(row, stays, left, stopped, hold)` is a decision of facts alone (`code.7`). It says how each row lands: `"proof"`, `"send"` or `"hold"`.
- A bolt marked to stay, one the user left, and one whose land on proof at its head was stopped land on the send.
- A fix of main lands on the send, always (`state.3`).
- A bolt that would land on proof while a hold stands reads `"hold"`.
- Every other bolt lands on proof.

`landings_raised` and the rail's line (Decision 6) both read it, so they agree.

Not taken:
- **A stop barring every later land at its head**, as `lands_due` read a land posted at a head before. A stopped land on proof would then hold its bolt for good, and a card following a spent send would ask for a bolt its send could not land.
- **The rail's read posting the land itself**, with no raise. It makes no forecast against GitHub's main, so it could land a bolt that conflicts with what main has since landed. `plan.8` rules that out.
- **A land on proof posted at a new head after a stop**, the bolt never asked about. A stop is nothing of the bolt's, and no fix moves its head, so it would wait forever. Decision 3 asks the user instead.

### 2. The rail's read raises each kit with a bolt due a land on proof

`plan.proof_due(row, stays, left, posted, hold)` decides it from the land row and the run record (`code.7`): a bolt that can land, not marked, not left, with no land posted at its head now (`lands_posted`), on a kit and drive with no hold.

`plan.landings_proven(read, label, here, kits)` applies it on the main level's host to every kit's land row, whether a card is open or not. `sweep_moved` raises each such kit once, after those main moved under, those answered and those unoffered. Its result's `raised` entries carry `proven`, the bolts a kit was raised for alone.

The cost:
- A read that finds no bolt due raises nothing more than today (`plan.12`).
- A bolt whose land is posted reads asked on its line, so it is due no more.
- A bolt the raise's forecast finds in conflict has its conflict recorded, so the rail reads it unable to land and raises it no more.

Two existing readers change with it:
- `unoffered` counts only the rows a card asks about. A bolt that lands on proof is never a row the card should show, and one waiting on a hold is neither due nor asked about, so no read raises a card for either.
- `sweep_judged` owes a land row a card only while it holds a row the card asks about or a bolt to tell (`asks` on the row). Otherwise a row of bolts that land on proof would be raised by the sweep on every read, each raise changing nothing.

`sweep_sessions` opens a reading only for a row the card asks about, since a bolt that lands on proof has no card row to link it from.

Events go on raising the card through `land_hand`. Two new ones hand a raise too: `crew bolt unstay`, for a started bolt, and `crew plan go`, for each kit it held.

Not taken: a raise handed from the act that reads the proof. No act of crew's makes the proof, and the runner's report is read by the rail.

### 3. The landings card asks only about the rows a send must land

The card's rows are the rows `lands_by` reads `"send"`: bolts marked to stay, bolts the user left, bolts whose land on proof at their head was stopped, and fixes of main. Beside them, as today, sit their rows taking main first and their rows held with no box (`card_rows`, `landings_step`). A bolt that lands on proof, or waits on a hold to land on proof, is no row.

So `landings_step`, `card_rows`, `cards.landings_card` and every rail-cards requirement on a row keep their rules, applied to these rows. The spec says so once (rail-cards "A landings card asks only about the rows a send must land"), so its many scenarios about a row stand as they are.

A bolt not marked to stay that the user left, from a card open when this lands or by `crew bolt leave` on their words in ops's pane, stays a row until they tick it, as rail-cards "A bolt the user left stays left until they tick it" has it. A leave is their word to stop it, and proof is no word over theirs.

A row whose last land, stopped at its head, crew posted on proof (`stopped_on_proof`, from the run record's entries) says so: "Its land on proof at <head> was stopped, nothing of the bolt's: <words>. Ticked, it lands on this send." No send of the user's made that land, so none is spent by it: `landings_step` reads such a row as stopped by nothing of the send's, and the user's send of it lands it, or stands under a hold, rather than closing the card as a send spent. `crew card read` says the same of it.

**Departure** from record 0067's words "the card asks only about marked bolts", agentplot-design's choice. The card also asks about a bolt the user left and one whose land on proof was stopped:
- The leave is the user's own stop, and landing it on proof would override it.
- A stop holds the bolt at a head no fix moves, so only a send can land it. It keeps its box, as rail-cards "A landing the runner or Flume stopped keeps its box" already has.

Each is cheap to change, and the design agent may rule otherwise.

### 4. A bolt that landed on proof is told on its kit's landings card

`plan.told_on(entries, key, owner, kit)` is a decision of facts alone (`code.7`). It returns `[(bolt, commit, at)]`, the bolts of the kit that landed on proof and that no card the user answered or tapped told. Its inputs:
- each `bolt.land` of the kit not refused, whose bolt's newest land before it, at the head that landed, was posted on proof (`Form: proof`);
- the card's post and change entries, which record each told bolt among `Heads` as `<bolt>@<commit>:landed`;
- the user's answers and closes of those cards.

A told bolt is spent only by the user's answer or tap of a card that told it. A card followed or withdrawn before they saw it leaves its told bolts to the next card.

The card's form follows (`cards.landings_form(n, told)`):
- **`tell`**: no row to ask about and a bolt to tell. A one-tap notice, `kind: fyi`, `intent: tell`, urgency `whenever`, as a batch's card is. Its title is `Landed on <kit>'s main: <bolts>`. It names each told bolt with the commit main holds after it and when, and asks nothing.
- **`approve`** or **`multi`**: as today, by how many rows it asks about. Its face and opening name the told bolts first, then its rows.

`landings_step` gains told:
- No row and something to tell: post the notice, following the kit's last card where one is open, or change the open notice in place as more land.
- A row joins while the notice is open: follow it with the asking card, since a card's kind does not change in place.
- An asking card waiting on the user when a bolt lands on proof: change it in place, its note naming the bolt.
- An answered card: left, as today. What it did not tell goes to the card that follows it.
- The user taps the notice: it closes, and with no row to ask about, no card follows.
- With neither a row nor anything to tell, the step is today's `none` or `withdraw`.

The rail's land row is raised while a bolt is told (crew-rail "A kit's row under land holds the bolts its card tells"). `rail_record` reads `told` for each kit's key from the drive's run record, and `rail_rows` makes the row from it, so the sweep owes it its card (`asks`).

Not taken:
- **A heads-up card of its own**, under a new key such as `landed/<kit>`. `briefs.11` has the kit's landings card tell, and one key per kit keeps the card's rules in one place, its lock and its follows among them.
- **The tell said only on the next asking card.** With no marked bolt, the user would hear nothing, and record 0067 asks for a heads-up.

### 5. The mark to stay is the plan's, set at planning or start, lifted by the user

The plan's `Bolt` descriptor allows `Stays`, `%type: Stays enum yes`, brought in step on each branch's next write (`in_step`).
- `crew bolt new … --stays` sets it in the write that plans the bolt.
- `crew bolt start <bolt> --stays` sets it in the write that starts it, a start run again on a refused launch among them, nothing having been built then.
- Each runs by its own hands: a proposal, or the user (`roles.1`, `may_write`).
- No other command sets it. So the mark is set ahead of time and never after the bolt is proven (record 0067), with no read of the kits needed to refuse a late mark.

The proposal card says of each such command that the bolt stays unlanded until the user's send, so they approve the mark knowingly (`cards.proposal_rows`, `drawn`).

`crew bolt unstay <bolt>` lifts the mark, recording `bolt.unstay` on `bolt/<bolt>`. The user runs it, or a proposal holds it, as `crew bolt start` (`may_write`). Any agent running it directly is refused, naming the planner: a lift lets a land be posted, and no agent's judgment lands a bolt (`roles.2`). It is refused for a bolt not marked. Its after-act hands a raise of a started bolt's kit card to the main level's host, so the bolt lands on its next proof, at once where it is proven already.

Not taken: **`crew bolt stay <bolt>` on a started bolt not yet proven.** Record 0067 says the mark is set when the bolt is planned or started. A bolt started before this change lands on proof once proven, unless the user puts a hold on its kit or leaves it (Migration).

### 6. A hold on a drive or a kit is a Hold record of the plan

The plan gains a record set, `Hold`:
- `%allowed: Kit Why`, `%mandatory: Why`.
- One with no `Kit` holds the whole drive.
- `HEADER` declares it first, ahead of the Bolt and Unit sets, so a record added at the file's end, by a hand or a tool, is still read as a Unit, and a hand edit's duplicated Unit is refused as a duplicated key (bolt-plan "A plan that fails its schema").
- crew refuses a second Hold on one kit, or two on the drive, at every write (`check`, `plan.1`) and at every read of the plan (`read`), since recfix's `%unique` is per record and passes two (bolt-plan "Two holds on one kit"). Both call `holds_once`.
- `in_step` brings a branch's descriptors in step, as it does the Bolt's, and a plan declaring no Hold set takes crew's ahead of its first set (`holds_declared`).
- `crew kit rename` renames a Hold's `Kit` with the rest (`plan.22`; bolt-plan "A rename renames every record a reader matches the repository by"), so a hold on a renamed kit still holds it.
- `Plan.holds()` reads them, and `plan.hold_on(plan, kit)` gives the hold standing on a kit: its own, or the drive's.

The plan holds marks of the user's intent (`state.2`; bolt-plan's "any hold on it"), and its words are text the plan may hold where the run record may not (`record.3`).

`crew plan hold "<why>" [--repo <kit>] [--excerpt "<the user's words>"] [--label L]`:
- puts the hold, or changes the words of one standing on the same kit or drive;
- records `plan.hold` on `kit/<kit>`, or on `plan/<label>` for the drive, holding none of the words;
- is refused for a kit the drive does not name, as `crew bolt new --repo` is;
- hands no raise, since a hold changes nothing on a card.

`crew plan go [--repo <kit>] [--label L]`:
- lifts it, recording `plan.go`, refused where no hold names the kit or the drive, naming the drive's hold where only that stands;
- hands a raise of each card it held, so what came due meanwhile is posted at once: the kit's, or for the drive's hold each kit of the drive (`Write.kits`, its plan's and its landings'), a kit whose card holds only a fix of main among them, but one a hold of its own still holds.

Who runs them (`may_write`):
- **The user** runs both.
- **Main-level ops** puts a hold only with `--excerpt`, the user's words in its pane, read in its own session's transcript as the user's, as `crew bolt leave` reads them (`acts.heard`), refusing otherwise. It lifts none: a lift lets lands be posted, and no word in a pane lands anything (main-level "The user's words in ops's pane are no word to land").
- **The planner and the design agent** are refused, naming the user and ops.
- **A proposal** holds neither: they are not plan commands of bolts and units (plan-proposals), so `PROPOSABLE` leaves them out.

While a hold stands, the raise posts no land, not a send's and not one on proof. A send made meanwhile stands, its lands posted by the first raise after the lift, since `lands_due` reads it as it stands then. `crew card read land/<kit>` says the send stands until the hold is lifted.

The card itself is raised as ever. It asks about the rows it asks about, a send standing over the hold, and says nothing of the hold, since the user put it. The rail and the bands say the hold (Decision 7). An answered card that closes or is followed under a hold says the user's send stands for the bolts it would land, no land being asked while the hold stands, never that they were asked of the runner (`landings_step`'s `hold`). `crew card read` reads the hold for an earlier card's send as for its own.

Not taken: **Hold declared after Unit.** recutils puts a record under the descriptor before it, so a unit appended at the file's end would be read as a Hold, refused as one lacking `Why`.

Not taken:
- **The host's hold.** `crew hold` holds a host's agents, and a drive's kits run on several hosts.
- **A hold kept as run-record entries alone.** Its words could not be kept (`record.3`), and a hold is intent, the plan's (`state.2`).
- **A `land hold` command family.** The record names "a hold on the drive or the kit", and `crew plan` is where crew's commands of a drive's intent are.

### 7. The rail and the bands say how each bolt lands

`rail_rows`:
- Each land row's `bolts` carry `stays`, besides `bolt`, `host`, `can` and `head`.
- A bolt that can land says how, from `lands_by`: that it lands on proof, crew asking the runner to land it in ops's name, with its land's request once posted; that it stays, lands on the user's send, was left, or that its land on proof at that head was stopped, in the runner's or Flume's words; or that the hold on the drive or the kit holds it, with the hold's words.
- The row carries `told`, each told bolt with its commit, and `asks`, whether its card has a row to ask about or a bolt to tell.
- `rail_text` ends each bolt's line with its time (`land_times`) and draws each told bolt's line after them as it is, so `crew rail` and the rail tab show every told bolt.

The board's data of a started bolt carries `stays`, and a drive's carries `holds`, each `{kit, why}`. `board.agent_views` draws both (`code.8`):
- `bolt_row` says `stays` beside a marked bolt's name, and so does ops's line for a bolt whose landing is in flight with no land row.
- `planner_view` and `ops_view` open with a line for each hold: what it holds, its words, and that no land is posted until the user lifts it with `crew plan go`.

The views stay lists of `(text, style)` segments, so `plugin/hooks/status.js` reads no new key and is unchanged. `tests/py/test_board.py` pins the new lines.

### 8. The briefs and the docs

Main-level ops's brief (`main-ops.md`, *Landing a bolt*) says:
- a proven bolt not marked to stay lands on proof, crew posting its land in ops's name at any hour, so ops runs nothing for it;
- the landings card asks only about bolts marked to stay, bolts the user left, bolts whose land on proof was stopped, and fixes of main, and tells the user each bolt that landed on proof;
- a hold is put on the user's words in its pane with `crew plan hold … --excerpt`, and ops lifts none, telling the user that `crew plan go` is theirs.

The planner's brief (`planner.md`) says:
- a bolt the user wants to keep working on after it is done is marked on their word, by `--stays` on the proposal's `bolt new` or `bolt start`;
- the mark is lifted by a proposal holding `bolt unstay`, or by the user;
- the planner puts no hold.

README, `plugin/skills/crew/SKILL.md` and `crew`'s usage header say the same, and name `crew bolt unstay`, `crew plan hold` and `crew plan go` (`docs.2`). Each new command answers `-h` and `--help` with its usage (`code.11`).

### Rules relied on

- `plan.16` and `state.3` as record 0067 amends them: proof is the word to land a bolt not marked to stay; the send lands a marked one.
- `briefs.11` as record 0067 amends it: the landings card asks only about bolts marked to stay and tells the rest.
- `briefs.12`: a bolt is proven only once every unit's latest change has been in a batch the user answered.
- `plan.8`: a bolt is forecast against main before it lands, and lands on none while it conflicts.
- `state.2`: the plan holds intent and its marks, the mark to stay and the holds among them.
- `roles.1`, `roles.2`, `roles.3`:
  - who writes the mark, the lift and the holds is crew's check (`may_write`), not a brief's word alone;
  - no agent's judgment lifts a mark or a hold;
  - ops's hold rests on the user's words read as theirs.
- `roles.5`: crew decides when to post a land, and the runner and Flume land it.
- `read.1`: a bolt crew can't read lands on nothing, and a told bolt is never guessed.
- `record.3`: no entry holds a hold's words or the user's.
- `code.4`: the mark's value and the hold's kit match crew's names.
- `code.7`: `lands_by`, `proof_due`, `told_on`, `landings_proven`, `hold_on`, `landings_step` and `cards.landings_form` start no process.
- `code.8`: the views draw the mark and the holds.
- `code.9`: each write answers once its commit is made and its raise handed.
- `code.11`: each new command answers its help.
- `plan.1`, `plan.3`: the new records and commands are checked on every write, `lands_change` re-checking the hold and the mark at the tip it is applied to, and proposals hold only the plan's commands of bolts and units.
- `plan.22`: a rename renames a Hold's `Kit`, a field a reader matches the repository by.
- `docs.2`, `docs.6`, `docs.7`.
- `tests.4`, `tests.11`: every case is in the logic tier but the briefs' and the docs' words, which are their end-to-end tests'.

### Departures

- From record 0067's "the card asks only about marked bolts": the card also asks about a bolt the user left and one whose land on proof was stopped (Decision 3).
- No rule is departed from.

## Risks / Trade-offs

- **[A bolt lands that the user meant to keep, started before this change]** → it carries no mark and lands on its next proof. The user stops it with a hold on its kit, or with their words in ops's pane (`crew bolt leave`), as the Migration plan has it.
- **[The rail's follower is not running on the main level's host]** → no read raises a proven bolt, and it lands at the next event's raise, a close or a lift, or at the next read. That is today's cost for every card, not a new one.
- **[A raise refused for a kit, its row's host not answering]** → its row is left off and nothing is posted for it (`read.1`, `read.3`). The next read raises the kit again, said on the rail's text.
- **[The notice stays open while the user does not tap it]** → it gathers each landing on proof, changed in place, never a card per landing.
- **[A hold forgotten]** → no land is posted while it stands. The planner's and ops's bands open with it, so it is seen every turn.

## Migration Plan

- Bolts in the plan when this lands carry no mark, so each lands on its next proof. A bolt the user wants to keep is held by a hold on its kit until they decide, or left on their words in ops's pane. A bolt not yet started can still be marked by `crew bolt start --stays`.
- A landings card open when this lands is raised at the first read or event on the main level's host whose crew carries this change:
  - its rows not marked to stay land on proof, but those the user left and those a send still lands;
  - the card changes, follows or is withdrawn by `landings_step` as its rows now stand;
  - a send standing on it still lands what it ticked.
- A drive's `plan.rec` takes `Stays` and the `Hold` record set, declared ahead of its Bolt set, at its next write (`in_step`). An older crew reading a newer branch passes a Bolt's `Stays` and a Hold through `still_allowed` and `recfix`, as it does any field its own descriptor lacks.

## After deploy

None. Every outcome here is a logic-tier case, or the briefs' and the docs' end-to-end tests, and nothing waits on a host or on the user.

## Task notes

**1.1** `plugin/lib/plan.py`:
- `HEADER`'s Bolt allows `Stays`, `%type: Stays enum yes`, and its `%doc` says a bolt marked `Stays: yes` waits for the user's send. The header's comment names `crew plan hold` among the plan's writers.
- The parser's `bolt new` and `bolt start` take `--stays`, `store_true`.
- `op_bolt_new` adds `("Stays", "yes")` to the record.
- `op_bolt_start` sets it in its change, on a start and on a start run again.
- The usage lines in `plan.py`'s docstring and `plugin/bin/crew`'s header name the flag.

Cases in `tests/py/test_bolt_commands.py`:
- `test_a_bolt_planned_to_stay_is_marked_in_the_plan`
- `test_a_bolt_started_to_stay_is_marked_in_the_start_write`
- `test_no_command_marks_a_bolt_to_stay_later`
- `test_a_branch_from_before_the_mark_takes_it_at_its_next_write`

**1.2** `plugin/lib/cards.py` `proposal_rows` and `drawn`: the row of a `bolt new` or `bolt start` holding `--stays` says the bolt stays unlanded until the user's send. Case: `tests/py/test_proposal_card.py::test_a_bolt_planned_to_stay_says_it_waits_for_the_send`.

**1.3** `plugin/lib/plan.py`:
- `op_bolt_unstay`: refused, naming the bolt, where it is not marked. Its change drops `Stays`. Its act is `bolt.unstay` on `bolt/<bolt>`. Its `after` calls `land_hand` for a started bolt's kit.
- `OPS`, `PLAN_WRITES` and `ACTS` take `("bolt", "unstay")`.
- `may_write` refuses it for every agent, as `bolt start` is refused, naming the planner.
- The parser takes `bolt unstay <bolt> [--label L]`.

Cases in `tests/py/test_bolt_commands.py`:
- `test_the_user_lifts_a_bolts_mark_to_stay`, with the lift's `land_hand` on a stand-in;
- `test_an_agent_lifting_a_mark_is_refused_naming_the_planner`;
- `test_a_bolt_not_marked_has_no_mark_to_lift`.

**1.4** `plugin/lib/plan.py`:
- `HEADER` gains the `Hold` record set, as Decision 6 has it. `check` refuses a second Hold on a kit or on the drive, naming them.
- `Plan.holds()` and `hold_on(plan, kit)`.
- `op_plan_hold` and `op_plan_go`, with acts `plan.hold` and `plan.go` on `kit/<kit>` or `plan/<label>`, the words never in the entry (`record.3`), a kit read through `ctx.kit` as `op_bolt_new` reads it. `op_plan_go`'s `after` hands `land_hand` for the kit it names, or each kit of the drive with a started bolt.
- `PLAN_WRITES` and `ACTS` take `("plan", "hold")` and `("plan", "go")`, and `PROPOSABLE` leaves them out.
- `may_write`: the user; ops's hold only with `--excerpt`, read as `bolt_leave` reads it (`acts.heard`); ops's go, the planner's and the design agent's refused, naming the user and ops.
- The parser takes `plan hold <why> [--repo <kit>] [--excerpt <words>] [--label L]` and `plan go [--repo <kit>] [--label L]`.

Cases in a new `tests/py/test_plan_holds.py`:
- a kit held and the drive held, as Hold records, with their entries holding none of the words;
- a hold's words changed by a second hold;
- two Holds refused by `check`;
- a lift handing the raise;
- nothing to lift, naming the drive's hold;
- ops's hold with the user's words read as theirs, and with none;
- ops's go refused;
- the planner and the design agent refused;
- a proposal holding `plan hold` refused.

**1.5** `crew bolt unstay`, `crew plan hold` and `crew plan go` answer `-h` and `--help` with their usage and act on nothing (`code.11`): `crew.usage_asked` and `answer_usage` reach them as every Python entry point. Cases in `tests/py/test_help.py`, as its other commands'.

**1.6** `plugin/lib/plan.py` `HEADER` declares the Hold set first, its comment saying why, and `holds_declared` inserts crew's Hold descriptor ahead of a plan's first record set. Cases in `tests/py/test_plan_holds.py`: an old plan takes the Hold set ahead of Bolt and Unit, a Unit appended after still a Unit; crew's header declares Hold, Bolt, Unit in that order. The contract tier's `test_recfix.py` fixtures (`HEADER` with units appended) and `t-journey-board`'s hand-appended duplicate Unit, refused as a duplicated key, pass unchanged.

**1.7** `plugin/lib/plan.py` `holds_once`, called by `check` and by `read` inside its refusal naming the commit. Case `tests/py/test_plan_holds.py::test_crew_refuses_to_read_a_plan_holding_two_holds_on_one_kit_naming_the_commit`, with `recfix`, `show` and `kept_listing` stood in.

**1.8** `plugin/lib/plan.py` `op_plan_go`: the drive's lift hands a raise of each of `w.kits()` that no hold of its own holds. Case `tests/py/test_plan_holds.py::TestLift::test_the_drives_lift_raises_each_kit_of_the_drive_it_held`, a kit known by its landings alone among them.

**1.9** `plugin/lib/plan.py` `rename_branch` renames each Hold's `Kit` by `renamed_kit`, counted. Case `tests/py/test_repository_rename.py::TestWhatTheRenameRenames::test_a_hold_on_the_kit_is_renamed_with_it_and_still_holds_it`.

**2.1** `plugin/lib/plan.py` `lands_by(row, stays, left, stopped, hold)`, beside `card_stand`, as Decision 1 has it. Case `tests/py/test_landings.py::test_how_each_row_lands`, covering:
- a bolt not marked;
- one marked;
- one left;
- one whose land on proof was stopped at its head now, and at an old head;
- a fix of main;
- each under a hold on the kit and on the drive.

**2.2** `plugin/lib/runner.py` `lands_due`: the rows due a land on proof come as a send keyed by no card. A stopped land holds a row only at the head it was posted at, for a proof land, as Decision 1 has it. `send_stood` is unchanged. Case `tests/py/test_runner.py::test_a_land_on_proof_is_due_once_for_each_head`, covering:
- posted once at a head;
- none while one stands asked or submitted, or reads unknown;
- none after a stop at that head, and one at a new head;
- the send's rules for a card's rows unchanged.

**2.3** `plugin/lib/plan.py`:
- `lands_change` and `lands_post` take `proof`: each entry carries `Form: proof` and no `Card`, and the subject reads `plan(<kit>): land <bolts> on proof`.
- `landings_raised` posts them after the sends' lands, for the rows `lands_by` reads `"proof"` that have a box and do not take main first, and says each on its output: `card land/<kit>: <bolt> is asked of the runner to land at <head> (request <n>), on proof`.
- `plugin/lib/record.py`'s notes on `Form` name a land's.

`tests/py/test_landings.py`'s `PLAN` marks its bolts `y`, `w` and `z` `Stays: yes`, so every existing case of the card's rows holds of rows the card asks about. The proof cases add bolts not marked. Cases in `tests/py/test_landings.py`, through `plan.raise_landings` on `LandActs`:
- `test_a_proven_bolt_lands_on_proof_at_the_raise`: one land, its entry with `Form: proof` and no `Card`, and the next raise posting none;
- `test_a_bolt_forecast_in_conflict_lands_on_no_proof`;
- `test_a_send_lands_before_the_proof_lands_of_one_raise`.

**2.4** `plugin/lib/plan.py` `landings_raised`, `card_rows` and `landings_step` take only the rows `lands_by` reads `"send"`, and the rows taking main first or held beside them, as Decision 3 has it. Case `tests/py/test_landings.py::test_the_card_asks_only_about_the_rows_a_send_must_land`, covering:
- a bolt not marked beside one marked;
- a stopped land on proof asked with its box, saying so in the runner's words;
- a left bolt shown unticked with no land posted;
- a bolt not marked taking main first, no row.

**2.5** `plugin/lib/cards.py`:
- `landings_form(n, told)` gives `"tell"` for no row and a told bolt.
- `landings_card(f)` takes `told`, `[{bolt, commit, at}]`. In the tell form it builds the notice of Decision 4. In the asking forms it opens the face and the summary with "Landed on proof since your last look: …". It marks each told bolt in `heads` as `<bolt>@<commit>:landed`.
- `plugin/lib/plan.py` `card_heads`, `heads_taking` and `heads_next` read past `:landed`, and a new `heads_landed` reads it.

Cases in `tests/py/test_cards.py`:
- `test_a_landings_notice_tells_what_landed_on_proof_and_asks_nothing`
- `test_an_asking_landings_card_opens_with_what_landed_on_proof`

**2.6** `plugin/lib/plan.py`:
- `told_on(entries, key, owner, kit)`, as Decision 4 has it.
- `landings_step` takes `told` and decides the notice's post, change and follow, and the asking card's change, as Decision 4 has it.
- `landings_raised` reads `told` and hands it to the step and the card.

Case `tests/py/test_landings.py::test_a_bolt_landed_on_proof_is_told_until_the_user_taps`, covering:
- the notice posted;
- changed in place as another lands;
- tapped and closed, no later card telling either;
- followed by an asking card that opens with the told bolt;
- an asking card changed in place by a landing on proof;
- a card followed unseen leaving its told bolts to the next.

**2.7** `plugin/lib/plan.py`:
- `landings_raised` posts no land, on a send or on proof, while `hold_on` gives a hold for the kit, and says so on its output.
- `card_read` says a send stands and lands what it ticked once the hold is lifted.

Case `tests/py/test_landings.py::test_a_hold_posts_no_land_and_its_lift_posts_what_came_due`:
- a proven bolt and a send under a kit's hold;
- the lift's raise posting the send's land and then the proof land;
- the drive's hold outlasting the kit's lift.

**2.8** `plugin/lib/runner.py` `lands_due`: where the launch's last land is stopped, a send is barred at its head only by a land it posted itself, there or at any head, and a land on proof by any land posted there; otherwise any land posted at its head bars it, as before. `plugin/lib/plan.py`:
- `stopped_on_proof(entries, bolt, head)`, a decision of facts.
- `landings_raised` marks each row whose stopped land was on proof `stopped_on: "proof"`, and hands `landings_step` those rows with no `stopped`, so the send lands them.
- `cards.stopped_said` says a land on proof stopped and that ticked it lands on this send.
- `card_read` and `landing_lines` take `on_proof`, saying the user's send lands such a bolt.

Cases: `tests/py/test_runner.py::test_a_send_lands_a_row_at_the_head_of_a_land_stopped_on_proof_or_on_another_send`; `tests/py/test_landings.py::test_the_users_send_lands_a_bolt_whose_land_on_proof_was_stopped`, through `plan.raise_landings` on `LandActs`, its send posting the land, the card left, the next raise posting nothing, `landing_lines` before the raise, and the send standing under a hold; `tests/py/test_cards.py::test_a_row_whose_land_on_proof_was_stopped_says_so_and_that_a_send_lands_it`. `LandActs.post_lands` writes over the plan the raise read, or the case's `tip`.

**2.9** `plugin/lib/plan.py` `landings_raised` posts no land on proof for a row whose forecast against main reads `("main", None)`, saying why on its output. Case `tests/py/test_landings.py::test_a_bolt_whose_forecast_could_not_be_made_lands_on_no_proof`.

**2.10** `plugin/lib/plan.py` `lands_change` raises `Unposted` where `hold_on(w.plan, kit)` gives a hold, and with `proof` keeps only rows whose bolt the plan at the tip holds unmarked. Case `tests/py/test_landings.py::test_a_hold_or_a_drop_found_at_the_writes_tip_posts_no_land`.

**2.11** `plugin/lib/plan.py` `landings_step(…, hold)`: a close or follow under a hold says the send stands, naming the hold; `landings_raised` hands it the hold's name. `card_read` reads the hold whenever the card's send or an earlier one lands a bolt. Case `tests/py/test_landings.py::test_under_a_hold_a_close_says_the_send_stands_and_asks_nothing`.

**2.12** `plugin/lib/plan.py`:
- `stopped_by(entries, bolt, head)`, a decision of facts: what the newest land crew posted of the bolt at that head was posted on, `"proof"` or the card whose send it carried, or None. `stopped_on_proof` reads it.
- `stop_spends(by, card)`, a decision of facts: a stopped land spends a card's send only where that card's send posted it, and one whose posting crew can't tell is read as spending it (`read.1`).
- `landings_raised` hands `landings_step` with no `stopped` each row whose stop spends none of the card's send, on proof or on another card's, so a later card's send lands the row and leaves the card answered rather than closing it as spent.
- `card_read` passes `landing_lines` `on_send`, the bolts the card ticked whose stopped land an earlier card's send posted, said as that send spent and this card's send landing them.

Case `tests/py/test_landings.py::test_a_later_cards_send_lands_a_bolt_whose_land_on_an_earlier_send_was_stopped`, through `plan.raise_landings` on `LandActs`: the land posted on `req_k1`'s send, the card left as answered with no card posted, changed or closed, the next raise posting nothing more, `stop_spends` for the card that posted the stop and for one that did not, and `landing_lines` before the raise.

**3.1** `plugin/lib/plan.py`:
- `rail_rows`: each land row's bolts carry `stays`. Each line says how the bolt lands, as Decision 7 has it, replacing `can land on your send of land/<kit>` for a bolt that lands on proof. The row carries `told` and `asks`, and is made for a kit with a told bolt and nothing waiting.
- `rail_record` reads `told` for each kit's key (`told_on`) and the plan's holds.
- `stand_said` keeps its words for the rows the card asks about.

Cases in `tests/py/test_rail.py`:
- `TestRows.test_a_bolt_not_marked_says_it_lands_on_proof`, and its land asked with its request;
- `TestRows.test_a_bolt_marked_to_stay_says_it_waits_for_the_send`;
- `TestRows.test_a_held_bolt_names_the_hold_and_its_words`;
- `TestRows.test_a_kit_with_a_bolt_told_and_nothing_waiting_is_a_row`.

The existing `TestRows` and `TestCrossedLandings` cases pin `stays` on their bolts, and those asserting a bolt's `can land on your send of land/<kit>` mark it to stay in their plan.

**3.2** `plugin/lib/plan.py`:
- `proof_due` and `landings_proven`, as Decision 2 has it. `sweep_moved` raises each kit once, after `due`, `sent` and `unoffered`, its result's `raised` entries carrying `proven`.
- `unoffered` counts only the rows `lands_by` reads `"send"`.
- `sweep_judged` owes a land row a card only where the row's `asks` is true.
- `sweep_sessions` takes readings only for the rows a card asks about.
- `rail_text` says a card raised for a bolt due a land on proof under "landings cards raised for bolts due a land on proof:", naming the bolt and the card or the raise's refusal.

Cases in `tests/py/test_landings.py`, through `plan.sweep_moved` on a `SweepActs` stand-in whose `raise_kit` runs `plan.raise_landings` on `LandActs`:
- `test_the_rail_read_raises_a_kit_whose_bolt_is_due_a_land_on_proof`: no card open; the read after it raises none;
- `test_a_bolt_due_a_land_on_proof_beside_an_open_card_raises_it_once`;
- `test_a_held_kit_is_raised_by_no_read`;
- `test_a_row_of_bolts_landing_on_proof_owes_no_card`, through `plan.sweep_judged`.

**3.3** `plugin/lib/board.py`:
- The board's data of a started bolt carries `stays`, and of a drive `holds`, `[{kit, why}]`, `kit` None for the drive's.
- `bolt_row` says `stays` beside a marked bolt's name.
- `planner_view` and `ops_view` open with a line for each hold, as Decision 7 has it.
- `agent_views`' docstring names both.

Cases in `tests/py/test_board.py`:
- `test_a_bolt_marked_to_stay_says_so_in_the_planners_and_ops_bands`
- `test_each_hold_opens_the_planners_and_ops_bands`
- `test_no_hold_and_no_mark_draw_nothing`

The case pinning every key the mod reads is unchanged.

**3.4** `plugin/lib/plan.py` `rail_text` zips `land_times` with the bolts' lines alone, padded, and draws the told lines after them; `rail_rows`' proof line names `<label>-ops`. Cases in `tests/py/test_rail.py`: `TestRows.test_the_rail_draws_each_told_bolts_line_after_the_bolts_that_wait`, and `test_a_bolt_not_marked_says_it_lands_on_proof` with ops named.

**3.5** `plugin/lib/board.py` `ops_view`'s line for a bolt with its landing in flight and no land row names it by `named_`. Case `tests/py/test_board.py::TestStaysAndHolds::test_a_bolt_marked_to_stay_says_so_in_the_planners_and_ops_bands`.

**4.1** `plugin/roles/main-ops.md`, *Landing a bolt* and the opening paragraph: the words of Decision 8 for ops. `tests/t-briefs.sh` asserts:
- "lands on proof";
- that crew posts its land in your name at any hour;
- "asks only about bolts marked to stay";
- `plan hold`, with `--excerpt`;
- that the lift, `crew plan go`, is the user's.

**4.2** `plugin/roles/planner.md`: the words of Decision 8 for the planner. `tests/t-briefs.sh` asserts:
- `--stays` on the proposal's `bolt new` or `bolt start`, on the user's word;
- `bolt unstay`;
- that the planner puts no hold.

**4.3** `README.md`, in the paragraph on the landings card and in the plan's commands:
- a proven bolt not marked to stay lands on proof, its land posted by crew at the first rail read on the main level's host;
- `--stays`, `crew bolt unstay`, `crew plan hold` and `crew plan go`;
- the card asks only about the rows a send must land and tells each bolt landed on proof.

`plugin/skills/crew/SKILL.md`'s rows and `plugin/bin/crew`'s usage header say the same of each command (`docs.2`). `tests/t-docs.sh` finds each new command in the usage, as it does every command README names.

**4.5** `README.md`'s bolt paragraph, its *asked* state, ops's role and the landings card's rows; `plugin/skills/crew/SKILL.md`'s proven bolt and `crew bolt submit`; `plugin/bin/crew`'s and `plan.py`'s `bolt submit` usage; `main-ops.md`'s answer to the user's words in its pane; `plan.submit_refused` and `landing_refused_said`'s "none": each says a bolt lands on proof, or, marked to stay, on the user's send. `tests/t-docs.sh` and `tests/t-briefs.sh` assert the new words and `lacks` the old; `tests/py/test_bolt_commands.py` and `tests/py/test_landing.py` pin crew's own.

**4.4** `tests/t-journey-land.sh`:
- its bolts are planned with `crew bolt new … --stays`, `y` and those of its loop, so its card, send, preview and landing steps stand as they are;
- one step plans and starts a bolt with no mark, has the stub runner carry its last unit landed at its head, reads the rail on the main level's host, and finds one land of its launch in `requests.rec`, its `bolt.submit` entry marked `Form: proof`, and no card asking for it.

Its `# Reads:` line is unchanged, so `tests/moon-tasks` writes the same task.
