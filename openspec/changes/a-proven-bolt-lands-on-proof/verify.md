# Verify: a-proven-bolt-lands-on-proof

Verified on `change/a-proven-bolt-lands-on-proof` at 14a66c3a, cut from `bolt/crews-proven-bolts-land-on-proof`, on 2026-11-13.

**Verdict: not archived.** The whole checks pass and every task is ticked. But one path the change itself adds falls short: a later card's send at the head of a land stopped on an earlier send is posted as a land, and then the same raise closes that card saying the send is spent and posts a new card asking to land the bolt again. The change goes back to its code stage.

## The whole checks

`tests/suite --affected` was run once. That is the run CLAUDE.md asks for when a change is done and before it merges: it runs the `#check-full` tasks the change affects, against the merge-base with `main`, as sluice picks them. It selected 32 tasks.

**32 passed, 0 failed.** Five were replayed from runs on this host with identical inputs: `contract`, `logic`, `t-briefs`, `t-docs` and `t-journey-board`. The other 27 ran, among them `t-journey-land`, `t-hold`, `t-cards`, `t-help` and `t-specs`.

## Tasks

All 30 tasks of `tasks.md` are ticked. Each task's own check passed inside this run: `logic` holds every pytest file the tasks name, and `contract`, `t-journey-board`, `t-briefs`, `t-docs` and `t-journey-land` passed.

## Specs

`openspec validate a-proven-bolt-lands-on-proof --strict`: valid.
- Every requirement's text above its first scenario is at most 500 characters. The longest is 497: rail-cards "A landings row is due one land for each send and head".
- Every RENAMED FROM and MODIFIED header exists in `openspec/specs/`.
- Each MODIFIED requirement keeps every scenario its current spec has.
- The change edits nothing under `docs/` or `openspec/specs/` (`docs.4`, `docs.7`).

Each scenario of the eight delta specs was read against the code and its tests. Every scenario is met, and a test pins it, except the one below. These are now met:
- **The Hold record set.** It is declared ahead of Bolt and Unit, and an old plan takes it there (`holds_declared`). So a record appended at the file's end is still a Unit, and a hand edit's duplicated Unit is refused as a duplicated key.
- **Two holds on one kit.** crew refuses to read such a plan, naming the commit (`read` → `holds_once`).
- **The drive's lift.** It raises each kit of the drive (`Write.kits`), except one its own hold still holds.
- **A rename.** It renames a Hold's `Kit`.
- **A forecast not made.** It posts no land on proof and says why.
- **Re-checks at the write's tip.** `lands_change` looks again for the hold and the mark at the tip it is applied to (`plan.1`).
- **Under a hold, a card's close or follow.** It says the user's send stands.
- **A stopped land on proof.** The user's send lands it. The send is not read as spent, and the row and `crew card read` say the land on proof stopped.
- **`crew rail` and the rail tab.** Each told bolt has a line of its own, and a proof line names `<label>-ops`.
- **The docs and crew's own words.** README, the crew skill, `crew`'s usage, ops's brief, `submit_refused` and `landing_refused_said` all say a bolt lands on proof, or, marked to stay, on the user's send.

### The finding the code stage must fix

**rail-cards "A landings row is due one land for each send and head" / "A later card at the head of a stopped land": the land is posted, but the same raise closes the card as a send spent and asks for the bolt again.**

- `runner.lands_due` now lets a later card's send land a row at the head of a land stopped on an earlier card's send, as the modified requirement asks (`plugin/lib/runner.py:1671`).
- But `landings_step` still reads every boxed row with `stopped` facts as spent (`plugin/lib/plan.py:3382`, `spent = {r["bolt"] for r in rows if r["box"] and r["facts"].get("stopped")}`).
- `landings_raised` strips `stopped` before the step only for a land stopped on proof (`stopped_on == "proof"`, `plan.py:4142`). It does not strip it for one stopped on another card's send, and it does not read the rows again after `post_lands`.

Reproduced through `plan.raise_landings` on the logic tier's `LandActs`, as in `test_the_users_send_lands_a_bolt_whose_land_on_proof_was_stopped`:
- **The case.** `z` is marked to stay. Its land on `req_k0`'s send, request 5 at `abc1234`, was stopped by the runner. `req_k1` follows with `Heads: z@abc1234`, and the user answers it, approved.
- **What the raise does, in one pass:**
  1. It posts `plan(crew): land z on the user's send`, `Card: req_k1`, request 6, at `abc1234`.
  2. It closes `req_k1` with the outcome "z's landing at abc1234 was stopped, nothing of the bolt's: flume refused it: a place on bolt/z is live; your send of it is spent, and the card that follows asks for it again."
  3. It posts a new card, "Land the bolt z on crew's main", `Heads: z@abc1234`, asking for a bolt whose land it has just asked of the runner.

So the user is told their send is spent when crew carried it, and is asked again to land a bolt already being landed. Design Decision 3 says the card that follows a spent send "lands it on its own send"; the land is posted, but the card the user sent is treated as spent.

`crew card read land/crew` has the same fault between the send and the raise. `landing_lines` says "z's last landing at abc1234 was stopped …; it lands again only on the user's next send" of the send that lands it, and names no land to come (`plan.py:12734-12744`).

No test covers this path above the runner. `tests/py/test_runner.py::test_a_send_lands_a_row_at_the_head_of_a_land_stopped_on_proof_or_on_another_send` checks `lands_due` alone. The case above belongs in `tests/py/test_landings.py`, beside the on-proof one: the land posted on `req_k1`, the card left as answered and not closed as spent, and the next raise posting nothing more.

A fix that fits the existing shape is for `landings_raised` to mark a row whose stopped land a send other than this card's posted, as it marks one stopped on proof, and to hand `landings_step` that row with no `stopped`. Then `card_read` and `landing_lines` read it the same way.

### For the design agent, not the code stage

- `CLAUDE.md` *Proving and landing a bolt* still says "a bolt lands on the user's send of its row on its kit's landings card … and on nothing else". Record 0067 changes that.
- rail-cards "A yes frees the team for its next bolt" has no code in `plugin/`. This predates the change: the team machinery is gone. The MODIFIED text carries it unchanged.
