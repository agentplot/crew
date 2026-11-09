## RENAMED Requirements

- FROM: `### Requirement: No entry for a partition on another host or a role that runs as its kind`
- TO: `### Requirement: No entry for a drive on another host or a role that runs as its kind`


## MODIFIED Requirements

### Requirement: Each standing main-level role is declared at its address as its agent
On a host that is the machine of one or more drives, crew's roles file, `~/.local/state/crew/flume/roles.toml`, SHALL hold one entry at `<label>/<role>` for each main-level role, `design`, `planner`, `reviewer`, `ops` and `operator`, of each such drive whose teams-file `flume` names that role `false`, `<label>` being the drive's label. Each entry SHALL give `agent`, the name crew gives that role's agent, `<label>-<role>`.

#### Scenario: deneb's three partitions
- **WHEN** crew writes the file on deneb from a teams file whose drives agentplot, madswan and swancloud have deneb as their machine and name every role `false`
- **THEN** the file holds fifteen entries, five for each of `agentplot`, `madswan` and `swancloud`, among them `agentplot/planner` with `agent = "agentplot-planner"` and `madswan/ops` with `agent = "madswan-ops"`

### Requirement: An entry names the session crew opens its agent in
Each entry SHALL give `session`, the herdr session crew opens the role's agent in: the role's own where the drive's `roles` names one, the reviewer beside the planner where only the planner's is named, else the drive's.

#### Scenario: Sessions of the partitions' names
- **WHEN** crew writes the file on deneb from a teams file whose drives agentplot, madswan and swancloud run in sessions of the same names and name no role's session
- **THEN** every `agentplot/` entry gives `session = "agentplot"`, every `madswan/` entry `session = "madswan"` and every `swancloud/` entry `session = "swancloud"`

#### Scenario: A role with a session of its own
- **WHEN** crew writes the file on chuck-herdr-alpha from a teams file whose drive wldn has that machine, the session `wldn-2`, and its planner in the session `wldn-1`
- **THEN** `wldn/planner` and `wldn/reviewer` give `session = "wldn-1"`, and `wldn/design`, `wldn/ops` and `wldn/operator` give `session = "wldn-2"`

### Requirement: No entry for a drive on another host or a role that runs as its kind
crew SHALL write no entry for a drive whose machine is another host, carried or otherwise, and none for a role whose teams-file `flume` names a stream.

#### Scenario: wldn on deneb
- **WHEN** crew writes the file on deneb from a teams file that also lists wldn, its machine chuck-herdr-alpha
- **THEN** no address in it begins `wldn/`

#### Scenario: A planner that runs as its kind
- **WHEN** madswan's teams-file `flume` names the stream `madswan` for its planner and `false` for its other roles
- **THEN** the file holds `madswan/design`, `madswan/reviewer`, `madswan/ops` and `madswan/operator`, and no `madswan/planner`

### Requirement: A host with no main level declares nothing
On a host that is no drive's machine, crew SHALL make no roles file, and SHALL write one already there with no entry.

#### Scenario: A main level moved away
- **WHEN** the teams file moves wldn's main level from chuck-herdr-alpha to mac-studio's session `wldn-5`, and the follower runs on chuck-herdr-alpha
- **THEN** chuck-herdr-alpha's roles file, where its follower wrote wldn's entries before, holds no entry; and where it had none, none is made
