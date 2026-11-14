# A deploy's card is raised whatever its steps

## Why

crew builds a deploy's offer card in a form Pending You refuses once the deploy waits on four or more of the user's open steps. Four step boxes and the deploy's box are more than one list holds (`BOXES`, five). So `cards.deploy_card` splits them into lists of questions, and each question carries `highStakes`. Pending You refuses any card of questions carrying `highStakes`, on the card or on a question. It refused boomdrive's landings card in that form on deneb from 2026-11-11T23:09Z, and crew's stub has refused it since `a-landings-card-is-raised-whatever-its-rows`. Such a deploy card is never posted, and the user has no card to give the word on (signal `afterthought/crew-state:agentplot/main signals/2026-11-12-agentplot-planner-39f6eca8/01-a-deploy-card-of-many-steps-is-refused`).

The landings card fixed this by giving five rows boxes and keeping the rest on its face for the card that follows the send. A deploy's steps cannot wait like that. The word is given only once each step the deploy waits on is ticked on its card (swancloud record 0038, `plan.14`), so every step must be ticked on the card that carries the deploy's box.

## What Changes

- **A deploy's card is always one list or the hold-to-approve, never questions.** While a step it waits on is open, the card is one list of at most five boxes carrying `highStakes` and what follows a yes on the card, the deploy's box last, whatever the number of steps. The lists of questions go.
- **Past four open steps, the fourth box holds the rest.** With four open steps or fewer, each has a box of its own, as today. With more, the first three open steps each have a box. The fourth box holds every other open step: its id is `before:` and their numbers joined by `-` (`before:4-5-6-7`), its label names their numbers, and its detail their words. Every step stays on the card's face with its why, as today. The summary says which steps share the fourth box.
- **The send names every step of each ticked box.** Main-level ops runs `crew ops approve --ticked` with each step number in every step box the user ticked, `before:4-5-6-7` giving 4, 5, 6 and 7. crew already refuses an approval naming each step neither ticked nor done (`ticked_refusal`), so a shared box passed as one number gives no word. A case now pins that.
- **A change of the shared box changes the card in place.** The card stays one list as steps are recorded done, so its boxes change through `update_request`, and the card is followed only when it moves to or from the hold-to-approve, as today.
- **main-level ops's brief and README say a step past the fourth shares the fourth box, and the send names each of its steps.**

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `rail-cards`: a deploy's card asks no questions. While a step it waits on is open it is one list of at most five boxes carrying `highStakes`, its fourth box holding every open step past the third when more than four are open. The requirement that a deploy's card of questions carries `highStakes` on each question goes.

## Impact

- `plugin/lib/cards.py`: a new decision, `deploy_boxes`; `deploy_card`'s options, summary and docstring.
- `plugin/roles/main-ops.md` and `tests/t-briefs.sh`: one sentence and its pinned phrase.
- `README.md`: the deploy card's boxes.
- `tests/py/test_cards.py`, `tests/py/test_ops.py`, `tests/py/test_card_commands.py`: the cases.
- `openspec/changes/an-offer-card-shows-the-step-the-deploy-waits-on-first`: its proposal, design, spec and tasks say one list, not lists of five (`docs.3`).
- No change to the stub Pending You, which already refuses a card of questions carrying `highStakes` (`tests.4`).
- No change to `crew ops approve`, its usage or `ticked_refusal`.
- No change to the views or crew's mod (`code.8`): no bolt, unit, stage, card key or rail row changes shape.
