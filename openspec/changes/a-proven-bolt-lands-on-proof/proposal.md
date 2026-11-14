# A proven bolt lands on proof

## Why

A bolt lands only on the user's send of its row on its kit's landings card (`plan.16`, record 0056 point 3). A bolt proven at night waits for the morning, though every unit's change in it has already been in a batch the user answered (`briefs.12`). On wldn's switchboard-kit, bolts proven overnight since 2026-11-06 waited 400 to 1,055 minutes for a landings card and the user's send (record 0067's sources).

The user decided, on wldn's card `req_be80263b` on 2026-11-12, that a proven bolt lands without waiting for them, and that a bolt they keep working on is marked ahead of time to stay (record 0067, accepted that day; afterthought/crew-state `signals/2026-11-12-agentplot-planner-b27b864a/01-a-proven-bolt-lands-unless-marked-to-stay.md` on `agentplot/main`; queued at `agentplot/main` aae7bb70). `plan.16`, `briefs.11` and `state.3` are amended for it. This change builds it.

## What Changes

- **A proven bolt lands on proof, at any hour.** Proven means its verification green at its head, its forecast clear of what main has landed, and every unit's latest change in a batch the user answered. The raise of the kit's landings card posts its `land` itself, in main-level ops's name, by one plan write, as it posts a send's. The runner carries it out as it carries a send's.
- **The rail's read lands it at once.** On the main level's host, each rail read raises the landings card of each kit holding a bolt due a land on proof. So nothing waits on an agent or on the user.
- **A bolt marked to stay waits for the user's send.** `crew bolt new … --stays` and `crew bolt start <bolt> --stays` mark it, in a proposal or by the user. No other command marks it, so the mark is set ahead of time and never after the bolt is proven. `crew bolt unstay <bolt>`, the user's or a proposal's, lifts it, and the bolt lands on its next proof.
- **The landings card asks only about what a send must land.** Its rows are the bolts marked to stay, the bolts the user left, the bolts whose land on proof was stopped at their head, and each fix of main. A bolt that lands on proof is no row.
- **The landings card tells the rest.** Each bolt that landed on proof is told on its kit's landings card, naming it and the commit main holds after it, until the user answers or taps a card that told it. With nothing to ask, the card is a one-tap notice asking nothing.
- **A hold on the drive or a kit stops both.** `crew plan hold "<why>" [--repo <kit>]` puts a hold on the drive's landings or one kit's. While it stands, crew posts no land, on proof or on a send. `crew plan go [--repo <kit>]` lifts it, and the raise it hands posts what came due meanwhile. The hold is the user's. Main-level ops puts one only on the user's words in its pane, read as theirs, and lifts none.
- **The plan holds the mark and the holds.** A Bolt record allows `Stays: yes`. A new `Hold` record holds a kit, or the whole drive, with its words.
- **The rail and the bands say how each bolt lands.** A bolt's land line says it lands on proof, that it stays for the user's send, or that a hold holds it. The planner's and ops's bands mark a bolt that stays and open with each hold standing (`code.8`).
- **The briefs, README, the crew skill and `crew`'s usage say so** (`docs.2`).

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `rail-cards`: a proven bolt not marked to stay lands on proof, posted by the card's raise, and the rail's read raises a kit due one. The landings card asks only about the rows a send must land, tells each bolt landed on proof, and posts no land while a hold stands.
- `bolt-teams`: a bolt lands by a land crew posts on proof, or on the user's send when it stays.
- `main-level`: a bolt lands on proof, or on the user's send when it stays. Main-level ops puts a hold on the user's words in its pane and lifts none.
- `crew-rail`: a bolt that can land says how it lands, and a kit's land row holds the bolts its card tells.
- `bolt-plan`: the plan holds a bolt's mark to stay and the holds. A bolt is marked only when it is planned or started, the user lifts the mark, and a hold is put and lifted through crew.
- `plan-proposals`: a proposal may hold `bolt start` and `bolt unstay`, and no hold.
- `crew-board`: the planner's and ops's bands mark a bolt that stays and open with each hold.
- `run-record`: a land on proof is one entry marked as on proof, and the mark's lift and the holds leave entries.

## Impact

- `plugin/lib/plan.py`:
  - the plan's `HEADER` (`Stays`, `Hold`) and `check`;
  - `op_bolt_new`, `op_bolt_start`, a new `op_bolt_unstay`, new `op_plan_hold` and `op_plan_go`, `may_write`, `PLAN_WRITES`, `PROPOSABLE`, `ACTS`, the parser;
  - `landings_raised`, `lands_change`, `lands_post`, `landings_step`, `card_rows`;
  - new decisions `lands_by`, `told_on`, `proof_due`, and a new `landings_proven` in `sweep_moved`;
  - `unoffered`, `rail_rows`, `rail_record`, `card_read`.
- `plugin/lib/runner.py`: `lands_due` takes the lands due on proof.
- `plugin/lib/cards.py`: `landings_form`, `landings_card`, and the proposal card's rows.
- `plugin/lib/board.py`: `bolt_row`, `planner_view`, `ops_view`, and the board's data of a bolt and of a drive.
- `plugin/lib/record.py`: the descriptor's notes on `Form`.
- `plugin/roles/main-ops.md`, `plugin/roles/planner.md`.
- `README.md`, `plugin/skills/crew/SKILL.md`, `plugin/bin/crew`'s usage header (`docs.2`).
- Tests: `tests/py/test_bolt_commands.py`, `tests/py/test_proposal_card.py`, a new `tests/py/test_plan_holds.py`, `tests/py/test_help.py`, `tests/py/test_landings.py`, `tests/py/test_runner.py`, `tests/py/test_cards.py`, `tests/py/test_rail.py`, `tests/py/test_board.py`, `tests/t-briefs.sh`, `tests/t-docs.sh`.
- The views change (`code.8`): `board.agent_views` draws the mark and the holds, and `tests/py/test_board.py` pins them. `plugin/hooks/status.js` draws the views' lines as they come and reads no new key, so it is unchanged.
- No rule or record changes: `plan.16`, `briefs.11` and `state.3` already carry record 0067 (`docs.7`).
