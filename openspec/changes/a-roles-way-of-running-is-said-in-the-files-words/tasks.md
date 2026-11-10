# Tasks

## 1. The briefs and the turn's prompt

- [ ] 1.1 Each main-level brief's `{{TURN}}` says its drive's `runs` names it `standing` or `on-demand`, and the planner's own words name an on-demand reviewer so (design, Decision 1; Task notes 1.1). Verify `tests/suite t-briefs t-journey-roles` ends with "0 failed".
- [ ] 1.2 The turn's prompt says the run is of a role its drive's `runs` names `on-demand` (design, Decision 2; Task notes 1.2). Verify `tests/suite logic` ends with "0 failed".

## 2. Main status and the skill

- [ ] 2.1 `crew main status` says `on-demand` in stream `<label>` of each on-demand role and `standing` before each standing role's status, and the usage header says so (design, Decision 4; Task notes 2.1). Verify `tests/suite logic t-journey-main` ends with "0 failed".
- [ ] 2.2 The crew skill says `standing` and `on-demand` and never that a role runs as its kind (design, Decision 3; Task notes 2.2). Verify `tests/suite t-docs` ends with "0 failed".

## 3. The change's tests

- [ ] 3.1 The tests the change affects pass. Verify `tests/suite --affected` ends with "0 failed".
