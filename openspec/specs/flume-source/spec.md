# flume-source Specification

## Purpose
crew as a source of its host's Flume (Flume record 0039; agentplot/flume v0.17.0, `reference/configuration.md`, "The host's sources" and "A source's roles"): the roles file crew writes from its teams file, declaring at each address of a drive on the host the agent that holds it, and the kinds folder beside it. The host declares the source, naming both paths; crew writes what they hold (record 0057, `teams.25`).

## Requirements

### Requirement: Each standing main-level role is declared at its address as its agent
On a host that is the machine of one or more drives, crew's roles file, `~/.local/state/crew/flume/roles.toml`, SHALL hold one entry at `<label>/<role>` for each main-level role, `design`, `planner`, `reviewer`, `ops` and `operator`, of each such drive whose teams-file `runs` names that role `standing`, `<label>` being the drive's label. Each entry SHALL give `agent`, the name crew gives that role's agent, `<label>-<role>`.

#### Scenario: deneb's three drives
- **WHEN** crew writes the file on deneb from a teams file whose drives agentplot, madswan and swancloud have deneb as their machine and whose `runs` names every role `standing`
- **THEN** the file holds fifteen entries, five for each of `agentplot`, `madswan` and `swancloud`, among them `agentplot/planner` with `agent = "agentplot-planner"` and `madswan/ops` with `agent = "madswan-ops"`

### Requirement: An entry names the session crew opens its agent in
Each entry SHALL give `session`, the herdr session crew opens the role's agent in: the role's own where the drive's `roles` names one, the reviewer beside the planner where only the planner's is named, else the drive's.

#### Scenario: Sessions of the drives' names
- **WHEN** crew writes the file on deneb from a teams file whose drives agentplot, madswan and swancloud run in sessions of the same names and name no role's session
- **THEN** every `agentplot/` entry gives `session = "agentplot"`, every `madswan/` entry `session = "madswan"` and every `swancloud/` entry `session = "swancloud"`

#### Scenario: A role with a session of its own
- **WHEN** crew writes the file on chuck-herdr-alpha from a teams file whose drive wldn has that machine, the session `wldn-2`, and its planner in the session `wldn-1`
- **THEN** `wldn/planner` and `wldn/reviewer` give `session = "wldn-1"`, and `wldn/design`, `wldn/ops` and `wldn/operator` give `session = "wldn-2"`

### Requirement: What a role answers is the words crew's briefs give for whom to ask
The design agent's, the planner's and ops's entries SHALL give `answers`, the words crew's briefs give for whom to ask about what, from the one text the briefs' sentence is built from: the design agent `the design`, the planner `the plan`, ops `a live system, a deploy or a landing`. The operator's entry SHALL give `answerer = true` and no `answers`. The reviewer's SHALL give neither.

#### Scenario: The words in the file and in the brief
- **WHEN** crew writes madswan's entries, and builds madswan's planner's brief
- **THEN** `madswan/design` answers `the design`, `madswan/planner` `the plan` and `madswan/ops` `a live system, a deploy or a landing`; and the brief tells its agent to ask `madswan-design` for the design, `madswan-ops` for a live system, a deploy or a landing, and `madswan-planner` for the plan

#### Scenario: The door and the reviewer
- **WHEN** crew writes madswan's entries
- **THEN** `madswan/operator` gives `answerer = true` and no `answers`, and `madswan/reviewer` gives only `agent` and `session`

### Requirement: An entry gives a standing agent's keys alone
Each entry SHALL give only `agent`, `session`, `answers` and `answerer`, never `kind`, `repository`, `priority`, `base`, `brief`, `name`, `intent`, `agents`, `carried` or any other key, and the file SHALL give `roles` alone, as TOML.

#### Scenario: Read as Flume reads it
- **WHEN** the file crew writes from a teams file is read as TOML
- **THEN** its one key is `roles`, every key under it is an address `<stream>/<role>`, and every entry's keys are among `agent`, `session`, `answers` and `answerer`, `agent` and `session` in every one

### Requirement: No entry for a drive on another host or a role that runs as its kind
crew SHALL write no entry for a drive whose machine is another host, carried or otherwise, and none for a role whose teams-file `runs` names it `on-demand`.

#### Scenario: wldn on deneb
- **WHEN** crew writes the file on deneb from a teams file that also lists wldn, its machine chuck-herdr-alpha
- **THEN** no address in it begins `wldn/`

#### Scenario: A planner that runs as its kind
- **WHEN** madswan's teams-file `runs` names its planner `on-demand` and its other roles `standing`
- **THEN** the file holds `madswan/design`, `madswan/reviewer`, `madswan/ops` and `madswan/operator`, and no `madswan/planner`

### Requirement: The file is written whole and renamed over the old one, only when it differs
crew SHALL write the roles file whole to a new file beside it and rename it over the old one, never editing it in place, and only when what it would write differs from what the file holds.

#### Scenario: Nothing moved
- **WHEN** crew's follower runs on mac-studio twice with the teams file unchanged
- **THEN** the second run does not write the roles file

#### Scenario: Renamed over
- **WHEN** a second link is kept to the roles file, the teams file is rewritten naming madswan's planner the session `madswan-2`, and the follower runs again
- **THEN** the roles file gives `madswan/planner` the session `madswan-2`, and the old link still holds the file as it was

### Requirement: The follower and a main-level start keep the file
crew's follower SHALL write the roles file each time it reads the teams file, and crew SHALL write it each time it starts a main-level role's agent. crew SHALL run no `flume` command to write it, and SHALL change nothing in the teams file.

#### Scenario: The follower's first read
- **WHEN** crew's follower runs once on mac-studio, the machine of madswan and swancloud, with no roles file there
- **THEN** the roles file holds madswan's and swancloud's ten entries, the teams file is unchanged, and no `flume` command ran

#### Scenario: A main level started
- **WHEN** `crew main up wldn` starts wldn's main level on chuck-herdr-alpha
- **THEN** chuck-herdr-alpha's roles file holds wldn's five entries

### Requirement: A host with no main level declares nothing
On a host that is no drive's machine, crew SHALL make no roles file, and SHALL write one already there with no entry.

#### Scenario: A main level moved away
- **WHEN** the teams file moves wldn's main level from chuck-herdr-alpha to mac-studio's session `wldn-5`, and the follower runs on chuck-herdr-alpha
- **THEN** chuck-herdr-alpha's roles file, where its follower wrote wldn's entries before, holds no entry; and where it had none, none is made

### Requirement: A teams file crew refuses leaves the file as it is
When crew cannot read the teams file, it SHALL leave the roles file as it is and say why, naming the teams file.

#### Scenario: A teams file at another version
- **WHEN** the teams file is rewritten at version 4, and the follower runs
- **THEN** the roles file is left as it was, and the follower says why it could not read the teams file, naming it

### Requirement: crew's kinds folder holds its bolt kind
Wherever crew writes a roles file with an entry, it SHALL make the folder `~/.local/share/flume/kinds/crew` when it is missing, and keep in it crew's one kind package, `bolt@1/kind.toml`, byte for byte as crew ships it in `plugin/flume/kinds/bolt@1/kind.toml`, and nothing else (record 0056). Where it writes the roles file with no entry, it SHALL make no folder and write no package.

#### Scenario: The package beside the file
- **WHEN** crew's follower first writes the roles file on mac-studio
- **THEN** `~/.local/share/flume/kinds/crew/bolt@1/kind.toml` holds crew's bolt kind byte for byte, and the folder holds nothing else

#### Scenario: A main level started
- **WHEN** `crew main up wldn` starts wldn's main level on chuck-herdr-alpha
- **THEN** chuck-herdr-alpha's kinds folder holds `bolt@1/kind.toml`

#### Scenario: A host with no main level
- **WHEN** crew writes the roles file on a host that is no drive's machine, where no kinds folder is
- **THEN** no kinds folder is made and no package is written

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
