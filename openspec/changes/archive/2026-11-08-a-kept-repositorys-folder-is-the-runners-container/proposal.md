# A kept repository's folder is the runner's container

## Why

crew names a kit's folder `<session dir>/<name>` and its checkout `<session dir>/<name>/main`, built from the sessions in swancloud's hosts file (`crew.py` `checkout`, `kit_kept`, `kept_on`). swancloud record 0060, accepted by the user on 2026-11-08, makes the runner's clone the one copy of each repository on a runner host (agentplot/boomdrive `core.14`). Every agent that submits there works in worktrees of that clone and reads the default branch from the runner's view.

The runner's container holds `<name>.git`, a `.git` file and `places`. It has no `main`. The default branch's working tree is the runner's view, `~/Code/boomdrive/<owner>/<name>` on deneb, which the runner alone moves. No setting of swancloud's can point crew's folders there, since crew builds them.

Record 0061 (accepted 2026-11-08) decides where crew learns them: crew's own teams file names each kept repository's `dir` and `checkout` for the host it is written on. swancloud writes the key for deneb, and Boomdrive's module once the flake is ready (`flake.2`). Where the file names none, crew names them as today.

## What Changes

- **The teams file may name the host's kept repositories.** A top-level `repositories` object maps each repository's address, `<owner>/<name>`, to its `dir` and its `checkout`, each an absolute path. crew checks every entry at load, before any is used, and refuses a bad one naming the file and the machine's configuration. The file stays at version 5, and a file without the key loads as today.
- **crew names a kept repository's folder and checkout from the file, on the host it is written on.** On that host a repository the file names is kept at its `dir` and `checkout`, whether or not a session's space lists it. One the file does not name is found in the sessions' spaces, as today. For another host, crew names folders from the hosts file, as today.
- **Every place crew reads a kit's folder on the host follows**:
  - the partition's checkout, where its main level starts;
  - `kit_kept`, and so `main_kit`, the main level's kit folders and the brief's kits;
  - `kept_on`, and so the blueprints folders and the teams doors;
  - ops's deploy range (`ops.kit_range`).
- **Every main level's brief names them.** The design brief names its blueprints checkout and each kit's checkout, each with its folder, where its worktrees go. The operator's brief names swancloud's checkout and folder as its main level's host keeps them, in place of the hard-coded `~/Code/github_afterthought/swancloud`. The design brief says a checkout is moved by its host: the fleet's timer, or the runner on a runner host.
- **The flake follows the file's shape** (`flake.2`). `services.crew.settings.repositories` is declared, each entry with `dir` and `checkout` and no default. A pinned file of deneb's partitions with kept repositories, `nix/tests/files/runner.json`, is pinned by the nix test and loaded by crew's logic tier.
- **README and the crew skill** say what the key does.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `main-level`: the teams file may name the host's kept repositories, checked at load. The design and operator briefs name each kept repository's checkout and folder as the host keeps it.
- `drive-state`: work done before a runner takes it is done in the checkout the teams file names, where the main-level host is the host crew runs on and its file names the repository. Elsewhere it is the checkout the spaces keep.
- `crew-flake`: the module writes `repositories` from `services.crew.settings`, each entry with its `dir` and `checkout`, and fails evaluation for an entry that is not of that shape.

## Impact

- `plugin/lib/crew.py`: `load` reads and checks `repositories`. A new pure resolver serves `checkout`'s callers, `kit_kept`, `kept_on` and the partition's checkout. `main_tokens` gains the folders and swancloud's tokens.
- `plugin/lib/ops.py`: `kit_range` reads its checkouts through the resolver.
- `plugin/roles/design.md`, `plugin/roles/operator.md`: the folders named from tokens.
- `nix/modules/options.nix`, `nix/tests/settings.nix`, `nix/tests/file.nix`, `nix/tests/files/runner.json`.
- `tests/py/test_teams.py`, `tests/py/test_kits.py`, `tests/py/test_ops.py`, `tests/py/test_module_file.py`, `tests/t-briefs.sh`.
- `README.md`, `plugin/skills/crew/SKILL.md`.
- Unchanged:
  - a kit's folder the runner reports (`runner.where`, `plan.kit_of`), already the runner's container;
  - `gather.py`, which takes the folder and checkout it is given;
  - `crew_on`, which reads another host;
  - the views and crew's mod (`code.8`): no bolt, unit, stage, card or rail row changes shape.
