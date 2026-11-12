# A batch due is decided at the run record's tip

## Why

Overnight on 2026-11-11 to 12, wldn's proven bolts waited 400 to 1055 minutes for a landings card, because no batch of their changes was reviewed (signal `2026-11-12-agentplot-planner-237b59c7/01`). The planner was never told the next batch was due.

The cause is in `plugin/lib/plan.py`:

- `batch_check` decides from the read it is handed, the follower's kept read (`read["logs"]`).
- `record.emit` writes `batch.due` at the moment of writing.
- A read that predates the `review.batch` just delivered counts that batch's own changes as due. crew tells the planner, and writes a `batch.due` timed after the batch.
- `told_since_last_batch` then reads that entry as a tell since the last batch. It silences every later tell until the next `review.batch`.
- The planner, told of changes a batch already holds, finds nothing to review, so no next batch comes. `briefs.12`'s once-per-batch tell never fires again.

## What Changes

- **Decided at the tip.** Before it tells the planner, `batch_check` fetches the drive's branch and reads the run record at its tip, where the tip is newer than its read. It decides again there. A batch delivered since the read leaves nothing due by it, and the planner is not told.
- **A tip that cannot be read tells nothing.** It is said, and the follower tries again at its clock's next tick, as it does for a tell that did not go through (`read.1`).
- **A `batch.due` names its changes.** It records `Units`, each `<unit>:<bolt>@<commit>`, as a `review.batch` does.
- **A tell stands only while its changes are due.** A `batch.due` after the last batch keeps the next tell back only while a change it names is still due. An entry naming only changes a batch has since held silences nothing. An entry from before, which names its units alone, is judged by its units.
- README's account of batches and of the run record's fields says so.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `review-batches`: a batch due is decided at the run record's tip as the planner is told; a `batch.due` names its changes, and keeps the next tell back only while one of them is due.

## Impact

- `plugin/lib/plan.py`: `told_since_last_batch`, `batch_due`, `batch_check`, and a new `batch_reckoned` and `batch_entries_at_tip`.
- `tests/py/test_batches.py`, `tests/py/facts.py`: the cases.
- `README.md`: the batches paragraph and the run record's fields.
- Unchanged:
  - the views and crew's mod (`code.8`), since no view reads `batch.due`;
  - the command's usage (`docs.2`), since no command or flag changes.
