# Tasks

Each check is a moon task of the `tests` project, run through `tests/suite`: `logic` is `tests:logic`, `contract` is `tests:contract`, and an end-to-end test runs by its name. Build the groups in order. Submit nothing: Flume submits the place once its last stage delivers.

## 1. One composition of an entry and a day file

- [x] 1.1 An entry's text and a day file's text with entries added are composed by two functions of plain facts in `record.py`, which `emit` and `unpushed` compose through (design Decision 2; Task notes 1.1). Passes `tests/py/test_record.py` (`tests/suite logic`).

## 2. A write carries its entries

- [x] 2.1 A plan write's commit adds the entries of its act, its asks and its further acts to its host's day file in its own tree, made again on each replay, named in its trailers and naming no `Commit`, and once its push is accepted the host's own file holds them and the host's kept entries are pushed after it (design Decisions 1, 4 and 5; Task notes 2.1). Passes `tests/py/test_a_write_carries_its_entry.py` (`tests/suite logic`).
- [x] 2.2 A state init step's commit carries its `state.init` entry, while an adoption's entry stays a commit of its own naming the tip it adopted (design Decision 3; Task notes 2.2). Passes `tests/py/test_a_write_carries_its_entry.py` (`tests/suite logic`).
- [x] 2.3 An approval's one commit carries and names the entry of each command it applies, a unit add's route move among them (design Decision 3; Task notes 2.3). Verify `tests/suite t-journey-plan` ends with "0 failed".
- [x] 2.4 Against a bare repository standing for GitHub, a plan write's commit is the tip holding its entry, and a write refused because another command of the same host pushed an entry to that day's file lands on top with both entries whole (design Decision 1; Task notes 2.4). Passes `tests/contract/test_record.py` (`tests/suite contract`).
- [x] 2.5 Through the `crew` command, a plan write's one commit changes the plan and the host's day file with an entry naming no commit, a tell's kept entry follows the next write as its own commit, and an entry cut short in the host's file stops no write (design Decisions 1 and 5; Task notes 2.5). Verify `tests/suite t-journey-state` ends with "0 failed".

## 3. Every decision reads the tip

- [ ] 3.1 Every read of a drive's branch is `tip_of`, with the read below a write whose entry has not arrived gone from `plan.py` and `record.py` and every logic test that stood in `plan.fetch` standing in `plan.tip_of` (design Decision 6; Task notes 3.1). Verify `tests/suite logic` ends with "0 failed".
- [ ] 3.2 An older crew's two-step write is read at the tip, its entry absent from the record until its own commit lands (design Decision 7; Task notes 3.2). Passes `tests/contract/test_record.py` (`tests/suite contract`).
- [ ] 3.3 `crew plan proposed` prints a proposal written after an older crew's two-step write whose entry has not arrived, saying nothing of a read below the tip, and `crew events` prints the entry once it lands (design Decision 7; Task notes 3.3). Verify `tests/suite t-journey-plan` ends with "0 failed".

## 4. The docs and the tests the change affects

- [ ] 4.1 README, the crew skill and `plugin/bin/crew`'s header say a write's commit carries its entry and a decision reads the tip, and none of them speaks of a read below the tip (Task notes 4.1). Verify `tests/suite t-docs` ends with "0 failed".
- [ ] 4.2 Verify `tests/suite --affected` ends with "0 failed".
