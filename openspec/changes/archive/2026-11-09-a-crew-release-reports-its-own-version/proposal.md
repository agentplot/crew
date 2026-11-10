# A crew release reports its own version

## Why

A build of a crew release tag does not know the tag's version. crew keeps its version in no file (`code.10`), so crew's flake versions its package `0-unstable-<date>` whatever commit it is built from, and the build's release file, `plugin/release.json`, names that. Each flake that builds crew supplies the version itself:

- Boomdrive's set (agentplot/boomdrive `nix/packages/crew.nix`, on its bolt `the-boomdrive-flake-configures-the-whole-host`, read 2026-11-09) overrides crew's package version with the tag its `flake.nix` pins. The release file is written before that override, so the build's crew still reads itself as `0-unstable-<date>+<commit>` while its package says `0.50.2`.
- swancloud's `packages/crew` copies the tag's `plugin/` and writes its own `plugin/release.json` for its teamless pin, naming the commit and version it pins.

Both break agentplot/blueprints `design/principles.md` 14: a tool that needs what another program knows reads that program's own source, never a file a host makes for it. agentplot/boomdrive record 0023 (accepted) has the set take each tool's own package. Flume already releases in the family's form: its tag names a release commit, cut from the pushed commit, that writes the release's version into every file carrying Flume's version (`set-version.sh`). Main stays at `0.0.0`.

## What Changes

- **crew's tree names its version.** `plugin/release.json` is in the tree, giving `{"version": "0.0.0"}` on main. crew's manifest, `plugin/.claude-plugin/plugin.json`, gives `0.0.0` too.
- **A release's tag names a release commit.** CI's release job runs a new `set-version.sh <x.y.z>` on the pushed commit, which writes the version into both files. It commits them by path as `chore(release): v<x.y.z>`, tags that commit, pushes the tag alone and publishes the GitHub release at it. Nothing is committed to main, and no branch is pushed.
- **CI reckons from the newest tag by version.** The version job runs git-cliff with `--unreleased`. The conventional check starts at the newest `v*` tag by version, since a release tag is now off main's history.
- **crew's flake takes its package's version from the release file.** A release's `x.y.z` is used as it is. Main's `0.0.0` becomes `0-unstable-<date>` as today. A build that knows its commit writes it into the release file beside the version. A build that knows none keeps the tree's file as it is.
- **crew reads a release file that names a version and no commit.** A copy of a tag's `plugin/` with nothing added reads as `v<x.y.z>` with no commit. `0.0.0` is never shown as a release's version. `crew _release` prints such a crew with a null commit, and one crew reads another's answer of that shape.
- **A checkout reads a release tag at the commit it was cut from.** `git describe` can't see a tag off main's history. So a checkout's version is the newest release tag whose source is HEAD or before it, plus the commits past that source. A tag's source is the release commit's parent, or the commit the tag names for a release made before this change.
- README says so, and the rules' departure from `code.10` is named for the design agent.

## Capabilities

### New Capabilities

- `crew-release`: how crew is released. Main's tree names `0.0.0`; `set-version.sh` writes a release's version; a release's tag names a release commit cut from the pushed commit; CI reckons the next release from the newest tag by version.

### Modified Capabilities

- `crew-flake`: the package's version is the release file's, and a build that knows no commit keeps the tree's release file.
- `host-holds-and-updates`: crew reads a release file that names a release's version and no commit, shows no `0.0.0` as a release's, reads a checkout's version at each release tag's source, and reads another crew's answer that names a release's version and no commit.

## Impact

- New: `plugin/release.json`, `set-version.sh`, `nix/version.nix`, `nix/tests/version.nix`, `tests/t-release.sh`, `tests/contract/test_release.py`.
- `plugin/.claude-plugin/plugin.json`: version `0.0.0`.
- `plugin/lib/crew.py`: `RELEASED`, `release_read`, `release_version`, `crew_read`, `release_said`, `git_version`, new `tag_source` and `checkout_version`, the `_release` usage. `plugin/bin/crew`: the `_release` usage line.
- `flake.nix`, `nix/packages/crew.nix` (comments only), `nix/moon.yml` (inputs), `nix/tests/default.nix`, `nix/tests/package.nix`.
- `.github/workflows/release.yml`, `cliff.toml` (header comment).
- `tests/py/test_release.py`, `tests/t-session-hook.sh`, `tests/moon.yml`.
- `README.md`.
- Unchanged: what crew models and the views of it (`code.8`), and update_due's judgment, which already says it can't tell where the installed crew names no commit.
- Outside crew: Boomdrive's `nix/packages/crew.nix` override and swancloud's own release file for its teamless pin are no longer needed once a release is made this way. Each belongs to its own repository.
