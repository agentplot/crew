# Tasks

Each check is a moon task of the `tests` project, run through `tests/suite`: `logic` is `tests:logic`. Build the groups in order. Submit nothing, and never run `wt submit --help`.

## 1. The step the deploy waits on, decided on facts

- [x] 1.1 A steps line with `before` among its when words is a step of the user's the deploy waits on, with its why; one for an agent, or two for one environment with one number, is refused with nothing offered (design Decision 1; Task notes 1.1). Passes `tests/py/test_ops.py` (`tests/suite logic`).
- [x] 1.2 The steps the open offer waits on are found with the user's step the record holds in the same words, its key, head and latest state, or none while unrecorded, and a user's step recorded in those words is marked as one (design Decisions 2 and 3; Task notes 1.2). Passes `tests/py/test_ops.py` (`tests/suite logic`).
- [x] 1.3 A marked step waiting has no row and no card of its own while its environment's offer is open, the deploy's row says it waits on it, and it has its row again once no offer is open (design Decision 3; Task notes 1.3). Passes `tests/py/test_ops.py` (`tests/suite logic`).
- [x] 1.4 `crew ops approve` is refused naming each step the deploy waits on that is neither ticked nor done, a number no step has, or a ticked step not yet recorded, and otherwise records each ticked step done under the deployer's key before the word (design Decision 5; Task notes 1.4). Passes `tests/py/test_ops.py` (`tests/suite logic`).
- [x] 1.5 The deploy's card says first that it waits on the steps, lists them first on its face before the notes, and is boxes carrying highStakes, a box for each open step and one for the deploy, none ticked, in one list of at most five, until every step is done, when it is the hold-to-approve (design Decision 4; Task notes 1.5). Passes `tests/py/test_ops.py` (`tests/suite logic`).
- [x] 1.6 Each post and change of a deploy's card records its form, a card whose form moves is followed rather than changed, and a carried step recorded done while the card is open raises it again (design Decision 6; Task notes 1.6). Passes `tests/py/test_ops.py` (`tests/suite logic`).

## 2. Through the command and the brief

- [x] 2.1 Through `crew ops` on the stubs, an offer with a step the deploy waits on posts the boxes, the deployer's record of the step is marked and posts no card, an approval with it open is refused naming it, and one with it ticked records it done and gives the word (Task notes 2.1). Verify `tests/suite t-journey-ops` ends with "0 failed".
- [x] 2.2 Main-level ops's brief says to run the approval with the boxes ticked and to close a card sent with a box unticked as declined, and the README, the skill and the usage give `--ticked` (design Decision 7; Task notes 2.2). Verify `tests/suite t-briefs t-docs` ends with "0 failed".

## 3. The tests the change affects

- [x] 3.1 Verify `tests/suite --affected` ends with "0 failed".
