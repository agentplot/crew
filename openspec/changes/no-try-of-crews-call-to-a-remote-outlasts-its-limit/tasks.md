# Tasks

Build the tasks in order. Each check runs from the place's root as written. A logic or contract check syncs the tests' venv through moon (`tests:venv`), then runs one class by its pytest node id. An end-to-end check runs one test by name through `tests/suite`. Submit nothing, and never run `wt submit --help`.

## 1. A try

- [x] 1.1 `gather.TRY_FOR` is thirty seconds and `gather.GRACE` two; `gather.span` says a limit as `30s` or `300ms`; and `gather.stopped` gives git's last line and `; `, where git wrote one, then the family's words naming the call, the remote and the limit (design Decisions 2 and 3; Task notes 1.1). Passes `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_remote_limit.py::TestTheFamilysLimit'`.
- [x] 1.2 `gather.tried` runs a command in a process group of its own and waits no longer than its limit. A command that ends within the limit gives its exit and everything it printed. At the limit the group is asked to end, given the grace, then killed, and the try is said stopped with nothing the command started left (design Decision 1; Task notes 1.2). Passes `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/contract/test_remote_limit.py::TestATry'`.

## 2. The state repository

- [x] 2.1 `plan.git` runs `fetch`, `ls-remote` and `push` as tries to `gather.TRY_FOR`, each naming its address. A stopped result never reads exit 0. Every other git call runs to its end as before (design Decision 4; Task notes 2.1). Passes `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_remote_limit.py::TestTheStateRepositorysTries'`.
- [x] 2.2 A stopped fetch in `tip_of` or `tips_of` refuses the read at once, naming the branch, the repository and the failure. It is never tried again for a lock and never read as a branch the repository lacks (design Decision 5; Task notes 2.2). Passes `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_remote_limit.py::TestAStoppedFetch'`.
- [x] 2.3 A stopped push in `land` refuses the write at once with the failure: no wait, no fetch and no replay. The command's next read of the branch fetches it, and a run-record entry whose push stopped stays on the host, said once (design Decision 6; Task notes 2.3). Passes `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_remote_limit.py::TestAStoppedPush'`.
- [x] 2.4 Against a state repository that takes the call and never answers, `tip_of` and `land` each refuse well inside the silent remote's sixty seconds, naming `git fetch` or `git push`, the address and `300ms`, and the call's process is gone (design Decisions 5 and 6; Task notes 2.4). Passes `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/contract/test_remote_limit.py::TestTheStateRepository'`.

## 3. A kit's fetch

- [x] 3.1 `FETCH`'s `origin_fetch` tries its `git fetch` through a bash `bounded` whose limit and grace are filled from gather's. So `MAIN`, `CARRIES` and `ORIGIN_FETCH`, on an origin that never answers, fail in `gather.stopped`'s words under every bash the host has, the call's process gone, and fetch as before from an origin that answers (design Decision 7; Task notes 3.1). Passes `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/contract/test_remote_limit.py::TestOriginFetch'`.
- [ ] 3.2 `origin_fetched` and `landing_opened` fetch a kit by running `ORIGIN_FETCH` through `fetch_told` on its host. No kit fetch is left in `kit_git`, gather's `ran` or a script's text outside `FETCH`. `FETCH` sets its limit and grace once each, and neither it nor gather's try reads a setting (design Decisions 2 and 7; Task notes 3.2). Passes `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_remote_limit.py::TestAKitsFetch tests/py/test_kits.py::TestNoFetchInTheRunnersClone tests/py/test_cards.py::TestLandingReading'`.
- [ ] 3.3 gather's fetch of a kit's origin is a try, and a stopped one gives the family's words naming `origin` and the limit (design Decision 8; Task notes 3.3). Passes `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/contract/test_remote_limit.py::TestGathersFetch'`.

## 4. The docs

- [ ] 4.1 README and plan.py's opening docstring say each fetch and push a write makes, and a kit's fetch of its origin, is one try ended at the family's limit of thirty seconds, and that a stopped push is not applied again and the next write reads whether it landed (Task notes 4.1). Verify `tests/suite t-docs` ends with "0 failed".
