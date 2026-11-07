# crew's tests keep the host's load within its cores

## Why

On deneb, on 2026-10-29 at 18:00Z, the load stood at 70 to 77 on 18 cores. crw-6's conductor read it to crew's end-to-end tests: "up to 16 crew end-to-end tests run at once across the host, and each one starts many crew, git and python processes. That, not the number of sluice runs, is what pushes the load far past 18 cores" (signal `afterthought/crew-state:madswan/main signals/2026-10-30-crw-6-conductor-80044148/01`). The tests shared `tests/slot`'s slots, the host's cores less two, sixteen there, one test to a slot.

`tests.9` bounds the suite's parallelism by the host's cores, so that two suites side by side never load a host past them. A count of one test per core holds only if a test costs the host one core. Read on deneb on 2026-11-07, it costs more beside others, and sixteen of them fill the host.

Two of the tests' own waits also start more than they test. The stub sluice's pause returns at once on macOS, so a landing's waiter spins on a held submission. And `until_ok` starts its command and a sleep ten times a second for as long as it waits.

## What Changes

- **The host's slots come from what one test costs.** `tests/slot` counts the slots as many tests as the host's cores less two hold at `TEST_CORES`, a core and a half each, at least one: ten on deneb's 18 cores, nine on the box's 16, five on ten. `CREW_TEST_SLOTS` still names a count.
- **A test's waits start little.** `tests/lib.sh` gains `nap`, a pause on a fifo nothing writes, which starts no process. `until_ok` looks at once, then at pauses doubling from a tenth of a second up to a second.
- **The stub sluice pauses on every host.** Its pause reads the test's fifo instead of `<> <(:)`, which macOS refuses. A held wait exits 5 after a second, or once the hold is lifted, so a waiter on a held submission calls about once a second.
- `t-journey-main` waits for the other roles' greetings with `until_ok`, not a loop of its own starting three greps and a sleep ten times a second.
- `t-waits` proves the waits. `t-slot` proves the count. README and CLAUDE.md say how many slots a host has and that a test's waits start little.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `test-suite`: a host's slots are as many tests as its cores less two hold at what one test costs the host beside others. A test's waits look less often the longer they wait and start no process to pause, and the stub sluice's held wait pauses on every host.

## Impact

- `tests/slot`: `TEST_CORES` and `count`.
- `tests/lib.sh`: `nap`, `until_ok`.
- `tests/stubs/sluice`: `pause`, the held wait.
- `tests/t-journey-main.sh`: the wait for the greetings.
- `tests/t-slot.sh`, `tests/t-waits.sh` (new), `tests/moon.yml`.
- `README.md`, `CLAUDE.md`.
- No change to `plugin/`. `crew ops quiet` still reads each held slot as one running test.
