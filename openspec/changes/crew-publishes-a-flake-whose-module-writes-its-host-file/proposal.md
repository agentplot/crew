# crew publishes a flake whose module writes its host file

## Why

agentplot/boomdrive record 0023 (accepted by the user 2026-11-06) has one flake configure a whole host, each tool by its own module, which the Boomdrive flake takes as a locked input and re-exports, so each tool can also be used without Boomdrive. It names crew's part: "afterthought/crew a flake with its package and a module for its host file", whose `services.crew.settings.partitions` lists every partition with its `machine` and whose `services.crew.host` names the host, the Boomdrive module deriving the runner's crew table from both. Today crew publishes no flake: swancloud packages crew itself (`packages/crew`) and writes `~/.config/crew/teams.json` from `lib/crew-teams.nix` through home-manager, so a host outside the fleet has no way to configure crew, and the Boomdrive flake has no module of crew's to re-export. The siblings in agentplot's plan, `flume-publishes-its-own-flake-and-module` and `sluice-publishes-a-module-for-its-host-settings`, do the same for Flume and sluice, and boomdrive's `the-flake-configures-each-tool-by-its-own-module` takes this module.

## What Changes

- **A flake at crew's root**, `flake.nix` and `flake.lock`, giving `packages.<system>.crew` and `default` for `aarch64-darwin`, `aarch64-linux` and `x86_64-linux`: crew's plugin folder from the tree under `plugin/`, and `bin/crew`, which runs the plugin's own `bin/crew` with jq, Python 3.13 and recutils on its path. It gives `darwinModules.crew` and `nixosModules.crew`, each also `default`.
- **The `services.crew` module, for nix-darwin and NixOS**, writes crew's teams file from `services.crew.settings`, each key named as the file names it: `partitions`, every partition listed once with its `label`, `partition`, `blueprints`, `state`, `machine`, `session`, `review`, `flume` and, where given, `roles`; and `version`, which the module sets to the version `plugin/lib/crew.py` reads and no host can set. No key crew requires has a default. The file is `builtins.toJSON` of the settings, nulls left out: for the same partitions, the same bytes the fleet's writer gives today.
- **`services.crew.host` names the host** as `hostname -s` names it, which the partitions' `machine` names. It is no key of the file, since crew reads its host from `hostname -s` and does not change; the Boomdrive module reads it, and crew's activation says when this host's name is not it.
- **The file is linked at `~/.config/crew/teams.json`** by the system's activation, as nix-darwin's primary user or as NixOS's `services.crew.user`: a link there replaced, a file there that is no link moved aside once, as Boomdrive's module links the runner's file.
- **`services.crew.package`** is installed in the system profile, the flake's crew unless the host gives its own, as the fleet gives crew's today.
- **The module writes no other tool's file** and runs no service: no file in `/etc`, no launchd agent or systemd unit, and swancloud's hosts file stays the fleet's.
- **The flake's checks are crew's moon project `nix`**: `format` (nixfmt), `lint` (statix, deadnix), `typecheck` (every package evaluates, each module in a system of its platform) and `test` (the file pinned byte for byte, each module's activation and assertions, the activation script's cases), each tagged `check-full`, so `tests/suite` and sluice run them beside the suite. They evaluate offline and read-only against no store, building nothing, the flake's inputs fetched by crew's devenv shell, as Boomdrive's nix project does (boomdrive record 0020). crew's logic tier loads the pinned file with `crew.load`, so the module writes what crew reads.
- **`tests/suite`** runs every project's `check-full` tasks, takes `<project>:<task>` by name, and reports another project's task as `<project>:<task>`.
- **crew's devenv shell** carries nix, nixfmt, statix and deadnix, and gives the flake's inputs' store paths as `CREW_FLAKE_INPUTS`.
- **Unchanged:** what crew reads and how (`code.5`), its teams file's version, the hosts file, every crew command, and anything on crew's main.
- Record 0058 holds the choices with the paths not taken; `docs/architecture/flake.md` adds `flake.1` to `flake.3`; `code.1` and `tests.5` are amended and `code.5`'s details name the module.

## Capabilities

### New Capabilities

- `crew-flake`: crew's flake, its package and its `services.crew` module, which writes crew's teams file and no other tool's, and the checks that pin it.

### Modified Capabilities

- `test-suite`: the suite runs every project's `check-full` tasks, the flake's among them, and crew's shell carries the flake's tools.

## Impact

- New: `flake.nix`, `flake.lock`; `nix/inputs.nix`, `nix/check.sh`, `nix/moon.yml`; `nix/packages/crew.nix`; `nix/modules/options.nix`, `json.nix`, `darwin.nix`, `nixos.nix`, `activate.sh`; `nix/tests/default.nix`, `lib.nix`, `typecheck.nix`, `file.nix`, `darwin.nix`, `nixos.nix`, `settings.nix`, `activate.sh`, `files/deneb.json`.
- `.moon/workspace.yml` (the project `nix`), `devenv.nix` (the tools and `CREW_FLAKE_INPUTS`), `tests/suite`, `tests/t-suite.sh`, `tests/moon-tasks` and `tests/moon.yml` (the logic task reads `nix/tests/files/`), `tests/py/test_module_file.py`, `tests/contract/test_toolchain.py`.
- README and `openspec/config.yaml`'s context say who writes the teams file.
- `docs/adr/0058-…`, `docs/architecture/flake.md`, `core.md` (`code.1`, `code.5`'s details, the pages' table), `tests.md` (`tests.5`), in this change's own commit.
- Nothing crew models changes, so the board, the agents' views and the mod are untouched (`code.8` not reached). crew's Python imports nothing new (`code.1`).
- Outside crew: boomdrive's `the-flake-configures-each-tool-by-its-own-module` re-exports the module and derives the runner's crew table from `services.crew.settings.partitions` and `services.crew.host`; swancloud, once the modules land, passes its partitions as option values and stops writing the teams file (boomdrive record 0023, Consequences).

## Touches

```
flake.nix
flake.lock
nix/
.moon/workspace.yml
devenv.nix
tests/suite
tests/t-suite.sh
tests/moon-tasks
tests/moon.yml
tests/py/test_module_file.py
tests/contract/test_toolchain.py
README.md
openspec/config.yaml
```
