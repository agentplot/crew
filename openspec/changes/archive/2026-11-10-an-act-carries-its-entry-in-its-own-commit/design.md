# Design

## Context

**How a write reaches the branch today**, read in `plugin/lib/plan.py` and `plugin/lib/record.py` on 2026-11-10:

- `write` makes an id ahead (`record.new_id`) and applies the change at the tip. It commits the change's files under a message whose `Crew-Entry` names that id, each ask's (`w.asked`) and each further act's (`w.also`). Then `land` pushes it, applying it again on a refused push.
- Only after the push does `write` call `record.emit` for each named entry, naming the write's commit in `Commit`. Each `emit` appends to the host's file and `record.reach` pushes the entries the branch lacks, each as its own commit.
- `init_step` does the same for a state init's steps. `plan_approve` emits each applied command's entry after the write, and those entries go unnamed in its trailers. `op_unit_add`'s `after` emits the route's `signal.move` the same way.
- So every act on the branch is two commits, and between them the branch holds an act whose entry it lacks.

**The read below it.** Chore b429b20c (2026-10-30) made `fetch` read a branch at `read_point`. That is the parent of the oldest of its newest `ARRIVAL` (twenty) first-parent commits whose `Crew-Entry` the tip's files lack (`decision_at`, `in_flight`, `entry_paths`, `entry_held`). `below_said`, `below_read`, `Reading.keep_below` and `record.below` then say so with the command's answer.

**Where it held.** wldn-planner's signal of 2026-11-10, `crew-read-held-behind-a-write-without-run-record`, found reads held ten minutes and more three times on 11-09 and 11-10 (86faafb, 057291e, 029a85e). Each time the write's entry push had failed every retry. An entry whose writer died is recovered by nothing, so the read waits until the write passes out of the twenty commits.

**Who writes the branch**, by grep of `plugin/` for `land(` and for entries naming a state repository's commit:
- `write`, with its asks, its `also` acts, an approval's commands and a unit add's route move;
- `init_step`;
- `state_init`'s adoption of a blueprints branch's history, a push of commits crew did not make;
- `record.reach`, the entries' own commits.

`record.accepted` names a kit's commit. No other module writes the branch.

**Area pages this change touches:** `core.md` (`state.1`, `state.4`, `read.5`, `code.7`, `code.8`, `code.9`), `plan.md` (`plan.1`, `plan.2`), `record.md` (`record.1`, `record.2`, `record.3`, `record.4`), `tests.md` (`tests.4`, `tests.11`), `docs.md` (`docs.2`, `docs.7`). This change edits no rule page (`docs.7`).

## Goals / Non-Goals

**Goals:**
- An act that writes a drive's branch has its entry in that commit, so the branch never holds an act without its entry.
- Every decision reads a branch at its tip, and nothing says it read below it.
- A commit an older crew wrote in two steps is read at the tip, its entry joining the record whenever it arrives.

**Non-Goals:**
- Carrying the host's kept entries in a write's commit. The carry clause stays gone (`plan.2`).
- Changing how an act that writes no branch pushes its entry.
- Reading, for each entry, the commit that carries it.

## Decisions

### 1. The write's tree carries every entry of its acts

In `write`'s `make(tip)`, once the change has run and been checked, each entry of the write is composed and added to the host's `runs/<host>/<day>.rec` in the write's own files. That covers the act's entry, each ask's, and each `also` act's.
- The day file is the file as the change has left it (`Write.text`): replaced, else at the tip. Its entries and the write's are joined by `Id` in `Id` order under crew's descriptor, as `record.unpushed` joins them (`record.4`).
- `land` checks it with every other file the commit holds (`plan.1`), and a refused push applies the whole again to the new tip (`state.1`). A replay's entries are composed again there, so another command's entry in that file stays as it was.
- The commit's `Crew-Entry` trailers name each entry it carries (`plan.2`).
- The act's id is made once per write, as now. Each entry's `At` is the moment of the application that composes it, and its file is that host's file for `At`'s UTC day.

Not taken:
- **An entry's own commit before the act's.** It is still two commits, with the same half state the other way round.
- **Carrying the host's kept entries too.** One kept entry cut short would fail the write's check and refuse the act, which `record.2` rules out.

### 2. One composition of an entry and of a day file

Two functions of plain facts in `record.py` (`code.7`):
- an entry's text from its fields, which `emit` composes through;
- a day file's text with entries added, which `unpushed` composes through.

The write and `emit` make one shape of entry, and the write and `reach` make one shape of file.

### 3. Every act a write holds is carried

- `plan_approve`'s change puts each applied command's entry on `w.also`, with its `On`, its `From` (`proposal/<n>` among them), its `Why` and its fields. It no longer emits them after the write. This makes an approval's commit name every act it holds.
- `op_unit_add`'s change puts the route's `signal.move` on `w.also`, so its entry rides the commit that holds the move. Its `after` keeps only its line of output.
- `w.also` takes a `From`.
- `init_step` carries its `state.init` entry as `write` carries an act's.
- `state_init`'s adoption pushes commits crew did not make. Its `state.init` entry stays a commit of its own, naming the adopted tip.

### 4. An entry carried in its act's commit names no `Commit`

The commit carrying it is its commit, and a commit cannot name its own sha. The entry still names any commit an act wrote outside the drive's branch: the kit's for an approval or a record.
- `crew events`, `crew trace` and the page print an entry's commits as it names them, so a carried entry shows `-`.
- `git log --grep "Crew-Entry: <id>"` finds the commit from the entry, and the trailer goes the other way (`plan.2`).

Not taken: finding each entry's carrying commit on every read of the record. That is a `git log` over the record's window, paid by every refresh of the follower (`plan.12`).

### 5. After the push: the host's own file, then what a refused push left

Once `land` returns, the write appends each entry it carried to the host's own file (`record.4`): one write each, after the descriptor, as `emit` appends. A failed append is said once and changes nothing (`record.2`).

Then the write runs `record.reach` in its said mode, which pushes, each as its own commit, the host's entries the branch still lacks. Normally there are none, and it pushes nothing, reading the tip the write left with no fetch. A refusal is said once and changes nothing (`record.2`). A cut-short entry in the host's file fails that push and not the write.

A refused write writes nothing locally. The command's refusal is recorded by `refused` as its own commit, as now (`record.1`).

### 6. Every decision reads the tip

These go:
- `fetch`, `read_point`, `decision_at`, `in_flight`, `waited_on`, `ARRIVAL`;
- `entry_paths`, `entry_held`, `ENTRY_ID`, `writer_of`;
- `below_said`, `below_read`, `Reading.keep_below`, `Reading.below` and `record.below`, with the `read-point-` and `waits-` readings.

Every caller of `fetch`, in `plan.py`, `record.on_branch`, `board.py` and `ops.py`, reads `tip_of`. `plan.py`'s and `record.py`'s entry points exit with a refusal's words alone.

Not taken: keeping `fetch` as a second name for `tip_of`, which leaves two names for one read.

### 7. A two-step commit of an older crew is read at the tip

A host whose crew is older than this change still writes an act and then its entry. Read at the tip, such an act is half there until its entry arrives.
- For b429b20c's case, a landings card's close read in between says "Landed or left the plan: y." where it would have said where y landed.
- The card closes either way, and only its words lack the head.
- That lasts until every host that writes the drive runs a crew that carries its entry.

The brief accepts it: "a commit an older crew wrote in two steps is read at the tip like any other, its entry joining the record whenever it arrives."

### Rules relied on

- `state.1`: a write is one commit applied again to the new tip on a refused push, its entries composed again with it.
- `plan.1`: the carried day file is checked with every file the commit holds.
- `plan.2`: the subject ends with ` (<agent>)`, and the trailers name every entry the commit carries.
- `record.2`: a local append or a kept entry's push that fails is said once and changes nothing.
- `record.3`: a carried entry holds no typed text, composed as `emit` composes it.
- `record.4`: a host adds only to its own file, and the branch's file is the union by `Id`. A rename's rewrite is the base its entry is added to.
- `read.5`: the record is read from the branch alone. Its words "every entry reaches the branch as it is written, as its own commit from the host that wrote it" hold: a write's commit is from that host and is the commit of the entry it carries.
- `code.7`: composing an entry and a day file are decisions of facts, and the git calls stay in `land`.
- `code.9`: a write answers once its one push is accepted, one push sooner than today.
- `code.8`: no bolt, unit, stage, card or rail row changes shape, so `board.agent_views` and `status.js` are untouched.

### Departures

- **`record.1`** has an entry appended "after the act". Where the act writes the branch, it is now with the act, in its commit. The rule's words become: "Every command that moves work appends one entry per act, done or refused: with the act, in its commit, where it writes the drive's branch, and after it otherwise; a pure read appends nothing."
- **`read.5`'s details** read on 2026-10-30 that a decision reads the branch at the newest commit whose entry has arrived. That reading goes: an act carries its entry in its commit, so a decision reads the tip. Source: wldn-planner's signal of 2026-11-10.
- **`plan.2`'s details** name `decision_at`, `read_point`, `waited_on`, `below_said` and `below_read` as built. They go with this change.

The design agent writes these on the pages once this lands (`docs.7`).

## Risks / Trade-offs

- **A writer that dies between its push and its local append** leaves the branch holding an entry its host's file lacks. → The record is read from the branch alone (`read.5`), and `unpushed` pushes only what the branch lacks, so nothing is lost or pushed twice.
- **An older crew's two-step writes are read half** until their entries arrive. → Decision 7. The window is seconds, unless the entry's push fails, as before b429b20c.
- **`crew events` shows `-` for a carried entry's commit.** → Decision 4. The trailer and `git log --grep` link them.

## Migration Plan

None. Entries already on the branch are read as written, and an older crew's two-step commits are read at the tip.

## After deploy

None. Every outcome is a logic, contract or end-to-end case. A host reaches this with its next crew release or live move.

## Task notes

**1.1** `plugin/lib/record.py`:
- `entry_text(fields)` gives an entry's lines from its `[(key, value)]`, one line each, in `emit`'s order. `emit` builds its fields and composes through it.
- `with_entries(text, blocks)` gives a day file's text with `blocks` (`{Id: lines}`) added. It is the union by `Id` of what `text` holds (`blocks`'s parse) and the new blocks, in `Id` order, under `DESCRIPTOR`. `unpushed` composes each chain step through it.

Cases in `tests/py/test_record.py` `TestUnpushed`:
- an entry's text is `emit`'s;
- a file with an entry added keeps every entry it held, as it was, in `Id` order;
- adding an entry the file holds changes nothing;
- a file that is `None` becomes the descriptor and the entry.

**2.1** `plugin/lib/plan.py` `write`. In `make(tip)`, after `check` and `appended`:
- the act's entry (`seen["eid"]`, the act, `on`, `frm`, `why`, the fields), each ask's (`record.ask_entry`) and each `also`'s are composed by `record.entry_text`;
- they are added to `runs/<host>/<At's day>.rec` through `record.with_entries` on `w.text(path)`, and replaced in `w.files`;
- no `Commit` names the state repository.

After `land`: `record.append` (the append half of `emit`, which `emit` now calls) writes each carried entry to the host's file, then `record.reach(label, said=True)`. `asked` prints its lines and emits nothing.

Cases in `tests/py/test_a_write_carries_its_entry.py`, which `tests/py/test_in_flight.py` becomes, keeping its two cases of `unacted` and of every write naming its act. `plan.land` is stood in to run `make` on fake tips, with `plan.show`, `plan.read` and `record.reach` stood in:
- the commit's files hold the plan and the host's day file with the act's entry;
- an ask's and an `also`'s entries are there, each named in a trailer;
- no entry names a `Commit`;
- a replay on a tip whose day file gained another entry keeps that entry;
- a change that replaced the day file has the entry added to its text. The case is `crew kit rename tailrace timber`'s change on a tip whose `runs/deneb/<day>.rec` holds a `bolt.land` under `tailrace`, the host deneb. The commit's file holds that entry under `timber` and the `kit.rename` entry beside it with `From: kit/tailrace`;
- after the push the host's file holds the entries and `reach` ran said;
- a refused `land` leaves the host's file as it was.

**2.2** `init_step` carries its `state.init` entry as `write` does. `state_init`'s adoption is unchanged. A case in the same file, `land` stood in.

**2.3** `plan_approve`'s change appends each op's entry to `w.also`: its `act`, `on + added_on`, `frm + added_frm + [proposal/<n>]`, `record.subject(op.subject)` as `Why` and `op.fields`. The emit after the write goes, and `op.after` stays. `w.also` entries take `frm` (the tuple gains it, or `more["frm"]`), and `write` composes it. `op_unit_add`'s change appends the `signal.move` to `w.also` with its `On` and `Why`, and its `after` keeps the printed line.

`tests/t-journey-plan.sh`, after the approval of the proposal holding `unit add … --signal`:
- the act's commit (`act_tip`) adds the `plan.approve`, `unit.add` and `signal.move` entries to the host's day file;
- its trailers name the three;
- no `runs(` commit follows it for them.

**2.4** `tests/contract/test_record.py`, against the bare repository standing for GitHub:
- `test_a_plan_write_is_read_at_the_tip_it_leaves_…` becomes one case: the write's commit is the tip, its tree's day file holds its entry (`bolt.new`, `On: bolt/b`, no `Commit`), its trailer names it, and the host's file holds it;
- a new case: a write whose push is refused because another clone pushed an entry to the same host's day file lands on top with both entries whole, and the file passes `recfix --check`;
- the module docstring says so.

**2.5** `tests/t-journey-state.sh`:
- the plan write's case: `wldn/main`'s tip changes `plan.rec` and `runs/mac-studio/<day>.rec`, its trailer names the `bolt.new` entry, which names no `Commit`, and the host's file holds it;
- the refused-push case: a tell's entry is refused, the next plan write lands with its own entry, the tell's entry follows as its own commit, and nothing is pushed twice;
- a host file holding an entry cut short does not stop a plan write, and the command names the file on standard error.

**3.1** In `plugin/lib/plan.py`, `fetch`, `read_point`, `decision_at`, `in_flight`, `waited_on`, `ARRIVAL`, `ENTRY_ID`, `entry_paths`, `entry_held`, `writer_of`, `below_said`, `below_read`, `Reading.keep_below` and `Reading.below` go. Every `fetch(` caller calls `tip_of(` with the same arguments.

`record.on_branch`, `board.py`'s and `ops.py`'s `plan.fetch` call `plan.tip_of`. `record.below` goes. `plan.py`'s `__main__` exits `sys.exit(str(e))` on a refusal and nothing more on a stop, and `record.py`'s likewise.

In the logic tests:
- each test that stood in `plan.fetch` stands in `plan.tip_of`: `test_asks.py`, `test_kits.py`, `test_proposal_life.py`, `test_proposal_card.py`, `test_cards.py`, `test_review.py`, `test_landings.py`;
- `test_landings.py`'s `test_a_landing_whose_entry_is_still_in_flight_…` loses its `decision_at` lines and keeps its `landings_step` cases, named for what they hold;
- the read-below cases of the former `test_in_flight.py` go.

**3.2** `tests/contract/test_record.py`: `test_a_branch_is_read_below_a_write_whose_entry_is_in_flight_…` becomes a two-step write, its entry not yet there. `tip_of` reads the tip, and `record.at` at the tip lacks the entry until its commit lands, then holds it.

**3.3** `tests/t-journey-plan.sh`: the in-flight case becomes a hand-made two-step write. `crew plan proposed <n>` prints the proposal written after it and nothing of a read below. Once the entry's commit lands, `crew events` prints the entry.

**4.1** README's state paragraph (the one beginning "Drives sharing a repository never meet") and its run-record paragraph ("Every entry reaches the drive's branch as it is written"):
- a write's commit carries its entry, which names no commit of its own;
- an act that writes no branch pushes its entry as its own commit;
- a decision reads the tip;
- the read below the tip goes.

The crew skill's *Read below the tip* bullet goes, and `plugin/bin/crew`'s header loses its paragraph on it. No command's usage changes (`docs.2`).

`tests/t-docs.sh` pins the change in its opening comment and its cases:
- README says a write's commit carries its entry;
- README, the skill and `plugin/bin/crew` lack "below its tip".
