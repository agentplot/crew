# Tasks

Each check is a moon task of the `tests` project, run through `tests/suite`: `logic` is `tests:logic`, `contract` is `tests:contract`. Build the groups in order. Submit nothing: Flume submits the place once its last stage delivers.

## 1. The decisions

- [x] 1.1 A path is in the runner's clone where the host's teams file names its repository and the path is its `dir` or `checkout` or under either, on that host alone, and crew fetches nothing there (design Decision 1; Task notes 1.1). Passes `tests/py/test_kits.py` (`tests/suite logic`).
- [x] 1.2 Every script that fetches in a kit fetches only through `origin_fetch`, is told `fetch=no` in the runner's clone by `fetch_told` at every run, and main now there is `origin/main` as the runner last fetched it (design Decisions 2 and 3; Task notes 1.2). Passes `tests/py/test_kits.py` (`tests/suite logic`).
- [x] 1.3 A forecast's, a bolt's work's and a reading tried again's fetch is made only where crew may fetch (design Decision 1; Task notes 1.3). Passes `tests/py/test_kits.py` (`tests/suite logic`).
- [x] 1.4 A survey that fetches asks each kit fetched by its own entry, a kit in the runner's clone unfetched (design Decision 5; Task notes 1.4). Passes `tests/py/test_bolt_commands.py` (`tests/suite logic`).

## 2. Against git

- [x] 2.1 Told `fetch=no`, main now, what a tip carries and a landing's copies read with no fetch and move no ref, a landing waiting while GitHub's bolt is past the runner's fetch, and gather fetches a kit only on its own entry's word (design Decisions 2 to 5; Task notes 2.1). Passes `tests/contract/test_git.py` and `tests/contract/test_gather.py` (`tests/suite contract`).

## 3. The briefs, the docs and the tests the change affects

- [x] 3.1 The design agent's and the operator's briefs mark the runner's clone and have no fetch or pull run there, the blueprints committed on a branch in a worktree where its checkout is the runner's view (design Decision 6; Task notes 3.1). Verify `tests/suite t-briefs` ends with "0 failed".
- [x] 3.2 README and the crew skill say crew fetches nothing in the runner's clone (Task notes 3.2). Verify `tests/suite t-docs` ends with "0 failed".
- [ ] 3.3 Verify `tests/suite --affected` ends with "0 failed".
