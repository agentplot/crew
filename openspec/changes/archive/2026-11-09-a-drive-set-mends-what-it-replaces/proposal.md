# A drive set mends what it replaces

## Why

`crew drive set <label>` refuses every teams file at crew's own version that fails a check, before it sets the drive (`a-drive-set-loses-no-drive-and-no-record`, archived 2026-11-09). That includes a file whose only fault is in the drive's own entry, or in a host the flags name. The set replaces those parts whole anyway (record 0065, point 3). So the person is refused for a fault the command would have mended, and the only way past it is a hand edit, which agentplot/boomdrive record 0009's amendment never asks of them.

agentplot-design ruled on it in record 0065's amendment of 2026-11-09, point 8: "A file at crew's own version is written where every check passes once the drive's entry and the hosts the flags name are set as given, whatever the file held for them before. Where a check still fails, the file is refused, naming the check, with nothing written (point 6)." Not taken: "refusing every file at crew's version that fails a check before the set, as the build first did."

## What Changes

- A teams file at crew's own version is no longer checked before the set. `crew drive set` sets the drive in it as it does for a file that loads, and checks the file it would write. Where every check passes, it writes that file and names each key it changed, so a fault in the drive's entry, in a host `--hosts` names, in the drive's console or in a kept repository the flags give is mended by the set.
- Where the file it would write still fails a check, the command is refused in crew's words for the check. The refusal says that the set sets only the drive's entry and the hosts, console and kept repositories its flags give, and that it moves aside only a file crew cannot read at all, so the file and every drive it names are left as they are. Nothing is written, nothing is moved and no state is made.
- A teams file at crew's own version whose `drives` is no list of objects, or whose `hosts`, `consoles` or `repositories` is no object, is refused the same way, naming the key, since the set cannot keep what such a part holds beside the drive. A part that is absent or null holds nothing to keep.
- A file that lists the drive more than once is written with the drive's one entry, the set naming `drives.<label>` as changed.
- A file at crew's own version is still never moved aside. The aside of a file crew cannot read at all, the link's handling, and the refusal of a file crew would write where there was no file or it was moved aside, are as they are.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `drive-setup`: a teams file at crew's own version is written wherever the set mends every check it fails, and refused only where a check still fails once the drive is set, or where a part of it is of a shape the set cannot keep.

## Impact

- **Code**: `plugin/lib/crew.py` (`settable`, new; `teams_set`, which reads any file `readable` gives without a traceback; `teams_step`'s readable path), and the `drive_set` docstring and usage header of `plugin/lib/plan.py`.
- **Tests**: `tests/py/test_drive_set.py`, `tests/t-docs.sh`.
- **Docs**: README's *State*, `plugin/skills/crew/SKILL.md`, the usage headers of `plugin/bin/crew` and `plugin/lib/plan.py`.
- **Unchanged**: the teams file's version and every key crew reads; every check `fleet_of` makes and its words; `crew.load`; a link's handling; the aside's path, its reasons and its refusal when taken; the refusal of a file crew would write where there was none or it was moved aside; the answer's lines and JSON; the set's `drive.set` entry and when it reaches the branch; `crew state init`; crew's module.
- **Views and mod** (`code.8`): nothing the agents' views or `plugin/hooks/status.js` draw changes.
- **Rules and records**: none written here (`docs.7`). Once this lands, the design agent may mark record 0065's point 8 built, and bring point 9's words on a version-6 file that lists no drives to point 8, which has the set write it (design, Decision 2).
