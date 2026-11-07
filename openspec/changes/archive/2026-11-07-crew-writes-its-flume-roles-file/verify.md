# Verify: crew-writes-its-flume-roles-file

Read 2026-11-07 on deneb, at `cc1526ed` on `change/crew-writes-its-flume-roles-file`, cut from `teamless/deneb` at `9cceaca3`.

**Outcome: archived.** All 6 tasks are ticked, and every check they name passes. Each requirement and scenario of the `flume-source` delta is met by the code and proved by a case. `teamless/deneb` has since moved to `2128e612` (#462 and #463). The branch merges onto it cleanly (`git merge-tree`), so sluice's submission meets no conflict. Nothing fails.

## Checks

| Check | Result |
|---|---|
| `openspec validate crew-writes-its-flume-roles-file --strict` | Valid |
| `tests/suite --force logic t-briefs t-flume-source t-journey-main t-docs` | 5 passed (0 replayed), 0 failed |
| `tests/suite --affected` | 28 passed, 0 failed: `contract`, `logic`, `mod`, `t-briefs`, `t-cards`, `t-docs`, `t-flume-source`, `t-help`, `t-hold`, `t-journey-board`, `-cross`, `-land`, `-main`, `-main-fix`, `-ops`, `-plan`, `-review`, `-roles`, `-signals`, `-state`, `t-roles`, `t-runner`, `t-session-hook`, `t-slot`, `t-sluice`, `t-stage-facts`, `t-suite`, `t-teams` |

`--affected` replayed every test from the code stage's passing run on identical inputs (`tests.10`). The five tests the tasks name were run again here with `--force`, so none of them rests on a replay. `tests/suite` ran, so `tests/moon.yml` is in step with the tests, `t-flume-source` among them.

## Tasks

| Task | Read |
|---|---|
| 1.1 | `plugin/lib/source.py` imports only `json`, `os` and `pathlib`, and nothing of crew's (`code.1`). `entries(fleet, host, asks)` walks the partitions in the teams file's order and `ROLES` in `KIND_ROLES` order. It skips a partition whose `machine` is not the host and a role whose `flume` is not `False`. Each entry gives `agent = "<label>-<role>"` and `session = p["sessions"][role]`. It adds `answers` from `asks` where the role has words, and `answerer = true` for the operator. `text` gives the comment header and one `[roles."<address>"]` table per entry, with no clock in it. `tests/py/test_source.py` covers every scenario of the first five requirements on deneb's fleet, built through `crew.load`, and reads the text back with `tomllib`. |
| 1.2 | `crew.ASKS` holds design "the design", planner "the plan" and ops "a live system, a deploy or a landing". `cards_how` builds its sentence from it in the order design, ops, planner. `test_the_briefs_sentence_on_whom_to_ask_gives_the_same_words` pins the sentence. `t-briefs` expects the new words for wldn and passes. |
| 2.1 | `source.keep` makes nothing when there is no entry and no file. Otherwise it compares the text with the file's bytes, writes `roles.toml.<pid>.tmp` beside the file and `os.replace`s it over. When there is an entry it makes `KINDS_DIR`, and it returns whether it wrote. `crew.keep_roles` calls it with `this_host()` and `ASKS`, and reports an `OSError` on standard error, naming the file. `Follower.fleet` calls `keep_roles` after a load inside its `try`, so a `Refusal` from `crew.load` reaches no write (`read.1`). `t-flume-source` proves the rest: the ten entries on mac-studio, the empty kinds folder, the teams file left alone and no `flume` call; the second run with the same inode and mtime; the rename-over with the hard link holding the old text; the version-4 refusal naming the teams file with the roles file unchanged; and the box with no file made, then wldn's five entries, then a file with no entry. |
| 2.2 | `Agents.start` calls `keep_roles(self.fleet)` once a role's agent is up, when `self.kind == "main"`. That covers `crew main up`, `restart`, `resume` and `revive`, and leaves out the console and the `retired` operator. `t-journey-main` reads the box's roles file after `crew main up wldn` and finds `wldn/design wldn/planner wldn/reviewer wldn/ops wldn/operator`. |
| 3.1 | README's "The main level and the console" gains the paragraph Task notes 3.1 asks for. No command changes, so the usage header and the skill gain no line (`docs.2`). `t-docs` passes. |
| 3.2 | As *Checks* above. |

## The delta: `flume-source` (ADDED)

- **Each standing main-level role is declared at its address as its agent.**
  - "deneb's three partitions" (fifteen entries, `agentplot-planner`, `madswan-ops`): `test_deneb_holds_five_entries_for_each_of_its_three_partitions`.
- **An entry names the session crew opens its agent in.**
  - "Sessions of the partitions' names": `test_sessions_of_the_partitions_names`.
  - "A role with a session of its own" (`wldn-1` for the planner and the reviewer, `wldn-2` for the rest): `test_a_role_with_a_session_of_its_own_and_the_reviewer_beside_the_planner`. The sessions come from `p["sessions"]`, which `crew.load` already gives (record 0035).
- **What a role answers is the words crew's briefs give for whom to ask.**
  - "The words in the file and in the brief": `test_the_design_agent_the_planner_and_ops_answer_their_words` and `test_the_briefs_sentence_on_whom_to_ask_gives_the_same_words`. Both read `ASKS`, the one text, and `t-briefs` checks the built brief.
  - "The door and the reviewer": `test_the_operator_is_the_door_and_the_reviewer_answers_nothing`, which compares whole entries, so no other key slips in.
- **An entry gives a standing agent's keys alone.**
  - "Read as Flume reads it": `test_read_as_flume_reads_it`, on deneb and on the box. A file with no entry gives no `roles` key, which TOML reads as `{}` and Flume as declaring nothing (`test_a_host_that_is_no_partitions_machine_declares_nothing`).
- **No entry for a partition on another host or a role that runs as its kind.**
  - "wldn on deneb": `test_wldn_on_deneb`, and again end to end on mac-studio.
  - "A planner that runs as its kind": `test_a_planner_that_runs_as_its_kind`.
- **The file is written whole and renamed over the old one, only when it differs.**
  - "Nothing moved": `t-flume-source`, by inode and mtime.
  - "Renamed over": `t-flume-source`, with the hard link and `madswan-2`.
- **The follower and a main-level start keep the file.**
  - "The follower's first read": `t-flume-source`, whose `flume` shim logs and fails, so a call would show in the log.
  - "A main level started": `t-journey-main`.
- **A host with no main level declares nothing.**
  - "A main level moved away": `t-flume-source` on the box, in both orders.
- **A teams file crew refuses leaves the file as it is.**
  - "A teams file at another version": `t-flume-source`. `expect_fail` matches the teams file's path in the refusal.
- **crew's kinds folder exists and holds nothing yet.**
  - "The folder beside the file": `t-flume-source`. `plugin/flume/kinds.toml` is untouched.

## Rules

- **`code.1`**: `source.py` imports only the standard library. `crew.py` imports `source`, and `tests/moon-tasks` adds it to the core every task takes (`tests.10`).
- **`code.7`**: the entries and their text are functions of the fleet, the host and `ASKS`. `keep` is the one act.
- **`code.5`**: the teams file is read only, which `t-flume-source` checks byte for byte.
- **`code.8`**: not reached, since nothing crew models changes.
- **`read.1`**: covered by the refusal case.
- **`teams.9`**: covered by the rename-over.
- **`roles.5`**: crew runs no `flume` command and builds no delivery.
- **`teams.25`** is as record 0057 has it. Its mark "not built: `crew-writes-its-flume-roles-file` builds it" stays as written. By `docs.7`, the design agent lifts a rule's not-built clause after the landing, reading main's log, and no stage of the change does.

## After deploy

The design's one step: swancloud-ops reads `flume status` on deneb once swancloud's deploy brings Flume 0.17.0, `sources/crew.toml` and crew's pin at this change. It stays outside crew's tiers for the reason the design gives, and it is no task.
