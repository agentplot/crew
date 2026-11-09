# Tasks

## 1. The fix crew names

- [x] 1.1 Every refusal of the teams file, its version, a `teams` key, no drives, a drive's `state`, `review` or `flume`, and a kept repository named wrongly, names its fix as crew's own module, `services.crew`, or the machine's configuration that writes it, from one text, and names no module of another repository's (design, Decision 1). Passes `tests/py/test_teams.py` (`tests/suite logic`).
- [x] 1.2 The end-to-end teams file's refusals say the same. Verify `tests/suite t-teams` ends with "0 failed".

## 2. The docs and the change's tests

- [x] 2.1 README, the crew skill and `crew`'s usage header name crew's own module or the machine's configuration as the fix of a refused teams file (`docs.2`). Verify `tests/suite t-docs` ends with "0 failed".
- [x] 2.2 The tests the change affects pass. Verify `tests/suite --affected` ends with "0 failed".
