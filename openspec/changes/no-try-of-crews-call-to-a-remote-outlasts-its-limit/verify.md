# Verify: no-try-of-crews-call-to-a-remote-outlasts-its-limit

Read on 2026-11-11 at `change/no-try-of-crews-call-to-a-remote-outlasts-its-limit`, head 91814b9b, cut from `bolt/no-try-of-crews-call-to-a-remote-outlasts-its-limit`.

**Verdict: ready to archive.** The whole checks pass, every task is done, and every requirement and scenario of the change's two specs is met.

## The whole checks

`tests/suite` ran once, with every project's `check-full` tasks, as `.config/sluice.toml` requires of `bolt/*` and `main`:

```
37 passed (35 replayed), 0 failed
exit 0
```

- **logic** ran afresh: 3559 passed.
- **contract** ran afresh: 125 passed.
- The other 35 tasks were replayed from runs on this host whose inputs were identical, and every one passed. They are `mod`, the flake's `nix:format`, `nix:lint`, `nix:test` and `nix:typecheck`, and every end-to-end test, `t-docs` and `t-specs` among them.

## The tasks

All 12 tasks, 1.1 to 4.1, are ticked done, and the check each one names is inside the whole checks above:

- **1.1 to 1.2**: `TestTheFamilysLimit` (logic) and `TestATry` (contract).
- **2.1 to 2.3**: `TestTheStateRepositorysTries`, `TestAStoppedFetch` and `TestAStoppedPush` (logic).
- **2.4**: `TestTheStateRepository` (contract).
- **2.5**: `tests/contract/test_record.py`. The case of a branch busy for three pushes fakes `plan`'s own clock (`LandsClock`) and leaves `gather`'s `time` module alone. It records `land`'s replay waits and nothing else, while each fetch and push, now a try, looks at its git as it runs.
- **3.1 and 3.3**: `TestOriginFetch` and `TestGathersFetch` (contract).
- **3.2**: `TestAKitsFetch`, `test_kits.py::TestNoFetchInTheRunnersClone` and `test_cards.py::TestLandingReading` (logic).
- **3.4**: `tests/py/test_landings.py`. Its forecast and bolt-work cases fake the kit's fetch at `host_run` (`origin_fetches`). Each asserts that `ORIGIN_FETCH` runs once in the kit's folder and that no fetch goes through `kit_git`. A refused fetch is said in `host_run`'s words, `on <host>: <git's words>`, which keeps git's words as rail-cards' "crew cannot compare the heads" asks.
- **4.1**: `t-docs`.

## The change against its specs

`openspec validate no-try-of-crews-call-to-a-remote-outlasts-its-limit --strict` reports the change valid.

### remote-limit: 6 requirements, 18 scenarios, all met

- **A try runs to its limit in a process group of its own.** `gather.tried` starts its command with `process_group=0`. At the limit it asks the group to end, waits `GRACE`, then kills it. Its four scenarios are in `TestATry`.
- **A try that ends within its limit gives its exit and all it printed.** `tried` gives its exit, its standard output and its standard error, and passes on the input it is given. Both scenarios are in `TestATry`.
- **The limit and the grace are the family's.** `gather.TRY_FOR` is 30 and `GRACE` 2. `plan.FETCH` fills `try_for_ms=30000` and `grace_ms=2000` from them, once each. Neither `tried`, `stopped` nor `FETCH` reads an environment variable, a file or the teams file. The cases are `TestTheFamilysLimit` and `TestAKitsFetch`.
- **A stopped try is named with its call, its remote and its limit.** `gather.stopped` and `gather.span` give these words, and so does bash `bounded`'s line for the same stop. The cases are `TestTheFamilysLimit`, `TestOriginFetch` and `TestGathersFetch`.
- **The state repository's calls to its remote are tries.** `plan.git` sends `fetch`, `ls-remote` and `push` (`REMOTE_WORDS`, `reaches_remote`) through `gather.tried`, naming the address. Every other call runs to its end. The case is `TestTheStateRepositorysTries`.
- **A kit's fetch of its origin is a try.**
  - gather's `fetched` runs `git fetch -q origin` through `tried`.
  - `MAIN`, `CARRIES` and `ORIGIN_FETCH` fetch only through `FETCH`'s `origin_fetch`, which uses `bounded`.
  - `origin_fetched` and `landing_opened` run `ORIGIN_FETCH` through `fetch_told` and `host_run`.
  - No `git fetch` of a kit is left in `kit_git`, `ran` or a script outside `FETCH`. The only remaining fetches in `plan.py` are the state repository's, in `tip_of` and `tips_of`, and those go through `plan.git`.
  - The cases are `TestOriginFetch`, `TestGathersFetch` and `TestAKitsFetch`.

### drive-state: 2 requirements, 5 scenarios, all met

- **A stopped fetch of a drive's branch fails the read.** In `tip_of` and `tips_of`, a stopped fetch (`was_stopped`) refuses at once, naming the branch, the repository and the stopped try. It is never tried again for a lock and never read as an absent branch. The cases are `TestAStoppedFetch` and the contract tier's `TestTheStateRepository`.
- **A stopped push fails the write and is never replayed.** In `land`, a stopped push refuses at once with the stopped try. Nothing waits, nothing is fetched and nothing is applied again. `Reading.forget_tip` makes the next read fetch, and a run-record entry stays on the host for its next push. The cases are `TestAStoppedPush` and `TestTheStateRepository`.

### Docs and the rest

README's account of a write and `plan.py`'s opening docstring say that each fetch and push is one try, ended at the family's limit of thirty seconds. They say a stopped push is not applied again, and the next write reads whether it landed. `t-docs` checks this.

Nothing crew models changes shape, so the views and crew's mod are unchanged (`code.8`). No command or flag changes, so the usage is unchanged (`docs.2`), as the proposal says.

## Outcome

The whole checks are green and the work meets its specs and tasks, so the change is archived with this report.
