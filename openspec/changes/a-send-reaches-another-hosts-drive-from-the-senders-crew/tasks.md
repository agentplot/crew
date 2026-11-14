# Tasks

Run each check from the worktree's root, as written. A logic check runs pytest through crew's devenv shell and the tests' locked environment, and passes when pytest reports no failure. An end-to-end check passes when `tests/suite` ends with "0 failed". Submit nothing, and never run `wt submit --help`.

## 1. The send's decisions

- [x] 1.1 `send_door` takes this host's name, and its refusal of a name the host's teams file names no drive by names the drives the file names, the file on this host, that a drive another host runs is sent to once that file names it, never by `crew send` run on that host over ssh, and that nothing was sent (design, Decision 3; Task notes 1.1). Verify `devenv shell -- uv run --locked --project tests python -m pytest -q -p no:cacheprovider tests/py/test_send.py` passes.
- [x] 1.2 A send typed into its operator whose entry's push is refused, `record.emit` answering `None`, is reported made: `crew.send` returns `True` (design, Decision 2; Task notes 1.2). Verify `devenv shell -- uv run --locked --project tests python -m pytest -q -p no:cacheprovider tests/py/test_send.py -k entry_is_kept` passes.

## 2. A send from a box to a Mac's drive

- [x] 2.1 `crew send swancloud` run by `wldn-planner` on the box types into `swancloud-operator` on mac-studio through ssh and herdr, runs no crew command on mac-studio, writes its entry in the box's own file of swancloud's record alone, and pushes it from the box as the commit `runs(chuck-herdr-alpha): send agent/swancloud-operator (wldn-planner)` on `swancloud/main`, its text nowhere in the branch's record (design, Decisions 1 and 2; Task notes 2.1). Verify `tests/suite t-journey-main` ends with "0 failed".

## 3. The briefs and the docs

- [x] 3.1 Every brief's line beside its roster says anything for another drive is sent with `crew send <drive> "<text>"`, run on your own host and never over ssh, which reaches that drive's operator, its one door, wherever it runs, and to nobody else (design, Decision 4; Task notes 3.1). Verify `tests/suite t-briefs` ends with "0 failed".
- [x] 3.2 README, the crew skill and `crew`'s usage say a host's teams file names each drive its agents send to, that `crew send` runs on the sender's host, typed through ssh and herdr where the drive runs on another and its entry pushed from the sending host, never over ssh, and that a drive the file does not name is refused with nothing sent (design, Decision 5; Task notes 3.2). Verify `tests/suite t-docs t-help` ends with "0 failed".
