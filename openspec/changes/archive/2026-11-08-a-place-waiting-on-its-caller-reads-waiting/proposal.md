# A place waiting on its caller reads waiting

## Why

On deneb on 2026-11-08, agentplot's unit `pull-requests-are-queued-on-the-forge` (request 362, its place `change--pull-requests-are-queued-on-the-forge` on `bolt/sluice-runs-one-host-process`) had gone back three times. Its fourth verify delivered, and sluice's #24 found the submission in conflict. Flume read that at 05:27:17Z. The place had gone back as often as its kind allows, so Flume set it waiting on its caller to retry code, past its bound. At 05:27:18Z Flume delivered the end `submission/1/conflict` to the place's recipient, `agentplot/planner`, as a notice in its pane (Flume 43, 112, 130).

At 05:27:30Z the planner ran `crew answer`. crew refused it: "is at verify, with no question and nothing it waits on its caller for, so there is nothing to answer". The planner then ran `flume retry` by hand, and code began again by 05:28:38Z (signal `afterthought/crew-state:agentplot/main signals/2026-11-08-agentplot-planner-fa099747/01-a-place-past-its-bound-waits-unseen`).

crew had read the runner's carry, not a misread of Flume. Of request 362's place, `agentplot/runner/deneb` held a status carried at 05:26:37Z (147645b3), with verify begun and nothing waited on. The next carry, at 05:27:38Z (2cf78efa), holds Flume's wait: `waiting_on {act: retry, stage: code, why: past_bound}`, its current stage verify delivered. crew's reading of that carry is already right. It reads the place waiting on its caller at code with Flume's words, the planner's band lists it, and `crew answer` appends the retry of code. No case pins any of that, though. And crew's refusal said there was nothing to answer, from a reading 53 seconds older than Flume's notice. The planner had no way to know that crew's reading lagged, or that answering again a minute later would have worked.

## What Changes

- **A place past its bound reads waiting at the stage it waits to retry, whatever stage it last delivered.** The same holds for one waiting on a retry of its submission. This is how crew reads them today. Cases on Flume 0.17.0's own status pin it: request 362's carry at 05:27:38Z, and a submission the merge queue refused made from it. They cover `crew bolts`, the board's ledger, the planner's band and `crew answer`.
- **`crew answer` refuses a live place as of the runner's carry.** For a place neither stopped short nor waiting on its caller, the refusal names the stage, the runner's host and when that runner carried what crew read. It says that a wait Flume has told of since reaches crew with that runner's next carry, and to answer again once `crew bolts` shows the place waiting. It never says a live place has nothing to answer. A place whose work is over is still refused as having nothing to answer, since Flume refuses any retry of it (Flume 50).
- README's list of a piece's stages says that `waits` covers a place past its bound, at the stage it waits to retry, and that `stalled` is Flume's stalled. README, `plugin/skills/crew/SKILL.md`, `plugin/bin/crew`'s usage and the planner's brief say what the refusal names and that the answer is given again once the wait is carried.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `bolt-plan`: a launched place that Flume's status says waits on its caller for a retry reads waiting at the stage it waits to retry, or its submission, past its bound among them, whatever stage it last delivered.
- `bolt-teams`: `crew answer` retries the stage a place past its bound waits to retry. It refuses a live place naming its stage as the runner carried it, with the host and the time, never saying it has nothing to answer.
- `crew-board`: the planner's band lists a place past its bound with Flume's words, at the stage it waits to retry.

## Impact

- `plugin/lib/runner.py`: `answer_retry` takes the runner's carry it read from, and words the refusal of a live place by it.
- `plugin/lib/plan.py`: `answer_place` hands `answer_retry` the host and time of the runner's record of the place.
- `tests/py/flume-0.17.0/`: `past-bound.json`, from request 362's carry, and `submission-refused.json`, made from it. The folder's README names both.
- `tests/py/test_runner.py`, `test_cross.py`, `test_bolt_commands.py`, `test_board.py`: the cases. `test_cross.py`'s refusals of a live place take the new wording.
- `README.md`, `plugin/skills/crew/SKILL.md`, `plugin/bin/crew`'s usage, `plugin/roles/planner.md`: what a place past its bound reads, and what `crew answer`'s refusal names.
- No change to the views file's shape or to `plugin/hooks/status.js`. The bands draw the same keys (`code.8`).
