## ADDED Requirements

### Requirement: A checkout reads each release tag at the commit it was cut from
In a checkout, crew's version SHALL be the newest release tag, `v<x.y.z>` by version, whose source is HEAD or an ancestor of it, with `+<n>` for the n commits from the source to HEAD, and the tag alone where HEAD is the tag's own commit. A tag's source SHALL be the parent of the commit it names where that commit is a release commit, its subject `chore(release): <tag>`, and otherwise that commit.

#### Scenario: Main past a release
- **WHEN** a checkout's HEAD on main is two commits past P, and `v0.56.0` names a commit off main, `chore(release): v0.56.0`, whose parent is P
- **THEN** crew's version there is `v0.56.0+2` and its commit HEAD's

#### Scenario: Main at the commit a release was cut from
- **WHEN** a checkout's HEAD is P, from which `v0.56.0`'s release commit was cut
- **THEN** crew's version there is `v0.56.0`

#### Scenario: A checkout of the tag
- **WHEN** a checkout's HEAD is the release commit `v0.56.0` names
- **THEN** crew's version there is `v0.56.0`

#### Scenario: A release tagged on main's own commit
- **WHEN** a checkout's HEAD on main is three commits past the commit `v0.55.0` names, a commit of main that is no release commit, and no newer tag's source is HEAD or before it
- **THEN** crew's version there is `v0.55.0+3`

#### Scenario: No release tag before HEAD
- **WHEN** no release tag's source is HEAD or an ancestor of it
- **THEN** crew reads HEAD's commit and no version

## MODIFIED Requirements

### Requirement: crew knows the release it runs from
crew SHALL read the crew it runs as from where it runs: in a checkout, HEAD's commit and the version git gives it; with no git, the version `plugin/release.json` names, and its commit where named; and nothing where it finds neither, or a release file naming neither a full commit nor a release's version, saying what it could not read wherever a decision rests on it. A session's start SHALL record the commit and version of the crew whose plugin it loaded.

#### Scenario: A build's release
- **WHEN** crew runs from a folder with no git whose `plugin/release.json` names the commit `fcedc22e6df6380f1f640efac5f796416b1fb4c9` and the version `0-unstable-2026-11-08`, and a crew agent's session that loaded that folder's plugin starts
- **THEN** the start records that commit and the version `0-unstable-2026-11-08+fcedc22`

#### Scenario: A release tag's plugin copied whole
- **WHEN** crew runs from a folder with no git whose `plugin/release.json` names the version `0.56.0` and no commit
- **THEN** crew reads the version `v0.56.0` and no commit, from the release, and says nothing is unread

#### Scenario: A copy of main's plugin
- **WHEN** crew runs from a folder with no git whose `plugin/release.json` names the version `0.0.0` and no commit
- **THEN** crew reads no release there and says the file names no commit

#### Scenario: A build with no release
- **WHEN** crew runs from a folder with no git and no release file
- **THEN** a start that loads its plugin records no commit and no version

#### Scenario: A release file crew can't read
- **WHEN** a build's release file names a commit that is not forty hexadecimal characters
- **THEN** crew reads no release there and says the file names no commit

#### Scenario: A start records the crew it loaded
- **WHEN** a crew agent's session starts on a crew checkout
- **THEN** its start records the commit and version `crew _release` prints for that checkout

### Requirement: A build's version is shown as a checkout's is
crew SHALL show a build's version as `v<x.y.z>` where its release file names a release's version, `x.y.z` other than main's `0.0.0`, and otherwise as the version the file names followed by `+` and the commit's first seven characters, so two builds of one day read apart.

#### Scenario: A release version
- **WHEN** a build's release file names the version `0.44.1`
- **THEN** crew's version there is `v0.44.1`

#### Scenario: An untagged version
- **WHEN** a build's release file names the version `0-unstable-2026-11-08` and the commit `fcedc22e6df6380f1f640efac5f796416b1fb4c9`
- **THEN** crew's version there is `0-unstable-2026-11-08+fcedc22`

#### Scenario: Main's version
- **WHEN** a build's release file names the version `0.0.0` and the commit `fcedc22e6df6380f1f640efac5f796416b1fb4c9`
- **THEN** crew's version there is `0.0.0+fcedc22`

### Requirement: crew _release prints what a crew is
`crew _release` SHALL print, as one line of JSON, the crew's root, commit and version, the commit null where a release names none, and whether they came from a checkout or a release, reading nothing else and starting nothing; `-h` and `--help` SHALL print its usage.

#### Scenario: From a build
- **WHEN** `crew _release` runs from a build whose release file names a commit and a version
- **THEN** it prints them with `from` `release`

#### Scenario: From a build of a tag that names no commit
- **WHEN** `crew _release` runs from a build whose release file names the version `0.56.0` and no commit
- **THEN** it prints the version `v0.56.0`, a null commit and `from` `release`

#### Scenario: From a checkout
- **WHEN** `crew _release` runs from a checkout
- **THEN** it prints the checkout's commit and version with `from` `checkout`

#### Scenario: From a build with no release
- **WHEN** `crew _release` runs from a folder with no git and no release file
- **THEN** it prints no commit and no version, with `from` null

### Requirement: crew reads the crew its host has installed
crew SHALL read what the installed crew is from its own files where the installed command is its own, and otherwise by asking it, `crew _release`, within five seconds. An answer that does not come in time, fails, or lacks a field SHALL read as unread, saying which; a null commit is no lack where the answer is from a release naming a release's version. A process SHALL ask once for each real path of the installed command.

#### Scenario: Its own crew
- **WHEN** the installed command is crew's own checkout's `plugin/bin/crew`
- **THEN** crew reads the checkout with no process

#### Scenario: The installed crew does not answer
- **WHEN** the installed command does not answer `crew _release` within five seconds
- **THEN** crew reads the installed crew as unread, saying it did not answer

#### Scenario: An answer with a field missing
- **WHEN** the installed command's `crew _release` prints JSON from a checkout with no `commit`
- **THEN** crew reads the installed crew as unread, saying the answer names no commit

#### Scenario: An installed release that names no commit
- **WHEN** the installed command's `crew _release` prints the version `v0.56.0`, a null commit and `from` `release`
- **THEN** crew reads the installed crew as `v0.56.0` with no commit, from a release
