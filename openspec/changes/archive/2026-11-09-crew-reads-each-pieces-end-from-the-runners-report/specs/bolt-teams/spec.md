## REMOVED Requirements

### Requirement: A bolt whose landing main holds closes whatever the runner carried of its places
**Reason**: It closed a bolt on its landing as main's landing commits name it, record 0062's stopgap (Decision 3 of `a-bolts-landing-on-main-reads-landed`), which goes now that the runner carries each place's end before Flume tidies it.
**Migration**: A landed bolt closes once each of its pieces reads merged at a commit main holds, as the runner reports its place's end ("A landed bolt closes on its pieces' ends as the runner reports them").

## ADDED Requirements

### Requirement: A landed bolt closes on its pieces' ends as the runner reports them
`crew bolt land`, and the landing's read that closes a landed bolt, SHALL close a started bolt once each of its units and chores reads merged, as the runner reports its place's end, at a commit its kit's main holds, its branch standing or not. No landing commit SHALL be read for it. A bolt with a piece that does not read so SHALL be refused, naming that piece and its stage, and nothing is removed.

#### Scenario: A landed bolt whose branch and places are gone
- **WHEN** `x` landed on main, GitHub has deleted `bolt/x`, Flume has tidied each of `x`'s places, and deneb's runner carries the record Flume holds for it of each, landed on `bolt/x` at a commit main holds
- **THEN** each of `x`'s units reads merged at the commit its record names, and `x`'s close is refused for none of them

#### Scenario: A piece whose end the runner never carried
- **WHEN** main holds `x`'s landing, the runner last carried `x`'s unit `b`'s place at submitted, Flume having tidied it holding no record for the runner, and a landing commit on `bolt/x` names `change/b` in its `Sluice-From`
- **THEN** `x`'s close is refused, naming `b` and that it has not merged into `bolt/x`: it is submitted
