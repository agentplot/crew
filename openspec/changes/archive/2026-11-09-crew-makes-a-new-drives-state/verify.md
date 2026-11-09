# Verify: crew-makes-a-new-drives-state

Verified 2026-11-09 on `change/crew-makes-a-new-drives-state` at a534e0b9. The branch was cut from `bolt/crew-names-each-drive-once`.

## The whole checks

`tests/suite` ran once. It runs every project's `check-full` tasks, which `.config/sluice.toml` requires of `bolt/*` and `main`. It ended `35 passed (4 replayed), 0 failed` and exited 0.

- Tiers: `logic`, `contract` and `mod`.
- The flake's checks: `nix:format`, `nix:lint`, `nix:test` and `nix:typecheck`.
- Every end-to-end task in `tests/moon.yml`, the new `t-drive-set` among them.

A replayed task is one whose inputs match a run that passed on this host (`tests.5`). This change touches crew's command core, so every task that takes the core ran afresh. Four were replayed: `mod`, `nix:format`, `nix:lint` and `t-docs`.

## Tasks

All 12 tasks in `tasks.md` are ticked. Each task's check is either one of the suite's tasks above or a pytest file in the `logic` tier, and every one passed.

## Specs

`openspec validate crew-makes-a-new-drives-state --strict` passes.

How the code meets each requirement:

- **drive-setup, Every key is a flag, with no default.**
  - `plan.parser()` gives `drive set` one flag per key. Each flag is `action="append"` with no default, and a flag of several words takes them as separate arguments.
  - `crew.drive_given` requires every flag except `--roles`, `--console` and `--repositories`.
  - Proved by `TestDriveGiven.test_a_persons_mac` and its neighbours, and by `test_parser.py`'s `drive set` run.
- **drive-setup, A flag crew does not accept is refused before anything is read.**
  - `drive_given` runs first in `plan.drive_set`, before any fetch or file read.
  - Each refusal names its flag and ends "nothing was read or written".
  - `--accounts` and `--flume` are refused when a role is left out, given twice or unknown. `--flume true` is refused.
  - Proved by the refusal cases of `TestDriveGiven`.
- **drive-setup, The flags agree before anything is read.**
  - Four mismatches are refused by `drive_given`, each with its own case:
    - a first `--blueprints` that is not among `--repos`;
    - a `--machine` that is not among `--hosts`;
    - a `--repositories` address that is not among `--repos`;
    - `--repositories` for a machine other than this host.
- **drive-setup, The file is written as crew's module writes it.**
  - `crew.teams_text` writes the file as sorted, compact JSON with no newline.
  - `test_the_module_files_are_written_again_byte_for_byte` rewrites `nix/tests/files/deneb.json` and `runner.json` byte for byte.
  - `drive_set` writes `teams.json.<pid>.new` and renames it over the old file.
- **drive-setup, The drive's facts are replaced and the rest of the file is kept.**
  - `crew.teams_set` replaces the drive's entry whole. It sets the given hosts, sets or removes the drive's console, and keeps every other drive, host, console and key.
  - It leaves out a `consoles` or `repositories` that ends up empty.
  - Proved by `TestTeamsSet`, including the cases "A second drive" and "A role's override no longer given".
- **drive-setup, A kept repository stays while a drive of the host keeps it.**
  - `teams_set` keeps a kept repository the file names only while another drive of this host lists it.
  - Proved by the cases for a repository removed from the drive, one another drive of the host keeps, and one only a drive of another host lists.
- **drive-setup, The file it would write is checked before it is written.**
  - `teams_step` checks the text it would write with `crew.fleet_of`. A refusal says "the teams file crew drive set would write is refused:" in `fleet_of`'s words and ends "Nothing was written."
  - Proved by the case "Two accounts in one session".
- **drive-setup, Run again with the same answers, it changes nothing.**
  - `teams_step` answers `unchanged` when the text would be the file's own.
  - `state_init` takes no step on a finished branch.
  - No changed key means no entry is written.
  - `t-drive-set` runs the same command twice. The file's bytes, the branch's commit count and the run record all stay as they were, and it answers `unchanged` and `exists`.
- **drive-setup, Where Nix links the teams file, nothing is written there.**
  - Where the linked file names the drive as given, `teams_step` answers `linked` with the link's target, and `drive_set` goes on to `state_init`.
  - Otherwise it refuses, naming the keys that differ or are missing and `services.crew.settings.drives.<label>`, with nothing made.
  - The cases cover a link that names the drive, one that names no drive `pat`, one that gives other `repos` and no console, and a link crew cannot read or load.
- **drive-setup, A teams file crew cannot load is moved aside once.**
  - For a file crew cannot load, `teams_step` answers `aside` with the reason: a version-5 file, a file that is no JSON, one that lists no drives, and JSON that is no object.
  - It refuses, naming both paths, when the aside is already taken.
  - `drive_set` moves the file by hard-linking it to `teams.json.before-drive-set`, then renames the new file over it. If the link fails because the aside is taken, it refuses with nothing written.
- **drive-setup, A drive's state is made as crew state init makes it.**
  - `drive_set` fetches `<label>/main` with `tip_of` before it takes the lock. Then it calls `state_init`, which now returns what it did.
  - `t-drive-set` covers two cases:
    - a repository crew cannot fetch is refused naming it, and no teams file is made;
    - an empty state repository gets `pat/main` with `plan.rec`, `moves.rec` and `proposals.rec`.
  - `t-journey-state` passes, so `crew state init` still says what it said before.
- **drive-setup, A set is one entry naming what it changed.**
  - `record.emit(label, "drive.set", ["drive/<label>"], why=...)` runs after the state is made, and only when a key changed.
  - In `t-drive-set` the entry's `On` is `drive/pat` and its `Why` is `set drives.pat, hosts.mac-studio, consoles.pat`. It names paths only, never values.
  - `main` asks no `may_write` for `drive set`.
- **drive-setup, crew drive set runs on the host it is invoked on.**
  - `plugin/bin/crew`'s `drive` arm executes `plan.py` directly, never forwarding.
  - `main` runs `drive set` before any teams file is loaded.
  - `t-drive-set` finds no ssh in the stub log.
- **drive-setup, Its answer is plain or JSON.**
  - `crew.drive_said` writes a line for a moved file first, then one line for the file and one for the state. With `--json` it writes one object.
  - Proved by `TestDriveSaid` and by `t-drive-set`'s `--json` run.
- **drive-setup, crew's agents start on the drive it set.**
  - In `t-drive-set`, `crew main up pat` starts pat-design, pat-planner, pat-ops and pat-operator, with the planner in `<folder>/blueprints/main`.
- **main-level, Drives are declared in the teams file.**
  - `crew.WRITER` now names `crew drive set`.
  - A missing file is refused naming `WRITER`.
  - `read_teams` refuses a file that is no JSON or no UTF-8, naming the file and the parser's words. `fleet_of` refuses JSON that is no object.
  - `fleet_of(data, here)` answers as `load` does, and reads `here` only where the file names kept repositories.
  - Proved by `test_teams.py`, and by `t-teams`, where `crew bolts` with no teams file names `crew drive set`.
- **operator-agent, The operator's brief says who changes the drives on its host.**
  - `operator.md`'s *Changing the drives* covers both cases:
    - a teams file that is no link into the Nix store changes through Boomdrive's setup with `crew drive set`, never by a hand edit;
    - the swancloud steps are for a link.
  - `t-briefs` pins the phrases.
- **Docs (`docs.2`).**
  - README's *State*, `plugin/skills/crew/SKILL.md`, both usage headers (`plugin/bin/crew` and `plan.py`) and `openspec/config.yaml` name `crew drive set`.
  - None of them still says the crew command never writes the file.
  - `t-docs` passes.

## Outcome

The checks pass and the work holds. The change is archived with this report.
