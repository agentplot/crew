# Tasks

Each check runs from the worktree's root as written. `tests/suite <name>` runs one moon task: `nix:test`, `nix:typecheck`, `nix:format` and `nix:lint` are the project `nix`'s, `t-docs` the `tests` project's. The verify stage runs the repository's whole checks once, after the last task. Submit nothing: Flume submits the place once its last stage delivers.

## 1. The module

- [x] 1.1 `services.crew.settings.drives` is an attribute set keyed by each drive's label, its `label` read-only and taken from its name, written as the file's list in label order so deneb's drives still render `nix/tests/files/deneb.json` and the runner's `runner.json` byte for byte; and drives with no machine, a label the host sets, a name crew does not accept, drives as a list, and no drive each fail evaluation, the label-twice assertion gone (design, Decision 1; Task notes 1.1). Verify `tests/suite nix:test nix:typecheck` ends with "0 failed".
- [x] 1.2 A drive's `machine` and `state` are unique options, so another module gives them by the drive's label beside the host's own keys for it and deneb's drives from the two render `nix/tests/files/deneb.json`, while a machine or state written twice, and a drive given and not configured, each fail evaluation (design, Decisions 2 and 3; Task notes 1.2). Verify `tests/suite nix:test` ends with "0 failed".
- [x] 1.3 Every nix file tasks 1.1 and 1.2 touched is as nixfmt writes it, and statix and deadnix find nothing in it (design, Decision 1; Task notes 1.3). Verify `tests/suite nix:format nix:lint` ends with "0 failed".

## 2. The words

- [x] 2.1 README's The flake says the drives are keyed by label and listed in label order, that another module can give a drive its `machine` and `state`, each written once, and what fails evaluation, with no "a label listed twice" (design, Decisions 1 to 3; Task notes 1.4). Verify `tests/suite t-docs` ends with "0 failed".
