# A repository is renamed by one explicit command once its work is finished

## Why

`crew kit rename`, as `a-kit-renamed-on-its-host-is-renamed-across-the-plan` built it, follows a rename in flight. It rewrites the plan's `Repo` while the repository's work still stands. Everything else stays under the old name: launches in `requests.rec`, the run record's landings and card objects, and decision-record sources. Readers were left to map those through `kit.rename` entries. swancloud's relabel to afterthought on 2026-11-07 showed what happens when a name moves under standing work: cards, batch answers and two bolts' units were left under the old name, reaching no one (signals `2026-11-07-agentplot-planner-cbc41169/01` to `/03`).

The user ruled on 2026-11-07 (record 0060, accepted on their card). Of the repository: "One explicit crew command, after the work is finished". Of a partition: "I don't think we want to have a partition rename." `plan.22` and `record.4` now say this. This change builds it.

## What Changes

- **The rename renames every record a reader matches the repository by**, in one commit with its `kit.rename` entry:
  - the plan's Sources that name a decision record in the repository;
  - each request's `Repo` in `requests.rec`, and the `Work` of a fix of its main;
  - the run record's entries on the drive's branch: their `Repo`, and each object of their `On` and `From` built on the name.

  `Count` is every record renamed. What no reader looks a repository up from is left as written: Goals, Intents, closed proposals, signals, moves, `asks.rec`, card keys and every earlier `kit.rename` entry.
- **The rename is refused while the repository's work stands**, naming what stands. That means any of:
  - a bolt, unit or chore of the plan;
  - a fix of its main, or a role's work in it, that has not landed;
  - a place Flume holds live;
  - an open `land/<old>` or `record/<old>/<n>` card;
  - an unanswered review batch holding its work;
  - an open proposal whose `Do` names it.
- **The rename is refused while any host still keeps `<old>`.** A host's keeping is read from its runner's `repositories.rec`, or, where that runner reports none, from the host's spaces in the hosts file. The partition's main-level host is always among the hosts read. The check that the host already keeps `<new>` goes, since the repository is added back under `<new>` only after the rename. A started bolt is no longer renamed under its work.
- **Running the rename again renames what an earlier one left.** `<old>` may be any name a record still holds. The rename first pushes the entries its own host kept unpushed, so those are renamed with the rest.
- **`requests.rec` stays append-only, except for the rename.** The append check reads the tip's requests as the rename leaves them.
- **A proposal's card draws the rename** as a block naming both names, with no bolt or unit under it.
- **A partition is never renamed.** No crew command renames a label. A label that changes in the teams file is read as another partition.
- README, the crew skill, `crew`'s usage and the planner's brief say all of this.
- Not in this change: taking out `kit_now` and every read through `kit.rename` entries. That is the unit `no-reader-maps-a-kits-former-name`, in the same bolt.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `bolt-plan`: the rename of a kit renamed on its host goes. In its place, a repository is renamed by one explicit command once its work is finished, and the rename renames every record a reader matches the repository by.
- `run-record`: the rename's entry counts every record it renamed and is left as written by a later rename. The branch's copy of an entry is rewritten only by the rename.
- `drive-state`: `requests.rec` is changed only by appending, or by a rename. A partition is never renamed.
- `plan-proposals`: the rename's block on a proposal's card names both names and no bolt or unit.

## Impact

- `plugin/lib/plan.py`:
  - `op_kit_rename`, `rename_refusal` and `renamed_in`;
  - new `renamed_kit`, `renamed_object`, `renamed_source`, `renamed_field`, `rename_rec`, `rename_branch`, `rename_standing`, `rename_kept` and `proposal_names`;
  - `appended`;
  - `Write`, which gains `paths`, `texts` and `renaming`.
- `plugin/lib/cards.py`: `renamed_drawn`.
- `plugin/lib/record.py`: the descriptor comment on `kit.rename`'s `Count`.
- `plugin/bin/crew`'s usage, `README.md`, `plugin/skills/crew/SKILL.md` and `plugin/roles/planner.md`.
- Tests:
  - new `tests/py/test_repository_rename.py`;
  - changed `tests/py/test_kit_rename.py`, `tests/py/test_proposal_card.py`, `tests/py/facts.py`, `tests/contract/test_recfix.py`, `tests/t-journey-plan.sh` and `tests/t-briefs.sh`.
- No change to the views or to crew's mod (`code.8`): a partition's kits keep their shape.
