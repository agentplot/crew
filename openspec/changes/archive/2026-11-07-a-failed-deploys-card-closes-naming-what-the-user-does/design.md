# Design

## Context

Read on 2026-11-07.

**crew's close.** `ops.deploy_outcome` builds the deploy card's close at the deploy's end (record 0031 §1). A failed deploy closes "The deploy of <to> to <env> failed[ at <step>][; its log: <log>]." `ops.record_cmd` passes it to `plan.row_card_close`, which cuts it to `cards.OUTCOME`, 200 characters, for Pending You and keeps it whole in the run record. `crew ops record` takes `--from`, `--step`, `--outcome`, `--log` and `--rows`; any other flag is argparse's unknown-flag refusal.

**swancloud's deployer.** `packages/swancloud-deployer/deployer.sh` at swancloud main 49469fba:
- `does_text <env> vars|host-key|other` gives what the user does about a failure, by its cause and the environment's policy (`deploy.6`), for example "run \`clan vars generate srv\`, land \`vars/\` on main, then ask ops to offer this deploy again".
- `user_does` ends the failed step's log with `deployer: what the user does: <words>` and keeps the words in the environment's own record as `does`.
- `crew_record` passes its extra arguments to `crew ops record` as given. It hands no `--does` yet.

**The rules.** swancloud `deploy.6`: a failed deploy's "row and its deploy card's close naming the step that failed and what the user does". crew `briefs.13`: a card's words are prose that wraps, and a card speaks in the document's own words. Record 0031 §1: the deploy's card closes when the deploy ends, "with each step's outcome, or fails, with the step and its log".

**The family.** No other tool closes a deploy card. The words are the deployer's, and crew shows them; crew works out none of them (`roles.5`). So the one owner of what the user does is swancloud's deployer, and crew carries its words through.

**Area pages this change touches:** `core.md` (`roles.5`, `read.2`, `code.7`, `code.8`), `briefs.md` (`briefs.13`), `record.md` (the run record's fields), `tests.md` (`tests.4`, `tests.11`) and `docs.md` (`docs.2`, the spec). No rule changes, so no page is edited (`docs.7`).

## Goals / Non-Goals

**Goals:**
- A failed deploy's card closes naming, after the step that failed and its log, the words of what the user does that the deployer handed.
- The deployer's record is never refused for handing them.
- A deploy recorded with no such words closes as today.

**Non-Goals:**
- crew working out what the user does. The words are the deployer's alone.
- Handing `--does` from swancloud's deployer. That is swancloud's change.
- The deploy's offer and approve cards: the sibling fix `an-offer-card-shows-the-step-the-deploy-waits-on-first` changes those.

## Decisions

### 1. `--does` on `crew ops record`, taken on every act

`crew ops record` takes `--does <words>` alongside `--log`. crew takes it on every act, start, step and end, and keeps the words on the entry as `Does`, so whatever record the deployer hands it to is recorded and never refused for it.

The other path was to refuse `--does` anywhere but a failed end, as `--held` is refused without an agent's doer. Not taken: the point of the flag is that the deployer's record is never refused for it, and a refusal there would lose the record of the deploy's end. A misplaced `--does` costs nothing: only a failed end's close reads it.

The words are kept on one line, their whitespace runs as single spaces, as every run-record field is (`record.one_line`). Empty words are no words.

### 2. The words follow the step and its log, as written

`deploy_outcome` takes the end's words. When the deploy failed and words were handed, the close is the failed sentence, then "What you do: " and the words, ending with a full stop unless they end with one already. The words are not reworded (`briefs.13`, a card speaks in the document's own words). "What you do" speaks to the user, as crew's other closes do ("Left out on your word: c.").

Handed no words, or ending well, the close is today's.

### 3. The words are read from the end alone

The close reads the words handed with the end, `--act end`, as the brief names. Words handed with a failed step are recorded on its entry and not read by the close. The other path was to fall back to the failed step's `Does`, as the close falls back from the step's log to the end's. Not taken: the deployer works out the words when the deploy ends, and one source keeps the close plain. It is cheap to add if the deployer ever hands them with the step.

### Rules relied on

- `roles.5`: crew wraps the deployer's words and builds none of its own.
- `read.2`: an absent `--does` never becomes text on the close.
- `code.7`: `deploy_outcome` is a decision on plain facts, tested in the logic tier.
- `code.8`: no bolt, unit, stage, card key or rail row changes shape, so the views and the mod are untouched.
- `briefs.13`: the close is prose that wraps, in the deployer's own words.
- `docs.2`: README's `crew ops record` line names `--does`. `plugin/bin/crew`'s header gives `crew ops record` as `[...]` and `SKILL.md` names no `ops record`, so neither changes.

### Departures

None.

## Risks / Trade-offs

- **[A long log path cuts the words on the card]** → Pending You takes 200 characters for a close, and the words come after the log, as the brief orders them. With a long log path the card's close ends in "…" before the words end. The run record keeps the close whole. The deployer's words are about 100 characters, so a log path under about 60 leaves them whole.
- **[`--does` handed to an older crew]** → A crew without this change refuses the flag. swancloud's deployer hands it only once the crew it pins carries this change, which its own change orders.

## Migration Plan

None. The run record's descriptor gains `Does`, as it gained `Submission`; a record written before reads as it did.

## After deploy

None: every outcome here is a logic-tier case, and nothing waits on a host or on the user.

## Task notes

**1.1** `plugin/lib/record.py`: `Does` joins `EXTRA` and the descriptor's `%allowed`, and the fields' comment names it. Case in `tests/py/test_record.py`: an entry emitted with `Does` reads back with it, and the descriptor allows it.

**1.2** `plugin/lib/ops.py`: the `record` parser takes `--does`; `record_cmd` emits `Does=` the words, and passes them to `deploy_outcome`; the usage names `[--does <words>]` and what a failed end closes with. Case in `tests/py/test_ops.py`: `parser().parse_args` takes `--does` on an end and on a step, and `args_refusal` refuses neither.

**1.3** `ops.deploy_outcome(es, env, to, outcome, log=None, does=None)`: a failed close gains " What you do: <words>." after its log. Cases in `tests/py/test_ops.py`: a failed deploy at guests with its log and words; words already ending with a full stop; the same with no words, as today; a deploy that ends ok handed words closes as today; words of only whitespace are none.

**2.1** `README.md`: the `crew ops record` line names `[--does W]`, and the paragraph says a failed end's close names what the user does as the deployer handed it.
