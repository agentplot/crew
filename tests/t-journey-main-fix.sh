# A fix of a red main through the crew command on the stubs (Decision 11 of teams-cross-to-flume-as-their-bolts-land;
# the main-level spec's "A red main's fix is a fix place on main on the kit's host", state.3): with wldn's plan naming
# switchboard-kit and a runner answering on the box, crew main fix appends to requests.rec on the state branch a launch
# of Flume's fix kind on main in the kit's repository, its submission held and main-level ops its recipient, and starts
# no agent; once its code has delivered, its row on the kit's landings card is sent by the user, and the card's next
# raise appends one land of its launch, a second appending none, while crew main fix --send refuses at once
# (crew-lands-each-bolt-through-flumes-base-place, Decision 5). The refusals where no runner answers, the drop and the
# role table are logic cases (tests/py/test_main_fix.py).
# Reads: plugin/roles/ tests/journeys.sh
. "${TESTS:?run crew tests through tests/run, which puts stub herdr, ssh and claude first}/lib.sh" || exit 2
. "$TESTS/journeys.sh"

# runner_writes <file>...: wldn/runner/$box on the state repository as the runner on the box writes it, and crew
# never does, holding each file named from its text in <file>_rec.
runner_writes() {
  local tree parent
  tree=$(for f in "$@"; do
    v=${f}_rec; printf '100644 blob %s\t%s.rec\n' "$(printf '%s\n' "${!v}" | git --git-dir "$ws" hash-object -w --stdin)" "$f"
  done | git --git-dir "$ws" mktree)
  parent=$(git --git-dir "$ws" rev-parse -q --verify "refs/heads/wldn/runner/$box") || parent=
  git --git-dir "$ws" update-ref "refs/heads/wldn/runner/$box" "$(git --git-dir "$ws" -c user.name=runner -c user.email=runner@example.com \
    commit-tree "$tree" ${parent:+-p "$parent"} -m "runner: $*")"
}
runner_rec=$(printf '%%rec: Runner\n%%key: Host\n%%type: Since date\n%%mandatory: Host Version Since\n%%allowed: Host Version Since\n\nHost: %s\nVersion: 0.1.0\nSince: 2026-10-31T11:00:00Z\n' "$box")
runner_writes runner

# wldn's plan names switchboard-kit by a bolt planned on it, so the kit is one of wldn's (plan.partition_kits).
expect_ok crew bolt new smoke-follow-up "Smoke's follow-up." --repo switchboard-kit

: > "$CREW_TEST_CLAUDE_LOG"
words="tests:logic failed on main after landing smoke: tests/py/test_rail.py reads a fixture that is gone."
expect_ok crew main fix switchboard-kit a-test-reads-its-fixture "$words"
has "$out" "fix main--a-test-reads-its-fixture is launched on switchboard-kit's main in switchboard-kit (request 1) for a runner whose configuration names it to take, its submission held"
eq "$(git --git-dir "$ws" show wldn/main:requests.rec | recsel -t Request -P Act,Host,Work,Repo,Kind,Name,Base,Stream,Intent,Recipient,Hold,Brief | grep . | paste -sd ' ' -)" \
  "launch fix/main/switchboard-kit/a-test-reads-its-fixture switchboard-kit fix main--a-test-reads-its-fixture main wldn/main/switchboard-kit wldn/ops submission $words"
eq "$(field "$HOST" fix.start On)" "fix/main/switchboard-kit/a-test-reads-its-fixture"
eq "$(launches)" ""
ok "crew main fix of a kit appends a launch of a fix on main in its repository, held for the user's send with ops its recipient, naming no host or stream, starting no agent"

# The runner launched the fix, and Flume's status of its place, carried on the runner's branch, shows its code
# delivered and its submission held: the branch gains answers.rec and places.rec beside runner.rec.
place=/flume/places/fix--main--a-test-reads-its-fixture
answers_rec=$(printf '%%rec: Answer\n%%key: Request\n%%type: Request int\n%%type: Outcome enum held launched done refused\n%%type: At date\n%%mandatory: Request Outcome At\n%%allowed: Request Outcome Place Words At\n\nRequest: 1\nOutcome: launched\nPlace: %s\nAt: 2026-10-31T12:01:00Z\n' "$place")
head=bf67379258f5c2165f8c8ee7454753332cab33f3
status='{"status":{"places":[{"place":"'"$place"'","kind":"fix","phase":"live","head":"'"$head"'","current":"code","stages":[{"name":"code","state":"delivered"}],"submission":{"read":"none","submits":0,"send_backs":0,"verdict":null,"waiting":null,"held":true},"waiting_on":{"act":"retry","stage":null,"why":"on_hold","since":1793469348,"words":null},"stalled":true,"holds":[{"on":"submission","since":1793469048}]}]}}'
places_rec=$(printf '%%rec: Place\n%%key: Request\n%%type: Request int\n%%type: At date\n%%mandatory: Request Place At Status\n%%allowed: Request Place At Status\n\nRequest: 1\nPlace: %s\nAt: 2026-10-31T12:20:00Z\nStatus: %s\n' "$place" "$status")
runner_writes runner answers places
expect_ok crew rail --label wldn
has "$out" "switchboard-kit (wldn): 1 fix of main waits to land on its main; each lands on your send of land/switchboard-kit"
has "$out" "fix main--a-test-reads-its-fixture on $box: tests:logic failed on main after landing smoke: tests/py/test_rail.py reads a fixture that is gone.; can land on your send of land/switchboard-kit"
lacks "$out" "crew tell wldn-ops"
lacks "$out" "crew main fix switchboard-kit a-test-reads-its-fixture --send"
ok "once the runner's record shows the fix's code delivered and its submission held, the kit's landings row carries it, landing on the user's send and naming no command"

# crew main fix --send lands nothing: refused at once, with or without the user's words, nothing appended
for more in "" "--excerpt Land-it."; do
  expect_fail "crew main fix --send lands nothing: fix a-test-reads-its-fixture of switchboard-kit's main lands on the user's send of its row, main--a-test-reads-its-fixture, on switchboard-kit's landings card, land/switchboard-kit, which crew carries to the runner as a land" \
    crew main fix switchboard-kit a-test-reads-its-fixture --send $more
done
eq "$(git --git-dir "$ws" show wldn/main:requests.rec | recsel -t Request -c)" "1"
ok "crew main fix --send refuses at once, naming the card's send, and appends nothing"

# The kit's landings card carries the fix's row; the user sends it, and the card's next raise appends one land of the
# fix's launch, in ops's name, and a second raise appends none.
: > "$CREW_TEST_LOG"
HOST=$box expect_ok crew _land-card wldn switchboard-kit
card=$(grep -o "^card land/switchboard-kit: req_stub-[0-9]*" <<<"$out" | cut -d' ' -f3)
[[ -n $card ]] || fail "no landings card was raised for the fix of main:"$'\n'"$out"
has "$(calls | grep "^$box pendingyou post_request " | tail -1)" "Land the fix main--a-test-reads-its-fixture on switchboard-kit's main"
mkdir -p "$(home_of $box)/.stub-pendingyou/answered"
echo '{"answer": {"approved": true}}' > "$(home_of $box)/.stub-pendingyou/answered/$card.json"
HOST=$box expect_ok crew _land-card wldn switchboard-kit
has "$out" "card land/switchboard-kit: main--a-test-reads-its-fixture is asked of the runner to land at ${head:0:7} (request 2), on the user's send"
eq "$(git --git-dir "$ws" show wldn/main:requests.rec | recsel -t Request -e "Request = 2" -P Act,Host,Work,Of | grep . | paste -sd ' ' -)" \
  "land fix/main/switchboard-kit/a-test-reads-its-fixture 1"
eq "$(field $box fix.merge Request fix/main/switchboard-kit/a-test-reads-its-fixture)" "2"
eq "$(field $box fix.merge Outcome fix/main/switchboard-kit/a-test-reads-its-fixture)" "asked"
HOST=$box expect_ok crew _land-card wldn switchboard-kit
eq "$(git --git-dir "$ws" show wldn/main:requests.rec | recsel -t Request -c)" "2"
expect_ok crew rail --label wldn
has "$out" "fix main--a-test-reads-its-fixture on $box: tests:logic failed on main after landing smoke: tests/py/test_rail.py reads a fixture that is gone.; sent on the user's word (request 2): the runner on $box submits it"
ok "the user's send of the fix's row on its kit's landings card appends one land of its launch, recorded asked with its request, a second raise appending none, and its row says it is sent"
