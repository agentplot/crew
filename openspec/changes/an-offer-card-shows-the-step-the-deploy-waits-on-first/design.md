# Design

## Context

See proposal.md for why, and the deltas, `rail-cards` and `main-level`, for what becomes true. The reasoning is record 0059; what must be true is swancloud record 0038, the user's.

The deployer as it stands (swancloud 49469fba, `packages/swancloud-deployer`):

- **The steps file.** `after-deploy.awk` prints a step marked `- before: deploy` with `before` in its when column. Such a step is the user's alone and names its environments. `offer_steps` puts these steps first, numbered from 1, and the rest after them.
- **The record.** `offer_deploy` runs `crew ops offer`, then `record_waited`. That records each waited-on step as `crew ops step <env> --to <offered> --key <key> --state waiting --doer user --text <file> --changes <a,b>`, with no `--when`. The key is the first twelve hex digits of the sha256 of `user\nbefore\n<words compared>`. A step crew holds waiting or done on the environment is not recorded again.
- **The hold.** `held_on_steps` holds a word until crew's `crew ops steps <env> --json` shows `done` as the latest state of each waited-on key.

crew as it stands: `handed_steps` reads `held` from the when words and passes any other word through, so `before` reached the card as an ordinary user's step. `crew ops step --doer user --state waiting` raises the step's own card. `crew ops approve` records the word for the open offer's head and checks nothing else.

Rules relied on: `read.1` (refuse what can't be read; tie no box by guess), `code.7` (each decision a function of facts: `waited_on`, `marked_before`, `own_card`, `ticked_refusal`, `deploy_form`, `form_asked`), `roles.2` (the word is the user's, on the card), `roles.3` (the rule that a step must be ticked is a check in crew, not only the brief's words), `record.3` (the steps file stays beside the offer; nothing typed enters the run record but the step's text, which `ops.step` already carries), `code.8` (no view changes shape), `docs.2`, `tests.4`, `tests.6`, `tests.11`. Pages whose area the change touches: `plan.md` (`plan.14`, amended by record 0059), `briefs.md` (main-ops's brief), `record.md` (the descriptor's comment), `docs.md`, `tests.md`. Departs from no rule.

## Goals / Non-Goals

**Goals:**

- The user meets a step a deploy waits on on the card where they give the word, ahead of everything else on it, and gives the word by ticking it.
- crew refuses the word while such a step is open.
- The deployer's hold lifts from the same send, with nothing of the deployer changed.

**Non-Goals:**

- A failed deploy's close (the sibling fix `a-failed-deploys-card-closes-naming-what-the-user-does`): this change keeps to the offer and the approval.
- Any change of swancloud's.
- A mark on the deployer's step record: none is sent, and none is read (record 0059, options).

## Decisions

### 1. The mark is read as the deployer hands it

`handed_steps` gives each step `before`, true when `before` is among its when words, and its `why`. A `before` step whose doer is not `user` is refused, naming the line, as `after-deploy.awk` refuses it: "line <i> is a step the deploy waits on, which is the user's alone, with the doer <doer>". So are two `before` steps for the environment with one number, since each number is a box's id. Every refusal of the steps file refuses the offer whole, as today.

### 2. The step's record is found by its words

`waited_on(handed, es, env)` gives the steps the open offer waits on. For each handed `before` step, in order, it finds the user's step on the environment whose recorded text has the same words, each run of spaces one (`words_of`). Where several match, it takes the one whose latest entry is newest. It reads the words from the entries that carry a text, since a later `done` entry carries none. Each comes back as `{n, text, why, to, key, state}`, with `to`, `key` and `state` None while the deployer has not recorded it.

The words are the deployer's identity of a step too: two steps in the same words are one key. Matching the words exactly, and not the deployer's lowercased comparison, keeps crew from copying swancloud's keying. Where they differ, nothing matches: the approval is refused naming the step, and the deployer's hold stands.

Alternative: crew computes the key, sha256 of `user\nbefore\n<compared>`. Not taken, since that would make crew a second owner of the deployer's keying.

### 3. The record carries the offer's mark

`crew ops step` with `--doer user` and a text reads the steps kept with the environment's open offer (`offered_steps`). When the text has a `before` step's words (`marked_before`), crew records the step with `before` among its when words and prints that it is ticked on the deploy's card. `own_card(e, offers)` is `waits_on_user(e)` and not (marked `before` while its environment has an offer open). `rows`, `step_due`, `step_point` and `environments`' row use it in place of `waits_on_user`. So such a step has no row and no card of its own while the offer is open, keeps its number among the environment's steps, and has its own row and card again once no offer is open. The deploy's row says it waits on the marked steps still waiting.

### 4. The card asks the steps first, as boxes

`deploy_facts` takes `waited` and leaves `before` steps out of `steps`. `deploy_card`:

- **Summary.** It opens "It waits on N step(s) of yours before the deploy". While one is open, it goes on: ": tick each once it is done, and the deploy; your send with every box ticked is the word to deploy, and a box left unticked deploys nothing." Once all are done: ", each done."
- **Face.** First, a text list titled "Before the deploy: N step(s), yours", each step `<n>  <words>` with its why, or `done`, under it. Then the notes or the landings, then the after-deploy steps.
- **Form while a step is open.** `kind: multi`, `intent: decide`, `highStakes`, `recommendedIds: []`, `multi {min 0, max}`. The options are each open step, `before:<n>` labelled `Done: <n>. <words>`, its why as detail, then `deploy`, labelled `Deploy <head> to <env>`. Its rationale says what follows a yes, as the approval's did. Past five boxes the card asks lists of at most five, each a question carrying the rationale, the deploy's box last (as the landings card does). Pending You refuses a card's rationale beside questions.
- **Form once every step is done**, or when there are none: the approve it always was.

`deploy_form(f)` is `boxes` while one is open, else None. The builder hands it back as `form`.

Alternatives: the steps' boxes alone, with no box for the deploy. Not taken: a lone step would need a two-sided choice whose recommendation either nudges a claim of done or recommends not deploying, and record 0038 speaks of the card's yes beside the ticks. A hold-to-approve with the steps on its face and nothing to tick: not taken, since the brief and the record ask for ticks.

### 5. One send, one approval

`crew ops approve <env> --to <sha> [--ticked <n>[,<n>...]]`. After the head check of today, crew reads `waited_on` for the open offer's kept steps. `ticked_refusal(env, to, waited, ticked)` refuses in this order:

- a number no step the deploy waits on has, naming the steps it waits on;
- each step neither ticked nor done, named with its number and words: "the deploy of <env> to <sha7> waits on your step 1 ("…"), not ticked: the word is its card's send with every step it waits on ticked";
- a ticked step the deployer has not recorded yet, whose tick crew could not keep on its key, saying to approve again once `crew ops steps` lists it.

A refusal is recorded as a refused `ops.approve`, and nothing else is written. Otherwise crew records each ticked step done, `ops.step` under the deployer's `to` and key, `Doer: user`, `When: before` and `Note: ticked on its deploy's card`. Then it records the approval. Last, it closes any card of a ticked step's own still open, one raised before this change. `--ticked` is checked by `args_refusal` as a comma-separated list of numbers.

### 6. The card's form is recorded and a move between forms is followed

`plan.built_fields` adds `Form` from the built card, so every post and change of a deploy's card records `Form: boxes` or nothing. `cards.form_asked(entries, card)` reads the last recorded form of a card. `raise_deploy` passes `kind_changed` to `row_card_change` when ops holds the card and its recorded form differs from the one built now. `row_card_change` then follows the card rather than change it in place. `crew ops step --state done` of a step whose latest entry was marked `before`, while the environment has an offer open and ops holds its card, raises the deploy's card again with the note "A step it waits on is recorded done".

### 7. What ops runs

Main-level ops's brief, *Deploying main*: a deploy that waits on steps of the user's has them first on its card, a box each and one for the deploy. Their send with every box ticked is the word, and ops runs the row's answer with `--ticked <n>,...` naming each step box they ticked by its number. crew refuses it naming any step left unticked. That send, like one with the deploy's box left unticked, is no word, and ops closes the card with `card read` as a declined one, ticking nothing for them. `tests/t-briefs.sh` pins the phrases.

## Risks / Trade-offs

- [The step's words differ between the steps file and the record] → no match. The approval is refused naming the step, and the deployer's hold stands. Both come from one text of the deployer's (`gather`'s), so this does not arise today.
- [The deployer has not recorded the step when the user sends] → the approval is refused, saying to approve again once `crew ops steps` lists it. The deployer records it in the same run as the offer.
- [A send with a box unticked] → no word, and the card is closed as declined. The offer stands, asked again at a newer head or with other files, as for a declined deploy. The step has no card of its own meanwhile, since the offer is open. swancloud's design names the decline as the user's way on.
- [A step recorded before this lands, with its own card open] → it keeps that card. The offer card shows its box too, and the approval with it ticked closes that card.

## Migration Plan

None. A step recorded before this lands is unmarked and keeps its card. The next offer's card is built in the new form, followed rather than changed when ops holds an older one, whose recorded form is none.

## After deploy

None: every behaviour here is proved by the logic tier and `t-journey-ops`. The deployer needs nothing new.

## Task notes

**1.1** `ops.handed_steps`: `when = f[3].split()`; refuse a `before` step whose doer is not `user`, and a second `before` step with a number already taken for the environment; each step `{n, text, doer, held, before, why}`. Cases in `test_ops.py` `TestOfferHanded` and `TestTheStepsADeployWaitsOn`.

**1.2** `ops.words_of`, `ops.waited_on`, `ops.marked_before`, `ops.BEFORE`, `ops.waits_before`. Cases: no record, a record with its words across a line break, a later `done` entry, another environment, an agent's, other words, a step declined under an older head and recorded again.

**1.3** `ops.own_card`; `rows` (the deploy row's words for the marked steps waiting, a carried step's row left out), `step_due`, `step_point`, `environments`. Cases: the open offer carries the step; the deploy ended, and the step has its row.

**1.4** `ops.ticked_refusal`, `ops.ticks_of`, `ops.offered_steps`, `ops.approve`, `ops.step_closed` (factored from `step`), the parser's `--ticked` and `args_refusal`'s `TICKED`. Cases: open, ticked, a stray number, none waited, done already, not recorded; `args_refusal` for `--ticked 1,x` and `1,2`.

**1.5** `ops.deploy_facts(…, waited)`, `cards.deploy_card`, `cards.deploy_form`. Cases: one step open (summary, face order, the multi's options, highStakes, no approve, `form`); every step done (approve, `done` on the face); five steps (two lists).

**1.6** `plan.built_fields` adds `Form`; `cards.form_asked`; `ops.raise_deploy` passes `kind_changed`; `ops.step` marks `before` and raises the deploy's card again on a carried step's `done`. Cases: `built_fields`, `form_asked`, `raise_deploy` against a held card with and without `Form: boxes`, `step` marking the deployer's record, and `step` raising the card on `done`.

**2.1** `tests/t-journey-ops.sh`, its last block: an offer to macbook-pro with a `before` step posts a multi with `before:1` and `deploy`, the face's first list "Before the deploy", and `Form: boxes` recorded. The deployer's record of the step is marked `before` and posts no card. The rail says the deploy waits on it. `approve` without `--ticked` is refused naming the step, with no word. `approve --ticked 1` records the step done and gives the word.

**2.2** `plugin/roles/main-ops.md` *Deploying main*; `tests/t-briefs.sh` pins "run the row's answer with `--ticked <n>,...` naming each step box they ticked by its number" and "ticking nothing for them". README, `plugin/skills/crew/SKILL.md` and `plugin/bin/crew`'s usage give `[--ticked <n>[,<n>...]]`, which `tests/t-docs.sh` checks.
