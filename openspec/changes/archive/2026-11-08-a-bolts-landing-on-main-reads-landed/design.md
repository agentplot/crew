# Design: a bolt's landing on main reads landed

## Context

The proposal gives the reading of 2026-11-08. Three readings of crew's meet in it:

- **Where a bolt's work runs** (`runner.where`, `plan.bolt_at`, `launched_at`, `kit_at`). The host is the runner that took the newest launch taken. The kit's folder is that runner's `repositories.rec` (Decision 6 of the archived `a-kit-renamed-on-its-host-is-renamed-across-the-plan`). Where the runner reports none, the folder falls back to Flume's status of the newest place it carried. Where it carried none of the bolt's, the folder falls back to its places of the kit's other work.
- **A bolt's landings** (`gather.bolt_landings`, #479). This reads the landings sluice made on the bolt's first-parent line, from the bolt's branch where it lives. Once main holds the bolt's head, it reads them back to the first parent of the merge whose other parent is that head.
- **A piece built on its bolt** (`runner.built_on_bolt`). A unit, chore or fix is `merged` at the landing that names its place's branch, and `landed` once main holds it (`Stages.crossed`).

Each reading assumed something that stopped holding once a bolt had landed and its tools had tidied:
- the runner still carrying a place;
- the bolt's branch still standing.

Neither holds after GitHub deletes a merged pull request's branch and Flume tidies the places. The facts that do stand are main's own: sluice's landing commit and its second parent's line.

Rules this change relies on:

- `read.1`: crew reads a fact where it is recorded, and never guesses. A kit whose folder the runner does not report is unread and names why. A bolt landing crew can't read builds nothing.
- `read.2`: crew reads another tool's output only by facts checked against the tool as it is now. sluice's landings are read as sluice wrote them on swancloud's main on 2026-11-08 (Decision 2).
- `roles.9`: a thin runner on each host keeps the repositories its configuration names, and crew reads where a kit is kept from the runner's report.
- `roles.5`: crew builds no mechanism another tool holds. Where a repository is kept is the runner's (boomdrive `core.5`). What a landing names is sluice's (clause 23).
- `code.1`: `gather.py` imports only the standard library, since it is piped to hosts.
- `code.7`: `main_landing`, `landing_sought`, `kept_folder` and `where` are functions of facts.
- `code.8`: no stage, object or field the views draw changes. A bolt's `landed` state and a piece's `merged` and `landed` are drawn already.
- `plan.12`: a command reads each kit once. Main's first-parent log is read once per kit, inside the kit's read, for every bolt asked of it.
- `plan.16`, `plan.21`: a landed bolt is closed by `crew bolt land`, or by the first read of its landing, and by nothing else.
- `state.2`: nothing records by hand how far work has got. The hand close of 16:43Z is what this makes unneeded.
- `state.4`: the run record's `bolt.submit` entries are read at the tip the plan was read at, and nothing is written for this reading.
- `docs.2`: README, the crew skill and the usage header change together.
- `tests.4`, `tests.11`, `tests.12`: each decision has its case in the logic tier and each git read its case in the contract tier. One end-to-end case proves the command's wiring. The stub sluice lands a pull request's submission as sluice does.
- Crew record 0056, decision 2: crew reads a bolt's places from what the work's tools hold.

It touches the areas of:
- `plan.md` (`plugin/lib/plan.py`, `plugin/lib/gather.py`);
- `teams.md` (`plugin/bin/crew`);
- `briefs.md` (`plugin/skills/`);
- `tests.md` (`tests/`);
- `docs.md` (`README.md`, `openspec/`).

It departs from no rule in `docs/architecture/`. It ends the interim of the rename change's design, *What this change rests on* §2: "Without R2, crew takes a kit's folder from a place's status as today". From this change, crew takes the folder from nowhere else.

Its tasks depart from `openspec/config.yaml`'s rule that the last task runs `tests/suite --affected`. The place's verify stage runs the repository's whole checks once, after every task. With `plugin/lib/` and `tests/lib.sh` edited, `--affected` is the whole suite (CLAUDE.md, Tests), so a last task running it would repeat the verify stage. The path not taken is that task.

**The family.** Each fact has one owner, and crew calls or cites it:
- **Where a repository is kept** is Boomdrive's runner's. It keeps the clones (`core.5`) and reports them to its control plane (`core.11`). crew reads that report and keeps no second reading of the folder from a place.
- **What a landing names** is sluice's (clause 23). The commit's second parent is the entry's head, and its `Sluice-From` names the agent and the worktree it came from.
- **A bolt as a base place** is Flume's (record 0056). Once it lands, its `Sluice-From` names `bolt/<bolt>` as a Flume place's branch, `bolt/<bolt> (bolt/<bolt>)`.

crew reads a bolt's landing by those facts alone, and needs no change from sluice or Flume. It needs one from Boomdrive, written in Decision 1 and *Migration Plan*.

## Decisions

### 1. The kit's folder is the runner's report alone

`runner.kept_folder(reading, kit, what)` now gives a reason where the runner reports no repositories (`repositories` None):

> the runner on `<host>` took `<what>`'s work and reports no repositories it keeps, so crew can't tell where it keeps `<kit>` there

The other two answers, by the kit's name or forge address, and two by the kit's name, are unchanged.

`runner.where` takes the folder from `kept_folder` alone. It no longer falls back to the `repository` of Flume's status of a place. The stream is still the newest carried place's `stream`, None while it carries none, since a stream is the place's fact (Decision 6 of the rename change).

So every caller gets either a folder or a reason:
- `plan.launched_at` loses its fallback for a taker with no folder, the kit's other work's places on that host. With its `at["dir"] or fail(...)`, that code can no longer be reached.
- `plan.kit_at` likewise loses its `at["dir"] or fail(...)`.
- `runner.launch_repositories` loses its check for a taker with no folder.
- `bolt_at`, `known_at`, `bolt_taken` and `Stages.at` keep their shape.

A host whose runner reports no repositories reads each started bolt there as `unknown`, naming the reason. `crew bolts` still names the host, as "A started bolt's host is named before its place is carried" has it, since the host comes from the runner's answers.

The main-level host's checkouts (`main_kit`, `crew.kit_kept`) are not touched. They are the hosts file's spaces, for work no runner has taken, which `roles.9` keeps until the runner keeps every host's repositories. They are no place the runner carried.

Alternatives considered:

- **Keep the place's folder until Boomdrive writes `repositories.rec`.** Not taken. The brief says the folder never comes from a place the runner carried. A place's repository is stale once its clone moves (rename change, *What this change rests on* §5). And a fallback that holds only while a place is carried is the defect this change mends.
- **Read the folder from the runner's configuration file on the host.** Not taken. That file is the runner's input, not its output (`read.2`), and `roles.9` has crew read a kit's whereabouts from the runner's report.

### 2. A bolt's landing is read from main's first-parent line

sluice's landing of a bolt, as it is now (read on swancloud's main, 2026-11-08):

| Landing | `Sluice-From` | Second parent |
|---|---|---|
| `4acecf09`, through pull request 377 | `afterthought-ops (pull/377)` | `900527e9`, the `Head` of the bolt's `bolt.submit` |
| `64629f0a`, `9fefa6fb`, `931d1ce0`, `67f28ea4`, each a landing of a `bolt/<b>` through a pull request | `afterthought-ops (pull/<n>)` | the head submitted |

A landing through a pull request names no branch in its `Sluice-From`. A submission from a worktree on the branch names it as the worktree, `<agent> (bolt/<b>)`. A Flume base place's names it as both. So crew reads a bolt's landing by either of two facts on the commit:

- its `Sluice-From` names `bolt/<bolt>`, as the agent or the worktree (`gather.FROM`, `landed_from`'s reading);
- its second parent is a head of the bolt crew knows. That is the `Head` of each `bolt.submit` entry naming the bolt, and the bolt's head where its branch is read. A head crew submitted is what sluice lands as the merge's second parent (clause 23). A head is a commit of the bolt's own, and no other bolt's landing has it as its second parent.

Only commits made at or after the bolt's first launch count. A bolt's name is free in the plan once it lands, so an earlier landing naming `bolt/<bolt>` is another bolt's. A head is exact and needs no bound, but one bound for both keeps the log short. A started bolt's first launch is its start (`bolt_launches`, requests.rec's `Date`). A bolt with no launch never ran work, and no landing is sought for it.

`gather.main_landing(log, bolt, heads, since)` decides it from facts:
- **`log`** is `git log --first-parent --since=<since> --format=%H%x1f%P%x1f%ct%x1f%(trailers:key=Sluice-From,valueonly,separator=%x1d)%x1e <main now> --`, newest first;
- **`heads`** is the heads crew knows of the bolt;
- **`since`** is UTC ISO 8601.

It returns `{"commit", "at", "base", "head"}` for the newest merge that names the bolt or merges one of the heads: its first parent as `base`, its second as `head`. It returns None where none does. A commit with fewer than two parents is no landing, since sluice's landing commit always has the entry's head as its second parent (clause 23). `at` is UTC ISO 8601 from the committer time, as `landed_from` gives it. Since `--since` lets git stop its walk early, `main_landing` also passes over a commit older than `since`.

`gather.kit` reads that log once per kit, from the oldest `since` among the bolts asked. For each asked bolt with a `since`, it records the landing on the bolt's facts as `landed`, or `landed_error` with git's words where git can't list the log. A log git can't list is said on each bolt asked, never read as no landing (`read.1`). The heads it passes are the request's for the bolt, with the bolt's branch head where the read found one.

The request carries what gather can't read on the host. `survey`'s kit request gains `seek`, `{bolt: {"since", "heads"}}`. `stages_for` fills it from `plan.landing_sought(requests, submits, bolt)`, a decision over:
- the partition's requests, as `runner_facts` reads them;
- the run record's `bolt.submit` entries at the plan's tip, which `runs_at` now reads beside the landings and renames.

`landing_sought` gives `{"since": <the oldest Date of bolt_launches>, "heads": [<each Head of a bolt.submit naming bolt/<bolt>, once each, in the record's order>]}`, or None for a bolt with no launch. A survey asked with no `seek` reads no landing, as today.

Alternatives considered:

- **Read the bolt's branch name from the landing's subject, `chore(land): #475 bolt/<b>`.** Not taken. The subject is sluice's words, in a form the branch's policy may change, and in one with no slot it names no branch (clause 23). crew reads a bolt's work from the branches and the trailers, never a commit's words (`gather.carried_bolts`).
- **Match the landing's `Sluice-Submission` against the `bolt.submit`'s `Submission`.** Not taken. They differ: `4acecf09` names 475 and the record names 73 for the same landing. One is the pull request's entry on main's queue, the other the submission crew made from the landing's place. A head names one commit in both.
- **`Sluice-From` alone, as the brief words it.** Not taken. It would miss every landing crew's own `crew bolt submit` makes through a pull request today, the landing of the reading among them (`read.2`). The brief's outcome, a landed bolt read landed whatever its places, is kept.
- **Read the landing from crew's own cache of the repository on GitHub.** Not taken. A kit the plan names by its name alone has its forge address only from the runner's report or the folder's origin, so the folder is needed either way. And the kit's read already reads main once (`plan.12`).

### 3. A landed bolt's pieces are read from its landing

`gather.bolt_landings(main, ref, now, landing=None)` takes the bolt's landing where the kit's read found one. It reads the landings on `<landing head> ^<landing base>`, the bolt's own line as main holds it, whether or not the bolt's branch stands. Given none, it reads as today:
- beyond main while main does not hold the bolt's head;
- once main does, back to the first parent of the merge whose other parent is the head.

`gather.kit` reads the landings so for each asked bolt with a landing, also one with no branch on the host or on GitHub. Such a bolt's facts carry `exists` False with its `landed` and `landings`, and nothing else of a branch.

Nothing else changes in `Stages`:
- `Stages.landings` gives the bolt's `landings` as today, now including a landed bolt whose branch is gone.
- `Stages.crossed` applies `built_on_bolt` to each unit and chore, and makes a merged one `landed` once the kit's main holds its change or its trailer, as today.
- `Stages.fixes` applies it to each fix, with the fix's launch date (`a-bolts-landed-fix-reads-merged`, #7).
- `Stages.bolt_state` reads `landed` once every piece reads landed, as today.

So a landed bolt reads landed by the reading that reads any bolt, with nothing for a landed one alone.

`crew bolt land` follows with no change of its own:
- `bolt_at` gives the folder from the runner's report (Decision 1);
- the survey reads the bolt's landing (Decision 2) and its pieces (above);
- `main_holds` finds main holding each piece's landing commit, since those are on the line main merged;
- `land_refusal` passes.

The read that closes a landed bolt, `landing_read` then `landing_close`, closes it the same way. A piece the landing's line does not name and the runner does not read landed keeps the bolt open, named by `land_refusal` as today (`read.1`).

The close asks sluice to delete the bolt's branch (`land_delete`). Where GitHub already deleted it, sluice's words for that are said, and the bolt leaves the plan all the same, as for any delete sluice refuses (`plan.19`).

### 4. The stub sluice lands a pull request as sluice does

The stub `wt-submit` writes `Sluice-From: $SLUICE_AGENT (<the submitted branch>)` for every landing. sluice writes `<agent> (pull/<n>)` for a submission made from a pull request's place. So the stub sluice, landing a branch whose policy takes pull requests, hands `wt-submit` the place it submits from, `pull/<n>`. `wt-submit` writes that as the worktree in `Sluice-From`. Without it, the end-to-end case would read the bolt's landing by a `Sluice-From` real sluice never writes there (`tests.4`).

`tests/lib.sh` `runner_writes` writes `repositories.rec` from what each host keeps (`keeps`). The stub runner then reports its repositories as Boomdrive's must. `runner_tidies <host> <request>...` has the runner carry no place for those requests, their answers kept, as deneb's runner carried none on 2026-11-08.

## Risks / Trade-offs

- **Every host whose runner writes no `repositories.rec` reads no started bolt.** That is every host today: at agentplot/boomdrive `c6eb79b`, `boomdrive-crew`'s `write.rs` writes three files. Until Boomdrive writes the fourth, a host's crew with this change reads each started bolt there as `unknown` and lands none. Accepted on the brief's word and `roles.9`: each refusal names the host and what its runner does not report, and nothing is landed on a guess. *Migration Plan* orders the deploy so no host meets it.
- **One more git log per kit read.** It is bounded by the oldest asked bolt's first launch, so it covers the days a bolt runs, a few dozen landings. It is read only for the bolts a command asks about, and the host's follower serves it unchanged while nothing moved (`plan.12`).
- **A `bolt.submit` head main merged through another route.** If a head crew submitted reached main as some other merge's second parent, crew would read the bolt landed there. That merge holds the bolt's work as it was submitted, so its pieces read from that line are on main. Each piece is still read by name, so the close drops nothing unread.
- **A landing found while the bolt's branch moved on.** If the bolt landed at a head and then took more work, the work after the head is not on main. The landing reads, and each later piece reads as the runner gives it, unbuilt, so the bolt is not closed. Accepted: `plan.8` refuses work joining a bolt whose landing is queued or landed.

## Migration Plan

1. This change is built on its bolt, `crew-reads-each-piece-as-the-tools-hold-it`, and lands with it.
2. Boomdrive's runner writes `repositories.rec` on each partition's runner branch, with crew's descriptor (`plugin/lib/runner.py` `REPOSITORIES`). It names each repository its configuration keeps by forge address, with its clone's folder. This is R2 of the rename change, which Boomdrive's control plane implementation for crew (`crates/boomdrive-crew`) builds and deploys in its own repository.
3. A host's crew is moved to a commit carrying this change only once each partition's runner branch for that host holds `repositories.rec`. On deneb, `afterthought/runner/deneb`, `agentplot/runner/deneb`, `madswan/runner/deneb` and `swancloud/runner/deneb` of afterthought/crew-state.

**Rollback.** The host's crew goes back to the commit before this change. Nothing is written by it, so nothing is undone.

## After deploy

- **deneb: move deneb's crew to this change's commit only after its runner reports its repositories.** The user does it, as every move of deneb's crew is the user's (`plan.19`, as `teamless/deneb` departs from it). It waits for `git show <label>/runner/deneb:repositories.rec` to succeed in afterthought/crew-state for each of the four partitions. No check in crew can be code for it: it is an order between two repositories' deploys, and crew's suite runs on stubs (`tests.11`).

## Task notes

Each check runs from the place's root. `moon run tests:venv` syncs `tests/.venv` from `tests/uv.lock`, as the logic task's own dependency does.

**1.1** `plugin/lib/runner.py`:
- `kept_folder`: a reading whose `repositories` is None gives `(None, "the runner on <host> took <what>'s work and reports no repositories it keeps, so crew can't tell where it keeps <kit> there")`.
- `where`: `"dir": folder`, no fallback to a place's `repository`; the stream as today.
- The docstrings of both, and `host_read`'s sentence on a branch with no `repositories.rec`, say so, naming this change's Decision 1.

In `tests/py/test_runner.py` `TestWhere`:
- `test_the_host_folder_and_stream_of_the_newest_launch_taken` gives deneb a `repositories.rec` naming `afterthought/crew` at `/Users/chuck/Code/github_afterthought/crew`. The same reading with none asserts the new reason.
- `test_the_folder_a_runner_reports_wins_over_a_places_stale_status` keeps its asserts.
- A new case `test_a_runner_that_reports_no_repositories_leaves_the_kit_unread_whatever_its_places_name`: a place carried naming `/w/crew` and no `repositories.rec` gives the reason. Its docstring names the drive-state scenario "A runner that reports no repositories".

**1.2** `plugin/lib/plan.py`:
- `launched_at`: drop the `if not at["dir"]` block and the `at["dir"] or fail(...)`.
- `kit_at`: drop the `at["dir"] or fail(...)`.
- `plugin/lib/runner.py` `launch_repositories`: drop the `if at and not at["dir"]` check.
- The docstrings of `bolt_at`, `launched_at`, `kit_at` and `launch_repositories` lose their place-folder clauses.

Cases:
- `tests/py/test_kits.py`, the case at its `match="^the runner on deneb took bolt x's work and has carried no place of it yet"`, asserts the new reason for a runner with no `repositories.rec`. With deneb's `repositories.rec` naming the kit, it asserts the bolt is read in that folder, every launch refused and no place carried: the drive-state scenario "A bolt whose places the runner no longer carries".
- `tests/py/test_branch_stands.py`, its two cases asserting "carries no place of it naming the folder it keeps crew in", assert where's new reason.

**1.3** Every logic case whose runner reports no repositories and reads a bolt's or kit's folder gives that runner a `repositories.rec` naming the kit at the folder its place named. This covers `tests/py/facts.py` and each case building `runner.host_read` readings. `tests/py/test_stages.py` at its `match="the runner on deneb took bolt x's work and has carried no place of it yet"` asserts the new reason. `tests/py/test_board.py`'s case at "has carried no place of x's work" keeps its ledger naming deneb, its runner reporting no repositories. Change no assert's outcome beyond the folder's source and the reason's words.

**1.4** `tests/lib.sh` `runner_writes`: from `keeps.json`, write `repositories.rec` with `runner.REPOSITORIES` and one `Repository: <owner>/<kit>` and `Folder: <folder>` per kit kept on that host, and add it to the branch's tree. `<owner>` is the owner of the kit's stub remote where the test names one, else any owner, since crew matches by the kit's name. Its opening comment says so.

**2.1** `plugin/lib/gather.py`: `LANDED`, the format string of Decision 2, and `main_landing(log, bolt, heads, since)` as Decision 2 gives it. The docstring names sluice clause 23, `read.2` and this change's Decision 2, and the readings of 2026-11-08. Cases in a new `tests/py/test_main_landing.py`, a log built as git prints it:
- a merge with `Sluice-From: afterthought-ops (pull/377)` whose second parent is a given head is the landing, with its `base`, `head`, `commit` and `at`;
- a merge whose `Sluice-From` is `bolt/x (bolt/x)` is the landing with no head given;
- `ops (bolt/x)` names it as the worktree;
- such a merge before `since` is none;
- a one-parent commit naming `bolt/x` is none;
- the newest of two is taken;
- a merge naming `bolt/xy` or `change/x` is none of `x`'s.

**2.2** `plugin/lib/plan.py`:
- `runs_at` reads `bolt.submit` entries as `submits`, beside `landings` and `renames`, and a helper `submits_at(repo, tip)` gives them.
- `landing_sought(requests, submits, bolt)` as Decision 2 gives it. Its docstring names Decision 2.

Cases in `tests/py/test_main_landing.py`:
- the oldest launch's `Date` is `since`, the heads are each `Head` of a `bolt.submit` on `bolt/x` once, a refused one with no `Head` and another bolt's left out;
- a bolt with no launch gives None.

**2.3** `plugin/lib/gather.py` `kit`:
- For a request with `seek`, run the log of Decision 2 once from the oldest `since`, in `main`, at `now`.
- Record each sought bolt's `landed` (`main_landing` with the request's heads and the bolt's branch head where read) or `landed_error`, on its facts.
- For a sought bolt whose branch the host does not hold, add its facts with `exists` False.
- `bolt_landings(main, ref, now, landing=None)` reads `<head> ^<base>` given a landing, and is called with the bolt's landing.

Cases in `tests/contract/test_gather.py`, beside `test_a_bolts_landings_name_each_place_landed_on_it_before_and_after_the_bolt_lands_on_main`, a new `test_a_landed_bolts_landings_are_read_from_its_landing_on_main_once_its_branch_is_gone`:
- bolt `te` holds a landing naming `change/a`;
- main merges `bolt/te` with `Sluice-From: ops (pull/1)`;
- `bolt/te` is deleted;
- the kit is read with `seek={"te": {"since": <before>, "heads": [<te's head>]}}`;
- `landed` is the merge, and `landings` names `change/a` at its commit;
- with no heads, `landed` is None;
- with a `since` after the merge, `landed` is None.

**2.4** `plugin/lib/plan.py`:
- `stages_for` passes each started bolt's `landing_sought` to `survey`, its held entries carrying it.
- `survey` puts it on the kit's request as `seek`.
- `Stages.landings` is unchanged in shape.

Cases in `tests/py/test_stages.py`, a new class `TestABoltLandedOnMain`, the kit's facts built as gather gives them:
- bolt `x` with `exists` False, `landed` set and `landings` naming the unit's `change/a`;
- the runner answering `a`'s launch `launched` and carrying no place;
- `a` in the kit's `main`.

It asserts:
- `a` reads `landed`, `bolt_state(x)` reads `landed`, and `land_refusal` over `st.of` with `main_holds` true for its commit gives None;
- with `landings` naming nothing of `b`, a second unit read at code, `land_refusal` names `b` (the bolt-teams scenario "A piece its landing does not hold");
- with `landed_error` and no landings, `a` reads launching.

Assert also that `stages_for` asks the survey with `seek` for `x` from its launch and its `bolt.submit`'s head. The survey is faked as the class's other cases fake it.

**3.1** `tests/stubs/sluice`: on a branch whose policy takes pull requests, run `wt-submit` with the place it submits from, `pull/<n>`, in an environment word the stub `wt-submit` reads. `tests/stubs/wt-submit` writes `Sluice-From: $SLUICE_AGENT (<that place>)` where given, else `(<the submitted branch>)` as today. Both opening comments say so, naming sluice's landing `4acecf09` on swancloud's main read 2026-11-08.

**3.2** `tests/lib.sh` `runner_tidies <host> <request>...`: the host's runner branch rewritten with those requests' answers kept and their places dropped from `places.rec`. Its opening comment names deneb's runner of 2026-11-08.

`tests/t-journey-land.sh` case: ops's `crew bolt land` reads a landing from sluice's record with the waiter stopped too. Before it runs:
- GitHub's `bolt/<bolt>` is deleted from the bare remote;
- the box's runner carries no place of the bolt's work (`runner_tidies`).

The bolt still closes, its entry naming the commit main holds. The test's opening comment says so, citing the bolt-teams scenario "A landed bolt whose branch and places are gone". Run `tests/moon-tasks` only if the test's reads change.

**4.1** `README.md`:
- The stage paragraph's sentence on where a started bolt's work runs: the kit's folder is the one that runner's `repositories.rec` names, a runner that reports none leaving the kit unread, and the clauses on a place's folder go.
- It adds that a bolt whose landing its kit's main holds, found by its `Sluice-From` naming `bolt/<bolt>` or by a head crew submitted as its second parent, since its first launch, has its pieces read from that landing's line whether or not its branch stands, and reads landed and closes once each does.

`plugin/skills/crew/SKILL.md`, its stage sentence, and `plugin/bin/crew`'s header stage sentence say a landed bolt's pieces are read from its landing on main.
