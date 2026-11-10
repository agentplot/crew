# drive-setup Specification

## Purpose
`crew drive set <label>` names a drive in this host's teams file from its flags, every key a flag with no default, and makes the drive's state as `crew state init` does, at Boomdrive's setup's asking on a host Nix does not configure.

## Requirements

### Requirement: Every key is a flag, with no default
`crew drive set <label>` SHALL take every key crew's module writes for a drive, for the hosts it needs, and for this host's console and kept repositories of it, as a flag named as the file names the key. A flag for a key crew requires, and `--hosts`, SHALL be required; `--roles`, `--console` and `--repositories` SHALL be optional. No flag SHALL have a default.

#### Scenario: A person's Mac
- **WHEN** `crew drive set pat` runs on `pats-mac` with `--state pat/crew-state`, `--blueprints pat/blueprints`, `--machine pats-mac`, `--session pat`, `--folder /Users/pat/.local/share/herdr/pat`, `--repos pat/blueprints`, the account `pat` for each role, every role's flume `false`, `--review 5 4`, `--hosts pats-mac pats-mac darwin`, `--console /Users/pat/.local/share/herdr/pat` and `--repositories pat/blueprints` with the runner's container and view
- **THEN** the teams file names the drive `pat` with those keys, `hosts` names `pats-mac`, `consoles` names `pat`, `repositories` names `pat/blueprints`, and crew loads the file

### Requirement: A flag crew does not accept is refused before anything is read
`--accounts` and `--flume` SHALL each be given once for each of the five main-level roles, `design`, `planner`, `reviewer`, `ops` and `operator`, and for no other. A flag left out, given more often than its count, or given a value crew does not accept for its key SHALL be refused naming the flag, before anything is read or written.

#### Scenario: A flag left out
- **WHEN** `crew drive set pat` is given every flag but `--folder`
- **THEN** it is refused naming `--folder`, and nothing is read or written

#### Scenario: An account left out
- **WHEN** `crew drive set pat` gives `--accounts` for `design`, `planner`, `ops` and `operator`, and none for `reviewer`
- **THEN** it is refused naming `--accounts` and the reviewer, and nothing is written

### Requirement: The flags agree before anything is read
`crew drive set` SHALL refuse, naming the flags, before anything is read or written, a first `--blueprints` that is not among `--repos`, a `--machine` that is not among `--hosts`, a `--repositories` address that is not among `--repos`, and `--repositories` where `--machine` is not the host the command runs on.

#### Scenario: A blueprints repo it does not keep
- **WHEN** `crew drive set pat` gives `--blueprints pat/blueprints` and `--repos pat/app`
- **THEN** it is refused naming `pat/blueprints` and `--repos`, and nothing is written

#### Scenario: Kept repositories of another host
- **WHEN** `crew drive set pat` runs on `pats-mac` with `--machine box-1` and `--repositories`
- **THEN** it is refused, saying `--repositories` names the kept repositories of the host it runs on, and nothing is written

### Requirement: The file is written as crew's module writes it
`crew drive set` SHALL write the teams file as JSON with every object's keys sorted, no space between tokens, no newline after it and no null in it, its drives a list in the order of their labels, so that for the same drives, hosts, consoles and kept repositories it holds the bytes crew's module writes. It SHALL write a new file and rename it over the old one.

#### Scenario: deneb's file
- **WHEN** the data of `nix/tests/files/deneb.json` or `nix/tests/files/runner.json` is written as `crew drive set` writes the teams file
- **THEN** the text is the pinned file's, byte for byte

### Requirement: The drive's facts are replaced and the rest of the file is kept
`crew drive set <label>` SHALL replace the drive's entry whole with the one its flags give, set each host `--hosts` names, and set the drive's console to `--console` or remove it where `--console` is not given. It SHALL keep every other drive, host, console and key of the file as the file holds it, and leave out a `consoles` it leaves empty.

#### Scenario: A second drive
- **WHEN** the teams file names the drive `pat` and `crew drive set lab` runs
- **THEN** the file names `lab` and `pat`, `pat`'s entry as it was

#### Scenario: A role's override no longer given
- **WHEN** the file's `pat` gives `roles.planner.effort` and `crew drive set pat` runs with no `--roles`
- **THEN** the file's `pat` has no `roles`

### Requirement: A kept repository stays while a drive of the host keeps it
`crew drive set` SHALL set each kept repository `--repositories` gives. A kept repository the file names SHALL stay only while another drive whose machine is this host lists it in its `repos`, and a `repositories` left empty SHALL be left out.

#### Scenario: A repository removed from the drive
- **WHEN** the file's `pat` lists `pat/app` in its `repos` with a kept repository for it, no other drive of the host lists `pat/app`, and `crew drive set pat` runs with `--repos pat/blueprints`
- **THEN** the file's `pat` lists only `pat/blueprints`, and `repositories` no longer names `pat/app`

#### Scenario: A repository another drive keeps
- **WHEN** `pat` and `lab` both run on this host and list `pat/app`, and `crew drive set pat` runs without it
- **THEN** `repositories` still names `pat/app`

### Requirement: The file it would write is checked before it is written
`crew drive set` SHALL check the file it would write as crew loads a teams file, and SHALL refuse a file crew would refuse, saying the file it would write is refused, giving crew's words for why, and writing nothing.

#### Scenario: Two accounts in one session
- **WHEN** `crew drive set pat` gives `--session pat` and no `--roles`, the planner the account `ia` and every other role `pat`
- **THEN** it is refused naming `pat`, the session `pat` and both accounts, and nothing is written

### Requirement: Run again with the same answers, it changes nothing
Where the drive's state is made and the drive's branch holds every entry this host's run record holds of the drive, `crew drive set` run with the flags that wrote the teams file SHALL write no byte of it, push no commit to the drive's branch and write no entry, and SHALL say the file names the drive as given and the branch exists.

#### Scenario: Set twice
- **WHEN** `crew drive set pat` runs a second time with the same flags after a first run that made `pat/main`
- **THEN** the teams file, the branch `pat/main` and the run record are as the first run left them, and it says `unchanged` and `exists`

### Requirement: Where Nix links the teams file, nothing is written there
Where `~/.config/crew/teams.json` is a link, `crew drive set` SHALL write nothing there and SHALL say so, naming the link's target and crew's module. Where the linked file names the drive with every fact the flags give, it SHALL make the drive's state. Otherwise it SHALL refuse, naming each key that differs or is missing and `services.crew.settings.drives.<label>`, with nothing made.

#### Scenario: The drive Nix already names
- **WHEN** the teams file is a link into the Nix store whose file names `pat` with every fact `crew drive set pat` gives
- **THEN** the link and its file are as they were, the command says the file is Nix's link, and `pat/main` is made

#### Scenario: A drive Nix does not name
- **WHEN** the teams file is a link into the Nix store whose file names no drive `pat`
- **THEN** `crew drive set pat` is refused naming `services.crew.settings.drives.pat`, and neither the file nor the branch is made

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

### Requirement: A drive's state is made as crew state init makes it
`crew drive set <label>` SHALL make `<label>/main` in the drive's state repository by the steps `crew state init <label>` takes, once the teams file names the drive, and SHALL leave a branch that exists as it is, finishing a step a stopped run left. Before it writes anything, it SHALL fetch the branch, and SHALL refuse a repository it cannot fetch from, naming it, with nothing written. An empty repository SHALL read as one with no such branch.

#### Scenario: An empty state repository
- **WHEN** `crew drive set pat` runs and `pat/crew-state` holds no commit
- **THEN** `pat/main` holds `plan.rec`, `moves.rec` and `proposals.rec`, as `crew state init pat` would make them

#### Scenario: A repository crew cannot reach
- **WHEN** `crew drive set pat` gives a `--state` crew cannot fetch from
- **THEN** it is refused naming the repository, and the teams file is as it was

### Requirement: crew drive set runs on the host it is invoked on
`crew drive set` SHALL write the teams file of the host it runs on and SHALL run no command on another host, whatever machine the drive names.

#### Scenario: Set on a person's Mac
- **WHEN** `crew drive set pat` runs on mac-studio
- **THEN** mac-studio's teams file names `pat`, and no ssh is run

### Requirement: Its answer is plain or JSON
`crew drive set` SHALL say one line for the teams file and one for the state, a moved file's line before them. With `--json`, it SHALL answer one JSON object naming the label, the teams file's outcome, `written`, `unchanged` or `linked`, with any path it moved a file to and the keys it changed, and the state's outcome, `made`, `finished` or `exists`, with its branch's tip. A refusal SHALL be crew's words on standard error, exiting non-zero.

#### Scenario: Setup reads the answer
- **WHEN** `crew drive set pat --json` names `pat` for the first time
- **THEN** it prints one JSON object whose `teams.outcome` is `written` and whose `state.outcome` is `made`

### Requirement: crew's agents start on the drive it set
A drive `crew drive set` named on a host that had no teams file SHALL be one crew's commands run for: `crew main up <label>` SHALL start its main level from the file it wrote.

#### Scenario: A person's first drive
- **WHEN** `crew drive set pat` runs on a host with no teams file and `crew main up pat` follows
- **THEN** pat's design agent, planner, ops and operator start in the session and folder its flags gave

### Requirement: A state not made is finished by the same command again
Where the teams file names the drive as given and `crew drive set` cannot make its state, it SHALL refuse saying so and that the same command again makes the state, and SHALL record a refused `state.init` on `plan/<label>`. The host SHALL keep the set's entry, and the run that makes the state SHALL push it before the state's own.

#### Scenario: A first push refused
- **WHEN** `crew drive set pat` writes the teams file and its push of `pat/main` is refused, and `crew drive set pat` then runs again with the same flags once a push is taken
- **THEN** the first run is refused saying the teams file names `pat` and that the same command again makes its state; the second writes no byte of the teams file and makes `pat/main`; and `pat/main`'s run record holds the first run's one `drive.set` entry, naming `drives.pat`, `hosts.mac-studio` and `consoles.pat`, and one refused `state.init` entry on `plan/pat`

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
