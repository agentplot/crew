# Proposal

## Why

On deneb on 2026-11-07 agentplot-ops read crew's board follower, `board.py _follow` (pid 20914, crew 0.41.0-unstable-2026-11-07), at 3m08s of CPU in 20 minutes, about 15% of a core, in bursts at each tick up to 97%, with five `sluice overview --json --watch` children and a fresh ssh to chuck-herdr-alpha each pass. Earlier it held a quarter of a core all the time, the host's biggest watcher (signal 2026-10-30-crw-6-conductor-e626c6ea/01). Read again here the same day, the follower did a whole read every twenty to forty seconds: each refresh, whatever moved, asked chuck-herdr-alpha for its kits' stamps over ssh and gathered one of its kits again; each tick asked Pending You and herdr in a bridge, read portless and fetched each partition's branches one fetch at a time, three times over for afterthought's state repository; and a card the last sweep left counted the cards as moved at every tick, so the follower's refused closes of swancloud-planner's batch cards, written as entries, moved madswan's branch and read everything again (1,756 refused `card.close` entries on madswan's deneb run record that day).

A follower's tick should cost nothing while nothing it reads has moved. sluice holds its own reader to that rule, core.31: a reader's tick that starts a process or reads an object while nothing changed is ruled out, and it asks the forge nothing but what the discovery due or a move on the host calls for. crew's own rule read.5 already says a host is read over ssh only for its kits.

## What Changes

- **A quiet tick starts nothing but its fetches.** When nothing the follower reads has moved, its tick fetches each repository once and starts no other process: no git besides, no ssh to another host, no sluice, no Pending You bridge, no herdr and no portless; it writes the frames again from its kept read.
- **Another host is asked only when something there could have moved.** This host's kits and card readings are stamped in the follower's process at each refresh, starting nothing. Another host is asked, in its one ssh, when the drive's branch of a partition with work there moved, when that host's runner's branch moved, when a watch of one of its kits printed or ended, when it did not answer the last time, and otherwise once in ten minutes; at a tick that asks it, it is asked for its dev servers and the overviews no watch follows in the same ssh.
- **Pending You and herdr are asked only when the cards could have moved.** At a tick, the follower asks after the cards its sweep acts on and their askers when one of them is new to it, when the last ask failed or herdr could not read an asker, and otherwise once in ten minutes, the card sweep's own retry; a card the last sweep left counts the cards as moved at the next ask, no longer at every tick.
- **One fetch for each repository.** The clock's fetch carries every branch the follower reads of a repository, each partition's branch with its runners' and the blueprints main, in one `git fetch`; a branch not yet made costs one fetch more.
- **One watch for each repository.** The follower keeps one `sluice overview --json --watch` for each repository whose queue its read shows on a host, two checkouts of one repository on this host sharing it (sluice's core.25: one reader of a repository's records on a host, every other watch following that reader).
- **A runner's report is a move.** The follower's look stamps each partition's runners' branches beside its own, so a runner's report of the places it runs, which arrives with no move of the partition's branch, is read at once.
- Unchanged: the rail's and the board's words, the frames and the agents' views, the one-minute clock, a write on this host shown within seconds, the batch reckoning at every refresh, and the card sweep's ten-minute retry of a refused card.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `crew-board`: the follower's quiet tick starts nothing but one fetch of each repository; its check asks another host only when something there could have moved; it asks Pending You and herdr only when the cards could have moved; it keeps one overview watch for each repository; and a runner's report is part of what it checks.
- `card-sessions`: a reading sent back on another host is swept at the follower's next refresh that asks that host, within ten minutes when nothing else moves there.

## Impact

- `plugin/lib/board.py`: the follower's check (`host_basis`, `hosts_due`, `Follower.check`, `Follower.answered`), its ask of Pending You (`cards_due`, `cards_stamp`), its fetch (`fetches`), its watches (`watch_key`, `Watches`), its look and `moved` (the runners' branches), `stamps_now`, `DISCOVERY`.
- `plugin/lib/plan.py`: `tips_of`, one fetch of several branches.
- `README.md`, `plugin/skills/crew/SKILL.md`, `plugin/bin/crew`'s usage, `board.py`'s header: the follower's words.
- Tests: `tests/py/test_board.py`, `tests/contract/test_git.py`, `tests/t-journey-board.sh`.
- Not this change: the follower's refused closes of another planner's cards, crew's card sweep acting in a name Pending You refuses, which is its own fix; sluice's own watchers.

## Touches

```
plugin/lib/board.py
plugin/lib/plan.py
plugin/bin/crew
plugin/skills/crew/SKILL.md
README.md
tests/py/test_board.py
tests/contract/test_git.py
tests/t-journey-board.sh
```
