## ADDED Requirements

### Requirement: A name whose Flume branch stands is refused when it is planned
`crew unit add`, `crew chore add` and `crew unit split` SHALL refuse a new name whose Flume branch, `change/<unit>` or `chore/<chore>`, stands in a repository a launch of the kit's work would be made in, read there with git. The refusal SHALL name the branch, its folder, host and commit, and the ways on: a fresh name, or the branch removed by the planner or the user. crew SHALL remove no branch. A drop of launched work SHALL say the name stays taken.

#### Scenario: A dropped unit added again under its name
- **WHEN** unit `a` of started bolt `x` was dropped, Flume keeps `change/a` in the kit's repository holding its work, and a proposal or a direct run adds unit `a` again
- **THEN** it is refused before anything is written, naming `change/a`, the folder and host it stands in, its commit, and the ways on, and `change/a` still stands

#### Scenario: The same work under a fresh name
- **WHEN** the same add names `a-again`, whose branch stands nowhere
- **THEN** it passes, and the unit is added and launched

#### Scenario: A chore reads its own branch
- **WHEN** `crew chore add bump` runs while `chore/bump` stands
- **THEN** it is refused naming `chore/bump`

#### Scenario: The branch is read where a launch would make it
- **WHEN** the runner that took the kit's work reports Flume cutting its places in a folder on its host
- **THEN** the add reads the branch in that folder on that host, never from crew's record of a drop

#### Scenario: crew can't tell where a launch would be made
- **WHEN** the runner that took the kit's work carries no place naming the folder it keeps the kit in
- **THEN** the add is refused, saying so, and nothing is written

#### Scenario: A kit no runner has taken work of
- **WHEN** no runner of the drive has taken any of the kit's work and none reports keeping it
- **THEN** no repository is read and the add passes on its other checks

#### Scenario: A drop says the name stays taken
- **WHEN** a unit or chore whose launch stands is dropped
- **THEN** the drop prints, and its entry's `Note` records, that Flume keeps its branch while it holds work its bolt lacks and the name stays taken while the branch stands; a drop of work never launched says nothing of a branch
