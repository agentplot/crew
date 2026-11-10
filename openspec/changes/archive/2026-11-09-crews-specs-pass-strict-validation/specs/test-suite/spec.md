## ADDED Requirements

### Requirement: crew's shell carries its system tools and activates proto's pins, and its tests run on its Python
crew's devenv shell SHALL carry proto, jq and recutils as its system tools. Entering it SHALL install the tools crew's `.prototools` pins, by a devenv task run before the entry and only when one is missing from crew's proto home, and SHALL activate them: moon at the version crew pins, Python at the minor the hosts run crew on, and uv.
crew's tests SHALL run on that Python, with pytest from `tests/pyproject.toml`, locked in `tests/uv.lock` and synced by moon.

#### Scenario: The tests' Python
- **WHEN** crew's logic tier runs as a moon task inside crew's shell
- **THEN** its `python3` is Python 3.13 with pytest importable

#### Scenario: moon's version
- **WHEN** `moon --version` runs inside crew's shell, as a task of crew's contract tier does
- **THEN** it prints the version `.prototools` pins, installed by proto under crew's own proto home

#### Scenario: A moon of the user's
- **WHEN** the user's own proto or moon home holds an older moon
- **THEN** no moon task of crew's runs it

### Requirement: The toolchain crew's policy names only activates, and crew declares it like any kit
The toolchain crew's policy names, `devenv print-dev-env`, SHALL only activate: the script it prints SHALL install nothing. In a working copy sluice equips, sluice's equip installs crew's `.prototools` pins (sluice 147; kit standard toolchain.8).
crew SHALL declare its own toolchain and runner in `.config/sluice.toml` like any kit.

#### Scenario: The toolchain crew's policy names only activates
- **WHEN** the command `.config/sluice.toml` names as its `[tests]` toolchain is run in crew's checkout
- **THEN** the script it prints activates proto's pins and runs no `proto install`

### Requirement: crew's specs pass openspec's strict validation
crew's suite SHALL hold every spec under `openspec/specs/` to `openspec validate --specs --strict`, run in crew's checkout by the machine's openspec, as the end-to-end test `t-specs`, so a requirement past openspec's 500 characters, or one with no SHALL, MUST or scenario, fails the merge whose change brought it. `t-specs` SHALL first find, in scratch specs of its own, a requirement of 501 characters refused and one of 500 taken. Open changes SHALL be outside it.

#### Scenario: crew's specs as they stand
- **WHEN** `tests/suite t-specs` runs in crew's checkout
- **THEN** `openspec validate --specs --strict` passes every spec under `openspec/specs/`, and the test passes

#### Scenario: A requirement one character past the limit
- **WHEN** `t-specs` validates its scratch spec whose one requirement is 501 characters, and the one whose requirement is 500
- **THEN** openspec's strict validation refuses the first and takes the second

## REMOVED Requirements

### Requirement: crew's own toolchain is devenv's system tools and proto's pins
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "crew's shell carries its system tools and activates proto's pins, and its tests run on its Python" and "The toolchain crew's policy names only activates, and crew declares it like any kit".
