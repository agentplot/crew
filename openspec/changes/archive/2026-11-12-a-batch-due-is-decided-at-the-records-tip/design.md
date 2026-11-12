# Design

## Context

**What went wrong.** Overnight on 2026-11-11 to 12, wldn's proven bolts waited 400 to 1055 minutes for a landings card (signal `2026-11-12-agentplot-planner-237b59c7/01`). A bolt is offered for landing only once each unit's latest change has been in a batch the user answered (`briefs.12`), and no next batch was reviewed.

**The code**, `plugin/lib/plan.py` on main at `461c2f6e`:

- `reckon_batches` runs `batch_check` for each drive whose main level runs on this host, at every refresh of the host's follower. It hands over the follower's kept read: the plan, the stages and the run record (`read["logs"]`), as the branch stood at the read's tip.
- `batch_check` counts the due changes from that read (`due_changes`), and asks `batch_due` whether they make a batch due. Both skip when `told_since_last_batch` finds a `batch.due` after the newest `review.batch`.
- When a batch is due, `batch_check` tells the planner (`crew.tell`), then writes `batch.due` through `record.emit`, timed at the moment it is written.

**The race.** A follower's read takes seconds, and a kept read stands until the follower's next look sees the branch move. Suppose a `review.batch` reaches the branch after the read but before the tell:

1. The read still counts the batch's own changes as due, so the planner is told, and a `batch.due` is written after the batch.
2. `told_since_last_batch` reads that entry as a tell since the last batch, and every later tell is kept back until the next `review.batch`.
3. The planner, told of changes a batch already holds, finds none due: `crew review` refuses, "no change of wldn is due".
4. So no next batch comes, and the drive's later changes are never told.

**Where else this is done.** No other tool of the Boomdrive family tells a planner of a batch. The review batch is crew's alone (`briefs.12`). The pattern this design takes is crew's own write protocol: a write is applied at the tip it lands on, and its change function re-checks every precondition there (`state.1`, `plan.1`).

**Area pages this change touches:**

- `core.md`: `state.1`, `state.4`, `read.1`, `read.5`, `code.7`, `code.8`;
- `plan.md`: `plan.1`, `plan.12`;
- `record.md`: `record.1`, `record.3`;
- `tests.md`: `tests.4`, `tests.11`;
- `docs.md`: `docs.2`, `docs.7`.

No rule page is edited by this change (`docs.7`).

## Goals / Non-Goals

**Goals:**

- No `batch.due` is written from a read that lacks the newest `review.batch`.
- No `batch.due` naming only changes a batch already held keeps a later tell back, whether this crew wrote it in a race it could not close, or an older crew wrote it.
- The follower still finds a batch due from its kept read, reading nothing (crew-board "A batch made due by the hours").

**Non-Goals:**

- Re-reading the plan or the stages at the tip. A delivered batch moves the run record, not the plan's units or their stages.
- Changing when a batch is due, or what the planner is told.

## Decisions

### 1. A batch due is decided again at the tip before the tell

When its read finds a batch due, `batch_check` fetches the drive's branch (`tip_of(..., fresh=True)`). Where the tip is not the one its read holds, it reads the run record there (`drive_entries`) and decides again, with the same plan, stages and clock. Only a batch still due at the tip is told and recorded.

- **The decision is a function of facts** (`code.7`). `batch_reckoned(plan, entries, st, crossing, setting, now)` gives the due changes and why a batch is due. The read and the act around it stay thin.
- **The read finds, the tip confirms.** The follower still finds a batch due from its kept read, reading nothing. Only a tell, at most once per batch and once a tick for one that did not go through (`batch_told`), costs one fetch. That fetch is the one a write makes before it lands (`state.1`), so `plan.12`'s idle host still idles.
- **The fetch moves crew's cache of the branch**, so the follower's next look sees the move and reads afresh. A read left behind by a batch is fetched for once, not at every refresh.

Not taken:

- **Deciding inside the write's replay** (`land`'s change function). The tell is an act outside git that cannot be replayed, and `record.1` writes its entry after the act.
- **Reading this host's unpushed entries beside the branch.** `read.5` reads the run record from the branch alone.

### 2. A `batch.due` names its changes, and keeps the next tell back only while one is due

A window remains between the read at the tip and the entry, while `crew.tell` reaches herdr. Records already hold entries the race wrote. So:

- **`batch.due` records `Units`**, each `<unit>:<bolt>@<commit>`, the field and form `review.batch` writes, composed from names (`record.3`).
- **`told_since_last_batch(entries, due)`** counts a `batch.due` after the newest `review.batch` only while a change it names is still due:
  - by `(unit, commit)` where it names `Units`;
  - by unit where it names only `On: unit/<u>`, as entries from before do.

A tell that stands names the changes still due, so it keeps the next tell back as before, until a batch is delivered.

Not taken: **counting an entry unless a batch holds every change it names.** It would keep a tell standing whose changes were all built again or dropped, though the planner can review none of them. What a tell is about is what is due.

### 3. A tip that cannot be read tells nothing until the next tick

When the fetch or the read at the tip is refused, `batch_check` tells nothing and writes nothing (`read.1`). It says why on standard error, which the follower keeps as what its refresh said, and answers that the planner was not told. The follower then reckons the drive again only at its clock's next tick (`batch_told`), as it does for a tell that did not go through, so an unreachable GitHub costs one fetch a minute.

### Rules relied on

- `state.1`, `plan.1`: a write's preconditions are checked again at the tip it lands on.
- `read.1`: an unreadable tip refuses, never a default.
- `read.5`: the run record is read from the branch alone.
- `record.1`, `record.3`: one entry after the act, composed from names.
- `code.7`: the decision is a function of facts, tested in the logic tier.
- `code.8`: no view reads `batch.due`, so the views and the mod are untouched.
- `plan.12`: the follower's refresh reads nothing to find a batch due; only a tell fetches.
- `tests.4`: the reproducing case is in the logic tier.

### Departures

None.

## Risks / Trade-offs

- **[A batch delivered after the tip's fetch and before the entry]** → the entry names changes no longer due, and Decision 2 keeps it from holding the next tell back.
- **[The tip's read is the whole record since `BATCH_DAYS`]** → it is read only at a tell, at most once per batch, as `crew review` reads it.

## Migration Plan

None. A `batch.due` already on a branch, naming its units alone, is judged by its units (Decision 2), so a stale one stops holding the planner back once crew at this change runs on the drive's main-level host.

## After deploy

None: every outcome here is a logic-tier case, and nothing waits on a host or on the user.

## Task notes

**1.1** `plugin/lib/plan.py`:

- `told_since_last_batch(entries, due)`: a `batch.due` after the newest `review.batch` counts while a change it names is still due. Its `Units` are read with `units_of_batch` and matched by `(unit, commit)` against `due`. With no `Units`, its `On: unit/<u>` are matched by unit.
- `batch_due` passes `due` through.
- Cases in `tests/py/test_batches.py` `TestBatchDue`:
  - an entry naming due changes keeps the tell back;
  - one naming only changes a batch held keeps nothing back;
  - one from before naming units no longer due keeps nothing back, and one naming a due unit keeps the tell back.
- `facts.told` takes the changes it names.

**1.2** `plugin/lib/plan.py`:

- `batch_reckoned(plan, entries, st, crossing, setting, now)` gives `(due, why)`, from `due_changes` and `batch_due`, with the bolts as `batch_check` builds them.
- `batch_entries_at_tip(fleet, label, read_at)` fetches the branch fresh (`tip_of(repo, ref, fresh=True)`). It gives `None` when the tip is `read_at`, else `drive_entries` at the tip.
- `batch_check` reckons from its read, and when a batch is due, reckons again from the tip's entries where they differ.
  - Nothing due there: it returns `None`, telling nothing.
  - A refused read at the tip: it says `no batch told for <label>: <why>` on standard error and returns `False`.
  - A tell: it records `Units` on `batch.due`.
- Cases in `tests/py/test_batches.py`:
  - the follower's reckoning tells from its read when the tip is the read's, fetching the tip and reading nothing else;
  - a `review.batch` at the tip that the read lacks leaves no tell and no entry, and a read holding it and newer due changes is told;
  - a refused fetch tells nothing, says why and answers `False`;
  - the entry carries `Units`.

**1.3** `README.md`: the batches paragraph says the batch is decided again at the branch's tip before the tell, and that a tell keeps the next back only while a change it names is due. The run record's fields name a batch due's `Units`.
