# Tasks

Each check is a moon task of the `tests` project, run through `tests/suite`: `logic` is `tests:logic`. Submit nothing: Flume submits the place once its last stage delivers.

## 1. The folder

- [x] 1.1 `runner.where` takes a kit's folder from the taking runner's `repositories.rec` where it reports its repositories, else from Flume's status of its newest place of the work, and `launch_repositories` refuses a taker that gives neither, naming its host (design, Decisions 1 and 2; Task notes 1.1). Verify `devenv shell -- sh -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_runner.py tests/py/test_branch_stands.py'` ends with "passed" and no "failed".
- [ ] 1.2 `launched_at` reads a bolt with no place of its own naming the folder by the taking runner's places of the kit's other work, on that host alone, and `launched_at` and `kit_at` refuse naming the host where neither the report nor a place names the folder (design, Decisions 1 and 2; Task notes 1.2). Verify `devenv shell -- sh -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_kits.py tests/py/test_stages.py'` ends with "passed" and no "failed".
- [ ] 1.3 Verify `tests/suite logic` ends with "0 failed".

## 2. The docs

- [ ] 2.1 README, the crew skill and `crew`'s usage header say a kit's folder is the runner's report where it reports its repositories, else its newest place's of the kit, and unread only where neither names it (`docs.2`; Task notes 2.1). Verify `tests/suite t-docs` ends with "0 failed".
