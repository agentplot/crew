## MODIFIED Requirements

### Requirement: The module is given for nix-darwin and NixOS
The flake SHALL give `darwinModules.crew` and `nixosModules.crew`, each also as `default`, declaring `services.crew`. A system of each platform with `services.crew` enabled SHALL evaluate. Each module SHALL carry a key that names it, `github:boomdrivedev/crew#darwinModules.crew` and `github:boomdrivedev/crew#nixosModules.crew`, so a configuration that imports it twice, directly and through another flake's module, declares `services.crew` once.

#### Scenario: A nix-darwin system
- **WHEN** a nix-darwin system of `aarch64-darwin` imports `darwinModules.default` and enables `services.crew` for its primary user
- **THEN** the system's derivation evaluates

#### Scenario: A NixOS system
- **WHEN** a NixOS system of `x86_64-linux` imports `nixosModules.default` and enables `services.crew` for a normal user
- **THEN** the system's toplevel evaluates

#### Scenario: The module imported twice
- **WHEN** `nix:test` evaluates a nix-darwin system, and a NixOS system, each importing the flake's module directly and again inside another module's `imports`, with `services.crew` enabled
- **THEN** each evaluates, and `services.crew.enable` is declared once
