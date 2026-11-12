# Design

## Context

This section records what was read on 2026-11-12, on deneb, so the decisions below rest on it.

**What crew sent and what Pending You said.** deneb's run record of agentplot (`agentplot/main` of afterthought/crew-state, `runs/deneb/2026-11-11.rec` and `2026-11-12.rec`):
- `land/boomdrive`'s card `req_313e35ea…` was a list of two rows. It was answered, and closed at 23:09:33Z with six bolts proven since the send.
- From 23:09:37Z, every post of the card that follows it was refused, about every eleven minutes, seven rows and then eight. Each refusal: "Pending You refused post_request: With questions, each question carries its own highStakes; leave the card’s highStakes out."
- crew 0.59.0 (tag `v0.59.0`, which holds fix 6f6ff0fe) builds that card as two questions of four boxes. Each question carries `highStakes: true`. The card carries no `highStakes` and no `rationale`. This was read by building it with `v0.59.0`'s `cards.landings_card`, eight rows, one taking main first, following a card. `cards.opened`, `post_args` and the bridge add no field.

**What Pending You has taken.** The run records of agentplot, swancloud, madswan and wldn from 2026-11-04 to 2026-11-12, and agentplot-design's transcript on deneb:
- A landings card of one row, an `approve` of risk high, many times a day.
- One list of boxes carrying `highStakes` on the card: `land/boomdrive` with two rows at 2026-11-11T21:25:19Z, `land/switchboard-kit` with four at 2026-11-10T19:40:36Z and with three at 14:28:15Z.
- A card of two questions carrying no `highStakes` and an `about`: agentplot-design's `ask/agentplot-design/how-boom-fits-six-points-2026-11-11b`, posted at 21:31:43Z and answered.
- No card of questions carrying `highStakes` has ever posted. switchboard-kit's six rows were refused twelve times on 2026-11-10 under crew 0.41.11, which set it on the card. boomdrive's were refused under 0.59.0, which set it on the questions.

**What Pending You says it takes.** Its guide, `https://www.pendingyou.com/skill.md`, revision 2.60: "Post `questions` (2–4) … each has … that kind's fields (`options` and `recommendedIds`, `approve`, `text`, `highStakes`)". More than four questions, or none with no `about`, is refused. The fleet's `pendingyou mcp` 0.41.0, `tools/list`, which posts nothing:
- `post_request`'s `options` hold 2 to 5.
- A question's `options` hold 2 to 5, and it has a `highStakes` of its own.
- `update_request` takes `options` (5 at most), `multi`, `recommendedIds` and `highStakes`, and adds or withdraws a question.
- Neither schema says when `highStakes` is refused. Only the refusal says it, and Pending You refuses the shape its own words and guide ask for.

**Why the stub let it through.** `tests/stubs/pendingyou` and `test_landings.marked_post` refuse a card of questions only when `"highStakes" in args`, the card's own. The fix of 2026-11-10 was proven against that model, and no live post of it ever passed.

**The family.** No other tool of the family builds a Pending You card (flume's requirements, "whoever shows the card"; sluice, timber, weir and boom post none). crew is the one owner of its cards' forms, so the fix is crew's alone. That Pending You refuses its documented shape is the user's to report to Pending You. This change does not wait on it.

**Area pages this change touches:** `core.md` (`roles.5`, `read.1`, `read.2`, `code.7`, `code.8`), `plan.md` (`plan.16`), `briefs.md` (`briefs.11`, `briefs.13`, `briefs.16`), `tests.md` (`tests.4`, `tests.6`, `tests.11`, `tests.12`) and `docs.md` (`docs.4`, `docs.7`). No rule changes, so no page is edited (`docs.7`).

## Goals / Non-Goals

**Goals:**

- A kit's landings card is posted whatever the number of its rows, in a form Pending You has taken, so the user always has a card to send them on.
- The landing keeps its hold-to-send: every landings card carries `highStakes` or an approval of risk high.
- Every row stays on the card in the plan's order, and a row with no box gets one on the card that follows the user's send, with no wait.
- crew's stub and fake refuse what Pending You refused, so a test finds it the next time.

**Non-Goals:**

- A deploy's card waiting on four or more steps, which builds lists of questions carrying `highStakes` too (see Risks).
- A proposal's card of more than five new units, which asks questions with no `highStakes`, a shape Pending You takes.
- Pending You's check. Its words and its guide disagree with what it refuses. That is Pending You's to mend and the user's to report.
- A retry of a refused card in another form. The rail's sweep already posts a refused card again after `CARD_RETRY` (rail-cards "A row's card that Pending You refused is owed until it posts").

## Decisions

### 1. A landings card asks no questions: it is an approval or one list of at most five boxes

One row stays an `approve` of risk high. Two or more rows are one list, `kind: multi`, carrying `highStakes` and `rationale` on the card, as two to five rows are today. `landings_form` gives "approve" or "multi", and "lists" goes.

A list holds five boxes at most, so a card of more than five rows gives five of them boxes (Decision 2). The others stay on its face (Decision 3).

Other paths, not taken:
- **Lists of questions, with no `highStakes` on any of them.** Pending You takes that shape. But a landing cannot be undone, and its card must carry the hold-to-send (record 0031 §5). The user would land eight bolts on one tap.
- **Lists of questions as built, waiting for Pending You to mend its check.** The user has had no card for boomdrive's eight bolts since 23:09Z. Lists also stop at four questions, twenty rows, so they never held every count of rows.
- **One card per five rows, under `land/<kit>/<n>`.** Record 0031 as amended 2026-10-23 keeps one card per kit, the order of the landings on one card, and one send for all the user ticked.
- **Lists first, and one list when Pending You refuses them.** That posts a form known refused at every raise, records a refusal each time, and keeps the outcome on Pending You's words. `read.1` asks for no guess, and here the facts are in: only one list has ever posted.

This is the unit's reading of Pending You's forms, which record 0031 as amended 2026-10-23 leaves to the unit ("Not decided here, the unit's reading of Pending You's forms as §5 leaves it"). It keeps `briefs.13`'s landings card: every proven bolt in the order they land, each row as its own card was, and the user's ticks and one send the word to land them in that order. A row with no box is on the card and is not ticked on it. It is asked for by the card that follows the send (Decision 5).

### 2. The five boxes go to the rows crew would tick, then to the others, each in the rows' order

`cards.landings_boxed(rows)` is a decision on plain facts (`code.7`). `rows` are the card's rows in order, each with `bolt`, `left` and `taking`. It gives the bolts that get a box:
- every bolt when there are five or fewer;
- else the rows crew ticks (neither left nor taking main first) in order, then the left and taking rows in order, the first five of that.

The boxes keep the rows' order on the card, and each box is labelled with its row's place among all the rows, `<n>. <bolt>`, so the face and the boxes number alike. `plan.landings_step` calls the same function, so the card and its raise agree on which rows have boxes.

Not taken: the first five rows in order. Then a row the user left, or one taking main first, would hold a box no one means to tick, while a row ready to land waits with none. Five rows crew would tick then never fit on one card, and the user sends less than they could.

### 3. A row with no box stays on the face in its place, and is recorded `:next`

On the face every row keeps its paragraph (`row_paragraph`), in order. A row with no box is marked after its bolt, ` · *waits for a box*`, as a row taking main first is marked today. The summary says how many rows wait for a box and that the card that follows the user's send asks for them, with no list of names, so it holds to `SUMMARY`. The details keep every row's line, as today.

`heads` marks each row with no box `:next`, after `:main` or `:left` when it has one, so `b1@abc1234:left:next` is a left row with no box. The post's and change's `Heads` carry it (`built_fields`). So the next raise knows which rows the card showed without a box:
- `card_heads` reads the mark and goes on giving `(bolt, head, left)`;
- `heads_taking` reads `:main` with or without `:next` after it;
- the new `heads_next` gives the bolts marked `:next`;
- `offered_boxes` leaves them out, as it leaves rows taking main first;
- `kit_card_state` hands them to `landings_step` as the card's `next`.

Not taken: leaving rows with no box out of `Heads`. A raise would then read each of them as joining the card, every time, and change the card with nothing changed. switchboard-kit's card was sent "Nothing changed" changes about every thirty seconds on 2026-11-11 from 18:48Z for a cause of the same kind.

### 4. A row coming to a box or losing one changes the card in place

In `landings_step`'s waiting branch, the rows shown now (`card_rows`) and the boxes they would have now (`landings_boxed`, with `left` as the step reads it) are set against the card's recorded rows and its `next`:
- a row with a box now, recorded `:next`: "<bolt> has a box now";
- a row with no box now, recorded with one: "<bolt> waits for a box".

Each is said with the step's other sentences. The form stays "multi", since `landings_form` reads every row shown, so `kind_changed` is false, the card has no questions, and `row_card_change` changes it in place through `update_request`. That call takes `options`, `multi` and `recommendedIds` (`cards.CHANGED`) up to five boxes. A card moving between one row and two is followed, as today.

### 5. The user's send of a card with rows waiting is followed at once

In `landings_step`'s answered branch, a row the card recorded `:next` counts as proven since the send, as a row recorded `:main` does today: it is in `anew`. So a send that lands rows returns `("follow", …)`. The card is closed, and the card that follows asks for every row the send does not land, the rows that waited among them. A send that ticks none returns `("close", …)`, and the next raise posts the new card, as today.

A row recorded `:next` is not one the user left:
- it is left out of `cleared`, so the close never says "Left:" of it, and `landing.left` does not record it;
- `left_now` reads an answered card's row recorded `:next` as left only when it was also marked `:left`, the user having left it on an earlier send. So a left row keeps its leave while it waits for a box, and is unticked on the card that follows.

The close's words name the rows that had no box: "Since your send, … ; <rows> had no box on this card, and the card that follows asks for them." `landings_since` says of the rows a followed card recorded `:next` "<rows>, which had no box on your last card, wait on this card", not "which you left". It reads them with `heads_next` from the followed card's `Heads`.

The time a row waits with no box stays the user's on the bolt's clock (`plan.20`, `landings_spans`). Its box comes at their send, and `card_heads` still names it among the card's rows.

### 6. The stub and the fake refuse what Pending You refused

`tests/stubs/pendingyou`'s `post_request` refuses a card of questions carrying `highStakes` on the card or on any question, in Pending You's words, as it refused boomdrive's on deneb from 2026-11-11T23:09Z (`tests.4`). A card of questions with no `highStakes` is taken, as agentplot-design's was.

`tests/py/test_landings.py`'s `marked_post` refuses the same, in the same words. `MARKED_WORDS` keeps Pending You's apostrophe as the stub and its refusal on deneb have it.

No end-to-end test posts a card of questions carrying `highStakes`. `t-cards`'s proposal of six rows carries none and is still taken.

### Rules relied on

- `roles.5`: crew wraps Pending You, and its cards' forms are Pending You's, read from what it takes. crew builds no form beside them.
- `read.1`, `read.2`: crew reads Pending You by what it does now, its refusals and its posts, not by its guide's words. It posts no form it has never seen taken.
- `code.7`: `landings_boxed`, `landings_step`, `left_now`, `landings_since` and the heads readers are decisions on plain facts, tested in the logic tier.
- `code.8`: no bolt, unit, stage, card key or rail row changes shape. Which rows of a card have a box is the card's, not the row's, so the views and the mod are untouched.
- `plan.16`, `briefs.11`, `briefs.13`: one landings card per kit, its rows in the order they land, one send the word for all the user ticked.
- `briefs.16`: crew posts and changes its own cards, recording each under the row's key.
- `tests.4`: the stub refuses as Pending You does. `tests.6`: the brief's new sentence is pinned in `t-briefs`. `tests.11`, `tests.12`: the cases are in the logic tier.
- `docs.4`, `docs.7`: the spec changes through this change's delta, and no rule page or record is edited.

### Departures

None.

## Risks / Trade-offs

- **[A deploy's card of four or more steps meets the same refusal]** → `cards.deploy_card` builds lists of questions, each carrying `highStakes`, once a deploy waits on four or more steps of the user's: four step boxes and the deploy's are more than five. Pending You will refuse it as it refused boomdrive's landings card. The stub now refuses it too, so a test that posts one fails. That card's own form is a change of its own, for the planner: steps cannot wait for a later card as rows do, since every one must be ticked for the deploy.
- **[Pending You mends its check]** → One list still posts. Asking eight rows on one card again would be a change of crew's own, once Pending You has been seen to take questions carrying `highStakes`.
- **[Eight bolts take two sends]** → The second card follows the first send at once, asking for the rest. The landings themselves are queued in order either way.
- **[A row the user would land first has no box]** → Boxes go to the rows crew would tick, in order, so a row with no box is a later one in the plan. A note on the card can move one in the order, which main-level ops reads, as today.

## Migration Plan

None. `land/boomdrive` stays owed on deneb's rail. The rail's sweep posts it again once crew at this change runs there, as one list of five boxes with three rows waiting. Nothing is done by hand.

## After deploy

None: every outcome here is a logic-tier case or a stub's, and nothing waits on a host or on the user.

## Task notes

**1.1** `plugin/lib/cards.py`:
- `BOXES`'s comment names its source: Pending You's most options in a list, a card's or a question's, `post_request`'s and `update_request`'s `options` (`tools/list`, pendingyou 0.41.0, read 2026-11-12). Keep its note on proposals' questions.
- `landings_form(n)` is "approve" for one row and "multi" for more. Its docstring says a landings card asks no questions, and why (Decision 1).

Case: `TestLandings::test_the_form_by_how_many_rows_can_land` gives "approve" for 1 and "multi" for 2, 5, 6 and 20.

**1.2** `cards.landings_boxed(rows)`, after `landings_form`. `rows` are dicts with `bolt`, `left` and `taking`, in the card's order. It returns the bolts with a box, in the card's order (Decision 2). Cases, in a new class `TestLandingsBoxed` in `tests/py/test_cards.py`:
- five rows or fewer: all;
- eight rows that can land: the first five;
- seven rows, the first left and the second taking main first: the third to the seventh;
- six rows that can land and a left row first: the first five of those that can land;
- seven rows, three left: the four that can land, then the first left row.

**1.3** `cards.landings_card`, for more than one row:
- One list always. The `else` branch of lists goes, with its `about` and its questions. `shape` is `kind="multi"`, `intent="decide"`, `options` of the boxed rows only, `multi={"min": 0, "max": len(boxed)}`, `recommendedIds` the boxed rows crew ticks, `rationale=then` and `highStakes=True`.
- `option(i, r)` keeps `i` as the row's place among all rows.
- `row_paragraph` takes whether the row has a box. A row with none is marked ` · *waits for a box*` after its bolt and any mark it has today: ` · *left on your last send* · *waits for a box*` for a left row, ` · *takes main first* · *waits for a box*` for one taking main first.
- The summary adds, when any row has no box: "<k> more wait below with no box yet; the card that follows your send asks for them." `prose` cuts it to `SUMMARY` as before.
- `heads` adds `:next` to each row with no box, after `:main` or `:left`.

The docstring says all of it. Cases, replacing the three lists cases in `TestLandings`:
- `test_eight_rows_are_one_list_of_five_boxes_the_rest_waiting_on_its_face`: `landings(8)` is `kind` "multi", options `land:b1` to `land:b5` labelled `1. b1` to `5. b5`, no `questions` and no `about`, every row's paragraph on the face in order, and `b6` to `b8` each marked ` · *waits for a box*`.
- `test_more_than_five_rows_carry_high_stakes_and_what_follows_on_the_card_and_ask_no_questions`, parametrised on 6, 8 and 21: `highStakes` true and `rationale` "After you send: …" on the card, `questions` absent, five options.
- `test_rows_with_no_box_are_marked_next_in_the_cards_heads`: eight rows, `b1` left on the last send and `b2` to `b8` able to land. The boxes go to `b2` to `b6`, so `heads` are `b1@abc1234:left:next`, `b2@abc1234` to `b6@abc1234`, `b7@abc1234:next` and `b8@abc1234:next`, and the summary says "3 more wait below".

**2.1** `plugin/lib/plan.py`:
- `card_heads`'s pattern takes `(:left|:main)?(:next)?` and still gives `(bolt, head, left)`.
- `heads_taking` takes `:main` with an optional `:next` after it.
- New `heads_next(text)`, beside `heads_taking`: the bolts marked `:next`.
- `offered_boxes` leaves out bolts in `heads_next(shown)`.
- `kit_card_state` returns `next` beside `taking`.

Case: `tests/py/test_landings.py::test_a_rows_next_mark_is_read_as_a_row_with_no_box`. Given `"a@abc1234 b@abc1234:left:next c@abc1234:main:next d@abc1234:next"`:
- `card_heads` gives four rows, `b` left;
- `heads_taking` gives `{c}`;
- `heads_next` gives `{b, c, d}`;
- `offered_boxes` gives `["land:a"]`.

**2.2** `landings_step`, waiting branch (Decision 4). It takes the card's `next` as it takes `taking`. It computes the boxes now with `cards.landings_boxed`, over `shows`, `left` and the rows taking main first. It adds "<b> has a box now" for a row in `card["next"]` with a box now, and "<b> waits for a box" for a row shown with a box that has none now. Cases in `tests/py/test_landings.py`:
- `test_a_row_coming_to_a_box_changes_the_waiting_card_in_place`: eight rows recorded, `b6` to `b8` `:next`. `b2` is now held for a fix. The step is `("change", …, False, [])`, its note naming `b2`'s hold and saying "b6 has a box now".
- `test_a_row_with_no_box_whose_head_moves_changes_the_card_and_keeps_it_with_no_box`: `b7` recorded `:next` at `abc1234`, now at `def5678`. A change saying `b7`'s head is now `def5678`, kind unchanged.

**2.3** `landings_step`, answered branch, and `left_now` (Decision 5):
- `anew` takes each bolt in `card["next"]` as it takes those in `took`.
- `cleared` leaves out bolts in `card["next"]`.
- The "Since your send" sentence says "<rows> had no box on this card" for those, in place of "reads proven".
- `left_now`'s answered case: a row in `card["next"]` is left only when `marked`.

Cases in `tests/py/test_landings.py`:
- `test_a_send_with_rows_waiting_for_a_box_is_followed_at_once_by_a_card_asking_for_them`: eight rows, `b1` to `b5` ticked, `b6` to `b8` recorded `:next`. The step is `("follow", outcome, [], [(b1, …) … (b5, …)])`, the outcome naming `b6`, `b7` and `b8` as having had no box and saying no "Left:".
- `test_a_left_row_waiting_for_a_box_stays_left`: `left_now` on an answered card whose `b1` is recorded `:left:next`, unticked, gives `b1` left. A row recorded `:next` alone, unticked, is not left.
- Through `plan.raise_landings` with `LandActs`: `test_a_send_with_rows_waiting_for_a_box_posts_the_card_that_follows_asking_for_them`. An answered card of eight rows, five ticked, is closed and a card follows it whose options are `b6` to `b8`, all recommended, recorded with `Heads` "b6@abc1234 b7@abc1234 b8@abc1234".

**2.4** `landings_since(earlier, rows, waited=())` takes the bolts the followed card recorded `:next`. The caller, at the raise of a card following another (`plan.py` around 3837), reads them with `heads_next` from the same `Heads`. A row among them still at its head is said "<rows>, which had no box on your last card, wait on this card", and not among `left_waits`. Case: `tests/py/test_landings.py::test_the_card_that_follows_says_the_rows_that_had_no_box_wait_on_it`.

**3.1** `tests/py/test_landings.py`:
- `marked_post` refuses a card of questions carrying `highStakes` on the card or on any question.
- The comment above `MARKED_WORDS` adds boomdrive's refusals on deneb from 2026-11-11T23:09Z (signal `2026-11-12-agentplot-ops-6907cc32/01` on agentplot/main of afterthought/crew-state).
- `test_six_proven_bolts_post_one_card_of_lists_each_marking_its_stakes_and_the_card_none` becomes `test_eight_proven_bolts_post_one_list_of_five_boxes_and_nothing_is_refused`. Eight rows through `plan.raise_landings` on `marked_post`: posted as `kind` "multi" with `highStakes` true and no `questions`, five options, and one `card.post` emitted with no `refused`, its `Heads` ending `b6@abc1234:next b7@abc1234:next b8@abc1234:next`.
- `test_rows_leaving_a_card_of_boxes_for_one_that_can_land_follow_it_with_an_approval_never_changed_in_place` and the other cases on `landings_form` still pass unchanged.

**3.2** `tests/stubs/pendingyou`: `post_request` refuses with `MARKED_WORDS` when `args.get("questions")` and `"highStakes"` is in the card or in any of its questions. The docstring says so, citing deneb's boomdrive refusals of 2026-11-11 and 2026-11-12 beside the Willdan box's of 2026-11-10. `t-cards` posts a proposal of six rows as two questions carrying no `highStakes`, which the stub still takes. `t-journey-land` posts a kit's landings cards through the stub.

**4.1** `plugin/roles/main-ops.md`, in the paragraph on the word to land, after "a bolt they cleared waits for a later card": "A row past the card's five boxes waits on its face with no box, no word to land, and the card that follows their send asks for it." `tests/t-briefs.sh` pins "A row past the card's five boxes waits on its face with no box" among main-level ops's phrases (`tests.6`).

**4.2** `README.md`, the paragraph on the landings card's form: "one of two to five rows is one list of boxes carrying `highStakes`, the same test, and one of more is lists of five" becomes "one of two or more rows is one list of boxes carrying `highStakes`, the same test, five boxes at most: past five, the rows crew would tick first have the boxes, the rest wait on its face with none, and the card that follows the user's send asks for them". In the same section, "a list of ticked boxes for more" stays.
