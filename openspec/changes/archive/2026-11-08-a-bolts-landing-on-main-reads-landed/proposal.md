# A bolt's landing on main reads landed

## Why

On 2026-11-08 at 16:05Z, `crew bolt land` refused to close swancloud's bolt `a-fleet-hosts-tailnet-key-never-expires` (signal `signals/2026-11-08-agentplot-operator-784a0698/01-crew-cant-close-tidied-bolt` on `agentplot/main` of afterthought/crew-state). It refused with: "the runner on deneb took bolt a-fleet-hosts-tailnet-key-never-expires's work and has carried no place of it yet, so crew can't tell where it keeps swancloud there". `crew bolts` showed the unit `every-fleet-mac-joins-the-tailnet-as-a-host` launching and the bolt unknown.

The bolt had landed. swancloud's main held sluice's landing `4acecf09` at 16:02:45Z:
- its subject was `chore(land): #475 bolt/a-fleet-hosts-tailnet-key-never-expires`;
- its trailer was `Sluice-From: afterthought-ops (pull/377)`;
- its second parent was `900527e9`, the head `crew bolt submit` recorded in the bolt's `bolt.submit` entry (submission 73).

That head's own first-parent line held the unit's landing, `chore(land): #65 change/every-fleet-mac-joins-the-tailnet-as-a-host`, with `Sluice-From: change/every-fleet-mac-joins-the-tailnet-as-a-host (change/every-fleet-mac-joins-the-tailnet-as-a-host)`. GitHub had deleted `bolt/a-fleet-hosts-tailnet-key-never-expires` once the pull request merged. deneb's runner branch `afterthought/runner/deneb` answered the unit's launch (request 88) `launched`, and its `places.rec` held no place at all. It holds no `repositories.rec`.

Two readings failed together:

- **The kit's folder.** `runner.where` takes it from the runner's `repositories.rec`, or, where the runner reports none, from Flume's status of the newest place the runner carried. A runner that carried none leaves the folder unread. `launched_at` then tried the kit's other work's places on that host and found none. A place is the place's fact, not where the host keeps the repository. The runner keeps the clones (boomdrive `core.5`), so the folder is the runner's report (`roles.9`).
- **The landing.** crew reads a landed bolt's pieces from its branch (`gather.bolt_landings`, #479), and its branch was gone. Main still held every fact: the landing's second parent is the bolt's head, and that head's line names each piece's place. crew read none of it, since it found the bolt only by its branch.

A landing read run as `chuck@deneb` closed it at 16:43:31Z. A bolt whose places the runner no longer carries, on a host whose runner carries none of its kit's other work, is still closed by nothing of crew's.

## What Changes

- **The kit's folder is the runner's report alone.** Where crew needs a kit's folder on a host, it reads the folder from the `repositories.rec` of the runner that took the work. It never reads it from Flume's status of a place that runner carried, or from its places of the kit's other work. A runner that reports no repositories leaves the kit unread, naming the host and that its runner reports no repositories it keeps (`read.1`). Its stream is still read from a place's status, since the stream is the place's fact.
- **A bolt's landing on main is read from main.** The kit's read finds, on main's first-parent line since the bolt's start, the landing that landed it. That is a commit whose `Sluice-From` names `bolt/<bolt>`, as the agent or the worktree, or whose second parent is a head crew submitted of the bolt, or its branch's head where its branch is read. It is read whether or not the bolt's branch still stands. A landing before the bolt's start builds nothing, since a bolt's name is free again once it lands. Reading sluice's landing commits is a stopgap that record 0062 names, with what retires it (`roles.5`).
- **A landed bolt's pieces are read from its landing.** Once main holds the bolt's landing, its landings are read from that landing's second parent back to its first parent. So each unit, chore and fix whose place's branch is named there reads `merged`, and `landed` once main holds it, whatever the runner carried of its places. The bolt then reads landed, and `crew bolt land` closes it.
- A piece its landing does not name still reads as the runner gives it. A bolt with such a piece is not closed, which is `land_refusal`'s rule today.
- `README.md`, `plugin/skills/crew/SKILL.md` and `crew`'s usage header say where a kit's folder is read and how a landed bolt is read (`docs.2`).

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `drive-state`: "A kit's work is taken by a runner whose configuration names its repository" reads the kit's folder from the runner's report alone.
- `bolt-plan`: adds "A bolt's landing is read from its kit's main" and "A landed bolt's pieces are read from its landing".
- `bolt-teams`: adds "A bolt whose landing main holds closes whatever the runner carried of its places".

## Impact

- `plugin/lib/runner.py`: `kept_folder` gives a reason where the runner reports no repositories. `where` takes no folder from a place's status. `launch_repositories` loses its check for a taker with no folder, which `where` now refuses.
- `plugin/lib/plan.py`:
  - `launched_at` and `kit_at` lose their fallbacks to a place's folder.
  - `runs_at` reads the run record's `bolt.submit` entries.
  - A new decision, `landing_sought`, gives each started bolt's start and the heads crew submitted of it.
  - `stages_for` and `survey` hand that to the kit's read.
  - `Stages.landings` reads a landed bolt's landings from its landing.
- `plugin/lib/gather.py`:
  - A new decision, `main_landing`, finds a bolt's landing on main's first-parent log.
  - `kit` reads that log once per kit, records each asked bolt's landing, and reads a bolt's landings from its landing, its branch standing or not.
  - `bolt_landings` takes the landing.
  - It still imports only the standard library (`code.1`).
- `plugin/bin/crew` (usage header), `README.md`, `plugin/skills/crew/SKILL.md`.
- `tests/lib.sh`: the stub runner writes `repositories.rec` from what each host keeps, and can carry no place of a launch it answered.
- No new stage, key or field reaches the views. A bolt's state `landed` and a piece's `merged` and `landed` are drawn already, so `code.8` is not reached.
- **Outside this repository: Boomdrive's runner must write `repositories.rec`.** This is R2 of the archived change `a-kit-renamed-on-its-host-is-renamed-across-the-plan` (its design, *What this change rests on*), which Boomdrive has not built. At agentplot/boomdrive `c6eb79b`, `boomdrive-crew`'s `write.rs` writes only `runner.rec`, `answers.rec` and `places.rec`. Until the runner writes it, every started bolt on a host whose runner reports no repositories reads unknown, and none lands. So a host's crew takes this change only once that host's runner branches hold `repositories.rec` (design, *After deploy*).

## Touches

```
plugin/lib/runner.py
plugin/lib/plan.py
plugin/lib/gather.py
plugin/bin/crew
README.md
plugin/skills/crew/SKILL.md
tests/lib.sh
tests/py/test_runner.py
tests/py/test_kits.py
tests/py/test_stages.py
tests/py/test_branch_stands.py
tests/py/test_board.py
tests/py/test_main_landing.py
tests/contract/test_gather.py
tests/t-journey-land.sh
```
