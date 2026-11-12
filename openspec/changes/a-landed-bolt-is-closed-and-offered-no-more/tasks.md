# Tasks

Each pytest check runs from the worktree's root as written: `devenv shell -- sh -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider <case>'`, written below as `pytest <case>`. It passes when it ends with "passed" and no "failed". Submit nothing: Flume submits the place once its last stage delivers.

## 1. The reading

- [x] 1.1 `plan.landing_head` gives the newest head a landing of the bolt carried since its newest start, with the submission or request of the landing still pending (design, Decision 1; Task notes 1.1). Verify `pytest tests/py/test_landed_on_main.py::TestLandingHead`.
- [x] 1.2 `plan.main_asks` and `plan.on_main` say whether a bolt's work is on its kit's main, every piece's landing commit and its newest landing head held, asking git nothing while a piece has not merged (design, Decision 1; Task notes 1.2). Verify `pytest tests/py/test_landed_on_main.py::TestOnMain`.
- [x] 1.3 `plan.main_holds` answers whether GitHub's main in crew's cache holds each commit, a commit the cache lacks reading not held, and `plan.landed_by` gives the oldest commit of main's first-parent line that holds them (design, Decisions 2 and 4; Task notes 1.3). Verify `pytest tests/contract/test_git.py::TestMainHolds`.
- [x] 1.4 `plan.main_tip` gives the kit's main fetched once per command, and in the follower's read only the tip the follower handed in, never fetching (design, Decisions 2 and 7; Task notes 1.4). Verify `pytest tests/py/test_landed_on_main.py::TestMainTip`.

## 2. Reading it

- [x] 2.1 `Stages.landing` reads a started bolt landed at main's commit where the runner's report does not and its kit's main holds its work, one with no launch of its own among them, reading no host and no kit, and `Stages.base` gives it no legacy words (design, Decision 3; Task notes 2.1). Verify `pytest tests/py/test_stages.py::TestABoltWhoseWorkIsOnMain`.

## 3. Recording and closing it

- [x] 3.1 `landing_entry` records a landing read on main once, as landed, naming its head and ending an older crew's queued landing and any stop (design, Decision 5; Task notes 3.1). Verify `pytest tests/py/test_landing.py::TestALandingReadOnMainIsRecorded`.
- [ ] 3.2 `landing_read` records and closes a bolt read landed on main, one with no launch of its own among them, asking ops nothing (design, Decision 5; Task notes 3.2). Verify `pytest tests/py/test_landing.py::TestALandingReadOnMainCloses`.
- [ ] 3.3 `crew bolt land` closes a started bolt read landed on main at main's commit, one with no launch of its own among them, and refuses one main does not hold, naming why, recording nothing (design, Decision 5; Task notes 3.3). Verify `pytest tests/py/test_landing.py::TestCrewBoltLandOfAStartedBolt`.
- [ ] 3.4 The sweep reads a bolt read landed on main with no land posted, under its host or, where crew can't tell it, the drive's main-level host (design, Decision 5; Task notes 3.4). Verify `pytest tests/py/test_landings.py::TestTheSweepClosesABoltOnMain`.

## 4. Offering it no more

- [ ] 4.1 A bolt whose landing reads landed is no row of its kit's landings card, so no land of it is posted on any send and no stop of it is said (design, Decision 6; Task notes 4.1). Verify `pytest tests/py/test_landings.py::TestABoltOnMainIsNoRow`.
- [ ] 4.2 A bolt whose landing reads landed has no line under *land* on the rail (design, Decision 6; Task notes 4.2). Verify `pytest tests/py/test_rail.py::TestABoltOnMainHasNoLandLine`.

## 5. The follower

- [ ] 5.1 The follower's clock fetch carries the main of each repository with a started bolt, and its read hands each tip in, so a refresh fetches nothing (design, Decision 7; Task notes 5.1). Verify `pytest tests/py/test_board.py::TestTheFollowerFetchesEachKitsMain`.

## 6. The docs

- [ ] 6.1 README, the crew skill and `crew`'s usage header say a started bolt whose work its kit's main holds reads landed and is closed whichever way it landed, and is offered on no landings card (`docs.2`; Task notes 6.1). Verify `tests/suite t-docs` ends with "0 failed".
