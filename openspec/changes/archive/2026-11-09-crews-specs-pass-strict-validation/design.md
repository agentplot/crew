## Context

openspec 1.16.0's spec validation warns on a requirement whose text is past 500 characters (`MAX_REQUIREMENT_TEXT_LENGTH`). Its text is every non-blank line under the `### Requirement:` header, down to the first `####`, trimmed and joined with a newline. `--strict` counts a warning as a failure. On crew's main at 83c9a149, `openspec validate --specs --strict` passes 4 specs and fails 23, each on that warning alone: 140 requirements. A change's own `--strict` validation does not catch every case: it checks an ADDED requirement's length, but leaves a MODIFIED one alone. crew's gate runs no openspec. So a change whose archive grows a requirement past the limit lands green, as `a-drive-set-loses-no-drive-and-no-record` did with drive-setup's "A set is one entry naming what it changed" (326 characters to 613; its verify report).

**Area pages this change touches:** `docs.md` (`docs.4`: a spec changes only through a delta; `docs.6`: every scenario is one a check proves; `docs.7`: a unit's change never edits `docs/architecture/` or `docs/adr/`) and `tests.md` (`tests.2`, `tests.5`, `tests.10`, `tests.11`).

## Goals / Non-Goals

**Goals:** every spec under `openspec/specs/` passes `openspec validate --specs --strict`, each long requirement split into requirements that together say the same. The suite fails a merge that would land a spec failing it.

**Non-Goals:** any change of behaviour, or of what a requirement says. Open changes under `openspec/changes/`: their own validation is each change's build's. Citations of spec requirements that were already stale before this change (64 in `plugin/` and `tests/`, read 2026-11-09).

## Decisions

### 1. A split is a removal and its parts added

Each long requirement is listed under `## REMOVED Requirements`, with a *Reason* and a *Migration* naming its parts. Its parts are listed under `## ADDED Requirements`. `openspec archive` refuses a MODIFIED block that drops any of the current requirement's scenarios (`specs-apply.js`, `diffScenarioNames`). So a requirement cannot keep its name and hand some of its scenarios to a new one. Not taken:

- A MODIFIED requirement keeping every scenario, plus ADDED parts with scenarios of their own. Those would be new scenarios that no check proves (`docs.6`; `openspec/config.yaml`'s spec rule).
- Moving each requirement's detail into its scenarios. That is openspec's other remedy, but the chore asks for a split, and a scenario's steps would then say more than its check asserts.

### 2. A part keeps the original's sentences

Each requirement is cut at sentence boundaries. Each sentence goes to the part whose one behaviour it states. A sentence is edited only where it no longer stands alone once cut: its subject or referent is restored ("It SHALL" becomes "`crew drive set` SHALL"). A list's lead-in may be repeated in each part that takes some of its items. A numbered list whose first item to apply wins keeps its numbers, and each part's lead-in says which items come before it. A sentence past 500 characters on its own is cut at a clause boundary, its subject repeated. A sentence or list item that had no SHALL of its own takes one where it stands alone in a part, saying what it said ("is its raise" becomes "SHALL be its raise"). Each part holds SHALL or MUST and is within 500 characters. Each scenario of the original goes, word for word, to the part whose behaviour it proves. Every scenario is carried exactly once, and every part has at least one. A part with no scenario of the original's to take gets a new one only where an existing check already proves it. Its steps say only what that check asserts (*Task notes* 2.1 names each one and its check).

### 3. A split requirement's parts follow the spec's other requirements

`openspec archive` adds a requirement at the end of its spec. So the parts follow the requirements that were not split, in the order of the requirements they came from, each requirement's parts together. Not taken: removing and re-adding every requirement after the first long one to keep the spec's order. A requirement re-added under its own name conflicts with its removal (`specs-apply.js`, "requirement present in multiple sections"), so every one of them would need a new name.

### 4. Each part is named for its behaviour, and citations follow

A part's name is a plain sentence saying its one behaviour, in its spec's voice. It never repeats the original's name exactly, which openspec would refuse. Every citation of a split requirement's name in `plugin/` and `tests/`, a docstring or comment, names the part that holds what it cites. Where a docstring or comment uses a requirement's words as plain prose, as `crew`'s usage and `page.py`'s deploys view do, it is left as it is.

- **Within the specs.** A requirement that quotes a split one by name quotes the part that holds what it quotes. Inside a split requirement, the part takes the new name; in two of drive-state's requirements that are not split, a MODIFIED block, every scenario kept, changes the quote alone: "A preview names its host, its work, its repository, its branch and its revision" and "A bolt's work is its base place's and its preview's".
- **Rule pages.** The citations in `docs/architecture/` are the design agent's to amend after the landing (`docs.7`): `plan.md` line 41 (drive-state "A commit names its run-record entry"), `plan.md` line 61 (bolt-plan "The file's order and dependencies are the plan") and `teams.md` line 44 (main-level "The main level is one herdr workspace"). *Task notes* 2.2 names the part each would cite.
- **Records.** The records in `docs/adr/` are dated, and keep the names they were written with.

### 5. The gate is an end-to-end test of crew's specs

`tests/t-specs.sh` runs `openspec validate --specs --strict` in crew's checkout, with the machine's openspec, which `tests/run` already requires of every host. Its `# Reads:` line names `openspec/specs/` and `openspec/config.yaml` (`tests.10`), so a change to a spec makes its task affected. Its task is tagged `check-full`, which crew's sluice policy requires of every bolt and of main (`tests.5`).

- **The check bites.** It first proves, on scratch specs of its own, that openspec takes a requirement of 500 characters and refuses one of 501. An openspec that checks no length fails the test, rather than passing crew's specs unread. `t-word` checks its own pattern in the same way.
- **No service.** openspec runs with `DO_NOT_TRACK`, `OPENSPEC_TELEMETRY=0` and `OPENSPEC_NO_UPDATE_CHECK`, so the test reaches no service (`tests.11`).
- **Scope.** Open changes stay outside it. Five of them already fail `--strict` on scenarios their MODIFIED blocks omit, and a change's validation is its build's.

Like `t-word` and `t-docs`, the test checks crew's text rather than the command's wiring. The tiers of `tests.11` give such a check no other place, and it pins no openspec behaviour crew's code assumes, so it is no contract test. Not taken: a moon project of `openspec/` with a lint task of its own. `tests.5` names crew's tasks as the tiers', the mod's, one per end-to-end test file and the flake's four, so another project would amend that rule, which is the design agent's (`docs.7`).

### 6. Change authors are told the limit

`openspec/config.yaml`'s rules for a change's specs gain a rule: a requirement's text is at most 500 characters as `openspec validate --strict` counts it, MODIFIED among them, which a change's own validation does not count, and a longer one is split. CLAUDE.md's *Specs* says `t-specs` holds every spec to it.

## Risks / Trade-offs

- [An open change's delta names a split requirement] → Its MODIFIED fails at archive ("not found"). When it is built, its delta moves onto the parts. These open changes modify a split requirement: `a-started-bolts-kit-folder-is-read-as-main-reads-it` (drive-state), `a-users-step-of-any-length-gets-its-card` (rail-cards, two), `an-offer-card-shows-the-step-the-deploy-waits-on-first` (main-level), `blocking-findings` (bolt-plan, plan-proposals), `crew-fetches-nothing-in-the-runners-clone` (main-level), `crew-keeps-no-card-wait-and-a-row-carries-its-submission-number` (card-sessions two, rail-cards, review-batches three), `curation-and-agenda` (main-level) and `no-worktree-holds-main-or-a-bolt-branch` (merge-gate). Five of them already fail `--strict`. Not taken: rewriting them here. None is this chore's, and each holds text of its own that is not built.
- [A host's openspec is older than 1.16.0, with no length check] → `t-specs` fails on that host, saying openspec took a requirement of 501 characters, and the host's openspec is updated through swancloud's packages.
- [A branch in flight grows a requirement this change split] → Its merge conflicts on the spec, or its archive fails on the removed name. Either is resolved the usual way, by a fix that takes main in.
- [The spec's order] → A split requirement's parts are read at the end of the spec, away from the requirements they once sat among (Decision 3).

## Departures

None.

## After deploy

None. The specs and the test are read in the checkout, and `t-specs` proves them at every merge.

## Task notes

**1.1** `tests/t-specs.sh`: a scratch project per length under `$T`, its one spec's one requirement exactly that many characters, with its SHALL and a scenario. 500 passes and 501 fails "1 failed". Then `openspec validate --specs --strict` in `$CREW` passes, its output saying " 0 failed". Run `tests/moon-tasks` and commit `tests/moon.yml`.

**1.2** `openspec/config.yaml`, `rules.specs`, a second rule; CLAUDE.md, *Specs*, one sentence.

**2.1** The delta specs under `specs/`, one per spec, as Decisions 1 to 4 have them: 140 requirements removed and 371 parts added, 15 of the parts with a new scenario. A trial archive in a scratch copy is checked before the real one. Every scenario of every spec is still there, word for word. Every requirement not split is unchanged but drive-state's two quotes. No spec quotes a removed name. `openspec validate --specs --strict` passes all 27. The new scenarios, and the check that proves each:

- bolt-plan "A start's launches name no host or stream, and a start reads no host", *A start reads no host*: `tests/py/test_bolt_commands.py`, `TestStart.test_a_start_launches_the_base_place_then_its_pieces_in_one_write_reading_no_host`, whose fixture fails on any read of a host.
- card-sessions "The sweep's try of a landings card is its raise, recorded as the card's change", *The sweep tries a landings card by raising it*: `tests/py/test_rail.py`, `test_the_sweeps_try_of_a_landings_card_is_its_raise_and_refused_while_a_row_still_stands_unread`.
- drive-setup "A set appends one entry naming the keys it changed", *A set whose state push is refused*: `tests/t-drive-set.sh`, "a set whose state push is refused keeps the teams file naming pat, its drive.set entry and a refused state.init".
- fleet-page "A drive's block names no team", *A drive's block with no team*: `tests/py/test_fleet.py`, `TestNoTeams.test_a_drives_block_names_no_team_slot_or_conductor`.
- fleet-page "No kit names a team that builds it", *Kits with no team*: `tests/py/test_fleet.py`, `TestKits.test_each_kit_once_in_the_boards_order_naming_no_team`.
- main-level "A kit's deployer asks crew for each deploy with its release notes and steps", *A deploy offered with its notes and steps*: `tests/t-journey-ops.sh`, "an offer is a rail row whose card crew raises in main-level ops's name with the notes and steps it was handed, …".
- main-level "A fix of main takes no team, and its drop drops its launch", *A fix of main dropped*: `tests/py/test_main_fix.py`, `test_drop_drops_its_launch`.
- main-level "Main-level ops answers a landing that does not land from the runner's report alone", *A landing fix that asks*: `tests/t-briefs.sh`, "main-level ops starts no fix Flume's landing fix covers, and one past its bound".
- operator-agent "An operator on a box sends a teams change to a drive on a Mac", *A teams change from a box*: `tests/t-briefs.sh`, "the operator carries what is sent to it in the sender's words, and sends a teams change from a box with crew send to a Mac's drive".
- plan-proposals "A replaced card Pending You cannot change in place is withdrawn and followed", *A rewrite that moves its card to another form*: `tests/py/test_proposal_life.py`, `test_a_rewrite_that_moves_its_card_to_another_form_withdraws_it_while_it_waits_and_its_new_version_follows_it[one-list-to-lists]`.
- plan-proposals "A rename asks no question of its own", *Renames alone*: `tests/py/test_proposal_card.py`, `test_a_rename_is_a_block_naming_both_names_and_no_bolt`.
- rail-cards "An agent adopts crew's card by get_request and runs no pendingyou command", *A brief that asks the user forbids Pending You from npm*: `tests/t-briefs.sh`, "the planner, main-level ops and the design agent carry one question discipline".
- rail-cards "A batch's card's title and words say what it is about and where notes go", *A batch's title and the opening of its summary*: `tests/py/test_cards.py`, `test_its_title_is_what_the_batch_is_about_and_its_body_opens_with_what_it_asks`.
- rail-cards "A record's status records whether its card offered alternatives", *A record's status says its card offered alternatives*: `tests/t-cards.sh`, "a record a rule decided is raised as one choice, …, its status recording that its card offered them".
- rail-cards "A card answered in a pane records that it was", *A card closed as answered in its owner's pane*: `tests/py/test_card_commands.py`, `test_a_card_closed_as_answered_in_its_owners_pane_records_the_pane_as_its_answer`.

test-suite's "crew's specs pass openspec's strict validation" adds two scenarios, both proved by `tests/t-specs.sh`.

**2.2** The citations, read by a search for each removed requirement's name with its whitespace free, across a line break and a comment's `#`, in `plugin/`, `tests/`, README, CLAUDE.md, `nix/`, `flake.nix`, `.config/` and `openspec/config.yaml`: 143 of them, all in `plugin/` and `tests/`, each now naming its part, but the two of plain prose Decision 4 leaves. For the design agent, after the landing, the rule pages' citations (`docs.7`):

- `plan.md`, `plan.2`'s details: drive-state "A commit names its run-record entry" is now "Each commit on a drive's branch names the run-record entry it describes or adds".
- `plan.md`, `plan.13`'s details: bolt-plan "The file's order and dependencies are the plan" is now "A unit's After holds its launch until that work has landed on the bolt".
- `teams.md`, `teams.7`'s details: main-level "The main level is one herdr workspace" is now "Every agent crew starts is greeted once per start".
