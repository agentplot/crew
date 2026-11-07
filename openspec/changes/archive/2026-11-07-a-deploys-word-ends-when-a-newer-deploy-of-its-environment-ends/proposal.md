# A deploy's word ends when a newer deploy of its environment ends

## Why

On 2026-10-31 swancloud-ops read three deploy words still standing after their environments had moved on. macbook-pro and mac-studio held the word for 3b12e8f, given on 2026-10-26 at 01:26 and 01:28. The deployer then started 8651be6 on both at 03:06 and ended it, and deployed 2f4f22c and e9cf42e since. chuck-herdr-alpha held 651063d after it deployed e9cf42e. Each `deploy/<env>` card stayed open as the agent's turn ("card deploy/macbook-pro: req_8da3aed726264821bcfd, answered, your turn: the user has answered"), and the board kept 3b12e8f approved, not yet deployed (signal `afterthought/crew-state:swancloud/main signals/2026-10-31-swancloud-ops-edced2f9/01`).

The cause is `plugin/lib/ops.py` `state`: it ended a word only at the end of a deploy of the word's own head. `plan.14` has the word spent at that deploy's end or once the environment has deployed a later head, since nothing behind what an environment runs is offered again (swancloud `deploy.7`).

## What Changes

- **A word ends at the end of its own deploy or a newer one.** A newer deploy is one of the same environment whose start is recorded after the word was given. A deploy already running when the word was given, or one whose start the record lacks, leaves the word standing (`read.1`). It ends at the newer deploy's end whatever its outcome, as a word's own deploy does.
- **The end that spends the word closes its card.** `crew ops record --act end` closes `deploy/<env>` whenever that end spends the word. When the deploy is a newer one, the close names it and the commit the user approved: "Deployed e9cf42e to mac-studio, newer than the 3b12e8f you approved: machine ok, suite ok."
- **The rail's sweep no longer leaves the card.** `ops.word_stands` reads the word as `state` does.
- **The deploys view follows the word.** `ops.environments` marks an approved deploy that never started `replaced` once a newer deploy's end spends its word. Its new field `spent` names that deploy's commit. The board says "approved, then the deploy of 8651be6 ended first", and the page's deploys view says the same. The deploy leaves main-level ops's view.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `main-level`: `crew ops word` gives the commit until that deploy's end or a newer deploy's end is recorded, and that end closes the card, naming the newer deploy.

## Impact

- `plugin/lib/ops.py`: `spends`, `state`, `environments`, `deploy_outcome`, `record_cmd`, and the usage header.
- `plugin/lib/board.py` `deploy_state`, `plugin/lib/page.py` `word_said`, `plugin/lib/page.html`: the words for a deploy whose word a newer deploy spent.
- `tests/py/test_ops.py`, `test_board.py`, `test_rail.py`, `test_page.py`: the cases.
- No change to crew's mod (`code.8`): `status.js` draws no deploy, and main-level ops's view counts the deploys it already counted.
- The two cards of the reading are in swancloud-ops's name, a role that has left the fleet. `a-card-whose-role-left-the-fleet-is-withdrawn` takes them down, not this change.
