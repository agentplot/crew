# Verify: another-hosts-crew-is-the-one-it-installed

Verified on `change/another-hosts-crew-is-the-one-it-installed` at 00f86fa6, 2026-11-10.

## The whole checks

`tests/suite --affected`, the `check-full` tasks the change affects against the merge-base with main, run once: **34 passed (3 replayed), 0 failed**, exit 0. The change edits crew's command core (`plugin/bin/crew`, `plugin/lib/crew.py`), so every one of the tests project's tasks is affected.

- tests: `logic`, `contract`, and every end-to-end task, `t-help`, `t-journey-main`, `t-docs` and `t-specs` among them.
- nix: `test`, `typecheck`.

`t-docs`, `t-help` and `t-journey-main` were replayed. Each replay is of a run that passed on this host with identical inputs, and moon never replays a failed run.

`openspec validate another-hosts-crew-is-the-one-it-installed --strict`: valid.

Archived in a scratch copy of the checkout's `openspec/` at 00f86fa6, the change writes `crew-command` (2 added, 3 removed). `openspec validate --specs --strict` then gives **28 passed, 0 failed**, so `t-specs` holds the specs once archived.

## Tasks

All 6 tasks of `tasks.md` are ticked, none open. Each one's check is among the tasks that passed above: 1.1 in `logic` (`tests/py/test_crew_on.py`), 1.2 in `contract` (`tests/contract/test_no_crew.py`), 2.1 in `t-help`, 2.2 and 2.3 in `t-journey-main`, and 3.1 in `t-docs`.

## Requirements and scenarios

### crew reaches another host by its ssh name and runs the crew that host has installed (added)

- **One line, built in one place.** `crew_there` gives `sh -c NO_CREW <host> env CREW_AGENT=… CREW_LABEL=… CREW_SESSION=… crew <args>` (`code.7`: plain facts, no process). `crew_argv` returns it for another host, `reach` gives bash only `REMOTE_CREW` as its `shlex.join`, and `read_agent`'s fallback is `crew_argv(fleet, host, "_found", name)`. bash's `there` runs `ssh -o BatchMode=yes <ssh name> "$REMOTE_CREW <args>"` (`code.3`). `identity()`, `REMOTE_CREW_REFUSED` and `CALLER_SESSION` are gone. `crew_at`, `crew_on`, `crew_repository`, `repository_named`, `GITHUB` and `MANIFEST` are gone from `plugin/`, with no caller left.
- **A command forwarded to a main level's host.** `TestCrewThere` pins the argv for `crew main status wldn` asked by swancloud-planner of wldn in session `deneb:s1`. In `t-journey-main`, with `agentplot/crew` in no drive's `repos`, `crew main status wldn` on mac-studio passes, and the calls log shows `ssh chuck-herdr-alpha` running `crew main status wldn` with no `plugin/bin/crew` in the line.
- **A send reaches another host's drive whatever the teams file keeps of crew there.** `TestCrewArgv` gives the same `crew_there` line for a fleet that keeps crew and one that does not, with no checkout path in it and the manifest unread (a read fails the case). In `t-journey-main`, `crew send wldn "Words NOCK for the drive"` reaches wldn-operator, marked from swancloud-planner, with crew in no drive's `repos`.
- **A tell finds an agent herdr names in no pane through the crew installed there.** `TestReadAgent` shows one run on the box, `herdr --session wldn-2 agent get wldn-planner || exec <crew_argv … _found wldn-planner>`, with nothing refused before it for a fleet that keeps no crew. `crew _found` dispatches to `crew.py found` and is in the usage header and the crew skill. `t-journey-main`'s dropped-name case reaches the planner through the box's installed crew and gives the name back.
- **crew's code names no address of its own.** `test_crews_code_writes_its_own_address_nowhere` reads the manifest's `repository` and finds it in no module under `plugin/lib/` and no command under `plugin/bin/`.

### crew is run on no host that has no ssh name or no crew on its login path (added)

- **A host that has installed no crew.** `NO_CREW` prints "`$0` has no crew on its login path, so crew can't run there" and exits 127, else execs the command. `tests/contract/test_no_crew.py` runs it through a real `sh`: an empty path gives exit 127, that message naming chuck-herdr-alpha and no output; a scratch `crew` on the path is run with its arguments intact and its own exit code. In `t-journey-main`, with the drive's `repos` listing crew again and the box's installed crew moved aside, `crew main status wldn` fails with "chuck-herdr-alpha has no crew on its login path, so crew can't run there", the box's checkout link still stands, and the log holds no line run on the box.
- **A host the file gives no ssh name.** `TestReach` refuses `macbook-pro` through `ssh_of`, `on_machine`, `opener`, `hold.fan` and `plan.forwarded`, naming the host and the teams file's `hosts`, with no ssh run.

### Removed

- **crew reads the repository it is from its own manifest**, **crew reaches another host by its ssh name and runs the checkout that host keeps of crew** and **crew is run on no host that keeps no checkout of it or has no ssh name** are removed by the delta. Nothing in `plugin/` reads the manifest's `repository`, and nothing looks for crew's checkout on another host. Those three requirements' cases (`TestCrewOn`, `TestCrewAt`, `TestRepositoryNamed`) are gone.

### Tests' hosts and docs

- The stub ssh puts `$CREW_TEST_ROOT/hosts/<target>/bin` first on the path (`tests.4`). `world()` installs there a wrapper that execs the test's `plugin/bin/crew`.
- `t-help` runs `_found wldn-planner` with `--help` and `-h` (`code.11`).
- README says a command crew runs on another host is the crew that host installed, by its name on its login path, over ssh to its `ssh` name as the one asking. It says a host whose path finds none fails naming it, and names `crew _found` beside `crew _release`. With the usage header and the skill, that keeps `docs.2`. `t-docs` passed.
- No page under `docs/architecture/` or `docs/adr/` is edited (`docs.7`).

## Outcome

The whole checks pass, every task is done, and every requirement and scenario holds. The change is archived.
