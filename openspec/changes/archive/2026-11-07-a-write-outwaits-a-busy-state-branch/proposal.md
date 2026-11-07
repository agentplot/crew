# A write outwaits a busy state branch

## Why

On deneb, on 2026-10-27 at 17:32:58Z, madswan-planner's `crew plan answer 170 plan approve` ended with its card.close entry refused six times by `madswan/main`. The branch took nineteen commits from deneb's writers in two minutes, and `plan.land` gave up inside ten seconds (signal `afterthought/crew-state:swancloud/main signals/2026-10-27-swancloud-operator-cbefe4ba/02-crew-state-push-refused-six-times`).

The cause is in `plugin/lib/plan.py`, `land`. When a push is refused because the branch moved, it fetches afresh and applies the write again at once, five times, with no pause between. A branch that several commands on one host write at the same moment refuses every replay, since the replays come in step with the writes that beat them.

`state.1` says a write is applied again to the new tip until it lands, and that a branch that is merely busy is outwaited, not given up on. Its details name a replay that waits a growing moment before it fetches again as a crew chore that changes no rule. The kept entry is the fallback for a branch that still will not take it: `record.reach` pushes every entry the branch lacks, oldest first, with the host's next entry (`record.2`).

## What Changes

- **A refused write waits before each replay's fresh fetch.** The waits grow, 0.5, 1, 2, 4, 8 and 8 seconds, each drawn afresh over its upper half, so commands refused at one moment do not replay in step.
- **The whole wait is bounded.** Six replays, at most 23.5 seconds of waiting in all, so a command with a write and its entry both replayed still answers within its shell's time (`code.9`).
- **A write still refused says so.** The refusal names the branch, how many times the write was applied and how long it waited.
- **The kept entry stays the fallback.** An entry whose push is still refused is said once and kept on the host, and the host's next push carries it, as today (`record.2`).
- README's State section says the replays wait.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `drive-state`: a rejected push is applied again after a growing wait, up to six times within a bounded wait, and a write still refused says so.
- `bolt-plan`: the same, for the plan's writes.
- `run-record`: an entry refused at every replay because the branch kept moving is kept and goes with the host's next push.

## Impact

- `plugin/lib/plan.py`: `REPLAY_WAITS`, `replay_wait` and `land`.
- `tests/py/test_record.py`: the schedule, and `record.reach` on a branch that keeps moving and then quiets.
- `tests/contract/test_record.py`: a branch busy for three pushes is outwaited and the write lands.
- `README.md`: the State section's replay sentence.
- No change to the views or crew's mod (`code.8`): nothing crew models changes shape.
