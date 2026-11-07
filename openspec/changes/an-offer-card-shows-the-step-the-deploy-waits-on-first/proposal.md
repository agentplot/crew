# An offer card shows the step the deploy waits on first

## Why

swancloud record 0038, accepted by the user on 2026-10-26, lets a design list a step of the user's that a deploy waits on: one the user does before the deploy, where the change's truth rests on a fact of the world no configuration makes true. The deployer hands such a step to the offer card first, and the user's word for that deploy is given only once the step is ticked, so the card's yes with the step unticked is not the word. The record's consequences name a crew chore for crew's side.

swancloud's deployer already does its part (its archived change `a-step-the-deploy-waits-on-stands-on-the-offer-card`). It hands the step in the steps file with `before` in the when column, and records it on the deploy as a user's step waiting. crew showed the step among the after-deploy steps, took the user's hold of the card as the word with the step undone, and raised the step's own card beside the deploy's. The user met one step twice, and the card where they give the word asked nothing of it. The deployer's own hold kept anything from deploying early.

## What Changes

- **crew reads the mark the deployer hands.** A steps line with `before` among its when words is a step of the user's the deploy waits on. A line marking an agent's step so, or two such lines for one environment with one number, is refused with nothing offered.
- **The offer card asks it first.** The card's summary opens saying the deploy waits on the steps. Its face lists them first, before the notes, each with its why or that it is done, and the after-deploy list leaves them out.
- **The card is boxes while a step is open.** It carries highStakes with no box ticked: a box for each open step, `before:<n>`, then one for the deploy, `deploy`, five to a list. The send with every box ticked is the word, and a send with a box unticked is none. Once every step is done, the card is the hold-to-approve again.
- **`crew ops approve --ticked <n>,...` is the send.** It records each ticked step done on the step the deployer recorded, so the deployer's hold lifts, and then records the word. It is refused, recording only the refusal, while a step the deploy waits on is neither ticked nor done, naming each. It is also refused for a number no step has, and for a ticked step the deployer has not recorded yet.
- **The step has no card of its own.** A user's step recorded in the words of a step the open offer waits on is recorded with `before` among its when words. It has no rail row and no card while that offer is open, and the deploy's row says it waits on it.
- **A card that moves between forms is followed.** Each post and change of the deploy's card records its form (`Form: boxes`). A card that moves between the boxes and the hold-to-approve is followed rather than changed in place, since Pending You changes no card's kind. A waited-on step recorded done while the card is open raises the card again.
- **Main-level ops's brief says what to run on the send.** It runs the approval with the boxes ticked, and closes a card sent with a box unticked as a declined one.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `rail-cards`: a deploy's card is boxes while a step the deploy waits on is open. Such a step is first on its offer's card, and has no card of its own while its offer is open.
- `main-level`: `crew ops approve` takes the steps ticked on the card, and is refused while a step the deploy waits on is open. `crew ops step` records a user's step in such a step's words as one.

## Impact

- `plugin/lib/ops.py`: `handed_steps`, `waited_on`, `marked_before`, `own_card`, `ticked_refusal`, `offered_steps`, `approve`, `step`, `step_closed`, `raise_deploy`, `rows`, `step_due`, `step_point`, `environments`, and the parser's `--ticked`.
- `plugin/lib/cards.py`: `deploy_card`, `deploy_form` and `form_asked`. `plugin/lib/plan.py`: `built_fields` records a card's `Form`. `plugin/lib/record.py`: the descriptor's comment.
- `plugin/roles/main-ops.md`, README, `plugin/skills/crew/SKILL.md` and `plugin/bin/crew`'s usage (`docs.2`).
- `tests/py/test_ops.py`, `tests/t-journey-ops.sh`, `tests/t-briefs.sh` and `tests/t-docs.sh`.
- Record 0059; `plan.14` amended.
- No change to the views or crew's mod (`code.8`): no rail row, card key or stage changes shape. A carried step's row is absent, as a done step's is.
- No swancloud change. Its deployer already hands the mark and records the step. Its hold reads the keys crew now marks done.
