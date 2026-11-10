## ADDED Requirements

### Requirement: The package's version is the release file's
crew's flake SHALL version its package by the `version` its tree's `plugin/release.json` gives: a release's `x.y.z` as it is, and main's `0.0.0` as `0-unstable-<date>`, the date of the tree's last change. A version that is neither SHALL fail evaluation, naming the file. Nothing else SHALL set the package's version.

#### Scenario: At a release
- **WHEN** the package's version is reckoned from a release file giving `0.56.0`, for a tree last changed on 2026-11-09
- **THEN** the version is `0.56.0`

#### Scenario: On main
- **WHEN** the package's version is reckoned from a release file giving `0.0.0`, for a tree last changed on 2026-11-09
- **THEN** the version is `0-unstable-2026-11-09`

#### Scenario: The flake's own package on main's tree
- **WHEN** the flake's outputs are evaluated on main's tree
- **THEN** each system's `crew.version` starts `0-unstable-`

#### Scenario: A version that is neither
- **WHEN** the package's version is reckoned from a release file giving `0.56`
- **THEN** evaluation fails, naming `plugin/release.json`

## MODIFIED Requirements

### Requirement: A package built from a commit holds a release file naming it
Where the flake knows the commit it is built from, the package's `plugin/release.json` SHALL name that commit as `commit` and the package's version as `version`, and nothing else. Built from a tree with no commit of its own, as one with uncommitted changes, the package SHALL hold the tree's release file as the tree gives it. The package's `release` SHALL give what its install writes, or null where it writes nothing.

#### Scenario: A build from a commit
- **WHEN** the flake's outputs are evaluated with `self.rev` `fcedc22e6df6380f1f640efac5f796416b1fb4c9`
- **THEN** each system's `crew.release` is that commit with the package's version, and its install writes them to `plugin/release.json`

#### Scenario: A build from a tree with no commit
- **WHEN** the flake's outputs are evaluated with no `self.rev`
- **THEN** each system's `crew.release` is null, and its install writes no `plugin/release.json`, so the package holds the tree's
