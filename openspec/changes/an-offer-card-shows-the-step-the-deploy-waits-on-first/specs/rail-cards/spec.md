## MODIFIED Requirements

### Requirement: A deploy's card is a high approval
A deploy's card SHALL be an `approve` of risk high, not reversible, because irreversible, naming the environment and the commit, while no step the deploy waits on is open, and boxes held to send while one is; its summary SHALL count the landings since the environment's last deploy and name the environments before and after it, and its details SHALL hold the landings' subjects. It SHALL follow its environment's last deploy card when the user declined that card, and otherwise no card.

#### Scenario: Three landings since srv's last deploy
- **WHEN** the deployer offers srv `c882cff` with git-cliff's notes for `6aed25c..c882cff` and two steps, and srv runs `6aed25c`
- **THEN** the card's approve block has risk high and reversible false, its summary counts three landings and says the box follows on its own and mac-studio is offered after srv, its face holds the notes as handed and the two steps with their doers, and its details name landings #16, #17 and #18

#### Scenario: A head a landing card put on main
- **WHEN** crew raises srv's deploy card for a head that landing #24's card put on main
- **THEN** the card follows no card, and its details name landing #24

## ADDED Requirements

### Requirement: A step the deploy waits on is first on its offer's card
A step handed to `crew ops offer` marked `before` among its when words SHALL be a step of the user's the deploy waits on (swancloud record 0038); the offer SHALL be refused, nothing offered, when its doer is not the user or two such steps share a number. The deploy's card SHALL say first that the deploy waits on them, and list them first on its face, before the notes, each with its why or that it is done; the after-deploy list SHALL leave them out.

#### Scenario: Move the Archives disk before srv's deploy
- **WHEN** the deployer offers swancloud-srv `bbbbbbb` with notes and the steps "Move the Archives disk from mac-studio to deneb.", the user's, marked `before`, and "rotate the kanidm admin password", the user's
- **THEN** the card's summary opens saying it waits on 1 step of yours before the deploy, and its face lists that step with its why first, then the notes, then the rotation as the one step after the deploy

#### Scenario: A step marked before for an agent
- **WHEN** the deployer hands a step marked `before` whose doer is main-ops
- **THEN** the offer is refused naming the line, a step the deploy waits on being the user's alone, and nothing is offered

### Requirement: A deploy's card with a step it waits on open is boxes whose send with every box ticked is the word
While a step the deploy waits on is open, the deploy's card SHALL be boxes carrying highStakes, none ticked: a box for each open step, `before:<n>`, then one for the deploy, `deploy`, in lists of five at most. Its send with every box ticked SHALL be the word; one with a box unticked SHALL be none. Once every such step is done it SHALL be the hold-to-approve. A card moving between the two SHALL be followed, not changed, the run record keeping each post's and change's form.

#### Scenario: One step open
- **WHEN** swancloud-srv's offer of `bbbbbbb` waits on the user's step 1, not done
- **THEN** its card is one list of two boxes carrying highStakes, `before:1` labelled "Done: 1. Move the Archives disk from mac-studio to deneb." and `deploy`, none ticked, and its post is recorded with the form `boxes`

#### Scenario: Every step it waits on done
- **WHEN** the step the deploy waits on is recorded done while its card of boxes is open
- **THEN** the card is raised again as the hold-to-approve, its face listing the step done, and the boxes card is followed rather than changed

#### Scenario: Five steps the deploy waits on
- **WHEN** the deploy waits on five steps of the user's, none done
- **THEN** its card asks two lists, the first of three steps' boxes and the second of two and the deploy's, each carrying what follows a yes

### Requirement: A step the deploy waits on has no card of its own while its offer is open
A user's step recorded with the words of a step the environment's open offer waits on SHALL be recorded as one, `before` among its when words, and SHALL have no row and no card of its own while that offer is open, the deploy's row saying it waits on it. With no offer open, it SHALL have its row and card as any user's step.

#### Scenario: The deployer records the step it waits on
- **WHEN** the deployer records that step waiting with doer user and the text "Move the Archives disk\nfrom mac-studio to deneb."
- **THEN** the run record holds it with `before` among its when words, no card is posted for it, the rail shows no row of its own, and the deploy's row says it waits on the step of yours ticked on its card

#### Scenario: The offer ends with the step still open
- **WHEN** swancloud-srv's deploy ends with no offer open and the step it waited on still waiting
- **THEN** the step has its own row and card, as any user's step
