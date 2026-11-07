## ADDED Requirements

### Requirement: A test's slot is free once the test has ended
A test's slot SHALL be held by its runner alone, in no process the test starts, so that the slot is free once the test has ended, whatever the test left running.

#### Scenario: A test that leaves a process running
- **WHEN** a test starts a process in the background, as `t-journey-board` starts crew's board follower, and ends without ending it
- **THEN** no file the process holds open is the slot's, and the slot is free once the test has ended

### Requirement: What a test leaves running ends with it
What a test leaves running in its process group SHALL be ended once the test ends, passed or failed: sent SIGTERM, and SIGKILL when it is still there five seconds later. The runner SHALL exit as the test did. A signal that stops the runner SHALL end the test and what it left, and a runner killed outright SHALL take them with it. A card's plannotator session, which crew starts in a session of its own, SHALL end once the test's shell has.

#### Scenario: A process left running
- **WHEN** a test starts a process in the background and exits 3 without ending it
- **THEN** the process is ended and the runner exits 3

#### Scenario: A process that ignores SIGTERM
- **WHEN** a process a test left running ignores SIGTERM
- **THEN** it is sent SIGKILL and ends

#### Scenario: A stopped runner
- **WHEN** the runner of a test that is still running is sent SIGTERM
- **THEN** the test and what it started end, the runner exits 143, and the slot is free

#### Scenario: A killed runner
- **WHEN** the runner of a test that is still running is killed with SIGKILL
- **THEN** the slot is free for the next test, and the test and what it started end

#### Scenario: A card's session
- **WHEN** a test that started a card's plannotator session, in a session of its own, ends while the session waits on no decision
- **THEN** the session ends, writing no result

### Requirement: A follower's round is counted from its own first read
A test that counts what crew's follower read in one round SHALL count from that round's own first read, and SHALL wait for that round's own frames, so that a read an earlier round made late is never counted as the round's.

#### Scenario: A quiet tick on a loaded host
- **WHEN** `t-journey-board` signals the board follower's clock with nothing moved, and a read of an earlier round reaches the reads log after the log was emptied but before the tick's fetch of wldn's state branch
- **THEN** the tick's count starts at its fetch and holds one fetch, no git, no gather and one stamp of the box, and the check fails only when the tick itself reads
