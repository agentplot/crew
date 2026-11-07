# Design

## Context

This section records what was read on 2026-11-07 on deneb, so the decisions below rest on it.

**What crew read at 20:13Z.** crew reads a crossed piece's stage from its launch, the answer of the runner that took it, and Flume's status of its place as that runner carried it in `places.rec` (`runner.stage_of`). It reads no Flume status itself. crew's cache of `afterthought/crew-state` shows `afterthought/runner/deneb`:

- e2fb96c7, committed at 19:40:45Z ("claims 88"), added one answer to request 88, the launch of `unit/every-fleet-mac-joins-the-tailnet-as-a-host` on `bolt/a-fleet-hosts-tailnet-key-never-expires`: `Outcome: held`, `Words: claimed by deneb's runner; launching once no other runner has claimed it`.
- The next write, 6fe719c0, came at 20:50:14Z ("answers 88 89 90 91 92 93"). It changed `answers.rec` alone: request 88 `launched` at `/Users/chuck/.local/share/flume/places/fb2dbfb942ae/change--every-fleet-mac-joins-the-tailnet-as-a-host`, `At: 19:42:17Z`.
- `places.rec` holds no record of request 88 at e2fb96c7, at 6fe719c0, or at any write since. The runner's log (`~/Library/Logs/swancloud-boomdrive.log`) shows one pass that claimed 88, launched it, then took agentplot's launches 310 to 398, and wrote both partitions' answers at its end. It wrote no `places` for afterthought after that pass.

So at 20:13Z crew held only the claim. `stage_of` read `Outcome: held` as waiting on After work, whatever the launch's `After`. `answer_retry` refused "held for its After work, with no question". `runner.where` found deneb's runner had taken the work, but no carried status named the kit's folder, and that runner writes no `repositories.rec`. So `launched_at` refused, `Stages.at` gave nothing, and `crew bolts` printed "where it runs can't be told".

**What `held` means from Boomdrive.** Boomdrive's crew implementation answers a launch `held` in three cases (agentplot/boomdrive at 3f428cf: `crates/boomdrive/src/carry.rs` `offer`; `crates/boomdrive-crew/src/write.rs` `claim_words`; its crew-control-plane spec, Decision 18, and work-into-flume spec):

- its claim, before it gives the launch to its host, with the words above;
- an offer whose `after` names a launch whose place has not landed, its words naming each;
- an offer already answered whose stream has no room, with the room's words.

A launch with no `After` is held only for a claim or for room. Neither is After work.

**Flume 0.17's status of a stop-short whose agent is kept open.** Read from flume 0.17.0 (`crates/flume-seams/src/held.rs` `WaitingOn`, `crates/flume-core/src/status.rs`, `crates/flume-core/src/answer.rs` `EndStatus`) and a live place on deneb at 22:20Z, `change--the-flake-configures-each-tool-by-its-own-module`:

- `phase` is `live`, and the current stage's state is `ended_short`, its `end.needs` `needs_answer`.
- `waiting_on` is `{act: retry, stage: code, why: answer, since, words, open_until}`, and the agent's state is `waiting`.
- `ends` holds the stop-short under the key `stage/code/1/ended-short`, with its `open_until`.

`runner.flume_facts` reads every field it needs from this as it did from 0.3.6: phase, current stage, state, end, tasks, `waiting_on.why`, `stage` and `words`, and `stalled`. So `stage_of` reads needs at code, and `answer_retry` gives the retry of code. Flume's statement makes that retry the answer: "a retry with words naming a stage whose agent is kept open for its answer (198) is that answer, which reaches that session as 42 says and starts no agent" (clause 49). A tell answering it does the same (53). Nothing of 0.17's status was misread. The fixture `tests/py/flume-0.17.0/kept-open.json` pins it.

**The family.** The format of `answers.rec` is crew's (`runner.ANSWERS`). Boomdrive writes it field for field (`roles.9`; boomdrive core.2). Boomdrive's claim, from its Decision 18, reuses `held`, and nothing in crew read it as anything but After work. Flume owns a place's stages and how an answer reaches a kept-open agent (`roles.5`). The runner owns carrying Flume's status to crew. crew owns reading both. The reconciliation is crew reading `held` as the runner means it: held for After work only where After work exists. The runner carrying no status of a launched place for over an hour is the runner's to mend, not crew's to work around. It is named under *Risks* and handed to the orchestrator.

**Area pages this change touches:** `plan.md` (`plugin/lib/plan.py`: `plan.6`, `plan.11`, a piece's stage read from the runner's records), `tests.md` (`tests.4`, `tests.11`), `docs.md` (`docs.2`, `docs.4`, `docs.6`). From `core.md`: `read.1`, `read.2`, `roles.5`, `roles.9`, `code.7`, `code.8`. No rule changes, so no page is edited (`docs.7`).

## Goals / Non-Goals

**Goals:**

- A launch with no `After` is never read as held for After work (`read.2`).
- `crew answer` answers a stop-short whose agent Flume keeps open, refused for nothing, and says what it could not read rather than guessing when the runner has not carried the place (`read.1`).
- A bolt's head line names the host whose runner took its work, never "where it runs can't be told" for taken work.

**Non-Goals:**

- crew reading `flume status` itself. A place's status reaches crew through its runner (`roles.9`), and crew calls no Flume command.
- A stop-short's key carried by a request, so the runner can pass `--answers`. requests.rec has no such field, and Boomdrive gives a retry as its `Stage` and `Words`. That is a change to the format both tools share.
- How `crew bolts` reads a unit already landed on its bolt (`a-unit-whose-work-its-bolt-holds-is-built`), or a bolt landed through Flume's base place (`crew-lands-a-bolt-through-flumes-base-place`).

## Decisions

### Decision 1: `held` reads waiting only for a launch whose `After` names work

`stage_of` reads `Outcome: held` as waiting on its After work only when the launch's `After` names some. Otherwise it reads launching, carrying the answer's `Words` where it has them. `piece_said` gives a launching piece with words the detail `held by the runner: <words>`, so `crew bolts`, the board and each band say why the runner holds it. A launch with `After` keeps its reading: the runner's words for it name the work it waits on.

*Not taken:* telling the claim apart by its words, as Boomdrive's `is_claim` does. That reads one tool's prose as a fact (`read.2`). The `After` crew wrote is crew's own fact. *Not taken:* a distinct outcome for a claim, `claimed`. It is a change to `answers.rec`'s format, so to crew's descriptor and Boomdrive's writer together. It would also not cover the room case.

### Decision 2: `crew answer` refuses a launching place by what it could not read

`answer_retry` refuses a launching piece saying crew can't tell whether its place waits on an answer, and why:

- the runner that took it has carried none of Flume's status of its place yet, where an answer names the place;
- the runner holds its launch, with its words;
- no runner has answered its launch yet.

It used to say "is launching, with no question and nothing it waits on its caller for, so there is nothing to answer". That is a guess: crew held no reading of the place.

A place the runner has carried that waits on an answer, its agent kept open or not, reads needs. It takes `crew answer` as before.

*Not taken:* appending the retry anyway and letting Flume judge it. With no stage read, crew can't name the stage, and a retry naming the current stage of a place that does not wait would start it again (Flume 49, 50).

### Decision 3: `Stages.host` names the runner's host before the kit's folder is known

`Stages.host(bolt)` gives the machine `Stages.at` reads where it reads one. Otherwise it gives the host `runner.where` names for the bolt's newest launch taken, which needs no folder. It gives none where no runner took it, two did, or the runner that did keeps no repository by the kit's name. `crew bolts`, the board's ledger and the page's bolt node take their host from it. Every decision that acts in the kit, such as landing, the kit's reads, sites and sessions, still goes through `bolt_at`. They keep refusing while the folder can't be told (`read.1`).

*Not taken:* a folder from the place's own path. Flume's places folder is named by a hash of the repository's location, not by the location (`fb2dbfb942ae`), so it names no folder.

## Risks / Trade-offs

- **A launch with `After` that the runner holds for a claim or for room reads waiting on its After work, even once that work has landed.** That is as before, and short: Boomdrive's next pass answers it.
- **A runner that never carries a launched place's status** leaves the piece launching and `crew answer` refused, naming why. Request 88 shows it. Boomdrive's pass that launched it took 68 minutes, and no write since carried its place. That is Boomdrive's, handed to the orchestrator with this reading.

## After deploy

None. Every behaviour here is a decision proven in the logic tier. It reaches deneb with the crew swancloud pins there (`plan.19`), and nothing on a host needs a hand.

## Task notes

**1.1** `plugin/lib/runner.py` `stage_of`: `held` with no `After` on the launch reads `{"stage": "launching", "words": <Words>}`, with `words` only where given. `piece_said`: a launching piece with words has the detail `held by the runner: <first line>`. Cases: `tests/py/test_runner.py` `test_a_launch_with_no_after_the_runner_holds_is_launching_with_its_words_and_never_held_for_after_work`, with the existing `test_held_for_its_after_work_it_is_waiting_on_that_work`.

**1.2** `runner.answer_retry`: a launching piece refuses with `can't tell whether <work>'s place[ <place>] waits on an answer: ` and one of the three reasons in Decision 2. Cases: `tests/py/test_cross.py` `TestAnswer.test_a_launch_the_runner_holds_with_no_after_is_not_held_for_after_work_and_crew_cant_tell_its_question` and `test_a_stop_short_whose_agent_flume_0_17_keeps_open_takes_the_answer`. `tests/py/test_runner.py` `test_a_stop_short_whose_agent_flume_0_17_keeps_open_needs_its_answer` reads `tests/py/flume-0.17.0/kept-open.json`, recorded and trimmed as its README says. `tests/py/facts.py` `ran` takes a fixture named with its folder (`flume_fixture`), `unplaced` launches, and `held` as `{n: words}`.

**1.3** `plugin/lib/plan.py` `Stages.host`, used by `bolts_data`, `board.board_data`'s ledger and `page.labelled`'s bolt node. Cases: `tests/py/test_bolt_commands.py` `test_a_bolt_whose_place_the_runner_has_carried_no_status_of_runs_on_that_runners_host` and `test_a_stop_short_whose_agent_flume_0_17_keeps_open_is_on_its_line_and_its_bolt_runs_on_its_host`; `tests/py/test_board.py` `TestStarted.test_a_launch_the_runner_holds_with_no_after_is_on_its_runners_host_with_its_words`, the board and the planner's band (`code.8`). `tests/py/test_page.py`'s stand-in readers give `host`.

**1.4** README's crossing paragraph, `plugin/skills/crew/SKILL.md`'s command table and `plugin/bin/crew`'s usage of `crew answer` say what a held launch with no After reads and what `crew answer` refuses when crew can't tell (`docs.2`).
