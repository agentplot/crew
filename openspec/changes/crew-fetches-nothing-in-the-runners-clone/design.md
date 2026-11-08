# Design

## Context

**The ruling.** agentplot-design, on batch 12 of `crew-finds-a-kit-in-the-runners-copy`: where the teams file names a kept repository for the host, crew runs no git fetch in it, and neither does any brief crew writes. Crew and the main-level agents read GitHub's branches there at origin's tracking refs, as the runner last fetched them. The runner fetches every pass and at once on a landing. A read that needs them fresher waits for the runner's next fetch. Elsewhere crew fetches as today. Sources: agentplot/boomdrive `core.14`; crew records 0056 and 0061.

**`core.14`, read on agentplot/boomdrive's main at 14a9139 on 2026-11-08:** "The runner's clone of a repository is the host's one clone of it: Flume, sluice and what a launch runs may work in its container, and the runner alone fetches it and moves its view; it reads every branch at origin's tracking ref".

**Where crew fetched in a kit, read by grep of `plugin/` on 2026-11-08:**
- gather's `kit`, through `fetched`, for a survey asked to fetch: `crew bolts`, and `stages_for` with fetch.
- `MAINS`, inside `POLICY`, `GIVE_READ`, `MAIN` and `LANDED`. These serve a give's policy, a landing's recorded head, `crew record`'s record, a change's folder and a pull request's hold.
- `BOLT_CREATE`, after sluice makes the bolt's branch.
- `CARRIES`, what a tip carries of other bolts.
- `LAND_COPIES`, the bolt's two copies before a landing.
- `origin_fetched`, for the landings card's forecasts and a bolt's work, in the folder the runner reported.
- `landing_opened`, when a landing's reading is tried again.
- The design brief: before reading what is built, before cutting a worktree, after a conflict, and `git pull --rebase` in the blueprints checkout. The operator brief: before cutting its swancloud worktree.
- No others. Crew's fetches of the state repositories go to its own bare cache, which is no kit's clone. `plugin/bin/crew` and `plugin/hooks` fetch nothing.

**The runner's views are detached.** On deneb on 2026-11-08, `~/Code/boomdrive/agentplot/blueprints`, `…/crew` and `afterthought/swancloud` each stand at a detached `HEAD`, a worktree of the container's bare clone.

**Area pages this change touches:** `core.md` (`code.7`, `read.1`, `roles.3`, `code.8`), `plan.md` (`plan.18`, `plan.19`), `briefs.md` (the briefs' words), `teams.md` (`teams.10`), `tests.md` (`tests.4`, `tests.6`, `tests.11`), `docs.md` (`docs.2`, `docs.7`). No rule page is edited by this change (`docs.7`).

## Goals / Non-Goals

**Goals:**
- No git fetch or pull run by crew, or told by a brief crew writes, in a repository the host's teams file names.
- Every read there takes origin's tracking refs as the runner last fetched them. A landing that would otherwise submit a head GitHub has moved past waits instead.
- Every other checkout fetched exactly as before.

**Non-Goals:**
- A folder the runner reports for a repository the host's teams file does not name. The ruling's "elsewhere" keeps that fetched as today.
- Another host's teams file, which crew does not read (record 0061, Decision 4 of `a-kept-repositorys-folder-is-the-runners-container`).
- Asking the runner to fetch. The runner fetches every pass and at once on a landing.
- crew's landings themselves, which record 0056 retires in its own unit.

## Decisions

### 1. One decision, on paths: `crew.fetches_in`

- `crew.runners_clone(fleet, host, path)` gives the repository the host's teams file names whose `dir` or `checkout` is the path, or holds it. A place or worktree under the container is included. On any other host, or for any other path, it gives none.
- `crew.fetches_in` is its negation. It starts no process (`code.7`).
- Keyed on the path, because every caller holds the path it would fetch in. A kit read at the folder the runner reported (`kit_at`) is the file's `dir` on a runner host, so it is caught too.
- Not taken: keying on the repository's address. `kit_at`'s kit carries a name and a folder, not always the address.

### 2. A script is told `fetch=no`, on its first line

- Every script that fetches defines `origin_fetch` (`FETCH`):
  - it fetches unless told `fetch=no`;
  - it does nothing on `fetch=no`;
  - it refuses any other word, fetching nothing (`read.1`).
- `plan.fetch_told(fleet, host, main, script)` prefixes `fetch=no` in the runner's clone and returns the script untouched elsewhere. Each run of `MAINS`'s four scripts, `BOLT_CREATE`, `CARRIES` and `LAND_COPIES` goes through it, on a host by ssh or here.
- A logic case reads `plan.py`: no such script reaches `host_run` or `bash -c` but through `fetch_told`, and no `git fetch` is left in one outside `FETCH` (`roles.3`).
- Not taken:
  - A word on every script, `fetch=yes` too, with a script told nothing refused. It is stricter, but some sixty landing cases key their fakes on each script's text, on a path record 0056 retires. The guard above holds the same line.
  - An environment variable, which ssh does not carry.

### 3. Main now in the runner's clone is `origin/main` as the runner last fetched it

- `MAINS` says `FETCHED=runner` there. `kit.main_now` takes `origin/main` as main now.
- A clone with no `origin/main` yet is refused, saying the runner's next fetch brings it.
- Every caller of main now reads as before: a give's policy, a landing's head and its end, `crew record`, a change's folder, a pull request's hold.

### 4. A landing waits where GitHub has moved past the runner's fetch

- A landing submits the bolt's head as `LAND_COPIES` reads it, and sluice pushes that head over GitHub's `bolt/<bolt>` (`plan.19`). Without crew's fetch, a stale tracking ref would submit a head behind GitHub's.
- So in the runner's clone `LAND_COPIES` compares the tracking ref with the head `git ls-remote` reads on GitHub. `ls-remote` writes no ref and fetches nothing. Where they differ, it reads `READ=`, saying the landing waits for the runner's next fetch, and nothing is submitted (`read.1`).
- Elsewhere the fetch makes them one, as before.
- `CARRIES`, a forecast and a bolt's work read stale branches at worst as more work beyond main. That refuses or warns, and never submits.

### 5. gather is asked kit by kit

- A survey that fetches marks each kit's entry `fetch`, from `crew.fetches_in` on the kit's host and checkout. gather fetches a kit only on its own entry's word.
- The request no longer carries a `fetch` of its own. gather is piped from the caller, so both sides change together.

### 6. The briefs name the runner's clone and fetch nothing there

- **`{{KIT_CHECKOUTS}}`** marks each kit in the runner's clone: `` (its folder `<dir>`; the runner's clone, which only the runner fetches) ``.
- **`{{FETCHING}}`** names the repositories the runner keeps on the main level's host. It says no `git fetch` or `git pull` is run there, that branches are read at `origin/<branch>` as the runner last fetched them, and that a fresher read waits for the runner's next fetch. Where none is the runner's, it says so in words (`teams.10`).
- **The design brief's fetches**, before reading what is built, before a worktree and after a conflict, each say none is run in a runner's clone. After a conflict, it merges `origin/main` once the runner's fetch holds the landing it conflicts with.
- **`{{BLUEPRINTS_COMMIT}}`.** Where the blueprints checkout is the runner's view, detached and moved by the runner alone, the agent commits on a branch of its own in a worktree under the container's `places/`, cut from `origin/main` as the runner last fetched it, and tells the user the branch. Elsewhere it keeps today's pull and commit on `main`. "Push only when the user says so" stands.
  - This is this change's choice, cheap to change, made on record 0061 ("Design worktrees and every other worktree crew's agents cut are worktrees of that folder's clone") and `plan.18`.
  - Not taken: leaving the pull, which is a fetch the ruling rules out; committing in the runner's view, which `core.14` gives the runner alone to move.
- **`{{SWANCLOUD_FETCH}}`.** The operator's brief cuts its worktree from `origin/main` as the runner last fetched it, with no fetch, where swancloud is in the runner's clone. Elsewhere it fetches first, in today's words.
- `tests/t-briefs.sh` pins the phrases (`tests.6`).

### Rules relied on

- `code.7`: `runners_clone` and `fetches_in` are decisions on plain facts. `fetch_told` and the scripts are the acts.
- `read.1`: a landing that cannot tell its head is GitHub's waits and says so, and a script given a word it cannot read fetches nothing.
- `roles.3`: the brief's words are backed by a check in crew that no script fetches without being told.
- `teams.10`: every new token fills with text on every host.
- `plan.19`: a bolt is read where it lives, at `origin/bolt/<bolt>`.
- `code.8`: no bolt, unit, stage, card or rail row changes shape, so `board.agent_views` and `status.js` are untouched.

### Departures

- **`plan.18`** says every read of main now in crew is `origin/main` after a fetch. In the runner's clone it is `origin/main` as the runner last fetched it, on agentplot-design's ruling and boomdrive `core.14`. The rule's words are the design agent's to amend once this lands (`docs.7`).

## Risks / Trade-offs

- **A read lags GitHub by up to one runner pass.** A forecast or `crew bolts` may show a merge landed on GitHub minutes late. → The runner fetches at once on a landing (Boomdrive clones spec), and the ruling accepts the wait.
- **A missed fetch site would fetch in the runner's clone silently.** → The logic case of Decision 2 reads every run of a fetching script, and the grep above found no other.

## Migration Plan

None. A host whose teams file names no repositories behaves as before.

## After deploy

None. Every outcome is a logic, contract or end-to-end case. deneb's crew reaches this on the user's word with record 0061's pin, as `a-kept-repositorys-folder-is-the-runners-container` does.

## Task notes

**1.1** `plugin/lib/crew.py`:
- `runners_clone(fleet, host, path)` and `fetches_in(fleet, host, path)`, beside `kept_at`;
- paths compared after `os.path.normpath`, a path the root or under `root + "/"`.

Cases in `tests/py/test_kits.py` `TestNoFetchInTheRunnersClone`:
- container, view, a place under the container and a worktree under another named repository are the clone;
- a sibling folder, a parent, the spaces' checkouts, another host, and a fleet with no `repositories` are not.

**1.2** `plugin/lib/plan.py`:
- `FETCH` and `fetch_told`;
- `MAINS`, `BOLT_CREATE`, `CARRIES` and `LAND_COPIES` take `FETCH` and fetch only through `origin_fetch`; `MAINS` says `FETCHED=runner` on `fetch=no`; `LAND_COPIES` keeps `ls-remote`'s head and compares it on `fetch=no`;
- every run of them through `fetch_told`: `kit_policy`, `bolt_land`, `pull_hold`, `landing_submitted`, `bolts_carried`, `landing_close_out`, `op_bolt_start`, `change_folder`, `record_read`.

`plugin/lib/kit.py` `main_now` takes `runner`. Cases in `TestNoFetchInTheRunnersClone`:
- `fetch_told` prefixes `fetch=no` in the clone and returns the script itself elsewhere;
- each script has `origin_fetch` and no other `git fetch`;
- no run in `plan.py` passes one but through `fetch_told`;
- `main_now` on `FETCHED=runner`, with and without `origin/main`.

**1.3** `origin_fetched` and `landing_opened` fetch only where `crew.fetches_in`, the latter's words saying it reads main as the runner last fetched it. A case in `TestNoFetchInTheRunnersClone` with `kit_git` faked.

**1.4** `plan.survey` marks each kit's entry `fetch` when it fetches, and gather reads the kit's own. `tests/py/test_bolt_commands.py` `TestWhenABoltIsFetched` reads the kits' marks: a kit in box's clone is asked unfetched, and so is none on another host.

**2.1** `tests/contract/test_git.py` `TestTheRunnersClone`, each script run as `fetch_told` gives it for a fleet naming the scratch repository:
- `MAIN` reads `origin/main` as last fetched with origin unreachable and every remote ref unmoved, then GitHub's head once the test fetches as the runner would. A word that is neither is refused.
- `CARRIES` reads at the tracking refs, and reads main's landing once the test fetches.
- `LAND_COPIES` waits while GitHub's `bolt/b` is past the tracking ref, and reads both copies once the test fetches.

`tests/contract/test_gather.py`: a kit asked `fetch` false reads the bolt as last fetched and moves no ref; one asked true reads GitHub's.

**3.1** `plugin/lib/crew.py` `main_tokens` and the briefs, as Decision 6 says. `tests/t-briefs.sh` pins every new phrase:
- the box's design brief says no checkout is a runner's clone, and keeps the pull;
- the runner host's design brief marks crew, names the runner's repositories, cuts a blueprints branch in a worktree and lacks `git pull --rebase`;
- its operator brief cuts with no fetch and lacks `fetch -q origin`.

**3.2** README's bolt paragraph and the crew skill's say crew fetches nothing in the runner's clone. No command's usage changes (`docs.2`).
