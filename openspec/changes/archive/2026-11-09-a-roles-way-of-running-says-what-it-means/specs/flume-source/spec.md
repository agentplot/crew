## MODIFIED Requirements

### Requirement: Each standing main-level role is declared at its address as its agent
On a host that is the machine of one or more drives, crew's roles file, `~/.local/state/crew/flume/roles.toml`, SHALL hold one entry at `<label>/<role>` for each main-level role, `design`, `planner`, `reviewer`, `ops` and `operator`, of each such drive whose teams-file `runs` names that role `standing`, `<label>` being the drive's label. Each entry SHALL give `agent`, the name crew gives that role's agent, `<label>-<role>`.

#### Scenario: deneb's three drives
- **WHEN** crew writes the file on deneb from a teams file whose drives agentplot, madswan and swancloud have deneb as their machine and whose `runs` names every role `standing`
- **THEN** the file holds fifteen entries, five for each of `agentplot`, `madswan` and `swancloud`, among them `agentplot/planner` with `agent = "agentplot-planner"` and `madswan/ops` with `agent = "madswan-ops"`

### Requirement: No entry for a drive on another host or a role that runs as its kind
crew SHALL write no entry for a drive whose machine is another host, carried or otherwise, and none for a role whose teams-file `runs` names it `on-demand`.

#### Scenario: wldn on deneb
- **WHEN** crew writes the file on deneb from a teams file that also lists wldn, its machine chuck-herdr-alpha
- **THEN** no address in it begins `wldn/`

#### Scenario: A planner that runs as its kind
- **WHEN** madswan's teams-file `runs` names its planner `on-demand` and its other roles `standing`
- **THEN** the file holds `madswan/design`, `madswan/reviewer`, `madswan/ops` and `madswan/operator`, and no `madswan/planner`
