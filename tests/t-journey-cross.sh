# A team's work through Flume, through the crew command on the stubs (record 0050 parts 2 and 3; the change
# teams-cross-to-flume-as-their-bolts-land; Decisions 1 and 10 of the-team-machinery-leaves): crew runs no team's
# conductor, ops or slot, so crew up is no command, answered with crew's usage, with no host reached and no pane opened. crew bolt start of a
# bolt is refused while no runner answers for the drive, the plan unchanged and no branch made; once a runner
# answers, sluice makes the bolt's branch, the plan marks the bolt Path: flume, naming no team, and requests.rec on the
# state branch holds a launch of each of its units and chores in its repository, naming no host or stream, for the
# runner whose configuration names it to take (the user's ruling of 2026-11-01), and no agent starts; a second start of it is refused. Once the runner's record shows a's place stopped short asking, crew
# answer a appends the retry of that stage with the answer's words, and crew fix of the bolt appends a launch of a fix
# on it. Two bolts more of the kit are started beside it (Decision 14 of the-team-machinery-leaves). Once a is dropped
# and Flume keeps change/a in the kit's repository on the box, an add of a again is refused, read there over ssh, and
# a fresh name is added. The launches, what an answer retries, a fix's launch and drop, where a branch is read and the
# refusals' words are logic cases (tests/py/test_cross.py, tests/py/test_fix.py, tests/py/test_branch_stands.py).
# Reads: plugin/hooks/ plugin/roles/ tests/journeys.sh
. "${TESTS:?run crew tests through tests/run, which puts stub herdr, ssh and claude first}/lib.sh" || exit 2
. "$TESTS/journeys.sh"

crew bolt new next "What comes next." --repo switchboard-kit >/dev/null

: > "$CREW_TEST_LOG"
expect_fail "crew bolts" crew up swb-1
grep -q "ssh $box " "$CREW_TEST_LOG" && fail "crew up of a team went to its host"
[[ -e $(home_of $box)/.stub-herdr/wldn-1.json ]] && fail "crew up of a team opened a pane"
ok "crew up is no command: crew answers it with its usage, reaching no host and opening no pane"

crew unit add a "Build a." --bolt next >/dev/null
crew unit add b "Build b on a." --bolt next --after a >/dev/null
crew chore add c "Bump c." --bolt next >/dev/null
plan_at=$(act_tip)
expect_fail "no runner answers for wldn: its state repository holds no wldn/runner/<host>, so nothing would take the bolt's work" \
  crew bolt start next
eq "$(act_tip)" "$plan_at"
git --git-dir "$r" rev-parse --verify -q bolt/next >/dev/null && fail "a start with no runner on the host made bolt/next on GitHub"
ok "a start is refused while no runner answers for the drive, the plan unchanged and no branch made"

# The runner on swb-1's host serves wldn: its own branch on the state repository, which crew reads and never writes.
runner_rec=$(printf '%%rec: Runner\n%%key: Host\n%%type: Since date\n%%mandatory: Host Version Since\n%%allowed: Host Version Since\n\nHost: %s\nVersion: 0.1.0\nSince: 2026-10-31T11:00:00Z\n' "$box")
blob=$(printf '%s\n' "$runner_rec" | git --git-dir "$ws" hash-object -w --stdin)
tree=$(printf '100644 blob %s\trunner.rec\n' "$blob" | git --git-dir "$ws" mktree)
git --git-dir "$ws" update-ref "refs/heads/wldn/runner/$box" \
  "$(git --git-dir "$ws" -c user.name=runner -c user.email=runner@example.com commit-tree "$tree" -m "runner: serve wldn on $box")"
: > "$CREW_TEST_CLAUDE_LOG"
expect_ok crew bolt start next
has "$out" "next is started: sluice made bolt/next on GitHub (origin) from switchboard-kit's main at"
has "$out" "no agent starts: unit/a (request 1), unit/b (request 2), chore/c (request 3) is launched in switchboard-kit, for a runner whose configuration names it to take, in the stream its host maps it to"
git --git-dir "$r" rev-parse --verify -q bolt/next >/dev/null || fail "the start made no bolt/next on GitHub"
eq "$(git --git-dir "$ws" show wldn/main:plan.rec | recsel -t Bolt -e "Bolt = 'next'" -P Team,Path | tr '\n' ' ')" "flume "
eq "$(git --git-dir "$ws" show wldn/main:requests.rec | recsel -t Request -P Act,Work,Repo,Kind,Base,Host,Stream,After | grep . | paste -sd ' ' -)" \
  "launch unit/a switchboard-kit change bolt/next launch unit/b switchboard-kit change bolt/next 1 launch chore/c switchboard-kit chore bolt/next"
eq "$(launches)" ""
eq "$(field "$HOST" bolt.start On bolt/next)" "bolt/next"
plan_at=$(act_tip)
expect_fail "bolt next is started already" crew bolt start next
eq "$(act_tip)" "$plan_at"
ok "a start makes its bolt's branch, marks it Path: flume with no team and launches each unit and chore, b after a, starting no agent, and a second start is refused"

# The runner launched a, and Flume's status of its place, carried on the runner's branch, shows its code stopped short
# asking: the branch gains answers.rec and places.rec beside runner.rec.
answers_rec=$(printf '%%rec: Answer\n%%key: Request\n%%type: Request int\n%%type: Outcome enum held launched done refused\n%%type: At date\n%%mandatory: Request Outcome At\n%%allowed: Request Outcome Place Words At\n\nRequest: 1\nOutcome: launched\nPlace: /flume/places/change--a\nAt: 2026-10-31T12:01:00Z\n')
status='{"status":{"places":[{"place":"/flume/places/change--a","phase":"live","current":"code","stages":[{"name":"code","state":"ended_short","end":{"needs":"needs_answer","words":"Which drive'"'"'s rail?"}}],"waiting_on":{"act":"retry","stage":"code","why":"answer","words":"Which drive'"'"'s rail?"},"stalled":false}]}}'
places_rec=$(printf '%%rec: Place\n%%key: Request\n%%type: Request int\n%%type: At date\n%%mandatory: Request Place At Status\n%%allowed: Request Place At Status\n\nRequest: 1\nPlace: /flume/places/change--a\nAt: 2026-10-31T12:02:00Z\nStatus: %s\n' "$status")
tree=$(for f in runner answers places; do
  v=${f}_rec; printf '100644 blob %s\t%s.rec\n' "$(printf '%s\n' "${!v}" | git --git-dir "$ws" hash-object -w --stdin)" "$f"
done | git --git-dir "$ws" mktree)
git --git-dir "$ws" update-ref "refs/heads/wldn/runner/$box" "$(git --git-dir "$ws" -c user.name=runner -c user.email=runner@example.com \
  commit-tree "$tree" -p "refs/heads/wldn/runner/$box" -m "runner: a's place stopped short")"
expect_ok crew answer a "wldn's"
has "$out" "unit/a's place /flume/places/change--a is asked to run code again with the answer (request 4): the runner on $box retries it"
eq "$(git --git-dir "$ws" show wldn/main:requests.rec | recsel -t Request -e "Request = 4" -P Act,Work,Of,Stage,Words | grep . | paste -sd ' ' -)" \
  "retry unit/a 1 code wldn's"
eq "$(field "$HOST" stage.answer On)" "unit/a bolt/next"
ok "crew answer of a place the runner shows stopped short asking appends the retry of its stage with the answer's words"

: > "$CREW_TEST_CLAUDE_LOG"
expect_ok crew fix next tidy "Tidy the rail's words."
has "$out" "fix next--tidy is launched on bolt/next in switchboard-kit (request 5) for a runner whose configuration names it to take"
eq "$(git --git-dir "$ws" show wldn/main:requests.rec | recsel -t Request -e "Request = 5" -P Act,Work,Kind,Name,Base,Brief | grep . | paste -sd ' ' -)" \
  "launch fix/next/tidy fix next--tidy bolt/next Tidy the rail's words."
eq "$(field "$HOST" fix.start On)" "fix/next/tidy bolt/next"
eq "$(launches)" ""
ok "crew fix of a started bolt appends a launch of a fix on it, starting no agent"

# next is started, none of its work merged, and two bolts more of its kit are started beside it: a start waits on no
# other bolt, neither for its proof nor for how many are started.
crew bolt new more "More of it." --repo switchboard-kit >/dev/null
crew bolt new last "The last of it." --repo switchboard-kit >/dev/null
: > "$CREW_TEST_CLAUDE_LOG"
expect_ok crew bolt start more
has "$out" "no agent starts: nothing, the bolt holding no unit or chore yet is launched in switchboard-kit"
expect_ok crew bolt start last
eq "$(git --git-dir "$ws" show wldn/main:plan.rec | recsel -t Bolt -e "Path = 'flume'" -P Bolt | grep . | paste -sd ' ' -)" "next more last"
eq "$(launches)" ""
ok "bolts of a kit whose started bolt's work has not merged are started beside it all the same, starting no agent"

# a is dropped, its place had work, and Flume keeps change/a in the kit's repository on the box while it holds it: the
# runner's record now names that repository, where Flume cuts the kit's places, in its repositories.rec, the one report
# crew reads a kit's folder from (Decision 1 of a-bolts-landing-on-main-reads-landed). An add under a again is refused before
# anything is written, read in that repository over the host's ssh, and the same work under a fresh name is added and
# launched (bolt-plan "A name whose Flume branch stands is refused when it is planned").
expect_ok crew unit drop a "Replaced by a-again."
has "$out" "Flume keeps change/a while it holds work bolt/next lacks, and the name a stays taken while that branch stands"
has "$(field "$HOST" unit.drop Note unit/a)" "Flume keeps change/a while it holds work bolt/next lacks"
kept=$(git -C "$k" commit-tree "$(git -C "$k" rev-parse 'HEAD^{tree}')" -p HEAD -m "feat: a's work, kept by Flume")
git -C "$k" branch change/a "$kept"
nb=$(git --git-dir "$ws" show wldn/main:requests.rec | recsel -t Request -e "Act = 'launch' && Work = 'unit/b'" -P Request | grep . | tail -1)
status_b='{"status":{"places":[{"place":"/flume/places/change--b","repository":"'"$k"'","phase":"live","current":"code","stages":[{"name":"code","state":"started"}],"stalled":false}]}}'
places_rec=$(printf '%s\n\nRequest: %s\nPlace: /flume/places/change--b\nAt: 2026-10-31T12:05:00Z\nStatus: %s\n' "$places_rec" "$nb" "$status_b")
answers_rec=$(printf '%s\n\nRequest: %s\nOutcome: launched\nPlace: /flume/places/change--b\nAt: 2026-10-31T12:04:00Z\n' "$answers_rec" "$nb")
repositories_rec=$(printf '%%rec: Repository\n%%key: Repository\n%%mandatory: Repository Folder\n%%allowed: Repository Folder\n\nRepository: WilldanGroup/switchboard-kit\nFolder: %s\n' "$k")
tree=$(for f in runner answers places repositories; do
  v=${f}_rec; printf '100644 blob %s\t%s.rec\n' "$(printf '%s\n' "${!v}" | git --git-dir "$ws" hash-object -w --stdin)" "$f"
done | git --git-dir "$ws" mktree)
git --git-dir "$ws" update-ref "refs/heads/wldn/runner/$box" "$(git --git-dir "$ws" -c user.name=runner -c user.email=runner@example.com \
  commit-tree "$tree" -p "refs/heads/wldn/runner/$box" -m "runner: b's place in the kit's repository")"
plan_at=$(act_tip)
: > "$CREW_TEST_LOG"
expect_fail "unit a can't be planned in switchboard-kit: Flume's branch change/a stands in $k on $box, at ${kept:0:7}" \
  crew unit add a "Build a again." --bolt next
has "$out" "propose the unit under a fresh name, or have the planner or the user remove the branch first"
eq "$(act_tip)" "$plan_at"
grep -q "^' crew $k refs/heads/change/a\$" "$CREW_TEST_LOG" || fail "the add did not read change/a in the kit's repository on $box"
git -C "$k" rev-parse -q --verify change/a >/dev/null || fail "crew removed Flume's branch change/a"
expect_ok crew unit add a-again "Build a again." --bolt next
eq "$(git --git-dir "$ws" show wldn/main:requests.rec | recsel -t Request -e "Work = 'unit/a-again'" -P Act,Kind,Name | grep . | paste -sd ' ' -)" \
  "launch change a-again"
ok "a unit dropped with its branch kept is refused when added again under its name, naming the branch and the ways on, and a fresh name is added"
