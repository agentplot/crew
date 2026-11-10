# How crew is released (crew-release): main's tree names no release, its release file, plugin/release.json, giving
# version 0.0.0 and no other key, and crew's manifest 0.0.0; set-version.sh, which the release job runs on the commit it
# releases, run on a scratch copy of those files with a version no release has, leaves each giving that version and
# changes no line but the one that gives it, refuses a version that is not major.minor.patch before it touches a file,
# and refuses a file it finds no version in, naming it.
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
