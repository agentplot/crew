---
status: accepted
date: 2026-11-07
decision-makers: the user (swancloud record 0038, what must be true); the code stage of the fix an-offer-card-shows-the-step-the-deploy-waits-on-first (how crew builds its side)
---

# 0059. A step the deploy waits on is a box on its offer card, tied to the deployer's record of it by its words

Status: the decision is the user's, swancloud record 0038, accepted on its card on 2026-10-26 (req_73b52dae13894077a094, "Approved"); its consequences name this crew chore. The choices below are the code stage's, made from record 0038, crew's rules and the deployer as it stands, each cheap to change; none is the user's alone.

Deciders: the user, for what must be true: a design may list a step of the user's the deploy waits on; the deployer hands it to the offer card first; the user's word is given only once each is ticked, so the card's yes with a step unticked is not the word. The code stage, 2026-11-07, for the card's form, how crew ties the card's box to the step the deployer records, and what of it crew keeps.

Amends: `plan.14`'s details. Relies on `read.1`, `code.7`, `roles.2`, `roles.3`, `record.3` and record 0031 §1, §3 and §5. Sources: swancloud record 0038; swancloud's archived change `a-step-the-deploy-waits-on-stands-on-the-offer-card` (its design's Decisions 1 to 4); swancloud `packages/swancloud-deployer/after-deploy.awk` (a waited-on step prints `before` in its when column, the user's alone, naming its environments), `deployer.sh` `offer_steps`, `offer_deploy`, `waited_steps`, `record_waited` and `held_on_steps` (read at swancloud 49469fba): the steps file puts waited-on steps first; after the offer the deployer records each as `crew ops step <env> --to <offered> --key <sha256 of user, before and its compared words> --state waiting --doer user --text <file>`, with no mark; it holds a word until crew reports each such key done in `crew ops steps --json`.

## Context and problem statement

swancloud's deployer already hands a waited-on step to `crew ops offer` in the shape record 0038 names, `before` among the when words of its steps line, and records it on the deploy as a user's step. crew showed it among the after-deploy steps, took the user's hold of the card as the word with the step undone, and raised the step's own card beside the deploy's, so the user met one step twice, and the word on the card the step belongs to asked nothing of it. The deployer's hold kept anything from deploying early; the card did not say what the word waits on.

## Decision

1. **crew reads the mark where the deployer hands it.** A steps line with `before` among its when words is a step the deploy waits on, the user's alone: a line marking an agent's step so, or two such lines for one environment sharing a number, is refused with nothing offered (`read.1`), as `after-deploy.awk` refuses the first.
2. **The card asks it first, as boxes.** The deploy's card says first that the deploy waits on the steps, lists them first on its face, before the notes, each with its why or that it is done, and leaves them out of the after-deploy list. While one is open the card is boxes carrying highStakes, none ticked: a box for each open step, `before:<n>`, then one for the deploy, `deploy`, five to a list. The card's send with every box ticked is the word; a send with a box unticked is none. Once every step is done the card is the hold-to-approve it always was.
3. **The deploy's box is the card's yes.** Record 0038 speaks of "the card's yes with a step unticked"; the deploy's own box is that yes, beside the steps' ticks, and gives a lone step the second option a Pending You list needs.
4. **crew ties the box to the deployer's record by the step's words.** The deployer's record of the step carries no mark and its key is not in the steps file, so the step the deploy waits on is the user's step the run record holds on the environment in the same words, each run of spaces one, the newest when several are; a step not yet recorded has no key. A user's step recorded in such words while the environment's offer is open is recorded with `before` among its when words, crew carrying the offer's mark onto the record, and has no row or card of its own while that offer is open: one thing, one card (record 0031 §3). With no offer open it is any user's step, with its own card.
5. **The send is one approval.** `crew ops approve --ticked <n>,...` names the steps ticked by their numbers on the card; crew records each done under the key and commit the deployer recorded it with, so the deployer's hold, which reads those keys, lifts, and records the word. It is refused, recording only the refusal, naming each step neither ticked nor done (`roles.3`: the rule is a check, not only the brief's words), a number no step has, or a ticked step the deployer has not recorded yet, whose tick crew could not keep on its key (`read.1`). Main-level ops runs it on the send, and closes a card whose send left a box unticked as a declined one.
6. **The card's form is kept with it.** Pending You changes no card's kind, so a card moving between the hold-to-approve and the boxes is followed rather than changed; each post and change records its form in `Form` (boxes, or none), a field the run record already allows, which the next raise reads. A step the deploy waits on recorded done while its card is open raises the card again.

## Considered options

- **Words tie the box to the record (chosen).** Works with the deployer as it stands; the deployer itself makes one step of two with the same words, so the words are its identity of the step too. A step whose words differ between the steps file and the record is no match: approve is refused naming it, and the deployer's hold stands; nothing deploys early.
- **A mark on the step record, `crew ops step --when before`.** An explicit tie, but the deployer passes none and record 0038 has the deployer record the step "as it records the others"; a second way to say one thing until the deployer sends it. Not taken.
- **crew computes the deployer's key.** Exact, but crew would own a copy of swancloud's keying, a second owner of one mechanism. Not taken.
- **Steps' boxes alone, no deploy box.** Truest to "the send with the step ticked"; a lone step then needs a two-sided choice whose recommendation either nudges the user to claim it done or recommends not deploying. Not taken.
- **Keep the step's own card and show it on the offer card.** Two asks for one step, against record 0031 §3. Not taken.

## Consequences

- crew's offer card is the one place the user ticks a step the deploy waits on, and the deployer's hold lifts from that send with nothing of the deployer's changed.
- A ticked send recorded refused because the deployer had not recorded the step yet is approved again once `crew ops steps` lists it.
- A step recorded before this lands, with its own card open, keeps that card; approving its deploy with it ticked marks it done and closes that card.
