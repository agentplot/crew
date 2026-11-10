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

## Amendment of 2026-11-10: a bolt's head that sluice landed passed (proposed)

Status: proposed on 2026-11-10 by the code stage of the fix `main--a-passed-landings-head-is-verified`, on agentplot-design's signal 2026-11-09-agentplot-design-9b1ec2dd/01, "sluice green at the head should read as verified whoever submitted it", which the fix's brief carries: "A head that is a sluice landing whose result passed is verified, whoever submitted it."

### Context

The three readings above went with `crew-reads-each-pieces-end-from-the-runners-report` (crew 0.49). Since then a bolt's verification is green only where its head is a piece's landing as the runner reports it. A landing on the bolt that is no piece crew launched, such as a design agent's record or a record's fix landed straight onto the bolt, leaves the head no such landing, so the bolt reaches no landings card. Six bolts were held 15 to 21 hours on 2026-11-09/10 this way, boomdrive's `bolt/the-runner-confirms-the-ends-it-carries` among them, at `8df8e1d`, sluice's #70 of record 0030's fix, `Sluice-Result: passed (3 run, 0 replayed)`. The runner's report carries no verdict for a bolt's head: Flume's status of a base place names its head and nothing of the landing at it.

### Decision

- **A second stopgap.** A bolt's head that is no landing of its work the runner reports reads verified where it is a landing sluice made on the bolt itself, the newest commit of the bolt's own first-parent line beyond main, whose commit names one verdict, its `Sluice-Result`, reading passed, whoever submitted it. crew reads that head's `Sluice-Submission` and `Sluice-Result` trailers by git, where it already reads the head, reads nothing of sluice's records and runs no sluice. sluice's clause 23 makes a landing commit's trailers the lasting record of the verdict it landed on, and has a landing beside its queue read passed. Flume reads the same trailers for a place's landing (its read-submission).
- **A piece's end stays the runner's report's.** The head's verdict says the head passed its checks, not whose work it is: no piece reads merged or landed from it, and a bolt with a piece not yet merged as the runner reports it is not offered for landing, whatever its head reads.
- **What retires it.** The change that follows the runner's report carrying each bolt's head with the verdict sluice landed it on, through Flume's status of the bolt's base place, onto every host crew serves. crew then reads the head's verdict there, and this reading goes. Flume and Boomdrive build that report; neither is changed here.
- **Not taken.**
  - Reading every commit on the bolt's own line as passed because sluice is the one writer of `bolt/*` on GitHub: a bolt kept on its host has no such ruleset, and the verification's words could name no verdict.
  - Waiting for the runner's report: the bolts would wait on hand-landings meanwhile.
  - Reading `Sluice-From` again, for whose work the head is: the pieces' ends stay the runner's alone.

### Consequences

- Departs from record 0056 point 4 ("What the report does not carry, crew does not read anywhere else") as `roles.5` allows a stopgap: named here with the move that retires it.
- merge-gate's "crew SHALL read no `Sluice-Result` or `Sluice-From` trailer" changes by `a-passed-landings-head-is-verified`, and `tests.5` is amended in the same commit as this amendment.
- Built in `gather.head_landing`, `runner.verification` and `runner.passed_landing`.
