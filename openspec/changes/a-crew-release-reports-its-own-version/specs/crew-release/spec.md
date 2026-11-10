## ADDED Requirements

### Requirement: Main's tree names no release
On main, crew's release file, `plugin/release.json`, SHALL give `version` `0.0.0` and no other key, and crew's manifest, `plugin/.claude-plugin/plugin.json`, SHALL give `version` `0.0.0`, so a tree that is no release's says so in crew's own source.

#### Scenario: Main's files
- **WHEN** `plugin/release.json` and `plugin/.claude-plugin/plugin.json` are read on main's tree
- **THEN** the release file is a JSON object whose one key is `version`, `0.0.0`, and the manifest's `version` is `0.0.0`

### Requirement: set-version.sh writes a release's version into every file that carries crew's version
`sh set-version.sh <x.y.z> [<root>]` SHALL write the version as `version` in the release file and crew's manifest under the root, the folder it is in by default, changing no other line. It SHALL refuse a version that is not `x.y.z`, and a file in which it finds no version to write, naming it and exiting non-zero.

#### Scenario: A release's version
- **WHEN** `sh set-version.sh 98.76.54 <copy>` runs on a copy of main's two files
- **THEN** both give `98.76.54`, and each file's diff from main's changes exactly the lines that give the version

#### Scenario: Not a version
- **WHEN** `sh set-version.sh 0.56 <copy>` runs
- **THEN** it exits non-zero, saying `0.56` is not a version `major.minor.patch`, and neither file changes

#### Scenario: A file with no version
- **WHEN** `sh set-version.sh 98.76.54 <copy>` runs where the copy's manifest gives no `version`
- **THEN** it exits non-zero, naming `plugin/.claude-plugin/plugin.json`

### Requirement: A release's tag names a release commit cut from the pushed commit
CI's release job SHALL run `set-version.sh` for the release's version on the pushed commit and commit the two files by path as `chore(release): v<x.y.z>`, so the pushed commit is its one parent. The tag SHALL name that commit and be pushed alone, and the GitHub release SHALL be published at the tag. Nothing SHALL be committed to main, no branch pushed and no tag moved.

#### Scenario: The release job
- **WHEN** `.github/workflows/release.yml` is read
- **THEN** its release job runs `sh set-version.sh "${TAG#v}"`, commits `plugin/release.json` and `plugin/.claude-plugin/plugin.json` by path as `chore(release): $TAG`, tags that commit, pushes `refs/tags/$TAG` and no other ref, and publishes the release with `--verify-tag`

### Requirement: CI reckons the next release from the newest tag by version
CI's version job SHALL reckon the next version with git-cliff's `--unreleased` and `--bumped-version`, and its conventional check SHALL check the commits since the newest `v*` tag by version, since a release's tag names a commit off main's history.

#### Scenario: The version and conventional jobs
- **WHEN** `.github/workflows/release.yml` is read
- **THEN** its version job runs `git-cliff --unreleased --bumped-version`, and its conventional job's range starts at the first of `git tag --list 'v*' --sort=-v:refname`, with no `git describe`
