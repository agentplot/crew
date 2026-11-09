# The operator's brief names no drive removal by setup

## Why

The operator's *Changing the drives* says that where a host's teams file is no link into the Nix store, a drive is "added, changed or removed through Boomdrive's setup", which gives crew the drive's entry with `crew drive set`. Neither source of that path provides a removal. agentplot/boomdrive record 0009's amendment of 2026-11-09 names as setup's later changes "Adding or removing a repository of the drive", and asks crew to "make a new drive's state and name the drive in its own file". crew record 0065 says: "A drive is not removed by this command. … It asks for no drive's removal, and nothing builds one. The operator's brief says only what setup can do." So the brief tells the operator, and through it the user, of a step that no tool runs.

## What Changes

- The operator's brief says a drive is added or changed through Boomdrive's setup with `crew drive set` where the teams file is no Nix link, and names no removal of a drive there.
- `t-briefs` pins the words and that the brief names no removal through setup (`tests.6`).

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `operator-agent`: "The operator's brief says who changes the drives on its host" says a drive is added or changed through Boomdrive's setup, and that the brief names no removal of a drive through setup.

## Impact

- `plugin/roles/operator.md`, *Changing the drives*.
- `tests/t-briefs.sh`.
- The views keep their shape (`code.8` not reached). No command changes, so README, the crew skill and `crew`'s usage are untouched (`docs.2`).
- Other repositories: none. Boomdrive's setup is unchanged; what it may later do for a removal is its own design.
