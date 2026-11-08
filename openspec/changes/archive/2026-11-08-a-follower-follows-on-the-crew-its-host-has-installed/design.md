# Design: a follower follows on the crew its host has installed

## Context

The proposal gives deneb's case. Rules this change relies on:

- `state.4`: a host has one follower, never two and never none.
- `read.1`: refuse or act on nothing rather than guess.
- `code.7`: a decision is a function of facts.
- `roles.3`: a fix adds a check, not firmer words.

It touches the areas of `teams.md` (`plugin/bin/crew`), `briefs.md` (`plugin/skills/`), `tests.md` (`tests/`) and `docs.md` (`README.md`, `openspec/`). It departs from no rule.

The host's follower is whoever holds `~/.cache/crew/board/follower.lock`: swancloud's job running `crew _follow`, or a console rail tab's own loop while no job runs (crew-board "A host has one follower"). Every crew command an agent runs is the installed crew (host-holds-and-updates "A standing agent's crew commands run the crew its host has installed"). The follower is the one reader whose code can differ from the install, since a tab's loop runs the build it was opened on. Its update check (`refresh_plan`'s "update", `Follower.again`) fires when crew's stamp moves between two of its own reads, where the stamp is the installed command's real path on a build. A follower that takes the lock already behind the install never sees a move. It reads rows and judges their cards as its own crew does, while every crew command beside it reads them as the installed one does.

That is the second reader of the brief. The rows and their sweep are right on either crew alone: 0.41.0 reads no land/flume row and withdraws the card as its row gone, and 0.46.0 reads the row with no card and posts one. Their disagreement is the churn. The cure is one crew for both readers, and the installed crew is the one every other reader already runs.

## Decisions

### Decision 1: a follower compares the crew it runs with the installed crew

`behind(mine, theirs)` decides from two of `crew_read`'s facts. It is True when both name a commit and the commits differ, False when they name the same commit, and None when either names none. `behind_here()` reads those facts. Where the installed command is crew's own (`crew.own_command`), as a checkout's always is, or the host has none (`crew.installed_here` None), it answers False with no process: there is no other crew to follow on. Otherwise it reads this build's release (`crew.crew_read()`, a file read) against the installed crew's (`crew.installed()`, its answer to `crew _release`, asked once for each real path of the installed command). So an idle follower starts no process for it (crew-board "A refresh after nothing moved reads nothing"), asking again only once an install moves the path.

The comparison is by commit and not by path, because the installed command is a wrapper. deneb's `/etc/profiles/per-user/chuck/bin/crew` resolves to `/nix/store/…-crew/bin/crew`, a script that execs `/nix/store/…-crew-0.46.0/plugin/bin/crew`, so `own_command` is False even for the installed build's own follower. A path test would start that follower again for ever.

Considered and not taken:

- Comparing versions. A build of an unreleased commit carries `0-unstable-<date>+<sha>`, and the commit says the same more simply.
- Having the rail tab never follow, leaving it to the job. A host with no job would then have no follower, which `state.4` rules out.

### Decision 2: a lag is an update, before anything is read

`refresh_plan(m, kept, crew_read, lag)` returns "update" whenever `lag` is True, ahead of "read" for a first refresh with nothing kept, so the follower hands out the restarts due and starts again through the installed command (`Follower.again`, its lock handed on through `CREW_FOLLOWER_LOCK`) before it reads a row or sweeps a card. A lag of None is read as no lag: the follower refreshes as it would on the installed crew and starts nothing again on a guess (`read.1`). The restarts are handed out as at any update, through `crew _update` run by the installed crew, which judges each agent against itself (teams.19).

### Decision 3: a start for a lag happens once

`again` marks a start made for a lag with `CREW_FOLLOWER_LAGGED=1`, and the follower it becomes keeps the mark (`Follower.started_lagging`). A follower so started that still reads a lag answers no lag (`Follower.lagging`). It says once on its standard error that it was started again as the installed crew and still runs another, and follows as it is. A build whose release disagrees with its own `crew _release`, or an install moving between the ask and the exec, could otherwise start the follower again at every refresh, each time handing out restarts. A start for any other reason marks 0, so a later lag after a real install is acted on again.

### Decision 4: the follower deneb runs now is a hand's

The tab running crew 0.41.0 (pid 66134) predates this change. It holds the lock until its pane is closed or the process ended, and swancloud's job (`crew-follow`, waiting on the lock) then follows on the installed crew. That is a live system's step and no task of this change.

## Risks

- A follower's first refresh on a build now asks the installed crew `crew _release`, one process within five seconds, where it asked nothing before. It is asked once for each real path.
- A tab that takes the lock behind the install now runs the installed crew's `_update` before its first read, as the job does at an install.

## After deploy

None, as no check can't be code. Ending deneb's 0.41.0 tab is Decision 4's hand step, for main-level ops or the user once they choose to.

## Task notes

**1.1** `plugin/lib/board.py`: `behind`, `behind_here` beside `crew_stamp`; `refresh_plan`'s `lag`; `Follower.__init__`'s `started_lagging` and `said_lag` from `CREW_FOLLOWER_LAGGED`, `Follower.lagging`, `Follower.refresh` passing its lag to `refresh_plan` and `again`, `Follower.again(fleet, lag=False)` setting `CREW_FOLLOWER_LAGGED`. Cases in `tests/py/test_board.py`:

- `TestFollower`: `refresh_plan` with a lag.
- `TestInstalledCrew`: `behind`'s table; a build behind another installed release, asked once; the installed crew's own follower and a host with none, asking nothing; a checkout; `again`'s mark.
- `TestRefresh`: started again before any read; a started-for-lag follower following as it is and saying so once; an unread lag.

**1.2** `README.md`, the follower's lock; `plugin/bin/crew`'s usage of `crew _follow`; `board.py`'s usage of `crew _follow` and `crew _rail`; `plugin/skills/crew/SKILL.md`'s `crew _follow` row.
