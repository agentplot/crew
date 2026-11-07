## MODIFIED Requirements

### Requirement: Every suite on a host shares the host's test slots
Every crew test on a host, whichever worktree, team or suite runs it, SHALL take one of the host's test slots before it runs and hold it until it ends, killed or not, and a test that finds none free SHALL wait its turn. A host SHALL have `CREW_TEST_SLOTS` slots, else as many tests as its cores less two hold at what one test costs the host beside others, a core and a half, and at least one; a count that is not a number SHALL be refused. A test started inside another's slot SHALL run in that slot.

#### Scenario: Two tests and one slot
- **WHEN** a host has one slot and a second test starts while the first holds it
- **THEN** the second waits, and runs once the first lets its slot go

#### Scenario: A killed test
- **WHEN** a test holding a slot is killed
- **THEN** its slot is free again for the next test

#### Scenario: No count given
- **WHEN** `CREW_TEST_SLOTS` is not set on a host with eighteen cores
- **THEN** the host has ten slots, and a host with ten cores five

## ADDED Requirements

### Requirement: A test's waits start little
A test's wait SHALL look at once and end there when what it waits on holds, and SHALL then look less often the longer it waits, its pauses doubling from a tenth of a second up to a second, within its limit of ten minutes. A test's pause SHALL start no process. The stub sluice's wait on a submission a test holds undecided SHALL exit 5 only after a moment of about a second, on every host the suite runs on, so a landing's waiter calling it again while it is held calls about once a second.

#### Scenario: A wait over at once
- **WHEN** a test waits on a command that succeeds
- **THEN** it runs the command once and does not pause

#### Scenario: A wait of three seconds
- **WHEN** a test waits on a command that succeeds once three seconds have passed
- **THEN** it runs the command no more than seven times

#### Scenario: A pause with no command on the path
- **WHEN** a test pauses for three tenths of a second with an empty folder as its path, on macOS
- **THEN** the pause succeeds and lasts at least three tenths of a second

#### Scenario: A held submission
- **WHEN** a test holds a submission undecided and waits on it with the stub sluice
- **THEN** the wait exits 5 after at least nine tenths of a second, and once the hold is lifted the next wait decides it
