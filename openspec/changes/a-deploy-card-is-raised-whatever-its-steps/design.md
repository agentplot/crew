# Design

## Context

This section records what was read on 2026-11-14, so the decisions below rest on it.

**The signal.** agentplot-planner, 2026-11-12T02:48Z, from batch 57's summary of `a-landings-card-is-raised-whatever-its-rows`: "A deploy card waiting on four or more of your steps is still built as questions marked high stakes, and Pending You will refuse it the same way; the test stand-in now refuses it too. Fixing it is left to the planner as its own change, since a deploy's steps cannot wait for a later card the way rows can." The planner queued this unit on it (proposal 167, agentplot/main 49aa81c6). Its intent asks for a form Pending You takes, "keeping the hold to send on a deploy and every step it waits on on the one card".

**What crew builds now** (`plugin/lib/cards.py` `deploy_card`, read at this branch's base):
- While a step the deploy waits on is open, the options are a box per open step, `before:<n>` labelled `Done: <n>. <words>`, then `deploy`.
- Five options or fewer are one list, `kind: multi`, with `highStakes` and `rationale` on the card.
- More than five are split evenly into lists of questions, `before-<k>`, each carrying `highStakes` and `rationale`, under an `about`. Four open steps make five options, so the lists start at five open steps. `tests/py/test_ops.py::TestTheDeployCardOfAStepItWaitsOn::test_more_boxes_than_a_list_holds_are_asked_as_lists_each_carrying_what_follows_a_yes` pins two lists for five steps.

**What Pending You takes and refuses**, as `a-landings-card-is-raised-whatever-its-rows` read it from the run records of four drives (its design's *Context*):
- It takes an approval of risk high, many times a day.
- It takes one list of up to five boxes carrying `highStakes` on the card.
- It takes a card of questions carrying no `highStakes` anywhere.
- It refuses a card of questions carrying `highStakes`, on the card (the Willdan box, 2026-11-10) or on each question (deneb, 2026-11-11), in the words "With questions, each question carries its own highStakes; leave the card’s highStakes out."
- No card of questions carrying `highStakes` has ever posted. A list holds 2 to 5 options (`post_request`'s and `update_request`'s `options`, pendingyou 0.41.0, read 2026-11-12).

**What the word must be.** The user's own decision, swancloud record 0038 (accepted 2026-10-26): "the user's word for that deploy is given only once each is ticked, so the card's yes with a step unticked is not the word". `plan.14` carries it: the word is "given only once each step of the user's the deploy waits on is ticked on that card". Record 0031 §5 makes a deploy's card held to send. Record 0059 is the code stage's reading of record 0038, each of its choices "cheap to change; none is the user's alone". Its Decision 2 gives "a box for each open step … five to a list", and its Decision 5 refuses an approval naming each step neither ticked nor done (`ops.ticked_refusal`).

**How the send reaches crew.** Main-level ops reads the user's answer and runs the row's answer with `--ticked <n>,...`, naming each step box ticked by its number (`plugin/roles/main-ops.md`, *An offer*). `ops.approve` refuses, recording only the refusal, while any step is neither ticked nor done. No code of crew's parses a deploy card's box ids: `cards.BOX` reads only `land:` and `add:`.

**The family.** No other tool of the family builds a Pending You card (flume's requirements, "whoever shows the card"; sluice, timber, weir and boom post none). crew is the one owner of its cards' forms, so the fix is crew's alone. The deployer, swancloud's, hands the steps and holds the environment until crew reports each step done. It is unchanged, since crew still records each step done on its own key.

**The open change beside this one.** `an-offer-card-shows-the-step-the-deploy-waits-on-first` built the boxes and is not archived. Its proposal, design, spec and tasks say the card asks lists of five. This change rewrites those sentences to one list (`docs.3`).

**Area pages this change touches:** `core.md` (`roles.2`, `roles.3`, `roles.5`, `read.1`, `read.2`, `code.7`, `code.8`), `plan.md` (`plan.14`), `briefs.md` (`briefs.11`), `tests.md` (`tests.4`, `tests.6`, `tests.11`, `tests.12`) and `docs.md` (`docs.2`, `docs.3`, `docs.4`, `docs.7`). No rule changes, so no page is edited (`docs.7`).

## Goals / Non-Goals

**Goals:**

- A deploy's card is posted whatever the number of steps it waits on, in a form Pending You has taken.
- The card keeps its hold to send: one list carrying `highStakes`, or the approval of risk high.
- Every step the deploy waits on is on the one card, each ticked before the word, and the word is that card's one send.

**Non-Goals:**

- Pending You's check, which refuses the shape its own words and guide ask for. That is Pending You's to mend and the user's to report.
- A deploy's card with no step open, which stays the approval of risk high.
- A proposal's card of more than five new units, which asks questions with no `highStakes`, a shape Pending You takes.
- A retry of a refused card in another form. The rail's sweep already posts a refused card again after `CARD_RETRY` (rail-cards "A row's card that Pending You refused is owed until it posts").

## Decisions

### 1. A deploy's card is one list of at most five boxes, and asks no questions

While a step the deploy waits on is open, the card is one list, `kind: multi`, `intent: decide`, `highStakes` and `rationale` on the card, `recommendedIds` empty, as a card of five boxes or fewer is today. The deploy's box is last. The `else` branch that builds lists of questions goes, with its `about`.

Other paths, not taken:
- **Lists of questions with no `highStakes`.** Pending You takes that shape. But a deploy is not undone, and its card must be held to send (record 0031 §5, `plan.14`). The user would deploy on one tap.
- **A question of kind `approve`, risk high, beside lists of steps carrying no `highStakes`.** Pending You has never been seen to take one. crew posts no form it has not seen taken (`read.1`, `read.2`).
- **Five steps' boxes on the first card, and the rest and the deploy's on the card that follows the send**, as the landings card does with its rows. The steps would no longer be on the one card that carries the deploy's box, as the intent asks. Each send would have to record its ticked steps done with no word, which record 0059 Decision 5 refuses: a send with a step left is recorded only as a refusal. And the user would send twice for one deploy.
- **The approval of risk high, every step on its face, past four open steps.** It is held to send and posts. But no step is ticked at all, and the user's hold would be the word with nothing on the card saying each step was done (swancloud record 0038).

### 2. Past four open steps, the fourth box holds the rest

`cards.deploy_boxes(numbers)` is a decision on plain facts (`code.7`). `numbers` are the open steps' numbers in the card's order. It gives the step boxes as lists of numbers:
- four or fewer: one list per step, `[["1"], ["2"], …]`;
- more: the first three alone, then one list of the rest, `[["1"], ["2"], ["3"], ["4", "5", "6", "7"]]`.

A box of one step is as today: id `before:<n>`, label `Done: <n>. <words>`, detail its why or words, and its consequence.

A box of several steps:
- its id is `before:` and their numbers joined by `-`, `before:4-5-6-7`. Hyphens and colons are characters Pending You has taken in ids (`land:<bolt>`), and a step's number is digits, so the id names each step plainly;
- its label is `Done: steps 4, 5, 6 and 7`, cut at whole words to `LABEL`;
- its detail is each step's number and words, `4. <words>; 5. <words>; …`, cut at whole words to `DETAIL`, the face holding them whole;
- its consequence is "Ticked: you have done each of them, and each is recorded done with your word."

The summary's opening becomes: "It waits on 7 steps of yours before the deploy: tick each box once its steps are done, steps 4, 5, 6 and 7 sharing the fourth, and the deploy; your send with every box ticked is the word to deploy, and a box left unticked deploys nothing." With four or fewer it is as today. The face's *Before the deploy* list is unchanged: every step with its why or that it is done.

This is the reading of record 0038 this change takes: each step is ticked when the box that names it is ticked, so the word is never given with a step unticked. It departs from record 0059 Decision 2's "a box for each open step … five to a list" past four open steps (see *Departures*).

Other groupings, not taken:
- **Every step in one box once more than four are open.** Fewer steps would be ticked on their own. A card of five steps would tick none alone where it can tick three.
- **The open steps spread evenly over four boxes.** For eight steps every box would hold two, none alone. The first three alone keep the card of five, six or seven steps closest to the card of four, and the steps on the face are read in the same order.

### 3. The send names every step of each ticked box

Main-level ops runs `crew ops approve <env> --to <sha> --ticked <n>,...` naming each step number in every step box ticked: `before:4-5-6-7` gives 4, 5, 6 and 7. crew needs no new check for it (`roles.3`). `ticked_refusal` already refuses an approval naming each step neither ticked nor done, so a shared box passed as its first number alone is refused, naming the others, and nothing is recorded but the refusal. A case now pins it on seven steps.

`--ticked` keeps taking numbers (`ops.TICKED`), and `crew ops approve`'s usage, README's command line and the skill's row are unchanged (`docs.2`). Only the brief's sentence and README's description of the card say how a shared box is named.

Not taken: `--ticked` taking box ids, `before:4-5-6-7`, as they come off the card. That is a second spelling of one argument for ops to choose between, and the refusal already catches a box named short.

### 4. The card stays one list as steps are done, so it changes in place

`deploy_form` stays "boxes" while a step is open, however the steps are boxed. So a step recorded done while the card waits, which raises it again (record 0059 Decision 6), changes it in place through `update_request`. That call takes `options`, `multi`, `recommendedIds` and `rationale` (`cards.CHANGED`) for up to five boxes. Seven open steps with step 5 done become `before:1` to `before:3`, `before:4-6-7` and `deploy`. The card is followed only when it moves between the boxes and the approval, as today. `ops.raise_deploy` is unchanged.

### Rules relied on

- `plan.14`, `roles.2`: a `manual` environment's deploy is held to approve on its card, the word given only once each step it waits on is ticked there.
- `roles.3`: the shared box's send named short is refused by `ticked_refusal`, a check, not only the brief's words.
- `roles.5`: crew wraps Pending You, and its cards' forms are Pending You's, read from what it takes.
- `read.1`, `read.2`: crew posts no form it has never seen Pending You take, and reads Pending You by its refusals, not its guide's words.
- `code.7`: `deploy_boxes` and `deploy_card` are decisions on plain facts, tested in the logic tier.
- `code.8`: no bolt, unit, stage, card key or rail row changes shape. A card's boxes are the card's, so the views and the mod are untouched.
- `briefs.11`: crew raises the deploy's card in main-level ops's name. Ops runs the row's answer on the send.
- `tests.4`: the stub Pending You and `test_landings.marked_post` already refuse a card of questions carrying `highStakes`, as Pending You does. `tests.6`: the brief's changed sentence is pinned in `t-briefs`. `tests.11`, `tests.12`: the cases are in the logic tier.
- `docs.2`: no command's usage changes. `docs.3`: the open change that describes lists is rewritten in this commit. `docs.4`: the spec changes through this change's delta. `docs.7`: no rule page or record is edited by this change.

### Departures

- **Record 0059 Decision 2**, "a box for each open step, `before:<n>`, then one for the deploy, `deploy`, five to a list". Past four open steps the fourth box holds the rest, and there is no second list. Why: the lists are a form Pending You refuses, and record 0059 calls its choices the code stage's, cheap to change. The record is the design agent's to amend once this lands (`docs.7`). `plan.14`'s rule, from the user's record 0038, holds as written.

## Risks / Trade-offs

- **[A box that holds several steps is ticked once for all of them]** → Its label names each number, its detail each step's words, and the face lists each with its why. The user ticks it only once every step it names is done, as the consequence says.
- **[Ops names a shared box by its first number]** → `ticked_refusal` refuses it naming the steps left out. Nothing is recorded but the refusal, and the deployer's hold stands.
- **[An open deploy card asking lists of questions]** → None should stand: Pending You refuses that form, so any such card was recorded refused and is owed. The rail's sweep posts it again in the new form. If one had posted, its change in place would be refused by Pending You and recorded so, and its send still names the steps by number.
- **[Pending You mends its check]** → One list still posts. Asking every step a box of its own across lists again would be a change of crew's own, once Pending You has been seen to take questions carrying `highStakes`.

## Migration Plan

None. A deploy card refused in lists stays owed on its drive's rail. The rail's sweep posts it again as one list once crew at this change runs there, with nothing done by hand.

## After deploy

None: every outcome here is a logic-tier case or a pinned phrase, and nothing waits on a host or on the user.

## Task notes

**1.1** `cards.deploy_boxes(numbers)`, before `deploy_card`. `numbers` are the open steps' numbers, strings, in the card's order. It returns a list of lists of them (Decision 2), each step in exactly one, in order. Its docstring says why the fourth holds the rest: one list holds `BOXES` options, the deploy's among them, and Pending You refuses questions carrying `highStakes`. Cases in a new class `TestDeployBoxes` in `tests/py/test_cards.py`:
- `[]` gives `[]`;
- one to four numbers give one list each;
- five give `[["1"], ["2"], ["3"], ["4", "5"]]`;
- `["1", "3", "4", "6", "7", "9"]` gives `[["1"], ["3"], ["4"], ["6", "7", "9"]]`;
- twenty give three lists of one and one of seventeen, and never more than `BOXES - 1` lists.

**1.2** `cards.deploy_card`, while a step is open:
- The options are one per `deploy_boxes([w["n"] for w in left])`, then `deploy`. A box of one step is built as today. A box of several is built as Decision 2 says: id `before:` and the numbers joined by `-`, label `by_words(f"Done: steps {joined(ns)}", LABEL)`, detail `by_words("; ".join(f"{w['n']}. {' '.join(w['text'].split())}" …), DETAIL)`, and its consequence.
- The shape is always the one list: `kind="multi"`, `intent="decide"`, `options`, `multi={"min": 0, "max": len(options)}`, `recommendedIds=[]`, `rationale=then`, `highStakes=True`. The `else` branch of questions goes.
- The summary's opening says "tick each box once its steps are done, steps <ns> sharing the fourth, and the deploy" when a box holds several. Otherwise it is as today.
- The docstring says the card is one list and never questions, and why.

Cases in `tests/py/test_ops.py`, class `TestTheDeployCardOfAStepItWaitsOn`, replacing `test_more_boxes_than_a_list_holds_are_asked_as_lists_each_carrying_what_follows_a_yes`:
- `test_seven_steps_it_waits_on_are_one_list_of_five_boxes_the_fourth_holding_the_rest`: seven open steps. `kind` "multi", `highStakes` true, `rationale` set, no `questions` and no `about`. Options `before:1`, `before:2`, `before:3`, `before:4-5-6-7` and `deploy`. The fourth labelled "Done: steps 4, 5, 6 and 7", its detail starting "4. step 4; 5. step 5". The face's first artifact lists all seven. The summary says "steps 4, 5, 6 and 7 sharing the fourth". `form` "boxes".
- `test_four_steps_it_waits_on_have_a_box_each`: options `before:1` to `before:4` and `deploy`, the summary as today.
- `test_a_step_done_among_six_leaves_the_fourth_box_holding_the_last_two`: steps 1 to 6, step 2 done. Options `before:1`, `before:3`, `before:4`, `before:5-6`, `deploy`. The face's list has step 2 `done`.

`test_the_steps_it_waits_on_come_first_before_the_notes_a_box_each_and_one_for_the_deploy_none_ticked` still passes unchanged.

**1.3** A step recorded done while the card of a shared box waits changes it in place (Decision 4). Case in `tests/py/test_ops.py`, class `TestTheDeployCardOfAStepItWaitsOn`: `test_a_step_done_while_a_shared_box_waits_changes_the_card_in_place`. Use the `raised` fixture's stand-ins, with a steps file of seven steps marked `before` and the entries holding the offer, each step waiting, and step 5 done. Raised with a held card recorded `Form: boxes`, `plan.row_card_change` is called with `kind_changed` false and a card whose options are `before:1`, `before:2`, `before:3`, `before:4-6-7` and `deploy`. Extend the fixture's stand-in to record the options beside the kind, and keep `test_a_held_card_that_moves_between_the_hold_to_approve_and_boxes_is_followed_and_one_that_stays_is_changed` passing.

**1.4** Through a Pending You that refuses questions carrying `highStakes`. In `tests/py/test_card_commands.py`, beside `strict_post`, a fake `marked_post` refusing a post whose `questions` carry `highStakes` on the card or on any question in Pending You's words (the same words as `test_landings.MARKED_WORDS`), any other post taken. Case `test_a_deploy_waiting_on_seven_steps_posts_one_list_of_five_boxes_and_nothing_is_refused`: deploy facts for swancloud-srv's offer of `bbbbbbb`, seven open steps, posted through `plan.row_card_post(None, "swancloud", "swancloud-ops", cards.deploy_card, facts, WHERE, acts)`. The post is `kind` "multi" with `highStakes` true, no `questions` and five options. One `card.post` is emitted with no `refused`, its `Form` "boxes". Also assert `marked_post` refuses a card of two questions with `highStakes` on one of them.

**1.5** The send names each step of a shared box (Decision 3). Case in `tests/py/test_ops.py`, class `TestTheStepsADeployWaitsOn`: `test_a_shared_box_named_by_one_number_is_refused_naming_the_steps_it_leaves`. Seven steps the deploy waits on, each recorded waiting with a key. `ops.ticked_refusal(SRV, S2, waited, ["1", "2", "3", "4"])` names steps 5, 6 and 7, each with its words, and says the word is the card's send with every step ticked. `["1", …, "7"]` gives None. No code changes for it.

**2.1** `plugin/roles/main-ops.md`, *An offer*:
- "has them first on its card, a box each and one for the deploy" becomes "has them first on its card, one list of at most five boxes: a box each, every step past the third sharing the fourth when more than four are open, and one for the deploy".
- "you run the row's answer with `--ticked <n>,...` naming each step box they ticked by its number" becomes "you run the row's answer with `--ticked <n>,...` naming every step of each step box they ticked by its number, `before:4-5-6` naming 4, 5 and 6".

`tests/t-briefs.sh` pins "naming every step of each step box they ticked by its number" in place of the old phrase, and "every step past the third sharing the fourth" beside it (`tests.6`).

**2.2** `README.md`, the paragraph on `crew ops`: "each with why, a box for the user to tick once it is done and one for the deploy, the card then boxes held to send" becomes "each with why, a box for the user to tick once it is done, every step past the third sharing the fourth box when more than four are open, and one for the deploy, the card then one list of at most five boxes held to send". "`approve --ticked <n>,...` naming the steps ticked by their numbers on the card" stays.
