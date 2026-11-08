# Verify: a-place-waiting-on-its-caller-reads-waiting

Read 2026-11-08 on deneb, at `e3a46db7` on `change/a-place-waiting-on-its-caller-reads-waiting`. The branch holds #7's landing, `479648d0`, through the merge `08d86b0b`, and `origin/bolt/crew-reads-each-piece-as-the-tools-hold-it` stands at `479648d0`, the branch's merge-base, so the branch merges onto its bolt with nothing between.

**Outcome: archived.** All 6 tasks are ticked. The whole checks pass. Each requirement and scenario of the three deltas, `bolt-plan`, `bolt-teams` and `crew-board`, is met by the code and proved by a case. #7's spec changes are requirements of their own in `bolt-plan`, so this change's MODIFIED requirements replace none of them. Nothing fails.

## Checks

| Check | Result |
|---|---|
| `openspec validate a-place-waiting-on-its-caller-reads-waiting --strict` | Valid |
| `tests/suite --affected`, run once | 28 passed (2 replayed), 0 failed: `contract`, `logic` (replayed), `t-briefs`, `t-cards`, `t-docs` (replayed), `t-flume-source`, `t-help`, `t-hold`, `t-journey-board`, `-cross`, `-land`, `-main`, `-main-fix`, `-ops`, `-plan`, `-review`, `-roles`, `-signals`, `-state`, `t-roles`, `t-runner`, `t-session-hook`, `t-slot`, `t-sluice`, `t-stage-facts`, `t-suite`, `t-teams`, `t-waits` |

The whole checks are `tests/suite --affected`, as crew's CLAUDE.md names them for a change that is done, since nobody runs the whole suite by hand. The change edits `plugin/lib/runner.py` and `plan.py`, which belong to the command core every task takes, so every test task was affected and ran. `logic` and `t-docs` were replayed from a passing run on identical inputs, task 2.3's run of `tests/suite t-docs logic` on this tree (`tests.10`). `mod` and the `nix` project were not affected: `plugin/hooks/status.js`, `plugin/tests/` and the flake are untouched, as `code.8` allows when the views keep their shape. `tests/suite` ran, so `tests/moon.yml` is in step with the tests. No test was added or removed.

## Tasks

| Task | Read |
|---|---|
| 1.1 | `tests/py/flume-0.17.0/past-bound.json` holds request 362's place: its current stage verify delivered, `waiting_on {act: retry, stage: code, why: past_bound}`, and submission #24 in conflict. `submission-refused.json` is made from it, with `waiting_on` naming no stage, `why: submission`, and the verdict `{refused: {reason}}`. The folder's README lists both and says what each holds. In `test_runner.py`, `test_a_place_past_its_bound_waits_on_its_caller_at_the_stage_it_waits_to_retry` gets `{stage: waits, of: code, why: past_bound, held: False, tasks: (37, 37)}` from `stage_of`, and `piece_said` gives `waits on its caller at code: …`. `test_a_place_waiting_on_a_retry_of_its_submission_waits_at_its_submission` gets `waits` with `of: None` and the line `waits on its caller at its submission: …`. Neither case reads verify. |
| 1.2 | `test_bolt_commands.py` `test_a_place_waiting_on_its_caller_is_on_its_line_at_what_it_waits_to_retry` is parametrized over both fixtures. `crew bolts`'s line for `a` reads `waits` with Flume's words, at code or at its submission, never verify. `test_board.py` `test_a_place_past_its_bound_in_the_planners_band` checks that madswan-planner's head line ends with `1 place waits on an answer`, that `a`'s band line reads `◑  a  waits  waits on its caller at code: …`, that the Construction lane of the ledger has the same line, and that none of `a`'s lines say verify. |
| 1.3 | `runner.answer_retry(work, s, carried=None)` keeps the retries as they were. For merged, landed, dropped, waiting (held for its After work) and refused, it keeps the refusal "nothing to answer". Any other live stage is refused as `<place> was <stage> when <host>'s runner carried it, at <At>, …: a wait Flume has told of since reaches crew with that runner's next carry, so answer again once crew bolts shows the place waiting`. With no carry, it says `when its runner last carried it`. Launching and unknown are refused before that, naming what crew could not read. `plan.answer_place` gives `carried` from `runner.taken`'s reading: its `host` and `places[n]["at"]`, or None where the reading holds no record of the place. In `TestAnswer`, the past-bound case appends `Stage: code`, and the submission case appends `Submission: yes` with no `Stage`. `test_nothing_to_answer_is_refused_as_of_the_runners_carry` matches the whole refusal, with deneb and `2026-10-31T12:02:00Z`, and asserts that "nothing to answer" is absent. The further-on case gives submitted and queued the carried wording and landed the merged refusal. The docstring of `answer_retry` says what `carried` is. |
| 2.1 | README's stage list says `waits` covers the stage it waits to retry or its submission, past the kind's bound among them, whatever stage last delivered, and that `stalled` comes once Flume says the place is stalled. Its `crew answer` sentence names the live place's stage as the runner carried it, with the host and the time, and says it is answered again once `crew bolts` shows it waiting. `plugin/skills/crew/SKILL.md`'s row and `plugin/bin/crew`'s usage lines say the same. `t-docs` passes. |
| 2.2 | `plugin/roles/planner.md` keeps "when the place neither stopped short nor waits on its caller" and adds "as its runner last carried it, naming the host and when, so a wait Flume told you of since is answered again once `{{TEAM_CMD}} bolts` shows the place waiting". `tests/t-briefs.sh` pins the added phrase beside the kept one. `t-briefs` passes. |
| 2.3 | `08d86b0b` merges `479648d0`, #7's landing on the bolt. README's paragraph on a `Path: flume` piece's stage keeps #7's words, a fix's `fix/<bolt>--<name>` in a landing's `Sluice-From` read merged, only from a landing made at or after its launch, and this change's `waits` at the stage a place waits to retry, with `stalled` as Flume's stalled. `84b9accd` moved the change out of the archive and took its deltas back out of `openspec/specs`, so `openspec/specs` stands as the bolt has it and this archive syncs the deltas onto #7's specs. `openspec validate --strict` passes, and so do `t-docs` and `logic`. |

## The deltas

Each MODIFIED requirement keeps every scenario of the requirement it replaces in `openspec/specs`. It adds the scenarios below and rewords the requirement's text to say them. In `bolt-teams`, "Nothing to answer" is rewritten to the refusal as of the carry, and "Work that is over" is added for the refusal that keeps "nothing to answer". The requirements #7 added to `bolt-plan`, "A fix whose place's landing its bolt's branch holds is merged" and "A fix read merged from its bolt's landing holds nothing", are untouched by this change.

### `bolt-plan` (MODIFIED): A launched place's stage is where Flume's status has it

- "A place past its bound": `test_a_place_past_its_bound_waits_on_its_caller_at_the_stage_it_waits_to_retry` (`stage_of`), the parametrized `crew bolts` case, and `test_a_place_past_its_bound_in_the_planners_band`, which covers the ledger and the band.
- "A submission that waits on its retry": `test_a_place_waiting_on_a_retry_of_its_submission_waits_at_its_submission` and the parametrized `crew bolts` case.
- The scenarios carried unchanged, "A unit in code", "A construct that asked", "A stop-short whose agent is kept open", "Sent back by sluice" and "Landed on the bolt", keep their existing cases, all in `logic`, which passes.

### `bolt-teams` (MODIFIED): A place is answered by a retry

- "A place past its bound": `test_a_place_past_its_bound_is_retried_at_the_stage_it_waits_to_retry`.
- "A submission that waits on its retry": `test_a_place_waiting_on_a_retry_of_its_submission_is_submitted_again`.
- "Nothing to answer": `test_nothing_to_answer_is_refused_as_of_the_runners_carry`. With no carry, `test_a_refusal_without_its_carry_says_when_its_runner_last_carried_it` covers it.
- "A place the runner has not carried": `test_a_launch_the_runner_holds_with_no_after_is_not_held_for_after_work_and_crew_cant_tell_its_question` and the launching refusals in `test_cross.py`.
- "Work that is over": the landed half of `test_a_place_further_on_is_refused_naming_where_it_is`.
- "A construct that asked" and "A stop-short whose agent is kept open" keep their existing cases.
- The requirement's "never say that a live place has nothing to answer" holds in code. Only over work, After-held work and runner-refused work keep that wording, and none of those is a carried live place.

### `crew-board` (MODIFIED): The planner's and ops's bands show what places wait on them for

- "A place past its bound in the planner's band": `test_a_place_past_its_bound_in_the_planners_band`. The mod draws the band from keys whose shape did not change, so `plugin/hooks/status.js` and its cases stand (`code.8`).
- "A question in the planner's band" and "A fix of main in ops's band" keep their existing cases.

## Rules

- **`code.7`**: `answer_retry` stays a function of plain facts, the stage and the carry. The read stays in `answer_place`.
- **`read.1`**: the refusal says what crew read and when, and appends nothing on a reading that does not say the place waits.
- **`roles.5` and `roles.6`**: crew adds no wait of its own on the runner's next carry.
- **`code.8`**: the views file's shape is unchanged, and so is `status.js`.
- **`docs.2`**: README, the skill and the usage say the same words.
