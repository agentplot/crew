## ADDED Requirements

### Requirement: A send's entry is pushed from the sending host
The entry of a `crew send` SHALL be appended to the sending host's own file of the receiving drive's record, and pushed from that host, with its own sign-in, as its own commit on the receiving drive's branch. A push that is refused SHALL keep the entry in that file, said once, and SHALL leave the send reported as made.

#### Scenario: A send from a box
- **WHEN** `wldn-planner` on chuck-herdr-alpha sends to swancloud, whose operator runs on mac-studio
- **THEN** chuck-herdr-alpha's own file of swancloud's record holds the `send` entry, mac-studio's holds none, and swancloud's branch gains it as the commit `runs(chuck-herdr-alpha): send agent/swancloud-operator (wldn-planner)`

#### Scenario: A refused push
- **WHEN** a send is typed into its operator and the push of its entry is refused
- **THEN** the entry stays in the sending host's file, the refusal is said once, and `crew send` reports the send made
