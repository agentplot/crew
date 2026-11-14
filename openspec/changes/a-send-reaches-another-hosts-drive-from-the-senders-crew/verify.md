# Verify: a-send-reaches-another-hosts-drive-from-the-senders-crew

Verified on `change/a-send-reaches-another-hosts-drive-from-the-senders-crew` at bf5c9a47, cut from `bolt/a-send-reaches-another-hosts-drive` at 1b4e1b3b. 2026-11-14.

**Outcome: falls short. The whole checks fail, so the change is not archived.** It goes back to its code stage for the failure below. The work holds against every requirement and scenario of the specs, and every task is ticked.

## The whole checks

`tests/suite --affected`, run once from the worktree's root: every `check-full` task the change affects, against the merge-base with main (CLAUDE.md, *Tests*; `tests.5`, `tests.10`).

```
33 passed (2 replayed), 1 failed
```

| Task | Outcome |
|---|---|
| `tests:logic` | **FAIL**: 3 failed, 3716 passed |
| `tests:contract`, `nix:test`, `nix:typecheck` | ok |
| `t-briefs`, `t-docs` (replayed), `t-help` (replayed), `t-journey-main`, `t-specs` and the 25 other end-to-end tasks | ok |

### What fails

Three cases of `tests/py/test_tell_asks.py`, `TestSend` fail:

- `test_a_send_to_an_operator_that_runs_as_its_kind_is_a_send_ask_carrying_whom_it_was_for`
- `test_a_send_to_a_teams_name_from_before_is_refused_and_asks_nothing`
- `test_a_standing_operator_still_up_is_typed_into_with_its_send_entry`

Each fails the same way:

```
plugin/lib/crew.py:979: in send
    label, door = send_door(fleet, name, caller(fleet), this_host())
plugin/lib/crew.py:850: in this_host
    return subprocess.run(["hostname", "-s"], capture_output=True, text=True, check=True).stdout.strip()
E   AssertionError: a logic test starts no process, and this one ran ['hostname', '-s']
```

`crew.send` now reads this host through `crew.this_host()` (task 1.1). `tests/py/test_send.py`'s `acts` fixture stubs `this_host`. The `herdr` and `sender` fixtures of `tests/py/test_tell_asks.py` (lines 35 and 108) do not, so `send` starts `hostname -s` there. The logic tier's conftest refuses any process (`tests.11`, `code.7`). Task notes 1.1 named only `test_send.py`'s fixture. The fix belongs to the code stage: stub `crew.this_host` in `test_tell_asks.py`'s send fixtures as `test_send.py` does, then rerun the logic tier.

## Tasks

All five are ticked `[x]`: 1.1, 1.2, 2.1, 3.1, 3.2. Each task's own check passes in the run above: `test_send.py` (none of its cases fails), `t-journey-main`, `t-briefs`, `t-docs` and `t-help`. Task 1.1's change to `send` is also what breaks the three cases above, so the work is not done until the logic tier passes.

## Requirements and scenarios

`openspec validate a-send-reaches-another-hosts-drive-from-the-senders-crew --strict`: valid.

### operator-agent

- **ADDED: A send to another host's drive runs on the sender's host.** Met.
  - *A send from a box to a Mac's drive*: `tests/t-journey-main.sh` (ok). On the box, `crew send swancloud` types `[crew tell from wldn-planner] (sent to swancloud) …` into `swancloud-operator` on mac-studio through `$box ssh mac-studio herdr --session swancloud-1 agent prompt …`. No ssh line to mac-studio runs `crew`, and mac-studio reaches back over no ssh. `send` is still `py send`, run where it is invoked and not forwarded.
- **MODIFIED: Every brief names one way to send to another drive.** Met.
  - *The planner's brief*: `tests/t-briefs.sh` (ok). For design, planner, main-ops, operator and reviewer, it pins ``/crew send <drive> "<text>"`, run on your own host and never over ssh, which reaches that drive's operator, its one door, wherever it runs, and to nobody else.``, and it checks that the old phrase is gone. `crew.sends` builds that line.
  - *The operator's brief on a box*: unchanged by this change; its existing pin in `t-briefs` passes.
- **MODIFIED: A send to no drive or to the operator's own drive is refused.** Met.
  - *A name crew does not know*: `test_send.py` `TestDoor` (passes), whose anchored pins now carry the refusal's new end; also `t-journey-main` (`crew send swb-2`, `crew send nosuch`).
  - *A drive the host's teams file does not name*: `test_send.py` `test_a_drive_this_hosts_file_does_not_name_is_refused_naming_the_way_on` checks for `drives wldn`, `crew.TEAMS` `on chuck-herdr-alpha`, `never by crew send run on that host over ssh` and `nothing was sent`. `send_door(fleet, name, caller, here)` takes the host as a fact (`code.7`) and refuses through `fail()` (`code.2`).
  - *The door sends to itself*: `test_send.py` `test_the_door_sending_to_its_own_label_is_refused` (passes).

### run-record

- **ADDED: A send's entry is pushed from the sending host.** Met.
  - *A send from a box*: `t-journey-main` (ok). The box's own file of swancloud's record, `runs/chuck-herdr-alpha/`, holds `agent/swancloud-operator wldn-planner 24`, and mac-studio's files hold no send. `swancloud/main`'s newest commit is `runs(chuck-herdr-alpha): send agent/swancloud-operator (wldn-planner)`. `BXMQ` is nowhere in the branch's `runs/`.
  - *A refused push*: `test_send.py` `test_a_send_whose_entry_is_kept_still_reports_it_sent` (passes): `emit` answers `None` and `send` returns `True`. The kept entry, said once, is pinned by `test_record.py` `test_a_push_that_is_refused_is_said_once_and_emit_still_returns_its_id`.

## Rules

- `docs.2`: README, `plugin/skills/crew/SKILL.md` and `plugin/bin/crew`'s usage each say a send runs on the sender's host, never over ssh, with its entry pushed from the sending host. `t-docs` pins it in all three.
- `docs.7`: nothing under `docs/` changes.
- `docs.4`: nothing under `openspec/specs/` changes ahead of the archive.
- `code.8`: nothing crew models moves, so no view or mod change is owed.
- `code.7` / `tests.11` are broken in the logic tier by the failure above.
