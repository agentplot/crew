# Verify: a-crew-release-reports-its-own-version

Verified on `change/a-crew-release-reports-its-own-version` at 748784d3, 2026-11-09.

## The whole checks

`tests/suite`, every project's `check-full` tasks, run once: **37 passed (37 replayed), 0 failed**, exit 0.

- tests: `logic`, `contract`, `mod`, and every end-to-end task, `t-release`, `t-session-hook`, `t-docs` and `t-specs` among them.
- nix: `format`, `lint`, `typecheck`, `test`.

Each replay is of a run that passed on this host with identical inputs; moon never replays a failed run.

`openspec validate a-crew-release-reports-its-own-version --strict`: valid.

Archived in a scratch copy of the checkout's `openspec/` at 748784d3, the change writes `crew-flake` (1 added, 1 modified), `crew-release` (created, 4 added) and `host-holds-and-updates` (1 added, 4 modified). `openspec validate --specs --strict` then gives **28 passed, 0 failed**. `openspec/specs/crew-release/spec.md` opens with the delta's `## Purpose`, how crew is released, and no placeholder, so `t-specs` holds the specs once archived.

## Tasks

All 11 tasks of `tasks.md` are ticked, none open. Each one's check is among the tasks that passed above. Task 5.2's check is the scratch archive above.

## Requirements and scenarios

### crew-release (new)

- **Purpose.** The delta opens with a `## Purpose` saying how crew is released: main names `0.0.0`, `set-version.sh` writes a release's version, a release's tag names a release commit cut from the pushed commit, and CI reckons from the newest tag by version.
- **Main's tree names no release.** `plugin/release.json` is `{"version": "0.0.0"}` and the manifest gives `0.0.0`. `t-release` reads both, the release file's keys being `["version"]`.
- **set-version.sh writes a release's version.** It checks the version as `x.y.z` before it touches a file, and rewrites each file through a scratch file by awk, refusing a file it writes nothing in and naming it. `t-release` proves the three scenarios on a scratch copy: `98.76.54` changing only the version lines, `0.56` refused with neither file changed, and a manifest with no version refused by name.
- **A release's tag names a release commit.** The release job runs `sh set-version.sh "${TAG#v}"`, commits the two files by path as `chore(release): $TAG`, runs `git tag "$TAG"`, pushes `refs/tags/$TAG` alone, and publishes with `gh release create "$TAG" --verify-tag`. `t-release` reads them in order.
- **CI reckons from the newest tag by version.** The version job runs `git-cliff --unreleased --bumped-version`. The conventional job's range starts at `git tag --list 'v*' --sort=-v:refname | head -n 1`, falling back to the push's `before`, with no `git describe`. `t-release` reads both.

### crew-flake

- **The package's version is the release file's.** `nix/version.nix` gives `x.y.z` as it is, `0.0.0` as `0-unstable-YYYY-MM-DD`, and throws naming `plugin/release.json` for anything else. `flake.nix` reads it from `lib.importJSON ./plugin/release.json`. `nix/tests/version.nix` and `nix/tests/package.nix` prove it, in `nix:test`.
- **A package built from a commit holds a release file naming it (modified).** Where the flake knows the commit it writes `{commit, version}` over the tree's file. With no commit, `release` is null and the tree's file stands. `nix/tests/package.nix` covers both.

### host-holds-and-updates

- **A checkout reads each release tag at the commit it was cut from (new).**
  - `tag_source` gives a release commit's first parent, or else the tagged commit. `checkout_version` gives the tag, with `+<n>` past its source. Both are pure (`code.7`), with logic cases in `tests/py/test_release.py`.
  - `git_version` lists `refs/tags/v*` by version, peeling annotated tags. It reads parents and subjects in one `git log`, and takes the first tag whose commit is HEAD or whose source is an ancestor of HEAD.
  - `tests/contract/test_release.py` proves each scenario against real git.
- **crew knows the release it runs from (modified).** `release_read` reads a release's version with no commit as `{commit: None, version}`. Any other version with no commit still reads as naming no commit. `crew_read` gives `v<x.y.z>`, a null commit, from `release`, nothing unread. `t-session-hook` checks a start's record against `crew _release` for the same checkout.
- **A build's version is shown as a checkout's is (modified).** `release_version` shows `0.0.0` as `0.0.0+<commit7>`, never `v0.0.0`, since `a_release` excludes `0.0.0`.
- **crew _release prints what a crew is (modified).** It prints `crew_read`'s facts, so a commit-less release prints a null commit. The usage in `crew.py` and in `plugin/bin/crew`'s header says the commit is null where a release names none.
- **crew reads the crew its host has installed (modified).** `release_said` takes a null commit only from `release` with a `v<x.y.z>` version that is not `v0.0.0`. Logic cases prove that answer read, and the others unread.

### Docs

README says what task 5.1 asks. `t-docs` passed.

## Observations, not blocking

- `docs.2`: `plugin/skills/crew/SKILL.md`'s `crew _release` row does not say the commit is null where a release names none. It is still accurate as written, and no task names it.
- `code.10`: the change departs from it, since main's tree names `0.0.0` and a release's tag names a release commit. The design's *Departures* names this. Amending the rule and its record is the design agent's (`docs.7`), after the landing.

## Outcome

The whole checks pass, every task is done, and the work meets every requirement and scenario. The change is archived on this branch with this report.
