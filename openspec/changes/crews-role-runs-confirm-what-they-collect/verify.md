# Verify: crews-role-runs-confirm-what-they-collect

Checked on `change/crews-role-runs-confirm-what-they-collect` at 09763ae0, cut from `bolt/crews-role-runs-confirm-their-ends`, merge-base with main 0563aa90, on 2026-11-08.

## The whole checks

`tests/suite --affected`, run once, as CLAUDE.md names it for a change that is done: **28 passed (2 replayed), 0 failed**, exit 0.

- Ran: `logic`, `contract` and all 26 end-to-end tests (`t-briefs`, `t-cards`, `t-docs`, `t-flume-source`, `t-help`, `t-hold`, `t-journey-board`, `t-journey-cross`, `t-journey-land`, `t-journey-main`, `t-journey-main-fix`, `t-journey-ops`, `t-journey-plan`, `t-journey-review`, `t-journey-roles`, `t-journey-signals`, `t-journey-state`, `t-roles`, `t-runner`, `t-session-hook`, `t-slot`, `t-sluice`, `t-stage-facts`, `t-suite`, `t-teams`, `t-waits`).
- Replayed: `t-docs` and `t-journey-roles`, from passing runs on this host with identical inputs.
- Not affected: `mod`, since nothing under `plugin/hooks/` or `plugin/tests/` changed, and the `nix` project's tasks.

`openspec validate crews-role-runs-confirm-what-they-collect --strict`: valid.

## Tasks

All 12 tasks in `tasks.md` are ticked. Each one's named case or test exists, and each passed in the run above:

| Task | Check | Where |
|---|---|---|
| 1.1 | `TestEndsOwed` | `tests/py/test_asks.py`; fixture `tests/py/flume-deliveries/` with its `README` |
| 1.2 | `TestEndsTaken` | `tests/py/test_asks.py` |
| 1.3 | `TestTurnConfirms` | `tests/py/test_asks.py` |
| 1.4 | `TestConfirmRequest` | `tests/py/test_runner.py` |
| 1.5 | `test_a_confirm_with_two_deliveries_passes_recfix_and_an_act_the_descriptor_lacks_is_refused` | `tests/contract/test_recfix.py` |
| 1.6 | `TestEndsSaid` | `tests/py/test_asks.py` |
| 1.7 | `test_a_turns_ends_are_counted_on_its_head_line_and_listed_nowhere` | `tests/py/test_board.py` |
| 2.1 | `TestStart`, its four named cases | `tests/py/test_asks.py` |
| 2.2 | `TestEnd`, its three named cases | `tests/py/test_asks.py` |
| 3.1 | `test_its_end_says_it_asks_the_runners_to_confirm_the_ends_the_turn_took` | `tests/py/test_role_kinds.py` |
| 3.2 | `t-docs` | `tests/t-docs.sh` |
| 3.3 | `t-journey-roles` | `tests/t-journey-roles.sh`; its `# Reads:` line names `tests/py/flume-deliveries/`, and `tests/moon.yml` follows it |

## Requirements against the code

### role-runs

- **A run's start takes every end Flume holds for its role.** `asks.owed_to` and `asks.ends_owed` read each end whose `owed` names `<label>/<role>`, from every carried place whose request is a launch, whatever its `Recipient`. Each end is given with its delivery key, and its took key is `end/<request>/<delivery>`. `plan.role_start` adds them to the turn through `asks.took`, after the asks and waits. An end owed to another role is not given (`test_an_end_the_address_confirmed_or_owed_to_another_alone_is_not_given`).
- **An end a confirm names is not taken again.** `asks.confirmed` reads every `confirm` of the address, whatever it was answered, and `asks.taken_ends` leaves those ends out. `role_start` reads the requests at the tip its write is applied to (`plan.1`).
- **An owed end makes no role wanted.** `role_start` raises `NothingPending` on asks and waits alone, before any end is read. `asks.wanted` and `asks.pending` are unchanged (`test_ends_alone_take_no_turn`).
- **An end crew cannot read is not taken.** Every field is guarded: `delivery` and `key` must be strings, `owed` a list of entries each with a string `recipient`, and `expired` counts only when it is `true`. A status from Flume 0.17.0 gives no end. A host whose runner can't be read is left out by `run_reads`, as its waits are.
- **A run's end asks the runners to confirm each end its turn took.** `asks.turn_confirms` groups the turn's `end/…` lines by launch, oldest first, with keys in the order taken. A Flume key holding slashes is kept whole, and a malformed line is refused through `fail`. `plan.role_end` appends one `confirm` per launch (`Of`, `Work`, `Recipient`, one `Delivery` per key) in the same write that ends the turn. A turn with no ends appends none. The journey proves this end to end: one commit touching only `asks.rec` and `requests.rec`.
- **A lost run confirms nothing.** No confirm is written outside `role_end`'s open turn, so a superseded turn's ends are taken again (`test_a_superseded_turns_ends_are_taken_again_with_no_confirm_naming_them`, `test_a_run_with_no_turn_asks_no_confirm`).
- **A turn's report counts its ends.** `asks.took_said` adds `- <k> ends of requests <a> and <b>, their confirmation asked of the runners` after the asks and waits.
- **A turn's prompt starts and ends the turn** (modified). `plugin/flume/turn.md` steps 1 and 3 say the start takes the ends Flume holds and the end asks the runners to confirm each one. No part in double braces was added.
- **A run's start gives its brief and what it took** (modified). `asks.ends_said` prints one line per launch after the waits and before the cards: its work, place and request, then each end's key with expired ones marked, under a heading saying they are confirmed when the turn ends.

### drive-state

- **crew asks a host's runner for work by requests on the drive's branch** (modified). The `REQUESTS` descriptor's `Act` enum takes `confirm` and its `%allowed` list takes `Delivery`. A confirm is numbered and appended through `plan.request` in the commit that ends the turn. The contract case shows a confirm with two `Delivery` lines passing `recfix --check`, and an act the enum lacks refused.
- **A launch names everything the runner passes to Flume** (modified). `ACTS["confirm"]` needs `Of`, `Recipient` and `Delivery`, and takes nothing else. `request_refusal` refuses:
  - a confirm whose `Of` is no launch, or another work's launch;
  - a `Recipient` that is not `<label>/<design|planner|reviewer|ops|operator>`;
  - a confirm with no `Delivery`, or carrying a field a confirm does not take.

  A confirm names no host.

### crew-board

- **A role that runs as its kind has its view** (modified). `asks.run_view`'s turn gains `ends`, a count, and its `took` leaves the ends out. `board.run_rows` writes `turn <n> took <k> and <m> ends` and draws no row for an end. The mod draws rows it is given and reads no turn field, so `plugin/hooks/status.js` and its cases stand (`code.8`), as design Decision 7 says.

## Docs

- `README.md`'s `requests.rec` line names a confirm.
- The role-runs paragraphs in `README.md` and `plugin/skills/crew/SKILL.md` say a start takes the ends Flume holds for its role and its end asks the runners to confirm them.
- `t-docs` pins these phrases.
- `plugin/bin/crew`'s usage is unchanged, since no command or argument changed.

## Findings

None. The work holds against every requirement and scenario of the change's three delta specs. The dependencies the design names are other tools' work, and nothing of crew's waits on them: `flume confirm` is on agentplot/flume's bolt `flumes-ends-are-owed-until-confirmed`, and the runner's reading of a confirm is Boomdrive's.
