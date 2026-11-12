# Verify: a-landings-card-is-raised-whatever-its-rows

Verified 2026-11-11 on `change/a-landings-card-is-raised-whatever-its-rows` at `cdb48da2`, cut from `bolt/crews-landings-reach-the-user`, whose base is main at `3b094ab9`.

**Outcome: the whole checks pass and the work holds.** Every task is ticked, and every requirement and scenario of the delta spec is met in the code and proven by a case in the suite.

## The whole checks

The checks run once, as CLAUDE.md names them for a finished change, from the place's root: `tests/suite --affected`, against the merge-base with main, nothing uncommitted.

```
32 passed (3 replayed), 0 failed
exit=0
```

These ran: `logic`, `contract`, and every end-to-end test the change affects: t-briefs, t-cards and t-docs, replayed from an identical tree that passed on this host; t-drive-set, t-flume-source, t-help, t-hold, t-journey-board, t-journey-cross, t-journey-land, t-journey-main, t-journey-main-fix, t-journey-ops, t-journey-plan, t-journey-review, t-journey-roles, t-journey-signals, t-journey-state, t-release, t-roles, t-runner, t-session-hook, t-slot, t-sluice, t-specs, t-stage-facts, t-suite, t-teams, t-waits and t-word. `mod` and the `nix` project's tasks were not affected: neither `plugin/hooks/status.js` nor the flake changed.

`openspec validate a-landings-card-is-raised-whatever-its-rows --strict`: valid.

## Tasks

All 11 tasks of `tasks.md` are ticked, 1.1 to 4.2. Each case a task names is in the suite, and `logic`, which runs them all, passed: `TestLandings::test_the_form_by_how_many_rows_can_land`, `TestLandingsBoxed`, the three new `TestLandings` cases in `tests/py/test_cards.py`, and the eight new cases in `tests/py/test_landings.py`. The end-to-end checks named by 3.2, 4.1 and 4.2 (t-cards, t-journey-land, t-briefs and t-docs) passed above.

## Requirements and scenarios

**MODIFIED: A row that can land is a box, ticked as crew proposes.** `cards.landings_card` builds one list of at most `BOXES` options, labelled `<n>. <bolt>` by place among all rows, ticked but for left and taking rows.
- *Three bolts*: the existing list cases in `TestLandings`.
- *Seven bolts*: `landings_boxed` and `landings_card` give boxes to the first five of more than five rows that can land, the rest on the face marked `WAITS`. The cases prove this with eight rows (`test_eight_rows_are_one_list_of_five_boxes_the_rest_waiting_on_its_face`, `TestLandingsBoxed::test_eight_rows_that_can_land_box_the_first_five`), and with six and twenty-one for the card's shape. Seven rows take the same path.

**REMOVED: A landings card of two or more rows is a list carrying highStakes**, and **A card of questions carries highStakes on each question.** Both requirement headers are in `openspec/specs/rail-cards/spec.md`, so the archive removes them. The lists branch is gone from `landings_card`, and `landings_form` gives only "approve" or "multi".

**ADDED: A landings card of two or more rows is one list carrying highStakes on the card.**
- *A list of three bolts* and *One that can land beside one taking main first*: the existing cases, unchanged and passing.
- *Eight bolts, one list marked*: `test_more_than_five_rows_carry_high_stakes_and_what_follows_on_the_card_and_ask_no_questions[8]`. `highStakes` and `rationale` are on the card, there are no `questions`, and it has five options.

**ADDED: A deploy's card of questions carries highStakes on each question.**
- *A deploy waiting on five steps*: `tests/py/test_ops.py::test_more_boxes_than_a_list_holds_are_asked_as_lists_each_carrying_what_follows_a_yes`. It has two questions, each with `highStakes`, and the card has none. `cards.deploy_card` is unchanged. The design's Risks note that the stub now refuses this shape too, which is that card's own change for the planner.

**ADDED: A landings card holds five boxes and the rest of its rows wait on its face.**
- *Eight bolts, and Pending You refuses questions carrying highStakes*: `test_eight_proven_bolts_post_one_list_of_five_boxes_and_nothing_is_refused`. It runs on `marked_post`, which refuses `highStakes` on the card or on any question. One `card.post` is emitted with nothing refused, its `Heads` ending `b6@abc1234:next b7@abc1234:next b8@abc1234:next`. The stub `tests/stubs/pendingyou` refuses the same, and t-cards and t-journey-land pass through it.
- *A left row and one taking main first among seven*: `TestLandingsBoxed::test_seven_rows_the_first_left_and_the_second_taking_main_first_box_the_third_to_the_seventh` gives `b3` to `b7`. `test_rows_with_no_box_are_marked_next_in_the_cards_heads` proves the face marks and `:left:next` and `:main:next` in `heads`. The labels by place, which no case asserts where the first box is not row 1, were read by building the card at this commit. Its options are `3. b3` to `7. b7`, all recommended, and its heads `b1@abc1234:left:next b2@abc1234:main:next b3@abc1234 … b7@abc1234`.
- *Twenty-one bolts*: the same parametrised case at 21. It has five options, its summary is within `SUMMARY`, and the summary says 16 more wait below.

**ADDED: A row coming to a box or losing one changes the waiting landings card in place.**
- *A boxed row is held for a fix*: `test_a_row_coming_to_a_box_changes_the_waiting_card_in_place`. The step is `("change", "b2 is held for a fix: …; b6 has a box now", False, [])`, so the card is changed in place and not followed. It also covers the way back ("b6 waits for a box").
- *A row waiting for a box moves its head*: `test_a_row_with_no_box_whose_head_moves_changes_the_card_and_keeps_it_with_no_box`. The step is `("change", "b7's head is now def5678", False, [])`. Nothing moved leaves the card.

**ADDED: A send with rows waiting for a box is followed at once by a card asking for them.**
- *Five ticked, three waiting*: `test_a_send_with_rows_waiting_for_a_box_is_followed_at_once_by_a_card_asking_for_them` covers the step's `("follow", …)`, with no "Left:". `test_a_send_with_rows_waiting_for_a_box_posts_the_card_that_follows_asking_for_them` covers the raise. The close says b6, b7 and b8 had no box. No `landing.left` is emitted. The card that follows is posted with `land:b6` to `land:b8` all recommended and `Heads` `b6@abc1234 b7@abc1234 b8@abc1234`. Its summary was read by running that raise at this commit. It opens with the close's outcome, "Since then: asked of the runner as you ticked: b1, b2, b3, b4 and b5. b6, b7 and b8 had no box on this card, and the card that follows asks for them.", as every followed card quotes its close. `test_the_card_that_follows_says_the_rows_that_had_no_box_wait_on_it` covers a card raised after a refused follow-on, which says "b6, b7 and b8, which had no box on your last card, wait on this card" and never "which you left".
- *A left row that waited for a box*: `test_a_left_row_waiting_for_a_box_stays_left`. `left_now` reads `b1@…:left:next`, unticked on an answered card, as left, and a row marked `:next` alone as not left. `landings_raised` shows every bolt in `left` unticked on the card that follows (`unticked`).

## Rules

- `code.7`: `landings_boxed`, `landings_step`, `left_now`, `landings_since` and the heads readers are decisions on plain facts, with logic-tier cases.
- `code.8`: no bolt, unit, stage, card key or rail row changes shape. `plugin/lib/board.py` and `plugin/hooks/status.js` read no `Heads`, so the `:next` mark reaches no view.
- `tests.4`: the stub and the logic tier's fake refuse what Pending You refused, in its words and with its apostrophe.
- `tests.6`: main-level ops's new sentence is pinned in t-briefs.
- `docs.7`: no page under `docs/architecture/` or `docs/adr/` is edited.

## Notes

- The followed card quotes its close's outcome, whose words say the rows "had no box on this card", meaning the card the user sent. This is the form `landings_step`'s close has always given a followed card ("…, and the card that follows asks for them"), and design Decision 5 sets it so. It meets the scenario's "its summary saying they had no box on the last card".
- No seven-row card case stands beside the eight-row ones. The decision has no branch between six and twenty-one rows, so this is no shortfall.
