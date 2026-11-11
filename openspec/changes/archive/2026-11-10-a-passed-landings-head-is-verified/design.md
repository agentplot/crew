# Design: a passed landing's head is verified

## Context

`runner.verification` reads a bolt green only where its head is a piece's landing as the runner reports it (record 0056 point 4; the change `crew-reads-each-pieces-end-from-the-runners-report`). The runner's report carries no verdict for a bolt's head: Flume's status of a base place names its head and nothing of the landing at it. sluice writes every landing as a commit naming the submission and the verdict it landed on, and lands nothing whose required checks did not pass, a landing beside its queue reading passed with nothing run (sluice clause 23). Flume reads those trailers for a place's landing (its read-submission).

## Decisions

1. **Read the head's verdict from its commit, as a stopgap.** gather reads, by git, the head's `Sluice-Submission` and `Sluice-Result` trailers, where it already reads the head, and nothing of sluice's records; crew runs no sluice. This departs from record 0056 point 4, as `roles.5` allows a stopgap named with the move that retires it: record 0062's amendment of 2026-11-10 names it, retired once the runner's report carries a bolt's head with its verdict. `tests.5` is amended with it. Not taken: reading every commit of the bolt's own line as passed because sluice is the one writer of `bolt/*` on GitHub, since a bolt kept on its host has no ruleset and the words could name no verdict; waiting for the runner's report, which would leave the held bolts to hand-landings.
2. **Only a landing on the bolt itself.** The head counts only as the newest commit of the bolt's first-parent line beyond main (`bolt_lines`), so a bolt standing where main holds it, main's tip itself a passed landing, reads none. A line git can't list is said, the verification unknown (`read.1`).
3. **The decision is runner's, on plain facts (`code.7`).** gather hands the trailer values raw; `runner.passed_landing` reads exactly one `Sluice-Result` whose first word is `passed` as sluice's passed landing, naming its one numeric `Sluice-Submission`; anything else is no such landing (`read.2`). A piece's landing at the head is named first, so its words stay "as the runner reports it".
4. **A piece's end is untouched.** The head's verdict proves the head, not whose work it is: no piece reads merged from it, and `landing_unready` and `bolt_state` still need every unit and chore merged as the runner reports it.
5. **What carries the fact.** `Stages.verification(bolt, head, landing)` takes the bolt's `head_landing` beside its head at each of its four callers, so `crew bolts`, the rail's landing row, the landings card's readiness and `bolt_state` read alike.

## Risks

- A landing commit whose `Sluice-Result` sluice words otherwise in a later version reads none until crew reads the new form; read as no landing, never as green (`read.1`).
