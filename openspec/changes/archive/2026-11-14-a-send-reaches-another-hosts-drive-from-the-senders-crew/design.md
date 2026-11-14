# Design

## Context

Record 0068 (accepted 2026-11-14, boomdrive-design's) decides how a send reaches a drive that runs on another host. The sending host's teams file names the drive. `crew send` there types the prompt into the drive's operator through herdr over ssh, as `crew tell` reaches an agent on another host (`code.3`). It writes the send's entry on the sending host and pushes it from there (`read.5`). So no agent runs ssh to send, and no crew command runs under ssh on a Mac, where the login keychain is out of reach. `briefs.10`'s details already rule out the ssh workaround and allow this way.

Read on crew's main at 1b4e1b3b, the send path already does this for any drive the host's teams file names:

- `crew send` is `py send` in `plugin/bin/crew`, run where it is invoked, never forwarded.
- `crew.send` resolves the door (`send_door`) and calls `tell`. `tell` finds the operator's machine and session from the drive's entry (`place_of_agent`, `role_session`). It reads whether the operator waits on a question (`waits_on_question`), and types with `on_machine(fleet, host, ["herdr", "--session", session, "agent", "prompt", …])`, which is `ssh -o BatchMode=yes <ssh name> …` for another host.
- `crew.send` then calls `record.emit(label, "send", …)`. That appends to this host's own file of the receiving drive's record (`record.4`) and pushes it through `record.reach`. `reach` fetches the drive's state branch into crew's bare cache and pushes over https with the host's own git credential (`state.1`). A refused push is said once and kept for the host's next entry (`record.2`).

deneb's teams file names wldn, which runs on chuck-herdr-alpha, and `tests/t-journey-main.sh` proves a send from mac-studio to the box's wldn. The reverse is what wldn's agents need, a send from the box to a Mac's drive. It fails today only because alpha's teams file names none of deneb's drives. `send_door` refuses those drives with "crew send sends to a drive by its label, not '<name>': drives wldn", which names no way on, and the agents took ssh. Over ssh on deneb, herdr and python3 are on the path (read 2026-11-14: `/etc/profiles/per-user/chuck/bin/herdr`, `/run/current-system/sw/bin/python3` 3.13.15), and a send's prompt reached the pane (the signal). Only the push met the keychain.

alpha's GitHub sign-in can push afterthought/crew-state from a non-interactive ssh session (afterthought-ops's reading, `signals/2026-11-14-boomdrive-planner-14f4a237/01` on boomdrive/main).

## Goals / Non-Goals

**Goals**

- A send from any host to a drive its teams file names on another machine is proven: typed by herdr over ssh, no crew command run on that machine, its entry pushed from the sending host.
- A send whose entry's push is refused still stands, the entry kept on the sending host.
- An agent refused for a drive its host's file does not name is told the way on: the host's configuration names the drive, never an ssh to another host.
- Every brief, README, the skill and the usage say a send runs on the sender's own host.

**Non-Goals**

- Writing alpha's teams file. Naming deneb's drives there is afterthought's host configuration's (record 0068, Consequences), swancloud's `lib/crew-teams.nix`.
- Other commands forwarded to a Mac over ssh (`code.3`), which still push from an ssh session there. Record 0068 leaves them undecided.
- A refusal of `crew send` run over ssh (Decision 3).
- Any change to the teams file's shape, to `record.py` or to what crew models.

## Decisions

### 1. A drive another host runs is named in the sending host's `drives`, as every drive is

The teams file already names every drive a host's crew deals with under `drives`, each with its `machine` (`code.5`; `services.crew`'s `drives` option: "Every drive, by its label, with its `machine`"). deneb's file names wldn on chuck-herdr-alpha that way. A drive the host's agents send to is named the same way, with its machine, its session and its state repository. It gets no `consoles` entry there, so the host's follower reads nothing of it (`board.labels_here`, the `operator-agent` requirement "A host's operator sessions are the consoles its teams file names", `tests/py/test_board.py`). Its roles get no entry in the host's Flume roles file (`source.py`, `teams.25`; `tests/py/test_source.py`), and `crew revive` and the batch reckoning pass it over, each reading only drives whose `machine` is the host. That is record 0068's "such a drive has no session on the host, so the host's follower reads nothing of it", and it holds today.

Not taken: a key of its own, such as `sends`, giving another host's drive by its machine, session and state alone. It would be a second shape of drive, which `send_door`, `place_of_agent`, `kind_role_of`, `plan.state_of` and `record.reach` would each have to learn. The writer would have two ways to name one drive. And it would name nothing the file does not already name for a drive. The configuration's cost is a full entry for each such drive, which a Nix writer emits from the same source as the drive's own host's file.

This decision is crew's own and cheap to change: it adds nothing to crew.

### 2. The send runs on the sender's host and reaches the other machine by herdr alone

What reaches the drive's machine for a send is what `tell` already sends there, over `ssh -o BatchMode=yes` (`code.3`):

- `herdr --session <s> agent get <operator>`, reading the operator (`read_agent`);
- `python3 -` fed `questions.py`, reading whether its session has a question open (`waits_on_question`, `piped`);
- `herdr --session <s> agent prompt <operator> "<marked text>"`, the send itself.

Only where herdr lists no agent by the operator's name does `read_agent` also ask that machine's own crew, `crew _found <operator>`. That command looks for the operator in the pane crew keeps for it and gives herdr its name back (`briefs.17`). It writes no entry and reaches no remote, so no keychain comes into it. Record 0068 says "no crew process on the drive's machine runs under ssh for a send, so its keychain never comes into it". Its aim is the keychain, which none of these reach. `crew _found` stays, rather than refusing a send to an operator whose name herdr dropped. The end-to-end case proves that a send to an operator herdr lists by name runs no crew command on the drive's machine.

The entry is the sending host's. `record.emit` appends it to that host's own file of the receiving drive's record (`record.4`) and pushes it as its own commit, `runs(<sending host>): send agent/<label>-operator (<sender>)`, with the `Crew-Entry` trailer (`plan.2`). The push goes through crew's bare cache with the host's own git credential (`state.1`, `read.5`), never with force (`state.5`). The entry holds the send's length and never its text (`record.3`). A refused push is said once and kept for the host's next entry (`record.2`). `crew.send` already returns whether the prompt was typed, not whether the entry was pushed, so the send stands. A logic case pins that (`tests.4`).

No code of this path changes. The cases are the change: one end-to-end case from the box to a Mac's drive, and one logic case for the refused push.

### 3. The refusal of a drive the host does not name points to the host's configuration

`send_door` refuses a name that is no drive of the host's teams file. Its words become:

> crew send sends to a drive by its label, not '\<name\>': drives \<labels\>. A drive another host runs is sent to from here once \<teams file\> on \<host\> names it, as the host's configuration writes it, never by crew send run on that host over ssh; nothing was sent

`<labels>` are the drives the file names, sorted, or `none`. `<teams file>` is `crew.TEAMS`, and `<host>` is this host. The first sentence is today's, so the existing pins hold. `send_door` takes the host as a fact, `send_door(fleet, name, caller, here)`, and `send` passes `crew.this_host()`. So the decision calls no tool (`code.7`). The refusal is a `Refusal` through `fail()` (`code.2`), and nothing is typed or recorded (`read.1`; `record.1`: a refusal before any act writes no entry, as today).

Not taken: a refusal of `crew send` run over ssh, read from `SSH_CONNECTION` with no `SSH_TTY`, as `roles.3` would have for a rule an agent breaks. crew cannot tell an agent's `ssh deneb crew send …` from the user's own scripted ssh, and `roles.2`'s spirit leaves the user's acts unrefused by caller. Until alpha's file names deneb's drives, that ssh is the only way wldn's agents' sends reach deneb at all, and it loses nothing: the entry goes up with deneb's next push (`record.2`). `roles.3` asks a check of a rule a brief already states. The briefs state it from this change on (Decision 4), so a second breach would be the case for that check.

### 4. Every brief's one line says a send runs on the agent's own host

`crew.sends(cmd)`, the line beside every brief's roster (`briefs.10`, `teams.10`), becomes:

> \`\<cmd\> send \<drive\> "\<text\>"\`, run on your own host and never over ssh, which reaches that drive's operator, its one door, wherever it runs, and to nobody else

So every brief reads "anything for another drive is sent with `crew send <drive> "<text>"`, run on your own host and never over ssh, which reaches that drive's operator, its one door, wherever it runs, and to nobody else." It is still one line naming one way (`briefs.10`), and `tests/t-briefs.sh` pins it (`tests.6`).

### 5. README, the skill and the usage say it

Per `docs.2`, the three say together:

- a host's teams file names each drive its agents send to, its own and those another host runs;
- `crew send` runs on the sender's host and types into the operator through ssh and herdr where the drive runs on another;
- the entry is pushed from the sender's host;
- a drive the host's file does not name is refused, nothing sent.

`tests/t-docs.sh` pins a phrase of it in each.

### Rules relied on

`briefs.10` (one way to send, and its record 0068 details); `code.2`, `code.3`, `code.5`, `code.7`; `read.1`, `read.5`; `record.1`, `record.2`, `record.3`, `record.4`; `state.1`, `state.5`; `plan.2`; `roles.2`, `roles.3`, `roles.4` (the send is marked as a tell); `teams.10`, `teams.11` (a send types nothing to an operator not up or at a question, unchanged), `teams.25`; `docs.2`, `docs.7`; `tests.2`, `tests.4`, `tests.6`, `tests.11`, `tests.12`; `code.8`, for which nothing changes: no object, stage or field crew models moves, so `board.agent_views` and `plugin/hooks/status.js` are untouched.

Pages of `docs/architecture/` whose area the change touches: `core.md`; `teams.md` (`plugin/lib/crew.py`, `plugin/bin/crew`); `briefs.md` (`plugin/skills/`, and the briefs' line, which `crew.py` builds); `tests.md` (`tests/`); `docs.md` (`README.md`, `openspec/`). `record.md` binds the entry's behaviour, which this change relies on and does not change.

### Departures

None.

## Risks / Trade-offs

- **The proof waits on configuration.** wldn's agents still cannot send to deneb's drives from alpha until afterthought's host configuration names them in alpha's teams file. This change makes the refusal say so and proves the path, and asks nothing of that change.
- **A full entry in a host's file for a drive it does not run.** alpha's crew then treats deneb's drives as drives for every command: a read with no label covers them, reaching deneb over ssh for its kits and naming deneb when it does not answer (`read.3`), and a command about their main level forwards to deneb (`code.3`), meeting the keychain wall record 0068 leaves undecided. That is today's behaviour for deneb naming wldn.
- **`crew _found` on the drive's machine.** It runs only where herdr lists the operator by no name, and it reads and renames only (Decision 2).

## Migration Plan

None. Nothing stored changes shape. A host whose teams file names another host's drive sends to it as soon as it runs this crew, as it already does.

## After deploy

None. Every outcome here is a logic case or an end-to-end case on the stubs. Naming deneb's drives in alpha's teams file is afterthought's host configuration's change, not a step of this one, and nothing here waits on it.

## Task notes

**1.1** `plugin/lib/crew.py`:
- `send_door(fleet, name, caller, here)`: `here` is this host's name. The refusal for a name not in `fleet["drives"]` is Decision 3's words: the first sentence as today, then `. A drive another host runs is sent to from here once {TEAMS} on {here} names it, as the host's configuration writes it, never by crew send run on that host over ssh; nothing was sent`. The door's own send is refused as today.
- `send` passes `this_host()`; its docstring says the send runs on this host for any drive its teams file names, whichever machine runs it.

`tests/py/test_send.py`:
- `TestDoor` passes a host to every `send_door` call. The two cases that anchor the refusal with `$` match its new end.
- A new case, `test_a_drive_this_hosts_file_does_not_name_is_refused_naming_the_way_on`: a fleet naming wldn alone, `send_door(fleet, "afterthought", "wldn-planner", "chuck-herdr-alpha")` raises naming `drives wldn`, `crew.TEAMS`, `on chuck-herdr-alpha`, `never by crew send run on that host over ssh` and `nothing was sent`.
- `TestSend`'s `acts` fixture already stubs `tell` and `emit`, and `send` reads the host through `crew.this_host`, which the fixture stubs (monkeypatch) so no process starts (`tests.11`).

**1.2** `tests/py/test_send.py`, `TestSend`: `test_a_send_whose_entry_is_kept_still_reports_it_sent`. `record.emit` is stubbed to record its call and return `None`, as it does when its push is refused and the entry kept. `crew.send(FLEET, "wldn", "hello")` returns `True`, one `send` entry was asked for, and `tell` was called once. That the refusal is said once and the entry kept is `record.reach`'s, already pinned by `tests/py/test_record.py` (`test_a_push_that_is_refused_is_said_once_and_emit_still_returns_its_id`). No code change is expected. If the case fails, `send` is made to return what `tell` returned whatever `emit` returned.

**2.1** `tests/t-journey-main.sh`, after the sends from mac-studio. The box's teams file names swancloud on mac-studio, session `swancloud-1`, with no console for it (`tests/lib.sh` `teams_json`).
- Make swancloud's state branch if the journey has not (`crew state init swancloud`), so its entry has a branch to reach.
- Put an agent named `swancloud-operator` in a pane of mac-studio's stub session `swancloud-1`, idle, with the stub's `herdr --session swancloud-1 stub agent <pane> swancloud-operator` and `stub status`, run `as mac-studio`.
- Empty `$CREW_TEST_LOG`, then on the box: `HOST=$box CREW_AGENT=wldn-planner expect_ok crew send swancloud "Words BXMQ for the drive"`.
- The log holds `mac-studio swancloud-1 agent prompt swancloud-operator '[crew tell from wldn-planner] (sent to swancloud) Words BXMQ for the drive'`, reached by a `$box ssh mac-studio` line. No `$box ssh mac-studio` line runs `crew` (the stub's ssh line holds the remote command).
- The box's own file of swancloud's record, `~/.local/state/crew/swancloud/runs/chuck-herdr-alpha/*.rec` in the box's home, holds one `send` entry on `agent/swancloud-operator`, `By: wldn-planner`, `Chars: 24`. mac-studio holds none for it.
- `swancloud/main` of `$(remote afterthought/crew-state)` has as its newest commit's subject `runs(chuck-herdr-alpha): send agent/swancloud-operator (wldn-planner)`.
- `BXMQ` is nowhere in the branch's `runs/`.
- The test's opening comment gains the case (`tests.2`). Its `# Reads:` line stays as it is unless the case reads another file of crew's, and then `tests/moon-tasks` is run and `tests/moon.yml` committed (`tests.10`).

**3.1** `plugin/lib/crew.py` `sends(cmd)` returns Decision 4's line; the comment above it says the same. `tests/t-briefs.sh`'s case "every brief sends anything for another drive with crew send" pins `'/crew send <drive> "<text>"`, run on your own host and never over ssh, which reaches that drive'"'"'s operator, its one door, wherever it runs, and to nobody else.'` for each of design, planner, main-ops, operator and reviewer in place of today's phrase, and lacks today's ``"<text>"`, which reaches``. Any other pin of the old phrase in `tests/` is updated the same way.

**3.2** `README.md`, the main level's paragraph where it says "Anything for another drive goes with `crew send`", and its listing of `crew send` if it says more there; `plugin/skills/crew/SKILL.md`, its table row for `crew send`; `plugin/bin/crew`'s usage lines for `crew send`. Each says Decision 5's four points. Each says "pushed from the sending host" and "never over ssh", which `tests/t-docs.sh` pins in all three beside its existing `crew send` checks. `tests/t-help.sh`'s pin of the usage line (`send anything for another drive to its operator`) still holds, or is updated with the line.
