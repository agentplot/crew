# Tasks

## 1. Every plan write is an act with its entry

- [x] 1.1 `plan.write` records the entry its commit names before it returns, and refuses a write given no act before it reads or pushes anything (design, Decision 1; Task notes 1.1). Passes `tests/py/test_in_flight.py` (`tests/suite logic`) and `tests/contract/test_record.py` (`tests/suite contract`).
- [x] 1.2 Every plan write crew makes names its act, read from `plan.py` itself (design, Decision 2; Task notes 1.2). Passes `tests/py/test_in_flight.py` (`tests/suite logic`).
- [x] 1.3 A command that read a drive's branch below its tip says so, naming the commit it read at, the tip, the write it waits on and that write's agent, on the line before its refusal and on standard error after its answer (design, Decisions 3 and 4; Task notes 1.3). Passes `tests/py/test_in_flight.py` and `tests/contract/test_record.py`; verify `tests/suite t-journey-plan` ends with "0 failed".
- [x] 1.4 README, the crew skill and `crew`'s usage header say that every write is an act and that a read below the tip says so (`docs.2`; Task notes 1.4). Verify `tests/suite t-docs` ends with "0 failed".

## 2. The change's tests

- [x] 2.1 The tests the change affects pass. Verify `tests/suite --affected` ends with "0 failed".
