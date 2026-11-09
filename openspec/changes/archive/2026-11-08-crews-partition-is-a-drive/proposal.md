# crew's partition is a drive

## Why

Boomdrive's record 0028, accepted by the user on 2026-11-07, gives the family two words where "partition" meant two things: an **account** is what a runner enrolls with a control plane, and a **drive** is a body of work of one account, its repositories, one Flume stream and one branch of the account's crew state. "Each drive runs on its own (record 0026, which reads 'drive' where it says 'partition'). crew's own word 'partition' becomes 'drive' with crew's rename." The user: "Yes the branches in crew correlate to the drives. That's correct", and of the old word, "That word being used in different places could be confusing". crew's record 0054 already calls a partition's loop and branch its drive; this change makes the partition itself the drive, so crew has one word for it.

The user's ruling of 2026-11-08 (signal `2026-11-08-agentplot-design-c2aff6f4/01-no-code-carries-a-transition` on `agentplot/main` of afterthought/crew-state): "I want the system to be built the way it should be and then have agents fucking fix the data transition as necessary". So crew reads no former name: no reader takes `partitions` beside `drives`, and the hosts' files are moved by whoever writes them.

## What Changes

- **BREAKING** The teams file is version 6. Its drives are listed under `drives`, each named by its label alone: an entry no longer names the swancloud partition its session is in. crew refuses a file at version 5, as at every other version, naming the machine's configuration, and reads no `partitions` key and no entry's `partition`.
- crew reads no session's `partition` in the hosts file. A drive names its sessions; the fleet's configuration checks at evaluation that each is the drive's (swancloud `lib/herdr-published.nix`), and crew no longer checks it again.
- **BREAKING** crew's module lists the drives as `services.crew.settings.drives`, each a `drive` with no `partition` option; the file it writes is version 6.
- crew's command says drive: `crew send <drive> "<text>"`, "which drive? drives: …", "no drive '<label>'. drives: …", and every refusal, usage line, card text, roles-file comment and commit message crew writes.
- crew's code names a drive a drive: the fleet's `drives`, `crew.drive_of`, `plan.drive_kits`, `plan.drive_hosts`, `plan.drive_entries`, `page.fleet_drive`, the page's and fleet page's `drives` data and `{{DRIVES}}` placeholder, `crew sites --json`'s `drives`, the board word's item kind `drive`, and every test named for a partition. Python's `str.partition` is the language's and stays.
- The briefs name their drive by its label: the `{{PARTITION}}` token goes, and every role's words say drive. The skill, README, CLAUDE.md, `openspec/config.yaml` and crew's mod's words say drive.
- The specs say drive: each requirement that named a partition, through this change's delta; each spec's purpose and each scenario's name, which OpenSpec 1.16.0 cannot carry in a delta, edited in place in the same build; and the open changes' words, so none writes the former word back when it is archived.
- A new end-to-end test, `t-word`, refuses the word "partition" in crew's command, plugin, module, README, CLAUDE.md, OpenSpec configuration and specs, but Python's `str.partition` and a former key quoted as one, so the word does not come back.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `main-level`: drives are declared under `drives` in a version-6 teams file, named by their label alone, and crew reads no session's partition; every other requirement's words.
- `crew-flake`: the module lists `services.crew.settings.drives`, with no `partition` option; its words.
- `agent-models`, `board-page`, `bolt-plan`, `bolt-teams`, `card-sessions`, `crew-board`, `crew-command`, `crew-rail`, `crew-sites`, `drive-state`, `fleet-page`, `flume-source`, `host-holds-and-updates`, `lineage-page`, `operator-agent`, `plan-proposals`, `rail-cards`, `review-batches`, `role-runs`, `run-record`, `signal-capture`: each requirement that names a partition names a drive, with no change to what it does.

## Impact

- **Code**: `plugin/lib/` (every module that reads the fleet or names a partition: `crew.py`, `plan.py`, `board.py`, `page.py`, `ops.py`, `runner.py`, `cards.py`, `asks.py`, `record.py`, `source.py`, `sites.py`, `hold.py`, `gather.py`, `page.html`, `fleet.html`), `plugin/bin/crew` and `crew-role`, `plugin/hooks/` (`session-start`, `cards`, `status.js`, `hooks.json`), `plugin/roles/`, `plugin/flume/turn.md`, `plugin/skills/crew/SKILL.md`, `nix/modules/`.
- **Tests**: `tests/py/` (fixtures in `facts.py`, every case named for a partition), `tests/lib.sh`'s teams file, the end-to-end tests whose words change, `plugin/tests/status.test.ts`, `nix/tests/` and its files, the new `tests/t-word.sh` and `tests/moon.yml`.
- **Docs**: README, CLAUDE.md, `openspec/config.yaml`, the specs' purposes and scenario names, and the open changes' words.
- **Unchanged**: `docs/architecture/` and `docs/adr/`, the design agent's (`docs.7`), whose rules and records name a partition and are amended in names by its hand once this lands; `openspec/explorations/` and the archived changes, which are dated readings; `label`, `--label` and `CREW_LABEL`, the drive's name; `teams.json`'s file name; the hosts file, swancloud's, whose sessions keep their `partition`; every file on a drive's branch, none of which names a partition; Boomdrive's runner, which reads nothing crew renames.
- **Other repositories**: swancloud writes the teams file (`lib/herdr-published.nix` `teamsFile`, its deployer's test) and reads it (`flake.nix`'s check of the roles file reads `partitions`); both move to version 6 with the release of crew that carries this change. That is swancloud's work, told to its design agent by this change's caller; crew carries nothing for it.
