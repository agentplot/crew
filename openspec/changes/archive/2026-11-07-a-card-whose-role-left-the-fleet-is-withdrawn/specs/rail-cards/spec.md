## ADDED Requirements

### Requirement: A card whose role left the fleet is withdrawn
On each rail read crew SHALL withdraw, in its owner's name, each open card of its own six posted on that host whose owner is `<label>-planner`, `<label>-ops` or `<label>-design` for a label no partition of the teams file has now, saying the owner left the fleet and how whoever holds the work now raises it again. The close SHALL be recorded, withdrawn, and the rail SHALL no longer show the card. Any other card SHALL keep the paths it has.

#### Scenario: A partition's label changed under an open deploy card
- **WHEN** the teams file labels the partition `wldn`, and its run record holds `deploy/dev`'s card posted on this host in `willdan-ops`'s name and open while the offer waits
- **THEN** the rail's read withdraws the card in `willdan-ops`'s name with "willdan-ops left the fleet, so an answer here reaches nobody. The deploy is offered again in the name of the ops of the partition that holds dev now.", records the close withdrawn with those words, and lists it among the cards it withdrew

#### Scenario: The partition stays
- **WHEN** the teams file labels the partition `wldn` and `deploy/dev`'s card is open in `wldn-ops`'s name while the offer waits
- **THEN** the rail's read leaves the card open and posts no other

#### Scenario: A deploy whose word stands
- **WHEN** `deploy/dev`'s card is open in `willdan-ops`'s name and the user's word on the deploy is recorded
- **THEN** the card is withdrawn with "willdan-ops left the fleet, so an answer here reaches nobody. Your word on dev's deploy stands, and the deploy goes on."

#### Scenario: A record's card in a former design agent's name
- **WHEN** `record/atlas-kit/0021`'s card is open in `willdan-design`'s name
- **THEN** it is withdrawn, saying "Record 0021 of atlas-kit is carded again with crew record by the design agent of the partition that holds it now."

#### Scenario: A question and a conductor's card are no partition role's
- **WHEN** a question card is open in `willdan-planner`'s name, and `land/y`'s card in `swb-1-conductor`'s
- **THEN** the sweep judges neither as a role that left the fleet: the question is judged by its asker's pane and the landing card by its row

### Requirement: A card in a former name cards no row
A card whose owner left the fleet SHALL card no row. A row whose only open card is such a card SHALL be posted through its kind's raise in its owner's name, as a row with no card open is. crew SHALL map no former name onto a new one, carry no card across, and take no partition as another's successor.

#### Scenario: The deploy row is carded in the standing ops's name
- **WHEN** `deploy/dev`'s card is open in `willdan-ops`'s name, the offer of dev's deploy still waits, and the teams file labels the partition `wldn`
- **THEN** the rail's read posts `deploy/dev`'s card through its raise in `wldn-ops`'s name, following no card
