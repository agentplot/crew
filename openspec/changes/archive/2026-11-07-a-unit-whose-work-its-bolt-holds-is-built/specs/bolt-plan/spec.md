## ADDED Requirements

### Requirement: A unit whose work its bolt's branch holds is built
crew SHALL read a started bolt's unit or chore as `merged`, at the landing's commit and time, once a landing sluice made on the bolt's first-parent line names its place's branch, `change/<unit>` or `chore/<chore>`, in its `Sluice-From`. This holds whatever the runner reports of the place and whichever partition's launch made it, mapping no partition onto another. Where crew can't read the bolt's landings, the runner's reading SHALL stand.

#### Scenario: A place landed and tidied
- **WHEN** `a`'s place was never carried by the runner and `b`'s was last carried at submitted, Flume having tidied both after they landed, and `bolt/x` holds sluice's landings of `change/a` and `change/b`
- **THEN** `a` and `b` read `merged` at their landings, a batch reads each at its landing, and `a` reads `landed` once main holds its change

#### Scenario: A launch refused for a change the bolt holds
- **WHEN** `a`'s place ran as another partition's launch and landed on `bolt/x`, and the runner refused this partition's launch of `a` because the base bolt already holds a change named `a`
- **THEN** `a` reads `merged` at its landing, nothing waits on it, and `crew bolts` shows `a` merged, naming `change/a` and the landing's commit

#### Scenario: Read once main holds the bolt
- **WHEN** `x` has landed on main and main has moved on since
- **THEN** `bolt/x`'s landings of `change/a` and `chore/c` still read, at the same commits, so its close finds main holding each

#### Scenario: Built with no launch here
- **WHEN** this partition holds no launch of `a`, and `bolt/x` holds a landing naming `change/a`
- **THEN** `a` reads `merged`, and a landing naming any other branch builds nothing

#### Scenario: Proven from its landings
- **WHEN** every piece of `x` reads merged from its landings and sluice passed the landing at `x`'s head
- **THEN** `x` waits to land

#### Scenario: Landings crew can't read
- **WHEN** git can't list the landings on `bolt/x`
- **THEN** each piece of `x` reads as the runner's records give it

## MODIFIED Requirements

### Requirement: A unit's stage is read from the runner, or from the plan before its bolt starts
crew SHALL read each unit's and chore's stage from the plan, the runner's records and its bolt's landings alone, never from a place in the kit: `queued` while it has no bolt; for a bolt not started, `ready`, or `waiting` while it names `After` work, which builds only once the bolt starts; for a started bolt, as "A started bolt's work reads its stage from the runner's records", "A launched place's stage is where Flume's status has it" and "A unit whose work its bolt's branch holds is built" give it, `landed` once main holds its change, open or archived, or a chore's trailer; and `unknown`, naming why, where crew cannot read what it rests on. Nothing SHALL be kept by hand to say how far work has got.

#### Scenario: Queued work
- **WHEN** a unit has no bolt
- **THEN** its stage is `queued`

#### Scenario: A bolt not started
- **WHEN** bolt `y` is planned and not started, unit `a` names no `After` and `b` has `After: a`
- **THEN** `a` reads `ready` and `b` `waiting`, and nothing of a runner or a place in the kit is read for them

#### Scenario: Nothing kept by hand
- **WHEN** `x` is started and deneb's runner reports `a`'s place in code with 6 of 26 tasks ticked
- **THEN** `crew bolts` shows `a` at `code 6/26`, and no file was edited to say so

#### Scenario: A worktree of crew's from before
- **WHEN** a `unit/a` worktree from before teams left stands under the kit's `places/` with every task ticked, and `x` is started
- **THEN** `a`'s stage is the runner's, and nothing of that worktree is read for it
