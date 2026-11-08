# Verify: a-bolts-landing-on-main-reads-landed

Read 2026-11-08 on deneb, at `05aa714a` on `change/a-bolts-landing-on-main-reads-landed`. The branch holds `bolt/crew-reads-each-piece-as-the-tools-hold-it` at `f9326439`, as GitHub has it, with `a-place-waiting-on-its-caller-reads-waiting` landed there.

**Outcome: archived.** The repository's checks pass, every one of the 13 tasks is ticked, and each requirement and scenario of the three deltas is met in the code and proved by a case.

## Checks

| Check | Result |
|---|---|
| `openspec validate a-bolts-landing-on-main-reads-landed --strict` | Valid |
| `tests/suite --affected`, run once | **28 passed (1 replayed), 0 failed.** `contract`, `logic`, `t-briefs`, `t-cards`, `t-docs`, `t-flume-source`, `t-help`, `t-hold`, `t-journey-board` (replayed), `-cross`, `-land`, `-main`, `-main-fix`, `-ops`, `-plan`, `-review`, `-roles`, `-signals`, `-state`, `t-roles`, `t-runner`, `t-session-hook`, `t-slot`, `t-sluice`, `t-stage-facts`, `t-suite`, `t-teams`, `t-waits`. |

The change edits crew's command core (`plugin/lib/`, `tests/lib.sh`), so every test whose task takes the core was affected and run. `mod` and the `nix` project's tasks were not selected, since none of their inputs changed. `t-journey-board` was replayed: moon found its inputs identical to a run that passed on this host, the stub sluice's fix (task 3.3) among them. sluice runs it afresh at this change's merge onto the bolt (`tests.5`).

The merge of `f9326439` into the branch (`cebb6326`) met one conflict, the README's stage paragraph that both changes edit. Its resolution keeps both: the bolt's `waits` and `stalled` words, and this change's folder and landing sentences.

## Tasks

| Task | Read |
|---|---|
| 1.1 | `runner.kept_folder` gives "reports no repositories it keeps" where `repositories` is None. `runner.where` takes the folder from `kept_folder` alone, the host from `newest_taker`, and the stream from the newest carried place's status. `test_runner.py` `TestWhere`. |
| 1.2 | `launched_at`, `kit_at` and `launch_repositories` read no folder from a place, of the bolt's work or the kit's other work. `test_kits.py`, `test_branch_stands.py`. |
| 1.3 | Every logic case whose runner reads a folder gives it a `repositories.rec`. The logic tier passes. |
| 1.4 | `tests/lib.sh` `runner_writes` writes `repositories.rec` from `keeps.json`. `t-journey-land` passes. |
| 1.5 | `tests/t-journey-cross.sh`'s hand-built `wldn/runner/<box>` branch gains a `repositories.rec` naming `WilldanGroup/switchboard-kit` at its folder (`2ed8f770`). The assertion is unchanged, and `t-journey-cross` passes. |
| 2.1 | `gather.LANDED` and `gather.main_landing`. `test_main_landing.py` `TestMainLanding`: found by a submitted head through a pull request, by `bolt/x` with no head, none before `since`, none of one parent, the newest of two, none for `bolt/xy` or `change/x`, none for an unreadable `since`. |
| 2.2 | `runs_at` reads `bolt.submit` as `submits`. `submits_at`, `submits_read` and `landing_sought` are added. `TestLandingSought`: the oldest launch, each head once, another bolt's left out, none for a bolt with no launch. |
| 2.3 | `gather.kit` reads main's first-parent line once from the oldest `since` sought. It sets `landed` or `landed_error` on each sought bolt, `exists: False` for one with no branch, and reads `bolt_landings` from the landing whether the branch stands or not. Contract case `test_a_landed_bolts_landings_are_read_from_its_landing_on_main_once_its_branch_is_gone`. |
| 2.4 | `stages_for`, `bolts_view` and `rail_read` hand `landing_sought` to `survey` as the request's `seek`. `test_stages.py` `TestABoltLandedOnMain`. |
| 3.1 | The stub `sluice` lands a pull request's submission with `Sluice-From: <agent> (pull/<n>)`. `t-journey-land` passes. |
| 3.2 | `t-journey-land`'s case deletes GitHub's `bolt/near-reach`, tidies the box's places, and `crew bolt land` closes the bolt naming main's commit. It passes. |
| 3.3 | The stub sluice's overview watch catches the `ValueError` of a half-written file, notes its host once in `sluice-overview-half-read`, and looks again (`be3f6bee`). `t-journey-board` writes a half document and waits until both kits' watches have looked at it. `t-journey-board` passes. |
| 4.1 | README, `plugin/skills/crew/SKILL.md` and `crew`'s usage header say a kit's folder is the runner's report alone and a landed bolt's pieces are read from its landing on main. `t-docs` passes. |

## The deltas

**drive-state, MODIFIED "A kit's work is taken by a runner whose configuration names its repository".** Met in `runner.where`, `kept_folder`, `newest_taker`, `launched_at`, `kit_at` and `launch_repositories`.
- *The runner that took the work*, *A runner that reports no repositories*, *A kit renamed under its place* and *A runner that does not keep the kit*: `TestWhere`.
- *A bolt none of whose own work is taken* and *A bolt whose places the runner no longer carries*: `test_kits.py` `TestWhereABoltRuns`.
- *A bolt whose every launch was refused*: `test_stages.py` `TestABoltWhoseLaunchesWereAllRefused`, the runner's folder taken and another host's place not.
- *Taken by two runners* and *No runner has reported the kit*: `TestWhere` and `TestWhereABoltRuns`.
- The end-to-end tier agrees: every stub runner, `tests/lib.sh`'s and `t-journey-cross`'s hand-built one, reports its repositories.

**bolt-plan, ADDED "A bolt's landing is read from its kit's main".** Met in `gather.main_landing` and `gather.kit`'s seek.
- *A bolt landed through a pull request, its branch gone*, *A landing that names the bolt's branch* and *An earlier bolt of the same name*: `TestMainLanding` and the contract case.
- *main's line can't be read*: gather sets `landed_error` with git's words, and `TestABoltLandedOnMain`'s `test_a_landing_crew_cant_read_builds_nothing` shows nothing reads landed from it.

**bolt-plan, ADDED "A landed bolt's pieces are read from its landing".** Met in `bolt_landings` given the landing, with `Stages` reading the landings as before.
- *The landed unit of a bolt whose branch and places are gone* and *A piece its landing does not name*: `TestABoltLandedOnMain`.

**bolt-teams, ADDED "A bolt whose landing main holds closes whatever the runner carried of its places".**
- *A landed bolt whose branch and places are gone*: the `t-journey-land` case and `TestABoltLandedOnMain`.
- *A piece its landing does not hold*: `test_a_piece_its_landing_does_not_name_keeps_the_bolt_open_named`, through `land_refusal`.

`gather.py` still imports only the standard library (`code.1`). `main_landing`, `landing_sought`, `kept_folder` and `newest_taker` call no tool (`code.7`). No stage, key or field the views draw changes shape (`code.8`).

## After deploy

As the proposal's *Impact* and the design's *After deploy* say: a host's crew takes this change only once that host's runner branches hold `repositories.rec`. Boomdrive's runner does not write it yet (agentplot/boomdrive `c6eb79b`, `boomdrive-crew` `write.rs`). Until it does, every started bolt on such a host reads its kit unread and none lands. This bears on landing the bolt onto main or a host's pin, not on this change's merge onto the bolt.
