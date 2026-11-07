# Tasks

## 1. The suite runs every project's checks

- [x] 1.1 `.moon/workspace.yml` lists the project `nix`, and `tests/suite` runs every project's `check-full` tasks when given no name, takes `<project>:<task>` by name, and names another project's task `<project>:<task>` in its lines and failure output (design, Decision 8; Task notes 1.1). Verify `tests/suite t-suite` ends with "0 failed".

## 2. The flake, its package and its checks

- [x] 2.1 `flake.nix` and `flake.lock` lock nixpkgs and nix-darwin, and crew's shell carries nix, nixfmt, statix and deadnix and gives `CREW_FLAKE_INPUTS`, each locked input's store path (design, Decisions 1 and 7; Task notes 2.1). Verify `tests/suite contract` ends with "0 failed".
- [x] 2.2 The flake gives `packages.<system>.crew` and `default` for aarch64-darwin, aarch64-linux and x86_64-linux, crew's plugin under `plugin/` and `bin/crew`, and the project `nix` has its `typecheck` and `test` tasks, evaluated offline and read-only against no store (design, Decisions 1 and 7; Task notes 2.2). Verify `tests/suite nix:typecheck` ends with "0 failed".
- [ ] 2.3 The project `nix` has its `format` and `lint` tasks over `flake.nix` and `nix/`, and every file of the flake passes them (design, Decision 7; Task notes 2.3). Verify `tests/suite nix:format nix:lint` ends with "0 failed".
- [ ] 2.4 moon lists the project `nix`'s `format`, `lint`, `typecheck` and `test`, each tagged `check-full` (design, Decision 7; Task notes 2.4). Verify `tests/suite contract` ends with "0 failed".

## 3. The module writes crew's teams file

- [ ] 3.1 `services.crew.settings` renders, byte for byte, the teams file deneb holds today from deneb's partitions, its version read from `plugin/lib/crew.py` and settable by no host, with no default for a key crew requires, and evaluation fails for a missing `state`, a label twice, a role crew has no kind for and `teams` (design, Decisions 2 and 3; Task notes 3.1). Verify `tests/suite nix:test` ends with "0 failed".
- [ ] 3.2 crew loads the file the module writes, `nix/tests/files/deneb.json`, as its teams file (design, Decision 7; Task notes 3.2). Passes `tests/py/test_module_file.py` (`tests/suite logic`).
- [ ] 3.3 crew's link makes `~/.config/crew/teams.json` a link to the module's file, replacing a link, moving a file that is no link aside once and refusing when the aside is taken, and says when this host's name is not `services.crew.host` (design, Decisions 4 and 5; Task notes 3.3). Verify `tests/suite nix:test` ends with "0 failed".
- [ ] 3.4 `darwinModules.default` links the file as the primary user with the host, installs the flake's crew or the host's own in the system profile, fails for a primary user with no home, writes nothing else, and evaluates in a nix-darwin system (design, Decisions 4 to 6; Task notes 3.4). Verify `tests/suite nix:typecheck nix:test` ends with "0 failed".
- [ ] 3.5 `nixosModules.default` links the file as `services.crew.user` alone with the host, installs the flake's crew or the host's own in the system profile, fails for a user the system does not declare, writes nothing else, and evaluates in a NixOS system (design, Decisions 4 to 6; Task notes 3.5). Verify `tests/suite nix:typecheck nix:test` ends with "0 failed".

## 4. The docs and the change's tests

- [ ] 4.1 README and `openspec/config.yaml`'s context say the machine's configuration writes the teams file, crew's module `services.crew` or swancloud's `lib/crew-teams.nix`, and README says what the flake gives (Task notes 4.1). Verify `tests/suite t-docs` ends with "0 failed".
- [ ] 4.2 The tests the change affects pass (Task notes 4.2). Verify `tests/suite --affected` ends with "0 failed".
