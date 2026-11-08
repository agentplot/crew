# Tasks

## 1. What a crew is

- [x] 1.1 crew reads a root's release where it runs: a checkout's from git, a build's from `plugin/release.json`, checked field by field and shown as `v<x.y.z>` or `<version>+<seven>`, and nothing where it finds neither, saying why (design, Decision 1; Task notes 1.1). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_release.py'` exits 0.
- [x] 1.2 crew's package writes `plugin/release.json`, the flake's commit and the package's version, where the flake knows its commit, and none where it does not, its `release` giving the same (design, Decision 2; Task notes 1.2). Verify `tests/suite nix:test nix:format nix:lint` ends with "0 failed".
- [x] 1.3 `crew _release` prints what its crew is as one line of JSON, from a checkout and from a build, reading nothing else (design, Decision 6; Task notes 1.3). Verify `tests/suite t-session-hook` ends with "0 failed".
- [x] 1.4 `crew _release --help` prints its usage and exits 0, and the help test lists it among the commands crew dispatches (design, Decision 6; Task notes 1.4). Verify `tests/suite t-help` ends with "0 failed".
- [x] 1.5 A start from a build records the commit and version its release file names, and one from a build with none records neither (design, Decision 1; Task notes 1.5). Verify `tests/suite t-session-hook` ends with "0 failed".

## 2. The crew the host has installed

- [x] 2.1 crew names its command by a checkout's own `plugin/bin/crew`, else the first `crew` on its path outside the Nix store, else its own build's (design, Decision 3; Task notes 2.1). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_release.py'` exits 0.
- [x] 2.2 crew reads the installed crew from its own files where the command is its own, and otherwise by asking it `crew _release` within five seconds, an answer late, failed or missing a field read as unread with its why, and asked once for each real path (design, Decision 6; Task notes 2.2). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_release.py'` exits 0.
- [x] 2.3 Every brief, `crew send`'s words and a command forwarded to this host name the installed crew, and the launch digest reads crew's command as one word whichever path names it (design, Decisions 4 and 5; Task notes 2.3). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_release.py tests/py/test_hold.py'` exits 0.
- [x] 2.4 The Stop hook's hand runs `crew _renew` through the installed crew (design, Decision 4; Task notes 2.4). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_hold.py'` exits 0.
- [ ] 2.5 The console's tabs run the installed crew (design, Decision 4; Task notes 2.5). Verify `tests/suite t-journey-main` ends with "0 failed".

## 3. Updates read against the installed crew

- [ ] 3.1 A standing agent is due when its launch changed, when an installed checkout's loaded plugin changed since its start's commit, or when an installed build is another release than its start recorded, and none is due for crew's plugin where its start recorded no release or the installed crew is unread, each said (design, Decision 7; Task notes 3.1). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_hold.py'` exits 0.
- [ ] 3.2 A band shows, once its agent is due, the version of the crew the host has installed (design, Decision 9; Task notes 3.2). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_hold.py'` exits 0.
- [ ] 3.3 The follower reads a build host's crew by the installed command's real path, hands out the due restarts through the installed crew when an install moves it, and starts again as it, its notice naming it too (design, Decision 8; Task notes 3.3). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_board.py'` exits 0.

## 4. The docs

- [ ] 4.1 README says crew's commands run the crew the host has installed, what a build's start records, when an install makes an agent due and when the follower catches one, and that crew's package carries `plugin/release.json` (design, Task notes 4.1). Verify `tests/suite t-docs` ends with "0 failed".
