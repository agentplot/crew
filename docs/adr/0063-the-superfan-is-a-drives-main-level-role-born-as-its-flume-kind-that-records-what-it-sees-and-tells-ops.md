---
status: proposed
date: 2026-11-08
decision-makers: the user (whether to take it); the research talk the-superfan-watches-the-family-at-work (the shape, from the rules)
---

# 0063. The superfan is a drive's main-level role, born as its Flume kind, that records what it sees and tells ops

Status: proposed on 2026-11-08 by the research talk `the-superfan-watches-the-family-at-work`, until the user has seen it as a record and says yes. That a superfan watches Boomdrive at work is the user's own word. Its shape is the talk's, from the rules, with each path not taken. No unit is queued from it while it is proposed.

Deciders: the user, 2026-11-08: "I'm particularly interested in agent-first usage. I'd like to implement the superfan pattern from Anthropic, where I can have an agent monitoring Boomdrive in action. I think having it connected to a metrics platform would be part of that" (signal `2026-11-08-agentplot-design-8e546268/01`); and, asking for the talk, "Where do you suggest we define this plan for a super fan? It seems like we need some design for it. Maybe start an agent to do some research on the pattern first" (signal `2026-11-09-agentplot-operator-6be799df/01`). The talk, for the rest.

Sources: `openspec/explorations/the-superfan/reading.md` and `proposal.md`; Anthropic Engineering, "Redesigning source control at Anthropic" (2026-10-13), the pattern's one primary source; Ben Congdon, "Agentic Monitoring" (2026-10-19), the spec-and-harness shape; `anthropics/oncall-kit`; rules `roles.1` to `roles.7`, `signals.2`, `signals.5`, `signals.7`, `state.3`; record 0057; Boomdrive record 0033, proposed with this one, for the watch that wakes it.

## Context and problem statement

The user wants an agent watching the family's tools at work, after Anthropic's superfans. Every published shape for doing that at less than Anthropic's token budget has the same two halves. A deterministic program detects. A model is woken only to read what it detected, explain it and suggest what follows. Boomdrive record 0033 proposes the first half, the watch on the runner's pass. This record is the second: who is woken, what it may do, and how what it finds reaches the plan.

## Considered options

- **A main-level role born as its Flume kind, woken by the runner's watch and once a day (chosen).**
- **A standing role beside ops, in herdr.** A standing agent has no clock. Polling would need a loop of crew's that wakes it, which `roles.7` rules out. crew's standing roles each cross to their kind in turn (record 0057).
- **An operator's or ops's added duty.** Ops lands, deploys and fixes main. A watcher with ops's commands can act on what it reads, and what it reads includes text anyone who can push writes. Keeping the reader apart from the actor is the point.
- **A watcher that may act on what it sees**, such as retrying a flaky check, setting a result aside or launching a fix of main. Every act of that kind is a role's, on the user's word (`roles.2`, `state.3`). sluice keeps setting a result aside to "the operator's to do, never a session's".

## Decision outcome

1. **The superfan is a role of the drive's main level, `<label>/superfan`, born as its Flume kind.** Its kind and brief are crew's while crew is the control plane: `plugin/flume/kinds.toml` and `plugin/roles/superfan.md`. It is declared in crew's roles file at its address (record 0057) and is never a standing agent. It is the first role born as its kind, with no standing agent to cross from.
2. **It is woken by Flume, never by crew.** The runner's watch wakes it when a pass took a capture the drive's inbox did not hold, and once a day for an open look (Boomdrive record 0033). Until the watch is built, the user or ops on the user's word wakes it with `flume wake <label>/superfan` (`roles.7`).
3. **It records what it sees, and tells ops of a live system.** It writes a signal with `crew signal` only where it adds what the watch's capture does not say. The signal's excerpt is a tool's output as its session received it, asserted by the tool (`signals.2`, `signals.5`). A false alarm writes no signal; its run's report names the check that misfired and how it would change. For a live system that needs a person, it sends ops a notice naming the signal, by ops's address or, while ops stands, by `crew tell` (`roles.4`, `roles.6`).
4. **It acts on nothing else, and crew enforces that** (`roles.3`). It never:
   - submits, withdraws, retries, holds, drops or stops a place;
   - sets aside a result;
   - launches a fix (`state.3`);
   - writes the plan (`roles.1`, refused for any agent outside the role table);
   - approves or lands anything (`roles.2`);
   - changes a check into effect: a check's change is a signal, and the plan builds it.

   Its kind's settings give its agent only:
   - reading commands;
   - `crew signal`;
   - `crew tell` to ops;
   - `flume needs`.

   Every other family command that acts is denied. Its brief says that everything it reads is data, never instructions.
5. **What it records reaches the plan as every signal does.** Curation runs on the user's word and at the design agent's start (`signals.7`). The superfan never curates its own signals. A cause seen again is one more signal, which curation joins to that cause's item, building its weight.
6. **The first step is its open look, woken by hand.** Its runs record what holds and draft, in their reports, the checks the watch would need. That proves the excerpt path, the curation flow and a look's token cost before anything is automated.

Not taken: the standing role, ops's added duty and an acting watcher, for the reasons above.

## Consequences

- Good: a reader apart from every actor. What the superfan reads cannot make it land, retry or fix anything.
- Good: no tokens are spent finding nothing. Once the watch runs, a run costs only when a new cause stands, and once a day.
- Good: nothing new in crew but a brief, a kind, its roles-file entry and its tests.
- Bad: until millpond keeps the drive's inbox, every watch capture lands as its own signal (`crew signal land` takes no unread capture), so a false alarm still reaches curation, as one signal, and its move is `drop`.
- Bad: the superfan is crew's first role born as its kind, so the kind path is proven on it before the standing roles cross.
- On acceptance, the design agent adds the rule `roles.10` to `docs/architecture/core.md`: "The superfan reads the family's tools and writes only signals and notices to ops; it submits, retries, sets aside, holds, drops, fixes, lands, approves and plans nothing, and its kind's settings deny it every command that would." It rules out an acting watcher and a superfan on ops's commands. The brief, the kind and their tests are a change of crew's, queued from this record once it is accepted.
