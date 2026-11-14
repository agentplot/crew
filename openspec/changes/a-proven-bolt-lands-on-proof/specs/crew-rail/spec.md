## RENAMED Requirements

- FROM: `### Requirement: A bolt that can land lands on the user's send of its kit's card`
- TO: `### Requirement: A bolt that can land says how it lands`

## MODIFIED Requirements

### Requirement: A bolt that can land says how it lands
Once a bolt can land, its line on its kit's row under land SHALL say how it lands: on proof, with its land and request once posted; on the user's send of `land/<kit>`'s card, for a bolt marked to stay, left by the user, or whose last land at its head was stopped, saying which and, for a stop, what stopped it in the runner's or Flume's words; or once the hold on its drive or kit is lifted, naming the hold and its words. It SHALL carry no command for main-level ops.

#### Scenario: The last unit merges
- **WHEN** the last unit of crew's bolt `b`, not marked to stay, merges into `bolt/b` through sluice, every unit's change has been in a batch the user has answered, and the runner carries that unit's place landed at `bolt/b`'s head
- **THEN** crew's row under land names `b` and `swancloud-ops`, saying `b` lands on proof, and carries no `crew tell`

#### Scenario: Its land posted
- **WHEN** crew posted `b`'s land on proof as request 57, which the runner has not answered
- **THEN** `b`'s line says its land on proof is asked, request 57

#### Scenario: Marked to stay
- **WHEN** crew's bolt `b`, marked to stay, can land
- **THEN** `b`'s line says it stays, and lands on the user's send of `land/crew`

#### Scenario: A stopped landing
- **WHEN** the runner answered `b`'s land on proof at its head refused, a place on `bolt/b` being live
- **THEN** `b`'s line says it can land, that its last landing at that head was stopped, in the runner's words, nothing of the bolt's, and that it lands on the user's send of `land/crew`

#### Scenario: Under a hold
- **WHEN** the user put a hold on the drive swancloud, saying "Cutover", and `b` can land
- **THEN** `b`'s line says the hold on swancloud holds it, "Cutover", and that it lands once the hold is lifted

## ADDED Requirements

### Requirement: A kit's row under land holds the bolts its card tells
A kit's row under land SHALL be raised while a bolt of the kit that landed on proof is still to be told on its landings card, as rail-cards "A bolt that landed on proof is told on its kit's landings card" has it, its line naming each such bolt with the commit its kit's main holds after it, until the user answers or taps a card that told it.

#### Scenario: Landed overnight
- **WHEN** `y` and `w` of crew landed on proof overnight, crew's main holding `9f1c2ab` after `y` and `4d5e6f7` after `w`, and no bolt of crew waits to land
- **THEN** crew's row under land names `y` at `9f1c2ab` and `w` at `4d5e6f7` as landed on proof, told on `land/crew`

#### Scenario: Tapped
- **WHEN** the user taps the notice telling `y` and `w`, and no bolt of crew waits to land
- **THEN** the rail has no row for crew under land
