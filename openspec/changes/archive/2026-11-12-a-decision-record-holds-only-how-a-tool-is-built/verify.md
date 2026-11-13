# Verify: a-decision-record-holds-only-how-a-tool-is-built

Verified on `change/a-decision-record-holds-only-how-a-tool-is-built` at 81d345e7, cut from `bolt/decision-records-hold-only-how-tools-are-built`, on 2026-11-12. Verdict: **the work holds; archive.**

## Whole checks

`tests/suite --affected`, run once from the worktree's root, as CLAUDE.md names it for a finished change:

```
ok    contract
ok    logic
ok    t-briefs   (replayed)
ok    t-docs   (replayed)
ok    t-journey-cross
ok    t-journey-land
ok    t-journey-main
ok    t-journey-main-fix
ok    t-journey-review
ok    t-journey-roles
ok    t-journey-signals
ok    t-roles
ok    t-teams
ok    t-word
14 passed (2 replayed), 0 failed
```

Exit 0. `t-briefs` and `t-docs` were replayed from a run that passed on this host with identical inputs (`tests.10`). sluice runs them again with nothing replayed at the merge.

`openspec validate a-decision-record-holds-only-how-a-tool-is-built --strict` (openspec 1.17.0): valid. `openspec validate --specs --strict`: 29 passed, 0 failed. Each requirement's text above its first scenario is under 500 characters (352, 448, 494 and 396), so `t-specs` holds after the archive.

## Tasks

All six tasks are ticked, and each one's words are in the file it names:

| Task | Where | Found |
|---|---|---|
| 1.1 | `plugin/roles/design.md`, *Decision records*, first paragraph | What a record holds; the plan's list in `briefs.15`'s words; told to `{{PLANNER}}`, or to `{{MAIN_OPS}}` for a live system, naming the signal; no record, amendment or card; a unit cites only records of how a tool is built or behaves |
| 1.2 | the same, second and third paragraphs and bullets | "states each of its decisions in its own words, never the user's words quoted as the decision"; the deciders line names where and when; "the record says where they gave it"; bullet retitled *What the user settled*; *Yes* states the note in the record's own words; *No* says why and where; the excerpt "is crew's evidence and go[es] into no record" |
| 1.3 | the same, *At your start* | "A proposed record or amendment that holds only a plan matter gets no card: take it out of the kit's main in a commit, submitted as any record is, and tell the planner, or ops for a live system" |
| 1.4 | *Elaboration on main*, *Talking design with the user*, *Answering a design question*, *Queuing work* | Each one's text matches Task notes 1.4 |
| 2.1 | `plugin/roles/planner.md`, *Proposals* | `--source` takes only records of how a tool is built or behaves; a new paragraph carries a plan matter in the plan and never asks for a record of one or cites one |
| 3.1 | `plugin/skills/constitution/SKILL.md`, §3 | One sentence after the MADR line, as specified |

Each old phrase is gone from `plugin/roles/design.md`: "record it with those words quoted as its deciders", "quotes those words as the user's decision", "quoting any note they added in their own words", "with the user's words, and take out", "quotes the user's words as their decision" and the bullet title "The user's own words." `tests/t-briefs.sh` pins each new phrase and checks with `lacks` that each old one is gone. `tests/t-docs.sh` pins the skill's sentence (`tests.6`). Neither test reads a new path, so `tests/moon.yml` is unchanged (`tests.10`).

## Requirements and scenarios (`main-level`)

**Renamed:** *The user's own words are their decision* becomes *A record states the user's decisions in its own words*. The old name is in `openspec/specs/main-level/spec.md`, line 52.

**Added: A decision record holds only how a tool is built or behaves.** Met.
- *A talk settles how a tool behaves*: *Talking design with the user* says "record it and commit: the record states the decision in its own words, is told to them by number and commit".
- *A unit's sources*: the design brief says "A unit you queue cites only records of how a tool is built or behaves", and *Queuing work*'s `--source` is "decision record of how the tool is built". The planner's `--source` takes "only records of how a tool is built or behaves".
- *A proposed amendment that is a plan matter*: *At your start* has it raise no card, take the amendment out in a commit "submitted as any record is" (through sluice, as *Elaboration on main* has it), and tell the planner in one line.

**Added: A plan matter goes to the planner, or to ops for a live system, with no record.** Met.
- *The user freezes fixes in the design talk*: *Talking design with the user* has the agent record the user's words as a signal, tell `{{PLANNER}}` in one line naming the signal, and write no decision record. *Decision records* adds no amendment and no card.
- *A carry-over on a live system*: the same sentence, told to `{{MAIN_OPS}}` for a live system.
- *A question that is a plan matter*: *Decision records* names "which bolt or unit carries something" as the plan's: tell the planner and record nothing. *Answering a design question* says a plan question "is no design question: tell whoever brought it that it is the plan's … and record nothing". That sentence lists only order of work, priority, freeze, schedule and carry-over. Task notes 1.4 set that list, and the general paragraph in *Decision records* covers which bolt carries something. This does not block the change, and a later wording pass can bring the two lists level.
- *The planner carries a plan matter*: the planner brief's new paragraph says "Carry it in the plan, by a proposal where it changes the plan, and never ask the design agent for a decision record of it".

**Modified: A decision record is accepted only on the user's yes.** Met. The brief commits every record and amendment as proposed. It says "it is accepted only on the user's yes, given in this pane or on that card, and the record says where they gave it". *Before the card* keeps rules marked proposed and queues no unit from the record. *Yes* sets "accepted by the user on <date>, on their card", runs `--accepted` and only then queues units. An amendment to an accepted record is marked proposed where it stands, and its card carries it. All three scenarios hold.

**Modified: A record states the user's decisions in its own words.** Met.
- *The user's own words*: the bullet *What the user settled* states the decision in the record's own words, with a deciders line naming the user and where and when, "quoting none of their words". Where the record also holds a choice of the user's alone, the card says the rest is theirs already.
- *The user's yes in the pane is crew's evidence, not the record's*: `--settled-in-pane --excerpt` still quotes the yes whole, and "those words are crew's evidence and go into no record".

## Scope

- The diff against main touches only the change's own files, the three brief and skill files and the two tests.
- No code, view or mod changes (`code.8` is not engaged).
- Nothing under `docs/architecture/` or `docs/adr/` is touched (`docs.7`).
- The departure from `openspec/config.yaml`'s last-task rule is named in the design's *Departures*. This stage ran the whole checks in its place.
