# Design

## Context

**What is asked.** Record 0065 (accepted 2026-11-09 by agentplot-design, on `bolt/crew-names-each-drive-once`) settles `crew drive set`. Its points 6 and 7 are agentplot-design's rulings on batch 25's review of `crew-makes-a-new-drives-state`, and name this change as their build:

- Point 6: "A file is moved aside only where crew cannot read it at all. A teams file that is not JSON, not an object, or at a version this crew does not read is the person's own in record 0009's sense. It is moved aside once to `teams.json.before-drive-set`, both paths named, as the modules move a file aside. A file at crew's own version that fails a check is crew's own file, written by this command or the module. It is refused, naming the check, with nothing written. Moving it aside would drop every other drive of the host from the live file for one wrong field."
- Point 7: "No set goes unrecorded. When a run's file write lands but its state push fails, the run that finishes the state records the set the drive's branch has no entry for. So the branch always says who named the drive, however many runs it took."

`code.5`'s details already rule out "`crew drive set` … moving aside a file at crew's own version (record 0065)", and allow "moving aside once a file crew cannot read at all".

**What crew does now.** `crew.teams_step` (`plugin/lib/crew.py`) reads the file with `read_teams` and checks it with `fleet_of`, and takes any refusal of either as a file to move aside. `plan.drive_set` (`plugin/lib/plan.py`) writes the file under its lock, makes the state with `state_init`, and only then, where its own step changed a key, emits one `drive.set` entry. A refusal anywhere is recorded by `drive_set_refused` as a refused `drive.set`, where the file loads and names the drive. So a run whose state push fails leaves the file naming the drive, a refused `drive.set` kept on the host, and no entry naming what was set; the run again finds the file unchanged, so it emits nothing.

**What the run record already does.** `record.emit` appends an entry to the host's own file and then pushes every entry of the drive the branch lacks, oldest first (`record.reach`). A push that is refused, or a branch that does not exist yet, keeps the entry in the host's file, said once on standard error, and the host's next push takes it first (`record.2`; the run-record spec, "An entry that did not reach the branch goes with the host's next"). `state_init`'s every step emits a `state.init` entry, so the state's first write is also a push of every entry the host kept.

**How the family does it.** crew's module moves every teams file that is no link aside to `teams.json.before-nix` (`nix/modules/activate.sh`), and agentplot/boomdrive record 0009's amendment has setup move "a file of the person's own" aside "as the modules do". The two agree once each is read by what its writer keeps. The module replaces the file whole with the machine's configuration, so to it every file there is the person's own. `crew drive set` keeps every other drive of a file it can read, so only a file it cannot read at all is the person's own to it. One rule covers both: a writer moves a file aside only where it cannot keep what the file holds. Nothing changes in the module or in Boomdrive.

**Rules this design relies on:** `state.1`, `state.4`, `roles.2`, `read.1`, `read.4`, `read.5`, `code.2`, `code.5`, `code.7`, `code.8` (core.md); `plan.1`, `plan.2` (plan.md); `teams.9` (teams.md); `record.1`, `record.2`, `record.3`, `record.4` (record.md); `tests.3`, `tests.4`, `tests.11`, `tests.12` (tests.md); `docs.2`, `docs.4`, `docs.6`, `docs.7` (docs.md).

**Area pages this change touches:** `core.md`, `plan.md` (`plugin/lib/plan.py`), `teams.md` (`plugin/lib/crew.py`, `plugin/bin/crew`), `record.md` (`plugin/lib/record.py`), `tests.md` and `docs.md`.

## Goals / Non-Goals

**Goals:**
- No run of `crew drive set` drops a drive from the live teams file of a host that crew can read.
- Every set that changed the file is recorded on the drive's branch, in the name of whoever ran it, however many runs its state took.
- A run that could not make the state says the file names the drive and how to finish.

**Non-Goals:**
- Mending a version-6 file that fails a check. Record 0065 has it refused with nothing written, and nothing of `crew drive set` writes one (Risks).
- Any change to the checks `fleet_of` makes, or their words.
- Any change to a link's handling, the aside's path, or the answer's lines and JSON.
- A record entry of a new kind, or a field the run record's descriptor lacks.

## Decisions

### 1. What crew cannot read at all

`crew.readable(text)` gives the data of a teams file's text or bytes where crew can read it at all, and otherwise refuses naming why:
- no JSON or no UTF-8: `read_teams`'s words;
- JSON that is no object: `fleet_of`'s words for it today;
- a version this crew does not read, a missing one among them (`version` absent, not an integer, or not `VERSION`): `fleet_of`'s words for it today.

`crew.known(data)` makes the last two checks and returns the data. `fleet_of` calls it first, so every refusal keeps one text. `readable` is `known(read_teams(text))`, and `load` reads the file through it. A version-6 file that lists `teams`, lists no drives, or fails any later check is one crew can read. It is crew's own file, and `fleet_of` refuses it as before.

Not taken:
- **A file whose `version` is missing read as crew's own.** Nothing of crew's writes a file without one, and a hand's file without one is the person's own.
- **A version-6 file listing `teams` read as unreadable.** Version 6 never held teams, so such a file was edited at crew's own version and is refused, as point 6 has every check of crew's own version.

### 2. A version-6 file that fails a check is refused

`teams_step` moves a file aside only where `readable` refuses it, with the aside's taken refusal as now. Where `readable` gives the data and `fleet_of` refuses it, the step refuses:

> `<teams file>` is at crew's version 6 and fails a check: `<fleet_of's words>` crew drive set moves aside only a file crew cannot read at all, so the file and every drive it names are left as they are, and nothing was written

The step runs under the lock before anything is written (`teams.9`), so nothing is written, nothing is linked aside, and `drive_set` makes no state. The fetch of `<label>/main` before the step reads only. The refusal is said alone and recorded nowhere: the file does not load, so no drive's record can hold it, as the design of `crew-makes-a-new-drives-state` has every refusal of a file that does not load (its Decision 10).

Not taken: **setting the drive into such a file where the file it would write passes.** That would mend a file whose only fault is the drive being set, but point 6 has the file "refused, naming the check, with nothing written", and `code.5` rules the same. The choice is cheap to change later, and is the design agent's to make.

### 3. The set's entry is written once the file is

Where the teams step wrote the file and changed a key, `drive_set` appends the `drive.set` entry to this host's run record at once, after the file is renamed into place and before the state is made. The entry is the same as before: `On` naming `drive/<label>`, and `Why` naming each changed key by its path. It is appended without a push of its own (`record.emit(..., push=False)`), since for a new drive no branch exists yet to take it. The same command pushes it:
- where the branch is new, with the state's first write, whose `state.init` entry pushes every entry the branch lacks, oldest first;
- where the branch stands, by the command's last act (Decision 5).

So for a new drive the branch holds the set before the state's first entry, and reads in the order the acts were done. The entry is written after its act, the file write (`record.1`), and holds names alone (`record.3`).

Not taken:
- **A marker file of sets not yet recorded, beside the teams file.** It would be a second record of the same fact, which the run record already keeps and carries (`record.2`, `state.4`).
- **The finishing run writing an entry of its own for a set the branch has no entry for.** It could not tell which keys the earlier run changed, since entries hold paths and never values, nor who ran it. The kept entry names both.
- **Emitting with its push where the branch is new.** Every first set of a drive would then say on standard error that its entry did not reach a branch, before the state made it.

### 4. A refusal once the file names the drive is the state's

Once the teams step is done, whether the file was written, unchanged or Nix's link naming the drive as given, what is left is the state. A refusal from then on is the state's:
- `drive_set` gives it in `crew.state_unmade(label, words)`'s words: `<teams file> names drive <label> as given, and its state was not made: <words>. crew drive set <label> run again with the same flags makes it.`
- `drive_set_refused` records it as a refused `state.init` on `plan/<label>`, the act and object `crew state init`'s steps record, not as a refused `drive.set`. The set was done and has its entry. One entry per act, done or refused (`record.1`).

The refusal's entry is emitted with its push, as any refused command's. Where the branch takes it, it carries the set's entry first. Where it does not, both stay in the host's file, said once (`record.2`).

A refusal before the teams step is done, of a flag, of the fetch or of the step itself, stays a refused `drive.set` where the file loads and names the drive, as now.

### 5. The command ends by pushing what the branch lacks

`drive_set`'s last act, once the state is made, pushes every entry of this host's record of the drive that the branch lacks (`record.reach(label, eid, said=True)`). A refused push is said once on standard error and changes nothing of the command's answer or exit (`record.2`). Where the branch already holds every entry, nothing is pushed and no commit is made, so a run again on a finished drive changes nothing.

This covers the cases the state's own writes do not: a changed drive whose branch stands, where `state_init` writes nothing; and a set kept on this host while another host made the drive's state.

`reach` gains `said`. With no entry just written, a refused push is said like a kept entry's and returns, rather than being the command's refusal, which stays the case for `crew events --push`.

### 6. Run again, it finishes what a run left

A run whose state push was refused leaves:
- the teams file naming the drive;
- in the host's record, the set's `drive.set` entry and the refused `state.init`;
- the branch absent, or short of the state's later steps.

The same command run again finds the file unchanged and appends no `drive.set` of its own, since it changed no key. It makes or finishes the state by `state_init`'s steps. The first of those writes pushes the kept entries, oldest first, then its own. The branch then says who named the drive, when, and that the first run's state was refused. However many runs it takes, only the run that changed the file records the set, and it is recorded once.

## Departures

- `read.5` has every entry reach the branch "as it is written". The set's entry reaches it later in the same command, with the state's first write or the command's last push, because for a new drive there is no branch to take it sooner. It still reaches the branch before the command returns whenever the state is made. The run-record spec's "the same command SHALL push it" holds.
- `openspec/config.yaml` asks that the last task run `tests/suite --affected`. This change's stage brief asks that no task run the repository's whole checks, which `--affected` is for any change to crew's command core (CLAUDE.md, *Tests*). So the verify stage runs them once, after the last task.

## Risks / Trade-offs

- [A version-6 file that fails a check stays refused, by `crew drive set` and by every crew command, until its writer mends it] → `crew drive set` and crew's module write only a file that passes `fleet_of`, so such a file comes from a hand, or from a crew whose checks were tightened. The refusal gives the check's words, which name the drive and the key. That leaves one more refusal to read, but loses no drive, where the aside dropped every drive the host had.
- [The process ends between the file's rename and the entry's append] → The set is not recorded, as before this change. The window is one local append. Nothing pushes or waits in it.
- [A host's run record is lost before a kept entry is pushed] → The set's entry is lost with every other kept entry of that host (`record.4`). That is no worse than any command's kept entry.
- [A set kept on a host that then never runs a command of the drive] → Its entry stays in the host's file, as any kept entry does (`record.2`). The person's next `crew drive set`, or any command of the drive on that host, pushes it.

## Migration Plan

None. A host's file and record change only when the command runs there.

## After deploy

None: every scenario is proved by a check in crew's tiers.

## Task notes

**1.1** `plugin/lib/crew.py`: add `known(data)`, which makes `fleet_of`'s object and version checks with their words today, taken out of `fleet_of`, and returns the data. `fleet_of` calls it first. Add `readable(text)`, which is `known(read_teams(text))`. `load` returns `fleet_of(readable(TEAMS.read_bytes()), this_host)`, so its words and its fleet are as they were. Update `load`'s and `fleet_of`'s docstrings. `tests/py/test_teams.py`: `readable` refuses, in the words `load` gives for the same file, text that is no JSON, bytes that are no UTF-8, `[]`, `{}` (version `null`), `{"version":"6"}`, `{"version":true}` and `{"version":5}`; it gives the data of `{"version":6,"drives":[],"hosts":{}}` and of `{"version":6,"teams":[]}`, which `fleet_of` then refuses; and the cases that pin `load`'s words pass unchanged.

**1.2** `crew.teams_step` (Decision 2): the aside path is taken only where `readable` refuses. Where `fleet_of` refuses data that `readable` gave, the step refuses with Decision 2's words, whether or not the aside is taken. The link path is unchanged. Update the docstring. `tests/py/test_drive_set.py`, `TestTeamsStep`:
- The parametrized aside case drops `{"version":6,"drives":[],"hosts":{}}` and gains `{}` (`is version null`) and bytes that are no UTF-8.
- New case: a version-6 file naming `lab` and `pat`, `lab`'s `folder` relative, is refused for `crew drive set pat`, naming `drive lab` and its folder, "moves aside only a file crew cannot read at all" and "nothing was written". With the aside taken, it is refused the same way and not as an aside taken.
- New case: a version-6 file that lists no drives, and one that lists `teams`, are each refused, not moved aside.

**2.1** `plugin/lib/record.py`: `emit(..., push=True)`. With `push` false the entry is appended as now, `reach` is not called, and its id is returned. `reach(label, eid=None, said=False)`: with `said` and no `eid`, a refused push is said once on standard error, naming the branch and that the host keeps what it holds and pushes it with its next entry, and returns None; with neither, the refusal is the command's, as `crew events --push` has it. Update the module's docstring where it says each entry is pushed by the command that appended it, "before it goes on". `tests/py/test_record.py`: an entry emitted with `push=False` is in the host's file and nothing is pushed (the `pushed` fixture); a `reach` with `said` whose fetch is refused says so once on standard error and returns None, raising nothing.

**2.2** `crew.state_unmade(label, words)`: Decision 4's words, with one period between the refusal's words and the next sentence whether or not they end with one. `tests/py/test_drive_set.py`: a new case gives the words for a refused push's words, `the push of pat/main to pat/crew-state failed: refused for the test`, naming the teams file, `drive pat as given`, the words, and `crew drive set pat run again with the same flags makes it`.

**2.3** `plugin/lib/plan.py`, `drive_set`:
- Once the teams step is done, clear `crew.load`'s cache and mark `CONTEXT["teams_done"] = True`. Where the step wrote the file and changed a key, append the set's entry: `eid = record.emit(label, "drive.set", [f"drive/{label}"], why="set " + ", ".join(changed), push=False)`.
- Run `state_init`. A refusal it raises is raised again in `crew.state_unmade(label, str(e))`'s words.
- Then `record.reach(label, eid, said=True)`, then the answer.
- Remove the `drive.set` emit after the state.

`drive_set_refused`: where `CONTEXT.get("teams_done")`, record the refusal as `record.emit(label, "state.init", [f"plan/{label}"], refused=<its words>)`; otherwise as now. Update both docstrings and the header of `drive_set`.

`tests/t-drive-set.sh`, its wiring after the unreachable repository's case:
- `state_repo pat/crew-state` with a `pre-receive` hook in its bare remote that refuses every push.
- `set_pat pat/crew-state` fails, naming `names drive pat as given, and its state was not made` and `crew drive set pat run again with the same flags makes it`.
- `crewpy labels` reads `pat`, the remote has no `pat/main`, and the host's own record of pat holds one `drive.set` entry and one refused `state.init` on `plan/pat`.
- With the hook removed, `set_pat pat/crew-state` passes, saying the file names drive pat as given and nothing was written, and `started an empty plan`.
- `pat/main` holds `plan.rec`, `moves.rec` and `proposals.rec`. Its run record holds one `drive.set` entry, whose `Id` is the first run's, on `drive/pat`, its `Why` `set drives.pat, hosts.mac-studio, consoles.pat`, and one `state.init` entry with `Refused`.
- No ssh in the stub log.

The rest stands: `crew main up pat`, then the run again that changes nothing, its one case beyond the wiring (`tests.12`). Update the opening comment. Its inputs do not change, so `tests/moon.yml` stays.

**3.1** README's *State*, its `crew drive set` paragraph:
- Where it says a file crew cannot load is moved aside, it says that a file crew cannot read at all, no JSON, no object, or at a version this crew does not read, is moved aside once. It adds that a file at crew's own version that fails a check is refused in crew's words with nothing written, since moving it would drop every other drive of the host.
- Where it says one `drive.set` entry names the keys, it adds that the entry is written once the file is and pushed with the state. Where the state is not made, the refusal says the file names the drive and is recorded as a refused `state.init`, and the same command run again makes the state and pushes the set's entry first.

`plugin/skills/crew/SKILL.md`: "moves a file crew cannot load aside once" says a file crew cannot read at all, and that one at its own version that fails a check is refused. The usage headers of `plugin/bin/crew` and `plugin/lib/plan.py` say the same in their `crew drive set` lines (`docs.2`).
