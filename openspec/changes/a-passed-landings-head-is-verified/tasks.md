# Tasks

Each check runs from the place's root. A logic or contract check syncs the tests' venv through moon (`tests:venv`), then runs one file, class or case by its pytest node id. An end-to-end check runs one test by name through `tests/suite`.

## 1. The verification

- [x] 1.1 `runner.verification` reads a head that is sluice's landing on the bolt with one verdict, passed, green naming the landing, after any piece's landing at the head; a head with no landing, another verdict, two verdicts or none reads none, and trailers unread read unknown (design Decisions 3 and 4). Passes `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_runner.py::TestVerification'`.
- [x] 1.2 `Stages.verification` and its four callers take the bolt's `head_landing`, so a bolt whose every piece merged and whose head is a record's fix sluice landed passed waits to land and is a row of its kit's landings card that can land, and one whose head names a piece the runner last carried at submitted is not offered (design Decision 5). Passes `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_stages.py::TestEndsHeldForTheRunner tests/py/test_rail.py -k "passed_landing or head_held_for_the_runner or take_main_fix_landed"'`.

## 2. The gather

- [x] 2.1 gather gives each bolt read its `head_landing`: the head's `Sluice-Submission` and `Sluice-Result` values where the head is the newest commit of the bolt's own line beyond main, None for a head main holds, and why where its line can't be listed; and it runs no sluice (design Decisions 1 and 2). Passes `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/contract/test_gather.py -k "verdict_sluice_landed or runs_no_sluice"'`.

## 3. The docs

- [x] 3.1 README, the crew skill, `crew`'s usage header and CLAUDE.md say a head that is a landing sluice made on the bolt that passed reads green whoever submitted it (`docs.2`). Verify `tests/suite t-docs` ends with "0 failed".
