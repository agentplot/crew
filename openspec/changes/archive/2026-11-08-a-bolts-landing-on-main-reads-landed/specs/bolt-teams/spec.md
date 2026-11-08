## ADDED Requirements

### Requirement: A bolt whose landing main holds closes whatever the runner carried of its places
`crew bolt land`, and the landing's read that closes a landed bolt, SHALL close a started bolt whose landing its kit's main holds once each of its units and chores reads landed through that landing ("A landed bolt's pieces are read from its landing"), whether or not its branch still stands and whatever the runner last carried of its places. A bolt with a piece that does not read landed SHALL be refused, naming that piece and its stage, and nothing is removed.

#### Scenario: A landed bolt whose branch and places are gone
- **WHEN** `x` landed on main through `crew bolt submit`, GitHub has deleted `bolt/x`, deneb's runner carries no place of `x`'s work, its `repositories.rec` names the kit, and ops runs `crew bolt land x`
- **THEN** `x` and its units leave the plan, and the landing's entry names the kit and the commit its main holds

#### Scenario: A piece its landing does not hold
- **WHEN** main holds `x`'s landing, and `x`'s unit `b` is named by no landing on that landing's line, and the runner reads `b` at code
- **THEN** `crew bolt land x` is refused, naming `b` and that it has not landed, and the plan is unchanged
