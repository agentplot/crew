# Tasks

Each check runs as written from the place's root. `tests:logic` and `tests:contract` are moon tasks of the `tests` project, and pytest's `-k` picks the named test files by their modules' names. Build the tasks in order. Submit nothing: Flume submits the place once its last stage delivers.

## 1. Each kit read as written

- [x] 1.1 A partition's launches, a landing's kit and a fix of main are read as `requests.rec` and the run record wrote them, with `launches_now` and `main_fix_work` gone, and a started bolt renamed still lands in its kit's clone from its launches as written (design, Decision 1; Task notes 1.1). Passes `tests/py/test_kits.py`, `tests/py/test_main_fix.py` and `tests/py/test_kit_rename.py`: `devenv shell -- moon run tests:logic -- -k "test_kits or test_main_fix or test_kit_rename"`.
- [x] 1.2 `bolt new`, `unit add` and `chore add` write `--repo` as given and say nothing of a rename, a chore given another name of its bolt's kit is refused, and `kit_given`, `former_said`, `former_kept_said`, `Direct.renames` and `Proposed.renames` are gone (design, Decision 2; Task notes 1.2). Passes `tests/py/test_kit_rename.py`, `tests/py/test_bolt_commands.py` and `tests/py/test_landings.py`: `devenv shell -- moon run tests:logic -- -k "test_kit_rename or test_bolt_commands or test_landings"`.
- [x] 1.3 A landings card's and a record card's key are read by the kit they name, with `record_now` and `row_gone`'s close for a renamed kit gone, and neither the rail's read nor its sweep carries renames (design, Decision 1; Task notes 1.3). Passes `tests/py/test_rail.py`: `devenv shell -- moon run tests:logic -- -k test_rail`.
- [x] 1.4 A source's repository is read as written when a proposal's records are read (design, Decision 1; Task notes 1.4). Passes `tests/py/test_proposals.py`: `devenv shell -- moon run tests:logic -- -k test_proposals`.
- [x] 1.5 A kit's landings and deploys, on the board's Operation lane and the page, are read by each `bolt.land` entry's `Repo` as written (design, Decision 1; Task notes 1.5). Passes `tests/py/test_ops.py` and `tests/py/test_page.py`: `devenv shell -- moon run tests:logic -- -k "test_ops or test_page"`.

## 2. The renames go

- [x] 2.1 `kit_now` and the partition's renames are gone. `landings_at` alone reads `runs/`, once per tip, and a partition's kits are its plan's and its landings' names as written, each once, on the board too. `crew kit rename` judges a name an earlier rename renamed as written (design, Decisions 1, 3 and 6; Task notes 2.1). Passes `tests/py/test_kits.py`, `tests/py/test_board.py`, `tests/py/test_asks.py`, `tests/py/test_proposal_life.py`, `tests/py/test_proposal_card.py` and `tests/py/test_kit_rename.py`: `devenv shell -- moon run tests:logic -- -k "test_kits or test_board or test_asks or test_proposal_life or test_proposal_card or test_kit_rename"`.
- [x] 2.2 A rename's commit holds `plan.rec` alone, and the day file holding its `kit.rename` entry passes a real `recfix --check`, with no read through renames (design, Decision 6; Task notes 2.2). Passes `tests/contract/test_recfix.py`: `devenv shell -- moon run tests:contract -- -k test_recfix`.
- [x] 2.3 `runner.py`'s docstrings and descriptor comment cite `roles.9` for where a runner keeps a kit, matched by the kit as the plan gives it, and name no kit's name now (design, Decision 5; Task notes 2.3). Passes `tests/py/test_runner.py`: `devenv shell -- moon run tests:logic -- -k test_runner`.

## 3. The docs and the brief

- [ ] 3.1 `crew`'s usage, README and the crew skill say that what crew recorded elsewhere under a former name stays under it, read as written, and no longer speak of a kit's name now (design, Decisions 1, 2 and 3; `docs.2`; Task notes 3.1). Verify `tests/suite t-docs` ends with "0 failed".
- [ ] 3.2 The planner's brief no longer says a `--repo` given the old name is written under the new (design, Decision 2; Task notes 3.2). Verify `tests/suite t-briefs` ends with "0 failed".
