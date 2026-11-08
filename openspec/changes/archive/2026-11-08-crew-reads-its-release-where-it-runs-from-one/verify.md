# Verify: crew-reads-its-release-where-it-runs-from-one

Verified on `change/crew-reads-its-release-where-it-runs-from-one` at d37451d6, cut from `bolt/crew-runs-the-crew-its-host-installed` at fcedc22e, on 2026-11-08.

## The whole checks

`tests/suite --affected`, once, as CLAUDE.md names the run when a change is done: every `check-full` task whose inputs differ from the merge-base with main.

```
32 passed (3 replayed), 0 failed
exit 0
```

Ran: `tests:logic`, `tests:contract`, `nix:test`, `nix:typecheck`, and every end-to-end task (`t-briefs`, `t-cards`, `t-flume-source`, `t-help`, `t-hold`, `t-journey-board`, `t-journey-cross`, `t-journey-land`, `t-journey-main`, `t-journey-main-fix`, `t-journey-ops`, `t-journey-plan`, `t-journey-review`, `t-journey-roles`, `t-journey-signals`, `t-journey-state`, `t-roles`, `t-runner`, `t-session-hook`, `t-slot`, `t-sluice`, `t-stage-facts`, `t-suite`, `t-teams`, `t-waits`). Replayed from an identical tree that passed: `nix:format`, `nix:lint`, `t-docs`. The only `check-full` task not selected is `tests:mod`, because its inputs (`plugin/hooks/status.js`, `plugin/tests/`) are unchanged, which matches the proposal: the views keep their shape and `code.8` is not reached.

`openspec validate crew-reads-its-release-where-it-runs-from-one --strict`: valid.

After the archive, `openspec validate --specs --strict` passes 8 of 26 specs, against 9 of 26 at fcedc22e. The one that changed is `crew-flake`: its modified requirement is now over 500 characters, which openspec warns of and strict mode counts as a failure. `host-holds-and-updates` failed in the same way before the archive. These are length warnings, not errors, of the kind most of crew's specs carry, so they stop nothing here.

## Tasks

All 17 tasks in `tasks.md` are ticked. Each one's named check is among the tasks above, and all of them passed.

## Requirements and scenarios

### host-holds-and-updates

| Requirement | Built in | Proved by |
|---|---|---|
| crew knows the release it runs from | `crew.py` `crew_read`, `release_read`, `crew_version`; `session-start` unchanged | `test_release.py` `TestReleaseFile`, `TestCrewRead`; `t-session-hook.sh` (a build's start records the file's commit and `0-unstable-2026-11-08+<seven>`, one with none records neither) |
| A build's version is shown as a checkout's is | `release_version` | `test_a_release_version_reads_as_its_tag`, `test_an_untagged_version_reads_with_the_commits_first_seven_characters` |
| crew _release prints what a crew is | `crew.py` `release_cmd`, answered before `load()`; `plugin/bin/crew` arm before a command's host is chosen | `t-session-hook.sh` (checkout, build, build with none, `from` null); `t-help.sh` (`_release --help`, the dispatch check) |
| crew names its command by the crew its host has installed | `installed_command`, `path_crews`, `installed_here`, `crew_command` | `TestInstalledCommand`, covering all three scenarios |
| A standing agent's crew commands run the crew its host has installed | `main_tokens`, `sends`, `crew_on`, `hold.hand`, `board.notice_argv`, `Follower.again`, `plan.console_cmd` | `TestBriefs`; `test_the_hand_of_a_restart_runs_crew_renew_through_the_installed_crew`; `test_board.py` `TestInstalledCrew`; `t-journey-main` |
| crew reads the crew its host has installed | `installed`, `own_command`, `ask_release` (five seconds), `release_said`, `ASKED` keyed by real path | `TestInstalled`: its own crew with no process, an answer read once per real path, late, failed, not JSON and missing-commit answers unread with their why |
| The launch digest reads crew's command as one word | `launch_digest(l, text, names)` | `TestDigest`: two crews digest alike, and a start digested the older way reads as its brief changed |
| An update makes a standing agent due a restart (modified) | `update_due(started, installed, launch, loaded)`, `due_of(now=)`, `hold.update_here`, `hold.renew` | `test_hold.py` `TestDue`: brief changed, code alone, a release installed, the same release, a start with no release (`NO_COMMIT_SAID`), the installed crew unread, `loaded_changed` only in an installed checkout's own root |
| A due agent is restarted at its next stop (modified, "An install moves while an agent sits idle") | `board.crew_stamp`, `moved_at`, `Follower.again` running `_update` and `_follow` through the installed command | `test_board.py` `TestInstalledCrew`: the stamp is the real path and moves with an install, unread without one, so the refresh only reads; the follower starts again through the installed crew, or as its own `board.py` from a checkout |
| A band shows the crew its agent runs (modified, "Due for a release") | `board.here_read` taking the host's version from `crew.installed()` | `test_a_due_agents_band_shows_the_release_the_host_has_installed` ("crew v0.44.1 → v0.44.2 at its next stop") |

### crew-flake

| Requirement | Built in | Proved by |
|---|---|---|
| The flake gives crew's package for each system (modified) | `nix/packages/crew.nix` `commit ? null`, `release`, `passthru.release`, install writing `plugin/release.json`; `flake.nix` `commit = self.rev or null` | `nix/tests/package.nix` in `nix:test`: built from a commit, `release` names it and the install writes it; built from a tree with no commit, `release` is null and no file is written; `nix:format`, `nix:lint` |

## Other checks

- The change touches neither `docs/architecture/` nor `docs/adr/` (`docs.7`), and leaves `openspec/specs/` to the archive (`docs.4`).
- `docs.2` holds: `crew _release` is in `plugin/bin/crew`'s usage, `plugin/skills/crew/SKILL.md` and README, and `t-docs` passes.
- `code.1` holds: nothing outside the standard library is imported. `code.7` holds: `installed_command`, `release_read`, `release_said`, `release_version` and `update_due` are decisions on plain facts. `code.11` holds: `_release` answers `-h` first.
- The design asks two readings of the design agent after the landing (`docs.7`): `teams.19`'s details for a build's release, and `NO_COMMIT_SAID` being built. Neither is this change's own edit.

## Outcome

The whole checks pass and the work meets every requirement and scenario of the change's specs. The change is archived.
