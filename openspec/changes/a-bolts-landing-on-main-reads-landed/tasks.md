# Tasks

## 1. The kit's folder is the runner's report

- [x] 1.1 `runner.where` takes a kit's folder from the taking runner's `repositories.rec` alone, and a runner that reports no repositories leaves the kit unread naming its host (design, Decision 1; Task notes 1.1). Verify `devenv shell -- sh -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_runner.py -k TestWhere'` ends with "passed" and no "failed".
- [x] 1.2 `launched_at`, `kit_at` and `launch_repositories` read no folder from a place the runner carried, of the bolt's work or the kit's other work (design, Decision 1; Task notes 1.2). Verify `devenv shell -- sh -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_kits.py tests/py/test_branch_stands.py'` ends with "passed" and no "failed".
- [x] 1.3 Every logic case whose runner reads a kit's folder gives that runner a `repositories.rec` naming it, with no outcome changed beyond the folder's source and the reason's words (design, Decision 1; Task notes 1.3). Verify `tests/suite logic` ends with "0 failed".
- [x] 1.4 The stub runner of `tests/lib.sh` reports the repositories each host keeps in `repositories.rec` (design, Decision 4; Task notes 1.4). Verify `tests/suite t-journey-land` ends with "0 failed".

## 2. A bolt's landing on main

- [ ] 2.1 `gather.main_landing` finds a bolt's landing on main's first-parent log by a `Sluice-From` naming `bolt/<bolt>` or a known head as its second parent, made at or after the bolt's first launch (design, Decision 2; Task notes 2.1). Verify `devenv shell -- sh -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_main_landing.py -k TestMainLanding'` ends with "passed" and no "failed".
- [ ] 2.2 `runs_at` reads the run record's `bolt.submit` entries, and `landing_sought` gives each started bolt's first launch and the heads crew submitted of it (design, Decision 2; Task notes 2.2). Verify `devenv shell -- sh -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_main_landing.py -k TestLandingSought'` ends with "passed" and no "failed".
- [ ] 2.3 The kit's read reads main's first-parent log once, records each sought bolt's landing, and reads a landed bolt's landings from that landing whether or not its branch stands (design, Decisions 2 and 3; Task notes 2.3). Verify `devenv shell -- sh -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/contract/test_gather.py -k landed_bolts_landings'` ends with "passed" and no "failed".
- [ ] 2.4 `stages_for` asks each kit for its started bolts' landings, so a bolt landed on main whose places the runner no longer carries reads landed, each piece through its landing, and one its landing does not hold keeps the bolt from closing (design, Decision 3; Task notes 2.4). Verify `devenv shell -- sh -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_stages.py -k TestABoltLandedOnMain'` ends with "passed" and no "failed".

## 3. The command, on the stubs

- [ ] 3.1 The stub sluice lands a pull request's submission with `Sluice-From: <agent> (pull/<n>)`, as sluice does (design, Decision 4; Task notes 3.1). Verify `tests/suite t-journey-land` ends with "0 failed".
- [ ] 3.2 `crew bolt land` closes a bolt landed on main whose branch GitHub deleted and whose places the runner no longer carries (design, Decision 3; Task notes 3.2). Verify `tests/suite t-journey-land` ends with "0 failed".

## 4. The docs

- [ ] 4.1 README, the crew skill and `crew`'s usage header say a kit's folder is the runner's report alone and a landed bolt's pieces are read from its landing on main (`docs.2`; Task notes 4.1). Verify `tests/suite t-docs` ends with "0 failed".
