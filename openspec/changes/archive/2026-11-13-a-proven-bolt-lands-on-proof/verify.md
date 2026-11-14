# Verify: a-proven-bolt-lands-on-proof

Verified on `change/a-proven-bolt-lands-on-proof` at b8917119, cut from `bolt/crews-proven-bolts-land-on-proof`, on 2026-11-13.

**Verdict: archived.** The whole checks pass, all 31 tasks are ticked, and every requirement and scenario of the eight delta specs is met in the code, each pinned by a test.

## The whole checks

`tests/suite --affected` was run once. CLAUDE.md asks for that run when a change is done and before it merges. It runs the `#check-full` tasks the change affects, against the merge-base with `main`, as sluice picks them. It selected 32 tasks.

**32 passed, 0 replayed, 0 failed.** These were the tasks: `contract`, `logic`, `t-briefs`, `t-cards`, `t-docs`, `t-drive-set`, `t-flume-source`, `t-help`, `t-hold`, `t-journey-board`, `t-journey-cross`, `t-journey-land`, `t-journey-main`, `t-journey-main-fix`, `t-journey-ops`, `t-journey-plan`, `t-journey-review`, `t-journey-roles`, `t-journey-signals`, `t-journey-state`, `t-release`, `t-roles`, `t-runner`, `t-session-hook`, `t-slot`, `t-sluice`, `t-specs`, `t-stage-facts`, `t-suite`, `t-teams`, `t-waits` and `t-word`.

## Tasks

All 31 tasks of `tasks.md` are ticked, 2.12 among them. Each task names a check, and that check passed inside this run: `logic` holds every pytest file the tasks name, and `contract`, `t-journey-board`, `t-briefs`, `t-docs` and `t-journey-land` passed too.

## Specs

`openspec validate a-proven-bolt-lands-on-proof --strict` says the change is valid.
- Every requirement's text above its first scenario is at most 500 characters. The longest is 497: rail-cards "A landings row is due one land for each send and head".
- Every RENAMED FROM and MODIFIED header exists in `openspec/specs/`.
- Each MODIFIED requirement keeps every scenario its current spec has.
- The change edits nothing under `docs/` or `openspec/specs/` (`docs.4`, `docs.7`).

Each scenario of the eight delta specs was read against the code and its tests. Every one is met, and a test pins it:
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

### A stopped land spends only the send that posted it

This covers rail-cards "A landings row is due one land for each send and head", scenario "A later card at the head of a stopped land".

**How the code meets it.**
- `stopped_by` reads what the newest land crew asked of the bolt at that head was posted on: `"proof"`, the card whose send it carried (that land's `Card`, which `lands_change` writes from the send it carries), or None.
- `stop_spends` holds that a stop spends a card's send only when that card's own send posted the land. A stop whose posting crew cannot tell is read as spent (`read.1`).
- `landings_raised` hands `landings_step` each row whose stop spends nothing of this card's with no `stopped`. That covers a stop on proof, as before, and now a stop on another card's send. So the step does not read the row as spent.
- `post_lands` still gets the rows as read, `stopped` and all. `runner.lands_due` posts the land at that head on the later send.

**The other scenarios still hold.**
- **A stopped row on the same send.** The stop was posted by this card, so `stop_spends` is true. The row stays spent and nothing is posted again.
- **A send at the head of a stopped land on proof.** It takes the same path it did before.

**Once the land is asked.** The bolt's last `bolt.submit` is now the asked one, so `stops` drops the stop. The next raise leaves the card as answered and posts nothing more.

**`crew card read`.** It passes `landing_lines` `on_send`: the bolts this card ticked whose stopped land an earlier card's send posted. For those it says the earlier send is spent and the user's send of this card lands the bolt. It does not show the earlier land's request as this send's.

**The test.** `tests/py/test_landings.py::test_a_later_cards_send_lands_a_bolt_whose_land_on_an_earlier_send_was_stopped` runs through `plan.raise_landings` on `LandActs`. It checks:
- the land is posted on `req_k1`'s send, request 6 at `abc1234`;
- `req_k1` is left as answered, with no card posted, changed or closed, and "spent" appears nowhere in what the raise says;
- the next raise posts nothing more;
- `stop_spends` holds for the card that posted the stop, for one that did not, and for a head where none was posted;
- `landing_lines` says the right thing before the raise.

### For the design agent, not the code stage

- `CLAUDE.md` *Proving and landing a bolt* still says "a bolt lands on the user's send of its row on its kit's landings card … and on nothing else". Record 0067 changes that. No task of this change names `CLAUDE.md`, and the change's own docs, README, the crew skill, `crew`'s usage and ops's brief (`docs.2`), say a bolt lands on proof.
- rail-cards "A yes frees the team for its next bolt" has no code in `plugin/`. That was already so before this change, since the team machinery is gone. The MODIFIED text carries the requirement unchanged.
