## ADDED Requirements

### Requirement: A set appends one entry naming the keys it changed
Where `crew drive set` changes a key of the teams file, it SHALL append one `drive.set` entry to this host's run record once the file is written and before the drive's state is made, naming `drive/<label>`, the path of each key it changed and never its value, and who ran it. A run that changes no key SHALL append none. crew SHALL refuse `crew drive set` to no caller.

#### Scenario: A set whose state push is refused
- **WHEN** `crew drive set pat` writes the teams file and its push of `pat/main` is refused
- **THEN** this host's run record holds one `drive.set` entry, and the teams file names `pat`

### Requirement: A set's entry reaches the drive's branch
`crew drive set` SHALL push its `drive.set` entry to the drive's branch: with the state's first write where the branch is new, or, where the branch stands, by its last act, which pushes every entry of this host's record of the drive that the branch lacks.

#### Scenario: A new drive
- **WHEN** `crew drive set pat` names `pat` in the teams file for the first time
- **THEN** `pat/main`'s run record holds one `drive.set` entry on `drive/pat`, naming `drives.pat`, `hosts.pats-mac` and `consoles.pat` and no folder, account or address it was given

### Requirement: A set mends a teams file at crew's own version
Where `~/.config/crew/teams.json` is a file at crew's own version, `crew drive set` SHALL set the drive in it and check the file it would write as crew loads a teams file, whatever the file held before for the drive's entry, the hosts `--hosts` names, the drive's console and the kept repositories the flags give. Where every check passes, it SHALL write that file and name each key it changed. A file at crew's own version SHALL never be moved aside.

#### Scenario: A fault in the drive's own entry
- **WHEN** the teams file is at version 6 and names the drives `lab` and `pat`, `pat`'s `folder` is not absolute, and `crew drive set pat` gives an absolute `--folder`
- **THEN** the file it writes names `lab` as it was and `pat` with the folder given, no `teams.json.before-drive-set` is made, and the one key it names as changed is `drives.pat.folder`

#### Scenario: A fault in a host the flags name
- **WHEN** the teams file is at version 6, its `hosts` gives `pats-mac` the kind `macos`, and `crew drive set pat` gives `--hosts pats-mac pats-mac darwin`
- **THEN** the file it writes gives `pats-mac` the kind `darwin`, and the one key it names as changed is `hosts.pats-mac`

#### Scenario: The drive listed twice
- **WHEN** the teams file is at version 6 and lists the drive `pat` twice, and `crew drive set pat` runs
- **THEN** the file it writes lists `pat` once, as the flags give it, and names `drives.pat` as changed

#### Scenario: A file that lists no drives
- **WHEN** the teams file is `{"version":6,"drives":[],"hosts":{}}` and `crew drive set pat` runs
- **THEN** the file it writes names `pat`, and no `teams.json.before-drive-set` is made

### Requirement: A set refuses a teams file it cannot mend
Where a check still fails, or where the file's `drives` is no list of objects or its `hosts`, `consoles` or `repositories` is no object, `crew drive set` SHALL refuse, giving crew's words for the check or naming the key. A refused set SHALL write nothing, move nothing aside and make no state.

#### Scenario: A file that lists teams
- **WHEN** the teams file is `{"version":6,"teams":[]}` and `crew drive set pat` runs
- **THEN** it is refused naming `teams`, nothing is written and no `teams.json.before-drive-set` is made

#### Scenario: A part of another shape
- **WHEN** the teams file is at version 6 and its `hosts` is a list, and `crew drive set pat` runs
- **THEN** it is refused naming `hosts`, nothing is written and no `teams.json.before-drive-set` is made

### Requirement: A set's refusal says what it leaves as it is
The refusal of a set that cannot mend a teams file at crew's own version SHALL say that the set sets only the drive's entry and the hosts, console and kept repositories its flags give, that it moves aside only a file crew cannot read at all, and that the file and every drive it names are left as they are.

#### Scenario: One wrong field beside another drive
- **WHEN** the teams file is at version 6 and names the drives `lab` and `pat`, `lab`'s `folder` is not absolute, and `crew drive set pat` runs
- **THEN** it is refused naming `lab`'s folder and saying the file and every drive it names are left as they are, nothing is written and no `teams.json.before-drive-set` is made

## REMOVED Requirements

### Requirement: A set is one entry naming what it changed
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A set appends one entry naming the keys it changed" and "A set's entry reaches the drive's branch".

### Requirement: A teams file at crew's own version is written where the set mends it
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A set mends a teams file at crew's own version", "A set refuses a teams file it cannot mend" and "A set's refusal says what it leaves as it is".
