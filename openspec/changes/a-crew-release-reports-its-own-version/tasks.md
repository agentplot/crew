# Tasks

Each check is a moon task run through `tests/suite`: `logic` is `tests:logic`, `contract` is `tests:contract`, and `nix:<task>` is the flake's project. Build the groups in order. Submit nothing: Flume submits the place once its last stage delivers.

## 1. The tree's version and its writer

- [x] 1.1 Main's tree holds `plugin/release.json` as `{"version": "0.0.0"}` alone and crew's manifest at `0.0.0`. `set-version.sh <x.y.z> [<root>]` writes the version into both, changing no other line, and refuses a version that is not `x.y.z` or a file with no version, naming it. `tests/t-release.sh` proves it, with its task in `tests/moon.yml` (design, Decisions 1 and 2; Task notes 1.1). Verify `tests/suite t-release` ends with "0 failed".

## 2. crew's reads of itself

- [x] 2.1 A release file naming a release's version and no commit reads as `v<x.y.z>` with no commit, from the release, nothing unread. A file with no commit and any other version reads as naming no commit, and `0.0.0` shows as `0.0.0+<commit>`, never `v0.0.0` (design, Decision 5; Task notes 2.1). Passes `tests/py/test_release.py` (`tests/suite logic`).
- [x] 2.2 Another crew's `crew _release` answer from a release, naming a release's version and a null commit, reads as that version with no commit. An answer from a checkout with no commit stays unread, and `_release`'s usage says the commit is null where a release names none (design, Decision 5; Task notes 2.2). Passes `tests/py/test_release.py` (`tests/suite logic`).
- [x] 2.3 `tag_source` gives a release commit's parent, or else the commit the tag names. `checkout_version` gives the tag with `+<n>` for the commits past its source (design, Decision 4; Task notes 2.3). Passes `tests/py/test_release.py` (`tests/suite logic`).
- [x] 2.4 `git_version` reads a checkout's version as the newest release tag, by version, whose source is HEAD or before it. Against real git, it reads a release commit cut off main and tagged, a checkout of the tag, and an older tag on main's own history (design, Decision 4; Task notes 2.4). Passes `tests/contract/test_release.py` (`tests/suite contract`).
- [ ] 2.5 A start's record is checked against the commit and version `crew _release` prints for the same checkout, with no `git describe` of the test's own (design, Decision 4; Task notes 2.5). Verify `tests/suite t-session-hook` ends with "0 failed".

## 3. The flake

- [ ] 3.1 `nix/version.nix` reckons the package's version from the release file: a release's `x.y.z` as it is, `0.0.0` as `0-unstable-<date>`, and any other version failing evaluation, naming the file. `flake.nix` takes it from the tree's `plugin/release.json`, and the nix project's type check and test take that file as an input (design, Decision 3; Task notes 3.1). Verify `tests/suite nix:format nix:lint nix:test` ends with "0 failed".
- [ ] 3.2 A build that knows no commit writes no release file over the tree's, and its `release` is null. `nix/packages/crew.nix` says the package holds the tree's release file and writes the commit and version over it where the flake knows the commit (design, Decision 3; Task notes 3.2). Verify `tests/suite nix:test` ends with "0 failed".

## 4. The release on GitHub

- [ ] 4.1 The release job runs `set-version.sh` on the pushed commit, commits its two files by path as `chore(release): $TAG`, tags that commit, pushes the tag alone and publishes the release with `--verify-tag`. The version job runs `git-cliff --unreleased --bumped-version`, the conventional job starts at the newest `v*` tag by version, and `tests/t-release.sh` reads them (design, Decisions 6 and 7; Task notes 4.1). Verify `tests/suite t-release` ends with "0 failed".

## 5. The docs

- [ ] 5.1 README says crew's tree holds `plugin/release.json` at `0.0.0` on main and at the release's version at its tag. It says a release's tag names a release commit `set-version.sh` writes, a build adds the commit it knows, a copy of a tag's `plugin/` reads as its version with no commit, and the flake's package takes its version from the file (Task notes 5.1). Verify `tests/suite t-docs` ends with "0 failed".
