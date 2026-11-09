# Tasks

Build the tasks in order, from the worktree's root. Each task names the narrowest check that shows it done, written to run as it stands:

- A logic check runs its pytest files through crew's shell: `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider <files>'`, which exits 0.
- An end-to-end check runs `tests/suite <name>...`, which ends with "0 failed".
- The mod's check runs `tests/suite mod`, which ends with "0 failed".

Submit nothing, and never run `wt submit --help`. An end-to-end test whose `# Reads:` line changes has `tests/moon-tasks` run and `tests/moon.yml` committed with it (`tests.10`).

## 1. The place holds the bolt's first unit

- [ ] 1.1 The place holds `crew-lands-each-bolt-through-flumes-base-place` as `bolt/crew-lands-through-the-runners-land-message` landed it, merged in from `origin`. Where the bolt does not hold it yet, the stage stops short naming that unit, and builds nothing (design Decision 1; Task notes 1.1). Verify `test -f plugin/flume/kinds/bolt@1/kind.toml && grep -q "crew's bolt kind is a base place" openspec/specs/flume-source/spec.md` exits 0.

## 2. The kind names its landing fix

- [ ] 2.1 `plugin/flume/kinds/bolt@1/kind.toml` names `landing_fix = "flume/fix@1"` and `max_landing_fixes = 3`, and the logic case pinning its bytes holds them (design Decision 2; Task notes 2.1). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_source.py'` exits 0.

## 3. crew reads the landing fix

- [ ] 3.1 `runner.flume_facts` reads a base place's fix kind, bound and fixes from Flume 0.19.0's status, guarded, and reads none from Flume 0.17.0's, on new fixtures in `tests/py/flume-0.19.0/` (design Decision 3; Task notes 3.1). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_runner.py'` exits 0.
- [ ] 3.2 `runner.landing_fix` and `landing_of`'s `fix` say whose a refused landing's way on is: crew's with no fix kind, Flume's while its fix is live, landed or due, and its caller's past the bound or after a fix dropped or not launched (design Decision 3; Task notes 3.2). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_runner.py'` exits 0.

## 4. crew acts on it

- [ ] 4.1 `plan.landing_read` launches no take-main fix and asks ops nothing where the way on is Flume's, and asks ops once in Flume's words, launching nothing, where it is the caller's (design Decision 4; Task notes 4.1). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_landing.py'` exits 0.
- [ ] 4.2 A live landing fix is a fix in flight on its bolt: the row has no box, takes main first or is held in its words, no land is posted while it runs, and the standing send lands the bolt once the fix that took main in has landed (design Decision 5; Task notes 4.2). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_runner.py tests/py/test_landings.py'` exits 0.
- [ ] 4.3 `runner.base_drop_due` asks a refused drop again only once the base place's landing fix has ended (design Decision 5; Task notes 4.3). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_runner.py'` exits 0.

## 5. The views

- [ ] 5.1 A landing's words, the bolt's head line and ops's band name Flume's landing fix, what it does, that it is due, or that the bound is spent (design Decision 6; Task notes 5.1). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_runner.py tests/py/test_landings.py tests/py/test_board.py'` exits 0.
- [ ] 5.2 The mod draws ops's band with a landing fix in flight as the views give it (design Decision 6; Task notes 5.2). Verify `tests/suite mod` ends with "0 failed".

## 6. The brief and the docs

- [ ] 6.1 Main-level ops's brief starts no fix where the row says Flume's landing fix covers it, starts one where the row names none, and says what to do past the bound and for a landing fix that asks (design Decision 7; Task notes 6.1). Verify `tests/suite t-briefs` ends with "0 failed".
- [ ] 6.2 README and the crew skill say that Flume launches a bolt's landing fix where its base place names one, and that crew's take-main fix and ops's fix are for the rest (design Decision 7; Task notes 6.2). Verify `tests/suite t-docs` ends with "0 failed".
