## ADDED Requirements

### Requirement: A stopped fetch of a drive's branch fails the read
A fetch of a drive's branch that is stopped at its limit SHALL refuse the read at once. The refusal SHALL name the branch, the repository and the stopped try. The fetch SHALL not be tried again for a lock, and SHALL not be read as a branch the repository lacks, whatever git wrote before it was stopped.

#### Scenario: A state repository that never answers
- **WHEN** crew fetches a drive's branch from a remote that takes the call and never answers, its limit 300 ms
- **THEN** the read is refused well inside the sixty seconds, naming the branch, `git fetch`, the repository's address and `300ms`, and the call's process is gone

#### Scenario: A stopped fetch is not a branch the repository lacks
- **WHEN** a fetch of several branches is stopped after git wrote that it couldn't find one of them
- **THEN** the read is refused naming the stopped try, no branch is read as absent, and no branch is fetched again on its own

### Requirement: A stopped push fails the write and is never replayed
A push of a write that is stopped at its limit SHALL refuse the write at once with the stopped try. It is no refusal of the branch. The write SHALL not wait, fetch again or be applied again. Whether it landed SHALL be read at the next write's fetch, where every check is made again. A run-record entry it carried SHALL stay on the host for its next push.

#### Scenario: A state repository that takes no push
- **WHEN** a write is pushed to a remote that takes the call and never answers, its limit 300 ms
- **THEN** the write is refused well inside the sixty seconds, naming the branch, `git push`, the repository's address and `300ms`, and the call's process is gone

#### Scenario: A stopped push is not replayed
- **WHEN** a write's push is stopped
- **THEN** the write is made once, nothing waits and nothing is fetched after the push, and the refusal names the stopped push

#### Scenario: A stopped push that landed is read at the next write
- **WHEN** a write's push is stopped after the remote took it, and the next write reads the branch
- **THEN** the next write reads the branch with the first write on it, and makes every check again on that tip
