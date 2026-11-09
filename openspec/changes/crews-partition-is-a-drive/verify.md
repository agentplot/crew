# Verify: crews-partition-is-a-drive

Verified on 2026-11-08 on `change/crews-partition-is-a-drive` at 73bad1d5, cut from `bolt/crew-names-each-drive-once` (merge-base b56c6bef, 17 commits on it).

**Verdict: does not hold. The whole checks fail on `nix:format`, so the change is not archived and goes back to its code stage.**

## The whole checks

`tests/suite`, run once from the worktree's root: every project's `check-full` tasks, the ones `.config/sluice.toml` requires of `bolt/*` and `main`.

```
FAIL  nix:format
      nix/tests/file.nix: not formatted

33 passed (20 replayed), 1 failed
```

- **Fails: `nix:format`.** `nixfmt --check` (nix/moon.yml) finds `nix/tests/file.nix` not formatted. The file was last changed by 38366137 (`feat(flake)!: crew's module lists services.crew.settings.drives, with no partition`), which added the `partitions` fixture and the case "Drives under `partitions`" for task 1.3. The fix is to run `nixfmt` on `nix/tests/file.nix` in crew's devenv shell, then run `tests/suite nix:format`. Task 1.3 named only `tests/suite nix:test` as its check, and that one passes. Nothing else in the change names `nix:format`, which is why the miss got through.
- **Pass:** the other 33 tasks. These include `tests:logic`, `tests:contract`, `tests:mod`, every end-to-end task (`tests:t-word` among them) and `nix:lint`, `nix:typecheck` and `nix:test`.

## The specs

- `openspec validate crews-partition-is-a-drive --type change --strict` passes: the change is valid.
- `openspec validate --specs`: "26 passed, 0 failed".
- The nine other open changes all validate strict as changes (`--type change --strict`), as task 6.2 requires: `a-started-bolts-kit-folder-is-read-as-main-reads-it`, `a-unit-whose-branch-stands-is-refused-at-its-proposal`, `a-users-step-of-any-length-gets-its-card`, `checked-capture`, `crew-fetches-nothing-in-the-runners-clone`, `crews-module-is-keyed-as-flumes-is`, `crews-tests-keep-the-hosts-load-within-its-cores`, `daily-pass-through-crew` and `lineage-page`.
- ``git grep -n -i partition -- openspec/specs | grep -v -E '`partitions?`'`` prints nothing (task 6.3).
- I ran `openspec archive crews-partition-is-a-drive -y` (OpenSpec 1.16.0) on a scratch copy of `openspec/`. It reports "Specs already in sync; no files changed", and the copy's `openspec/specs/` is identical to the branch's. So the delta is synced, as Decision 7 says, and the real archive will change no spec.

## Requirements and scenarios

The behaviour changes are in `main-level`'s "Drives are declared in the teams file" and `crew-flake`'s two module requirements. Every other modified requirement only changes words, and `t-word` and the logic, mod and end-to-end tiers check those.

- **The teams file at version 6** (`main-level`). `crew.VERSION` is 6, and `crew.load` reads `drives` alone. It refuses any other version naming the version, that crew reads only version 6, and swancloud's `lib/crew-teams.nix`. It refuses a version-6 file with no `drives` as "lists no drives", and a `teams` key at version 6. It reads no entry's `partition` and no session's `partition` in the hosts file, and refuses a role's `session` that the machine's hosts entry lacks (`plugin/lib/crew.py` 221–292). `tests/py/test_teams.py` has a case for each scenario: version 5 refused naming version 6; drives under `partitions` listing no drives; a session's `partition` of `clients/willdan`, `business` or none read by nothing; the version-2 box file; teams at versions 4, 5 and 6; a role's session the machine lacks. All of these pass in `tests:logic`, and `tests:t-teams` passes.
- **The module** (`crew-flake`). `nix/modules/options.nix` lists `services.crew.settings.drives` with no `partition` option, and its duplicate-label assertion names `services.crew.settings.drives`. `nix/tests/files/deneb.json` and `runner.json` are at version 6, with `drives` and no `partition`. `nix/tests/file.nix` adds the case "Drives under `partitions`", and `nix:test` passes. That case proves evaluation fails but not that the failure names `services.crew.settings.drives` as used but not defined. This is the same as the existing "A drive with no state repository" case, since an error from the module system reaches the test only as a failed evaluation. I note it here but don't count it as a gap.
- **Names and words** (every other modified requirement). The fleet's key is `drives`, with `crew.drive_of`, `plan.drive_hosts`, `plan.drive_kits` and `plan.drive_entries`. `page.DRIVES` with `<!--{{DRIVES}}-->` is in `page.html`, as is `page.fleet_drive`. `crew sites --json` lists `drives`. `crew.KINDS` holds `drive`. `crew send <drive> "<text>"` and "which drive? drives: …" are in `plugin/bin/crew`. No `{{PARTITION}}` is left in `plugin/` or `nix/modules/`. `t-word` passes on the branch, checking crew's command, plugin, module, README, CLAUDE.md, OpenSpec configuration and specs.

## Tasks

All 30 tasks in `tasks.md` are ticked. The work each one names is on the branch, and its own check passes in the run above. Task 1.3 is the exception: its own check (`nix:test`) passes, but the file it edited fails `nix:format`.

## What goes back to the code stage

- `nix/tests/file.nix` is not formatted as `nixfmt --check` requires, so the required `check-full` task `nix:format` fails. Format the file, commit it, and make sure `tests/suite nix:format` ends with "0 failed".
