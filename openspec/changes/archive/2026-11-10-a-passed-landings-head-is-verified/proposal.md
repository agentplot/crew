# A passed landing's head is verified

## Why

crew 0.49 reads a bolt's verification green only where its head is the landing of one of its units, chores or fixes as the runner reports it. A landing on the bolt that is no piece crew launched, a design agent's record or a record's fix landed straight onto the bolt, leaves the head no such landing: the bolt reads none and reaches no landings card. Six bolts were held 15 to 21 hours on 2026-11-09/10 this way: `sluices-sandbox-keeps-its-proof`, `the-hosted-protocol-carries-every-end`, `the-runner-confirms-the-ends-it-carries` (its head `8df8e1d`, sluice's #70 of record 0030's fix, `Sluice-Result: passed (3 run, 0 replayed)`), `boomdrive-keeps-its-site` and `a-put-away-preview-leaves-the-runners-report`. sluice lands nothing on a bolt but on its required checks passing, and its landing commit names the verdict it landed on (sluice clause 23), so a head sluice landed passed is verified whoever submitted it (signal 2026-11-09-agentplot-design-9b1ec2dd/01).

## What Changes

- **A bolt's head that sluice landed passed reads green.** Where no piece landed at the head, a head that is a landing sluice made on the bolt, the newest commit of the bolt's own line beyond main, whose commit names one `Sluice-Result` reading passed reads green, its words naming sluice's landing by its `Sluice-Submission`. A head main holds, a commit with no verdict, a verdict of another word or two verdicts read none; trailers git can't read read unknown, named.
- **gather reads the head's two trailers.** Each bolt's facts carry `head_landing`: the head's `Sluice-Submission` and `Sluice-Result` values where the head is on the bolt's own line beyond main, None otherwise, or why it can't be read. gather reads no other trailer and nothing of sluice's records, and runs no sluice.
- **A piece's end stays the runner's report's.** No piece reads merged or landed from the head's verdict, so a bolt with a piece not yet merged is not offered whatever its head reads.
- This is record 0062's stopgap as amended 2026-11-10, retired once the runner's report carries a bolt's head with its verdict. README, the crew skill, `crew`'s usage header and CLAUDE.md say so.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `merge-gate`: a bolt's verification reads green at a landing sluice made on the bolt that passed, whoever submitted it, and the gather reads the head's own `Sluice-Submission` and `Sluice-Result`.

## Impact

- `plugin/lib/gather.py`: `TRAILERS`, `head_landing`, and `kit`'s `head_landing` for each bolt read.
- `plugin/lib/runner.py`: `verification` takes the head's landing facts; `PASSED`, `passed_landing`.
- `plugin/lib/plan.py`: `Stages.verification` takes them, and `Stages.bolt_state`, `land_facts`, `bolts_data` and `rail_rows` pass each bolt's `head_landing`.
- Docs: README, `plugin/skills/crew/SKILL.md`, `plugin/bin/crew`'s usage header, CLAUDE.md; record 0062's amendment and `tests.5`.
- Tests: `tests/py/test_runner.py`, `tests/py/test_stages.py`, `tests/py/test_rail.py`, `tests/contract/test_gather.py`.
- Nothing of what the views file carries changes shape (`code.8`): the verification stays `{state, said}`.
