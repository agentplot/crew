# Design

## Context

Read on 2026-11-07, on deneb.

**What the teams file says now.** `~/.config/crew/teams.json` labels four partitions: `afterthought`, `agentplot`, `madswan` (deneb) and `wldn` (chuck-herdr-alpha). There is no `swancloud`. `afterthought/main` of afterthought/crew-state was cut at `swancloud/main`'s tip, d4a494b, and carries its history: its run record holds every entry swancloud's roles wrote, and deneb's local record folder for the label is `afterthought`, with none for `swancloud`.

**The cards it holds open.** Read from `afterthought/main`'s run record as `plan.record_reading` reads it: `deploy/mac-studio` and `deploy/macbook-pro` in `swancloud-ops`'s name, `proposal/508`, `batch/62` and `batch/63` in `swancloud-planner`'s, and `proposal/508` again in `afterthought-planner`'s. The brief's card, req_2061e578985d4c8f8fb0 on `deploy/swancloud-srv`, was posted at 18:39:10Z in `swancloud-ops`'s name and closed by that agent's own session at 19:03:36Z (`card.close` on `agent/swancloud-ops`), after the signal's reading.

**How the sweep treats them today.** `plan.sweep_judged` takes each card posted on this host. A card whose key is a row's that still stands is `held`: Pending You is asked whether it still finds it, and nothing else happens. A card whose row is gone is closed with why (`row_gone`). Neither asks whether the owner is still a role anywhere. The row's key counts as carded by any open card (`carded`), so a row whose only card is in a former name is never posted in its owner's name either. `cards.card_under` reads a card by its owner's name alone, so the new owner holds no card under the key, and Pending You refuses to move one: afterthought-ops's `whoami` with `previousName` swancloud-ops is refused.

**Who reads the teams file.** The host's follower reads it afresh at each tick (`board.Follower.fleet`, which also keeps crew's Flume roles file from it, `teams.25`), and every rail read is made against that fleet. So the rail's card sweep is where crew reads a host file in which a card's role no longer stands.

**The family.** Pending You holds the card and refuses to rename its asker. crew owns the card's life: it raises each of its six cards at its event and closes each at the event that ends it (record 0031 §1, `briefs.11`, `briefs.16`). Flume's roles file follows the teams file whole at the same read (`teams.25`): a label gone from the teams file leaves the file with no entry for it, and nothing maps the old address to a new one. So one owner closes the card, crew, as it closes every other card, and it follows the teams file as the roles file does, mapping nothing. No other tool closes a crew card, so nothing is reconciled.

**The user's rule.** There is no renaming: a label change is a partition removed and another added (record 0055, rejected by the user on 2026-11-07: "Reject 0055: crew is removed from swancloud and added to agentplot").

**Area pages this change touches:** `core.md` (`state.4`, `read.1`, `read.4`, `code.7`, `code.8`), `plan.md` (the sweep lives in `plan.py`), `briefs.md` (`briefs.11`, `briefs.13`, `briefs.16`), `tests.md` (`tests.4`, `tests.11`) and `docs.md` (`docs.4`, `docs.6`). No rule changes, so no page is edited (`docs.7`).

## Goals / Non-Goals

**Goals:**
- No card crew raised in a role's name stands once that role's partition has left the teams file.
- The withdrawal says why and how what the card asked is raised again, and is recorded.
- The row the card held is carded in a name that reaches someone, by the path any row with no card takes.

**Non-Goals:**
- Mapping a former name onto a new one, carrying a card across, or taking one partition as another's successor.
- A kit's rename: the sibling `crew-renames-no-kit` removes it.
- The deploy cards' own forms: the siblings `a-failed-deploys-card-closes-naming-what-the-user-does` and `an-offer-card-shows-the-step-the-deploy-waits-on-first`.
- An agent's own question, and a card in a conductor's name.

## Decisions

### 1. A role that left is a partition role's name whose label the teams file no longer has

A card's owner has left the fleet when it is a name crew raises its own cards in, `<label>-planner`, `<label>-ops` or `<label>-design` (`plan.row_owner`, the design agent's records), and `<label>` is no partition of the teams file now. `cards.role_left(owner, labels)` decides it from the name and the labels alone. The label is read greedily up to the last dash before the role, so a partition `foo-bar` owns `foo-bar-ops`.

Two other paths were not taken. The first was any owner `plan.role` reads as no role of the fleet. That would also take every conductor's card, whose rows already close them by their own paths with their own words (`row_gone`; README: a bolt's own landing card gives way to its kit's), and the brief keeps to the cards of a partition's role. The second was reading the run record of a partition gone from the teams file. The teams file then no longer names its state repository, and nothing crew reads does, so crew would have to guess it (`read.1`). A label change whose state branch carries on, as afterthought's did, puts the old roles' cards in a record crew reads; a partition removed with no branch carrying on leaves its cards in a record nobody reads (see Risks).

### 2. The rail's card sweep withdraws them, on the host they were posted on

`plan.sweep_judged` takes the teams file's labels (handed by `sweep_judgments`) and puts each card of crew's six (`cards.row_object` names its key) posted on this host whose owner left the fleet in a bucket of its own, `left_fleet`, before any other judgment. A card closed or posted and refused under `CARD_RETRY` seconds ago is left for a later read, as every other card is. `cards_asked` and `sweep_cards` ask Pending You after it in crew's own name, as they ask after every card. A card that reads "not found" is recorded lost. Any other is withdrawn in its owner's name, through the same bridge every close of crew's uses, and recorded as a `card.close`, state `withdrawn`, its words whole. The read lists it with `did` `withdrawn`, so the rail drops it from its cards (`swept_cards`) and from the next read's, whose record holds the close.

The other path was an act at the follower's read of the teams file. Not taken: the cards, their record and Pending You's answers are the sweep's, which already asks after every card on its tick and closes every card whose event came. A second closer would ask and close beside it.

### 3. The words say who left and who raises the work now, by kind

`cards.left_said(owner, key, stands)` gives "<owner> left the fleet, so an answer here reaches nobody." then, by the key's kind:

| Key | Then |
|---|---|
| `deploy/<env>` | "The deploy is offered again in the name of the ops of the partition that holds <env> now." |
| `deploy/<env>`, its word standing | "Your word on <env>'s deploy stands, and the deploy goes on." |
| `op/<env>/<n>` | "The step on <env> is recorded again by the partition that holds it now, its card in its ops's name." |
| `land/<kit>` | "Its landings are carded by the ops of the partition that holds them now." |
| `proposal/<n>` | "Proposal <n> is carded by the planner of the partition that holds it now." |
| `batch/<n>` | "Batch <n> is carded by the planner of the partition that holds it now." |
| `record/<kit>/<n>` | "Record <n> of <kit> is carded again with crew record by the design agent of the partition that holds it now." |

The words name no partition, since crew takes none as another's successor. A deploy offer is made again by the new partition's ops, which posts its card in that name (`ops.offer_move`'s "post", the same `ops.raise_deploy` the sweep's raise calls). A word the user already gave is read by the environment, not the card (`ops.word_stands`), so its deploy goes on, and the words say that rather than ask again. Pending You takes 200 characters for a close (`cards.OUTCOME`); the longest of these, with a long owner and environment, is about 190, and the run record keeps them whole.

### 4. Only the card goes, and the row is carded as a row with none

The withdrawal closes the card alone, by `plan.card_closed`, not `row_card_close`. A key's reading session and a batch's previews are kept by the partition and the key (`~/.local/state/crew/cards/<label>/<key>`), and a row whose card was in a former name is still the partition's row: a new card of the standing owner's links the same session. They end with the row, by the sweep of the card sessions (`sweep_sessions`), as they do for any row.

A card in a former name cards no row: `sweep_judged`'s `carded` leaves it out, so a row whose only open card is such a one is among the rows with none (`none`) and is posted through its kind's raise in its owner's name, under that owner's own key (`cards.post_key`, `<key>@<label>`), following no card (`cards.follows_of` follows only the owner's own). This is the path any row with no card takes, and nothing is carried: the new card is built from the row's facts now.

### Rules relied on

- `read.1`: a removed partition's record, which the teams file no longer names, is not guessed at; a card Pending You does not answer for on the tick is left.
- `read.4`: crew closes only its own cards, in their own owner's name, and takes over nothing.
- `state.4`: the sweep writes only its acts' run-record entries, as before.
- `code.7`: `role_left` and `left_said` are decisions on plain facts, tested in the logic tier; `sweep_judged` stays one.
- `code.8`: no bolt, unit, stage, card key or rail row changes shape, and `withdrawn` is a sweep outcome the rail already lists, so the views and the mod are untouched.
- `briefs.11`, `briefs.16`: crew closes its own cards, in the name of the role whose card it is, under the host's sign-in.
- `briefs.13`: the words are prose that wraps.
- Record 0031 §1: crew closes each card at the event that ends it.

### Departures

None.

## Risks / Trade-offs

- **[A removed partition whose record nobody carries on]** → Its open cards stay open: the teams file no longer names its state repository, so no read of crew's reaches them (`read.1`). The user dismisses them in the app. A label change whose state branch carries on, the case that happened, is covered.
- **[Pending You refuses the old name's whoami]** → The withdrawal is made in the owner's name, as every close of crew's is. If Pending You refused to open a session in a name that left, the close is recorded refused and said, the card stays on the rail, and the next read past `CARD_RETRY` tries again. The row is posted in its owner's name either way, so the user's answer reaches someone.
- **[A card in a name crew mints for something else]** → Only `-planner`, `-ops` and `-design` are read, and only for crew's six keys, so a question or a conductor's card is never judged here.

## Migration Plan

None. The first rail read on each host withdraws the cards in former names posted there.

## After deploy

None: every outcome here is a logic-tier case, and the withdrawal on deneb is the rail's own read once the host loads the release that carries it.

## Task notes

**1.1** `plugin/lib/cards.py`: `ROLE_NAME`, the pattern `([a-z0-9][a-z0-9-]*)-(planner|ops|design)`; `role_left(owner, labels)`, true when the owner matches and its label is not among the labels; `left_said(owner, key, stands=False)`, the words of Decision 3 by the key's first part. Cases in `tests/py/test_rail.py`: `willdan-ops` left where the labels are `wldn`, `wldn-ops` not; `foo-bar-ops` not where `foo-bar` is a label; `swb-1-conductor`, `chuck@mac-studio` and `None` not; the words for each kind, and a deploy's word standing.

**1.2** `plugin/lib/plan.py`: `sweep_judged(..., labels=None)` gains the bucket `left_fleet`, `[(card, words)]`, judged first for each card posted here whose key `cards.row_object` names and whose owner `cards.role_left` reads left, refused-lately cards left out, `stands` from `ops.word_stands`; `carded` leaves those cards out. `sweep_judgments` hands `labels=set(fleet["partitions"])`. `cards_asked` and `sweep_cards`' own ask include them. `sweep_cards` acts on each: not answered on the tick, skipped; lost, `card_lost` and `did` `lost`; else `card_closed(acts, l, owner, key, None, words)`, `did` `withdrawn` with the words when it closed, `left` when it did not. Cases in `tests/py/test_rail.py`: the label changed under `deploy/dev`'s card in `willdan-ops`'s name, withdrawn with its words, its close recorded and its row posted through its raise in `wldn-ops`'s name; the partition stays, the card left and nothing posted; `sweep_judged` putting a record's card in `willdan-design`'s name in `left_fleet` and not in `gone`, leaving a question in a former role's name and a conductor's card to their paths, and judging nothing left with no labels handed; `cards_asked` naming a card in a former name.

**2.1** `README.md`: in the paragraph on each rail read's sweep, after the question withdrawn, a clause: a card of crew's in a name of a partition role whose label the teams file no longer has is withdrawn, saying its role left the fleet and how what it asked is raised again, and its row is carded in its owner's name as a row with none.
