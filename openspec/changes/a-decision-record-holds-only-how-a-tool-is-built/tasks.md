# Tasks

Each check is a moon task of the `tests` project, run through `tests/suite`. Run each from the worktree's root. Submit nothing, and never run `wt submit --help`.

## 1. The design agent's brief

- [x] 1.1 *Decision records* opens by saying a record holds only how a tool is built or behaves, that a plan matter goes to the planner, or to ops for a live system, naming the signal of the user's words, with no record, amendment or card, and that a unit cites only records of how a tool is built (design, Decisions 1 and 2; Task notes 1.1). Verify `tests/suite t-briefs` ends with "0 failed".
- [ ] 1.2 Every record states each decision in its own words: a decision the user settled has a deciders line naming where and when, an acceptance states their note and a rejection says why and where, none quoting the user, and the brief says the `--excerpt` of their yes is crew's evidence and goes into no record (design, Decision 4; Task notes 1.2). Verify `tests/suite t-briefs` ends with "0 failed".
- [ ] 1.3 At its start, the design agent raises no card for a proposed record or amendment that holds only a plan matter, and instead takes it out of the kit's main and tells the planner or ops (design, Decision 3; Task notes 1.3). Verify `tests/suite t-briefs` ends with "0 failed".
- [ ] 1.4 *Elaboration on main*, *Talking design with the user*, *Answering a design question* and *Queuing work* follow the line: only how a tool is built is recorded, and a plan matter, asked or settled, goes to the planner or ops with nothing recorded (design, Decision 1; Task notes 1.4). Verify `tests/suite t-briefs` ends with "0 failed".

## 2. The planner's brief

- [ ] 2.1 A unit's `--source` names only records of how a tool is built or behaves, and a plan matter the design agent hands the planner is carried in the plan, by a proposal where it changes the plan, and is never asked for as a record or cited as a source (design, Decision 6; Task notes 2.1). Verify `tests/suite t-briefs` ends with "0 failed".

## 3. The constitution skill

- [ ] 3.1 The constitution skill says a kit's record holds only how the kit is built or behaves, states each decision in its own words with `decision-makers` naming who settled it without quoting them, and that a plan matter gets no record (design, Decision 7; Task notes 3.1). Verify `tests/suite t-docs` ends with "0 failed".
