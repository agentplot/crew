# How crew is released (crew-release): main's tree names no release, its release file, plugin/release.json, giving
# version 0.0.0 and no other key, and crew's manifest 0.0.0; set-version.sh, which the release job runs on the commit it
# releases, run on a scratch copy of those files with a version no release has, leaves each giving that version and
# changes no line but the one that gives it, refuses a version that is not major.minor.patch before it touches a file,
# and refuses a file it finds no version in, naming it. CI's release job, read from its workflow, runs set-version.sh on
# the pushed commit, commits the two files by path as chore(release): <tag>, tags that commit, pushes the tag alone and
# publishes the release at it, with no --target; its version job reckons with git-cliff's --unreleased, and its
# conventional job starts at the newest v* tag by version, never git describe, since the tag is off main's history.
# Reads: set-version.sh plugin/release.json .github/workflows/release.yml
. "${TESTS:?run crew tests through tests/run, which puts stub herdr, ssh and claude first}/lib.sh" || exit 2

files=(plugin/release.json plugin/.claude-plugin/plugin.json)

eq "$(jq -c 'keys' "$CREW/plugin/release.json")" '["version"]'
eq "$(jq -r '.version' "$CREW/plugin/release.json")" 0.0.0
eq "$(jq -r '.version' "$CREW/plugin/.claude-plugin/plugin.json")" 0.0.0
ok "main's release file gives version 0.0.0 and no other key, and crew's manifest gives 0.0.0"

# copy <folder>: main's two files under <folder>, at their paths in crew's tree; main's own are kept under $T/main
mkdir -p "$T/main/plugin/.claude-plugin"
cp "$CREW/plugin/release.json" "$T/main/plugin/release.json"
cp "$CREW/plugin/.claude-plugin/plugin.json" "$T/main/plugin/.claude-plugin/plugin.json"
copy() { rm -rf "$1"; cp -R "$T/main" "$1"; }
# changed <file under the copy>: the lines diff finds changed from main's file, removed then added
changed() { diff "$T/main/$1" "$T/copy/$1" | grep '^[<>]' || true; }

copy "$T/copy"
expect_ok sh "$CREW/set-version.sh" 98.76.54 "$T/copy"
for f in "${files[@]}"; do
  eq "$(jq -r '.version' "$T/copy/$f")" 98.76.54
  d=$(changed "$f")
  eq "$(grep -c . <<< "$d")" 2
  eq "$(grep -c '^< .*"version": "0\.0\.0"' <<< "$d")" 1
  eq "$(grep -c '^> .*"version": "98\.76\.54"' <<< "$d")" 1
done
[[ ! -e $T/copy/plugin/release.json.set-version && ! -e $T/copy/plugin/.claude-plugin/plugin.json.set-version ]] \
  || fail "set-version.sh left a scratch file beside a file it wrote"
ok "set-version.sh writes a release's version into the release file and crew's manifest, changing no other line"

copy "$T/copy"
expect_fail "0.56 is not a version major.minor.patch" sh "$CREW/set-version.sh" 0.56 "$T/copy"
for f in "${files[@]}"; do eq "$(changed "$f")" ""; done
ok "set-version.sh refuses a version that is not major.minor.patch and changes neither file"

copy "$T/copy"
jq 'del(.version)' "$T/main/plugin/.claude-plugin/plugin.json" > "$T/copy/plugin/.claude-plugin/plugin.json"
expect_fail "plugin/.claude-plugin/plugin.json gives no version" sh "$CREW/set-version.sh" 98.76.54 "$T/copy"
[[ ! -e $T/copy/plugin/.claude-plugin/plugin.json.set-version ]] || fail "set-version.sh left a scratch file beside the manifest it refused"
ok "set-version.sh refuses a manifest that gives no version, naming it"

# job <name>: the lines of the workflow's job, from its key to the next job's, or the comment above it
workflow="$CREW/.github/workflows/release.yml"
job() { awk -v key="  $1:" '$0 == key { on = 1; next } on && /^  [^ ]/ { exit } on' "$workflow"; }
# line <text> <lines>: the number of the first of the lines that has the text, 0 where none does
line() { awk -v t="$1" 'index($0, t) { print NR; found = 1; exit } END { if (!found) print 0 }' <<< "$2"; }

release=$(job release)
steps=('sh set-version.sh "${TAG#v}"'
  'commit -q -m "chore(release): $TAG" -- plugin/release.json plugin/.claude-plugin/plugin.json'
  'git tag "$TAG"'
  'git push origin "refs/tags/$TAG"'
  'gh release create "$TAG" --verify-tag')
last=0
for step in "${steps[@]}"; do
  n=$(line "$step" "$release")
  (( n > last )) || fail "the release job does not run, after what goes before it: $step"$'\n'"$release"
  last=$n
done
lacks "$release" "--target"
eq "$(grep -c 'git push' "$workflow")" 1
lacks "$(grep 'git push' "$workflow")" "+"
lacks "$(grep 'git push' "$workflow")" "--force"
ok "the release job writes the version, commits the two files by path as chore(release): <tag>, tags that commit, pushes the tag alone and publishes the release at it"

has "$(job version)" "git-cliff --unreleased --bumped-version"
conventional=$(job conventional)
has "$conventional" "git tag --list 'v*' --sort=-v:refname"
lacks "$conventional" "git describe"
ok "the version job reckons with git-cliff's --unreleased, and the conventional job starts at the newest v* tag by version"
