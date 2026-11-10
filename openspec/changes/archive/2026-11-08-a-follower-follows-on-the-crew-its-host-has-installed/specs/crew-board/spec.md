## ADDED Requirements

### Requirement: A follower follows on the crew its host has installed
Whoever holds the host's follower lock SHALL follow on the crew the host has installed. At every refresh, its first included, a follower running a build whose release names another commit than the installed crew's `crew _release` SHALL hand out the restarts due and start again through the installed command, keeping its lock, before it reads a row or acts on a card. A follower whose command is the installed one, or on a host with none installed, SHALL ask nothing for this.

#### Scenario: A tab older than the install takes the lock
- **WHEN** a rail tab opened on a build of crew 0.41.0 takes deneb's follower lock in the second swancloud's job ends for a new pin, and the host's installed crew is 0.46.0
- **THEN** at its first refresh, before it reads a row or sweeps a card, the tab hands out the restarts due and starts again through the installed command, keeping the lock, so no landings card the installed crew reads and posts is withdrawn as a row gone

#### Scenario: The installed crew's own follower
- **WHEN** the follower runs the build the installed command execs, its release naming the commit the installed crew's `crew _release` names
- **THEN** it follows on, starting nothing again, and asks `crew _release` once for the installed command's real path

#### Scenario: A checkout
- **WHEN** the follower runs from crew's checkout, which is the installed command
- **THEN** it asks nothing and starts nothing again for it

### Requirement: A follower starts again for its crew only on what it read
A follower that cannot read its own crew's commit or the installed crew's SHALL follow as it is, starting nothing again on a guess. One started again as the installed crew for running another that still reads another SHALL say so once and follow as it is, never starting again for it twice.

#### Scenario: The installed crew can't be read
- **WHEN** the follower runs a build and the installed command does not answer `crew _release`
- **THEN** it follows as it is and starts nothing again

#### Scenario: Started again and still another
- **WHEN** a follower started again as the installed crew for running another still reads its own release as another commit than the installed crew's
- **THEN** it says once that it follows as it is, and does not start again for it
