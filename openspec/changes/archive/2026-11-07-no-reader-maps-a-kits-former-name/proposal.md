# No reader maps a kit's former name

## Why

On 2026-11-06 the user ruled out any reader's workaround for a kit's former name (signal `2026-11-06-agentplot-planner-230ee466/01` on agentplot/main of afterthought/crew-state): "Wouldn't the root cause be that the original rename didn't rename the parts of the data that were necessary? If anything shouldn't the tools expose some sort of rename functionality? I don't want you to be building fucking custom workaround shit". On 2026-11-07 they rejected crew record 0055 ("Reject 0055: crew is removed from swancloud and added to agentplot"), and accepted record 0060, whose rule `plan.22` says no reader maps a former name and rules out "a reader through `kit_now` or the run record's `kit.rename` entries".

crew still has those readers. `a-kit-renamed-on-its-host-is-renamed-across-the-plan` added `kit_now` and the partition's renames, read from the run record's `kit.rename` entries. Through them crew reads a partition's kits, its launches in `requests.rec`, a landing's kit, a fix of main, card keys, a source's repository, and a kit's landings and deploys. It also writes a former name given by `--repo` under the name now. This change takes those readers out. Each kit is then read by the name its record gives it, and `requests.rec` and the run record are only ever appended to.

`crew kit rename` stays as it stands. The bolt's next unit, `a-repository-is-renamed-by-one-explicit-command`, makes it record 0060's command.

## What Changes

- **No reader maps a kit through `kit.rename` entries.** `kit_now` goes, along with the partition's renames (`renames_in`, `renames_at`, `renames_read`, `runs_at`, `Write.renames`, `Write.renamed`, `Direct.renames`, `Proposed.renames`) and every read through them:
  - a partition's kits, and a kit's partitions;
  - a partition's launches (`launches_now`), a landing's kit, and a fix of main (`main_fix_work`);
  - a landings card's and a record card's key (`record_now`, and `row_gone`'s close for a renamed kit);
  - a source's repository;
  - a kit's landings and deploys on the board and the page.

  crew reads each kit by the name its record gives it.
- **A command given a kit writes it as given.** `bolt new`, `unit add` and `chore add` no longer read `--repo` through renames. Nothing says "written as", and nothing is refused for a former name kept again (`kit_given`, `former_said` and `former_kept_said` go).
- **`crew kit rename` stays as it stands.** These all stay:
  - its grammar, its place in the role table and among the commands a proposal holds;
  - its card block, its act and its entry;
  - what it rewrites, the `Repo` of the plan's Bolt and Unit records.

  Its refusals stay too, all but one: "`<old>` is `<now>` since its rename". That refusal read a former name through the entries, which this change ends. A name an earlier rename renamed is now judged as written, like any other.
- **Entries stay as written and print as before.** A `kit.rename` entry renames nothing crew reads. `crew events` and `crew trace` print it as they do now, and `record.py` is unchanged.
- **Kept: the refusals that name `crew kit rename`.** The main-level host's refusal for a kit it keeps no checkout of still names `crew kit rename <kit> <new>` as the way on, and so does a runner's refusal for a kit it reports not keeping. The next unit decides what they offer, since it decides when the command may run.
- **Kept: where a runner keeps a kit is that runner's report.** The runner's `repositories.rec` stays. Each kit is matched by the name or forge address the plan gives it.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `bolt-plan`: two requirements go: one read a former name under the name now, the other wrote a former name given by `--repo` under the name now. In their place, crew reads each kit by the name its record gives it, `requests.rec` and the run record are only appended to, and a command writes a kit as given. The rename's requirement says what crew does with a name an earlier rename renamed, and that the files it does not rewrite are read as written.
- `drive-state`: a runner's report of a kit is matched by the name or forge address the plan gives the kit, not by its name now.
- `rail-cards`: a landings card no longer follows a rename.
- `run-record`: a `kit.rename` entry renames nothing crew reads.

## Impact

- **Code.** `plugin/lib/plan.py` loses `kit_now`, the renames and every read through them, and `landings_at` again reads only `bolt.land`, once per tip. `plugin/lib/ops.py` and `plugin/lib/page.py` read landings by `Repo` as written. `plugin/lib/runner.py` changes only in its docstrings and its descriptor comment. `plugin/bin/crew`'s usage drops what it says of a name now.
- **Docs and the brief.** README, `plugin/skills/crew/SKILL.md` and `plugin/roles/planner.md` drop what they say of a name now.
- **Tests.**
  - The logic tier's cases that read through renames go or become cases of a kit read as written, in `tests/py/test_kits.py`, `test_kit_rename.py`, `test_main_fix.py`, `test_rail.py`, `test_proposals.py`, `test_ops.py`, `test_page.py` and `test_board.py`.
  - `tests/py/facts.py` and three monkeypatches lose the renames.
  - The contract tier's rename case drops its read through `renames_in`, and pins that the day file holding the entry passes `recfix --check`.
- **Untouched:**
  - `docs/architecture/` and `docs/adr/`: record 0060 already states `plan.22`, and those pages are the design agent's (`docs.7`).
  - `plugin/lib/record.py` and `plugin/lib/cards.py`.
  - The board's views, which keep their shape, so the mod is untouched (`code.8`).
  - `t-journey-plan`, `t-help` and `t-briefs`, and the parser, help and role cases, since the command stays and none of them reads a former name.
  - `tests/moon.yml`, since no end-to-end test is added, removed or reads anything new.
- **Where it lands.** On `bolt/crew-reads-a-kit-by-its-name-alone`, the first of its two units.

## Touches

```
plugin/lib/plan.py
plugin/lib/ops.py
plugin/lib/page.py
plugin/lib/runner.py
plugin/bin/crew
plugin/roles/planner.md
plugin/skills/crew/SKILL.md
README.md
tests/py/facts.py
tests/py/test_kits.py
tests/py/test_kit_rename.py
tests/py/test_main_fix.py
tests/py/test_landings.py
tests/py/test_rail.py
tests/py/test_proposals.py
tests/py/test_ops.py
tests/py/test_page.py
tests/py/test_board.py
tests/py/test_asks.py
tests/py/test_proposal_life.py
tests/py/test_proposal_card.py
tests/contract/test_recfix.py
```
