# Verify: a-send-reaches-another-hosts-drive-from-the-senders-crew

Verified on `change/a-send-reaches-another-hosts-drive-from-the-senders-crew` at 33007f24, cut from `bolt/a-send-reaches-another-hosts-drive` at 1b4e1b3b. 2026-11-14.

**Outcome: the whole checks pass, and the work holds.** Every requirement and scenario of the specs is met, and every task is ticked. The change is archived along with this report.

## The whole checks

`tests/suite --affected`, run once from the worktree's root. It runs every `check-full` task the change affects, against the merge-base with main (CLAUDE.md, *Tests*; `tests.5`, `tests.10`).

```
34 passed (34 replayed), 0 failed
```

| Task | Outcome |
|---|---|
| `tests:logic` | ok (replayed) |
| `tests:contract`, `nix:test`, `nix:typecheck` | ok (replayed) |
| `t-briefs`, `t-docs`, `t-help`, `t-journey-main`, `t-specs` and the 25 other end-to-end tasks | ok (replayed) |

Every task was replayed. moon replays only a run that passed on this host with identical inputs, so each task passed at this tree's inputs (`tests/suite`'s header). The code stage's run of the logic tier at 33007f24 reported 3719 passed.

`tests/py/test_tell_asks.py`'s `TestSend.sender` fixture stubs `crew.this_host` (task 1.3), as `tests/py/test_send.py`'s `acts` fixture does. No logic case that calls `crew.send` starts `hostname` (`tests.11`, `code.7`).

## Tasks

All six are ticked `[x]`: 1.1, 1.2, 1.3, 2.1, 3.1 and 3.2. Each task's own check is among the passing tasks above: `test_send.py` and `test_tell_asks.py` in `tests:logic`, `t-journey-main`, `t-briefs`, `t-docs` and `t-help`.

## Requirements and scenarios

`openspec validate a-send-reaches-another-hosts-drive-from-the-senders-crew --strict`: valid.

### operator-agent

- **ADDED: A send to another host's drive runs on the sender's host.** Met.
  - *A send from a box to a Mac's drive*: `tests/t-journey-main.sh` (ok). On the box, `crew send swancloud` types `[crew tell from wldn-planner] (sent to swancloud) …` into `swancloud-operator` on mac-studio, through ssh and `herdr --session swancloud-1 agent prompt …`. No ssh line to mac-studio runs `crew`. `send` is `py send`, run where it is invoked and never forwarded. `crew.send` passes this host to `send_door` through `this_host()` (`plugin/lib/crew.py:979`).
- **MODIFIED: Every brief names one way to send to another drive.** Met.
  - *The planner's brief*: `tests/t-briefs.sh` (ok). For design, planner, main-ops, operator and reviewer, it pins ``/crew send <drive> "<text>"`, run on your own host and never over ssh, which reaches that drive's operator, its one door, wherever it runs, and to nobody else.``. It also checks that the old phrase is gone. `crew.sends` builds that line.
  - *The operator's brief on a box*: this change leaves it as it was, and its pin in `t-briefs` passes.
- **MODIFIED: A send to no drive or to the operator's own drive is refused.** Met.
  - *A name crew does not know*: `test_send.py` `TestDoor` and `t-journey-main` (`crew send swb-2`, `crew send nosuch`).
  - *A drive the host's teams file does not name*: `test_send.py` `test_a_drive_this_hosts_file_does_not_name_is_refused_naming_the_way_on` checks for `drives wldn`, `crew.TEAMS` `on chuck-herdr-alpha`, `never by crew send run on that host over ssh` and `nothing was sent`. `send_door(fleet, name, caller, here)` takes the host as a fact (`code.7`) and refuses through `fail()` (`code.2`).
  - *The door sends to itself*: `test_send.py` `test_the_door_sending_to_its_own_label_is_refused`.

### run-record

- **ADDED: A send's entry is pushed from the sending host.** Met.
  - *A send from a box*: `t-journey-main` (ok). The box's own file of swancloud's record, `runs/chuck-herdr-alpha/`, holds `agent/swancloud-operator wldn-planner 24`, and mac-studio's files hold no send. `swancloud/main`'s newest commit is `runs(chuck-herdr-alpha): send agent/swancloud-operator (wldn-planner)`. The send's text is nowhere in the branch's `runs/`.
  - *A refused push*: `test_send.py` `test_a_send_whose_entry_is_kept_still_reports_it_sent`. `emit` answers `None` and `send` returns `True`, because `send` returns what `tell` typed whatever `emit` answers. `test_record.py` `test_a_push_that_is_refused_is_said_once_and_emit_still_returns_its_id` pins that the kept entry is said once.

## Rules

- `docs.2`: README, `plugin/skills/crew/SKILL.md` and `plugin/bin/crew`'s usage each say a send runs on the sender's host, never over ssh, with its entry pushed from the sending host. `t-docs` pins this in all three.
- `docs.4`: nothing under `openspec/specs/` changes before the archive.
- `docs.7`: nothing under `docs/` changes.
- `code.7`, `tests.11`: the decision `send_door` takes this host as a fact, and no logic case starts a process.
- `code.8`: nothing that crew models changes, so no view or mod change is owed.
