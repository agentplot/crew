# Verify: a-bolts-landing-on-main-reads-landed

Read 2026-11-08 on deneb, at `fcab3222` on `change/a-bolts-landing-on-main-reads-landed`, cut from `bolt/crew-reads-each-piece-as-the-tools-hold-it` at `479648d0`.

**Outcome: not archived.** The repository's checks fail: two end-to-end tests fail, `t-journey-cross` and `t-journey-board`. All 13 tasks are ticked. The change validates, and the logic and contract tiers pass. Each requirement and scenario of the three deltas is met in the code and has its case, except where the two failing tests show the work falls short (below). The change goes back to its code stage.

## Checks

| Check | Result |
|---|---|
| `openspec validate a-bolts-landing-on-main-reads-landed --strict` | Valid |
| `tests/suite --affected`, run once | **26 passed (1 replayed), 2 failed.** Passed: `contract`, `logic`, `t-briefs`, `t-cards`, `t-docs` (replayed), `t-flume-source`, `t-help`, `t-hold`, `t-journey-land`, `-main`, `-main-fix`, `-ops`, `-plan`, `-review`, `-roles`, `-signals`, `-state`, `t-roles`, `t-runner`, `t-session-hook`, `t-slot`, `t-sluice`, `t-stage-facts`, `t-suite`, `t-teams`, `t-waits`. Failed: `t-journey-board`, `t-journey-cross`. |

The change edits `plugin/lib/` and `tests/lib.sh`, crew's command core, so every test whose inputs take the core was affected and run (CLAUDE.md, Tests). `mod` and the `nix` project's tasks were not selected, since none of their inputs changed. The design leaves out `openspec/config.yaml`'s closing `tests/suite --affected` task and says why (design, Context). This stage ran that check, above.

### `t-journey-cross` fails

```
FAIL: expected 'unit a can't be planned in switchboard-kit: Flume's branch change/a stands in
  …/hosts/chuck-herdr-alpha/work/willdan/switchboard-kit/main on chuck-herdr-alpha, at a09e0bf'
  from: crew unit add a Build a again. --bolt next
cannot check whether Flume's branch for unit a stands: the runner on chuck-herdr-alpha took
  switchboard-kit's work and reports no repositories it keeps, so crew can't tell where it keeps switchboard-kit there
```

This is Decision 1's new refusal. The test builds `wldn/runner/<box>` by hand, from `runner.rec`, then `answers.rec` and `places.rec` (`tests/t-journey-cross.sh` 35–65). It never goes through `tests/lib.sh` `runner_writes`, so its runner branch holds no `repositories.rec`. Before this change, `runner.where` took the folder from the place's status. Now the kit is unread, and the add's guard can't check Flume's branch. The change's tasks 1.3 and 1.4 gave a `repositories.rec` to every logic case and to the stub runner of `tests/lib.sh`, but not to this test's hand-built branch. `tests/t-journey-cross.sh` is not in the proposal's *Touches*. The outcome the test asserts is still right under the delta: the drive-state scenario "The runner that took the work" has the runner report its repositories. So the test's runner branch needs a `repositories.rec` naming the kit at its folder. The test's assertion should not change.

### `t-journey-board` fails

```
FAIL: the watch's new line did not put the submission on a's row:
  {"unit":"a","kind":"unit","stage":"code","tasks":[1,2],"submission":null,"worktree":null,"url":null,
   "flume":{"place":"…/switchboard-kit/places/change--a","tasks":[1,2],"stage":"code"}}
```

This is the follower case (`tests/t-journey-board.sh`, the case at "the watch's new line did not put the submission on a's row"). Sluice's overview watch gains a line with submission 41 from worktree `unit/a`. Within the test's wait, a's row on the follower's frame never shows `{"id":41,"state":"testing"}`, and nothing may be gathered meanwhile. Every case of the test before it passes, the quiet ticks among them. This stage did not find the cause. One lead: this change puts `seek` on the kit's request that the follower keeps (`plan.survey`, `seek_answered`). The stamp the follower sends now carries it, as `calls.log` shows (`"seek": {"tenant-environments": {"since": "2026-11-08T17:43:03Z", "heads": []}}`). The follower's kept answers are matched by their request (`kit_served`, `board.Follower.requeue`/`rekeep`, `queue_kits`). `t-journey-board` passed in this bolt's previous verify (`a-bolts-landed-fix-reads-merged`, at `7a7b8acd`). The scratch is kept at `/private/tmp/crew-test.y8eWiw` on deneb.

## Tasks

Each of the 13 tasks is ticked. What each reads as built:

| Task | Read |
|---|---|
| 1.1 | `runner.kept_folder` gives the new reason when `repositories` is None. `runner.where` takes the folder from `kept_folder` alone, never from a place's `repository`. The host is from the new `newest_taker`. The stream is still the newest carried place's. `TestWhere` covers it. |
| 1.2 | `launched_at` loses its fallback to the kit's other work and its `at["dir"] or fail`. `kit_at` loses its `at["dir"] or fail`. `launch_repositories` loses its no-folder check. `Stages.host` reads the host from `runner.newest_taker`, so the host is named before the folder can be told. `test_kits.py` and `test_branch_stands.py` assert the new reason. |
| 1.3 | `tests/py/facts.py` and the cases building runner readings give the runner a `repositories.rec`. The logic tier passes. |
| 1.4 | `tests/lib.sh` `runner_writes` writes `repositories.rec` from `keeps.json`. `t-journey-land` passes. Tests that build a runner branch by hand were not covered: see `t-journey-cross` above. |
| 2.1 | `gather.LANDED` and `gather.main_landing` are as Decision 2 gives them. `TestMainLanding` covers: the pull request's landing found by head; `bolt/x (bolt/x)` and `ops (bolt/x)`; a landing before `since`; one parent; the newest of two; `bolt/xy` and `change/x`; and an unreadable `since`. |
| 2.2 | `runs_at` reads `bolt.submit` as `submits`. `submits_at`, `submits_read` and `landing_sought` are added. `TestLandingSought` covers the oldest launch, each head once, a refusal with no head, another bolt's, and a bolt with no launch. |
| 2.3 | `gather.kit` reads main's first-parent log once, from the oldest `since`. It records `landed` or `landed_error` on each sought bolt. It adds `exists: False` facts for a bolt with no branch. It reads `bolt_landings(main, ref, now, landing)` on `<head> ^<base>`. The contract case `test_a_landed_bolts_landings_are_read_from_its_landing_on_main_once_its_branch_is_gone` passes. |
| 2.4 | `stages_for`, `bolts_view` and `rail_read` hand `landing_sought` to `survey`, which puts it on the request as `seek`. `TestABoltLandedOnMain` covers landed and closing, a piece not named keeping the bolt open, `landed_error`, and `stages_for`'s seek. |
| 3.1 | The stub `sluice` hands `SLUICE_STUB_PLACE=pull/<n>` to the stub `wt-submit`, which writes `Sluice-From: <agent> (pull/<n>)`. `t-journey-land` passes. |
| 3.2 | `tests/lib.sh` `runner_tidies` is added. The `t-journey-land` case deletes GitHub's `bolt/near-reach`, tidies the box's places, and checks that `crew bolt land` closes the bolt naming main's commit. It passes. |
| 4.1 | README, the crew skill and `crew`'s usage header say a kit's folder is the runner's report alone, and that a landed bolt's pieces are read from its landing on main. `t-docs` passes (replayed). |

## The deltas

**drive-state, MODIFIED "A kit's work is taken by a runner whose configuration names its repository".** Met in `runner.where`, `kept_folder`, `launched_at`, `kit_at` and `launch_repositories`.
- *A runner that reports no repositories*: `TestWhere`'s new case.
- *A bolt whose every launch was refused* and *A bolt whose places the runner no longer carries*: `test_kits.py` and `TestABoltWhoseLaunchesWereAllRefused`.
- *A kit renamed under its place* and *A runner that does not keep the kit*: the existing `TestWhere` cases.
- The end-to-end tier is not in step with the requirement: `t-journey-cross`'s runner reports no repositories, so its kit is now unread.

**bolt-plan, ADDED "A bolt's landing is read from its kit's main".** Met in `gather.main_landing` and `gather.kit`'s seek.
- *A bolt landed through a pull request, its branch gone*, *A landing that names the bolt's branch* and *An earlier bolt of the same name*: `TestMainLanding`, and the contract case.
- *main's line can't be read*: gather sets `landed_error` with git's words, and `TestABoltLandedOnMain` shows nothing reads landed from it. No view of crew's says `landed_error`. Neither does any view say the existing `landings_error`, so this follows that existing reading.

**bolt-plan, ADDED "A landed bolt's pieces are read from its landing".** Met in `bolt_landings` given the landing, with `Stages` unchanged.
- *The landed unit of a bolt whose branch and places are gone* and *A piece its landing does not name*: `TestABoltLandedOnMain`.

**bolt-teams, ADDED "A bolt whose landing main holds closes whatever the runner carried of its places".**
- *A landed bolt whose branch and places are gone*: the `t-journey-land` case, which passes.
- *A piece its landing does not hold*: `TestABoltLandedOnMain`'s `land_refusal` case.

`gather.py` still imports only the standard library (`code.1`). `main_landing`, `landing_sought`, `kept_folder`, `newest_taker` and `seek_answered` call no tool (`code.7`). No stage, key or field that the views draw changes shape (`code.8`).

## Beside the checks

`bolt/crew-reads-each-piece-as-the-tools-hold-it` has moved on to `f9326439` on GitHub, with `a-place-waiting-on-its-caller-reads-waiting` landed. This branch no longer merges onto it cleanly: `git merge-tree` finds a content conflict in `README.md`, on the stage paragraph's line that both changes edit. That is for this change's merge onto the bolt to take in. It is not a fault of the change's own work.
