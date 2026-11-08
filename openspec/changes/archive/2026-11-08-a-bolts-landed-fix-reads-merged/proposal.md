# A bolt's landed fix reads merged

## Why

On 2026-11-08 deneb's crew (teamless 937a6268, with #479) read four fixes that had landed on their bolts as `submitted`: `a-dropped-launch-is-never-offered` #28, `boomdrive-is-ready-to-go-public` #27, `weir-kinds-name-their-fix` #3 and `sluice-sessions-start-their-mcp-servers` #22. Each fix's place had landed, and the runner's last carried status of it was still `submitted`, Flume having tidied the place or the runner not having carried its end yet. A fix in flight holds its bolt's landing, so each bolt waited until the planner dropped the fix by hand (signal `signals/2026-11-08-agentplot-planner-7ea1b40c/01` on `agentplot/main` of afterthought/crew-state: "fix/a-dropped-launch-is-never-offered/its-tests-take-the-neutral-names fix submitted #28", read at 04:18:50Z). boomdrive's `bolt/a-dropped-launch-is-never-offered` already held the landing, sluice's `0a3c8843` at 04:18:32Z on its first-parent line, with `Sluice-From: fix/a-dropped-launch-is-never-offered--its-tests-take-the-neutral-names (fix/a-dropped-launch-is-never-offered--its-tests-take-the-neutral-names)`. The planner dropped the launch at 04:18:57Z (request 553).

#479 (`a-unit-whose-work-its-bolt-holds-is-built`) reads a unit or chore as merged once a landing sluice made on its bolt names its place's branch (sluice clause 23). It left fixes out: `runner.place_branch` gives no branch for a fix, and `Stages.fixes`, the landing's hold (`land_facts`, `runner.fixes_in_flight`) and a fix's drop read the runner's report alone. Crew record 0056, decision 2, has crew read a bolt's places from what the work's tools hold, and `read.1` and `read.2` have crew read a fact where it is recorded. The bolt's branch records the fix's landing as it records a unit's.

## What Changes

- **A fix on a started bolt is merged once a landing on the bolt names its place's branch.** A fix's place is Flume's fix kind named `<bolt>--<name>`, so its branch is `fix/<bolt>--<name>`. A landing sluice made on the bolt's first-parent line, at or after the fix's launch, that names that branch in its `Sluice-From` makes the fix `merged` at that landing's commit and time, whatever the runner last carried of its place. This is how a unit's and a chore's places are read. A landing made before the fix's launch builds nothing of it. That landing was a dropped launch's of the same name, which a fix launched again under that name must not inherit.
- **Every decision reads a fix the same way.** `crew bolts`, the board and the agents' bands read it so. A fix so read no longer holds its bolt's landing, so the bolt reads proven and its row on its kit's landings card is held for no fix. Its drop is refused, as a merged fix's is. The landing reads the bolt's fixes through the same reading as `crew bolts`, not through a second read of the runners.
- A fix of a kit's main lands on main, not on a bolt, and is never read from a bolt's landings. Where crew can't read the bolt's landings, the runner's reading stands (`read.1`).
- `crew bolts` says on such a fix's line which branch landed on the bolt and at which commit, as for a unit.
- README, the crew skill and `crew`'s usage header say a fix is read so (`docs.2`).

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `bolt-plan`: adds "A fix whose place's landing its bolt's branch holds is merged" and "A fix read merged from its bolt's landing holds nothing".

## Impact

- `plugin/lib/runner.py`: `place_branch` gives a bolt's fix's branch. `built_on_bolt` takes the launch's date, before which a landing builds nothing. `fixes_in_flight` reads the bolt's fixes as `Stages.fixes` gives them.
- `plugin/lib/plan.py`: `Stages.landings`, a bolt's landings as its kit was read, used by `Stages.crossed` and `Stages.fixes`. `Stages.fixes` applies `built_on_bolt`. `land_facts` reads the fixes in flight from `Stages.fixes`. `fix` and `fix_flume` read a fix's drop against the bolt's landings.
- `plugin/bin/crew` (usage header), `README.md`, `plugin/skills/crew/SKILL.md`.
- No new stage, key or field. A fix's `flume` value gains `on`, `branch` and `landed` when it is read from its bolt, the keys a unit's already has. The board and the mod draw them already, so `code.8` is not reached. Nothing outside the standard library is imported (`code.1`).

## Touches

```
plugin/lib/runner.py
plugin/lib/plan.py
plugin/bin/crew
README.md
plugin/skills/crew/SKILL.md
tests/py/test_fix.py
tests/py/test_stages.py
```
