# Design: a landed bolt is closed and offered no more

## Context

crew reads a started bolt's landing from the runner's report alone (record 0056 point 4; `runner.landing_of`), and closes it once that report reads it landed (`landing_read`, `landing_close`, `started_land`). Three facts keep a landed bolt open today.

**A bolt with no base place has no report.** A started bolt with no launch of `bolt/<bolt>` in `requests.rec` reads `legacy`. `Stages.base`, `Stages.landing` and `landing_read` give `runner.legacy_said`'s words, "lands under the crew that started it". `started_land` refuses it in them, and `landings_judged` and `reap_judged` never read it. The crew that started it was a crew that still submitted bolts to sluice itself. Its `crew bolt submit` recorded boomdrive's `a-boomdrive-release-reports-its-own-version` queued as `#154` at `62d2f06` at 00:21:46Z on 2026-11-12. Two minutes later it recorded the landing stopped at `62d2f06` with no `Submission`, its words naming the host's checkout `~/.local/share/flywheel/repositories/agentplot/boomdrive`, gone since the rename. Then `#154` landed on GitHub's main as `6cfc4aec`, whose second parent is `62d2f06`. Nothing of crew's main reads that, and nothing ever will: there is no place for the runner to report. In agentplot's plan on 2026-11-12, 61 of the 62 bolts had no launch of their own.

**A stop outlives the landing.** `stops` reads the bolt's last `bolt.submit` stopped at `62d2f06`. `landing_pending` keeps `#154` queued, since the stop names no submission and "leaves it to a later read". Nothing reads it later.

**A host's checkout lags or is gone.** The older crew read main in the host's checkout of the kit (`MAINS`, `kit.main_now`): "boomdrive's main checkout on deneb has no branch main and no origin". The day before, it read weir's and crew's call-limit bolts stopped because a host's copy of main had not moved, though sluice had landed each (signal `2026-11-11-agentplot-planner-b6097ea7/01`). crew's main reads a kit in the folder the runner reports (`runner.where`), at `origin/main` as the runner last fetched it, which lags too.

crew already reads GitHub's main in its own bare cache of a kit's repository, fetched over https once per command: a proposal's records (`proposal_records`, `tip_of(repo, "main")`). It already asks whether main holds a commit for a landed bolt's pieces: bolt-teams "A landed bolt closes on its pieces' ends as the runner reports them", `runner.unlanded` over `land_refusal`'s `held`. Today nothing feeds `held`.

**How the family does it.** Flume reads a place's landing from the trailers of sluice's landing commit (Flume's read-submission). Boomdrive's runner carries each place's end to crew (Boomdrive `core.54`). crew reads no trailer here. A bolt with a base place keeps its end as the runner's report; Decision 3 says where main is read beside it. The one owner of a bolt's landing stays the runner, once it reports every bolt's landing (*Departures*).

## Goals / Non-goals

**Goals**
- A started bolt whose work its kit's main holds reads landed, and is recorded and closed by the first act that reads it, whichever way it landed, a bolt with no base place among them.
- No stop or queued landing is said of it after.
- Its kit's landings card lists it no more, and no land of it is posted.
- No host's checkout is read for it.

**Non-goals**
- A bolt never started keeps `crew bolt land`'s own read in the checkout the drive's main-level host keeps (bolt-teams "A bolt never started lands by its close once main holds its work").
- A bolt landed by a squash or a rebase, whose commits main does not hold, is not read as landed (Risks).
- A bolt with no base place that has not landed still lands under the crew that started it (record 0056's Decision 9).
- No sluice, Flume or Boomdrive change.

## Decisions

### 1. "Its work is on main": every piece's landing commit and the newest landing head

A started bolt's work is on its kit's main when main holds two kinds of commit:
- the commit each of its units and chores landed at on the bolt, as the runner reports its place's end (`runner.unlanded`'s rule: each reads merged or landed with a commit main holds);
- the newest head a landing of it carried, where the run record holds one: the `Head` of its newest `bolt.submit` since its newest start, of any outcome, an older crew's `queued` or `stopped` and a land crew asked among them (`landing_head`).

It must have one or the other: a bolt with no merged piece and no recorded landing holds no work of its own, and a branch at main's revision is on main trivially. The decision is `on_main`, of facts alone (`code.7`). What it asks git is `main_asks`: nothing while any piece reads anything but merged or landed with a commit, so a bolt still building costs no git at all.

Paths not taken:
- **The landing commit's `Sluice-From`.** That is record 0062's retired third reading, and a trailer is sluice's record.
- **The bolt's branch tip, on GitHub or in the runner's clone.** It lags. A bolt just cut stands at main's revision. GitHub deletes a branch once its pull request merges.
- **The newest landing head alone.** A unit merged onto the bolt after a stop, while the hold was lifted, would be closed with the bolt and lost from the plan.
- **The pieces alone.** A land asked at a newer head, still standing, would be closed on an older landing that main holds.

### 2. Main is GitHub's, read in crew's own cache

`main_tip(repo)` is the kit's main as GitHub holds it:
- in a command, `tip_of(repo, "main")`, one fetch for the whole command (`plan.12`, `plan.18`);
- in the follower's read, the tip the clock's fetch brought and the follower handed in, never a fetch.

`main_holds(repo, tip, commits)` answers each commit in crew's cache. A commit the cache lacks after main's fetch reads not held, since main's fetch brings every commit main holds. Otherwise `git merge-base --is-ancestor` answers. Any other failure is "can't tell", and nothing is taken as landed (`read.1`). The kit's repository is the address the runner that took its work reports (`bolt_at`'s `kit["repo"]`), else the teams file's on the drive's main-level host (`main_kit`). A name crew can't place on GitHub leaves the bolt unread by main.

No host is reached and no host's checkout is read (`read.5`). A folder that is gone, or a copy of main that lags, changes nothing here.

### 3. The report first, main beside it, for every started bolt

`Stages.landing` gives the runner's report's outcome, and `legacy` for a bolt with no launch of its own, as today. Where that outcome is anything but landed, it reads main (`Stages.main_landing`, once per bolt per command). If main holds the bolt's work, the landing reads `{"outcome": "landed", "commit": <main's commit that landed it>}`, the same keys a landed report gives. `Stages.base` gives such a bolt no legacy words. The pieces' stages for the reading come from the runner's records alone (`main_work`: each launch's `runner.piece_stage`), never from a kit's folder, so a close reads no kit.

This holds whether the bolt landed through its base place while the report says stopped, through an older crew's submission, or by hand through sluice.

### 4. Main's commit that landed it

The `bolt.land`'s `Head` is the oldest commit of main's first-parent line that holds every commit the reading asked: the merge commit that brought them in, or the commit itself where it lies on that line (`landed_by`). Main's tip at the read would hold the bolt too, but a later tip names a later landing's commit, and a deploy's view tells the bolts it carried by these heads (`plan.14`, `ops.kit_range`).

### 5. Recorded and closed by the first act that reads it

`landing_read` and `started_land` take the main landing where the report is not landed. The act may be the landings card's raise, the follower's sweep, a kit's read or `crew bolt land` (`plan.21`). Whichever it is, it records one `bolt.submit` and closes the bolt by `crew bolt land`'s own code in main-level ops's name (`landing_close`). The `bolt.submit` reads:
- `Outcome: landed`;
- `Head`, the newest landing head, where there is one;
- `Submission` and `Request` of the landing still pending (`landing_pending`), where there is one;
- `Why`, "landed on <kit>'s main at <commit>, as GitHub's main holds it".

The `Submission` ends an older crew's queued entry. Being the last `bolt.submit`, it ends any stop (`stops`, `landing_phase`). It is decided at its write's tip: none is written where the run record already holds a landed `bolt.submit` of the bolt since its newest start, so two reads record once. `landing_entry`'s match on the request is not used for it, since an older crew's stop names no request and would match the empty one.

`landings_judged` lists a bolt read landed under its host, or under the drive's main-level host where crew can't tell its host. `reap_judged` reads such a bolt whether or not a land of it was posted. A bolt neither posted nor read landed is still read by nothing, so an idle sweep is unchanged (`plan.12`).

### 6. Offered no more

A bolt whose landing reads landed is no row:
- `land_facts` gives `(None, "landed at <commit>: crew closes it at its next read")` before it reads anything else. So the landings card lists no row for it, and `runner.lands_due`, which takes the card's rows, posts no land of it.
- The rail's land group gives it no line, as for a bolt whose every piece reads landed.

`crew bolts` and the board say "landed at <commit>" (`runner.landing_said`), and nothing of the stop or of the crew that started it. A close crew refuses is said on its head line as today (bolt-teams "A refused close is recorded and said on the bolt's head line"). No key is added to `board.agent_views` or drawn by `status.js` (`code.8` not reached).

### 7. The follower fetches each kit's main on its clock

`board.fetches` takes the repositories of the started bolts the follower's last read holds (`kit_mains`), and its clock fetch carries each one's `main` beside the drives' branches and blueprints. `look` reads each one's tip from the cache with no process (`tip_here`). `Follower.read` hands those tips in, so `main_tip` serves them and a refresh fetches nothing (`plan.12`). A repository first named by a read is fetched from the next tick. Until then its bolts read as the report gives them.

## Rules this rests on, and the pages it touches

- `core.md`: `read.1` (can't tell is never landed), `read.2`, `read.5` (no host for a landing), `state.4` (views write nothing), `code.1` (standard library), `code.7` (`on_main`, `main_asks`, `landing_head` and `kit_mains` are decisions; `main_holds`, `landed_by` and `main_tip` the thin reads), `code.8` (not reached), `code.9`, `roles.5` (a reading).
- `plan.md`, whose area `plan.py` is: `plan.12`, `plan.14`, `plan.16`, `plan.18` (GitHub's main after a fetch, never a host's copy), `plan.21` (the first act that reads a landed bolt records it).
- `teams.md`, for `plugin/bin/crew`'s usage header.
- `tests.md`: `tests.4`, `tests.11` (git's answers pinned in the contract tier, decisions in the logic tier), `tests.12`.
- `docs.md`: `docs.2`, `docs.4`, `docs.7`. No page under `docs/architecture/` or `docs/adr/` is edited.

## Departures

- **Record 0056 point 4**, "What the report does not carry, crew does not read anywhere else", and bolt-teams' "from nothing else". crew reads git's answer to whether GitHub's main holds a bolt's commits, beside the runner's report. It reads no trailer, and no record of sluice's or Flume's.

  Why:
  - The runner's report can never carry the end of a bolt with no base place, and those were all but one of agentplot's bolts.
  - A stop recorded by the runner or by an older crew does not take back a commit GitHub's main holds.
  - crew already reads GitHub's main in its cache (`proposal_records`). Record 0062's amendment reads a head's trailers there.

  `roles.5` allows a reading. Record 0062's stopgap, as the user chose it ("Keep them as a named stopgap until the runner reports each end"), covers reading a landing from GitHub while an end stands that the runner does not report.

  The move that retires it is the change that follows the runner reporting every bolt's landing, base place or none, onto every host crew serves. crew then reads it there, and `on_main` and its reads go.

  Record 0062 is to name this reading and that move. It is the design agent's to write after the landing (`docs.7`); this change edits no record.

## Risks / Trade-offs

- **Commits on the bolt that no piece made**, a record landed straight onto it after its newest landing head, are not asked. A bolt so landed is closed with them still on `bolt/<bolt>`. Where a landing was asked at the newer head, the head check holds it open.
- **A squash or a rebase by hand** leaves main without the bolt's commits, and the bolt reads as the report gives it. Sluice lands by merge commit (`plan.8`), so only a hand outside sluice does this.
- **The run record's window.** `drive_entries` reads 60 days back, and a landing head older than that is not seen. The pieces alone then decide.
- **Fetches.** One fetch of each kit's main per command that reads a landing. One per clock tick for each repository with a started bolt.
- **A fix in flight on a bolt read landed** stays Flume's place, as with today's close.

## After deploy

None. The reading, the record and the close are code, proved in the logic and contract tiers. A host takes them with its next crew release, the user's as for any release (`plan.19`, `code.10`). Its first read then closes every started bolt whose work GitHub's main holds, boomdrive's `a-boomdrive-release-reports-its-own-version` among them, with no hand.

## Task notes

**1.1** `plan.landing_head(entries, bolt)`, beside `landing_pending`.
- Takes the bolt's entries since its newest start, a `bolt.start` or the `bolt.give` an older crew wrote, else all of them. A bolt's name is free again once it lands.
- Returns `{head, submission, request}` from the newest `bolt.submit` of the bolt naming a `Head`, whatever its outcome. `submission` and `request` are those of the landing `landing_pending` gives over the same entries, where one stands, else `None`.
- Returns `None` where no entry names a head.

Cases in a new `tests/py/test_landed_on_main.py`, class `TestLandingHead`:
- boomdrive's two entries, queued `#154` at `62d2f06` then stopped at `62d2f06` with no submission, give `62d2f06` with submission `154`;
- a stop at `H1` then a land asked at `H2` gives `H2` with its request;
- a landed bolt's entries before its newest `bolt.start` are not read;
- no `bolt.submit` naming a head gives `None`.

**1.2** `plan.main_asks(work, head)` and `plan.on_main(bolt, kit, work, head, held)`. `work` is `[(name, kind, stage)]` as `runner.unlanded` takes it, a stage carrying its commit. `head` is `landing_head`'s or `None`. `held` is `{commit: 0 held, 1 not held, 2 can't tell}`.
- `main_asks` gives `[]` while any piece reads anything but merged or landed with a commit. Otherwise it gives the head, where there is one, then each piece's commit, each once.
- `on_main` gives `None` when main holds the work, else why, checked in this order:
  1. no work and no head: the bolt "holds no work crew can find on <kit>'s main";
  2. `runner.unlanded`'s words for the pieces;
  3. the head not held: "<kit>'s main does not hold <head7>, the head bolt <bolt>'s newest landing carried";
  4. the head can't be told: git could not read it.

Cases, class `TestOnMain`:
- boomdrive's unit merged at `896e642` and head `62d2f06`, both 0, gives `None`;
- a unit's commit 1 gives `unlanded`'s words;
- a unit in code gives `main_asks` `[]` and `unlanded`'s words;
- the head 1, with the units 0, gives the head's words;
- no work and no head gives that words;
- no work and the head 0 gives `None`;
- a commit 2 gives can't tell.

**1.3** `plan.main_holds(repo, tip, commits)` and `plan.landed_by(repo, tip, commits)`, run by `plan.git(..., check=False)` in crew's cache.
- `main_holds`: `cat-file -e <c>^{commit}` failing reads 1. Else `merge-base --is-ancestor <c> <tip>`'s exit 0 or 1. Anything else is 2.
- `landed_by` gives the oldest commit of `tip`'s first-parent line holding every commit given, or `None` when git can't tell. For each commit that is the commit itself where it lies on that line. Otherwise it is the oldest first-parent descendant of it up to `tip`, for example the first of `rev-list --first-parent --reverse --ancestry-path=<c> <tip> --not <c>^@` (git 2.38 or later; read on deneb's git 2.54 against boomdrive's `62d2f06`, giving `6cfc4aec`). Of those, the newest along the line.

Cases in `tests/contract/test_git.py`, class `TestMainHolds`. A scratch bare repository stands for GitHub, with `plan.url` monkeypatched to its path so `tip_of` fetches it into the case's cache:
- a bolt merged into main by a merge commit, with two commits after it: its head reads 0, and `landed_by` gives the merge, not main's tip;
- a commit fetched into the cache by another ref and not on main reads 1;
- a commit the cache never fetched reads 1;
- a fast-forwarded commit gives itself;
- two commits landed by two merges give the later merge.

**1.4** `plan.main_tip(repo)`.
- While `READ.follower` is set, it gives `READ.tip(repo, "main")`, or `None` where the follower handed none, and never fetches.
- Otherwise it gives `tip_of(repo, "main")`, whose `Refusal` reaches its caller.

Cases, class `TestMainTip`, with `plan.git` monkeypatched to raise wherever no fetch may run:
- the follower with a handed tip gives it;
- the follower with none gives `None`;
- a command calling it twice fetches once.

**2.1** `plan.main_work(plan_, requests, reads, bolt)` and `Stages.main_landing(bolt)`, with `Stages.landing` and `Stages.base`.
- `main_work` gives each unit and chore of the bolt from the runner's records alone: each newest launch's `runner.piece_stage`, as `(name, kind, stage)`, or unknown with `runner.stage_of`'s words where it has none. It reads no kit.
- `main_landing` is memoized per bolt and gives `({commit, head, submission, request}, None)` or `(None, why)`:
  - the drive's entries come from `drive_entries`, read once on the `Stages` object;
  - the repository is `known_at`'s `kit["repo"]`, else `main_kit`'s, and must name an owner;
  - the reads run in order: `main_asks`, and no git at all when it is `[]`; then `main_tip`, where `None` or a `Refusal` gives why; then `main_holds`, `on_main` and `landed_by`.
- `landing` replaces any outcome but landed with `{"outcome": "landed", "commit": c}` where `main_landing` reads it landed, carrying the keys `runner.landing_of` gives a landed outcome.
- `base` gives `{"stage": "landed"}` for a bolt with no launch of its own that `main_landing` reads landed, so no legacy words show.

Cases in `tests/py/test_stages.py`, class `TestABoltWhoseWorkIsOnMain`, with `main_tip`, `main_holds` and `landed_by` monkeypatched, and `host_run` and `crew.on_machine` raising:
- `y` with no launch of `bolt/y`, its unit merged at `896e642` and boomdrive's two entries, reads landed at `6cfc4ae`; its base line is empty, and `landing_line` says `landed at 6cfc4ae`;
- a base place the runner reports stopped, main holding its work, reads landed;
- a unit in code reads the report's outcome, and `main_holds` is never called;
- `main_tip` refusing gives the report's outcome, legacy for `y`;
- a repository named without an owner gives the report's outcome.

**3.1** `landing_entry(entries, bolt, l)` takes an `l` marked `by: "main"`, which only the reads of 3.2 and 3.3 build, carrying `commit`, `head`, `submission` and `request`.
- It gives `Outcome: landed`, `Head`, `Submission`, `Request` and `Why: bolt(<bolt>): landed on <kit>'s main at <c7>, as GitHub's main holds it`, each empty field left out by `outcome_fields`.
- It gives `None` where the bolt holds a landed `bolt.submit` since its newest start.

Cases in `tests/py/test_landing.py`, class `TestALandingReadOnMainIsRecorded`:
- boomdrive's entries give `Submission: 154` and `Head: 62d2f06`;
- with that entry appended, `landing_phase` gives `None` and `stops` lacks `y`;
- the same read again gives `None`.

**3.2** `landing_read`, where the bolt has no launch of its own or its landing does not read landed:
- it builds `l` from `Stages(fleet, plan_of(...), {}, runs={label: run}, label=label).main_landing(b)`, marked `by: "main"`;
- where that reads landed, it prints `bolt/<bolt>: landed at <c7>, as its kit's main holds it`, records it with `landing_record`, closes it with `landing_close`, whose `close_why` says it was read on main, and returns `(True, said)`, asking ops nothing;
- otherwise it goes on as today, a bolt with no launch of its own giving `runner.legacy_said`'s words.

Cases, class `TestALandingReadOnMainCloses`, next to `TestTheFirstReadActs`:
- `y` with no launch of `bolt/y` and main holding its work is recorded and closed;
- a base place reported stopped with main holding its work is closed, and `unlanded_ask` is not called;
- main not holding it leaves today's outcomes.

The existing case "a bolt started before bolts were base places is said so and read no further" keeps main monkeypatched not to hold it.

**3.3** `started_land`.
- A bolt with no launch of its own is no longer refused at once.
- Where its landing does not read landed from the report, it takes `main_landing` as 3.2 does. A landed reading closes it at `landed_by`'s commit, the `bolt.submit` from `landing_entry` in the same commit, `kit_name` coming from `b.get("Repo")` where there is no launch.
- Otherwise it is refused, recording nothing:
  - a bolt with no launch of its own in `"<legacy_said>, and <kit>'s main does not hold its work: <why>, so crew bolt land closes nothing of it here"`;
  - any other bolt in `landing_refused_said`'s words, then `"; nor does <kit>'s main hold its work: <why>"`.

Cases in class `TestCrewBoltLandOfAStartedBolt`, its fixture still forbidding `stages_for`, `survey`, `host_run` and `crew.on_machine`, with `main_tip`, `main_holds` and `landed_by` monkeypatched:
- the legacy case becomes refused while main lacks its work, naming both;
- a new case closes it at `6cfc4ae` once main holds it;
- a stopped base place closes once main holds its head and its chore's commit;
- a commit naming `bolt/z` in `Sluice-From`, holding neither, is refused.

The existing refusals keep their opening words.

**3.4** `landings_judged` and `reap_judged`.
- `landings_judged` counts a bolt whose `st.landing(b)` reads landed as decided, as today. It marks `main: True` where that came from `main_landing`. Where `known_at` gives no host for such a bolt, it lists it under `crew.drive_of(fleet, label)["machine"]`, with no kit or folder.
- `reap_judged` reads a bolt marked `main` whether or not a land of it was posted.

Cases in `tests/py/test_landings.py`, class `TestTheSweepClosesABoltOnMain`, with `landing_read` monkeypatched to record what it is given:
- `y`, read landed on main with nothing posted, is read;
- with its host unknown, it is listed under the main-level host;
- a bolt neither posted nor read landed is not read.

**4.1** `land_facts`: just after `st = stages_for(...)`, a bolt whose `st.landing(b)` reads landed gives `(None, f"landed at {c7}: crew closes it at its next read")`.

Cases in `tests/py/test_landings.py`, class `TestABoltOnMainIsNoRow`:
- `land_read` gives no row for `y` with no launch of its own read landed on main, nor for `z` stopped at `abc1234` with main holding it;
- `runner.lands_due` over the rows left, with `y` ticked on the send, posts nothing for `y`;
- `z` stopped with main not holding it keeps its box and its stop.

**4.2** The rail's land group in `plan.rail_rows`, where it reads `landing = st.landing(b)`: a bolt whose landing reads landed gives no line (`continue`).

Case in `tests/py/test_rail.py`, class `TestABoltOnMainHasNoLandLine`: `y` with no launch of its own read landed on main has no line under `land/boomdrive`, and `w` with no launch of its own, main lacking its work, keeps its legacy line.

**5.1** The follower.
- `board.kit_mains(fleet, read)` gives, sorted and each once, the repository of each started bolt in `read["found"]` as `known_at` gives it over `read["runs"]`, else as `main_kit_read` gives it. It is a decision and reads nothing.
- `board.fetches(fleet, labels, kits=())` adds `(repo, "main")` for each.
- The follower keeps `kit_mains` of its last read.
- `look` adds `"kits": {repo: plan.tip_here(repo, "main")}`.
- `Follower.read` hands each in with `plan.READ.keep_tip`.

Cases in `tests/py/test_board.py`, class `TestTheFollowerFetchesEachKitsMain`:
- `fetches` with two kits fetches each kit's main once, beside each drive's branch and blueprints;
- `kit_mains` names a started bolt's repository and none for a bolt not started;
- the read hands in the kit's tip, so `plan.main_tip` serves it with `plan.git` raising.

The existing case "each repository is fetched once with every branch read of it" holds unchanged with no kits.

**6.1** `README.md`, `plugin/skills/crew/SKILL.md` and `plugin/bin/crew`'s usage header say three things:
- a started bolt whose work its kit's main on GitHub holds, every piece's landing commit and its newest landing head, reads landed whatever the runner's report says, and is closed by the first act that reads it;
- `crew bolt land` closes it so, one started before bolts were base places among them;
- such a bolt is offered on no landings card.

Places: README's landing paragraphs after "A bolt started before bolts were base places says instead…"; the usage header's `crew bolts` head-line lines and its `land of a started bolt …` lines; the skill's `crew bolts` and landing rows. Proved by `tests/suite t-docs`.
