# Every plan write is an act with its entry

## Why

On 2026-11-07 at 17:46:34Z, swb-2-conductor's write on `wldn/main` of WilldanGroup/crew-state, 16f19a887, "plan(production-stands-stage-in-devs-account): the-copy-acting-for-a-class-is-one-declared-value constructed again, its mark cleared (swb-2-conductor)", named `Crew-Entry: 20261107T174633Z-983370-chuck-herdr-alpha-2601180-2`, an entry no run record on the branch holds. The same process's `-1`, its `stage.end` at 17:46:23Z, is held. A decision reads the branch at the parent of the oldest commit whose entry has not arrived (`read.5`), so every decision after it read the branch below it until it passed out of the newest twenty commits, about 18:02:50Z. Proposal 1010 was written after it (e0d5a954b, 17:47:23Z), so `crew plan answer 1010` and `crew plan proposed 1010` answered "no proposal 1010 in wldn/main" while `proposals.rec` held it open, and `crew plan proposed` listed 1009 after its approval at 18:01:26Z (18883a31f). Read from deneb later, crew lists 1010 open and 1009 closed. It is the third instance on wldn, after 39b5020fd and 220d7dfa9 on 2026-11-02 (signals 2026-11-02-wldn-planner-cb63bbdd/01 and 2026-11-02-wldn-planner-e3640241/01 on wldn/main; 2026-11-07-agentplot-planner-5c388333/01 on agentplot/main of afterthought/crew-state).

`plan.write` names a `Crew-Entry` in every commit it makes and writes that entry only when it is given an act. Three writes give none: the give of a bolt (`plan.py` 1978 at 361bd1dd), whose `bolt.give` entry is written apart after the write's own output; a unit marked amended so its construct runs again (8870), whose commit's entry was meant to be the construct's `stage.start`, written only once the stage's agent took its prompt and never when it did not; and a unit constructed again with its mark cleared (10839), whose entry nothing writes. `plan.2` holds that every commit names its entry, and the design agent ruled on 2026-11-02 one crew chore to build it, `every-plan-write-is-an-act-with-its-entry`, queued in swancloud/main's plan and never built. This fix builds that ruling on crew's main line, which wldn's host runs (crew 0.41.4 on chuck-herdr-alpha).

## What Changes

- **The three writes are acts.** The give writes its `bolt.give` entry as the write's own act, so a give comes to one entry. A unit marked amended is a `unit.mark` write naming the unit, its bolt and the head construct starts again from; the construct's `stage.start` still says it marked the unit and names the mark's commit, under an id of its own. A mark cleared once that construct delivered is a `unit.unmark` write naming the unit, its construct stage, its bolt and the mark it cleared.
- **A write names its act or writes nothing.** `plan.write` refuses a write given no act, before it reads or pushes anything, since its commit would name an entry nothing writes.
- **A write leaves the branch whole.** Once a write returns, its entry's commit follows its own on the branch, so no decision after it reads below it. A contract case holds this on a real repository, and a logic case holds every write in `plan.py` to naming its act.
- **A read below the tip says so.** A command that read the branch below its tip says, on the line before its refusal and on standard error after its answer, the commit it read at, the tip, the write it waits on and that write's agent, so "no proposal 1010 in wldn/main" read there is never taken for a branch holding none.
- Unchanged: `decision_at`, `read_point` and their window of the newest twenty first-parent commits; an act is read whole or not at all (`read.5`).

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `drive-state`: "A commit names its run-record entry" holds every plan write to being an act whose entry it records before it returns, and refuses one with no act; "A decision reads an act whole and says when it read below the tip" is new.

## Impact

- `plugin/lib/plan.py`: `unacted` and `write`; `bolt_give`; `mark_amended`, `run_check`, `chore_check`, `run_unit_stage`; `unmark`; `entry_held`, `in_flight`, `decision_at` (unchanged in what it answers), `waited_on`, `writer_of`, `below_said`; `read_point`, which keeps the write it waits on; `fetch`; `Reading.keep_below` and `Reading.below`; `below_read` at the entry point.
- `plugin/lib/record.py`: the `Head` of a `unit.mark` and a `unit.unmark` among the fields; the entry point says a read below the tip.
- `README.md`, `plugin/skills/crew/SKILL.md`, `plugin/bin/crew`'s usage header (`docs.2`).
- `docs/architecture/plan.md`: `plan.2`'s details read 2026-11-07 and say the ruling of 2026-11-02 is built.
- Tests: `tests/py/test_in_flight.py`, `tests/contract/test_record.py`, `tests/contract/test_recfix.py` (its give now names its act), `tests/t-journey-plan.sh`, `tests/t-journey-prompts.sh`.
- Nothing crew models changes, so neither `board.agent_views` nor the mod does (`code.8` not reached). Nothing outside the standard library is imported (`code.1`).
- On `teamless/deneb`, carried by `teamless-deneb-takes-crews-main-in` for main to take that line's code: none of the three writes is there, the team machinery having left it, and every write names its act already, so it carries `unacted` and `write`'s record of its entry, the read below the tip said, its tests and docs, and `plan.2`'s reading; `flywheel-state` is `drive-state` there, and `run-record`'s construct scenario, `record.py`'s `Head` of a `unit.mark`, the three writes and `t-journey-prompts` are main's alone.

## Touches

```
plugin/lib/plan.py
plugin/lib/record.py
plugin/bin/crew
README.md
plugin/skills/crew/SKILL.md
docs/architecture/plan.md
tests/py/test_in_flight.py
tests/contract/test_record.py
tests/contract/test_recfix.py
tests/t-journey-plan.sh
tests/t-journey-prompts.sh
```
