# Tasks

## 1. The gate

- [ ] 1.1 `tests/t-specs.sh` holds every spec under `openspec/specs/` to `openspec validate --specs --strict`, having first found a requirement of 501 characters refused and one of 500 taken in scratch specs of its own, and `tests/moon.yml` carries its `check-full` task (design, Decision 5; Task notes 1.1). Verify `tests/suite t-specs` ends with "0 failed" once the change is archived.
- [ ] 1.2 `openspec/config.yaml`'s spec rules and CLAUDE.md's *Specs* say a requirement's text is at most 500 characters and that `t-specs` holds every spec to it (design, Decision 6; Task notes 1.2). Verify `tests/suite t-docs` ends with "0 failed".

## 2. The split

- [ ] 2.1 Every requirement past 500 characters in crew's 23 failing specs is removed and added again as requirements that together say the same, each within the limit with its SHALL or MUST and the original's scenarios that prove it, each scenario carried once (design, Decisions 1 to 3; Task notes 2.1). Verify `openspec validate crews-specs-pass-strict-validation --strict` passes, and, once the change is archived, `tests/suite t-specs` ends with "0 failed".
- [ ] 2.2 Every citation of a split requirement's name in `plugin/` and `tests/` names the part that holds what it cites (design, Decision 4; Task notes 2.2). Verify `tests/suite logic` ends with "0 failed".

## 3. The change's tests

- [ ] 3.1 The tests the change affects pass. Verify `tests/suite --affected` ends with "0 failed".
