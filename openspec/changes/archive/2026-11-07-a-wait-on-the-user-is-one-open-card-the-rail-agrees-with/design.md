# Design

## Context

See `proposal.md`, *Why*, for the four ways the rail and the cards disagreed on 2026-11-07 and 08. Here is the state of the code those readings rest on, read at `7a7b8acd`.

- **The run record knows a card's post, change and close, never its answer.** `record_reading` (`plugin/lib/plan.py`) holds a card open from its `card.post` to its `card.close`. The user's answer reaches the record only as the close's `Answer`, written by `card_closed`. Crew reads the answer from Pending You in three places, and records it in none:
  - the raise of a kit's landings card, `kit_card_state`;
  - `crew card read`, `card_read`;
  - a close, `card_closed`.
- **`rail_text` prints every open card under a row's key, whoever's it is.** Each prints as `<key>, open, asked by <by> (<card>)`. afterthought's `proposal/508` printed two such lines.
- **An answered card closed with a reason alone is recorded withdrawn.** `cards.close_call` acks it and records State `withdrawn` whenever the event gives no outcome. `row_gone` gives a kit's landings card no outcome when its row is gone ("nothing waits to land on <kit>'s main"). `landings_sent` reads a send only from a close's `Heads`, and only `landings_step`'s close writes those.
- **`kit_card_state` reads every status but `answered` as `waiting`.** That includes a card Pending You has resolved, cancelled or expired.
- **The sweep never learns whether a card was answered or has ended.** Its one ask is in crew's own name (`cards_fetched`, `SWEEPER`), which Pending You refuses for every card as its holder's. The sweep reads only "not found" from it. The follower makes that ask at most every ten minutes when nothing moved (crew-board "The follower asks Pending You about cards on its clock").
- **`cards.lost` is true only for "not found".** madswan-planner's batch cards are refused to madswan-planner as swancloud-planner's on every close. They have stayed open in the record since 2026-10-25, and the rail promises each time that a later read closes them.
- **`bolt_facts` gives a bolt's minutes to the user:**
  - from the end of its last merge, for as long as its kit's landings card is open, whatever bolts the card's rows name;
  - for every question its partition's planner, ops or design agent asked since the bolt's start.

  That second count replaced crew-board's "a question an agent of the bolt's team asked" when the teams left deneb.

Pages of `docs/architecture/` whose areas this change touches:
- `core.md`;
- `plan.md`, for `plugin/lib/plan.py`;
- `record.md`, for `plugin/lib/record.py`'s docstring;
- `briefs.md`, whose card rules `briefs.11`, `briefs.13`, `briefs.16` and `briefs.17` this builds under, though no brief changes;
- `teams.md`, for `plugin/bin/crew`'s usage header;
- `tests.md`, for `tests/`;
- `docs.md`, for README and `openspec/`.

## Goals / Non-Goals

**Goals:**

- One open card per wait on the user, and every view crew draws (the rail, the board, the agents' bands) says the same of each card: waiting on the user, answered and waiting on its owner, or gone.
- The user's answer is read from the drive's branch like every other card act (`read.5`), so every host's rail agrees with nothing running (`state.4`).
- A send the user made is never lost to a close and never asked for again while it stands.

**Non-Goals:**

- No new card kind, form or key, and no change to how a card is raised, changed or followed beyond the closes named here.
- No card is closed in another agent's name. A copy Pending You holds under a name crew does not own is named and left to the user (`briefs.17`).
- Pending You's notice, `pendingyou watch -- crew _answered`, runs only while a role runs as its kind. This change does not make it record answers. When the main-level roles become Flume kinds (record 0049, move 6), it can record `card.answer` through the same helper, and nothing here stands in its way.
- No rule page or record changes. `docs/architecture/` and `docs/adr/` are the design agent's (`docs.7`). Decision 8 reads `plan.20`'s "the user, a card of the bolt's open" as a card waiting on the user, and the design agent may word the rule so.
- Not built here, found while reading: the host's follower appends what its shared read printed to every partition's rail frame. On 2026-11-07, agentplot's "card land/weir: req_afb5fd7… is left as it is" ended afterthought's, madswan's and wldn's rails too (`board.py` `Follower.write`, `last["said"]`). That is work owed as a change of its own (record 0053), and is said to this stage's caller.

## Decisions

### Decision 1: The user's answer is a card act, `card.answer`, recorded once by the first act of crew's that reads it

**What is recorded.** When crew reads a card the run record holds open and finds it answered (`status` answered, the agent's turn), it records one entry:
- `Act: card.answer`, on the card's object: `cards.row_object(key)`, or `agent/<asker>` for a question.
- `By`: the card's owner.
- `Card` and `Key`.
- `Answer`: `cards.answer_said`, crew's words made from names alone (`record.3`).
- For a kit's landings card, `Heads`: the bolts ticked (`ticked_of`) at the heads its last post or change showed (`card_heads`).

**When.** Once per card: an act that finds the card's `card.answer` already among the entries records nothing (`record.1`, one entry per act). Pending You changes no answered card, so one answer per card is final. The descriptor allows every field already. Only the act is new, named in `record.py`'s docstring beside the other card acts.

**Who records it.** Three acts, each in the owner's name under the host's sign-in, as crew reads its own cards (`briefs.16`):
- the landings raise's read, `kit_card_state`;
- `crew card read`;
- the rail's sweep (Decision 2).

The owner's own read records the answer at once. The sweep records it within its ask's ten minutes when nothing else moved.

**Alternatives.**
- The rail asks Pending You at each draw. Ruled out: the board and other hosts would not see the answer (`state.4`, `read.5`), and it costs a bridge a draw.
- Record the answer only in the close (today). Ruled out: that is the gap. A send waits on ops for minutes to hours, and the rail calls the card open throughout.
- `crew _answered`, from Pending You's notice. Not available on deneb, where every role stands (*Non-Goals*).

### Decision 2: The sweep reads its cards' states from each owner's pending list, in its one bridge

**The ask.** In the follower's one ask (`cards_fetched`), beside its asks in crew's own name, the sweep calls `list_pending` once in the name of each owner of a card open on this host. The owners are each row's owner, each question's asker, and the design agent for each record card. The list is read as `cards.run_cards` reads it, as Pending You's wake mod does: each request's id, title and turn. Every id is kept, not only those on the agent's turn, so that a card missing from the list can be found.

**What it reads whole.** Only cards whose state the list shows changed get a `get_request` in their owner's name:
- on the agent's turn and not yet recorded answered: crew records `card.answer`;
- absent from the list: the card has ended (Decision 5), is lost ("not found"), or is held in another name (Decision 6).

Decision 2 adds no ask the follower's clock does not already make. It adds one call per owner per ask, and one read per change.

**Why reading in an owner's name is allowed.** `briefs.16` has crew read and act on its own cards in the owner's name. crew already withdraws a question in its asker's name (`question_close`), so reading the asker's list is no new kind of act. `briefs.17` refuses an agent's call in another agent's name, not crew's.

**Alternative.** A `get_request` in the owner's name for every open card at every ask. Ruled out: each ask's calls would grow with the number of open cards, where the list is one call per owner.

### Decision 3: The rail, the board and the bands say an answered card is answered, and whose act it waits on

`record_reading` gives each open card its answer from the entries: `answered = {at, answer, heads}`, or None. Then:

- **A row's card line.** It says the card was answered, when, and what, and the act it waits on, by the key's kind (Task notes 4.1):
  - a landings card: ops lands what was ticked;
  - a proposal: the planner applies it;
  - a batch: the planner hands on its notes;
  - a deploy: ops records the word, and once `ops.word_stands`, the deploy's end closes it;
  - a step: ops records it.
- **Answered questions and record cards** leave "questions waiting on you" and "decision records waiting on you" for a list of their own, "answered, waiting on their askers".
- **The board's frame** carries `answered` and `answer` on each card and on each marker's card.
- **An agent's band** (`card_line`) says "answered 5m ago, yours to act on" in place of "open 5m". ops's landing line in its band (`ops_view`) says the landing is its own.

The mod draws the lines the views give, so it needs no code. Its case proves an answered card's line is drawn (`code.8`).

**Alternative.** Mark the card on the row alone and leave the lists and bands. Ruled out: the band is where the owner learns the next act is theirs, and `code.8` holds the bands to what crew models.

### Decision 4: An answered card is closed, never withdrawn, and a landings card's close keeps the send

**Closed, never withdrawn.** `cards.close_call` acks a card the user answered and records it closed in every case, its words the outcome or, with none, the reason. Record 0031 §1 closes a card "with its outcome". A withdrawal is for a card nobody answered. Pending You shows the ack's words to the user, and "nothing waits to land" on a card they approved reads as their send thrown away.

**The send is kept.** Every close of an answered kit's landings card carries `Heads`, the bolts ticked at the heads shown, unless the act gives its own (`landings_step`'s close does). The paths are:
- `card_closed`'s ack;
- its ended-in-Pending-You path;
- `kit_card_state` finding the card ended.

`landings_sent` and `rows_unsent` then read the send in every case. The card that follows has no row for a bolt the send still lands, as rail-cards "A follow-on with nothing changed is not posted" already wants.

**The raise reads an ended card as closed.** `kit_card_state` records a card Pending You reports ended as closed there (`ENDED_ELSEWHERE`, with its answer and send). It returns none held, so the raise posts with the send standing. Today it reads the card as waiting and changes or withdraws it.

**Alternative.** Keep withdrawals and have `landings_sent` read `Answer` too. Ruled out: `Answer` is crew's words for the user's ticks, with no heads. The send needs the heads (`send_stands`), and the user still sees "nothing waits" on the card they approved.

### Decision 5: The sweep leaves an answered landings card while a bolt it ticked waits to land, and records an ended card on the read that finds it

**Leaving an answered landings card.** `sweep_judged` does not judge a `land/<kit>` card gone while the run record holds its answer and a bolt the answer's `Heads` name has no `bolt.land` or `bolt.drop` since. It is left, said as waiting on ops to land those bolts, and listed with the answered cards. `landings_step` already leaves an answered card while a ticked bolt is still to land. The sweep's view of the row is one read: a kit not read, a head not yet read, a verification at a new head. Taking the wait as ended from that one read is a guess (`read.1`), and on 2026-11-08 it cost the user's send.

**Recording an ended card.** A card the owner's list no longer holds and `get_request` reports ended (`cards.ended`) is recorded closed there, as ended in Pending You already, with its answer and send, or withdrawn. Pending You is sent nothing. A batch's row then goes, as `batch_closed` already reads a close (`briefs.12`: a close in Pending You answers a batch). Any other row still waiting is a row with none, raised by the sweep's existing raise.

**Alternatives.**
- Leave ended cards until an act tries to change them (today). Ruled out: the rail names open a card the user can no longer see.
- Raise no new card for a row whose card the user dismissed. Ruled out: each wait on the user is one open card (record 0031 §2), and a card that ended unanswered is no answer (`briefs.12`'s details on a lost card).

### Decision 6: A card Pending You holds in another name is lost to its recorded owner

**The rule.** A refusal "This is <name>'s card" to a read, change or close in the recorded owner's name, where `<name>` is not the owner, is read as lost: `cards.held_elsewhere(words, owner)`, true where `cards.lost` is true too. It is recorded with `card_lost`, the words naming who holds it. The sweep's existing lost paths then post the row's card again in the owner's name, saying the older copy is dead, or post nobody when its row is gone. Either way the card leaves the rail's open cards.

**What is not read as lost.** The sweep's own asks in crew's name are refused as the holder's card by design (`cards_fetched`), so only a refusal to the recorded owner counts.

**What it means for madswan.** madswan's sixteen batch cards are recorded lost and leave the rail on the first read after this lands. The user's app keeps those copies, which the sweep's line names as held by swancloud-planner, for the user to dismiss. crew closes nothing in swancloud-planner's name (`briefs.17`).

**Alternative.** Close the copy in the name Pending You gives. Ruled out: that name is no owner the record knows for the card, and acting in it is what `briefs.17` refuses.

### Decision 7: A row shows one card, and a stray card whose close keeps being refused says so

**One card.** `rail_text` names as a row's card the one open in the row owner's name (`row_owner`). Any other card open under its key is named on its own line as a copy that is not the row's, with whose it is. The row's card line is what an owner reads to know whether its row has a card. Two lines left it guessing which is the row's.

**A refused close.** An open card whose row is gone, which the sweep did not close, is listed with its last refused close's words where there is one. "A later rail read here closes it" is said only where no close was refused.

### Decision 8: Each bolt's land line says whether its card carries, holds or follows it, and a bolt's time is the user's only while a card carrying it waits on them

**The card's stand.** A decision of facts alone, `card_stand` (`code.7`), reads, for each bolt on a kit's land row:
- the open card under `land/<kit>` in ops's name: its last post or change's rows (`card_heads`, `heads_taking`) and its answer;
- the sends kept on closed cards (`landings_sent`).

It gives one of:
- **carried**: the open card waits on the user and shows the bolt, naming the head shown when the bolt's head moved;
- **held**: the open card is answered and its answer ticked the bolt, or a kept send names the bolt and no open card shows it. A raise leaves out exactly the bolts whose send stands (`rows_unsent`), so the rail needs no git read to agree with it;
- **follows**: the bolt can land and neither of the above holds, naming whether the card that carries it follows an answered one;
- nothing, for a bolt that can't land and is no row of the card.

`record_reading` gives `rail_rows` what it needs in `held`, so `rail_rows` still reads only what the read holds.

**A bolt's time.** `bolt_facts` changes in three ways:
- a card's span for the user ends at its answer or its close, whichever comes first;
- the kit's landings card is the bolt's only while its last post or change names the bolt, from the later of that entry and the bolt's last merge (an older entry with no `Heads` counts, as today);
- a question counts only when its post names the bolt or its work.

After an answer, nothing holds the bolt until ops acts. `plan.20` names that holder nobody, and the rail's card line says it waits on ops. Counting every main-level question for every bolt is a guess at what each question concerns (`read.1`). The question in the readings was charged to bolts of four kits.

**Alternative.** A holder for ops, between the user and nobody. Ruled out: `plan.20` names five holders, and a sixth is a rule change, the design agent's to propose (`docs.7`).

### Departure: the last task

`openspec/config.yaml` asks that a change's last task run `tests/suite --affected`. This change's construct stage was briefed otherwise: each task names its narrowest check, no task runs the checks of every part the change touches, and the verify stage runs the repository's whole checks once after every task is done. The tasks follow the stage's brief, and the affected suite is the verify stage's to run. No rule of `docs/architecture/` is departed from.

## Risks / Trade-offs

- [The follower's ask can take ten minutes to see an answer when nothing else moved.] → The owner's own read records the answer at once (`crew card read`, the raise). The rail lags only for an owner that has not acted, which is the case it most needs to show, and it shows it within the ask's window.
- [One `list_pending` per owner at each ask is more work for the bridge.] → It is bounded by the partitions' roles on the host, about a dozen at most. The calls share the ask the follower already makes, and no ask is added to its clock.
- [A user who dismisses a proposal's or a landing's card gets a new card at the next ask.] → That is one open card per wait. The row stays answerable in a pane by the command the rail prints. A user who wants the wait gone answers or drops it.
- [madswan's stale copies stay in the user's app.] → The sweep's line names each one as held under another name, for the user to dismiss. crew does not act in that name.
- [A landings card's older post with no `Heads` cannot say which bolts it carried.] → It counts for every bolt of the kit, as it does today. Every landings card posted since the kits' cards carries `Heads`.

## After deploy

None. Every behaviour here is code proved in the logic tier, by one end-to-end case for the sweep's wiring and the docs' check, and by the mod's case. The stale cards in the fleet (madswan's sixteen batch cards, afterthought's swancloud-planner copies) are recorded by the first sweep after the release reaches a host, by code in this change, with no step of anyone's.

## Task notes

The logic tier's tests run from `tests/.venv`, which `devenv shell -- moon run tests:venv` syncs from `tests/uv.lock`. One file runs as `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/<file>`.

**1.1** `plugin/lib/plan.py`:
- `answer_due(entries, card)`: a decision of facts. True unless a `card.answer` of `card`, not refused, is among the entries.
- `answer_fields(key, got, heads=None, offered=())`: the entry's fields, `Card`, `Key`, `Answer` (`cards.answer_said`), and `Heads` for a `land/<kit>` key, from `ticked_of(got, heads)` at the heads shown. None when the reply holds no answer.
- `answer_seen(acts, label, owner, key, card, got, entries, heads=None, offered=())`: emits `card.answer` on `cards.row_object(key, acts.kits(label))`, or `agent/<owner>`, `by=owner`, when `answer_due` holds.

`plugin/lib/record.py`'s docstring names `card.answer` beside `card.post`, `card.update`, `card.close` and `card.reading`, and says what it carries. Cases in `tests/py/test_card_commands.py`:
- recorded once;
- a landings card's `Heads` are the ticked bolts at the heads shown;
- a question's object is `agent/<asker>`;
- "with a note" and never the note's words.

**1.2** `kit_card_state` calls `answer_seen` when Pending You gives the card answered, with the heads its last post or change recorded and the boxes offered (`land:<bolt>`). `card_read` calls it for any card it reads answered, before it closes a declined approval or raises the kit's card. Cases:
- `tests/py/test_landings.py`: a raise reading an answered card records one `card.answer` with `Heads`, and a second raise records none;
- `tests/py/test_card_commands.py`: `crew card read` of an answered proposal card records its answer.

**1.3** `cards_fetched`, or a helper beside it that the follower's tick calls with it, takes the owners of the cards the sweep asks after, adding each open record card's and each held card's owner. In the one bridge it calls `list_pending` with `{"name": owner}` once per owner, then `get_request` in the owner's name for each open card on the agent's turn with no `card.answer` yet, and for each the list does not hold.

`sweep_cards` gets those replies beside `found`:
- for each card read answered, it calls `answer_seen` and reports `did="answered"` with the answer's words;
- the cards read absent go to Decisions 5 and 6 (tasks 3.1 and 3.2).

`sweep_judgments`/`cards_asked` add the open record cards to what is asked, so their answers are read too. Cases in `tests/py/test_rail.py`: with fake acts, a held proposal card on the agent's turn records `card.answer` once; a card already recorded answered is read no more.

**2.1** `plugin/lib/cards.py` `close_call`: for a card whose status is answered, `ack_answer` with `close_words(got, outcome, reason)` and the state "closed" always. Cases in `tests/py/test_cards.py`:
- answered with a reason alone: ack, closed;
- waiting with a reason: cancel, withdrawn;
- answered with an outcome: ack, closed.

**2.2** `card_closed`: for a `land/<kit>` key whose reply holds an answer, `Heads` from `ticked_of` at the heads of the card's last post or change (`card_heads`), unless `more` gives `Heads`. The same on the ended-in-Pending-You path, which also keeps `Answer`. `kit_card_state`: a reply `cards.ended` reads as ended is recorded closed there (the ended path, with `Answer` and `Heads`), and the state returned is none held (`{"status": None}`), as a lost card's is. Cases in `tests/py/test_landings.py`:
- an answered landings card closed by the sweep keeps `Heads`, and the next raise has no row for the ticked bolt at its head;
- a card ops acked in Pending You, read resolved at a raise, is recorded closed with `Answer` and `Heads`, and the raise posts with no row for it.

**2.3** `sweep_judged`: before the gone judgment, a `land/<kit>` card (`kit` in `kits`) whose `card.answer` names in `Heads` a bolt with no `bolt.land` or `bolt.drop` entry, not refused, after the answer, is left in a new list, `waiting_on_owner: [(card, bolts)]`. `sweep_cards` reports each as `did="left"`, "answered: waits on <owner> to land <bolts>". `stray_cards` leaves it out, and the rail lists it with the answered cards (4.1). Cases in `tests/py/test_rail.py` (`TestSweepJudged`):
- the row is gone with a ticked bolt not landed: left, nothing withdrawn;
- the ticked bolt landed: gone, closed as answered.

**3.1** From 1.3's reads, a card absent from its owner's list whose `get_request` `cards.ended` reads as ended: `sweep_cards` records its close with `card_closed`'s ended path, sending nothing. Answered: closed with `Answer` and, for a landings card, `Heads`. Cancelled or expired: withdrawn. It reports `did="closed"` or `"withdrawn"`, "ended in Pending You already". `swept_cards` drops it from the read's cards. Cases in `tests/py/test_rail.py`:
- a cancelled proposal card is recorded withdrawn and its row is in the next judgment's `none`;
- a resolved question is recorded closed and listed nowhere;
- a cancelled batch card closes its batch's row (`batch_closed`).

**3.2** `plugin/lib/cards.py`:
- `held_elsewhere(words, owner)`: true when `words` read "This is <name>'s card" with `<name>` not `owner`;
- `lost(words, owner=None)`: true for it when an owner is given;
- `lost_said`: names who holds it.

Pass the owner where crew reads, changes or closes in an owner's name: `card_closed`, `kit_card_state`, `row_card_change`, 1.3's reads. The sweep's own asks in crew's name (`SWEEPER`) pass none. Cases:
- `tests/py/test_cards.py`: madswan-planner's refusal of 2026-10-26, quoted, is lost to madswan-planner and not to swancloud-planner, and no other refusal is;
- `tests/py/test_rail.py`: a gone `batch/16` card refused so is recorded lost and no longer a stray; a held proposal card refused so is posted again in the planner's name.

**3.3** `rail_text`:
- under a row, the card line names the card open in `row_owner`'s name, the newest;
- each other card open under the row's key gets `also:   <card>, <by>'s, open under <key>, not the row's card`;
- for a stray card, `last_close_refusal(entries, card)` (new, beside `last_refusal`) gives `left:   its last close was refused: <words>` where it has one, else the existing words.

`board.marker` takes the owner's card too. Cases in `tests/py/test_rail.py`:
- afterthought's `proposal/508`, with afterthought-planner's and swancloud-planner's cards;
- a stray whose close was refused.

**4.1** `record_reading`: each open card gets `answered`, `{at, answer, heads}` from its first `card.answer`, or None. `rail_text`:
- An answered row card: `card:   <key>, answered <HH:MM> (<age> ago): <answer>; <waits> (<card>)`. `<waits>` by the key's kind:
  - `land/<kit>`: "waits on <owner> to land <bolts of Heads>", or "sent with no bolt ticked: waits on <owner> to close it";
  - `proposal/`: "waits on <owner> to apply it" when approved or ticked, else "waits on <owner> to act on it";
  - `batch/`: "waits on <owner> to hand on its notes";
  - `deploy/`: "waits on <owner> to record your word", or "your word stands: the deploy's end closes it" when `ops.word_stands`;
  - `op/`: "waits on <owner> to record it";
  - anything else: "waits on <owner> to act on it".
- `question_cards` and `record_cards` leave answered cards out. A new list, `answered_cards`, gathers answered questions, answered record cards and 2.3's landings cards with no row, under the heading `answered, waiting on their askers:`, one line each: `<when>  <age>  <key> (<label>), asked by <by> on <host>, answered <HH:MM>: <answer>; <waits>`.

Cases in `tests/py/test_rail.py` (`TestText`): each kind's line; an answered question and record card under the new heading and not the old; an unanswered card as today.

**4.2** `card_stand(bolt, head, can, card, sends)`, a decision of facts:
- `card` is None, or `{card, heads: [(bolt, head7, left)], taking, answered: {heads} or None}`;
- `sends` is `landings_sent`'s `{bolt: head}`;
- returns `("carries", shown_head or None)`, `("holds",)`, `("follows", after_answered)` or None.

`record_reading` keeps in `held` each landings key's open card in ops's name, with its last post or change's `Heads` and its answer, and the sends (`landings_sent`). `rail_rows` appends the words to each bolt's line after `lands`/`can`, before the time:
- `carried by land/<kit>, waiting on you`;
- `carried by land/<kit> at <h>, its head now <h>, waiting on you`;
- `held by your send on land/<kit>: <label>-ops lands it`;
- `follows: the next card under land/<kit> carries it`;
- `follows: the card after land/<kit>'s answered one carries it`.

Cases in `tests/py/test_rail.py`, one per scenario of crew-rail "Each bolt's land line says whether its card carries, holds or follows it".

**4.3** `tests/t-cards.sh`, one case for the sweep's wiring (`tests.12`): a proposal card's answer is steered (`$stub/answered/<id>.json`) and `crew rail` runs. Its sweep records one `card.answer`, its row's card line says answered and that it waits on wldn-planner to apply it, and the stub's log shows one `list_pending` in wldn-planner's name. Then update:
- the expectations this case and the call sequences of the rail's reads in `t-cards.sh` now carry;
- the opening comment's "crew card read … recording nothing", since `crew card read` of an answered card now records its answer.

The stub's `list_pending` already answers in the name given, and its `refuse` file steers a refusal, so the stub needs no change (`tests.4`).

**5.1** `bolt_facts`:
- a card's span ends at its first `card.answer` or its close, whichever is first;
- for `land/<kit>` (`kit_name != bolt`), spans per post or change whose `Heads` name the bolt, from the later of the entry and `last_merge`, ended by a change not naming it, the answer or the close; an entry with no `Heads` names every bolt;
- the clause counting a main-level question since the start goes; `ours(c["on"])` stays.

Cases in `tests/py/test_bolt_time.py`, one per new scenario of crew-board "Each holder is read from what crew already keeps", the rest unchanged.

**5.2** `plugin/lib/board.py`:
- `board_data`'s cards carry `answered` (ISO) and `answer`;
- `marker`'s card carries `answered`;
- `card_line` says `answered <age> ago, yours to act on` for an answered card;
- `ops_view`'s land line adds `answered: the landing is yours` when its marker's card is answered;
- the views' shape case in `tests/py/test_board.py`, which pins every key the mod reads (`code.8`), takes the new keys.

Cases in `tests/py/test_board.py`: the planner's answered proposal card; ops's answered landings card and its land line.

**5.3** `plugin/tests/status.test.ts`: a case handing ops's views an answered card line, `your card  land/sluice  req_e9  answered 5m ago, yours to act on`, drawn above its view as given. `plugin/hooks/status.js` changes only if the case shows it must.

**6.1** README, *Operations*, where it describes the rail's card lines and the sweep: an answered card's line and whose act it waits on; the answered list; a row's one card; each bolt's card stand; the sweep recording answers and ended cards. `plugin/skills/crew/SKILL.md`'s `crew rail` row, and `plugin/bin/crew`'s usage header for `crew rail`, say the sweep records answers and ended cards (`docs.2`).
