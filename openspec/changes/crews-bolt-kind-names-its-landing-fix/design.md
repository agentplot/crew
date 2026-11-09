# Design

## Context

This section records what was read on 2026-11-08, so the decisions below rest on it. The proposal's *Why* says what the change is for.

**The base.** The place was cut at `4b813f18` from `bolt/crew-lands-through-the-runners-land-message`, which then held nothing beyond main. Everything this change narrows is built by the bolt's other unit, `crew-lands-each-bolt-through-flumes-base-place`. Its place was live in its verify stage, at `d4adecfc` on `change/crew-lands-each-bolt-through-flumes-base-place`, and not yet landed on the bolt. That unit builds:

- the kind, `plugin/flume/kinds/bolt@1/kind.toml`, with `version = 1`, `branch = "bolt"`, `lands = true` and `stages = []`, its bytes pinned by `tests/py/test_source.py` (`BOLT_KIND`);
- the read of a base place's status (`runner.flume_facts`), the landing's outcome (`runner.landing_of`, `landing_said`), and the act that records it (`plan.landing_read`). On a refusal for a conflict that act launches crew's take-main fix (`take_main_launch`, `runner.take_main`). On a refusal or a stop it asks ops (`unlanded_ask`);
- the fixes in flight that hold a row (`runner.fixes_in_flight`, read by `plan.py` near 3250 into `landing_rows`), and the drop asked again (`runner.base_drop_due`);
- ops's band's fixes in flight (`board.flume_waits`), and ops's brief: a forecast conflict's take-main fix is ops's to start, a failed check's fix too, and a refused conflict's is crew's.

This change is planned against that code as `d4adecfc` holds it, and its specs modify the requirements that unit adds. Its design leaves this one the landing fix: "crew's kind naming its landing fix (`crews-bolt-kind-names-its-landing-fix`). Until both, crew's read of a conflict launches the take-main fix as today."

**What Flume does with a landing fix** (agentplot/flume `site/src/content/docs/guides/merge-queue.md`, "Its fixes", and `guides/kinds.mdx`, "A kind with no stages", at v0.19.0; flume record 0056 as amended 2026-11-07; weir record 0005):

- A kind that lands with no stages may name `landing_fix`, the fix kind's whole identity with its version (`flume/fix@1` for Flume's own), and `max_landing_fixes`, how many fixes run before the place waits on its caller. Left out, that bound is the host's default (`status.rs`: `kind.fix_limit.unwrap_or(self.defaults.send_backs)`).
- Flume resolves the identity when the base place launches, and refuses the launch where it names no kind that lands and has stages. A bare name or one with no version is refused naming the field.
- While a base place waits on its caller, with no place on its branch live and no submission open, each settle has sluice forecast its branch against its base. A forecast conflict with the base itself, or a failed or conflicting submission, launches one fix of the named kind. The fix is cut from the branch, lands on it, and is named `<base place's name>-<n>`. It runs in the base place's stream at its priority, delivers to its recipients, and has a one-line brief over sluice's words: merge the base's revision first for a conflict, make the failed checks pass for a failure.
- Flume runs one fix at a time and acts on each forecast and each submission once. Every fix counts toward the bound, a launch it could not make among them. Past the bound, or once a fix is dropped, the base place waits on its caller with sluice's words. The submission stays the caller's.
- Flume 0.19.0's status of a base place (`crates/flume-core/src/answer.rs`, `PlaceStatus`; `crates/flume-seams/src/held.rs`) gives:
  - `fix_kind`: `{identity: {source, name, version, spelled}, from}`, written once at the launch and never resolved again;
  - `fix_limit`;
  - `forecast`;
  - `fixes`: each `{number, name, place, cause, launched, ended}`. `cause` is one of `{"forecast": {head, onto}}`, `{"failed": {submission}}` or `{"conflicted": {submission}}`. `ended` is `"live"`, `"landed"` with `commit`, `"dropped"`, or `"refused"` with `reason`.
  A fix's own status gives `fix_of`.
- deneb runs Flume 0.17.0, whose `weir-kinds` (weir `5562af52`) keeps a key it does not know among a kind's sections and never fails on it. There `landing_fix` is read by nothing: the base place launches with no fix kind, and its status gives none of the fields above.

**What the runner carries.** It carries Flume's status of each place it launched for crew, one record per launch request (`places.rec`, read on `afterthought/crew-state` `agentplot/runner/deneb` on 2026-11-08). A fix Flume launches for a base place is no launch of the runner's, so it has no record of its own. crew reads it only as its base place's status lists it in `fixes`.

**How many take-main fixes crew's bolts have needed.** crew's history names three: two on `crew-reads-each-piece-as-the-tools-hold-it` and one on `crew-talks-only-to-its-runner`.

**Rules this design relies on:**

- `roles.5`: a mechanism of crew's moves to its tool once that tool runs it on the host. The take-main fix moves to Flume wherever Flume's status shows it holds the bolt's landing fix.
- `roles.6`, `roles.9`.
- `read.1`, `read.2`: a fact the status lacks reads as none, never as Flume's.
- `code.7`, `code.8`.
- `plan.8`: a take-main fix Flume launches on the bolt takes main in.
- `plan.16`: a named bolt is held on its row for a fix on the bolt.
- `teams.25`, `docs.2`, `docs.6`, `tests.4`, `tests.10`, `tests.11`.

**Pages whose areas this change touches:** `core.md`; `plan.md` (`plan.py`); `briefs.md` (`plugin/roles/main-ops.md`, `plugin/skills/`); `tests.md` (`tests/`); `docs.md` (README, `openspec/`).

**Departures:**

- The sibling's Decision 2 says a change to the kind is `bolt@2` beside it. This change amends `bolt@1` itself, because no release or lock has carried it (Decision 2). That design is the sibling's, not a rule, and the pin's comment says so.
- `openspec/config.yaml`'s tasks rule asks for a last task running `tests/suite --affected`. This stage's brief has each task name the narrowest check that shows it done, and the verify stage runs the repository's whole checks once after every task, so the tasks end without it, as the sibling's do.

## Goals / Non-Goals

**Goals:**

- A bolt the merge queue sends back, or that Flume forecasts in conflict with main, gets its landing fix launched by Flume, with no agent or person deciding it. This needs a host whose Flume reads `landing_fix`.
- crew launches no fix and asks ops for none where Flume launches it, and asks ops once Flume's bound is spent.
- A live landing fix holds the bolt's land and its drop, as a fix crew launched does.
- Every view crew draws names the landing fix.

**Non-Goals:**

- Removing crew's take-main fix. It stays for a bolt whose base place names no landing fix (Decision 7).
- Reading Flume's forecast in place of crew's own. crew's landings-card forecast still holds a row that conflicts with main, and forecasts the rows among themselves, which Flume does not.
- Answering, dropping or showing the stage of a fix Flume launched. The runner's acts name crew's launches, and that fix is none of them (*Risks*).
- Any change to Flume, sluice, weir or Boomdrive.

## Decisions

### Decision 1: the place takes in the bolt once it holds its first unit

The kind, the landing read and the take-main path are the first unit's. This change cannot be built against `4b813f18`, where none of them exists, and its MODIFIED requirements need that unit's archived into `openspec/specs/`. So the first task merges `origin/bolt/crew-lands-through-the-runners-land-message` into the place once the bolt holds `crew-lands-each-bolt-through-flumes-base-place`'s landing. A merge, never a rebase, keeps the place's commits as they were made (`code.6`). Where the bolt does not hold it yet, the code stage stops short and says so, naming the unit it waits on. It does not build around the gap.

Paths not taken:
- Bringing the place to `d4adecfc` now. The first unit's work would then land on the bolt with this change, ahead of its own verify and review.
- Planning against `4b813f18`. Every function this change narrows is rewritten by the first unit.

### Decision 2: `bolt@1` names `flume/fix@1` and at most three landing fixes

```toml
# crew's bolt as a Flume base place, naming its landing fix (record 0056; crew-lands-each-bolt-through-flumes-base-place, Decision 2; crews-bolt-kind-names-its-landing-fix, Decision 2).
[kinds.bolt]
version = 1
branch = "bolt"
lands = true
stages = []
landing_fix = "flume/fix@1"
max_landing_fixes = 3
```

- **`flume/fix@1`.** A fix on a bolt is already a place of Flume's own fix kind (`runner.fix_launch`), and a take-main fix is one of those. Flume carries `fix@1`, its one stage code, so no lock is needed for it. Weir record 0005 asks for the whole identity with its version, so one version of crew's kind always means one fix.
- **Three.** This is Flume's documented default, and more than crew's bolts have needed (*Context*). Naming it makes the bound the kind's, not the host's send-back default, which a host's configuration may change.
- **`bolt@1` itself.** No release tag carries `bolt@1` and no host has locked it: the first unit has not landed, and this bolt carries both. So the kind's first release holds the landing fix, and the one hash a host locks is the one this bolt lands with (*After deploy*). The comment line names this change beside the first unit. The logic case that pins the bytes, `BOLT_KIND` in `tests/py/test_source.py`, takes the new bytes and keeps its comment that a released version never changes.

Paths not taken:
- `bolt@2` beside `bolt@1`. That would release a version no host should run, two packages to lock, and a start that must name the version.
- A fix kind of crew's own. That is a package to lock and keep, for what Flume's fix already does.
- Leaving the bound out, so the host's default decides it.
- Two, `train`'s example in Flume's guide, which a bolt that main moves past twice in a day would spend.

### Decision 3: crew reads the landing fix from the base place's status

`runner.flume_facts` gains three facts, each guarded so an absent field or one of another shape reads as none (`read.2`):

- `fix_kind`: the identity's `spelled` text.
- `fix_limit`: a count.
- `fixes`: a tuple of `{number, name, place, cause, submission, head, onto, ended, commit, reason}`. `cause` is `forecast`, `failed` or `conflicted`. `submission` is the merge queue's id for the two submission causes, and `head` and `onto` are the revisions for a forecast. `ended` is `live`, `landed`, `dropped` or `refused`. A fix crew can't read whole is left out and named in `fixes_unread`, so nothing is guessed of it (`read.1`).

A new decision of plain facts, `runner.landing_fix(f)`, gives the base place's landing fix as Flume holds it (`code.7`):

- **None** where `f` names no fix kind. Flume launches no fix for this bolt: its Flume predates 0.19.0, or the base place was launched before its host had one.
- Otherwise `{kind, limit, ran, live, fixes}`. `ran` counts every fix Flume listed, refused ones among them. `live` is the one fix whose `ended` is `live`, or None.

`runner.landing_of` attaches it to its outcome as `fix`, for every outcome it reads from Flume's status. For a refusal it also says whose the way on is, as `by`:

| The base place's status | `by` | crew |
|---|---|---|
| no fix kind | `crew` | launches the take-main fix for a conflict and asks ops for a failed check, as before |
| a fix whose cause names the refused submission is live, or landed | `flume` | launches nothing, asks nothing |
| no fix names the refused submission, and `ran` is below `limit` | `flume`, marked `due` | launches nothing, asks nothing: Flume launches it at its next settle, acting on each submission once |
| no fix names it and `ran` is at `limit`, or the newest fix naming it ended `dropped` or `refused` | `caller`, with Flume's words and `ran` | asks ops (Decision 4) |

A forecast fix names no submission: it holds the bolt as Decision 5 has it, whatever the landing's outcome.

Path not taken: reading the host's Flume version. crew names no tool's version in what it decides (record 0056 point 1), and a base place launched before an upgrade keeps no fix kind whatever runs now. The status says per bolt what Flume holds.

### Decision 4: a refused landing's way on

`plan.landing_read` records a refused landing as it does now, in Flume's words, its `bolt.submit` refused at the head sent back. Then it acts on `l["fix"]["by"]`:

- **`flume`.** No `take_main_launch`, no `unlanded_ask`. What it prints, and the row, say whether Flume's landing fix runs or is due.
- **`caller`.** `unlanded_ask` asks main-level ops, keyed by the land's request as now. Its words read: `Flume ran <ran> of its <limit> landing fixes on bolt <b>, and its landing was refused: <Flume's words>`, or `Flume's landing fix <name> was dropped` or `could not be launched: <reason>`. No take-main fix is launched, so a conflict past the bound is ops's to fix by hand or to take to the planner and the user. crew launching another would run past the bound the kind sets.
- **`crew`.** As now.

### Decision 5: a live landing fix holds the bolt

`runner.fixes_in_flight` returns, beside crew's own fixes on the bolt, each live fix in the bolt's base place's status. Each is keyed by Flume's name for it, `<bolt>-<n>`, which no crew fix's key shares, since crew's are `fix/<bolt>/<name>`. Its note is crew's words for its cause:

- a forecast or a conflict: `Take main into the bolt: Flume's landing fix <name> merges main at <onto or the refused entry's base, seven>`, beginning with `TAKE_MAIN`;
- a failed check: `Flume's landing fix <name> makes the failed checks pass: <first line of Flume's words>`.

So, through `landing_rows` as it stands:

- **No box while it is live.** The row has no box and no land is posted for it. Without this, the runner's land would be refused while a place on the branch is live, the row read stopped and the user's send spent (the sibling's "A landing stopped by nothing of the bolt's is recorded stopped, and its send is spent").
- **Taking main in.** A fix that takes main in leaves the row taking main first. The send that ticked it stands through it (rail-cards "A send stands for a ticked bolt taking main in"), so once the fix has landed and the bolt reads proven at its new head, the next raise posts the land again, with nothing asked.
- **A failed check.** A fix for a failed check holds the row for it. Once it has landed, the send stands only where the bolt's own work is unchanged, as for any fix.

`runner.base_drop_due` counts a live landing fix as a piece live on the bolt's branch, so a drop Flume refused is not asked again while it runs. A refused landing whose way on is `flume` and `due` is held on its row by the refusal at its head, as now. The row's words say Flume launches its landing fix.

### Decision 6: the views

- **`runner.landing_said`.** It ends a refused landing's words with one clause: `; Flume's landing fix <name> takes main in` or `… makes the failed checks pass`, `; Flume launches its landing fix`, or `; Flume ran its <ran> landing fixes, and it waits on ops`. For any outcome with a live forecast fix, it says `Flume's landing fix <name> takes main in` where it said nothing. The bolt's head line, `crew bolts` and ops's band draw these words as they stand.
- **`board.flume_waits`.** Its `fixing`, ops's band's fixes in flight, gains each live landing fix of a started bolt, read from the ledger's `landing` (`plan.Stages.landing`): `{fix: <name>, repo, host, stage: "landing fix", said: <its note>}`, after the take-main fixes. The band's head line counts it among the fixes in flight.
- **`plugin/hooks/status.js`** draws a view's segments as given, so it is unchanged. A case in `plugin/tests/` draws ops's band with a landing fix in flight (`code.8`).
- **The ledger's rows** list crew's fixes with their stages, and Flume's landing fixes are left out of them. crew reads no stage of such a fix but its end, and the head line names it.

### Decision 7: what stays crew's, and the brief

- **crew's take-main fix.** `take_main_launch`, `runner.take_main` and the rows' `TAKE_MAIN` words stay for a bolt whose base place names no landing fix. Removing them is a change of its own once no such base place can stand (`roles.5`). It is not listed here (record 0053).
- **A take-main fix by hand.** `crew fix <bolt> take-main-…` is not refused where Flume holds the landing fix. `roles.3` adds a check once an agent breaks a rule its brief states, and the brief and the row now say Flume's landing fix covers it. Path not taken: refusing it on the base place's status, a read the `crew fix` path does not make today.
- **`plugin/roles/main-ops.md`, *Landing a bolt*.**
  - *Step 1, a forecast conflict:* where the row says Flume's landing fix takes main in, or that Flume launches it, ops starts nothing and tells the user in one line. Only where the row names no landing fix of Flume's, or says Flume has run its bound, ops starts the take-main fix as now.
  - *A check that failed:* the same, for the fix that makes the checks pass.
  - *A conflict with main:* Flume's landing fix takes main in where the row names it, and crew's take-main fix where it names none.
  - *Past the bound:* crew asks ops in Flume's words. Ops starts a fix on the bolt by hand with them, or, where it judges the bolt should not land, tells the planner and the user in one line.
  - *A landing fix that asks:* Flume tells ops, as the fix's recipient. Crew cannot answer it, so ops tells the user it waits and on what.
- **README and `plugin/skills/crew/SKILL.md`** say the same where they say what follows a refused landing (`docs.2`). The usage header is unchanged, since no command's usage changes.

## Risks / Trade-offs

- **[A landing fix that asks, or stalls, can't be answered through crew.]** → The runner's acts name crew's launches, and Flume's fix is none of them. Its question reaches ops as its recipient, and the user answers it or drops it with Flume on the host. The bound and Flume's stall mark keep it from waiting unseen, and the bolt's head line says the fix is live. Answering it would take the runner carrying the places Flume launches for a launch, which is Boomdrive's to build. Until then this is a gap of reach, not of correctness.
- **[A dropped bolt with a live landing fix.]** → Flume refuses the base place's drop while the fix is live. crew asks the drop again only once the fix has ended (Decision 5), so the bolt's branch stays until then.
- **[A host whose Flume reads no `landing_fix`.]** → Its base places name no fix kind, and crew acts as before (Decision 3). The same holds for a base place launched before its host's Flume was upgraded, since a fix kind is resolved only at the launch.
- **[A read between a refusal and Flume's settle.]** → The refusal reads `flume`, `due`, and crew does nothing (Decision 3). Flume acts on each submission once, so the next read finds the fix.
- **[A forecast fix and crew's own forecast.]** → Both may find the conflict. Flume launches the fix, and crew's forecast holds the row, which the live fix's note then words as taking main in (Decision 5). Nothing launches twice, provided ops follows its brief (Decision 7).

## Migration Plan

Nothing in a file crew writes changes shape. `requests.rec` and the run record are as the first unit leaves them. The kind's bytes are new before any host holds them.

## After deploy

- **Lock `crew/bolt@1` at the hash of the package as this bolt lands it.** This is the first unit's step, its hash now this change's. The doer is the host's configuration, swancloud's or Boomdrive's flake, by `flume kinds lock --host crew/bolt@1`, in every environment whose runner takes crew's partitions' work, before the release that carries this bolt reaches it. It is no check of crew's, since the lock is the host's file. A lock made at the first unit's bytes alone would refuse every bolt start.
- Flume launches landing fixes only once a host runs Flume 0.19.0 or later. That is no step of this change's, since crew acts as before until it does (Decision 3).

## Open Questions

None.

## Task notes

**1.1** Run `git fetch origin` and read `git log origin/bolt/crew-lands-through-the-runners-land-message` for the landing of `crew-lands-each-bolt-through-flumes-base-place`, a merge commit naming its place's branch. Where it is there, `git merge --no-edit origin/bolt/crew-lands-through-the-runners-land-message` in the place. It merges cleanly, since the place holds only this change's `openspec/changes/crews-bolt-kind-names-its-landing-fix/`. Where it is not there, stop short with `flume needs "crews-bolt-kind-names-its-landing-fix builds on crew-lands-each-bolt-through-flumes-base-place, which bolt/crew-lands-through-the-runners-land-message does not hold yet: its code waits for that unit's landing on the bolt"` and build nothing. Read the code at the merge, and where it differs from `d4adecfc` as *Context* describes it, follow the code and name the difference in your summary.

**2.1** Write `plugin/flume/kinds/bolt@1/kind.toml` as Decision 2 gives it, the comment line first. In `tests/py/test_source.py`, `BOLT_KIND` takes the same bytes, and its comment says a version's bytes never change once released, `bolt@1`'s first release naming its landing fix (this change, Decision 2). `test_the_package_ships_as_pinned_and_is_a_base_place` asserts the parsed table holds the six keys and values. Add one case: the package parses with `landing_fix` an identity with a source, a name and a version (`^[a-z0-9-]+/[a-z0-9-]+@[0-9]+$`) and `max_landing_fixes` a positive integer. `tests/t-flume-source.sh` compares the package with crew's plugin by `cmp`, so it needs no change.

**3.1** Add `tests/py/flume-0.19.0/`, with a `README` and `version.txt` as `tests/py/flume-0.17.0/` has them. Its fixtures are written from Flume 0.19.0's shapes (`crates/flume-core/src/answer.rs` `PlaceStatus`, `crates/flume-seams/src/held.rs` `ForecastHeld`, `FixCause`, `FixEnded`, `BaseFix`, `FixKind`), since no host ran this kind when they were made, and the README says so. Each is a base place of `crew/bolt@1` on `bolt/y`, with `fix_kind` `flume/fix@1` and `fix_limit` 3:
- `bolt-conflict-fixing.json`: verdict conflict on entry `412` against main at `9f1c2ab…`, and one fix `y-1`, cause `conflicted` `412`, `ended` `live`.
- `bolt-failed-fix-due.json`: verdict failed on `412`, and no fixes.
- `bolt-failed-spent.json`: verdict failed on `415`, and three fixes, landed, landed and refused, none naming `415`.
- `bolt-forecast-fixing.json`: waiting on its caller, no submission, and one fix `y-1`, cause `forecast` with a head and onto, `live`.
- `bolt-conflict-dropped.json`: verdict conflict on `412`, and one fix `y-1` naming it, `dropped`.
- `bolt-fixed-landed.json`: verdict conflict on `412`, and `y-1` naming it, `landed` at a commit.

`flume_facts` reads `fix_kind`, `fix_limit`, `fixes` and `fixes_unread` as Decision 3 has them. Cases in `tests/py/test_runner.py`, class `TestBasePlaceFixes`:
- each fixture's facts;
- every `flume-0.17.0/bolt-*.json` reading `fix_kind` None and `fixes` empty;
- a fix with an unknown `ended` or a `cause` of no known shape left out and named in `fixes_unread`;
- `fix_limit` a string reading None.

**3.2** `runner.landing_fix(f)` and `landing_of`'s `fix` and `by` as Decision 3's table, on the fixtures of 3.1 and those of `flume-0.17.0/`. Cases in `tests/py/test_runner.py`, class `TestLandingFix`, one per row of the table:
- `bolt-failed.json` of 0.17.0 reads `by` `crew`;
- `bolt-conflict-fixing` reads `flume` with `y-1` live;
- `bolt-failed-fix-due` reads `flume` and `due`;
- `bolt-failed-spent` reads `caller` with `ran` 3;
- `bolt-conflict-dropped` reads `caller`, naming the drop;
- `bolt-fixed-landed` reads `flume`;
- `bolt-forecast-fixing` with no land posted reads outcome `none` with `fix.live` `y-1`.

**4.1** In `plan.landing_read`, after the entry is emitted: call `unlanded_ask` for a refusal only where `l.get("fix", {}).get("by")` is `caller` or `crew`, or for a stop, and with the `caller` words of Decision 4 for `caller`. Call `take_main_launch` only where `by` is `crew`. Cases in `tests/py/test_landing.py`, `TestTheLandingsRecord`, beside `test_a_conflict_launches_the_take_main_fix_with_mains_revision_and_flumes_words`, which keeps its fixture of 0.17.0 and passes as it is:
- `bolt-conflict-fixing`: the refusal recorded, nothing taken, nothing asked;
- `bolt-failed-fix-due`: the same;
- `bolt-failed-spent`: one ask of ops whose words name 3 landing fixes and Flume's words, keyed `request/<kit>/<the land's request>` as `test_a_stop_keeps_the_rows_box_and_asks_ops` reads a stop's, so a second read asks nothing more, and nothing taken;
- `bolt-conflict-dropped`: one ask naming the drop, nothing taken.

**4.2** `runner.fixes_in_flight(requests, reads, bolt)` adds each live landing fix of the bolt's base place, read from the runner that took `bolt/<bolt>` (`landing_of`'s `fix`), keyed and worded as Decision 5. `landing_rows` needs no change: its `TAKE_MAIN` test and its `held for a fix` words take the note. Cases:
- `tests/py/test_runner.py`, in `TestBasePlaceFixes`: `fixes_in_flight` on `bolt-conflict-fixing` gives `{"y-1": "Take main into the bolt: Flume's landing fix y-1 merges main at 9f1c2ab"}`, and nothing on `bolt-fixed-landed`.
- `tests/py/test_landings.py`, beside `test_a_take_main_fix_in_flight_holds_its_row_as_taking_main_first_in_its_words`:
  - beside `x`, which can land, a row `y` with a live conflict landing fix has no box and takes main first, naming `y-1`, and `card_rows` keeps it on the card unticked;
  - a row with a live forecast landing fix takes main first, naming `y-1`, and the raise appends no request;
  - a row with a live failed-check landing fix is held for it in its words;
  - `runner.lands_due` posts nothing for either on a standing send;
  - once `y-1` has landed and the row reads proven at a new head with its own work unchanged, `lands_due` posts one land on the same send.

**4.3** `runner.base_drop_due` asks no drop again while the bolt's base place lists a live landing fix. Cases in `tests/py/test_runner.py`, beside the cases of the sibling's "Not while a piece is live": a refused drop with `y-1` live asks nothing, and one with `y-1` ended asks once.

**5.1** `runner.landing_said` as Decision 6, and `board.flume_waits`' `fixing` gaining live landing fixes. Cases:
- `tests/py/test_runner.py`: `landing_said` on each fixture of 3.1, the clause as Decision 6 words it. `crew bolts` and the bolt's head line print `landing_said`, so these cases prove what they say of a landing fix.
- `tests/py/test_landings.py`: a row held by its refusal at its head, the run record's `Refused` written by `landing_said` on `bolt-failed-fix-due`, says Flume launches its landing fix.
- `tests/py/test_board.py`: `ops_view` of a partition with one bolt whose landing has `y-1` live lists `fix y-1  landing fix  Take main into the bolt: …` and counts `1 fix in flight` on its head line; a bolt's head line on `bolt-failed-spent` ends with `Flume ran its 3 landing fixes, and it waits on ops`; the case pinning every key the mod reads still passes with no new key.

**5.2** In `plugin/tests/status.test.ts`, one case beside the sibling's "ops's band draws a landing asked with its request": a views file whose `<label>-ops` view holds the fix line of 5.1 draws it above ops's prompt as given.

**6.1** `plugin/roles/main-ops.md`, *Landing a bolt*, as Decision 7: step 1's take-main sentence, the bullets *A check that failed* and *A conflict with main*, and a bullet on a landing past its bound and a landing fix that asks. `tests/t-briefs.sh` gains `has` checks on `crewpy brief wldn main-ops` for "Flume's landing fix", "start nothing" beside it, and "ran its" for the bound. Its `# Reads:` line already takes `plugin/roles/`, so `tests/moon.yml` is unchanged; run `tests/moon-tasks` to confirm it writes nothing.

**6.2** README's *Bolts* and landings card passages, and `plugin/skills/crew/SKILL.md`'s landing section: where a refusal for a conflict launches crew's take-main fix, or a failed check is ops's fix, say that Flume launches the bolt's landing fix where its base place names one, at most three, and that crew's take-main fix and ops's are for a bolt whose base place names none or whose bound is spent. Check with `tests/suite t-docs`.
