# A role's way of running says what it means

## Why

A drive in crew's teams file gives each of its five main-level roles a `flume`: `false` while the role stands, or the name of the Flume stream its runs run in. Read as a setting, `design = false` says Flume is turned off for the design agent, and says nothing of an agent standing in its pane. The user, reading a drive's settings as the Boomdrive flake would write them: "I don't understand what this section is about and why we're turning these things off". The stream named there can only be the drive's own, since a drive is its stream, named by its label (agentplot/boomdrive record 0028). And `review = { every = 5; hours = 4; }` says what `hours` counts but not what `every` does. The user: "a comment should explain the units/options".

Record 0064's amendment of 2026-11-09 (accepted) settles the names: `runs`, each role `"standing"` or `"on-demand"`, and `review`'s `after_changes` and `after_hours`, each option's description saying its unit and range. The file stays at version 6, and nothing reads the older names. `code.5` and `flake.2` were amended with it.

## What Changes

- **BREAKING** A drive's `flume` becomes `runs`. It names each of the five main-level roles, `design`, `planner`, `reviewer`, `ops` and `operator`, as `"standing"` or `"on-demand"`. `"standing"`: crew keeps the role's agent running in its pane on the drive's machine. `"on-demand"`: the host's runner has Flume run the role in the drive's own stream while something is pending for it, each run ending when its work is done. No stream is named.
- An on-demand role runs in the stream named by its drive's label. Its role record's `Stream`, the stream a role's run launches its landing work in, and the stream `crew main status` names are the label.
- **BREAKING** `review`'s `every` and `hours` become `after_changes`, a whole number of at least 1, and `after_hours`, a number above 0. A batch is due once `after_changes` changes wait, or once `after_hours` hours have passed since the last batch with at least one change waiting.
- crew refuses a drive that names `flume`, or a `review` that names `every` or `hours`, naming the key, `runs` or the new keys, and the teams file's writer. It reads neither. The file stays at version 6.
- crew's module, `services.crew`, declares `runs` and `review.after_changes` and `review.after_hours`, each option's description saying what it holds, its unit and its range. The pinned files `nix/tests/files/deneb.json` and `runner.json` carry the new keys.
- **BREAKING** `crew drive set` takes `--runs <role> standing|on-demand`, once for each of the five roles, and `--review <after_changes> <after_hours>`. `--flume` is refused as an argument crew does not take.
- README, the crew skill, the usage headers of `crew` and `plan.py`, and the operator's brief name `runs` and `review`'s new keys, and no `flume` as a key of the teams file.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `main-level`: a drive declares how each role runs under `runs`, `standing` or `on-demand`. A drive naming `flume`, or a `review` naming `every` or `hours`, is refused naming the key.
- `review-batches`: the batch setting is `after_changes` and `after_hours`.
- `drive-setup`: `crew drive set` takes `--runs` and `--review <after_changes> <after_hours>`.
- `crew-flake`: the module declares `runs` and the new `review` keys, each option's description saying its unit and range.
- `role-runs`: an on-demand role's record names its drive's label as its stream, and role records follow `runs`.
- `flume-source`: the roles file declares each role `runs` names `standing`.
- `operator-agent`: the operator runs on demand by `runs`, and its brief names `runs` and the batch setting's keys among what a drive's entry says.
- `host-holds-and-updates`: a standing agent is ended at its next stop once `runs` names its role `on-demand`.

## Impact

- **Code**: `plugin/lib/crew.py` (`role_settings` becomes `runs_of`; `review`'s check in `fleet_of`; `role_stream`, `kind_role_of`, `run_of`, `turn_said`, `launch_shell`, `main_sessions`; `drive_given`'s `--runs` and `--review`), `plugin/lib/asks.py` (`role_record`, `roles_due`), `plugin/lib/plan.py` (`batch_due`, `kinds_said`, `kinds_up`, `moved_role`, `roles_lines`, `role_land`, the asks of a role that runs on demand, the `drive set` parser and its usage header), `plugin/lib/board.py` (`roles_read`, `answers_watched`), `plugin/lib/source.py` (`entries`), `plugin/bin/crew`'s usage header.
- **Module**: `nix/modules/options.nix`; `nix/tests/settings.nix`, `nix/tests/file.nix`, `nix/tests/files/deneb.json`, `nix/tests/files/runner.json`.
- **Docs and briefs**: `README.md`, `plugin/skills/crew/SKILL.md`, `plugin/roles/operator.md`.
- **Tests**: the logic tier's fixtures and cases that build a drive (`tests/py/`), `tests/contract/test_recfix.py`, `tests/lib.sh` and the end-to-end tests that set a role's way of running, `tests/t-drive-set.sh`, `tests/t-docs.sh`, `tests/t-briefs.sh`.
- **Hosts**: a host whose teams file names `flume` or `every` is refused by the release that carries this change, until its writer writes `runs` and the new `review` keys. No host writes a version-6 file yet (record 0064's amendment). swancloud's configuration and the Boomdrive flake write the new keys when they take that release.
- **Views**: the agents' views (`board.agent_views`) keep their shape. A role's run view still names its `stream`, now the drive's label, so crew's mod (`plugin/hooks/status.js`) is unchanged (`code.8`).
