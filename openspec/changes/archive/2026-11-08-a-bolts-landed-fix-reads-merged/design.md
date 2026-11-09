# Design: a bolt's landed fix reads merged

## Context

The proposal gives the reading of 2026-11-08. #479 (`a-unit-whose-work-its-bolt-holds-is-built`, archived `2026-11-07-a-unit-whose-work-its-bolt-holds-is-built`) built the reading this change extends: `gather.bolt_landings` gives each bolt's landings, `{branch: {"commit", "at"}}`, from the `Sluice-From` trailers on its first-parent line. `runner.built_on_bolt` makes a piece merged at the landing naming its place's branch. `Stages.crossed` applies it to units and chores. This change applies the same reading to a bolt's fixes. It reads no new fact from git, and adds no new read.

Rules this change relies on:

- `read.1`: crew reads a fact where it is recorded, and never guesses. A fix is merged only on its landing's evidence, landings crew can't read change nothing, and a fix crew can't read stays in flight.
- `read.2`: crew reads another tool's output only by facts checked against the tool as it is now. A fix's place branch is read as Flume names it today, from boomdrive's `0a3c8843`, swancloud's `217bdfd5` and `ebd9f481`, and crew's `a737f57a`, each `Sluice-From: fix/<name> (fix/<name>)`.
- `code.7`: a decision is a function of facts. `place_branch`, `built_on_bolt` and `fixes_in_flight` call no tool.
- `code.8`: no stage, object or field the views draw changes shape. A fix's `flume` value gains the keys a unit's already carries.
- `plan.12`: a command reads each kit and the runners once. The landing's fixes come from the same `Stages` reading as its units, not from a second `runner_facts`.
- `plan.16`: a bolt's row on its kit's landings card can land once the bolt reads proven, no fix in flight on it.
- `teams.5`: a fix merges into its bolt only through a submission to sluice, which its place under Flume makes. So sluice's landing on the bolt is the record of the fix's merge.
- `state.2`: nothing records by hand how far work has got. The planner's hand drop of a landed fix is what this change makes unneeded.
- `docs.2`: the command's words change together in README, the skill and the usage header.
- Crew record 0056, decision 2: crew reads a bolt's places from what the work's tools hold.

It touches the areas of:

- `plan.md` (`plugin/lib/plan.py`)
- `teams.md` (`plugin/bin/crew`)
- `briefs.md` (`plugin/skills/`)
- `tests.md` (`tests/`)
- `docs.md` (`README.md`, `openspec/`)

It departs from no rule in `docs/architecture/`. Its tasks depart from `openspec/config.yaml`'s rule that the last task runs `tests/suite --affected`. The place's verify stage runs the repository's whole checks once, after every task. And with `plugin/lib/` edited, `--affected` is the whole suite (CLAUDE.md, Tests). So a last task running it would run the suite the verify stage runs. The path not taken is that task.

The family: Flume names each place's branch `<kind>/<name>` from its launch, and sluice's landing names the branch it took (sluice clause 23). Flume's own `landed` commit for a place it still holds is that same landing. crew reads a bolt's pieces through one decision, `built_on_bolt`, for units, chores and now fixes. It keeps no second reading for one kind of work.

## Decisions

### 1. A fix's place branch is `fix/<bolt>--<name>`

`fix_launch` launches a fix on a bolt as Flume's `fix` kind named `<bolt>--<name>`. Flume cuts the place on `fix/<bolt>--<name>`, and sluice's landing on the bolt names it so (boomdrive #28: `fix/a-dropped-launch-is-never-offered--its-tests-take-the-neutral-names`). `place_branch` gives that branch for a fix on a bolt, work `fix/<bolt>/<name>` in three parts.

A fix of a kit's main, `fix/main/<kit>/<name>`, lands on main, never on a bolt, and its stage is read from Flume and the runner's records (`main_fixes_waiting`). `place_branch` gives it none, so no bolt's landing builds it. A role's work also has none, as before.

`place_branch`'s other callers, `branch_refusal` and `drop_kept_said`, pass only a unit or a chore, so they are unchanged.

Alternatives considered:

- Reading the fix's branch from the launch's `Name` field. `place_branch` is a function of the work's own name, which every caller already holds. The launch's `Name` is the same `<bolt>--<name>` by `fix_launch`.

### 2. A landing before the fix's launch builds nothing

A unit's place may be built by another partition's launch made before this partition's, so #479 reads a unit merged by any landing naming its branch. A fix differs. Its name is free on its bolt again once its launch is dropped: `fix_launch` refuses a name only while a launch of it stands. The four fixes of the reading were dropped so, by hand, after their places had landed. A fix launched again under such a name would read merged at once, at the dropped fix's landing, and hold its bolt's landing no longer, though its own work had not landed.

A take-main fix is the case that matters. Its name, `take-main-<main, seven>`, comes again whenever sluice refuses the bolt at the same main. Read merged from the old landing, the new take-main fix would leave the bolt's row landable. ops would submit it again, and sluice would refuse it again.

So `built_on_bolt` takes the launch's `Date`. A landing whose `at` is before it builds nothing. Both are UTC ISO 8601 to the second, as `requests.rec` and `gather.landed_from` write them, so they compare as text. A fix's place is cut after its launch and lands minutes later at least, so no fix's own landing is before its launch. `landed_from` keeps the newest landing per branch, so once the new fix lands, its landing is the one read.

`Stages.crossed` passes no date for a unit or chore, and their reading is unchanged.

Alternatives considered:

- Refusing `crew fix` a name a landing on the bolt already names. That needs the bolt's kit read on every fix start, and `take_main` starts its fix from a read that has no kit. The date is on the launch already.
- Applying the date to units and chores too. That undoes #479's reading of a unit built by another partition's earlier launch.

### 3. Every decision reads a bolt's fixes through `Stages.fixes`

`Stages.landings(b)` gives a bolt's landings as its kit was read, or None where the kit or its landings can't be read. `Stages.crossed` reads them through it, the expression it holds today moved into the method. `Stages.fixes(b)` applies `built_on_bolt` to each fix with those landings and the fix's launch `Date`. `crew bolts`, the board's ledger and its `asking` and `fixing` bands read `Stages.fixes` already, so they read a landed fix merged with no change of theirs. `piece_said` says its line as a unit's, `fix/<bolt>--<name> landed on its bolt at <commit>`.

The landing's hold, `land_facts`, read its fixes with `runner.fixes_in_flight(*runner_facts(fleet, label), bolt)`, a second read of the runners that knew nothing of the landings. It now reads `runner.fixes_in_flight(st.fixes(b), bolt)`, from the `Stages` it already holds. `fixes_in_flight` becomes a decision over `Stages.fixes`' triples, `(work, launch, stage)`. It keeps each fix of the bolt that has not merged, landed or been dropped, with its launch's brief. A fix whose stage crew can't tell is still in flight (`read.1`).

`Stages.fixes` gives none where the partition's runners can't be read. `land_facts` reads the bolt's kit through `st.kit(b)` first, and that refuses when the runners can't be read. So an empty list never stands for fixes crew could not read.

A fix's drop, `crew fix <bolt> <name> --drop`, reads its stage inside the write from the runners at the tip it is applied to (`plan.1`). `fix` reads the bolt's landings before the write, through `stages_for(...).landings(b)`, as a unit's drop reads its stage before its write. `fix_flume` takes them and applies `built_on_bolt` to the stage before `fix_drop_refusal`. A landing read before the write still stands at the tip, since a landing is never undone, so the refusal holds there. A fix read merged is refused with the words a merged fix's drop has today. A start reads no landings.

## Risks / Trade-offs

- **A fix's drop reads the bolt's kit**, on the host its work runs on, as a unit's drop does. One more read for the drop alone, none for a start.
- **A dropped fix whose place lands after a fix of its name is launched again.** The new fix would read merged at the old landing, which is newer than its launch. That takes a drop while the dropped place's submission still stands, then a new launch of the same name before sluice decides that submission. crew does not read whether Flume withdraws a dropped place's standing submission. Since a fix read merged can't be dropped, the drop that opens this window is one made while crew could not read the landing.

## After deploy

None. Every scenario is proved by the logic tier, and nothing is set by hand on a host. The four fixes of the reading were dropped by hand and their bolts' landings followed. Nothing of them waits on this change.

## Task notes

Each check runs from the place's root. `moon run tests:venv` syncs `tests/.venv` from `tests/uv.lock`, as the logic task's own dependency does.

**1.1** `plugin/lib/runner.py`. `place_branch(work)`: a fix on a bolt, `fix/<bolt>/<name>` in three parts, gives `fix/<bolt>--<name>`. `fix/main/<kit>/<name>` and a role's work give None. The docstring says so. `built_on_bolt(work, s, landings, launched=None)`: a landing whose `at` is before `launched` builds nothing. The docstring names Decision 2. Cases in `tests/py/test_fix.py`, a new class `TestAFixItsBoltHolds`:
- a fix's branch is `fix/x--tidy`, and a fix of main's and a role's are None;
- a fix last read submitted is merged at a landing naming `fix/x--tidy` made after its launch, keeping its place, with `on`, `branch` and `landed`, and `piece_said` gives `("merged", "fix/x--tidy landed on its bolt at 1111111")`;
- a landing before its launch builds nothing;
- `fix/main--red` in a bolt's landings builds no fix of main.

Change the line in `tests/py/test_stages.py`, `TestBuiltOnItsBolt.test_a_unit_another_partitions_place_built_with_no_launch_here_is_merged_by_its_branch_alone`, that asserts a fix is never read from the landings. It asserts instead that a landing naming `fix/x--tidy` builds `fix/x/tidy`, and that a landing naming another fix's branch builds nothing.

**1.2** `plugin/lib/plan.py` `Stages`: `landings(b)`, used by `crossed` in place of its inline read. `fixes(b)` applies `runner.built_on_bolt(work, s, self.landings(b), launch.get("Date"))`. The docstrings name the bolt-plan requirement. Cases in `tests/py/test_stages.py`, beside `test_a_crossed_bolts_fixes_read_their_stages_from_the_runner`, the fix request given a `Date`:
- with `bolt={"landings": {"fix/x--tidy": ...}}` and the runner at submitted, `st.fixes` reads `fix/x/tidy` merged at the landing;
- with `landings_error` and no landings, it reads submitted;
- with a landing dated before the launch, it reads submitted.

**1.3** `plugin/lib/runner.py` `fixes_in_flight(fixes, bolt)`, over `Stages.fixes`' `(work, launch, stage)`. `plugin/lib/plan.py` `land_facts`: `runner.fixes_in_flight(st.fixes(b), bolt)`, and no `runner_facts` call of its own. In `tests/py/test_fix.py`, `test_a_fix_in_flight_holds_the_bolts_landing_until_it_has_merged_or_been_dropped` passes the triples `runner.fixes_on` gives (`[(l.get("Work"), l, s) for l, s in runner.fixes_on(requests, reads, "bolt/x")]`), and asserts the same results. A new case in `TestAFixItsBoltHolds`: a fix whose stage `built_on_bolt` made merged is not in flight, and `plan.landing_unready` then reads the bolt proven. The same fix with its landings unread is in flight.

**1.4** `plugin/lib/plan.py` `fix`: for `--drop` on a started bolt, read `stages_for(fleet, label, plan, [b]).landings(b)` before the write and pass it to `fix_flume(..., landings=...)`. `fix_flume` applies `runner.built_on_bolt(work, s, landings, launch.get("Date"))` to the piece's stage before `fix_drop_refusal`. Cases in `tests/py/test_fix.py` `TestAFixOfAStartedBolt`, its `fix` helper taking `landings`:
- the runner at submitted and a landing naming `fix/x--rail-word` after its launch: the drop is refused with `^fix/x/rail-word has merged into bolt/x, so it is not dropped`, and no request is appended;
- with no landings given: the drop goes as today.

**2.1** `README.md`, the stage paragraph's sentence on a piece merged from its bolt's landing, names a fix's `fix/<bolt>--<name>`, read only from a landing at or after its launch, and that a fix so read holds its bolt's landing no longer. `plugin/skills/crew/SKILL.md`, the stage sentence: "a unit, chore or fix is merged once a landing sluice made on its bolt names its place's branch". `plugin/bin/crew`, the header's stage sentence, likewise.
