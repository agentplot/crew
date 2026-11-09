# crew runs from its own file alone

## Why

crew reads two files: its own teams file and swancloud's `~/.config/swancloud/herdr-hosts.json`. `crew.load` refuses to start without the second ("is missing; swancloud's home-manager writes it"). A person's Mac set up by Boomdrive's setup runs no swancloud, so it has no hosts file, and no tool may write another's file. Record 0064 (accepted 2026-11-09 by agentplot-design, carrying the user's choice in agentplot/boomdrive record 0009's amendment of that day, that a colleague's Mac runs their own drive with crew "the same way I'm working today") decides:

> crew reads a host's drives, and everything it needs of the hosts that serve them, from its teams file alone, on every host: each drive's machine, its herdr session and folder, the Claude account each role runs under, and each host's kind and ssh name. It reads no file of swancloud's or of any fleet's.

`code.5` already says so. This change builds it. `crew-makes-a-new-drives-state` follows it in the bolt, so a new drive's entry written at setup's asking holds every fact crew then reads.

## What Changes

- **BREAKING** crew reads no hosts file. `crew.load` reads every fact of a host's drives from `~/.config/crew/teams.json`, and refuses a file that lacks one, naming the key and the teams file's writer, with nothing done. The file stays at version 6.
- The teams file gives:
  - `hosts`: each host crew reaches or reads, by name, with exactly its `ssh` name and its `kind`, `darwin` or `nixos`. Every drive's `machine` is one of them.
  - for each drive, beside its keys today: `folder`, the absolute folder of its herdr session on its machine; `repos`, the repositories that folder keeps, each by its address; and `accounts`, the Claude account each of its five main-level roles runs under.
  - `consoles`, for the host it is written on: the drives whose console that host opens, each with the folder its tabs open in.
- Where a host keeps a repository is the teams file's `repositories` entry, for the host it is written on, and otherwise `<folder>/<name>` of a drive on that host whose `repos` lists it. This is the layout the hosts file's sessions gave, with the drive's folder in place of a session's.
- crew on another host is still the checkout that host keeps of crew's repository, now found by the drives the teams file puts there.
- ssh names, a host's kind and the accounts shown in briefs, on the fleet page and on a drive's page all come from the teams file. A session's account is the one its roles name, and two roles in one session that name two accounts are refused.
- A drive's console opens only on a host whose `consoles` names it, in the herdr session named for the label, in the folder given. A host's follower, and `crew go`, act on the drives its `consoles` names.
- A batch's report on another host is opened by its path under the home that ssh starts in, so crew needs no host's `home`.
- A role's `session` is no longer checked against a list of sessions. The teams file names it, and herdr runs it.
- crew's module declares `services.crew.settings.hosts`, `consoles`, and each drive's `folder`, `repos` and `accounts`, with no default for any, and its pinned files hold them.
- The end-to-end tests write no hosts file. Each simulated host's teams file gives these facts.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `main-level`: the teams file declares every fact of a host's drives: the hosts, each drive's folder, repositories and accounts, and the consoles of the host it is written on. No hosts file is read.
- `crew-command`: crew runs itself on another host from the checkout the teams file puts there.
- `drive-state`: before a runner takes a kit's work, the kit is found where the teams file keeps it on the main-level host.
- `bolt-plan`: a rename reads a host's keeping from its runner, else from the teams file.
- `fleet-page`: subscriptions and each drive's sessions take their accounts from the drives' roles.
- `board-page`: a subscription's dock lists the drive's sessions whose roles name that account.
- `operator-agent`: a host opens the consoles its teams file names, in the folder it gives.
- `crew-flake`: the module declares and writes the new keys, with no default.

## Impact

- **Code**: `plugin/lib/crew.py` (`load` and its checks, `HOSTS`, `read_hosts`, `session_of` and `repo_in` gone; `kept_at`, `kept`, `session_checkouts`, `on_machine`, `operator_session`, `standing`, `main_tokens`), `plugin/lib/plan.py` (`forwarded`, `opener`, a batch row's report path, the rename's keeping), `plugin/lib/hold.py`, `plugin/lib/ops.py` (`kit_range`, `quiet`), `plugin/lib/page.py`, `plugin/lib/sites.py`, `plugin/lib/board.py` (`labels_here`).
- **Module**: `nix/modules/options.nix`, `nix/tests/settings.nix`, `nix/tests/file.nix`, and `nix/tests/files/deneb.json` and `runner.json` written again as the module writes them.
- **Tests**: `tests/lib.sh` (no `hosts_json`, and a teams file for each host), `tests/run`'s comment, every logic case that builds a fleet with a hosts file's sessions, and the end-to-end tests that edit the hosts file or rely on a session that is no drive's.
- **Docs**: README, the crew skill, `openspec/config.yaml`'s context, and the briefs' account words where they change.
- **Views and mod** (`code.8`): the agents' views and `plugin/hooks/status.js` show nothing this changes. A session's account and a host's kind are not drawn in a band, so neither changes.
- **Unchanged**: the version of the teams file, `repositories` and the runner's-clone rule (`crew-fetches-nothing-in-the-runners-clone`), and what crew writes.
- **Other repositories**: afterthought/swancloud gives crew these facts through crew's module options on each host it configures, filled at build time from its own list of hosts (record 0064's consequence), in the change that takes the crew release carrying this. Its herdr-operator timer then calls `crew console up` only for the consoles it writes into `consoles`. Boomdrive's setup gives them on a host Nix does not configure, through crew's command (`crew-makes-a-new-drives-state`). This change's caller passes both on.
