# Another host's crew is the one it installed

## Why

A crew command that runs crew on another host, a tell, a send, an ops act or a command forwarded to a main level's host, runs the checkout of crew's repository that the teams file keeps there: the folder of a drive on that host whose `repos` lists crew (`crew_at`, `plugin/lib/crew.py`). A host keeps that checkout only where a drive's `repos` happens to list crew, and a released host does not run it anyway: it runs its release. So both directions between the box and deneb fail today:

- On the box, crew 0.41.11, 2026-11-10 13:57: "none of deneb's sessions keeps afterthought/crew", so a send to deneb's operator was refused before anything was asked of deneb.
- On deneb, the teams file names no checkout of crew on chuck-herdr-alpha, so a send to wldn's operator is refused the same way.

Each host already has crew installed on its login path. Checked 2026-11-10: the box reaches deneb by ssh and finds `/etc/profiles/per-user/chuck/bin/crew` there, and deneb reaches the box and finds the same. A tool's own source says what it knows (agentplot/blueprints `design/principles.md` 14), and the set installs each tool's own package (agentplot/boomdrive record 0023). So the crew on another host is the one that host installed, found by its name.

## What Changes

- **crew on another host is `crew`, by its name on that host's login path,** run over ssh to the host's `ssh` name in the teams file's `hosts`, as the one asking (`code.3`). crew looks for no checkout there and reads no repository of its own to find one.
- **A host whose login path finds no crew fails, naming the host,** and nothing else is tried in its place (`read.1`). A host the teams file's `hosts` does not name is refused before any ssh, as today.
- **One command line, built in one place.** crew's Python and bash's forwarding both run the line `crew_argv` builds, so the asker's identity, the check for crew and the run are the same on every path.
- **`crew _found <agent>`:** a tell's look for an agent that herdr names in no pane, asked of the other host's crew through its command, where it used to start that host's checkout's `crew.py` by path.
- **crew stops reading its own address.** `crew_repository`, `repository_named`, `GITHUB` and `MANIFEST` go, since nothing reads them now. The manifest keeps its `repository`, and a logic case still checks that crew's code names no address of its own.
- **The tests' hosts each have crew installed on their login path.** The stub ssh puts the host's own `bin` first on the path, as a login shell's profile does.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `crew-command`: crew runs the crew another host installed, by name on its login path, and fails naming a host whose login path finds none. It no longer reads the repository it is from its manifest to find a checkout there.

## Impact

- `plugin/lib/crew.py`: `crew_there` (new), `crew_argv`, `reach`, `read_agent`. Removed: `crew_at`, `crew_on`, `crew_repository`, `repository_named`, `GITHUB`, `MANIFEST`.
- `plugin/bin/crew`: `there`, `one` and `identity`; the `_found` command and its usage line.
- `tests/py/test_crew_on.py`; `tests/stubs/ssh`; `tests/lib.sh` (`world`); `tests/t-journey-main.sh`; `tests/t-help.sh`.
- `README.md` and `plugin/skills/crew/SKILL.md`: what crew runs on another host, and `crew _found`.
- Reaches a host when its crew release carrying it is installed there (`code.10`, `plan.19`). The asking side is the one that changes. The far side needs only an installed crew on its login path, which both hosts have.
