# Verify: a-bolt-proven-after-a-send-is-offered-at-once

Verified 2026-11-12 on `fix/main--a-bolt-proven-after-a-send-is-offered-at-once` at `856db339`, cut from main at `461c2f6e`.

**Outcome: the checks pass and the work holds.** Every task is ticked, and every requirement and scenario of the delta spec is met in the code and proven by a case in the suite.

## The checks

`tests/suite --affected`, against the merge-base with main, nothing uncommitted, from the place's root:

```
32 passed (0 replayed), 0 failed
exit 0
```

These ran: `logic`, `contract`, and every end-to-end test, since `plugin/lib/plan.py` is crew's command core: t-briefs, t-cards, t-docs, t-drive-set, t-flume-source, t-help, t-hold, t-journey-board, t-journey-cross, t-journey-land, t-journey-main, t-journey-main-fix, t-journey-ops, t-journey-plan, t-journey-review, t-journey-roles, t-journey-signals, t-journey-state, t-release, t-roles, t-runner, t-session-hook, t-slot, t-sluice, t-specs, t-stage-facts, t-suite, t-teams, t-waits and t-word. `mod` and the `nix` project's tasks were not affected.

`openspec validate a-bolt-proven-after-a-send-is-offered-at-once --strict`: valid.

The reproducing case fails on main's `plan.py`: `test_a_bolt_proven_between_a_send_and_its_landing_gets_its_card_in_the_same_sweep` reads `{'raised': [], 'unread': []}` there, the sweep raising nothing (`tests.4`).

## Requirements and scenarios

**ADDED: The rail's read raises a landings card that does not show a row as it stands.** `plan.unoffered` decides the rows. `plan.landings_unoffered` applies it to each card open on the host in ops's name, and `plan.sweep_moved` raises each such card once.
- *A bolt proven between a send and its landing*: `tests/py/test_landings.py::test_a_bolt_proven_between_a_send_and_its_landing_gets_its_card_in_the_same_sweep`, through `sweep_moved` and `raise_landings`. `req_k1` is closed with `Heads` `y@abc1234`, a card following it asks for `z`, and the next read raises none.
- *A bolt proven while the card waits*: `test_a_bolt_proven_while_the_card_waits_raises_it_in_the_same_sweep`.
- *A ticked bolt proven at a new head*: `test_a_row_the_open_card_does_not_offer_as_it_stands_is_unoffered` gives `y` ticked at `abc1234` and read at `def5678` as unoffered. That raise posts its land on the send, as `test_a_row_taking_main_first_posts_nothing_then_once_at_its_new_head` proves.
- *A bolt the user left beside a send still landing*: `test_a_bolt_the_user_left_beside_a_send_still_landing_raises_no_card`.
- *The rail names the card it raised*: `tests/py/test_rail.py` `TestMainMoved.test_a_card_raised_for_a_row_it_did_not_offer_is_said_naming_the_row`.

**ADDED: A bolt proven while an answered landings card waits on its landings is offered at once.**
- *Proven since the send*: the existing `test_a_bolt_proven_after_the_answer_gets_a_new_card_following_it_and_the_send_still_lands_the_rest`. The close says "Asked of the runner as you ticked: y. Since your send, z reads proven, and the card that follows asks for it." with `Heads` `y@abc1234`, the card following it asks for `z`, and the next raise prints that `y` lands on the earlier send and is no row.

**MODIFIED: An answered landings card closes once each bolt it ticked has landed, been held or stopped.** The four scenarios stand unchanged, proven by the `landings_step` cases they were proven by. The added sentence, a row proven meanwhile closing it sooner with its send kept, is the case above.

## Tasks

All 6 tasks of `tasks.md` are ticked. `logic` ran every case they name. `t-docs`, named by 2.1, passed above.
