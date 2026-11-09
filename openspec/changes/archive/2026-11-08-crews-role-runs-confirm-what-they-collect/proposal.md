# crew's role runs confirm what they collect

## Why

Flume now keeps each end of a place owed to each of its recipients until that recipient confirms it by its delivery's key (weir record 0006, accepted by the user 2026-11-08; flume record 0061). A hand-over confirms nothing. A tidied place's document stays until every end of it is confirmed, and an end nobody confirms expires and shows in status with its recipient. Flume's record names crew among the callers this binds: "every caller that collects must now confirm. crew's role kinds, the runner and a person's own scripts confirm what they act on, or are handed it again at each inbox."

crew names a role's address as the recipient of every place it launches: the planner's for a unit, chore or fix, ops's for a fix of a red main, and a role's own for its work that lands. A role that runs as its kind collects what waits on it at its run's start, from Flume's status as the runner carries it, and acts on it in its turn. It confirms nothing. So every end of every place crew launched stays owed to a role's address for good. The place's document is never let go, and Flume's host status lists the ends as expired after a week.

## What Changes

- **A run's start takes every end Flume holds for its role.** Beside the asks and the places that wait on the role, `crew role start` takes each end that the runners' records show Flume holding for the role's address, owed and not yet confirmed, by its delivery key. It prints them by place after the places that wait. An end a confirm of the role's already names is not taken again. These ends do not make the role wanted: a run is still started only for an ask or a place that waits on it, and takes them with the rest.
- **A run's end asks the runners to confirm each end its turn took.** In the commit that ends the turn, `crew role end` appends to `requests.rec` one `confirm` per place whose ends the turn took. Each names the place's launch, the role's address and each end's delivery key, for the runner that holds the launch to carry to Flume as `flume confirm`. A run lost before its end confirms nothing, and the next run takes those ends again.
- **`requests.rec` gains the act `confirm`**, with a `Delivery` field for each key. crew's rules refuse a confirm that names no launch, no role's address or no key.
- **The report and the run's view count the ends.** The turn's report names how many ends it took, of which places, and that their confirmation was asked. The run's view on the board counts them rather than listing each.
- The turn's prompt, README and the crew skill say so.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `role-runs`: a run's start takes the ends Flume holds for its role and prints them, and its end asks the runners to confirm each one.
- `drive-state`: `requests.rec` holds a confirm of a launch's ends for a role's address, beside the launch, retry, drop, priority and preview.
- `crew-board`: a run's view counts the ends its turn took.

## Impact

- `plugin/lib/asks.py`: the ends owed to an address in the runners' records, the ends a confirm already names, a turn's confirms, and what a start, a report and a run's view say of them.
- `plugin/lib/runner.py`: `REQUESTS`, `FIELDS` and `ACTS` take `confirm` and `Delivery`; `request_refusal` checks a confirm.
- `plugin/lib/plan.py`: `role_start` and `role_end`, and one read of the runners for both the waits and the ends.
- `plugin/lib/board.py`: `run_rows`.
- `plugin/flume/turn.md`, `README.md`, `plugin/skills/crew/SKILL.md`.
- `tests/py/test_asks.py`, `tests/py/test_runner.py`, `tests/py/test_role_kinds.py`, `tests/py/test_board.py`, `tests/contract/test_recfix.py`, `tests/t-journey-roles.sh`, and a fixture of Flume's status with its ends' deliveries under `tests/py/`.
- Depends on two other tools, neither changed here. Flume's `flume confirm` is built on agentplot/flume's bolt `flumes-ends-are-owed-until-confirmed`. The runner reading and carrying a `confirm` is Boomdrive's. Until both reach a host, a confirm stands unanswered and Flume's ends stay owed, as they are today.
