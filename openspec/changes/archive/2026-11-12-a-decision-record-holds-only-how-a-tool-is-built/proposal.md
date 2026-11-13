# A decision record holds only how a tool is built

## Why

The design agent's brief tells it to record whatever a design talk settles and to quote the user's words in the record as their decision. Two things went wrong because of that:
- Plans became records. Sluice's record 0117 was amended on 2026-11-12 to freeze fixes on main until a rebuild and a redesign land, and the user was asked to accept that freeze as a record. Crew's record 0060 was amended the same way to carry a drive's queue, and that amendment has since been taken out (375083fb). The user said a record is not for that (signal `2026-11-13-agentplot-planner-ca38ed28/01` on afterthought/crew-state `agentplot/main`).
- The user's own words went into records as the decision. The user does not want that (signal `2026-11-13-agentplot-design-3d529768/01`, whose move challenges `plugin/roles/design.md`'s *Decision records*).

`briefs.15`, as amended on 2026-11-13 (2b6422de), now draws the line:
- A decision record holds only how a tool is built or how it behaves.
- An order of work, a priority, a freeze, a schedule or a trial, which bolt or unit carries something, and how a one-off move, rename or carry-over is carried out belong to the plan. The design agent tells them to the planner, or to ops for a live system, and records none of them.
- A record states each decision in its own words. Its deciders line names where and when the user settled it, and never quotes them.
- A unit cites only records of how a tool is built or behaves.

The briefs still say the opposite. This change brings them in line with the rule.

## What Changes

- **The design agent's brief** (`plugin/roles/design.md`):
  - *Decision records* opens by saying what a record holds and where a plan matter goes: to the planner, or to ops when it moves a live system, in one line naming the signal of the user's words when they settled it. No record, no amendment and no card is made for it.
  - Every record states each decision in its own words. A decision the user settled has a deciders line naming the user and where and when they settled it, with none of their words quoted.
  - An acceptance states the user's note in the record's own words, and a rejection says why and where the user said no.
  - At the agent's start, a proposed record or amendment that holds only a plan matter raises no card. The agent takes it out and tells the planner or ops.
  - *Elaboration on main*, *Talking design with the user*, *Answering a design question* and *Queuing work* follow the same line. A question about a plan matter is no design question: it goes to the planner, or to ops for a live system, and nothing is recorded.
  - `crew record --settled-in-pane --excerpt` still quotes the user's yes whole. Those words are the evidence crew checks in the session's transcript, and they go into no record.
- **The planner's brief** (`plugin/roles/planner.md`):
  - A unit's `--source` names only records of how a tool is built or behaves.
  - A plan matter that reaches the planner is carried in the plan, by a proposal where it changes the plan. The planner never asks for a record of one and never cites one as a source.
- **The constitution skill** (`plugin/skills/constitution/SKILL.md`): a kit's record holds only how the kit is built or behaves, states each decision in its own words, and names who settled it in `decision-makers` without quoting them. A plan matter gets no record.
- **`tests/t-briefs.sh` and `tests/t-docs.sh`** pin the new words and refuse the old ones (`tests.6`).

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `main-level`:
  - A decision record holds only how a tool is built or behaves, and a unit cites only such records.
  - A plan matter goes to the planner, or to ops for a live system, with no record and no card.
  - A record states the user's decisions in its own words, its deciders line naming where and when they settled them.
  - A record's acceptance names where the user gave their yes instead of quoting their words.

## Impact

- `plugin/roles/design.md`, `plugin/roles/planner.md`, `plugin/skills/constitution/SKILL.md`: their words.
- `tests/t-briefs.sh`, `tests/t-docs.sh`: the pins. Neither test reads a new path, so `tests/moon.yml` is unchanged (`tests.10`).
- No code changes. `crew record`, its card and its transcript check stay as they are. Crew reads no record's deciders line, and no check reads a record's words.
- No change to the views or crew's mod (`code.8`): no bolt, unit, stage, card or rail row changes shape.
- `docs/architecture/` and `docs/adr/` are not touched (`docs.7`). `briefs.15` already says this, as amended in 2b6422de.
