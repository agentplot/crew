## ADDED Requirements

### Requirement: crew's bolt kind is a base place at version 1, whose bytes never change once released
The package SHALL declare the kind `bolt` at version 1, its places' branches `bolt/<bolt>`, that lands with no stages, so a launch naming `crew/bolt` is a bolt's base place.
A version's bytes SHALL never change once released: a change to the kind is a new version beside it.

#### Scenario: The package's bytes
- **WHEN** `plugin/flume/kinds/bolt@1/kind.toml` is read
- **THEN** its one table is `kinds.bolt`, with `version = 1`, `branch = "bolt"`, `lands = true`, `stages = []`, `landing_fix = "flume/fix@1"` and `max_landing_fixes = 3` and no other key, and its bytes are those crew's logic case pins

### Requirement: crew's bolt kind names Flume's fix kind as its landing fix, and how many it runs
The package SHALL name its landing fix, the kind Flume runs when the merge queue sends the bolt's branch back or forecasts it in conflict with main, as `landing_fix = "flume/fix@1"`, Flume's own fix kind by its whole identity with its version, and the most landing fixes Flume runs before the base place waits on its caller as `max_landing_fixes = 3` (weir record 0005; flume record 0056).

#### Scenario: The landing fix is named by identity
- **WHEN** the package's `landing_fix` is read
- **THEN** it names a source, a kind and a version, `flume`, `fix` and `1`, and `max_landing_fixes` is a positive count

## REMOVED Requirements

### Requirement: crew's bolt kind is a base place, and a version of it never changes
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "crew's bolt kind is a base place at version 1, whose bytes never change once released" and "crew's bolt kind names Flume's fix kind as its landing fix, and how many it runs".
