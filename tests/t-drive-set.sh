# crew drive set through the crew command on the stubs (tests.11, tests.12), on mac-studio with its teams file removed
# as Boomdrive's setup finds a person's Mac: a state repository crew cannot fetch from is refused naming it, with no
# teams file made, since it reads the branch before it writes; with an empty state repository it writes the teams file
# crew then reads, makes pat/main with crew state init's files, and records one drive.set entry naming the keys it
# changed, running nothing on another host; crew main up then starts pat's main level from that file. Its one case beyond
# the wiring: the same command again changes no byte of the file, no commit of the branch and no entry, and says
# unchanged and exists. What it decides, its flags, the file it writes, a link and an aside, is the logic tier's
# (tests/py/test_drive_set.py).
# Reads: plugin/hooks/
. "${TESTS:?run crew tests through tests/run, which puts stub herdr, ssh and claude first}/lib.sh" || exit 2
world
teams=$(home_of mac-studio)/.config/crew/teams.json
rm "$teams"
folder=$(space mac-studio pat)
blueprints pat/blueprints >/dev/null
clone pat/blueprints "$folder/blueprints/main"
day=$(date -u +%F)

# set_pat <state repository> [<flag>...]: crew drive set pat as Boomdrive's setup runs it on a person's Mac
set_pat() {
  local state=$1; shift
  crew drive set pat --state "$state" --blueprints pat/blueprints --machine mac-studio --session pat --folder "$folder" \
    --repos pat/blueprints --accounts design pat --accounts planner pat --accounts reviewer pat --accounts ops pat \
    --accounts operator pat --flume design false --flume planner false --flume reviewer false --flume ops false \
    --flume operator false --review 5 4 --hosts mac-studio mac-studio darwin --console "$folder" "$@"
}

: > "$CREW_TEST_LOG"
expect_fail "could not fetch pat/main of nobody/crew-state over https" set_pat nobody/crew-state
[[ ! -e $teams ]] || fail "a refused crew drive set made a teams file"
ok "a state repository crew cannot fetch from is refused naming it, and no teams file is made"

state_repo pat/crew-state
ps=$(remote pat/crew-state)
expect_ok set_pat pat/crew-state
has "$out" "$teams: drive pat set, changing drives.pat, hosts.mac-studio, consoles.pat"
has "$out" "pat/main of pat/crew-state $(git --git-dir "$ps" rev-parse --short "$(git --git-dir "$ps" log -1 --format=%H --invert-grep --grep='^runs(' pat/main)"): started an empty plan"
expect_ok crewpy labels; eq "$out" "pat"
files=$(git --git-dir "$ps" ls-tree --name-only pat/main)
for f in plan.rec moves.rec proposals.rec; do grep -qx "$f" <<<"$files" || fail "pat/main has no $f"; done
entries=$(git --git-dir "$ps" show "pat/main:runs/mac-studio/$day.rec")
eq "$(recsel -e "Act = 'drive.set'" -P On <<<"$entries")" "drive/pat"
eq "$(recsel -e "Act = 'drive.set'" -P Why <<<"$entries")" "set drives.pat, hosts.mac-studio, consoles.pat"
grep -q " ssh " "$CREW_TEST_LOG" && fail "crew drive set ran a command on another host"
ok "crew drive set writes the teams file crew reads, makes pat/main with crew state init's files, and records one drive.set entry naming the keys it changed, running no ssh"

expect_ok crew main up pat
for a in pat-design pat-planner pat-ops pat-operator; do has "$out" "$a started"; done
eq "$(jq -r 'select(.agent == "pat-planner") | .cwd' "$CREW_TEST_CLAUDE_LOG" | tail -1)" "$folder/blueprints/main"
ok "crew main up starts the main level of the drive crew drive set named"

before=$(cat "$teams"); commits=$(git --git-dir "$ps" rev-list --count pat/main)
record() { cat "$(home_of mac-studio)"/.local/state/crew/pat/runs/*/*.rec; }
was=$(record)
expect_ok set_pat pat/crew-state --json
eq "$(jq -r '"\(.teams.outcome) \(.teams.changed | length) \(.state.outcome)"' <<<"$out")" "unchanged 0 exists"
eq "$(cat "$teams")" "$before"
eq "$(git --git-dir "$ps" rev-list --count pat/main)" "$commits"
eq "$(record)" "$was"
ok "the same command again changes no byte of the file, no commit and no entry, and says unchanged and exists"
