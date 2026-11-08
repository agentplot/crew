# Tasks

Build the tasks in order, from the worktree's root. Each task names the narrowest check that shows it done, written to run as it stands:

- A logic or contract check runs its pytest files through crew's shell: `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider <files>'`, which exits 0.
- An end-to-end check runs `tests/suite <name>...`, which ends with "0 failed".

Submit nothing, and never run `wt submit --help`.

## 1. A bolt's verification from the runner's report

- [x] 1.1 `runner.verification(head, pieces)` reads a bolt green when its head is the commit at which one of its units, chores or fixes reads merged or landed, naming the head and the work. It reads none for any other head, and unknown with no head (design Decision 4; Task notes 1.1). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_runner.py'` exits 0.
- [x] 1.2 Every reader of a bolt's verification takes it from `runner.verification` over the bolt's pieces as `Stages` reads them: its state, `landing_unready`, `land_facts`, `crew bolts` and the landings row. `kit.verification`, `kit.covering` and `kit.VERDICT` are gone, and the fixtures make a bolt green by its head (design Decision 4; Task notes 1.2). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_kit.py tests/py/test_runner.py tests/py/test_stages.py tests/py/test_rail.py tests/py/test_landing.py tests/py/test_landings.py tests/py/test_pane_landing.py tests/py/test_bolt_commands.py tests/py/test_batch_answer.py tests/py/test_board.py tests/py/test_cards.py tests/py/test_ops.py tests/py/test_kit_rename.py'` exits 0.
- [x] 1.3 The gather reads no `Sluice-Result` and runs no `sluice status` for a bolt's head. `gather.landing_read`, `LANDING_TRAILERS` and `BESIDE_FIELDS` are gone, and a bolt's read carries no `verdict` and no `beside` (design Decisions 4 and 6; Task notes 1.3). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/contract/test_gather.py'` exits 0.

## 2. A piece's submission and a bolt's landing from the runner and the run record

- [x] 2.1 `crew bolts`, the board's lanes and the agents' bands show each piece's submission only as `runner.piece_said` says it, and a bolt's landing only as the run record holds it. They give no `submission`, `landing` or `submissions_error`, and `merge_said`, `landing_said` and `queue_said` are gone (design Decision 2; Task notes 2.1). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_bolt_submissions.py tests/py/test_board.py tests/py/test_rail.py'` exits 0.
- [x] 2.2 A bolt's time on the board, the rail and the bands places no minute by a submission. The landing's entry still records its split from sluice's record read at the landing (design Decision 5; Task notes 2.2). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_board.py tests/py/test_bolt_time.py tests/py/test_landing.py'` exits 0.

## 3. The gather and the follower run no sluice

- [x] 3.1 The board's follower keeps no sluice watch, asks no overview at its tick and keeps no submission of its own. A moved runner's branch is a host's move, and `crew _follow --once` still ticks once (design Decision 3; Task notes 3.1). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_board.py'` exits 0.
- [x] 3.2 A gather of a kit runs no sluice command. Its request hands in no queue, and its answer carries no `submissions`, `decided`, `overview` or `overviews`. crew's requests hand in none, `Kept` keeps none, and `stamped` asks no overview (design Decision 6; Task notes 3.2). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/contract/test_gather.py tests/py/test_bolt_submissions.py tests/py/test_board.py'` exits 0.
- [x] 3.3 The running follower starts no `sluice` on any host, and a runner's report of a piece submitted as `#41` shows `submitted #41` on its line at the next refresh after the follower's fetch (design Decisions 3 and 7; Task notes 3.3). Verify `tests/suite t-journey-board` ends with "0 failed".
- [x] 3.4 `crew bolts` reads a bolt's verification from the runner's report of its work's landing at its head, end to end (design Decision 4; Task notes 3.4). Verify `tests/suite t-sluice t-journey-land` ends with "0 failed".

## 4. The words

- [x] 4.1 These say where a bolt's queue and verification now come from: `crew`'s usage, README, the crew skill, main-level ops's brief, CLAUDE.md, `board.py`'s follower usage and the mod's comment. None of them says a view reads sluice's queue or its verdict (design Decision 8; Task notes 4.1). Verify `tests/suite t-docs t-briefs mod` ends with "0 failed".
