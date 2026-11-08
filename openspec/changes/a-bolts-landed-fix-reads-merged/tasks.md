# Tasks

## 1. A fix its bolt holds is merged

- [x] 1.1 A fix on a bolt names its place's branch `fix/<bolt>--<name>` and a fix of main none, and `built_on_bolt` reads a fix merged at a landing on its bolt naming that branch, unless the landing was made before the fix's launch (design, Decisions 1 and 2; Task notes 1.1). Verify `devenv shell -- sh -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_fix.py tests/py/test_stages.py -k "TestAFixItsBoltHolds or TestBuiltOnItsBolt"'` ends with "passed" and no "failed".
- [x] 1.2 `Stages.fixes` reads each fix of a started bolt through its bolt's landings, as `Stages.crossed` reads a unit through `Stages.landings`, so `crew bolts` and the board show a landed fix merged (design, Decision 3; Task notes 1.2). Verify `devenv shell -- sh -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_stages.py'` ends with "passed" and no "failed".
- [ ] 1.3 A fix read merged from its landing holds its bolt's landing no longer, the landing reading its fixes in flight from `Stages.fixes` with no second read of the runners (design, Decision 3; Task notes 1.3). Verify `devenv shell -- sh -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_fix.py'` ends with "passed" and no "failed".
- [ ] 1.4 `crew fix <bolt> <name> --drop` is refused for a fix its bolt's landing reads merged, and goes as today where no landing names it (design, Decision 3; Task notes 1.4). Verify `devenv shell -- sh -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_fix.py -k TestAFixOfAStartedBolt'` ends with "passed" and no "failed".

## 2. The docs

- [ ] 2.1 README, the crew skill and `crew`'s usage header say a unit, chore or fix is merged once a landing on its bolt names its place's branch, a fix's only from a landing at or after its launch (`docs.2`; Task notes 2.1). Verify `tests/suite t-docs` ends with "0 failed".
