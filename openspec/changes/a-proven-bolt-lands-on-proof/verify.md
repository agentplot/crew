# Verify: a-proven-bolt-lands-on-proof

Verified on `change/a-proven-bolt-lands-on-proof` at 3bbb1156, cut from `bolt/crews-proven-bolts-land-on-proof` (28f2e646), on 2026-11-13.

**Verdict: not archived.** The whole checks fail. Six of the specs' scenarios are not met, or met only in part, and three docs tasks leave stale claims behind. The change goes back to its code stage.

## The whole checks

`tests/suite --affected` was run once. That is the run CLAUDE.md asks for when a change is done and before it merges: it runs the `#check-full` tasks the change affects, against the merge-base with `main`, as sluice picks them. It selected 32 tasks.

**30 passed (0 replayed), 2 failed: `contract` and `t-journey-board`.** Every other task passed, including `logic`, `mod`, `t-specs`, `t-briefs`, `t-docs` and `t-journey-land`.

- `contract`: three cases of `tests/contract/test_recfix.py` fail:
  - `test_the_plan_takes_a_chore_among_its_units_and_refuses_any_other_kind`
  - `test_a_rename_is_one_commit_whose_files_pass_recfix_and_its_entry_names_both_names`
  - `test_a_rename_whose_plan_breaks_unique_repo_goal_is_refused_before_any_commit`

  Each fails with recfix's `mandatory field 'Why' not found in record` / `field 'Unit' not allowed in this record set`.
- `t-journey-board`: it expected `duplicated key` from a hand edit that adds a second `Unit: a` at the end of `plan.rec`. It got `plan.rec:78: error: mandatory field 'Why' not found in record … field 'Unit' not allowed in this record set`. In the kept scratch (`/private/tmp/crew-test.bVaNAF`), the plan crew wrote has `%rec: Hold` at line 72, after every Unit, and the appended `Unit: a` at line 78 falls under it.

**Cause.** The new `Hold` record set is the plan's last record set. `plan.HEADER` declares it after `Unit` (`plugin/lib/plan.py:199`). `holds_declared` appends it at the file's end for a plan written before it (`plan.py:450`). recutils puts each record under the descriptor before it, so any record added at the end of `plan.rec` becomes a Hold record. That covers the contract fixtures (`HEADER + "Unit: …"`), the journey's hand edit, and any hand or tool that appends a unit. crew's own writes still place records correctly (`Plan.end_of`).

## Tasks

All 20 tasks of `tasks.md` are ticked. Each task's own check passed inside this run: `logic` holds every pytest file the tasks name, and `t-briefs`, `t-docs` and `t-journey-land` passed. Tasks 4.1 and 4.3 pass their checks, but the docs still contradict what they add (finding 6).

## Specs

`openspec validate a-proven-bolt-lands-on-proof --strict`: valid. Every requirement's text above its first scenario is at most 500 characters, the longest 486 (bolt-teams). Every RENAMED FROM and MODIFIED header exists in `openspec/specs/`. The change edits nothing under `docs/` or `openspec/specs/` (`docs.4`, `docs.7`).

Each scenario of the eight delta specs was read against the code and tests. The scenarios not listed below are met, and a test pins each.

### Findings the code stage must fix

1. **The whole checks fail** (above). Either declare `Hold` before `Unit`, with `holds_declared` putting it there for an old plan, so `Unit` stays the plan's last set; or bring every fixture and the journey's hand edit in step. The first choice also keeps a hand-appended unit a Unit.

2. **rail-cards "A landings card asks only about the rows a send must land" / "A land on proof stopped": the user's send cannot land the bolt at that head.**
   - `runner.lands_due` skips any row with a land already posted at its head, from any card or none (`plugin/lib/runner.py:1660`). The stopped land on proof is such a post, so the send posts nothing.
   - `landings_step` then reads the send as spent. The card asks again at the same head, forever.
   - The row's own text promises otherwise: "ticked again, it lands on this send" (`plugin/lib/cards.py:1025`). So does design Decision 3, which says "A stop holds the bolt at a head no fix moves, so only a send can land it".
   - The delta also leaves `rail-cards` "A landings row is due one land for each send and head" unmodified. That requirement says no land is due where one "was posted at that head", so the archived spec would contradict this scenario. The fix needs a MODIFIED delta of that requirement, one in which a stopped land on proof bars no send's land at its head, and the matching change in `lands_due`.
   - No test sends a card at the head of a stopped land on proof.

3. **crew-rail "A kit's row under land holds the bolts its card tells" / "Landed overnight": `crew rail` drops the told bolts' lines.**
   - `rail_rows` builds `<bolt> landed on proof at <commit>, told on land/<kit>` (`plan.py:10612`).
   - `rail_text` then zips the lines after the fixes with `land_times`, which gives one time per row bolt (`plan.py:11345`). Every told line is cut, so the rail and the rail tab show only the head line, "2 bolts landed on proof, told on land/crew".
   - `test_rail.py::TestRows::test_a_kit_with_a_bolt_told_and_nothing_waiting_is_a_row` checks the row's data and never renders it through `rail_text`.

4. **bolt-plan "Two holds on one kit": crew reads such a plan.** The scenario says crew refuses to read it, naming the holds. But `read()` runs only `recfix` (`plan.py:1009`), and recfix accepts two Holds naming one kit (`%unique` is per record). `check()`, which refuses them, runs only at a write, a proposal's apply and a join. Until the next write, crew acts on the last hold's words (`hold_on`).

5. **bolt-plan "A hold on a drive or a kit is put and lifted through crew": the drive's lift misses some cards.** The requirement says `crew plan go` hands "a raise of each landings card it held". With no `--repo`, the lift raises only kits with a started bolt (`plan.py:5547`). A kit whose card holds only a fix of main, with a send standing under the hold, is not raised, and its lands wait for the next rail read. No test covers it.

6. **Tasks 4.1 and 4.3 (`docs.2`): the docs still say every proven bolt waits for the user's send.** Each line below contradicts the new text beside it:
   - `README.md:18`: "it waits to land on the user's yes, a row of its kit's landings card".
   - `README.md:223`: ops lands the bolts "on the user's send on their kit's landings card".
   - `README.md:235`: the landings card has a row "for each proven bolt waiting on its main".
   - `README.md:70`: "asked, from the land crew posted on the user's send", where a land on proof is asked too.
   - `plugin/skills/crew/SKILL.md:10`: a proven bolt "waits to land, a row of its kit's landings card".
   - `plugin/bin/crew:135-139`: the `bolt submit` usage, "a bolt lands on the user's send of its row on its kit's landings card".
   - `plugin/roles/main-ops.md:29`: "tell the user that their send of the row on the kit's landings card lands it", true only of a bolt marked to stay.
   - crew's own words say the same:
     - `plan.py:4380`, a landing with no land asked: "it lands on the user's send of its row on its kit's landings card";
     - `submit_refused`, `plan.py:5033-5039`.

### Findings for the code stage to weigh

These are departures from the design and the rules. No scenario names them.

7. **A forecast that could not be made counts as clear.**
   - `landings_raised` keeps only conflicts found (`plan.py:4046`), and `proven` never reads `unmade` (`plan.py:4074`). So a bolt whose forecast failed lands on proof unattended.
   - Design Decision 1 says a row reads clear of main "only once that forecast found no conflict". `read.1` rules out a guess in a decision. Sluice still refuses a real conflict at the landing.
   - No test covers it.
8. **No re-check of the hold against the tip.** `lands_change` (`plan.py:3788`) does not look for a hold at the tip the write is applied to. A hold put while a raise runs does not stop that raise's lands. That breaks `plan.1`'s "its change function re-checks every precondition against the tip it is applied to".
9. **Smaller wording faults:**
   - A proof-only land row names no `swancloud-ops`, which crew-rail "The last unit merges" asks for. Its card line reads "none open".
   - `ops_view`'s line for a bolt with a landing record but no land row leaves out `stays` (`board.py:862`).
   - Under a hold:
     - an answered card that is followed closes saying "Asked of the runner as you ticked", though nothing was asked;
     - `crew card read` with no card open says "crew's next raise posts it".
   - A stopped land on proof's row says "Your send of it is spent", though no send was made.
10. **Outside these specs:** `crew kit rename` leaves Hold records alone. `rename_branch` renames `Source` only, and `rename_standing` does not refuse while a hold stands. A hold on a renamed kit would quietly stop holding.

### For the design agent, not the code stage

- `CLAUDE.md` *Proving and landing a bolt* still says "a bolt lands on the user's send of its row on its kit's landings card … and on nothing else". Record 0067 changes that.
- rail-cards "A yes frees the team for its next bolt" has no code in `plugin/`. This predates the change: the team machinery is gone. The MODIFIED text carries it unchanged.
