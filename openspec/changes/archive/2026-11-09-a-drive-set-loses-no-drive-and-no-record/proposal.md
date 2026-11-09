# A drive set loses no drive and no record

## Why

`crew drive set <label>` (built by `crew-makes-a-new-drives-state`, archived on `bolt/crew-names-each-drive-once`) can lose what it was given in two ways, which batch 25's review of that change found and agentplot-design ruled on in record 0065, points 6 and 7 (accepted 2026-11-09).

- **A drive.** `crew.teams_step` moves aside every teams file `crew.fleet_of` refuses. A file at crew's own version 6 with one wrong field is crew's own file, written by this command or crew's module, and moving it to `teams.json.before-drive-set` drops every other drive of the host from the live file for that one field. Record 0065, point 6: "A file at crew's own version that fails a check is crew's own file, written by this command or the module. It is refused, naming the check, with nothing written." Only a file crew cannot read at all, "not JSON, not an object, or at a version this crew does not read", is the person's own in agentplot/boomdrive record 0009's sense and moved aside once. `code.5`'s details already rule out "moving aside a file at crew's own version".
- **A record.** `drive_set` writes its `drive.set` entry only after the drive's state is made, and only from the keys its own file write changed. A run whose file write lands but whose state push fails writes none, and the run again finds the file unchanged and writes none either, so the drive's branch never says who named the drive. Record 0065, point 7: "When a run's file write lands but its state push fails, the run that finishes the state records the set the drive's branch has no entry for. So the branch always says who named the drive, however many runs it took."

## What Changes

- A teams file crew cannot read at all is moved aside once, as now: one that is no JSON or no UTF-8, holds no object, or gives a version this crew does not read, a missing version among them.
- A teams file at crew's own version that fails any other check is refused, in crew's words for the check, saying that only a file crew cannot read at all is moved aside and that the file and every drive it names are left as they are. Nothing is written, nothing is moved and no state is made.
- The set's `drive.set` entry is appended to this host's run record as soon as the file write lands, before the state is made. The same command pushes it to the drive's branch: with the state's first write where the branch is new, or by its last act, which pushes every entry of this host's record of the drive that the branch lacks. Where the state is not made, the host keeps the entry, and the run that makes the state pushes it first.
- A refusal once the teams file names the drive as given is the state's. It is recorded as a refused `state.init` on `plan/<label>`, beside the set's entry, not as a refused `drive.set`. Its words say the teams file names the drive and that the same command run again makes the state.
- `record.emit` can append an entry without pushing it. `record.reach` can say a refused push and go on when it carries entries no entry of the command's own names.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `drive-setup`: only a teams file crew cannot read at all is moved aside, and one at crew's own version that fails a check is refused; the set's entry is written once the file is, and reaches the branch with the state; a state not made is the state's refusal, finished by the same command again.

## Impact

- **Code**: `plugin/lib/crew.py` (`readable`, read by `load` and `teams_step`; `teams_step`'s refusal of a version-6 file that fails a check; `state_unmade`, the words of a state not made), `plugin/lib/record.py` (`emit`'s `push`, `reach`'s `said`), `plugin/lib/plan.py` (`drive_set`'s order of acts and last push, `drive_set_refused`).
- **Tests**: `tests/py/test_teams.py`, `tests/py/test_drive_set.py`, `tests/py/test_record.py`, `tests/t-drive-set.sh`.
- **Docs**: README's *State*, `plugin/skills/crew/SKILL.md`, the usage headers of `plugin/bin/crew` and `plugin/lib/plan.py`.
- **Unchanged**: the teams file's version and every key crew reads; every check `fleet_of` makes and its words; a link's handling; the aside's path and its refusal when taken; the answer's lines and JSON; `crew state init`; the run record's descriptor; crew's module.
- **Views and mod** (`code.8`): nothing the agents' views or `plugin/hooks/status.js` draw changes.
- **Rules and records**: none written here (`docs.7`). Once this lands, the design agent may lift record 0065's consequence "Until `a-drive-set-loses-no-drive-and-no-record` lands, …" and record the choices this design makes as its own.
