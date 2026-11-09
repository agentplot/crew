# Tasks

Each check runs from the worktree's root as written. `tests/suite <name>` runs one moon task; a pytest check runs the files it names. The verify stage runs the repository's whole checks once, after the last task. Submit nothing: Flume submits the place once its last stage delivers.

## 1. The teams file and the module

- [x] 1.1 crew loads the teams file at version 6, its drives under `drives`, each named by its label with no `partition`, reads no session's `partition` in the hosts file, refuses a version-5 file and a version-6 file with no `drives` naming the fix, and gives every reader in `plugin/lib/` and `plugin/hooks/` the fleet's `drives` (design, Decisions 2 and 3; Task notes 1.1). Verify `tests/suite logic` ends with "0 failed".
- [x] 1.2 The end-to-end tests' teams file is version 6 with its drives under `drives`, and `t-teams` proves a version-5 file refused naming version 6 and a session's `partition` read by nothing (design, Decisions 2 and 3; Task notes 1.2). Verify `tests/suite t-teams` ends with "0 failed".
- [ ] 1.3 crew's module lists `services.crew.settings.drives`, each a `drive` with no `partition` option, writes deneb's drives at version 6 byte for byte as its files hold them, and fails evaluation for settings that list `partitions` and no `drives` (design, Decision 4; Task notes 1.3). Verify `tests/suite nix:test` ends with "0 failed".

## 2. crew's names

- [ ] 2.1 Every function, constant, method and test of crew's named for a partition is named for a drive, with every caller, and no `.partition(` call is touched (design, Decision 5; Task notes 2.1). Verify `tests/suite logic` ends with "0 failed".
- [ ] 2.2 A board word on a drive is on the item kind `drive`, and a word naming no drive is refused naming the drives (design, Decision 5; Task notes 2.2). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_board_word.py'` exits 0.
- [ ] 2.3 The page and the fleet page carry their drives as `drives`, the page's header placeholder is `{{DRIVES}}`, the fleet page names each drive by its label, and `crew sites --json` lists `drives` (design, Decisions 3 and 5; Task notes 2.3). Verify `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_page.py tests/py/test_fleet.py'` exits 0.

## 3. crew's words

- [ ] 3.1 Every refusal, message, card text, commit message and comment crew's Python and hooks write says drive where it said partition (design, Decisions 1 and 5; Task notes 3.1). Verify `tests/suite logic` ends with "0 failed".
- [ ] 3.2 crew's usage and `crew-role`'s comments say drive, `crew send <drive> "<text>"` among them, and a command given no label asks which drive (design, Decision 5; Task notes 3.2). Verify `tests/suite t-help` ends with "0 failed".
- [ ] 3.3 `t-journey-board` expects crew's words for a drive (design, Decision 1; Task notes 3.3–3.17). Verify `tests/suite t-journey-board` ends with "0 failed".
- [ ] 3.4 `t-journey-main` expects crew's words for a drive (design, Decision 1; Task notes 3.3–3.17). Verify `tests/suite t-journey-main` ends with "0 failed".
- [ ] 3.5 `t-roles` expects crew's words for a drive (design, Decision 1; Task notes 3.3–3.17). Verify `tests/suite t-roles` ends with "0 failed".
- [ ] 3.6 `t-journey-review` expects crew's words for a drive (design, Decision 1; Task notes 3.3–3.17). Verify `tests/suite t-journey-review` ends with "0 failed".
- [ ] 3.7 `t-journey-ops` expects crew's words for a drive (design, Decision 1; Task notes 3.3–3.17). Verify `tests/suite t-journey-ops` ends with "0 failed".
- [ ] 3.8 `t-journey-land` expects crew's words for a drive (design, Decision 1; Task notes 3.3–3.17). Verify `tests/suite t-journey-land` ends with "0 failed".
- [ ] 3.9 `t-journey-roles` expects crew's words for a drive (design, Decision 1; Task notes 3.3–3.17). Verify `tests/suite t-journey-roles` ends with "0 failed".
- [ ] 3.10 `t-journey-cross` expects crew's words for a drive (design, Decision 1; Task notes 3.3–3.17). Verify `tests/suite t-journey-cross` ends with "0 failed".
- [ ] 3.11 `t-journey-state` expects crew's words for a drive (design, Decision 1; Task notes 3.3–3.17). Verify `tests/suite t-journey-state` ends with "0 failed".
- [ ] 3.12 `t-sluice` expects crew's words for a drive (design, Decision 1; Task notes 3.3–3.17). Verify `tests/suite t-sluice` ends with "0 failed".
- [ ] 3.13 `t-hold` expects crew's words for a drive (design, Decision 1; Task notes 3.3–3.17). Verify `tests/suite t-hold` ends with "0 failed".
- [ ] 3.14 `t-journey-main-fix` expects crew's words for a drive (design, Decision 1; Task notes 3.3–3.17). Verify `tests/suite t-journey-main-fix` ends with "0 failed".
- [ ] 3.15 The session-start hook names a session's drive and reads its main level's machine by `crew.drive_of` (design, Decision 5; Task notes 3.3–3.17). Verify `tests/suite t-session-hook` ends with "0 failed".
- [ ] 3.16 The cards hook names a card's drive and checks an area's kit among the drive's kits (design, Decision 5; Task notes 3.3–3.17). Verify `tests/suite t-cards` ends with "0 failed".
- [ ] 3.17 crew's Flume roles file opens naming each drive whose main level runs on the host (design, Decision 5; Task notes 3.3–3.17). Verify `tests/suite t-flume-source` ends with "0 failed".

## 4. The briefs and the docs

- [ ] 4.1 Every brief names its drive by its label, no brief or builder keeps `{{PARTITION}}`, and each role's words say drive (design, Decisions 1 and 3; Task notes 4.1). Verify `tests/suite t-briefs` ends with "0 failed".
- [ ] 4.2 README, the crew skill, CLAUDE.md and `openspec/config.yaml` say drive, README naming the teams file's version 6, its `drives` and the module's keys with no `partition` (design, Decisions 1, 2 and 4; Task notes 4.2). Verify `tests/suite t-docs` ends with "0 failed".

## 5. The mod

- [ ] 5.1 crew's mod, its hooks' description and its cases say drive, the views it draws unchanged (design, Decision 6; Task notes 5.1). Verify `tests/suite mod` ends with "0 failed".

## 6. The specs

- [ ] 6.1 Each spec's purpose says drive where it said partition, edited in place as no delta can carry it (design, Decision 7; Task notes 6.1). Verify `openspec validate --specs` exits 0, its totals saying "0 failed".
- [ ] 6.2 Every scenario's name says drive in `openspec/specs/` and in this change's delta alike, and every open change's words say drive, so each change that validated before still does (design, Decision 7; Task notes 6.2). Verify `for c in crews-partition-is-a-drive a-started-bolts-kit-folder-is-read-as-main-reads-it a-unit-whose-branch-stands-is-refused-at-its-proposal a-users-step-of-any-length-gets-its-card checked-capture crew-fetches-nothing-in-the-runners-clone crews-module-is-keyed-as-flumes-is crews-tests-keep-the-hosts-load-within-its-cores daily-pass-through-crew lineage-page; do openspec validate "$c" --strict || exit 1; done` exits 0.

## 7. The word stays gone

- [ ] 7.1 `t-word` fails naming each file and line of crew's command, plugin, module, README, CLAUDE.md, OpenSpec configuration and specs that holds "partition", but for a `.partition(` or `.rpartition(` call and a former key quoted as one, and passes on this branch, its task in `tests/moon.yml` (design, Decision 8; Task notes 7.1). Verify `tests/suite t-word` ends with "0 failed".
