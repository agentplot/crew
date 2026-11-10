# Verify: a-roles-way-of-running-says-what-it-means

Checked on `change/a-roles-way-of-running-says-what-it-means` at 879bd700, cut from `bolt/a-roles-way-of-running-says-what-it-means`, merge-base with main 83c9a149, on 2026-11-09.

## The whole checks

`tests/suite --affected`, run once, as CLAUDE.md names it for a change that is done: **34 passed (3 replayed), 0 failed**, exit 0.

- Ran: `logic`, `contract`, `nix:test`, `nix:typecheck`, and every end-to-end test but `t-briefs` (`t-cards`, `t-docs`, `t-drive-set`, `t-flume-source`, `t-help`, `t-hold`, `t-journey-board`, `t-journey-cross`, `t-journey-land`, `t-journey-main`, `t-journey-main-fix`, `t-journey-ops`, `t-journey-plan`, `t-journey-review`, `t-journey-roles`, `t-journey-signals`, `t-journey-state`, `t-roles`, `t-runner`, `t-session-hook`, `t-slot`, `t-sluice`, `t-stage-facts`, `t-suite`, `t-teams`, `t-waits`, `t-word`).
- Replayed: `nix:format`, `nix:lint` and `t-briefs`, from passing runs on this host with identical inputs (the code stage ran them by name for tasks 1.1, 3.2 and 4.2).
- Not affected: `mod`, since nothing under `plugin/hooks/` or `plugin/tests/` changed (Decision 7).

`openspec validate a-roles-way-of-running-says-what-it-means --strict`: valid.

## Tasks

All 10 tasks in `tasks.md` are ticked. Each one's named check exists and passed in the run above:

| Task | Check | Where |
|---|---|---|
| 1.1 | `nix:format`, `nix:lint`, `nix:test`; `file.nix`'s "A role crew has no kind for", "A batch setting by its former names", "A batch setting out of range" and "The descriptions"; `deneb.json` and `runner.json` carry `runs` and `after_changes`/`after_hours` | `nix/modules/options.nix`, `nix/tests/` |
| 2.1 | `TestRoleSettings` rewritten for `runs`; the refusals of `flume`, of `runs` and of `review`'s former and out-of-range keys | `tests/py/test_teams.py` |
| 2.2 | `test_a_way_of_running_crew_does_not_take_is_refused`, `test_a_batch_setting_out_of_range_is_refused_naming_the_key_and_its_range`, `test_the_former_flag_is_refused_by_the_parser_before_anything_is_read`; `test_parser.py`'s argv | `tests/py/test_drive_set.py`, `tests/py/test_parser.py` |
| 2.3 | the logic tier, its fixtures naming `runs` and the new `review` keys, every expected stream the drive's label | `tests/py/` |
| 2.4 | `test_recfix.py`'s role record, its `Stream` the drive's label | `tests/contract/test_recfix.py` |
| 3.1 | `t-roles`, `t-journey-roles`, `t-journey-main`; `tests/lib.sh`'s `role_runs` | `tests/` |
| 3.2 | `t-briefs`, `t-hold`, `t-journey-review`, `t-journey-signals`, `t-cards`, `t-help` | `tests/` |
| 3.3 | `t-drive-set` | `tests/t-drive-set.sh` |
| 4.1 | `t-docs`'s new check | `tests/t-docs.sh` |
| 4.2 | `t-briefs`'s operator check | `tests/t-briefs.sh` |

## Requirements against the code

### main-level

- **Drives are declared in the teams file** (modified). `crew.runs_of` replaces `role_settings`: it refuses an entry naming `flume` first, then no `runs`, a `runs` that is no object, a key outside `KIND_ROLES`, a role left out, and a value other than `standing` or `on-demand`, each naming the drive and ending with `regenerate … from WRITER`. `crew.review_of` refuses a `review` naming `every` or `hours` first, then a missing `after_changes` or `after_hours`, another key, an `after_changes` that is no whole number of at least 1 (booleans refused) and an `after_hours` that is no number above 0, each naming the key with its unit and range. `fleet_of` sets `drive["runs"]` and `drive["review"]` from them; neither function reads a former key's value.
  - "A drive with no flume", "A drive with no runs", "A role crew has no kind for", "Each role standing or on demand", "A drive that names flume", "A batch setting by its former names", "A batch setting out of range": `tests/py/test_teams.py`'s `TestRoleSettings` and its parametrised refusals (`runs` as `false`, `true`, `null`, `""`, `"madswan"`, `"Standing"`, a list, naming `dispatcher`, leaving out `operator`; `flume` beside a `runs` and with none; `every`/`hours`; `after_changes` 0, `True`, 1.5; `after_hours` 0, -1, `True`; a third key).
  - "Every refusal of the file names crew's own fix": each new refusal names `WRITER`, as the cases assert.
  - The scenarios carried over unchanged keep their cases, which passed.
- **The main level is one herdr workspace** (modified). `main_sessions`, `kinds_up` and `moved_role` ask `crew.on_demand`; a role on demand gets no tab and its record is written. "Two roles run as their kinds", "A standing planner from before": `t-journey-roles`, `t-roles`.
- **A role that runs as its kind is not started by crew-role** (modified). `launch_shell` refuses by `on_demand`; `kinds_said` passes the label to `kind_said`. "Main status": `test_teams.py` 616 ("runs as its kind in stream madswan") and `t-journey-main` 263–274 ("in stream wldn").

### review-batches

- **A batch spans the drive's bolts** (modified). `plan.batch_due` reads `setting["after_changes"]` and `setting["after_hours"]` and says "`<n>` changes are due, and a batch is due after `<after_changes>`" and "`<after_hours>` hours have passed since …". "Changes from several bolts", "The time is reached", "Nothing due": `tests/py/test_batches.py`, `tests/py/test_review.py`, `t-journey-review` 96 ("a batch is due after 2").

### drive-setup

- **Every key is a flag, with no default** (modified) and **A flag crew does not accept is refused before anything is read** (modified). `crew.drive_given` reads `--runs` through `per_role`, refusing anything but `standing` or `on-demand`, and `--review` as `after_changes` and `after_hours`, each refusal naming the key with its unit and range; it writes `runs` and `review: {after_changes, after_hours}`. `plan.py`'s parser declares `--runs ROLE STANDING_OR_ON_DEMAND` and `--review AFTER_CHANGES AFTER_HOURS` and no `--flume`, so `--flume` is refused as an unrecognized argument before anything is read. "A person's Mac": `t-drive-set` and `test_drive_set.py`. "A way of running crew does not take", "A batch setting out of range", "The former flag": `test_drive_set.py`.

### crew-flake

- **The module writes crew's teams file from options named as the file names them** (modified), **Another module gives a drive its machine and its state repository** (modified) and **Every drive gives every key crew requires** (modified). `options.nix` declares `runs`, a submodule of the five roles each `types.enum [ "standing" "on-demand" ]` with no default, and `review` with `after_changes` (`types.ints.positive`) and `after_hours` (a positive number), no free-form type, so `every`/`hours` fail evaluation. `deneb.json` and `runner.json` hold the new keys byte for byte. `file.nix`'s render case asserts no drive renders `flume`, `every` or `hours`; "A role crew has no kind for" (`dispatcher`, `false`, `true`, `"always"`), "A batch setting by its former names" and "A batch setting out of range" fail evaluation as asked. `test_module_file.py` loads the pinned files ("crew reads the file the module writes").
- **The module's options say what they hold, in their units** (added). The descriptions of `runs` and `runs.<role>` carry `standingSays` and `onDemandSays`; `review.after_changes` and `review.after_hours` say what they count, their unit and range. `file.nix`'s "The descriptions" holds them to it and to naming no `` `flume` ``, `every =` or `hours =`.

### role-runs

- **A role record names its run** (modified). `asks.role_record` asks `on_demand` and writes `"Stream": label`. "The planner's record": `test_asks.py` 185 (`"Stream": "madswan"`), and `test_recfix.py` in the contract tier.
- **Role records follow the teams file** (modified). `roles_due` and `roles_lines` iterate `KIND_ROLES` by `on_demand`. "The planner moves", "An ask before main up", "The planner stands again": `test_asks.py`, `test_tell_asks.py`, `t-journey-roles`.
- **A role's work that lands is a place it launches** (modified). `role_land`'s stream is the label. "The design agent's records": `test_asks.py` 1183–1194 (stream `madswan`).

### flume-source

- **Each standing main-level role is declared at its address as its agent** and **No entry for a drive on another host or a role that runs as its kind** (modified). `source.entries` skips a role by `on_demand`. "deneb's three drives", "wldn on deneb", "A planner that runs as its kind": `tests/py/test_source.py`, `t-flume-source`.

### operator-agent

- **The operator is a main-level role** (modified). The operator on demand gets no tab or start (`main_sessions`), and a tell to it is an ask (`kind_role_of`): `test_tell_asks.py` (operator `on-demand`), `t-journey-roles` 28.
- **The operator's brief says who changes the drives on its host** (modified). `operator.md` *Changing the drives* names "how each of its roles runs, `runs`, `standing` or `on-demand`, or its batch setting, `review`'s `after_changes` and `after_hours`", and no `` its `flume` ``. "What a drive's entry says": `t-briefs`.

### host-holds-and-updates

- **A standing agent of a role that now runs as its kind is ended at its next stop** (modified). The stop's decision reads `kind_role_of` (`crew.py` 2725–2727), which asks `on_demand`. "The planner moves", "An update after the move": `t-hold` 144–156, its planner set `on-demand` by `role_runs`.

### Views (`code.8`)

`board.roles_read` gives `kinds = {role: label}` for each role on demand, so a run's view keeps its `stream` key, now the label; `answers_watched` asks `on_demand`. No view gains or loses a key, so `plugin/hooks/status.js` is unchanged, as Decision 7 says.

### No reader of the former keys

`grep -rnE "\[.flume.\]\[|role_settings|role_stream|\[.every.\]|\[.hours.\]" plugin/` finds none. The `["flume"]` reads left in `plan.py` and `board.py` are a piece's stage under `flume` in the runner's report, a different field. README, the skill and the usage name `flume`, `every` and `hours` only as keys crew refuses.

## Notes

These hold no requirement back:

- `tests/py/test_source.py` 64 keeps the name `test_the_roles_are_the_ones_a_drives_flume_names`. Its body asserts `source.ROLES == crew.KIND_ROLES`, which is right. Only the name still says `flume`.
- `fleet_of` runs `review_of` before `runs_of`. So an old entry that names both `flume` and `review.every` is refused for `review.every` first. Each refusal names its key and the writer, and the writer is told the second once it fixes the first. Decision 4 asks only that `flume` be refused before `runs` is read, and it is.
- `board.pip`'s `u["flume"]["of"]` became `.get("of")`, which changes nothing: the line runs only after `.get("of")` was found truthy.
