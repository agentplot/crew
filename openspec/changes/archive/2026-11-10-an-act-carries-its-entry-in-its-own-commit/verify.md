# Verify: an-act-carries-its-entry-in-its-own-commit

Verified on `change/an-act-carries-its-entry-in-its-own-commit` at 379d9c83, 2026-11-10.

## The whole checks

`tests/suite --affected` ran once, against the merge-base with main (586afa5c), as CLAUDE.md names it for a finished change. Result: **32 passed (32 replayed), 0 failed**, exit 0.

- The change edits crew's command core (`plugin/lib/plan.py`, `record.py`), so every task that takes it ran: `logic`, `contract` and all 30 end-to-end tasks. `t-journey-plan`, `t-journey-state`, `t-docs` and `t-specs` are among them.
- `mod` and the `nix` project's tasks were not selected. Their inputs (`plugin/hooks/`, `plugin/tests/`, the flake) are the same as at the merge-base.

Each replay is of a run that passed on this host with identical inputs. moon never replays a failed run.

`openspec validate an-act-carries-its-entry-in-its-own-commit --strict`: valid.

A trial archive in a scratch copy of the checkout's `openspec/` at 379d9c83 wrote:

- `drive-state`: 1 added, 2 modified, 1 removed;
- `run-record`: 5 modified.

`openspec validate --specs --strict` then gave **28 passed, 0 failed**. Each delta's MODIFIED and REMOVED header matches a requirement in `openspec/specs/`. Each requirement's text above its first scenario is under 500 characters (the longest is 490), so `t-specs` holds the specs once archived.

## Tasks

All 11 tasks of `tasks.md` are ticked and none are open. Each task's check is among the tasks that passed above.

- **1.1** `record.entry_text` and `record.with_entries` are plain functions (`code.7`).
  - `emit` composes through `fields_of` and `entry_text`, then `append`.
  - `unpushed` composes each step of its chain through `with_entries`.
  - `TestUnpushed` has the four cases the task notes name.
- **2.1** `write`'s `make` calls `carried`. That composes the act's entry, each ask's and each `also`'s at the tip being applied, and adds them to `runs/<host>/<day>.rec` through `w.replace(path, record.with_entries(w.text(path), …))`. The trailers name each one.
  - After `land`, each carried entry is appended to the host's file, then `record.reach(label, said=True)` runs.
  - A refused `land` raises before any append.
  - `tests/py/test_a_write_carries_its_entry.py` holds every case the task notes list, the rename case among them.
- **2.2** `init_step` carries its `state.init` entry the same way. `state_init`'s adoption still emits its own entry, naming `{repo}@{tip}`.
- **2.3** `plan_approve` inserts each applied op's entry into `w.also` at `Op.also_at`, with `frm` plus `proposal/<n>`. Nothing is emitted after the write.
  - `op_unit_add` puts the route's `signal.move` on `w.also`. Its `after` keeps the printed line.
  - `t-journey-plan` checks the approval's commit:
    - its diff adds `plan.approve`, `signal.move` and `unit.add`;
    - its trailers name those ids;
    - no `runs(` commit follows it for them.
- **2.4** `tests/contract/test_record.py`:
  - `test_a_plan_writes_commit_is_the_tip_holding_its_entry_and_one_given_no_act_moves_nothing`;
  - `test_a_write_refused_for_another_commands_entry_in_its_days_file_lands_on_top_with_both_entries_whole`.
- **2.5** `t-journey-state` checks four things:
  - a plan write's one commit changes `plan.rec` and `runs/mac-studio/<day>.rec`, carrying a `bolt.new` entry with no `Commit` that the host's file also holds;
  - a refused tell's kept entry follows the next write as its own commit, and nothing is pushed twice;
  - an entry cut short in the host's file stops no write, and its file is named on standard error;
  - `crew events --push` then says nothing is left.
- **3.1** None of these remain in `plugin/` or `tests/`: `fetch`, `read_point`, `decision_at`, `ARRIVAL`, `ENTRY_ID`, `entry_paths`, `entry_held`, `writer_of`, `below_said`, `below_read`, `Reading.keep_below`, `Reading.below`, `record.below`. Every read of a drive's branch is `tip_of`.
  - The names `board.in_flight`, `board.Fleet.fetch` and `ops.waited_on` remain. They predate the change and belong to other reads.
  - `plan.py`'s and `record.py`'s `__main__` exit with the refusal's words alone.
  - The logic tests that stood in `plan.fetch` now stand in `plan.tip_of`.
- **3.2** `test_an_older_crews_two_step_write_is_read_at_the_tip_its_entry_absent_until_its_own_commit_lands`.
- **3.3** `t-journey-plan`:
  - makes a two-step write by hand;
  - `crew plan proposed <n>` prints the later proposal and lacks "below its tip";
  - `crew events` prints the entry (`unit.order swb-1-conductor unit/a-drop`) once its own commit lands.
- **4.1** README says "every write is an act whose commit carries its entry", "names no commit of its own" and "a decision reads the branch at its tip". README, the crew skill and `plugin/bin/crew` lack "below its tip" and "below the tip". `t-docs` pins both.
- **4.2** The run above.

## Requirements and scenarios

### drive-state

- **A decision reads the drive's branch at its tip (added).** Every decision reads `tip_of`, and no read below the tip is left to say.
  - *A write whose entry has not arrived*: 3.3's case.
  - *The entry arrives later*: 3.2's and 3.3's cases.
- **Each commit names the run-record entry it describes or adds (modified).**
  - *From a commit to its entry*: 2.1's and 2.4's cases. Each `Crew-Entry` id is an `Id` the commit adds, and none names a commit.
  - *An approval's one commit*: 2.3's case.
  - *An entry's own commit*: 2.5's tell case. Its subject is `runs(mac-studio): tell agent/wldn-planner (<agent>)`, and it changes only the day file.
- **Every plan write is an act whose entry is pushed before it returns (modified).**
  - *Once a write returns*: 2.4's and 2.5's cases. The tip is the write's commit, holding the plan's change and the entry, and the host's file holds it too.
  - *A write applied again*: 2.4's refused-write case and 2.1's replay case.
  - *A write that names no act*: `unacted`, with cases in the logic and contract tiers.
- **A decision reads an act whole and says when it read below the tip (removed).** The code and its cases are gone with it.

### run-record

- **Every command that moves work leaves an entry (modified).**
  - *A plan write*: the `unit.add` entry is in the write's commit, by 2.3's case.
  - The other scenarios are behaviour this change leaves as it was.
- **An entry names the commit it wrote (modified).**
  - *A plan write*: `bolt.new` names no `Commit`, by 2.5's case.
  - *An approval*: unchanged. `crew record` and `crew unit approve` still emit naming the kit's commit.
  - *A tell*: unchanged.
- **Every entry reaches the branch as it is written (modified).**
  - *A plan write*: one commit and no `runs(` commit after it, by 2.3's and 2.5's cases.
  - *A tell*: 2.5's case.
  - *Two hosts at once*: the contract case of a push refused because another clone pushed first.
  - *A host is rebuilt*: `TestUnpushed`'s case of a host that lost its record.
- **An entry that did not reach the branch goes with the host's next (modified).**
  - *The next write* and *A write after an entry that fails its check*: 2.5's cases.
  - *A branch too busy*: the contract case of a busy branch.
  - *By hand*: `crew events --push` in `t-journey-state`.
- **A rename's entry reaches the branch and stands there as written (modified).** *The rename's one commit*: 2.1's rename case. The `bolt.land` entry is under `timber`, and the `kit.rename` entry is beside it with `From: kit/tailrace`.

### Rules

- `code.8`: no bolt, unit, stage, card or rail row changes shape. `board.agent_views` and `plugin/hooks/status.js` are untouched.
- `docs.7`: the change edits nothing under `docs/architecture/` or `docs/adr/`. The design's *Departures* names three things for the design agent to amend after the landing: `record.1`'s words, `read.5`'s reading of 2026-10-30 and `plan.2`'s built names.

## Observations, not blocking

- The archive warns that the proposal's Why section is longer than 1000 characters. `--strict` validation passes with it, and the spec deltas are what reaches `openspec/specs/`.

## Outcome

The whole checks pass, every task is done, and the work meets every requirement and scenario. The change is archived on this branch with this report.
