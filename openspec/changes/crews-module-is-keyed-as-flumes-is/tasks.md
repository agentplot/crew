# Tasks

Each check is a moon task run through `tests/suite`: `nix:format`, `nix:lint`, `nix:typecheck` and `nix:test` are the project `nix`'s, `t-docs` the `tests` project's. Submit nothing: Flume submits the place once its last stage delivers.

## 1. The keyed module

- [x] 1.1 Each of crew's modules carries the key `github:boomdrivedev/crew#<platform>Modules.crew`, so a nix-darwin system and a NixOS system that each import it directly and again inside another module's `imports` evaluate with `services.crew.enable` declared once, and everything else the module does holds (design, Decisions 1 and 2; Task notes 1.1). Verify `tests/suite nix:format nix:lint nix:typecheck nix:test` ends with "0 failed".
- [x] 1.2 README's The flake names the key and the double import it allows (design, Decision 1; Task notes 1.2). Verify `tests/suite t-docs` ends with "0 failed".
- [x] 1.3 Verify `tests/suite --affected` ends with "0 failed".
