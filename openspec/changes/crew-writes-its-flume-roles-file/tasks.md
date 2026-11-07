# Tasks

## 1. The roles file's entries

- [x] 1.1 The roles file's text from a teams file holds one standing entry at `<label>/<role>` for each role that stands of each partition whose machine is the host, `agent` its agent's name and `session` the session crew opens it in, `answers` from `ASKS` for the design agent, the planner and ops, `answerer = true` for the operator, no other key, and none for another host's partition or a role that runs as its kind (design, Decisions 3 to 5; Task notes 1.1). Passes `tests/py/test_source.py` (`tests/suite logic`).
- [x] 1.2 The briefs' sentence on whom to ask is built from `ASKS`, ops's words "a live system, a deploy or a landing" (design, Decision 4; Task notes 1.2). Verify `tests/suite t-briefs` ends with "0 failed".

## 2. crew keeps the file

- [x] 2.1 crew's follower writes the roles file whole and renames it over the old one at each read of the teams file, only when it differs, leaves it as it is when the teams file is refused, makes none on a host that is no partition's machine and empties one there, makes the empty kinds folder beside it, runs no `flume` command and changes nothing in the teams file (design, Decisions 2, 5 and 6; Task notes 2.1). Verify `tests/suite t-flume-source` ends with "0 failed".
- [x] 2.2 Starting a main level's role writes the roles file with that partition's entries (design, Decision 2; Task notes 2.2). Verify `tests/suite t-journey-main` ends with "0 failed".

## 3. The docs and the change's tests

- [x] 3.1 README's main-level section says crew writes its Flume roles file and kinds folder from the teams file and keeps them (`docs.2`; Task notes 3.1). Verify `tests/suite t-docs` ends with "0 failed".
- [ ] 3.2 The tests the change affects pass (Task notes 3.2). Verify `tests/suite --affected` ends with "0 failed".
