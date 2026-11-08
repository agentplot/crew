# Design: a held fix of main raises its kit's landings card

## Context

The proposal gives the case of 2026-11-08. Rules this change relies on: `state.3`, under which a fix of main reaches main only by its submission, held for the user's send and retried by ops on it; `roles.2`, which makes that send the user's word and ops's act; `plan.16`, under which the kit's landings card is raised in main-level ops's name and its send is the word for what it ticks; `read.1`, under which a fix whose stage crew can't read is no row and a send crew can't tell of is not taken as standing; `code.7`, which keeps each decision here a function of plain facts; `docs.2`; `tests.4` and `tests.11`, which put the reproducing cases in the logic tier. The family's side is unchanged: Flume holds the place's submission (`Hold: submission`) and the runner submits it on crew's retry; crew changes only what it shows and reads. It touches the areas of `plan.md` (`plugin/lib/plan.py`), `briefs.md` (`plugin/roles/`, `plugin/skills/`), `tests.md` (`tests/`) and `docs.md` (`README.md`, `openspec/`). It departs from no rule.

## Decisions

### Decision 1: a fix of main rides the card's rows, named by its place and shown at its launch

A fix's row is a row of the card as a bolt's is, named `main--<name>`, its place's name, and shown at its launch's request number, `r<n>`, in the Heads every post and change records. Every reader of the card's rows (the raise's change and close, the send's read, the answer's record, the sweep's wait on ops, the rail's answered line) then reads the fix where it reads a bolt, and tells it from one by its head (`fix_head`). A bolt's head is a commit; `r<n>` is none, so the two never meet.

Considered: a track of fix rows beside the bolts' on the card, which every one of those readers would read a second time, the change and close of the card done twice over; showing the fix at its place's commit, which Flume's status of a place whose submission waits held does not carry (`read.2`); and showing it at its name alone, under which a fix dropped and launched anew under the same name would inherit the user's send on the first.

### Decision 2: a sent fix is no row, and stands on the send until its runner takes it

A fix sent on the user's word already, its retry standing, is no row: nothing of it is the user's to tick. The raise counts every fix of the kit's main that waits held, sent or not, among what is still to land on a send that ticked it, as it counts a bolt the plan holds, so an answered card is left while ops is still to send a ticked fix and while its runner is still to submit it. Once it no longer waits held, the close says how it went, read from the requests (`runner.main_fix_gone`): sent on the user's word for its runner to submit, dropped, or gone on by another way.

Considered: closing the card at ops's send, before the runner's submission, which would close it while the kit's row still carries the fix and before the submission the user's send is for has been made, where a bolt's card is left until the bolt has landed.

### Decision 3: the read gives a ticked fix as ops's command, bare

`crew card read land/<kit>` gives each fix the user ticked, on the card or on an earlier send while it waits held at the launch that send showed, as `crew main fix <kit> <name> --send`, the line the rail already names, ahead of the bolts' submit. It carries no `--excerpt`: the word is the card's send, which `crew main fix --send` takes without words, as `crew bolt submit` takes a card's. A fix the read gives that ops sent already is refused by the send itself, once (`runner.send_refusal`).

### Decision 4: ops's wait on an answered card ends at the fix's send

The sweep leaves an answered landings card while a bolt its send ticked has no landing or drop recorded since. For a fix, ops's act is its send: the wait ends at a `fix.merge` or `fix.drop` on `fix/main/<kit>/<name>` recorded since the answer, so a card whose fix was sent is closed once its row is gone, and not left waiting on ops for an act ops has made.

### Decision 5: a fix alone is an approval, and forecast against nothing

A card's form follows its count of rows, so a fix alone is the card's one row, an approval of risk high as a lone bolt's is, since Pending You takes no list of fewer than two boxes. A fix is cut from main and submitted onto it alone, so no conflict with main or with a bolt above it is forecast for it, and none is recorded.
