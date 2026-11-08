## ADDED Requirements

### Requirement: The suite runs every project's checks
`tests/suite` SHALL select every moon project's `check-full` tasks when given no name, as sluice selects them by `#check-full`, take a task of another project than `tests` by `<project>:<task>`, and name such a task `<project>:<task>` in its lines and its failure output.

#### Scenario: Every project's checks in one run
- **WHEN** `tests/suite` runs with no name in a workspace whose project `nix` has a `check-full` task `test` beside the tests' tasks
- **THEN** `nix:test` runs beside them, and the run reports it on a line `ok    nix:test`

#### Scenario: A project's task by name
- **WHEN** `tests/suite nix:test` runs
- **THEN** only `nix:test` runs

#### Scenario: Another project's task fails
- **WHEN** `nix:test` fails
- **THEN** the run names it on a line `FAIL  nix:test` with its output, the other tasks still run, and the command exits non-zero

#### Scenario: Only the flake's files changed
- **WHEN** `tests/suite --affected` runs on a branch whose only edit is under `nix/`
- **THEN** only the project `nix`'s tasks whose inputs hold that file run

### Requirement: The flake's checks are the moon project nix
crew's flake SHALL be the moon project `nix`, whose tasks `format`, `lint`, `typecheck` and `test` are each tagged `check-full`, and whose checks evaluate the flake offline and read-only, building nothing, with the inputs crew's shell fetched.

#### Scenario: The flake's four checks
- **WHEN** moon lists crew's projects and their tasks in crew's checkout
- **THEN** the project `nix` gives `format`, `lint`, `typecheck` and `test`, each tagged `check-full`

### Requirement: crew's shell carries the flake's tools and inputs
crew's devenv shell SHALL carry nix, nixfmt, statix and deadnix, from its own nixpkgs, and SHALL give `CREW_FLAKE_INPUTS`, the store path of each input `flake.lock` locks, fetched by the shell, so the flake's checks read them with no network.

#### Scenario: The flake's tools
- **WHEN** a contract case runs inside crew's shell
- **THEN** `nix`, `nixfmt`, `statix` and `deadnix` are on its path from the Nix store, and `CREW_FLAKE_INPUTS` names, for each input of `flake.lock`, a store path that exists
