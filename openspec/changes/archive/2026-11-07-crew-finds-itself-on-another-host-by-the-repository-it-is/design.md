# Design

## Context

This section records what was read on 2026-11-07 on deneb, so the decisions below rest on it.

**The refusal.** `crew_at(fleet, host)` gave the crew command on another host as the checkout of `afterthought/crew` that the host's sessions keep (`kept_on`). Every command that runs crew on another host goes through it: `crew_argv` for each forwarded command, `reach` for bash's forwarding (`code.3`), and `read_agent` for a tell's reading of an agent on another host. The hosts file now keeps `agentplot/crew` in every space that keeps crew: chuck-herdr-alpha's wldn sessions and deneb's agentplot session. So each such command was refused on the box.

**What crew's install carries.** deneb loads crew released, at the teamless pin (`plan.19`, swancloud `packages/crew/default.nix`). The store path `crew-0.41.0-unstable-2026-11-07` holds `plugin/` alone, copied whole from the commit, with no `.git`. So a released crew cannot read its own address from git. Its manifest, `plugin/.claude-plugin/plugin.json`, is in every install, because the fleet copies the `plugin` folder whole and its install check reads that very file.

**The fleet's declaration.** swancloud declares crew's home in its package's `fetchFromGitHub { owner = "agentplot"; repo = "crew"; }`, in its meta's `homepage`, and in `lib/release-sources.nix` (`github:agentplot/crew`). It writes none of these anywhere a host reads at run time. The hosts file lists `agentplot/crew` among a session's repositories, but nothing there says which of them is crew.

**The family.** Flume's Claude Code plugin names its own repository in the same manifest field, `"repository": "https://github.com/agentplot/flume"`. No other tool of the family runs itself on another host from a checkout there, so crew owns this behaviour and there is nothing to reconcile.

**Area pages this change touches:** `teams.md` (for `plugin/lib/crew.py`), `tests.md` (`tests.4`, `tests.10`, `tests.11`) and `docs.md` (`docs.4`, `docs.6`). From `core.md`: `code.3`, `code.7` and `read.1`. From `plan.md`: `plan.22` (proposed, record 0058), under which no reader maps a former name. No rule changes, so no page is edited (`docs.7`).

## Goals / Non-Goals

**Goals:**

- Every command that runs crew on another host finds crew there under the address crew has now.
- crew's address is read from what crew is, never from a name in its code, so the next move of crew changes no code.
- A host that keeps no checkout of crew is refused naming the repository crew looked for (`read.1`).

**Non-Goals:**

- Running another host's own released crew in place of its checkout. `crew_at` runs the checkout, as `teams.19`'s details read it.
- crew's other repositories named in code, such as `afterthought/swancloud` in `main_tokens`. They are not crew's own address.
- The kits' and records' fixtures in the logic tier that name `afterthought/crew` as plain data. No decision there reads crew's own address.

## Decisions

### Decision 1: crew's address is its manifest's `repository`

crew reads the repository it is from `repository` in `plugin/.claude-plugin/plugin.json`, `https://github.com/agentplot/crew`, taking the owner and name from a GitHub address. That manifest is crew's own declaration of what it is. Claude Code reads it too, and every install carries it. It is the one place crew's address is written, so the next move changes that line alone, in the move's own commit.

Paths not taken:

- *The checkout's origin remote.* A released install has no git (Context), and deneb, the host of the reading, runs released.
- *The fleet's declaration.* swancloud writes crew's home nowhere a host reads. Reading it would need a swancloud change, and it would be a second source beside the manifest. The manifest is what the fleet copies, so the fleet's install carries crew's own word already.
- *Mapping `afterthought/crew` to `agentplot/crew`.* Ruled out by `plan.22` and the user's no-renaming rule (record 0055, rejected; record 0058).
- *Any repository by the name `crew`, as `kit_kept` finds a kit by name alone.* That is a name in crew's code again, and two spaces' repositories by that name would make it ambiguous.

### Decision 2: The decision is `crew_on`, on plain facts

`crew_on(fleet, host, here, repo)` gives this crew's command where `host` is `here`. Otherwise it gives the checkout of `repo` the host's sessions keep, or it refuses. `crew_at` reads `this_host()`, and reads crew's repository only for another host. So a command for this host never depends on the manifest (`code.7`). `repository_named(text, where)` parses the manifest's text. `crew_repository()` reads the file once a process.

### Decision 3: A refusal names what crew looked for

A host that keeps none: "none of <host>'s sessions keeps <repo>, the repository crew is, so crew can't run there". The callers already carry this text in their own words, as a tell's "Could not tell ...". A manifest crew cannot read, or one that names no GitHub repository, is refused naming the file (`read.1`, `code.2`). A checkout kept under a former address is simply not the repository crew is.

### Decision 4: The manifest is part of the command core

Every crew command that reaches another host reads the manifest. So `tests/moon-tasks` puts it in `CORE`, the inputs of every end-to-end task, and in the logic tier's inputs. The logic tier reads it and also scans `plugin/bin/` (`tests.10`).

### Decision 5: A check that crew's code names no address of its own

A logic case reads the modules under `plugin/lib/` and the commands under `plugin/bin/`, and fails if one names the manifest's address. So a fix that writes crew's address into code again fails its gate.

## Risks / Trade-offs

- [A released host loads crew's manifest as of its pin] → If crew moves again, a host on an older pin looks for the address that pin's manifest names, and it is refused naming that address until its pin moves. The refusal says what was looked for, and no former name is followed.

## After deploy

None. The fix reaches deneb when swancloud moves its teamless pin past this landing, and every other host with crew's main line once the merge back to main carries it there. Neither is a step of this change: each is the fleet's move on the user's word.

## Task notes

**1.1** `plugin/lib/crew.py`: `MANIFEST`, `GITHUB`, `repository_named`, `crew_repository`, `crew_on` and `crew_at`. `plugin/.claude-plugin/plugin.json` gains `repository`. Cases in `tests/py/test_crew_on.py`:
- crew found on chuck-herdr-alpha under `agentplot/crew`;
- a host that keeps none refused with the full message;
- a host keeping only `afterthought/crew` refused naming `agentplot/crew`;
- a repository of any address followed as given;
- this host given this crew with no repository asked;
- `crew_at` with `this_host` set to deneb finding the box's checkout from the real manifest, and reading no manifest for deneb;
- the real manifest giving `agentplot/crew`;
- the GitHub forms, with and without `.git`, a trailing slash, and `git@github.com:`;
- the refusals for no `repository`, a non-GitHub address, an object, an address with no name, text that is no JSON, and a JSON array;
- no file under `plugin/lib/*.py` or `plugin/bin/` naming the manifest's address.

**1.2** `tests/lib.sh`: `box_repos` and `mac_madswan` keep `agentplot/crew`, so `t-journey-main`'s `crew send wldn` from mac-studio reaches the box through crew's checkout found under its current address.

**1.3** `tests/moon-tasks`: `/plugin/.claude-plugin/plugin.json` is in `CORE`. The logic tier's inputs add it and `/plugin/bin/**/*`. Regenerate `tests/moon.yml`. `CLAUDE.md`'s Tests section names the manifest in the command core.
