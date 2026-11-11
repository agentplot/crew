# No try of crew's call to a remote outlasts its limit

## Why

crew's git calls that reach a remote have no limit. A remote that takes the call and never answers holds the command, and the agent's shell behind it, for as long as the remote stays silent. On deneb on 2026-11-10, sluice's reads hung for 10 to 17 minutes on such a call: a git fetch whose credential helper waited on GitHub (agentplot-ops' signal `2026-11-10-agentplot-ops-e19d134d/01`).

The family now bounds every try of a call to a remote:

- **The statement.** agentplot/blueprints `design/weir/requirements.md`, 69 and C.3 as amended at `ad3a1ae` (2026-11-11). Each git call of the write protocol's steps that reaches the remote is one try, bounded at the family's limit. C.3 says crew keeps a twin of these steps in Python.
- **The other tools.** weir's own steps are bounded by `weir-bounded` (weir record 0008, the bolt `no-try-of-weirs-call-to-a-remote-outlasts-its-limit`). sluice's are bounded by its record 0109 (`crates/sluice/src/bounded.rs`, `retry::TRY_FOR`). Boomdrive's runner's are bounded by its record 0042.
- **crew's share.** Batch 49's report names crew's Python twin as crew's to bound.

Python cannot take `weir-bounded`, so crew mirrors its behaviour and its words and cites it.

## What Changes

- **A try of crew's own.** `gather.py` gains `tried`, which runs a command in a process group of its own, as `weir-bounded`'s `output` does. It waits no longer than `TRY_FOR`, thirty seconds. At the limit it asks the group to end, gives it `GRACE`, two seconds, then kills it, and says the try stopped. It writes what the command prints to unnamed temporary files and starts no thread.
- **One fixed limit.** Python reads `TRY_FOR` and `GRACE` from `gather.py`, and bash takes them as filled in from there. No setting of crew's, no environment variable and no file sets either one.
- **The family's words.** A stopped try fails with git's last line on standard error and `; `, where git wrote one, followed by `git <fetch|ls-remote|push> with <remote> was still going after 30s, the most a try may take, and was stopped`. Its standard output is never read as an answer.
- **The state repository's calls are tries.** `plan.git` runs `fetch`, `ls-remote` and `push` through `tried`. These are the fetches in `tip_of` and `tips_of`, the push in `land` and state init's adopting push. Every other git call is local and runs to its end, as before.
- **A stopped fetch fails the read** at once, naming the branch and the repository. It is not retried for a lock, and it is not read as a branch the repository lacks.
- **A stopped push fails the write** at once. It is no refusal, so the write does not wait, fetch again or replay. The next write's fetch reads whether the push landed, and every check is made again there. A run-record entry whose push stopped stays on the host for its next push, as one refused does.
- **A kit's fetch of its origin is a try:**
  - gather's fetch runs through `tried`;
  - `FETCH`'s `origin_fetch`, in `MAIN`'s and `CARRIES`'s scripts, runs `git fetch` through a bash `bounded`, its limit, grace and words gather's;
  - the two fetches that went through `kit_git` (a landings card's forecasts and a bolt's work, and a reading tried again) run as `ORIGIN_FETCH`, so a kit is fetched only by gather or `origin_fetch`.

  Each try is bounded on the host where its git runs, so nothing it started outlives it there.
- README's account of a write says each fetch and push is one try to the family's limit.

## Capabilities

### New Capabilities

- `remote-limit`: a try of crew's call to a remote runs in a process group of its own, to the family's limit, and is ended with everything it started. The limit and grace are the family's, set by nothing of crew's. A stopped try is named in the family's words. A kit's fetch of its origin is such a try. Every local git call runs to its end.

### Modified Capabilities

- `drive-state`: a fetch of the drive's branch that stops fails the read. A push that stops fails the write, and it is never replayed. The next write reads whether it landed.

## Impact

- `plugin/lib/gather.py`: `TRY_FOR`, `GRACE`, `span`, `stopped`, `tried`; `fetched` through `tried`.
- `plugin/lib/plan.py`: `git` routes its remote calls through `tried`; `tip_of`, `tips_of`, `land` and `state_init` change; `FETCH` gains `bounded`; `ORIGIN_FETCH`; `origin_fetched`, `landing_opened`.
- `tests/py/test_remote_limit.py` (new), `tests/py/test_kits.py`, `tests/contract/test_remote_limit.py` (new), `README.md`, `tests/t-docs.sh`.
- Unchanged:
  - every local git call;
  - ssh to another host, which is no git call to a remote, though the kit fetch it carries is now bounded on that host;
  - the views and crew's mod (`code.8`), since nothing crew models changes shape;
  - the command's usage (`docs.2`), since no command or flag changes.
