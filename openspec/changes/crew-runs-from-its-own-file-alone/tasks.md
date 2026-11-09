# Tasks

Each check runs from the worktree's root as written. `tests/suite <name>` runs one moon task. A pytest check runs the files it names. The verify stage runs the repository's whole checks once, after the last task. Submit nothing: Flume submits the place once its last stage delivers.

## 1. The teams file

- [x] 1.1 `crew.load` reads no hosts file and loads with none present. It reads `hosts`, each drive's `folder`, `repos` and `accounts`, and `consoles` from the teams file, and refuses each missing or wrong key as main-level's requirement says, naming the field and the fix. Where a host keeps a repository is read from the teams file alone. A role's brief names each session's account from the drive's `accounts`, and a host's kind from `hosts` (design, Decisions 1 to 4, 6, 8 and 9; Task notes 1.1). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_teams.py'` exits 0.
- [x] 1.2 A kit is found where the teams file keeps it: the file's `repositories` entry on this host, else `<folder>/<name>` of the first drive on that host whose `repos` lists it. A repository no drive lists is not kept, and two by one name are refused (design, Decision 4; Task notes 1.2). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_kits.py'` exits 0.
- [ ] 1.3 crew reaches another host by the `ssh` name the teams file's `hosts` gives it, and runs crew there from the checkout the drives on that host keep. It refuses a host the file does not list, or one keeping no checkout of crew, naming what it looked for (design, Decisions 2 and 5; Task notes 1.3). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_crew_on.py'` exits 0.

## 2. crew's module

- [ ] 2.1 crew's module declares `settings.hosts`, `settings.consoles` and each drive's `folder`, `repos` and `accounts`, with no default. It fails evaluation for each case the crew-flake delta names, and writes deneb's drives, hosts and consoles byte for byte as `nix/tests/files/deneb.json` and `runner.json`, which are written again (design, Decision 10; Task notes 2.1). Verify `tests/suite nix:test` ends with "0 failed".
- [ ] 2.2 The module's typecheck evaluates with the new keys given (design, Decision 10; Task notes 2.2). Verify `tests/suite nix:typecheck` ends with "0 failed".
- [ ] 2.3 The nix files tasks 2.1 and 2.2 touched are as nixfmt writes them (Task notes 2.3–2.4). Verify `tests/suite nix:format` ends with "0 failed".
- [ ] 2.4 The nix files tasks 2.1 and 2.2 touched pass statix and deadnix (Task notes 2.3–2.4). Verify `tests/suite nix:lint` ends with "0 failed".
- [ ] 2.5 crew loads `deneb.json` and `runner.json` with no hosts file: four drives, wldn's planner and reviewer on ia and its other roles on willdan-alex, and the four consoles on deneb (design, Decision 10; Task notes 2.5). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_module_file.py'` exits 0.

## 3. What crew reads of a host and an account

- [ ] 3.1 The fleet page's subscriptions, each drive's sessions and a drive page's account docks take their accounts from the drives' roles, and no session is shown with no account (design, Decision 8; Task notes 3.1). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_page.py tests/py/test_fleet.py'` exits 0.
- [ ] 3.2 `crew sites` reads the kind of the host it runs on from `hosts`, saying where it can't tell. A deploy's range reads the checkouts the teams file keeps on the drive's host. An environment's host is checked against `hosts` (design, Decisions 2 and 4; Task notes 3.2). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_ops.py tests/py/test_page.py'` exits 0.
- [ ] 3.3 `crew kit rename` reads a host's keeping from its runner, else from the teams file, and refuses a host whose keeping it can't read (design, Decision 4; Task notes 3.3). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_repository_rename.py tests/py/test_kit_rename.py'` exits 0.
- [ ] 3.4 A batch row for a report on another host opens it by its path under the home ssh starts in, over the host's `ssh` name (design, Decision 7; Task notes 3.4). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_rail.py'` exits 0.
- [ ] 3.5 A drive's console opens only on a host whose `consoles` names it, in the folder given. A host's follower and `crew go` act on the drives its `consoles` names (design, Decision 6; Task notes 3.5). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_board.py tests/py/test_console.py tests/py/test_hold.py'` exits 0.
- [ ] 3.6 Every other logic case builds its fleet from the teams file's facts, with no hosts file's sessions (Task notes 3.6). Verify `tests/suite logic` ends with "0 failed".
- [ ] 3.7 The contract cases build their fleets the same way (Task notes 3.7). Verify `tests/suite contract` ends with "0 failed".

## 4. The end-to-end tests

- [ ] 4.1 The end-to-end tests write no hosts file. Each simulated host's teams file gives `hosts`, each drive's `folder`, `repos` and `accounts`, and that host's `consoles`. `t-teams` proves a file loading with a hosts file read for nothing, and refusing a dropped blueprints repo and a missing `folder` (design, Decisions 1 to 6; Task notes 4.1). Verify `tests/suite t-teams` ends with "0 failed".
- [ ] 4.2 `t-journey-board` passes with the new fixture, its subscriptions unchanged (Task notes 4.2–4.23). Verify `tests/suite t-journey-board` ends with "0 failed".
- [ ] 4.3 `t-journey-review` passes with the new fixture (Task notes 4.2–4.23). Verify `tests/suite t-journey-review` ends with "0 failed".
- [ ] 4.4 `t-journey-plan` passes with the new fixture, its hosts-file edit made in the teams file (Task notes 4.2–4.23). Verify `tests/suite t-journey-plan` ends with "0 failed".
- [ ] 4.5 `t-hold` passes with the new fixture, `crew go` opening the consoles `consoles` names (Task notes 4.2–4.23). Verify `tests/suite t-hold` ends with "0 failed".
- [ ] 4.6 `t-journey-main` passes with the new fixture (Task notes 4.2–4.23). Verify `tests/suite t-journey-main` ends with "0 failed".
- [ ] 4.7 `t-briefs` expects each role's account as the drive's `accounts` gives it (Task notes 4.2–4.23). Verify `tests/suite t-briefs` ends with "0 failed".
- [ ] 4.8 `t-roles` passes with the new fixture (Task notes 4.2–4.23). Verify `tests/suite t-roles` ends with "0 failed".
- [ ] 4.9 `t-journey-cross` passes with the new fixture (Task notes 4.2–4.23). Verify `tests/suite t-journey-cross` ends with "0 failed".
- [ ] 4.10 `t-flume-source` passes with the new fixture (Task notes 4.2–4.23). Verify `tests/suite t-flume-source` ends with "0 failed".
- [ ] 4.11 `t-help` passes with the new fixture (Task notes 4.2–4.23). Verify `tests/suite t-help` ends with "0 failed".
- [ ] 4.12 `t-journey-land` passes with the new fixture (Task notes 4.2–4.23). Verify `tests/suite t-journey-land` ends with "0 failed".
- [ ] 4.13 `t-journey-ops` passes with the new fixture (Task notes 4.2–4.23). Verify `tests/suite t-journey-ops` ends with "0 failed".
- [ ] 4.14 `t-journey-state` passes with the new fixture (Task notes 4.2–4.23). Verify `tests/suite t-journey-state` ends with "0 failed".
- [ ] 4.15 `t-journey-signals` passes with the new fixture (Task notes 4.2–4.23). Verify `tests/suite t-journey-signals` ends with "0 failed".
- [ ] 4.16 `t-journey-roles` passes with the new fixture (Task notes 4.2–4.23). Verify `tests/suite t-journey-roles` ends with "0 failed".
- [ ] 4.17 `t-journey-main-fix` passes with the new fixture (Task notes 4.2–4.23). Verify `tests/suite t-journey-main-fix` ends with "0 failed".
- [ ] 4.18 `t-session-hook` passes with the new fixture (Task notes 4.2–4.23). Verify `tests/suite t-session-hook` ends with "0 failed".
- [ ] 4.19 `t-cards` passes with the new fixture (Task notes 4.2–4.23). Verify `tests/suite t-cards` ends with "0 failed".
- [ ] 4.20 `t-sluice` passes with the new fixture (Task notes 4.2–4.23). Verify `tests/suite t-sluice` ends with "0 failed".
- [ ] 4.21 `t-waits` passes with the new fixture (Task notes 4.2–4.23). Verify `tests/suite t-waits` ends with "0 failed".
- [ ] 4.22 `t-stage-facts` passes with the new fixture (Task notes 4.2–4.23). Verify `tests/suite t-stage-facts` ends with "0 failed".
- [ ] 4.23 `t-runner` passes with the new fixture (Task notes 4.2–4.23). Verify `tests/suite t-runner` ends with "0 failed".

## 5. The docs

- [ ] 5.1 README, the crew skill and `openspec/config.yaml` name the teams file as the one file crew reads for a host's drives: its `hosts`, each drive's `folder`, `repos` and `accounts`, and `consoles`. None names swancloud's hosts file (design, Decisions 1 to 6; Task notes 5.1). Verify `tests/suite t-docs` ends with "0 failed".
