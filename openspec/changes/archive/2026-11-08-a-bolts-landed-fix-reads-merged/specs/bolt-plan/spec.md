## ADDED Requirements

### Requirement: A fix whose place's landing its bolt's branch holds is merged
crew SHALL read a fix on a started bolt as `merged`, at the landing's commit and time, once a landing sluice made on the bolt's first-parent line names the fix's place's branch, `fix/<bolt>--<name>`, in its `Sluice-From`, whatever the runner last carried of its place. A landing whose time is before the fix's launch SHALL build nothing of that fix. A fix of a kit's main SHALL never be read from a bolt's landings. Where crew can't read the bolt's landings, the runner's reading SHALL stand.

#### Scenario: A landed fix whose place the runner last carried at submitted
- **WHEN** fix `x--tidy`'s place was last carried by the runner at submitted, Flume having tidied it after it landed, and `bolt/x` holds sluice's landing naming `fix/x--tidy`, made after the fix's launch
- **THEN** `fix/x/tidy` reads `merged` at that landing, and `crew bolts` shows it merged, naming `fix/x--tidy` and the landing's commit

#### Scenario: A fix launched again under a landed fix's name
- **WHEN** `bolt/x` holds a landing naming `fix/x--tidy` made before the standing launch of `fix/x/tidy`, an earlier launch of that name having been dropped after its place landed
- **THEN** `fix/x/tidy` reads its stage from the runner's records

#### Scenario: Landings crew can't read
- **WHEN** git can't list the landings on `bolt/x`, and the runner last carried `fix/x/tidy`'s place at submitted
- **THEN** `fix/x/tidy` reads submitted

### Requirement: A fix read merged from its bolt's landing holds nothing
`crew bolts`, the board, the bolt's landing and `crew fix <bolt> <name> --drop` SHALL read a fix through its bolt's landings alike. A fix read merged SHALL hold its bolt's landing no longer, and its drop SHALL be refused as any merged fix's is.

#### Scenario: A landed fix holds its bolt's landing no longer
- **WHEN** every unit of `x` has merged, sluice passed the landing at `x`'s head, and `fix/x/tidy` reads merged from its landing while the runner last carried it at submitted
- **THEN** no fix is in flight on `x`, and `x` reads proven

#### Scenario: A landed fix is not dropped
- **WHEN** `fix/x/tidy` reads merged from its landing on `bolt/x`, and the planner runs `crew fix x tidy --drop`
- **THEN** it is refused, saying the fix has merged into `bolt/x`, and nothing is appended to `requests.rec`

#### Scenario: A fix whose landings crew can't read still holds
- **WHEN** git can't list the landings on `bolt/x`, and the runner last carried `fix/x/tidy`'s place at submitted
- **THEN** `fix/x/tidy` is in flight on `x`, and holds its landing
