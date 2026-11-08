# Verify: a-repository-is-renamed-by-one-explicit-command

Read on 2026-11-07, on `change/a-repository-is-renamed-by-one-explicit-command` at f5bb06b1, which holds `bolt/crew-reads-a-kit-by-its-name-alone` at 6fbd8e71 (`no-reader-maps-a-kits-former-name` landed on it) by the merge 7cd5e353.

**Verdict: the work holds.** The whole checks pass, every task is done, and every requirement and scenario of the four spec deltas is met by code and proved by a check.

## The whole checks

`tests/suite --affected` was run once from the worktree's root, as CLAUDE.md names it for a finished change. It took every `check-full` task whose inputs differ from the merge-base with main.

```
ok    contract
ok    logic
ok    t-briefs   (replayed)
ok    t-cards
ok    t-docs   (replayed)
ok    t-flume-source
ok    t-help   (replayed)
ok    t-hold
ok    t-journey-board
ok    t-journey-cross
ok    t-journey-land
ok    t-journey-main
ok    t-journey-main-fix
ok    t-journey-ops
ok    t-journey-plan
ok    t-journey-review
ok    t-journey-roles
ok    t-journey-signals
ok    t-journey-state
ok    t-roles
ok    t-runner
ok    t-session-hook
ok    t-slot
ok    t-sluice
ok    t-stage-facts
ok    t-suite
ok    t-teams
ok    t-waits
28 passed (3 replayed), 0 failed
```

It exited 0. The three replayed tests (`t-briefs`, `t-docs`, `t-help`) replay runs on identical inputs that passed on this host; sluice runs every test afresh at the merge. Neither `mod` nor the flake's tasks were affected, since the change leaves `plugin/hooks/status.js` and the flake as they were (`code.8`: the views keep their shape). `openspec validate a-repository-is-renamed-by-one-explicit-command --strict` reports the change valid.

## Tasks

All 15 tasks in `tasks.md` are ticked, 1.1 to 5.1. Each one's check exists under the name it gives:

- the classes of `tests/py/test_repository_rename.py`, in the logic tier;
- `tests/py/test_kit_rename.py`;
- `tests/py/test_proposal_card.py::test_a_rename_is_a_block_naming_both_names_and_no_bolt`;
- `tests/contract/test_recfix.py::test_a_rename_is_one_commit_whose_files_pass_recfix_and_its_entry_names_both_names`, in the contract tier;
- `t-journey-plan`, `t-docs`, `t-briefs` and `t-help`.

Each passed in the run above. No task adds or removes an end-to-end test, and `tests/moon.yml` is unchanged.

Task 5.1, the bolt taken in, holds as it says:

- No reader through `kit.rename` entries is left in `plugin/` or `tests/`: no `kit_now`, `Write.renamed`, `renames_in`, `renames_at`, `launches_now`, `kit_given`, `former_said`, `former_kept_said` or `renamed_kept`.
- `test_kit_rename.py`'s `TestAKitAsGiven` reads a kit as given over an earlier rename's plan.
- The contract rename case checks the entry's day file with a real `recfix --check`.
- Every requirement the deltas modify or remove stands in the bolt's specs by its name, and the one they add, "A partition is never renamed", does not, so the archive applies onto them.

## Requirements against the code

### bolt-plan

| Requirement | Where it is built | Proved by |
|---|---|---|
| A repository is renamed by one explicit command | `op_kit_rename`: one write, one `kit.rename` entry, no request appended, `return []` launching nothing. A proposal applies it through `OPS`. Who may run it is still `may_write`'s. | `TestTheCommand`; `tests/py/test_plan_roles.py`; `t-journey-plan` (the user's run, the planner's refused run naming `crew plan propose`, and a proposal's approval with `From` naming `proposal/<n>`) |
| A rename waits until the repository's work is finished | `rename_standing`: bolts, the queue, fixes of main and roles' work by `runner.piece_stage`, live or making places, open or lost cards under `land/<old>` and `record/<old>/<n>[/<commit>]`, unanswered unsettled batches, open proposals other than `own` (`proposal_names`). `rename_refusal` step 3 names them all in one message. | `TestWhatStands`, one case per scenario; `TestRefused.test_work_standing_both_named_in_one_message`; `TestTheCommand.test_a_started_bolt_refuses_naming_it_with_the_write_as_it_was` |
| A rename waits until no host keeps the old name | `rename_kept` takes the runner's `repositories.rec` where it is reported, and otherwise the host's spaces. An unreadable runner, or a host that neither reports nor is listed, is unread. `op_kit_rename` reads the runner hosts together with the main-level host and requires none to keep `<new>`. | `TestWhatAHostKeeps`; `TestRefused.test_a_host_keeping_it`, `test_unread_keeping`; `TestTheCommand.test_a_host_keeping_the_old_name_refuses`, and the direct run with no host keeping either name |
| A rename takes only a name some record holds, and a new name of its own | `rename_refusal` steps 1 and 2 run before anything is renamed. Step 5 (count 0) runs after `rename_branch`. | `TestRefused.test_one_repository`, `test_a_bolts_name`, `test_no_record_naming_it`; `TestWhatTheRenameRenames.test_a_name_no_record_holds_renames_nothing_and_records_no_rename` |
| A rename renames every record a reader matches the repository by | `rename_branch` with `RENAMED_FIELDS`: plan Sources, `requests.rec` `Repo` and `Work`, and the runs files' `Repo`, `On` and `From`. `renamed_kit` keeps an address's owner. `renamed_object` covers `kit/`, `land/`, `queue/`, `record/<repo>/<n>` and `fix/main/<repo>/<name>`. | `TestWhatAFieldBecomes`; `TestWhatTheRenameRenames.test_flywheel_cloud_renamed_boomdrive_cloud_across_madswans_records`; the contract case through real git and recfix |
| A rename leaves what no reader looks a repository up from | `rename_rec` skips descriptor and comment blocks and every `kit.rename` entry, renames only the named fields, and returns a text naming no old name byte for byte. `rename_branch` touches no file but those three kinds, and replaces only a file whose records changed. | `TestWhatAFieldBecomes.test_a_key_and_any_other_field_is_as_it_was`, `test_a_kit_rename_entry_is_left_whole`, `test_a_text_naming_no_old_name_is_returned_byte_for_byte`; `TestWhatTheRenameRenames.test_only_the_files_it_changed_are_replaced` |
| A rename run again renames what an earlier one left | No refusal of a name an earlier rename renamed. `prepare` runs `record.reach(label)` before the write reads the branch, for a direct run and an approval alike, and a refused push refuses the command. | `TestRunAgain`; `TestTheCommand.test_prepare_pushes_this_hosts_kept_entries_before_the_change` |
| REMOVED: A kit renamed on its host is renamed across the plan in one act | Gone, with its spaces check for `<new>` and its rename of Bolt and Unit `Repo`. | logic tier; `t-journey-plan` |
| REMOVED: requests.rec and the run record are only appended to | Its rule and one exception stand in drive-state's and run-record's requirements as this delta modifies them; `appended` allows the rename alone. | `TestAppendOnly`; the contract case |

### drive-state

| Requirement | Where it is built | Proved by |
|---|---|---|
| crew asks a host's runner for work by requests on the drive's branch (modified) | `appended` reads the tip's `requests.rec` through each rename on the write (`appended_refusal(was, now, w.renaming)`), so only a rename's write may change a request, and only its repository's name. | `TestAppendOnly`: a rename's write passes; the same change with no rename is refused; a rename that also changes `Name` is refused; an append beside a rename passes |
| A partition is never renamed (added) | No command renames a label. `crew.partition_of` refuses a former label, naming the partitions. `state_of` gives a new label its own branch. | `TestAPartitionIsNeverRenamed` |

### plan-proposals

| Requirement | Where it is built | Proved by |
|---|---|---|
| A proposal's card draws a kit's rename (modified) | `cards.renamed_drawn` draws a block naming both names, saying the work is finished and what is renamed. It names no bolt or unit and returns no section, and the card stays a plain approval. A card of renames alone is titled by the repositories it renames. | `test_a_rename_is_a_block_naming_both_names_and_no_bolt`; `t-journey-plan` (the card drawing the block) |

### run-record

| Requirement | Where it is built | Proved by |
|---|---|---|
| The run record is files on the host, appended and never rewritten (modified) | Only `rename_branch` rewrites the branch's copy, in the rename's one commit. Each host's own files are never touched. | contract case (the parent holds each file as it was); `t-journey-plan` (the host's own runs file still names the old name) |
| A kit's rename is one entry naming both its names (modified) | `Op(..., "kit.rename", on=[kit/<new>], frm=[kit/<old>], fields={Repo, Count})`, where `Count` is every record renamed. An approval emits `proposal/<n>` beside `kit/<old>` in its `From`. No reader maps a name through the entry: `landings_at` and `kits_at` read every record as written. | `TestTheCommand.test_a_direct_run_over_finished_work_renames_and_fills_repo_and_count`; `TestRunAgain.test_a_later_rename_leaves_the_earlier_entry_whole`; `tests/py/test_kits.py::TestRunsRead::test_a_renames_entry_renames_nothing`; contract case (the entry is the commit after, `Count: 3`, its day file passing `recfix --check`) |

## Docs and briefs

- README, `plugin/skills/crew/SKILL.md` and `plugin/bin/crew`'s usage header all say the same things (`docs.2`, `t-docs`):
  - the order around the rename;
  - what stands and refuses it;
  - where a host's keeping is read;
  - what is renamed and what is left;
  - that running it again mends what an earlier rename left;
  - that no command renames a partition;
  - that every record is read as written.
- The planner's brief has the table row "rename a repository once its work is finished" and the paragraph "A repository renamed on its forge", pinned by `t-briefs` (`tests.6`).
- No page under `docs/architecture/` or `docs/adr/` is edited (`docs.7`).

## Notes, none blocking

- Words that name `crew kit rename` as the way on for a kit a host keeps none of (`main_kit_said`, `runner.kept_folder`, and their cases in `test_bolt_commands.py`, `test_kits.py` and `test_cross.py`) still say "names it so in the plan". The design's Non-Goals leave them out of this change.
- Read after the archive: `openspec validate <spec> --type spec --strict` warns that a requirement's text runs over 500 characters, and strict mode fails on that warning. This change takes three requirements over the limit: drive-state's "crew asks a host's runner for work by requests on the drive's branch" (600), plan-proposals' "A proposal's card draws a kit's rename" (514) and run-record's "The run record is files on the host, appended and never rewritten" (534). run-record's "A kit's rename is one entry naming both its names" was already over (600, now 881). All four touched specs already had other requirements over the limit at 6fbd8e71. No check of the repository's runs that validation; the change's own `openspec validate --strict` passes.
- After deploy, the user renames madswan's `flywheel-cloud` and `tailrace` on deneb, as the design's *After deploy* says. No check can do that step.
