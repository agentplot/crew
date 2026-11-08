# Tasks

Build the groups in order. Each check runs from the worktree's root as written. Submit nothing, and never run `wt submit --help`.

## 1. crew reads the host's kept repositories

- [x] 1.1 `crew.load` reads the teams file's `repositories`, refuses any entry not of its shape naming the file, the repository and the machine's configuration, and keeps the entries on the fleet with the host they are for, reading the host only when the file names any (design, Decisions 2, 3 and 4; Task notes 1.1). Verify `devenv shell -- sh -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_teams.py'` ends with "passed" and no "failed".
- [x] 1.2 On the host its teams file is for, a repository the file names is kept at its `dir` and `checkout` whether or not a session's space lists it, by address or name alone, one name for two repositories across the file and the spaces is refused, and every other host's kits are the spaces' as today, through one resolver that `kit_kept` and `kept_on` read (design, Decision 5; Task notes 1.2). Verify `devenv shell -- sh -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_kits.py'` ends with "passed" and no "failed".
- [x] 1.3 A partition whose main level runs on the host its teams file is for, and whose first blueprints repository the file names, has that `checkout` as its checkout, where its roles start (design, Decision 6; Task notes 1.3). Verify `devenv shell -- sh -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_teams.py'` ends with "passed" and no "failed".
- [x] 1.4 ops's deploy range reads each repository its main level's session keeps at the checkout the resolver names (design, Decision 8; Task notes 1.4). Verify `devenv shell -- sh -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_ops.py'` ends with "passed" and no "failed".

## 2. Every main level's brief names them

- [x] 2.1 The brief's tokens name the first blueprints repository's folder, each kit's checkout with its folder, and swancloud's checkout and folder as the main level's host keeps them, in words where it keeps none (design, Decision 7; Task notes 2.1). Verify `devenv shell -- sh -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_teams.py'` ends with "passed" and no "failed".
- [ ] 2.2 The design brief names its checkout's and each kit's folder and says a checkout is moved by its host alone, and the operator's brief names swancloud's checkout and folder from its tokens and no hard-coded `~/Code/github_afterthought/swancloud`, each pinned by a phrase (design, Decision 7; `tests.6`; Task notes 2.2). Verify `tests/suite t-briefs` ends with "0 failed".

## 3. The flake writes the key

- [ ] 3.1 `services.crew.settings.repositories` is declared, keyed by `<owner>/<name>`, each entry exactly an absolute `dir` and `checkout` with no default, left out of the file where unset (design, Decision 9; Task notes 3.1). Verify `devenv shell -- moon run nix:format nix:lint nix:typecheck` exits 0.
- [ ] 3.2 deneb's partitions with crew's and swancloud's kept repositories render `nix/tests/files/runner.json` byte for byte, `deneb.json` still has no `repositories`, and an entry with no `checkout`, a relative `dir`, a key with no owner or a `view` key fails evaluation (design, Decision 9; Task notes 3.2). Verify `devenv shell -- moon run nix:test` prints "nix: test: every case holds".
- [ ] 3.3 crew loads `nix/tests/files/runner.json` on deneb as its teams file and names crew's folder and checkout as the file gives them (design, Decision 9; `flake.3`; Task notes 3.3). Verify `devenv shell -- sh -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_module_file.py'` ends with "passed" and no "failed".

## 4. The docs

- [ ] 4.1 README and the crew skill say the teams file may name the host's kept repositories, whose folders and checkouts crew names on that host, and today's folders where it names none (design, Decision 10; `docs.2`; Task notes 4.1). Verify `tests/suite t-docs` ends with "0 failed".
