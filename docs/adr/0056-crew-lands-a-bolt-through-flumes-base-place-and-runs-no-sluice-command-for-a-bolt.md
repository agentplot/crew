---
status: accepted
date: 2026-11-07
decision-makers: the user (crew no longer submits to sluice); the design agent (what crew asks of Flume and reads from it)
---

# 0056. crew lands a bolt through Flume's base place, and runs no sluice command for a bolt

Status: accepted by the user on 2026-11-07, in agentplot-design's pane: "For 56, yes."

Deciders: the user, 2026-11-07, in agentplot-design's pane, after a bolt's landing card had agentplot-ops run `sluice submit` by hand, relayed by agentplot-design through the operator: "I want to make sure that the changes required to retrofit crew are part of all of that because crew would no longer have to be submitting to sluice". That crew stops submitting to sluice is theirs. What crew asks of Flume in its place, and what it reads, is the design agent's, on Flume's statement as written.

Amends the rules `plan.8` and `plan.19`, each from the release that carries the unit below; `state.5` stands as written, since crew still pushes only to its state branch. Sources: agentplot/blueprints `design/flume/requirements.md` 202 to 204 (a bolt's branch is a base place: Flume asks the merge queue to make it at launch, places are cut from it and land on it, and it is submitted only on its caller's retry naming the submission, the outcome read from the merge queue and delivered to its recipients); agentplot/sluice record 0093 (sluice starts its own host process when work arrives, so nothing waits on a driver); agentplot-design's message of 2026-11-07.

## Context and problem statement

crew makes a bolt's branch with sluice's `branch create`, lands it with `crew bolt submit`, a `sluice submit` of the branch to main, waits on it with `sluice wait`, reads missed outcomes with `sluice inbox`, and ends the branch with `branch delete` (`plan.8`, `plan.19`). Flume now carries a branch that work lands on, and that lands on another, as a base place: it makes the branch through the merge queue, cuts the units' places from it, and submits it on its caller's word. Two tools each driving the same branch's landing is how a landing card ended with an operator running `sluice submit` by hand.

## Decision

1. **The user's: crew runs no sluice command for a bolt.** It makes no bolt branch, submits none, waits on none, reads no sluice inbox for one and deletes none. Flume does each through the merge queue.
2. **A bolt is a base place of Flume's.** Its launch, on main, makes its branch; every unit, chore and fix of the bolt is a place whose base is the bolt's branch. crew reads the bolt's head, its places and its submission from Flume, never from sluice.
3. **A bolt lands on the user's send by Flume's submission of its base place.** Main-level ops's landing asks Flume to submit the bolt's base place (a retry naming the submission), and crew reads the landing, a failure or a conflict from what Flume delivers and holds. A conflict is mended as Flume's statement has it: a place on the bolt takes main in, then the submission is asked again. A landing card, its send and its close follow Flume's outcome alone.
4. **Until the release that carries this, crew lands as it does today.** Nothing in this record is true of a host before its crew carries the unit. That unit is ordered after a Flume release with base places.

## Considered options

- **Flume's base place lands the bolt, crew asks and reads (chosen).**
- **crew keeps submitting the bolt to sluice beside Flume's places.** Not taken: the user's words; and two tools driving one landing is the defect that brought it.
- **crew drives sluice through Flume's places alone, making the bolt's branch itself.** Not taken: the branch would still be crew's sluice command, and Flume's base place already makes it.

## Consequences

- One crew unit, on the user's yes and after the Flume release: `crew bolt submit` and its land path, and main-level ops's landing steps, ask Flume and read Flume, with no sluice command for a bolt (swancloud-planner names it `crew-lands-a-bolt-through-flumes-base-place`).
- Boomdrive's runner carries a bolt as a launch (agentplot/boomdrive's unit `a-bolt-is-a-launch`), so crew's launch of a bolt reaches Flume as any work does.

## Amendment of 2026-11-08: crew is the control plane, and a bolt lands by the runner alone

crew reaches Flume and sluice for a bolt only as the control plane, through the Boomdrive runner: it offers the bolt as a launch and the user's send as an act on it, it reads the runner's report, and no role runs a landing. Status: proposed to the user on 2026-11-08, as `briefs.15` has it; accepted only on their yes.

Deciders: the user, 2026-11-08, first declining proposal 62 (`crew-lands-each-bolt-by-name`), as agentplot-planner relayed it (signal 2026-11-08-agentplot-planner-9cdb51ff/01-crew-lands-nothing): "It's not crew's job to land anymore. That's the whole point of the runner in Flume and sluice. Crew no longer is responsible for landing itself. I guess I'm thinking about how the control plane would work. It is going to be a decision in the user's rail to land, so that's a message for a Flume place, theoretically." Then, sending an earlier draft of this amendment back on its card: "But crew is like the control plane. It doesn't talk to Flume. Remember, the Boom Drive runner is pulling from the control plane. Everything has to happen from the Boom Drive runner. There can be messages back and forth with the control plane but crew doesn't know about Flume directly except for whatever the control plane contract allows." agentplot-design for writing it here, and for the choices marked as its own.

Decisions 2 and 3 above are replaced by these:

1. **crew is the control plane, and only that.** crew reaches Flume and sluice only through the Boomdrive runner, by the control-plane contract. It offers launches and acts, which the runner pulls, and it reads the runner's report: its answers and the statuses it carries. crew calls neither Flume nor sluice, reads neither one's records or files, and names neither in what it decides (`roles.9`; agentplot/boomdrive's control-plane interface).
2. **A bolt is a launch, and the user's send is an act on it.** crew offers a bolt as a launch of a kind that lands with no stages, as any work is offered (agentplot/boomdrive's work-into-flume, "A bolt is a launch"). The user's send on the bolt's row of the kit's landings card is the act crew offers on that launch: a retry of its submission, once for each row the send ticked (the same spec, "A bolt's send is a retry of its submission"). The runner pulls the act and carries it out, and the bolt lands by what the runner runs. This is how crew already offers the user's send of a red main's fix.
3. **No role runs a landing.** Main-level ops asks for nothing at a landing, crew runs no landing command, and crew makes no worktree on a bolt's branch. `crew bolt submit` and `crew bolt land` leave the landing's way.
4. **What crew knows of a bolt is the runner's report.** A bolt's head, its pieces, its submission's outcome, a failure, a conflict and a landing fix are whatever the runner's report carries, and crew closes each row on that report. What the report does not carry, crew does not read from another tool: either the contract carries it, or crew does without.
5. **agentplot-design's choices.**
   - The send's acts are offered in the plan's order and answered one by one. A row whose act the runner refuses keeps its box with the answer's words, and the rest go. The "all or none" of `plan.16` goes.
   - A drive's own control plane, once it replaces crew's (`roles.9`), offers the same act from the same send.

Consequences:

- Rules `plan.8`, `plan.16` and `plan.19` are amended to match, each marked proposed.
- The unit `crew-lands-each-bolt-through-flumes-base-place` builds points 2 to 4.
- crew still calls sluice in three other places, each a departure from point 1:
  - its plan's reads of a landing, a `sluice ... --json` run in a kit's main (`plan.py`);
  - its gather of a kit (`gather.py`);
  - the board's watch of `sluice overview`.

  Each moves onto the runner's report by a unit of its own, queued on the user's yes, with a Boomdrive unit first wherever the contract must carry what crew needs.
- Until the release that carries them, crew lands as it does today (decision 4 above).
