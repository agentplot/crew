# Tasks

Build the tasks in order, from the worktree's root. Each task names the narrowest check that shows it done, written to run as it stands:

- A logic or contract check runs its pytest files through crew's shell: `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider <files>'`, which exits 0.
- An end-to-end check runs `tests/suite <name>...`, which ends with "0 failed".
- The mod's check runs `tests/suite mod`, which ends with "0 failed".

Submit nothing, and never run `wt submit --help`. An end-to-end test whose `# Reads:` line changes has `tests/moon-tasks` run and `tests/moon.yml` committed with it (`tests.10`).

## 1. crew's bolt kind

- [x] 1.1 crew ships `plugin/flume/kinds/bolt@1/kind.toml`, a kind that lands with no stages and branches `bolt/<bolt>`, and `source.keep` writes it into crew's kinds folder whole, only when its bytes differ, wherever it makes the folder (design Decision 2; Task notes 1.1). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_source.py'` exits 0.
- [x] 1.2 A main-level start on the stubs leaves the bolt kind's package in the scratch HOME's kinds folder (design Decision 2; Task notes 1.1). Verify `tests/suite t-flume-source` ends with "0 failed".

## 2. The requests a bolt takes

- [x] 2.1 `requests.rec` takes a launch of `bolt/<bolt>` of `Kind: crew/bolt` on `main` with no brief and no After, a fix on a bolt started before this release, and a `land` naming a bolt's or a fix of main's launch, and crew's rules refuse each other shape naming its field (design Decisions 3 and 4; Task notes 2.1). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_runner.py'` exits 0.
- [x] 2.2 `recfix --check` passes a `requests.rec` holding a `crew/bolt` launch and a land under crew's descriptor (design Decision 3; Task notes 2.1). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/contract/test_recfix.py'` exits 0.

## 3. A start launches the base place

- [x] 3.1 `crew bolt start` appends the bolt's base-place launch and then its pieces' launches in one plan write, reads no host and makes no branch, and run again on a bolt whose own launch the runner refused launches it anew with its unlaunched pieces (design Decision 3; Task notes 3.1). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_runner.py tests/py/test_made.py tests/py/test_bolt_commands.py'` exits 0.
- [x] 3.2 A started bolt's row reads its base place's launch as the runner answers it, unlaunched with the runner's words while it is not launched, and a started bolt with no base-place launch reads as started before bolts were base places, landing under the crew that started it (design Decisions 3 and 9; Task notes 3.2). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_stages.py'` exits 0.

## 4. The user's send posts a land

- [x] 4.1 `runner.lands_due` gives the rows a send lands, in the card's order with fixes of main first, once per send and head, none for a row taking main first, stopped, or started before this release (design Decisions 4 and 5; Task notes 4.1). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_landings.py'` exits 0.
- [x] 4.2 The raise of a kit's landings card posts the due lands in one plan write, each recorded `bolt.submit` or `fix.merge` with its card, head, request and `Outcome: asked`, a replay writing nothing, and `crew card read land/<kit>` prints the lands posted and no command (design Decisions 4 and 10; Task notes 4.2). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_landings.py tests/py/test_card_commands.py tests/py/test_record.py'` exits 0.
- [x] 4.3 `crew bolt submit` and `crew main fix --send` refuse at once, before any read, naming the card's send as the way, and a fix of main's due land comes from `lands_due` alone (design Decisions 1 and 5; Task notes 4.3). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_main_fix.py tests/py/test_send.py tests/py/test_bolt_commands.py'` exits 0.
- [x] 4.4 On the stubs, a fix of main's row sent on its kit's landings card appends one land of its launch, and both refusing commands still answer `--help` (design Decisions 1 and 5; Task notes 4.3). Verify `tests/suite t-journey-main-fix t-help` ends with "0 failed".

## 5. The outcome from the runner's report

- [x] 5.1 `runner.landing_of` reads a bolt's landing from its base place as the runner reports it: unlaunched, none, asked, stopped, submitted, landed with its commit, refused for a failed check or a conflict, unknown or dropped (design Decision 6; Task notes 5.1). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_runner.py'` exits 0.
- [x] 5.2 The first read after a decided outcome records it once and acts on it: a landing closes the bolt at Flume's commit with its age and split from the run record, a failed check holds its row in Flume's words, a conflict launches the take-main fix once with the send standing, and a stop keeps the row's box with its send spent (design Decisions 6 and 7; Task notes 5.2). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_landing.py tests/py/test_landing_state.py tests/py/test_landings.py tests/py/test_rail.py'` exits 0.
- [x] 5.3 crew's own sluice landing is gone: its submit, wait and read scripts, `crew _landing-read`, the landing's waiter and the leftovers kept for it, with their cases and fixtures (design Decision 1; Task notes 5.2). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_bolt_submissions.py tests/py/test_pane_landing.py tests/py/test_landing.py tests/contract/test_gather.py'` exits 0.
- [x] 5.4 On the stubs a bolt runs from its start to its close through the runner: its land is posted on the send, it closes at the commit the runner reports landed, a conflict's take-main fix is launched once and a second land posted at the bolt's new head on the standing send, and a failed check holds its row (design Decisions 3 to 7; Task notes 5.3). Verify `tests/suite t-journey-land` ends with "0 failed".

## 6. The drop and the tidy

- [ ] 6.1 A drop of a started bolt drops its pieces' launches and then the bolt's, asks the bolt's drop again once no piece is live after the runner refused it, and asks nothing of sluice for its branch (design Decision 8; Task notes 6.1). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_runner.py tests/py/test_bolt_commands.py'` exits 0.
- [ ] 6.2 The tidy runs no sluice, deletes no bolt branch and keeps no bolt-branch mark, and names a landing or legacy bolt worktree it finds with the commands that remove it (design Decision 8; Task notes 6.1). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_tidy.py'` exits 0.

## 7. Nothing of crew's runs a tool for a bolt

- [ ] 7.1 No command string in `plan.py`, `gather.py`, `kit.py`, `board.py`, `runner.py` or `plugin/bin/crew` runs sluice, `wt submit`, `wt merge`, `wt remove`, `gh` or `read-tree`, but the preview functions' (design Decision 1; Task notes 7.1). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_no_tool_for_a_bolt.py'` exits 0.
- [ ] 7.2 The stubs' log of a bolt's run from start to close holds no sluice, `wt` or `gh` call, and no scratch kit's `HEAD`, index or refs but its remotes' moved (design Decision 1; Task notes 7.2). Verify `tests/suite t-journey-land` ends with "0 failed".

## 8. The views

- [ ] 8.1 A bolt's head line, the rail and ops's band say its landing from the runner's report, asked with its request, submitted with Flume's entry, landed, refused, stopped or under the crew that started it, under the keys the mod reads (design Decision 10; Task notes 8.1). Verify `devenv shell -- bash -c 'moon run tests:venv >/dev/null && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_board.py tests/py/test_bolt_submissions.py'` exits 0.
- [ ] 8.2 The mod draws a landing asked with its request and one under test with its entry in ops's band (design Decision 10; Task notes 8.1). Verify `tests/suite mod` ends with "0 failed".

## 9. The words

- [ ] 9.1 Main-level ops's brief has the user's send on the kit's landings card as the one word to land and names no `crew bolt submit`, `wt submit` or `sluice withdraw`, and the planner's and operator's briefs follow (design Decision 11; Task notes 9.1). Verify `tests/suite t-briefs` ends with "0 failed".
- [ ] 9.2 The usage of `plugin/bin/crew`, README, `plugin/skills/crew/SKILL.md` and CLAUDE.md say a bolt starts as a base place and lands on the user's send through the runner, and `crew bolt submit` and `crew main fix --send` refuse (design Decision 11; Task notes 9.1). Verify `tests/suite t-docs` ends with "0 failed".
