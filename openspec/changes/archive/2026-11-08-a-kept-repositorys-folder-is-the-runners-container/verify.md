# Verify: a-kept-repositorys-folder-is-the-runners-container

Verified on 2026-11-08 on `change/a-kept-repositorys-folder-is-the-runners-container` at `358615e1`, cut from `bolt/crew-finds-a-kit-in-the-runners-copy` (merge-base with main `2e0b0e7d`).

**Outcome: the work holds.** The whole checks pass, every task is done, and every requirement and scenario of the three delta specs is met and proved by a check in crew's tiers.

## Whole checks

`tests/suite --affected`, run once from the worktree's root, as CLAUDE.md names it for a finished change before its merge. The change edits crew's command core (`plugin/lib/crew.py`) and `nix/`, so every `check-full` task of both projects counts as affected. `mod` is the one task left out: no file under `plugin/hooks/` or `plugin/tests/` changed.

```
ok    contract            ok    t-journey-cross
ok    logic               ok    t-journey-land
ok    nix:format          ok    t-journey-main
ok    nix:lint            ok    t-journey-main-fix
ok    nix:test (replayed) ok    t-journey-ops
ok    nix:typecheck       ok    t-journey-plan
ok    t-briefs (replayed) ok    t-journey-review
ok    t-cards             ok    t-journey-roles
ok    t-docs (replayed)   ok    t-journey-signals
ok    t-flume-source      ok    t-journey-state
ok    t-help              ok    t-roles
ok    t-hold              ok    t-runner
ok    t-journey-board     ok    t-session-hook
ok    t-slot              ok    t-sluice
ok    t-stage-facts       ok    t-suite
ok    t-teams             ok    t-waits
32 passed (3 replayed), 0 failed
```

Three tasks were replayed: `nix:test`, `t-briefs` and `t-docs`. A replay is moon finding the same inputs in a run that already passed on this host, the code stage's own run of that task. sluice runs every task afresh on submission (`tests.5`).

`openspec validate a-kept-repositorys-folder-is-the-runners-container --strict`: valid.

## Tasks

All 11 tasks, 1.1 to 4.1, are ticked, and each has the code and the case it names:

| Task | Built in | Proved by |
|---|---|---|
| 1.1 | `crew.repositories_of`, `crew.load` | `test_teams.py` `TestKeptRepositories` |
| 1.2 | `crew.named_on`, `kept_at`, `kept`; `kit_kept` and `kept_on` read `kept` | `test_kits.py` `TestInTheRunnersCopy` |
| 1.3 | `load`'s partition `checkout` through `kept_at` | `test_teams.py` `test_a_partition_whose_blueprints_the_file_names_on_its_host_starts_in_the_files_checkout` (incl. `launch`'s `cwd`) |
| 1.4 | `crew.session_checkouts`, `ops.kit_range` | `test_ops.py` `TestRangesKits` |
| 2.1 | `main_tokens`: `FOLDER`, `KIT_CHECKOUTS`, `SWANCLOUD_CHECKOUT`, `SWANCLOUD_FOLDER` | `test_teams.py` brief cases |
| 2.2 | `plugin/roles/design.md`, `plugin/roles/operator.md` | `t-briefs.sh` |
| 3.1 | `nix/modules/options.nix` `settings.repositories` | `nix:format`, `nix:lint`, `nix:typecheck` |
| 3.2 | `nix/tests/settings.nix` `runner`, `nix/tests/files/runner.json` | `nix/tests/file.nix` |
| 3.3 | (no code: crew's loader as built) | `test_module_file.py` `test_crew_reads_the_kept_repositories_the_module_writes` |
| 4.1 | `README.md`, `plugin/skills/crew/SKILL.md` | `t-docs.sh` |

`crew.checkout` is now called only inside `kept_at`. A grep of `plugin/lib` and `plugin/bin` finds no other folder-built `/main`. No brief or skill still names `~/Code/github_afterthought/swancloud`.

## Specs

Each MODIFIED requirement keeps every scenario the current spec holds and only adds new ones, so archiving drops nothing.

### main-level

- **Partitions are declared in the teams file** (MODIFIED):
  - *A runner host's kept repositories*: `TestKeptRepositories` and `test_module_file.py`.
  - *A kept repository named wrongly*, for no owner, no `checkout`, a relative `dir`, a `view` key, plus `[]`, `null`, a string entry, an empty `dir` and a non-string `checkout`: each is refused naming `teams.json`, the repository and swancloud's `lib/crew-teams.nix`, before the hosts file is read.
  - *A file that names no repository*: it loads with `repositories` `{}` and reads no host. Kits keep `<session dir>/<name>` and `/main`, per `test_kits.py` and the brief case.
  - Existing scenarios unchanged.
- **The design agent's brief names each kept repository's checkout and folder** (ADDED):
  - *On a runner host*: `test_teams.py` and `t-briefs.sh`'s runner-host case (the view as checkout, the container as folder).
  - *Where the file names none*: the brief case and `t-briefs.sh` (`<space>/<name>/main` in the folder `<space>/<name>`).
  - The brief says a checkout is moved by "its host alone … the fleet's timer or, on a runner host, the runner", and no longer says "this directory".
- **The operator's brief names swancloud's checkout and folder** (ADDED):
  - *On a runner host*: `t-briefs.sh` checks the fetch in the view, the worktree under `<container>/places/crew-teams-<label>` and the `wt -C … remove`, with no `~/Code/github_afterthought/swancloud`.
  - *A box's operator*: on chuck-herdr-alpha every token is filled in words ("swancloud's checkout, which chuck-herdr-alpha does not keep"). The door sentence stays.

### drive-state

- **What comes before a runner takes a kit's work is done on the main-level host** (MODIFIED), in `test_kits.py` `TestInTheRunnersCopy`:
  - *A kit in the runner's copy*: by the name `crew` and by the address `agentplot/crew`, it is found at `/v`/`/r` even though a space also keeps it, and `kits_on` gives the view.
  - *A repository the file names and no space keeps*: weir.
  - *Another host's kit*: alpha keeps its spaces' folders.
  - *One name, two repositories*: refused, "deneb's teams file and spaces keep agentplot/blueprints and afterthought/blueprints", while each address resolves.
  - Existing scenarios unchanged and still green in `TestBeforeARunnerTookIt`.

### crew-flake

- **The module writes crew's teams file from options named as the file names them** (MODIFIED):
  - *deneb's partitions*: `deneb.json` is still rendered byte for byte and has no `repositories` key.
  - *A runner host's kept repositories*: `runner.json` is rendered byte for byte.
  - *crew reads the kept repositories the module writes*: `test_module_file.py` finds four partitions, and crew's and swancloud's `kit_kept` on deneb at the file's container and view.
- **A kept repository is named by its address with its folder and checkout** (ADDED): `nix/tests/file.nix` covers the four failing cases. No `checkout` and a relative `dir` fail through the submodule's types. A `view` key fails through the closed submodule. `crew` fails the assertion, which names `services.crew.settings.repositories` and "crew, which is no owner/name".

## Rules

- `code.5`: the key is checked whole at load, with no default for `dir` or `checkout`.
- `code.7`: `kept_at`, `kept`, `kit_kept` and `session_checkouts` are pure, and the host is read once at load, only when the file names any repository.
- `read.1`: a bad entry, or one name for two repositories, is refused naming what crew could not tell.
- `teams.10`: every token fills with text.
- `code.8`: no modelled object changes shape, so `board.agent_views` and `status.js` are untouched.
- `flake.2`, `flake.3`: the module and its pinned file change together, and the logic tier loads the file.
- The design's departures from `code.5` and `plan.18` are the design agent's to amend once this lands (`docs.7`). No rule page is edited here.

## For a later reader

- `plan.main_kit`'s docstring still says "as that host's spaces keep it". `plan.main_kit_said`'s refusal still says "no space there keeps {kit}". Both are now read through `kit_kept`, which counts the teams file too. The refusal is only given where neither keeps the kit, so it is not wrong, only narrower than the spec's words. No scenario reads it.
- The design's open question on crew fetching in the runner's clone (Risks, against boomdrive `core.14`) is agentplot-design's to answer. This change keeps crew's fetches as they were.
