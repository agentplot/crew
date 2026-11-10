# Design

## Context

**What is asked.** agentplot/boomdrive record 0009's amendment of 2026-11-09 has a person whose Mac Nix does not manage install Boomdrive's programs with `nix profile add` and run setup, "one command, which an agent can run": "Each of its questions is also a flag, and it reports in JSON". "Run again with the same answers, it changes nothing." Setup makes the drive's state repository on GitHub where none exists, and leaves "crew's file names this drive and its state". Each tool's managed layer "is written for the person by the same keys Nix writes on a host it manages, so a host reads the same whichever wrote it", and "A file of the person's own already there is moved aside once and named, as the modules do." "On a host Nix manages, setup writes nothing Nix writes and says so." Its consequence: "crew is asked to make a new drive's state and name the drive in its own file at setup's asking, since crew alone knows its state's layout."

**What crew has.** Record 0064 (accepted 2026-11-09) has crew read every fact of a host's drives from its teams file alone, and names "crew's own command, at setup's asking, on a host Nix does not configure" as the file's writer there. `crew-runs-from-its-own-file-alone` built the reading and landed on this bolt at f564d22, and `code.5` as amended reads: crew "never writes it, save through its own command at setup's asking where Nix does not link it; no field has a default." `crew state init <label>` makes `<label>/main` with an empty plan, `moves.rec` and `proposals.rec`, but only for a drive the file names: it reads the drive through `crew.load`, and `record.reach` loads the file again to push each entry. crew's module writes the file as `builtins.toJSON` of its settings, keys sorted, no space, no newline, the drives a list in the order of their labels (`nix/modules/json.nix`, `flake.2`), and its activation links `~/.config/crew/teams.json` into the store, moving a file that is no link to `teams.json.before-nix` once (`nix/modules/activate.sh`).

**What the user settled for this change** (on the construct's question of 2026-11-09): this change makes the drive's state and its entry in crew's teams file only, crew running from its own file alone being `crew-runs-from-its-own-file-alone`, which comes first. "The drive's entry holds every fact crew then reads: its machine, its herdr session and folder, the Claude account each role runs under, and each host's kind and ssh name. Each is a flag of crew's command, with no default (code.5). The values a person's Mac takes, a session named for the drive, herdr's own folder for it and the login's own Claude account, are setup's to pass." And as the question put it: setup makes the GitHub repository where none exists; crew makes `<label>/main` on it with crew's starting files and writes the drive's entry into `~/.config/crew/teams.json` with the keys crew's module writes, each a flag of the command, with no default; it writes nothing where Nix links that file and says so; run again with the same answers, it changes nothing.

**Rules this design relies on:** `state.1`, `state.4`, `state.5`, `roles.2`, `roles.9`, `read.1`, `read.4`, `code.2`, `code.3`, `code.4`, `code.5`, `code.7`, `code.8`, `code.9`, `code.11` (core.md); `plan.1`, `plan.2`, `plan.22` (plan.md); `teams.9`, `teams.10` (teams.md); `flake.2` (flake.md); `briefs.10` (briefs.md); `tests.4`, `tests.6`, `tests.10`, `tests.11`, `tests.12` (tests.md); `docs.2`, `docs.4`, `docs.6`, `docs.7` (docs.md).

**Area pages this change touches:** `core.md`, `plan.md` (`plugin/lib/plan.py`), `teams.md` (`plugin/bin/crew`, `plugin/lib/crew.py`), `briefs.md` (`plugin/roles/operator.md`), `tests.md` and `docs.md`.

## Goals / Non-Goals

**Goals:**
- One crew command that names a drive in this host's teams file from its flags and makes the drive's state, which setup runs on a host Nix does not configure.
- Every key it writes is a key crew's module writes, given by a flag, with no default, and the file it writes is the module's bytes for the same settings.
- Run again with the same answers, it changes nothing; run with other answers, it changes only what they change.
- On a host whose teams file Nix links, it writes nothing there and says so.

**Non-Goals:**
- Making the GitHub repository: setup's (record 0009's amendment).
- Removing a drive from the file. Nothing asks for it yet; a person's later changes in the record are a repository added or removed, which `crew drive set` covers.
- Writing the runner's, Flume's or sluice's configuration, or herdr's plugins: setup's, through each tool.
- Starting the drive's main level or console: `crew main up` and `crew console up`, which the person or setup runs after.
- A change to crew's module or its pinned files: the keys are the ones it already writes.

## Decisions

### 1. One command, `crew drive set <label>`

`crew drive set <label>` sets the drive's entry in this host's teams file to what its flags give, and makes the drive's state where it has none. It is declarative, as setup is: the same flags give the same file and the same branch, and other flags change the entry to them.

Not taken:
- **`crew state init` with flags.** `state init` makes the state of a drive the file names, wherever the file came from, Nix's among them. Folding the file into it would give one command two jobs, one of them refused on every host Nix configures.
- **`crew drive new`.** "New" reads as a refusal when the drive exists, and setup runs the command again for a repository added or removed (record 0009's amendment: "Adding or removing a repository of the drive is a setup command").
- **Two commands, one for the file and one for the state.** Setup would order them itself, and a person at a shell could leave a drive named with no state.

### 2. Every key a flag, named as the file names it, with no default

The flags are the keys crew's module declares for a drive, for the hosts and for this host's consoles and kept repositories (`nix/modules/options.nix`, `flake.2`), each named as the file names it:

| Flag | File | Given |
|---|---|---|
| `<label>` | `drives[].label` | once, a name crew accepts (`code.4`) |
| `--state <owner/name>` | `state` | once |
| `--blueprints <owner/name>` | `blueprints` | once or more, in order, the first the drive's default |
| `--machine <host>` | `machine` | once |
| `--session <name>` | `session` | once |
| `--folder <path>` | `folder` | once, absolute |
| `--repos <owner/name>` | `repos` | once or more |
| `--accounts <role> <account>` | `accounts` | once for each of the five roles of `KIND_ROLES` |
| `--flume <role> false\|<stream>` | `flume` | once for each of the five roles |
| `--review <every> <hours>` | `review` | once |
| `--hosts <host> <ssh> <kind>` | `hosts` | once or more, the drive's machine among them |
| `--roles <role> model\|effort\|session <value>` | `roles` | optional, each role's key once |
| `--console <folder>` | `consoles[<label>]` | optional, absolute |
| `--repositories <owner/name> <dir> <checkout>` | `repositories` | optional, each address once |
| `--json` | | the answer as one JSON object |

A flag left out, given twice where once is its count, or given a value crew does not accept is refused naming the flag, before anything is read or written (`read.1`, `code.2`). So is the first `--blueprints` not among `--repos`, the drive's machine not among `--hosts`, an address of `--repositories` not among `--repos`, and `--repositories` where `--machine` is not this host, since `repositories` names the kept repositories of the host the file is written on. A value a repeated flag gives twice, a blueprints repo, a repository, a host, a role or a role's key, is refused the same way, and so is `--flume <role> true`, which reads as the JSON `true` the file refuses rather than a stream's name. A flag that takes several words takes them as separate arguments, since a path may hold any character a separator would be.

`--repos` is required with at least one address, since the drive's first blueprints repo is among them (the last check above). A drive whose machine keeps a repository through the runner gives it in `--repos` and in `--repositories`, as deneb's file does for every repository its runner keeps.

Not taken:
- **One `--accounts <account>` for all five roles.** It would be a default by another name. Setup passes the login's account five times.
- **`<key>=<value>` flags, or comma lists.** An address or a path can hold a `=` or a comma; separate arguments hold anything.
- **Leaving `roles` out.** It is a key the module writes. Leaving it out would make an entry with `roles` lose it on every run, or keep keys the flags did not give.

### 3. What the command owns in the file

The command reads the file's data, not the fleet `crew.load` makes of it, and changes only these:
- **The drive's entry**, replaced whole by the flags': any key of the old entry the flags do not give is gone. Other drives stay as the file holds them. The drives are written in the order of their labels.
- **`hosts`**: each host `--hosts` names is set to its `ssh` and `kind`. Every other host stays. None is removed, since another drive or `crew hold` may name it.
- **`consoles`**: the drive's console is set to `--console`, or removed where it is not given. Other drives' consoles stay. A `consoles` left empty is left out.
- **`repositories`**: each entry `--repositories` gives is set. An entry the file holds stays only while another drive whose machine is this host lists its address in its `repos`. A `repositories` left empty is left out.
- **`version`** is crew's own, `VERSION`. Every other key of the file stays as it is.

So a repository dropped from a drive's `--repos` leaves `repositories` with it, unless another drive of this host keeps it, and the runner's dropping of its clone does not leave crew naming a folder that has gone.

Not taken:
- **Merging the flags into the old entry.** A key a run no longer gives, a role override among them, would stay, and the same flags would give different files on two hosts.
- **`repositories` only ever added to.** A repository setup removes from the drive would stay named, its folder gone.
- **Removing a host no drive names.** `hosts` also serves `crew hold <host>` and an environment's host (record 0064).

### 4. The module's bytes

The file is written as `json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)`, with no newline after and nothing null in it, the drives a list in the order of their labels. That is what `json.nix` writes for the same settings, so a host reads the same whichever wrote it (record 0009's amendment, `flake.2`). A logic case reads `nix/tests/files/deneb.json` and `runner.json` and writes each again byte for byte, so a change to the module's rendering that this does not follow fails.

### 5. Checked as crew loads it, before it is written

`crew.load`'s checks become `crew.fleet_of(data, here)`, a function of the file's data and this host's name, which `load` calls with the data it reads (`code.7`). `load` reads `here` only when the file names `repositories`, as now. The command checks the file it would write with `fleet_of`, and refuses with nothing written, giving `fleet_of`'s words after "the teams file crew drive set would write is refused:" and ending "nothing was written". Its own flag checks (Decision 2) catch what a flag can break alone, so `fleet_of` refuses only what the flags break together with the file, such as two roles in one session under two accounts.

A file that is no JSON is refused by `load` naming the file and the parser's words, never a traceback (`code.2`), and so are a file that is no UTF-8, since `load` reads the file's bytes, and JSON that is no object. `fleet_of`'s `here` may be the function that reads this host, which it calls only where the file names kept repositories, so a file whose kept repositories are named wrongly is still refused before any process starts.

### 6. The order of its acts

1. The flags are checked (Decision 2).
2. `<label>/main` of `--state` is fetched into crew's cache. A repository crew cannot fetch from is refused naming it, with nothing written (`read.1`). An empty repository, as setup leaves a new one, has no such branch, which reads as none.
3. Under a lock on `~/.config/crew/`, the file is read, decided on (Decision 7) and written by a new file renamed over the old (`teams.9`), so two runs at once each keep the other's drive.
4. crew loads the file afresh (`crew.load`'s cache cleared).
5. The state is made by `crew state init`'s own steps (Decision 9).
6. Where the file changed a key, one `drive.set` entry is written (Decision 10).

The file comes before the state because `state init` and the run record read the drive from the file (`record.reach`). A step that fails leaves what came before it, and the same command run again finishes it: an unchanged file is left as it is, and `state init`'s steps each check whether the branch already shows them.

### 7. The file as it stands

`crew.teams_step` decides from plain facts: whether `~/.config/crew/teams.json` is a link and where it points, the file's text or none, whether `teams.json.before-drive-set` exists, the flags, the label and this host.
- **No file**: written new.
- **A file that loads** (`fleet_of`): the drive set in it (Decision 3). Where the text the command would write is the file's own, nothing is written and it says the file names the drive as given. Otherwise it is written.
- **A file that does not load**, for its JSON, its version or any check: moved once to `teams.json.before-drive-set`, and both paths named with the reason crew could not load it, then written new. The move is a hard link to the aside, which fails where the aside is taken, and the new file renamed over the old, so the host is never without a teams file between the two. Where `teams.json.before-drive-set` already exists, both are left and the command refuses, naming both, with nothing written, as crew's module's activation does (`read.4`).
- **A link**, as crew's module and the fleet's home-manager make it: nothing is written there (`read.4`). The command says the file is a link, naming its target, and that crew's module writes it. Where the linked file loads and names the drive with every fact the flags give, its hosts, console and kept repositories among them, the command goes on to make the state. Otherwise it refuses, naming each key that differs or is missing and `services.crew.settings.drives.<label>`, with nothing made.

Not taken:
- **Writing through the link, or replacing it with a file.** It would write into the store, or undo the host's own configuration until its next activation.
- **Refusing a file crew cannot load.** The record has a person's own file moved aside once and named. A file that loads is crew's to add to, so only a file that does not load is the person's own in that sense.
- **A link whose target is outside the Nix store treated as a file.** A link is someone's configuration, whatever writes it.

### 8. Run again, it changes nothing

The same flags on the file they wrote give the same text, so nothing is written. `state init`'s steps find the branch done and push nothing. No key changed, so no entry is written. The answer says each of these.

### 9. The state is `crew state init`'s

`state_init` returns what it did, the repository, the branch, its tip and its steps, and its caller says it, so `crew state init` says what it says today and `crew drive set` carries the same words. A new drive's blueprints repos hold no `plan/<label>`, so the branch starts with an empty plan, `moves.rec` with the first blueprints repo's moves (none where it has none), and `proposals.rec`. Every step is a write by `land` (`state.1`, `plan.1`, `plan.2`), pushed without force (`state.5`). A branch that exists stays as it is: a label names one drive and its one branch (`plan.22`), and setting it again never starts it again.

### 10. A set is recorded

A change to the drives runs on the user's word, and crew records who ran it (`roles.2`). Where the command changed a key of the file, it writes one `drive.set` entry on the drive's branch, after the state is made: `On` naming `drive/<label>`, and `Why` naming the keys it changed, `drives.<label>.<key>`, `hosts.<host>`, `consoles.<label>` and `repositories.<owner/name>`, each by its path and never its value (the run-record spec, "An entry holds no text anyone typed"). Its `By` and `Session` are who ran it, setup's run in the person's session read as the person. A rewrite that changes no key, such as a hand-written file's spacing, writes none.

crew refuses `crew drive set` to no caller (`roles.2`), and `may_write` is not asked, since it guards plan writes. A refusal is an entry where the file loads and names the drive, as any refused command's is; elsewhere it is said alone, there being no drive's record to hold it.

### 11. Run on the host it is invoked on

The command writes the teams file of the host it runs on and pushes the state to GitHub from there. It is never forwarded, though it names a main level's machine.

### 12. Its answer

Plain, one line for the file and one for the state, an aside's line before them. With `--json`, one object:

```json
{"label": "pat",
 "teams": {"file": "/Users/pat/.config/crew/teams.json", "outcome": "written", "aside": null,
           "changed": ["drives.pat", "hosts.pats-mac", "consoles.pat"]},
 "state": {"repository": "pat/crew-state", "branch": "pat/main", "tip": "<sha>", "outcome": "made",
           "did": ["started an empty plan", "added moves.rec with 0 moves of pat/blueprints"]}}
```

`teams.outcome` is `written`, `unchanged` or `linked`. `aside` is the path a file was moved to, else null. `changed` lists the keys changed, `drives.<label>` alone for a new drive. `state.outcome` is `made` where the branch was absent, `finished` where it stood and a step was done, `exists` where nothing was. A refusal is crew's words on standard error with exit 1, as every command's (`code.2`). The JSON is built by a function of what was done (`code.7`).

### 13. The file's writer, as every refusal names it

`WRITER` becomes "crew's own module, services.crew, crew drive set, or the machine's configuration that writes it", so a refusal on a person's Mac names the fix there. A host with no teams file is refused naming the same writers, where today it names the machine's configuration alone.

### 14. The operator's brief

The operator's *Changing the drives* has the operator change a drive in swancloud's `lib/crew-teams.nix`, which no person's Mac keeps. It gains its first words for the case: where the host's `~/.config/crew/teams.json` is a file and not a link into the Nix store, as Boomdrive's setup leaves a person's Mac, a drive is added, changed or removed through Boomdrive's setup on the user's word, which gives crew the drive's entry with `crew drive set` and the runner the same repositories. The operator tells the user so, and never edits the teams file by hand. The swancloud steps stand for a link. The words name a fact the agent reads with `test -L`, so no token is added (`teams.10`). `t-briefs` pins the phrase (`tests.6`).

### 15. No record and no rule is written here

The rules and records are the design agent's (`docs.7`). `code.5` already lets crew's command write the file. Once this lands, the design agent may write the record of this design's own choices, Decisions 1 to 3, 7 and 10, each cheap to change before setup calls the command, and add `crew drive set` to `code.5`'s words for the command.

### Departures

- `code.3` has every bash command about a main level forward to the host the teams file names. `crew drive set` runs where it is invoked (Decision 11), because it writes that host's own file, as `crew signal` runs where it is invoked (`signals.2`).
- `openspec/config.yaml` asks that the last task run `tests/suite --affected`. This change's stage brief asks that no task run the repository's whole checks, which `--affected` is for any change to crew's command core (CLAUDE.md, *Tests*). So the verify stage runs them once, after the last task.

## Risks / Trade-offs

- [A file a newer crew wrote, at a version this crew does not read, is moved aside] → It is named, with the reason, and the aside is never overwritten. On a host Nix does not configure, one crew is installed (`nix profile add`).
- [The file is written and the state push then fails, for credentials or the network] → The file names a drive with no branch, and crew's commands for it refuse naming `crew state init <label>`. Running `crew drive set` again with the same flags finishes it, the file unchanged.
- [Setup gives a `--repositories` path the runner later moves] → crew names a folder that is gone until setup runs the command again. The runner's report, where it names the kit's folder, is read first, as today (record 0061).
- [The same label set on two hosts with different flags] → Each host's file is its own, as with the module. The state branch is shared, made once, and never started again.

## Migration Plan

None. No host's file changes until the command is run there.

## After deploy

None: every scenario is proved by a check in crew's tiers. Setup's call of the command is Boomdrive's change.

## Task notes

**1.1** `plugin/lib/crew.py`: split `load` into `read_teams(text)`, the file's data or a refusal naming `TEAMS` and the JSON parser's words, and `fleet_of(data, here)`, every check `load` makes today, returning the same fleet, with `here` used where `repositories` needs this host. `load` reads the file, calls `read_teams`, reads `this_host()` only when the data names `repositories`, and calls `fleet_of`; it stays cached per process. `WRITER` gains `crew drive set` (Decision 13), and the missing file's refusal names `WRITER`. Update `load`'s and the module header's docstrings, which say the command never writes the file. `tests/py/test_teams.py`: the writer's words wherever a case pins them; a missing file refused naming the four writers; a file that is no JSON refused naming the file, with no traceback; `fleet_of` called with plain data answering as `load` does on the same file.

**1.2** `tests/t-teams.sh`: its `has "$out" "crew's own module, services.crew, or the machine's configuration that writes it"` lines take the new words, and one case runs `crew bolts` with no teams file and finds the refusal naming `crew drive set`.

**2.1** `crew.drive_given(a)`: from the parsed flags (an `argparse.Namespace`), `{"drive": <entry>, "hosts": {<host>: {"ssh", "kind"}}, "console": <folder or None>, "repositories": {<address>: {"dir", "checkout"}}}`, or a `Refusal` naming the flag, by Decision 2. The entry holds `label`, `blueprints`, `state`, `machine`, `session`, `folder`, `repos`, `accounts`, `flume` (`False` for `false`), `review` (`every` an int; `hours` an int where it is a whole number, else a float) and `roles` only where `--roles` is given. Every value is checked as `fleet_of` would check its key, reusing `NAME`, `ADDRESS`, `HOST_KINDS`, `KIND_ROLES`, `MAIN_ROLES` and `EFFORTS`. `here`, this host, is a parameter for the `--repositories` check. New `tests/py/test_drive_set.py`: a person's Mac's flags (drive `pat` on `pats-mac`, `pat/crew-state`, `pat/blueprints`, session `pat`, folder `/Users/pat/.local/share/herdr/pat`, every account `pat`, every role standing, review 5 and 4, `pats-mac` with ssh `pats-mac` and kind `darwin`, console the folder, `pat/blueprints` kept at the runner's container and view); each required flag left out; an account or a flume role left out, named twice or unknown; a flume setting that is no stream's name; a review of 0; a kind of `macos`; a relative folder or console; a first blueprints repo not among `--repos`; a machine not among `--hosts`; a kept address not among `--repos`; `--repositories` for another machine. Each refusal names its flag. Build the namespace with plan.py's own parser, `plan.parser().parse_args(["drive", "set", ...])`, so the cases read the flags as the command does.

**2.2** `crew.teams_set(data, given, here)`: the file's data, or `None` for no file, with the drive set by Decision 3, and the changed keys' paths (Decision 10); and `crew.teams_text(data)` by Decision 4. Cases: a new file from no file; a second drive added, the first kept byte for byte; the drive's entry replaced whole, a `roles` the flags no longer give gone; a host added and one replaced, another kept; a console set and one removed, `consoles` left out when empty; a repository dropped from `--repos` leaving `repositories` while no other drive of this host lists it, and staying while one does; a given kept repository replacing the file's; an unknown top-level key kept; the drives in label order; `teams_text(json.loads(text)) == text` for `nix/tests/files/deneb.json` and `runner.json`, read as bytes.

**2.3** `crew.teams_step(facts)`: the step of Decision 7 from plain facts (`linked`, `target`, `text`, `aside_taken`, `given`, `here`), one of write (the text and changed keys), unchanged, aside then write (the reason), linked as given, or a refusal. It calls `fleet_of` on the file's data and on the result (Decision 5). Cases: no file; the file the same flags wrote, unchanged; a version-5 file, a file that is no JSON and a version-6 file failing a check, each moved aside with its reason; the aside taken, refused naming both paths; a link whose file names the drive as given; a link whose file lacks the drive, and one giving it another `repos` and no console, each refused naming the keys and `services.crew.settings.drives.pat`; two roles in one session under two accounts, refused with `fleet_of`'s words after "the teams file crew drive set would write is refused:" and naming nothing written.

**2.4** `crew.drive_said(done, json)`: the answer of Decision 12, plain or JSON, from what was done. Cases: the plain lines and the JSON object for a new drive; for a run again, `unchanged` and `exists`; for a link, `linked`; an aside named.

**3.1** `plugin/lib/plan.py`: the parser's `drive` command with `set` and its flags (Decision 2), each multi-word flag `nargs` of its count and `action="append"` where it repeats. `main` runs `("drive", "set")` before `crew.load()`, and asks no `may_write`. `drive_set(a)` makes the acts of Decision 6 thinly around the decisions of 2.1 to 2.4: the lock (`fcntl.flock` on `~/.config/crew/.teams.lock`, the folder made where missing), the reads, the rename aside, the write of `teams.json.<pid>.new` renamed over `teams.json`, `crew.load.cache_clear()`, `state_init`, the entry (`record.emit(label, "drive.set", [f"drive/{label}"], why=...)`) and the answer. Its refusal is recorded by Decision 10. `state_init` returns its repository, branch, tip, outcome and steps, and `crew state init`'s caller prints them as it does today. Add `("drive", "set"): "drive.set"` to `ACTS` and the command to `HOST_COMMANDS` where its steps print as they go. `plugin/bin/crew`: `drive` in the dispatch to plan.py and in the help case, and the usage header's line (5.1). New `tests/t-drive-set.sh`, `# Reads: plugin/hooks/`, proving the command's wiring and one case beyond it (`tests.12`), on mac-studio with its teams file removed as setup finds a person's Mac, `world` building the rest. Its wiring: with `--state` naming a remote that does not exist, `crew drive set pat ...` is refused naming it and no teams file is made (the read before the write); with `state_repo pat/crew-state`, an empty bare remote, and `blueprints pat/blueprints` cloned at `<folder>/blueprints/main`, it writes the file, which `crewpy labels` reads, makes `pat/main` holding `plan.rec`, `moves.rec` and `proposals.rec`, and writes one `drive.set` entry naming `drives.pat`, `hosts.mac-studio` and `consoles.pat`, no ssh in the stub log; and `crew main up pat` then starts pat's design agent, planner, ops and operator, as `t-journey-main` brings wldn's up. Its one case beyond: the same command again leaves the file's bytes, the branch's commit count and the run record as they were, and says `unchanged` and `exists`. Then `tests/moon-tasks`, and commit `tests/moon.yml`.

**3.2** `tests/t-journey-state.sh` passes as it stands: `crew state init` says what it said.

**3.3** `tests/t-help.sh`: the commands list gains `drive set pat`.

**3.4** `tests/py/test_parser.py`'s `RUNS` gains a `drive set pat` run giving every flag once, `--roles`, `--console` and `--repositories` among them; `tests/py/test_help.py`'s runs gain `drive set pat --help`.

**4.1** `plugin/roles/operator.md`, *Changing the drives*: its first words by Decision 14, the swancloud steps then said for a teams file that is a link into the Nix store. `tests/t-briefs.sh` pins the phrase in the operator's brief.

**5.1** `README.md`'s *State*: `crew drive set <label>` and its flags in the command block, and a paragraph on what it writes, keeps, moves aside and leaves where Nix links the file, and that it makes the state as `crew state init` does. `plugin/skills/crew/SKILL.md`: a table row beside `crew state init`'s. `plugin/bin/crew`'s usage header: the command's lines beside `crew state init`'s. `plugin/lib/plan.py`'s header usage likewise. `openspec/config.yaml`'s context: "The crew command never edits it" becomes that the crew command writes it only through `crew drive set`, where Nix does not link it. `docs.2`: README, the skill and the usage say the same.
