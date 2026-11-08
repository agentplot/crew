# Tasks

Build the groups in order. Sync the tests' venv once before the first check: `devenv shell -- moon run tests:venv`. A pytest check below runs as written from the worktree's root and passes when it exits 0; each new case's name holds the word its task's `-k` selects. An end-to-end check passes when it ends with "0 failed". Submit nothing: Flume submits the place once its last stage delivers.

## 1. The request and the runner's answer

- [x] 1.1 `requests.rec` takes a preview and its done, naming its host, its work (`bolt/<bolt>` or `unit/<unit>`), its repository, its branch and its revision, with crew's rules refusing one that names no host or carries what it does not take, and `bolt/<bolt>` on any other request (design Decision 1; Task notes 1.1). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_runner.py -k TestPreviewRequest`.
- [x] 1.2 crew reads a runner's `previews.rec` under its descriptor held byte for byte, a file it can't read hiding that runner and a preview's bad JSON marking that preview alone (design Decision 3; Task notes 1.2). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_runner.py -k TestHostReadPreviews`.
- [x] 1.3 A preview's report, its ask's standing and whether an ask is written are read from the requests and the runner on the host the request names alone, a refusal in `answers.rec` read as the runner's (design Decisions 2, 3 and 6; Task notes 1.3). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_runner.py -k TestPreviewReport`.
- [x] 1.4 The asks to put away are those no row, no work and no grace keeps (design Decision 7; Task notes 1.4). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_runner.py -k TestPreviewsPutAway`.
- [x] 1.5 A preview, its done and a `previews.rec` as the runner writes it pass recfix under crew's descriptors (design Decisions 1 and 3; Task notes 1.5). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/contract/test_recfix.py -k preview`.

## 2. What a card says

- [ ] 2.1 A landing row and a batch line say a preview asked, waiting for room, coming up, up, failed with no output, refused in the runner's or sluice's words, no longer listed or unread, and no longer say "No preview." (design Decision 4; Task notes 2.1). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_cards.py -k "preview or made"`.

## 3. The commands

- [ ] 3.1 `crew card preview` on the partition's main machine writes one request, a bring-up or its done, recorded as `card.preview`, changes the card in place and answers, writing nothing for an ask that stands and running nothing on the work's host (design Decision 6; Task notes 3.1). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_card_commands.py -k preview`.
- [ ] 3.2 Each row of a kit's landings card that can land offers a preview with no policy read and carries the runner's report of its ask, and the card's raise writes the done of each ask no row that can land carries (design Decisions 5 and 7; Task notes 3.2). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_landings.py -k preview`.
- [ ] 3.3 A batch card's lines carry the runner's report of their asks, and its close writes the done of each ask of its units no other open batch card holds (design Decision 7; Task notes 3.3). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_batches.py -k preview`.
- [ ] 3.4 The rail's read on the partition's main machine writes the done of each ask whose card or row is gone once it is two minutes old, and changes a waiting card in place when what the runner reports changes what the card was told (design Decisions 7 and 8; Task notes 3.4). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_rail.py -k preview`.
- [ ] 3.5 crew runs no `sluice preview`, `sluice previews` or `sluice release`, reads no kit's `[preview]` and keeps no preview record of its own (design Decision 9; Task notes 3.5). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_runner.py -k test_crew_runs_no_sluice_command_for_a_preview`.
- [ ] 3.6 The internal commands `_preview`, `_card-preview` and `_preview-release` are gone from `crew` and its parser (design Decision 9; Task notes 3.6). Verify `tests/suite t-help` ends with "0 failed".

## 4. End to end

- [ ] 4.1 On the stubs, a landings row's preview is asked by a request, listed once the runner reports it, said failed, put away by the user's done and by the landing's raise, with no sluice preview command run (design Decisions 6 to 8; Task notes 4.1). Verify `tests/suite t-journey-land` ends with "0 failed".

## 5. The briefs and the docs

- [ ] 5.1 Main-level ops's and the planner's briefs say crew asks the runner on the host where the work runs, and that the card changes once the runner reports it (design Decision 10; Task notes 5.1). Verify `tests/suite t-briefs` ends with "0 failed".
- [ ] 5.2 README, the crew skill and the usage of `crew card preview` say the same (design Decision 10; Task notes 5.2). Verify `tests/suite t-docs` ends with "0 failed".
