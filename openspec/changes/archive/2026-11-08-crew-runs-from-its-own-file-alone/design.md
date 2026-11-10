# Design

## Context

**What record 0064 asks.** Record 0064 (accepted 2026-11-09 by agentplot-design, on agentplot/main's `docs/adr/0064-crew-reads-a-hosts-drives-from-its-own-file-alone-and-no-fleets-file.md`; `code.5` as amended on the bolt at c0e9934e) has crew read "a host's drives, and everything it needs of the hosts that serve them, from its teams file alone, on every host: each drive's machine, its herdr session and folder, the Claude account each role runs under, and each host's kind and ssh name". It reads no file of swancloud's or of any fleet's. No field has a default. crew's module writes the facts where Nix configures the host, and crew's own command writes them at setup's asking elsewhere (`crew-makes-a-new-drives-state`, after this change in the bolt). The record rules out a fallback to the hosts file: "two sources for one fact".

**What crew reads of the hosts file today** (read on this branch at the bolt's tip, 92b872fa, 2026-11-09). `crew.load` refuses without `~/.config/swancloud/herdr-hosts.json` (`read_hosts`). It checks each drive's session and each role's `session` against the host's sessions (`session_of`), and checks that the main session's space keeps the first blueprints repo (`repo_in`). It takes the drive's `ssh` from the host and its `dir` from the session. Everything else reads `fleet["hosts"]`:

| What | Where | Fact |
|---|---|---|
| ssh to a host | `crew.on_machine`, `plan.forwarded`, `plan.opener`, `hold.fan` (484) | host `ssh` |
| a Mac or not | `crew.main_tokens` (`SHOWING`, `TEAMS_DOORS`), `sites.url_of` (38) | host `kind` |
| a batch report on another host | `plan.py` rail rows (11683) | host `home` |
| a host crew may act on | `hold.hosts_named`, `ops.quiet` | the host is listed |
| where a host keeps a repository | `crew.kept`, `kept_at`, `kept_on`, `kit_kept`, `kits_kept`, `blueprints_on`, `session_checkouts`; `ops.kit_range`; `plan.py` rename (6710) | each session's `dir` and `repos` |
| crew on another host | `crew.crew_on` through `kept_on` | the sessions' `repos` |
| a drive's console | `crew.operator_session`, `standing`, `plan.console_cmd` | a session named for the label, its `dir` |
| the drives a host follows | `board.labels_here`, `hold.labels_here`, `record.follow` | sessions named for a label |
| accounts | `crew.main_tokens` (`MAIN_SESSIONS`), `page.where`, `subscriptions`, `on_subscription`, a drive page's sessions (615) | each session's `account` |

Only `ssh`, `kind`, a session's folder and its account are in record 0064's list. The rest is read today and has to come from somewhere too: which repositories a host keeps and their addresses, which hosts open a drive's console and in what folder, and a host's `home`.

**Which hosts run this crew.** deneb runs crew's main at version 6. Its teams file names all 27 of its repositories in `repositories`, the runner's. chuck-herdr-alpha (wldn), mac-studio and macbook-pro still hold version-2 files and a pinned older crew (read over ssh 2026-11-09). A person's Mac set up by Boomdrive runs a runner. deneb opens consoles of afterthought, agentplot, madswan and of wldn, whose main level runs on the box. swancloud's `lib/herdr-operator.nix` (03ca21db) runs `crew console up <session>` for each of a host's sessions that names a partition.

**Area pages this change touches:** `core.md` (`code.3`, `code.5`, `code.7`, `code.8`, `read.1`, `read.2`, `roles.9`), `teams.md` (`teams.2`, `teams.6`, `teams.10`), `plan.md` (`plan.18`, `plan.22`), `flake.md` (`flake.1`, `flake.2`, `flake.3`), `tests.md` (`tests.4`, `tests.10`, `tests.11`) and `docs.md` (`docs.2`, `docs.4`, `docs.7`). No rule page or record is edited here (`docs.7`, Decision 11).

## Goals / Non-Goals

**Goals:**
- crew loads and runs with no hosts file on the host, and reads none where one is present.
- Every fact crew reads of a host's drives and of the hosts that serve them is a key of the teams file, with no default.
- What crew does on deneb today stays the same, given the same facts in its teams file.
- crew's module declares and writes the new keys, so a host Nix configures gets them from options.

**Non-Goals:**
- Writing the file for a host Nix does not configure: `crew-makes-a-new-drives-state`.
- swancloud's module values and its console timer, which swancloud changes when it takes this release, and Boomdrive's setup.
- The operator brief's *Changing the drives*, which names swancloud's `lib/crew-teams.nix`, and the swancloud tokens behind it. On a host that keeps no swancloud checkout, the tokens already say so in words (`teams.10`).
- `repositories` and the runner's-clone rule (`crew-fetches-nothing-in-the-runners-clone`, `plan.18`), which stay as they are.
- Carrying any host's file to the new keys (the user's ruling of 2026-11-08: "build it the way it should be and then have agents fucking fix the data transition as necessary").

## Decisions

### 1. One file, at version 6

`crew.load` reads the teams file alone. `HOSTS`, `read_hosts`, `session_of` and `repo_in` go, and nothing under `plugin/` names `herdr-hosts.json` or `~/.config/swancloud/`. A file that lacks a new key is refused naming the key and the teams file's writer, as a file lacking `state` or `flume` is (`code.5`, `read.1`). The refusals name the fix in the words `load`'s other refusals use on the bolt when this is built: the bolt's `WRITER` if `fix/crew-names-each-drive-once--refusal-names-crews-own-module` has landed, else the machine's configuration as today.

The version stays 6. Keys are added, and none is renamed or moved.

Not taken:
- **Version 7.** A version marks a file crew refuses whole. Here a file without the new keys is already refused by key. An older crew reading a file with the new keys passes them unread (`load` keeps a drive's undeclared keys), so the machine's configuration can write them ahead of the release that reads them, and swancloud's change and crew's release need not land in one step.
- **Reading the hosts file where it exists.** Record 0064, option 3.

### 2. The hosts: `hosts`, each with exactly `ssh` and `kind`

`hosts` is an object keyed by host name, a name crew accepts (`code.4`), as `hostname -s` gives it. Each entry is exactly `{"ssh": <non-empty string>, "kind": "darwin" | "nixos"}`. Every drive's `machine` is a key. Other hosts may be listed too, for `crew hold <host>` and an environment's host. `crew.on_machine`, `plan.forwarded`, `plan.opener` and `hold.fan` take `ssh` from it. `main_tokens` and `sites` take `kind` from it. `hold.hosts_named` and `ops.quiet` check a named host against it, their words naming the teams file. A host the file does not list is refused where crew would reach it or read its kind, naming the host and `hosts` (`read.1`). The kind of the host crew runs on is read the same way. A host with no entry is neither a Mac nor not one.

`home` is not carried (Decision 7). Neither are the hosts file's `supervised`, `roamgate` and `registered`, which crew never read.

Not taken:
- **`home` in each entry.** Its one reader can do without it.
- **`kind` as any string.** crew reads only whether a host is a Mac. Taking the two kinds the family's hosts are, and refusing others, keeps a typo from reading as "not a Mac".

### 3. A drive's `folder`, `repos` and `accounts`

Each drive gains three keys, each required:
- `folder`: an absolute path, the folder of its herdr session on its machine. It is where the drive keeps the repositories its `repos` lists (Decision 4). It is what the hosts file's session `dir` was.
- `repos`: a list of addresses, `<owner>/<name>`, possibly empty: the repositories its folder keeps on its machine. It is what the session's `repos` was. A runner host whose file names every repository under `repositories` may give an empty list.
- `accounts`: an object naming exactly the five roles of `KIND_ROLES` (`design`, `planner`, `reviewer`, `ops`, `operator`), each a name crew accepts, the Claude account the role runs under.

`load` checks each and refuses as the main-level spec says. The first blueprints repo must be kept on the drive's machine: among its `repos`, or named in `repositories` where the machine is this host. That keeps `repo_in`'s check, now on the file's own facts. Two roles whose sessions (`role_session`) are one and whose accounts differ are refused. A herdr session runs under one account, and the page shows one account per session. The drive's entry keeps `ssh` from its machine's `hosts` entry, and `folder` in place of the session's `dir`. Its `checkout` is the first blueprints repo where its machine keeps it (Decision 4).

`repos` is not in record 0064's list. It is the one fact of the hosts file's spaces crew cannot do without: which repositories a drive's folder keeps, and each one's owner, for a kit the plan names by its name alone. Without it, crew could not name wldn's kits on chuck-herdr-alpha from deneb, or find crew's checkout there (Decision 5). It is what Boomdrive's record 0028 already gives ("each drive its repositories").

Not taken:
- **Reading the folder from disk**, each `<folder>/*/main` a kept repository, with its address read from its `origin`. That reads only this host, so another host's kits could not be named, and a git process per checkout runs on every view's read.
- **`repositories` alone**, every host's kept repositories under the runner's key. A repository named there is the runner's clone, where crew fetches nothing (`plan.18`). On a host with no runner, and in every end-to-end test, crew would stop fetching kits a runner does not fetch.
- **Accounts per session, in a host's sessions.** That is the hosts file again, which record 0064 reshapes by drive ("the Claude account each role runs under").
- **Accounts only for standing roles.** A role that runs as its kind is still the drive's, and `accounts` is keyed as `flume` is, every role named.

### 4. Where a host keeps a repository

`kept_at(fleet, host, drive, repo)` is the `repositories` entry where the file names the repository and the host is this one. Otherwise it is `<folder>/<name>` and `<folder>/<name>/main` in that drive's folder. `kept(fleet, host)` lists the `repositories` entries first, where the host is this one, then each repository in the `repos` of each drive whose machine is the host, in the file's order, at its first drive. `kept_on`, `kit_kept` (and its two-by-one-name refusal), `kits_kept` and `blueprints_on` read `kept` as before. `session_checkouts` goes. `ops.kit_range` reads the checkouts `kept` gives the drive's machine. The rename (`plan.py` near 6710) gives `rename_kept` each host's `kept` addresses: for this host, and for any host a drive runs on, and `None` for any other. Its words name the teams file where they named spaces. This is record 0061's structure, its spaces fallback replaced by the drives' folders.

A repository that only a session with no drive kept (the hosts file's `willdan` session on deneb, `agentplot-2` on mac-studio) is no longer kept by crew. No drive works in it.

### 5. crew on another host

`crew_on` finds crew's checkout on another host through `kept_on`, as now (Decision 4), so the `repos` of a drive on that host must list crew's repository. Its refusal says the host keeps no checkout of crew's repository as the teams file gives it. Nothing else changes: `crew_at`, `crew_argv` and the `found` read at 619.

Not taken:
- **A `crew` path in each host's entry.** It would be a second place a host's crew checkout is named, beside `repos`.
- **`crew` from the far host's login PATH.** It is a fact read from a shell's environment, and it would run the far host's installed crew, not its checkout, which changes what runs there.

### 6. Consoles: `consoles`, for the host the file is written on

`consoles` is an optional object, written for the host the file is written on as `repositories` is. It maps a drive's label to the absolute folder its console's tabs open in on this host. `load` refuses a label no drive has, and a folder that is not absolute. `operator_session` becomes the console's place on this host: the session named for the label, as today, and the folder `consoles` gives. A drive this host's `consoles` does not name is refused, naming the drive, the host and `consoles`. `standing` takes that folder as the console's `cwd`. `board.labels_here(fleet, host)` and `hold.labels_here` become the drives `consoles` names, in the file's order, where the host is this one, and none elsewhere. The follower, `record.follow` and `crew go` read them unchanged.

deneb keeps wldn's console, whose main level runs on chuck-herdr-alpha. swancloud's timer opens one console per session that names a partition, and fills `consoles` from the same sessions. A person's Mac gets its drive's console from setup.

Not taken:
- **A console on the drive's machine alone, in its `session`.** deneb would lose wldn's console, rail and board, the user's only view of wldn from a crew that reads drives.
- **Asking herdr which sessions run** (`herdr --session <label> status server`). `record.follow` reads `labels_here` every second, so herdr would be asked once a second per drive. The console's folder on a host that is not the drive's machine would still be unknown.
- **The drive's `folder` on every host.** That is a path on the drive's machine. deneb's wldn console opens in `/Users/chuck/Code/clients/github_willdan`, not wldn's `/workspace`.

### 7. A batch report on another host is opened by a path under its home

The rail's batch row (`plan.py` near 11683) names a report on the drive's main-level host as `.local/state/crew/<label>-main/reports/batch-<label>-<n>.md` where that host is another one. `opener` runs `ssh -t <ssh> plannotator-tui <path>`, and ssh starts the command in the user's home there, so the relative path opens the same file. The row's open command is there for every batch whose host the file lists. Today a host's missing `home` drops it.

### 8. A session's account

`main_tokens`' `MAIN_SESSIONS` names each role's session with its role's account, which every role now has. `page.where`, `subscriptions`, `on_subscription` and the drive page's sessions (`page.py` 615) read a session's account as the account of the drive's roles in it (Decision 3 makes them one). A subscription's accounts are every account a drive's `accounts` gives, beside those readings name. `NO_ACCOUNT` and a session "running no crew agent" go: crew knows only the sessions its roles run in. The page's data shape is unchanged.

### 9. A role's session is checked against nothing

`roles.<role>.session` names a session of the main level's machine (`teams.6`). crew no longer holds a list of a host's sessions, so it checks the name as a non-empty string and the session's account (Decision 3). herdr runs what the file names.

### 10. crew's module declares the keys

`nix/modules/options.nix` declares `settings.hosts` (`attrsOf` a submodule of `ssh`, `types.nonEmptyStr`, and `kind`, `types.enum [ "darwin" "nixos" ]`, with no free-form type and no default) and `settings.consoles` (`nullOr (attrsOf absolute)`, unset by default, so the file has no key). Each `drive` declares `folder` (`absolute`), `repos` (`listOf repository`) and `accounts` (a submodule of the five `kindRoles`, each `crewName`, with no default). Cross-key checks, such as a machine with no host, a blueprints repo not kept or two accounts in one session, are crew's at load. The module types each key, as it does `flume`, and does not join them. `json.nix` is unchanged: `builtins.toJSON` orders keys, and nulls are left out. `nix/tests/settings.nix` gives deneb's drives, hosts and consoles the values deneb's hosts file gave on 2026-11-09 (Task notes 2.1). `deneb.json` and `runner.json` are written again from them. The logic tier loads both with no hosts file.

### 11. No record and no rule is written here

The rules and records are the design agent's (`docs.7`). Once this lands, the design agent amends these:
- `code.5`: add `repos`, `consoles` and the `hosts` entry's exact keys to its list.
- `teams.6`'s details: a role's session is "checked at load against the hosts file".
- `roles.9`: swancloud's spaces.
- `flake.2`'s details: its list of keys with no default.

It also writes the record of this design's own choices (Decisions 3 to 7) if it keeps them. Each is cheap to change before swancloud and setup write the keys.

### Departures

- Record 0064 lists four facts. This change adds three more: `repos` (Decision 3), `consoles` (Decision 6) and the `hosts` entry's `kind` values. Each is a fact the hosts file gave and crew reads, under the record's "everything it needs of the hosts that serve them". `code.5`'s list is amended after the landing (Decision 11).
- `teams.6`'s details check a role's session against the hosts file. This change checks it against nothing (Decision 9).
- `openspec/config.yaml` asks that the last task run `tests/suite --affected`. This change's stage brief asks that no task run the repository's whole checks, which `--affected` is for any change to crew's command core (CLAUDE.md, *Tests*). So the verify stage runs them once, after the last task.

## Risks / Trade-offs

- [deneb, on a release carrying this, refuses every command until its file gives the new keys] → The refusal names the key and the writer. swancloud writes the keys first, which an older crew ignores (Decision 1), then takes the release. On a host that loads crew live (`plan.19`), the timer can bring crew first, and the host is refused until swancloud's deploy. This change's caller tells swancloud's design agent, with the values in Task notes 2.1.
- [swancloud's console timer runs `crew console up` for a session `consoles` does not name] → It is refused and logged each time, until swancloud fills `consoles` from the same sessions it starts consoles for.
- [A kit kept only in a session no drive has stops being kept] → Decision 4. On deneb every kit is named in `repositories`. In the end-to-end tests, the mac-studio checkout of atlas-kit is moved or named (Task notes 4.2–4.23).
- [`fix/crew-names-each-drive-once--refusal-names-crews-own-module` lands first and changes `load`'s refusals and the main-level requirement this delta modifies] → Decision 1 takes its wording. The verify stage validates this delta against the specs as they stand when it runs, and carries the fix's words into the MODIFIED block if the fix archived first.
- [`repos` and `repositories` read alike] → The one is a drive's list of addresses and the other the host's map to folder and checkout. README says so (Task notes 5.1).

## Migration Plan

None in crew. A host moves when its configuration writes the new keys: swancloud from its list of hosts through crew's module options, Boomdrive's setup through `crew-makes-a-new-drives-state`. Rollback is the earlier release, which reads the hosts file and ignores the new keys.

## After deploy

None: every scenario is proved by a check in crew's tiers. Moving each host's file is swancloud's change or setup's, done by whoever writes it.

## Task notes

**1.1** `plugin/lib/crew.py`: drop `HOSTS`, `read_hosts`, `session_of`, `repo_in`. Add `hosts_of(data)`, checking `hosts` as Decision 2 says. In `load`, per drive: `folder` (a string starting `/`), `repos` (a list, each matching `ADDRESS`), `accounts` (`set(a) == set(KIND_ROLES)`, each `NAME`), `machine in hosts`, the first blueprints repo kept (Decision 3), and two accounts in one session refused across `MAIN_STANDING + ("reviewer",)` by `role_session`. Then `consoles_of(data, labels)`. The fleet is `{"hosts", "drives", "repositories", "consoles"}`, `consoles` being `{label: folder}`. A drive keeps `ssh`, `folder`, `repos`, `accounts`, `checkout`, `roles`, `flume` and `sessions`, and no `dir`. Every refusal names the field, the drive or host, and the fix as `load`'s other refusals name it. `this_host()` is read only where `repositories` or the blueprints check needs it. Update `load`'s and `this_host`'s docstrings and the module's header comment. `tests/py/test_teams.py`: its `hosts` fixture goes, and `data` gives `hosts`, `folder`, `repos` and `accounts`. Add cases for each main-level scenario this delta adds or changes: no hosts file; a hosts file present and read for nothing; a missing `folder`, `repos`, `accounts` or `hosts`; a relative folder; an account left out; two accounts in one session; a blueprints repo not kept; a machine with no host; a host entry named wrongly; a role's session of another drive loading; `consoles` naming no drive. Decision 4 is built here too, since `load` names each drive's checkout through it and the briefs read it: `kept_at(fleet, host, drive, repo)`, `kept`, `kept_on`, `kit_kept`, `kits_kept` and `blueprints_on` by Decision 4, `session_checkouts` removed. And `crew.main_tokens`: `MAIN_SESSIONS` from `p["accounts"]`; `TEAMS_DOORS` and `SHOWING` from `fleet["hosts"][h]["kind"]`, refusing (`teams.10`) where the host has no entry; `FOLDER` from `kept_at(fleet, p["machine"], p, p["blueprints"][0])["dir"]`; the `sess` lookup goes; and its cases in `tests/py/test_teams.py` (near 327 to 371) give the new keys.

**1.2** `kit_kept`'s words name the teams file where they named spaces. `tests/py/test_kits.py` and `tests/py/facts.py`'s `keeping` give drives with `folder` and `repos` in place of sessions. Cases: drive-state's scenarios as modified, and a repository kept only by a session with no drive is not kept.

**1.3** `crew_on`'s refusal (Decision 5); `crew.on_machine`, `plan.forwarded`, `plan.opener` and `hold.fan` take `fleet["hosts"][host]["ssh"]`, refusing a host the file does not list. `tests/py/test_crew_on.py`'s fleets give drives with `repos`. Cases: crew-command's scenarios as modified, the refusal's words among them, and a host with no `hosts` entry.

**2.1** `nix/modules/options.nix` by Decision 10: the `host` submodule (`ssh`, `kind`) and the `drive` options `folder`, `repos` and `accounts`, and `settings.hosts` and `settings.consoles`, each described as the file names it. `nix/tests/settings.nix` gives each of deneb's drives `folder`, `repos` and `accounts`, and gives `hosts` and `consoles`, from deneb's hosts file read 2026-11-09:
- afterthought: folder `/Users/chuck/Code/github_afterthought`, repos `afterthought/blueprints`, `afterthought/paymaster`, `afterthought/swancloud`, every account `madswan`.
- agentplot: folder `/Users/chuck/Code/github_agentplot`, repos the 24 of deneb's `agentplot` session, `agentplot/agentplot` to `agentplot/weir` as the hosts file lists them, every account `madswan`.
- madswan: folder `/Users/chuck/Code/github_afterthought`, repos as afterthought's, every account `madswan`.
- wldn: folder `/workspace`, repos `agentplot/crew`, `WilldanGroup/atlas-kit`, `WilldanGroup/aws-bootstrap`, `WilldanGroup/breadboard-kit`, `WilldanGroup/switchboard-kit`, `WilldanGroup/willdan-blueprints`, `WilldanGroup/willdan-sandbox`; `planner` and `reviewer` `ia` (session `wldn-1`), `design`, `ops` and `operator` `willdan-alex` (`wldn-2`).
- `hosts`: `deneb` (`ssh` `deneb`, `kind` `darwin`) and `chuck-herdr-alpha` (`ssh` `chuck-herdr-alpha`, `kind` `nixos`).
- `consoles`: `afterthought` and `madswan` at `/Users/chuck/Code/github_afterthought`, `agentplot` at `/Users/chuck/Code/github_agentplot`, `wldn` at `/Users/chuck/Code/clients/github_willdan`.

The host's settings in the "from two modules" case give the new drive keys, `hosts` and `consoles`, as that case says. `nix/tests/file.nix` gains the crew-flake delta's failing cases (no hosts; a `kind` of `macos`; a `home` beside `ssh` and `kind`; a drive with no `folder`, `repos` or `accounts`; a relative folder; an account left out; a relative console folder) and its no-consoles case. Write `nix/tests/files/deneb.json` and `runner.json` again as the module renders them, one line each, the bytes `nix:test` compares.

**2.2** `nix/tests/typecheck.nix`, `darwin.nix` and `nixos.nix` read the settings 2.1 gives; any system they build gives the new required keys.

**2.3–2.4** The nix files 2.1 and 2.2 touched, as nixfmt, statix and deadnix leave them.

**2.5** `tests/py/test_module_file.py`: its `hosts` fixture goes, and it loads `deneb.json` and `runner.json` with no hosts file, asserting wldn's accounts as crew-flake's scenario says and the four consoles.

**3.1** `plugin/lib/page.py`: Decision 8. `NO_ACCOUNT` and `account_said`'s none case go. `where`, `subscriptions`, `on_subscription` and the drive page's `sessions` read `p["accounts"]` through one helper giving a session's account from its roles. `tests/py/test_page.py` and `test_fleet.py`: fleet-page's and board-page's scenarios as modified.

**3.2** `plugin/lib/sites.py` `url_of`: the kind of the host crew runs on from `fleet["hosts"]`, saying it can't tell where the file lists no such host (`read.1`). `plugin/lib/ops.py`: `kit_range` reads the checkouts of `crew.kept(fleet, p["machine"])`, and `quiet` names the teams file's hosts. `tests/py/test_ops.py`, and a case of `url_of`'s note in the logic file that covers sites (`git grep -n url_of tests/py`), else in `tests/py/test_page.py`.

**3.3** `plan.op_kit_rename`: `spaces` becomes each host's `kept` addresses where the host is this one or a drive's machine, else `None`; `rename_kept`'s words and docstring name the teams file. `tests/py/test_repository_rename.py` and `test_kit_rename.py`: bolt-plan's scenarios as modified.

**3.4** `plan.rail_rows`: Decision 7. `tests/py/test_rail.py`: a batch on another host opens by the relative path over the host's `ssh` name.

**3.5** `crew.operator_session` gives the console's folder on this host from `fleet["consoles"]`, refusing as Decision 6 says; `standing` uses it; `board.labels_here` and `hold.labels_here` read `fleet["consoles"]` where the host is this one; `plan.console_cmd`'s docstring. `tests/py/test_board.py` (its `labels_here` case near 395 rewritten to `consoles`), `tests/py/test_console.py` and `tests/py/test_hold.py`: operator-agent's added scenarios.

**3.6** Every other logic case that builds a fleet with a hosts file's `sessions` or reads `crew.HOSTS` builds it from the teams file's facts (`git grep -n -E '"sessions"|HOSTS|herdr-hosts' tests/py`): `test_asks.py`, `test_bolt_submissions.py`, `test_cards.py`, `test_tell_asks.py`, `test_proposals.py`, `test_release.py`, `test_batch_answer.py`, `test_card_commands.py`, `test_source.py`, `test_fleet.py`, `test_landing.py`, `test_review.py`, `test_signals.py`, `test_proposal_card.py`, and any other it lists.

**3.7** `tests/contract/test_git.py` and `test_record.py` build their fleets the same way.

**4.1** `tests/lib.sh`: `hosts_json` and the hosts file go. `teams_json <host>` writes each simulated host's file: `hosts` for both hosts (`kind` `nixos` for the box, `darwin` for mac-studio; `ssh` their names); each drive's `folder` and `repos` as its session's `dir` and `repos` were; `accounts` from the sessions' accounts, chosen so the fleet page's subscriptions are still credits, ia, madswan and willdan-alex (`t-journey-board` 330); `consoles` for the drives with a session named for their label on that host (mac-studio: wldn, madswan, swancloud; the box: wldn) at that session's `dir`. `fixtures` writes each host's own. `teams_old` builds on `teams_json mac-studio`. `kit()` reads a kit's owner from the drives' `repos` in the host's teams file. `edit()` loses its `hosts` case. `tests/run`'s header comment. `tests/t-teams.sh`: its hosts-file edits (62 to 69) become a hosts file present and read for nothing, a blueprints repo dropped from wldn's `repos` refused, and a missing `folder` refused.

**4.2–4.23** Each end-to-end test named proves its case with the new fixture. In `t-journey-board` and `t-journey-review`, the mac-studio checkout of atlas-kit at `work/willdan`, which no drive on mac-studio keeps, is named in mac-studio's `repositories` or made under a drive's folder there, whichever keeps what the test proves. `t-journey-plan`'s `edit hosts` near 297 becomes the teams file's edit of the same fact. `t-hold` and `t-journey-main` open consoles `consoles` names. `t-briefs` expects each role's account. The rest need only the fixture.

**5.1** `README.md`: its opening list and *The main level* name the teams file as the one file, its `hosts`, each drive's `folder`, `repos` and `accounts`, and `consoles`, with no hosts file. *The flake* lists the new options. One sentence tells `repos` from `repositories`. `plugin/skills/crew/SKILL.md` likewise (line 84). `openspec/config.yaml`'s context drops "hosts and sessions come from swancloud's ~/.config/swancloud/herdr-hosts.json". `docs.2`: README, the skill and the usage say the same.
