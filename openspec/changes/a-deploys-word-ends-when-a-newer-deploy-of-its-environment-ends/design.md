# Design

Rules relied on: `plan.14` (a word is for one head, spent at that deploy's end or once the environment has deployed a later head, its card closing naming the deploy that spent it), `read.1` (what crew can't read removes nothing), `state.4` (every view is computed from the record), `code.7` (a decision is a function of plain facts), `code.8` (the views and the mod follow what crew models). Pages touched: `plan.md` (`plugin/lib/ops.py` is read with the plan's rules) and `docs.md` for the spec. It departs from no rule.

## Decision 1: a newer deploy is one started after the word was given

The run record cannot say one commit is later than another without git, and `code.7` keeps git out of a decision. It can say one deploy is newer than a word: the deployer records each deploy's start, and the record is read oldest first. So `ops.spends(word, to, started)` is true for the end of a deploy of the word's own head, or of a head in `started`, the heads whose deploys started since the word was given. `state` resets `started` at each word and adds to it at each start.

Path not taken: ending a word at any deploy's end of its environment. A deploy that was running when the user gave the word is older than it. Its end would spend a word the deployer has not yet acted on.

A deploy end with no start in the record is not counted newer. crew cannot tell when it began, so the word stands (`read.1`).

## Decision 2: a newer deploy that failed spends the word too

A word's own deploy spends it at its end whatever the outcome, and the deployer offers again after a failure (mac-studio's 3b12e8f, failed at 01:16 on 2026-10-26 and offered again at 01:16:21). A newer deploy is treated the same way.

Path not taken: keeping the word through a newer deploy that failed. The deployer would then deploy the older head the word names, behind the head it just tried, which `deploy.7` rules out.

## Decision 3: the close names the newer deploy and the approved head

`deploy_outcome` takes the word's head. When that differs from the deploy that ended, the close says the deploy is newer than the head the user approved. It is said inline, before the steps, so a long log path, which comes last, is all that the 200-character cut (`cards.OUTCOME`) can drop.

## Decision 4: the deploys view mirrors the word

`environments` already marks an approved deploy that never started `replaced` when the word goes to another commit, "as state reads the word". It now does the same when a newer deploy's end spends the word, using the same `spends`, and adds `spent`, that deploy's commit, `None` otherwise. Without this, the board would keep the deploy approved and not yet deployed. With `replaced` alone, the board would say the word went to a newer offer, which is untrue. `board.deploy_state`, `page.word_said` and `page.html` name the deploy when `spent` is set. Main-level ops's view already leaves out a replaced deploy. `status.js` draws no deploy, so the mod is unchanged (`code.8`).

## After deploy

None. Every change here is crew's own reading of its run record, proved by the logic tier. The two cards of the reading are in swancloud-ops's name, a role that has left the fleet, and `a-card-whose-role-left-the-fleet-is-withdrawn` takes them down.

## Task notes

**1.1** `ops.spends` and `ops.state`. Cases in `tests/py/test_ops.py` `TestState`: a word ended by a newer deploy's end, ok or failed; a word standing through the end of a deploy running when it was given, of one with no start, and of another environment's; `word_stands` after a newer deploy's end.

**1.2** `ops.environments`: `spent` on every deploy, and `replaced` with `spent` for the approved deploy not started whose word a newer deploy's end spent. The case in `TestEnvironments` holds the invariant that, at every point, the approved deploy not ended is the word `state` reads, for a newer deploy and for one running when the word was given.

**1.3** `ops.deploy_outcome(…, word)` and `ops.record_cmd`: the card closes when the end spends the word (the word stood before the end and not after), naming the newer deploy. Cases in `TestDeployCard`: the close's words, and `record_cmd` with `emit`, `entries`, `plan.row_card_close` and `raise_deploy` replaced, closing for a newer deploy and not for one running when the word was given.

**1.4** `board.deploy_state`, `page.word_said`, `page.html`'s `word`. Cases: `tests/py/test_board.py` (main-level ops's view and the Operation lane), `tests/py/test_page.py` `TestDeploys`, and `tests/py/test_rail.py` (the sweep no longer leaves the card).
