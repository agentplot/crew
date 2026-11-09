# Sourced by every test, in its scratch directory $T. `world` builds the fleet the fixtures describe:
#
#   mac-studio (darwin)                         chuck-herdr-alpha (nixos, the box)
#     madswan, in madswan-1, folder madswan       wldn, in wldn-3, folder willdan
#     swancloud, in swancloud-1, folder madswan
#     consoles: wldn (folder willdan), madswan    consoles: wldn (folder willdan)
#     and swancloud (folder madswan)
#
# Each host's teams file (teams_json <host>) is the one file crew reads of its drives (record 0064): the three drives,
# each with its machine, session, folder, the repos that folder keeps and each role's account; both hosts, each with
# its ssh name and kind; and the consoles that host opens, each with its folder. No hosts file is written. Each host has
# its own HOME under hosts/<host>/home and its folders under hosts/<host>/work/<space>. Commands run as mac-studio
# unless HOST says otherwise.
set -euo pipefail
CREW=$(cd "$TESTS/.." && pwd -P)
export CREW_TEST_ROOT=$T CREW_TEST_LOG=$T/calls.log CREW_TEST_CLAUDE_LOG=$T/claude.log
# What a test leaves running ends with it, passed or failed: tests/slot ends whatever is left in the test's process
# group once the test has ended, and a card's plannotator session, which crew starts in a session of its own, ends once
# the test's own shell, CREW_TEST_PID, has (tests/stubs/plannotator).
export CREW_TEST_PID=$$
export PATH="$TESTS/stubs:$PATH" GIT_CONFIG_NOSYSTEM=1 GIT_TERMINAL_PROMPT=0
unset CREW_AGENT CREW_LABEL FLUME_PLACE FLUME_AGENT FLUME_STAGE HERDR_PANE_ID HERDR_WORKSPACE_ID HERDR_TAB_ID HERDR_ENV HERDR_BIN_PATH HERDR_SOCKET_PATH HERDR_SESSION SLUICE_BRANCH GIT_DIR GIT_WORK_TREE
# A suite an agent starts carries its Claude session's process id, which crew's waits end with (teams.24): a test's
# wait runs in no session but one the test names.
unset CLAUDE_PID
# A wt run that starts the suite, a hook's, hands it worktrunk's own variables, among them the file its shell wrapper
# reads a cd from: a test's wt never writes there, or the run ends trying to cd into a removed scratch dir.
unset $(env | sed -n 's/^\(WORKTRUNK_[A-Za-z0-9_]*\)=.*/\1/p')
# A test's wt, crew's tidy among them, reads its config and approvals under the simulated host's HOME, never the user's.
unset XDG_CONFIG_HOME
HOST=${HOST:-mac-studio}
# The user at a shell, as crew names them in what it writes: <me>@<host>.
me=$(python3 -c 'import getpass; print(getpass.getuser())')
: > "$CREW_TEST_LOG"; : > "$CREW_TEST_CLAUDE_LOG"
# The test's own commands (making kits and remotes) run with a scratch HOME too, never the user's.
export HOME=$T/home; mkdir -p "$HOME"

home_of() { echo "$T/hosts/$1/home"; }
space() { echo "$T/hosts/$1/work/$2"; }
as() { local h=$1; shift; (export CREW_TEST_HOST=$h HOME; HOME=$(home_of "$h"); cd "$HOME" && "$@"); }
crew() { as "$HOST" "$CREW/plugin/bin/crew" "$@"; }
crewpy() { as "$HOST" python3 "$CREW/plugin/lib/crew.py" "$@"; }
remote() { echo "$T/remotes/$1.git"; }

fail() { echo "FAIL: $*" >&2; exit 1; }
# The real sleep, for a test's own waits: the stub's returns at once.
zzz=$(type -a -P sleep | grep -vxF "$TESTS/stubs/sleep" | head -1)
# nap <seconds>: a pause that starts no process: a read that waits on a fifo nothing writes, $T/.pause, held open on fd 9,
# which the stubs pause on too. A read on `<> <(:)` is no pause on macOS, which refuses a read-write open of a pipe's
# /dev/fd and so returns at once.
mkfifo "$T/.pause"; exec 9<>"$T/.pause"
nap() { read -rt "$1" -u 9 _ || true; }
# until_ok <cmd...>: wait until the command succeeds, for up to ten minutes, a limit that holds on a host under heavy
# load (tests.8). It looks at once, then a tenth of a second later, each pause twice the last up to a second, so a wait
# that is over at once costs no pause and a long one runs its command about once a second rather than ten times;
# the wait ends as soon as it succeeds, and returns non-zero when it never did.
until_ok() {
  local end=$((SECONDS + 600)) gap=1
  until "$@"; do
    (( SECONDS < end )) || return 1
    nap "$((gap / 10)).$((gap % 10))"; (( gap = gap * 2 > 10 ? 10 : gap * 2 ))
  done
}
ok() { echo "ok: $*"; }
# expect_ok <cmd...>: it succeeds; its output is in $out
expect_ok() { out=$("$@" 2>&1) || fail "expected success: $*"$'\n'"$out"; }
# expect_fail <text> <cmd...>: it fails, saying <text>; its output is in $out
expect_fail() {
  local want=$1; shift
  if out=$("$@" 2>&1); then fail "expected failure: $*"$'\n'"$out"; fi
  [[ $out == *"$want"* ]] || fail "expected '$want' from: $*"$'\n'"$out"
}
has() { [[ $1 == *"$2"* ]] || fail "expected '$2' in:"$'\n'"$1"; }
lacks() { [[ $1 != *"$2"* ]] || fail "did not expect '$2' in:"$'\n'"$1"; }
eq() { [[ $1 == "$2" ]] || fail "expected '$2', got '$1'"; }
calls() { cat "$CREW_TEST_LOG"; }
# merge_as <agent> <place> <branch>: what Flume does to submit a place's work: submits the place's head without
# waiting, then waits on the submission with sluice wait, returning its exit
merge_as() {
  local id
  id=$(cd "$2" && SLUICE_AGENT=$1 sluice submit "$3" --no-wait --json 2>/dev/null | jq -r .id) && [[ $id =~ ^[0-9]+$ ]] || return 2
  (cd "$2" && sluice wait "$id" --timeout 9m --json >/dev/null 2>&1)
}
launches() { cat "$CREW_TEST_CLAUDE_LOG"; }

fixtures() {  # each host's teams file (version 6, or an older one named: teams_old), written into its HOME; no hosts file
  local v=${1:-6} h
  for h in mac-studio chuck-herdr-alpha; do
    mkdir -p "$(home_of $h)/.config/crew"
    if [[ $v == 6 ]]; then teams_json $h; else teams_old "$v"; fi > "$(home_of $h)/.config/crew/teams.json"
  done
}

# teams_json <host>: the host's teams file, version 6, every fact crew reads of its drives and of the hosts that serve
# them (record 0064): its drives under `drives`, each named by its label with no `partition`, with its machine and
# session, its herdr session's `folder` there, the `repos` that folder keeps, each main-level role's account, as the
# hosts file's sessions gave them (wldn-3 on credits, madswan-1 and swancloud-1 on madswan), and its `flume`, every role
# standing; `hosts`, both hosts with their ssh names and kinds; and the `consoles` this host opens, each drive's console
# in the folder of the session named for its label, as the hosts file gave it
teams_json() {
  local box=chuck-herdr-alpha consoles
  case ${1:?teams_json names the host its file is for} in
    mac-studio) consoles="\"wldn\": \"$(space mac-studio willdan)\", \"madswan\": \"$(space mac-studio madswan)\", \"swancloud\": \"$(space mac-studio madswan)\"" ;;
    "$box") consoles="\"wldn\": \"$(space $box willdan)\"" ;;
    *) fail "teams_json: no host $1" ;;
  esac
  cat <<EOF
{ "version": 6,
  "hosts": {"$box": {"ssh": "$box", "kind": "nixos"}, "mac-studio": {"ssh": "mac-studio", "kind": "darwin"}},
  "consoles": {$consoles},
  "drives": [
    { "label": "wldn", "blueprints": ["WilldanGroup/willdan-blueprints"],
      "state": "WilldanGroup/crew-state", "review": {"every": 5, "hours": 4},
      "machine": "$box", "session": "wldn-3", "folder": "$(space $box willdan)",
      "repos": ["agentplot/crew", "WilldanGroup/atlas-kit", "WilldanGroup/breadboard-kit", "WilldanGroup/switchboard-kit",
                "WilldanGroup/willdan-blueprints"],
      "accounts": {"design": "credits", "planner": "credits", "reviewer": "credits", "ops": "credits", "operator": "credits"},
      "flume": {"design": false, "planner": false, "reviewer": false, "ops": false, "operator": false} },
    { "label": "madswan", "blueprints": ["afterthought/blueprints", "agentplot/blueprints"],
      "state": "afterthought/crew-state", "review": {"every": 5, "hours": 4},
      "machine": "mac-studio", "session": "madswan-1", "folder": "$(space mac-studio madswan)",
      "repos": ["afterthought/blueprints", "agentplot/crew", "afterthought/swancloud"],
      "accounts": {"design": "madswan", "planner": "madswan", "reviewer": "madswan", "ops": "madswan", "operator": "madswan"},
      "flume": {"design": false, "planner": false, "reviewer": false, "ops": false, "operator": false} },
    { "label": "swancloud", "blueprints": ["afterthought/blueprints"],
      "state": "afterthought/crew-state", "review": {"every": 5, "hours": 4},
      "machine": "mac-studio", "session": "swancloud-1", "folder": "$(space mac-studio madswan)",
      "repos": ["afterthought/blueprints", "agentplot/crew", "afterthought/swancloud"],
      "accounts": {"design": "madswan", "planner": "madswan", "reviewer": "madswan", "ops": "madswan", "operator": "madswan"},
      "flume": {"design": false, "planner": false, "reviewer": false, "ops": false, "operator": false} } ] }
EOF
}

# teams_old <version>: the teams file as the machine's configuration wrote it for an older crew, at that version, its
# drives under `partitions` with a team listed beside them, which crew refuses
teams_old() {
  teams_json mac-studio | jq --argjson v "$1" '.version = $v | .partitions = .drives | del(.drives) | .teams = [{name: "swb-1", system: "Switchboard", machine: "chuck-herdr-alpha",
    session: "wldn-1", units: 4, repos: ["switchboard-kit", "willdan-blueprints"], flume: false}]'
}

gitconfig() {  # every host's git: an identity, and github.com over https rewritten to the bare remotes here
  cat > "$1/.gitconfig" <<EOF
[user]
	name = Test User
	email = test@example.com
[init]
	defaultBranch = main
[advice]
	detachedHead = false
[gc]
	auto = 0
[maintenance]
	auto = false
[receive]
	autogc = false
[fetch]
	writeCommitGraph = false
[pack]
	threads = 1
[index]
	threads = 1
[protocol "file"]
	allow = always
[url "file://$T/remotes/"]
	insteadOf = https://github.com/
EOF
}

world() {  # hosts, fixtures, crew's checkout where each host's teams file keeps it
  local h
  gitconfig "$HOME"
  for h in mac-studio chuck-herdr-alpha; do mkdir -p "$(home_of $h)" "$T/hosts/$h/work"; gitconfig "$(home_of $h)"; done
  fixtures
  mkdir -p "$(space chuck-herdr-alpha willdan)/crew" "$(space mac-studio madswan)/crew"
  ln -s "$CREW" "$(space chuck-herdr-alpha willdan)/crew/main"
  ln -s "$CREW" "$(space mac-studio madswan)/crew/main"
  state_repo WilldanGroup/crew-state; state_repo afterthought/crew-state
}

# state_repo <owner/name>: an empty bare remote, as a state repository is before crew state init
state_repo() { local r; r=$(remote "$1"); mkdir -p "$(dirname "$r")"; [ -d "$r" ] || git init -q --bare "$r"; }

commit_all() { git -C "$1" add -A && git -C "$1" commit -qm "${2:-wip}"; }
# act_tip [<ref>] [<git dir>]: the newest commit of a state branch, wldn/main of $ws unless named, that is an act's and
# no run-record entry's own, which follows each act on the branch as a commit of its own (read.5)
act_tip() { git --git-dir "${2:-$ws}" log -1 --format=%H --invert-grep --grep='^runs(' "${1:-wldn/main}"; }
# acts_since <commit> [<ref>] [<git dir>]: how many acts' commits the state branch holds since the commit, its entries'
# own commits left out
acts_since() { git --git-dir "${3:-$ws}" rev-list --count --invert-grep --grep='^runs(' "$1..${2:-wldn/main}"; }
# rewrite <file> <sed script>: the file edited in place, alike under macOS's sed and the GNU sed devenv's shell puts first
rewrite() { sed -e "$2" "$1" > "$1.new" && mv "$1.new" "$1"; }

# kit <host> <space> <name>: a kit's main checkout at <space>/<name>/main, with OpenSpec set up and a sluice policy
# naming the checks its bolt branches and main require, which a bolt is started only with (teams.5), and origin, GitHub,
# for both (plan.19): its origin is a bare remote under the test's remotes, as https://github.com/<owner>/<name>, its
# owner the one the host's teams file's drives name it under in their repos, its main pushed there. A kit already standing on its remote,
# made again on another host, is cloned from it.
kit() {
  local d r own; d=$(space "$1" "$2")/$3/main
  own=$(jq -r --arg n "$3" 'first(.drives[].repos[] | select(endswith("/" + $n))) // empty' \
    "$(home_of "$1")/.config/crew/teams.json" 2>/dev/null); own=${own:-kits/$3}
  r=$(remote "$own")
  if [ -d "$r" ]; then git clone -q "https://github.com/$own" "$d"; echo "$d"; return; fi
  mkdir -p "$d/openspec/changes/archive" "$d/openspec/specs" "$d/.config"
  git init -q "$d"; printf 'schema: spec-driven\n' > "$d/openspec/config.yaml"
  printf '[branches."bolt/*"]\nrequired = ["#check-full"]\nremote = "origin"\n\n[branches.main]\nrequired = ["#check-full"]\nremote = "origin"\n' > "$d/.config/sluice.toml"
  touch "$d/openspec/changes/archive/.keep" "$d/openspec/specs/.keep"; echo "# $3" > "$d/README.md"
  commit_all "$d" "chore: start $3"
  mkdir -p "$(dirname "$r")"; git clone -q --bare "$d" "$r"
  git -C "$d" remote add origin "https://github.com/$own"; git -C "$d" fetch -q origin
  echo "$d"
}
# push <checkout>: its main pushed to its origin, as a landing on GitHub's main leaves it, so crew reads it as main now
push() { git -C "$1" push -q origin main; }
# push_state <clone>: a hand edit of the state branch pushed as crew pushes its own writes (state.1): a push refused
# because the branch moved, an entry a crew command still running pushed at the same moment (read.5), is rebased onto
# the new tip and pushed again
push_state() {
  local n
  for n in 1 2 3 4 5 6 7 8 9; do
    git -C "$1" push -q origin wldn/main 2>/dev/null && return
    git -C "$1" pull -q --rebase origin wldn/main || return
  done
  git -C "$1" push -q origin wldn/main
}

# blueprints <owner/name>: a bare remote with signals/moves.rec and .gitattributes on main
blueprints() {
  local r w; r=$(remote "$1"); w=$T/seed-${1//\//-}
  mkdir -p "$(dirname "$r")"; git init -q --bare "$r"
  git init -q "$w"; mkdir -p "$w/signals"
  cat > "$w/signals/moves.rec" <<'EOF'
# One move per signal, appended through crew.

%rec: Move
%mandatory: Signal Move Date By
%allowed: Signal Move Target Reason Date By
%type: Move enum attach challenge new-territory answered drop route
%type: Date date
%key: Signal
%doc: A curation move over one signal, stored with its inputs.
EOF
  printf 'signals/moves.rec merge=union\n' > "$w/.gitattributes"
  commit_all "$w" "chore: start" && git -C "$w" push -q "$r" main
  echo "$r"
}

# pull <owner/name> <branch> <draft: true|false>: an open pull request from the branch into main on GitHub, as
# sluice's landing opens one, in the stub gh's file; prints its number
pull() {
  local f=$T/gh-pulls.json; [[ -e $f ]] || echo '[]' > "$f"
  jq --arg repo "$1" --arg head "$2" --argjson draft "$3" \
    '. + [{repo: $repo, number: (length + 1), head: $head, base: "main", state: "open", isDraft: $draft}]' "$f" > "$f.new" &&
    mv "$f.new" "$f" && jq 'length' "$f"
}
# drafted <number>: whether the stub gh holds that pull request a draft, true or false
drafted() { jq -r --argjson n "$1" '.[] | select(.number == $n) | .isDraft' "$T/gh-pulls.json"; }

# clone <owner/name> <dir>: a checkout of a bare remote, as a drive's folder keeps it
clone() { git clone -q "$(remote "$1")" "$2"; }

# change <dir> <name> [done] [total]: an OpenSpec change with planning complete and <done> of <total> tasks ticked,
# its proposal ending with the paths it touches, src/<name>/**
change() {
  local c=$1/openspec/changes/$2 i n=${4:-3} d=${3:-0}
  mkdir -p "$c/specs/x"
  printf '# Proposal\n\n## Why\n\nx\n\n## What Changes\n\n- y\n\n## Touches\n\n```\nsrc/%s/**\n```\n' "$2" > "$c/proposal.md"
  printf '# Design\n\nz\n' > "$c/design.md"
  printf '## ADDED Requirements\n\n### Requirement: X\nThe system SHALL x.\n\n#### Scenario: s\n- **WHEN** a\n- **THEN** b\n' > "$c/specs/x/spec.md"
  { echo "## 1. Work"; echo; for ((i = 1; i <= n; i++)); do if ((i <= d)); then echo "- [x] 1.$i task $i"; else echo "- [ ] 1.$i task $i"; fi; done; } > "$c/tasks.md"
}

# path_without <cmd>: this PATH less every directory holding <cmd>, with the tools crew needs kept by link
path_without() {
  local keep=$T/keep-$1 d c p=
  mkdir -p "$keep"
  for c in bash env python3 git jq awk sed grep tr cat head tail sort cut mkdir mktemp rm mv ls dirname basename seq; do
    d=$(command -v "$c" 2>/dev/null) && [[ $d == /* ]] && ln -sf "$d" "$keep/$c"
  done
  local IFS=:
  for d in $PATH; do [[ -x $d/$1 ]] || p=$p:$d; done
  echo "$keep$p"
}

# edit teams <python>: change the teams file on every host; the python statement changes `d` in place
edit() {
  local f h
  [[ $1 == teams ]] || fail "edit: no fixture $1: crew reads the teams file alone"
  for h in mac-studio chuck-herdr-alpha; do
    f=$(home_of $h)/.config/crew/teams.json
    python3 -c 'import json, sys
f = sys.argv[1]; d = json.load(open(f))
exec(sys.argv[2])
json.dump(d, open(f, "w"), indent=1)' "$f" "$2"
  done
}
part() { echo "[p for p in d['drives'] if p['label'] == '$1'][0]"; }
# role_stream <label> <role> <stream|false>: on every host, the drive's main-level role set to run as its kind in
# that Flume stream, or to stand (record 0047 move 6)
role_stream() { local s="'$3'"; [[ $3 == false ]] && s=False; edit teams "$(part "$1")['flume']['$2'] = $s"; }

# The Flume world: every bolt's work runs in Flume places, taken by a runner whose configuration names its
# repository (the user's ruling of 2026-11-01; Decision 1 of the-team-machinery-leaves).
# flume_world: a runner serving wldn on each host, its own branch wldn/runner/<host> on wldn's state repository, and
# the box's runner keeping switchboard-kit in its checkout ($k) in stream wldn where the world made one
flume_world() {
  [ -n "${k:-}" ] && keeps chuck-herdr-alpha switchboard-kit "$k"
  runner_writes chuck-herdr-alpha; runner_writes mac-studio
}
# keeps <host> <kit> <folder> [<stream>]: the runner on <host> keeps <kit> in <folder>, as its configuration names them,
# and the host's Flume configuration maps the kit to <stream> (wldn by default): the repository its repositories.rec
# names (runner_writes), and the repository and stream Flume's status of each place it takes of the kit names, which
# runner_writes gives a status naming none
keeps() {
  local d=$T/runner/$1; mkdir -p "$d"
  python3 -c 'import json, os, sys
f = sys.argv[1]; kept = json.load(open(f)) if os.path.exists(f) else {}
kept[sys.argv[2]] = [sys.argv[3], sys.argv[4]]; json.dump(kept, open(f, "w"))' "$d/keeps.json" "$2" "$3" "${4:-wldn}"
}
# runner_writes <host> [<request> <place> <status JSON>]...: wldn/runner/<host> on the state repository as that host's
# runner writes it, and crew never does: its runner.rec, and each request named answered launched at its place with
# Flume's status of the place as the runner carried it, beside those an earlier call named, a status naming no
# repository or stream given the folder the runner keeps the request's kit in and the stream its host maps it to
# (keeps), as Flume's status names them; and its repositories.rec, as Boomdrive's runner reports what it keeps, each kit
# kept on the host (keeps) by its forge address, <owner>/<kit>, the owner of the kit's stub remote where the test made
# one and any owner else, since crew matches a kit by its name, with its folder (runner.REPOSITORIES; Decision 1 of
# a-bolts-landing-on-main-reads-landed)
runner_writes() {
  local h=$1 d=$T/runner/$1 tree parent f; shift
  mkdir -p "$d"
  git --git-dir "$ws" show wldn/main:requests.rec > "$d/requests.rec" 2>/dev/null || : > "$d/requests.rec"
  python3 - "$CREW/plugin/lib" "$d" "$h" "$T/remotes" "$@" <<'EOF'
import glob, json, os, sys
sys.path.insert(0, sys.argv[1])
import runner
d, h, remotes, args = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:]
f = os.path.join(d, "kept.json")
kept = json.load(open(f)) if os.path.exists(f) else {}
keeps = json.load(open(os.path.join(d, "keeps.json"))) if os.path.exists(os.path.join(d, "keeps.json")) else {}
recs = [dict(l.split(": ", 1) for l in r.splitlines() if ": " in l and not l.startswith(("%", "#")))
        for r in open(os.path.join(d, "requests.rec")).read().split("\n\n")]
repo = {r["Request"]: r.get("Repo", "").split("/")[-1] for r in recs if "Request" in r}
for i in range(0, len(args), 3):
    status = json.loads(args[i + 2])
    for p in status.get("status", {}).get("places", []):
        if repo.get(args[i]) in keeps:
            folder, stream = keeps[repo[args[i]]]
            p.setdefault("repository", folder)
            p.setdefault("stream", {"name": stream, "from": "intent"})
    kept[args[i]] = [args[i + 1], status]
json.dump(kept, open(f, "w"))
t = os.path.join(d, "tidied.json")
tidied = set(json.load(open(t)) if os.path.exists(t) else []) - set(args[0::3])
json.dump(sorted(tidied), open(t, "w"))
at = "2026-10-31T12:01:00Z"
files = {"runner": runner.RUNNER + f"\nHost: {h}\nVersion: 0.1.0\nSince: 2026-10-31T11:00:00Z\n",
         "answers": runner.ANSWERS + "".join(f"\nRequest: {n}\nOutcome: launched\nPlace: {p}\nAt: {at}\n" for n, (p, _) in sorted(kept.items(), key=lambda x: int(x[0]))),
         "places": runner.PLACES + "".join(f"\nRequest: {n}\nPlace: {p}\nAt: {at}\nStatus: {json.dumps(s)}\n" for n, (p, s) in sorted(kept.items(), key=lambda x: int(x[0])) if n not in tidied),
         "repositories": runner.REPOSITORIES}
for kit, (folder, _) in sorted(keeps.items()):
    owners = sorted(os.path.basename(os.path.dirname(r)) for r in glob.glob(os.path.join(remotes, "*", f"{kit}.git")))
    files["repositories"] += f"\nRepository: {(owners or ['WilldanGroup'])[0]}/{kit}\nFolder: {folder}\n"
for name, text in files.items():
    open(os.path.join(d, f"{name}.rec"), "w").write(text)
EOF
  tree=$(for f in runner answers places repositories; do printf '100644 blob %s\t%s.rec\n' "$(git --git-dir "$ws" hash-object -w "$d/$f.rec")" "$f"; done |
    git --git-dir "$ws" mktree)
  parent=$(git --git-dir "$ws" rev-parse -q --verify "refs/heads/wldn/runner/$h") || parent=
  git --git-dir "$ws" update-ref "refs/heads/wldn/runner/$h" "$(git --git-dir "$ws" -c user.name=runner -c user.email=runner@example.com \
    commit-tree "$tree" ${parent:+-p "$parent"} -m "runner: $h")"
}
# runner_tidies <host> <request>...: wldn/runner/<host> rewritten as its runner writes it once Flume has tidied those
# requests' places: each request's answer kept, launched at its place, and its place dropped from places.rec, as deneb's
# runner on afterthought/runner/deneb answered request 88 launched and carried no place at all on 2026-11-08; a later
# runner_writes naming one of them carries it again
runner_tidies() {
  local h=$1; shift
  python3 -c 'import json, os, sys
t = sys.argv[1]; tidied = set(json.load(open(t)) if os.path.exists(t) else [])
json.dump(sorted(tidied | set(sys.argv[2:])), open(t, "w"))' "$T/runner/$h/tidied.json" "$@"
  runner_writes "$h"
}
# landed_status <place> <commit>: Flume's status of a place whose work has landed at the commit, as runner_writes takes it
landed_status() { printf '{"status":{"places":[{"place":"%s","phase":{"over":{"over":{"landed":{"commit":"%s"}}}},"current":"verify","stages":[]}]}}' "$1" "$2"; }
# request_of <work>: the number of the newest launch of the work (unit/<u>, chore/<c>, fix/<bolt>/<name>) in requests.rec
request_of() { git --git-dir "$ws" show wldn/main:requests.rec | recsel -t Request -e "Act = 'launch' && Work = '$1'" -P Request | tail -1; }
# flume_lands <host> <unit|chore> <name> <bolt> [<file>]: what Flume does with a launched unit or chore once it has
# built: its place, cut from the bolt on GitHub, commits its work, a unit's change written and archived and a chore's
# commit carrying its trailer, and submits it to the bolt through sluice, which lands it there as a merge commit
# carrying its verdict; then the runner on <host> carries Flume's status of the place, landed at the bolt's new head
flume_lands() {
  local h=$1 kind=$2 n=$3 b=$4 p=$T/flume/$3 head
  git -C "$k" fetch -q origin
  git -C "$k" worktree add -q -b "$kind/$n" "$p" "origin/bolt/$b"
  git -C "$p" branch -q --set-upstream-to "origin/bolt/$b"
  if [[ $kind == unit ]]; then
    change "$p" "$n" 3 3; mkdir -p "$p/openspec/changes/archive"; mv "$p/openspec/changes/$n" "$p/openspec/changes/archive/2026-10-31-$n"
    commit_all "$p" "docs($n): the change, archived"
  else
    echo "$n" > "$p/${5:-$n}"; git -C "$p" add -A && git -C "$p" commit -qm "chore($n): $n" -m "Chore: $n"
  fi
  merge_as "flume" "$p" "bolt/$b" || fail "$n's submission to bolt/$b failed"
  git -C "$k" fetch -q origin; head=$(git -C "$k" rev-parse "origin/bolt/$b")
  git -C "$k" worktree remove --force "$p"
  runner_writes "$h" "$(request_of "$kind/$n")" "$p" "$(landed_status "$p" "$head")"
}

# race <owner/name> <host> <agent> <crew args...>: the next push to that remote first lets this crew write land,
# run as <agent> on <host> from the remote's pre-receive hook, so the push in flight finds the branch moved.
race() {
  local r; r=$(remote "$1"); shift
  local host=$1 who=$2; shift 2
  printf 'CREW_TEST_HOST=%q HOME=%q CREW_AGENT=%q %q' "$host" "$(home_of "$host")" "$who" "$CREW/plugin/bin/crew" > "$T/race"
  printf ' %q' "$@" >> "$T/race"
  cat > "$r/hooks/pre-receive" <<'HOOK'
#!/usr/bin/env bash
refs=$(cat)
# With $CREW_TEST_ROOT/race.ref, only a push to that ref lets the competing write in.
if [ -f "$CREW_TEST_ROOT/race.ref" ] && ! grep -q " $(cat "$CREW_TEST_ROOT/race.ref")\$" <<<"$refs"; then exit 0; fi
if [ -f "$CREW_TEST_ROOT/race" ]; then
  cmd=$(cat "$CREW_TEST_ROOT/race"); rm "$CREW_TEST_ROOT/race"
  # Another agent's command, in a process of its own.
  (unset $(env | sed -n 's/^\(GIT_[A-Z_]*\)=.*/\1/p'); cd /; eval "$cmd") >> "$CREW_TEST_ROOT/race.log" 2>&1
fi
exit 0
HOOK
  chmod +x "$r/hooks/pre-receive"
}

# on_branch <kit main> <branch> <message> <file> <text>: a commit on the branch writing the file, made with no
# checkout of it, as a bolt's branch takes work in a test that is not the merge it proves
on_branch() {
  local idx=$T/on-branch.index blob tree c
  blob=$(printf '%s' "$5" | git -C "$1" hash-object -w --stdin)
  GIT_INDEX_FILE=$idx git -C "$1" read-tree "$2"
  GIT_INDEX_FILE=$idx git -C "$1" update-index --add --cacheinfo "100644,$blob,$4"
  tree=$(GIT_INDEX_FILE=$idx git -C "$1" write-tree); rm -f "$idx"
  c=$(git -C "$1" commit-tree "$tree" -p "$2" -m "$3")
  git -C "$1" update-ref "refs/heads/$2" "$c"
}

# place <kit main> <bolt> <unit>: the unit's worktree, made the way construct makes it
place() {
  local kd; kd=$(dirname "$1")
  git -C "$1" worktree add -q --track -b "unit/$3" "$kd/places/$3" "bolt/$2"
  echo "$kd/places/$3"
}
# stage <unit> [label]: the unit's stage as crew bolts reads it
stage() { crew bolts --label "${2:-wldn}" --json | jq -r --arg u "$1" '[.drives[].plans[].bolts[].units[] | select(.unit == $u) | .stage] | first // "none"'; }

# transcript <host> <session> [account folder]: a Claude Code transcript of that session on the host, its JSON lines
# read from standard input, in the account's folder (~/.claude unless named); prints its path
transcript() {
  local d; d=$(home_of "$1")/${3:-.claude}/projects/-work
  mkdir -p "$d"; cat > "$d/$2.jsonl"; echo "$d/$2.jsonl"
}

# ago <minutes>: the UTC time that many minutes ago, as a transcript's records carry it
ago() { python3 -c 'import datetime, sys; t = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=float(sys.argv[1])); print(t.strftime("%Y-%m-%dT%H:%M:%S.") + f"{t.microsecond // 1000:03d}Z")' "$1"; }

# herdr_state <host> <session> <jq>: what the stub herdr holds there
herdr_state() { jq -r "$3" "$(home_of "$1")/.stub-herdr/$2.json"; }
# bolt_world: the box's switchboard-kit and willdan-blueprints checkouts, and wldn's drive started, its plan
# empty, which a test's bolts and units fill as the planner's commands do
bolt_world() {
  world
  wb=$(blueprints WilldanGroup/willdan-blueprints); ws=$(remote WilldanGroup/crew-state)
  k=$(kit chuck-herdr-alpha willdan switchboard-kit); kd=$(dirname "$k")
  clone WilldanGroup/willdan-blueprints "$(space chuck-herdr-alpha willdan)/willdan-blueprints/main"
  crew state init wldn >/dev/null
}
