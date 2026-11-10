# Tasks

Build the tasks in order. Each check runs from the worktree's root, as written. Submit nothing, and never run `wt submit --help`.

## 1. crew's Python runs the crew another host installed

- [x] 1.1 `crew_there` builds the one line that runs `crew` by its name on another host as the one asking, `crew_argv`, `reach` and `read_agent` all run it, and `crew_at`, `crew_on`, `crew_repository`, `repository_named`, `GITHUB` and `MANIFEST` are gone (design Decisions 1, 2 and 5; Task notes 1.1). Verify `devenv shell -- uv run --project tests --locked python -m pytest -q -p no:cacheprovider tests/py/test_crew_on.py` exits 0.
- [ ] 1.2 The guard in that line fails on a host whose path finds no `crew`, naming the host and exiting 127, and otherwise execs the crew it finds (design Decision 3; Task notes 1.2). Verify `devenv shell -- uv run --project tests --locked python -m pytest -q -p no:cacheprovider tests/contract/test_no_crew.py` exits 0.

## 2. The command and the tests' hosts

- [ ] 2.1 `crew _found <agent>` is dispatched, in the usage header and the crew skill, and answers `-h` and `--help` with its usage (design Decision 5; Task notes 2.1). Verify `tests/suite t-help` ends with "0 failed".
- [ ] 2.2 bash's forwarding runs the line `reach` gives, and each test host has crew installed on the login path the stub ssh puts first, so a forwarded command and a tell's look for an agent reach the box's installed crew (design Decisions 2 and 6; Task notes 2.2). Verify `tests/suite t-journey-main` ends with "0 failed".
- [ ] 2.3 A forwarded command and a send reach the box with crew in no drive's `repos`, and a box whose login path finds no crew fails naming it, with nothing run there and no checkout tried (design Decisions 1 and 3; Task notes 2.3). Verify `tests/suite t-journey-main` ends with "0 failed".

## 3. What the README says

- [ ] 3.1 README says a command crew runs on another host runs that host's installed crew by its name on its login path, failing where it finds none, and names `crew _found` (Task notes 3.1). Verify `tests/suite t-docs` ends with "0 failed".
