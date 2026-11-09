# Design

## Context

**The double import.** The Boomdrive flake configures the whole host, each tool by its own module, which it re-exports from the tool's own flake and whose options it sets (agentplot/boomdrive record 0023). A host that also imports crew's module itself imports it twice. crew's `darwinModules.crew` and `nixosModules.crew` were `import ./nix/modules/<platform>.nix { inherit packages; }`, a function with no key, and the module system dedupes only by key, so the second import declared `services.crew.enable` again and the system failed to evaluate. Read on this branch on 2026-11-08: the new cases of Task notes **1.1**, run against the unkeyed flake, fail with "a system importing the module twice does not evaluate" on both platforms.

**Flume's flake, read at agentplot/flume 81d57226 on 2026-11-08.** `flake.nix`'s `moduleOf` wraps each platform's module in `{ _file; key = "github:agentplot/flume#${platform}Modules.flume"; imports = [ module ]; }`, and its `nix/tests/darwin.nix` and `nix/tests/nixos.nix` each evaluate a system that imports the module twice, expecting one declaration of `services.flume.enable`. Its reasoning is its change `flume-publishes-its-own-flake-and-module`, design Decision 4: the module system takes a module once per key; of two revisions, the first one taken wins; a host that imports both takes them at one revision by following one input.

**One design, one owner.** Keying a tool's module so a re-exporting flake can import it again is one thing done by both tools, so crew takes Flume's design rather than one of its own: the same wrapper, the same key form, the same case. Flume's Decision 4 is the owner and crew cites it.

**Area pages this change touches:** `flake.md` (`flake.1`, `flake.3`), `tests.md` (`tests.4`, `tests.5`). Rules relied on: `flake.1`, which names the modules `crew` and `default` on each platform, and which a key leaves true; `flake.3`, under which the new cases are part of `nix:test`, evaluated offline and read-only against no store; `tests.4`, whose lowest tier for a module's evaluation is `nix:test`. No rule page is edited by this change (`docs.7`); the requirement it adds is the `crew-flake` spec's.

## Goals / Non-Goals

**Goals:**
- A configuration that imports crew's module directly and through Boomdrive's evaluates, with `services.crew` declared once.
- The same wrapper and key form as Flume's.

**Non-Goals:**
- Changing what the module declares, writes or installs.
- Holding two revisions of crew's module together: the first one taken wins, as with Flume's.

## Decisions

### 1. Each module is keyed `github:agentplot/crew#<platform>Modules.crew`

`flake.nix` gains `moduleOf platform file`, giving `{ _file = file; key = "github:agentplot/crew#${platform}Modules.crew"; imports = [ (import file { inherit packages; }) ]; }`; `darwinModules.crew` is `moduleOf "darwin" ./nix/modules/darwin.nix`, `nixosModules.crew` `moduleOf "nixos" ./nix/modules/nixos.nix`, and each `default` is the same value as `crew`, so one key covers both names. The key names the flake by its repository and the output, as Flume's does, so it is the same for every revision and every path the flake is fetched to. Not taken: a key from the module file's store path, which differs between two revisions and between a flake fetched by `github:` and by `path:`, so the double import Boomdrive makes would still declare `services.crew` twice; and `lib.modules.importApply`, which keys a module by its file and its arguments together, the same failure.

### 2. The nix-darwin comparison system gives crew one import deep

`nix/tests/darwin.nix`'s "Nothing else on the host" compares the activation of a system with the module to the same system without it and with crew's package added by hand. The module system orders the profile's packages by where each definition sits among the imports, and the keyed module gives crew's package one import deeper than before, so the comparison system's applications folder differed only by order. Its crew is now given inside an `imports` entry, which lists it in the same place; the case still asks that only crew's link differs. NixOS's comparison reads no package order and is unchanged.

### Departures

None.

## Risks / Trade-offs

- **Two revisions of the module.** A host that imports crew's module from two inputs at two revisions takes the first one imported and ignores the other with no word, as with Flume's (its Decision 4). A host that imports both follows one input, so both are one revision.

## Migration Plan

None. A host that imports the module once evaluates as before.

## After deploy

None. Every outcome is a case of `nix:test`, and the module writes and installs what it did.

## Task notes

**1.1** `flake.nix`: `moduleOf` in the outputs' `let`, beside `packages`, and `darwinModules`/`nixosModules` built with it. `nix/tests/darwin.nix`: `twice = t.darwinSystem { imports = [ { imports = [ t.outputs.darwinModules.crew ]; } ]; }` and the case "The module imported twice on nix-darwin", asserting `(builtins.tryEval twice.system.drvPath).success` and `builtins.length twice.options.services.crew.enable.declarations == 1`; `off` gives `set.crew` in `imports = [ { environment.systemPackages = [ set.crew ]; } ]` (Decision 2). `nix/tests/nixos.nix`: the same with `t.nixosSystem`, `t.outputs.nixosModules.crew` and `twice.config.system.build.toplevel.drvPath`, the case "The module imported twice on NixOS". Each file's opening comment names the module imported twice.

**1.2** `README.md`, The flake: the modules' bullet names the key, that a host importing the module directly and through Boomdrive's declares `services.crew` once, and that the first revision imported wins; the checks' line counts each module imported twice among `test`'s cases.
