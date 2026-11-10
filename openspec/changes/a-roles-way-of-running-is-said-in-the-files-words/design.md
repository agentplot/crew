## Context

`a-roles-way-of-running-says-what-it-means` (archived 2026-11-09) gave the teams file its words for how a role runs: a drive's `runs` names each of its five main-level roles `"standing"` or `"on-demand"` (record 0064's amendment, accepted; `code.5`). It renamed the file's keys, the flags and the texts that name them, and left as a non-goal the phrase "runs as its kind", which the specs, the briefs and `crew main status` use for a role whose runs Flume runs. This chore takes that phrase out of what a role and the user read about the role's way of running: its brief, its turn's prompt, the crew skill and `crew main status`.

What says it now:
- `crew.KIND_TURN`, an on-demand role's `{{TURN}}` in every main-level brief: "You run as your kind: no agent of you stands, …". `crew.STANDING_TURN`, a standing role's: "You stand in your pane, an agent crew started and keeps up: …", which names no way of running. `crew.TURN_OWN["planner"]`: "asks the reviewer a batch where it runs as its kind".
- `plugin/flume/turn.md`: "a run of one of crew's main-level roles, which runs as its kind".
- `plugin/skills/crew/SKILL.md`: a role "may instead **run as its kind**", "a reviewer that runs as its kind", "a role that runs as its kind with no standing agent of it up", "open a main-level role that runs as its kind", "**A role that runs as its kind**", and "`crew main status` says it runs as its kind".
- `plan.kind_said`, each on-demand role's words in `crew main status`: "runs as its kind in stream <label>; …". `plan.main_cmd`'s status prints a standing role's agent status alone, "idle" or "not up".
- `plugin/bin/crew`'s usage header for `crew main`: "status says it runs as its kind in its drive's stream".

**Rules this design relies on:** `code.5` (the file's words), `code.7` (`kind_said` stays a function of facts), `code.8` (the views keep their shape) in core.md; `briefs.8` (plain English) in briefs.md; `tests.4`, `tests.6`, `tests.11`, `tests.12` in tests.md; `docs.2`, `docs.4`, `docs.6` in docs.md.

**Area pages this change touches:** `briefs.md` (`plugin/skills/crew/SKILL.md`), `teams.md` (`plugin/lib/crew.py`, `plugin/bin/crew`), `plan.md` (`plugin/lib/plan.py`), `tests.md` (`tests/`), `docs.md` (`openspec/`). No rule names the phrase, and no rule changes.

## Goals / Non-Goals

**Goals:**
- A main-level role's brief and turn's prompt, the crew skill and `crew main status` say a role is `standing` or `on-demand`, the word its drive's `runs` gives, and never that it runs as its kind.

**Non-Goals:**
- crew's other words that use the phrase: `crew-role`'s refusal (`crew.kind_said`), `crew main up`'s words when it ends a standing agent, the reason a standing agent is due an end (`crew.KIND_SAID`), the run record's `why` texts, and code comments and docstrings. None is a brief or `crew main status`.
- README, which names no words of `crew main status` and is no brief.
- The specs' and records' own use of the phrase, which names the mechanism.

## Decisions

### 1. A brief opens its `{{TURN}}` with the file's word

`STANDING_TURN` opens "Your drive's `runs` names you `standing`: you stand in your pane, an agent crew started and keeps up, and your work reaches you there, …". `KIND_TURN` opens "Your drive's `runs` names you `on-demand`: no agent of you stands, and each run of you is one turn, …". The rest of each stands. Naming the key and its value says in one clause where the word comes from and what it is, which is what the file's own words are for.

`TURN_OWN["planner"]` says "`{{TEAM_CMD}} review {{LABEL}}` asks the reviewer a batch where your drive's `runs` names it `on-demand`".

Not taken: "You are on-demand" alone. It says the word without saying it is the file's, and a role reading its brief then has no way to know where it is set.

### 2. The turn's prompt says the role is on-demand

`turn.md`'s first sentence says the turn is "a run of one of crew's main-level roles, one its drive's `runs` names `on-demand`". The prompt reaches only an on-demand role's run, so it names that word alone.

### 3. The skill says `standing` and `on-demand`

The skill's paragraph on a role's way of running opens "A main-level role may instead be **on-demand**", says `crew main status` says it is `on-demand`, and names a standing role `standing`. Each other place says "an on-demand role" or "a reviewer its drive's `runs` names `on-demand`" where it says "a role that runs as its kind" now.

### 4. `crew main status` says the word on every role's line

`kind_said(stream, waiting, run, now)` answers "on-demand in stream <stream>; <ran>; <waits>", keeping the rest of its words and its arguments. `main_cmd`'s status prints a standing role's status column as "standing; <status>", its status "not up" where herdr reads none, as now. Every line of `crew main status` then says how its role runs in the file's word, the standing role's first so its agent's status keeps its place at the end. The usage header says status says "on-demand" and "standing".

Not taken: a fifth column for the word. It would move every line's columns for a word the status column can carry.

## Risks / Trade-offs

- [A script reads a standing role's status from `crew main status` by matching the whole column] → None in crew or its tests: each reads the line by the agent's name and asks whether it holds the status. The line still ends with the status.

## Departures

None.

## After deploy

None. The logic tier proves `kind_said`'s words, the turn's prompt and the briefs' `{{TURN}}`, and the end-to-end tests the tasks name prove the briefs, the skill, the usage and `crew main status`'s lines.

## Task notes

**1.1** `plugin/lib/crew.py`: `STANDING_TURN`, `KIND_TURN` and `TURN_OWN["planner"]` as Decision 1 gives them; the comment above `KIND_TURN` and `turn_said`'s docstring say `standing` and `on-demand`. `tests/t-briefs.sh`, the case "each main-level brief says how its work reaches it": a standing brief has "Your drive's \`runs\` names you \`standing\`: you stand in your pane" and lacks "\`on-demand\`" and "as your kind"; an on-demand brief has "Your drive's \`runs\` names you \`on-demand\`: no agent of you stands", lacks "as your kind" and "as its kind", and the planner's has "where your drive's \`runs\` names it \`on-demand\`". `tests/t-journey-roles.sh`'s check of the run's brief has "names you \`on-demand\`" in place of "You run as your kind".

**1.2** `plugin/flume/turn.md` as Decision 2 gives it. `tests/py/test_role_kinds.py`, `TestThePrompt`: a case that the prompt says "one its drive's \`runs\` names \`on-demand\`" and lacks "as its kind".

**2.1** `plugin/lib/plan.py`: `kind_said` answers "on-demand in stream {stream}; …", its docstring following, and `main_cmd`'s status prints "standing; " before a standing role's status. `tests/py/test_teams.py`'s case for `kind_said` expects "on-demand in stream madswan; …" and that the words lack "as its kind". `tests/t-journey-main.sh`: the first `crew main status wldn` has "standing; idle" on each standing role's line, and the on-demand lines read "on-demand in stream wldn; …". `plugin/bin/crew`'s usage header for `crew main` says status says such a role is on-demand, and each standing role standing.

**2.2** `plugin/skills/crew/SKILL.md` as Decision 3 gives it. `tests/t-docs.sh`: the skill lacks "as its kind" and has "**on-demand**" and "\`crew main status\` says it is \`on-demand\`"; the usage and README keep their check for "runs as its kind", and the usage has "standing".
