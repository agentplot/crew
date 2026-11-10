# Tasks

Each check runs from the worktree's root as written. `tests/suite <name>...` runs those moon tasks and ends with its summary line. A pytest check runs only the files it names. The verify stage runs the repository's whole checks once, after the last task. Submit nothing: Flume submits the place once its last stage delivers.

## 1. The module

- [ ] 1.1 crew's module declares a drive's `runs`, each of the five roles `"standing"` or `"on-demand"`, and `review`'s `after_changes` and `after_hours`, each description saying what it holds, its unit and its range; deneb's settings and the pinned files `nix/tests/files/deneb.json` and `runner.json` carry the new keys; evaluation fails for a `runs` value it does not take, for `review`'s `every` and `hours`, and for a setting out of range (design, Decision 5; Task notes 1.1). Verify `devenv shell -- moon run nix:format nix:lint nix:test` exits 0.

## 2. crew reads the file by its names

- [ ] 2.1 crew loads a drive's `runs` and its `review`'s `after_changes` and `after_hours`. It refuses a drive naming `flume`, a `review` naming `every` or `hours`, a `runs` that leaves a role out, names another key or gives a value other than `standing` or `on-demand`, and a setting out of range, each refusal naming the drive, the key and the teams file's writer. `crew.on_demand` and `crew.role_runs` answer how a role runs (design, Decisions 1, 3 and 4; Task notes 2.1). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_teams.py'` exits 0.
- [ ] 2.2 `crew drive set` takes `--runs <role> standing|on-demand` once for each role, and `--review <after_changes> <after_hours>`, and writes them as the file names them. It refuses another way of running, a setting out of range, and `--flume`, each before anything is read (design, Decision 6; Task notes 2.2). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_drive_set.py tests/py/test_parser.py'` exits 0.
- [ ] 2.3 Every reader of a role's way of running asks `crew.on_demand` or `crew.role_runs`, and an on-demand role's stream, in its role record, its run's landing work, `crew main status` and the board's run views, is its drive's label. A batch is due by `after_changes` and `after_hours`. The logic tier's fixtures name `runs` and the new `review` keys (design, Decisions 1 to 3 and 7; Task notes 2.3). Verify `tests/suite logic` ends with "0 failed".
- [ ] 2.4 The contract tier's role record is written from a drive's `runs`, naming the drive's label as its stream (design, Decision 2; Task notes 2.4). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/contract/test_recfix.py'` exits 0.

## 3. The end-to-end tests

- [ ] 3.1 `tests/lib.sh`'s fixture names `runs` and the new `review` keys, its `role_runs` sets a role `standing` or `on-demand`, and the tests that read a role's stream read the drive's label (design, Decision 2; Task notes 3.1). Verify `tests/suite t-roles t-journey-roles t-journey-main` ends with "0 failed".
- [ ] 3.2 The other end-to-end tests that set a role's way of running call `role_runs`, and the review journey reads the batch's new words (design, Decision 3; Task notes 3.2). Verify `tests/suite t-briefs t-hold t-journey-review t-journey-signals t-cards t-help` ends with "0 failed".
- [ ] 3.3 `t-drive-set` names a person's drive with `--runs` for each role (design, Decision 6; Task notes 3.3). Verify `tests/suite t-drive-set` ends with "0 failed".

## 4. The texts

- [ ] 4.1 README, the crew skill and the usage headers of `crew` and `plan.py` name a drive's `runs`, `standing` or `on-demand`, its `review`'s `after_changes` and `after_hours`, and `crew drive set`'s `--runs` and `--review <after_changes> <after_hours>`, and none names `--flume` or a drive's `flume`; `tests/t-docs.sh` holds them to it (design, Decision 8; Task notes 4.1). Verify `tests/suite t-docs` ends with "0 failed".
- [ ] 4.2 The operator's brief names `runs`, `standing` or `on-demand`, and `after_changes` and `after_hours` among what a drive's entry says, and no `flume`; `tests/t-briefs.sh` holds it to it (design, Decision 8; Task notes 4.2). Verify `tests/suite t-briefs` ends with "0 failed".
