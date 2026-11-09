## RENAMED Requirements

- FROM: `### Requirement: A teams file at crew's own version that fails a check is refused`
- TO: `### Requirement: A teams file at crew's own version is written where the set mends it`

## MODIFIED Requirements

### Requirement: A teams file at crew's own version is written where the set mends it
Where `~/.config/crew/teams.json` is a file at crew's own version, `crew drive set` SHALL set the drive in it and check the file it would write as crew loads a teams file, whatever the file held before for the drive's entry, the hosts `--hosts` names, the drive's console and the kept repositories the flags give. Where every check passes, it SHALL write that file and name each key it changed. Where a check still fails, or where the file's `drives` is no list of objects or its `hosts`, `consoles` or `repositories` is no object, it SHALL refuse, giving crew's words for the check or naming the key. The refusal SHALL say that the set sets only the drive's entry and the hosts, console and kept repositories its flags give, that it moves aside only a file crew cannot read at all, and that the file and every drive it names are left as they are. A refused set SHALL write nothing, move nothing aside and make no state. A file at crew's own version SHALL never be moved aside.

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

#### Scenario: One wrong field beside another drive
- **WHEN** the teams file is at version 6 and names the drives `lab` and `pat`, `lab`'s `folder` is not absolute, and `crew drive set pat` runs
- **THEN** it is refused naming `lab`'s folder and saying the file and every drive it names are left as they are, nothing is written and no `teams.json.before-drive-set` is made

#### Scenario: A file that lists teams
- **WHEN** the teams file is `{"version":6,"teams":[]}` and `crew drive set pat` runs
- **THEN** it is refused naming `teams`, nothing is written and no `teams.json.before-drive-set` is made

#### Scenario: A part of another shape
- **WHEN** the teams file is at version 6 and its `hosts` is a list, and `crew drive set pat` runs
- **THEN** it is refused naming `hosts`, nothing is written and no `teams.json.before-drive-set` is made
