# crew as a source of its host's Flume (record 0057, teams.25), through the crew command on the stubs (tests.11,
# record 0022): the host's follower, crew _follow --once, writes crew's roles file from the teams file at its read, with
# madswan's and swancloud's ten standing entries on mac-studio and none of wldn's, the box's, makes the empty kinds folder
# beside it, runs no flume command and leaves the teams file as it was; a second read with nothing moved writes nothing;
# a teams file rewritten has the file renamed over, the old file left whole for a link that holds it; a teams file crew
# refuses leaves the file as it was and is named; and a host whose main level moved away keeps no entry, making no file
# where it had none. What each entry says is a logic case (tests/py/test_source.py).
# Reads: plugin/lib/board.py
. "${TESTS:?run crew tests through tests/run, which puts stub herdr, ssh and claude first}/lib.sh" || exit 2
world
box=chuck-herdr-alpha
# flume, logged and failing: crew runs none for its roles file
mkdir -p "$T/shim"
cat > "$T/shim/flume" <<'EOF'
#!/usr/bin/env bash
printf '%s flume %s\n' "${CREW_TEST_HOST:-?}" "$*" >> "$CREW_TEST_LOG"; exit 1
EOF
chmod +x "$T/shim/flume"
export PATH="$T/shim:$PATH"
roles_file() { echo "$(home_of "$1")/.local/state/crew/flume/roles.toml"; }
kinds_dir() { echo "$(home_of "$1")/.local/share/flume/kinds/crew"; }
teams_file() { echo "$(home_of "$1")/.config/crew/teams.json"; }
# entries <host>: each entry of the host's roles file as Flume reads it, address|agent|session|answers|answerer
entries() {
  python3 -c 'import sys, tomllib
for a, e in tomllib.load(open(sys.argv[1], "rb")).get("roles", {}).items():
    print("|".join([a, e["agent"], e["session"], e.get("answers", ""), str(e.get("answerer", ""))]))' "$(roles_file "$1")"
}
inode() { python3 -c 'import os, sys; s = os.stat(sys.argv[1]); print(s.st_ino, s.st_mtime_ns)' "$1"; }

# The follower's first read on mac-studio, the machine of madswan and swancloud: their ten entries, none of wldn's
cp "$(teams_file mac-studio)" "$T/teams.before"
: > "$CREW_TEST_LOG"
expect_ok crew _follow --once
got=$(entries mac-studio)
eq "$(wc -l <<<"$got" | tr -d ' ')" 10
for r in design planner reviewer ops operator; do
  has "$got" "madswan/$r|madswan-$r|madswan-1|"
  has "$got" "swancloud/$r|swancloud-$r|swancloud-1|"
done
has "$got" "madswan/ops|madswan-ops|madswan-1|a live system, a deploy or a landing|"
has "$got" "swancloud/operator|swancloud-operator|swancloud-1||True"
lacks "$got" "wldn/"
[ -d "$(kinds_dir mac-studio)" ] && [ -z "$(ls -A "$(kinds_dir mac-studio)")" ] || fail "crew's kinds folder is missing or not empty"
cmp -s "$T/teams.before" "$(teams_file mac-studio)" || fail "the follower changed the teams file"
lacks "$(calls)" " flume "
ok "the follower's first read writes madswan's and swancloud's entries, the empty kinds folder, and runs no flume"

# Nothing moved: the second read writes nothing
was=$(inode "$(roles_file mac-studio)")
expect_ok crew _follow --once
eq "$(inode "$(roles_file mac-studio)")" "$was"
ok "a read with the teams file unchanged leaves the roles file alone"

# The teams file rewritten: the file renamed over, a link to the old one holding it whole
ln "$(roles_file mac-studio)" "$T/held.toml"
cp "$(roles_file mac-studio)" "$T/roles.before"
rewrite "$(teams_file mac-studio)" 's/"session": "madswan-1",/"session": "madswan-1", "roles": {"planner": {"session": "madswan-2"}},/'
expect_ok crew _follow --once
got=$(entries mac-studio)
has "$got" "madswan/planner|madswan-planner|madswan-2|the plan|"
has "$got" "madswan/reviewer|madswan-reviewer|madswan-2||"
has "$got" "madswan/ops|madswan-ops|madswan-1|"
cmp -s "$T/held.toml" "$T/roles.before" || fail "the roles file was edited in place"
ok "a rewritten teams file has the roles file renamed over the old one"

# A teams file crew refuses: the roles file as it was, the teams file named
cp "$(roles_file mac-studio)" "$T/roles.before"
was=$(inode "$(roles_file mac-studio)")
rewrite "$(teams_file mac-studio)" 's/"version": 5/"version": 4/'
expect_fail "$(teams_file mac-studio) is version 4" crew _follow --once
eq "$(inode "$(roles_file mac-studio)")" "$was"
cmp -s "$T/roles.before" "$(roles_file mac-studio)" || fail "a refused teams file changed the roles file"
ok "a teams file crew refuses leaves the roles file as it was, naming the teams file"

# The box: wldn's main level moved to mac-studio's wldn-5 makes no file where there was none; back on the box, its five
# entries; moved again, a file with no entry
moved='s/"machine": "chuck-herdr-alpha", "session": "wldn-3"/"machine": "mac-studio", "session": "wldn-5"/'
rewrite "$(teams_file $box)" "$moved"
HOST=$box expect_ok crew _follow --once
[ ! -e "$(roles_file $box)" ] || fail "a host with no main level was given a roles file"
fixtures
HOST=$box expect_ok crew _follow --once
got=$(entries $box)
eq "$(wc -l <<<"$got" | tr -d ' ')" 5
has "$got" "wldn/planner|wldn-planner|wldn-3|the plan|"
rewrite "$(teams_file $box)" "$moved"
HOST=$box expect_ok crew _follow --once
[ -e "$(roles_file $box)" ] || fail "the roles file of a host whose main level moved away was removed"
eq "$(entries $box)" ""
lacks "$(calls)" " flume "
ok "a host whose main level moved away keeps a roles file with no entry, and makes none where it had none"
