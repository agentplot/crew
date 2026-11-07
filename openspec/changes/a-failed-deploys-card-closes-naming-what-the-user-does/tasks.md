# Tasks

Each check is a moon task of the `tests` project, run through `tests/suite`: `logic` is `tests:logic`. Build the groups in order. Submit nothing, and never run `wt submit --help`.

## 1. A failed deploy's close names what the user does

- [x] 1.1 The run record takes the field `Does` (design Decision 1; Task notes 1.1). Passes `tests/py/test_record.py` (`tests/suite logic`).
- [x] 1.2 `crew ops record` takes `--does <words>` on every act and keeps the words on its entry, refused for none of them (design Decision 1; Task notes 1.2). Passes `tests/py/test_ops.py` (`tests/suite logic`).
- [x] 1.3 A failed deploy's close names, after the step that failed and its log, the words the end was handed; with none, or ending well, it closes as today (design Decisions 2 and 3; Task notes 1.3). Passes `tests/py/test_ops.py` (`tests/suite logic`).

## 2. The how-to

- [x] 2.1 README's `crew ops record` line and its paragraph name `--does` and the close it gives (`docs.2`; Task notes 2.1). Passes `tests/t-docs.sh` (`tests/suite t-docs`).

## 3. The tests the change affects

- [ ] 3.1 Verify `tests/suite --affected` ends with "0 failed".
