# A card's preview is asked of the runner

## Why

crew brings up a card's preview itself today. `crew card preview` hands a process of its own `sluice preview <branch> <revision> --wait --json` on the host where the work runs, reads the preview back with `sluice previews`, puts it away with `sluice release`, keeps a record of it under `~/.local/state/crew/previews` on that host, and offers a preview on a landings row by reading `[preview]` in the kit's `.config/sluice.toml`. That is crew calling sluice and reading sluice's file.

Record 0056, accepted by the user on 2026-11-08, has crew talk only to Boomdrive's runner: "crew never calls Flume or sluice, reads neither one's records or files, and names neither in what it decides" (point 1). Its consequence on previews, agentplot-design's choice that day, keeps what the user sees on a card and changes only how a preview is brought up: crew posts a message, `preview`, naming the repository, the branch and the revision, and the same message marked `done` to put it away; a runner that keeps the repository, on the host where the work runs, carries it out through sluice's own preview command and reports sluice's answer as sluice gave it; crew reads a preview's addresses and state from the runner's report alone; where the report cannot yet say whether a kit declares a preview, the row offers it, and a kit that declares none answers in sluice's words. It is one Boomdrive unit, then one crew unit.

Boomdrive's unit has landed, released as v0.6.0 (`the-runner-brings-up-a-preview-its-control-plane-asks-for`): the runner reads `Act: preview` in crew's `requests.rec`, naming its `Host`, `Repo`, `Branch` and `Revision`, `Done: yes` to put it away, and writes its answer in `previews.rec` on its branch, under a descriptor it proposes for crew to hold byte for byte. This is crew's unit.

The brief: "A card's preview comes up, is listed and goes as the user sees it today, by a message crew posts to the runner, with crew calling no sluice and reading no sluice file for it."

## What Changes

- **A preview is a request.** `requests.rec` takes `Act: preview`, naming the host whose runner reported the work, the work it serves (`bolt/<bolt>` for a landings row, `unit/<unit>` for a batch line), its repository, a branch and a revision, and `Done: yes` to put it away. crew's descriptor matches the runner's copy.
- **crew reads the runner's answer.** A runner's branch holds a fifth file, `previews.rec`, read with the other four. A preview the runner refused in `answers.rec`, as one before v0.6.0 does, reads refused in its words.
- **`crew card preview` writes the request and answers.** On the partition's main machine, the card's owner on the user's words writes one request and changes the card in place saying the preview is asked. It no longer waits up to twenty seconds for sluice, and does nothing on the work's host.
- **Every row that can land offers a preview.** crew reads no `.config/sluice.toml` for it. A kit that declares none answers in sluice's words when asked.
- **crew writes the done where it released before.** The user's `--done`; the raise of a kit's landings card for a row held, gone, landed, dropped or at a moved head; a batch card's close; and the rail's read for a preview whose card or row is gone.
- **The rail's read changes a card when the runner reports anew.** On the partition's main machine it compares what each waiting card was last told of each preview with what the runner now reports, and changes the card in place when they differ.
- **What goes:**
  - crew's records of previews under `~/.local/state/crew/previews`;
  - the internal commands `crew _preview`, `crew _card-preview` and `crew _preview-release`;
  - every `sluice preview`, `sluice previews` and `sluice release` crew runs;
  - `kit.previewed`;
  - the preview part of each host's `crew card sweep`.
- The briefs of main-level ops and the planner, README, the crew skill and the command's usage say so.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `rail-cards`: a card's preview is asked of the runner and read from its report, every row that can land offers one, it is put away by a done request, and a card is changed in place when the runner reports its preview anew.
- `drive-state`: `requests.rec` carries a preview and its done, which names its host, and a runner's branch holds `previews.rec`.

## Impact

- `plugin/lib/runner.py`: `REQUESTS`, `FIELDS`, `ACTS`, `WORK`, `request_refusal`; `PREVIEWS`, `FILES`, `host_read`; new decisions `preview_fields`, `previews_standing`, `preview_report`, `ask_step`, `preview_word`, `previews_put_away`.
- `plugin/lib/plan.py`: `card_preview`, `preview_target`, `preview_owner`, `preview_caller`, `REQUESTERS`; `land_row`, `landing_preview`, `land_end`, `landings_raised`; the batch card's raise and close; `CardActs`; `rail_read`'s sweeps, `card_sweep`; the preview section from `PREVIEWS` to `card_preview_cmd` removed; the parser and dispatch of `_preview`, `_preview-release`, `_card-preview`.
- `plugin/lib/cards.py`: `preview_said`, `made_said`.
- `plugin/lib/kit.py`: `previewed` removed.
- `plugin/lib/record.py`: its docstring names `card.preview`.
- `plugin/bin/crew`: the usage header and the internal commands' dispatch.
- `plugin/roles/main-ops.md`, `plugin/roles/planner.md`, `README.md`, `plugin/skills/crew/SKILL.md`.
- Tests:
  - logic: `tests/py/test_runner.py`, `tests/py/test_cards.py`, `tests/py/test_card_commands.py`, `tests/py/test_landings.py`, `tests/py/test_landing.py`, `tests/py/test_rail.py`, `tests/py/test_kit.py`, `tests/py/test_batches.py`, `tests/py/test_batch_answer.py`;
  - contract: `tests/contract/test_recfix.py`;
  - end to end: `tests/lib.sh`, `tests/stubs/sluice`, `tests/t-journey-land.sh`, `tests/t-help.sh`, `tests/t-briefs.sh`, `tests/t-docs.sh`.
- Unchanged: the views and crew's mod (`code.8`), since no view carries a preview; the run record's descriptor, which `card.preview`'s fields already fit.
