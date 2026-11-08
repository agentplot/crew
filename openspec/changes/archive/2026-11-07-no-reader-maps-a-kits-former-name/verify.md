# Verify: no-reader-maps-a-kits-former-name

Read 2026-11-07 on deneb, at `993d384c` on `change/no-reader-maps-a-kits-former-name`, cut from `bolt/crew-reads-a-kit-by-its-name-alone` at `7a7b8acd`, where GitHub's bolt still stands, so the branch meets it with no conflict.

**Outcome: archived.** All 10 tasks are ticked, the whole checks pass, and each requirement and scenario of the four deltas is met by the code and proved by a case. No reader maps a kit through `kit.rename` entries: `kit_now`, the partition's renames and every name the proposal lists are gone from `plugin/`, `README.md` and the tests. Nothing fails.

## Checks

| Check | Result |
|---|---|
| `openspec validate no-reader-maps-a-kits-former-name --strict` | Valid |
| `tests/suite --affected`, run once | 28 passed (1 replayed), 0 failed, exit 0: `contract`, `logic`, `t-briefs` (replayed), `t-cards`, `t-docs`, `t-flume-source`, `t-help`, `t-hold`, `t-journey-board`, `-cross`, `-land`, `-main`, `-main-fix`, `-ops`, `-plan`, `-review`, `-roles`, `-signals`, `-state`, `t-roles`, `t-runner`, `t-session-hook`, `t-slot`, `t-sluice`, `t-stage-facts`, `t-suite`, `t-teams`, `t-waits` |

These are the `check-full` tasks the change affects, which is what CLAUDE.md names as the run once a change is done and what sluice runs at the merge (`tests.5`, `tests.10`). The change edits crew's command core (`plugin/bin/crew`, `plan.py`), so every end-to-end test is among them. `mod` and the `nix` project's tasks are not, since their inputs (`plugin/hooks/status.js`, `plugin/tests/`, the flake) are untouched, as the proposal says (`code.8`). `t-briefs` replayed a pass on identical inputs. `tests/suite` ran, so `tests/moon.yml` is in step with the tests, unchanged as the proposal says.

## Tasks

| Task | Read |
|---|---|
| 1.1 | `launches_now` and `main_fix_work` are gone. `runner_facts` and `rail_runs` read `requests.rec`'s records as written. `main_fix_change` uses `fix/main/{kit}/{name}` for every mode. `test_kits.py` `test_a_launch_read_as_written`, `test_main_fix.py` `TestReadAsWritten` and `test_kit_rename.py` `TestTheStartedBoltLands` pass in `logic`. |
| 1.2 | `kit_given`, `former_said`, `former_kept_said`, `Direct.renames` and `Proposed.renames` are gone. `op_bolt_new` writes `("Repo", a.repo)`. `op_unit_add` refuses `bolt {a.bolt} is in {kit}, not {a.repo}`. `TestAKitAsGiven`'s three cases pass, and the stub `renames` of `test_landings.py` is gone. |
| 1.3 | `record_now` is gone. `row_gone` takes no renames and no longer closes a card under a former name. `rail_runs` and the rail's read carry none. `test_rail.py`'s two rename cases are dropped, with rail-cards' requirement. |
| 1.4 | `test_a_source_read_as_written` (`test_proposals.py:221`) reads `WilldanGroup/old-board:docs/adr/0017` as `WilldanGroup/old-board`'s, with no renames passed. |
| 1.5 | `ops.landings` reads `Repo` as written, with no `import plan`. `ops.raise_deploy`, `page.deploys` and `page.fleet_kits` take `bolt.land` alone. The renamed-kit cases of `test_ops.py` and `test_page.py` are dropped. |
| 2.1 | `kit_now`, `renames_in`, `renames_at`, `renames_read`, `runs_at`, `Write.renamed` and `Write.renames` are gone (grep over `plugin/` and `tests/` finds none). `landings_at` reads `runs/` once per tip under `landings-<tip>`, its `bolt.land` entries alone. `partition_kits(plan, landings)` reads `Repo` as written. `kit_labels` is `kit_in(kit, kits_read(fleet, l))`. `rename_refusal` has no "since its rename" branch. `TestPartitionKits`, `TestRunsRead`, `test_board.py`'s renamed-kit case, `facts.py` and the three monkeypatches are as the notes ask. |
| 2.2 | `test_recfix.py` runs a real `plan.recfix` of `runs/deneb/<day>.rec` at the entry's commit in place of `renames_in`, and keeps its assertion that the rename's commit holds `plan.rec` alone. `contract` passes. |
| 2.3 | `runner.py`'s descriptor comment, `kept_folder`, `where` and `main_fixes_waiting` cite `roles.9` and name no kit's name now. No behaviour changes. `test_runner.py` passes. |
| 3.1 | `crew`'s usage, README's rename paragraph, its "for the kit as the plan names it", its `kit.rename` act line and `SKILL.md` say what crew recorded elsewhere under `<old>` stays under it, read as written. `t-docs` passes. |
| 3.2 | `planner.md` drops the `--repo` clause and keeps both phrases `t-briefs` pins. `t-briefs` passes. |

## The deltas

### bolt-plan

- **ADDED: crew reads each kit by the name its record gives it.**
  - "Landings under another name": `test_kits.py` `test_landings_under_another_name` gives `["tailrace", "timber"]`. On the board, `test_board.py`'s renamed-kit case (line 2305) gives the kits as written and keeps the keys the mod reads.
  - "A launch read as written": `test_a_launch_read_as_written` is refused for `boomdrive-cloud` ("no runner has reported taking boomdrive-cloud's work yet") and reads `flywheel-cloud` at deneb.
  - "A fix of main read as written": `TestReadAsWritten` shows it on `land/tailrace`. `crew main fix timber x --send` is refused "no launch of fix/main/timber/x stands in requests.rec", and `tailrace x --send` sends request 2's retry.
  - "A source read as written": `test_a_source_read_as_written`.
- **ADDED: requests.rec and the run record are only appended to.**
  - "A rename appends only its entry": `test_recfix.py`'s diff assertion (`plan.rec` alone) and `TestTheStartedBolt` (`requests.rec` unchanged).
- **ADDED: A command given a kit writes it as given.**
  - "A kit given by --repo is written as given": `test_a_kit_given_by_repo_is_written_as_given`, with `Repo: tailrace` written and nothing printed.
  - "A chore given another name of its bolt's kit": `test_a_chore_given_another_name_of_its_bolts_kit_is_refused`, refused "bolt trc-1 is in timber, not tailrace", with the plan unchanged.
- **MODIFIED: A kit renamed on its host is renamed across the plan in one act.**
  - "A kit only its landings name": `test_a_kit_only_the_landings_name_renames_no_record_and_still_writes_its_entry` asserts `w.kits() == ["crew", "tailrace"]`.
  - "A name an earlier rename renamed": `test_a_name_an_earlier_rename_renamed_is_judged_as_written`, refused "madswan's plan names no kit tailrace: neither its plan nor its landings name it" and naming no rename.
  - "A started bolt renamed lands in its kit's clone": `TestTheStartedBoltLands` reads request 1 as written, and the bolt lands as `land/boomdrive-cloud`.
  - The other scenarios (the rename itself, refused on its host, the new name a bolt's, the planner, another agent, a started bolt, the command at a shell) are unchanged in substance. They stay proved by `TestTheRename`, `TestRefused`, `TestTheStartedBolt` and `t-journey-plan`, all of which pass.
- **REMOVED: the read under the name now, and the former name written under the name now.** No code or case of either remains.

### drive-state

- **MODIFIED: A kit's work is taken by a runner whose configuration names its repository.** The folder is matched "by the name or forge address the plan gives the kit". `runner.kept_folder` takes the kit as the plan gives it, through `kit_in`.
  - "A kit renamed under its place" and "A runner that does not keep the kit": `test_kit_rename.py` `TestTheStartedBoltLands` (both cases) and `test_runner.py`.

### rail-cards

- **REMOVED: A kit's landings card follows its rename.** `row_gone`'s close for a renamed kit and both rail cases are gone. A card key is read by the kit it names.

### run-record

- **MODIFIED: A kit's rename is one entry naming both its names.**
  - "The entry of a rename": `test_recfix.py`, with a real `recfix --check` of the day file.
  - "A refused rename renames nothing": `TestRefused`, which writes nothing, together with `partition_kits`, which reads no entry.
  - "A rename's entry renames nothing": `TestRunsRead` gives the one `bolt.land` in one read, and the kits `["tailrace"]`. `record.py` is unchanged, so `crew events` and `crew trace` print the entry as before.

## Rules

- **`plan.22`** (record 0060): no reader maps a former name. The grep over `plugin/` and `tests/` finds no `kit_now`, renames or `launches_now`.
- **`code.7`**: `partition_kits`, `rename_refusal` and `row_gone` stay functions of plain facts.
- **`code.8`**: the views keep their shape, and `test_board.py` pins the keys the mod reads, so the mod is untouched.
- **`plan.12`**: `landings_at` reads `runs/` once per tip, which `TestRunsRead` pins.
- **`docs.7`**: `docs/architecture/` and `docs/adr/` are untouched.
