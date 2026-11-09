# Design

## Context

**The user's word.** agentplot/boomdrive's record 0028, accepted by the user on 2026-11-07, names an **account**, what a runner enrolls with a control plane, and a **drive**, a body of work of one account: its repositories, one Flume stream and one branch of the account's crew state. It reads "drive" where record 0026 said "partition", and says "crew's own word 'partition' becomes 'drive' with crew's rename (crew record 0054)". "A drive's name is its stream's and its crew branch's. So a host's drives keep the names they run under today, and none is renamed." crew's record 0054 made a partition's loop and branch its drive (`plugin/lib/plan.py` line 4: "A drive is a partition's loop, named by its label"); here the partition itself is the drive. The user, 2026-11-08, in agentplot-design's pane (signal `2026-11-08-agentplot-design-c2aff6f4/01-no-code-carries-a-transition`, `agentplot/main` of afterthought/crew-state): "I want the system to be built the way it should be and then have agents fucking fix the data transition as necessary". Boomdrive's record 0032 (accepted 2026-11-08) relies on this rename: "crew's rename of 'partition' to 'drive' (crew record 0054) moves in the change that moves crew's version", and the next unit of this bolt, `another-module-gives-crew-a-drives-machine-and-state`, builds on `services.crew.settings.drives`.

**Two partitions in crew, read 2026-11-08.** crew writes "partition" about 3,500 times, in two senses:

- **crew's own**, a label with its main level and its branch `<label>/main` (`afterthought`, `agentplot`, `madswan`, `wldn`): the teams file's `partitions`, `crew.partition_of`, `plan.partition_kits`, `crew send <partition>`, every brief and spec. This is the drive.
- **swancloud's**, the herdr session grouping of `lib/partitions.nix` (`personal`, `business`, `agentplot`, `clients/willdan`), which the hosts file gives each session as `partition` and which crew's teams file repeats in each entry as `partition` (deneb's file of 2026-11-08: `"label": "afterthought", "partition": "personal"`). crew reads it four ways: `crew.load` checks the main level's session and each role's session are in the entry's partition; `crew.operator_session` and `board.labels_here` check a host's session named for the label is; the briefs' `{{PARTITION}}` and `crew.main_tokens` show it as the drive's name ("You plan what business builds"); and `page.fleet_partition` puts it in the fleet page's data. swancloud already checks the same at evaluation: `lib/herdr-published.nix` asserts each drive's sessions name `partitionOf.${label}` before it writes either file. swancloud's record 0057 has "each context has one name on every layer, the personal partition is afterthought, crew's label among them".

**Who reads crew's shapes.** swancloud writes the teams file (`lib/herdr-published.nix` `teamsFile`, by the version `teamsVersion` it reads) and reads it in one check (`flake.nix`, `teams.get("partitions", [])`); its deployer's test writes a stub. crew's module writes it on hosts that use crew's flake (`flake.2`). Boomdrive's runner reads crew's records on the drive's branch, none of which names a partition, and its own `[control_plane.crew] partitions` is Boomdrive's word, renamed by Boomdrive's chore under its record 0028. No file on a drive's branch, no run-record field, no card key and no Pending You group names a partition (`plugin/lib/record.py`, `cards.py`, read 2026-11-08). The board's word kinds (`crew.KINDS`) hold `partition`, an item kind a dock's word may be on.

**The specs, and OpenSpec 1.16.0.** 136 requirements of 23 specs name a partition, 22 in their headers, and 10 purposes do. OpenSpec 1.16.0 drops a delta's Purpose for a spec that has one (`specs-apply.js`), and its strict validation refuses a MODIFIED block that leaves out a scenario name the current spec has (`validation/validator.js`, "omits scenario(s) the current spec still has"), so no delta can rename a scenario. 5ae11449 edited a purpose in place for the first reason, saying so. Two landed changes are not yet archived and modify requirements this change also modifies: `crew-fetches-nothing-in-the-runners-clone` ("The operator's brief names swancloud's checkout and folder as its host keeps them") and `an-offer-card-shows-the-step-the-deploy-waits-on-first` ("A deploy and every operation are approved and recorded through crew"). Of the other open changes, every delta that names a partition would write it back when archived.

**Area pages this change touches:** `core.md` (`code.4`, `code.5`, `code.7`, `code.8`, `code.11`, `read.1`, `read.2`, `roles.3`, `roles.5`), `teams.md` (`teams.6`, `teams.10`, `teams.25`), `plan.md` (`plan.22`), `briefs.md`, `flake.md` (`flake.1`, `flake.2`, `flake.3`), `tests.md` (`tests.4`, `tests.10`, `tests.11`), `docs.md` (`docs.2`, `docs.3`, `docs.4`, `docs.6`, `docs.7`). No page is edited by this change (`docs.7`); see Decision 9.

## Goals / Non-Goals

**Goals:**
- crew's word for a partition is drive in everything crew writes: its commands' words and usage, the teams file, the module's options, the code's names, the briefs, the cards, the pages, the mod, README, CLAUDE.md, the skill and the specs.
- crew reads no former name: no reader of `partitions` beside `drives`, and nothing that carries a host from one shape to the other.
- A check that keeps the word from coming back.

**Non-Goals:**
- Renaming `label`, `--label`, `CREW_LABEL` or `teams.json`. A drive's label is its name; the bolt's next unit and Boomdrive's records keep the word.
- Accounts. Record 0028's account is Boomdrive's, given to crew by the next unit of this bolt and Boomdrive's change after it (Boomdrive record 0032).
- Moving any host's file. swancloud's writer and check move with swancloud's bump to the release that carries this change; crew carries nothing for the hosts (Decision 2).
- Rewriting records, rules, explorations or archived changes (Decision 9).

## Decisions

### 1. A partition is a drive, named by its label

Wherever crew writes about its partition it writes drive: "a drive", "drives", "the drive's", "drives'". Where crew already wrote both, the drive is what it was the partition of: "the partition's drive branch" is "the drive's branch", "the drive's branch of a partition" "the branch of a drive", and "which partition's drive?" "which drive?". In code the names follow the words, `drive` and `drives`, `DRIVE` in constants, as `code.4` names anything crew mints. The drive's name is its label, as it is the branch's and the stream's (Boomdrive record 0028).

What keeps its text: Python's `str.partition` and `str.rpartition`, the language's; the hosts file's `partition` of a session, swancloud's field, which crew no longer reads (Decision 3) but whose fixtures in `tests/` still hold it as swancloud writes it; the user's own words where quoted; the former keys where a refusal, a requirement or a case names them as keys, `` `partitions` `` and `` `partition` ``; `docs/architecture/`, `docs/adr/`, `openspec/explorations/` and `openspec/changes/archive/` (Decision 9).

Not taken: keeping "partition" for crew's and calling Boomdrive's unit a drive only outside crew, which leaves the word the user found confusing and two words for one thing across the family (CLAUDE.md, *The family*).

### 2. The teams file is version 6, its drives under `drives`

`crew.VERSION` is 6. `crew.load` reads `drives`, each entry with `label`, `blueprints`, `state`, `machine`, `session`, `review`, `flume` and, where given, `roles`, and returns the fleet as `{"hosts", "drives", "repositories"}`. Its refusals say drive: "lists no drives", "lists drive <label> twice", "drive <label>: …". A file at version 5, or any other, is refused as now, naming its version, version 6 and the machine's configuration (`code.5`); a version-6 file with `partitions` and no `drives` is refused as listing no drives, by the same check that refuses an empty list, with nothing that knows the former key. A stray `partition` in an entry is carried as any unknown key is today and read by nothing.

Why a new version: the file's shape changes, and the version is how crew and its writers agree on a shape (`code.5`; swancloud's `teamsFile` branches on the version it reads from crew, `v == 5`). A host whose writer has not moved is refused with the fix named, never half read (`read.1`). Not taken: reading `partitions` where `drives` is missing, which is the transition code the user ruled out; keeping version 5 with renamed keys, which would let an old writer's file reach the new crew as "lists no drives" instead of naming its version.

### 3. crew reads no session's partition

`crew.load` no longer reads `partition` from an entry or from the hosts file's sessions, nor compares them; a role's `session` must still be one the hosts file lists on the main level's machine (`crew.session_of`), refused naming the session and the machine otherwise. `crew.operator_session` takes the session of the label's name on the host, refused when the host has none, and `board.labels_here` lists each drive whose label names a session on the host. The briefs' `{{PARTITION}}` token goes, and every brief, `crew.main_tokens`' roster line and the fleet page name the drive by its label.

Why: the binding of a session to its grouping is swancloud's, written and checked by swancloud at evaluation before either file reaches the host (`lib/herdr-published.nix`); crew checking it again is a mechanism of another tool's that crew keeps (`roles.5`), and repeating the grouping in crew's file makes a second name for the drive where record 0028 and swancloud's record 0057 give it one. Each drive's sessions are named by the drive (swancloud `herdr.2`, record 0057), so a session named for the label is the drive's.

Not taken: renaming the entry's field to a qualified key, such as `hosts_partition`, which keeps the word and the second name in crew's file; keeping `partition`, which writes the former word into a drive's entry.

### 4. crew's module lists `services.crew.settings.drives`

`nix/modules/options.nix`: the submodule `partition` becomes `drive`, with no `partition` option; `settings.partitions` becomes `settings.drives`; the duplicate-label assertion names `services.crew.settings.drives`; `services.crew.host`'s description names the drives' `machine`. The module writes `version` from `crew.py` as now, so it writes 6 (`flake.2`). A host's configuration that still sets `partitions` fails evaluation, since `drives` is required and given no default (`flake.2`), naming `services.crew.settings.drives` as used but not defined; nothing in the module names the former key. `nix/tests/files/deneb.json` and `runner.json` become the bytes the module writes for deneb's drives at version 6.

### 5. The command, the code and what it writes say drive

- **Usage and refusals.** `plugin/bin/crew`'s header and `crew-role`'s comments; `need_label`, "which drive? drives: …"; `crew send <drive> "<text>"`; `crew.drive_of`'s "no drive '<label>'. drives: …"; `crew.send_door`'s "crew send sends to a drive by its label"; `plan.py`'s "crew card runs as the card's drive", "crew card sweep runs for a drive", "crew record runs as the record's drive"; `runner.py`'s "no runner answers for the drive" and "a start waits for a runner (Boomdrive) to serve the drive". `code.11`'s usage text is the one each entry point prints, so `t-help` proves it.
- **Names.** `fleet["drives"]`; `crew.drive_of`; `plan.drive_hosts`, `plan.drive_kits`, `plan.drive_entries`, the landing reads' `drive` method beside `kits` and `forecast`; `page.fleet_drive`, `page.DRIVES` and the template's `<!--{{DRIVES}}-->`; module docstrings and comments. Every caller, `plugin/hooks/session-start` and `plugin/hooks/cards` among them.
- **What crew writes for others to read.** The fleet page's data, `drives` with each subscription's `drives` and `drives_said`, and `fleet.html` reading them; the page's `drives` for its header; `crew sites --json`'s `drives`; the board word's item kind `drive` in `crew.KINDS`, with the dock that makes such a key; card texts (`cards.py`'s withdrawals, "the ops of the drive that holds …"); the Flume roles file's opening comment (`source.py`, `teams.25`); the commit messages and run-record `why` crew writes. None of these is read by another tool (Context).
- **Tests.** Every case, class and helper in `tests/py/` named for a partition, and its fixtures (`facts.py`'s fleet, `PARTITION_KITS` in `test_cards.py`, the landing reads' method list in `test_landings.py`); `test_repository_rename.py`'s case that no command renames a drive asks `crew drive rename` and `crew label rename`.

### 6. The mod and the views

`board.agent_views` carries no key named for a partition (read 2026-11-08), so the views' shape is unchanged and `code.8` asks nothing of the mod but its words: `status.js`'s comments, `hooks.json`'s description and `plugin/tests/status.test.ts`'s case names say drive.

### 7. The specs: a delta, and the purposes and scenario names in place

This change's delta modifies every requirement that names a partition, with its words renamed by Decision 1 and its header renamed where it names one, and changes behaviour only in `main-level`'s "Drives are declared in the teams file" (Decisions 2 and 3) and `crew-flake`'s two module requirements (Decision 4). The delta keeps every scenario's name as the current spec has it, since OpenSpec 1.16.0 refuses a MODIFIED block that drops one. The build then renames, in place and in one commit, each spec's purpose and each scenario's name that names a partition, in `openspec/specs/` and in this change's delta alike, so the delta still validates and its archive applies it whole.

**Departure from `docs.4`** (and CLAUDE.md's *Specs*): purposes and scenario names are edited in `openspec/specs/` directly. No delta can carry them in OpenSpec 1.16.0 (Context), the words they change are this change's, and they reach the specs with its build, not ahead of it, as 5ae11449 did for a purpose. Everything a requirement says goes through the delta.

The two landed, unarchived changes: `crew-fetches-nothing-in-the-runners-clone`'s requirement is carried in this delta with its words, so either archive order leaves its text. `an-offer-card-shows-the-step-the-deploy-waits-on-first` renames two scenarios of its requirement, which a delta checked against main's spec cannot carry, so this delta keeps main's text there; whichever of the two archives later is reconciled by its archive's strict validation, which refuses the mismatch. Every open change's words are renamed by Decision 1 too (`docs.3`), its proposal, design, tasks and delta, its quotes kept, so none writes the former word back when archived.

### 8. `t-word` keeps the word from coming back

A new end-to-end test, `tests/t-word.sh`, reads crew's live text, `plugin/`, `nix/modules/`, `nix/packages/`, `flake.nix`, `README.md`, `CLAUDE.md`, `openspec/config.yaml` and `openspec/specs/`, and fails naming each file and line that holds "partition" in any case, but for a Python `.partition(` or `.rpartition(` call and a former key quoted as one, `` `partition` `` or `` `partitions` ``. Its `# Reads:` line names those paths (`tests.10`), and `tests/moon-tasks` writes its task.

Why a check: a word renamed by hand comes back with the next change written from an old reading, and a bolt that takes main in carries other units' words (`roles.3`: a rule broken again is refused by a check, not only by wording). Why end to end: the logic tier calls decisions on facts and the contract tier runs tools; the checks of crew's own text, README against the usage and the briefs' words, are `t-docs` and `t-briefs` (`tests.11`). `tests/`, `nix/tests/`, the records, the rules, the explorations and `openspec/changes/` are outside it: tests hold the former shapes on purpose, and the rest is dated or the design agent's.

### 9. No record and no rule is written here

The rules and records are the design agent's (`docs.7`, as the design agent has kept them since 2026-10-11: 7c048ac4 amended `code.5` after its landing). Twenty-one rules name a partition: `briefs.6`, `briefs.10`, `briefs.12`, `briefs.16`, `code.3`, `code.5`, `code.11`, `flake.2`, `plan.12`, `plan.14`, `plan.16`, `plan.22`, `read.1`, `read.5`, `signals.1`, `signals.6`, `state.3`, `state.4`, `teams.2`, `teams.6` and `teams.25`; once this lands the design agent amends them in names, and `code.5` for version 6 and `drives`, citing Boomdrive's record 0028 and the user's ruling above.

### Departures

- `code.5` names the teams file at version 5 with its partitions; this change builds version 6 with its drives, on the user's word in Boomdrive's record 0028 and their ruling of 2026-11-08; the rule is amended after the landing (Decision 9).
- `docs.4`: the purposes and scenario names (Decision 7).
- `openspec/config.yaml` asks that the last task run `tests/suite --affected`; this change's stage brief asks that no task run the repository's whole checks, which `--affected` is for any change to crew's command core (CLAUDE.md, *Tests*), so the verify stage runs them once, after the last task.

## Risks / Trade-offs

- [A host on the new crew with the old file refuses every command] → The refusal names version 6 and the machine's configuration. swancloud moves its writer to version 6 (`teamsFile`: `drives`, no `partition`) and its `flake.nix` check to `drives` in the same bump that moves a host to a release carrying this change; on a host that loads crew live (`plan.19`) the timer can bring crew first, and the host is refused until swancloud's deploy, which is the data fix the user assigned to agents. This change's caller tells swancloud's design agent.
- [Other units landing on main name a partition] → The bolt takes main by a submission (`teams.5`) and `t-word` fails on what it brought, naming the lines.
- [A session named for a label that is not the drive's] → swancloud names each drive's sessions by the drive and checks them at evaluation (Decision 3); crew trusts the file it is given, as it trusts the session it names for the main level.
- [The mechanical rename reaches a word that is not crew's] → Decision 1's list of what keeps its text; `str.partition` calls are untouched, and `t-word` allows them.
- [An open change archives before this one and changes a requirement this delta modifies] → its later or earlier archive is caught by strict validation where scenarios differ; where only words differ, this delta's text, built from main at the time it was written, would stand. The verify stage validates this change against the specs as they stand when it runs.

## Migration Plan

None in crew: crew reads only version 6 once this lands (Decision 2). swancloud's writer and check move with its bump to the release carrying this change; a host using crew's module moves when its configuration renames `partitions` to `drives` and drops each entry's `partition`. Rollback is the earlier release with its version-5 file.

## After deploy

None: every scenario is proved by a check in crew's tiers, and moving each host's file is swancloud's change or the host's configuration, done by whoever writes it.

## Task notes

**1.1** `plugin/lib/crew.py`: `VERSION = 6` and its comment; `load` reads `data.get("drives")`, refusing "lists no drives" and "lists drive <label> twice", `what = f"drive {label}"`; drop `"partition"` from the fields read with `need`, drop both session checks against it, and drop `partition=name` from the entry it keeps; the fleet's key is `drives`. Every reader of `fleet["partitions"]` in `plugin/lib/` and `plugin/hooks/` reads `fleet["drives"]` (`git grep -n 'fleet\["partitions"\]\|\.partitions\b\|"partitions"'`). `tests/py/facts.py`'s fleet and every case that builds one take `drives`; `test_teams.py` covers main-level's teams-file scenarios: version 6 loads; version 5 with `partitions` and `partition` refused naming version 6; version 6 with `partitions` and no `drives` refused as listing no drives; a hosts file giving `wldn-2` a `partition` of `clients/willdan`, `business` or none loads the same; a role's `session` the machine's hosts entry lacks refused naming the session and the machine. `test_fleet.py:106`'s `partition == "business"` goes.

**1.2** `tests/lib.sh` `teams_json`: version 6, `drives`, no entry's `partition`, its comment saying so; the hosts file's sessions keep their `partition`, as swancloud writes it. `tests/t-teams.sh`: the case at line 61 that sets a session's `partition` to `None` now expects the file to load; a version-5 file is refused naming version 6; the words it expects say drive.

**1.3** `nix/modules/options.nix` (Decision 4), `nix/modules/json.nix`'s comment, `nix/tests/file.nix`, `settings.nix`, `lib.nix`, `darwin.nix`, `nixos.nix`, `activate.sh`; `nix/tests/files/deneb.json` and `runner.json` regenerated as the module writes them (`builtins.toJSON` orders keys: `drives` before `repositories` and `version`). Add the case of crew-flake's "Drives under `partitions`": settings with `partitions` and no `drives` fail evaluation.

**2.1** The names of Decision 5's second point, with every caller in `plugin/lib/`, `plugin/bin/`, `plugin/hooks/` and `tests/py/` (`crew.partition_of` has about 60 callers). Leave every `.partition(` and `.rpartition(` call. Test functions and classes named for a partition (`git grep -n -E 'def test_[a-z_]*partition|class Test[A-Za-z]*Partition'`) take drive in their names.

**2.2** `crew.KINDS`' `partition` becomes `drive`, and the comment above it; `tests/py/test_board_word.py`'s cases, a word on `drive:<label>` going to its operator, and its expected refusal "no drive 'nosuch'. drives: …".

**2.3** `plugin/lib/page.py`: `DRIVES`, `<!--{{DRIVES}}-->` in `page.html` with `aria-label="Drives"`, `fleet_drive` returning no `partition`, the fleet data's `drives`, each subscription's `drives` and `drives_said`; `plugin/lib/fleet.html` reads them and shows each drive's label; `plugin/lib/sites.py`'s `drives`; the comments of `page.html` and `fleet.html`. `tests/py/test_page.py` and `test_fleet.py`.

**3.1** Every message, refusal, card text, commit message, `why` and comment crew's Python and hooks write (Decision 5's first and third points), and the words `tests/py/` expects of them: `test_send.py`, `test_cross.py`, `test_cards.py`, `test_card_commands.py`, `test_landing.py`, `test_landings.py`, `test_rail.py`, `test_board.py`, `test_asks.py`, `test_kits.py`, `test_source.py`, `test_runner.py` and the rest `git grep -il partition tests/py` lists.

**3.2** `plugin/bin/crew`'s header comment and usage (`<partition>` in `crew send`), `need_label`, `send)`'s usage, the comments in its `case`; `plugin/bin/crew-role`'s comments. `tests/t-help.sh`'s expected words.

**3.3–3.17** Each end-to-end test named expects the words crew now writes: replace "partition" in its expected text and comments by Decision 1, keeping any `.partition(` call and the hosts file's `partition` where a fixture writes it.

**4.1** `plugin/roles/design.md`, `main-ops.md`, `operator.md`, `planner.md`, `reviewer.md`, `plugin/flume/turn.md`: `{{PARTITION}}` becomes `the drive {{LABEL}}` or `{{LABEL}}` as the sentence reads, and every "partition" drive; `crew.main_tokens` drops `"PARTITION"` and the roster line's `({p['partition']})`; `crew.sends`' words. `teams.10` refuses a token with no builder, so no brief keeps `{{PARTITION}}`. `tests/t-briefs.sh`'s expected words.

**4.2** `README.md` (the teams file's version 6 and `drives` in its opening list, The main level, The flake's `settings` keys without `partition`, line 122's "A partition's **drive** is its loop" rewritten as what a drive is, every "partition"), `plugin/skills/crew/SKILL.md`, `CLAUDE.md`'s first line, `openspec/config.yaml`'s context ("Drives are data in ~/.config/crew/teams.json", and "drive" in its vocabulary). `docs.2`: README, the skill and the usage say the same.

**5.1** Decision 6: `plugin/hooks/status.js`, `plugin/hooks/hooks.json`, `plugin/tests/status.test.ts`.

**6.1** The purposes of `agent-models`, `board-page`, `bolt-plan`, `crew-board`, `fleet-page`, `flume-source`, `main-level`, `operator-agent`, `review-batches` and `role-runs`, edited in `openspec/specs/` by Decision 1 (Decision 7's departure; the commit says so, as 5ae11449 did).

**6.2** Every `#### Scenario:` line naming a partition, in `openspec/specs/` and in this change's `specs/`, renamed alike by Decision 1 in one commit (`git grep -n -i '^#### Scenario:.*partition' openspec/specs openspec/changes`); then every open change's words (`openspec/changes/<name>/`, not `archive/`), its quoted words kept. The ten changes that validate today: this one, `a-started-bolts-kit-folder-is-read-as-main-reads-it`, `a-unit-whose-branch-stands-is-refused-at-its-proposal`, `a-users-step-of-any-length-gets-its-card`, `checked-capture`, `crew-fetches-nothing-in-the-runners-clone`, `crews-module-is-keyed-as-flumes-is`, `crews-tests-keep-the-hosts-load-within-its-cores`, `daily-pass-through-crew` and `lineage-page`.

**7.1** `tests/t-word.sh` (Decision 8): its opening comment, its `# Reads:` line naming `plugin/ nix/modules/ nix/packages/ flake.nix README.md CLAUDE.md openspec/config.yaml openspec/specs/`, the first line every test keeps (`TESTS` unset stops it), and one `ok` naming how many files it read. It lists each offending `file:line` and fails once at the end. Then `tests/moon-tasks`, and commit `tests/moon.yml`.
