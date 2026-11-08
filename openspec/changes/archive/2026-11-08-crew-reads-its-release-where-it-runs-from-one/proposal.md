# crew reads its release where it runs from one

## Why

A standing agent's brief names crew's command by the path of the crew that built it, `{HOME}/plugin/bin/crew`. On a host that runs crew from a build in the Nix store, that path names one build forever: once the host installed a newer crew, the standing agents kept running the build their sessions started on. On deneb on 2026-11-08 every afterthought agent's brief named `/nix/store/7292pjr3…-crew-0.41.0-unstable-2026-11-07`, older than the change that reads a unit merged from its bolt's landing (#479), while the installed crew was `1gmha0787…`; the agents read every landed unit as submitted, and a `crew rail` run from a brief twice closed swancloud's landings card as having nothing to land (signal 2026-11-08-agentplot-operator-451767f3/01: "Every afterthought agent's brief still names that build's path …, so any crew rail an agent runs from its brief withdraws cards the installed crew … raises").

And a build cannot tell what it is. crew reads its version and commit from git alone (`crew.crew_version`), so a start from a build records no commit, `update_due` reads such a start by its launch digest alone, and a new install makes no standing agent due a restart (`NO_COMMIT_SAID`; record 0050 as amended 2026-10-30). Worse, a session's hooks run from the plugin folder the session loaded, so the Stop hook that decides whether an agent is due runs the old build, which could only ever compare the agent's start with itself.

Record 0050 as amended 2026-11-08 says what must be true: a standing agent's crew commands run the crew the host has installed now, never the build its session started on, so a change to crew's code is live for every command at once (`teams.19`); and crew knows the release it runs from, so a change to what a session loads at its start makes each standing agent due a restart at its next stop. The hold on this unit is lifted, and crew's own flake builds the package that carries the release (record 0058).

## What Changes

- **crew's package carries its release.** The flake's package writes `plugin/release.json`, naming the commit the flake is built from and the package's version, when the flake knows its commit; a build from a tree with uncommitted changes carries none.
- **crew reads the release it runs from.** In a checkout, from git as today; in a build, from its release file; in neither, nothing, said where a decision rests on it. A build's version is `v<x.y.z>` where the package names a release, else the package's version with the commit's first seven characters, `0-unstable-2026-11-08+fcedc22`. A start records the release of the crew whose plugin the session loaded.
- **`crew _release`** prints what a crew is, its root, commit, version and where they were read from, as JSON, reading nothing else; it is how one crew reads another it cannot import.
- **crew names its command by the crew the host has installed.** Where crew runs from a checkout, its own `plugin/bin/crew`, as today; where it runs from a build, the first `crew` on its path in a folder outside the Nix store, a profile's link that each install moves; its own build's path only where it finds neither. Every place crew names its command for a later run follows: the briefs, a command forwarded to this host, the Stop hook's hand to `crew _renew`, the follower's Pending You notice, its `_update` and its start again, and the console's tabs.
- **The update check reads the installed crew.** A standing agent is due when its brief, model, effort or folders changed, as today; when the installed crew is a checkout and what a session loads changed between its start's commit and the checkout's, as today; and when the installed crew is a build of another release than its start recorded, since the session loaded that build's plugin folder whole and its hooks run from it. crew says it can't tell, and makes none due for crew's plugin, where it can't read the installed crew or the start recorded no release.
- **The launch digest reads crew's command as one word,** whichever path a brief names it by, so two crews of a host digest one start alike; every start made before this change reads as due once, which moves each standing agent onto a brief that names the installed crew.
- **The follower watches the installed crew.** On a host where crew runs from a build, the follower reads the installed command's real path where it reads a checkout's commit, and when an install moves it, hands out the due restarts and starts again as the installed crew.
- **Unchanged:** a checkout's reading of itself, the teams file, the views' shape and the mod, `crew-role`, and the reading of a host whose crew is a build that carries no release, which keeps today's words.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `host-holds-and-updates`: a standing agent's crew commands run the crew its host has installed; crew knows the release it runs from; an update is read against the installed crew; the follower catches an idle agent when the installed crew moves; the band shows a build's release.
- `crew-flake`: crew's package carries its release.

## Impact

- `plugin/lib/crew.py`: the release read (`crew_version`, `release_read`, `release_version`), the installed crew (`installed_command`, `crew_command`, `installed`), `crew _release`, `launch_digest`, `main_tokens` and `SENDS`, `crew_on` for this host, `update_due`, `due_of` and their words.
- `plugin/bin/crew`: the `_release` arm and its help.
- `plugin/hooks/session-start`: unchanged in shape; what it records follows `crew_version`.
- `plugin/lib/hold.py`: `hand`, `update_here` and `renew` on the installed crew.
- `plugin/lib/board.py`: `here_read`, `notice_argv`, `moved_at` and `Follower.again`.
- `plugin/lib/plan.py`: the console's tabs.
- `nix/packages/crew.nix`, `flake.nix`, and a new case in `nix/tests/`.
- README's *Holding a host, and updates* and *The flake*.
- Tests: `tests/py/test_release.py` (new), `tests/py/test_hold.py`, `tests/py/test_board.py`, `tests/t-session-hook.sh`, `tests/t-help.sh`, `nix/tests/`.
- Nothing crew models changes: the views keep their shape, so `status.js` is untouched (`code.8` not reached). Nothing outside the standard library is imported (`code.1`).
- A host takes the release reading once its installed crew and the plugin its sessions load are crew's flake's package; that is the host configuration's, Boomdrive's module or swancloud's, and asks nothing of crew.

## Touches

```
plugin/lib/crew.py
plugin/bin/crew
plugin/lib/hold.py
plugin/lib/board.py
plugin/lib/plan.py
nix/packages/crew.nix
flake.nix
nix/tests/default.nix
nix/tests/package.nix
README.md
tests/py/test_release.py
tests/py/test_hold.py
tests/py/test_board.py
tests/t-session-hook.sh
tests/t-help.sh
```
