# crew reads each piece's end from the runner's report

## Why

Record 0062, accepted by the user on 2026-11-08, kept a stopgap. When Flume tidied a finished place, the runner kept only the last status it had carried, so a piece that landed read as submitted. Three readings of crew's told such a piece landed from GitHub's landing commits instead, outside the control-plane contract (record 0056 point 4):

- a unit or chore read merged once a landing commit on its bolt's first-parent line names its place's branch in `Sluice-From` (crew #479);
- a fix read merged the same way, from a landing at or after its launch (`a-bolts-landed-fix-reads-merged`);
- a bolt's landing found on its kit's main by its `Sluice-From` or a submitted head, and its pieces read from that landing's line (`a-bolts-landing-on-main-reads-landed`, Decisions 2 and 3).

The record names what retires them: "The readings go in the change that follows the Boomdrive unit `the-runner-carries-each-places-end` onto every host crew serves." That unit landed on agentplot/boomdrive's main at `76e0226` on 2026-11-08 (Boomdrive record 0030, `core.54`). The runner is now one more recipient of each launch that names recipients, and crew names one on every launch. So Flume keeps a tidied place's record for the runner until its report holds it, and the runner carries that record as the place's status: tidied, its work over, landed at its commit or dropped. crew already writes the carried status to `places.rec` and reads it through `runner.stage_of`. Every piece's end is now in the runner's report, and the stopgap goes (`roles.5`: a stopgap is retired by a change of its own; `roles.9`; `read.2`).

## What Changes

- **A piece's end is read from the runner's report alone.** A unit, chore or fix of a started bolt reads merged only once the runner's report carries its place landed, a held record among them, and landed once main holds it. No landing commit on its bolt is read for it.
- **The three readings go.** gather reads no `Sluice-From` and seeks no bolt's landing on main: `landed_from`, `bolt_landings`, `main_landing`, the `landings`, `landed`, `landings_error` and `landed_error` facts and the request's `seek` all go. So do `runner.built_on_bolt`, `Stages.landings`, `plan.landing_sought`, `seek_answered`, and the drop's read of a fix's landings.
- **A bolt's verification** is green only where its head is a piece's landing as the runner reports it.
- **A landed bolt closes** once each of its pieces reads landed from the runner's report, its branch standing or not.
- **A piece whose place was tidied before the runner carried its end** reads as the runner last carried it. Places launched before their host's runner named itself a recipient are the only such pieces.
- `crew bolts` says no piece "landed on its bolt" from a landing commit. README, the crew skill and `crew`'s usage header say a piece's end is the runner's report's.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `bolt-plan`: a piece's stage, a fix's merge and a landed bolt's pieces are read from the runner's report alone; the readings of a bolt's landing commits and of its landing on main go.
- `bolt-teams`: a landed bolt closes on its pieces' ends as the runner reports them.
- `merge-gate`: a bolt's verification reads no landing commit of its bolt.

## Impact

- `plugin/lib/gather.py`: `FROM`, `landed_from`, `LANDINGS`, `bolt_landings`, `LANDED` and `main_landing` go, with `kit`'s reading of them and the request's `seek`.
- `plugin/lib/runner.py`: `built_on_bolt` goes; `verification` and `piece_said` lose the bolt's-landing wording. `place_branch` stays, for the branch Flume refuses a launch over.
- `plugin/lib/plan.py`: `Stages.crossed`, `Stages.fixes` and `crew fix --drop` read the runner alone; `Stages.landings`, `landing_sought`, `seek_answered`, `submits_read` and `submits_at` go, and `survey`, `stages_for`, `bolts_view` and the rail's read seek nothing.
- `plugin/bin/crew`'s usage header, `README.md`, `plugin/skills/crew/SKILL.md`.
- Tests: `tests/py/test_main_landing.py` goes; `tests/py/test_stages.py`, `tests/py/test_fix.py`, `tests/py/test_kit.py`, `tests/py/test_bolt_commands.py`, `tests/py/test_rail.py`, `tests/py/test_runner.py` and `tests/contract/test_gather.py` change; a Flume 0.20.0 fixture of a record held for the runner is added under `tests/py/`; `tests/t-journey-land.sh`'s comment.
- Depends on agentplot/boomdrive's `the-runner-carries-each-places-end` (`76e0226`) and Flume 0.20.0 on every host crew serves. Neither is changed here.
