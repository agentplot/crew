# Design

## Context

The host's follower is `board.py`'s `Follower`, as `a-rail-refresh-after-no-change-reads-nothing` built it (archived 2026-10-28): a look each second at this host's caches with no process, a refresh after a move, and a tick each minute that fetches the state and blueprints caches, asks Pending You and herdr after the cards, and refreshes. A refresh first checks what moved (`moved`) from stamps (`stamps_now`): this host's in the follower's process, every other host's in one ssh each, at every refresh. At a tick the same ssh brings each host's portless routes and the overviews no watch follows.

Read on deneb on 2026-11-07, pid 20914, over two minutes: a whole read every twenty to forty seconds, each with a stamp ssh to chuck-herdr-alpha and a gather there of switchboard-kit, whose stamp moved each time; at each tick seven `git fetch`es, three of them of afterthought/crew-state, one per partition, and a Pending You bridge; and refused `card.close` entries on madswan's branch, the follower's own, each moving the tip it follows. The cards counted as moved at every tick while the last sweep had left a card (`cards_stamp`'s `["again", tick]`), so a refusal that stands was tried at every tick's sweep, and the card sweep's ten-minute gate (`plan.CARD_RETRY`) was the only brake.

Rules this relies on: `read.5` (a host is read over ssh only for the stages of its own kits; every act reaches the drive's branch as it is written), `read.1` (what can't be read is not taken as unmoved), `state.4` (the follower's kept read is a derived cache), `plan.12` and its reading of 2026-10-28 (fetches on the clock alone, no faster than a minute; a refresh with nothing moved forks nothing beyond the check), `code.7` (each decision a function of plain facts), `roles.5` (crew builds no mechanism its tools hold). sluice's `core.31` (a reader's tick that starts a process or reads an object while nothing changed is ruled out; it asks the forge nothing but what the discovery due or a move on the host calls for; the remote's one fetch a tick carrying every ref is not ruled out) and `core.25` (one reader of a repository's records on a host, every other watch following it). Pages whose areas this touches: `plan.md` (`plan.py`), `tests.md` (`tests/`), `docs.md` (README, `openspec/`); `board.py` is under `core.md` alone.

## Goals / Non-Goals

**Goals:**
- A tick after nothing moved starts nothing but one fetch of each repository.
- Another host, Pending You and herdr asked only when something there could have moved, as read with no process.
- One fetch for each repository, one overview watch for each repository on a host.

**Non-Goals:**
- The card sweep acting in a name Pending You refuses (the refused closes of swancloud-planner's batch cards as madswan-planner): its own fix; this change only stops the follower from trying it at every tick.
- The cost of a read after a real move, and of the frames' render: a move is not a quiet tick.
- sluice's watchers.

## Decisions

### 1. Another host is asked when something there could have moved

What says something on a host could have moved is read with no process (`host_basis`): the drive's branch of each partition the host serves (`readings_hosts`, the partition's main machine and every host its runners answer on), its tip as this host's cache holds it, since every act on the host reaches that branch as it is written (`read.5`); the host's own runner's branch of each, where its runner reports the places it runs; and the queue of each of its kits as its watch last read it, where a merge or a landing shows. A refresh asks a host (`hosts_due`) when its basis moved since it last answered, when it never answered or its last answer was not whole (a kit's or the readings' stamp unreadable, `read.1`), or when ten minutes have passed (`DISCOVERY`, `plan.CARD_RETRY`'s ten minutes). This host's kits and readings are stamped in the follower's process at every refresh, which starts nothing and is what tells it nothing moved here. A host not asked keeps the stamps its last read was made at, so it moves nothing in `moved`. At a tick, each host something could have moved on since the last tick asked it (a second memory, `asked_at_tick`) is asked its portless routes and the overviews no watch follows of its kits, in the same ssh; this host's routes are one `portless list` only then.

The ten minutes are what only the host can say: a dev server started by hand, an exploration landed on a kit's main with no act of crew's, a reading the user sent back on that host. Each shows within ten minutes when nothing else moves; the host's own follower, where it runs, sweeps its own readings within seconds.

Considered: an ssh to each host at every tick, the check `plan.12`'s reading allowed and what deneb ran (rejected: a tick after nothing moved would still start a process, which the brief and `core.31` rule out); no ssh at all until the host's branch moves (rejected: what only the host can say, a dev server or a reading sent back there, would never show while its partition is quiet).

### 2. Pending You and herdr are asked when the cards could have moved

At a tick the follower asks after the cards its sweep acts on (`plan.cards_asked`) and their askers' panes (`plan.askers_asked`) only when it is due (`cards_due`): a card or asker the last ask did not answer, a last ask whose bridge failed or whose listing could not read an asker, none made yet, or ten minutes since the last; never when there is none to ask, which needs no bridge. The cards' stamp (`cards_stamp`) moves only at an ask: a failed bridge or a card the last sweep left counts as moved at the next ask, which is the card sweep's own ten-minute retry of a refused card (`plan.refused_lately`), and no longer at every tick. The read's own ask, made when no answers are kept, counts as an ask.

The ten minutes are what only Pending You can say: a card the user dismissed, which the sweep posts again; an asker's pane emptied, which herdr says and the sweep withdraws its question. Before, both showed within the minute.

Considered: Pending You's notice, `pendingyou watch`, as the word that a card moved (rejected for now: the follower runs it only while a role here runs as its kind, since the notice marks each change handed in the host's Pending You state, and with it absent there is no word at all; where it runs, a change it hands could make the cards due, a step left to the role-runs work).

### 3. One fetch for each repository

The clock's fetch (`fetches`) groups every branch the follower reads by repository, each partition's drive's branch, which brings its runners' branches beside it (`plan.beside`), and its first blueprints repo's main, and fetches each repository once (`plan.tips_of`), sluice's `core.31` shape: the remote's one fetch a tick carrying every ref the reader reads from it. A branch the repository does not have yet makes git refuse the fetch naming it; `tips_of` fetches again without it, reading it as `None`, one fetch more and not one per branch. A fetch is the one question only GitHub can answer for crew, so it stays at every tick: the operator-agent spec has another host's entry shown within the minute.

Considered: an in-process conditional ask of GitHub (an HTTP request with an `ETag`, as sluice's discovery is), which would start no process at a tick (rejected here: it needs a credential in crew's own process, where crew's git takes it from the host's helper, a design of its own across the family's credentials); a fetch only every ten minutes (rejected: another host's entries would show ten minutes late).

### 4. One overview watch for each repository

The follower's watches are keyed by repository (`watch_key`): on this host a kit's main checkout's common git folder, read from its files (`gather.git_dirs`), so two checkouts of one repository share one watch and its line is each one's queue; on another host, and where the files can't say, the kit's main checkout. sluice reads a repository's records once on a host and every other watch follows that reader (`core.25`), so one watch per repository is what the host pays once.

### 5. A runner's report is a move

The look stamps each partition's runners' branches as this host's cache holds them (`plan.runner_tips` with no fetch, from the cache's files), and `moved` counts a runner's branch moved, made or gone as its partition's state moved, so its read is made again. The read rests on those branches (`plan.runners`), and a runner's report of the places it runs arrives with no move of the partition's own branch; before, it waited for something else to move (`read.1`). It is also what makes the runner's host due in Decision 1.

## Risks / Trade-offs

- [A dev server started by hand on another host, an exploration landed with no act, or a reading sent back there shows up to ten minutes late] → the discovery's interval; each showed within the minute before, at the cost of an ssh a minute per host.
- [A card the user dismissed in Pending You, or an asker's pane emptied, is acted on up to ten minutes late] → the card sweep's own retry interval; the ask was once a minute.
- [The basis of a host serving a busy partition moves often, and each move asks it] → one ssh after a move is the check `plan.12` allows; a move of a partition with nothing there asks nothing.
- [A branch not made yet costs its repository one fetch more at each tick] → until it is made; one partition's branch at most.

## Migration Plan

None beyond landing: the follower starts again as the new crew when crew moves (`teams.19`).

## After deploy

None: every behaviour here is pinned by the logic, contract and end-to-end tiers on the stubs.

## Task notes

**1.1** `plugin/lib/board.py`: `host_basis(host, labels, tips, runners, queues)`, `hosts_due(bases, asked, now)` and `DISCOVERY`; the `Follower`'s `bases`, `check` and `answered`, with `asked` and `asked_at_tick`; `stamps_now` taking `hosts` and a set of `routes`. Cases in `tests/py/test_board.py`: the basis moves on its partition's tip, its runner and its kits' queue and on nothing else; a host never asked, moved, unanswered or ten minutes on is due and else not; the box asked at its runner's report, wldn's move, an unanswered ask and ten minutes on, not at swancloud's move; a watch's new line asks the box.

**2.1** `plugin/lib/board.py`: `cards_due(cards, askers, answers, listed, at, now)`; `cards_stamp` counting asks; `Follower.ask` asking only when due, `read` counting its own ask. Cases: no card or asker asks nothing; one unanswered, a failed bridge, an unread asker or ten minutes asks; answered ones ask nothing; the tick after the cards were answered asks Pending You nothing and one ten minutes on asks; an asker's pane emptied is swept at the next ask.

**3.1** `plugin/lib/plan.py` `tips_of(repo, refs)`; `board.py` `fetches(fleet, labels)` and `Follower.fetch`. Logic case: each repository once with its branches, in the partitions' order. Contract case in `tests/contract/test_git.py`: two partitions' branches and a runner's in one fetch; a branch not made fetched again without it, two fetches.

**4.1** `plugin/lib/board.py` `watch_key` and `Watches` keyed by repository, each watch's line and end every kit's of it. Cases: two checkouts of one repository on this host share a key, another host's kit is keyed by its checkout, a checkout with no git folder by itself; one watch opened for both, its end said on both, closed once no kit of it is shown.

**5.1** `plugin/lib/board.py` `look` stamping `runners`, `moved` counting them as the partition's state. Case: a runner's branch moved, made or gone moves its partition and reads; a check from before runners were stamped moves nothing.

**6.1** The quiet tick: `tests/py/test_board.py`, a tick after the cards were answered and nothing moved fetches each repository once and asks no host, route, overview, Pending You or herdr; `tests/t-journey-board.sh`, the running follower's quiet tick logs one fetch of each repository, this host's stamps in its process and nothing else, no ssh, sluice, Pending You or herdr, and the steps after it wait on the frames rewritten.

**6.2** README's follower paragraph, the crew skill's `crew _follow` row, `plugin/bin/crew`'s usage and `board.py`'s header say it fetches each repository once, asks another host, Pending You or herdr only when something there could have moved, and follows each repository's queue through one watch (`docs.2`).
