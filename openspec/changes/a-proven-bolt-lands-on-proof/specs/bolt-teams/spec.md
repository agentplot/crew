## RENAMED Requirements

- FROM: `### Requirement: A bolt lands on the user's send alone, carried to the runner as a land`
- TO: `### Requirement: A bolt lands by a land crew posts on proof, or on the user's send when it stays`

## MODIFIED Requirements

### Requirement: A bolt lands by a land crew posts on proof, or on the user's send when it stays
A started bolt whose verification is green SHALL land only by a `land` of its launch that crew posts: on proof, or, for a bolt marked to stay, on the user's send of its row on its kit's landings card (record 0067). The runner SHALL carry it out with Flume, which submits the base place through sluice onto GitHub's main (record 0056). No agent SHALL run anything to land a bolt. Each bolt's land SHALL be its own, one refused or stopped holding no other. A landing SHALL deploy nothing.

#### Scenario: The bolt lands
- **WHEN** bolt `x`, not marked to stay, reads proven and its forecast is clear of main
- **THEN** `requests.rec` gains one land of `x`'s launch, posted by crew with no card answered; once the runner's branch carries `x`'s base place landed at a commit, the next raise of the card records `x` landed at that commit and closes it, with no agent's command run between

#### Scenario: A bolt marked to stay lands on the send
- **WHEN** bolt `x`, marked to stay, reads proven
- **THEN** no land of `x` is posted until the user sends its kit's landings card with `x` ticked, and then one is

#### Scenario: Three bolts on one send
- **WHEN** the user's send ticks `y`, `z` and `w`, each marked to stay, in that order, and the runner's report then carries `z`'s verdict conflict
- **THEN** lands of `y`, `z` and `w` are posted in that order, `y` and `w` land and are closed, and `z` reads refused for its conflict, its take-main fix launched

#### Scenario: A landing deploys nothing
- **WHEN** bolt `x` lands on proof
- **THEN** nothing is deployed by the landing
