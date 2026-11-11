## ADDED Requirements

### Requirement: A host opens the consoles its teams file names
`crew console up <label>` SHALL open a drive's console only on a host whose teams file names the drive in its `consoles`, in the host's herdr session named for the label, its tabs and the rail's shell opening in the folder `consoles` gives the drive. Elsewhere it SHALL be refused, naming the drive, the host and `consoles`, with nothing opened.

#### Scenario: A console the host names
- **WHEN** deneb's teams file gives `consoles` naming wldn with `/Users/chuck/Code/clients/github_willdan`, wldn's main level runs on chuck-herdr-alpha, and `crew console up wldn` runs on deneb
- **THEN** the `console` workspace of deneb's `wldn` session opens, its `shell` tab in `/Users/chuck/Code/clients/github_willdan`, and no agent is started

#### Scenario: A console the host does not name
- **WHEN** mac-studio's teams file gives no `consoles`, and `crew console up wldn` runs on mac-studio
- **THEN** it is refused naming wldn, mac-studio and `consoles`, and no tab is opened

### Requirement: A host's operator sessions are the consoles its teams file names
A host's operator sessions SHALL be the drives its teams file's `consoles` names, read from no other file. Its follower SHALL follow those drives and no other, and `crew go` SHALL open each of their consoles again.

#### Scenario: The drives a host follows
- **WHEN** deneb's `consoles` names afterthought, agentplot, madswan and wldn, and its teams file lists those four drives and swancloud
- **THEN** deneb's follower refreshes afterthought, agentplot, madswan and wldn, and not swancloud

#### Scenario: Consoles after a hold
- **WHEN** `crew go deneb` lifts deneb's hold and deneb's `consoles` names agentplot and wldn
- **THEN** crew opens agentplot's and wldn's consoles on deneb again, and no other drive's
