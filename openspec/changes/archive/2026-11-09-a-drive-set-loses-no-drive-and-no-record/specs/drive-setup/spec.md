## RENAMED Requirements

- FROM: `### Requirement: A teams file crew cannot load is moved aside once`
- TO: `### Requirement: A teams file crew cannot read at all is moved aside once`

## MODIFIED Requirements

### Requirement: A teams file crew cannot read at all is moved aside once
Where `~/.config/crew/teams.json` is a file crew cannot read at all, `crew drive set` SHALL move it to `teams.json.before-drive-set` beside it, name both paths and why crew cannot read it, and write the file new. A file crew cannot read at all SHALL be one that is no JSON or no UTF-8, holds no JSON object, or gives a version this crew does not read, a missing version among them. Where `teams.json.before-drive-set` already exists, it SHALL leave both, refuse naming both, and write nothing.

#### Scenario: A file at version 5
- **WHEN** the teams file is at version 5 and `crew drive set pat` runs
- **THEN** that file is at `teams.json.before-drive-set`, the command names both paths and its version, and the teams file names `pat`

#### Scenario: A file that is no JSON
- **WHEN** the teams file holds text that is no JSON and `crew drive set pat` runs
- **THEN** that file is moved aside, named with the JSON parser's words, and the teams file names `pat`

#### Scenario: An aside already taken
- **WHEN** the teams file is at version 5 and `teams.json.before-drive-set` exists
- **THEN** `crew drive set pat` is refused naming both paths, and both files are as they were

### Requirement: Run again with the same answers, it changes nothing
Where the drive's state is made and the drive's branch holds every entry this host's run record holds of the drive, `crew drive set` run with the flags that wrote the teams file SHALL write no byte of it, push no commit to the drive's branch and write no entry, and SHALL say the file names the drive as given and the branch exists.

#### Scenario: Set twice
- **WHEN** `crew drive set pat` runs a second time with the same flags after a first run that made `pat/main`
- **THEN** the teams file, the branch `pat/main` and the run record are as the first run left them, and it says `unchanged` and `exists`

### Requirement: A set is one entry naming what it changed
Where `crew drive set` changes a key of the teams file, it SHALL append one `drive.set` entry to this host's run record once the file is written and before the drive's state is made, naming `drive/<label>`, the path of each key it changed and never its value, and who ran it. The same command SHALL push the entry to the drive's branch: with the state's first write where the branch is new, or, where the branch stands, by its last act, which pushes every entry of this host's record of the drive that the branch lacks. A run that changes no key SHALL append none. crew SHALL refuse `crew drive set` to no caller.

#### Scenario: A new drive
- **WHEN** `crew drive set pat` names `pat` in the teams file for the first time
- **THEN** `pat/main`'s run record holds one `drive.set` entry on `drive/pat`, naming `drives.pat`, `hosts.pats-mac` and `consoles.pat` and no folder, account or address it was given

## ADDED Requirements

### Requirement: A teams file at crew's own version that fails a check is refused
Where `~/.config/crew/teams.json` is a file at crew's own version that fails any check crew makes when it loads a teams file, `crew drive set` SHALL refuse, giving crew's words for the check, saying that it moves aside only a file crew cannot read at all and that the file and every drive it names are left as they are. It SHALL write nothing, move nothing aside and make no state.

#### Scenario: One wrong field beside another drive
- **WHEN** the teams file is at version 6 and names the drives `lab` and `pat`, `lab`'s `folder` is not absolute, and `crew drive set pat` runs
- **THEN** it is refused naming `lab`'s folder, and the teams file still names `lab` and `pat` and no `teams.json.before-drive-set` is made

### Requirement: A state not made is finished by the same command again
Where the teams file names the drive as given and `crew drive set` cannot make its state, it SHALL refuse saying so and that the same command again makes the state, and SHALL record a refused `state.init` on `plan/<label>`. The host SHALL keep the set's entry, and the run that makes the state SHALL push it before the state's own.

#### Scenario: A first push refused
- **WHEN** `crew drive set pat` writes the teams file and its push of `pat/main` is refused, and `crew drive set pat` then runs again with the same flags once a push is taken
- **THEN** the first run is refused saying the teams file names `pat` and that the same command again makes its state; the second writes no byte of the teams file and makes `pat/main`; and `pat/main`'s run record holds the first run's one `drive.set` entry, naming `drives.pat`, `hosts.mac-studio` and `consoles.pat`, and one refused `state.init` entry on `plan/pat`
