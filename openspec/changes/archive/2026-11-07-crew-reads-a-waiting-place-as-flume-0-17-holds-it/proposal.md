# crew reads a waiting place as Flume 0.17 holds it

## Why

On deneb, on 2026-11-07 at 20:13Z, `crew answer every-fleet-mac-joins-the-tailnet-as-a-host` refused, saying the place was held for its After work with no question. The unit names no After. At the same time, `flume status` showed its place `change--every-fleet-mac-joins-the-tailnet-as-a-host` waiting on an answer to `stage/code/1/ended-short`, with its agent kept open. `crew bolts` said its bolt `a-fleet-hosts-tailnet-key-never-expires` ran where it can't be told. afterthought-planner answered through `flume tell --answers`, which took the answer (signal `afterthought/crew-state:agentplot/main signals/2026-11-07-agentplot-planner-0d0aca85/01-crew-answer-reads-a-place-held-for-after-work`).

crew read the runner's records, not Flume's status. At 20:13Z `afterthought/runner/deneb` held one answer to the unit's launch, request 88: `Outcome: held`, `Words: claimed by deneb's runner; launching once no other runner has claimed it`. That is Boomdrive's claim of a launch it takes (its crew-control-plane spec, Decision 18). crew reads every `held` answer as held for After work. The runner's `launched` answer came in a write at 20:50Z, and the runner never carried Flume's status of the place in `places.rec`. With no place carried, crew could not tell the kit's folder on deneb, so `crew bolts` named no host.

## What Changes

- **A held launch with no After reads launching.** A runner's `held` answer reads waiting on After work only for a launch whose `After` names work. One whose launch names none reads launching, with the runner's words, since the runner also answers `held` for its claim and for a stream with no room. Its line says the runner's words.
- **`crew answer` says when it can't tell.** For a place that reads launching, `crew answer` is refused saying crew can't tell whether the place waits on an answer, and why: no runner has answered its launch, the runner holds it in these words, or the runner has carried none of Flume's status of the place yet. It no longer says there is nothing to answer.
- **A stop-short whose agent Flume keeps open takes `crew answer`.** On Flume 0.17's status, such a place reads needing an answer at its stage. `crew answer` appends the retry naming that stage, which Flume hands the session kept open, as a tell answering it does (Flume 42, 49, 198). A fixture of Flume 0.17.0's own status pins it.
- **A started bolt's host is its runner's, read before its place is carried.** `crew bolts`, the board's ledger and the page name the host whose runner took the newest of the bolt's launches, while the kit's folder there can't be told yet. They never say where it runs can't be told for work a runner has taken.
- README and the `crew answer` usage say both.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `bolt-plan`: a launch the runner holds reads waiting only when its `After` names work, and launching with the runner's words otherwise. A stop-short whose agent is kept open reads needing an answer.
- `bolt-teams`: `crew answer` answers a stop-short whose agent is kept open by the retry of its stage. It is refused naming what crew could not read when the runner has not carried the place.
- `drive-state`: a started bolt's host is the one whose runner took its newest launch taken, named while the kit's folder there can't be told yet.

## Impact

- `plugin/lib/runner.py`: `stage_of`, `piece_said`, `answer_retry`.
- `plugin/lib/plan.py`: `Stages.host`, `bolts_data`, the `answer` docstring.
- `plugin/lib/board.py`, `plugin/lib/page.py`: the ledger's and the page's host, from `Stages.host`.
- `plugin/bin/crew`, `README.md`: what `crew answer` refuses, and what a held launch with no After reads.
- `tests/py/flume-0.17.0/`: Flume 0.17.0's status of a stop-short whose agent is kept open. `tests/py/facts.py` `ran` carries it, a runner's words on a held answer, and a launch with no place carried.
- `tests/py/test_runner.py`, `test_cross.py`, `test_bolt_commands.py`, `test_board.py`: the cases. `tests/py/test_page.py`: its stand-in readers give `host`.
- No change to the views file's shape or `plugin/hooks/status.js`. The bands draw the same keys, the piece's words through `runner.piece_said` and the ledger's host (`code.8`).
