## MODIFIED Requirements

### Requirement: Every suite on a host shares the host's test slots
Every crew test on a host, whichever worktree, team or suite runs it, SHALL take one of the host's test slots before it runs and hold it until it ends, killed or not, and a test that finds none free SHALL wait its turn. The slot SHALL be held by the test's runner alone, in no process the test starts, so it is free once the test has ended, whatever the test left running. What a test leaves running in its process group SHALL be ended once the test ends, passed or failed: sent SIGTERM, and SIGKILL when it is still there five seconds later. A signal that stops the runner SHALL end the test and what it left, and a runner killed outright SHALL take them with it. A card's plannotator session, which crew starts in a session of its own, SHALL end once the test's shell has. A host SHALL have `CREW_TEST_SLOTS` slots, else its cores less two and at least two; a count that is not a number SHALL be refused. A test started inside another's slot SHALL run in that slot.

#### Scenario: Two tests and one slot
- **WHEN** a host has one slot and a second test starts while the first holds it
- **THEN** the second waits, and runs once the first lets its slot go

#### Scenario: A killed test
- **WHEN** a test holding a slot is killed
- **THEN** its slot is free again for the next test, and the test and what it left running end

#### Scenario: A test that leaves a process running
- **WHEN** a test starts a process in the background, as `t-journey-board` starts crew's board follower, and ends without ending it, exiting 3
- **THEN** the process never held the slot's file, the slot is free once the test has ended, the process is ended, and the runner exits 3

#### Scenario: A process that ignores SIGTERM
- **WHEN** a process a test left running ignores SIGTERM
- **THEN** it is sent SIGKILL and ends

#### Scenario: A stopped runner
- **WHEN** the runner of a test that is still running is sent SIGTERM
- **THEN** the test and what it started end, the runner exits 143, and the slot is free

#### Scenario: A card's session
- **WHEN** a test that started a card's plannotator session, in a session of its own, ends while the session waits on no decision
- **THEN** the session ends, writing no result

#### Scenario: No count given
- **WHEN** `CREW_TEST_SLOTS` is not set on a host with ten cores
- **THEN** the host has eight slots

### Requirement: A test waits on a condition, never on the clock
No fixed sleep SHALL decide a test's outcome: a test SHALL wait on the condition it proves, ending as soon as it holds, with a limit that holds on a host loaded far past its cores, ten minutes for a wait on a condition and thirty for a background wait; a test that needs time to have passed SHALL move the time rather than wait for it. A test that counts what a follower read in one round SHALL count from that round's own first read, and SHALL wait for that round's own frames, so a read an earlier round made late is never counted as the round's.

#### Scenario: A follower's tails on a loaded host
- **WHEN** the test of `crew events --follow` runs on a host loaded past its cores and the follower's tails take longer than usual to start
- **THEN** the test waits until they start, up to ten minutes, and passes

#### Scenario: A commit in an earlier second
- **WHEN** a test needs a commit made before a stage began
- **THEN** it backdates the commit rather than sleeping into the next second

#### Scenario: A quiet tick on a loaded host
- **WHEN** `t-journey-board` signals the board follower's clock with nothing moved, and a read of an earlier round reaches the reads log after the log was emptied but before the tick's fetch of wldn's state branch
- **THEN** the tick's count starts at its fetch and holds one fetch, no git, no gather and one stamp of the box, and the check fails only when the tick itself reads
