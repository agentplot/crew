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
- crew still calls sluice directly in four other places, each against point 1:
  - its plan's reads of a landing (`plan.py`, a `sluice ... --json` run in a kit's main);
  - its gather of a kit (`gather.py`);
  - the board's watch of `sluice overview`;
  - a card's preview, which `crew card preview` brings up and puts away with `sluice preview` and reads with `sluice previews` on the work's host, and which crew offers on a row by reading `[preview]` in the kit's `.config/sluice.toml`.

  The first three move onto the runner's report by one crew unit, with a Boomdrive unit first wherever the report must carry what crew needs. Previews move as below.
- **Previews go through the runner (agentplot-design's choice, 2026-11-08, on point 1).** What the user sees on a card stays as it is: a row or a batch line says whether its work has a preview, the preview comes up when the user asks on the card, the card lists its addresses while it is up, and it goes when they are done or the row ends. Only the way it is brought up changes:
  - crew posts a message, `preview`, naming the repository, the branch and the revision, and the same message marked `done` to put it away. Like `land`, it is named for what it does, not by sluice's word.
  - A runner that keeps the repository, on the host where the work runs, carries it out through sluice's own preview command, once, and reports sluice's answer as sluice gave it: its addresses and its state, or its refusal.
  - crew reads whether a kit has a preview, and each preview's addresses, from the runner's report alone. Where the report cannot yet say whether a kit declares one, the row offers it, and a kit that declares none answers in sluice's words.
  - crew puts away only previews it asked for, and the runner only what its control plane asked it to bring up; a person's own preview is left alone.
  - Not taken: crew keeping its own preview calls until a later change, since it would go on calling sluice against point 1; and dropping previews from the cards, which the user relies on for swancloud's and switchboard-kit's bolts.
  - This is one Boomdrive unit, then one crew unit. The hosted protocol carries `preview` in a later version of its own, as it will `land`.

## Amendment of 2026-11-12: a bolt started before bolts were base places is landed by hand, once

Status: proposed to the user on 2026-11-12, as `briefs.15` has it; accepted only on their yes. Rules of the user's decided it between two paths, and its card names the other.

Deciders: the user, asking for it on 2026-11-12 in agentplot-ops's pane: "we need to figure this out and get transitioned." The way is decided by blueprints principle 12, from the user's words of 2026-11-08 ("I want the system to be built the way it should be and then have agents fucking fix the data transition as necessary"), and by Flume's clause 3. agentplot-design for the record.

### Context

Point 7 had each host land as before until it ran the release that carries this record. crew's change for it said a host's pin moves only once `crew bolts` names no bolt started before that release. Deneb's pin moved first. On 2026-11-12 every started bolt there had no base place: 13 of boomdrive's and 5 of sluice's. 8 of boomdrive's and 2 of sluice's were green, each at a head `crew bolts` names. crew posts no `land` for such a bolt, and Flume refuses to open a base place over a branch already present (Flume 3 and 205). So no send of the user's lands any of them.

### Decision

- **A hand step, once.** Each such bolt lands as the crew that started it landed bolts. Main-level ops submits the bolt's branch to main through sluice, on the user's word naming that bolt, at the green head `crew bolts` names (`state.3`). It moves data from the old shape to the new by hand, as principle 12 asks. Nothing in crew, Flume or Boomdrive is written for it.
- **What must hold.**
  - No bolt is submitted at a head other than the one `crew bolts` reads green, or before the user's word names it.
  - No worktree is made on `bolt/<bolt>` (`plan.18`).
  - No bolt with a base place lands this way.
  - ops records nothing in crew's plan for it. crew reads each such bolt landed from GitHub's main and closes it (record 0062 as amended 2026-11-12).
  - A submission that fails or conflicts gets a fix place on the bolt's branch, as any fix on such a bolt, and lands only on the user's word again.
- **The bolts still active.** Each finishes and lands the same way, or the planner drops it and plans what is left into a bolt that is a base place.
- **When it ends.** Once `crew bolts` names no bolt started before this release on any host whose main level runs it. No code goes with it, so nothing retires.
- **Not taken.**
  - Flume opening a base place over a branch its merge queue already lands on, with crew launching one for each such bolt. It is the planner's and ops's choice. It has Flume adopt a branch it did not make, which Flume's clause 3 rules out. It is a unit written for one move, which principle 12 rules out. It would also be code in flume and crew during the code pause of 2026-11-12.
  - A new bolt for each, made by Flume, with one place that takes in the old branch. Every bolt's checks would run twice, with an agent's merge between, for a move the hand step makes at once.

### Consequences

- Departs from point 5, "No agent and no crew command runs a landing", for bolts started before this release alone, as point 7 had them land as before.
