# Design

## Context

**What Pending You refuses.** A post whose card asks `questions` and carries `highStakes` on the card is refused: "With questions, each question carries its own highStakes; leave the card's highStakes out." This was read on the Willdan box on 2026-11-10, where crew 0.41.11 posted `land/<kit>` for six proven bolts and was refused each time (signals `2026-11-10-wldn-ops-6352d0d6/01` and `2026-11-10-wldn-operator-9599d7fa/01` on WilldanGroup/crew-state `wldn/main`). A card of one list takes `highStakes` on the card, "the same test as risk high" (pendingyou's `post_request` schema, read 2026-10-23, in `one-landings-card-lands-the-proven-bolts-in-order`'s design).

**Where crew puts `highStakes` beside questions.** Two builders in `plugin/lib/cards.py` pass `highStakes=True` to `built` whatever their form:
- `landings_card`, whose form is lists of questions past `BOXES` rows (`landings_form`). Rows taking main first are rows, so they count toward the six.
- `deploy_card`, whose boxes are lists of questions past `BOXES` options, once a deploy waits on five or more open steps.

No other builder sets `highStakes`. The proposal card asks questions but carries none.

**The family.** No other tool of the Boomdrive family builds a Pending You card: Flume shows a stop-short through its caller, and sluice, timber, weir and boom post none. crew is the one owner of these cards' forms, so the fix is crew's alone.

**Area pages this change touches:** `core.md` (`roles.5`, `code.7`, `code.8`), `tests.md` (`tests.4`, `tests.11`, `tests.12`) and `docs.md` (the spec). No rule changes, so no page is edited.

## Goals / Non-Goals

**Goals:**

- A landings card of any number of rows, and a deploy's card of any number of boxes, is posted, its stakes high on every list the user answers.

**Non-Goals:**

- A change to when a card is lists rather than one list (`BOXES`), or to anything else of the forms.
- Raising again a card refused before this change. The rail's sweep already posts a refused card again (rail-cards "A row's card that Pending You refused is owed until it posts").

## Decisions

### 1. Each builder puts `highStakes` in its form's shape

`highStakes` moves from the `built` call into each shape: on the card for one list, on each question for lists. Each list is a box list the user ticks to land or deploy, so each is high stakes, as one list is today.

The other path was a rule inside `built` that moves a card's `highStakes` onto each question whenever the card asks questions. Not taken: it would mark every question of any card of questions, a proposal's among them should one ever carry it, by a rule no reader of the builder sees. The shape is where each builder already says what Pending You takes beside questions, its rationale per list, so the stakes sit beside it.

### 2. The stub refuses as Pending You does

`tests/stubs/pendingyou`'s `post_request` refuses a card of `questions` that carries `highStakes`, in Pending You's words (`tests.4`). The stub took such a card until now, which is why the end-to-end tier never met the refusal.

### Rules relied on

- `roles.5`: crew wraps Pending You and builds its cards in the forms Pending You takes.
- `code.7`: the builders are decisions on plain facts, tested in the logic tier.
- `code.8`: no bolt, unit, stage, card key or rail row changes shape, so the views and the mod are untouched.
- `tests.4`: the reproducing cases are in the logic tier, one on a fake that refuses as Pending You does, and the stub refuses the same way.

### Departures

None.

## Risks / Trade-offs

- **[Pending You changes where it takes `highStakes`]** → a post is refused again in Pending You's words, recorded refused, and shown on the rail's card line (`plan.last_refusal`).

## Migration Plan

None. A landings card refused on a host is owed on its rail; the rail's sweep posts it again once crew at this change runs there.

## After deploy

None: every outcome here is a logic-tier case, and nothing waits on a host or on the user.

## Task notes

**1.1** `plugin/lib/cards.py`: `landings_card`'s and `deploy_card`'s shapes carry `highStakes=True`, on the card for one list and on each question for lists, and neither passes it to `built`. Their docstrings and `landings_form`'s say so. Cases: `tests/py/test_cards.py` `TestLandings`, rows 6, 7 and 11 carry `highStakes` on each list and none on the card, and three rows carry it on the card; `tests/py/test_ops.py`, a deploy waiting on five steps carries it on each of its two lists and none on the card.

**1.2** `tests/py/test_landings.py`: `LandActs`'s bridge takes a function of the tool's arguments as an answer. `marked_post` refuses a card of questions that carries `highStakes` in Pending You's words. Six proven bolts of crew, raised through `plan.raise_landings` on it, post one card of two lists of three, each carrying `highStakes`, the card none, recorded posted.

**1.3** `tests/stubs/pendingyou`: `post_request` refuses a card of `questions` carrying `highStakes`, "With questions, each question carries its own highStakes; leave the card's highStakes out.", after its key is checked.
