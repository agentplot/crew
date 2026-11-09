# A partition's main-level roles that run as their kinds, through the crew command on the stubs (tests.11, record
# 0022; record 0047 move 6): with madswan's planner and operator named a stream, a tell to the planner with no
# standing agent of it up is an ask of the role from its sender on madswan's drive branch, its role record written in
# the same commit, nothing typed into any pane and one ask entry holding the words' length and never their text, which
# crew trace of the run lists; a send to madswan is an ask of its operator carrying whom it was for; and a tell to wldn's
# planner, which stands, is refused as today with nothing asked. The planner's run, named from its place: crew role start
# takes both asks of it in one turn, writes its brief to the host's file and prints it, each ask and the card the user
# answered in its name, read from Pending You as madswan-planner; an ask written after the start is not the turn's; crew
# role end, as the turn's prompt names it, answers the turn and writes the report; and outside a run each is refused.
# The user opens madswan's design agent: with no run of it in mac-studio's runner's records, an open ask from the user
# naming the place its run opens as; with one live there, nothing written and the run's place named. The design agent's
# run lands a record: crew role land writes a launch of Flume's chore kind in a blueprints repository on main for
# mac-studio's runner, the brief file's text whole and madswan/design its recipient, which crew trace lists; a repository
# crew does not name, and a land outside a run, are refused requesting nothing. crew board reads each run beside the
# plan, its turn and the asks that wait for it, and names the design agent's run for attention once the runner shows it
# lost. Once mac-studio's runner carries the place of a unit's launch whose status gives two ends Flume owes
# madswan/planner (tests/py/flume-deliveries/), the planner's next run, a tell pending, takes them with the tell and
# prints them, and its end appends, in the commit that ends the turn, one confirm naming the launch, madswan/planner and
# both delivery keys, for the runner to carry to Flume.
# What a tell decides, the ask's fields, what a start takes and prints, what an open reads of the runner and what a land
# writes or refuses, and what a run's view and the attention line say, are logic cases (tests/py/test_tell_asks.py,
# test_asks.py, test_board.py); each step here checks a command's wiring once.
# Reads: plugin/flume/ plugin/roles/ plugin/lib/board.py tests/py/flume-deliveries/
. "${TESTS:?run crew tests through tests/run, which puts stub herdr, ssh and claude first}/lib.sh" || exit 2
world
blueprints afterthought/blueprints >/dev/null; blueprints agentplot/blueprints >/dev/null
crew state init madswan >/dev/null
role_stream madswan planner madswan-main; role_stream madswan operator madswan-main
ms=$(remote afterthought/crew-state)
at() { git --git-dir "$ms" show "madswan/main:$1"; }
asks() { at asks.rec | recsel -t Ask "$@"; }

# A tell to the planner, which runs as its kind with no standing agent up: an ask, nothing typed.
: > "$CREW_TEST_LOG"
t0=$(act_tip madswan/main "$ms")
CREW_AGENT=madswan-design expect_ok crew tell madswan-planner "Record 0053 is accepted ZQXR"
has "$out" "asked madswan-planner"
eq "$(asks -p Role,From,What,Words | tr '\n' ' ')" "Role: planner From: madswan-design What: tell Words: Record 0053 is accepted ZQXR "
eq "$(at roles.rec | recsel -t Role -P Address,Stream,Kind,Name,Intent | tr '\n' ' ')" "madswan/planner madswan-main crew-planner madswan madswan-planner "
eq "$(acts_since "$t0" madswan/main "$ms")" "1"
grep -q "agent prompt" "$CREW_TEST_LOG" && fail "a tell to a role that runs as its kind typed into a pane"
expect_ok crew trace agent/madswan-planner --label madswan
has "$out" "agent/madswan-planner (28 characters)"
[[ $(git --git-dir "$ms" log -p madswan/main -- runs/) != *ZQXR* ]] || fail "an ask's words are in the run record"
ok "a tell to a role that runs as its kind is an ask from its sender with its role record in one commit, typing nothing, and its entry holds no words"

# A send to madswan: an ask of its operator, which runs as its kind, carrying whom it was for.
CREW_AGENT=swancloud-planner expect_ok crew send madswan "The zone check fails"
has "$out" "asked madswan-operator"
eq "$(asks -e "Role = 'operator'" -p From,What,Words | tr '\n' ' ')" "From: swancloud-planner What: send Words: (sent to madswan) The zone check fails "
ok "a send to a partition whose operator runs as its kind is an ask of the operator carrying whom it was for"

# wldn's planner stands: a tell to it, not up, is refused as today, and nothing is asked.
blueprints WilldanGroup/willdan-blueprints >/dev/null; crew state init wldn >/dev/null
CREW_AGENT=madswan-design expect_fail "could not tell wldn-planner on chuck-herdr-alpha: it is not up" crew tell wldn-planner "hello"
git --git-dir "$(remote WilldanGroup/crew-state)" show wldn/main:asks.rec >/dev/null 2>&1 && fail "a tell to a role that stands wrote an ask"
ok "a tell to a role that stands is today's, and asks nothing"

# madswan's planner's run, in its place: its start takes both tells of it and the card the user answered in its name.
run() { FLUME_PLACE=$T/flume/places/crew-planner--madswan "$@"; }
CREW_AGENT=madswan-design expect_ok crew tell madswan-planner "Batch 4 is due"
stub=$(home_of mac-studio)/.stub-pendingyou; mkdir -p "$stub/answered"
echo '{"req_stub-90": {"key": "zone-question-1", "posted": {"name": "madswan-planner", "title": "Which zone?"}, "status": "pending", "turn": "you", "version": 1}}' > "$stub/cards.json"
echo '{"answer": {"text": "eu-west-1"}}' > "$stub/answered/req_stub-90.json"
: > "$CREW_TEST_LOG"
t0=$(act_tip madswan/main "$ms")
run expect_ok crew role start
brief=$(home_of mac-studio)/.local/state/crew/madswan/turns/planner.md
has "$out" "Read $brief whole first: it is your brief as madswan-planner, filled for madswan."
has "$out" "ask 1: tell from madswan-design"$'\n'"  Record 0053 is accepted ZQXR"$'\n'"ask 3: tell from madswan-design"$'\n'"  Batch 4 is due"
has "$out" "card card/req_stub-90/2: Which zone?"$'\n'"  words: eu-west-1"
has "$(cat "$brief")" "You run as your kind"; lacks "$(cat "$brief")" "{{"
grep -q '^mac-studio pendingyou list_pending {"name": "madswan-planner"}$' "$CREW_TEST_LOG" || fail "the start did not read its cards as madswan-planner"
eq "$(at asks.rec | recsel -t Turn -p Turn,Run,Place,Took | tr '\n' ' ')" "Turn: 1 Run: madswan-planner Place: crew-planner--madswan Took: ask/1 Took: ask/3 "
eq "$(acts_since "$t0" madswan/main "$ms")" "1"
expect_ok crew trace agent/madswan-planner --label madswan
has "$out" "(took 2)"
ok "a role's run, named from its place, takes what waits in one turn, writes and prints its brief, its asks and the card the user answered in its name"

# An ask after the start waits for the next run; the end, as the turn's prompt names it, answers the turn and writes the report.
CREW_AGENT=madswan-design expect_ok crew tell madswan-planner "One more thing"
end=$(grep -o 'crew role end --report {{report}}' "$CREW/plugin/flume/turn.md" | head -1)
report=$T/flume/state/crew-planner--madswan/turn.md
read -ra endcmd <<< "${end//\{\{report\}\}/$report}"
run expect_ok "${endcmd[@]}" "proposed the fix bolt"
has "$out" "turn 1 of madswan-planner is ended, and its report is $report."
eq "$(at asks.rec | recsel -t Turn -P Said)" "proposed the fix bolt"
has "$(cat "$report")" "# Turn 1 of madswan-planner"; has "$(cat "$report")" "- ask/3: tell from madswan-design"
eq "$(at asks.rec | recsel -C -t Ask -e "Role = 'planner'" -P Id | tr '\n' ' ')" "1 3 4 "
lacks "$(at asks.rec | recsel -t Turn -P Took)" "ask/4"
ok "an ask written during a run is not its turn's, and the end answers the turn and writes the report at the prompt's path"

# Outside a run, the start and the end are refused and write nothing.
t0=$(git --git-dir "$ms" rev-parse madswan/main)
CREW_AGENT=madswan-planner expect_fail "crew role start runs only in a run of a crew role" crew role start
expect_fail "crew role end runs only in a run of a crew role" crew role end --report "$T/elsewhere.md" "done"
eq "$(git --git-dir "$ms" rev-parse madswan/main)" "$t0"; [[ -e $T/elsewhere.md ]] && fail "an end outside a run wrote a report"
ok "a start and an end outside a role's run are refused and write nothing"

# The user opens madswan's design agent, which runs as its kind, while mac-studio's runner shows no run of it: an open
# ask from the user, naming the place its run opens as. The runner's branch is its own, written here as a runner would.
role_stream madswan design madswan-main
runner_commit() {  # runner_commit <message> [<places.rec>]: mac-studio's runner's branch on madswan's state, with the files given
  local tree runner_rec
  runner_rec=$(printf '%%rec: Runner\n%%key: Host\n%%type: Since date\n%%mandatory: Host Version Since\n%%allowed: Host Version Since\n\nHost: mac-studio\nVersion: 0.1.0\nSince: 2026-10-31T11:00:00Z\n')
  tree=$( { printf '100644 blob %s\trunner.rec\n' "$(printf '%s\n' "$runner_rec" | git --git-dir "$ms" hash-object -w --stdin)"
            [[ -z ${2:-} ]] || printf '100644 blob %s\tplaces.rec\n' "$(printf '%s\n' "$2" | git --git-dir "$ms" hash-object -w --stdin)"; } |
          git --git-dir "$ms" mktree)
  git --git-dir "$ms" update-ref refs/heads/madswan/runner/mac-studio "$(git --git-dir "$ms" -c user.name=runner -c user.email=runner@example.com \
    commit-tree "$tree" $(git --git-dir "$ms" rev-parse -q --verify refs/heads/madswan/runner/mac-studio | sed 's/^/-p /') -m "$1")"
}
runner_commit "runner: serve madswan on mac-studio"
t0=$(act_tip madswan/main "$ms")
expect_ok crew role open design --label madswan
has "$out" "asked madswan-design to open: its run opens as the place crew-design--madswan in herdr on mac-studio once the runner there makes it"
eq "$(asks -e "What = 'open'" -p Role,What | tr '\n' ' ')" "Role: design What: open "
[[ $(asks -e "What = 'open'" -P From) == *@mac-studio ]] || fail "the open ask is not from the user at mac-studio"
eq "$(at roles.rec | recsel -t Role -e "Role = 'design'" -P Address)" "madswan/design"
eq "$(acts_since "$t0" madswan/main "$ms")" "1"
ok "the user opening a role that runs as its kind, with no run of it live, is an open ask naming the place its run opens as"

# Once the runner's places.rec shows the design agent's run live, opening it writes nothing and names its place.
live='{"status":{"places":[{"place":"/flume/places/crew-design--madswan","phase":"live","current":"turn","waiting_on":null,"stalled":false}],"host":{}}}'
runner_commit "runner: madswan/design's run" "$(printf '%%rec: Place\n%%key: Request\n%%type: Request int\n%%type: At date\n%%mandatory: Request Place At Status\n%%allowed: Request Place At Status\n\n%%rec: Run\n%%key: Address\n%%type: At date\n%%mandatory: Address At\n%%allowed: Address Place At Status Words\n\nAddress: madswan/design\nPlace: /flume/places/crew-design--madswan\nAt: 2026-10-31T12:10:00Z\nStatus: %s\n' "$live")"
t0=$(git --git-dir "$ms" rev-parse madswan/main)
expect_ok crew role open design --label madswan
has "$out" "madswan-design's run is live on mac-studio, the place /flume/places/crew-design--madswan: talk to it there now, as crew-design--madswan in herdr; nothing is written"
eq "$(git --git-dir "$ms" rev-parse madswan/main)" "$t0"
ok "opening a role whose run the runner shows live writes nothing and names the run's place"

# madswan's design agent's run lands a record: a launch of Flume's chore kind in a blueprints repository on its default
# branch, for mac-studio's runner, the brief file's text whole and the run's address its recipient, in a commit of its own.
printf 'Write docs/adr/0053-roles-run-as-kinds.md with this text whole:\n# 53. Roles run as kinds\n' > "$T/record-0053.md"
design() { FLUME_PLACE=$T/flume/places/crew-design--madswan "$@"; }
t0=$(act_tip madswan/main "$ms")
design expect_ok crew role land afterthought/blueprints record-0053 --brief-file "$T/record-0053.md"
has "$out" "the runner on mac-studio launches chore record-0053 in afterthought/blueprints on main (request 1) in stream madswan-main"
landed() { at requests.rec | recsel -t Request -e "Work = 'role/design/record-0053'" "$@"; }
eq "$(landed -P Act,Host,Repo,Kind,Name,Base,Stream,Priority,Intent,Recipient,By | tr '\n' ' ')" \
   "launch mac-studio afterthought/blueprints chore record-0053 main madswan-main 0 madswan-design madswan/design madswan-design "
eq "$(landed -P Brief)" "$(cat "$T/record-0053.md")"
eq "$(acts_since "$t0" madswan/main "$ms")" "1"
expect_ok crew trace role/design/record-0053 --label madswan
has "$out" "role.land"
ok "a role's run lands its work as a chore launch on the repository's main, its brief whole and its address the recipient"

# A repository crew does not name, and a land outside a role's run, are refused and request nothing; the first, in the
# run, records its refusal.
before=$(at requests.rec)
design expect_fail "crew names no repository afterthought/crew" crew role land afterthought/crew record-0054 --brief-file "$T/record-0053.md"
CREW_AGENT=madswan-design expect_fail "crew role land runs only in a run of a crew role" \
  crew role land afterthought/blueprints record-0054 --brief-file "$T/record-0053.md"
eq "$(at requests.rec)" "$before"
expect_ok crew trace role/design/record-0054 --label madswan
has "$out" "crew names no repository afterthought/crew"
ok "a land in a repository crew does not name, or outside a role's run, is refused and requests nothing"

# crew board reads the roles that run as their kinds beside madswan's plan: each run has its turn and the asks that wait
# for it from asks.rec, and once mac-studio's runner shows the design agent's run lost the attention line names it, its
# place and host, and no command.
expect_ok crew board --label madswan --json
eq "$(jq -c '.partitions[0].runs | map([.run, .stream, (.turn.turn // "none"), .waiting])' <<<"$out")" \
   '[["madswan-design","madswan-main","none",1],["madswan-planner","madswan-main","1",1],["madswan-operator","madswan-main","none",1]]'
eq "$(jq -c '[.partitions[0].attention[] | select(.what == "run")]' <<<"$out")" "[]"
lost='{"status":{"places":[{"place":"/flume/places/crew-design--madswan","phase":"live","current":"turn","waiting_on":{"act":"retry","stage":"turn","why":"lost","since":1793440000,"words":null},"stalled":false}],"host":{}}}'
runner_commit "runner: madswan/design's run lost" "$(printf '%%rec: Place\n%%key: Request\n%%type: Request int\n%%type: At date\n%%mandatory: Request Place At Status\n%%allowed: Request Place At Status\n\n%%rec: Run\n%%key: Address\n%%type: At date\n%%mandatory: Address At\n%%allowed: Address Place At Status Words\n\nAddress: madswan/design\nPlace: /flume/places/crew-design--madswan\nAt: 2026-10-31T12:20:00Z\nStatus: %s\n' "$lost")"
expect_ok crew board --label madswan
has "$out" "! madswan's design run: lost, its place /flume/places/crew-design--madswan on mac-studio"
[[ $out != *"flume retry"* ]] || fail "the board printed a command for a lost run"
ok "crew board reads each role's run beside the plan, its turn and the asks that wait from asks.rec, and names a run the runner shows lost"

# A unit's launch on madswan's branch, a hand edit as crew bolt start would write it, and mac-studio's runner carrying
# its place at the status tests/py/flume-deliveries/ holds, its ends owed to madswan/planner: the construct's second
# start delivered, expired, and its code ended short, waiting on the planner's answer. The planner's next run, the tell
# written during its last turn pending, takes the tell, the place that waits on it and both ends, and prints the ends
# after the waits; its end asks the runners to confirm both in the commit that ends the turn.
w=$T/madswan-state; git clone -q -b madswan/main "$ms" "$w"
printf '\nRequest: 2\nAct: launch\nWork: unit/a\nRepo: afterthought/crew\nKind: change\nName: a\nBase: bolt/b\nPriority: 1\nIntent: madswan/b\nRecipient: madswan/planner\nBrief: Build a.\nDate: 2026-11-08T10:00:00Z\nBy: madswan-planner\n' >> "$w/requests.rec"
commit_all "$w" "requests: a unit's launch by hand"; git -C "$w" push -q origin madswan/main
owed=$(jq -c . "$CREW/tests/py/flume-deliveries/owed.json" | sed 's#agentplot/planner#madswan/planner#g')
runner_commit "runner: unit a's place" "$(printf '%%rec: Place\n%%key: Request\n%%type: Request int\n%%type: At date\n%%mandatory: Request Place At Status\n%%allowed: Request Place At Status\n\nRequest: 2\nPlace: /flume/places/change--a\nAt: 2026-11-08T10:05:00Z\nStatus: %s\n' "$owed")"
keys="change--the-flake-configures-each-tool-by-its-own-module/3f9a61c2/stage/construct/2/delivered change--the-flake-configures-each-tool-by-its-own-module/3f9a61c2/stage/code/1/ended-short"
run expect_ok crew role start
has "$out" "unit/a waits on you: the place /flume/places/change--a, launched by request 2 (place/2@1794085696)"
has "$out" $'Flume holds these ends for you, each confirmed to it as you when your turn ends (crew role end):\nunit/a (the place /flume/places/change--a, request 2): stage/construct/2/delivered (expired), stage/code/1/ended-short\n'
eq "$(at asks.rec | recsel -t Turn -e "Turn = 2" -P Took | tr '\n' ' ')" "ask/4 place/2@1794085696 $(for k in $keys; do printf 'end/2/%s ' "$k"; done)"
t0=$(act_tip madswan/main "$ms")
run expect_ok "${endcmd[@]}" "answered unit a's stop-short"
has "$out" "The 2 ends it took are confirmed to Flume as madswan/planner once the runners carry request 3."
eq "$(at requests.rec | recsel -t Request -e "Act = 'confirm'" -P Request,Work,Of,Recipient | tr '\n' ' ')" "3 unit/a 2 madswan/planner "
eq "$(at requests.rec | recsel -t Request -e "Act = 'confirm'" -P Delivery | tr '\n' ' ')" "$keys "
eq "$(acts_since "$t0" madswan/main "$ms")" "1"
eq "$(git --git-dir "$ms" diff --name-only "$t0" "$(act_tip madswan/main "$ms")" | grep -v '^runs/')" $'asks.rec\nrequests.rec'
has "$(cat "$report")" "- 2 ends of request 2, their confirmation asked of the runners"
ok "a role's run takes the ends Flume owes its address with what waits, prints them, and its end asks one confirm of the launch's keys in the commit that ends its turn"
