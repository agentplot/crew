# crew finds itself on another host by the repository it is

## Why

On deneb, on 2026-11-07, running crew 0.41.0-unstable-2026-11-07, `crew send wldn ...` answered: "Could not tell wldn-operator on chuck-herdr-alpha: none of chuck-herdr-alpha's sessions keeps afterthought/crew, so crew can't run there, so crew can't tell whether it is waiting on a question; nothing was sent" (signal `signals/2026-11-07-agentplot-planner-19c0453f/01` on agentplot/main of afterthought/crew-state).

`crew_at` (`plugin/lib/crew.py`) looked for `afterthought/crew` on the other host, a name written in crew's code. crew moved to agentplot/crew that day, by removal and addition (record 0055, rejected), and the box's spaces keep `agentplot/crew`. So every command crew runs on another host was refused: a tell, a send, an ops act, a card or a landing's read. crew follows no former name (record 0058, `plan.22`), so the fix is not to map the old name to the new one. crew reads its own address.

## What Changes

- **crew reads the repository it is from its own manifest.** `plugin/.claude-plugin/plugin.json` names it as `repository`, `https://github.com/agentplot/crew`. Every install carries the manifest: a checkout, and the release the fleet copies whole. No module or command of crew's names the address.
- **crew runs itself on another host from that repository's checkout**, found as the host's sessions keep it. A host that keeps none is refused, naming the repository crew looked for. A checkout kept under a former address is not crew's.
- **A manifest that names no GitHub repository is refused**, naming the file, and nothing is run on the other host (`read.1`).
- The decision, `crew_on`, is a function of plain facts, and `crew_at` reads around it (`code.7`).
- The test fixtures' hosts keep crew under its current address. The manifest joins the command core every end-to-end task takes as an input (`tests.10`).

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `crew-command`: crew runs itself on another host from the checkout of the repository its manifest names, and refuses a host that keeps none, naming that repository.

## Impact

- `plugin/.claude-plugin/plugin.json`: its `repository`.
- `plugin/lib/crew.py`: `MANIFEST`, `repository_named`, `crew_repository`, `crew_on`, `crew_at`.
- `tests/py/test_crew_on.py`: the cases.
- `tests/lib.sh`: the hosts fixture keeps `agentplot/crew`.
- `tests/moon-tasks`, `tests/moon.yml`, `CLAUDE.md`: the manifest in the command core and the logic tier's inputs.
