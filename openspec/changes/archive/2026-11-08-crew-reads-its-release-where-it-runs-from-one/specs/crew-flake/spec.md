## MODIFIED Requirements

### Requirement: The flake gives crew's package for each system
crew's flake SHALL give `packages.<system>.crew` and `packages.<system>.default`, one derivation whose main program is `crew`, for `aarch64-darwin`, `aarch64-linux` and `x86_64-linux`, and no other system. The package SHALL hold crew's plugin folder from the flake's tree under `plugin/`, and `bin/crew`, which runs the plugin's own `bin/crew`. Where the flake knows the commit it is built from, the package SHALL also hold `plugin/release.json`, naming that commit as `commit` and the package's version as `version`, and nothing else; built from a tree with no commit of its own, as one with uncommitted changes, it SHALL hold no release file. The package's `release` SHALL give what the file names, or null where it holds none.

#### Scenario: Every system's package
- **WHEN** the flake's outputs are evaluated
- **THEN** `packages` gives `aarch64-darwin`, `aarch64-linux` and `x86_64-linux`, each giving `crew` and `default` and nothing else, each a derivation that evaluates, `default` the same derivation as `crew`, its `meta.mainProgram` `crew`

#### Scenario: A build from a commit
- **WHEN** the flake's outputs are evaluated with `self.rev` `fcedc22e6df6380f1f640efac5f796416b1fb4c9`
- **THEN** each system's `crew.release` is that commit with the package's version, and its install writes them to `plugin/release.json`

#### Scenario: A build from a tree with no commit
- **WHEN** the flake's outputs are evaluated with no `self.rev`
- **THEN** each system's `crew.release` is null, and its install writes no `plugin/release.json`
