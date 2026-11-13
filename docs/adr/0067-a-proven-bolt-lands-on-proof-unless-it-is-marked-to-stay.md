---
status: accepted
date: 2026-11-12
decision-makers: the user (a proven bolt lands on proof unless marked to stay); agentplot-design (the record, and the choices marked as its own)
---

# 0067. A proven bolt lands on proof, unless it is marked to stay

Status: accepted by the user on 2026-11-12, on their card.

Deciders: the user, on wldn's card `req_be80263b` on 2026-11-12, relayed by wldn-planner through agentplot-operator: "I think, yes, we could make this change because 99% of the time that's what we want. I think we want to send an upstream request to Crew as a new feature, though, because I think a bolt should be marked (or maybe it's on an upstream Crew feature). I don't know. I'm going to say a bolt. There might be some bolts that we want to stick around for a while because we are working on that bolt, testing it in a test environment, and adding new stuff even after it's "done." We're just adding new feedback. I think that's an explicit decision, though: we would assign it to the bolt ahead of time so we knew. In those cases they don't land automatically but for all the other ones they would". agentplot-design for the record, and for the choices marked as its own.

Sources: record 0031, the landings card; record 0056, the user's send as the one message `land`; `plan.16`; `briefs.11` and `briefs.12`; `state.3`; wldn-ops's reading of switchboard-kit's landings since 2026-11-06, where bolts proven overnight waited 400 to 1,055 minutes for a landings card and the user's send.

## Context and problem statement

A bolt lands only on the user's send on its kit's landings card (`plan.16`, record 0056 point 3). A bolt proven at night waits for the morning, though its every unit's change has already been in a batch the user answered (`briefs.12`). The user wants that to be the rare case, chosen ahead of time for a bolt they keep working on.

## Decision outcome

- **A proven bolt lands on proof.** Once a bolt is proven, crew posts its `land` itself, at once, at any hour. Proven means verification green at its head, a forecast clear of what main has landed, and every unit's latest change in a batch the user answered. The runner carries it out as it carries a send's (record 0056). This is the user's decision.
- **A bolt marked to stay waits for the send.** A bolt can be marked, when it is planned or started, as one that stays unlanded while it is tested and added to. A marked bolt is offered on its kit's landings card and lands only on the user's send, as today. The mark is set ahead of time, never after the bolt is proven. This is the user's decision.
- **The landings card tells, and asks only for marked bolts.** A bolt that landed on proof reaches the user as a heads-up naming it and its landing, with nothing to answer. The card asks only about marked bolts. agentplot-design's choice.
- **The mark is the plan's, set by whoever plans or starts the bolt on the user's word, and the user can lift it.** Once lifted, the bolt lands on its next proof. agentplot-design's choice.
- **Every drive, the same.** Landing on proof is crew's behavior for every drive, with no setting to turn it off. A drive that wants a send marks its bolts. agentplot-design's choice, from the user's "99% of the time that's what we want".
- **What still holds a proven bolt:** a hold the user put on the drive or the kit, such as a code pause. crew posts no `land` while it stands. agentplot-design's choice.

### Not taken

- A drive setting choosing between landing on proof and on the send: the user put the choice on the bolt, not the drive.
- Landing on proof while a unit's latest change waits for a batch: the batch the user answers stays the one place they review the work (`briefs.12`).

### Consequences

- `plan.16`, `briefs.11` and `state.3` are amended when this is accepted, as is record 0056's point 3, so that the user's send lands a marked bolt and proof lands the rest.
