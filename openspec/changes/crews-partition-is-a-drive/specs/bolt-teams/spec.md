## MODIFIED Requirements

### Requirement: crew removes only its own worktrees
crew SHALL remove only the landing worktrees it cut, `<kit>/places/land-<bolt>` on a `bolt/` branch, and only bolt branches it marked as its own. It SHALL never remove the main checkout, a place of Flume's, a worktree elsewhere, one on another branch or on none, or a locked one, which it names as kept. It SHALL remove nothing when it cannot read every plan the kit's work goes in.

#### Scenario: A worktree made by hand
- **WHEN** a kit checkout has a worktree beside `main` that the user made, on a branch of their own
- **THEN** crew leaves it as it is

#### Scenario: A place of Flume's
- **WHEN** a kit checkout has `places/change--x` on `change/x`, a place Flume made
- **THEN** crew leaves it as it is

#### Scenario: A merge partway through its rebase
- **WHEN** a place is on no branch because a rebase stopped partway
- **THEN** crew leaves it as it is

#### Scenario: A plan that can't be read
- **WHEN** crew lands a bolt while the plan of a drive whose work is in the kit cannot be fetched
- **THEN** no worktree is removed, and crew says why

### Requirement: A started bolt's work is launched whole
`crew bolt start <bolt>` SHALL check the kit's policy and have sluice make `bolt/<bolt>` from the kit's main, in the checkout the drive's main-level host keeps of the kit, and SHALL be refused while that host keeps none or is held, or no runner answers for the drive. Its one plan write SHALL set `Path: flume` on the bolt, and no `Team`, and append a launch for each of its units and chores in the file's order, cut from `bolt/<bolt>`, in the kit's repository and naming no host or stream, for a runner whose configuration names the repository to take. It SHALL start, restart and greet no agent.

#### Scenario: A bolt of three
- **WHEN** `crew bolt start x` runs, `x` holding units `a` and `b`, `b` after `a`, and chore `c`, and a runner answers for madswan
- **THEN** the plan marks `x` `Path: flume` with no `Team`, `requests.rec` holds three launches of `change`, `change` and `chore` on `bolt/x`, each in crew's repository and naming no host or stream, and no agent starts

#### Scenario: No runner on the host
- **WHEN** `crew bolt start x` runs and madswan's state repository holds no runner's branch
- **THEN** the start is refused naming that no runner answers for madswan, and no branch is made

### Requirement: A place is answered by a retry
`crew answer <work> "<words>"`, the planner's, the design agent's or main-level ops's, SHALL append a retry of the stage the work's place stopped short on or waits on, carrying the words, its agent kept open for the answer or not, and past its kind's bound or not, whatever stage it last delivered; or of its submission where that waits on its caller unheld. It SHALL be refused naming the place's stage when the place neither stopped short nor waits on its caller. For a live place, the refusal SHALL name that stage as the runner carried it, with the runner's host and when it carried it, and say that a wait Flume has told of since reaches crew with that runner's next carry. It SHALL be refused naming what crew could not read when it can't tell whether the place waits. It SHALL never say that a live place has nothing to answer.

#### Scenario: A construct that asked
- **WHEN** the runner's record shows `a`'s construct stopped short asking "Which drive's rail?", and the planner runs `crew answer a "madswan's"`
- **THEN** `requests.rec` gains a retry of `a`'s construct with the words `madswan's`

#### Scenario: A stop-short whose agent is kept open
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place, its code ended short needing an answer with its agent kept open, and the planner runs `crew answer a "Wait for the releases; retry once they land."`
- **THEN** `requests.rec` gains a retry of `a`'s code with those words, and nothing is refused

#### Scenario: A place past its bound
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place waiting on its caller to retry code past its bound, its verify delivered, and the planner runs `crew answer a "Take the bolt in and resolve the conflict."`
- **THEN** `requests.rec` gains a retry of `a`'s code with those words

#### Scenario: A submission that waits on its retry
- **WHEN** the runner carries Flume 0.17.0's status of `a`'s place waiting on its caller to retry its submission, which the merge queue refused, and the planner runs `crew answer a "Submit it again."`
- **THEN** `requests.rec` gains a retry of `a`'s submission with those words

#### Scenario: Nothing to answer
- **WHEN** deneb's runner last carried `a`'s place in code with no question, Flume may since have told the planner the place waits on its caller, and the planner runs `crew answer a "yes"`
- **THEN** it is refused naming `a`'s stage as code when deneb's runner carried it, at the time it carried it, and saying that a wait Flume has told of since reaches crew with that runner's next carry, never that there is nothing to answer, and `requests.rec` gains nothing

#### Scenario: A place the runner has not carried
- **WHEN** `a`, naming no `After`, is answered held with the runner's claim, or launched at a place whose status the runner has not carried, and `crew answer a "yes"` runs
- **THEN** it is refused saying crew can't tell whether `a`'s place waits on an answer, with the runner's words or that no status of the place is carried, and never that it is held for its After work

#### Scenario: Work that is over
- **WHEN** the runner's record shows `a`'s place landed on its bolt, and `crew answer a "yes"` runs
- **THEN** it is refused naming `a` merged, with nothing to answer

### Requirement: A bolt whose work is on main lands by its close alone
`crew bolt land` SHALL land a bolt with no merge to make, on the user's word, once its kit's main holds each of its units' changes, open or archived, and each of its chores, read in the checkout the drive's main-level host keeps of its kit, since no runner took any of its work, recording the landing as any landing; it SHALL be refused for such a bolt with no units or chores, whose kit that host keeps no checkout of, or while any unit's change is not on main.

#### Scenario: A bolt built outside its branch
- **WHEN** the plan holds the bolt `deploys-go-through-crew`, nothing has merged into its branch, and each of its units' changes is archived on crew's main
- **THEN** `crew bolt land deploys-go-through-crew` removes it and its units from the plan, and the landing's entry names crew and the commit its main holds

#### Scenario: A unit not yet on main
- **WHEN** one unit of such a bolt has no change on its kit's main
- **THEN** `crew bolt land` is refused, naming the unit and its stage
