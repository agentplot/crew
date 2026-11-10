# Design: crew bolt land reads the runner's report alone

## Context

The bolt `crew-reads-every-end-from-the-runner` took main in at `773784c` by its take-main fix (`plan.8`), merge `f631fe94`. Its change, `crew-reads-each-pieces-end-from-the-runners-report`, retires record 0062's stopgap, and its Decision 7 says what becomes of main's fallback once the bolt meets main:

- `main_landed` and its call in `started_land` go. A started bolt closes once `runner.landing_of` reads its base place landed, the record Flume holds for the runner after the base place's tidy among them.
- A bolt started before bolts were base places is closed by the crew that started it, and `crew bolt land` here refuses it in `runner.legacy_said`'s words.
- Main's scenario "A base place the runner no longer carries" goes with the requirement the change removes.

The merge built all three and resolved the conflicts in `openspec/specs/` to the bolt's side. This change says the rest in the specs: two bolt-teams requirements that still name main's fallback, and merge-gate's scenario that batch 27's review found misnamed.

**Rules relied on:**
- `plan.8`: a take-main fix merges main into the bolt, the conflict being the bolt's.
- `roles.5`: a stopgap named in its record is retired by a change of its own.
- `roles.9`: crew reads Flume's ends through the runner, never from anywhere but its report.
- `read.1`: what crew cannot read closes nothing, and no fallback stands in for it.
- `code.7`: `landing_of` and `landing_refused_said` stay decisions on facts.
- `docs.2`, `docs.4`.

It departs from none.

**Area pages this change touches:** `plan.md` (`plugin/lib/plan.py`), `teams.md` (`plugin/bin/crew`'s usage), `briefs.md` (`plugin/skills/crew/SKILL.md`), `tests.md` (`tests/`), `docs.md` (`README.md`, `openspec/`). No rule page or record is edited here (`docs.7`).

## Decisions

### 1. A started bolt closes at Flume's commit alone

`started_land` reads the base place's landing from the runner's report and closes the bolt at Flume's commit once it reads landed, as the bolt built it before main's reconciliation. A base place Flume tidied after landing is read from the record Flume holds for the runner, which the runner carries as its status and `flume_facts` reads at `<location>@<at>` as any status. Nothing reads the kit's main for it: `stages_for` and `survey` are not called.

Not taken: keeping main's fallback for a base place the runner no longer carries. That is record 0062's stopgap, which the bolt's change retires, and a fallback to another tool's record is what `read.1` and `roles.9` rule out. A base place launched before its host's runner named itself a recipient, and tidied, reads as last carried and is refused; its way on is the bolt's drop by proposal, as for any piece so read (the bolt's Decision 3).

### 2. A bolt started before bolts were base places is refused

Such a bolt has no launch of `bolt/<bolt>`, so `started_land` refuses it in `runner.legacy_said`'s words, "<bolt> was started before bolts were base places and lands under the crew that started it, so crew bolt land closes nothing of it here". The crew that started it lands and closes it.

Not taken: main's close at the landing its kit's main holds. That reads `Sluice-From` on main, the stopgap again.

### 3. merge-gate's scenario names what it checks

"A landing read from the bolt's own landings" becomes "A head only a landing commit names": the head's piece is named only by a landing commit, the runner having last carried it at submitted, and the verification reads none. Its steps are unchanged.

OpenSpec 1.16 refuses a MODIFIED requirement that drops a scenario the spec holds, and a requirement both REMOVED and ADDED under one name, so a scenario is renamed only with its requirement. The requirement is removed and added again whole as "A bolt's verification is its work's landing at its head, as the runner reports it alone", every other scenario as it was. bolt-teams "A bolt's proof is its verification" and rail-cards "The landing card is posted once the bolt's verification is green" cite it by name, so each is modified to cite the new one, its scenarios unchanged. `tests.5`'s details cite the old name; under `docs.7` the design agent's hand amends that citation after the landing, read from main's log.

Not taken: keeping the scenario's name, as the bolt's change did (its Decision 6), which batch 27's review found misleading.

## Risks / Trade-offs

- **[A bolt whose base place the runner no longer carries stays in the plan]** → Only a base place tidied before its host's runner named itself a recipient. Its row reads as last carried, and the planner drops it by proposal.

## Migration Plan

None. The code is in the merge.

## After deploy

None: every scenario here is a logic case or `t-journey-land`'s.

## Task notes

**1.1** `plan.started_land`, built in the merge. Cases in `tests/py/test_landing.py` `TestCrewBoltLandOfAStartedBolt`, whose fixture makes `stages_for` and `survey` raise: `test_a_base_place_held_for_the_runner_landed_closes_at_flumes_commit` ("A base place held for the runner", over `flume-0.20.0/landed-held` with its commit set), `test_a_base_place_the_runner_no_longer_carries_is_refused_whatever_main_holds` ("A landing main holds that the runner does not report"), `test_a_bolt_not_read_landed_is_refused_naming_its_outcome_and_records_nothing` ("Closed by hand before it landed"), `test_a_bolt_started_before_bolts_were_base_places_is_refused` ("crew bolt land refuses it").

**1.2** `tests/t-journey-land.sh`'s last landing: Flume lands z on main, GitHub deletes `bolt/z`, the runner carries the records Flume holds for it of z's base place and chore (`held_status` in `tests/lib.sh`), and ops's `crew bolt land z` closes z at Flume's commit "as the runner reports it".

**1.3** `tests/py/test_stages.py` `test_a_head_held_for_the_runner_reads_green_and_one_only_a_landing_commit_names_reads_none` cites "A head only a landing commit names", and `tests/py/test_runner.py` `TestVerification` cites the requirement's new name.

**1.4** README, the skill and `crew`'s usage say `crew bolt land` reads no landing commit on its kit's main and refuses a bolt started before bolts were base places; `tests/t-docs.sh` pins "no landing commit on its kit's main read for it" in each and "main holds its landing" in none.
