# Verify: a-bolts-landed-fix-reads-merged

Read 2026-11-08 on deneb, at `7a5029ed` on `change/a-bolts-landed-fix-reads-merged`, cut from `bolt/crew-reads-each-piece-as-the-tools-hold-it` at `7a7b8acd`.

**Outcome: archived.** All 5 tasks are ticked. The repository's checks pass. Each requirement and scenario of the `bolt-plan` delta is met by the code and proved by a case in the logic tier. The bolt still stands at `7a7b8acd` on GitHub, and the branch merges onto it cleanly (`git merge-tree`). Nothing fails.

## Checks

| Check | Result |
|---|---|
| `openspec validate a-bolts-landed-fix-reads-merged --strict` | Valid |
| `tests/suite --affected`, run once | 28 passed (1 replayed), 0 failed: `contract`, `logic`, `t-briefs`, `t-cards`, `t-docs` (replayed), `t-flume-source`, `t-help`, `t-hold`, `t-journey-board`, `-cross`, `-land`, `-main`, `-main-fix`, `-ops`, `-plan`, `-review`, `-roles`, `-signals`, `-state`, `t-roles`, `t-runner`, `t-session-hook`, `t-slot`, `t-sluice`, `t-stage-facts`, `t-suite`, `t-teams`, `t-waits` |

The change edits `plugin/lib/` and `plugin/bin/crew`, crew's command core, so every test whose inputs take the core was affected and run (CLAUDE.md, Tests). `mod` and the `nix` project's tasks were not selected: none of their inputs changed (`plugin/hooks/`, `plugin/tests/`, the flake). `t-docs` was replayed from the code stage's passing run on identical inputs (`tests.10`). `tests/suite` ran, so `tests/moon.yml` is in step with the tests.

## Tasks

| Task | Read |
|---|---|
| 1.1 | `runner.place_branch` gives `fix/<bolt>--<name>` for a fix on a bolt, `fix/<bolt>/<name>` in exactly two non-empty parts after the kind. It gives None for `fix/main/<kit>/<name>`, which has three parts, and for a role's work. `built_on_bolt` takes `launched` and returns `s` unchanged when the landing's `at` sorts before it. Units and chores pass no date and read as before. `TestAFixItsBoltHolds` in `tests/py/test_fix.py` covers the branch names, the landed fix read merged with `on`, `branch` and `landed` and its `piece_said` line, a landing before the launch, and `fix/main--red` building no fix of main. `TestBuiltOnItsBolt` now asserts that `fix/x--tidy` builds `fix/x/tidy` and that `fix/x--gap` builds nothing. |
| 1.2 | `Stages.landings(b)` returns None when the partition's runners can't be read. Otherwise it gives the bolt's landings as its kit was read. `crossed` reads them through it. `Stages.fixes` applies `built_on_bolt` with each launch's `Date`. `crew bolts` (`plan.py` 10152), the board's ledger (`board.py` 297) and the fixing band (`plan.py` 11423) already read `Stages.fixes`, so they need no change of their own. `test_a_crossed_bolts_landed_fix_reads_merged_from_its_bolts_landing` in `tests/py/test_stages.py` covers merged at the landing, submitted when `landings_error` is set, and submitted for a landing dated before the launch. |
| 1.3 | `runner.fixes_in_flight(fixes, bolt)` takes `Stages.fixes`' triples. `land_facts` calls `runner.fixes_in_flight(st.fixes(b), bolt)` from the `Stages` it already holds, and makes no `runner_facts` call of its own (`plan.12`). `st.kit(b)` comes first and refuses when the runners can't be read (`Stages.at`), so an empty `fixes` never stands for fixes crew could not read (`read.1`). The existing in-flight case passes `fixes_on`'s triples with the same results. `test_a_landed_fix_holds_its_bolts_landing_no_longer` covers the merged fix out of flight with the bolt proven, and the unread landings keeping it in flight and holding the landing. |
| 1.4 | For `--drop` on a started bolt, `fix` reads `stages_for(...).landings(b)` before the write. `fix_flume` applies `built_on_bolt` with the launch's `Date` before `fix_drop_refusal`. A start reads no landings. `test_a_fix_its_bolts_landing_reads_merged_is_not_dropped` checks the refusal, `^fix/x/rail-word has merged into bolt/x, so it is not dropped`, with no request appended. It also checks that the same drop with no landings goes through as request 3. |
| 2.1 | The README's stage paragraph, the crew skill's stage sentence and `crew`'s usage header each name a fix's `fix/<bolt>--<name>`, read only from a landing at or after its launch (`docs.2`). README and the skill also say that a fix so read no longer holds its bolt's landing. `t-docs` passes. |

The design leaves out `openspec/config.yaml`'s closing `tests/suite --affected` task and says why (design, Context). This stage ran that check, above.

## The delta: `bolt-plan` (ADDED)

**A fix whose place's landing its bolt's branch holds is merged.** Met by `place_branch`, `built_on_bolt` and `Stages.fixes`.
- *A landed fix whose place the runner last carried at submitted*: `test_a_landed_fix_the_runner_last_carried_at_submitted_reads_merged` and the Stages case. `piece_said` gives `crew bolts`' line, `fix/x--tidy landed on its bolt at <commit>`.
- *A fix launched again under a landed fix's name*: `test_a_landing_before_the_fixs_launch_builds_nothing` and the Stages case dated `03:59:59Z`. In both, the fix reads its stage from the runner's records.
- *Landings crew can't read*: the Stages case with `landings_error`, which reads submitted. `test_landings_crew_could_not_read_leave_the_runners_reading` covers the same for units.
- A fix of a kit's main is never read from a bolt's landings: `test_a_fix_of_main_is_never_read_from_a_bolts_landings`.

**A fix read merged from its bolt's landing holds nothing.** `crew bolts`, the board, the landing (`land_facts`) and the drop (`fix_flume`) all read a fix through `built_on_bolt` over the bolt's landings.
- *A landed fix holds its bolt's landing no longer*: `test_a_landed_fix_holds_its_bolts_landing_no_longer`, first half.
- *A landed fix is not dropped*: `test_a_fix_its_bolts_landing_reads_merged_is_not_dropped`.
- *A fix whose landings crew can't read still holds*: `test_a_landed_fix_holds_its_bolts_landing_no_longer`, second half.

The reads around these decisions stay thin, and the decisions call no tool (`code.7`). Those reads are `Stages.landings` and its call in `fix`. They are proved by the end-to-end tier's crossed and landing journeys (`t-journey-cross`, `t-journey-land`), which pass. No stage, key or field the views draw changes shape. A fix's `flume` value gains `on`, `branch` and `landed`, which a unit's already carries, so `code.8` is not reached. Nothing outside the standard library is imported (`code.1`).
