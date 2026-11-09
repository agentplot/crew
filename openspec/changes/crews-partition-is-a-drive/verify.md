# Verify: crews-partition-is-a-drive

Verified on 2026-11-08 on `change/crews-partition-is-a-drive` at 7e902361. The branch was cut from `bolt/crew-names-each-drive-once`, with merge-base b56c6bef and 19 commits on it.

**Verdict: the work holds. The whole checks pass, every task is ticked, and every requirement and scenario of the delta is met. The change is archived with this report.**

## The whole checks

`tests/suite` was run once from the worktree's root. It runs every project's `check-full` tasks, which are the ones `.config/sluice.toml` requires of `bolt/*` and `main`.

```
ok    nix:format   (replayed)
ok    nix:lint
ok    nix:test
ok    nix:typecheck
…
ok    t-word   (replayed)
34 passed (31 replayed), 0 failed
```

All 34 tasks pass and the suite exits 0. This covers `tests:logic`, `tests:contract`, `tests:mod`, every end-to-end task (`tests:t-word` among them) and the four `nix` tasks. `nix:lint`, `nix:test` and `nix:typecheck` ran fresh. The other 31 tasks replayed: a replay is a passing run on this host whose inputs are identical (`tests.10`). `nix:format` replayed from the run that task 1.4's check made on `nix/tests/file.nix` at this head.

## The specs

- `openspec validate crews-partition-is-a-drive --type change --strict` reports "Change 'crews-partition-is-a-drive' is valid".
- `openspec validate --specs` (OpenSpec 1.16.0) reports "26 passed, 0 failed". The one warning is a long requirement in `test-suite`, a spec this change does not touch.
- Task 6.2 requires nine other open changes to validate strict as changes, and all nine do: `a-started-bolts-kit-folder-is-read-as-main-reads-it`, `a-unit-whose-branch-stands-is-refused-at-its-proposal`, `a-users-step-of-any-length-gets-its-card`, `checked-capture`, `crew-fetches-nothing-in-the-runners-clone`, `crews-module-is-keyed-as-flumes-is`, `crews-tests-keep-the-hosts-load-within-its-cores`, `daily-pass-through-crew` and `lineage-page`.
- Five open changes do not validate strict: `an-offer-card-shows-the-step-the-deploy-waits-on-first`, `blocking-findings`, `crew-keeps-no-card-wait-and-a-row-carries-its-submission-number`, `curation-and-agenda` and `no-worktree-holds-main-or-a-bolt-branch`. None of them validated at the merge-base b56c6bef either (checked on an extract of `openspec/` at that commit), so this change broke none of them. None of the five holds the word "partition" any longer, so every open change's words say drive.
- ``git grep -n -i partition -- openspec/specs | grep -v -E '`partitions?`'`` prints nothing (task 6.3).
- `openspec archive crews-partition-is-a-drive -y` was run first on a scratch copy of `openspec/`. It reported "Specs already in sync; no files changed", and the copy's `openspec/specs/` is identical to the branch's. The delta is synced as Decision 7 says, so the real archive changes no spec.

## Requirements and scenarios

- **The teams file at version 6** (`main-level`, "Drives are declared in the teams file").
  - `crew.VERSION` is 6, and `crew.load` reads `drives` alone (`plugin/lib/crew.py` 221–288).
  - It refuses a file at any other version, naming swancloud's `lib/crew-teams.nix`. It refuses a version-6 file with no `drives` as "lists no drives", and it refuses a `teams` key.
  - It reads no entry's `partition` and no session's `partition` in the hosts file.
  - `tests/py/test_teams.py` covers each scenario (version 5 refused naming version 6, drives under `partitions`, a session's `partition` read by nothing), and `tests:logic` and `tests:t-teams` pass.
- **The module** (`crew-flake`).
  - `nix/modules/options.nix` lists `services.crew.settings.drives` with no `partition` option, and its duplicate-label assertion names `services.crew.settings.drives`.
  - `nix/tests/files/deneb.json` and `runner.json` are at version 6, with `drives` and no `partition`.
  - The case "Drives under `partitions`" fails evaluation. `nix:test` passes, and `nix:format` passes on `nix/tests/file.nix`.
  - That case shows evaluation fails, but not that the failure names `services.crew.settings.drives` as used but not defined. The existing "A drive with no state repository" case has the same limit, because a module-system error reaches the test only as a failed evaluation. I note it here but don't count it as a gap.
- **Names and words** (every other modified requirement, a rename with no change of behaviour).
  - The fleet's key is `drives`, with `crew.drive_of`, `plan.drive_hosts`, `plan.drive_kits` and `plan.drive_entries`.
  - `page.DRIVES` and `<!--{{DRIVES}}-->` are in `page.html`, as is `page.fleet_drive`. `crew sites --json` lists `drives`, and `crew.KINDS` holds `drive`.
  - `crew send <drive> "<text>"` and "which drive? drives: …" are in `plugin/bin/crew`.
  - No `{{PARTITION}}` is left in `plugin/` or `nix/modules/`.
  - `t-word` passes on the branch with its task in `tests/moon.yml`. It checks crew's command, plugin, module, README, CLAUDE.md, OpenSpec configuration and specs.

## Tasks

All 31 tasks in `tasks.md` are ticked and none is open. The work each task names is on the branch, and each task's own check passes in the run above.
