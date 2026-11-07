# Verify: crew-publishes-a-flake-whose-module-writes-its-host-file

Verified 2026-11-07 on `change/crew-publishes-a-flake-whose-module-writes-its-host-file` at `bb27ddb4`, which carries teamless/deneb `7bac42c6` merged in (`2f7a147f`).

**Verdict: the whole checks pass and the work holds. The change is ready to archive.**

## The whole checks

`tests/suite` with no name, run once on the branch as it stood (clean tree). That runs every project's `check-full` task, which is what sluice's `#check-full` resolves to (`.config/sluice.toml`, `tests.5`).

```
ok    contract   (replayed)
ok    logic   (replayed)
ok    mod
ok    nix:format   (replayed)
ok    nix:lint   (replayed)
ok    nix:test
ok    nix:typecheck
ok    t-briefs … t-waits   (26 end-to-end tasks, t-docs replayed, the rest run)
33 passed (5 replayed), 0 failed
exit 0
```

`nix:test`, `nix:typecheck`, `mod` and every end-to-end task but `t-docs` ran on this tree. The 5 replayed tasks had inputs identical to a run that had already passed on this host (`tests.10`). `tests/moon-tasks --check` passes, so `tests/moon.yml` matches the tests. `openspec validate crew-publishes-a-flake-whose-module-writes-its-host-file --strict` reports the change valid.

## Tasks

All 13 tasks in `tasks.md` are ticked, none open, and each one's check is among the passing tasks above:

| Task | Its check | Where it is proved |
|---|---|---|
| 1.1 | `t-suite` | `tests/t-suite.sh`, stand-in project `nix` cases |
| 2.1, 2.4 | `contract` | `tests/contract/test_toolchain.py`, its two new cases |
| 2.2 | `nix:typecheck` | `nix/tests/typecheck.nix` |
| 2.3 | `nix:format`, `nix:lint` | `nix/moon.yml` over `flake.nix` and `nix/` |
| 3.1, 3.3, 3.4, 3.5 | `nix:test` (with `nix:typecheck` for 3.4 and 3.5) | `nix/tests/file.nix`, `activate.sh`, `darwin.nix`, `nixos.nix` |
| 3.2 | `logic` | `tests/py/test_module_file.py` |
| 4.1 | `t-docs` | README's "The flake", `openspec/config.yaml` |
| 4.2 | the run above | |
| 4.3 | `openspec validate --strict`, `t-docs`, `logic`, `contract` | the merge `2f7a147f` and `bb27ddb4`; see below |

## teamless/deneb 7bac42c6 taken in (task 4.3)

- README's suite paragraph says `tests/suite` runs every other project's `check-full` tasks, the project `nix`'s among them, named `<project>:<task>`. It also says a test holds its slot only while it runs, and that whatever it leaves running is ended with it.
- In `tests/moon-tasks`, the command core takes crew's manifest (`plugin/.claude-plugin/plugin.json`). The logic tier's inputs take the manifest and `plugin/bin/` beside `nix/tests/files/**/*`, and the contract tier's keep `flake.lock`, `nix/inputs.nix`, `nix/moon.yml` and `.moon/workspace.yml`. `tests/moon.yml` is as `tests/moon-tasks` writes it.
- `openspec/specs/test-suite/spec.md` keeps sluice's slot and follower requirements. The change's three test-suite requirements, and the whole `crew-flake` spec, are absent from `openspec/specs`, so the archive adds them.
- The merge changed none of the flake's own files (`flake.nix`, `flake.lock`, `nix/`, `devenv.nix`, `.moon/`), and `plugin/lib/crew.py`'s `VERSION` is still 5. The spec tables below therefore hold as they are, and `nix:test` and `nix:typecheck` ran afresh on this tree.

## crew-flake spec

| Requirement / scenario | Met by |
|---|---|
| Package for each system | `flake.nix` `packages` over the three systems; `nix/packages/crew.nix` (`plugin/` copied, `bin/crew` a wrapper with jq, python313 and recutils, `meta.mainProgram = "crew"`). typecheck "Every system's packages" checks that each system gives only `crew` and `default`, that `default` is `crew`, and the main program. |
| Module for nix-darwin and NixOS | `darwinModules`/`nixosModules` `crew` and `default`. typecheck "The nix-darwin module" (`system.drvPath`) and "The NixOS module" (toplevel `drvPath`). |
| deneb's partitions, byte for byte | `nix/modules/json.nix` (nulls dropped at every depth, then `builtins.toJSON`). file.nix "deneb's partitions" compares the output with `nix/tests/files/deneb.json`, which matches the design's pinned bytes and has no `roles` key for afterthought. |
| crew reads the file the module writes | `test_module_file.py`: `crew.load` gives the four labels in order, wldn's planner and reviewer in `wldn-1`, and every role standing. |
| The version is crew's | `options.nix` reads `VERSION = <n>` from `plugin/lib/crew.py` into a `readOnly` option. file.nix "The version is crew's" reads crew.py on its own and checks that `version = 4` fails. |
| Every partition once, with every key | No default for the eight required keys; `flume` a submodule of exactly `KIND_ROLES`, each `false` or a name; assertions for a label given twice and for `teams`. file.nix covers no `state`, `madswan` twice (the message names the option path and the label), `dispatcher`, `planner = true`, and `teams` (the message says version 5 has no place for teams). |
| `services.crew.host` names the host | It is passed to `activate.sh link <file> <host>` and is not part of `settings`. darwin.nix and nixos.nix check that the activation text names `host-a`. activate.sh "A host whose name is not services.crew.host" checks the one line naming both names, and no line for `host-a.local`. |
| Linked for the user who runs crew | darwin: `sudo --user=alice … HOME=/Users/alice`. NixOS: `userActivationScripts.crew` guarded by `id -un`. Assertions name `users.users.alice.home` and `services.crew.user`/`users.users.carol`, and the "On nix-darwin", "A primary user with no home", "On NixOS" and "A user the system does not declare" cases check them. |
| crew's link replaces only a link | `nix/modules/activate.sh`. activate.sh covers: nothing there, a link there, already linked, a file there, a folder there, a file there with an aside already present (exit 1, both unchanged, both paths named), and usage. Both modules append `|| true`, so a refusal does not stop the rest of the system's activation. |
| The package is the flake's unless the host gives its own | `services.crew.package` defaults to `packages.${system}.crew`. "The flake's crew" and "A host's own crew" cases on both platforms check the profile and that the linked file is unchanged. |
| Writes no other tool's file | "Nothing else on the host" on both platforms compares against the same system without the module: same `environment.etc`, launchd agents and daemons or systemd units, `users.users` and linger; activation identical once crew's line or snippet is removed. |

## test-suite spec

| Requirement / scenario | Met by |
|---|---|
| Every project's checks in one run | `tests/suite` with no name targets `:#check-full`. t-suite: `ok    nix:test` beside the stand-ins. |
| A project's task by name | `<project>:<task>` is checked against `.moon/workspace.yml` and the project's `moon.yml`. t-suite: `nix:test` runs alone, and `nix:nope` is refused before anything runs. |
| Another project's task fails | t-suite: `FAIL  nix:test` with its output, the other tests pass, exit 1. |
| Only the flake's files changed | t-suite: `--affected` with only an uncommitted edit under `nix/` runs `nix:test` alone. |
| The flake's four checks | `nix/moon.yml`. contract: `moon query tasks --project nix` returns the four tasks, each tagged `check-full`. |
| The shell carries the flake's tools and inputs | `devenv.nix` adds `pkgs.nix`, `nixfmt`, `statix` and `deadnix`, and sets `env.CREW_FLAKE_INPUTS`. contract: the tools come from `/nix/store`, and every node of `flake.lock` names an existing store path. |

## Rules and records

- Record 0058 (`docs/adr/0058-…`) and `docs/architecture/flake.md` (`flake.1` to `flake.3`) are in the change's first commit, along with `code.1` and `tests.5` amended, `code.5`'s details, and the page table. Each new or amended clause still says "not built: `crew-publishes-a-flake-whose-module-writes-its-host-file` builds it". Lifting that after the landing is the design agent's job (`docs.7`), not part of this change.
- `code.8` is not reached, since nothing crew models changed. `code.1` holds: no new Python import, and devenv adds only the four tools the amended rule names.

## Gaps

None.
