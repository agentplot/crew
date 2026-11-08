# Design

## Context

The proposal says why this change is needed. This section records what was read on 2026-11-07, so the decisions below rest on it. The change starts from the written proposal of `crew-renames-no-kit` (agentplot/crew 0a993f48, kept in deneb's crew repository), whose Decisions 2 to 5 it keeps. That proposal also removed the command (its Decision 1). This change does not: the unit's intent leaves `crew kit rename` as it stands, and record 0060 keeps it.

**The readers the rename change built.** `a-kit-renamed-on-its-host-is-renamed-across-the-plan` landed on `teamless/deneb` as sluice #440 (805679d7) and reached crew's main with `teamless/deneb` (#1, v0.42.0). At 7a7b8acd, `plugin/lib/plan.py` holds:
- **The renames.** `kit_now` and `renames_in` at 1755 to 1774. `runs_at`, `landings_at`, `renames_at`, `kits_at` and `renames_read` at 2335 to 2386: `runs_at` reads `bolt.land` and `kit.rename` entries in one pass under `runs-<tip>`. `Write.renamed` at 1034, `Write.renames` at 1065 and `Write.kits` at 1071. `Direct.renames` and `Proposed.renames` at 5861 and 5886.
- **The reads through them.**
  - `kit_labels` (1646) and `partition_kits` (2323).
  - `runner_facts` and `launches_now` (2212 to 2231). `raise_proposal_at`'s read of where a proposal's kit runs (8007).
  - `landing_at` (5347). `main_fix_change` and `main_fix_work` (9559 to 9599).
  - `record_items` and `proposal_records` (7177, 7228), fed by `plan_propose` (7283).
  - `rail_record`'s operations entries (11264). `row_gone`, `record_now`, `record_settled` and `record_proposed` (11523 to 11600). `sweep_judged` (11678).
  - `rail_runs` and `rail_read`'s `renames` map (11850 to 11911). `sweep_judgments` (15362).
- **A former name given.** `kit_given`, `former_said` and `former_kept_said` (5965, 1701, 1707), used by `op_bolt_new` (5979) and `op_unit_add` (6146).
- **The command's own read.** `rename_refusal` (1718) refuses "`<old>` is `<now>` since its rename", reading `kit_now` over the write's renames. `op_kit_rename` (6408) passes it `w.renames()` and appends to `w.renamed`.

Elsewhere:
- `ops.landings` (`plugin/lib/ops.py` 241 to 252), which imports `plan` for the renames, and `ops.raise_deploy`'s landings at 705, which take `kit.rename` entries beside `bolt.land`;
- `page.deploys`, whose entries at 185 to 189 take `kit.rename` beside `bolt.land`, and `page.fleet_kits` (266 to 275);
- docstrings in `plugin/lib/runner.py`: `kept_folder` (365), `where` (387), `main_fixes_waiting` (1079), and the descriptor comment at 194.

**What the live partitions hold.** Read from crew's cache of afterthought/crew-state: `refs/crew/madswan/main` at 12127bbe, `agentplot/main` at 78c4a3a8, `afterthought/main` at ed16e640 and `swancloud/main` at d4a494b4; and of WilldanGroup/crew-state, `wldn/main`.
- **madswan.** It holds two `kit.rename` entries, written at 2026-11-06 00:09Z by the approval of proposal 241: `flywheel-cloud` to `boomdrive-cloud` (Count 2) and `tailrace` to `timber` (Count 21). Its plan holds no bolt or unit. Its landings not refused are under the names they were made in: `tailrace` 4, `timber` 2, `flywheel-web` 4, `boomdrive-cloud` 1, and `sluice`, `paymaster`, `flume` and `weir`. Its `requests.rec` names `flywheel-cloud` twice, `boomdrive-cloud` twice and `timber` six times.
- **agentplot, afterthought, swancloud and wldn.** None holds a `kit.rename` entry.
- **Proposals.** No open proposal holds `kit rename`.

**The bolt.** `crew-reads-a-kit-by-its-name-alone` holds two units. This one comes first. Then `a-repository-is-renamed-by-one-explicit-command` makes `crew kit rename` record 0060's command: refused while the repository's work stands, and renaming every record a reader matches by. Its work starts from `fix/a-kit-rename-renames-every-record-naming-it` (a31916d7), which takes the same readers out.

**The family.** Boomdrive's record 0021 and Flume's record 0053 rule that no tool follows a rename in flight. A repository is added or removed, and there is no rename. crew's part here is to stop reading through renames. No other tool is asked for anything.

**Area pages this change touches:**
- `core.md`: `state.1`, `state.2`, `state.4`, `roles.1`, `roles.5`, `roles.9`, `read.1`, `read.5`, `code.7` and `code.8`.
- `plan.md`: `plan.1`, `plan.4`, `plan.12` and `plan.22`.
- `record.md`: `record.4`.
- `teams.md`: `plugin/bin/crew`'s usage.
- `briefs.md`: the planner's brief.
- `tests.md`: `tests/`.
- `docs.md`: README, the skill and the specs.

No rule changes. `plan.22` (record 0060, accepted 2026-11-07) already says that no reader maps a former name. The pages are the design agent's (`docs.7`), so none is edited.

## Goals / Non-Goals

**Goals:**

- No reader maps a kit's name through `kit.rename` entries or through any list of former names. Each kit is read by the name its record gives it (`plan.22`).
- `requests.rec` and the run record are written only by appending (`record.4`, `state.1`).
- `crew kit rename` stays as it stands: its grammar, its role, its card block, its act and what it rewrites.

**Non-Goals:**

- Record 0060's command, which is the bolt's next unit. That covers the refusals while a repository's work stands, the rename of every record a reader matches by, and the rewrite `record.4` now allows.
- What a refusal offers as the way on for a kit a host does not keep (Decision 4).
- Rewriting madswan's records. Its plan stays as proposal 241 left it, and its two entries stay as written.
- Moving any repository between partitions.

## Decisions

### 1. No reader maps a kit through `kit.rename` entries

These go:
- `kit_now`, `renames_in`, `renames_at`, `renames_read` and `runs_at`;
- `Write.renames`, `Write.renamed`, `Direct.renames` and `Proposed.renames`;
- `launches_now`, `main_fix_work` and `record_now`.

Each read through them reads its record as written:

| Read | After this change |
|---|---|
| A partition's kits (`partition_kits`, `kits_at`) | The plan's and the landings' `Repo` as written, each once. `partition_kits(plan, landings)` loses `renames` |
| A kit's partitions (`kit_labels`) | `kit_in(kit, kits_read(fleet, l))` |
| The run record's acts at a tip | `landings_at(repo, tip)` alone reads `runs/`, its `bolt.land` entries, in one read per tip kept under `landings-<tip>` (`plan.12`) |
| A partition's launches (`runner_facts`, `rail_runs`, `raise_proposal_at`) | `requests.rec`'s records as written |
| A landing's kit (`landing_at`) | Its last queued submission's `Repo` as written |
| A fix of main (`main_fix_change`) | Its work is `fix/main/<kit>/<name>` for every mode, as the row's kit names it |
| A source's repository (`record_items`, `proposal_records`) | As written. `renames` leaves both, and `plan_propose` passes none |
| Card keys (`row_gone`, `record_settled`, `record_proposed`, `sweep_judged`) | The key's kit as written. `renames` leaves each, and `row_gone`'s close for a renamed kit goes. `sweep_judgments` passes none |
| A kit's landings and deploys (`ops.landings`, `page.deploys`, `page.fleet_kits`, `rail_record`) | Each entry's `Repo` as written. `kit.rename` leaves the entries they read, and `ops.py` no longer imports `plan` for it |

`runner.main_fixes_waiting` goes on naming a fix's kit from its launch's `Repo`, which is the launch's own field. Only its docstring's rename clause goes.

The board's views read kits from `partition_kits` and keep their shape, so `board.agent_views` and `plugin/hooks/status.js` are untouched (`code.8`). Each read stays a function of plain facts (`code.7`).

Alternatives considered:
- **Keep `kit_now` for history alone,** reading the entries madswan wrote. Rejected: that is the reader `plan.22` rules out ("a reader through `kit_now` or the run record's `kit.rename` entries"), and history reads as written without it (Decision 5).

### 2. A command given a kit writes it as given

`kit_given`, `former_said` and `former_kept_said` go. `op_bolt_new` writes `a.repo`. `op_unit_add`, for a unit or chore alike, writes `a.repo` or the bolt's `Repo`. It checks `a.repo in (None, kit)` against the bolt's kit, so a former name of the bolt's kit is refused as "bolt `<b>` is in `<kit>`, not `<repo>`". Nothing prints "written as".

### 3. `crew kit rename` stays, but for its one reader

These stay:
- the command's grammar;
- its place in `PLAN_WRITES`, `PROPOSABLE`, the role table (`plan.may_write`, `roles.1`), `OPS`, `COMMANDS` and `ACTS`;
- its card block (`cards.renamed_drawn`);
- its `kit.rename` entry and `Op`'s `fields`;
- what it rewrites, the `Repo` of the plan's Bolt and Unit records (`renamed_in`).

One refusal goes: "`<old>` is `<now>` since its rename: crew kit rename `<now>` `<new>` renames it again". It mapped `<old>` through the write's renames, so it is a reader through `kit.rename` entries. `rename_refusal` loses its `renames` argument and that branch. `op_kit_rename` stops appending to `w.renamed`, which only `Write.renames` read.

A name an earlier rename renamed is then judged as written, as any name is. Where neither the plan nor the landings name it, it is refused as no kit of the partition, and the refusal names no rename. Where its landings still name it, it passes that check and meets the spaces check like any name. `Write.kits()` reads the plan as the write has left it so far, so a command after a rename in one proposal sees the renamed records without any renames list.

Alternatives considered:
- **Keep the "since its rename" refusal** by reading the entries in the command alone. Rejected: it is a reader through `kit.rename` entries, which the unit's intent and `plan.22` rule out.
- **Remove the command,** as 0a993f48 did. Rejected: the unit's intent leaves it as it stands, record 0060 keeps it, and the bolt's next unit builds it.

### 4. The refusals that name `crew kit rename` stay

`main_kit_said` still ends "; if it was renamed on its host, crew kit rename `<kit>` `<new>` names it so in the plan". `runner.kept_folder`'s refusal for a kit the runner reports not keeping still ends the same way. Both stay true of the command as it stands: it renames the plan's records, and a started bolt's work is found by its branch (`bolt_launches` by `Base`), so the bolt is read where the runner keeps the new name.

Record 0060 makes the command refuse while the repository's work stands and before the runner's removal of `<old>`. The way on such a refusal offers is then the next unit's to say, so it is left here as it stands.

Alternatives considered:
- **Drop the clause now,** as 0a993f48's Decision 4 did once the command went. Not taken: the command stays, and changing what other commands say of it belongs with the change that decides when it may run.

### 5. Where a runner keeps a kit stays the runner's report

The runner's `repositories.rec` (`REPOSITORIES`, `host_read`'s `repositories`), `kept_folder` and `where`'s `kit` stay. They rest on `roles.9`, not on a rename: where a kit lives on a host is the runner's report. `kept_folder` already compares the kit it is given by name or forge address. Its callers now pass the kit as the plan gives it, never one read through renames. Its docstring, `where`'s, `main_fixes_waiting`'s and the descriptor comment at `runner.py` 194 cite `roles.9` and the drive-state spec, not the rename change.

### 6. Entries already written stay, and print as before

madswan's two `kit.rename` entries, and any the command writes from here on, are never rewritten or removed (`record.4`). crew reads them as renaming nothing: `landings_at` reads `bolt.land` alone, and no reader looks for `kit.rename`. `record.py` is unchanged: its descriptor allows the entries' fields, so they stay valid under `recfix --check` on every write (`plan.1`), and `crew events` and `crew trace` print them as before.

What this leaves on madswan:
- **Its kits** read as `boomdrive-cloud`, `flume`, `flywheel-web`, `paymaster`, `sluice`, `tailrace`, `timber` and `weir`: `tailrace` by its four landings, beside `timber`, as `flywheel-web` already stood by its own landings. The board and the page show `tailrace`'s last landing under that name.
- **The main level's folders** leave `tailrace` out, as deneb keeps none (`crew.kits_on`). No landings card is raised for it, since no bolt of it waits.
- **The launches under `flywheel-cloud`** read as `flywheel-cloud`'s. Their work is in no plan, so no decision reads them.

### Rules relied on

- **State:** `state.1` (one commit through crew, never merged), `state.2` (the plan is intent alone), `state.4` (views from the files and the run record).
- **Roles:** `roles.1` (the role table keeps the command), `roles.5` (crew changes here by a removal), `roles.9` (where a kit lives is the runner's report).
- **Reading:** `read.1` (a name crew can't place is refused by name, never guessed), `read.5` (the run record from the branch alone).
- **Code:** `code.7` (each read stays a decision of plain facts), `code.8` (the views keep their shape).
- **Plan:** `plan.1` (`recfix --check` of a branch holding the entries), `plan.4` (proposal 241's `Do` lines stay as written), `plan.12` (one read of `runs/` per tip), `plan.22` (no reader maps a former name).
- **Records:** `record.4`.
- **Docs:** `docs.2` (usage, README and skill together), `docs.4`, `docs.7`.
- **Tests:** `tests.4`, `tests.11`, `tests.12`.

### Departures

- **`openspec/config.yaml`'s tasks rule** asks for a last task that runs `tests/suite --affected`. This change's construct brief has the verify stage run the repository's checks once, after every task, and has no task check every part the change touches. So no task runs `--affected`, and each task names only the narrowest check for itself.
- **`record.4` as amended by record 0060** allows one rewrite, `crew kit rename`'s. The unit's intent keeps `requests.rec` and the run record append-only "without exception". These do not conflict: this change builds no rewrite, and bolt-plan's "requests.rec and the run record are only appended to" states what is built. The next unit changes that requirement when it builds the rewrite.

## Risks / Trade-offs

- **madswan's history shows an old name.** `tailrace` reads beside `timber` on the board and the page. Accepted: it is the user's model, and it matches `flywheel-web`.
- **A rename in flight now reads its old records as written.** Until the next unit makes the command refuse while work stands, a rename run over standing work leaves some records under the old name. That covers launches, a fix of main and a review batch's unit read from its launch's `Repo` (`batch_unit_at`). A started bolt still reads and lands by its branch (Decision 4). A fix of main stays on the old name's row and is sent under that name, and a batch's unit may be refused naming the runner's repositories. Accepted: it is what reading as written means, `plan.22` rules out the rename in flight, and no partition holds such a rename today.

## Migration Plan

1. Build on `change/no-reader-maps-a-kits-former-name`, cut from `bolt/crew-reads-a-kit-by-its-name-alone`. Flume submits it to the bolt, and it reaches main with the bolt's landing.
2. A host runs it once its crew loads a release or a live checkout that holds the landing (`plan.19`).

**Rollback:** sluice lands the change as one merge commit on the bolt, and reverting that commit restores the readers. No data changes in either direction.

## After deploy

None. The change rewrites no record and asks nothing of a live host. madswan's two entries are inert once no reader looks for them, and no other partition holds one.

## Task notes

These hold for every task:
- The tasks run in order. Each takes out a reader's last caller before the reader itself, so each task's own check passes once it is done.
- A logic or contract check runs through moon, its `venv` dependency syncing the tests' venv first: `devenv shell -- moon run tests:logic -- -k <the files' modules>`. pytest's `-k` matches a module's name, so `-k test_kits` runs `tests/py/test_kits.py`.
- No end-to-end test is added or removed, and none reads anything new, so `tests/moon.yml` stays as it is (`tests.10`).
- Never run `wt submit --help` (CLAUDE.md), and submit nothing.
- A case whose name or docstring cites the rename change, and still holds without renames, is renamed and cites the requirement it now proves. Cite `roles.9` for the runner's report, or this change for a kit read as written.

**1.1** Launches as written (Decision 1):
- `launches_now` goes.
- `runner_facts` returns `requests.rec`'s records as written, and so does `rail_runs` (`out[l] = (rq, runners(repo, l))`).
- `raise_proposal_at` passes `kit_at` `requests.rec`'s records as written.
- `landing_at` passes `launched_at` its queued submission's `Repo` as written.
- `main_fix_change` uses `work = f"fix/main/{kit}/{name}"` for every mode, and `main_fix_work` goes. Its docstring's rename sentence goes.
- `runner.main_fixes_waiting`'s docstring loses "which a launch read through the partition's renames names by its name now (plan.launches_now), so a fix launched under a former name is its renamed kit's".

In `tests/py/test_kits.py` `TestWhereABoltRuns`:
- drop `test_a_launch_under_a_kits_former_name_is_its_kits_after_the_rename` and `test_a_commands_launches_are_read_through_the_renames_at_the_tip_they_were_read_at`;
- add bolt-plan's "A launch read as written". `launches` holds request 1 under `flywheel-cloud`, and `reads` has deneb take it. `plan.kit_at(FLEET, "madswan", "boomdrive-cloud", (launches, reads))` is refused "no runner has reported taking boomdrive-cloud's work yet". `plan.kit_at(…, "flywheel-cloud", …)` is read at deneb. Then, with `state_of`, `fetch`, `show` and `runners` monkeypatched as the dropped case had them and nothing monkeypatched for renames, `plan.runner_facts` and `plan.rail_runs` give request 1's `Repo` as `flywheel-cloud`.

In `tests/py/test_main_fix.py`, `TestRenamed` (from its line 150) becomes bolt-plan's "A fix of main read as written":
- the fix is launched as `fix/main/tailrace/x` and read at a tip whose entries hold `RENAME`;
- `runner.main_fixes_waiting` on `requests.rec` as written names its kit `tailrace`;
- the land row of `plan.rail_rows`, given the requests as written, is `land/tailrace`;
- `plan.main_fix_change(…, "timber", "x", "send", None)` is refused "no launch of fix/main/timber/x stands in requests.rec";
- `plan.main_fix_change(…, "tailrace", "x", "send", None)` sends request 1's retry.

In `tests/py/test_kit_rename.py` `TestTheStartedBoltLands`, `test_one_seam_reads_merged_…` reads `plan.Plan(REQUESTS).recs("Request")` as written in place of `plan.launches_now(…)`, and keeps every assertion: bolt-plan's "A started bolt renamed lands in its kit's clone". Its docstring drops "is read as boomdrive-cloud's (plan.launches_now)" and says request 1 is read as written, the bolt's launches found by its branch.

**1.2** `--repo` as given (Decision 2):
- `kit_given`, `former_said` and `former_kept_said` go.
- `op_bolt_new` writes `("Repo", a.repo)`, and its `after` prints nothing of a rename.
- `op_unit_add` writes `a.repo` or the bolt's `Repo`, and checks `a.repo in (None, kit) or fail(f"bolt {a.bolt} is in {kit}, not {a.repo}")`. Its `after` prints nothing of a rename.
- `Direct.renames` and `Proposed.renames` go, since nothing calls them now.

In `tests/py/test_kit_rename.py`, `TestAFormerName` becomes `TestAKitAsGiven` (bolt-plan "A command given a kit writes it as given"):
- `test_a_new_bolt_under_a_former_name_is_written_under_the_name_now` becomes "A kit given by --repo is written as given": with `renamed("tailrace", "timber")` among the entries, `bolt new y "Y is built." --repo tailrace` writes `Repo: tailrace` and prints nothing.
- `test_a_chore_into_a_renamed_kits_bolt_given_its_former_name_goes_in` becomes "A chore given another name of its bolt's kit": the same chore add is refused "bolt trc-1 is in timber, not tailrace", and the plan is unchanged.
- `test_a_proposal_approved_after_the_rename_…`, `test_a_command_after_a_rename_in_one_proposal_writes_the_name_now` and `test_a_former_name_kept_again_is_refused_naming_the_rename` are dropped.
- `test_a_name_no_rename_renamed_is_written_as_given_and_says_nothing` stays.
- The module docstring's Decision 4 sentence goes.

In `tests/py/test_landings.py`, the stub context's `renames` method at its line 88 goes.

**1.3** Card keys as written (Decision 1):
- `record_now` goes.
- `row_gone`, `record_settled`, `record_proposed` and `sweep_judged` lose `renames`, and their docstrings lose the rename clauses. `row_gone` loses the two lines that close a card under a former name.
- `sweep_judgments` passes no renames.
- `rail_read` drops its `renames` map and the `renames=` it hands on.
- `rail_record`'s ops entries (line 11264) take `bolt.land` alone.

In `tests/py/test_rail.py`, drop `test_a_renamed_kits_landings_card_closes_saying_so_and_its_new_card_is_raised_for_its_rows` and `test_a_records_card_under_a_renamed_kit_is_settled_by_the_record_under_its_new_name` (rail-cards' requirement is removed).

**1.4** Sources as written (Decision 1): `record_items` and `proposal_records` lose `renames` and their docstrings' former-name sentence, and `plan_propose` passes none. In `tests/py/test_proposals.py`, `test_a_source_naming_the_works_kit_by_a_former_name_is_read_in_the_kits_checkout` (line 221) becomes bolt-plan's "A source read as written". It keeps the assertion that `WilldanGroup/old-board:docs/adr/0017` reads as `("unit", "n", "WilldanGroup/old-board", "WilldanGroup/old-board", 17)` beside sluice's, and drops the call that passed renames.

**1.5** Landings and deploys as written (Decision 1):
- `ops.landings` reads each `Repo` as written, with no `import plan`, `plan.renames_in` or `plan.kit_now`, and `ops.raise_deploy`'s landings at 705 take `bolt.land` alone.
- `page.deploys`' read at 185 to 189 and `page.fleet_kits` take `bolt.land` entries alone and compare `Repo` as written.
- Their docstrings drop the renames.

In `tests/py/test_ops.py`, drop `test_landings_under_a_kits_former_name_are_its_landings_after_the_rename`. In `tests/py/test_page.py`, drop `TestFleetKits`' two renamed-kit cases (from its line 99), and its docstring's rename clause. Keep the class if another case remains, else drop it.

**2.1** The renames go, and a partition's kits are read as written (Decisions 1, 3 and 6):
- Remove `kit_now`, `renames_in`, `renames_at`, `renames_read`, `runs_at`, `Write.renamed` and `Write.renames`.
- `landings_at(repo, tip)` reads `runs/` itself, its `bolt.land` entries by `record.acts_in`, kept under `landings-<tip>` (`plan.12`).
- `partition_kits(plan, landings)` reads each `Repo` as written. `kits_at` and `Write.kits` call it without renames.
- `kit_labels` is `kit_in(kit, kits_read(fleet, l))`.
- `rename_refusal(label, old, new, kits, bolts, host, spaces)` loses the "since its rename" branch. `op_kit_rename` calls it so and no longer appends to `w.renamed`. Its docstring loses "the partition's record of the rename that crew reads what it never rewrites through (kit_now)".

In the tests:
- `tests/py/test_kits.py`: drop `renamed`, `TestKitNow` and `TestRenamesIn`.
  - `TestPartitionKits` drops its three rename cases and gains bolt-plan's "Landings under another name": a plan naming `timber` and one `bolt.land` under `tailrace` give `["tailrace", "timber"]`.
  - `TestRunsRead` becomes run-record's "A rename's entry renames nothing". A tip whose `runs/` holds a `bolt.land` under `tailrace` and a `kit.rename` of `tailrace` to `timber` gives `landings_at` the one landing. `kits_at` with `the_plan()` gives `["tailrace"]`, `runs/` is shown once for both, and a tip of None gives none.
- `tests/py/test_board.py`: `TestRenamedKit` (line 2305) becomes the same scenario on the board. In place of its `runs_at` monkeypatch, `plan.landings_at` is monkeypatched to give `[self.LANDED]`, the landings a tip holding `LANDED` and `RENAMED` gives (`TestRunsRead` proves that read), and `RENAMED` goes from the class if nothing else uses it. The partition's kits read by `plan.kits_at` are `["agentplot/tailrace", "breadboard-kit", "switchboard-kit"]`, and the agents' views keep the keys the mod reads (`code.8`).
- `tests/py/facts.py`: `FactsWrite` loses `renames`, its `kits` calls `plan.partition_kits(self.plan, self.logged)`, and its docstring loses the renames.
- `tests/py/test_asks.py:860`, `tests/py/test_proposal_life.py:370` and `tests/py/test_proposal_card.py:407`: the `renames_at` monkeypatches go.
- `tests/py/test_kit_rename.py`:
  - `test_a_kit_only_the_landings_name_renames_no_record_and_still_writes_its_entry` asserts `w.kits() == ["crew", "tailrace"]` in place of the renames (bolt-plan "A kit only its landings name").
  - `TestRefused` drops `w.renamed == []`.
  - `test_a_name_a_rename_already_renamed_is_renamed_by_its_name_now` becomes bolt-plan's "A name an earlier rename renamed". Rename the plan's records with `rename(was, "tailrace", "timber")`, write `written(was.plan.text(), entries=[renamed("tailrace", "timber")])`, and `rename(w, "tailrace", "trc", fleet("agentplot/trc"))` is refused "madswan's plan names no kit tailrace: neither its plan nor its landings name it".
  - The module docstring says the rename renames the plan's records alone and nothing reads its entry.

**2.2** In `tests/contract/test_recfix.py` `test_a_rename_is_one_commit_whose_plan_passes_recfix_and_its_entry_names_both_names`, replace `assert plan.renames_in([e]) == [("tailrace", "timber")]` with a real `plan.recfix` of the day file's text at the entry's commit, `runs/deneb/<day>.rec`. That pins run-record's "The entry of a rename" and Decision 6: a branch holding the entry still takes every write (`plan.1`). The case's diff assertion, `plan.rec` alone in the rename's commit, also proves bolt-plan's "A rename appends only its entry", with `TestTheStartedBolt` in `tests/py/test_kit_rename.py`. The module docstring's rename clause stays.

**2.3** `plugin/lib/runner.py`'s docstrings (Decision 5):
- `kept_folder`'s says it takes the kit as the plan gives it, matched by name or forge address, and cites `roles.9`.
- `where`'s drops "the kit's name now (kit, plan.kit_now's)" and "(Decision 6 of a-kit-renamed-on-its-host-is-renamed-across-the-plan)" in favour of `roles.9`.
- The descriptor comment at 194 cites `roles.9` and the drive-state spec for `repositories.rec`.

No behaviour changes. `tests/py/test_runner.py`'s docstrings at its lines 215 and 438 cite `roles.9`.

**3.1** The docs (`docs.2`):
- In `plugin/bin/crew`'s usage for `crew kit rename`:
  - drop "or that a rename already renamed";
  - replace "What crew recorded under a former name and never rewrites is read under the name now, and bolt new, unit add and chore add given one write the name now and say so" with "what crew recorded elsewhere under <old> stays under it, read as written".
- In README's rename paragraph (the plan section):
  - drop ", or one an earlier rename renamed, naming its name now";
  - replace the sentences from "What crew recorded under a former name and never rewrites…" to "…is refused, naming the rename." with one saying that what crew recorded elsewhere under `<old>` (launches, landings and entries, a fix of main's work, a card's key, a source's repository) stays under it and is read as written, as is a `--repo` given `<old>`.
- In README's paragraph on where a started bolt's work runs, "for the kit's name now" becomes "for the kit as the plan names it".
- In README's `Act` list, `kit.rename` reads "a kit renamed across the plan, on `kit/<new>` from `kit/<old>`, with `Repo` and `Count`, renaming nothing crew reads".
- In `plugin/skills/crew/SKILL.md`, replace "what crew recorded under the former name, launches, landings, a fix of main, a card's key and a source, is read under the name now, and a command given the former name writes the name now and says so" with "what crew recorded elsewhere under the former name stays under it, read as written".

**3.2** In `plugin/roles/planner.md`'s paragraph "**A kit renamed on its host**", drop ", and a `--repo` given the old name after the rename is written under the new". The two pins of `tests/t-briefs.sh` (its lines 99 and 100) stay as they are.
