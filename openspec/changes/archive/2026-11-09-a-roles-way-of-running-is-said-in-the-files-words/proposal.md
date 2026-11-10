# A role's way of running is said in the file's words

## Why

A drive's teams file names how each of its five main-level roles runs, under `runs`, `standing` or `on-demand` (record 0064's amendment of 2026-11-09, accepted; `code.5`). crew's briefs and `crew main status` still say it another way. An on-demand role's brief opens its turn with "You run as your kind", its turn's prompt calls it a role "which runs as its kind", the crew skill says a role may "run as its kind", and `crew main status` says of it "runs as its kind in stream madswan". A standing role's brief and its line in `crew main status` name no way of running at all. A person or an agent reading either has to learn a second name for the word the file already gives.

## What Changes

- Each main-level role's brief says how its drive's `runs` names it. A standing role's `{{TURN}}` opens "Your drive's `runs` names you `standing`", and an on-demand role's "Your drive's `runs` names you `on-demand`", with the rest of each as it stands. The planner's own words for an on-demand reviewer say the drive's `runs` names it `on-demand`.
- A turn's prompt, `plugin/flume/turn.md`, says it is a run of a role its drive's `runs` names `on-demand`.
- The crew skill says `standing` and `on-demand` wherever it says what a role's way of running is, and never that a role runs as its kind.
- `crew main status` says `standing` before a standing role's agent status, and `on-demand` in the stream named by the drive's label for an on-demand role, never "runs as its kind". The usage header of `plugin/bin/crew` says so.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `main-level`: `crew main status` says an on-demand role is `on-demand` ("A role that runs as its kind is not started by crew-role"), and a standing role `standing`, in a requirement of its own.
- `role-runs`: a role's brief says how its drive's `runs` names it, and the turn's prompt says the role is `on-demand`, neither saying it runs as its kind.

## Impact

- `plugin/lib/crew.py` (`KIND_TURN`, `STANDING_TURN`, `TURN_OWN`), `plugin/lib/plan.py` (`kind_said`, `main_cmd`'s status), `plugin/flume/turn.md`, `plugin/skills/crew/SKILL.md`, `plugin/bin/crew`'s usage header.
- Tests: `tests/py/test_teams.py`, `tests/t-briefs.sh`, `tests/t-journey-roles.sh`, `tests/t-journey-main.sh`, `tests/t-docs.sh`.
- The views keep their shape (`code.8` not reached). README names no words of `crew main status` and is unchanged (`docs.2`).
- Other repositories: none.
