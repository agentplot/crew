# Tasks

Each check is a moon task of the `tests` project, run through `tests/suite`. Build the groups in order. Submit nothing, and never run `wt submit --help`.

## 1. crew found on another host by the repository it is

- [x] 1.1 crew runs itself on another host from the checkout of the repository its manifest's `repository` names, and refuses a host that keeps none, or a manifest that names none, naming what it looked for (design Decisions 1 to 3 and 5; Task notes 1.1). Verify `tests/suite logic` ends with "0 failed".
- [x] 1.2 The test fixtures' hosts keep crew under its current address, so a send from mac-studio reaches the box's partition through crew's checkout there (Task notes 1.2). Verify `tests/suite t-journey-main` ends with "0 failed".
- [x] 1.3 The manifest is in the command core every end-to-end task takes, and in the logic tier's inputs (design Decision 4; Task notes 1.3). Verify `tests/suite t-suite` ends with "0 failed".

## 2. The tests the change affects

- [x] 2.1 Verify `tests/suite --affected` ends with "0 failed".
