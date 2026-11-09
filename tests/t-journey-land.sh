# A bolt lands through the runner, through the crew command on the stubs (tests.11, record 0022;
# crew-lands-each-bolt-through-flumes-base-place, Decisions 3 to 7): crew bolt start appends the bolt's base place's
# launch, of crew's kind on main, and then its chore's, making no branch and reaching no host; the runner on the box
# launches the base place, which has the bolt's branch made, and the chore's place, which Flume lands on the bolt; the
# bolt reads proven and the raise of its kit's landings card on the main level's host posts its row; the user's send of
# it makes the next raise post one land of the bolt's launch, in ops's name, recorded asked with its request, and a raise
# after it posts none; the runner carries the land and Flume's status of the base place submitted, then landed at a
# commit, and the next raise records the landing, closes the bolt at that commit and closes the card naming it, putting
# away the preview its row carried. Before the send, ops's crew card preview, on the user's words on the card, writes
# one preview request for the runner on the box, where the bolt's work runs, and the card, changed in place, says it is
# asked; once the runner reports it, the rail's read changes the card listing its address, and ops's --done writes its
# done (a-cards-preview-is-asked-of-the-runner). Two
# bolts proven together are one card of two boxes; the user ticks both and the raise posts their lands in the card's
# order; Flume refuses the first for a conflict with main and the second for a failed check: the raise records both,
# launches the first's take-main fix once however often it reads it, and holds the second's row in Flume's words; once
# the take-main fix lands on its bolt, which reads proven at its new head with its own work unchanged, the next raise
# posts a second land of it on the standing send; Flume lands it on main, GitHub deletes its branch and the runner
# carries no place of its work, so its report never reads it landed, and ops's crew bolt land closes it at the landing
# its kit's main holds, its chore read landed through that landing (bolt-teams "A bolt whose landing main holds closes
# whatever the runner carried of its places"). Through it all, no sluice, wt or gh call is made, and the kit's
# checkout on the box keeps its HEAD, index and refs but its remotes' (Decision 1). Every decision on the way is a logic
# case (tests/py/test_runner.py, test_landings.py, test_landing.py).
# Reads: plugin/lib/board.py plugin/roles/
. "${TESTS:?run crew tests through tests/run, which puts stub herdr, ssh and claude first}/lib.sh" || exit 2
bolt_world
box=chuck-herdr-alpha
export CREW_LABEL=wldn
flume_world
on_box() { HOST=$box crew "$@"; }
# field <host> <act> <field> [object]: a field of that host's last entry of the act naming the object (tests/journeys.sh)
field() {
  as "$1" python3 -c 'import glob, json, os, sys; sys.path.insert(0, sys.argv[1]); import record
es = [e for f in sorted(glob.glob(os.path.expanduser("~/.local/state/crew/wldn/runs/*/*.rec"))) for e in record.parse(open(f).read())
      if e["Act"] == sys.argv[2] and (len(sys.argv) < 4 or sys.argv[3] in e["On"])]
print(json.dumps(es[-1] if es else {}))' "$CREW/plugin/lib" "$2" ${4:+"$4"} | jq -r --arg f "$3" 'if (.[$f] | type) == "array" then .[$f] | join(" ") else .[$f] // "" end'
}
r=$(remote WilldanGroup/switchboard-kit)
fl=$T/flume-clone; git clone -q "$r" "$fl"
# kit_state: the kit's checkout on the box as crew must leave it: its HEAD, its index and every ref but its remotes'
kit_state() {
  { git -C "$k" symbolic-ref -q HEAD || true; git -C "$k" rev-parse HEAD; shasum "$(git -C "$k" rev-parse --absolute-git-dir)/index" | cut -d' ' -f1
    git -C "$k" for-each-ref --format='%(refname) %(objectname)' | grep -v '^refs/remotes/' || true; } | tr '\n' ' '
}
before=$(kit_state)
: > "$CREW_TEST_LOG"
live=$BASE_LIVE
# flume_builds <chore> <bolt> <file>: what Flume does with a launched chore once it has built, done in a clone of its
# own so the kit's checkout is crew's alone: its commit, carrying its trailer, landed on the bolt on GitHub as sluice
# lands a place, a merge naming its place's branch (Sluice-From); then the fleet's timer fetches the kit on the box,
# and the runner carries the chore's place landed at the bolt's new head
flume_builds() {
  git -C "$fl" fetch -q origin; git -C "$fl" checkout -q --detach "origin/bolt/$2"
  echo "$1" > "$fl/$3"; git -C "$fl" add "$3"; git -C "$fl" commit -qm "chore($1): $1" -m "Chore: $1"
  local c; c=$(git -C "$fl" rev-parse HEAD); git -C "$fl" checkout -q --detach "origin/bolt/$2"
  git -C "$fl" merge -q --no-ff -m "chore(land): chore/$1" -m "Sluice-From: chore/$1 (chore/$1)" "$c"
  git -C "$fl" push -q origin "HEAD:refs/heads/bolt/$2"
  git -C "$k" fetch -q origin
  runner_writes $box "$(request_of "chore/$1")" "/flume/places/chore--$1" "$(landed_status "/flume/places/chore--$1" "$(git -C "$fl" rev-parse HEAD)")"
}
# base_launched <bolt>: the runner launches the bolt's base place, which has sluice make bolt/<bolt> from main on GitHub
base_launched() {
  git -C "$fl" fetch -q origin; git -C "$fl" push -q origin "origin/main:refs/heads/bolt/$1"
  git -C "$k" fetch -q origin
  runner_writes $box "$(request_of "bolt/$1")" "/flume/places/bolt--$1" "$(base_status "/flume/places/bolt--$1" '"live"' "$live")"
}
# flume_lands_bolt <bolt> <request of its land>: Flume submits the bolt's branch and the merge queue lands it on main as
# a merge commit; the runner carries the land and the base place landed at that commit, whose sha it prints
flume_lands_bolt() {
  git -C "$fl" fetch -q origin; git -C "$fl" checkout -q --detach origin/main
  git -C "$fl" merge -q --no-ff -m "chore(land): bolt/$1" "origin/bolt/$1"; git -C "$fl" push -q origin HEAD:refs/heads/main
  git -C "$k" fetch -q origin
  local c; c=$(git -C "$fl" rev-parse HEAD)
  runner_writes $box "$2" - '{}' "$(request_of "bolt/$1")" "/flume/places/bolt--$1" \
    "$(base_status "/flume/places/bolt--$1" '{"over":{"over":{"landed":{"commit":"'"$c"'"}},"kept":null}}' \
       '{"read":{"found":{"submission":{"id":"412","branch":"bolt/'"$1"'","target":"main","state":{"landed":{"commit":"'"$c"'"}}}}},"submits":1,"send_backs":0,"verdict":{"landed":{"commit":"'"$c"'","place_removed":false,"branch_removed":false}},"waiting":null,"held":false}')"
  echo "$c"
}
requests() { git --git-dir "$ws" show wldn/main:requests.rec | recsel -t Request -P "$1" | grep . | paste -sd ' ' -; }
req() { git --git-dir "$ws" show wldn/main:requests.rec | recsel -t Request "$@"; }
land_of() { git --git-dir "$ws" show wldn/main:requests.rec | recsel -t Request -e "Act = 'land' && Work = 'bolt/$1'" -P Request | tail -1; }

# A start launches the base place and then the chore, making no branch and reaching no host
expect_ok crew bolt new y "Y's files." --repo switchboard-kit
expect_ok crew chore add y-files "Y's files." --bolt y
: > "$T/start.log"; CREW_TEST_LOG=$T/start.log expect_ok crew bolt start y
has "$out" "y's base place, bolt/y, is asked of the runner (request 1)"
eq "$(requests Work)" "bolt/y chore/y-files"
eq "$(git --git-dir "$ws" show wldn/main:requests.rec | recsel -t Request -e "Request = 1" -P Kind,Base,Recipient | paste -sd ' ' -)" "crew/bolt main wldn/ops"
git --git-dir "$r" rev-parse -q --verify refs/heads/bolt/y >/dev/null && fail "the start made bolt/y"
[[ ! -s $T/start.log ]] || fail "the start reached a host or ran a tool: $(cat "$T/start.log")"
ok "crew bolt start appends the bolt's base place's launch, of crew's kind on main, then its chore's, making no branch and reaching no host"

# The runner launches both; Flume lands the chore on the bolt, which reads proven; the raise posts its row
base_launched y
flume_builds y-files y y.txt
expect_ok on_box _land-card wldn switchboard-kit
card=$(grep -o "^card land/switchboard-kit: req_stub-[0-9]*" <<<"$out" | cut -d' ' -f3)
[[ -n $card ]] || fail "no landings card was raised for y:"$'\n'"$out"
has "$(calls | grep "^$box pendingyou post_request " | tail -1)" "Land the bolt y on switchboard-kit's main"
ok "the bolt reads proven once its chore lands on it as the runner reports, and its kit's landings card carries it"

# The user writes on the card asking to try it running: ops's crew card preview writes one preview request on
# wldn/main's requests.rec, naming the box, whose runner took the bolt's work, the bolt, its kit, its branch and its
# head, and the card, changed in place, says it is asked of the runner on the box; once the runner reports it, sluice's
# listing of it starting at one address, the rail's read on the partition's main machine changes the card listing the
# address; the user is done with it and ops's --done writes its done; asked again, it stands at the send.
ops() { (export CREW_AGENT=wldn-ops; HOST=$box crew "$@"); }
kit_repo=$(git --git-dir "$ws" show wldn/main:plan.rec | recsel -t Bolt -e "Bolt = 'y'" -P Repo)
h=$(git -C "$k" rev-parse origin/bolt/y)
out=$(ops card preview land/switchboard-kit y 2>&1) || fail "ops could not ask for the preview:"$'\n'"$out"
asked=$(req -e "Act = 'preview'" -P Request | tail -1)
[[ -n $asked ]] || fail "no preview request was written:"$'\n'"$out"
eq "$(req -e "Request = $asked" -p Host,Work,Repo,Branch,Revision,Done)" \
  "$(printf 'Host: %s\nWork: bolt/y\nRepo: %s\nBranch: bolt/y\nRevision: %s' "$box" "$kit_repo" "$h")"
has "$out" "request $asked: y: Its preview of ${h:0:7} is asked of the runner on $box"
has "$(calls | grep "^$box pendingyou update_request " | tail -1)" "\"changeNote\": \"y: Its preview of ${h:0:7} is asked of the runner on $box\""
st=$(jq -nc --arg r "$h" '{name: "preview-y", branch: "bolt/y", revision: $r, state: "starting", made: "2026-10-31T12:05:00Z", addresses: {web: "http://web-y"}}')
runner_previews $box "$asked" done "$st" "$st" yes
expect_ok on_box rail --label wldn
changed=$(calls | grep "^$box pendingyou update_request " | tail -1)
has "$changed" "\"changeNote\": \"y: Its preview of ${h:0:7} is coming up\""
has "$changed" "web: http://web-y"
out=$(ops card preview land/switchboard-kit y --done 2>&1) || fail "ops could not put the preview away:"$'\n'"$out"
done_=$(req -e "Act = 'preview'" -P Request | tail -1)
eq "$(req -e "Request = $done_" -p Work,Revision,Done)" "$(printf 'Work: bolt/y\nRevision: %s\nDone: yes' "$h")"
has "$out" "request $done_: y: Its preview of ${h:0:7} is put away"
out=$(ops card preview land/switchboard-kit y 2>&1) || fail "ops could not ask for the preview again:"$'\n'"$out"
again=$(req -e "Act = 'preview'" -P Request | tail -1)
(( again > done_ )) || fail "the preview was not asked again:"$'\n'"$out"
ok "ops's crew card preview writes one preview request for the runner on the box, where the bolt's work runs, the card changed in place saying it is asked and, once the runner reports it, listing its address, and its --done writes its done"

# The user's send: the next raise posts one land of y's launch, recorded asked, and the raise after it none
mkdir -p "$(home_of $box)/.stub-pendingyou/answered"
echo '{"answer": {"approved": true}}' > "$(home_of $box)/.stub-pendingyou/answered/$card.json"
head=$(git -C "$k" rev-parse origin/bolt/y)
expect_ok on_box _land-card wldn switchboard-kit
ly=$(land_of y)
has "$out" "card land/switchboard-kit: y is asked of the runner to land at ${head:0:7} (request $ly), on the user's send"
eq "$(req -e "Request = $ly" -P Act,Work,Of | paste -sd ' ' -)" "land bolt/y 1"
eq "$(field $box bolt.submit Outcome bolt/y) $(field $box bolt.submit Request bolt/y) $(field $box bolt.submit By bolt/y)" "asked $ly wldn-ops"
n=$(requests Request | wc -w | tr -d ' ')
expect_ok on_box _land-card wldn switchboard-kit
eq "$(requests Request | wc -w | tr -d ' ')" "$n"
has "$out" "card land/switchboard-kit: $card is left as it is, the user having answered it"
ok "the user's send makes the raise post one land of the bolt's launch in ops's name, recorded asked with its request, and a second raise posts none"

# Flume lands the bolt on main; the next raise records the landing, closes the bolt at that commit and the card
landed=$(flume_lands_bolt y "$ly")
: > "$T/ack"
expect_ok on_box _land-card wldn switchboard-kit
eq "$(field $box bolt.submit Outcome bolt/y)" "landed"
eq "$(field $box bolt.land Head bolt/y)" "$landed"
eq "$(field $box bolt.land By bolt/y)" "wldn-ops"
plan() { git --git-dir "$ws" show wldn/main:plan.rec > "$T/plan.rec"; recsel -C "$@" "$T/plan.rec"; }
[[ -z $(plan -t Bolt -e "Bolt = 'y'" -P Bolt) ]] || fail "y is still in the plan"
has "$(calls | grep "^$box pendingyou ack_answer " | tail -1)" "Landed on GitHub's main: y at ${landed:0:7}"
has "$out" "card land/switchboard-kit: put away y's preview of ${h:0:7} on $box"
eq "$(req -e "Act = 'preview' && Revision = '$h' && Done = 'yes'" -c)" "2"
ok "once the runner reports the base place landed, the raise records the landing, closes the bolt at Flume's commit in ops's name and closes the card naming it, putting its preview away"

# Two bolts proven together, both ticked: the lands posted in the card's order
for b in z w; do
  expect_ok crew bolt new $b "$b's files." --repo switchboard-kit
  expect_ok crew chore add $b-files "$b's files." --bolt $b
  expect_ok crew bolt start $b
  base_launched $b
  flume_builds $b-files $b $b.txt
done
expect_ok on_box _land-card wldn switchboard-kit
card=$(grep -o "^card land/switchboard-kit: req_stub-[0-9]*" <<<"$out" | tail -1 | cut -d' ' -f3)
[[ -n $card ]] || fail "no landings card was raised for z and w:"$'\n'"$out"
has "$(calls | grep "^$box pendingyou post_request " | tail -1)" '"label": "2. w"'
echo '{"answer": {"choiceIds": ["land:z", "land:w"]}}' > "$(home_of $box)/.stub-pendingyou/answered/$card.json"
expect_ok on_box _land-card wldn switchboard-kit
lz=$(land_of z); lw=$(land_of w)
[[ -n $lz && -n $lw && $lz -lt $lw ]] || fail "z's and w's lands were not posted in the card's order: $(requests Act)"
ok "a send ticking two bolts posts their lands in the card's order"

# Main moves under them, by another kit's work, and Flume refuses z for a conflict with main and w for a failed check
git -C "$fl" fetch -q origin; git -C "$fl" checkout -q --detach origin/main
echo other > "$fl/other.txt"; git -C "$fl" add other.txt; git -C "$fl" commit -qm "feat: other work"
git -C "$fl" push -q origin HEAD:refs/heads/main
main=$(git -C "$fl" rev-parse HEAD)
refused() {  # refused <bolt> <land> <verdict JSON> <entry state JSON> <words>
  runner_writes $box "$2" - '{}' "$(request_of "bolt/$1")" "/flume/places/bolt--$1" \
    "$(base_status "/flume/places/bolt--$1" '"live"' \
       '{"read":{"found":{"submission":{"id":"5'"$2"'","branch":"bolt/'"$1"'","target":"main","state":'"$4"'}}},"submits":1,"send_backs":0,"verdict":'"$3"',"waiting":"'"$5"'","held":false}' \
       '{"act":"retry","stage":null,"why":"submission","since":1794172800,"words":"'"$5"'"}')"
}
conflict="bolt/z conflicts with main at ${main:0:7} on z.txt"
refused z "$lz" '{"conflict":{"files":["z.txt"],"words":"'"$conflict"'"}}' '{"conflict":{"files":["z.txt"],"base":"'"$main"'","words":"'"$conflict"'"}}' "the submission conflicted with its base: $conflict"
failed="check-full failed: tests:logic 1 failed"
refused w "$lw" '{"failed":{"words":"'"$failed"'"}}' '{"failed":{"words":"'"$failed"'"}}' "the submission failed: $failed"
expect_ok on_box _land-card wldn switchboard-kit
eq "$(field $box bolt.submit Refused bolt/z)" "landing refused in conflict with main at ${main:0:7}: $conflict"
eq "$(field $box bolt.submit Refused bolt/w)" "landing refused, a check failed: $failed"
take="fix/z/take-main-${main:0:7}"
eq "$(git --git-dir "$ws" show wldn/main:requests.rec | recsel -t Request -e "Act = 'launch' && Work = '$take'" -c)" "1"
expect_ok on_box _land-card wldn switchboard-kit
eq "$(git --git-dir "$ws" show wldn/main:requests.rec | recsel -t Request -e "Act = 'launch' && Work = '$take'" -c)" "1"
expect_ok crew rail --label wldn
has "$out" "w, on $box, in Flume stream wldn: landing refused at $(git -C "$k" rev-parse --short=7 origin/bolt/w), a check failed, the bolt's, open for work: $failed; it waits for a fix on the bolt, which ops starts with Flume's words, crew fix w <name> \"$failed\""
has "$out" "z, on $box, in Flume stream wldn: takes main first: its landing at $(git -C "$k" rev-parse --short=7 origin/bolt/z) was refused in conflict with main at ${main:0:7}: $conflict; crew launches the fix that takes main into it"
ok "Flume's refusals are recorded in its words: the conflicting bolt's take-main fix is launched once however often it is read, and the failed one's row is held"

# The take-main fix lands on z, which reads proven at its new head with its own work unchanged: a second land on the send
git -C "$fl" fetch -q origin; git -C "$fl" checkout -q --detach origin/bolt/z
git -C "$fl" merge -q --no-ff -m "fix(z): take main in" origin/main; git -C "$fl" push -q origin HEAD:refs/heads/bolt/z
git -C "$k" fetch -q origin
runner_writes $box "$(request_of "$take")" /flume/places/fix--z--take-main "$(landed_status /flume/places/fix--z--take-main "$(git -C "$fl" rev-parse HEAD)")"
expect_ok on_box _land-card wldn switchboard-kit
lz2=$(land_of z)
[[ -n $lz2 && $lz2 -gt $lz ]] || fail "no second land of z was posted on the standing send:"$'\n'"$out"
has "$out" "card land/switchboard-kit: z is asked of the runner to land at $(git -C "$fl" rev-parse --short=7 HEAD) (request $lz2), on the user's send"
ok "once the take-main fix lands on the bolt, which reads proven at its new head, the next raise posts a second land of it on the standing send"

# Flume lands z on main through the merge queue, its landing naming bolt/z, GitHub deletes the branch, and Flume tidies
# the box's places of z's work, so the runner carries none and its report never reads z landed: ops's crew bolt land
# reads the landing main holds, z's chore read landed through it, and closes z at it.
git -C "$fl" fetch -q origin; git -C "$fl" checkout -q --detach origin/main
git -C "$fl" merge -q --no-ff -m "chore(land): #9 bolt/z" -m "Sluice-From: wldn-ops (bolt/z)" origin/bolt/z
git -C "$fl" push -q origin HEAD:refs/heads/main; git -C "$fl" push -q origin :refs/heads/bolt/z
zl=$(git -C "$fl" rev-parse HEAD)
git -C "$k" fetch -q --prune origin
runner_tidies $box $(req -e "Act = 'launch' && (Work = 'bolt/z' || Base = 'bolt/z')" -P Request)
out=$(export CREW_AGENT=wldn-ops; on_box bolt land z 2>&1) || fail "ops's crew bolt land z failed:"$'\n'"$out"
has "$out" "z has landed at switchboard-kit's ${zl:0:7}, as its kit's main holds it"
eq "$(field $box bolt.land Head bolt/z) $(field $box bolt.land By bolt/z)" "$zl wldn-ops"
eq "$(field $box bolt.submit Outcome bolt/z)" "asked"  # no outcome of the runner's is recorded for it
[[ -z $(plan -t Bolt -e "Bolt = 'z'" -P Bolt) ]] || fail "z is still in the plan"
[[ -z $(plan -t Unit -e "Bolt = 'z'" -P Unit) ]] || fail "z's chore is still in the plan"
ok "a bolt Flume landed, its branch deleted from GitHub and its places no longer carried by the runner, is closed by ops's crew bolt land at the landing its kit's main holds"

# Nothing of crew's ran sluice, wt or gh, nor moved the kit's checkout but its remotes
# each stub logs its call as `<host> <tool> <args>`, wherever it runs, a command run over ssh among them
ran=$(grep -E '^[^ ]+ (sluice|wt|gh) ' "$CREW_TEST_LOG" || true)
[[ -z $ran ]] || fail "crew ran a tool for the bolts:"$'\n'"$ran"
eq "$(kit_state)" "$before"
ok "a bolt's run from its start to its close makes no sluice, wt or gh call, and leaves the kit's checkout's HEAD, index and refs but its remotes as they were"
