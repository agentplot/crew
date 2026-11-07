# Design: a unit whose branch stands is refused at its proposal

## Context

A unit or chore of a started bolt is a Flume place of the change or chore kind. Its branch is `<kind>/<name>`: `change/<unit>` or `chore/<chore>` (`runner.reach`, `plan.line_branches`). A drop of the work has the runner drop its place. Flume then removes the place and keeps its branch while it holds a commit whose change the base lacks, naming it once (flume 67). It refuses any launch that would make that branch again while it stands (flume 3). So a name dropped with work stays taken in its repository until someone removes the branch, and no work is lost.

crew checked a new name against the plan (`already has unit`) and the kit's main (`plan.7`, `plan.11`: a change or a chore trailer by it), never against the branch its launch would make. On 2026-11-07 agentplot-planner re-added a dropped unit under its own name. The proposal passed, the user approved a card that could not be carried out (`plan.4`), and Flume refused the launch (signal `afterthought/crew-state:agentplot/main signals/2026-11-07-agentplot-planner-b2717722/01`).

Rules this relies on:
- `read.1`: a repository crew can't place refuses, and names what it could not read.
- `read.2`: the branch is read as Flume reads it, from the tool as it is now.
- `read.4`: crew removes no branch it did not make for the work in hand.
- `plan.1` and `plan.3`: the check runs in the op, so a proposal is checked at its writing and again at its approval, at the tip each is applied to.
- `plan.4`: a card holds only what can be carried out.
- `plan.7` and `plan.11`: the name's own checks, which this one stands beside.
- `state.3`: nothing of a kit's main moves.
- `record.3`: the drop's `Note` is made from names.
- `code.7`: the decisions are functions of facts.
- `code.8`: no view changes.
- `roles.5`: Flume's refusal at launch stays Flume's. crew reads Flume's fact to keep its own plan honest and builds no mechanism Flume holds.
- `tests.4` and `tests.12`: each decision in the logic tier, git's read in the contract tier, one wiring case end to end.

Pages whose area the change touches: `core.md`, `plan.md` (`plugin/lib/plan.py`), `record.md` (`plugin/lib/record.py`) and `docs.md` (README). It departs from none.

The family: Flume owns the refusal and the branch (flume 3, 67, 78). It offers no dry run of a launch (flume 0.17.0, `flume launch --help`), and `flume status` lists places, while a kept branch is no place. So crew reads the one fact Flume reads, whether `refs/heads/<kind>/<name>` exists in the repository it cuts the place in. No second rule is made. crew's check is earlier and narrower than Flume's, and Flume's stays the gate.

## Goals / Non-Goals

**Goals:** a name Flume would refuse to launch is refused when the work is planned, by direct run or proposal, naming the branch, where it stands and the ways on. A drop of launched work says the name stays taken, as it prints and on its entry. The fact is read where the launch would be made, never from crew's memory of a drop.

**Non-Goals:**
- crew removes no branch, and a drop removes none (flume 3, 67, 204).
- The check covers only the acts that bring a name into the plan: an add, a chore's add and a split's new names.
- A unit requeued by `crew bolt drop --requeue` keeps its name. Its kept branch would refuse its launch alike once a bolt it is placed in starts, or once it is moved into a started bolt. Neither `unit move` nor `bolt start` reads branches in this change.

## Decisions

### Decision 1: the check sits with the name's own

`Reads.free(label, kit, names, kind)` runs `name_free`, the kit's main, then `branch_free`, Flume's branch. Every caller of `free` gets both: `op_unit_add` with the command's kind and `op_unit_split` with `unit` for each name it adds. That covers the direct run (`Direct`), the proposal's check at its writing (`check_ops`, `Proposed`) and the approval's apply (`apply_all`, `Proposed`), each at the tip it is applied to (`plan.1`, `plan.3`). A proposal's card drawn reads no host (`Drawn.free`, the name's form alone), as it reads no kit today.

### Decision 2: read where a launch of the kit's work would be made

The repository is the one Flume cuts the place in. That is not the checkout the partition's main-level host keeps (`main_kit`). On deneb, agentplot's runner cuts boomdrive's places in `~/.local/share/flywheel/repositories/agentplot/boomdrive`, while the main level's space keeps `~/Code/github_agentplot/boomdrive` (read 2026-11-07 from `agentplot/runner/deneb`'s `places.rec`).

`runner.launch_repositories` gives each repository once:
- the kit's folder where its work runs, as `runner.where` reads it from the runner that took the newest of the kit's launches (its `repositories.rec`, else Flume's status of a place it carries);
- each runner's own report that it keeps the kit (`repositories.rec`), since a runner whose configuration names the repository may take the launch.

The kit's launches are `runner.kit_launches`, which `kit_at` now shares.

Not taken: the main-level host's checkout. It is a guess at another repository.

### Decision 3: read the branch as Flume reads it

`plan.BRANCHES` runs `git for-each-ref --format='%(objectname) %(refname)' refs/heads/<branch>...` in the folder, on its host through `crew.on_machine`, as every host read is (`code.3`). `runner.refs_standing` keeps only the exact refs. `for-each-ref` also lists a ref below a pattern, and a branch name beside another (`change/a-b`) is no match. This is the ref `git worktree add -b`, Flume's place profile's make, refuses (flume 78). A host that does not answer, or a folder git can't read, refuses naming it (`read.1`).

### Decision 4: refuse where crew can't place the repository; read nothing where no runner has the kit

`launch_repositories` refuses, with its words, in three cases:
- `where`'s own why: a runner unread while none has taken the kit's work, or two runners taking one launch;
- the runner that took the kit's work carrying no place naming its folder;
- a runner keeping two repositories by the kit's name.

Where no runner of the partition has taken any of the kit's work and none reports keeping it, no repository is read and the add passes on its other checks. requests.rec and the runners' answers are append-only claims, so no launch of the partition's has cut a place of the kit, and crew can name no repository to read. That is a reading, not a fallback.

Not taken: refusing there. It would refuse every first unit of a kit new to the runners, with no way on in crew. A branch a person made by hand in a repository no runner reports is outside what crew can read, and Flume still refuses its launch.

### Decision 5: the refusal names the branch, where it stands, and the ways on

`runner.branch_refusal`:

> `<kind> <name> can't be planned in <kit>: Flume's branch <branch> stands in <folder> on <host>, at <commit>, where a launch of <name> would make its place, and Flume refuses a launch that would make it again while it stands; propose the <kind> under a fresh name, or have the planner or the user remove the branch first, which may hold work and which crew never removes (git -C <folder> branch -D <branch>, on <host>)`

The command is given so the person who chooses to remove the branch knows where. Running it is theirs (`read.4`). A chore by a dropped unit's name makes `chore/<name>`, another branch, and passes this check.

### Decision 6: a drop of launched work says the name stays taken

`op_unit_drop`, for work of a started bolt whose launch stands, sets its entry's `Note` to `runner.drop_kept_said` and prints it:

> `Flume keeps <branch> while it holds work bolt/<bolt> lacks, and the name <name> stays taken while that branch stands: a <kind> added as <name> again is refused until the planner or the user removes it`

The words are crew's, made from names (`record.3`), on a field the run record's descriptor already allows, and `record.line` shows it on the drop's line in `crew trace` and `crew events`. A drop of work never launched has no place and says nothing of a branch.

## After deploy

None: the check and the drop's words run in the commands themselves, and the logic, contract and end-to-end tiers prove them.

## Task notes

**1.1** `plugin/lib/runner.py`, under *a name's branch*, reading each branch with `place_branch(work)`, the one reading of a place's branch from its work's name that `built_on_bolt` already uses:
- `kit_launches(requests, kit)`;
- `launch_repositories(reads, launches, kit)`;
- `refs_standing(out, branches)`;
- `branch_refusal(kit, kind, names, found)`;
- `drop_kept_said(kind, name, base)`.

Cases in `tests/py/test_branch_stands.py`:
- `TestTheBranch`;
- `TestWhereALaunchWouldBeMade`: the runner's places, `repositories.rec` with no work taken, nowhere, no folder carried, two by the name;
- `TestTheRefusal`: the words, a fresh name, a chore's own branch.

**1.2** `plugin/lib/plan.py`:
- `BRANCHES`, `branches_in`, `branch_free`;
- `Reads.free` and `Drawn.free` with `kind`;
- `op_unit_add` passes its kind;
- `kit_at` uses `runner.kit_launches`.

`tests/py/facts.py`: `known(standing=...)` and `Known.free` with `kind`.

Cases in `TestAtItsProposal`, through `plan.Proposed`'s own reads with `runner_facts` and `branches_in` given:
- the re-add refused, nothing written;
- a fresh name passes;
- a chore's branch;
- a split's new name;
- crew can't place the repository;
- a drawn card reads nothing.

**1.3** `op_unit_drop`'s `fields`, and `record.line` and `EXTRA`'s comment in `plugin/lib/record.py`. Cases in `TestTheDrop`: a launched unit's, a chore's, work never launched, the entry's line.

**2.1** `tests/contract/test_git.py`, `test_a_branch_flume_kept_is_read_standing_in_its_repository_and_a_name_beside_it_is_not`:
- `BRANCHES` in a checkout and a bare clone, with a kept branch and a live worktree's branch;
- `change/a-b` and `change/b/old` not counted;
- `worktree add -b` refusing a standing branch;
- a folder that is no repository exiting non-zero.

**3.1** `tests/t-journey-cross.sh`, its last case:
- `crew unit drop a` prints the words and records the `Note`;
- with `change/a` in the box's kit checkout and the runner's place naming it, `crew unit add a` is refused, read over ssh in that folder, nothing written, the branch still standing;
- `crew unit add a-again` is added and launched.

**3.2** README's plan section, `plugin/skills/crew/SKILL.md` and `plugin/bin/crew`'s usage header for `crew unit` and `crew chore` (`docs.2`).
