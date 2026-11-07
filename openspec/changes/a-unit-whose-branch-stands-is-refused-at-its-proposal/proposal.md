# A unit whose branch stands is refused at its proposal

## Why

On deneb on 2026-11-07, agentplot-planner dropped `a-base-place-that-conflicts-with-its-base-launches-its-fix` and added it again under the same name. `crew plan propose` passed it, the user approved it, and Flume refused its launch: "the branch change/a-base-place-that-conflicts-with-its-base-launches-its-fix already exists" (signal `afterthought/crew-state:agentplot/main signals/2026-11-07-agentplot-planner-b2717722/01`). Flume keeps a dropped place's branch while it holds work, and refuses a launch that would make it again while it stands (flume 3, 67), so no work is lost. crew checked a new name against the plan and the kit's main alone, never against the branch its launch would make, so it passed a card that could not be carried out (`plan.4`). The planner proposed both again under fresh names (proposal 49).

## What Changes

- **An add reads the branch its launch would make.** `crew unit add`, `crew chore add` and `crew unit split` read whether Flume's branch for each new name, `change/<unit>` or `chore/<chore>`, stands, with git, in each repository a launch of the kit's work would be made in. They read it where the runner reports Flume cutting the kit's places, never from crew's record of a drop (`read.2`).
- **A branch that stands refuses the add.** The refusal names the branch, the folder and host it stands in, its commit, and the two ways on: the work proposed under a fresh name, or the branch removed first by the planner or the user. crew never removes it. A proposal holding such an add is refused when it is written and again at its approval, nothing written.
- **A repository crew can't place refuses the add, saying why** (`read.1`). A kit no runner has taken work of and none reports keeping is not read.
- **A drop of launched work says the name stays taken.** It prints, and records on its entry as `Note`, that Flume keeps the place's branch while it holds work and the name stays taken while it stands. A drop still removes no branch.
- README's plan section says so.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `bolt-plan`: a name whose Flume branch stands is refused when it is planned, and a drop of launched work says the name stays taken.

## Impact

- `plugin/lib/runner.py`: `place_branch`, `kit_launches`, `launch_repositories`, `refs_standing`, `branch_refusal`, `drop_kept_said`.
- `plugin/lib/plan.py`: `BRANCHES`, `branches_in`, `branch_free`, `Reads.free`, `Drawn.free`, `op_unit_add`, `op_unit_drop`, `kit_at`.
- `plugin/lib/record.py`: a drop's `Note` on its entry's line.
- `tests/py/test_branch_stands.py`, `tests/py/facts.py`, `tests/contract/test_git.py`, `tests/t-journey-cross.sh`.
- `README.md`: the plan section.
- No change to the views or crew's mod (`code.8`): no object, stage or field the board reads changes.
