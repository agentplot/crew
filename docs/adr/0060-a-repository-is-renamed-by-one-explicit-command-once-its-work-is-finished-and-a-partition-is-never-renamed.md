---
status: accepted
date: 2026-11-07
decision-makers: the user (a repository is renamed in crew by one explicit command once its work is finished; a partition is never renamed); the design agent (what the command renames and refuses, from record 0055's reading)
---

# 0060. A repository is renamed by one explicit command once its work is finished, and a partition is never renamed

Status: accepted by the user on 2026-11-07, on their card.

Deciders: the user, 2026-11-07. In agentplot-operator's pane, on the change `crew-renames-no-kit`: "To be clear I'm referring to renaming the repos. I think we do want a rename function for renaming the state but it would be something that's done explicitly. Just to rename the state, it should be simple. Now that I think about it, I don't know how to coordinate that with removing the repo and adding it back so I don't know what to do about that". On agentplot-design's card, of the repository: "One explicit crew command, after the work is finished". Of a partition: "I don't think we want to have a partition rename. I imagine that in the cloud we'd have a slug that either can't be changed or we'd refer to and use a UUID on disk (although it would be easier for the user to navigate the folders if it was a slug)". What the command renames, what it refuses and the order around it are the design agent's, from record 0055's reading of crew's records.

Amends: record 0055 (rejected), whose decisions 2 to 6 this record takes up for an explicit command alone; the rule `record.4`; adds `plan.22`. Sources: the user's words above; Boomdrive's record 0021 and Flume's record 0053, where the user said a repository moves by removal and addition and no tool follows a rename in flight; record 0055; signal `signals/2026-11-07-agentplot-planner-cbc41169/01` to `/03` on agentplot/main of afterthought/crew-state (what swancloud's relabel to afterthought left behind).

## Context and problem statement

On 2026-11-06 and 2026-11-07 the user ruled that no tool follows a repository's rename in flight: its work is finished, it is removed, it is renamed apart, and it is added back. Record 0055, which renamed crew's records of a kit, was rejected when crew moved to agentplot, and the change `crew-renames-no-kit` was launched to take `crew kit rename` out. The user then said they meant repositories: crew's state should still be renamed, explicitly, and they weren't sure how that fits removing and adding back.

The same day, swancloud's partition was relabelled afterthought in the host file. The cards its roles held, the answers on two batches and two bolts' units were left under the old name, reaching no one (signals `cbc41169/01` to `/03`).

## Considered options

**A repository's rename.**

1. **One explicit crew command, refused until the repository's work is finished, run between its removal and its adding back** (chosen, the user's).
2. **No rename in crew.** The repository is added back under its new name with an empty plan, and its history stays under the old one. Not taken: the user wants the state renamed.
3. **A rename followed in flight**, as `crew kit rename` and its readers through `kit_now` did. Ruled out by the user's words on records 0021 and 0053.

**A partition's rename.**

1. **None: a partition's label is fixed once it is made** (chosen, the user's).
2. **The same explicit command, refused until the partition's work is finished.** Not taken, by the user's answer.

## Decision

1. **The user's: a repository's state is renamed by one explicit command, once its work is finished.** `crew kit rename <old> <new>` renames crew's records of the repository, in one act. Nothing renames on its own, and no reader maps a former name.
2. **The order around it.** The repository's work is finished or dropped. The repository is removed from the runner, Flume and sluice, each by its own removal. It is renamed on its forge. crew's rename runs. The repository is added back under the new name. crew's rename is refused while any host's runner still keeps `<old>`, so it never runs before the removal.
3. **What finished means.** The rename is refused, naming what stands, while any of these remains:
   - a live place of the repository's, as Flume holds it;
   - a bolt or a fix of its work not landed;
   - an open card whose key names it, `land/<old>` or `record/<old>/<n>`;
   - a review batch carrying its work that the user hasn't answered;
   - an open proposal whose `Do` lines name it (`plan.4`).
   So the rename closes and raises no card, and changes nothing under the user.
4. **What the rename renames.** Every record a reader matches a repository by, as record 0055's decision 2 lists them: the `Repo` of the plan's records, each launch's `Repo` in `requests.rec`, the run record's entries' `Repo`, `On` and `From`, and a Source naming a decision record's repository. What no reader looks a repository up from stays as written, as 0055's decision 3 has it. `<old>` given to any command afterwards is refused as a repository the partition doesn't have (0055's decision 4).
5. **The append-only rules keep their purpose.** `requests.rec` and the run record are written only by appending, except for the rename's rewrite of the repository's name, one commit with its `kit.rename` entry. The commit holds what each record said before (`state.1`), so no history is lost (`record.4`, amended).
6. **The user's: a partition is never renamed.** Its label is fixed once it is made. A label that changes in the host file is a partition removed and another added: the removed partition's work is finished first, by hand, and its roles' cards are withdrawn (the fix `a-card-whose-role-left-the-fleet-is-withdrawn`). How a hosted Boomdrive names a drive on disk, a fixed slug or an identifier, is Boomdrive's to design.

## Consequences

- `plan.22` says the rename, and `record.4` is amended for its one rewrite, both marked proposed.
- The change `crew-renames-no-kit` is dropped: it took `crew kit rename` out. One crew change replaces it once this record is accepted: the explicit command as above, refused until the repository's work is finished, and `kit_now` and every read through renames taken out. The held branch `fix/a-kit-rename-renames-every-record-naming-it`, built for record 0055, holds the renaming of every record and may be its start.
- madswan's former names, `tailrace` and `flywheel-cloud`, are renamed by the command once it ships, each once its work is finished.
- The user's words on a drive's name on disk go to Boomdrive as a signal.

## Amendment, 2026-11-12: a drive that replaces another takes its unstarted queue, and the other's history stays on its own branch

Status: proposed to the user on 2026-11-12, as `briefs.15` has it; accepted only on their yes. You asked for the agentplot drive to be renamed boomdrive, and crew never renames a drive, so boomdrive starts fresh: agentplot first finishes or drops what it has running, then everything planned but not yet started moves to boomdrive, and agentplot's old history stays where it is. Nothing new is built, so deneb's switch to the Boomdrive flake waits only for agentplot's running work. The other way is to build a rename command in crew first, which keeps the history under the new name but pushes the switch back.

Deciders: the user, 2026-11-12, in agentplot-ops' pane, on deneb's drives in afterthought/swancloud's `machines/deneb/boomdrive.nix` (branch `deneb-is-on-the-boomdrive-flake`): "[accounts.personal.drives.agentplot] that drive gets renamed to boomdrive and drops", then "the agentplot repos". Point 6, the user's, rules that this is a partition removed and another added. Which of agentplot's work the new drive takes, and how, is agentplot-design's. Whether point 6 is loosened to a rename of a drive's whole state is the user's, on this amendment's card.

Sources: agentplot-ops' and agentplot-planner's tells of 2026-11-12, which relay the words; the planner's question, which recommends one crew act that carries a drive's state to a new label; agentplot's plan at afterthought/crew-state `agentplot/main` 77c7346, which holds no work in the six repositories that leave.

- **agentplot is removed and boomdrive added (point 6, the user's).** The boomdrive drive is a partition of its own. It has its own state branch, Flume stream, herdr session, Pending You area and main level, whose roles are named boomdrive-design, boomdrive-planner, boomdrive-ops, boomdrive-operator and boomdrive-reviewer. Nothing reads agentplot for it. Its repositories are the boomdrivedev ones. agentplot/agentplot, agentplot-kit, boomdrive-web, claude-honcho, flywheel-next and nix-claude-plugins leave with agentplot, and join no drive unless the user names one.
- **agentplot's work is finished first.** Before deneb's host file drops agentplot, every started bolt has landed or been dropped, every landing has been sent or withdrawn, every proposal has been decided or withdrawn, and every card of agentplot's roles has been withdrawn. Until then deneb keeps the drive agentplot, and the new name deploys after.
- **The new drive takes the unstarted queue (agentplot-design's).** Every bolt not started and every unit and chore still queued goes into boomdrive's plan with its intent, order and sources. Each one names as a source the commit of `agentplot/main` it came from, so no queued work is lost and its history is one reference away. Not taken: an empty plan the planner proposes again, which loses the queue's order and sources.
- **agentplot's history stays where it was written.** `agentplot/main` keeps its plan, proposals, moves, signals and run record as they stand, and is read as a finished partition. Nothing is rewritten.
