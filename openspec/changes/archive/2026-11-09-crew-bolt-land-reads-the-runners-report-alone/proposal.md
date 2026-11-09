# crew bolt land reads the runner's report alone

## Why

The bolt `crew-reads-every-end-from-the-runner` took main in at `773784c` (`plan.8`). Main had landed `crew-lands-through-the-runners-land-message`, whose change `the-runners-land-takes-mains-readings-in` lets `crew bolt land` close a started bolt at the landing its kit's main holds, found by its `Sluice-From`, where the runner's report does not read it landed. The bolt's change `crew-reads-each-pieces-end-from-the-runners-report` removes that reading with record 0062's stopgap, and its Decision 7 leaves to the take-main fix what becomes of main's fallback: it goes, every end is read from the runner's report alone, and a bolt started before bolts were base places is refused, closed only by the crew that started it.

The merge built that in the code. Two requirements still say otherwise:

- bolt-teams "A landing records the commit main holds" still has `crew bolt land` close a started bolt "or at the landing its kit's main holds", citing the requirement the bolt removed.
- bolt-teams "A bolt started before bolts were base places lands under the crew that started it" does not say that `crew bolt land` refuses such a bolt.

And batch 27's review found merge-gate's scenario "A landing read from the bolt's own landings" named for what it no longer checks: crew reads no such landing.

## What Changes

- **A started bolt closes on the runner's report alone.** `crew bolt land` closes a started bolt once its base place reads landed, as the runner reports it, the record Flume holds for the runner after it tidies the base place among them. While it does not, the command is refused, recording nothing, naming the landing as the runner's report has it. No landing commit on its kit's main is read for it.
- **A bolt started before bolts were base places is refused.** `crew bolt land` refuses it in the words `crew bolts` gives it, recording nothing. The crew that started it closes it.
- **merge-gate's scenario is renamed** "A head only a landing commit names", its steps unchanged. OpenSpec drops a scenario only with its requirement, so the requirement is removed and added again whole as "A bolt's verification is its work's landing at its head, as the runner reports it alone", and the two requirements that cite it by name cite the new one.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `bolt-teams`: "A landing records the commit main holds" and "A bolt started before bolts were base places lands under the crew that started it"; "A bolt's proof is its verification" cites merge-gate's requirement by its new name.
- `merge-gate`: "A bolt's verification is its work's landing at its head, as the runner reports it" is removed and added again as "… as the runner reports it alone", its scenario "A landing read from the bolt's own landings" named "A head only a landing commit names".
- `rail-cards`: "The landing card is posted once the bolt's verification is green" cites the new name.

## Impact

- `plugin/lib/plan.py`: `started_land`; `main_landed` goes (built in the merge, `f631fe94`).
- `README.md`, `plugin/skills/crew/SKILL.md`, `plugin/bin/crew`'s usage (written in the merge).
- Tests: `tests/py/test_landing.py`, `tests/py/test_stages.py`, `tests/t-journey-land.sh`, `tests/t-docs.sh`, `tests/lib.sh` (written in the merge); `tests/py/test_landing.py`, `tests/py/test_stages.py` and `tests/py/test_runner.py` cite the scenarios and requirement by their new names.
