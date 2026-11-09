---
status: accepted
date: 2026-11-09
decision-makers: agentplot-design; the construct of `crew-makes-a-new-drives-state`
---

# 0065. `crew drive set` names a drive in crew's own file and makes its state, from flags alone

Status: accepted on 2026-11-09 by agentplot-design. Each choice here is cheap to change before Boomdrive's setup calls the command, and is made on the rules and records written (`briefs.15`). Points 1 to 5 are the construct's, as its design gives them. Points 6 and 7 are agentplot-design's, on the batch review's open points.

Deciders: the construct of `crew-makes-a-new-drives-state`, its design's Decisions 1 to 3, 7 and 10 (archived 2026-11-09 on `bolt/crew-names-each-drive-once`, 5342e96b); agentplot-design, on batch 25's review of that change. The user's choice they carry is agentplot/boomdrive record 0009's amendment of 2026-11-09: "One command, which an agent can run", "Run again with the same answers, it changes nothing", "A file of the person's own already there is moved aside once and named, as the modules do", and its consequence, "crew is asked to make a new drive's state and name the drive in its own file at setup's asking".

Sources: agentplot/boomdrive record 0009, amendment of 2026-11-09; record 0064; rules `code.3`, `code.5`, `roles.2`, `read.4`, `flake.2`; the change `crew-makes-a-new-drives-state`, archived on `bolt/crew-names-each-drive-once`, and its batch review (batch 25).

## Context and problem statement

On a Mac that Nix does not manage, Boomdrive's setup has to name a person's drive in crew's teams file and make the drive's state branch, so the person can run `crew main up`. crew reads every fact of a host's drives from that file alone (record 0064), and the file has to be the same whoever writes it, crew's module or setup. So crew needs a command that writes the file, that an agent can run with flags and run again safely, and that never writes over a file Nix manages.

## Decision outcome

1. **One declarative command, `crew drive set <label>`.** It sets the drive's entry to what its flags give and makes the drive's state where there is none. Run again with the same flags, it changes nothing. Run with other flags, it changes only what they change. Not taken:
   - flags on `crew state init`, which would give one command two jobs, one of them refused wherever Nix writes the file;
   - `crew drive new`, which reads as a refusal when setup runs it again for a repository added or removed;
   - two commands, one for the file and one for the state, which would let a person at a shell name a drive with no state.
2. **Every key is a flag, named as the file names it, with no default (`code.5`).** Each role's account and Flume setting is given once for each of the five roles, never once for all of them, which would be a default by another name. A flag that takes several words takes them as separate arguments, since a path or an address can hold `=` or a comma. The flags are checked against each other before anything is read: the first blueprints repository must be among the drive's repositories, the machine among the hosts, and each kept repository among the repositories, kept only on the host the command runs on.
3. **What the command owns in the file.**
   - The drive's entry is replaced whole, so a key the flags no longer give is gone.
   - Each host the flags name is set, and no host is removed, since another drive or `crew hold` may name it.
   - The drive's console is set, or removed where it is not given.
   - A kept repository the drive dropped leaves the file unless another drive of this host lists it.
   - Everything else in the file stays, unknown keys included.

   The file is written in the module's exact bytes, so a host reads the same whichever wrote it (`flake.2`). Not taken: merging the flags into the old entry, under which the same flags would give different files on two hosts.
4. **A linked file is never written through or replaced (`read.4`).** Where Nix links the teams file, the command writes nothing there and says so. It goes on to make the state only if the linked file already names the drive with every fact the flags give; otherwise it refuses, naming each key that differs and the Nix setting to change.
5. **A set that changes the file is recorded on the drive's branch (`roles.2`).** The entry names the paths of the keys that changed, never their values, and who ran it. crew refuses the command to no caller, since a drive changes on the user's word and the record says who acted on it.
6. **A file is moved aside only where crew cannot read it at all (agentplot-design's).** A teams file that is not JSON, not an object, or at a version this crew does not read is the person's own in record 0009's sense. It is moved aside once to `teams.json.before-drive-set`, both paths named, as the modules move a file aside. A file at crew's own version that fails a check is crew's own file, written by this command or the module. It is refused, naming the check, with nothing written, unless the set itself mends it (point 8). Moving it aside would drop every other drive of the host from the live file for one wrong field. Not taken: moving every file that fails to load aside. Built by `a-drive-set-loses-no-drive-and-no-record`.
7. **No set goes unrecorded (agentplot-design's).** When a run's file write lands but its state push fails, the set's entry still reaches the drive's branch with the run that finishes the state. So the branch always says who named the drive, however many runs it took. Not taken: recording only the run whose own file write changed a key, which loses the entry after a failed first push. Built by `a-drive-set-loses-no-drive-and-no-record`.

**A drive is not removed by this command.** Record 0009's amendment names, as later changes, a repository of the drive added or removed, which `crew drive set` covers. It asks for no drive's removal, and nothing builds one. The operator's brief says only what setup can do.

**The command runs on the host it is invoked on**, and is never forwarded. It writes that host's own file, as `crew signal` runs where it is invoked. This departs from `code.3`, which forwards a main level's commands to the machine the file names.

## Consequences

- `code.5` names `crew drive set` as the file's writer on a host where Nix does not link it.
- Boomdrive's setup calls the command with the Mac's own values: a session named for the drive, herdr's folder for it, the login's Claude account for each role, and the runner's folders for each kept repository. Before that, setup makes the GitHub state repository where none exists (record 0009's amendment).
- `a-drive-set-mends-what-it-replaces` builds point 8.
- The operator's brief says a drive is added or changed through Boomdrive's setup, and names no removal of one there; the chore `the-operators-brief-names-no-drive-removal-by-setup` brings it to that.

## Amendment, 2026-11-09: what the build decided, and a set mends what it replaces

Status: accepted on 2026-11-09 by agentplot-design. Points 9 to 12 are the construct's of `a-drive-set-loses-no-drive-and-no-record`, from its design, taken as accepted. Point 8 is agentplot-design's, on batch 26's review of that change. Each is cheap to change.

8. **A set mends what it replaces (agentplot-design's).** A file at crew's own version is written where every check passes once the drive's entry and the hosts the flags name are set as given, whatever the file held for them before. Where a check still fails, the file is refused, naming the check, with nothing written (point 6). The set replaces those parts whole anyway (point 3), so a fault there is one the set itself mends, and refusing it would ask the person for a hand edit, which record 0009's amendment never asks of them. Not taken: refusing every file at crew's version that fails a check before the set, as the build first did.
9. **Where the person's file ends and crew's begins.** A file with no version, a version that is no integer or another version is the person's own, and is moved aside. A file at version 6 that lists teams or lists no drives is crew's own, and is refused, since version 6 never held teams. A writer moves a file aside only where it cannot keep what the file holds: crew's module replaces the whole file, so it moves every file aside, while `crew drive set` keeps every other drive.
10. **The set's entry is kept on the host until the branch can take it.** It is written to the host's run record as soon as the file is in place, before the state is made, since a new drive has no branch yet. It reaches the branch with the state's first write, or with the command's last step, which pushes whatever of the drive the branch still lacks. Not taken: a separate file of unrecorded sets, a second record of one fact; the finishing run writing its own entry, which cannot know which keys changed or who changed them. This departs from the run record's rule that an entry reaches the branch as it is written: the set's entry reaches it later, in the same command or with the run that finishes the state.
11. **A refusal once the file names the drive is the state's.** Its words say the file names the drive and that the same command, run again, makes the state, and it is recorded as a refused state init.
12. **A refused push at the last step is said once.** It is said on standard error and changes neither the answer nor the exit.
