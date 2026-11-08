# Verify: a-cards-preview-is-asked-of-the-runner

Verified 2026-11-08 on `change/a-cards-preview-is-asked-of-the-runner` at 7f7ff0a8, cut from `bolt/crew-asks-the-runner-for-previews` (at main's 3d5a2e5a).

**Verdict: the work falls short.** Two of the whole checks fail, so the change is not archived and goes back to its code stage.

## The whole checks

`tests/suite --affected` was run once from the worktree's root. This is the set of check-full tasks the change affects, the same set sluice's gate runs; the change touches crew's command core, so every task was selected. It ended **`26 passed (1 replayed), 2 failed`**, exit 1.

| task | outcome |
|---|---|
| logic, contract (125 passed), mod, nix | ok |
| t-briefs, t-docs (replayed), t-help, t-flume-source, t-hold, t-journey-board, t-journey-cross, t-journey-main, t-journey-main-fix, t-journey-ops, t-journey-plan, t-journey-review, t-journey-roles, t-journey-signals, t-journey-state, t-roles, t-runner, t-session-hook, t-slot, t-sluice, t-stage-facts, t-suite, t-teams, t-waits | ok |
| **t-cards** | **FAIL** |
| **t-journey-land** | **FAIL** |

### t-cards: the rail's read crashes on a card posted with no key

`crew rail --label wldn` exits with a traceback (`code.2` rules out a traceback reaching the user):

```
File "plugin/lib/plan.py", line 12350, in rail_read
    read["previewed"] = previews_changed(fleet, read)
File "plugin/lib/plan.py", line 15911, in previews_changed
    elif c["by"] == f"{l}-planner" and re.fullmatch(r"batch/\d+", key):
TypeError: expected string or bytes-like object, got 'NoneType'
```

- **The cause.** `previews_changed` takes every open card on the main machine from `read["cards"]`. `rail_times` keeps a card's `key` as `e.get("Key")`, which is `None` for a card posted with no `Key`. The planner's own question reaches `re.fullmatch` with `None`: t-cards posts it at `tests/t-cards.sh:614` (`card.post` on `agent/wldn-planner` with only `Card`), and `crew rail --label wldn` at line 627 then fails.
- **What it breaks.** An agent's own question is posted with no key, so the whole rail read on the partition's main machine fails whenever such a card is open in the planner's name, not only the preview part. `land_key` reads a missing key as `""`, so ops's keyless cards pass. It is the planner's `batch/` test that has no such guard.
- **Where the logic tier missed it.** `tests/py/test_rail.py`'s `TestPreviews` has no case of an open card without a key.
- **What fixing it needs.** `previews_changed` passes over a card with no key, and a logic case pins that.

### t-journey-land: ended with no output

moon recorded `exitCode: -1` after 3 m 15 s, with empty `stdout.log` and `stderr.log` (`.moon/cache/states/tests/t-journey-land/`). The process ended on a signal before `tests/run` printed anything. This is the end-to-end test of task 4.1, so 4.1's check ("ends with 0 failed") is not met on this run. The checks were not run a second time, as this stage requires, so whether it hangs, times out or fails is the code stage's to find. The rail read's crash above is one candidate: the test runs `crew rail` across a landing's preview.

## The work against the change

### Tasks

All 15 tasks of `tasks.md` are ticked. Two of their checks do not hold on this run:
- 4.1: t-journey-land, above.
- 3.4: its pytest case passes, but the rail's read it describes fails end to end on t-cards.

### drive-state

- **"crew asks a host's runner for work by requests on the drive's branch"** is met.
  - `requests.rec`'s `Act` takes `preview`, last, with `Done bool` and `Branch Revision Done` after `Base`.
  - Apart from `land`, which the `land` change adds (design Decision 1), this matches Boomdrive v0.6.0's tests' copy (`crates/boomdrive-crew/tests/common/mod.rs`).
  - A preview and its done are each one plan write.
- **"crew reads each host's runner from that runner's own branch"** is met.
  - `PREVIEWS` is Boomdrive v0.6.0's `write.rs` `PREVIEWS` byte for byte, read against the tag on this host.
  - `host_read` reads `previews.rec` as specified: a request twice or missing hides the runner; a Text or Status that is no JSON marks that preview alone; no file means no preview answered.
- **"A preview names its host, its work, its repository, its branch and its revision"** is met. `request_refusal` refuses:
  - a preview naming no `Host`;
  - extra fields;
  - work other than `bolt/<b>` or `unit/<u>`;
  - `bolt/<b>` on any other act;
  - a `Done` other than `yes`.
- **"A preview is read from the runner on the host it names"** is met. `preview_report` reads that host alone, reading a refusal in `answers.rec` as the runner's. `previews_standing` keys asks by `(Host, Repo, Revision)` and stands again after a done.

### rail-cards

- **What a card says.** `cards.preview_said` and `made_said` carry each state of Decision 4, and "No preview." and the policy shape are gone. This covers "A preview that fails is said on the card and holds nothing" and "A card is changed in place when the runner reports its preview anew".
- **Changing a card.** `previews_changed` compares each card's word with `previews.json` and changes the card once. It leaves a card answered by `card.answer`, and changes it once more when the cache is lost. It also covers the case it crashes on, a card with no key (above).
- **The offer on every row.** Each row that can land carries `{branch, head, state: "ask"}` with no policy read (`kit.previewed` and `head_previewed` gone), which is "A landing row carries what brings its bolt's preview up".
- **`crew card preview`** is "The user asks for a preview by writing on the card" and "A preview asked for from a card is asked of the runner and listed while it is up".
  - It is refused for anyone but the owner, and for a thing the card does not carry.
  - It is forwarded to the main machine, writes one request through `ask_step`, and writes nothing for a standing ask.
  - It asks again after a refusal.
  - `REQUESTERS` names `card preview` for main-ops and the planner.
- **Where crew writes a done.** This is "A preview is released on the user's done and when its card or row ends" and "A moved head releases the preview of the old one and asks for none". A done is written:
  - at the raise of a landings card, in `landings_previews`, for a row held, gone, landed or at a moved head, the last saying `released`;
  - at a batch card's close, in `batch_previews_put_away`, keeping a unit another open batch card holds;
  - at the rail's read after two minutes of grace, in `sweep_previews`.
  None is written for a refused ask or for a preview crew did not ask for.
- **What is gone** (Decision 9): every `sluice preview`, `sluice previews` and `sluice release` for a preview, `~/.local/state/crew/previews`, and `_preview`, `_card-preview` and `_preview-release`. `test_crew_runs_no_sluice_command_for_a_preview` guards against their return.
- **The briefs and docs** (Decision 10, `docs.2`) are updated together: ops's and the planner's briefs, README, the crew skill and the usage header of `crew card preview`.

`openspec validate a-cards-preview-is-asked-of-the-runner --strict` passes. Each MODIFIED requirement is in `openspec/specs/`, and the renamed one's FROM header is there too.

Beyond the two failing checks, the code meets every requirement and scenario read here. The change is not archived.
