## MODIFIED Requirements

### Requirement: crew asks a host's runner for work by requests on the drive's branch
crew SHALL write every request for a host's runner as a record of `requests.rec` on the drive's branch: a launch of a place, or a retry, drop or priority of one it launched. Each SHALL be numbered once, appended by a crew command in the commit of the plan write that occasions it, and checked by `recfix --check` and crew's own rules. A request SHALL never be removed. It SHALL never be changed, except by `crew kit rename`, which renames a repository's name in a request's `Repo` and in a fix of its main's `Work`, in the rename's one commit. Any other write that changes a request SHALL be refused.

#### Scenario: Never renumbered
- **WHEN** `requests.rec` holds requests 1 to 7 and a drop is written
- **THEN** it is request 8, and requests 1 to 7 are as they were

#### Scenario: A rename's write changes a request's repository
- **WHEN** the user renames `flywheel-cloud` to `boomdrive-cloud` and request 3 has `Repo: flywheel-cloud`
- **THEN** the write passes crew's append check with request 3's `Repo` renamed and nothing else of it changed

#### Scenario: Any other write that changes a request
- **WHEN** a write other than a rename would change request 3's `Repo`
- **THEN** it is refused, saying a request is never changed or removed, and nothing is pushed

## ADDED Requirements

### Requirement: A partition is never renamed
A partition's label SHALL be fixed once it is made, and no crew command SHALL rename one; `crew kit rename` renames a repository within the one partition it runs as. A label that changes in the teams file SHALL be read as one partition removed and another added: the new label's state is its own branch, `<new label>/main`, nothing of the old label's branch is read as the new partition's, and a command naming the old label is refused as naming no partition.

#### Scenario: A label changed in the teams file
- **WHEN** the teams file names `afterthought` where it named `swancloud`
- **THEN** crew reads afterthought's state from `afterthought/main` of its state repository, and a command run with `--label swancloud` is refused naming the partitions the teams file has
