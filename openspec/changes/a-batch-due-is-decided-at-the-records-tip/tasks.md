# Tasks

Each check is a moon task of the `tests` project, run through `tests/suite`: `logic` is `tests:logic`. Submit nothing, and never run `wt submit --help`.

## 1. A batch due is decided at the run record's tip

- [ ] 1.1 A `batch.due` after the drive's last batch keeps the next tell back only while a change it names is still due, by its `Units`, or by its units in an entry from before (design Decision 2; Task notes 1.1). Passes `tests/py/test_batches.py` (`tests/suite logic`).
- [ ] 1.2 When its read finds a batch due, `batch_check` decides again from the run record at the branch's tip fetched then: a batch delivered since the read leaves no tell and no `batch.due`, the next due change is told, a tip it cannot read tells nothing and answers not told, and a tell's entry names its changes as `Units` (design Decisions 1 to 3; Task notes 1.2). Passes `tests/py/test_batches.py` (`tests/suite logic`).
- [ ] 1.3 README says a batch due is decided again at the branch's tip before the tell, that a tell keeps the next back only while a change it names is due, and names a batch due's `Units` among the run record's fields (Task notes 1.3). Verify `tests/suite t-docs t-journey-review` ends with "0 failed".

## 2. The tests the change affects

- [ ] 2.1 Verify `tests/suite --affected` ends with "0 failed".
