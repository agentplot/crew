---
status: accepted
date: 2026-11-08
decision-makers: the user (the stopgap); agentplot-design (the record)
---

# 0062. crew reads a piece's landing from GitHub's landing commits as a stopgap, until the runner reports each place's end

Status: accepted by the user on 2026-11-08, on their card ("Should crew keep telling a piece landed from GitHub for now, until Boomdrive's runner reports each piece's end?", answered "Keep them as a named stopgap until the runner reports each end").

Deciders: the user, on that card, choosing the stopgap. agentplot-design for the record.

Sources: `roles.5`, under which crew changes only by a removal, a reading, or a stopgap named in the record that calls for it with the move that retires it; `roles.9`, under which the runner carries Flume's ends back to the control plane; record 0056 as amended 2026-11-08 (proposed), under which crew knows Flume and sluice only through the runner's report; agentplot/boomdrive's work-into-flume, "A place the listing no longer holds keeps its last status".

## Context and problem statement

When Flume tidies a finished place, the runner keeps only the last status it carried, so a piece that landed reads as submitted. crew reads it so, and its row is dropped by hand. Three readings of crew's tell such a piece landed from what GitHub holds instead: a landing commit's `Sluice-From` naming the piece's branch on its bolt's first-parent line, or a bolt's on main. They are a unit or chore read as merged (crew #479), `a-bolts-landed-fix-reads-merged` and `a-bolts-landing-on-main-reads-landed`. Each reads sluice's landing commits directly, outside the control-plane contract.

## Decision outcome

- **The stopgap.** crew keeps those three readings: a piece, a fix or a bolt reads landed once a landing commit on its base, as GitHub holds it, names its branch in `Sluice-From`. This is the user's choice.
- **What retires it.** The readings go in the change that follows the Boomdrive unit `the-runner-carries-each-places-end` onto every host crew serves. That unit has the runner carry each place's end, landed, failed, refused or dropped, to the control plane's report before Flume tidies the place. From then on crew reads every piece's end from the runner's report alone.
- **Not taken.** Taking the readings out now and waiting for the runner. The hand-drops would go on until the Boomdrive change lands.
