## MODIFIED Requirements

### Requirement: A bolt on GitHub is fetched before crew bolts and a landing read it
As main is read (plan.18), crew SHALL read a bolt on GitHub as the host last fetched it on every read of a kit and every refresh of the rail and the board, fetching nothing. `crew bolts` and a landing's submission SHALL fetch the kit's origin first, but in the runner's clone, which crew fetches nothing in, where they SHALL read the bolt as the runner last fetched it. A fetch that fails SHALL be named with git's words, never read past to the host's copy.

#### Scenario: crew bolts after a landing elsewhere
- **WHEN** a merge has landed on GitHub's `bolt/b` since the host last fetched, and `crew bolts` runs
- **THEN** it fetches the kit's origin once on the kit's host and shows the merged unit as `merged`

#### Scenario: crew bolts in the runner's clone
- **WHEN** `crew bolts` runs for a kit whose folder on its host is a repository that host's teams file names
- **THEN** it asks the kit read with no fetch, at `origin/bolt/b` as the runner last fetched it

#### Scenario: The board does not fetch
- **WHEN** the rail's or the board's refresh reads the kit
- **THEN** no fetch is run, and the bolt is read at `origin/bolt/b` as the host last fetched it

#### Scenario: A fetch that fails
- **WHEN** `crew bolts` runs and the fetch of the kit's origin on the kit's host fails
- **THEN** the kit's stages read `unknown`, naming that GitHub could not be fetched and git's words, and nothing is read from the host's `bolt/b`
