# Tasks

Build the tasks in order; each names the one check that proves it. Submit nothing, and never run `wt submit --help`.

## 1. A place waiting on its caller reads waiting

- [x] 1.1 A place Flume 0.17.0's status says waits on its caller to retry code past its bound, its verify delivered, reads waiting at code with Flume's words, and one waiting on a retry of its refused submission reads waiting at its submission, each pinned on `tests/py/flume-0.17.0/past-bound.json` and `submission-refused.json` (design Decision 1; Task notes 1.1). Verify `devenv shell -- moon run tests:logic -- -k "test_a_place_past_its_bound_waits_on_its_caller_at_the_stage_it_waits_to_retry or test_a_place_waiting_on_a_retry_of_its_submission_waits_at_its_submission"` passes.
- [x] 1.2 `crew bolts`'s line, the board's ledger and the planner's band show such a place waiting on its caller at the stage it waits to retry, or its submission, with Flume's words (design Decisions 1 and 3; Task notes 1.2). Verify `devenv shell -- moon run tests:logic -- -k "test_a_place_waiting_on_its_caller_is_on_its_line_at_what_it_waits_to_retry or test_a_place_past_its_bound_in_the_planners_band"` passes.
- [x] 1.3 `crew answer` retries the stage a place past its bound waits to retry, or its submission. It refuses a live place neither stopped short nor waiting by naming its stage as the runner carried it, with the runner's host and when it carried it, and never says that place has nothing to answer (design Decision 2; Task notes 1.3). Verify `devenv shell -- moon run tests:logic -- -k "TestAnswer or test_a_refusal_without_its_carry_says_when_its_runner_last_carried_it"` passes.

## 2. What a wait reads and what a refusal names, said

- [ ] 2.1 README, `plugin/skills/crew/SKILL.md` and `plugin/bin/crew`'s usage say that `waits` covers a place past its bound at the stage it waits to retry, and that `stalled` is Flume's stalled. They also say what `crew answer`'s refusal of a live place names (design Decision 4; Task notes 1.4). Verify `tests/suite t-docs` ends with "0 failed".
- [ ] 2.2 The planner's brief says the refusal names the stage as the runner carried it, and that a wait Flume told of since is answered again once `crew bolts` shows the place waiting, with the added phrase pinned in `tests/t-briefs.sh` (design Decision 4; Task notes 1.5). Verify `tests/suite t-briefs` ends with "0 failed".
