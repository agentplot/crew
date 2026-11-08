# A started bolt's kit folder is read as main reads it

## Why

`a-bolts-landing-on-main-reads-landed`, archived on `bolt/crew-reads-each-piece-as-the-tools-hold-it`, read a started bolt's kit folder from the taking runner's `repositories.rec` alone. It refused a runner that reports no repositories for that alone, whatever its places named. That rests on Boomdrive's runner writing `repositories.rec`, R2 of the archived `a-kit-renamed-on-its-host-is-renamed-across-the-plan`, which Boomdrive has not built: at agentplot/boomdrive `c6eb79b`, `boomdrive-crew`'s `write.rs` writes only `runner.rec`, `answers.rec` and `places.rec`. So, as the bolt stood, every started bolt on a host whose runner reports no repositories read unknown and none landed, where crew main reads it in the folder its runner's places name.

agentplot-design ruled on the fix (resting on crew record 0061, the kit-rename change's design R2, and record 0055):

> A started bolt's kit folder is read as crew main reads it today: the folder the runner's repositories.rec names where that runner reports its repositories, else the folder Flume's status of that runner's newest place of the kit names. A runner that reports no repositories is not refused for that alone. Keep the landing read from main and every other part of the change. Where neither gives a folder, as on 8 November (no repositories.rec and no place carried), the kit reads unread, naming the host, as the bolt has it.

Record 0061 has crew name a kept repository's folder from its own teams file, and not from the runner's report alone. Its option 3, the runner's report on its branch, was not taken, since crew could not name a folder until the runner had reported. Record 0055 is rejected, but its Decision 6, the runner reporting the repositories it keeps, stands. R2 says what crew does until the runner reports them: "Without R2, crew takes a kit's folder from a place's status as today".

## What Changes

- **The kit's folder is the runner's report where it reports its repositories, else its newest place's.** Where crew needs a started bolt's kit folder on a host, it reads the one the taking runner's `repositories.rec` names, where that runner reports its repositories. Where it reports none, crew reads the folder Flume's status names of that runner's newest place of the bolt's work. Where the runner carries no place of the bolt's, crew reads the folder of its newest place of the kit's other work, on that host alone. This is how crew main reads it.
- **A runner that reports no repositories is not refused for that alone.** The kit reads unread, naming the host, only where neither the report nor a place gives a folder, as on 2026-11-08: no `repositories.rec` and no place carried.
- A runner that reports its repositories but none for the kit is still refused, naming what it keeps and `crew kit rename`. Its places are not read for the folder.
- The landing read from main, the stub runner's `repositories.rec`, and every other part of `a-bolts-landing-on-main-reads-landed` stand.
- `README.md`, `plugin/skills/crew/SKILL.md` and `crew`'s usage header say so (`docs.2`).

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `drive-state`: "A kit's work is taken by a runner whose configuration names its repository" reads the kit's folder from the runner's report, else from its newest place of the kit, and leaves the kit unread only where neither names it.

## Impact

- `plugin/lib/runner.py`:
  - `kept_folder` gives no folder and no reason for a runner that reports no repositories.
  - `where` takes the folder from the newest place of the work where the runner reports none.
  - `launch_repositories` refuses a taker that gives no folder either way.
- `plugin/lib/plan.py`: `launched_at` falls back to `kit_at` on the taking runner's host. `launched_at` and `kit_at` refuse, naming the host, where no folder is given.
- `README.md`, `plugin/skills/crew/SKILL.md`, `plugin/bin/crew` (usage header).
- `tests/py/test_runner.py`, `tests/py/test_kits.py`, `tests/py/test_stages.py`, `tests/py/test_branch_stands.py`.
- No stage, key or field reaches the views, so `code.8` is not reached.

## Touches

```
plugin/lib/runner.py
plugin/lib/plan.py
plugin/bin/crew
README.md
plugin/skills/crew/SKILL.md
tests/py/test_runner.py
tests/py/test_kits.py
tests/py/test_stages.py
tests/py/test_branch_stands.py
```
