# crew's bolt kind names its landing fix

## Why

When the merge queue sends a bolt back, for a conflict with main or a check that fails, someone has to launch the fix that takes main in or makes the checks pass. Under `crew-lands-each-bolt-through-flumes-base-place` (this bolt's first unit), crew's read of a conflict launches its own take-main fix, and main-level ops starts the fix for a failed check, or for a forecast conflict, by hand. On 2026-11-07 two of Flume's proven bolts were forecast to conflict with main for 9h 46m and 2h 14m while nothing launched that fix (agentplot/flume record 0056).

Flume record 0056, the user's ("After we rework Boomdrive and Flume, the fixes should be automatic"), has Flume launch a base place's fix itself, on its own forecast of the branch against its base or on a failed or conflicting submission, when the base place's kind names the kind its fixes run as. Weir record 0005, the user's ("Yes, write it into both formats"), spells it: `landing_fix`, the fix kind's whole identity with its version, and `max_landing_fixes`, how many run before the place waits on its caller. Flume 0.19.0 reads both and launches the fixes (agentplot/flume #24, #31).

crew's bolt kind, `crew/bolt@1`, names neither, so Flume launches no fix for a crew bolt. The sibling unit's design says so and leaves it here: "crew's kind naming its landing fix (`crews-bolt-kind-names-its-landing-fix`). Until both, crew's read of a conflict launches the take-main fix as today."

## What Changes

- **crew's bolt kind names its landing fix.** `plugin/flume/kinds/bolt@1/kind.toml` gains `landing_fix = "flume/fix@1"` and `max_landing_fixes = 3`. `bolt@1` has never been released or locked, so it holds them from its first release.
- **crew reads the landing fix from the base place's status.** The runner already carries Flume's status of the base place. crew reads from it the fix kind, the bound and each fix Flume launched, with its cause and how it ended. Where the status names no fix kind, crew acts as before. That covers a Flume older than 0.19.0, or a base place launched before its host had one.
- **crew launches no fix Flume launches.** For a bolt whose base place names a landing fix, crew's read of a refused landing records it as before, but launches no take-main fix and asks ops nothing. That holds while Flume's fix is live, and while Flume has yet to launch it within its bound.
- **Past the bound, ops is asked.** Once Flume has run as many fixes as the bound allows, or its fix was dropped or its launch refused, the base place waits on its caller. crew then asks main-level ops in Flume's words, naming how many fixes ran. crew launches no take-main fix of its own, since that would defeat the bound.
- **A live landing fix holds the bolt.** It counts as a fix in flight on the bolt, so the row has no box and no land is posted while it runs. Without that, Flume would refuse the land and the user's send would be spent. A fix that takes main in leaves the row taking main first, with the send standing for it. A bolt's drop is not asked again while one is live.
- **The views say it.** The bolt's head line, its row, `crew bolts` and main-level ops's band name Flume's landing fix, its cause and whether it runs, is due or is spent.
- **Main-level ops's brief.** Ops starts no take-main fix for a forecast conflict and no fix for a failed check where the row says Flume's landing fix covers it. It starts one only where the row says Flume names none or has run its bound.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `flume-source`: crew's bolt kind names its landing fix and the most landing fixes.
- `bolt-teams`: a refused landing's way on is Flume's landing fix where the base place names one; crew's take-main fix only where it names none; a live landing fix holds the bolt and its drop.
- `main-level`: what ops does after a landing that does not land, with Flume's landing fix.
- `rail-cards`: a row held for, or taking main first by, Flume's landing fix says so.
- `crew-board`: ops's band lists each landing fix Flume runs on a bolt, and the bolt's head line names it.

## Impact

- `plugin/flume/kinds/bolt@1/kind.toml`.
- `plugin/lib/runner.py`: `flume_facts`, a new `landing_fix`, `landing_of`, `landing_said`, `fixes_in_flight`, `base_drop_due`.
- `plugin/lib/plan.py`: `landing_read`; the row words in `landing_rows`.
- `plugin/lib/board.py`: `flume_waits`.
- `plugin/roles/main-ops.md`, `README.md`, `plugin/skills/crew/SKILL.md`.
- Tests: `tests/py/test_source.py`, `tests/py/test_runner.py` with new fixtures in `tests/py/flume-0.19.0/`, `tests/py/test_landing.py`, `tests/py/test_landings.py`, `tests/py/test_board.py`, `plugin/tests/status.test.ts`, `tests/t-briefs.sh`, `tests/t-docs.sh`.
- Other tools: none changes. Flume launches the fixes only on a host whose Flume is 0.19.0 or later. Until then crew acts as before, with nothing to do on the host (design, *After deploy*).
