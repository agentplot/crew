# Design

## Context

This section records what was read on 2026-11-10 on deneb, so the decisions below rest on it.

**How crew runs crew on another host today.** One function, `crew_at(fleet, host)` in `plugin/lib/crew.py`, gives the crew command on a host. On this host it is `crew_command()`, the crew the host installed (README, "crew's commands run the crew the host has installed"). On another host it is `<checkout>/plugin/bin/crew`, where the checkout is the one `kept_on` finds for the repository crew's manifest names (`crew_on`, `crew_repository`). Every path to another host goes through it:

- `crew_argv`, which builds `env CREW_AGENT=… CREW_LABEL=… CREW_SESSION=… bash <crew_at> <args>` for Python's `on_machine`. Its callers include `hold.fan`, `ops.py`'s forwarded acts, and `plan.py`'s sweep, cards, landings, `_made` and `_land-row`.
- `reach`, which hands bash `REMOTE_CREW` (or `REMOTE_CREW_REFUSED`) and `CALLER_SESSION`. Bash's `there` then runs `env … bash "$REMOTE_CREW" …` over ssh (`code.3`).
- `read_agent`, which builds `python3 <checkout>/plugin/lib/crew.py found <agent>` for a tell's look at an agent herdr names in no pane. It builds that line before it runs anything, so a host that keeps no checkout refuses the whole tell, even where herdr would have named the agent.

**The failures.** On the box, crew 0.41.11, at 13:57: "none of deneb's sessions keeps afterthought/crew". On deneb, the teams file names no checkout of crew on chuck-herdr-alpha. So a send fails in both directions before anything is asked of the other host.

**What each host has installed.** Checked on 2026-11-10:

- On deneb, `crew` on the path is `/etc/profiles/per-user/chuck/bin/crew`, a Nix wrapper that is a bash script, and `crew _release` answers `v0.49.0` from release.
- `ssh -o BatchMode=yes chuck-herdr-alpha 'command -v crew'`, run from deneb, answers `/etc/profiles/per-user/chuck/bin/crew`. The same command under `sh -c` answers the same. The box's login shell is zsh.
- The brief records the other direction: the box reaches deneb by ssh and finds the same path there.

**deneb's teams file.** It is at version 5, with its drives under `partitions` and no `hosts`. That is the version deneb's pinned crew reads. This crew reads only version 6 (`code.5`), whose `fleet_of` refuses any drive whose machine `hosts` does not name.

**The family.** agentplot/blueprints `design/principles.md` 14 says a tool that needs what another program knows reads that program's own source, never a file a host makes for it. agentplot/boomdrive record 0023 (accepted) has the set install each tool's own package, crew's among them. No other tool of the family runs itself on another host over ssh: Flume, sluice and Timber each act on their own host. So this behaviour is crew's alone, with nothing to reconcile. What a host has installed is the host's own word, and its login path is where it says it.

**Area pages this change touches:**

- `teams.md`, for `plugin/bin/crew` and `plugin/lib/crew.py`. It relies on `teams.9`: what bash evals is shell assignments quoted with `shlex.quote`.
- `tests.md`, for `tests/`. It relies on `tests.4`, `tests.11` and `tests.12`.
- `docs.md`, for README and `openspec/`. It relies on `docs.2`, `docs.4` and `docs.7`.
- `briefs.md`, for `plugin/skills/crew/SKILL.md`.

From `core.md`, it relies on `code.3`, `code.5`, `code.7`, `code.11` and `read.1`. No rule changes, and no rule page or record is edited (`docs.7`). `teams.19`'s details, as read on 2026-10-31, describe a host whose checkout another host's command ran (`crew_at`). They stay as the reading of that day. Whether they need a note once this lands is the design agent's call, after the landing.

## Goals / Non-Goals

**Goals:**

- Every command that runs crew on another host runs the crew that host installed, whether or not the teams file lists crew among a drive's repositories there.
- A host whose login path finds no crew is named in the failure (`read.1`).
- One place builds the command line that runs crew on another host, used by both the Python and bash paths.

**Non-Goals:**

- Which crew a host installs, or when it moves. That is the host's own configuration and crew's releases (`code.10`, `plan.19`).
- What `crew_command()` gives on this host. It is unchanged.
- The kits' checkouts that `kept_on` and `kit_kept` find for the drives' repositories. They still serve kits and blueprints. Only crew's own lookup of itself goes.
- `tests/moon-tasks`' command core. It keeps `plugin/.claude-plugin/plugin.json`, which the logic case for crew's own address still reads.

## Decisions

### Decision 1: crew on another host is `crew`, by its name on that host's login path

crew runs `crew` on another host by its bare name. ssh hands the line to the user's login shell there, and that shell's path finds the crew the host installed. On deneb and the box that is the Nix profile's `crew`. crew reads neither the teams file's repositories nor its own manifest to find it. The crew is the host's own word, given where the host gives it: on its path (principle 14).

It is run directly, as `env CREW_AGENT=… CREW_LABEL=… CREW_SESSION=… crew <args>`, not as `bash <path>`. An installed crew is whatever executable the host put on its path. deneb's is a bash wrapper script today, but a compiled wrapper would not run under `bash`.

Paths not taken:

- *The checkout the teams file keeps there, as today.* It fails wherever no drive lists crew, as on both hosts now. Where one does, a released host would run that checkout and its release side by side, two crews on one host. That is what `teams.19`'s reading of 2026-10-31 found restarting every agent on the box.
- *A fixed path, such as `/etc/profiles/per-user/<user>/bin/crew`.* It differs between NixOS, nix-darwin and a person's Mac, and between users. crew would be writing down a host's layout that only the host knows.
- *Asking the other host's `crew _release` first for its root, then running that root's `plugin/bin/crew`.* That costs a second ssh round trip for each command, and it reaches into another crew's files where its command already answers.

### Decision 2: `crew_there` builds the one command line, and every path runs it

`crew_there(host, who, label, session, args)` is a decision on plain facts (`code.7`). It gives the argv that runs crew on another host as the one asking:

```
["sh", "-c", NO_CREW, host, "env", f"CREW_AGENT={who}", f"CREW_LABEL={label}", f"CREW_SESSION={session}", "crew", *args]
```

`NO_CREW` is `command -v crew >/dev/null 2>&1 || { printf '%s\n' "$0 has no crew on its login path, so crew can't run there" >&2; exit 127; }; exec "$@"`, quoted as a Python constant. `$0` is the host's name.

Each path uses it:

- `crew_argv(fleet, host, *args)` returns it for another host, with `rec.who()`, `caller_label(fleet) or ""` and `rec.session() or ""`. For this host it returns today's line.
- `reach(fleet, machine)` gives bash `REMOTE_CREW` as `shlex.join(crew_argv(fleet, machine))`, the line with no arguments. It gives nothing else, because the line already carries the session. `REMOTE_CREW_REFUSED` and `CALLER_SESSION` go.
- bash's `there` runs `ssh -o BatchMode=yes "$SSH_TARGET" "$REMOTE_CREW $(printf '%q ' "${orig[@]}")"`. `identity()` goes once nothing calls it.
- `read_agent`'s look on another host is `sh -c "<herdr agent get> || exec <shlex.join(crew_argv(fleet, host, '_found', name))>"`. Nothing in it can be refused before ssh runs.

So the asker's identity (`code.3`), the check for crew and the run are the same on every path. `crew_at`, `crew_on`, `crew_repository`, `repository_named`, `GITHUB` and `MANIFEST` go, since nothing reads them.

Path not taken: *bash builds its own line beside Python's, as today.* The check of Decision 3 would then be written twice, and `identity()` and `rec.who()` would keep two spellings of the asker.

### Decision 3: A host whose login path finds no crew fails, naming the host

Where `command -v crew` finds nothing on the other host, the guard prints "<host> has no crew on its login path, so crew can't run there" on standard error and exits 127, the shell's own code for a command not found. Nothing else runs there, and crew tries no checkout in its place (`read.1`).

Each caller says that failure as it already says any failure of the command there. Bash's `there` passes the remote's standard error through and exits with its code. A tell's `found_answer` reads a failed `found` as "crew on <host> could not look for it", followed by what it said. A host that does not answer still exits 255 and is read as unanswered (`unanswered`), unchanged.

Path not taken: *letting `env` say "crew: No such file or directory".* Those words name no host, and the box's and deneb's `env` spell them differently.

### Decision 4: A host is reached by its `ssh` name in `hosts`, with no fallback to its machine name

`ssh_of` is unchanged. A host the teams file's `hosts` does not name is refused, naming the host and `hosts`, before any ssh runs.

The brief asks for the host's ssh name in `hosts`, "else its machine name". No fallback is built, for two reasons:

- On the version-6 file this crew reads, the fallback has no case. `fleet_of` refuses a drive whose machine `hosts` does not name, and every host crew runs crew on is a drive's machine, or is checked against `hosts` (`crew hold`).
- A default would break `code.5` ("no field has a default") and `read.1`.

deneb's file today is at version 5 with no `hosts`, but it is read by deneb's pinned crew, not by this one. A host reaches this crew's code only with a version-6 file, which its writer, crew's module or the machine's configuration, gives `hosts`. This choice is the design's own and cheap to change. A fallback, if one were ever wanted, would be a change to `code.5` first.

### Decision 5: `crew _found <agent>` asks another host's crew to find an agent in its pane

A tell's look at an agent herdr names in no pane on another host used to start that host's checkout's `crew.py` by path. It now asks that host's crew through its command: `crew _found <agent>`. The command runs crew.py's `found` and prints its one line of JSON, as `found` does now.

Like any internal command, it is in the usage header and answers `-h` or `--help` with its usage line before it reads anything (`code.11`). bash reads it, as it does the other commands that have no arm of their own. A far host whose crew predates `_found` fails the command, and `found_answer` already reads that failure ("as one on a host whose crew is older").

Path not taken: *`python3 "$(crew _release | jq -r .root)/plugin/lib/crew.py" found <agent>` on the far host.* It needs jq there and two starts, and it reaches into another crew's files.

### Decision 6: The tests' hosts each have crew installed on their login path

Each simulated host's login path is `$CREW_TEST_ROOT/hosts/<host>/bin`. The stub ssh puts that folder first on the path it runs a command with, as a host's login shell puts its profile first (`tests.4`: the stub behaves as ssh to such a host does). `world()` installs `crew` there on each host as a two-line wrapper that execs the test's own `$CREW/plugin/bin/crew`, as the Nix wrapper execs a build's.

It is a wrapper, not a link, because `plugin/bin/crew` finds its `lib` from its own folder (`here=$(cd "$(dirname "$0")" && pwd)`), which a link in another folder would mislead.

The links of crew's checkout into the spaces stay, as the drives' kits the fixture's `repos` name. A case then removes the box's installed crew while that checkout still stands, and shows that crew does not fall back to it.

## Departures

None. Decision 4 declines a fallback the brief names. That keeps `code.5` and `read.1`, and departs from no rule.

## Risks / Trade-offs

- **The far host's crew may be another version than the asker's.** A forwarded command runs whatever release the far host installed. A command or flag that release lacks is refused there in its own words. That is the cost of each host running its own package (agentplot/boomdrive record 0023). The checkout it replaces could lag or lead just the same, and could be absent.
- **A host whose non-interactive ssh shell does not put its profile on the path.** Such a host fails with Decision 3's words, naming it. The fix is the host's own path, not a crew setting. Both of today's hosts find their crew (Context).

## Migration Plan

None. A host needs no new file or setting. It needs only the crew it already has installed on its login path.

## After deploy

None. Every outcome is a logic or end-to-end case of this change. The change reaches a host once a crew release carrying it is installed there, which is the fleet's move on the user's word (`code.10`, `plan.19`), not a step of this change.

## Task notes

**1.1** `plugin/lib/crew.py`:

- Add `NO_CREW` and `crew_there(host, who, label, session, args)` (Decision 2), beside `crew_argv`.
- `crew_argv`: for another host, return `crew_there(host, rec.who(), caller_label(fleet) or "", rec.session() or "", args)`. For this host, return today's line, with `crew_command()` in place of `crew_at`.
- `reach`: for another host, return `{"REMOTE_CREW": shlex.join(crew_argv(fleet, machine))}`. Fix its docstring.
- `read_agent`: build the fallback from `crew_argv(fleet, host, "_found", name)`, and drop its `Refusal` catch around the line, which can no longer refuse.
- Remove `crew_at`, `crew_on`, `crew_repository`, `repository_named`, `GITHUB`, `MANIFEST` and `MANIFEST`'s comment.
- Fix every docstring that names them, such as `found_answer`'s "crew.py found", which becomes "`crew _found`". Find them with `grep -n "crew_at\|crew_on\|crew_repository\|MANIFEST" plugin/lib/*.py`.

`tests/py/test_crew_on.py`, rewritten with its opening docstring citing this change's reading:

- `crew_there` gives exactly the argv above for `("chuck-herdr-alpha", "swancloud-planner", "wldn", "deneb:s1", ["main", "status", "wldn"])`.
- `crew_argv(KEPT, BOX, "x")`, with `this_host` deneb, `CREW_AGENT` set and `rec.session` stubbed, ends `["crew", "x"]` and names no checkout path. The same holds with a fleet whose `repos` list no crew. It reads no manifest: monkeypatch `pathlib.Path.read_text` for the manifest to fail.
- `crew_argv` for this host is unchanged.
- `reach(KEPT, BOX)` gives only `REMOTE_CREW`, and `shlex.split` of it equals `crew_argv(KEPT, BOX)`.
- `read_agent` on another host runs one `on_machine` whose `sh -c` line ends with `crew _found wldn-planner`, and it does not refuse for a fleet that keeps no crew. Stub `on_machine` to record the argv.
- `TestReach` stays: the ssh name, and the refusal of a host `hosts` does not name, with no ssh. Its `fan` case still monkeypatches `crew_argv`.
- `test_crews_code_writes_its_own_address_nowhere` reads the address with `json.loads` of `plugin/.claude-plugin/plugin.json` and a regex in the test.
- Delete `TestCrewOn`, `TestCrewAt` and `TestRepositoryNamed`.

**1.2** `tests/contract/test_no_crew.py` (new), importing `crew` as the contract tier's other cases do, with scratch folders from `tmp_path`. Its docstring names `crew.NO_CREW` and `crew_there` as what assumes the behaviour (`tests.11`). It has two cases, each running `crew_there`'s argv less its `env …` tail through a real `sh`:

- With `PATH` set to an empty scratch folder, the guard prints "chuck-herdr-alpha has no crew on its login path, so crew can't run there" on standard error and exits 127.
- With a scratch executable `crew` that echoes its arguments on that `PATH`, the guard execs it with the arguments, and their exit code is its own.

**2.1** `plugin/bin/crew`:

- Add the usage header line `crew _found <agent>`, worded as the other internal lines are: "where herdr names an agent in no pane on this host, look for it in the pane crew keeps for it and give its name back; one line of JSON, as another host's crew asks it".
- Add a `_found)` arm among the commands that exec `python3 "$here/../lib/crew.py" found "${args[@]:1}"`, placed so that `--help` reaches bash's own usage first, as the other internal commands without a parser do.

`tests/t-help.sh`: add `_found wldn-planner` to the commands its loop runs with `--help` and `-h`. `plugin/skills/crew/SKILL.md`: add a row for `crew _found` beside `crew _release`'s.

**2.2** `plugin/bin/crew`:

- `there <ssh name> <args...>` runs `ssh -o BatchMode=yes "$1" "$REMOTE_CREW $(printf '%q ' "${@:2}")"`.
- `one` drops the `REMOTE_CREW_REFUSED` line and calls `there "$SSH_TARGET" "${orig[@]}"`.
- `identity()` goes if nothing else calls it.

`tests/stubs/ssh`: after `HOME` is set, `export PATH="$CREW_TEST_ROOT/hosts/$target/bin:$PATH"`. Extend its opening comment: the host's own `bin` comes first, as its login shell's profile does.

`tests/lib.sh` `world()`: for each host, `mkdir -p "$T/hosts/$h/bin"`, and write `$T/hosts/$h/bin/crew` as `#!/usr/bin/env bash` and `exec "$CREW/plugin/bin/crew" "$@"`, made executable. Its comment says crew is installed on each host's login path, and that crew's checkout in each space is the drives' kit.

Done when the existing forwarding (`crew main status wldn` on mac-studio) and the found case pass.

**2.3** `tests/t-journey-main.sh`, after the send cases and before the board word:

- Write mac-studio's teams file again with crew's repository in no drive's `repos`, through `jq` to a new file and `mv`. Then `crew main status wldn` passes and `crew send wldn "Words NOCK for the drive"` reaches wldn-operator. The calls log shows `ssh chuck-herdr-alpha` running `crew main status wldn` with no `plugin/bin/crew` in the line.
- Restore the file. Move `$T/hosts/$box/bin/crew` aside and clear the calls log. `crew main status wldn` fails with "chuck-herdr-alpha has no crew on its login path, so crew can't run there". Nothing ran on the box: the checkout link in its space still stands, and the log holds no line from chuck-herdr-alpha, only mac-studio's ssh to it.
- Move the crew back.
- Name these cases in the opening comment. Its `# Reads:` line is unchanged.

**3.1** `README.md`: where it says crew's commands run the crew the host has installed, add that a command crew runs on another host is likewise that host's installed crew. It is found as `crew` by its name on the host's login path, over ssh to its `ssh` name in the teams file's `hosts`, as the one asking, and a host whose login path finds none fails naming it. Add `crew _found` beside `crew _release` as how one crew asks another to find an agent.
