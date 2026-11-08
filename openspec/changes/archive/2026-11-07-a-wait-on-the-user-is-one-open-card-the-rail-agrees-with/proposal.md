# Proposal

## Why

Record 0031 makes every wait on the user one open card, closed by crew at the event that ends it, and record 0053 keeps no list beside the cards: what waits on the user is the cards and the rail that shows them. On 2026-11-07 and 08 the rail and the cards disagreed in four ways.

- **An answered card reads as waiting on the user.** The rail prints every open card as `open, asked by <owner>`, whether or not the user has answered it. crew writes the answer only into the card's close. A landings card the user sent stays `open` until ops lands the bolts, and the bolts' time reads as the user's.
- **An answered card is withdrawn as if nothing were asked.** agentplot's `land/sluice` card `req_5fd09f93…` was approved by the user. At 03:14:20Z a sweep found the kit's row gone for a moment and withdrew it: "nothing waits to land on sluice's main", State withdrawn, Answer approved. Pending You acked the user's answer with those words. 57 seconds later ops submitted the bolt the user had approved (#21). 28 seconds after that, the next card asked the user for that same bolt again, because a withdrawn close keeps no send (`landings_sent` reads only a close's Heads).
- **A closed card stays on the rail.** madswan's batch cards 16 to 31 were posted under a Pending You name that is not crew's owner. Every close is refused ("This is swancloud-planner's card; leave it"). Their batches were answered in a pane two weeks ago. The rail has listed them since 2026-10-25 under open cards whose row is gone, each saying "a later rail read here closes it", which no read can. afterthought's `proposal/508` row shows two open cards, one in the name of a partition that left the fleet. A card Pending You has ended reads as open to crew until crew next tries to change or close it.
- **A land row does not say which card holds a bolt.** Every bolt line on agentplot's land rows ended "user since 19:01, ask/agentplot-design/sluice-who-claims-runs-when-the-host-is-idle". That is one design question, charged to bolts of four kits. Since the teams left deneb, every question a main-level role asks counts against every started bolt. No line said whether the kit's card carries the bolt, holds the user's send for it, or will carry it on the card that follows.

## What Changes

- crew records the user's answer on a card as an entry of its own, `card.answer`, the first time it reads the answer from Pending You. Every host's rail, the board and the agents' bands then read the answer from the drive's branch (`read.5`).
- A row whose card the user answered says so on the rail: when they answered, what they answered in crew's words, and whose act it now waits on (ops's landing, the planner's apply, the design agent's record). An answered question or record card leaves the lists of what waits on the user. The owner's band says the card is answered and is theirs to act on.
- A card the user answered is closed, never withdrawn. A kit's landings card's close carries the user's send as Heads in every path, so the card that follows never asks again for a bolt the send still lands. The sweep leaves an answered landings card open while a bolt it ticked still waits to land on that send, even when the kit's row is briefly gone.
- A card leaves the rail once crew records it closed. The sweep records a card Pending You reports ended as closed or withdrawn on the read that finds it. A card Pending You holds in another assistant's name is lost to its recorded owner, so its row's card is posted again in the owner's name, or no one posts it when its row is gone. A row shows one card: its owner's. Any other card open under its key is named apart. A card whose close keeps being refused is listed with the refusal's words, never with a promise that a later read closes it.
- Each bolt line on a kit's land row says which of these holds:
  - **carries**: the kit's open card carries the bolt and waits on the user;
  - **holds**: the user's send holds it, and ops lands it;
  - **follows**: no card carries it yet, and the next card does.
- A bolt's time is the user's only while a card that carries the bolt or its work waits on them. A landings card counts for a bolt while its rows name the bolt, until the user's answer. A question counts only when its post names the bolt or its work.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `crew-rail`: a row's card line says when its card was answered and whose act it waits on, and each bolt line on a land row says whether its card carries, holds or follows it.
- `rail-cards`: an answer is a recorded card act. An answered card is closed, never withdrawn, and keeps its send. An answered landings card is held while a bolt it ticked waits to land. A card Pending You ended, or holds in another name, leaves the rail. A row shows one card.
- `crew-board`: a bolt's time is the user's only while a card carrying it waits on them, and a question counts only when it names the bolt. An agent's band says which of its cards the user answered.

## Impact

- `plugin/lib/plan.py`:
  - the rail: `record_reading`, `rail_rows`, `rail_text`, `stray_cards`;
  - the sweep: `sweep_judged`, `sweep_cards`, `cards_asked`;
  - the landings card: `kit_card_state`, `card_closed`, `card_read`;
  - a bolt's time: `bolt_facts`.
- `plugin/lib/cards.py`: `close_call`, `lost`.
- `plugin/lib/record.py`: the docstring that names the card acts.
- `plugin/lib/board.py`: the board's cards and markers, `card_line`, `ops_view`.
- The mod's cases: `plugin/tests/status.test.ts`.
- Docs: README's rail section, `plugin/skills/crew/SKILL.md` and `plugin/bin/crew`'s usage header (`docs.2`).
- Logic-tier cases: `tests/py/test_rail.py`, `test_cards.py`, `test_card_commands.py`, `test_landings.py`, `test_bolt_time.py`, `test_board.py`.
- No new field in the run record; one new act, `card.answer`. Nothing new reads Pending You beyond the reads crew already makes, but for each open decision record's card, which the sweep now asks after with the others.
