# Verify: crew-runs-from-its-own-file-alone

Verified 2026-11-08 on `change/crew-runs-from-its-own-file-alone` at c0038d25. The branch was cut from `bolt/crew-names-each-drive-once`.

## The whole checks

`tests/suite` ran once, every project's `check-full` tasks, as `.config/sluice.toml` requires of `bolt/*` and `main`. It ended `34 passed (21 replayed), 0 failed` and exited 0.

- Tiers: `logic`, `contract` and `mod`.
- The flake's checks: `nix:format`, `nix:lint`, `nix:test` and `nix:typecheck`.
- Every end-to-end task in `tests/moon.yml`.

A replayed task is one whose inputs are identical to a run that passed on this host (`tests.5`). This change touches crew's command core, so every task is affected. `contract`, `nix:test`, `nix:typecheck`, `t-flume-source`, `t-help`, `t-journey-board`, `t-journey-land`, `t-journey-main`, `t-journey-roles`, `t-journey-state`, `t-slot`, `t-suite` and `t-word` ran afresh.

## Tasks

All 39 tasks in `tasks.md` are ticked. Each one's check is one of the suite's tasks above, or a pytest file inside the `logic` tier, and all of them passed.

## Specs

`openspec validate crew-runs-from-its-own-file-alone --strict` passes.

At first it failed. `a-teams-file-refusal-names-crews-own-module` archived onto the bolt (325a3c33) after this delta was written. It added the scenario "Every refusal of the file names crew's own fix" and the clause that no refusal names another repository's module. The MODIFIED block of "Drives are declared in the teams file" left both out. The design's Risks section has this stage carry the fix's words into that block when the fix archives first, so the delta now does:

- It defines the teams file's writer as `crew.WRITER` gives it: "crew's own module, `services.crew`, or the machine's configuration that writes the file".
- It carries the scenario. The scenario's refusals now include this change's new keys, which `tests/py/test_teams.py`'s `test_every_refusal_of_the_file_names_crews_own_module_and_no_other_repositorys` already covers (`hosts`, `folder`, `repos`, `accounts`, `consoles`).

Each requirement, as the code meets it:

- **main-level, Drives are declared in the teams file.**
  - `crew.load` reads `teams.json` alone. Nothing under `plugin/` names `herdr-hosts.json` or `~/.config/swancloud/`.
  - `hosts_of`, `accounts_of` and `consoles_of`, and `load`'s checks on `folder`, `repos`, the first blueprints repo, `machine in hosts` and one account per session, refuse as the scenarios say. Each refusal names `WRITER`.
  - A role's `session` is checked against nothing.
  - `kept_at` and `kept` give the `repositories` entry for this host, else `<folder>/<name>` in the first drive's folder that lists the repository.
  - Proved in `tests/py/test_teams.py`, `test_kits.py` and `t-teams`. That includes the "no hosts file" and "hosts file read for nothing" cases.
- **crew-command, crew runs itself on another host.**
  - `crew_on` refuses "keeps no checkout of <repo>, the repository crew is, as the teams file gives it", and follows no former address.
  - `ssh_of` refuses a host `hosts` does not name, before any ssh runs, through `on_machine`, `plan.forwarded`, `plan.opener` and `hold.fan`.
  - Proved in `tests/py/test_crew_on.py`.
- **drive-state, What comes before a runner takes a kit's work.**
  - `kit_kept` reads through `kept`. It refuses two repositories by one name, counting `repositories` with the drives' `repos`.
  - A kit kept by no drive's `repos` and not named in `repositories` is not kept.
  - Proved in `tests/py/test_kits.py`.
- **bolt-plan, A rename waits until no host keeps the old name.**
  - `rename_kept` takes a host's runner report where it gives one, else the teams file's keeping. It cannot read a host that is neither this one nor a drive's machine, and refuses it.
  - Proved in `test_repository_rename.py` and `test_kit_rename.py`.
- **fleet-page and board-page.**
  - `placed_on`, `subscriptions` and `on_subscription` take each session's account from the drive's `accounts`. `NO_ACCOUNT` is gone.
  - Proved in `test_page.py`, `test_fleet.py` and `t-journey-board`.
- **operator-agent, the consoles.**
  - `operator_session` gives `consoles`' folder on this host and refuses elsewhere, naming the drive, the host and `consoles`.
  - `board.labels_here` follows the drives `consoles` names, and `crew go` opens their consoles again through it (`hold.py`).
  - Proved in `test_console.py`, `test_board.py`, `test_hold.py` and `t-hold`.
- **crew-flake.**
  - `nix/modules/options.nix` declares `hosts`, `consoles` and each drive's `folder`, `repos` and `accounts`, with no default.
  - `nix/tests/file.nix` holds every failing case and the no-consoles case the delta names, and compares `deneb.json` and `runner.json` byte for byte (`nix:test`).
  - `tests/py/test_module_file.py` loads both with no hosts file.
- **Docs.** README, `plugin/skills/crew/SKILL.md` and `openspec/config.yaml` name the teams file as the one file and name no hosts file (`t-docs`).

## Outcome

The checks pass and the work holds. The change is archived with this report.
