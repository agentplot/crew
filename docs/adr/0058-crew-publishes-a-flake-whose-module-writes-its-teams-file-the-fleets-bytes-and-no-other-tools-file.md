---
status: accepted
date: 2026-11-07
decision-makers: the construct stage of crew-publishes-a-flake-whose-module-writes-its-host-file, on agentplot/boomdrive record 0023 (accepted by the user 2026-11-06) and agentplot's plan
---

# 0058. crew publishes a flake whose module writes its teams file, the fleet's bytes, and no other tool's file

Status: decided 2026-11-07 by the construct stage of the change `crew-publishes-a-flake-whose-module-writes-its-host-file` on `teamless/deneb`, for the parts agentplot/boomdrive record 0023 and the plan's unit leave to crew. That crew publishes a flake with its package and a module for its host file, that the module writes crew's file alone from options named as the file names them, with `services.crew.settings.partitions` and `services.crew.host`, and that crew's reading does not change, are record 0023's, the user's. Nothing here is the user's alone, and each part is cheap to change.

Adds `flake.1`, `flake.2` and `flake.3` on the new page `docs/architecture/flake.md`; amends `code.1` and `tests.5`, and `code.5`'s details. Sources: agentplot/boomdrive record 0023 and its sketch of deneb (`design/the-flakes-configuration/deneb.nix`); boomdrive record 0020 and its design Decision 14, and its `flake.nix`, `nix/modules/` and `nix/tests/` at `3f428cf`, the family's shape for a tool's flake and its checks; agentplot/blueprints `design/principles.md` 10; swancloud `packages/crew`, `lib/host-crew.nix`, `lib/claude-account-tools.nix` and `lib/herdr-published.nix` `teamsJsonFor`, read 2026-11-07; deneb's `~/.config/crew/teams.json` read that day; `crew.load`, `crew.this_host` and `plugin/bin/crew`.

## Context and problem statement

Record 0023 has the Boomdrive flake configure a whole host, each tool by its own module, re-exported from the tool's own flake, so each tool can be used without Boomdrive. crew publishes no flake: swancloud packages crew and writes `~/.config/crew/teams.json` itself, so a host outside the fleet cannot configure crew, and the Boomdrive flake has no module of crew's to re-export or to read crew's partitions and host from.

## Decision

1. **crew's flake gives its package and its module.** `packages.<system>.crew` and `default` for aarch64-darwin, aarch64-linux and x86_64-linux: the tree's `plugin/` under `$out/plugin`, unpatched, and `$out/bin/crew`, a wrapper that puts jq, Python 3.13 and recutils first on its path and runs the plugin's own `bin/crew`; and `darwinModules` and `nixosModules`, each `crew` and `default`, declaring `services.crew`. Inputs: nixpkgs at `nixos-unstable` and nix-darwin for the tests, Boomdrive's.
2. **Options named as the file names them, with no default for what crew requires.** `services.crew.settings` is the teams file: `partitions`, a list, each declaring `label`, `partition`, `blueprints`, `state`, `machine`, `session`, `review` and `flume` with no default and `roles` optional, undeclared keys passing to the file; and `version`, read-only, taken at evaluation from `plugin/lib/crew.py`'s `VERSION`. A label twice and a `teams` key fail evaluation. Beside it `services.crew.package`, the flake's crew unless the host gives its own; `services.crew.host`; and, on NixOS, `services.crew.user`.
3. **The file is `builtins.toJSON` of the settings, nulls left out, no newline added**: for the same partitions, the bytes the fleet writes today, so a host moving to the module changes no byte crew reads.
4. **The activation links `~/.config/crew/teams.json` to the file** as nix-darwin's primary user or as NixOS's `services.crew.user`, a link replaced and a file that is no link moved aside once, as Boomdrive's module links the runner's file; a link that fails stops nothing else.
5. **`services.crew.host` is no key of the file.** crew reads its host from `hostname -s`, unchanged; the Boomdrive module reads the option; crew's activation says, after linking, when the host's own name is not it.
6. **The module writes nothing else and runs no service**: no file under `/etc`, no launchd job or systemd unit; the hosts file stays the fleet's.
7. **The flake's checks are the moon project `nix`**: `format`, `lint`, `typecheck` and `test`, each tagged `check-full`, evaluating offline and read-only against a dummy store with the inputs crew's devenv shell fetched (`CREW_FLAKE_INPUTS`), building nothing, as Boomdrive's; the module's file pinned byte for byte as `nix/tests/files/deneb.json`, which crew's logic tier loads with `crew.load`. `tests/suite` runs every project's `check-full` tasks.

## Considered options

- **The module writes the teams file alone, as above (chosen).**
- **The module also writes the hosts file.** Not taken: `~/.config/swancloud/herdr-hosts.json` is swancloud's file, naming herdr's sessions and spaces; a tool's file is written by its own module and never by another (principle 10).
- **`host` written into the file, crew reading it there.** Not taken: record 0023 changes nothing crew reads, and crew already reads its host from `hostname -s`, so the file would carry a second name crew ignores.
- **Defaults for `flume` (every role `false`) and `review`, the fleet's values.** Not taken: crew's file has no defaulted field (`code.5`), and the module would become a second place a default of crew's file lives.
- **Partitions as an attribute set keyed by label.** Not taken: it would reorder the fleet's list and change the file's bytes; record 0023 and its sketch give a list.
- **`pkgs.formats.json`.** Not taken: it renders through jq in a build, so no check could compare the text without building, and it pretty-prints, changing every byte.
- **A home-manager module, or a real file installed and moved over.** Not taken: a host need not run home-manager, Boomdrive's modules are system modules, and crew reads bytes, so a link into the store, as home-manager's is today, serves.
- **A build of the package or of a system in the check, or `nix flake check`.** Not taken: each needs every platform's builder and the network; evaluation proves what the specs say, as Boomdrive's checks do.
- **An install check in the package, as the fleet's.** Not taken: it proves a fetched pin whole, and the flake builds its own tree, which crew's suite checks.

## Consequences

- crew's file keeps its name and has no local layer, departing from principle 10's names and layers, since record 0023 changes nothing crew reads and a drive's own control plane replaces crew (`roles.9`).
- The flake is built on `teamless/deneb`, whose crew reads version 5; the Boomdrive flake takes it at a commit of that branch, as swancloud pins deneb's crew, until the refactor returns to main.
- boomdrive's `the-flake-configures-each-tool-by-its-own-module` re-exports the module, and `crews-partitions-give-the-runner-its-crew-table` reads `services.crew.settings.partitions` and `services.crew.host`. swancloud, once the modules land, passes its partitions as option values, gives its own crew through `services.crew.package` where it pins another, and drops its home-manager entry for the file in the same deploy.
- A host configured only through the module still needs the hosts file until crew stops reading it.
