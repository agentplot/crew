# Tasks

Each check is a moon task of the `tests` project, run through `tests/suite`: `logic` is `tests:logic`, `contract` is `tests:contract`. Build the groups in order. Submit nothing: Flume submits the place once its last stage delivers.

## 1. The decisions

- [x] 1.1 runner.py gives a name's Flume branch, the repositories a launch of the kit's work would be made in, what stands there, the refusal naming the branch, where it stands and the ways on, and the drop's words (design Decisions 2, 4, 5 and 6; Task notes 1.1). Passes `tests/py/test_branch_stands.py` (`tests/suite logic`).
- [x] 1.2 An add, a chore's add and a split's new names are refused at a proposal's writing, at its approval and on a direct run while Flume's branch for the name stands where a launch would be made, nothing written, a fresh name passing and a drawn card reading nothing (design Decisions 1 and 3; Task notes 1.2). Passes `tests/py/test_branch_stands.py` (`tests/suite logic`).
- [x] 1.3 A drop of launched work prints that Flume keeps its branch and the name stays taken, and records it as its entry's `Note`, shown on its line (design Decision 6; Task notes 1.3). Passes `tests/py/test_branch_stands.py` (`tests/suite logic`).

## 2. Against git

- [x] 2.1 git reads a branch Flume kept, and a live place's, standing at its commit in a checkout and a bare clone, a name beside it not, and `worktree add -b` refuses it (design Decision 3; Task notes 2.1). Passes `tests/contract/test_git.py` (`tests/suite contract`).

## 3. The command, its docs and the tests the change affects

- [x] 3.1 Through the crew command on the stubs, a dropped unit added again is refused, read in the kit's repository on its host over ssh, and a fresh name is added (Task notes 3.1). Verify `tests/suite t-journey-cross` ends with "0 failed".
- [x] 3.2 README's plan section, the crew skill and `crew`'s usage header say so (Task notes 3.2). Verify `tests/suite t-docs` ends with "0 failed".
- [x] 3.3 Verify `tests/suite --affected` ends with "0 failed".
