---
status: accepted
date: 2026-11-11
decision-makers: afterthought-design
---

# 0066. The design pages have one writer, and a unit's change never edits them

Status: accepted on 2026-11-11 by afterthought-design. It is the design agent's own choice, made on the rules and records written and cheap to change later (`briefs.15`). It settles `docs.7`, proposed on 2026-10-11 and left without an answer since.

Deciders: afterthought-design, on `docs.7` as proposed on 2026-10-11 (commit f77e41a1) and on main's log since record 0053 took the open-items page away.

Sources: signal 2026-10-11-swancloud-ops-3755d04a/01; records 0053 and 0025; rules `docs.4`, `docs.5`, `plan.8`, `state.3`, `briefs.15`.

## Context and problem statement

`docs.7` was proposed after the open-items page stopped six landings in three days: each bolt took its own item off the page while the design agent edited the same page on main. Record 0053 then removed the open-items page, which ended those particular conflicts. The question the rule asks is still open, though. Should a unit's change edit the rule pages and the records?

Main's log since 2026-11-04 says it still happens. Changes and fixes built on bolts have rewritten rule details as built. Meanwhile the design agent amends the same pages on main through sluice, carrying each record's amendment and each rule's not-built clause. Two writers of one page make a merge conflict on whichever lands second. They also leave two readings of one rule: the one the unit wrote from its task, and the one the design agent wrote from the decision.

## Considered options

1. **One writer (chosen).** The design agent alone writes `docs/architecture/` and `docs/adr/` on main. A unit's change never edits them. What a landing builds leaves a rule's not-built clause by the design agent's hand, read from main's log after the landing. A carrying fix that conflicts there takes main's side.
2. **Withdraw `docs.7`.** Record 0053 ended the conflicts the rule was written for, and sluice already refuses a submission that conflicts with main. Not taken: a refused submission costs a round trip to the bolt's team. A unit's rewrite that merges cleanly is worse, because it changes a rule's wording with no decision behind it, which `docs.5` and `briefs.15` rule out.
3. **One file per open item under `docs/architecture/open/`.** This was considered in `docs.7`'s details. It is moot now that record 0053 keeps no file of open items.

## Decision outcome

Option 1. `docs.7` stands as written and is accepted, with this record as its source.

- A unit's change may still edit README, the briefs, the skills and the specs, as `docs.2` and `docs.4` have it. A spec still reaches `openspec/specs/` only with the build.
- The design agent reads what a landing built from main's log and amends the rule's not-built clause after it. Nothing waits on a unit to do that.

### Consequences

- A unit, `a-unit-never-edits-the-design-pages`, makes the rule hold: a unit's change that touches either folder is refused before it lands, and the words a unit's construct is given say so.
