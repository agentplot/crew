# Design

## Context

**Record 0062** (accepted by the user 2026-11-08): crew keeps three readings of GitHub's landing commits "until the runner reports each place's end", and "the readings go in the change that follows the Boomdrive unit `the-runner-carries-each-places-end` onto every host crew serves. … From then on crew reads every piece's end from the runner's report alone." The three readings, on this bolt at `05ffe51e`:

- **A unit or chore read merged from its bolt's landings** (crew #479). `gather.bolt_landings` lists the bolt's first-parent line with `LANDINGS` and `landed_from` maps each `Sluice-From` name to its commit and time. `runner.built_on_bolt` then reads a piece merged once a landing names its place's branch (`runner.place_branch`), whatever the runner carried. `plan.Stages.crossed` applies it through `Stages.landings`.
- **A fix read merged the same way** (`a-bolts-landed-fix-reads-merged`). `Stages.fixes` and `crew fix --drop` (`fix_flume`'s `landings`) pass the fix's launch `Date`, so a landing before it builds nothing.
- **A bolt's landing read on main** (`a-bolts-landing-on-main-reads-landed`, Decisions 2 and 3). `plan.landing_sought` builds a `seek` from the bolt's first launch and the `Head` of its `bolt.submit` entries (`submits_read`, `submits_at`). `survey` puts it on the kit's request, and `seek_answered` decides whether a kept answer serves it. `gather.kit` reads main's first-parent line with `LANDED`, finds the landing with `main_landing`, and reads the pieces from that landing's line with `bolt_landings`. `stages_for`, `bolts_view` and the rail's read seek it.

**What the runner carries now.** agentplot/boomdrive's `the-runner-carries-each-places-end` landed on its main at `76e0226` on 2026-11-08 (Boomdrive record 0030, `core.54`). The runner names itself, `boomdrive`, one more recipient of each launch that names recipients. So Flume keeps a tidied place's record for it, `<location>@<at>`, until the runner collects it, and the runner collects only once its report file holds it. Its design: "Where Flume holds a place's record for the runner after its tidy, `<location>@<at>`, the runner carries it as it carries any place's status … A control plane reads each end there: a landing, a drop and a done as the record's `over`." Its non-goals name this change: "crew's implementation already writes the carried status, a held record among them, to `places.rec`. crew's unit `crew-reads-each-pieces-end-from-the-runners-report` reads it there and retires record 0062's stopgap." Once collected, Flume refuses the place's status, and the runner leaves the held record standing as the status it last carried. Flume 0.20.0's tidied phase is `{"tidied":{"over":…,"at":…,"pending_for":[…]}}`.

**What crew reads already.** Every crew launch names a recipient (`runner.py`, each `launch` request gives `Recipient`), so every place crew launches on such a host has its end held. `runner.flume_facts` takes a place's entry at its location or at `<location>@<at>`, and reads a tidied phase's `over` as it reads an over one's. `runner.stage_of` reads it merged at its commit on a bolt, landed on main, or dropped. `tests/py/flume-0.3.6/landed.json` is such a tidied record, pending for `madswan/planner`.

**Where this bolt stands against main.** The bolt was cut at `05ffe51e`. Main has since landed `bolt/crew-lands-through-the-runners-land-message` (`ec4bd355`). There a bolt is a Flume base place, and `crew bolt land`'s `started_land` closes a bolt at its base place's landing as the runner reports it (`runner.landing_of`). Where the runner reports none, it falls back to `main_landed`, which reads `gather.main_landing`'s `landed`. The bolt-plan, bolt-teams and merge-gate requirements this change removes or modifies read the same on both. Decision 7 says what becomes of main's fallback.

**Rules relied on:**
- `roles.5`: a stopgap named in its record is retired by a change of its own.
- `roles.9`: crew reads Flume's ends through the runner, never a kit's host from anywhere but the runner's report.
- `read.1`: no fallback, and a fact crew can't read is `unknown`.
- `read.2`: each field guarded.
- `code.7`: `stage_of`, `verification` and `unlanded` stay decisions on facts.
- `code.8`: no view key changes.
- `state.2`: nothing is kept by hand.
- `plan.8`: a bolt meets main at its landing.
- `plan.12`: one read per command.
- `plan.16`.
- `tests.4`, `tests.11` and `tests.12`.
- `docs.2`, `docs.4` and `docs.7`.

**Area pages this change touches:**
- `core.md`.
- `plan.md` (`plugin/lib/plan.py`, `plugin/lib/gather.py`).
- `teams.md` (`plugin/bin/crew`'s usage header).
- `briefs.md` (`plugin/skills/crew/SKILL.md`).
- `tests.md` (`tests/`).
- `docs.md` (`README.md`, `openspec/`).

No rule page or record is edited here (`docs.7`). After the landing, the design agent's hand lifts `tests.5`'s "or record 0062's stopgap reads it" and marks record 0062 retired.

## Goals / Non-Goals

**Goals:**
- Every unit's, chore's and fix's end on a started bolt is read from the runner's report alone, a record Flume holds for the runner among them.
- crew reads no `Sluice-From` to tell a piece merged, a fix merged or a bolt landed, and seeks no bolt's landing on main.
- A bolt's verification and its close rest on the same reading.

**Non-Goals:**
- **Places launched before their host's runner named itself a recipient.** Flume holds nothing of them for the runner. A piece Flume tidied so reads as the runner last carried it (Decision 3).
- **Decision 1 of `a-bolts-landing-on-main-reads-landed`.** It says where a kit's folder is read: the runner's `repositories.rec` (`runner.where`). That is the runner's report, and it stays.
- **Other readers of `Sluice-From`.** The landing card's pull request (`plan.pull_of`, read at the bolt's head) and a deploy offer's landings (`ops.RANGE`) name what a landing or a deploy carries, never a piece's end. Record 0062 does not name them. The landing card's goes with crew's own landing through sluice, which record 0056 retires on main.
- **Collecting or confirming a held record.** That is the runner's (Boomdrive record 0030). crew reads `pending_for` not at all.

## Decisions

### 1. A place's end is the record Flume holds for the runner, read as any status the runner carries

Nothing in `stage_of` or `flume_facts` changes. A held record is the place's tidied entry, its `over` landed at a commit or dropped, and crew already reads that as merged, landed or dropped. A Flume 0.20.0 fixture of a landing and a drop held for `boomdrive` pins the shape the runner carries (Task notes 1.1).

Not taken: telling a held record from another tidied one by `pending_for` naming `boomdrive`. The end is Flume's either way, and `pending_for` is what the runner acts on, not crew.

### 2. The three readings go whole

- **gather:** `FROM`, `landed_from`, `LANDINGS`, `bolt_landings`, `LANDED` and `main_landing` go. `kit` reads no `seek` and answers no `landed`, `landed_error`, `landings` or `landings_error`. gather reads with git only what it read before the stopgap.
- **runner:** `built_on_bolt` goes. `place_branch` stays, since `refs_standing` and `plan`'s launch check name the branch Flume refuses a launch over.
- **plan:** `Stages.landings` goes. `Stages.crossed` and `Stages.fixes` take `stage_of`'s answer as it is. `landing_sought`, `seek_answered`, `submits_read` and `submits_at` go, and `runs_at` reads `bolt.land` entries alone. `survey`'s `held` is `[(where, bolt)]` again: a kit already read serves any later step of the command (`plan.12`). `stages_for`, `bolts_view` and the rail's read seek nothing.

Not taken: keeping a reading as a fallback where the runner carries no end. That is the stopgap itself, and a fallback to another tool's record is what `read.1` and `roles.9` rule out.

### 3. A place tidied before the runner carried its end reads as last carried

Such a place was launched before its host's runner became a recipient, or its host's runner or Flume is older than Boomdrive's `76e0226` and Flume 0.20.0. It reads as `places.rec` last held it, submitted for instance. That is how it read before record 0062. The way on is the same too: its row is dropped by proposal, as record 0062's context says. No landing commit is read for it.

### 4. A launch the runner refused for a change the bolt holds reads refused

crew #479 read such a piece merged when another partition's launch had built it. That came from swancloud's relabel of afterthought to agentplot on 2026-11-07 (signal `2026-11-07-agentplot-planner-cbc41169/02`). `plan.22` (record 0060) now rules out renaming a partition. The runner's refusal is its word, and the piece reads refused with it (`stage_of`).

### 5. A fix is read as any piece

`fix_flume`'s `landings` goes, and `crew fix --drop` reads the fix's stage from the runner alone. A fix the runner reports merged holds its bolt's landing no longer, and its drop is refused (`runner.fixes_in_flight`, `runner.fix_drop_refusal`). The launch-date guard of `a-bolts-landed-fix-reads-merged`, Decision 2, goes with it. A fix launched again under a dropped launch's name reads its own place, and no landing is matched to it by name.

### 6. Verification and close, and what `crew bolts` says

- **Verification.** `runner.verification` is green only where a piece's commit, as the runner reports it, is the head. Its "as its landing on the bolt names it" wording goes.
- **What `crew bolts` says.** `runner.piece_said`'s `<branch> landed on its bolt at <commit>` detail goes. A merged piece's line gives its place, as for any merged piece.
- **Close.** A bolt closes through `runner.unlanded` as today: each piece merged at a commit main holds (bolt-teams "A landed bolt closes on its pieces' ends as the runner reports them").
- **The specs.** OpenSpec keeps every scenario of a modified requirement. So bolt-plan's "A fix read merged from its bolt's landing holds nothing" and bolt-teams' "A bolt whose landing main holds closes whatever the runner carried of its places" are removed, and added again under new names without their landing-commit scenarios. merge-gate's verification requirement is cited by name from bolt-teams and rail-cards, so it is modified in place. Its scenario "A landing read from the bolt's own landings" keeps its name, and its outcome is now none.
- **Views.** The views carry the same keys. `status.js` reads none of `on`, `branch` or `landed`, the keys `built_on_bolt` added, so the mod and `tests/py/test_board.py`'s pinned keys need no change (`code.8`).

### 7. When the bolt takes main in

This bolt meets main at its landing, by the take-main fix Flume launches on it (`plan.8`). Main then brings `started_land`'s fallback to `main_landed`, the last reader of `gather.main_landing`. The fix keeps this change's outcome:

- `main_landed` and its call in `started_land` go. A started bolt closes once `runner.landing_of` reads its base place landed. That reading is the record Flume holds for the runner after the base place's tidy, which `landing_outcome` reads through `flume_facts` as any status.
- A bolt started before bolts were base places is closed by the crew that started it. `crew bolt land` here refuses it in `runner.legacy_said`'s words, as bolt-teams "A bolt started before bolts were base places lands under the crew that started it" has it.
- Main's scenario "A base place the runner no longer carries" goes with the requirement this change removes.
- `stages_for`, `survey`, `bolts_view` and the rail's read lose their `seek` on main as here. The conflicts in `openspec/specs/` take this change's side.

Not taken:
- Writing this change against main's code. The bolt does not hold that code, so the code stage could not build it.
- Asking for the bolt to take main in first. `plan.8` takes main in early only on a forecast's conflict, and it buys nothing the landing's take-main fix does not do.

## Dependencies

This change's reading is whole only on a host whose runner carries Boomdrive's `76e0226` and whose Flume is 0.20.0 or later (`flume::LEAST`). Elsewhere a place tidied after landing reads as last carried (Decision 3), as before record 0062. A released host takes crew only at swancloud's bump, on the user's word (`plan.19`). That bump waits for the host's Boomdrive.

## Risks / Trade-offs

- **Rows from before.** A piece launched before its host's runner became a recipient, and tidied after this lands, stands at its last carried stage until it is dropped. Few places are in flight across the change; the runner carries every later one.
- **A held record crew reads after its collection.** The runner collects once its report holds the record. Flume then refuses the place's status, and the runner keeps the record as the last carried status. crew keeps reading it, so the end is not lost at collection.

## After deploy

None: a host's reading changes with the release it loads, and every scenario here is a logic or contract case.

## Task notes

**1.1** Add `tests/py/flume-0.20.0/` with `landed-held.json`, `dropped-held.json` and a `README` in the shape of `flume-0.17.0/README`. Each holds one place whose phase is Flume 0.20.0's `{"tidied":{"over":…,"at":…,"pending_for":["boomdrive"]}}`, its `place` `<location>@<at>`: one landed at a commit, one dropped. Record them from a host running Flume 0.20.0 where one holds such a record: `flume status --json --repository <container> <place>`, or a runner's `places.rec` on afterthought/crew-state. Otherwise make them from `flume-0.3.6/landed.json` and `dropped.json` by Flume v0.20.0's own types. The README says which, and how they are trimmed. In `tests/py/test_runner.py`'s `TestStageOf`, add:
- `test_a_landing_held_for_the_runner_is_merged_at_its_commit`: through a `stage`-like helper reading the new folder, merged at the record's commit on a bolt, and landed on main for `Base: main`;
- `test_a_drop_held_for_the_runner_is_dropped`.

`facts.flume_fixture` already takes a name with its folder.

**2.1** In `plan.py`:
- `Stages.crossed` drops its `built_on_bolt` call and the `res["carried"]` override.
- `Stages.fixes` returns `(work, launch, s)` with `s` from `runner.fixes_on` as it is.
- `crew fix`'s drop no longer calls `stages_for(...).landings`, and passes `fix_flume` no landings.
- `Stages.landings` goes. Every docstring in `plugin/lib/` and `tests/` that cites a removed requirement or record 0062's readings cites what replaces it, `runner.fixes_in_flight`'s and `TestABoltWhoseLaunchesWereAllRefused`'s among them.
- `runner.built_on_bolt` goes.

In `tests/py/test_stages.py`, `TestBuiltOnItsBolt`, `TestABoltLandedOnMain` and `LANDED` give way to `TestEndsHeldForTheRunner`, x, a, b and c as `TestCrossed.stages` has them. It holds:
- `test_a_place_landed_and_tidied_reads_merged_from_the_record_held_for_the_runner`: `ran({1: "flume-0.20.0/landed-held"})`, a merged at the record's commit, landed with `main=["a"]` (bolt-plan "A landing held for the runner");
- `test_a_place_tidied_before_the_runner_carried_its_end_reads_as_last_carried`: b at `submitted`, x's facts given a `landings` naming `change/b` that nothing reads (bolt-plan "A place tidied before the runner carried its end");
- `test_a_launch_refused_for_a_change_its_bolt_holds_reads_refused`: bolt-plan "A launch refused for a change the bolt holds".

`TestCrossed.test_a_crossed_bolts_landed_fix_reads_merged_from_its_bolts_landing` becomes `test_a_crossed_bolts_fix_held_for_the_runner_reads_merged`, its fix carried `flume-0.20.0/landed-held`.

**2.2** In `runner.py`:
- `verification`'s `how` goes: green always says "as the runner reports it".
- `piece_said`'s `st == "merged" and s.get("on") == "bolt"` line goes, and so does its docstring's clause.

`tests/py/test_runner.py`'s `TestVerification.test_a_piece_read_from_its_bolts_landing_says_so` goes. In `TestEndsHeldForTheRunner` add `test_a_head_held_for_the_runner_reads_green_and_one_only_a_landing_commit_names_reads_none`, holding merge-gate's "A landing held for the runner" and "A landing read from the bolt's own landings":
- every piece of x carried landed-held at its commit, x's `head` the last, gives `st.verification(...)[0] == "green"`;
- b last carried `submitted` with x's facts' `landings` naming `change/b` at the head gives `"none"`.

**2.3** `fix_flume` loses its `landings` parameter and its `built_on_bolt` call, reading the fix's stage as `runner.fixes_on` gives it. In `tests/py/test_fix.py`:
- `TestAFixItsBoltHolds` becomes `TestAFixTheRunnerReportsMerged`. With tidy launched as request 2 and carried `flume-0.20.0/landed-held`, tidy is merged, `runner.fixes_in_flight` is empty and x reads proven ("A landed fix holds its bolt's landing no longer"). With tidy carried `submitted`, tidy is submitted and in flight ("A fix the runner last carried at submitted").
- `test_a_fix_its_bolts_landing_reads_merged_is_not_dropped` becomes `test_a_fix_held_for_the_runner_landed_is_not_dropped`: rail-word carried landed-held, its drop refused and nothing appended ("A landed fix is not dropped"). Its submitted half keeps "the drop goes".
- The `place_branch` case stays.

**2.4** No code beyond 2.1. In `TestEndsHeldForTheRunner` add:
- `test_a_landed_bolt_whose_places_are_held_for_the_runner_closes`: x's facts gone (`exists` False, no head), a, b and c each carried landed-held, `plan.land_refusal("x", ["a", "b", "c"], st.of, [], "madswan", {<the record's commit>: 0}, "crew") is None`;
- `test_a_piece_whose_end_the_runner_never_carried_keeps_the_bolt_open`: b at `submitted`, its refusal `"unit b has not merged into bolt/x: it is submitted"`.

These are bolt-teams' two scenarios.

**2.5** In `plan.py`:
- `survey`'s `held` takes `(where, bolt)` pairs and puts no `seek` on a kit's request. A kit `READ.kits` holds serves the command unasked, the `seek_answered` filter gone.
- `stages_for` reads `runner_facts` alone.
- `bolts_view` and the rail's read (the two `landing_sought(…submits_at…)` comprehensions) build `[(t, b.name())]`.
- `landing_sought`, `seek_answered`, `submits_read` and `submits_at` go, and `runs_at` returns `{"landings"}` alone, its docstring with it.

`tests/py/test_main_landing.py` goes whole. Add `test_stages_for_asks_the_survey_for_each_started_bolt_and_seeks_nothing` to `TestEndsHeldForTheRunner`, the survey faked as `test_stages_for_seeks…` faked it: `asked == [(deneb's kit, "x")]`, each entry a pair.

**2.6** In `gather.py`:
- remove `FROM` through `main_landing` (lines 222–321 at `05ffe51e`);
- remove `kit`'s seek block and its per-bolt `bolt_landings` call;
- drop the module docstring's landings clause.

`ran` and `datetime` stay if anything else uses them. Remove an import nothing uses.

In `tests/contract/test_gather.py`:
- `test_a_bolts_landings_name_each_place_landed_on_it_before_and_after_the_bolt_lands_on_main`, `test_a_landed_bolts_landings_are_read_from_its_landing_on_main_once_its_branch_is_gone`, `landing` and `utc_of` go, unless another case uses them.
- `test_a_gather_of_a_kit_with_a_held_bolt_runs_no_sluice` gains `assert not {"landings", "landed", "landings_error", "landed_error"} & set(got["bolts"]["te"])`, its docstring naming merge-gate's "Nothing of sluice's is read" as this change words it. Its fixture's landing commits already carry `Sluice-From`.

`tests/py/test_kit.py`'s `TestLandedFrom` goes.

**2.7** `tests/py/test_bolt_commands.py`'s `test_a_bolt_whose_units_its_branch_holds_reads_where_it_runs_and_each_unit_merged` becomes `test_a_bolt_whose_places_the_runner_holds_ended_reads_each_unit_merged`:
- a and b carried landed-held at `"1" * 40` and `"2" * 40`, x's head `"2" * 40`, no `landings` given;
- `"x  crew  @ deneb  waits"` is in the text, each of a and b on a `merged` line naming its place and no "landed on its bolt".

`tests/py/test_rail.py`'s `test_a_bolt_whose_head_is_its_take_main_fix_landed_beside_the_queue_can_land` reads zone-one merged from the runner, by `runs(... at={"zone-one": "landed"} …)` or the held fixture, in place of `sv[…]["landings"]`.

**3.1** Each of the following says a unit's, chore's or fix's end is read from the runner's report, the record Flume holds for the runner after it tidies the place among them, and a landed bolt closes once each piece reads landed so, its branch standing or not. Each drops the sentences on `Sluice-From`, a landing on the bolt or main naming a branch, and a fix's landing at or after its launch:
- README's paragraph at line 61;
- `plugin/skills/crew/SKILL.md` line 10;
- `plugin/bin/crew`'s header, lines 9–12.

`tests/t-docs.sh` holds them to one another (`docs.2`).

**3.2** `tests/t-journey-land.sh`'s opening comment, at its near-reach case, cites bolt-teams' "A landed bolt closes on its pieces' ends as the runner reports them", which replaces the requirement it cites, and drops "Decision 3 of a-bolts-landing-on-main-reads-landed". The case itself lands a bolt with no pieces, from sluice's record, and is unchanged. Run it to show no later case of the file rested on a bolt's landings.
