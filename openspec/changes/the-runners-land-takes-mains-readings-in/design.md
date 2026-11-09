# Design: the runner's land takes main's readings in

## Context

The bolt `crew-lands-through-the-runners-land-message` took main in at `0563aa90`. Its fix kept both sides' intents (`plan.8`), and two pairs of requirements now in `openspec/specs/` disagree (proposal, *Why*). This design says how the merge reconciled them. It touches the area of `docs/architecture/plan.md` (`plugin/lib/plan.py`) and relies on these rules:

- `plan.8`: a take-main fix merges main into the bolt, the conflict being the bolt's.
- `plan.21`: a bolt whose landing main shows is recorded landed by the first act of crew's that reads it.
- `read.1`: what crew cannot read closes nothing.
- `code.7`: the readings that decide stay facts.
- `roles.5`: crew runs no sluice command, a card's preview included.

It departs from none.

## Decisions

### 1. A started bolt closes at either reading

`started_land` reads the runner's report first (`runner.landing_of`). Where that reads landed, the close is as the bolt built it: at Flume's commit, its `bolt.submit` outcome recorded in the same commit where no read recorded it.

Where it does not, `main_landed` reads the kit's main as main's change reads it: `stages_for`, which seeks the bolt's landing on main's first-parent line since its start (`gather.main_landing`), and the pieces through that landing. Main holding the landing with every unit and chore read landed closes the bolt at the landing's commit. Its `bolt.land` names the kit and that commit, and no `bolt.submit` is written, since the runner reported nothing. Main holding the landing with a piece not landed refuses, naming the piece. Main holding no landing, or a kit crew can't read, refuses as the runner's report has it (`read.1`).

So a bolt started before bolts were base places, which lands under the crew that started it (bolt-teams), closes here once that crew's landing is on main. A base place the runner no longer carries closes too. Nothing of crew's lands either: the reading is git's of main, and no tool is run (`roles.5`).

Path not taken: refusing a bolt started before bolts were base places outright, as the bolt had it. That would leave such a bolt in the plan once its host's pin moved, with nothing to close it.

### 2. `bolt/<bolt>` serves its base place and its preview

`runner.WORK` takes `bolt/<bolt>` for the base place's requests, and `PREVIEW_WORK` takes it, or `unit/<unit>`, for a preview. A request names a launch by `Of`, and `launch_of`, `lands_of` and `previews_standing` each read their own act, so a preview and the base place's requests never stand for one another. What main's rule kept out, a launch of a bolt's work that is no base place, is still refused: a launch of `bolt/<bolt>` must name `crew/bolt`. A retry or drop naming a preview names no launch.

Path not taken: a work name of its own for a preview, such as `preview/<bolt>`. That would change the runner's reading of a preview's work, which Boomdrive holds.

## Risks / Trade-offs

- **[A close reads more when the runner's report does not read landed]** → `crew bolt land` reads the kit's main once more for a bolt not yet landed, a read `crew bolts` makes already.

## Migration Plan

None. The code is in the merge.

## After deploy

None. Every behaviour here is proved by a check in crew's tiers.

## Task notes

**1.1** `plan.main_landed` and `plan.started_land`. Cases: `tests/py/test_landing.py` `TestCrewBoltLandOfAStartedBolt`, its main-held cases, and `tests/py/test_stages.py` `TestABoltLandedOnMain.test_crew_bolt_land_reads_the_landing_main_holds_and_names_a_piece_it_does_not_hold`.

**1.2** `runner.request_refusal`, `PREVIEW_WORK`. Case: `tests/py/test_runner.py` `TestPreviewRequest.test_a_bolts_work_is_its_base_places_and_its_previews_alone`.

**1.3** `tests/t-journey-land.sh`: the preview steps, and `z` closed by `crew bolt land` at the landing main holds once the runner carries no place of its work.
