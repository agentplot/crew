# Tasks

Each check runs from the worktree's root as written. `tests/suite <name>` runs one moon task. A pytest check runs the one file it names. The verify stage runs the repository's whole checks once, after the last task. Submit nothing: Flume submits the place once its last stage delivers.

## 1. The set mends what it replaces

- [x] 1.1 `crew.settable` refuses a teams file whose `drives` is no list of objects, or whose `hosts`, `consoles` or `repositories` is no object, naming the key, and `crew.teams_set` calls it first and sets the drive in any other file `crew.readable` gives with no traceback, writing a drive listed twice once and naming `drives.<label>` (design, Decisions 3 and 4; Task notes 1.1). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_drive_set.py'` exits 0.
- [x] 1.2 `crew.teams_step` sets the drive in a file at crew's own version before it checks it, writing the file wherever the file it would write passes every check, and refusing where a check still fails or a part is of a shape the set cannot keep, saying the set sets only what its flags give and that the file and every drive it names are left as they are, with nothing written (design, Decisions 1 to 3; Task notes 1.2). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_drive_set.py'` exits 0.

## 2. The docs

- [ ] 2.1 README, the crew skill, the usage headers of `crew` and `plan.py` and `plan.drive_set`'s docstring say that `crew drive set` mends what it replaces in a file at crew's own version and refuses it only where a check still fails, and `tests/t-docs.sh` holds README and the skill to saying so (design, Decision 2; Task notes 2.1). Verify `tests/suite t-docs` ends with "0 failed".
