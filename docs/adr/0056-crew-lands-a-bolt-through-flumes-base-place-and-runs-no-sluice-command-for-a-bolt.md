---
status: accepted
date: 2026-11-07
decision-makers: the user (crew lands nothing and talks only to the runner); agentplot-design (the record, and the choices marked as its own)
---

# 0056. crew lands nothing: the user's send is one message to the runner, "land this bolt"

Status: accepted by the user on 2026-11-07, in agentplot-design's pane: "For 56, yes." Rewritten on 2026-11-08 on the user's words below, and accepted by the user that day on their card ("Is this what you mean for landing a bolt? Crew only talks to Boomdrive's runner, never to Flume or sluice", answered "Yes, that's it. Rewrite the record that way").

Deciders: the user. On 2026-11-07: "I want to make sure that the changes required to retrofit crew are part of all of that because crew would no longer have to be submitting to sluice". On 2026-11-08, declining proposal 62, `crew-lands-each-bolt-by-name` (signal 2026-11-08-agentplot-planner-9cdb51ff/01-crew-lands-nothing): "It's not crew's job to land anymore. That's the whole point of the runner in Flume and sluice. Crew no longer is responsible for landing itself. I guess I'm thinking about how the control plane would work. It is going to be a decision in the user's rail to land, so that's a message for a Flume place, theoretically." And on this record's card the same day: "But crew is like the control plane. It doesn't talk to Flume. Remember, the Boom Drive runner is pulling from the control plane. Everything has to happen from the Boom Drive runner. There can be messages back and forth with the control plane but crew doesn't know about Flume directly except for whatever the control plane contract allows." agentplot-design for the record, and for the choices marked as its own.

Amends the rules `plan.8`, `plan.16` and `plan.19`. Sources: `roles.9`; agentplot/boomdrive's control-plane interface, crew control plane and work-into-flume specs; record 0062.

## Context and problem statement

Today crew makes a bolt's branch with sluice's `branch create`. It lands the bolt with `crew bolt submit`, a `sluice submit` from a worktree on the bolt's branch, waits with `sluice wait`, reads `sluice inbox`, and deletes the branch (`plan.8`, `plan.19`). Main-level ops runs that landing on the user's send (`plan.16`). So crew talks to sluice directly, an agent runs every landing, and a landing fails whenever another folder holds the bolt's branch.

## Decision

1. **crew is the control plane, and talks only to Boomdrive's runner.** crew never calls Flume or sluice, reads neither one's records or files, and names neither in what it decides. It posts messages the runner pulls, and it reads the runner's report (`roles.9`; agentplot/boomdrive's control-plane interface).
2. **A bolt is work crew hands the runner,** as it hands any work (agentplot/boomdrive's work-into-flume, "A bolt is a launch"). The bolt's branch is made, its pieces land on it, and it lands on main, all by what the runner runs.
3. **The user's send is one message: land this bolt.** When the user sends a bolt's row on the kit's landings card, crew posts one message for it, "land this bolt", once for each row sent. The runner picks it up and gets Flume and sluice to land the bolt. A red main's fix is sent the same way.
4. **crew learns what happened only from the runner's report.** Landed, failed, or a conflict and its fix: crew reads it there and closes the row on it. What the report does not carry, crew does not read anywhere else. Record 0062 names the one stopgap, and what retires it.
5. **Nothing of crew's lands anything.** No agent and no crew command runs a landing. Main-level ops asks for nothing at a landing, `crew bolt submit` and `crew bolt land` leave the landing's way, and no worktree is made on a bolt's branch.
6. **agentplot-design's choices.**
   - The message is named `land`, in crew's requests and in the runner's list of messages, for a bolt and a fix alike. Today's name for it, a retry of the submission, is Flume's word, and it goes.
   - Each row's message is posted in the plan's order and answered on its own. A row the runner refuses keeps its box, with the runner's words, and the rest go. The "all or none" of `plan.16` goes.
   - A drive's own control plane, once it replaces crew's (`roles.9`), posts the same message from the same send.
7. **Until the release that carries this, crew lands as it does today.**

## Considered options

- **crew posts "land this bolt" to the runner, and the runner has Flume and sluice land it (chosen).** This is the user's design.
- **crew asks Flume to submit the bolt.** Not taken: crew would talk to Flume, which the user ruled out.
- **crew keeps submitting the bolt to sluice.** Not taken: the user's words, and two tools driving one landing.

## Consequences

- Rules `plan.8`, `plan.16` and `plan.19` are amended to match.
- crew's unit `crew-lands-each-bolt-through-flumes-base-place` builds points 1 to 5 for a bolt, and posts `land`.
- Boomdrive's runner takes `land` as the message for a work's landing, and carries it out as Flume's retry of the work's submission. That is a Boomdrive unit.
- crew still calls sluice directly in three other places, each against point 1:
  - its plan's reads of a landing (`plan.py`, a `sluice ... --json` run in a kit's main);
  - its gather of a kit (`gather.py`);
  - the board's watch of `sluice overview`.

  They move onto the runner's report by one crew unit, with a Boomdrive unit first wherever the report must carry what crew needs.
