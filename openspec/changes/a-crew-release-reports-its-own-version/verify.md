# Verify: a-crew-release-reports-its-own-version

Verified on `change/a-crew-release-reports-its-own-version` at 6fcaf1b5, 2026-11-09.

## The whole checks

`tests/suite`, every project's `check-full` tasks, run once: **37 passed (4 replayed), 0 failed**, exit 0.

- tests: `logic`, `contract`, `mod`, and every end-to-end task, `t-release` (replayed), `t-session-hook` (replayed), `t-docs` (replayed) and `t-specs` among them.
- nix: `format`, `lint`, `typecheck`, `test` (replayed).

The four replays are of runs that passed on this host with identical inputs; moon never replays a failed run.

`openspec validate a-crew-release-reports-its-own-version --strict`: valid. Each requirement's text above its first scenario is under 500 characters, the modified ones included (the longest, "crew knows the release it runs from", 457), so `t-specs` holds the specs once archived. Each modified requirement's header exists in `openspec/specs/crew-flake` or `openspec/specs/host-holds-and-updates`.

## Tasks

All 9 tasks of `tasks.md` are ticked, and each one's check is among the tasks that passed above.

## Requirements and scenarios

### crew-release (new)

- **Main's tree names no release.** `plugin/release.json` is `{"version": "0.0.0"}`, and the manifest gives `0.0.0`. `t-release` reads both with `jq`, the release file's keys being `["version"]`.
- **set-version.sh writes a release's version.** `set-version.sh` checks the version before it touches any file and rewrites each file through a scratch file by awk, refusing a file it writes nothing in and naming it. `t-release` proves each scenario on a scratch copy: both files at `98.76.54` with only their version lines changed, `0.56` refused with neither file changed, and a manifest with no version refused by name.
- **A release's tag names a release commit.** The release job runs `sh set-version.sh "${TAG#v}"`, commits the two files by path as `chore(release): $TAG`, runs `git tag "$TAG"`, pushes `refs/tags/$TAG` alone, and publishes with `gh release create "$TAG" --verify-tag`, with no `--target`. `t-release` reads them in order, with one `git push`, no `+` and no `--force`.
- **CI reckons from the newest tag by version.** The version job runs `git-cliff --unreleased --bumped-version`. The conventional job's range starts at `git tag --list 'v*' --sort=-v:refname | head -n 1`, falling back to the push's `before`, with no `git describe`. `t-release` reads both.

### crew-flake

- **The package's version is the release file's.** `nix/version.nix` gives `x.y.z` as it is, gives `0.0.0` as `0-unstable-YYYY-MM-DD`, and throws naming `plugin/release.json` for anything else. `flake.nix` takes it from `lib.importJSON ./plugin/release.json`. `nix/tests/version.nix` proves the three cases, and `nix/tests/package.nix` checks that the flake's own package on main's tree starts `0-unstable-`. `nix/moon.yml` adds `/plugin/release.json` to `typecheck`'s and `test`'s inputs.
- **A package built from a commit holds a release file naming it (modified).** The install copies the tree's `plugin/`, and where `commit` is given it writes `{commit, version}` over the release file. With no commit, `release` is null and nothing is written. `nix/tests/package.nix` covers both.

### host-holds-and-updates

- **A checkout reads each release tag at the commit it was cut from (new).**
  - `tag_source` and `checkout_version` are pure (`code.7`), with logic cases in `tests/py/test_release.py`.
  - `git_version` lists `refs/tags/v*` by version, peeling annotated tags, and reads parents and subjects in one `git log`. It takes the first tag whose commit is HEAD or whose source is an ancestor of HEAD, counting the commits past that source.
  - `tests/contract/test_release.py` proves each of the five scenarios against real git, with history made as the release job makes it: `v0.56.0+2` past P, `v0.56.0` at P and at R, `v0.55.0+3` on a branch past an annotated tag on main, and a commit with no version where no release tag exists.
- **crew knows the release it runs from (modified).**
  - `release_read` reads a file with a release's version and a missing or null commit as `{commit: None, version}`.
  - Main's `0.0.0`, an unstable version or anything else with no commit still reads as "the release file names no commit".
  - `crew_read` gives `v0.56.0` with a null commit, from `release`, with nothing unread.
  - Logic cases cover each scenario. `t-session-hook` checks a start's record against `crew _release` for the same checkout.
- **A build's version is shown as a checkout's is (modified).** `release_version` shows `0.0.0` as `0.0.0+<commit7>`, never as `v0.0.0`. A logic case proves it.
- **crew _release prints what a crew is (modified).** It prints `crew_read`'s facts, so a commit-less release prints a null commit. The usage in `release_cmd` and in `plugin/bin/crew`'s header says the commit is null where a release names none.
- **crew reads the crew its host has installed (modified).**
  - `release_said` accepts a null commit only from `release` with a `v<x.y.z>` version other than `v0.0.0`.
  - Logic cases prove the commit-less release read as itself.
  - They also prove five answers unread: a null commit from a checkout, `v0.0.0`, an unprefixed version, an unstable version and a null version.

### Docs

README's start paragraph, flake section and a new release paragraph say what task 5.1 asks. `t-docs` passed.

## Observations, not blocking

- `docs.2`: `plugin/skills/crew/SKILL.md`'s `crew _release` row was not updated to say the commit is null where a release names none. It is still accurate as written, and no task named it.
- `code.10`: the change departs from it, since main's tree now names `0.0.0` and a release's tag names a release commit. The design's *Departures* names this. Amending the rule and its record is the design agent's (`docs.7`), from main's log after the landing.

## Outcome

The whole checks pass and the work meets every requirement and scenario of the change, with every task done. The change is archived.
