# Design: every plan write is an act with its entry

## Context

The proposal gives wldn's case of 2026-11-07 and the two of 2026-11-02. Rules this change relies on: `plan.2`, every commit on a flywheel's branch names its run-record entry, and its ruling of 2026-11-02, which this change builds; `read.5`, a decision reads the branch at the newest commit whose entry has arrived, so an act is read whole or not at all; `state.1`, every write one commit pushed without force; `record.1`, one entry per act after the act; `record.2`, a failed append said once and changing nothing the command does; `code.2`, a refusal is a `Refusal`; `code.7`, a decision is a function of plain facts; `teams.9`, what bash evals is assignments and everything else such a command says goes to standard error; `docs.2`, README, the crew skill and `crew`'s usage header say a change together; `tests.4` and `tests.11`, the reproducing case at the lowest tier that holds it. It touches the areas of `plan.md` (`plugin/lib/plan.py`), `record.md` (`plugin/lib/record.py`), `teams.md` (`plugin/bin/crew`), `briefs.md` (`plugin/skills/`), `tests.md` (`tests/`) and `docs.md` (`README.md`, `openspec/`, `docs/`). It departs from no rule.

How a write and its entry reach the branch today: `write` makes the entry's id before its commit, names it in the commit's `Crew-Entry` trailer, lands the commit, and then, only when given `act`, has `record.emit` append the entry, which `record.reach` pushes as the commit after. A decision reads the branch by `fetch`, which reads the newest twenty first-parent commits and, when one names an entry the tip lacks, reads at the parent of the oldest such commit (`decision_at`, `read_point`).

## Decisions

### Decision 1: every write is an act, and the write records its entry

`write` emits the entry its commit names, every time, before it returns; a write given no act is refused by `unacted` before `write` reads the branch or pushes, naming its subject. The entry reaches the branch through `record.reach` in the same call, so once `write` returns its entry's commit follows its own, unless that push is refused and kept (`record.2`), which delays the branch's view of it as before and changes nothing the command does.

Considered: a commit that names no entry when given no act. `plan.2` asks every commit to name its entry, and a write with no act is a change to the plan with no record of who made it.

### Decision 2: the three writes take their acts

- **The give.** `bolt_give` passes `act="bolt.give"` and `on=[bolt/<bolt>, team/<team>]` to its write, and no longer emits the entry itself. The entry's `Why` is the write's subject, `plan(<bolt>): give to <team>`, as it was.
- **A unit marked amended.** `mark_amended` is a `unit.mark` write on `unit/<unit>` and `bolt/<bolt>`, its `Head` the head construct starts again from. The construct's `stage.start` keeps `Amended: yes` and names the mark's commit in `Commit`, under an id of its own: it is written only once the stage's agent took its prompt, and not at all when it did not, so it cannot be the entry a commit pushed before it names. `run_check` and `chore_check` no longer hand the stage an `ENTRY`.
- **The mark cleared.** `unmark` is a `unit.unmark` write on `unit/<unit>`, `stage/<unit>/construct` and `bolt/<bolt>`, its `Head` the mark it cleared.

`unit.mark` and `unit.unmark` are acts and no new kind of object: the run record's objects stay closed. `Head` is already among an entry's allowed fields.

Considered: naming the `stage.end` the unmark follows from in the unmark's commit. That entry is written by the wait before the plan write and is its own act; the unmark is another.

### Decision 3: the read below the tip is kept with the write it waits on

`read_point` reads each commit's subject beside its parents and trailers, in the same `git log`. `waited_on(commits, texts)` gives the oldest commit in flight when `decision_at` reads below the tip, from the same facts; `entry_held` and `in_flight` are what both share, so `decision_at` answers exactly as before. `read_point` keeps that write and its subject for the tip it read. `fetch` hands each read to `Reading.keep_below`, which keeps a command's latest read of each branch: below its tip, with the write it waits on, or at its tip, which takes back what an earlier read kept, since the command's later steps read past it.

### Decision 4: the command says so, before a refusal and on standard error after an answer

`below_said(ref, tip, at, write, subject)` words one read: `<ref> was read at <at>, below its tip <tip>: the write <write> by <agent> is on the branch without its run-record entry yet, so nothing from <write> on was read (read.5)`, the agent from the write's subject (`writer_of`), or that its subject names none. `below_read` gives a refusal's words after one such line for each branch read below its tip, so a caller that takes a refusal's last line still takes the refusal; with no refusal it says the lines on standard error, where no caller parses them (`teams.9`), once the command has answered. `plan.py`'s and `record.py`'s entry points call it. A stop at 0 is a command handed to its host, whose own process says its reads there, so it says nothing; a stop with any other code says its reads.

Considered: standard output after an answer. bash evals what some commands print, and `--json` answers are read whole; standard error reaches the agent and the person all the same. Considered: the note on the refusal's own line. A refusal may span several lines, and the note is a sentence of its own.

## After deploy

None. Every case is held by the logic tier, the contract tier and `t-journey-plan` and `t-journey-prompts` on the stubs; what a host runs is its pin of crew's release, not a step of this change.

## Task notes

**1.1** `plugin/lib/plan.py`: `unacted`, called first in `write`, which records its entry always. Logic: `tests/py/test_in_flight.py`, a write with no act refused before `state_of` or `land`; every call of `write` in `plan.py` names `act`, read from its syntax tree. Contract: `tests/contract/test_record.py`, a real write on a bare repository read at the tip it leaves once it returns, its entry's commit the tip and naming the write's commit, and a write with no act leaving the branch where it was. `tests/contract/test_recfix.py`'s give, which wrote with no act, names `bolt.give`, its entry held by the case rather than written to the host's record.

**1.2** `plugin/lib/plan.py`: `bolt_give`'s write; `mark_amended`; `run_check`'s facts and `chore_check`'s without `ENTRY`; `run_unit_stage`'s `extra`; `unmark`. `plugin/lib/record.py`: the fields' comment. Logic: `tests/py/test_in_flight.py`, `mark_amended` and `unmark` each handing `write` its act, objects and `Head`. End to end: `tests/t-journey-prompts.sh`, the amend's mark commit naming the `unit.mark` entry, which names it, and the cleared mark's commit naming the `unit.unmark` entry; the give's entry in `t-journey-teams` and the board's and cards' tests as before.

**1.3** `plugin/lib/plan.py`: `entry_held`, `in_flight`, `decision_at`, `waited_on`, `writer_of`, `below_said`, `read_point`, `fetch`, `Reading.keep_below`, `Reading.below`, `below_read`, the entry point; `plugin/lib/record.py`'s entry point. Logic: `tests/py/test_in_flight.py`, on wldn/main's commits of 2026-11-07: `decision_at` unchanged, `waited_on` the cleared mark's write, `writer_of`, `below_said`'s words, `keep_below`'s latest read and its taking back, `below_read` before a refusal and on standard error. Contract: `tests/contract/test_record.py`, the read below a write in flight keeping that write and its subject, and nothing once its entry arrives. End to end: `tests/t-journey-plan.sh`, a hand's write naming an entry the branch lacks, `crew plan proposed <n>` refused for a proposal written after it with the line naming the commit read at, the tip, the write and its agent, then read once the entry arrives.

**1.4** README's paragraph on the branch's commits, the crew skill's line under keeping a team healthy, and `crew`'s usage header's closing paragraph.
