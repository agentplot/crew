# Verify: a-wait-on-the-user-is-one-open-card-the-rail-agrees-with

Read on 2026-11-07 against `change/a-wait-on-the-user-is-one-open-card-the-rail-agrees-with` at 264daa6e. The branch was cut from `bolt/each-wait-on-the-user-is-one-open-card`, which stood at `origin/main`, 7a7b8acd.

## Outcome

**The change holds and is archived.** The whole checks pass. Every requirement and scenario of its three specs is met in the code and pinned by a case. All 17 tasks are ticked. `openspec validate --strict` passes.

## The whole checks

`tests/suite --affected` ran once, as CLAUDE.md names it for a change that is done. The change edits crew's command core, so every check-full task was affected and selected.

```
29 passed (29 replayed), 0 failed
exit 0
```

These tasks passed: `contract`, `logic`, `mod`, `t-briefs`, `t-cards`, `t-docs`, `t-flume-source`, `t-help`, `t-hold`, `t-journey-board`, `t-journey-cross`, `t-journey-land`, `t-journey-main`, `t-journey-main-fix`, `t-journey-ops`, `t-journey-plan`, `t-journey-review`, `t-journey-roles`, `t-journey-signals`, `t-journey-state`, `t-roles`, `t-runner`, `t-session-hook`, `t-slot`, `t-sluice`, `t-stage-facts`, `t-suite`, `t-teams` and `t-waits`.

Every task was replayed. `tests/suite` replays a task only when its inputs match a run that passed on this host (`tests.10`), so each one passed on the tree as it stands. Sluice runs them all afresh when the change is submitted (`tests.5`).

`t-journey-ops` expects the rail's sweep to call `list_pending` once in swancloud-ops's name, beside an approved deploy card. That is the read design Decision 2 and task 1.3 call for. Task 4.4 added the expectation, and the test passes.

`openspec validate a-wait-on-the-user-is-one-open-card-the-rail-agrees-with --strict`: valid.

## Tasks

All 17 tasks in `tasks.md`, 1.1 to 6.1, are ticked, and none is left open. Each task's own check is one of the suite's tasks above or a logic-tier file the `logic` task runs.

## Requirements and scenarios

Each scenario is met in `plugin/lib/` and pinned by the case named. Every case named is present in `tests/py/` or `plugin/tests/`. The scenarios a modified requirement carries unchanged are pinned by its existing cases, which pass in `logic`.

### rail-cards

| Requirement | Scenarios | Where it is pinned |
|---|---|---|
| A crew agent's card acts are in the run record (modified) | "A card the user answered" | `test_landings.py` `test_a_raise_reading_its_card_answered_records_the_answer_once_with_the_bolts_ticked`; `record.py`'s docstring names `card.answer` |
| The rail shows each row's card (modified) | "Two cards open under one row's key"; "A row's card the user answered" | `test_rail.py` `test_a_row_names_its_owners_card_and_each_other_card_open_under_its_key_apart`, `test_a_landings_card_the_user_sent_says_when_what_and_that_it_waits_on_ops_to_land_them` |
| The rail names an open card whose row is gone (modified) | "A card whose close was refused" | `test_a_stray_card_whose_close_was_refused_is_listed_with_the_refusals_words` |
| crew records the user's answer the first time it reads it | all four | `test_a_held_proposal_card_on_the_agents_turn_has_its_answer_recorded_once`, `test_a_card_already_recorded_answered_is_read_no_more_and_one_waiting_on_the_user_is_not_read`, `test_an_answered_question_and_record_card_have_their_answers_recorded_on_their_askers_and_records`, `test_an_answered_landings_card_records_the_bolts_ticked_at_the_heads_it_showed`; `test_card_commands.py` for `crew card read`; `t-cards` on the stub pendingyou |
| A card the user answered is closed, never withdrawn | both | `test_cards.py` `test_a_card_the_user_answered_is_closed_with_the_reason_as_its_outcome_and_never_withdrawn` (`cards.close_call`) |
| A kit's landings card's close keeps the user's send | all three | `test_landings.py` `test_an_answered_landings_card_the_sweep_closes_keeps_the_send_and_the_next_raise_has_no_row_for_it`, `test_a_send_ops_acked_in_pending_you_read_resolved_at_a_raise_is_recorded_closed_with_its_answer_and_send` |
| The sweep leaves an answered landings card while a bolt it ticked waits to land | both | `test_rail.py` `test_an_answered_landings_card_whose_row_is_gone_is_left_while_a_bolt_it_ticked_waits_to_land`, `test_an_answered_landings_card_whose_ticked_bolt_landed_is_gone_and_closed_as_answered`, `test_an_answered_landings_card_whose_row_is_gone_is_left_said_as_waiting_on_ops_and_nothing_withdrawn` |
| A card Pending You has ended is recorded on the read that finds it | both | `test_a_card_the_user_dismissed_is_recorded_withdrawn_and_its_row_is_a_row_with_none_at_the_next_read`, `test_a_question_its_asker_acked_is_recorded_closed_and_listed_nowhere`, `test_an_ended_landings_card_keeps_its_answer_and_send` |
| A card Pending You holds in another assistant's name is lost to its owner | both | `test_cards.py` `test_a_card_held_in_another_assistants_name_is_lost_to_its_recorded_owner_alone`; `test_rail.py` `test_a_gone_batch_card_held_in_another_name_is_recorded_lost_and_no_longer_a_stray`, `test_a_held_rows_card_in_another_name_is_posted_again_in_its_owners_name_saying_the_older_copy_is_dead` |

### crew-rail

| Requirement | Scenarios | Where it is pinned |
|---|---|---|
| A row whose card the user answered says whose act it waits on | landings, proposal, batch, deploy, not yet answered | `test_a_landings_card_the_user_sent_…`, `test_a_proposals_card_answered_waits_on_the_planner`, `test_a_batch_a_deploy_and_a_steps_card_answered_each_say_whose_act_they_wait_on`; an unanswered card keeps the existing `open, asked by` cases; `t-journey-ops` for the deploy card's sweep |
| An answered question or record card no longer waits on the user | both | `test_an_answered_question_and_record_card_wait_on_their_askers_and_not_on_the_user` |
| Each bolt's land line says whether its card carries, holds or follows it | all seven | `test_a_bolts_card_stand` (parametrized), `test_each_bolt_line_ends_with_how_its_kits_card_stands_for_it`, `test_a_bolt_that_cant_land_and_is_no_row_of_the_card_says_nothing_of_it` |

### crew-board

| Requirement | Scenarios | Where it is pinned |
|---|---|---|
| Each holder is read from what crew already keeps (modified) | "The user answered the landings card"; "A landings card that no longer carries the bolt"; "A main-level question about something else" | `test_bolt_time.py` `test_the_user_answered_the_landings_card`, `test_a_landings_card_that_no_longer_carries_the_bolt`, `test_a_main_level_question_about_something_else_is_no_card_of_the_bolts`, `test_a_cards_span_ends_at_the_users_answer_or_its_close_whichever_is_first` |
| An agent's band says which of its cards the user answered | all three | `test_board.py` `test_the_planners_answered_proposal_card_says_it_was_answered_and_is_the_planners_to_act_on`, `test_ops_answered_landings_card_says_the_landing_is_ops_own`; `plugin/tests/status.test.ts` "an answered card's line is drawn above ops's view as the views give it" (`code.8`) |

The command's words, `docs.2`: README's *Operations*, `plugin/skills/crew/SKILL.md` and `plugin/bin/crew`'s usage header were changed, and `t-docs` passed.
