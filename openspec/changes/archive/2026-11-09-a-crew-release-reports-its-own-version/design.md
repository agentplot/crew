# Design

## Context

**The brief.** A crew release's tag names a release commit that writes the release's version into crew's release file and its flake package's version, as Flume's release does. So any build of that tag reports the tag's version with nothing overriding it, whether crew's own flake builds it or another's does. Sources: agentplot/boomdrive record 0023 (accepted), the set takes each tool's own package; agentplot/blueprints `design/principles.md` 14, a tool that needs what another program knows reads that program's own source, never a file a host makes for it; Flume's release commit, `set-version.sh`, as the family's form.

**crew today, read on this branch's tree on 2026-11-09:**
- `code.10`: CI tags the pushed main commit `v<x.y.z>` when git-cliff finds a new version, and the version is kept in no file.
- `flake.nix` versions the package `0-unstable-<date>` from `self.lastModifiedDate`. `nix/packages/crew.nix` writes `plugin/release.json`, `{commit, version}`, where the flake knows `self.rev`, and writes nothing otherwise. The comments call it "a file of the build alone, never of the tree".
- `crew.py` `crew_read` reads a checkout by git, `git describe --tags --long --match 'v[0-9]*'`, and a build by its release file. `release_read` refuses a file with no full commit. `release_version` shows `v<x.y.z>` for any `x.y.z`, `0.0.0` among them.
- `plugin/.claude-plugin/plugin.json` gives `"version": "0.1.0"`, which no release reads or writes (`code.10` details).
- `.github/workflows/release.yml`: the conventional job's range starts at `git describe --tags --abbrev=0`; the version job runs `git-cliff --bumped-version`; the release job runs `gh release create "$TAG" --target "$GITHUB_SHA"`.
- `tests/t-session-hook.sh` reckons the version a start records with its own `git describe` of crew's checkout.

**Who overrides crew's version, read 2026-11-09:**
- agentplot/boomdrive's `nix/packages/crew.nix`, on its bolt `the-boomdrive-flake-configures-the-whole-host`, sets `version` to the tag its `flake.nix` pins, by `overrideAttrs`. The package's release file is written from the version crew's flake gave, before the override, so the build's crew reads itself as `0-unstable-<date>+<commit>`.
- afterthought/swancloud's `packages/crew` copies the pinned commit's `plugin/` and, for its teamless pin, writes its own `plugin/release.json`.

**Flume's form, read on agentplot/flume's main at e2973d57:** `set-version.sh <x.y.z> [<root>]` writes the version into every file that carries Flume's version, each by an awk program that refuses a file it writes nothing in. Main gives `0.0.0` in each. The release job runs it on the pushed commit, commits `chore(release): $TAG`, tags that commit and pushes the tag, plus a `release` branch for its marketplace. Its conventional job starts at `git tag --list 'v*' --sort=-v:refname | head -n 1`, and its version job runs `git-cliff --unreleased --bumped-version`, because "the newest tag names a release commit off main". `check-versions.sh` holds every file to the workspace's version and runs `set-version.sh` on a scratch copy.

**Area pages this change touches:** `core.md` (`code.1`, `code.2`, `code.6`, `code.7`, `code.10`, `read.1`, `read.2`, `state.3`, `state.5`), `flake.md` (`flake.1`, `flake.3`), `tests.md` (`tests.4`, `tests.10`, `tests.11`), `docs.md` (`docs.2`, `docs.6`, `docs.7`), `teams.md` (`teams.19`, whose band shows the version this reads). No rule page is edited by this change (`docs.7`).

## Goals / Non-Goals

**Goals:**
- A build of a release tag reports that tag's version, whether by crew's flake, by a flake that takes crew's package, or as a copy of the tag's `plugin/` with nothing added.
- crew's own source names its version: `0.0.0` on main, the release's at its tag.
- A checkout's version stays right once tags no longer stand on main's history.
- CI keeps finding the next version and checking the commits since the last release.

**Non-Goals:**
- Boomdrive's override and swancloud's own release file. Each is its own repository's to drop once a release is made this way.
- Judging an agent due when the installed crew names a version and no commit. `update_due` already says it can't tell (`teams.19`), and a build of crew's own package names its commit.
- A `release` branch like Flume's, which serves Flume's marketplace. No host of crew's reads one.
- Changing what crew models or the views of it (`code.8`).

## Decisions

### 1. The release file is in crew's tree, `0.0.0` on main

`plugin/release.json` joins the tree as `{"version": "0.0.0"}` and nothing else. It is crew's one statement of its own version: the file crew already reads where it runs with no git, beside the code that reads it. A release commit writes the release's version there. A build adds `commit` where it knows one.

crew's manifest, `plugin/.claude-plugin/plugin.json`, carries a version Claude Code reads. It gives `0.0.0` on main and the release's at its tag, as Flume's plugin manifest does, so it never states a version that no release has.

Not taken: a separate `VERSION` file beside a build-only release file, which keeps one fact in two files; the version in `flake.nix`, which a copy of the tag's `plugin/` cannot read.

### 2. `set-version.sh` writes every file that carries crew's version

`set-version.sh` sits at the tree's root, named and called as Flume's is: `sh set-version.sh <major.minor.patch> [<root>]`. It is POSIX sh and awk, so CI's runner needs nothing installed for it (`code.1`). Each file is rewritten by an awk program into a scratch file and moved over the original. A program that writes nothing refuses the file, naming it. A version that is not `x.y.z` is refused before any file is touched. It writes:
- `plugin/release.json`: the `"version": "<v>"` line.
- `plugin/.claude-plugin/plugin.json`: its `"version": "<v>"` line.

`tests/t-release.sh` holds main's files at `0.0.0`. It runs `set-version.sh` on a scratch copy and checks each file changes in exactly its version lines. These are Flume's `check-versions.sh` cases, as an end-to-end test of the tests project (`tests.10`).

### 3. The flake takes its package's version from the release file

`nix/version.nix` is a function, `{ release, date }`, that returns the package's version. `release.version` of `x.y.z` (not `0.0.0`) is returned as it is. `0.0.0` becomes `0-unstable-YYYY-MM-DD` from `date`, `self.lastModifiedDate`, as today. Anything else throws, naming `plugin/release.json`. `flake.nix` calls it with `lib.importJSON ./plugin/release.json`, so nothing but the tree sets the version.

`nix/packages/crew.nix` keeps its install: `cp -R plugin` copies the tree's file, and where `commit` is given, `{commit, version}` is written over it. With no commit, nothing is written and the package holds the tree's file. `release` stays null there. Only the comments change. They no longer call the file the build's alone.

The nix project's `typecheck` and `test` take `/plugin/release.json` as an input (`flake.3`, `tests.10`). `nix/tests/version.nix` holds the function's cases. `nix/tests/package.nix` checks that the flake's own package on main's tree is `0-unstable-` and keeps its two release cases.

### 4. A checkout reads each release tag at the commit it was cut from

A release commit is off main, so `git describe` from main never reaches it. A host that loads crew live, from a checkout at GitHub's main (`plan.19`), would read the last tag made the old way forever. So `git_version` reads the tags itself:
- **Reads:**
  - `git for-each-ref --sort=-v:refname --format=... refs/tags/v*`, kept to `^v[0-9]+\.[0-9]+\.[0-9]+$`, each peeled to its commit.
  - One `git log --no-walk=unsorted --format=%H%x09%P%x09%s` of those commits, for each one's parents and subject.
  - Then, newest first: whether HEAD is the tag's commit, else `git merge-base --is-ancestor <source> HEAD`, stopping at the first that holds.
  - `git rev-list --count <source>..HEAD` for that tag.
- **Decisions (`code.7`):**
  - `tag_source(tag, commit, parents, subject)` gives the first parent where the subject is `chore(release): <tag>`, else the commit. Tags made before this change name main's own commits.
  - `checkout_version(tag, past)` gives `tag`, or `tag+<past>`.
- HEAD at a tag's own commit reads as the tag. No tag whose source is HEAD or before it reads HEAD's commit and no version, as today.

The contract tier proves the read against a scratch repository: a release commit cut off main as the release job cuts it and tagged, main moved past it, and an older tag on main's own history. `tests/t-session-hook.sh` takes the commit and version a start should record from `crew _release` of the same checkout, so it no longer reckons them with `git describe`.

### 5. A release file with a version and no commit is a release

A copy of a tag's `plugin/` with nothing added holds `{"version": "0.56.0"}`. `release_read` reads it as `{"commit": None, "version": "0.56.0"}`. `crew_read` gives version `v0.56.0`, commit None, `from` `"release"`, and `unread` None. A `commit` that is absent or null, beside a version that is no release's (`0.0.0` or `0-unstable-…`), still reads as "the release file names no commit" (`read.1`). A commit that is present but not forty hex characters still refuses, as today (`read.2`).

`RELEASED` keeps its pattern. `release_version` treats `0.0.0`, main's placeholder, as no release's: `0.0.0+<commit>`, never `v0.0.0`.

`release_said` accepts a null commit only where `from` is `"release"` and the version is `v<x.y.z>`. A checkout's answer with no commit stays unread. `crew _release`'s usage, in `crew.py` and `plugin/bin/crew`'s header, says the commit is null where a release names none (`docs.2`).

`update_due` is unchanged. A start that recorded no commit is read by its digest alone. An installed crew with no commit makes no agent due for its plugin, and crew says it can't tell (`teams.19`).

### 6. The release commit is made by CI and tagged, and nothing reaches main

The release job, after git-cliff's notes:

```sh
sh set-version.sh "${TAG#v}"
git -c user.name='github-actions[bot]' -c user.email='41898282+github-actions[bot]@users.noreply.github.com' \
  commit -q -m "chore(release): $TAG" -- plugin/release.json plugin/.claude-plugin/plugin.json
git tag "$TAG"
git push origin "refs/tags/$TAG"
gh release create "$TAG" --verify-tag --title "$TAG" --notes-file body.md "${attach[@]}"
```

The commit is made by path (`code.6`). The tag is pushed alone, with no force and no branch (`state.5`). Main is untouched (`state.3`). The release commit's subject is `chore`, so git-cliff's notes leave it out (`cliff.toml`). The notes' cut over 120,000 bytes stays.

### 7. CI reckons from the newest tag by version

- **Version job:** `git-cliff --unreleased --bumped-version`. `--unreleased` starts the range at the newest tag, which is off main's history (Flume's reading).
- **Conventional job:** `last="$(git tag --list 'v*' --sort=-v:refname | head -n 1)"`, checking `"${last:-$BEFORE}..HEAD"`. A tag's release commit has the pushed commit as its parent, so `R..HEAD` is the commits main took since.
- **`release-preview`** in `devenv.nix` already runs `git cliff --unreleased --bump` and is unchanged.

### Rules relied on

`code.1` (POSIX sh and awk on CI; the Python standard library), `code.2`, `code.6` (the release commit by path), `code.7` (`tag_source`, `checkout_version`, `release_read` decide on facts), `read.1`, `read.2`, `state.3`, `state.5`, `flake.1`, `flake.3`, `teams.19`, `tests.4`, `tests.10`, `tests.11`, `docs.2`, `docs.6`, `docs.7`.

### Departures

- **`code.10`.** It keeps the version in no file, tags the pushed commit, and leaves the manifest's version to no release. Under this change, main's tree names `0.0.0` in `plugin/release.json` and in crew's manifest. A release's tag names a release commit, cut from the pushed commit, that writes the release's version into both. Nothing is committed back to main and no tag is moved, so that part of the rule holds. Why: principle 14 and Boomdrive record 0023 call for crew's own source to say its version, and Flume's release is the family's form. Amending `code.10`, and the record behind it, is the design agent's (`docs.7`).
- **`docs.7`** (proposed): this change edits no rule page.

## Risks / Trade-offs

- **git-cliff and an off-main tag.** The version job and notes rely on `--unreleased` starting at a tag that is not in HEAD's history. Flume's CI releases this way.
- **A tag pushed before its release.** If `gh release create` fails after the tag is pushed, the next run finds the tag released and makes no GitHub release. The same holds for Flume, and the cure is a hand `gh release create` at the tag.
- **More git calls for a checkout's version.** One `for-each-ref`, one `log`, usually one `merge-base` and one `rev-list`, in place of one `describe`.
- **One version, two commits.** A checkout at P and a build of the tag R both read `v0.56.0`, with commits P and R. A host that moves between live and released loading sees a commit change, so its agents are due once.

## Migration Plan

Nothing moves. Tags up to the last one made the old way name main's own commits, and `tag_source` reads them so. The first push to main after this lands is released the new way. git-cliff finds the newest tag by version, the conventional check starts there, and the release commit is cut from the pushed commit.

## After deploy

None. The release job runs on the push that lands this change, with nobody's step. Its commands are pinned by `t-release`, and what crew reads of a release commit is proven in the contract tier against a release commit made the same way.

## Task notes

**1.1** The tree's version and its writer:
- `plugin/release.json`: `{"version": "0.0.0"}` on one line with a newline, the form `set-version.sh`'s awk rewrites.
- `plugin/.claude-plugin/plugin.json`: `"version": "0.0.0"`.
- `set-version.sh` at the root, Flume's structure (`put <file> <awk>`). One program each for the release file and the manifest, matching `/^ *"version": "[^"]*",?$/` in the manifest and `"version": "[^"]*"` in the release file's one line. Usage text and the version check as Flume's.
- `tests/t-release.sh`, its opening comment saying what it proves, guarded by `${TESTS:?…}` (`tests.2`), with a `# Reads:` line naming `set-version.sh`, `plugin/release.json` and `.github/workflows/release.yml`. Cases:
  - Main's two files at `0.0.0`, the release file's one key `version`, read with `jq`.
  - `set-version.sh 98.76.54 "$T/copy"` on a copy leaves both at `98.76.54`, and `diff` of each file shows only version lines changed.
  - `set-version.sh 0.56` exits non-zero, saying it is not a version `major.minor.patch`, and neither file changes.
  - A copy whose manifest has no `version` line is refused, naming `plugin/.claude-plugin/plugin.json`.
- Run `tests/moon-tasks` and commit `tests/moon.yml`.

**2.1** In `plugin/lib/crew.py`:
- `release_read`: an absent or null `commit` beside a version that `RELEASED` matches and that is not `0.0.0` reads as `({"commit": None, "version": v}, None)`. Any other absent or null commit stays "the release file names no commit". A present commit that is not forty hex characters keeps that refusal.
- `release_version`: `0.0.0` reads as `0.0.0+<commit7>`.
- `crew_read`: a release read with no commit sets `commit` None, `version` `release_version`'s for a release (`v<x.y.z>`), `from` `"release"` and `unread` None.
- Update the `RELEASE` comment, which no longer calls the file the build's alone.
- `tests/py/test_release.py`:
  - Split `test_a_file_whose_commit_is_not_forty_hexadecimal_characters_reads_as_no_release`: None and absent read as version-only for `0.44.1`, and the malformed values are refused.
  - Add cases for `0.0.0` and `0-unstable-…` with no commit (refused), for `crew_read` of `{"version": "0.56.0"}`, and for `release_version("0.0.0", COMMIT)`.

**2.2** `release_said`:
- Where `commit` is None, accept only `from == "release"` with a version matching `v` plus `RELEASED`, not `v0.0.0`. Every other check is as now.
- `release_cmd`'s description and `plugin/bin/crew`'s `_release` usage lines say the commit is null where a release names none.
- Cases in `TestInstalled`: an answer `{"root", "commit": null, "version": "v0.56.0", "from": "release", "unread": null}` reads as itself, and the same with `from: "checkout"` reads as unread, "its answer names no commit".

**2.3** Pure functions beside `git_version`:
- `tag_source(tag, commit, parents, subject)` returns `parents[0]` where `subject == f"chore(release): {tag}"` and there is a parent, else `commit`.
- `checkout_version(tag, past)` returns `tag` for 0, else `f"{tag}+{past}"`.
- Logic cases in `tests/py/test_release.py` for a release commit, a main commit, a release-commit subject naming another tag (its own commit), and the version string.

**2.4** `git_version(root)` as Decision 4:
- Keep its return shape and its fallback to `rev-parse HEAD` with version None.
- Peel tags with `%(objectname)` and `%(*objectname)` (an annotated tag's commit).
- New `tests/contract/test_release.py`, using conftest's `repo` fixture with no global config. Each case names `crew.git_version` as what assumes git's behaviour:
  - Main with commits A, P, an older `v0.55.0` tagged on A.
  - A release commit R cut from P on a detached HEAD, its `plugin/release.json` written with `0.56.0` as the release job writes it, committed `chore(release): v0.56.0` and tagged `v0.56.0`. The test writes the file itself, so the contract task's inputs need no `set-version.sh`.
  - Main moved two past P reads `v0.56.0+2`. Main at P reads `v0.56.0`. Detached at R reads `v0.56.0`. A branch from A plus three reads `v0.55.0+3`. A repository with no tags reads its commit and no version.

**2.5** In `tests/t-session-hook.sh`, replace the `git describe` lines with `crew _release`'s answer for the same checkout, `jq -r .commit` and `.version` (empty for null). The start's record must equal them.

**3.1** The flake:
- `nix/version.nix`: `{ lib }: { release, date }:` as Decision 3. It throws `"crew: plugin/release.json gives version ${...}, neither x.y.z nor 0.0.0"`.
- `flake.nix`'s `version` comes from it, with `release = lib.importJSON ./plugin/release.json` and today's `date`. Its comment cites the release file in place of "crew keeps its version in no file".
- `nix/moon.yml`: `/plugin/release.json` among `typecheck`'s and `test`'s inputs.
- `nix/tests/version.nix`, registered in `nix/tests/default.nix`'s `test`. Cases: `0.56.0` gives itself; `0.0.0` with `20261109…` gives `0-unstable-2026-11-09`; `0.56` fails (`builtins.tryEval`).
- `nix/tests/package.nix`: the flake's own package on main's tree has a version starting `0-unstable-`.
- nixfmt, statix and deadnix clean.

**3.2** `nix/packages/crew.nix`:
- Its comments say the package holds the tree's release file and writes `{commit, version}` over it where the flake knows the commit.
- The no-commit case in `nix/tests/package.nix` keeps its two checks, `release` null and the install writing no release file. Its comment says the package then holds the tree's file.

**4.1** `.github/workflows/release.yml` as Decisions 6 and 7:
- Its header comment and the release job's comment say the tag names a release commit cut from the pushed commit.
- `cliff.toml`'s header no longer says the version lives only in the tag. It lives in the tag's release commit.
- Cases in `tests/t-release.sh`, reading the workflow's text:
  - The release job runs `sh set-version.sh "${TAG#v}"`, commits by path the two files as `chore(release): $TAG`, runs `git tag "$TAG"`, pushes `refs/tags/$TAG` with no other refspec and no `+`, and runs `gh release create "$TAG" --verify-tag`.
  - No `--target`.
  - The version job runs `git-cliff --unreleased --bumped-version`.
  - The conventional job uses `git tag --list 'v*' --sort=-v:refname` and no `git describe`.

**5.1** `README.md`:
- The paragraph on what each start records says a build's version comes from `plugin/release.json`, which crew's tree holds at `0.0.0` on main and at the release's version at its tag. A build adds the commit it knows, and a copy of a tag's `plugin/` reads as `v<x.y.z>` with no commit.
- The flake section drops "The file is the build's alone, never the tree's". The package's version is the release file's, `0-unstable-<date>` on main.
- Say where crew's releases are described, if README has no such line: a release's tag names a release commit that `set-version.sh` writes, and `devenv shell -- release-preview` shows the next one.
- `t-docs` must still pass. Add a phrase check for the release commit if `t-docs` pins README's release words elsewhere.
