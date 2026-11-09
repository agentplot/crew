# Verify: crew-lands-each-bolt-through-flumes-base-place

Read 2026-11-08 on `change/crew-lands-each-bolt-through-flumes-base-place` at `179f9348`. **Verdict: not ready to archive.** The whole checks pass, but run-record's delta cites a bolt-teams requirement that bolt-teams' delta removes. The change goes back to its code stage with what follows.

## The whole checks

`tests/suite` was run once from the worktree's root. It runs every project's `check-full` tasks, as sluice selects them. Result: **33 passed (32 replayed), 0 failed**, exit 0.

Passed: `contract` (run afresh), and replayed from earlier passing runs: `logic`, `mod`, `nix:format`, `nix:lint`, `nix:test`, `nix:typecheck`, `t-briefs`, `t-cards`, `t-docs`, `t-flume-source`, `t-help`, `t-hold`, `t-journey-board`, `t-journey-cross`, `t-journey-land`, `t-journey-main`, `t-journey-main-fix`, `t-journey-ops`, `t-journey-plan`, `t-journey-review`, `t-journey-roles`, `t-journey-signals`, `t-journey-state`, `t-roles`, `t-runner`, `t-session-hook`, `t-slot`, `t-sluice`, `t-stage-facts`, `t-suite`, `t-teams`, `t-waits`.

The contract tier's three cases that failed at `8f062e3c` now pin `plan.BOLT_HOME`, the policy read crew still runs (task 3.5, `6114002e`):

- `tests/contract/test_git.py::test_mains_policy_is_read_from_origin_main_as_last_fetched_ahead_of_the_hosts_own`
- `tests/contract/test_kit.py::test_the_remote_mains_bolts_live_on_is_read_from_the_policy_mains_commit_holds`

## Tasks

All 39 tasks in `tasks.md` are ticked. `openspec validate crew-lands-each-bolt-through-flumes-base-place --strict` passes.

## The last verify's findings, read again

- **The contract tier** passes, as above.
- **bolt-plan's two citations** now name bolt-teams' requirements as they stand: "A bolt is a base place of crew's kind" and "A start launches the bolt's base place before its pieces" for a start, and "A bolt's drop drops its base place last" and "A base place's drop the runner refused is asked again once nothing on its branch is live" for a drop (task 9.4, `179f9348`). Task 9.4's grep prints 0.

## Words in the delta

Every quoted requirement name the deltas cite was checked against the requirements each capability holds once the change is applied: the main specs, plus each delta's ADDED and MODIFIED names, less its REMOVED ones. All resolve but one.

- run-record's "A landing's Submission is the merge queue's entry Flume names" says the outcome of a land is "recorded as bolt-teams "A landing is recorded by the first act that reads the bolt after it" has it". bolt-teams' delta removes that requirement. Its own migration names the replacement: "A landing is recorded by the first act that reads it in the runner's report". So once archived, run-record cites a requirement bolt-teams no longer has.

`openspec validate` passes, since it does not check names inside quotes. The citation should name "A landing is recorded by the first act that reads it in the runner's report". No code, test or other document uses the removed name.

## What holds

Apart from that one citation, the work holds against the delta. The whole checks pass. Every task is ticked. Each of the last verify's findings is met, each with its check. The pieces spot-checked against the delta are where it says they are:

- `plugin/flume/kinds/bolt@1/kind.toml` lands with no stages on `bolt` branches.
- `tests/py/test_no_tool_for_a_bolt.py` pins that no command runs a tool for a bolt.
- The start's and landing's sluice scripts and `kit.policy_said` are gone from `plugin/`.
