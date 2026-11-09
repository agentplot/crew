# The runner's land takes main's readings in

## Why

The bolt `crew-lands-through-the-runners-land-message` took main in at `0563aa90` (`plan.8`). Each side had archived its own changes into `openspec/specs/`, and two of the merged requirements now contradict each other:

- **A started bolt's close.** bolt-teams "A landing records the commit main holds", the bolt's (`crew-lands-each-bolt-through-flumes-base-place`, Decision 7), refuses `crew bolt land` on a started bolt while its base place does not read landed in the runner's report. bolt-teams "A bolt whose landing main holds closes whatever the runner carried of its places", main's (`a-bolts-landing-on-main-reads-landed`, Decision 3), has `crew bolt land` close a started bolt once its kit's main holds its landing, whatever the runner carried. A bolt whose base place the runner no longer carries, or one started before bolts were base places that the crew that started it landed, meets both: one says refuse, the other says close.
- **What `bolt/<bolt>` serves.** drive-state "A launch names everything the runner passes to Flume", the bolt's, makes `bolt/<bolt>` the work of the bolt's base place: its launch of `crew/bolt` and the retry, drop, priority and land of it. drive-state "A preview names its host, its work, its repository, its branch and its revision", main's (`a-cards-preview-is-asked-of-the-runner`, Decision 1), says `bolt/<bolt>` SHALL be the work of no request but a preview.

The merge built the reconciliation (`414c80cf`): `crew bolt land` closes at either reading, and `bolt/<bolt>` serves both the base place and a landings row's preview. This change says so in the specs.

## What Changes

- **A started bolt closes at either reading.** `crew bolt land` on a started bolt closes it once the runner reports its base place landed, at Flume's commit, or once its kit's main holds its landing with each of its units and chores read landed through it, at that landing. It is refused, recording nothing, while neither holds, naming its landing as the runner's report has it, or naming the piece its landing on main does not hold. A close at the landing main holds records no outcome of the runner's.
- **`bolt/<bolt>` serves its base place and its preview.** A preview of a landings row's bolt names `bolt/<bolt>`, as the base place's requests do. A launch of `bolt/<bolt>` of any kind but `crew/bolt` is refused, as a bolt's base place is of crew's kind; a retry or drop naming a preview names no launch and is refused.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `bolt-teams`: "A landing records the commit main holds" says a started bolt closes at either reading, and is refused only while neither holds; "A bolt whose landing main holds closes whatever the runner carried of its places" gains the scenario of a base place the runner no longer carries.
- `drive-state`: "A preview names its host, its work, its repository, its branch and its revision" leaves what else `bolt/<bolt>` serves to a new requirement, "A bolt's work is its base place's and its preview's".

## Impact

- `plugin/lib/plan.py`: `main_landed`, `started_land` (built in the merge).
- `plugin/lib/runner.py`: `request_refusal`, `PREVIEW_WORK` (built in the merge).
- `README.md`, `plugin/skills/crew/SKILL.md`, `plugin/bin/crew`'s usage (written in the merge).
- Tests: `tests/py/test_landing.py`, `tests/py/test_stages.py`, `tests/py/test_runner.py`, `tests/t-journey-land.sh` (written in the merge).
