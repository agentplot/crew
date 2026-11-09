## MODIFIED Requirements

### Requirement: A subscription's dock lists the main level's sessions on it
The Claude account a session of the drive's main level runs on, as the drive's `accounts` in the teams file gives its roles, SHALL have a dock on the drive's page, opened from the fleet page's subscription by the drive's link, which SHALL list the drive's sessions on that account: each main-level agent on it, with its host and session.

#### Scenario: One account for three roles
- **WHEN** wldn's design agent, planner and reviewer run in mac-studio's session wldn and its ops in session ops, and wldn's `accounts` gives the first three madswan-2 and ops willdan
- **THEN** madswan-2's dock lists wldn-design, wldn-planner and wldn-reviewer with mac-studio and session wldn, and willdan's lists wldn-ops
