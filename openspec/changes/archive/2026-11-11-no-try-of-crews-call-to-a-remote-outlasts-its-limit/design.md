# Design

## Context

**The hang.** On deneb on 2026-11-10, sluice's reads of one repository each hung for 10 to 17 minutes. A git fetch's credential helper waited on GitHub, which had taken the call and never answered (agentplot-ops' signal `2026-11-10-agentplot-ops-e19d134d/01`). Nothing bounded the call.

**The family's design.** agentplot/blueprints `design/weir/requirements.md`, read on its main at `ad3a1ae` on 2026-11-11:

- 69 says a try of a call to a remote waits no longer than the family's limit, and is then ended with everything it started, the call failing and naming the call, the remote and the limit.
- C.3 lists the write protocol's tries: the fetch of step 1, the listing that says whether a branch not fetched exists, and the push of step 4.
  - A try runs in a process group of its own and ends at thirty seconds, agentplot/sluice record 0109's limit.
  - At the limit its group is asked to end, given two seconds, then killed, so git's remote helper ends with it.
  - A stopped try fails as `git <fetch|ls-remote|push> with <remote> was still going after 30s, the most a try may take, and was stopped`, after git's last line on standard error where it wrote one.
  - A stopped fetch or listing fails the read. A stopped push fails the write and is no refusal, so it is not replayed.
  - Whether a stopped push landed is read at the next write's fetch. No setting of a writer's changes the limit.
- C.3 also says "crew keeps a twin of these steps in Python, and the pack's cases for the protocol hold both".

**The family's code.** weir's `weir-bounded` holds the limit, the group's ending and the words. Its spec is `remote-limit` on weir's main at `9cba691`, and weir record 0008 gives the reasoning. Both are mirrored here:

- `output` runs a command in a process group of its own and writes its output to unnamed temporary files, with no thread. It waits until the leader has exited and the group is empty, or until the limit. At the limit it ends the group: asked, given `GRACE`, then killed.
- `TRY_FOR` is 30 s, and `GRACE` is 2 s.
- `stopped(call, remote, limit)` gives the words. `span` says a limit as `30s` or `300ms`.
- weir-branch's tests use a silent remote. It is an `ssh://silent.invalid/…` address whose `core.sshCommand` is a script that writes its process id and then becomes `sleep 60`, with `ssh.variant` set to `simple`. The branch's limit is shortened to 300 ms by the crate's own code alone.

sluice bounds its calls by record 0109 (`crates/sluice/src/bounded.rs`, `retry::TRY_FOR`), and Boomdrive's runner by its record 0042. Python cannot take a Rust crate, so crew mirrors `weir-bounded` and cites it.

**Where crew reaches a remote**, read by grep of `plugin/` on 2026-11-11, `ls-remote`, `git fetch`, `git push`, `"fetch"`, `"push"` and `clone`, all fail to show any other call:

- **The state repository**, through `plan.git` in crew's bare cache:
  - `tip_of`'s fetch of one branch (plan.py 682);
  - `tips_of`'s fetch of several (708);
  - `land`'s push (859);
  - `state_init`'s push adopting a blueprints repo's `plan/<label>` (1186).

  There is no listing: crew reads a branch the repository lacks from the fetch's own `couldn't find remote ref`. `record.reach` and `push_now` write through `land`.
- **A kit's origin:**
  - `FETCH`'s `origin_fetch`, inside the scripts `MAIN` (through `MAINS`) and `CARRIES`, run on the kit's host by `host_run` or by `bash -c` here;
  - `kit_git`'s fetch in `origin_fetched` (3112) and `landing_opened` (3297), run on the kit's host through `crew.on_machine`;
  - gather's `fetched` (gather.py 449), run on the kit's host by `ran`.
- Nothing in `plugin/bin/crew`, `plugin/hooks`, `crew.py`, `record.py`, `kit.py` or `runner.py`.

**gather.py stands alone.** It is piped to a host as text (`python3 - < gather.py`) and imports only the standard library (`code.1`), since a host's crew may be older. plan.py already imports it.

**Area pages this change touches:**
- `core.md`: `code.1`, `code.2`, `code.7`, `code.8`, `code.9`, `read.1`, `state.1`, `state.5`, `roles.5`.
- `plan.md`: `plan.1`, `plan.12`, `plan.18`.
- `record.md`: `record.2`, `record.4`.
- `tests.md`: `tests.4`, `tests.8`, `tests.11`.
- `docs.md`: `docs.2`, `docs.6`, `docs.7`.

No rule page is edited by this change (`docs.7`).

## Goals / Non-Goals

**Goals:**
- Every try of crew's git call to a remote ends within the family's limit and its grace. Nothing the try started outlives it, on the host where its git runs.
- A stopped try fails in the family's words, naming the call, the remote and the limit.
- A stopped push is never replayed. Its landing is read at the next write.
- Every local git call runs to its end, as before.

**Non-Goals:**
- **ssh to another host.** It is no git call to a remote. A kit fetch it carries is bounded on that host (Decision 7). `code.3`'s `BatchMode` stands.
- **Other tools' calls crew runs:** sluice, flume, `gh` and `openspec`. Each bounds its own, and sluice's by record 0109.
- **A retry of a stopped read.** crew has none, as weir has none: a command run again tries again.
- **Running weir's conformance pack against crew's twin.** The pack's protocol cases are weir's to run (C.3). crew's own cases mirror `weir-bounded`'s and `shared-branch-write`'s bounded scenarios by name and words.
- **Moving crew's writes onto weir-branch.** That is a change of its own, taking this bound with it.

## Decisions

### 1. One try, `gather.tried`, mirroring weir-bounded's `output`

`tried(argv, cwd=None, input=None, env=None, limit=None)` returns `(exit, out, err, stopped)`:

- It runs the command with `process_group=0`. Its standard output and error go to `tempfile.TemporaryFile()`s, and its input is a temporary file holding `input`, or `/dev/null`.
- Every 10 ms it looks whether the leader has exited and been reaped and whether `os.killpg(group, 0)` finds the group gone. It does this with `time.sleep`, which forks nothing.
- At the limit it sends the group `SIGTERM` and keeps looking for up to `GRACE`. It then sends `SIGKILL` and reaps the leader.
- `limit` None reads `TRY_FOR` at the call.
- A command that cannot start answers `(None, "", why, False)`, as `ran` does.

It lives in gather.py because gather is the one module that must stand alone on a host (`code.1`), and plan.py imports it already.

Not taken:
- **`subprocess.run(timeout=…)`.** It kills only the leader. git's remote helper and credential helper live on, and `communicate` waits on the pipes they hold, which is the deneb hang.
- **A thread per pipe.** weir record 0008 rules it out, and a pipe lets a process outside the group hold the call open, which a file does not.
- **A module of its own beside gather.** It cannot travel with gather's text to a host.

### 2. The limit and the grace are the family's, and fixed

`gather.TRY_FOR = 30.0` and `gather.GRACE = 2.0`, in seconds, each citing `weir-bounded` and sluice record 0109. No teams-file key, environment variable or file sets either.

A test shortens the limit by code alone:
- it passes `limit` to `tried`;
- it sets `gather.TRY_FOR` on the module for a case through `plan.git` or `gather.fetched`, which read it at the call;
- it rewrites the limit's one line in a script's text it runs (Decision 7).

This is the same latitude weir gives its own unit tests ("which the crate's own code alone can set").

Not taken: a key in the teams file or an environment variable, which C.3 rules out ("No setting of a writer's changes the limit").

### 3. The words are weir-bounded's

- `gather.span(limit)` gives whole seconds as `30s` and anything else in milliseconds, as `300ms`.
- `gather.stopped(call, remote, limit, err="")` gives git's last non-empty line of `err` and `; `, where there is one, then `<call> with <remote> was still going after <span>, the most a try may take, and was stopped`.
- **The remote** is named as the call addresses it: a state repository by `url(repo)`, `https://github.com/<owner>/<name>.git`, which holds no credential; a kit by `origin`.
- A stopped try's standard output is never read as an answer.

### 4. Which calls are tries: decided by the call's word

- `plan.reaches_remote(args)` is true when `args[0]` is `fetch`, `ls-remote` or `push`. It is a decision on plain facts (`code.7`), since crew's cache reaches no remote by any other word.
- `plan.git` runs such a call through `gather.tried`, naming the remote as the call's first argument after the word that is not an option.
- Its result carries `stopped`, and a stopped result's `returncode` is never 0, so every caller that reads only the exit still fails it. For a stopped result, `stderr` is the failure (Decision 3) and `stdout` is empty.
- With `check=True`, a stopped call is refused as `git <word> in crew's cache of <repo> failed: <failure>`.
- Every other call runs through `subprocess.run` as before.

Not taken: bounding every git call. A local write killed partway adds a way to fail with nothing to bound (weir record 0008).

### 5. A stopped fetch of a drive's branch fails the read

- `tip_of` and `tips_of` look at `stopped` first. A stopped fetch refuses at once, as `could not fetch <ref(s)> of <repo> over https: <failure>`.
- It is not tried again for `cannot lock ref`, and its `stderr` is never searched for `couldn't find remote ref`.
- So `tips_of` reads no branch as absent from a stopped fetch, and makes no fetch of each branch alone, which would cost a silent remote one more try per branch.
- That this refuses is `read.1`.

### 6. A stopped push fails the write, and is never replayed

- `land` looks at `stopped` before anything else of a failed push. It forgets the command's held tip of the branch (`Reading.forget_tip`), so the command's next read fetches. Then it refuses: `the push of <ref> to <repo> failed: <failure>; it is not pushed again, and the next write reads whether it landed`.
- It does not wait, fetch, or call `make` again.
- `state.1`'s replay is for a push refused because the branch moved. A stopped push is no such refusal: it may have landed. So `state.1` holds, and its outcome, a busy branch outwaited, is unchanged.
- The next write fetches the tip and applies its change there, checking every precondition again (`plan.1`). A write that has landed meets its own effect there, as any write meets another's.
- `record.reach` already says a refused push once and keeps the entry on the host for its next push (`record.2`). A stopped push reaches it as a `Refusal` and is kept the same way.
- If the stopped push did land, the branch holds the entry and the host's file does not. The branch's day file is the union of both by `Id` (`record.4`), so nothing is lost or doubled.
- `state_init`'s adopting push already refuses on any failure, naming git's words. With Decision 4 those words are the failure.

Not taken:
- **Replay.** It forms the write again on a tip that may already hold it (weir record 0008).
- **Reading the branch again before deciding.** It asks the remote that just held a try for thirty seconds once more in the same command.

### 7. A kit's fetch is tried on its own host, in bash

The scripts that fetch a kit (`MAIN`, `CARRIES`) run on the kit's host, over ssh or here. There the host's crew may be older and no crew module is on disk.

**`FETCH` gains a function `bounded <call> <remote> <command…>`**, which tries a command as `tried` does:
- `try_for_ms` and `grace_ms` are set on one line each, filled from `gather.TRY_FOR` and `gather.GRACE` when plan.py builds `FETCH`.
- It runs the command in a process group of its own, with job control on for that start.
- It writes the command's output to temporary files and removes them once read, so no process can hold its caller's pipe open.
- It waits for the leader and the group, or to the limit. At the limit it sends the group `TERM`, waits up to the grace, sends it `KILL`, and reaps the leader.
- When the try is stopped, it writes the failure in `gather.stopped`'s words on standard error, prints none of the command's standard output, and returns 124.
- When the try ends within its limit, it passes the command's standard output, standard error and exit through as they were.
- It runs on bash 3.2, which a Mac's `/bin/bash` is, as well as bash 5: no `wait -n`, no fractional `read -t`, no `$EPOCHREALTIME`.
- It starts no process per look beyond a `sleep` of a tenth of a second. A watcher process that ends the group at the limit, killed with its own group once the try ends, is equally fine.

`origin_fetch` runs `bounded "git fetch" origin git fetch -q origin "$@"`. `MAIN` and `CARRIES` already turn its standard error into `FETCHED=` and `READ=`, so the failure reaches `kit.main_now`'s and `kit.carries_of`'s refusals as it stands.

**`ORIGIN_FETCH`** is `FETCH` with `cd "$1"` and `origin_fetch`. It takes the place of `kit_git(…, "fetch", "-q", "origin")` in `origin_fetched` and `landing_opened`. Both run it with `host_run(fleet, t["machine"], fetch_told(fleet, t["machine"], main, ORIGIN_FETCH), main)`, so every fetching script still goes through `fetch_told` (`roles.3`, `crew-fetches-nothing-in-the-runners-clone`). Both callers already fetch only where `crew.fetches_in`, so `fetch_told` gives the script unchanged. The refusal names the host and carries the failure in place of git's words.

Not taken:
- **Bounding `kit_git`'s ssh here.** Killing a local ssh leaves the far git fetch running on the kit's host, which is what 69 rules out.
- **Running the bounded try through `python3` on the host.** No crew module is on disk there, and handing gather's text to every script is more moving parts than one bash function pinned to the same words by its cases.

This gives crew two copies of one behaviour, in Python and in bash. A logic case pins the bash text's limit and grace to gather's, and a contract case compares its words with `gather.stopped`'s.

### 8. gather's fetch is a try

`gather.fetched` runs `tried(["git", "fetch", "-q", "origin"], main)`. A stopped fetch answers `stopped("git fetch", "origin", TRY_FOR, err)`, which gather already returns as the kit's fetch failure. Its other `ran` calls are local and run as before.

### Rules relied on

- `code.1`: `tried`, `span` and `stopped` are in gather.py, standard library alone.
- `code.2`: every stopped try reaches the user as a `Refusal` through `fail()`.
- `code.7`: `reaches_remote`, `span` and `stopped` are decisions on plain facts. `tried` and `bounded` are the acts.
- `code.9`: a remote that never answers costs a command one try, about 32 s, where it cost it the rest of the agent's shell before.
- `read.1`: a read whose fetch stopped refuses and names what it could not read. It never reads a branch absent or a main unchanged.
- `state.1`, `state.5`: a write is still fetched, applied, checked, committed and pushed without force. Only a refused push is replayed.
- `plan.1`: the next write re-checks every precondition on the tip it lands on.
- `plan.12`: a command still fetches the state branch once. A stopped fetch ends the command's read.
- `plan.18`: main now is still `origin/main` after a fetch. A stopped fetch refuses it as any failed fetch does.
- `record.2`, `record.4`: an entry whose push stopped is said once and kept, and the branch's day file is a union by `Id`.
- `roles.5`: the twin is the statement's own (C.3: "crew keeps a twin of these steps in Python"), and the limit is a step of it. So no mechanism of Flume's, sluice's, Timber's or Pending You's moves into crew, and no stopgap is added.
- `tests.4`, `tests.11`: words and routing are checked in the logic tier, and a process group's ending, a silent remote and the scripts in the contract tier.
- `tests.8`: each case waits on a condition with a generous bound, the try said stopped well inside the silent remote's sixty seconds and its process gone, never on a fixed sleep.
- `code.8`: nothing crew models changes shape, so `board.agent_views` and `status.js` are untouched.

### Departures

None.

## Risks / Trade-offs

- **A slow but live remote** that needs more than thirty seconds, such as a first fetch of a large repository, is stopped every time until the family raises its limit. → The limit is the family's (record 0109), and a host whose calls need longer raises it for the family.
- **A stopped push that landed is reported failed.** An agent that runs the command again may meet its own write. → `plan.1`'s re-check on the new tip refuses it naming what holds, and the refusal's words say the next write reads whether it landed.
- **Two copies, Python and bash, may drift.** → The logic case pins `FETCH`'s limit and grace to gather's, and the contract case holds the bash failure equal to `gather.stopped`'s words.
- **A write's longest is its tries.** Each try is at most 32 s, and each replay of a write refused by a moved branch has its own fetch and push. A remote that answers just inside the limit at every try could hold a write longer than an agent's shell gives a command (`code.9`). → Before this change it was unbounded. A silent remote now costs one try.

## Migration Plan

None. Nothing is stored or read differently.

## After deploy

None. Every outcome is a logic or contract case, and a remote that never answers is staged in the contract tier with no network. A host reaches it with crew's next release (`plan.19`, `code.10`), as any landing does.

## Task notes

**1.1** `plugin/lib/gather.py`:
- `TRY_FOR`, `GRACE`, `span(limit)` and `stopped(call, remote, limit, err="")`, beside `ran`, each docstring citing `weir-bounded`, weir 69 and C.3, and sluice record 0109.

Cases in `tests/py/test_remote_limit.py` `TestTheFamilysLimit`:
- `TRY_FOR` is 30 and `GRACE` is 2;
- `span(30)` is `30s`, and `span(0.3)` is `300ms`;
- `stopped("git fetch", "origin", 30)` gives the family's sentence, and with `err` `"a\nfatal: x\n"` it gives `fatal: x; ` and the sentence.

**1.2** `gather.tried`, as Decision 1. Cases in `tests/contract/test_remote_limit.py` `TestATry`, each passing `limit=0.3`, are the five scenarios of `remote-limit`'s first two requirements:
- the never-ending process with a background sleep;
- one trapping `TERM` that prints `asked`;
- one ignoring `TERM`, stopped no sooner than 2.3 s;
- a leader exiting 0 at once with a background sleep;
- an exit 3 with `out` and `err`, plus `cat` reading the input it is given.

Each wait is on a condition, bounded at 20 s for the try and 10 s for a process to be gone, as `kill -0` reads it (`tests.8`).

**2.1** `plugin/lib/plan.py`:
- `reaches_remote(args)`;
- `git` routes as Decision 4, its try result an object with `returncode`, `stdout`, `stderr` and `stopped`, and `stopped` False on every local call's result.

Cases in `tests/py/test_remote_limit.py` `TestTheStateRepositorysTries`, with `gather.tried` and `subprocess.run` faked to record what they were given:
- `fetch`, `ls-remote` and `push` reach `tried` once each, with `gather.TRY_FOR` and the address;
- `rev-parse`, `commit-tree` and `update-ref` reach `subprocess.run` and never `tried`;
- a stopped result's `returncode` is not 0 even where the leader exited 0;
- `check=True` refuses a stopped call naming the word, the repository and the failure.

**2.2** `tip_of` and `tips_of`, as Decision 5. Cases in `TestAStoppedFetch`, with `plan.git` faked:
- a stopped `tip_of` fetch refuses once, naming the ref, the repository and the failure, with no second fetch for a lock;
- a stopped `tips_of` fetch whose `stderr` holds `couldn't find remote ref` refuses once, reading no branch as None and calling `tip_of` for none.

**2.3** `land` and `Reading.forget_tip`, as Decision 6. Cases in `TestAStoppedPush`, with `plan.git` faked so a push stops, and with `time.sleep` and `random.random` faked:
- the write refuses with the failure and the closing words, `make` called once, no sleep and no fetch after the push;
- the command's next `tip_of` of the branch fetches, and a `make` given that tip is applied on it;
- `record.reach` with a stopped push says it once on standard error and keeps the entry in the host's file.

**2.4** Cases in `tests/contract/test_remote_limit.py` `TestTheStateRepository`. The silent remote is weir's: a `silent.sh` that writes its process id and becomes `sleep 60`, set as `core.sshCommand` with `ssh.variant = simple`, and `url."ssh://silent.invalid/".insteadOf = https://github.com/` in the case's home `.gitconfig`. `gather.TRY_FOR` is set to 0.3 for the case.
- `plan.tip_of` refuses within 20 s naming the branch, `git fetch`, `https://github.com/<owner>/<name>.git` and `300ms`, and the silent process is gone.
- `plan.land`, its tip held as none (`READ.keep_tip(repo, ref, "")`, so nothing is fetched first), refuses naming `git push`, the address and `300ms`. The silent script ran once, and its process is gone.

**3.1** `FETCH`'s `bounded` and `origin_fetch`, and `ORIGIN_FETCH`, as Decision 7. `FETCH` is built in plan.py from `gather.TRY_FOR` and `GRACE` as `try_for_ms=30000` and `grace_ms=2000`, one line each.

Cases in `tests/contract/test_remote_limit.py` `TestOriginFetch`, run under every distinct bash among `bash` on the path and `/bin/bash`. Each runs a kit whose `origin` is `ssh://silent.invalid/kit.git`, with the silent script in the kit's own config, and the script's text with `try_for_ms=30000` rewritten to `try_for_ms=300`:
- `MAIN` says `FETCHED=` with `git fetch with origin was still going after 300ms, the most a try may take, and was stopped`, equal to `gather.stopped("git fetch", "origin", 0.3)`, within 20 s, and the silent process is gone;
- `CARRIES` says `READ=` with the same words;
- `ORIGIN_FETCH` exits non-zero with the words on standard error;
- against a responsive bare origin, `ORIGIN_FETCH` fetches and exits 0 with nothing on standard error.

**3.2** `origin_fetched` and `landing_opened` run `ORIGIN_FETCH`, as Decision 7.

Cases in `tests/py/test_remote_limit.py` `TestAKitsFetch`:
- `FETCH` holds `try_for_ms=30000` and `grace_ms=2000` once each, and no `${` reading either from outside;
- the source of `gather.tried`, `gather.stopped` and `gather.span` (read with `inspect.getsource`), and `FETCH`'s text, hold no `environ`, `getenv`, `open(` or `teams`;
- no `kit_git(` call in plan.py passes `"fetch"`;
- no `ran(` or `subprocess` call in gather.py passes `"fetch"`;
- `origin_fetched` runs `ORIGIN_FETCH` through `fetch_told` and `host_run` on the kit's host, `host_run` faked.

Two existing classes change with it:
- `tests/py/test_kits.py` `TestNoFetchInTheRunnersClone`: add `ORIGIN_FETCH` to `FETCHING`, and have `test_a_forecasts_read_fetches_nothing_in_the_runners_clone` fake `host_run` in place of `kit_git`.
- `tests/py/test_cards.py` `TestLandingReading`: its `read` helper fakes `host_run` for the reading's fetch in place of `kit_git`. Each case then records the folder the fetch ran in and the fetch that was told.

**3.3** `gather.fetched` through `tried`, as Decision 8. A case in `tests/contract/test_remote_limit.py` `TestGathersFetch`, with `gather.TRY_FOR` set to 0.3: a kit whose origin is the silent remote gives the stopped words naming `origin` and `300ms` within 20 s, and the silent process is gone.

**4.1** README's sentence on a write in The plan ("pushes without force; a push refused because someone wrote first is applied again…") gains:
- each fetch and push a write makes is one try, ended at the family's limit of thirty seconds with everything it started;
- a stopped push fails the write and is not applied again, and the next write reads whether it landed;
- a kit's fetch of its origin is such a try too.

plan.py's opening docstring says the same of a write.

`tests/t-docs.sh` gains a check that README says a try is ended at thirty seconds and a stopped push is not applied again. No command's usage changes (`docs.2`).
