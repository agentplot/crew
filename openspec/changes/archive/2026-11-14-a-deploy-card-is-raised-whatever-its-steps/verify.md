# Verify: a-deploy-card-is-raised-whatever-its-steps

Verified on `change/a-deploy-card-is-raised-whatever-its-steps` at c51b9d6c, cut from `bolt/a-deploy-card-of-any-size-is-raised`, on 2026-11-14.

**Verdict: archived.** The whole checks pass, all 7 tasks are ticked, and every requirement and scenario of the delta spec is met in the code, each pinned by a test.

## The whole checks

`tests/suite --affected` was run once. CLAUDE.md asks for that run when a change is done and before it merges. It runs the `#check-full` tasks the change affects, against the merge-base with `main`, as sluice picks them. It selected 32 tasks.

**32 passed, 2 replayed, 0 failed.** `t-briefs` and `t-docs` were replayed from runs on this host with identical inputs. The other 30 ran: `contract`, `logic`, `t-cards`, `t-drive-set`, `t-flume-source`, `t-help`, `t-hold`, `t-journey-board`, `t-journey-cross`, `t-journey-land`, `t-journey-main`, `t-journey-main-fix`, `t-journey-ops`, `t-journey-plan`, `t-journey-review`, `t-journey-roles`, `t-journey-signals`, `t-journey-state`, `t-release`, `t-roles`, `t-runner`, `t-session-hook`, `t-slot`, `t-sluice`, `t-specs`, `t-stage-facts`, `t-suite`, `t-teams`, `t-waits` and `t-word`.

## Tasks

All 7 tasks of `tasks.md` are ticked. Each task names a check, and that check passed inside this run: `logic` holds every pytest case tasks 1.1 to 1.5 name, and `t-briefs` (2.1) and `t-docs` (2.2) passed.

## Specs

`openspec validate a-deploy-card-is-raised-whatever-its-steps --strict` says the change is valid.
- Each added requirement's text above its first scenario is at most 500 characters. The longest is 480: "Past four open steps a deploy's fourth box holds the rest".
- The REMOVED header, "A deploy's card of questions carries highStakes on each question", exists in `openspec/specs/rail-cards/spec.md`.
- The change edits nothing under `docs/` or `openspec/specs/` (`docs.4`, `docs.7`).
- The open change `an-offer-card-shows-the-step-the-deploy-waits-on-first` now says one list, not lists of five, in its proposal, design, spec and tasks (`docs.3`). It still validates. Its `main-level` delta's note that the archive would refuse a MODIFIED header was already there at this branch's base, so it is not this change's.

Each scenario of the delta spec was read against the code and its tests:

**A deploy's card waiting on steps is one list of at most five boxes.**
- **Seven steps, and Pending You refuses questions carrying highStakes.** `deploy_card` builds one shape while a step is open: `kind: multi`, `highStakes`, `rationale`, `recommendedIds` empty, the deploy's box last. The lists of questions are gone (`plugin/lib/cards.py`). `test_card_commands.py::test_a_deploy_waiting_on_seven_steps_posts_one_list_of_five_boxes_and_nothing_is_refused` posts it through `marked_post`, a fake that refuses questions carrying `highStakes` on the card or on any question. That test also checks that `marked_post` refuses both shapes. The post is one list of five, and one `card.post` is recorded with nothing refused and `Form: boxes`.
- **Four steps.** `test_four_steps_it_waits_on_have_a_box_each` gives `before:1` to `before:4` and `deploy`, and the summary is as it was.

**Past four open steps a deploy's fourth box holds the rest.**
- **`deploy_boxes`** is a decision on plain facts (`code.7`). Up to four open steps, each has a box of its own. Past four, the first three have one each and the fourth holds the rest, never more than `BOXES - 1` step boxes. `TestDeployBoxes` covers none, one to four, five, numbers with gaps, and twenty.
- **Seven steps share four boxes.** `test_seven_steps_it_waits_on_are_one_list_of_five_boxes_the_fourth_holding_the_rest` checks these:
  - the boxes are `before:1` to `before:3`, `before:4-5-6-7` and `deploy`;
  - the fourth is labelled "Done: steps 4, 5, 6 and 7", its detail is each step's words, and it has its own consequence;
  - the face lists all seven;
  - the summary says "steps 4, 5, 6 and 7 sharing the fourth";
  - the form is `boxes`.
- **A step done among six.** `test_a_step_done_among_six_leaves_the_fourth_box_holding_the_last_two` gives `before:1`, `before:3`, `before:4`, `before:5-6` and `deploy`, with step 2 listed `done` on the face.
- **A step recorded done while the card of a shared box waits.** `deploy_form` stays `boxes`, so `raise_deploy` changes the card in place. `test_a_step_done_while_a_shared_box_waits_changes_the_card_in_place` records step 5 done among seven against a held card with `Form: boxes`. It gets `kind_changed` false and the boxes `before:1` to `before:3`, `before:4-6-7` and `deploy`. The case where the card moves between forms and is followed still passes.
- **The send's shared box named as one step.** `ticked_refusal` is unchanged. `test_a_shared_box_named_by_one_number_is_refused_naming_the_steps_it_leaves` shows `--ticked 1,2,3,4` refused, naming steps 5, 6 and 7 with their words, and `1`–`7` refused nothing. No code of crew's reads a deploy box's id: `cards.BOX` reads only `land:` and `add:`, and no other `before:` id is read under `plugin/`.

**The words.**
- **main-level ops's brief** (`plugin/roles/main-ops.md`, *An offer*) says the card is one list of at most five boxes, with every step past the third sharing the fourth. It says the answer names every step of each ticked step box, `before:4-5-6` naming 4, 5 and 6. `t-briefs` pins both phrases (`tests.6`).
- **README** says the same of the card, and `crew ops approve`'s usage is unchanged (`docs.2`).
- **Views and the mod.** Nothing they draw changes shape (`code.8`). No bolt, unit, stage, card key or rail row changed, so `board.agent_views` and `status.js` are untouched.

## Left for others

Record 0059 Decision 2 still says "five to a list" (`docs/adr/0059-…`, line 22). The design names this as a departure for the design agent to amend once this lands (`docs.7`). This change edits no record, so that is not a shortfall here.
