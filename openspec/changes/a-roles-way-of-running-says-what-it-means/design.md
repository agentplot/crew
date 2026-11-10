# Design

## Context

**What is asked.** Record 0064's amendment of 2026-11-09 (accepted) names how a drive says each role's way of running and its batch setting. The direction is the user's, in the pane, reading a drive's settings as the Boomdrive flake would write them. Of `flume = { design = false; planner = false; reviewer = false; ops = false; operator = false; };` they said: "I don't understand what this section is about and why we're turning these things off". Of a number among the settings: "a comment should explain the units/options". The names are agentplot-design's own choice:

- `runs`, in place of `flume`, names each of the five main-level roles `"standing"` or `"on-demand"`. No stream is named: it is the drive's own.
- `review`'s keys say their units: `after_changes`, a whole number of at least 1, and `after_hours`, a number above 0. The module's description of each option says its unit and its range.
- `crew drive set` takes `--runs <role> standing|on-demand`, given for each of the five roles, and `--review <after_changes> <after_hours>`.
- The file stays at version 6. A version-6 file naming `flume` or `every` is refused naming the key, and no code reads the older names (the user's rule against transition code: "I want the system to be built the way it should be and then have agents fucking fix the data transition as necessary").

`code.5` and `flake.2` were amended with the record. The record's *Consequences* name this unit: the module and its option descriptions, crew's reading of the file and its refusals, `crew drive set`, the README, the operator's brief, the crew skill and the test files.

**What crew does now.** `crew.fleet_of` (`plugin/lib/crew.py`) checks each drive's `review` for `every` and `hours`, and reads its `flume` through `role_settings` into `drive["flume"]`, a role's value `False` or a stream's name. Every reader of a role's way of running asks whether `drive["flume"][role] is not False`. Those readers are `crew.role_stream`, `kind_role_of`, `run_of`, `turn_said`, `launch_shell` and `main_sessions`; `asks.role_record` and `roles_due`; `plan.py`'s `roles_lines`, `capture_asks`, `landed_asks`, `unlanded_ask`, `role_open`, `role_land`, `moved_role`, `kinds_up`, `kinds_said`, `review_cmd` and `review_delivered`; `board.roles_read` and `answers_watched`; and `source.entries`. Three of them use the stream's name. `asks.role_record` writes it as the role record's `Stream`, which the runner launches the run in. `plan.role_land` launches the run's landing work in it. `plan.kinds_said` says it in `crew main status`, and `board.roles_read` carries it into each run's view. `plan.batch_due` reads `setting["every"]` and `setting["hours"]`. `crew.drive_given` reads `--flume` and `--review <every> <hours>`. The module, `nix/modules/options.nix`, declares `flume` and `review.every` and `review.hours`.

**How the family does it.** A drive is its stream, named by its label (agentplot/boomdrive record 0028). The address crew declares for a role in its roles file is `<label>/<role>`, which Flume reads as a role of the stream `<label>` (`teams.25`). So the stream a role's run runs in can only be the drive's label. No other tool's file changes: the runner reads a role record's `Stream` as it does now, and this change only makes it the label. swancloud's configuration and the Boomdrive flake write crew's file through `services.crew`'s options, so they write the new keys when they take the release that carries this change (record 0064's amendment, *Consequences*).

**Rules this design relies on:** `code.2`, `code.4`, `code.5` (as amended 2026-11-09), `code.7`, `code.8`, `read.1`, `roles.9`, `state.4` (core.md); `teams.25` (teams.md); `flake.2` (as amended 2026-11-09), `flake.3` (flake.md); `briefs.1` (briefs.md); `tests.4`, `tests.10`, `tests.11`, `tests.12` (tests.md); `docs.2`, `docs.4`, `docs.6`, `docs.7` (docs.md).

**Area pages this change touches:** `core.md`; `teams.md` (`plugin/lib/crew.py`, `plugin/bin/crew`); `plan.md` (`plugin/lib/plan.py`); `briefs.md` (`plugin/roles/operator.md`, `plugin/skills/crew/SKILL.md`); `flake.md` (`nix/`); `tests.md` (`tests/`); `docs.md` (README, `openspec/`). No rule changes here: `code.5` and `flake.2` already say what this builds (`docs.7`).

## Goals / Non-Goals

**Goals:**
- A drive names each role's way of running as `runs`, `standing` or `on-demand`, and its batch setting as `after_changes` and `after_hours`, in crew's reading, its module, `crew drive set`, and every text that tells a person or an agent how to write them.
- An on-demand role's run runs in the drive's own stream, and crew names the drive's label wherever it names that stream.
- A file that names `flume`, `every` or `hours` is refused naming the key, and nothing reads those names.

**Non-Goals:**
- A new version of the teams file (record 0064's amendment: "Version 7. A new version for names no host has written.").
- Renaming "runs as its kind", the phrase the specs, briefs and words of `crew main status` use for a role whose runs Flume runs. That names the mechanism, and stays. This change renames only the teams file's keys, the flags and the texts that name them.
- Any change to what a role run does, how the runner launches it, or how a batch is reckoned beyond the names of its setting.
- Any change to how a kit's work names its stream: kit work names none, the runner's configuration giving it (`roles.9`).
- Writing swancloud's configuration or the Boomdrive flake; each takes the release on its own side.

## Decisions

### 1. `runs` holds a word for each role, and `on_demand` is the one question

`crew.runs_of(entry, what)` replaces `role_settings`. It reads `runs` as an object naming each role of `KIND_ROLES` and no other, each `"standing"` or `"on-demand"`, and `fleet_of` sets `drive["runs"]` to it. Every check runs before any value is used, and each refusal names the drive, the key and crew's own module, `services.crew`, `crew drive set`, or the machine's configuration that writes the file (`WRITER`), as every refusal of the file does (`code.5`, `read.1`). Each role is still written out, never one value for all (record 0065, point 2).

One function answers every reader: `crew.on_demand(drive, role)`, true where the drive's `runs` names the role `on-demand`. `crew.role_runs(fleet, label, role)` replaces `role_stream` for callers that hold a fleet and a label. It answers the word, refusing a role outside `KIND_ROLES` and a drive the file does not name, as `role_stream` did. Every `drive["flume"][role] is not False` becomes `on_demand(drive, role)`, and every `role_stream(...) is False` becomes `role_runs(...) == "standing"`.

Not taken:
- **Keeping `drive["flume"]` inside crew, mapped from `runs` at load.** Crew's readers would then speak a name no file holds, and the next reader would have to learn both.
- **A boolean, `drive["on_demand"][role]`, inside crew.** The file's word is the one fact. A second shape of it in memory is a translation to keep in step.

### 2. An on-demand role's stream is its drive's label

The stream is named nowhere in the file. Wherever crew names it, it names the drive's label:
- `asks.role_record`'s `Stream`, which the runner launches the run in.
- `plan.role_land`'s launch of the run's landing work.
- `plan.kinds_said`'s words in `crew main status`, "runs as its kind in stream `<label>`".
- `board.roles_read`'s `kinds`, `{role: label}` for each role on demand, from which each run's view takes its `stream`.

`roles.rec` keeps its `Stream` field, since the runner reads it, and crew writes the label there. A record written before this change with another stream differs from the one `roles_due` wants, so `crew main up` and the next ask of the role write it again (role-runs, "Role records follow the teams file"). No reading of the old value is needed for that.

Not taken: **leaving the stream out of the role record.** The runner reads `Stream` from it today. Removing the field is a change to the runner's reading, which this change does not make.

### 3. `review` is `after_changes` and `after_hours`

`fleet_of` checks `review` as an object with exactly `after_changes`, a whole number of at least 1 and no boolean, and `after_hours`, a number above 0 and no boolean. Each refusal names the key with its unit and range: "'review.after_changes' is how many of the drive's constructed changes, waiting for the user's read, make a batch due, a whole number of at least 1, not …". `plan.batch_due` reads `setting["after_changes"]` and `setting["after_hours"]`. Its reason for a batch made due by its count reads "`<n>` changes are due, and a batch is due after `<after_changes>`". Its reason by the hours keeps its words, "`<after_hours>` hours have passed since …", which already name their unit.

### 4. The former names are refused, and read nowhere else

`fleet_of` refuses a drive's entry that holds `flume`, whatever else it gives, before it reads `runs`. The refusal names the drive and `flume`, says the file names how each of its roles runs under `runs`, each `standing` or `on-demand`, and names `WRITER`. A `review` that holds `every` or `hours` is refused the same way, naming `review.every` or `review.hours` and saying the batch setting is `review.after_changes` and `review.after_hours`. These are the record's own refusals ("A version-6 file naming `flume` or `every` is refused naming the key"). Each reads only whether the key is there, never its value, so nothing maps an old value to a new one.

Without them, a file naming only the old keys would be refused for lacking `runs`, naming none of what the host's writer must change. A file naming both would load with a key crew ignores beside the one it reads.

### 5. The module declares `runs` and `review`'s new keys, each description saying what it holds

`nix/modules/options.nix` declares a drive's `runs` as a submodule of the five roles of `kindRoles`, each `types.enum [ "standing" "on-demand" ]` with no default. It declares `review` as a submodule of `after_changes`, `types.ints.positive`, and `after_hours`, the positive number it already declares for `hours`. The descriptions say what each holds:
- `runs`: "How each of the drive's main-level roles runs: `"standing"`, crew keeping the role's agent running in its pane on the drive's machine, or `"on-demand"`, the host's runner having Flume run the role in the drive's own stream, named by its label, while something is pending for it, each run ending when its work is done. Every role is named."
- `runs.<role>`: "How the `<role>` runs: `"standing"`, … or `"on-demand"`, …", with the same two clauses.
- `review`: "The drive's batch setting: a batch of its constructed changes is due for the user's read once `after_changes` of them wait, or once `after_hours` hours have passed since its last batch with at least one waiting, whichever comes first."
- `after_changes`: "How many of the drive's constructed changes, waiting for the user's read, make a batch due: a whole number of at least 1."
- `after_hours`: "How many hours since the drive's last batch make one due while at least one change waits: a number above 0, such as 4 or 1.5."

The `review` submodule declares no free-form type, so `every` or `hours` there fails evaluation by itself. A drive's `flume` passes to the file through the drive's free-form type, and crew refuses it at load (Decision 4). That is the place `flake.2` leaves a key the module does not declare.

Not taken: **an assertion in the module refusing a drive's `flume`, as it refuses `teams`.** It would be a second place naming the old key. `teams` is refused there because no drive could mean it. `flume` is refused once, by crew, in words that name `runs`.

### 6. `crew drive set` takes `--runs` and `--review <after_changes> <after_hours>`

`crew.drive_given` reads `--runs` through its `per_role`, as it reads `--accounts`. Each value is `standing` or `on-demand`, and anything else is refused: "--runs gives the planner "false", and a role runs standing or on-demand". It reads `--review`'s two words as `after_changes` and `after_hours`, with the checks it makes now, each refusal naming the key with its unit and range. It writes them as the file names them, `after_hours` a whole number where its value is one, as it does now. `plan.py`'s parser declares `--runs` with `metavar=("ROLE", "STANDING_OR_ON_DEMAND")` and `--review` with `metavar=("AFTER_CHANGES", "AFTER_HOURS")`, and drops `--flume`. `Strict.error` then refuses a `--flume` as an unrecognized argument before anything is read (`code.2`).

### 7. The views keep their shape, so the mod is unchanged

`board.agent_views` gives no view a drive's `runs` or `review`. A role's run view keeps its `stream` key, now always the drive's label (Decision 2). `plugin/hooks/status.js` reads no stream. So nothing the views draw moves, and `code.8` asks no change of the mod.

### 8. The texts name the new keys

README, the crew skill, the usage headers of `plugin/bin/crew` and `plugin/lib/plan.py`, and the operator's brief describe a drive's `runs` and its batch setting by the new names (`docs.2`). Each text names no `flume` as a key of the teams file and no `--flume`. `tests/t-docs.sh` and `tests/t-briefs.sh` hold them to it.

## Risks / Trade-offs

- **A host's file naming the old keys is refused by the release that carries this.** No host writes a version-6 file yet: deneb's file is version 5, under the crew 0.49.0 swancloud pins (record 0064's amendment). So the first crew a host loads at version 6 reads the new names, and its writer writes them in the same bump. The refusal names the key and the writer either way.
- **A role record written before with another stream is written again.** That is one commit on the drive's branch at the next `crew main up` or ask, and the run launches in the drive's stream from then on. No drive runs a role on demand today: every drive's file names every role `false`.

## Migration Plan

None of crew's own. The file's writers, swancloud's configuration and the Boomdrive flake, write `runs` and the new `review` keys when they take crew's release (record 0064's amendment, *Consequences*), each in its own repository.

## After deploy

None. Every behaviour here is proved by the logic tier, the module's own test and the end-to-end tests the tasks name. A host's file is written by its own configuration when that takes the release, which is that repository's work and no step of this change's (`docs.6`).

## Task notes

**1.1** `nix/modules/options.nix`:
- Declare `runs` in place of `flume`, and `review`'s `after_changes` and `after_hours` in place of `every` and `hours`, with the descriptions Decision 5 gives.
- Give the drive's `review` and `runs` options their descriptions, and name `runs` in the head comment's list of a drive's keys.

`nix/tests/settings.nix`:
- `standing` gives each role `"standing"`, `review` gives `after_changes = 5; after_hours = 4;`, and each drive gives `runs = standing;`.
- Its head comment says the drives carry `runs` and `review` as record 0064's amendment of 2026-11-09 names them.

`nix/tests/files/deneb.json` and `runner.json`:
- In each drive, replace `flume` with `"runs"` naming every role `"standing"`, and `review` with `{"after_changes":5,"after_hours":4}`.
- Write them as crew's module writes them: keys sorted, no space, no newline after (`crew.teams_text`).

`nix/tests/file.nix`:
- `dispatcher` gives `runs.dispatcher = "standing"`.
- `planner` gives `runs.planner = false`, with cases beside it for `true` and `"always"`.
- New cases fail evaluation for `review = { every = 5; hours = 4; }`, for `after_changes = 0` and for `after_hours = 0`.
- A new case, "The descriptions", evaluates `options.nix` as `evaluated` does but takes `.options`. It reads a drive's options through `options.services.crew.settings.type.getSubOptions [ ]`, then `.drives.type.nestedTypes.elemType.getSubOptions [ ]`, and `runs`' and `review`'s own through their `type.getSubOptions [ ]`.
- That case expects the descriptions of `runs` and `runs.planner` to hold `"standing"` and `"on-demand"`, that of `review.after_changes` to hold "changes" and "at least 1", and that of `review.after_hours` to hold "hours" and "above 0". It expects none of them to hold the text `` `flume` ``, `every =` or `hours =`.

**2.1** `plugin/lib/crew.py`, crew's reading of the file (Decisions 1, 3 and 4):
- `runs_of(entry, what)` in place of `role_settings`. In order, it refuses:
  - an entry holding `flume`;
  - no `runs`;
  - a `runs` that is no object;
  - a key outside `KIND_ROLES`;
  - a role left out;
  - a value other than `"standing"` or `"on-demand"`, the refusal naming `runs.<role>` and both words.
- Each refusal ends `: regenerate {TEAMS} from {WRITER}`, as `role_settings`' do now. `fleet_of` sets `drive["runs"] = runs_of(p, what)` where it sets `drive["flume"]` now.
- `review`'s check in `fleet_of`:
  - a `review` holding `every` or `hours` is refused first, naming `review.every` or `review.hours`;
  - then both `after_changes` and `after_hours` must be there, and no other key;
  - `after_changes` is an `int` and no `bool`, at least 1;
  - `after_hours` is an `int` or `float` and no `bool`, above 0;
  - each refusal names the key with its unit and range;
  - the comment above the check follows (`briefs.12`).
- Add `on_demand(drive, role)`. Add `role_runs(fleet, label, role)` in place of `role_stream`, keeping its refusals of a role outside `KIND_ROLES` and of a drive the file does not name.
- Move `kind_role_of`, `run_of`, `turn_said`, `launch_shell` and `main_sessions` to `on_demand`, with their docstrings.

Cases in `tests/py/test_teams.py`:
- Every fixture names `runs` and `after_changes`/`after_hours` (`STANDING` becomes `{r: "standing" for r in crew.KIND_ROLES}`).
- `TestRoleSettings`, rewritten for `runs`: madswan's planner and reviewer `on-demand` and the rest `standing`; `drive["runs"]` is the file's, and `role_runs` and `on_demand` answer each role.
- Refused, each naming madswan, the key and `crew.WRITER`:
  - no `runs`;
  - `runs` as a list;
  - `runs` naming `dispatcher`;
  - `runs` leaving out `operator`;
  - `runs.planner` as `false`, `true`, `null`, `""`, `"madswan"` or `"Standing"`;
  - `flume` beside a good `runs`, and `flume` with no `runs`;
  - a `review` with `every` and `hours`;
  - `after_changes` as 0, `True` or `1.5`;
  - `after_hours` as 0, `-1` or `True`;
  - a third key under `review`.
- `kind_role_of`'s cases, and `role_runs`' refusals, as `role_stream`'s are today.
- `test_main_status_says_…` passes the label where it passes `madswan-main`.

**2.2** `plugin/lib/crew.py` `drive_given` (Decision 6):
- `per_role("--runs", "how each role runs, standing or on-demand", runs)`, where `runs(role, v)` refuses anything but `standing` or `on-demand`.
- `--review`'s two words are `after_changes` and `after_hours`, each refusal naming the key with its unit and range.
- The drive dict holds `"runs"` and `"review": {"after_changes": …, "after_hours": …}`.

`plugin/lib/plan.py`'s `drive set` parser:
- `--runs` in place of `--flume`, and `--review`'s metavars `AFTER_CHANGES` and `AFTER_HOURS`.
- The comment above the parser, `crew.py`'s section comment and `drive_set`'s docstring name `--runs`.

Cases in `tests/py/test_drive_set.py`:
- `flags()` gives `--runs <role> standing` for each role.
- A drive given the planner `on-demand` has `runs.planner == "on-demand"` and `runs.ops == "standing"`.
- `--review 3 1.5` gives `{"after_changes": 3, "after_hours": 1.5}`, and `5 4.0` gives `{"after_changes": 5, "after_hours": 4}`.
- `--runs planner false`, `pat-work`, `true` and `Standing` are each refused naming `--runs`, the planner and both words.
- `--review 0 4` and `5 0` are each refused naming the key and its range.
- `--flume design false` beside every flag is refused by the parser naming `--flume`.
- The data of the pinned files is written as their bytes, as now.

`tests/py/test_parser.py`'s argv names `--runs`.

**2.3** The other readers of a role's way of running, each moved to `crew.on_demand` or `crew.role_runs` (Decision 1), with the stream named by the drive's label (Decision 2):
- `plugin/lib/asks.py`: `role_record` (`"Stream": label`, `None` for a standing role) and `roles_due`.
- `plugin/lib/plan.py`: `roles_lines`, `capture_asks`, `landed_asks`, `unlanded_ask`, `role_open`, `role_land` (its `stream` the label), `moved_role`, `kinds_up`, `kinds_said` (passing the label to `kind_said`), `review_cmd` and `review_delivered`.
- `plugin/lib/board.py`: `roles_read` (`kinds = {r: label for r in crew.KIND_ROLES if crew.on_demand(p, r)}`) and `answers_watched`.
- `plugin/lib/source.py`: `entries`.

Their docstrings name `runs` where they name `flume` now. `plan.batch_due` reads `setting["after_changes"]` and `setting["after_hours"]`, gives its count's reason as "`{n}` changes are due, and a batch is due after `{after_changes}`", and its docstring follows (Decision 3). No reader of a drive's `flume` remains: `grep -rn '\["flume"\]\[' plugin/lib` finds nothing.

Fixtures in `tests/py/`:
- Every drive naming `flume` names `runs` instead, a stream's name becoming `"on-demand"` and `False` becoming `"standing"`.
- Every expected `Stream`, stream word or run view's `stream` becomes the drive's label: `madswan-main` and `madswan-roles` become `madswan`, `wldn-main` becomes `wldn`, `swancloud-main` becomes `swancloud`.
- Every `review` names `after_changes` and `after_hours`. The expected batch words in `test_batches.py` and `test_review.py` follow.
- The files: `facts.py`, `test_asks.py`, `test_tell_asks.py`, `test_batches.py`, `test_board.py`, `test_card_commands.py`, `test_hold.py`, `test_kit_rename.py`, `test_repository_rename.py`, `test_landing.py`, `test_plan_roles.py`, `test_proposal_card.py`, `test_review.py`, `test_signals.py`, `test_source.py`, `test_release.py`, `test_rail.py`, `test_module_file.py` (each drive's `runs` all `"standing"`, its docstring following), and any other the logic tier finds.

**2.4** `tests/contract/test_recfix.py`: its drive names `runs`, the planner and ops `on-demand`, and its role record's expected `Stream` is the drive's label.

**3.1** `tests/lib.sh`:
- The fixture's three drives give `"review": {"after_changes": 5, "after_hours": 4}` and `"runs"` naming every role `"standing"`.
- `role_stream` becomes `role_runs <label> <role> standing|on-demand`, writing `['runs']['<role>']`, with its comment saying so.

`t-roles.sh`, `t-journey-roles.sh` and `t-journey-main.sh` call `role_runs`, a stream's name becoming `on-demand` and `false` becoming `standing`. Where they read the stream, they read the drive's label:
- `t-journey-main.sh` 256 and 263 to 274: `wldn`.
- `t-journey-roles.sh` 39, 137, 140 and 163: `madswan`.

No test's `# Reads:` line changes, so `tests/moon.yml` stays as `tests/moon-tasks` writes it.

**3.2** `t-briefs.sh`, `t-hold.sh`, `t-journey-review.sh`, `t-journey-signals.sh`, `t-cards.sh` and `t-help.sh` call `role_runs` as in 3.1. `t-journey-review.sh` 96 expects "a batch is due after 2".

**3.3** `tests/t-drive-set.sh`'s `set_pat` gives `--runs <role> standing` for each role in place of `--flume <role> false`.

**4.1** `README.md`:
- Line 5's account of the teams file names `runs` where it names `flume`, and `review: {after_changes, after_hours}` where it names `review: {every, hours}`.
- The usage block (127) shows `--runs <role> standing|on-demand... --review <after_changes> <after_hours>`.
- `crew drive set`'s paragraph (147) names `--runs` once for each of the five roles.
- The run-as-its-kind paragraph (220) says a role runs on demand by its drive's `runs`: an object naming each of the five roles, `standing` while it stands as above or `on-demand`, the host's runner having Flume run it in the drive's own stream, named by its label. It keeps "every role stands" for a drive naming every role `standing`, and keeps the refusals it lists, `flume` among them.
- The batches paragraph (236) names `review`'s `after_changes` and `after_hours`.
- `roles.rec`'s `Stream` (141) is the drive's label.

`plugin/skills/crew/SKILL.md` makes the same changes at 16, 61 and 85. The usage headers of `plugin/bin/crew` (56–57) and `plugin/lib/plan.py` (18) show `--runs <role> standing|on-demand... --review <after_changes> <after_hours>`.

`tests/t-docs.sh` gains a check:
- The usage, README and skill each have `--runs <role> standing|on-demand` and `--review <after_changes> <after_hours>`.
- README and the skill have `after_changes` and `on-demand`.
- None has `--flume`, `` its `flume` ``, `` names `flume` on every drive `` or `` `every` changes ``.

Its `ok` line at 163 says "a drive's runs" where it says "a drive's flume".

**4.2** `plugin/roles/operator.md` *Changing the drives* (51) names, among what a drive's entry says, "how each of its roles runs, `runs`, `standing` or `on-demand`, or its batch setting, `review`'s `after_changes` and `after_hours`", where it names "its `flume` or its batch setting". `tests/t-briefs.sh` checks that the operator's brief has `` `runs`, `standing` or `on-demand` `` and `` `after_changes` and `after_hours` ``, and lacks `` its `flume` ``.
