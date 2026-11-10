# An act carries its entry in its own commit

## Why

A write to a drive's branch reaches it in two commits: the act's, whose `Crew-Entry` names an entry, and then the entry's own commit, which adds it to `runs/<host>/<day>.rec`. Between them the branch holds half an act. Chore b429b20c (2026-10-30) made every decision read below a write whose entry was a commit behind it, so that half was never read: `plan.fetch` reads the branch at the parent of the oldest of its newest twenty commits whose entry the tip lacks (`read_point`, `decision_at`, `ARRIVAL`), and a command read there says so (`below_said`).

That read holds as long as the entry is missing. wldn-planner's signal of 2026-11-10, `crew-read-held-behind-a-write-without-run-record`, found reads held ten minutes and more three times on 2026-11-09 and 11-10 (86faafb, 057291e, 029a85e), each below a write whose entry's push failed every retry. Nothing recovers an entry whose writer died: the read waits until the write passes out of the twenty commits it looks through.

The hold is there only because an act and its entry are two commits. Record 0029 (accepted) has the run record read from the branch alone and every entry reach it as it is written (`read.5`). State writes are one commit each and are applied again on a refused push (`state.1`). An act that writes the branch can put its entry in that same commit. Then the branch never holds an act without its entry, and a decision reads the tip.

## What Changes

- **A write carries its entries.** An act that writes a drive's branch appends its run-record entry to its host's `runs/<host>/<day>.rec` in the write's own tree. That covers a plan write, a state init step and the acts an approval applies. Each ask, each further act and each route move the write makes goes in the same tree, beside the plan's change. The entries are composed again with the write on every replay of a refused push (`state.1`). The commit's `Crew-Entry` trailers name each entry it carries (`plan.2`).
- **Such an entry names no `Commit` of its own.** The commit carrying it is its commit. An entry still names any commit an act wrote elsewhere, in a kit, and the tip a state init adopted.
- **Once the push is accepted**, the write appends its entries to the host's own file (`record.4`). Then it pushes any of the host's entries a refused push left, each as its own commit. A refusal of those is said once and changes nothing (`record.2`).
- **Every decision reads the branch at its tip.** The read below a write whose entry has not arrived goes: `fetch`, `read_point`, `decision_at`, `in_flight`, `waited_on`, `ARRIVAL`, `entry_paths`, `entry_held`, `ENTRY_ID`, `writer_of`, `below_said`, `below_read`, `Reading.keep_below` and `Reading.below`, and `record.below`. Every read of a branch's tip is `tip_of`. A commit an older crew wrote in two steps is read at the tip like any other, and its entry joins the record whenever it arrives.
- **Unchanged:** an act that writes no branch (a tell, a send, a launch, a card's post), and an act refused before its write, push their entry as its own commit, as now. A write still refuses one given no act (`unacted`).
- README, the crew skill and `plugin/bin/crew`'s header drop the read below the tip and say a write's entry is in its commit.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `drive-state`: a write's commit carries its entries. A decision reads the branch at its tip and never says it read below it.
- `run-record`: an act that writes the drive's branch leaves its entry in that commit, naming no commit of its own. A rename's entry is in the rename's commit. A write after a refused push pushes the host's kept entries after it.

## Impact

- `plugin/lib/plan.py`: `write`, `init_step`, `plan_approve`, `op_unit_add`, `asked`, `Write`, `land`'s callers; the read below the tip, removed; every `fetch` caller reading `tip_of`; the `__main__` exit.
- `plugin/lib/record.py`: an entry's text and a day file's text composed apart from `emit`'s append; the host's own append of entries a write carried; `on_branch` reading `tip_of`; `below`, removed.
- `plugin/lib/board.py`, `plugin/lib/ops.py`: their `plan.fetch` reads `plan.tip_of`.
- `plugin/bin/crew` (its header), `README.md`, `plugin/skills/crew/SKILL.md`.
- `tests/py/test_in_flight.py`, `tests/py/test_landings.py`, `tests/py/test_record.py` and each logic test that stood in `plan.fetch`; `tests/contract/test_record.py`; `tests/t-journey-state.sh`, `tests/t-journey-plan.sh`.
- Unchanged: crew's mod and the agents' views (`code.8`), since no bolt, unit, stage, card or rail row changes shape. `crew events`, `crew trace` and the page print an entry's commits as it names them.
