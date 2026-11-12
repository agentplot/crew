# crew's module is keyed as Flume's is

## Why

The Boomdrive flake re-exports each tool's module and sets its options (boomdrivedev/boomdrive record 0023, "Each tool's module writes its own file"). A host that imports crew's module directly and through Boomdrive's imports it twice. crew's `darwinModules.crew` and `nixosModules.crew` are bare functions, which the module system cannot tell apart, so such a host declares `services.crew` twice and fails to evaluate. Flume's flake already gives each module a key that names it, so the module system takes it once (Flume's `flume-publishes-its-own-flake-and-module`, design Decision 4; its `flake` spec, "A module imported twice"). crew's module is the same thing and is made the same way.

## What Changes

- Each of crew's modules is an attribute set with `_file` and `key = "github:boomdrivedev/crew#<platform>Modules.crew"`, whose `imports` holds the module itself, as Flume's are. `default` stays the same module as `crew`.
- `nix:test` evaluates a nix-darwin system and a NixOS system that each import the module directly and again inside another module's `imports`, and checks each evaluates with `services.crew` declared once.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `crew-flake`: each module carries a key that names it, so a configuration importing it twice declares `services.crew` once.

## Impact

- `flake.nix`: `moduleOf`, and `darwinModules` and `nixosModules` built with it.
- `nix/tests/darwin.nix`, `nix/tests/nixos.nix`: the module imported twice; the nix-darwin comparison system without crew gives crew's package one import deep, where the keyed module now gives it, so its profile lists crew in the same place.
- `README.md`: The flake says each module is keyed so, and that `nix:test` imports it twice.
- Unchanged: `docs/architecture/` (`docs.7`), since `flake.1` already names the modules and a key changes none of what it says; what the module writes and installs, and crew's command, plugin, views and mod (`code.8`), since nothing crew models changes.
