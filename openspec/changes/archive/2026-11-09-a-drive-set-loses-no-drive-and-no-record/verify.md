# Verify: a-drive-set-loses-no-drive-and-no-record

Verified 2026-11-09 on `change/a-drive-set-loses-no-drive-and-no-record` at a385f1c6. The branch was cut from `bolt/crew-names-each-drive-once`.

## The whole checks

`tests/suite` ran once. It runs every project's `check-full` tasks, which `.config/sluice.toml` requires of `bolt/*` and `main`. It ended `35 passed (4 replayed), 0 failed` and exited 0.

- Tiers: `logic`, `contract` and `mod`.
- The flake's checks: `nix:format`, `nix:lint`, `nix:test` and `nix:typecheck`.
- Every end-to-end task in `tests/moon.yml`, `t-drive-set` and `t-journey-state` among them.

A replayed task is one whose inputs match a run that passed on this host (`tests.5`). This change touches crew's command core, so every task that takes the core ran afresh. Four were replayed: `mod`, `nix:format`, `nix:lint` and `t-docs`.

## Tasks

All 7 tasks in `tasks.md` are ticked. Each task's check is either a pytest file in the `logic` tier (`test_teams.py`, `test_drive_set.py`, `test_record.py`) or one of the suite's tasks (`t-drive-set`, `t-docs`). The whole run above ran every one of them.

## Specs

`openspec validate a-drive-set-loses-no-drive-and-no-record --strict` passes. The delta's requirement names match `openspec/specs/drive-setup/spec.md`: the renamed one is at line 91, and the two modified ones are at lines 73 and 113.

How the code meets each requirement of the delta:

- **A teams file crew cannot read at all is moved aside once** (renamed from "… cannot load …").
  - `crew.known` makes `fleet_of`'s object and version checks, with their words unchanged, and `fleet_of` calls it first. `crew.readable` is `known(read_teams(text))`, and `load` reads through it.
  - `teams_step` takes the aside path only where `readable` refuses: no JSON, no UTF-8, no object, or a version this crew does not read, a missing one among them. The aside's path and its refusal when taken are unchanged.
  - Proved by:
    - `TestReadable` in `test_teams.py`: `readable` refuses eight files in exactly the words `load` gives for the same bytes.
    - `TestTeamsStep.test_a_file_crew_cannot_read_at_all_is_moved_aside_with_its_reason`: version 5, no JSON, no UTF-8, `{}` and `[]` are each moved aside with their reason.
    - `test_an_aside_already_taken_is_refused_naming_both_paths`.
- **A teams file at crew's own version that fails a check is refused** (added).
  - Where `readable` gives the data and `fleet_of` refuses it, `teams_step` refuses with these words: "… is at crew's version 6 and fails a check: `<fleet_of's words>` crew drive set moves aside only a file crew cannot read at all, so the file and every drive it names are left as they are, and nothing was written". It refuses this way whether or not the aside is taken.
  - `drive_set` calls the step under its lock before it writes the new file or links the aside. So nothing is written, nothing is moved and no state is made.
  - Proved by:
    - `test_a_file_at_crews_own_version_that_fails_a_check_is_refused_and_never_moved_aside`: the scenario's file names `lab` and `pat`, with `lab`'s folder relative. The refusal names `lab`'s folder, with the aside both free and taken.
    - `test_a_version_6_file_that_lists_no_drives_or_lists_teams_is_refused_not_moved_aside`.
    - `TestReadable.test_a_file_at_crews_own_version_is_read_and_fleet_of_refuses_it`.
- **A set is one entry naming what it changed** (modified).
  - Where the step changed a key, `drive_set` appends the `drive.set` entry with `record.emit(..., push=False)` once the file is renamed into place and before `state_init` runs. The entry is on `drive/<label>`, and its `Why` names the keys' paths and no values.
  - Where the branch is new, the state's first `state.init` write pushes the entry, oldest first.
  - The command's last act, `record.reach(label, eid, said=True)`, pushes whatever of the host's record of the drive the branch still lacks. A refused push is said once on standard error and changes nothing of the answer or the exit.
  - The emit after the state is gone. `main` still asks no `may_write` for `drive set`.
  - Proved by:
    - `test_record.py`: `test_an_entry_emitted_without_its_push_is_in_the_hosts_file_and_nothing_is_pushed` and `test_a_push_said_and_refused_is_said_once_and_goes_on`.
    - `t-drive-set`: `pat/main`'s run record holds one `drive.set` entry on `drive/pat`, whose `Why` is `set drives.pat, hosts.mac-studio, consoles.pat`.
- **A state not made is finished by the same command again** (added).
  - `state_init`'s refusal is raised again in `crew.state_unmade`'s words: "`<teams>` names drive `<label>` as given, and its state was not made: `<words>`. crew drive set `<label>` run again with the same flags makes it."
  - Once the teams step is done, `drive_set_refused` records the refusal as a refused `state.init` on `plan/<label>` (`CONTEXT["teams_done"]`). The host keeps the set's entry, and the next run's first state write pushes it before its own.
  - Proved by:
    - `TestStateUnmade`, which checks the words whether the refusal ends with no period, with one, or with one and a newline.
    - `t-drive-set`'s new wiring. A `pre-receive` hook refuses every push. The first run is refused with both phrases, `crewpy labels` reads `pat`, and the remote has no `pat/main`. The host's record holds one `drive.set` entry and one refused `state.init` on `plan/pat`.
    - Then, with the hook removed, the same command says the file names drive pat as given with nothing written, and makes `pat/main` with `plan.rec`, `moves.rec` and `proposals.rec`. The branch's record holds the first run's `drive.set`, the same `Id`, and one refused `state.init`.
- **Run again with the same answers, it changes nothing** (modified).
  - `teams_step` answers `unchanged`, and no key changed, so no entry is appended. `state_init` takes no step on a finished branch.
  - The last `reach` finds nothing the branch lacks, so it makes no commit.
  - Proved by `t-drive-set`'s last case. The second run's file bytes, the branch's commit count and the run record are as before, and it answers `unchanged 0 exists`.
- **Unchanged by the change**: the teams file's version and keys, `fleet_of`'s checks and words, a link's handling, the answer's lines and JSON, and `crew state init`. `t-journey-state` and the `TestTeamsStep` link cases pass.
- **Views and mod (`code.8`)**: nothing crew models changes, so `board.agent_views` and `plugin/hooks/status.js` are untouched, and `mod` passes.
- **Docs (`docs.2`)**: README's *State*, `plugin/skills/crew/SKILL.md` and the usage headers of `plugin/bin/crew` and `plugin/lib/plan.py` say what this change builds:
  - only a file crew cannot read at all is moved aside;
  - a file at crew's own version that fails a check is refused;
  - the set's entry is written once the file is and pushed with the state;
  - a state not made is refused as a `state.init` that the same command run again finishes.

  `t-docs` passes.

Observation, not a shortfall: `teams_step`'s refusal of a taken aside still says "a file crew cannot load (…)". Task note 1.2 keeps "the aside's taken refusal as now", and its test pins those words. `drive_set`'s own refusal for an aside taken in a race now says "cannot read at all". The two texts differ, and the spec asks only that both paths are named.

Observation, not a shortfall: once archived, `openspec validate drive-setup --type spec --strict` gives one warning, which strict counts as a failure. The requirement "A set is one entry naming what it changed" is over 500 characters: the delta grows it from 326 to 613. The change's own `--strict` validation passes, and so does the spec's without `--strict`. 19 other specs on the branch already fail `openspec validate --specs --strict`. Splitting the requirement is the design agent's to judge.

## Outcome

The checks pass and the work holds. The change is archived with this report.
