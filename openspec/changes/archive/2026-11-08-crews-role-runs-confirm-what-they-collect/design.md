# Design

## Context

**The direction.** weir record 0006, accepted by the user on 2026-11-08 ("Runner as one more recipient now; one shared inbox in weir next"): a message one tool owes a reader is a *delivery*, recorded once under a key with each of its readers, and owed to each reader until that reader confirms it by its key. Handing it over, by an inbox, a wait or a notice, confirms nothing. An owed delivery expires after a time the host sets and is then shown, with its reader, wherever the tool shows what is owed, never dropped.

**Flume's side**, flume record 0061 (accepted 2026-11-09) on agentplot/flume's bolt `flumes-ends-are-owed-until-confirmed`, read at 3573e0f0 on 2026-11-08:
- Each end of a place is a delivery under `<kind>--<name>/<token>/<end key>`, its readers the place's recipients.
- `flume confirm <KEY>... --recipient <name>` confirms as the recipient it names. Flume "takes a recipient's confirmation from the caller that names it ... and never confirms for one itself" (statement 43).
- A tidied place's document stays until every end is confirmed by each recipient (62).
- Status gives each end its `delivery` key, `expires_at`, `owed` (each recipient that has not confirmed it, `{recipient, expired, known}`), `confirmed` (`{recipient, at}`) and `pending_for` (`site/…/reference/state.md`; `flume-seams` `held.rs` `OwedTo`, `ConfirmedBy`).
- Its consequence names crew: "every caller that collects must now confirm. crew's role kinds, the runner and a person's own scripts confirm what they act on, or are handed it again at each inbox."

**crew's side, read on this branch, cut from main at 0563aa90:**
- Every place crew launches names a role's address as its recipient (`runner.py`): the planner's for a unit, chore or fix (`<label>/planner`), ops's for a fix of a red main (`<label>/ops`), and the role's own for its work that lands (`role_launch`). The runner names itself, `boomdrive`, beside it (Boomdrive's `work-into-flume`).
- A role that runs as its kind collects at its run's start (`roles.7`): its asks, and each place the runner's records show waiting on it (`asks.waits_on`), read from Flume's status as the runner carried it into `places.rec`. Its turn's end marks them answered in `asks.rec`. Nothing tells Flume.
- crew never calls Flume or sluice. It posts requests the runner pulls and reads the runner's report (record 0056, point 1, on the user's words "crew lands nothing and talks only to the runner"; `roles.9`).
- Boomdrive's runner reads `requests.rec` as acts on launches (`crew-control-plane`: "An act naming no host is given to the runner that holds its launch") and carries each as Flume's own command on the launch's place (`work-into-flume`). It knows `launch`, `retry`, `land`, `drop`, `priority` and `preview`, and gives a no-host request of an act it does not read nothing, naming it in its log. It mirrors crew's `asks.pending` to decide when a role is wanted, reading `Took` only for `ask/…` and wait keys (`crates/boomdrive-crew/src/roles.rs` `wanted`, main at 76e0226).
- Every partition's roles stand today on both machines (the teams file on deneb, read 2026-11-08). So this change takes effect for a role once its partition runs it as its kind.

**Who owns what across the family.** weir owns the form: who owes, who confirms, expiry. Flume owns the deliveries of a place's ends and `flume confirm`. The runner is the one caller that reaches Flume for crew. crew decides only which of its role's ends a turn took, and asks the runner to confirm those. crew builds no record of deliveries of its own and keeps no second list of what Flume owes (`roles.5`).

**Area pages this change touches:** `core.md` (`roles.5`, `roles.6`, `roles.7`, `roles.9`, `state.1`, `read.1`, `read.2`, `read.3`, `code.1`, `code.7`, `code.8`), `plan.md` (`plan.1`, `plan.12`), `briefs.md` (the crew skill), `tests.md` (`tests.4`, `tests.10`, `tests.11`), `docs.md` (`docs.2`, `docs.6`, `docs.7`). No rule page or record is edited by this change (`docs.7`). It departs from no rule. `roles.6` says delivery is "at least once, the sender marking the record delivered". It is held here as weir record 0006 settles it: Flume marks an end delivered once its reader confirms it, and crew's role is that reader.

## Goals / Non-Goals

**Goals:**
- Every end Flume owes a role's address, of a place crew launched, is confirmed by that role's run once a turn that took it has ended, so Flume lets go of the place's document.
- An end a turn took is never taken by another turn, unless the turn was lost before its end.
- crew still talks only to the runner.

**Non-Goals:**
- A role that stands. Flume hands its standing agent each end by a notice into its pane, which names the end's key and how to confirm it. Whether a standing agent confirms is not this change's. Standing roles leave crew with record 0047's move 6.
- A role's run's own place. The runner offers it under an id of its own with no request and no recipient (Boomdrive's `crew-control-plane`, "A role's run is offered …"), so no `Of` names it, and its ends are the runner's.
- The runner's own confirmation as `boomdrive`: Boomdrive's unit `the-runner-confirms-an-end-once-its-control-plane-has-it`.
- sluice's outcomes, which move onto weir's form in sluice's own bolt `sluices-outcomes-are-owed-until-confirmed`.
- Building the runner's reading of a confirm, or `flume confirm`. Both are the other tools'. See *Dependencies*.

## Decisions

### 1. A run collects every end Flume owes its address, read from Flume's `owed`

- At its start, a run takes each end whose carried status gives an `owed` entry naming `<label>/<role>`, together with its `delivery` key. It reads this from every place the partition's runners carry in `places.rec`, whatever the launch's `Recipient`.
- Flume's `owed` is the one truth of whom an end is owed to. crew reads it and keeps no copy (`roles.5`, `read.2`).
- Every field is guarded (`read.2`). An end with no string `delivery`, or an `owed` that is not a list of entries each with a string `recipient`, gives nothing. `expired` reads true only where it is `true`. So a status from a Flume older than record 0061 gives no end, and the run takes its waits as today.
- A host whose runner can't be read gives none of its ends. They are left for the next run, as its waits are (`read.3`).
- Not taken:
  - **Only the ends of places that wait on the role.** Every delivered stage's end, and a unit's landing, would stay owed to the planner for good, and its place's document with them. That is the very thing record 0061's consequence asks callers to end.
  - **Only places whose launch names the address.** Flume may owe the address an end the launch did not route to it, such as a stall's to the stream's answerer. Reading `owed` takes whatever Flume owes, and nothing else.

### 2. An owed end makes no role wanted

- Only an ask or a place that waits on the role starts a run, as now. A run takes every owed end along with the rest. With no ask and no waiting place, a start records no turn and takes no end.
- Why:
  - A delivered stage is no work for a role (`role-runs`: "A place whose stage delivers while its kind runs through SHALL be pending for no role").
  - Boomdrive's mirror of `wanted` stays as it is.
- What it costs: a tidied place's document waits for the role's next run. A bolt's landing asks the planner and the design agent (`role-runs`, "A capture and a landing are asks"), so a bolt's units' documents go, at the latest, with the planner's run after the bolt lands.
- Not taken:
  - **An owed end waking a run.** It would mean a session of a role for every stage end, to read and do nothing.
  - **The follower, or any act of crew's outside a run, confirming them.** crew would be deciding for the role what the role has read, and a run's start is the one collector of what is pending for a role (`roles.7`).

### 3. Confirmed when the turn ends, never at its start

- A turn records the ends it took. Its end asks for their confirmation in the same commit that records the turn ended (`state.1`).
- A run lost before its end asks for none. Its turn is superseded at the next start, which takes those ends again: at least once (`roles.6`).
- Why: weir 0006 has a reader confirm what it acted on. A turn's end is where crew already says a run has acted on what it took.
- Not taken: **confirming on receipt at the start.** A run that dies mid-turn would lose the end, the very failure weir 0006 records against Flume's old form.

### 4. A confirm is a request the runner that holds the launch carries

- `requests.rec` gains the act `confirm`. It names:
  - `Of`, the launch whose place's ends it confirms;
  - `Work`, that launch's work, as every act on a launch names it;
  - `Recipient`, the role's address;
  - one `Delivery` for each key.
- It names no host. Boomdrive gives an act on a launch to the runner that holds it, which acts on the place its report holds for that launch. Flume takes the confirmation from that caller naming the recipient (statement 43). So the runner carries it as `flume --json confirm --recipient <Recipient> <Delivery>...`.
- crew's rules (`runner.request_refusal`, `plan.1`) refuse a confirm whose `Of` is no launch or is another work's launch. They also refuse one whose `Recipient` is not `<label>/<role>` of one of crew's five roles, and one with no `Delivery`.
- Not taken:
  - **The run running `flume confirm` itself.** crew never calls Flume (record 0056, point 1). The place may also be on another host, which only its runner reaches.
  - **The runner confirming from the turns it already reads.** That would give Boomdrive crew's meaning of a turn, beyond the mirror of `wanted` it keeps. A confirm the runner was never asked for would be implicit, and nothing would record that it was asked.
  - **One request naming every launch.** An act is on one launch, and its routing is by its `Of`.

### 5. An end is taken once a confirm names it, whatever the runner answered

- An end that any `confirm` of the address names is never taken again: unanswered, done or refused.
- Why: once Flume lets go of a tidied document, the runner can't read its status again, and `places.rec` keeps the last status it carried until the work leaves the plan. A stale status still shows the end owed. Taking again an end whose confirm was refused would then ask again for a key Flume no longer holds, run after run.
- A refused confirm stays in the runner's `answers.rec`. If the end is still owed, Flume's host status lists it expired with its recipient, where the operator confirms it as that recipient by hand (flume record 0061).
- Not taken: **taking an end again once its confirm was refused.** It would loop on a key Flume has let go.

### 6. The turn records its ends in `Took` as `end/<request>/<delivery key>`

- The key carries the launch, which its confirm names as `Of`, and Flume's key. It splits at its first two slashes, since Flume's key holds slashes of its own.
- The end confirms what the start took, never what arrived during the turn: that waits for the next run, as an ask does.
- The `turn.begin` entry's `Took` keeps counting the asks and the waiting places alone (`run-record` spec: "how many it took" of what was pending). The run record is otherwise unchanged.
- Boomdrive's mirror reads `Took` only for `ask/…` and wait keys, so `end/…` lines answer nothing there.

### 7. What the run reads, its report and its view

- `crew role start` prints the ends after the places that wait, one line per launch: its work, its place, its request, and each end's key, an expired one marked. It says they are confirmed when the turn ends.
- The report's *What it took* lists the asks and waits as now, then one line counting the ends, naming their requests and saying their confirmation was asked.
- The board counts a turn's ends on its head line and lists none (`code.8`). Only `board.run_rows` and `asks.run_view` change. The mod draws the rows it is given and reads no turn's field, so `plugin/hooks/status.js` and its cases stand, and `test_board`'s pin of every key the mod reads is unchanged.

### 8. One read of the runners for the waits and the ends

- `role_start` reads `requests.rec` and each host's runner once (`runner_facts`, `plan.12`), and decides the waits and the ends from that one read.
- `role_end` reads `requests.rec` in its own write, at the tip it is applied to, for each launch's work (`plan.1`). It reads no runner.

## Dependencies

- **Flume.** `flume confirm` and the status fields above are on agentplot/flume's bolt `flumes-ends-are-owed-until-confirmed` (record 0061), not yet in a release. Until a host's Flume carries them, its statuses give no delivery key, so crew takes no end and writes no confirm.
- **Boomdrive's runner.** Reading `Act: confirm` as an act on `<label>/<Of>` with its `Recipient` and each `Delivery`, and carrying it as `flume --json confirm --recipient <Recipient> <Delivery>...`, answered `done` or `refused`, belongs in Boomdrive's `crew-control-plane` and `work-into-flume` specs. No unit in the plan builds it yet. Until it does, the runner gives each confirm nothing and names it in its log (`crew-control-plane`, "A request crew's implementation cannot read …"). Flume's ends stay owed as they are today. A confirm written meanwhile is carried once the runner reads it, and a key Flume let go of by then is refused, harmlessly (Decision 5).
- Nothing of crew's waits on either. crew's side lands alone.

## Risks / Trade-offs

- **A document lingers until the role's next run** (Decision 2). The ends a bolt's units owe the planner go, at the latest, with the planner's run after the bolt lands. For ops's fix of a red main, they go with ops's next run.
- **The runner's log names every unread confirm on each pass** until Boomdrive reads the act. The noise is the runner's and ends with its change.
- **Took grows** by one line per end a turn takes, a few dozen for a busy planner, in `asks.rec`, which is append-only. A turn is still one record.

## After deploy

None. Every behaviour here is a crew command's, proved by the logic and end-to-end tiers. The runner's and Flume's parts are those tools' own changes, proved there.

## Task notes

**1.1** `plugin/lib/asks.py`:
- `owed_to(place, address)`: from a place's status as `status_of` gives it, each `(end key, delivery key, expired)` of an end whose `owed` names the address, guarded as Decision 1 says.
- `ends_owed(address, places)`: over each host's `places.rec` records as `waits_on` takes them (`Request`, `Place`, `Status`), each `(took key, request, work, place, end key, delivery key, expired)`, where the took key is `end/<request>/<delivery key>`; ordered by request, then in the status's order.
- `ends_owed` takes the launches too, `requests`, for each request's work, as `waits_on` does. A record whose status can't be read gives nothing.
- The fixture is `tests/py/flume-deliveries/`, made from `flume-0.17.0/kept-open.json`. Each end gains `delivery`, `expires_at`, `owed` and `confirmed`, as agentplot/flume's `site/src/content/docs/reference/state.md` gives them at 3573e0f0: one end owed to `agentplot/planner`, one owed and expired, and one confirmed by `agentplot/planner` and owed to `boomdrive` alone. Its `README` says so, as `flume-0.17.0/README` does.
- Cases in `tests/py/test_asks.py`, class `TestEndsOwed`:
  - the fixture's owed ends, with their keys and the expired mark;
  - an end confirmed by the address, or owed to another, not given;
  - flume-0.17.0's `kept-open.json` gives none;
  - each guard: a `delivery` that is no string, an `owed` that is no list, an entry with no `recipient`, an `expired` of `"yes"`;
  - an unreadable status gives none.

**1.2** `plugin/lib/asks.py`:
- `confirmed(requests, address)`: the took keys every `confirm` request of the address names, one for each `Delivery`, `end/<Of>/<Delivery>`.
- `taken_ends(ends, requests, address)`: the ends of `ends_owed` that no confirm names.
- `took(asks, waits, ends=())` appends the ends' took keys after the waits'.
- `pending` and `wanted` are unchanged.
- Cases in `tests/py/test_asks.py`, class `TestEndsTaken`:
  - an end a confirm names is not taken, whether its answer is none, done or refused;
  - a confirm of another address holds nothing;
  - `wanted` is false with ends owed and nothing pending;
  - a superseded turn's end keys are taken again, no confirm naming them.

**1.3** `plugin/lib/asks.py` `turn_confirms(took, requests)`:
- From a turn's `Took`, the `end/…` keys grouped by request: `[(request, work, [delivery…])]`, oldest request first, each request's keys in the order taken.
- The work is the launch's `Work` in `requests`.
- A key that does not split as `end/<n>/<key>`, or whose request is no launch, is refused with `Refusal` naming it (`read.1`): nothing in crew writes one.
- Cases in `tests/py/test_asks.py`, class `TestTurnConfirms`:
  - two launches' keys grouped in order;
  - a turn with only asks and waits gives none;
  - a Flume key holding slashes kept whole;
  - a malformed key refused.

**1.4** `plugin/lib/runner.py`:
- `REQUESTS`: `%doc` names a confirm; `Act` enum gains `confirm`; `%allowed` gains `Delivery`.
- `FIELDS`: `Delivery` after `Words`.
- `ACTS["confirm"] = (("Of", "Recipient", "Delivery"), ())`.
- `request_refusal`:
  - the `Of` check of retry, drop and priority covers confirm;
  - a confirm's `Recipient` must match `^[a-z0-9][a-z0-9-]*/(design|planner|reviewer|ops|operator)$`;
  - the act list in its words names a confirm.
- Cases in `tests/py/test_runner.py`, class `TestConfirmRequest`:
  - a confirm of a launch with two `Delivery` lines is written in `FIELDS` order and passes;
  - refused with no `Delivery`, with no `Recipient`, with a recipient of no role, with an `Of` that is no launch or another work's, and carrying a `Stage`.

**1.5** `tests/contract/test_recfix.py`, a case `test_a_confirm_with_two_deliveries_passes_recfix_and_an_act_the_descriptor_lacks_is_refused`: a launch then a confirm of it with two `Delivery` lines pass `plan.checked` with `runner.REQUESTS`, and a request whose `Act` the enum lacks is refused by recfix.

**1.6** `plugin/lib/asks.py`:
- `ends_said(ends)`: one line per launch, `<work> (the place <place>, request <n>): <end key>, <end key> (expired), …`, under a heading saying Flume holds them for the role and they are confirmed when the turn ends.
- `took_said` lists asks and waits as now, then one line for the ends: `- <k> ends of requests <a>, <b> and <c>, their confirmation asked of the runners`.
- `run_view`'s turn gains `ends`, the count of its `end/…` keys, and its `took` leaves them out.
- Cases in `tests/py/test_asks.py`, class `TestEndsSaid`: the lines for two launches, an expired mark, the report's count line, `run_view`'s count and its `took` without them.

**1.7** `plugin/lib/board.py` `run_rows`: the head says `turn <n> took <k>` then ` and <m> ends` where the turn took any, and no row is drawn for an end. Case in `tests/py/test_board.py`, class `TestRuns`: `test_a_turns_ends_are_counted_on_its_head_line_and_listed_nowhere`.

**2.1** `plugin/lib/plan.py`:
- `run_waits` becomes `run_reads(fleet, label, role)`. It reads `runner_facts` once and returns the waits, the ends owed (`ends_owed`), the requests and the unread hosts.
- `role_start`:
  - takes `asks.taken_ends` over the requests at the tip its write is applied to, inside its change, so a confirm written meanwhile is seen (`plan.1`);
  - passes them to `asks.took`;
  - keeps `NothingPending` on asks and waits alone;
  - gives `record.turn_begin_entry` the count of asks and waits;
  - prints `asks.ends_said` after the waits and before the cards.
- Cases in `tests/py/test_asks.py`, class `TestStart`:
  - `test_a_start_takes_the_ends_flume_holds_for_the_role_and_prints_them_after_the_waits`;
  - `test_ends_alone_take_no_turn`;
  - `test_an_end_a_confirm_names_is_not_taken_again`;
  - `test_the_entry_counts_the_asks_and_waits_alone`.

**2.2** `plugin/lib/plan.py` `role_end`:
- In its change, for the open turn, `asks.turn_confirms` over `requests_of(w)`. Each confirm is appended with `request(w, "confirm", work, Of=n, Recipient=f"{label}/{role}", Delivery=keys)` in the same write.
- The subject adds `, asking <k> confirms of <m> ends` where there are any.
- The report is written by `asks.report` with 1.6's line.
- The printed line names the confirms' request numbers.
- Cases in `tests/py/test_asks.py`, class `TestEnd`:
  - `test_a_turns_end_asks_the_runners_to_confirm_its_ends_in_the_same_commit`, two launches and the report's line;
  - `test_a_turn_with_no_ends_appends_no_request`;
  - `test_a_run_with_no_turn_asks_no_confirm`.

**3.1** `plugin/flume/turn.md`: step 1 says the start also takes the ends Flume holds for the role. Step 3 says `crew role end` asks the runners to confirm to Flume each end the turn took, so none is taken again. No part in double braces is added. Case in `tests/py/test_role_kinds.py`, class `TestThePrompt`: `test_its_end_says_it_asks_the_runners_to_confirm_the_ends_the_turn_took`.

**3.2** `README.md`:
- the `requests.rec` line names a confirm;
- the role-runs paragraph says the start takes the ends Flume holds for the role, and the end asks for their confirmation.

`plugin/skills/crew/SKILL.md`: the same, in its role-runs paragraph. `plugin/bin/crew`'s usage is unchanged, since no command or argument changes.

**3.3** `tests/t-journey-roles.sh`:
- After the planner's run's turn, the runner's branch carries a place of a unit's launch, via `runner_commit` with a `Place` record. Its status is the `flume-deliveries` fixture's place. The run's next start, with a tell pending, prints its ends. `crew role end` appends one confirm naming the launch, `madswan/planner` and the fixture's owed keys.
- The test's opening comment says so. Its `# Reads:` line adds `tests/py/flume-deliveries/` if it reads the fixture, and then `tests/moon-tasks` is run and `tests/moon.yml` committed (`tests.10`).
