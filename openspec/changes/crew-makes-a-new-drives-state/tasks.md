# Tasks

Each check runs from the worktree's root as written. `tests/suite <name>` runs one moon task. A pytest check runs the files it names. The verify stage runs the repository's whole checks once, after the last task. Submit nothing: Flume submits the place once its last stage delivers.

## 1. The teams file

- [x] 1.1 `crew.load` is a read of the file and `crew.fleet_of(data, here)`, which makes every check it made and answers the same fleet; a file that is no JSON is refused naming the file and the parser's words; and every refusal of the file, a missing file's among them, names crew's own module, `services.crew`, `crew drive set` or the machine's configuration as its writer (design, Decisions 5 and 13; Task notes 1.1). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_teams.py'` exits 0.
- [x] 1.2 `t-teams` finds the new writer's words in each refusal it pins, and `crew bolts` on a host with no teams file refused naming `crew drive set` (design, Decision 13; Task notes 1.2). Verify `tests/suite t-teams` ends with "0 failed".

## 2. What crew drive set decides

- [x] 2.1 `crew.drive_given` makes the drive's entry, its hosts, its console and its kept repositories from the flags alone, and refuses each flag left out, repeated past its count or given a value crew does not accept, naming the flag (design, Decision 2; Task notes 2.1). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_drive_set.py'` exits 0.
- [x] 2.2 `crew.teams_set` replaces the drive's entry whole, its console and its kept repositories, keeps everything else the file holds and names each key it changed, and `crew.teams_text` writes `nix/tests/files/deneb.json` and `runner.json` again byte for byte (design, Decisions 3, 4 and 10; Task notes 2.2). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_drive_set.py'` exits 0.
- [x] 2.3 `crew.teams_step` writes a new file, leaves one the same flags wrote, moves a file crew cannot load aside once, refuses where the aside is taken, writes nothing through a link and goes on only where the linked file names the drive as given, and refuses a file `fleet_of` would refuse, naming nothing written (design, Decisions 5, 7 and 8; Task notes 2.3). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_drive_set.py'` exits 0.
- [x] 2.4 `crew.drive_said` answers what was done in plain lines or as one JSON object, naming each outcome (design, Decision 12; Task notes 2.4). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_drive_set.py'` exits 0.

## 3. The command

- [x] 3.1 `crew drive set <label>` runs on the host it is invoked on before any teams file is loaded, fetches the state branch before it writes, writes the file under its lock, makes the drive's state by `crew state init`'s steps and records one `drive.set` entry where it changed a key; `crew main up` then starts the drive's main level; and run again it changes nothing (design, Decisions 1, 6 and 9 to 11; Task notes 3.1). Verify `tests/suite t-drive-set` ends with "0 failed".
- [x] 3.2 `crew state init` says what it said before, now that `state_init` returns what it did (design, Decision 9; Task notes 3.2). Verify `tests/suite t-journey-state` ends with "0 failed".
- [x] 3.3 `crew drive set --help` prints its usage and does nothing else (`code.11`; Task notes 3.3). Verify `tests/suite t-help` ends with "0 failed".
- [x] 3.4 plan.py builds `drive set` alone as its whole parser builds it, and its `-h` answers the command's usage (`code.11`; Task notes 3.4). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_parser.py tests/py/test_help.py'` exits 0.

## 4. The operator's brief

- [x] 4.1 The operator's brief says a teams file that is no link into the Nix store changes through Boomdrive's setup, which writes crew's entry with `crew drive set`, never by a hand edit, and keeps the swancloud steps for a link (design, Decision 14; Task notes 4.1). Verify `tests/suite t-briefs` ends with "0 failed".

## 5. The docs

- [x] 5.1 README, the crew skill, crew's usage and `openspec/config.yaml` name `crew drive set` and what it writes, and none says the crew command never writes the teams file (design, Decisions 1 to 13; Task notes 5.1). Verify `tests/suite t-docs` ends with "0 failed".
