# Design: a write outwaits a busy state branch

## Context

Every write to a drive's branch goes through `plan.land` (`state.1`): make the change on the tip the command holds, commit, push without force, and on a refused push fetch afresh and make it again on the new tip. Today that replay runs five times with no pause. On 2026-10-27, `madswan/main` took nineteen commits in two minutes from deneb's own writers, and a card.close lost all five replays inside ten seconds. The entry was kept and pushed by deneb's next command nine seconds later (`record.2`), so nothing was lost but the branch's view of it for those seconds (`read.5`).

Rules this relies on: `state.1` (a busy branch is outwaited; a growing wait changes no rule), `record.2` (a failed push is said once and changes nothing else), `code.7` (the schedule is a decision of plain facts), `code.9` (a command answers within its shell's time), `read.1` (a write still refused says so and names what it could not do), `tests.4` (the reproducing case in the lowest tier) and `tests.8` (no test waits on the clock). Pages whose area the change touches: `core.md` (`state.1`), `plan.md` (`plan.1`: the change still re-checks every precondition on each replay, unchanged) and `record.md` (`record.2`). It departs from none.

## Goals / Non-Goals

**Goals:** a refused write's replays spread out in time and out of step with the writers that beat them; the whole wait has a bound a command can afford; the kept entry stays the fallback.

**Non-Goals:** no change to how a write is made, checked or committed; no lock between commands on one host; no queue of writes.

## Decisions

### Decision 1: a growing wait before each replay's fresh fetch

`land` waits before it fetches the branch afresh, not after. A replay made straight after a refusal meets the same burst that refused it; the wait is what lets the burst pass. The waits double from half a second up to eight: `REPLAY_WAITS = (0.5, 1, 2, 4, 8, 8)`. The last attempt's refusal waits for nothing, since no replay follows it; `land` still fetches afresh then, to tell a moved branch from a push that failed for another reason.

A push refused for another reason, GitHub out of reach or a credential refused, now costs the first wait, at most half a second, before the fresh fetch finds the branch where it was and `land` fails as before. Not taken: a fetch at once to read whether the branch moved, then the wait, then a second fetch. It doubles the fetches on the common path to save half a second on the rare one.

Not taken: replays at a fixed interval. A fixed interval keeps commands refused together in step, and either spends the bound on short waits that a burst outlasts or on long waits a quiet branch never needed.

### Decision 2: each wait drawn afresh over its upper half

`replay_wait(n, draw)` gives the nth wait as `REPLAY_WAITS[n] * (1 + draw) / 2`, for a draw in [0, 1). `land` draws with `random.random()` for each wait. Writers on one host refused at one moment, as deneb's were, then replay at different moments rather than colliding again. The draw is a fact handed in, so the schedule stays a function of plain facts (`code.7`) and its logic case names its draws. Each wait is never more than its nominal, so the bound holds whatever is drawn.

Not taken: full jitter over [0, w). It can draw several near-zero waits in a row, which is the no-pause loop this fixes.

### Decision 3: six replays, at most 23.5 seconds of waiting

Six replays give seven attempts spread over 12 to 23.5 seconds of waiting, plus each attempt's own fetch and push, about two seconds each over https: roughly half a minute, three times the window that lost all five on 2026-10-27. A command may land two writes, its plan write and then its entry, each replayed to the end: about a minute in all, inside the two minutes an agent's shell gives one command (`code.9`).

Not taken: a longer bound. Past half a minute a write that still fails is a branch that will not take it, and the kept entry already carries it with the host's next push (`record.2`), while a longer wait would push a command with two writes past its shell's time.

### Decision 4: the refusal names the wait

A write still refused fails with `<ref> of <repo> kept moving: the write was applied 7 times, waiting <s> s in all between them, and each push was refused`. `record.reach` already turns a refused entry push into one line on standard error, keeps the entry and goes on (`record.2`), so the kept entry is the fallback with no change to `reach`.

## Risks / Trade-offs

- **A command takes longer on a busy branch.** Up to 23.5 seconds more per write, where it used to give up in ten. That is the trade: the write lands, or a command waits half a minute before it keeps its entry.
- **The bound is read from one day's burst.** Nineteen commits in two minutes is the busiest branch on the record; a busier one would keep more entries for the next push, which loses nothing.

## After deploy

None: the schedule, the bound and the fallback are each proved by the logic and contract tiers, and nothing about the change needs a live host to show.

## Task notes

**1.1** In `plugin/lib/plan.py`, beside `LOCK_TRIES`: `REPLAY_WAITS = (0.5, 1.0, 2.0, 4.0, 8.0, 8.0)` and `REPLAYS = len(REPLAY_WAITS)`, with a comment citing `state.1` and `code.9`; `replay_wait(n, draw)` returning `REPLAY_WAITS[n] * (1 + draw) / 2`. `random` is imported where `land` draws, as the module's rarer imports are, since only a refused push needs it. Cases in `tests/py/test_record.py`: the nominal waits grow, the first under a second, and sum to at most 23.5 s; a draw of 0 gives half the nominal and a draw near 1 just under it.

**1.2** In `land`: after a refused push, when a replay follows, `time.sleep(replay_wait(n, random.random()))` before `tip_of(repo, ref, fresh=True)`; the last refusal sleeps for nothing. The final refusal names the attempts and the waiting in all. The docstring says the replays wait. Case in `tests/py/test_record.py`, with `plan.git`, `plan.commit`, `plan.checked`, `plan.show`, `plan.tip_of`, `time.sleep` and `random.random` stood in for: a branch that moves at every push sees a wait before each fresh fetch but the last, growing, and `record.reach` with an entry id says once that the entry did not reach the branch, naming "kept moving", keeps it in the host's file, and returns None; once the branch takes pushes again, the next `reach` pushes it and returns 1.

**2.1** In `tests/contract/test_record.py`, beside the case of one refused push: another clone pushes before each of this command's first three pushes; `land` lands on the fourth, its chain on top of the other clone's last commit, after three waits each smaller than the next, recorded by a stand-in for `time.sleep` and each made before a fresh fetch.

**3.1** README's State section: the replay sentence says a refused push is applied again after a growing wait, up to six times.
