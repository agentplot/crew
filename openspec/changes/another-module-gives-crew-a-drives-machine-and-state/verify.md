# Verify: another-module-gives-crew-a-drives-machine-and-state

Verified on 2026-11-08 on `change/another-module-gives-crew-a-drives-machine-and-state` at 4497165a. The branch was cut from `bolt/crew-names-each-drive-once` and has 5 commits on it.

**Verdict: the work holds. The whole checks pass, every task is ticked, and every requirement and scenario of the delta is met. The change is archived with this report.**

## The whole checks

`tests/suite` was run once from the worktree's root. It runs every project's `check-full` tasks, which are the ones `.config/sluice.toml` requires of `bolt/*` and `main`.

```
ok    contract   (replayed)
ok    logic   (replayed)
ok    mod   (replayed)
ok    nix:format   (replayed)
ok    nix:lint   (replayed)
ok    nix:test
ok    nix:typecheck
…
ok    t-docs   (replayed)
…
ok    t-word
34 passed (31 replayed), 0 failed
```

All 34 tasks pass and the suite exits 0. `nix:test`, `nix:typecheck` and `t-word` ran fresh. The other 31 replayed: a replay is a passing run on this host whose inputs are identical (`tests.10`). `nix:format`, `nix:lint` and `t-docs` replayed from the runs that tasks 1.3 and 2.1 made at this head.

## The specs

- `openspec validate another-module-gives-crew-a-drives-machine-and-state --type change --strict` reports "Change 'another-module-gives-crew-a-drives-machine-and-state' is valid".
- `openspec validate --specs` (OpenSpec 1.16.0) reports "26 passed, 0 failed". The one warning is a long requirement in `test-suite`, a spec this change does not touch.
- `openspec archive another-module-gives-crew-a-drives-machine-and-state -y` was run first on a scratch copy of `openspec/`. It applied "+ 4 added, ~ 1 modified, - 1 removed" to `crew-flake`, and the copy's specs then validated 26 passed, 0 failed. The one warning the archive prints is the proposal's Why over 1000 characters, which blocks nothing.

## Requirements and scenarios

- **The module writes crew's teams file from options named as the file names them** (modified).
  - `services.crew.settings.drives` is `types.attrsOf drive` (`nix/modules/options.nix`), and `json.nix` writes it as `builtins.attrValues`, the file's list in label order, each drive carrying its `label`.
  - "deneb's drives": `nix/tests/settings.nix` keys deneb's four drives by label. The case renders `nix/tests/files/deneb.json` byte for byte, fails no assertion, renders no `roles` for afterthought, and lists the labels afterthought, agentplot, madswan, wldn in that order. The pinned file holds no `partition` and no `repositories`.
  - "A runner host's kept repositories" renders `nix/tests/files/runner.json` byte for byte.
  - "crew reads the file the module writes" and "crew reads the kept repositories the module writes": neither pinned file changed on this branch, and the logic tier that loads them passes.
  - "The version is crew's": the rendered version is crew.py's, and a host's `version` fails evaluation.
- **Another module gives a drive its machine and its state repository** (added).
  - `machine` and `state` are `types.unique` with crew's message, over the name and repository types, with no default.
  - "deneb's drives from two modules": `settings.given` (each drive's `machine` and `state`) from one module beside `settings.own` (the rest) as the host's settings renders `deneb.json` byte for byte with no assertion failing.
  - "A machine written twice" and "A state repository written twice" fail evaluation. I evaluated each on its own to read why: the module system reports "The option `services.crew.settings.drives.agentplot.machine' is defined multiple times while it's expected to be unique.", then crew's message, then both definitions. The same holds for `state`. Equal values fail, as the requirement asks. In the cases each definition's file reads `<unknown-file>`, since the test's modules are inline. A host's modules carry their files, and Boomdrive chooses the name its own definitions carry (design, Decision 2).
- **A drive another module gives is configured in the host's settings** (added).
  - "A drive given and not configured" fails evaluation. Read on its own, the failure is "The option `services.crew.settings.drives.extra.blueprints' was accessed but has no value defined", which is the missing-key failure Decision 3 names.
- **Every drive is named once, by its label** (added).
  - `label` is read-only, its default the drive's name, its type `code.4`'s name type.
  - "A label the host sets" fails evaluation. Read on its own, the failure is "The option `services.crew.settings.drives.madswan.label' is read-only, but it's set multiple times."
  - "A name crew does not accept" (`Madswan`) and "Drives as a list" fail evaluation.
  - "Drives under `partitions`" fails, since `drives` has no definition.
  - "No drive" fails the assertion `cfg.settings.drives != { }`, whose message names `services.crew.settings.drives` and "names no drive". The label-twice assertion is gone.
- **Every drive gives every key crew requires** (added).
  - No key crew requires has a default, and the drive declares no `partition` option.
  - "A drive with no state repository", "A drive with no machine", "A role crew has no kind for" (`dispatcher`, and `planner = true`) and "Teams" each fail evaluation. Teams fails on an assertion that names `services.crew.settings.teams` and "has no place for teams".
- **Every drive is listed once, with every key crew requires** (removed). Its scenarios carry over to the two requirements above, except "A label twice": the case and its `madswan` and `twice` fixtures are gone from `nix/tests/file.nix`.
- **README's The flake** says the drives are keyed by label and listed in label order, that another module can give `machine` and `state`, each written once, and what fails evaluation, with no "a label listed twice". `t-docs` pins each phrase and passes. `t-word` passes too, so no "partition" is left in `nix/modules/` or the README.

## Departures

The design's one departure is from `flake.2`'s details, which rule out "partitions keyed by label" (`docs/architecture/flake.md`). The design names it and leaves the amendment to the design agent after the landing (`docs.7`). This change edits no rule page, as `docs.7` requires.

## Tasks

All 4 tasks in `tasks.md` (1.1, 1.2, 1.3 and 2.1) are ticked and none is open. The work each task names is on the branch, and each task's check passes in the run above.
