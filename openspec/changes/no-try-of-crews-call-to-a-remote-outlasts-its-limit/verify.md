# Verify: no-try-of-crews-call-to-a-remote-outlasts-its-limit

Read on 2026-11-11 at `change/no-try-of-crews-call-to-a-remote-outlasts-its-limit`, head 4dbdb979, cut from `bolt/no-try-of-crews-call-to-a-remote-outlasts-its-limit`.

**Verdict: not ready to archive.** The whole checks fail in two tasks, `logic` and `contract`, and this change caused both failures. The change is not archived. It goes back to its code stage.

## The whole checks

`tests/suite` ran once, with every project's `check-full` tasks, as `.config/sluice.toml` requires of `bolt/*` and `main`:

```
35 passed (5 replayed), 2 failed
exit 1
FAIL  contract
FAIL  logic
```

### logic: 9 failed, 3550 passed

Every failing case is in `tests/py/test_landings.py`:

- `test_a_bolt_branch_crew_cannot_read_is_said_and_its_box_kept`
- `test_a_bolt_on_github_is_forecast_where_it_lives`
- `test_a_bolt_kept_on_its_host_is_forecast_at_the_hosts_branch`
- `test_a_policy_crew_cannot_read_at_githubs_copy_is_said_and_forecasts_nothing`
- `test_the_forecast_hands_back_the_revision_of_main_it_forecast_against`
- `test_a_forecast_whose_fetch_or_read_of_main_failed_hands_back_no_revision`
- `test_a_bolts_own_work_is_its_non_merge_commits_main_lacks_gained_and_lost_between_the_heads`
- `test_a_fetch_refused_reads_no_work_in_gits_words`
- `test_a_sent_head_that_names_no_one_commit_reads_no_work_and_says_so`

Each case fails the same way:

```
plugin/lib/plan.py:3211: in forecast_rows
    origin = origin_fetched(fleet, t, main)
plugin/lib/plan.py:3243: in origin_fetched
    host_run(fleet, t["machine"], fetch_told(fleet, t["machine"], main, ORIGIN_FETCH), main)
plugin/lib/plan.py:2208: in host_run
    r = crew.on_machine(fleet, host, ["bash", "-c", script, "crew", *args])
plugin/lib/crew.py:850: in this_host
    return subprocess.run(["hostname", "-s"], ...)
E   AssertionError: a logic test starts no process, and this one ran ['hostname', '-s']
```

The cause is task 3.2. It moved `origin_fetched`'s fetch from `kit_git` to `host_run` running `ORIGIN_FETCH`. These cases fake only `plan.kit_git`, so the forecast's fetch now reaches `crew.on_machine` and starts a process. Task notes 3.2 updated `tests/py/test_kits.py` and `tests/py/test_cards.py` for the same move. They missed `tests/py/test_landings.py`, whose `forecast_rows` cases call `origin_fetched` too. These cases need the fetch faked at `host_run`, as `TestLandingReading` now has it, so that each case reads what it read before.

### contract: 1 failed, 124 passed

The failing case is `tests/contract/test_record.py::test_a_branch_busy_for_three_pushes_is_outwaited_each_wait_longer_and_made_before_a_fresh_fetch`:

```
>       assert events == ["read", waits[0], "fetch", waits[1], "fetch", waits[2], "fetch"]
E       At index 2 diff: 0.01 != 'fetch'
E       Left contains 1004810 more items, first extra item: 0.01
```

The case fakes `plan.time.sleep` to record `land`'s replay waits. `plan.time` and `gather.time` are the same `time` module, so the fake also replaces the `time.sleep(LOOK)` that `gather.tried` sleeps between looks. Each fetch and push of the case is now a try, and the fake records every look of 0.01 s. The fake also sleeps for none of them, so the tries spin, and over a million looks were recorded. The case read `land`'s waits and nothing else, and it held before this change. Either the case must record only `land`'s replay waits, or `tried`'s looks must not go through the `time.sleep` that `plan` uses. Which of the two is the code stage's choice. The design names neither.

### What passed

The cases the tasks name all passed inside these two tiers. In `tests/py/test_remote_limit.py` these are `TestTheFamilysLimit`, `TestTheStateRepositorysTries`, `TestAStoppedFetch`, `TestAStoppedPush` and `TestAKitsFetch`. In `tests/contract/test_remote_limit.py` they are `TestATry`, `TestTheStateRepository`, `TestOriginFetch` and `TestGathersFetch`. Also passing are `tests/py/test_kits.py::TestNoFetchInTheRunnersClone` and `tests/py/test_cards.py::TestLandingReading`. Every end-to-end task, `t-docs` and `t-specs` among them, passed, as did `mod` and the flake's tasks.

## The change against its artifacts

- **Validation:** `openspec validate no-try-of-crews-call-to-a-remote-outlasts-its-limit --strict` reports the change valid.
- **Tasks:** all 11 tasks, 1.1 to 4.1, are ticked done.
- **remote-limit:** each of its 7 requirements and 17 scenarios is met in code and named by a case:
  - `gather.TRY_FOR`, `GRACE`, `span`, `stopped`, `tried` and `fetched`;
  - `plan.FETCH`'s `bounded` and `origin_fetch`, and `ORIGIN_FETCH`;
  - `origin_fetched` and `landing_opened`;
  - the cases are in `TestTheFamilysLimit`, `TestATry`, `TestTheStateRepositorysTries`, `TestAKitsFetch`, `TestOriginFetch` and `TestGathersFetch`.
- **drive-state:** both requirements and their 5 scenarios are met:
  - in `plan.git`, `tip_of`, `tips_of`, `land` and `Reading.forget_tip`;
  - the cases are in `TestAStoppedFetch`, `TestAStoppedPush` and `TestTheStateRepository`.
- **Docs:** README's account of a write and `plan.py`'s opening docstring say each fetch and push is one try to the limit of thirty seconds. `t-docs` checks this.

The work meets its specs. It falls short only in the ten existing cases it broke, which leaves the whole checks red, so the change is not archived.
