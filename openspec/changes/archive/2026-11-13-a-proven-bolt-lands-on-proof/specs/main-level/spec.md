## RENAMED Requirements

- FROM: `### Requirement: A bolt lands on the user's send, carried in ops's name`
- TO: `### Requirement: A bolt lands on proof, or on the user's send when it stays, carried in ops's name`

## MODIFIED Requirements

### Requirement: A bolt lands on proof, or on the user's send when it stays, carried in ops's name
A bolt whose verification is green SHALL land by one procedure, main-level ops's (`plan.16` as records 0056 and 0067 amend it): crew posts its land to the runner itself, in ops's name, once it is proven, or, for a bolt marked to stay, on the user's send of its row on its kit's landings card, with no agent running anything. Nothing else SHALL be a word to land: not the planner, not another agent, not a bolt's row appearing on the rail.

#### Scenario: Landing
- **WHEN** swb-1's bolt, not marked to stay, reads proven
- **THEN** crew's next raise of willdan's landings card posts the bolt's land to the runner, no agent running anything for it, and once the runner reports the bolt's base place landed, crew's read closes the bolt and the plan no longer holds it

#### Scenario: Landing a bolt marked to stay
- **WHEN** the user sends swb-1's bolt, marked to stay, ticked on willdan's landings card
- **THEN** crew's next raise of the card posts the bolt's land to the runner, no agent running anything for it

#### Scenario: No word from the planner
- **WHEN** the planner tells the main-level ops that a bolt marked to stay may land
- **THEN** ops runs nothing, no land is posted for the bolt, and it lands only once the user sends the kit's landings card with it ticked

## ADDED Requirements

### Requirement: Main-level ops puts a hold on the user's words in its pane, and lifts none
Main-level ops SHALL put a hold on a drive's or a kit's landings only on the user's own words in its pane, `crew plan hold "<why>" [--repo <kit>] --excerpt "<their words>"`, which crew reads in ops's own session transcript as the user's, as `crew bolt leave` reads them, refusing otherwise. Ops SHALL lift no hold: `crew plan go` is the user's alone, since a lift lets lands be posted and no word in a pane lands a bolt.

#### Scenario: The user's words typed in ops's pane
- **WHEN** the user types "Pause landings on crew for the cutover" in swancloud-ops's pane, and ops runs `crew plan hold "Cutover" --repo crew --excerpt "Pause landings on crew for the cutover" --label swancloud`
- **THEN** crew reads the words as the user's, the plan holds a hold on crew with the words "Cutover", and its entry holds none of the user's words

#### Scenario: No words of the user's
- **WHEN** ops runs `crew plan hold "Cutover" --repo crew --label swancloud` with no `--excerpt`
- **THEN** it is refused, naming the user's words as what it needs, and the plan is unchanged

#### Scenario: Ops lifts a hold
- **WHEN** ops runs `crew plan go --repo crew --label swancloud`
- **THEN** it is refused, saying the lift is the user's, and the hold stands
