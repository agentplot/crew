## ADDED Requirements

### Requirement: crew's kinds folder holds its bolt kind
Wherever crew writes a roles file with an entry, it SHALL make the folder `~/.local/share/flume/kinds/crew` when it is missing, and keep in it crew's one kind package, `bolt@1/kind.toml`, byte for byte as crew ships it in `plugin/flume/kinds/bolt@1/kind.toml`, and nothing else (record 0056). Where it writes the roles file with no entry, it SHALL make no folder and write no package.

#### Scenario: The package beside the file
- **WHEN** crew's follower first writes the roles file on mac-studio
- **THEN** `~/.local/share/flume/kinds/crew/bolt@1/kind.toml` holds crew's bolt kind byte for byte, and the folder holds nothing else

#### Scenario: A main level started
- **WHEN** `crew main up wldn` starts wldn's main level on chuck-herdr-alpha
- **THEN** chuck-herdr-alpha's kinds folder holds `bolt@1/kind.toml`

#### Scenario: A host with no main level
- **WHEN** crew writes the roles file on a host that is no partition's machine, where no kinds folder is
- **THEN** no kinds folder is made and no package is written

### Requirement: crew's bolt kind is a base place, and a version of it never changes
The package SHALL declare the kind `bolt` at version 1, its places' branches `bolt/<bolt>`, that lands with no stages, so a launch naming `crew/bolt` is a bolt's base place. A version's bytes SHALL never change: a change to the kind is a new version beside it.

#### Scenario: The package's bytes
- **WHEN** `plugin/flume/kinds/bolt@1/kind.toml` is read
- **THEN** its one table is `kinds.bolt`, with `version = 1`, `branch = "bolt"`, `lands = true` and `stages = []` and no other key, and its bytes are those crew's logic case pins

### Requirement: The package is written whole and renamed over the old one, only when it differs
crew SHALL write the package whole to a new file beside it and rename it over the old one, never editing it in place, and only when its bytes differ from the file's. It SHALL run no `flume` command for it and lock no kind: the lock of `crew/bolt@1` is the host's.

#### Scenario: Nothing moved
- **WHEN** crew's follower runs again on mac-studio with the package in the kinds folder as crew ships it
- **THEN** the package is not written, and its modification time is as it was

#### Scenario: Renamed over
- **WHEN** a second link is kept to the package in the kinds folder, its bytes differ from crew's, and the follower runs again
- **THEN** the package holds crew's bytes, and the old link still holds the file as it was

#### Scenario: No flume command
- **WHEN** crew's follower writes the package on mac-studio
- **THEN** no `flume` command runs, and no lock file of the host's is written

## REMOVED Requirements

### Requirement: crew's kinds folder exists and holds nothing yet
**Reason**: The folder holds crew's bolt kind, `crew/bolt@1`, the base place each bolt is launched as (record 0056 point 2). Record 0057 decision 5 left the folder empty until crew had a kind to declare in it.
**Migration**: crew makes the folder where it made it before and keeps its one package there (requirement "crew's kinds folder holds its bolt kind"). The host locks `crew/bolt@1` by its own configuration; until it does, Flume refuses the bolt's launch naming the lock.
