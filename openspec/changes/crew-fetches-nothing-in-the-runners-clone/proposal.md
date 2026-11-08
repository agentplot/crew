# crew fetches nothing in the runner's clone

## Why

`a-kept-repositorys-folder-is-the-runners-container` has crew name the runner's container and view as a kit's folder and checkout on a runner host (record 0061). crew's reads still fetched GitHub into that checkout before a decision, and the design and operator briefs still had their agents fetch there, as that change's design said under *Risks*. On batch 12 agentplot-design ruled that this breaks agentplot/boomdrive `core.14` ("the runner alone fetches it and moves its view"), since two fetchers of one repository race on its refs as sluice's own fetch-lock race showed, and crew record 0056 point 1 (crew reaches the tools only through the runner):

> What must be true: where the teams file names a kept repository for the host, crew runs no git fetch in it, and neither does any brief crew writes. Crew and the main-level agents read GitHub's main there at origin's tracking ref, as the runner last fetched it, which it does every pass and at once on a landing (Boomdrive clones spec, 'When the running runner is told that a kept repository has had a landing'). A read that needs it fresher waits for the runner's next fetch; it doesn't fetch. Elsewhere crew fetches as today.

## What Changes

- **One decision says where crew may fetch.** A path is in the runner's clone where the host's teams file names its repository and the path is that entry's `dir` or `checkout`, or under either. crew fetches nothing there. Everywhere else it fetches as before.
- **Every fetch crew makes in a kit asks that decision first**:
  - `crew bolts` and every other read that asks a kit fetched (`plan.survey`, gather's `kit`), now asked kit by kit;
  - main now (`MAINS`: a give's policy, a landing's recorded head, `crew record`'s record, a change's folder, a pull request's hold), which says the runner's clone and reads `origin/main` as the runner last fetched it;
  - a bolt's start (`BOLT_CREATE`), what a tip carries (`CARRIES`), a landing's two copies (`LAND_COPIES`) and its end (`LANDED`);
  - a landings card's forecasts and the bolt's work (`origin_fetched`), and a reading tried again (`landing_opened`).
- **A landing waits rather than submit a stale head.** In the runner's clone, a landing whose tracking ref of `bolt/<bolt>` is not where GitHub's is, read by `git ls-remote`, which fetches nothing, submits nothing and says it waits for the runner's next fetch.
- **The briefs fetch nothing there.** The design agent's brief names which of its checkouts are the runner's clone, says no `git fetch` or `git pull` is run there, and has it cut a blueprints branch in a worktree rather than pull the runner's view. The operator's brief cuts its swancloud worktree from `origin/main` as the runner last fetched it.
- README and the crew skill say so.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `drive-state`: crew fetches nothing in the runner's clone, reading origin's tracking refs there as the runner last fetched them, and a landing there waits for the runner's fetch where GitHub's bolt has moved past it.
- `bolt-plan`: `crew bolts` and a landing's submission fetch nothing in the runner's clone.
- `main-level`: the design agent's and the operator's briefs fetch and pull nothing in the runner's clone.

## Impact

- `plugin/lib/crew.py`: `runners_clone`, `fetches_in`; `main_tokens`'s `KIT_CHECKOUTS`, `FETCHING`, `BLUEPRINTS_COMMIT` and `SWANCLOUD_FETCH`.
- `plugin/lib/plan.py`: `FETCH`, `fetch_told` and every script that fetches (`MAINS`, `BOLT_CREATE`, `CARRIES`, `LAND_COPIES`), each of their runs; `origin_fetched`, `landing_opened`, `survey`.
- `plugin/lib/kit.py`: `main_now` reads `FETCHED=runner`.
- `plugin/lib/gather.py`: each kit's `fetch`.
- `plugin/roles/design.md`, `plugin/roles/operator.md`, `README.md`, `plugin/skills/crew/SKILL.md`.
- `tests/py/test_kits.py`, `tests/py/test_bolt_commands.py`, `tests/contract/test_git.py`, `tests/contract/test_gather.py`, `tests/t-briefs.sh`.
- Unchanged: crew's own bare cache of the state repositories, which is no kit's clone; the views and crew's mod (`code.8`), since nothing crew models changes shape.
