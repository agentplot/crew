# Tasks

Each check runs from the worktree's root as written. `tests/suite <name>` runs one moon task. A pytest check runs the one file it names. The verify stage runs the repository's whole checks once, after the last task. Submit nothing: Flume submits the place once its last stage delivers.

## 1. The teams file as it stands

- [x] 1.1 `crew.readable` gives the data of a teams file crew can read at all and refuses one that is no JSON, no UTF-8, no object or at a version this crew does not read, in the words `crew.load` gives for each, and `load` reads through it with its words and fleet unchanged (design, Decision 1; Task notes 1.1). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_teams.py'` exits 0.
- [ ] 1.2 `crew.teams_step` moves aside only a file crew cannot read at all, and refuses a file at crew's own version that fails a check, naming the check and that the file and every drive it names are left as they are, with nothing written (design, Decision 2; Task notes 1.2). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_drive_set.py'` exits 0.

## 2. The set's record

- [ ] 2.1 `record.emit` appends an entry without pushing it when asked, and `record.reach` with `said` says a refused push once and goes on (design, Decisions 3 and 5; Task notes 2.1). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_record.py'` exits 0.
- [ ] 2.2 `crew.state_unmade` says the teams file names the drive as given, why its state was not made, and that the same command run again makes it (design, Decision 4; Task notes 2.2). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_drive_set.py'` exits 0.
- [ ] 2.3 `crew drive set` appends the set's `drive.set` entry once the file is written and before the state is made, records a refusal once the file names the drive as a refused `state.init` in `crew.state_unmade`'s words, and ends by pushing what of the host's record of the drive the branch lacks, so a run again after a refused first push makes the state and puts the first run's entry on the branch (design, Decisions 3 to 6; Task notes 2.3). Verify `tests/suite t-drive-set` ends with "0 failed".

## 3. The docs

- [ ] 3.1 README, the crew skill and the usage headers of `crew` and `plan.py` say that only a teams file crew cannot read at all is moved aside, that one at crew's own version that fails a check is refused, and how a set's entry reaches the branch when its state is not made (design, Decisions 1 to 6; Task notes 3.1). Verify `tests/suite t-docs` ends with "0 failed".
