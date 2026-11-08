## MODIFIED Requirements

### Requirement: A bolt on GitHub is read where it lives
crew SHALL read a bolt at GitHub's copy of its branch, `origin/bolt/<bolt>`, when the host holds that copy and the policy in it names a remote for the bolt. Otherwise it SHALL read the bolt at the host's own `bolt/<bolt>`. The bolt's head, the changes and chores it holds, and every stage read from it SHALL come from that ref. So SHALL its verification: whether that head is the landing of its work, as the runner reports it. crew SHALL never read a bolt on GitHub from the host's own `bolt/<bolt>`, which is sluice's copy, whether or not sluice has levelled it.

#### Scenario: A merge landed on GitHub while the host's copy stayed behind
- **WHEN** sluice lands a unit's merge and a chore's merge on GitHub's `bolt/b`, the host has fetched it, and the host's own `bolt/b` is still at the commit before them
- **THEN** the unit and the chore read `merged`, the bolt's head is GitHub's, and its verification is read at that head

#### Scenario: A proven bolt whose copy lags
- **WHEN** every unit of a bolt on GitHub has merged, GitHub's head is the commit at which the runner carries the bolt's last unit landed, and the host's `bolt/b` is at an earlier landing
- **THEN** the bolt reads proven, and its row on its kit's landings card is offered

#### Scenario: A bolt kept on its host
- **WHEN** a bolt was made before gives went through sluice, the policy at GitHub's copy of it names no remote for its bolts, and the host's own `bolt/b` holds merges GitHub's copy lacks
- **THEN** the bolt is read at the host's `bolt/b`, those merges counted

#### Scenario: A bolt GitHub's copy of which this host has not got
- **WHEN** the host holds no `origin/bolt/b`
- **THEN** the bolt is read at the host's `bolt/b`, the only copy the host has, and is missing when that is not there either

#### Scenario: A policy crew can't read
- **WHEN** the policy in GitHub's copy of the bolt is not TOML
- **THEN** the bolt's stages read `unknown`, naming the file and the bolt, and nothing is read from the host's `bolt/b`

#### Scenario: A chore's place and a fix beside a bolt on GitHub
- **WHEN** a chore's place holds one commit of its own beyond GitHub's `bolt/b`, and a fix's tip is in GitHub's `bolt/b` but not in the host's
- **THEN** the chore reads `verify` and the fix reads merged
