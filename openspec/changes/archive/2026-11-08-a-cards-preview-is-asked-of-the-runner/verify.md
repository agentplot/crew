# Verify: a-cards-preview-is-asked-of-the-runner

Verified 2026-11-08 on `change/a-cards-preview-is-asked-of-the-runner` at b55e1e4c, cut from `bolt/crew-asks-the-runner-for-previews` (at main's 3d5a2e5a).

**Verdict: the work holds.** The whole checks pass and the code meets every requirement and scenario of the change's specs. The change is archived with this report.

## The whole checks

`tests/suite --affected` was run once from the worktree's root. It runs the check-full tasks the change affects, the same set sluice's gate runs. The change touches crew's command core, so every task of the `tests` project was selected. It ended **`28 passed (1 replayed), 0 failed`**, exit 0.

| task | outcome |
|---|---|
| logic, contract | ok |
| t-briefs, t-cards, t-docs, t-flume-source, t-help, t-hold, t-journey-board, t-journey-cross, t-journey-main, t-journey-main-fix, t-journey-ops, t-journey-plan, t-journey-review, t-journey-roles, t-journey-signals, t-journey-state, t-roles, t-runner, t-session-hook, t-slot, t-sluice, t-stage-facts, t-suite, t-teams, t-waits | ok |
| t-journey-land | ok, replayed |

- **The replay.** t-journey-land's inputs are identical to a run that passed on this host, the code stage's run of task 4.2, so `tests/suite` replayed it. sluice runs it afresh on the submission (`tests.5`).
- **Not selected.** The `tests` project's `mod` task and the `nix` project's four tasks were not selected. The change touches none of their inputs: `plugin/hooks/`, `plugin/tests/`, `plugin/lib/crew.py`, `flake.nix`, `nix/`, the devenv files and the toolchain files.

## The work against the change

### Tasks

All 17 tasks of `tasks.md` are ticked, and each check named holds on this run.
- 3.7 is met. `previews_changed` passes over a card whose key is `None` (`plugin/lib/plan.py`, `previews_changed`), and `TestPreviews.test_a_card_posted_with_no_key_is_passed_over` pins it. t-cards' `crew rail --label wldn`, with the planner's keyless question open, passes.
- 4.1 and 4.2 are met. t-journey-land passes with every check under it.

### drive-state

- **"crew asks a host's runner for work by requests on the drive's branch"** is met.
  - `requests.rec`'s `Act` takes `preview`, last, with `Done bool`, and `Host` and `Branch Revision Done` in `%allowed`.
  - Apart from `land`, which the `land` change adds (design Decision 1), the descriptor matches Boomdrive v0.6.0's tests' copy (`crates/boomdrive-crew/tests/common/mod.rs`, read against the tag on this host).
  - A preview and its done are each one plan write.
- **"crew reads each host's runner from that runner's own branch"** is met.
  - `runner.PREVIEWS` is Boomdrive v0.6.0's `crates/boomdrive-crew/src/write.rs` `PREVIEWS` byte for byte, read against the tag.
  - `FILES` reads `previews.rec` as the fifth file.
  - `host_read` treats it as specified: a request twice or missing hides that runner; a `Text` or `Status` that is no JSON marks that preview alone unread; no file means no preview answered.
- **"A preview names its host, its work, its repository, its branch and its revision"** is met. `request_refusal`, under `ACTS["preview"]` and `WORK`, refuses:
  - a preview naming no `Host`;
  - fields a preview does not take;
  - work other than `bolt/<b>` or `unit/<u>`;
  - `bolt/<b>` on any other act;
  - a `Done` other than `yes`.
- **"A preview is read from the runner on the host it names"** is met.
  - `preview_report` reads that host's runner alone, and reads a refusal in `answers.rec` as the runner's.
  - `previews_standing` keys asks by `(Host, Repo, Revision)`. The newest request stands while it is a bring-up the runner has not refused, and it stands again after a done.

### rail-cards

- **What a card says.**
  - `cards.preview_said` and `made_said` say each state of Decision 4: asked, held, coming up, up, failed, refused in the runner's or sluice's words, unlisted and unread.
  - "No preview." and the policy shape are gone.
  - This covers "A preview that fails is said on the card and holds nothing".
- **The offer on every row.** Each row that can land carries `{branch, head, state: "ask"}`. No policy is read for it: `kit.previewed` and `head_previewed` are gone, and no `.config/sluice.toml` is read. No request is written when the row is posted or changed. This is "A landing row carries what brings its bolt's preview up".
- **`crew card preview`** meets "The user asks for a preview by writing on the card" and "A preview asked for from a card is asked of the runner and listed while it is up".
  - It is refused for anyone but the owner, and for a thing the card does not carry.
  - It is forwarded to the main machine and writes one request through `ask_step`. It writes nothing while an ask stands that the runner has neither refused nor reported failed, unlisted or unread, and it asks again after a refusal.
  - It changes the card in place.
  - `REQUESTERS` names `card preview` for main-ops and the planner.
- **Where crew writes a done.** This covers "A preview is released on the user's done and when its card or row ends" and "A moved head releases the preview of the old one and asks for none". A done is written:
  - by `--done`;
  - at the raise of a landings card, in `landings_previews`, for a row held, gone, landed or at a moved head, the last saying `released`;
  - at a batch card's close, in `batch_previews_put_away`, keeping a unit another open batch card holds;
  - at the rail's read after two minutes of grace, in `sweep_previews`.
  None is written for a refused ask or for a preview crew did not ask for.
- **Changing a card when the runner reports anew.** `previews_changed` compares each waiting card's word with `previews.json` and changes the card once per change. It leaves a card answered by `card.answer`, changes it once more when the cache is lost, and passes over a card posted with no key. This is "A card is changed in place when the runner reports its preview anew".
- **What is gone** (Decision 9). crew runs no `sluice preview`, `sluice previews` or `sluice release` for a preview. `sluice release --worktree` is still used, but only by the tidy of a place's worktree. Also gone are `~/.local/state/crew/previews` and the commands `_preview`, `_card-preview` and `_preview-release`. `test_crew_runs_no_sluice_command_for_a_preview` guards against their return.
- **The briefs and docs** (Decision 10, `docs.2`) are updated together: ops's and the planner's briefs, README, the crew skill and the usage header of `crew card preview`. t-briefs and t-docs pass.
- **The views and the mod.** `code.8` is unchanged, since no view carries a preview. The `mod` task is unaffected.

`openspec validate a-cards-preview-is-asked-of-the-runner --strict` passes.
