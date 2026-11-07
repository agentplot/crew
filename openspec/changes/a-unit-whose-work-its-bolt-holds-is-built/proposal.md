# A unit whose work its bolt holds is built

## Why

Two readings of 2026-11-07 on deneb found crew reading built work as unbuilt, so no bolt carrying it could be proven, batched or landed:

- **Built by another partition's place.** afterthought's units on `bolt/moons-store-keeps-its-recent-entries-beside-the-compile-cache` and `bolt/a-boxs-build-engine-is-never-killed-at-its-cap` were built by places launched as swancloud before the partition became afterthought, and landed on their bolts (sluice #41, `23e7c55e`, and #35, `b1d81ee4`, each naming `change/<unit>`). crew launched them again for afterthought, and the runner refused each: "the base bolt/… already holds a change named …". afterthought's runner reports no `repositories.rec` and carried no place of either bolt, so `crew bolts` read both bolts "where it runs can't be told" and their units refused (signal `signals/2026-11-07-agentplot-planner-cbc41169/02` on `agentplot/main` of afterthought/crew-state).
- **Landed and tidied.** flume's two units on `flume-names-each-repository-by-its-address` and sluice's on `sluices-own-module-writes-a-hosts-settings` landed on their bolts (flume #22 and #23), and Flume tidied their places. The runner's last carried status of one was `submitted`, and it never carried the other's, so crew read them `submitted` and `launching`. No batch came due and no landing card went up (agentplot-design, 2026-11-07).

In both, the bolt's branch already records the work: sluice's landing commit on the bolt names the place's branch in its `Sluice-From` trailer (sluice clause 23). crew read only the runner's report. Crew record 0056, decision 2, has crew read a bolt's places from what the work's tools hold. `read.1` and `read.2` have crew read a fact where it is recorded, and never guess.

## What Changes

- **A unit or chore is built once its bolt's branch holds its landing.** gather reads each bolt's landings on its first-parent line where crew reads the bolt (`plan.19`), by the branch each one's `Sluice-From` names. A bolt that has landed on main is read beyond main as it stood when the bolt landed. A started piece whose place's branch is named there is `merged` at that landing's commit and time, whatever the runner reports of its place. That branch is `change/<unit>` or `chore/<chore>`, as Flume names it from the launch, and it is the same whichever partition's launch made the place. Then `landed` once main holds its change, as before. A launch refused because the bolt already holds the change reads `merged` and asks nothing more. A batch reads such a unit at its landing, a bolt whose pieces are all merged and whose verification is green waits to land, and a landing's close finds main holding each landing. No partition is read as another (crew record 0055, rejected). Landings crew can't read leave the runner's reading (`read.1`).
- **A bolt whose every launch was refused is read where its runner keeps the kit.** Where the runner that took a bolt's work has carried no place of it, crew reads the bolt in the kit's folder on that runner's host, as the runner's places of the kit's other work name it, never on another host. So `crew bolts` says where it runs.
- `crew bolts` says on such a piece's line which branch landed on the bolt and at which commit.
- README, the crew skill and `crew`'s usage header say this (`docs.2`).

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `bolt-plan`: "A unit whose work its bolt's branch holds is built", added. "A started bolt's work reads its stage from the runner's records" and "A unit's stage is read from the runner, or from the plan before its bolt starts" each name it.
- `drive-state`: "A kit's work is taken by a runner whose configuration names its repository" reads a bolt whose launches were all refused where its runner keeps the kit.

## Impact

- `plugin/lib/gather.py`: the decision `landed_from`, the read `bolt_landings`, and each bolt's `landings` or `landings_error` in a kit's read.
- `plugin/lib/runner.py`: `place_branch` and `built_on_bolt`. `piece_said` names a landing read from the bolt.
- `plugin/lib/plan.py`: `Stages.crossed` reads the bolt's landings, and `launched_at` reads a bolt whose launches carried no place where its runner keeps the kit.
- `plugin/bin/crew` (usage header), `README.md`, `plugin/skills/crew/SKILL.md`.
- No new stage. A piece's `flume` value gains `on`, `branch` and `landed` when it is read from its bolt, and its line's words say so. The board and the mod draw the same keys, so `code.8` is not reached. Nothing outside the standard library is imported (`code.1`).
- `crew-lands-a-bolt-through-flumes-base-place`, a sibling on `teamless/deneb` whose code is held, changes how crew reads a bolt's places once it ships. This change keeps to today's reading, so it merges beneath it.

## Touches

```
plugin/lib/gather.py
plugin/lib/runner.py
plugin/lib/plan.py
plugin/bin/crew
README.md
plugin/skills/crew/SKILL.md
tests/py/facts.py
tests/py/test_stages.py
tests/py/test_bolt_commands.py
tests/py/test_kit.py
tests/contract/test_gather.py
```
