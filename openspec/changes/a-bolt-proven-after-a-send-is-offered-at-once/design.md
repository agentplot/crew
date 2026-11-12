# Design

## Context

**What the raise does, and what calls it.** `plan.raise_landings` reads a kit's landings card and its rows, and `plan.landings_step` decides what to do with them.
- On a card that waits on the user, a bolt that joins, moves its head or comes back from taking main first changes the card in place. The card is followed instead when its form changes.
- On a card the user answered, a bolt proven since their send makes the step `follow`. The card is closed keeping their send for what it still lands, as its close's `Heads` (`landings_sent`), and a card following it asks for the new bolt (`tests/py/test_landings.py::test_a_bolt_proven_after_the_answer_gets_a_new_card_following_it_and_the_send_still_lands_the_rest`).

The raise is called by:
- an event of crew's: a bolt's close (`landing_cards_closed`, `bolt_land`), a hold for a fix, a leave in ops's pane, a reading opened, a preview's change;
- `crew card read land/<kit>`;
- the rail's read on the main level's host (`sweep_moved`), for a card main moved under (`landings_moved`) or one whose answer the sweep recorded in that read (`landings_answered`);
- the sweep, for a row with no card open (`sweep_judged`'s `none`).

A bolt's proof is none of these. No act of crew's makes it: the rail reads it from the runner's report (`rail_rows`, `Stages.verification`). So with a card open, a bolt that reads proven waits until one of those events happens. The bolt's land line says the card that follows carries it (crew-rail "Each bolt's land line says whether its card carries, holds or follows it"), but nothing posts that card.

**What it cost.** On wldn's drive, switchboard-kit bolts proven overnight waited 400 to 1055 minutes for a landings card (signal `2026-11-12-agentplot-planner-237b59c7/01` on afterthought/crew-state `agentplot/main`).

**The family.** The landings card is crew's alone. Flume, sluice and the runner report a bolt's place, its landing and its verdict, and crew reads them (`roles.5`). No other tool raises a card for a proven bolt, so the fix is crew's. Pending You resolves an answered card when a card follows it, as its guide says a post does (`tests/stubs/pendingyou`; rail-cards "A post that follows an open card reads it").

**Area pages this change touches:** `core.md` (`state.4`, `read.1`, `code.7`, `code.8`, `docs.2` through `docs.md`), `plan.md` (`plan.16`), `briefs.md` (`briefs.11`), `tests.md` (`tests.4`, `tests.11`, `tests.12`). No rule changes, so no page is edited (`docs.7`).

## Goals / Non-Goals

**Goals:**

- A bolt proven while its kit's landings card is open is offered in the same rail read, the one where it first reads proven on the main level's host: on a card following the user's send when they answered the card, and on the card itself when it waits on them (`briefs.11`: a landings card for every proven bolt waiting on its main).
- A card that shows every row as it stands is raised by none of this. A rail read that finds nothing new costs nothing more than today.

**Non-Goals:**

- A change to what a raise does with its rows (`landings_step`).
- A raise for a bolt the user ticked whose head moved. Its send is read where the kit's forecasts are made (`bolt_work`), and the rail does not read that. A take-main fix's merge reaches the raise as it does today.
- An event of crew's own at a bolt's proof. The proof is read, not done, and the rail's read is the first act that reads it on the main level's host.

## Decisions

### 1. The rail's read raises a card for a row it does not offer as it stands

`plan.unoffered(rows, card, sends)` is a decision on plain facts (`code.7`). A row of the kit's land row is unoffered when all of these hold:
- it can land;
- no send holds it: the card's answer did not tick it, and no closed card's kept send names it while this card does not show it, as `card_stand`'s `holds` reads;
- the card shows it on no row, at another head than its head now, taking main first, or, once the user answered it, with no box.

These are the rows for which `landings_step` changes a waiting card or follows an answered one. A row the card shows as it stands is not unoffered, a bolt the user left on their send among them, since a raise for it would change nothing.

`plan.landings_unoffered(read, label, here, kits)` applies it to each landings card the read finds open on this host in main-level ops's name. It reads the card's rows as the run record holds its last post or change (`shown_heads`), its answer as the read holds it, and the sends kept on its key. `sweep_moved` raises each such card, once, after those main moved under and those whose answer the sweep recorded.

A card whose rows the record holds no post of is left. That includes one the sweep posted in this read, which was raised as its rows stand. So nothing is raised on a guess (`read.1`).

Not taken: raising every open landings card on every read. Each raise asks Pending You, forecasts the rows with git, and on a kit outside the runner's clone fetches GitHub's main. The rail reads every thirty seconds, and `plan.12`'s reading of 2026-10-28 rules out a read that forks for nothing. Also not taken: raising a card whenever a bolt's land line says it follows (`card_stand`). For a bolt the user left beside a send still landing, that line is true, yet a raise for it changes nothing. It would raise the card on every read until the send's bolts landed.

### 2. The answered card closes at the follow, its send kept

The brief asks for two things: a bolt proven meanwhile is offered at once on a card that follows the answered one, as a send's waiting rows are; and the answered card stays open until its own landings end. With Pending You and crew's cards as they stand, the two cannot both hold literally.
- Pending You resolves an answered card when a card follows it.
- crew keeps one card under `land/<kit>` in ops's name (`cards.card_under`), and a post under a key still open gives that card back (rail-cards "A card still open under its key keeps its key and is recorded once").

So this change does what the brief's model, a send's rows that waited for a box (rail-cards "A send with rows waiting for a box is followed at once by a card asking for them"), already does. The answered card is closed at once, and the user's send stays standing: kept as its close's `Heads`, it lands what they ticked on that send and is no row of any later card while its heads stand (`rows_unsent`). The rail's land line says the send holds each such bolt. That is the existing `follow` step, now reached at the bolt's proof. The answered card still stays open until its own landings end whenever nothing is proven meanwhile, as before.

Not taken: a second card under `land/<kit>` beside the answered one, not following it, so the answered card's close could name what landed. That is two open cards under one key in one owner's name, which `card_under`, the rail's `row_cards` and the sweep each read as one card and an older copy. It is a change to how crew keys its cards, beyond a fix.

### 3. A land row's bolts carry their head now

`rail_rows` adds each bolt's head to its land row's `bolts`, beside `bolt`, `host` and `can`, so `unoffered` can tell a row the card shows at another head. A fix of main is read by its name alone, its head being its place's (`fix_row`). The board reads only `bolt` from these, and the agents' views and crew's mod read none (`code.8`).

### Rules relied on

- `briefs.11`: a landings card for every proven bolt waiting on its main.
- `plan.16`: the user's send is the word to land the bolts it ticked, in their order, and it stands until they land.
- `read.1`: a card whose rows can't be read from the record is raised by none.
- `state.4`: the read writes nothing but by the raise's own acts.
- `code.7`: `unoffered` and `landings_unoffered` start no process.
- `code.8`: no modelled shape the views draw changes.
- `docs.2`: README, the skill and the usage say what `crew rail` now raises.
- `tests.4`, `tests.11`, `tests.12`: the reproducing case is in the logic tier, through `sweep_moved` and `raise_landings` on stand-ins.

### Departures

None from a rule. From the brief: the answered card closes at the follow, its send kept (Decision 2).

## Risks / Trade-offs

- **[The rail reads a row as able to land that the raise holds]** → the card is raised on each read and left as it is, for instance where the raise's own read of the bolt's host fails while the rail's survey read it. Each such raise is said on the rail's text under the landings cards raised for rows they did not offer, naming the row, so it is seen, and it changes nothing.
- **[Pending You refuses the follow-on]** → the answered card is closed and the row has no card, and the sweep posts it as a row with none, as it does for any refused post (rail-cards "A row's card that Pending You refused is owed until it posts").

## Migration Plan

None. A card open when this lands is raised at the first rail read on its host whose crew carries this change, if it does not show a row as it stands.

## After deploy

None: every outcome here is a logic-tier case, and nothing waits on a host or on the user.

## Task notes

**1.1** `plugin/lib/plan.py` `rail_rows`: each land row's `bolts` entry carries `head`, the bolt's head now. Its docstring says so. Cases: `tests/py/test_rail.py` `TestRows.test_a_kit_with_a_bolt_whose_every_unit_merged_is_one_row_timed_by_its_last_merge` and `TestCrossedLandings.test_a_crossed_bolt_proven`, and `tests/py/test_kit_rename.py` `TestTheStartedBoltLands`, each pinning the row's bolts with their head.

**1.2** `plugin/lib/plan.py`: `unoffered(rows, card, sends)` beside `card_stand`, as Decision 1 has it. Case: `tests/py/test_landings.py::test_a_row_the_open_card_does_not_offer_as_it_stands_is_unoffered`, covering:
- a bolt proven since the send, on no row;
- a left bolt at its head, and at a new head;
- rows shown taking main first or with no box on an answered card;
- a send ticking none;
- a kept send;
- a waiting card's joining, moved and taking rows, and its rows with no box;
- a row that can't land;
- a fix of main by name.

**1.3** `plugin/lib/plan.py`: `landings_unoffered(read, label, here, kits)` beside `landings_answered`. `sweep_moved` raises its cards once each, after `due` and `sent`, its result's `raised` entries carrying `rows`, the rows a card was raised for alone, else `[]`. Cases in `tests/py/test_landings.py`, through `plan.sweep_moved` on a `SweepActs` stand-in whose `raise_kit` runs `plan.raise_landings` on `LandActs`:
- `test_a_bolt_proven_between_a_send_and_its_landing_gets_its_card_in_the_same_sweep`: the answered card is closed with `Heads` `y@abc1234`, a card following it asks for `z`, and the next read raises none.
- `test_a_bolt_proven_while_the_card_waits_raises_it_in_the_same_sweep`.
- `test_a_bolt_the_user_left_beside_a_send_still_landing_raises_no_card`.

The two `TestMainMoved` cases in `tests/py/test_rail.py` pin `rows=[]`.

**1.4** `plugin/lib/plan.py` `rail_text`: a card raised for its rows alone is said under "landings cards raised for rows they did not offer as they stand:", `  land/<kit> (<label>): <rows>: raised (<card>)`, or its raise's refusal, and not among those forecast again. Case: `tests/py/test_rail.py` `TestMainMoved.test_a_card_raised_for_a_row_it_did_not_offer_is_said_naming_the_row`.

**2.1** `README.md`, in the paragraph on the landings card, after the ticked bolt taking main in: on each rail read on the main level's host, a card that does not show a row that can land as it stands is raised. A bolt proven while the card waits joins it, and one proven since the user's send is offered at once on a card following theirs, which closes keeping their send for what it still lands. `plugin/skills/crew/SKILL.md`'s `crew rail` row and `plugin/bin/crew`'s usage of `crew rail` say the same in a clause.
