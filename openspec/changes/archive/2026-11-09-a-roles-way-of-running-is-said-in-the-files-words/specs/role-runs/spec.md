## MODIFIED Requirements

### Requirement: A turn's prompt starts and ends the turn
`plugin/flume/turn.md` SHALL say the run is of a role its drive's `runs` names `on-demand`, never that it runs as its kind. It SHALL have the run start with `crew role start` and end with `crew role end`, writing its report at `{{report}}`, saying the end asks the runners to confirm to Flume each end the turn took. It SHALL place `{{needs}}` in a sentence saying the run asks the user only on a card and stops short only when `crew role start` refuses. It SHALL ask for no `{{brief}}`.

#### Scenario: The prompt's parts
- **WHEN** `plugin/flume/turn.md` is read
- **THEN** every part in double braces is one Flume fills for a stage with a report deliverable and no `makes`, `{{needs}}` among them, and `{{brief}}` is not among them

#### Scenario: The end confirms
- **WHEN** `plugin/flume/turn.md` is read
- **THEN** its step that runs `crew role end` says the end asks the runners to confirm each end the turn took

#### Scenario: The role's way of running
- **WHEN** `plugin/flume/turn.md` is read
- **THEN** it says the run is of a role its drive's `runs` names `on-demand`, and says nowhere that the role runs as its kind

### Requirement: A run's brief says how a turn goes
A role's brief SHALL say the word its drive's `runs` names it by, `standing` or `on-demand`, never that it runs as its kind. An on-demand role's SHALL say its turn starts with `crew role start`, acts on what that took, and ends with `crew role end`; that it waits in its session on nothing, what it would have waited for reaching its next run as an ask; and that it asks the user only on a card in its own name. A standing role's SHALL say its work reaches it as tells and cards in its pane.

#### Scenario: Every brief filled
- **WHEN** each of the five briefs prints for a drive whose `runs` names all five `on-demand`
- **THEN** each says its drive's `runs` names it `on-demand`, holds the turn's words, says nowhere that it runs as its kind, and leaves no token unfilled

#### Scenario: Every brief of a standing role
- **WHEN** each of the five briefs prints for a drive whose `runs` names all five `standing`
- **THEN** each says its drive's `runs` names it `standing` and that its work reaches it in its pane, and none holds the turn's words
