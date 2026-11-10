# A follower follows on the crew its host has installed

## Why

On deneb on 2026-11-08, from 22:42Z (17:42 local), crew withdrew agentplot's landings card for flume and posted it again every sweep, for a row that never changed (flume-launches-a-conflicting-bolts-fix can land at 06ab3bc; a-tidied-places-end-stays-readable waits on batch 16): req_ddea1736, req_c4f94b96, req_c6b8e5cd and req_03a4c8c7 each withdrawn, "nothing waits to land on flume's main", and the next sweep printing "land/flume (agentplot), agentplot-ops's req_03a4c8c7e44e419faa40: posted: its row had none open" (signal 2026-11-08-agentplot-ops-2411bbac/01). rail-cards' requirements "A row's card is changed in place when its thing changes" and "A row taking main first changes the card in place" rule this out.

The run record and the host name the second reader. Every withdrawal is one process's, `deneb-66134-*`, and every post a crew command run in agentplot-ops's session on the installed crew. Process 66134 is `board.py _rail agentplot` from `/nix/store/…-crew-0.41.0-unstable-2026-11-06`, a console rail tab opened on 6 November. At 22:41:30Z swancloud's deploy started its `crew-follow` job again on crew 0.46.0; in the second between the old job's end and the new one's start the old tab took the host's follower lock (`tab agentplot 66134 2026-11-08T22:41:31Z`), and the new job waits on it. So the host's one follower ran crew 0.41.0, whose read has no land/flume row (its rail frame lists sluice's and crew's landings and no flume's), and judged the card's row gone each sweep, while every crew command on the host, 0.46.0, read the row with no card and posted one.

A follower watches the crew the host has installed for a move (host-holds-and-updates, "An install moves while an agent sits idle"), comparing the installed command's real path at each refresh with its own last stamp. It never compares the install with the crew it runs itself. A follower that takes the lock already behind the install, as a tab opened before it does, keeps following on its old crew until the host installs another.

## What Changes

- **A follower follows on the installed crew.** Each refresh, the first one included, a follower checks whether the crew it runs is the one the host has installed. It compares its own build's release with the installed crew's answer to `crew _release`, asked once for each real path of the installed command. If they differ, it hands out the restarts due and starts again through the installed command, its lock handed on, before it reads a row or judges a card. A follower whose command is the installed one, as a checkout's always is, or on a host with no crew installed, asks nothing.
- **Nothing is started again on a guess.** If either commit can't be read, the follower follows on as it is. One started again for this that still reads another crew says so once and follows on as it is, so it is never started again for it twice.
- README says so beside the follower's lock.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `crew-board`: two new requirements, "A follower follows on the crew its host has installed" and "A follower starts again for its crew only on what it read".

## Impact

- `plugin/lib/board.py`: `behind`, `behind_here`; `refresh_plan` takes the lag; `Follower.lagging`, `Follower.again`'s `lag`, `CREW_FOLLOWER_LAGGED`.
- `tests/py/test_board.py`: `TestFollower`, `TestInstalledCrew`, `TestRefresh`.
- `README.md`, the follower's paragraph.
- Unchanged: the rows, the cards and their sweep, which judged rightly on the crew that ran them; crew's mod and the views (`code.8` not reached), since nothing crew models changes shape.
- The tab running 0.41.0 on deneb predates this change and can't take it up. It holds the lock until it is closed or ended, and swancloud's job then follows on the installed crew.
