---
paths:
  - "flake.nix"
  - "flake.lock"
  - "nix/**"
---

# Flake rules

The rules for crew's flake: its package, its `services.crew` module and their checks. `core.md` binds here too; the how-to is README's The flake section. Why crew publishes a flake and what its module writes is agentplot/boomdrive record 0023; how, record 0058.

## Rules

- **[flake.1]** crew's flake gives `packages.<system>.crew` and `default` for aarch64-darwin, aarch64-linux and x86_64-linux, crew's plugin from the flake's tree with `bin/crew` running the plugin's own, and `darwinModules` and `nixosModules`, each `crew` and `default`, whose `services.crew` writes crew's teams file and no other tool's file, installs `services.crew.package`, the flake's crew unless the host gives its own, in the system profile, and runs no service. (Record 0058; not built: `crew-publishes-a-flake-whose-module-writes-its-host-file` builds it.)
- **[flake.2]** The module writes the teams file whole from `services.crew.settings`, each key named as the file names it, at the version `plugin/lib/crew.py` reads, which no host sets, with no default for a key crew requires, as `builtins.toJSON` with nulls left out, the fleet's bytes for the same drives, linked at `~/.config/crew/teams.json` for the user who runs crew; `services.crew.host` names the host as `hostname -s` does and is no key of the file; and a change to the file's shape changes the module and its pinned file in the same change. (Record 0058; not built: as `flake.1`.)
- **[flake.3]** The flake's checks are the moon project `nix`'s `format`, `lint`, `typecheck` and `test`, each tagged `check-full`, which evaluate the flake offline and read-only against no store with the inputs crew's devenv shell fetched, building nothing; the test pins the module's file byte for byte, and crew's logic tier loads that pinned file. (Record 0058; not built: as `flake.1`.)

## Details

**[flake.1]** Rules out: the module writing `~/.config/swancloud/herdr-hosts.json`, a Flume, sluice or Boomdrive file, a file under `/etc`, a launchd job or a systemd unit; a `bin/crew` that links to the plugin's, which finds its root from its own path unresolved; an output for x86_64-darwin, which nixpkgs refuses. Not ruled out: a host's own crew laid out the same, `plugin/` and `bin/crew`, as the fleet gives crew's; the Boomdrive module setting `services.crew`'s options. Source: agentplot/boomdrive record 0023 ("Each tool's module writes its own file"; "afterthought/crew a flake with its package and a module for its host file"); agentplot/blueprints `design/principles.md` 10; record 0058; `state.4`.

**[flake.2]** Rules out: a default for `label`, `blueprints`, `state`, `machine`, `session`, `review` or `flume` (`code.5`); a version written in the module beside crew.py's; drives keyed by label; a rendering through a build, or pretty-printed; a `host` key in the file; crew's reading changed for the module. Not ruled out: a key the module does not declare passing to the file for crew to judge. Source: agentplot/boomdrive record 0023 ("`services.crew.settings.partitions` lists every partition with its `machine`, and `services.crew.host` names this host to crew"; "neither the runner nor crew changes"); swancloud `lib/herdr-published.nix` `teamsJsonFor`; deneb's `~/.config/crew/teams.json`, read 2026-11-07, pinned as `nix/tests/files/deneb.json`; record 0058; `code.8`, which holds the mod to what crew models as this holds the module to the file.

**[flake.3]** Rules out: a check that builds, fetches, or writes the host's store; a check that runs only by hand; `nix flake check`. Not ruled out: the shell fetching the locked inputs, outside the check. Source: agentplot/boomdrive record 0020, its design Decision 14, `nix/check.sh`, `nix/inputs.nix` and `nix/moon.yml`; record 0058; `tests.5`, `tests.10`, `tests.11`; the user's instruction that every part of a repository with its own language is a project of its task runner with a task per check.
