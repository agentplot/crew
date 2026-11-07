# Design: a unit whose work its bolt holds is built

## Context

The proposal gives the two readings of 2026-11-07. Rules this change relies on:

- `read.1`: crew reads a fact where it is recorded, and never guesses. A piece is built only on its landing's evidence, and landings crew can't read change nothing.
- `read.2`: crew reads another tool's output only by facts checked against the tool as it is now. `Sluice-From` is read as sluice writes it today (its `text.rs`, `landing_message`: `Sluice-From: {agent} ({worktree})`), and a value of another shape is taken whole.
- `plan.19`: a bolt on GitHub is read there, at `origin/bolt/<bolt>`, never from the host's copy. Its landings are read at the same ref.
- `plan.21` and `plan.16`: a landed bolt is closed once main holds each piece's landed commit (`runner.unlanded`). That close runs after main holds the bolt, so the landings must still read then.
- `state.2`: nothing records by hand how far work has got. The stage comes from the bolt's branch, which sluice writes.
- `code.7`: a decision is a function of facts. `landed_from`, `place_branch` and `built_on_bolt` call no tool, and `bolt_landings` is the thin read around them.
- `code.8`: no stage, object or field the views draw changes shape.
- Crew record 0056, decision 2: crew reads a bolt's places from what the work's tools hold.
- Crew record 0055 (rejected) and the user's no-renaming rule: no reader maps one partition onto another. The landing names the work's own branch, which carries no partition.

It touches the areas of:

- `plan.md` (`plugin/lib/plan.py`, `plugin/lib/gather.py`)
- `teams.md` (`plugin/bin/crew`)
- `briefs.md` (`plugin/skills/`)
- `tests.md` (`tests/`)
- `docs.md` (`README.md`, `openspec/`)

It departs from no rule.

## Decisions

### 1. The bolt's landing names the piece's place

sluice writes each landing as a merge commit on the bolt. Its `Sluice-From` trailer names the branch submitted, either as the agent or as the worktree in parentheses (sluice clause 23). A Flume place's landing names its branch as both: `change/<unit> (change/<unit>)`. A session's submission in pull-request mode names it as the agent: `fix/<f> (pull/<n>)`. gather reads the bolt's first-parent line, which holds only sluice's landings on it, and maps each name to the newest landing giving it, with that commit's committer time in UTC.

A place's branch is the name Flume cuts it on: `<kind>/<name>`, from the launch's `Kind` and `Name`. For a unit that is `change/<unit>`, and for a chore `chore/<chore>` (`runner.reach`; Flume's status `branch`). It is the work's own name, so a landing made by any partition's launch names the same branch. Nothing of one partition is read as another's.

Read on deneb on 2026-11-07: swancloud's `23e7c55e` and `b1d81ee4` name `change/moons-store-sits-beside-the-compile-cache-and-keeps-its-recent-entries` and `change/a-boxs-build-engine-restarts-cleanly-before-its-cap`. flume's `f33f6dce` and `b685768b` name `change/a-repository-is-named-by-its-address` and `change/flume-publishes-its-own-flake-and-module`. Flume's own landed commit for a place, where its status gives one, is that same landing commit (timber `f6b227ec`, boomdrive `4a4b7c83`). So a piece read either way names one commit, and a batch that held a unit at Flume's commit holds it at the bolt's too.

Alternatives considered:

- Reading the landing's subject, `chore(land): #<n> <from>`. A submitter may give its own subject in place of the branch, so it was not chosen.
- Reading the bolt's tree for the archived change. That says a change is on the bolt, not which landing brought it or when, and a chore archives nothing.

### 2. The bolt's line, before and after it lands

While main does not hold the bolt's head, the line is the bolt's first-parent commits beyond main. Once main holds the head, the line beyond main is empty, but the close still needs each piece's commit. So the read finds the merge on main's first-parent line whose other parent is the head, and reads beyond that merge's first parent: main as it stood when the bolt landed. `git log --format=%P` keeps every parent under `--first-parent` (read 2026-11-07 under git 2.54). A head main holds with no such merge, a bolt with nothing of its own, names nothing. A head git can't read, or an ancestry it can't tell, is said as `landings_error` (`read.1`).

### 3. The landing wins over the runner's report, and keeps its commit

`Stages.crossed` reads the runner's stage as before, then `built_on_bolt`. Where a landing names the place's branch and the runner does not already read the piece merged or landed at a commit, the piece is `merged` at the landing's commit. Its place and tasks are kept where the runner gave them. It carries `on: bolt`, the branch, and `landed`, the landing's time, which a batch reads as its `carried`. This covers a launch that is launching, refused, submitted, unknown for want of a launch in this partition, or anything else. `landed` follows as before, once main holds the unit's change. A piece the runner reads merged at Flume's commit keeps it, which is the same commit (Decision 1).

A launch refused because the bolt holds the change reads merged once its landing is read, and so asks nothing more. Without a landing it stays refused with the runner's words, never guessed built.

### 4. A bolt whose launches carried no place

`launched_at` reads where a bolt's work runs from the runner that took its newest launch. When every launch was refused, that runner carried no place, and a runner that reports no `repositories.rec` gives no folder. crew then read "where it runs can't be told", and with no kit read it could read no landing. Now, where the runner that took the bolt's work gives no folder, crew reads the kit's folder from that same runner's places of the kit's other work (`kit_at`), on that host only. A folder on another runner's host is refused as before, since the bolt was taken on this one. The stream is the bolt's own where a place named it, else the kit's.

## Risks / Trade-offs

- **One more git read per bolt in a kit's read**, and two more for a bolt main already holds. Each is one `git log` bounded by the bolt's own line, run once per command (`plan.12`).
- **A branch name reused by another unit.** A unit's name is refused where main already holds its change (`plan.7`), so `change/<unit>` on a bolt's first-parent line is that unit's.

## After deploy

None. Every scenario is proved by the logic and contract tiers, and nothing is set by hand on a host.

## Task notes

**1.1** `plugin/lib/gather.py`: `FROM`, `landed_from(log)`, `LANDINGS`, `bolt_landings(main, ref, now)`. In `kit`, after `carries`, each bolt read gets `landings` or `landings_error`. Cases: `tests/py/test_kit.py` `TestLandedFrom`, and `tests/contract/test_gather.py` `test_a_bolts_landings_name_each_place_landed_on_it_before_and_after_the_bolt_lands_on_main`: two landings by merge, a place's own commit carrying a stray `Sluice-From` on the second parent, main moving on, the bolt landed on main, an empty bolt, a missing ref.

**1.2** `plugin/lib/runner.py`: `place_branch(work)`, `built_on_bolt(work, s, landings)`, and `piece_said`'s words for `on: bolt`. `plugin/lib/plan.py` `Stages.crossed`: read the bolt's kit once, apply `built_on_bolt`, and set `carried` to the landing's time. Cases: `tests/py/test_stages.py` `TestBuiltOnItsBolt`: landed and tidied pieces read merged, the batch reads them (`crossed_changes`), landed once main holds the change, the bolt waits once green, a refused launch reads merged, a unit with no launch here reads merged by its branch alone, another branch or a fix's builds nothing, unread landings leave the runner's stage, and a runner-landed piece keeps Flume's commit.

**1.3** `plugin/lib/plan.py` `launched_at`: where `runner.where` gives the host and no folder, take `kit_at` when it names the same host. Cases: `tests/py/test_stages.py` `TestABoltWhoseLaunchesWereAllRefused`, and `tests/py/test_bolt_commands.py` `TestCrewBoltsCrossed.test_a_bolt_whose_units_its_branch_holds_reads_where_it_runs_and_each_unit_merged`. `tests/py/facts.py` `ran` takes `refused`.

**2.1** `README.md`, the stage paragraph and where a bolt's work runs; `plugin/skills/crew/SKILL.md`, the stage sentence; `plugin/bin/crew`, the header's stage sentence.
