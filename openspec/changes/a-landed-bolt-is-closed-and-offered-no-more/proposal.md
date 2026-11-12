# A landed bolt is closed and offered no more

## Why

On 2026-11-12 at 01:17Z, agentplot-ops found boomdrive's bolt `a-boomdrive-release-reports-its-own-version` still listed on `land/boomdrive`, to land again on the user's next send (signal `signals/2026-11-12-agentplot-ops-de559c7f/01-landed-bolt-still-read-as-stopped` on `agentplot/main` of afterthought/crew-state). The bolt had landed. GitHub's main held `6cfc4aec`, `chore(land): #154 bolt/a-boomdrive-release-reports-its-own-version`, whose second parent is `62d2f06`, the head its landing carried. The run record held two `bolt.submit` entries for it:

- at 00:21:46Z, `Outcome: queued`, `Submission: 154`, `Head: 62d2f06`;
- at 00:23:43Z, `Outcome: stopped`, `Head: 62d2f06` and no `Submission`, its `Why` reading "boomdrive's main checkout on deneb has no branch main and no origin", the folder it named being `~/.local/share/flywheel/repositories/agentplot/boomdrive`, gone since the rename.

The day before, crew read weir's and crew's call-limit bolts stopped although sluice had landed each and main held the landing commit, because a host's copy of main had not moved, and ops closed them by hand (signal `2026-11-11-agentplot-planner-b6097ea7/01`).

Both entries came from a crew that still submitted bolts to sluice itself. crew's main no longer submits, and reads a landing from the runner's report alone (record 0056 point 4). That leaves every such bolt with nothing to close it:

- **No base place, so no report.** The bolt has no launch of `bolt/<bolt>` in `requests.rec`. crew reads it as started before bolts were base places, landing "under the crew that started it" (`runner.legacy_said`). `crew bolt land` refuses it in those words, `landing_read` stops at them, and the sweep reads only bolts the runner reports decided. Of the 62 bolts in agentplot's plan on 2026-11-12, one had a launch of its own.
- **A stop that outlives the landing.** `stops` keeps the stop at `62d2f06`, and `landing_pending` keeps `#154` queued, since the stop names no submission. The bolt reads stopped, or queued, for good.
- **A host's checkout.** The older crew read main in the host's checkout of the kit, which lagged GitHub's main or was gone.

A bolt whose work is on its kit's main has landed, whichever way it landed. crew should read it so, close it, and offer it no more.

## What Changes

- **A bolt whose work is on its kit's main reads landed.** Where the runner's report does not read a started bolt landed, crew reads GitHub's main in its own cache of the kit's repository. It reads whether main holds the commit at which each of the bolt's units and chores landed on the bolt, as the runner reports it. Where the run record holds a landing of the bolt at a head, it reads whether main holds the newest such head too. The bolt reads landed at main's commit that landed it once main holds them all. It reads no landing commit's trailer, no record of sluice's or Flume's, and no host's checkout. A bolt with no base place is read the same way.
- **It is recorded and closed by the first act that reads it.** That act is the landings card's raise, the follower's sweep, a kit's read or `crew bolt land` (`plan.21`). It records one `bolt.submit` landed, which ends an older crew's queued landing and any stop, and the `bolt.land` at main's commit, in main-level ops's name, by `crew bolt land`'s own code. `crew bolt land` closes a bolt read landed so, one started before bolts were base places among them.
- **It is offered no more.** A bolt read landed is no row of its kit's landings card, has no line under *land* on the rail, and gets no land on any send. `crew bolts` and the board say it landed at main's commit. It says nothing of a stop or of the crew that started it.
- **Main is read once per command, and by the follower's clock.** A command fetches a kit's main from GitHub into crew's cache once (`plan.12`). The follower's clock fetch carries the main of each repository with a started bolt, and a refresh fetches nothing.
- `README.md`, `plugin/skills/crew/SKILL.md` and `crew`'s usage header say a bolt whose work is on its kit's main is closed whichever way it landed (`docs.2`).

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `bolt-teams`:
  - adds "A bolt whose work is on its kit's main reads landed", "A bolt read landed on main is recorded and closed by the first act that reads it", and "A bolt read landed on main is offered no more";
  - changes "A landing's outcome is read from the runner's report", "A landing's entry names its kit, its head and its time", "crew bolt land closes a started bolt only once its base place reads landed" and "A bolt with no launch of its own lands under the crew that started it".
- `rail-cards`: changes "A landing the runner or Flume stopped keeps its box" and "A bolt started before bolts were base places has no box".

## Impact

- `plugin/lib/plan.py`:
  - new decisions `landing_head` and `on_main`;
  - new reads `main_tip`, `main_holds` and `landed_by`, in crew's cache of the kit's repository;
  - `Stages.landing` and `Stages.base` read main where the report does not read the bolt landed;
  - `landing_entry`, `landing_read`, `started_land`, `landings_judged` and `reap_judged` record and close a bolt read landed on main;
  - `land_facts` and the rail's land group leave it out.
- `plugin/lib/board.py`: `fetches` and the follower's read carry each started bolt's repository's main.
- `plugin/bin/crew` (usage header), `README.md`, `plugin/skills/crew/SKILL.md`.
- Tests: a new `tests/py/test_landed_on_main.py`. Cases in `tests/py/test_stages.py`, `tests/py/test_landing.py`, `tests/py/test_landings.py`, `tests/py/test_rail.py` and `tests/py/test_board.py`, and in `tests/contract/test_git.py`.
- No new key reaches the views: a bolt read landed on main gives the same landing a landed report gives, so `code.8` is not reached.
- Nothing outside this repository changes. No rule page or record is edited (`docs.7`). The design names the departure from record 0056 point 4 that record 0062 is to carry.

## Touches

```
plugin/lib/plan.py
plugin/lib/board.py
plugin/bin/crew
README.md
plugin/skills/crew/SKILL.md
tests/py/test_landed_on_main.py
tests/py/test_stages.py
tests/py/test_landing.py
tests/py/test_landings.py
tests/py/test_rail.py
tests/py/test_board.py
tests/contract/test_git.py
```
