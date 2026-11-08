# Design

## Context

This section records what was read on deneb on 2026-11-08, so the decisions below rest on it.

**What Flume held.** agentplot's request 362 launched `unit/pull-requests-are-queued-on-the-forge` on `bolt/sluice-runs-one-host-process`, recipient `agentplot/planner`. Its place is `/Users/chuck/.local/share/flume/places/8fbc1094d53c/change--pull-requests-are-queued-on-the-forge`. Verify found work three times, at 04:28, 04:57 and 05:05Z, and each time sent the place back to code (`send_backs` 3). The fourth verify delivered and was submitted as sluice's #24, which conflicted on seven files. Flume read the conflict at 05:27:17Z (`read_at` 1794115637). That was past the kind's bound (Flume 23, 112), so `status.rs` `waiting_on` set the place waiting on `{act: retry, stage: code, why: past_bound, since: 1794115637, words: "the submission conflicted with its base: …"}`. Its current stage was verify, delivered. The end `submission/1/conflict` was delivered to `agentplot/planner` by notice at 05:27:18Z (Flume 43).

**What crew read.** crew reads a launched place's stage from Flume's status as the place's runner carried it in `places.rec` on `<label>/runner/<host>` (`runner.stage_of`, `roles.9`). It calls no Flume command. `afterthought/crew-state`'s `agentplot/runner/deneb` carried request 362's place every minute or so:

- 147645b36bc74970dc03588644d221ba11bd9596, its record `At: 2026-11-08T05:26:37Z`: verify `begun`, `waiting_on` null, `submits` 0.
- 2cf78efa050a5db00ea37d16b05fdeb3fee79743, `At: 2026-11-08T05:27:38Z`: verify `delivered`, `waiting_on` past bound at code as above, the submission #24 in conflict.
- by 05:28:38Z: code `begun`, `waiting_on` null, after the planner's `flume retry` by hand.

The planner's `crew answer` ran at 05:27:30Z. It fetched the runner's branch (`plan.runner_tips`) and found 147645b3 at its tip. So crew read verify running and refused: "is at verify, with no question and nothing it waits on its caller for, so there is nothing to answer". The place had been waiting 13 seconds, and the runner carried the wait 8 seconds after crew's refusal.

**crew's reading of the carried wait is right.** `runner.flume_facts` on 2cf78efa's status gives phase live, current verify, state delivered, `waiting` past_bound, `waiting_stage` code, held false. `stage_of` checks `waiting_on` before the submission and the current stage. It gives `{stage: waits, of: code, why: past_bound, words: <Flume's words>, held: false, tasks: (37, 37)}`. `piece_said` says `waits` / `waits on its caller at code: the submission conflicted with its base: …`. `answer_retry` gives `("stage", "code")`. `board.flume_waits` lists it in the planner's band. deneb's installed crew (0.41.0-unstable-2026-11-07) holds the same `flume_facts`, `stage_of` and `answer_retry` as this branch. No case pins any of this. Flume's past-bound wait always names a stage, the kind's fix round (`submit.rs` `fix_round_of`). A submission the merge queue refused or withdrew waits on a retry of the submission with no stage (`Waits::Submission`), which `stage_of` reads `waits` with no `of`, and `answer_retry` answers by a retry of the submission.

**What was wrong.** Flume's notice reaches the recipient's pane at the settle that reads the end (Flume 43). The runner carries the place's status at its next pass. A standing role that acts on the notice at once asks crew while crew's reading still shows the stage running. crew then refused as though its reading were the place now: "there is nothing to answer". The planner took that as crew failing to see the wait, and went round crew. The refusal named no reading time, so nothing told the planner that crew's reading lagged Flume's notice, or that answering a minute later would work.

**README is wrong too.** Its list of a piece's stages says "`waits` with Flume's words when it waits on its caller, `stalled` past its bound". In the code, and in Flume, a place past its bound reads `waits` (`why` past_bound). `stalled` is Flume's `stalled`, a wait under no hold's words for five minutes (Flume 130).

**The family.** Flume owns whether a place waits on its caller and what move it waits for (Flume 130), and it delivers that to the recipient (43). The runner (Boomdrive) owns carrying Flume's status to crew's state repository (`roles.9`). crew owns reading the carry and the answer it appends to `requests.rec`, which the runner gives Flume as `flume retry` (`runner.ANSWERS`, `requests.rec`). Two tools deliver one fact here: Flume's notice to the role's pane, and the runner's carry to crew. They do so at different times, and only Flume's status at the moment is the truth (`roles.6`: a message is a notice naming the record, and the record is pulled). crew cannot make its reading as fresh as the notice, since it reads Flume only through the runner. So crew says how old its reading is. A retry judged by what the place waits on at the moment it is given needs the runner, which reads Flume live, or Flume itself, as Flume 49 already does for a retry naming a stop-short's key. That is Boomdrive's and Flume's to design, with the format `requests.rec` shares, and it is named under *Risks*.

**Area pages this change touches:** `plan.md` (`plugin/lib/plan.py` `answer_place`: `plan.1`, its write re-reading the stage at the tip it is applied to), `tests.md` (`tests.4`, `tests.6`, `tests.11`), `docs.md` (`docs.2`, `docs.6`), `briefs.md` (`plugin/roles/planner.md`). From `core.md`: `read.1`, `read.2`, `roles.5`, `roles.6`, `roles.9`, `code.7`, `code.8`, `code.9`. No rule changes, and no page is edited (`docs.7`).

## Goals / Non-Goals

**Goals:**

- A place Flume's status says waits on its caller to retry a stage, past its bound or not, reads waiting at that stage, whatever stage it last delivered, in `crew bolts`, the board, the planner's band and `crew answer`. One that waits on a retry of its submission reads waiting at its submission. Cases on Flume 0.17.0's own status pin both.
- `crew answer` never says a live place has nothing to answer from the runner's carry alone. It names the stage as that runner carried it, the runner's host and when it carried it, and that a wait Flume has told of since reaches crew with that runner's next carry (`read.1`).

**Non-Goals:**

- crew reading Flume's status itself (`roles.9`), or the runner carrying a place sooner. The runner's pass is Boomdrive's.
- A retry judged against the place's wait at the moment it is given, by the runner or by Flume, keyed by the end the notice named. That changes `requests.rec`'s format, which crew and Boomdrive share, and Flume's retry. The archived `crew-reads-a-waiting-place-as-flume-0-17-holds-it` left a stop-short's key out of `requests.rec` for the same reason.
- A row on the user's rail for a place that waits on a role (Decision 3).

## Decisions

### Decision 1: A wait Flume's status names reads waiting at its move, whatever stage last delivered

`stage_of` already reads Flume's `waiting_on` before the current stage and the submission. A place that waits on its caller to retry a stage reads `waits`, or `stalled` once Flume says it is stalled, at the stage `waiting_on` names. One that waits on a retry of its submission, unheld, reads `waits` with no stage. That holds whatever stage is current and whatever state it is in. It holds past the kind's bound, whose `why` is `past_bound`, and for every other `why` that names a retry. This change writes no new code for it. It pins it with two fixtures of Flume 0.17.0's status:

- `past-bound.json`, request 362's carry at 05:27:38Z;
- `submission-refused.json`, made from it as Flume 0.17.0's `status.rs` `waiting_on` gives a submission the merge queue refused: `Waits::Submission` with no stage, and the verdict `refused` with its reason.

The cases cover `stage_of` and `piece_said` (`test_runner.py`), `crew bolts`'s line (`test_bolt_commands.py`), the board's ledger and the planner's band (`test_board.py`), and `crew answer`'s retry (`test_cross.py`). That is the lowest tier that holds each (`tests.4`, `tests.11`).

*Not taken:* reading a delivered last stage, or a submission in conflict, as the place's stage when Flume says it waits. Flume's `waiting_on` is the move the place waits for (Flume 130), and the current stage is only where it stands (`read.2`).

### Decision 2: `crew answer` refuses a live place as of the runner's carry

`runner.answer_retry(work, s, carried=None)` takes `carried`, the host and the `At` of the runner's `places.rec` record that the stage was read from. `plan.answer_place` gives it from the reading of the runner that took the launch (`runner.taken`). When the place neither stopped short nor waits on its caller and its work is not over, the refusal reads:

`<work>'s place <path> was <stage> when <host>'s runner carried it, at <At>, with no question and nothing it waited on its caller for: a wait Flume has told of since reaches crew with that runner's next carry, so answer again once crew bolts shows the place waiting`

That covers queued, construct, code or verify running, sent back, and submitted. `<stage>` is `stage_said`'s words: `at verify`, `submitted to sluice (24)`, `queued for room at construct`. Where `carried` is not given, the refusal says `when its runner last carried it`, with no host or time.

A place whose work is over, merged, landed or dropped, keeps today's refusal, `is <stage>, with no question and nothing it waits on its caller for, so there is nothing to answer`. Flume refuses any retry of over work (Flume 50), so that holds whatever has happened since the carry. A launching place, one held for its After work and one the runner refused keep today's refusals: none of them was carried.

This is a decision of plain facts (`code.7`). The refusal says what crew read and when, rather than presenting an old reading as the place now (`read.1`). The answer is still appended only on a reading that says the place waits. So nothing crew appends restarts a stage that runs.

*Not taken:*

- `crew answer` waiting for the runner's next carry before it refuses. That is a wait of crew's own on a tool's state (`roles.5`, `roles.6`). It is also no bound crew holds: the runner's pass has taken over an hour (the archived change's request 88).
- Appending the retry anyway, or taking the stage from the asker, who read it in Flume's notice. A retry naming a stage of a place that does not wait on it ends the place's agent and starts that stage (Flume 49, 50). A notice crew has not read is a fact acted on blindly (`roles.6`, `read.1`).
- Saying the refusal only when the carry is older than some age. crew cannot tell how old a reading may be before Flume has moved on, and the host and time cost nothing to say every time.

### Decision 3: The planner's band lists a waiting place, and the user's rail does not

The intent's "the rail lists it" is read as the planner's band, which the intent's sources name (crew-board "The planner's and ops's bands show what places wait on them for"). The band lists each place that `answer_retry` answers, so a place past its bound is listed as soon as its wait is carried. A case pins it.

*Not taken:* a row on the user's rail. The rail is what waits on the user (crew-rail "The rail lists what waits on the user in four groups"). A place waits on its recipient, who is delivered the end (Flume 43) and has it pending (role-runs "A place that waits on a role is pending for the role"). A question the recipient cannot answer goes to the user on that role's card.

### Decision 4: The docs say what a wait reads and what a refusal names

README's list of a piece's stages says `waits` with Flume's words and the stage it waits to retry, or its submission, past the kind's bound among them, whatever stage it last delivered. It says `stalled` once Flume says the place is stalled. README's `crew answer` sentence, `plugin/skills/crew/SKILL.md`'s command row and `plugin/bin/crew`'s usage say that the refusal of a live place names its stage as the runner carried it, with the host and the time (`docs.2`). The planner's brief keeps its pinned phrase, "when the place neither stopped short nor waits on its caller" (`tests.6`). It adds that the refusal names the stage as the runner carried it, and that the planner answers again once `crew bolts` shows the place waiting.

## Risks / Trade-offs

- **An answer given on Flume's notice before the runner's next carry is refused, and given again a carry later.** On deneb that is about a minute. A runner pass that runs long holds the answer as long, and the refusal says since when. A retry judged at the moment it is given needs a change to the runner, which reads Flume live, or to Flume, as Flume 49 judges a retry naming a stop-short's key, and to the `requests.rec` format crew and Boomdrive share. That is handed to the orchestrator with this reading, for Boomdrive's and Flume's statements.
- **A planner that retries in Flume by hand goes round crew,** and `requests.rec` and the run record hold no answer. The refusal now says when to answer again through crew. The brief says the same.

## After deploy

None. Every behaviour here is a decision proven in the logic tier, and the docs are checked by `t-docs` and `t-briefs`. It reaches deneb with the crew swancloud pins there (`plan.19`), and nothing on a host needs a hand.

## Task notes

**1.1** Record `tests/py/flume-0.17.0/past-bound.json` from crew's cache of `afterthought/crew-state` on deneb. Run `git -C ~/.cache/crew/git/afterthought/crew-state.git show 2cf78efa050a5db00ea37d16b05fdeb3fee79743:places.rec | recsel -t Place -e 'Request = 362' -P Status`, and trim it as `tests/py/flume-0.17.0/README` says: each readiness step's words emptied, each task's text cut to its first 60 characters, each end's words and last words set to null, the agent's last words, instructions and environment emptied, and the host's lists and tables emptied. Keep `waiting_on` whole and the submission's verdict whole, with sluice's words. Make `submission-refused.json` from it as Flume 0.17.0's types give a submission the merge queue refused (agentplot/flume `crates/flume-core/src/status.rs` `waiting_on`; `crates/flume-seams/src/merge_queue.rs` `Verdict::Refused`). Set `submission.waiting` and `waiting_on` to `{act: retry, stage: null, why: submission, since, words}`, with the refusal's words, and set the verdict to `{"refused": {"reason": …}}`. Each serde field is as Flume serialises it. Add both to the README's list with what each holds. Cases in `tests/py/test_runner.py`:

- `test_a_place_past_its_bound_waits_on_its_caller_at_the_stage_it_waits_to_retry`: `stage_of` gives `waits` with `of` code, `why` past_bound, Flume's words, `held` false and tasks (37, 37), never verify, and `piece_said` gives `("waits", "waits on its caller at code: the submission conflicted with its base: …")`.
- `test_a_place_waiting_on_a_retry_of_its_submission_waits_at_its_submission`: `waits`, no `of`, `held` false, its line `waits on its caller at its submission: …`.

**1.2** Cases in `tests/py/test_bolt_commands.py`: `test_a_place_waiting_on_its_caller_is_on_its_line_at_what_it_waits_to_retry`, parametrized over `ran({1: "flume-0.17.0/past-bound"})` and `ran({1: "flume-0.17.0/submission-refused"})`. `crew bolts`'s line for `a` reads `waits`, with `waits on its caller at code:` or `waits on its caller at its submission:` and Flume's words. In `tests/py/test_board.py`: `test_a_place_past_its_bound_in_the_planners_band`, where the planner's view's head line counts `1 place waits on an answer` and `a`'s ledger line says `waits on its caller at code:` with Flume's words, in the Construction lane too. No change to the views file's shape or `status.js` (`code.8`).

**1.3** `plugin/lib/runner.py` `answer_retry(work, s, carried=None)`, worded as Decision 2. Its docstring says what `carried` is. `plugin/lib/plan.py` `answer_place` reads `carried` from `runner.taken(w.runners(), <the launch's number>)`'s reading: its host and its `places[<n>]["at"]`, None where it holds no record of the place. `board.flume_waits` keeps calling `answer_retry(name, s)` for its first element. Cases in `tests/py/test_cross.py` `TestAnswer`:

- `test_a_place_past_its_bound_is_retried_at_the_stage_it_waits_to_retry`: `answered("flume-0.17.0/past-bound")` appends `{Act: retry, Stage: code, Words: …}`.
- `test_a_place_waiting_on_a_retry_of_its_submission_is_submitted_again`: `answered("flume-0.17.0/submission-refused")` appends a retry with `Submission: yes` and no `Stage`.
- `test_nothing_to_answer_is_refused_as_of_the_runners_carry` (bolt-teams "Nothing to answer"): `answered("code")` is refused matching `^unit/a's place <path> was at code when deneb's runner carried it, at 2026-10-31T12:02:00Z, with no question and nothing it waited on its caller for: a wait Flume has told of since reaches crew with that runner's next carry, so answer again once crew bolts shows the place waiting$`, never `nothing to answer`. This replaces `test_nothing_to_answer_is_refused_naming_its_stage`.
- `test_a_place_further_on_is_refused_naming_where_it_is`: submitted and queued take the carried wording, and landed keeps `is merged, with no question … so there is nothing to answer`.

In `tests/py/test_runner.py`, `test_a_refusal_without_its_carry_says_when_its_runner_last_carried_it`: `answer_retry` on a code stage with no `carried` says `when its runner last carried it`.

**1.4** `README.md`: the stage list's `waits` and `stalled` (the paragraph beginning "A unit, chore or fix of a bolt marked `Path: flume` reads its stage"), and the `crew answer` sentence. `plugin/skills/crew/SKILL.md`'s `crew answer` row. `plugin/bin/crew`'s usage lines for `crew answer`. Each says Decision 4's words (`docs.2`).

**1.5** `plugin/roles/planner.md`, the bullet "**Its places' questions are yours.**". After "when the place neither stopped short nor waits on its caller", which `tests/t-briefs.sh` pins and which stays, add: as its runner last carried it, naming the host and when, so a wait Flume told you of since is answered again once `crew bolts` shows the place waiting. Pin the added phrase in `tests/t-briefs.sh` beside the existing one (`tests.6`).
