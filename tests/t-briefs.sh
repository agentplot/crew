# Every brief prints for its drive's main level with no token left unfilled, and none for a team or a dispatcher,
# which the teams file names none of (Decision 2 of the-team-machinery-leaves).
# Reads: plugin/roles/
. "${TESTS:?run crew tests through tests/run, which puts stub herdr, ssh and claude first}/lib.sh" || exit 2
world
# wldn's plan names three kits, which its main level's host, the box, keeps (Decision 3 of the-team-machinery-leaves).
blueprints WilldanGroup/willdan-blueprints >/dev/null; crew state init wldn >/dev/null
for k in atlas breadboard switchboard; do crew bolt new "$k-work" "Work in $k-kit." --repo "$k-kit" --label wldn >/dev/null; done
for role in conductor ops construct coder verify dispatcher fable; do
  expect_fail "no definition '$role' for a main level. definitions: design planner main-ops operator reviewer" crewpy brief wldn $role
done
expect_fail "no drive 'swb-1'. drives: wldn madswan swancloud" crewpy brief swb-1 planner
for gone in fable explorer verifier conductor ops dispatcher construct coder verify; do
  [[ ! -e $CREW/plugin/roles/$gone.md ]] || fail "the retired role $gone is still there"
done
ok "no brief prints for a team, a dispatcher or a retired role"

# sluice's verdict can outlast an agent's ten-minute call (teams.5's details; sluice ADR 0041), so every brief that
# submits by hand submits without waiting and waits a call at a time with sluice wait, never reading a listing; and
# the wait runs from the harness's background, so a submission never holds the agent's session (teams.5, as amended
# 2026-10-23), in the foreground only where the harness runs nothing in the background.
for brief in "wldn design" "wldn operator"; do
  expect_ok crewpy brief $brief
  for want in "sluice wait <n> --timeout 9m --json" "for as long as it exits 5, still waiting" "--no-wait --json" \
    "submit again to move" "listing, which a decided submission leaves" \
    "wait on it from your harness's background, a call at a time" "as a background command" \
    "so the submission never holds your session and a tell or the user's message reaches you meanwhile" \
    "where your harness runs nothing in the background, run it in the foreground instead"; do
    has "$out" "$want"
  done
  lacks "$out" "wait on it a call at a time, giving the command its full ten minutes"
done
ok "the design agent and the operator submit without waiting and wait on the submission with sluice wait from the background, never a listing"

# No brief has an agent run `wt submit`, whose --help removes the worktree it ran in with sluice 0.3.1 (teams.5's
# details): main-level ops runs no landing (main-level "Main-level ops runs no landing"; Decision 11 of
# crew-lands-each-bolt-through-flumes-base-place), and CLAUDE.md says never to run it where every agent reads.
named=()
for brief in "wldn design" "wldn planner" "wldn main-ops" "wldn operator" "wldn reviewer"; do
  expect_ok crewpy brief $brief
  [[ $out == *"wt submit"* ]] && named+=("${brief#* }")
done
[[ -z ${named[*]} ]] || fail "the briefs naming wt submit are ${named[*]}"
ok "no brief names wt submit"

# The question discipline each of the three that ask carries (record 0031, briefs.11; Decision 6 of
# the-team-machinery-leaves): who asks and after whom, a Flume place's question answered with crew answer, Pending
# You's test for what is the user's, a question's fields and its key of its own, how its answer is heard, and every
# row's card as crew's.
asks_say() {
  for want in "A question of yours for the user reaches them on a Pending You card you ask yourself; every other card on the rail is crew's." \
    "Three ask the user: the planner, main-level ops and the design agent." \
    "A Flume place that stops short asks the one of you it names, who gets the answer and gives it to the place with \`$CREW/plugin/bin/crew answer\`" \
    "the operator and the reviewer ask nothing; and crew refuses a card from any other agent" \
    "\`$CREW/plugin/bin/crew tell\`: \`wldn-design\` for the design, \`wldn-ops\` for a live system, a deploy or a landing, \`wldn-planner\` for the plan" \
    "in their name, their money, their plans, public or hard to undo" "when its choices lead to noticeably different products" \
    "decide what a careful product designer would, and say so" "its options, with the one you recommend" \
    "\`blocking\` false and the fallback you take meanwhile" "what you tried, in its \`tried\`" \
    "\`ask/<your crew name>/<what it is about>\`, a key of your own" "Pending You gives that card back" \
    "a new card under a new key, following the one answered" \
    "\`proposal/\`, \`batch/\`, \`land/\`, \`deploy/\`, \`op/\` or \`record/\`, is crew's" "refuses your post, change or close of one" \
    "call \`whoami\` with your crew name" "\`create-area:<owner>/<kit>\`: crew refuses an area under any other key" \
    "Never run \`npx pendingyou\` or \`pendingyou hold\`" "close your question's card with \`ack_answer\` and a one-line outcome" \
    "ask it again if it still matters, under the same key, saying in it that an older copy is dead" "leave every other card alone"; do
    has "$out" "$want"
  done
  for gone in "rail row's of your own" "the form its row takes" "plan card" "begins with the link to the card's plannotator session" \
    "No card carries a path" "kind \`image\`" "An older copy of this card is dead" "posted again by nobody" \
    "Four ask the user" "crew needs" "stop short to their" \
    "The one exception is a lost card" "card session <key>" "answeredHere" "Never open a browser for a card"; do
    lacks "$out" "$gone"
  done
}
for role in design planner main-ops operator reviewer; do
  expect_ok crewpy brief wldn $role
  [[ $out =~ \{\{[A-Z_]+\}\} ]] && fail "roles/$role.md left ${BASH_REMATCH[0]} unfilled"
  has "$out" "of wldn"; lacks "$out" "fable"
  echo "$role: $(wc -c <<<"$out" | tr -d ' ') characters"
done
# Each role's session is named with the account the drive's `accounts` gives the role (record 0064), read from the
# teams file alone: wldn's every role in wldn-3 on credits; with its planner and reviewer on ia in wldn-1, those two
# there on ia.
for r in design planner ops operator reviewer; do has "$out" "\`wldn-$r\` in session wldn-3 (account credits)"; done
edit teams "$(part wldn)['roles'] = {'planner': {'session': 'wldn-1'}}; $(part wldn)['accounts'].update(planner='ia', reviewer='ia')"
expect_ok crewpy brief wldn design
has "$out" "\`wldn-design\` in session wldn-3 (account credits); \`wldn-planner\` in session wldn-1 (account ia); \`wldn-ops\` in session wldn-3 (account credits); \`wldn-operator\` in session wldn-3 (account credits); \`wldn-reviewer\` in session wldn-1 (account ia)"
fixtures
ok "a brief names each role's session with the account the drive's accounts gives it"
expect_ok crewpy brief wldn design
for want in attach challenge new-territory answered drop "unit add" "tell wldn-planner" "tell <agent>" "## Answering a design question" \
  "a design question the planner, \`wldn-ops\` or a Flume place brings" \
  "answer <work> \"<the answer, with the pages or commits it rests on>\"\`, \`<work>\` the unit's or chore's name or the fix's place"; do
  has "$out" "$want"
done
for want in "names, in the message that carries it, the documentation page or the reading it rests on" "Read the thing itself" \
  "not the sequence" "Answer linked questions together" "never the mechanism"; do has "$out" "$want"; done
has "$out" "\`--source\` also names what the signal points at"
expect_ok crewpy brief wldn planner
for want in "only agent that proposes bolts" "--signal" "plan propose <file>" "--replaces <n>" "--unblocks <bolt>" \
  "bolt start <bolt>" "It waits on the user alone, and no agent is told of it" "A started bolt is in flight" "only when the user says so" "wldn/main" "is refused while a unit of the bolt has a worktree, since a queued unit has none" \
  "A dropped bolt's own branch sluice deletes, on GitHub and the host, or keeps and crew names as the drop's unmerged work, the user's, while main lacks its tip"; do
  has "$out" "$want"
done
for gone in "bin/crew bolt new" "bin/crew unit add" "bin/crew unit move" "bin/crew unit drop" "Agree any change to it" "plan agree" \
  "bolt give" "it no longer waits on that conductor"; do lacks "$out" "$gone"; done
has "$out" "and with \`--source\` what the signal points at"
for want in "| rename a repository once its work is finished | \`kit rename <old> <new>\` |" \
  "**A repository renamed on its forge** is removed and added back, its work finished first" \
  "crew refuses it while any of the repository's work stands or a host still keeps the old name, naming what stands" \
  "A drive is never renamed"; do has "$out" "$want"; done
for want in 'unit amend <unit> "<new intent>"' "never a drop and a new unit" "why the unit changes rather than being replaced" \
  "A unit that has merged is not amended"; do has "$out" "$want"; done
for want in "An intent names the outcome and the records that govern it" "never the mechanism" \
  "Corrections to a unit under construction are batched" "blocks the bolt"; do has "$out" "$want"; done
for want in "Never name a proposal by its number alone" "Recite no command" "which holds the change whole" \
  "say in a sentence what you propose and point to its card"; do has "$out" "$want"; done
lacks "$out" "plannotator-tui"
for want in "crew card session" "crew card read" \
  "crew raises a proposal's card itself, in your name, when \`$CREW/plugin/bin/crew plan propose\` accepts the proposal" \
  "changes it when you rewrite the proposal with \`--replaces\`, in place while it waits on the user and as a new version following the one they answered" \
  "a card whose rows fill more than one list withdrawn and followed by its new version instead" "closes it with what was applied when the proposal is approved" \
  "You post, change and close no proposal card." \
  "call get_request (requestId req_…, name wldn-planner)" "crew raises its card in your name" \
  "The card asks only the units and chores the proposal makes new to a bolt or the queue" \
  "is drawn on its face and applies with it" "A lone new unit is the choice of its two sides" \
  "is a hold-to-approve, which the user declines with a note to keep something it drops or amends" \
  "so each new unit's \`Do\` carries its direction" "crew plan answer <n> <question> <box>... --label wldn" \
  "\`rows-<k>\` and the ids of the boxes the user left ticked" "--note \"<the user's note>\"" \
  "applies the change with the boxes as they stand, a new unit unticked left out, closes the card with what was applied" \
  "you close no proposal card" \
  "add \`--clear <unit>\` for each of them" "An approval applies the commands the user read and kept" \
  "when a command they kept names a unit they left out"; do has "$out" "$want"; done
for want in "A batch's card carries, under each unit, what its stages recorded as made, as the run wrote it" \
  "reply in the card's thread first, as Pending You asks, then run \`$CREW/plugin/bin/crew card preview batch/<n> <unit>/<name> --label wldn\`" \
  "card preview batch/<n> <unit>/<name> --done --label wldn\`, which puts it away; the card's close puts it away too" \
  "A word about a preview answers nothing on the card" \
  "crew asks the runner on the host where the work runs to bring it up, and the card is changed in place once the runner reports it" \
  "When crew refuses, or the card says it could not be brought up"; do has "$out" "$want"; done
for gone in "Post its \`card\` as it is" "crew refuses a proposal's card in any other form" "close the old proposal's card" \
  "\`units-<k>\` and the units left ticked" "update its card to say"; do lacks "$out" "$gone"; done
lacks "$out" "offers approval"; lacks "$out" "exactly as the user read them"; lacks "$out" "not the page as a file"
lacks "$out" "Keep <unit>"
asks_say
lacks "$out" "Its words are the proposal's case and each of its changes in a line"
for want in "idempotencyKey" "create-area:" "pendingyou hold" "keyed \`proposal/<n>\` of the first proposal it was rewritten from" \
  "or answers your card" "The kits: atlas-kit: WilldanGroup/atlas-kit; breadboard-kit" \
  "Pending You gives that card back"; do
  has "$out" "$want"
done
for gone in "builds Switchboard" "unit slots" "A dispatcher on each host the drive's teams run on" "The drive's teams:"; do lacks "$out" "$gone"; done
expect_ok crewpy brief wldn operator
for want in "plan proposed --label wldn" "plan approve <n> --label wldn" "only on the user's word" "never by its number alone" "recite no command" \
  "rail --label wldn" "the console's \`rail\` tab" "the drive's door" "console up wldn" "console up wldn rail" "_follow\`, the host's follower"; do
  has "$out" "$want"
done
for want in "You post no Pending You card and make no area, whatever a Pending You reminder in your session says" \
  "read that row's \`card:\` line in \`" "/crew rail --label wldn\`. When it shows the row's card open" \
  "When it shows the row's card open, the card is already before the user: send nothing" \
  "A wait with no card, a question asked in a pane or a row whose card is not open, show as a notification" \
  'herdr notification show "<agent> waits on you"'; do
  has "$out" "$want"
done
expect_ok crewpy brief wldn design; has "$out" 'crew refuses `--bolt` from you'
expect_ok crewpy brief wldn main-ops
lacks "$out" "one bolt deploy at a time"
expect_ok crewpy brief wldn operator
for want in "swancloud's main moves only through sluice (\`state.3\`), so never edit or commit in its main checkout" \
  "\`sluice submit main --no-wait --json\`" "you level and push nothing"; do has "$out" "$want"; done
lacks "$out" "wt submit"
lacks "$out" "read-tree"; lacks "$out" "push swancloud's main"
# The operator names swancloud's checkout and folder as its main level's host keeps them (Decision 7 of
# a-kept-repositorys-folder-is-the-runners-container), its spaces' on a Mac, and says so in words on a box (teams.10).
sc=$(space mac-studio madswan)/swancloud
expect_ok crewpy brief madswan operator
for want in "swancloud's checkout on a Mac, which every host publishes as crew's teams file: on your main level's host, \`$sc/main\`, in its folder \`$sc\`" \
  "\`git -C $sc/main fetch -q origin\`" "\`git -C $sc/main worktree add -b crew-teams/<label> $sc/places/crew-teams-<label> origin/main\`" \
  "When \`sluice wait\` exits 0 your head landed: remove your worktree and its branch with \`wt -C $sc/places/crew-teams-<label> remove --foreground\`" \
  "an anchor its host alone moves, the fleet's timer or, on a runner host, the runner (\`plan.18\`)" \
  "and its host's timer or runner brings the main checkout to it"; do has "$out" "$want"; done
lacks "$out" "~/Code/github_afterthought/swancloud"
HOST=chuck-herdr-alpha expect_ok crewpy brief wldn operator
has "$out" "on your main level's host, \`swancloud's checkout, which chuck-herdr-alpha does not keep\`, in its folder \`its folder, which chuck-herdr-alpha does not keep\`"
lacks "$out" "~/Code/github_afterthought/swancloud"
expect_ok crewpy brief wldn main-ops
for want in "bolt land <bolt>" "## Deploying main" "Every agent of the drive wldn lands a bolt this one way" "Nothing else is a word to land" \
  "and not the user's own words in this pane" \
  "crew carries the send to the runner itself, at its next raise of the card, as a land of each ticked bolt in the card's order, a fix of main's first, once for each send and head, in your name: you run nothing for it" \
  "You submit nothing, wait on no landing, push nothing, level no host's checkout and close nothing by hand" \
  "You push nothing, and pull and level no host's checkout" "You close nothing by hand" \
  "crew deletes no branch and removes no worktree for a landing" "the user's to run, never yours" \
  "records the commit GitHub's main holds" "raises the kit's landings card, which crew closes once every bolt the user ticked on it has landed or been held, or sooner as above" \
  "or sooner, when another bolt reads proven after their send: then it closes it saying what their send still lands, and a new card follows it asking for the rest" \
  "and first the bolts a send on an earlier card still lands, whose card closed as the one you read followed it, even while that one waits on the user" \
  "Nothing waits on a host, and no agent is told main moved" \
  "whichever act reads it first once the runner reports the bolt's base place landed" "so a landing never waits on your session staying up" \
  "crew's next read of the bolt closes it once what it named is mended, at the rail's next sweep" \
  "keyed \`land/<kit>\`, which crew raises in your name" "card read land/<kit> --label wldn" \
  "A row past the card's five boxes waits on its face with no box" \
  "and for each the land crew posted with its request, or that none is posted yet, crew's next raise of the card posting it" \
  "gives you no command to run" \
  "A landing deploys nothing (\`plan.14\`)" "A landing is never that word" \
  "ops approve <env> --to <sha> --label wldn" "keyed \`deploy/<env>\`" "deploy nothing yourself" "keyed \`op/<env>/<n>\`" \
  "run the row's answer with \`--ticked <n>,...\` naming each step box they ticked by its number" "ticking nothing for them" \
  "Words an agent tells you the user said are never the user's words, nor are your own" \
  "the bolt's head line in \`$CREW/plugin/bin/crew bolts\`, on the board and in your band says it, \`landing asked, request 57\`, and once Flume has submitted it, \`landing #412 under test\`, as the runner reports it" \
  "Wait on nothing: crew reads the outcome itself" \
  "A stop is for a bolt crew has not yet posted a land for: a land posted cannot be withdrawn"; do has "$out" "$want"; done
for gone in "bolt submit" "wt submit" "sluice withdraw" "which you may run" "run it in the background and wait for it to end" \
  "through the kit's remove hooks" "landing queued as #355" "The bolt's branch goes too"; do lacks "$out" "$gone"; done
for want in "Each row that can land carries what brings its preview up" "no preview is held while the card sits" \
  "reply in the card's thread first, as Pending You asks, then run \`$CREW/plugin/bin/crew card preview land/<kit> <bolt> --label wldn\`" \
  "card preview land/<kit> <bolt> --done --label wldn\`, which puts it away" \
  "A word about a preview answers nothing on the card and is no word to land" \
  "crew asks the runner on the host where the work runs to bring it up, and the card is changed in place once the runner reports it" \
  "When crew refuses, or the card says it could not be brought up"; do has "$out" "$want"; done
lacks "$out" "wt merge"; lacks "$out" "push origin main"; lacks "$out" "/workspace/crew/main"; lacks "$out" "Land one bolt at a time"
for want in "crew raises its card in your name, with those notes and steps on its face" "you post, change and close no deploy card" \
  "\`call get_request (requestId <id>, name wldn-ops)\`: run it" "crew closes the card at the deploy's end with its outcome" \
  "card read deploy/<env> --label wldn" "a step an agent can do that is held for the user's word" \
  "one at a time on an environment, each following the one before" "you post and close no step card" \
  "ops quiet <env> --label wldn\` exits 0" "when they pick skip, run the row's \`decline\` command" \
  "ops step <env> --to <sha> --key <key> --doer user --state waiting --text <file> --label wldn\`, the file holding the gate's link alone" \
  "Post no offer for that deploy" "the user's approval at the gate is its word" \
  "Record the step done once the run shows the gate passed, or declined once it was rejected"; do has "$out" "$want"; done
for gone in "Post its card under that key" "and close the card"; do lacks "$out" "$gone"; done
asks_say
has "$out" $'A landing is never that word.\n\n## Asking the user\n\nA question of yours for the user'
expect_fail "no definition 'conductor' for a main level" crewpy brief wldn conductor
ok "every main-level brief prints for wldn with no unfilled token"

# How a main-level role's work reaches it (design Decision 9, role-runs "A run's brief says how a turn goes"), each
# brief saying the word its drive's `runs` names it by and never that it runs as its kind: a standing role, in its
# pane; an on-demand one, a turn from crew role start to crew role end, waiting in its session on nothing, and asking
# the user only on a card in its own name.
for role in design planner reviewer main-ops operator; do
  expect_ok crewpy brief wldn $role
  has "$out" "Your drive's \`runs\` names you \`standing\`: you stand in your pane, an agent crew started and keeps up, and your work reaches you there, as tells marked"
  lacks "$out" "names you \`on-demand\`"; lacks "$out" "as your kind"
done
for r in design planner reviewer ops operator; do role_runs wldn $r on-demand; done
for role in design planner reviewer main-ops operator; do
  expect_ok crewpy brief wldn $role
  [[ $out =~ \{\{[A-Z_]+\}\} ]] && fail "roles/$role.md left ${BASH_REMATCH[0]} unfilled for a drive running all five on-demand"
  for want in "Your drive's \`runs\` names you \`on-demand\`: no agent of you stands" "Your turn starts with \`$CREW/plugin/bin/crew role start\`" \
    "end the turn with \`$CREW/plugin/bin/crew role end\`" "Wait in your session on nothing" \
    "end your turn instead, and the thing reaches your next run as an ask" "Ask the user only on a card in your own name, wldn-"; do
    has "$out" "$want"
  done
  lacks "$out" "names you \`standing\`"; lacks "$out" "as your kind"; lacks "$out" "runs as its kind"
done
expect_ok crewpy brief wldn reviewer; has "$out" "run \`$CREW/plugin/bin/crew review delivered\`, which records it"
expect_ok crewpy brief wldn main-ops; has "$out" "You run nothing for a landing: crew carries the user's send to the runner, and how each landing ends reaches your next run as an ask when it does not land"
expect_ok crewpy brief wldn planner; has "$out" "asks the reviewer a batch where your drive's \`runs\` names it \`on-demand\`, and its delivery reaches you as an ask, with the line that adopts its card"
for r in design planner reviewer ops operator; do role_runs wldn $r standing; done
ok "each main-level brief says the word its drive's runs names it by and how its work reaches it: in its pane while standing, and as a turn that waits on nothing while on-demand, every brief filled for a drive running all five so"

expect_ok crewpy brief wldn operator
has "$out" "the deployer offers that host's deploy under *operations* on swancloud's rail"; has "$out" "never ask \`wldn-ops\` to deploy it"
has "$out" "never hand the user a deploy command"; has "$out" "deploys by hand only a kit with no deployer"
[[ $out =~ \{\{[A-Z_]+\}\} ]] && fail "roles/operator.md left ${BASH_REMATCH[0]} unfilled"
for want in "bolts --label wldn" "bolts <bolt> --label wldn" "sites wldn" "tell <agent>" '`wldn-planner`' '`wldn-design`' '`wldn-ops`' "terminal-browser open <url> --split right"; do has "$out" "$want"; done
for gone in "status <team>" "<team>-conductor" "unit approve"; do lacks "$out" "$gone"; done
for want in "/crew page wldn\`" "open the file it prints in terminal-browser beside your pane" \
  "on a box, give the user the path and say it opens from a Mac" "say as of when the page is, and name any host whose kits it could not read"; do has "$out" "$want"; done
for want in "## A batch answered in your pane" "card answer batch/<n> --excerpt \"<their words, as they wrote them>\"\` at once" \
  "records the batch answered as a tap on its card does, closes its card, and tells \`wldn-planner\` the words" \
  "which the planner acts on as the batch's notes; you hand them to no one else" "Only when crew says it could not tell the planner, carry the user's words to \`wldn-planner\` yourself" \
  "never record an answer from words that are not the user's own"; do has "$out" "$want"; done
HOST=chuck-herdr-alpha expect_ok crewpy brief wldn operator
has "$out" "chuck-herdr-alpha is a box, which can't open the dev.swancloud.net names"; lacks "$out" "terminal-browser open"
ok "the operator brief prints for wldn, recording a batch answered in its pane, opening sites and the lineage page on a Mac and giving the Mac URL or the page's path on a box"
has "$out" "reads crew's run record on the drive's branch, where each entry is pushed as it is written"
lacks "$out" "on every host the drive runs on"
ok "the operator reads the run record on the drive's branch, asking no host for it (read.5)"

# The operator carries what crew send brings it, and sends a teams change from a box to a Mac's drive with crew
# send, never with a tell to another operator (briefs.10).
HOST=chuck-herdr-alpha expect_ok crewpy brief wldn operator
for want in "A message that reaches you marked \`(sent to <drive>)\`" "in the sender's words and naming the sender" \
  "you record as a signal, its excerpt the words as sent" "a landing, a deploy or a live system to \`wldn-ops\`" \
  "Don't answer it in the sender's place" "crew refuses a send of yours to your own drive." "## Changing the drives" \
  "one of \`madswan\`, \`swancloud\`, with \`" "/crew send <label> \"<the request>\"\`, which reaches that drive's operator"; do has "$out" "$want"; done
lacks "$out" "TEAMS_OPERATORS"; lacks "$out" "TEAMS_DOORS"; lacks "$out" "to an operator whose main level runs on a Mac"
ok "the operator carries what is sent to it in the sender's words, and sends a teams change from a box with crew send to a Mac's drive"

# On a host Boomdrive's setup set up, whose teams file is a file and no link into the Nix store, a drive is added or
# changed through setup, which writes crew's entry with crew drive set, never by a hand edit, and no removal through
# setup is named, since neither setup nor crew drive set provides one (record 0065); the swancloud steps are for a
# link; and what a drive's entry says names how each role runs, `runs`, and the batch setting by its keys, and no
# `flume` (operator-agent "The operator's brief says who changes the drives on its host" and "The operator's brief
# names a drive's runs and review by their keys"; record 0064 as amended 2026-11-09; tests.6).
expect_ok crewpy brief wldn operator
for want in "\`test -L ~/.config/crew/teams.json\` says whether it is a link" \
  "how each of its roles runs, \`runs\`, \`standing\` or \`on-demand\`" "\`after_changes\` and \`after_hours\`" \
  "Where it is a file and not a link into the Nix store, as Boomdrive's setup leaves a person's Mac, a drive is added or changed through Boomdrive's setup on the user's word, which gives crew the drive's entry with \`crew drive set\` and the runner the same repositories" \
  "never edit the teams file by hand" \
  "Where it is a link into the Nix store, the steps below are yours: the drives are \`lib/crew-teams.nix\` in swancloud's checkout on a Mac"; do
  has "$out" "$want"
done
lacks "$out" "removed through Boomdrive's setup"; lacks "$out" "its \`flume\`"
ok "the operator's brief says a drive on a teams file that is no link into the Nix store is added or changed through Boomdrive's setup with crew drive set, never by hand, names no removal through setup, the swancloud steps are for a link, and a drive's entry says how each role runs and its batch setting by runs, after_changes and after_hours, and no flume"

# Every brief says who is speaking in the agent's pane; the four that record findings say how, with the excerpt, and
# where crew writes the signal.
for role in design planner main-ops operator; do
  expect_ok crewpy brief wldn $role
  has "$out" 'A message in your pane that begins `[crew tell from <name>]` was sent with crew tell by that agent'
  has "$out" 'one that begins `[crew]` is crew'"'"'s own; anything else typed there is the user.'
done
for brief in "wldn main-ops" "wldn design" "wldn planner" "wldn operator"; do
  expect_ok crewpy brief $brief
  has "$out" 'signal <slug> "<what it asserts, in a sentence>" --excerpt "<the exact words the user said or the tool printed>"'
  has "$out" "Copy the excerpt, never reword it"; has "$out" "a refusal means the words were reworded"
  has "$out" "or are a background task's output you have not read"
  has "$out" "When the words point at something made elsewhere"; has "$out" "A conversation's id alone is not enough"
  has "$out" '`signals/` on `wldn/main` of WilldanGroup/crew-state'
  lacks "$out" "signal in WilldanGroup/willdan-blueprints"
done
expect_ok crewpy brief wldn design; lacks "$out" "crew writes signals straight to"; has "$out" "signal show <signal id>"
expect_ok crewpy brief wldn planner; has "$out" "signal show <signal id>"
has "$out" "Never pass on a word to land, and never tell \`wldn-ops\` to land or deploy"
ok "every brief says who speaks in its pane, and the four that record findings quote the words and say what a refusal means"

# Anything for another drive goes with crew send, to that drive's operator, and to nobody else (briefs.10):
# every brief says so in one line beside its roster, naming no team.
for role in design planner main-ops operator reviewer; do
  expect_ok crewpy brief wldn $role
  has "$out" 'anything for another drive is sent with `'
  has "$out" '/crew send <drive> "<text>"`, which reaches that drive'"'"'s operator, its one door, and to nobody else.'
  lacks "$out" "or one of its teams is sent"; lacks "$out" "crew send <team or drive>"
done
ok "every brief sends anything for another drive with crew send, to that drive's operator and to nobody else"
ok "a signal names where what it points at lives, a unit carries it as a source, and the construct reads it, stops when it can't, and builds from its sources over its intent"

# Every message an agent sends another goes through crew tell, marked: no brief prompts an agent through herdr.
for role in design planner main-ops operator reviewer; do
  expect_ok crewpy brief wldn $role; lacks "$out" "herdr agent prompt"
done
ok "no brief prompts another agent through herdr"

# No main-level brief names the team machinery (Decisions 6 and 7 of the-team-machinery-leaves): each hands what it
# hands to the planner, main-level ops, the design agent or a Flume place, and none to a conductor, a team or a slot.
# The brief's words are read with crew's checkout path left out, which names the place the suite runs in and may hold
# any word.
for role in design planner main-ops operator reviewer; do
  expect_ok crewpy brief wldn $role
  words=${out//"$CREW"/<crew>}
  for gone in conductor dispatcher "team ops" "a team's ops" slot "bolt give" "fix <team>" "/crew unit run" "/crew unit wait" "/crew needs" \
    "status <team>" "its team" "team's" "crossed" "drive a team"; do
    lacks "$words" "$gone"
  done
done
ok "no main-level brief names a conductor, team ops, a dispatcher, a slot, a give, crew fix <team>, crew unit run or wait, crew needs or crew status <team>"

# Every kit's main is an anchor the timer moves, and a host loads crew live or released, never from a checkout on main
# (plan.18, plan.19): no brief pulls, fast-forwards or levels crew's checkout (tests.6).
for brief in "wldn design" "wldn planner" "wldn main-ops" "wldn operator" "wldn reviewer"; do
  expect_ok crewpy brief $brief
  for gone in "/workspace/crew/main" "crew/main/plugin" "merge --ff-only" "read-tree"; do lacks "$out" "$gone"; done
done
ok "no brief pulls, fast-forwards or levels crew's checkout"

# The plan and the moves live on the drive's branch of its state repository: no brief names a plan/<label>
# branch or a moves.rec in the blueprints, and the design agent and the planner name the state repository.
for role in design planner main-ops operator reviewer; do
  expect_ok crewpy brief wldn $role; lacks "$out" "plan/wldn"; lacks "$out" "signals/moves.rec"
done
expect_ok crewpy brief wldn design; has "$out" "\`moves.rec\` on \`wldn/main\` of WilldanGroup/crew-state"
lacks "$out" "route moves straight to"
expect_ok crewpy brief wldn planner; has "$out" "\`wldn/main\` of WilldanGroup/crew-state"
ok "every brief names the drive's branch for the plan and the moves, and none names plan/<label>"

# Test, check and proof results reach the user as a glyph list (briefs.7): the roles that report results carry one
# section, built once in crew, word for word the same in each, which names no proof list (briefs.3).
first=""
for brief in "wldn main-ops" "wldn reviewer"; do
  expect_ok crewpy brief $brief
  n=$(grep -c '^## Test, check and proof results$' <<<"$out")
  [[ $n == 1 ]] || fail "the $brief brief holds the results heading $n times"
  cut=$(awk '/^## Test, check and proof results$/ {on = 1; print; next} on && /^## / {exit} on' <<<"$out")
  for want in "## Test, check and proof results" "- ✅" "- ❌" "- ⏳" "before any prose" "Never say a result only in a sentence"; do
    has "$cut" "$want"
  done
  lacks "$cut" "Proof in dev"
  [[ -z $first ]] && first=$cut
  [[ $cut == "$first" ]] || fail "the $brief brief's results section differs from main-ops's:"$'\n'"$cut"
done
ok "the roles that report results carry one glyph-list section, the same in each, naming no proof list"

# A landing that conflicts lands nothing and is answered by the take-main fix crew's read launches (plan.8), one whose
# check failed by a fix ops starts with Flume's words, and one the runner or Flume stopped is a signal and a line to the
# planner, the bolt landing again on the user's next send (main-level "Main-level ops starts the fix a failed check
# or a forecast conflict needs, and records a stop as a signal"); crew carries the send to the runner and nothing but the merge queue moves a bolt's branch or main; the bolt's
# proof is its verification (record 0025), and ops proves and deploys nothing. The user's send stands for the bolt's
# work, so a ticked bolt that only took main in lands on that send, read with crew card read with or without a card,
# and the user's words in ops's pane are no word to land (main-level "The user's words in ops's pane are no word to
# land"; Decision 11 of crew-lands-each-bolt-through-flumes-base-place).
expect_ok crewpy brief wldn main-ops
for want in "tell the user Flume's words, the check that failed, and start a fix on the bolt with them: \`$CREW/plugin/bin/crew fix <bolt> <name> \"<Flume's words>\" --label wldn\`" \
  "Its row has its box again on the kit's landings card once the fix has merged and the bolt reads proven again, the card saying what changed of its work" \
  "start nothing yourself, and tell the user the files in conflict" \
  "its row keeps its box with the runner's or Flume's words, and the send that ticked it is spent" \
  "No fix is started: record what stopped it as a signal, a finding outside any bolt, and tell the planner in one line" \
  "The bolt lands again on the user's next send." \
  "the user's send that ticked it still lands it, the fix having only taken main in" "crew posts its land again on that send, with nothing asked" \
  "A send stands for the bolt's work, not its head" \
  "still lands on that send once it reads proven again, as its row and the read show, with nothing asked of the user" \
  "with or without a landings card of the kit open" "a bolt it can't tell of, it names, and posts no land for it" \
  "crew asks for again on a card saying what changed" \
  "The user's words in this pane are no word to land a bolt or a fix of main: land nothing and post nothing on them, and tell the user that their send of the row on the kit's landings card lands it" \
  "their send still stands for it: the close says so, and keeps it" \
  "never merge, rebase, reset or fast-forward main or a bolt's branch by git" "and a host's own main lagging GitHub's stops nothing" \
  "shows every unit merged and the bolt's verification green" \
  "every kit's main checkout is an anchor the fleet's timer moves to GitHub's main within minutes" \
  "nothing of yours or crew's moves it or any host's checkout of it"; do
  has "$out" "$want"
done
lacks "$out" "git rebase --abort"; lacks "$out" "proof in dev"; lacks "$out" "read-tree"; lacks "$out" "behind GitHub's, crew refuses"
lacks "$out" "The user's words in this pane stand the same way"; lacks "$out" "submit that bolt again"
ok "a landing's conflict becomes a fix that takes main into the bolt; the bolt's proof is its verification, and ops proves nothing"

# A question goes up a chain of command (briefs.11, record 0031): the planner, main-level ops and the design agent
# carry one question discipline.
for brief in "wldn planner" "wldn main-ops" "wldn design"; do expect_ok crewpy brief $brief; asks_say; done
ok "the planner, main-level ops and the design agent carry one question discipline"

# Units are reviewed in batches (briefs.12): the planner runs the reviewer, whose summary has crew raise the batch's one
# card in the planner's name with one reading session on the batch, posts and closes no batch card, and acts on the
# notes the card's read prints from the session and the card as fixes on the bolts of the units they speak of, or new
# work (briefs.9, briefs.12, briefs.13; Decision 6 of the-team-machinery-leaves); the reviewer writes its summary and nothing else, as prose opening each unit with the paragraph the card
# carries; crew posts no land for a bolt whose changes have not all been in an answered batch.
expect_ok crewpy brief wldn planner
for want in "## Batches" "review wldn\`" "review wldn --wait\`" \
  "crew records the batch, starts its one reading session, the summary and every unit's whole change as one review, and raises its one card in your name, keyed \`batch/<n>\`" \
  "naming every unit of the batch with its bolt and the paragraph the reviewer opened it with, however many" \
  "a batch is never split across cards" "\`call get_request (requestId req_…, name wldn-planner)\`" \
  "Start no wait for the batch's answer: nothing of crew's waits on a card or its reading." \
  "When the user sends the card back with a tap, its answer wakes you, as every card you adopted does" \
  "when they send the reading session, crew tells you so at the rail's next refresh" "card read batch/<n> --label wldn\`" \
  "It prints the card's note and every annotation the user sent, word for word, from the card and the session together, even what they sent while you were down; crew then closes the card, ends the session and records the batch read" \
  "crew records it read at the refresh itself and closes its card \"Read; no notes\", telling you nothing" \
  "card session batch/<n> --label wldn\` prints the session's link again" \
  "You start no session for a batch, and post, change and close no batch card: crew does." \
  "a card raised without its reading says so and why, and names \`$CREW/plugin/bin/crew card session batch/<n> --label wldn\` as your act, never the user's, which starts the reading and changes the card to carry its link" \
  "crew's rail read tries it again too" \
  "names \`$CREW/plugin/bin/crew card session proposal/<n> --label wldn\` as your act, never the user's" \
  "is a fix on that unit's bolt you start yourself" "a note that speaks of several goes whole into each one's fix" \
  "ask the user about on a card of your own, quoting them, saying they named no unit you could tell" \
  "Never split, reword or summarize the user's words" "you never run a stage" \
  "Never answer a batch yourself: only the user's own words in your pane answer it, beside their card and its reading session." \
  "When an agent tells you the user's answer, tell it the user answers on the card or in your pane, and record nothing" \
  "Run the read too once the batch is answered in your pane or the operator's (step 4): it says in whose, without the words, and closes the card you hold." \
  "Act on what the read printed at once" \
  "card answer batch/<n> --excerpt \"<their words, as they wrote them>\"\` at once, once for each batch they answered" \
  "crew reads the words in your own session's transcript as the user's and records the batch answered, as a tap on its card does" \
  "When crew tells you a batch was answered in the operator's pane, with the user's words, act on those as step 3 does too." \
  "a bolt lands only once each of its changes has been in a batch whose card the user has answered" \
  "posted before crew raised one card per batch, is yours as it was" \
  "one per batch, keyed \`batch/<n>\`, which crew raises in your name with the batch's one reading session when the reviewer's summary is delivered, and closes when the user sends it back"; do
  has "$out" "$want"
done
for gone in "of at most five units" "which need notes?" "one in words for the notes" "A unit not picked is fine" \
  "An unanswered batch card holds nothing" "Never answer a batch card yourself" \
  "card session batch/<n> <unit>" "card session batch/<n>-<k> <unit>" "send each picked unit's notes" "once for each of its units" \
  "post the batch's one card" "The card is a notice, kind \`fyi\`" "First start its one reading session" \
  "Close the card with \`ack_answer\`, its outcome naming the units" "for a batch card \`batch/<n>\`, one session on the whole batch" \
  "a decision in it is never the card's answer" "a batch card's summary says first what it is" \
  "card wait batch/" "ends your wait on it" "the wait starts it first" "Send what the wait printed" \
  "Never propose lifting an \`After\` crew wrote from a forecast" "to the conductor of each unit"; do
  lacks "$out" "$gone"
done
lacks "$out" "the user reviews the change written for the new intent"
expect_ok crewpy brief wldn reviewer
[[ $out =~ \{\{[A-Z_]+\}\} ]] && fail "roles/reviewer.md left ${BASH_REMATCH[0]} unfilled"
for want in "# You are wldn-reviewer, the reviewer of wldn" "Write nothing but this file" "at the commit the prompt names" \
  "Each section opens with a paragraph of a few sentences saying what the change does and what the user would most care about" \
  "the planner puts that paragraph on the batch's card as you wrote it" "**The decisions it took**" "**Its risks**" \
  "**Its Touches**: what the change edits, named in words" "never as paths" "**What the user would likely care about**" \
  "paragraphs and plain lists that wrap on a phone, with no code block and no table" "the planner posts the batch's one card from it"; do
  has "$out" "$want"
done
for gone in "**What it does**" "the paths it declares" "the batch's cards"; do lacks "$out" "$gone"; done
expect_ok crewpy brief wldn design; has "$out" "\`wldn-reviewer\`, started fresh for each batch"
expect_ok crewpy brief wldn main-ops
for want in "plugin/bin/crew rail --label wldn\` names it as one that can land" \
  "lands only once each unit's latest change has been in a batch the user has answered: crew posts no land for it until then" \
  "or batches whose card the user has not answered"; do
  has "$out" "$want"
done
ok "the briefs put changes before the user in batches, and main-level ops lands a bolt only once its changes have been in one"

# A decision record is settled by whose decision it is (briefs.15, amended 2026-11-02 on the user's words): what the user
# settled is stated in the record's own words, its deciders line naming where and when, never quoting them, proposed
# until they have seen the record and accepted on their yes with no card, the design agent's own choices are decided and said in the
# pane, and only a choice that is the user's alone is committed as proposed and accepted on their yes; for that one the
# design agent runs crew record at each turn of its status once it is on the kit's main, which raises, changes and closes
# the record's one card in its name, adopts the card by the line crew record prints, names a rule-decided choice in an
# alternatives file, never settled silently, and queues nothing before the yes; it posts and closes no record card, and
# the planner posts none. A decision record holds only how a tool is built or how it behaves (briefs.15 as amended
# 2026-11-13): an order of work, a priority, a freeze, a schedule or a trial, which bolt or unit carries something and
# how a one-off move, rename or carry-over is carried out are the plan's, told to the planner, or to ops for a live
# system, naming the signal of the user's words, with no record, amendment or card, and a unit cites only records of how
# a tool is built or behaves.
expect_ok crewpy brief wldn design
for want in "A decision record holds only how a tool is built or how it behaves" \
  "which bolt or unit carries something, and how a one-off move, rename or carry-over is carried out are the plan's, whoever settles them, the user included" \
  "or to \`wldn-ops\` when it moves a live system, naming the signal of the user's words when they settled it" \
  "write no record or amendment of it and raise no card for it" \
  "A unit you queue cites only records of how a tool is built or behaves" \
  "Every decision record you write, and every amendment you make to one, states each of its decisions in its own words, never the user's words quoted as the decision, and says which of its decisions is whose" \
  "What the user settled, in this pane or relayed by the operator, is theirs: state it in the record's own words, its deciders line naming the user and where and when they settled it, proposed until the user has seen it as a record" \
  "every decision lives in the repository's records and rules, never only in a message" \
  "What the rules already written decide, and every choice cheap to change later, is yours: decide it as a careful designer would" \
  "a design handed back to the user to approve is no design" \
  "Only a choice that is the user's alone, in their name, their money, their plans, public or hard to undo, or one that takes a rule of theirs loosened, is committed as proposed" \
  "put to them on one Pending You card in the record's own words, which crew raises for it through \`crew record\`" \
  "it is accepted only on the user's yes, given in this pane or on that card, and the record says where they gave it" \
  "Your own reading never settles a choice that is the user's" "\`status: proposed\`" "accepted only on their yes.)" \
  "For a record or amendment that holds a choice of the user's alone, commit it with \`status: proposed\`" \
  "the record is proposed until they have seen it and accepted on their yes with no card; where the same record also holds a choice of the user's alone, the card asks that choice and says the rest is theirs already" \
  "Queue no unit from a proposed record or amendment" "Only then queue the units it calls for" \
  "its deciders line names the user and where and when they settled it, quoting none of their words" \
  "states each of its decisions in its own words, never the user's words quoted as the decision" \
  "stating any note they added in the record's own words" "those words are crew's evidence and go into no record" \
  "At each turn of a record's status, once the commit that holds it has landed on the kit's main, run \`$CREW/plugin/bin/crew record <kit> <number> --proposed|--accepted|--rejected\`" \
  "the kit one of atlas-kit, breadboard-kit, switchboard-kit" "refuses a status the file there does not hold" \
  "\`record/<kit>/<number>\`, one card however often the record is revised" \
  "adopt it with the line the command prints, \`call get_request (requestId <id>, name wldn-design)\`" \
  "run it with \`--settled-in-pane --excerpt \"<their yes, as they wrote it in this pane>\"\`, quoting their yes whole" \
  "crew reads those words in your session's transcript, records their yes as given here, and raises no card" \
  "It refuses your own words, or another agent's tell of what the user said" \
  "When it refuses, run it again without the flag, and the user answers on the record's card" \
  "You post and close no record card yourself: crew does both" \
  "a rule-decided choice is never settled silently" "the rules that decided and each rule as it would read loosened" \
  "\`crew record … --proposed --alternatives <file>\`" "loosen the rules as drafted and take the other path, accept the record as ruled, or send it back" \
  "run \`crew record … --proposed\` again: the card you were answered on is closed, naming the new commit, and the revised record goes on a new card that follows it" \
  "run \`crew record … --accepted\`, which closes the card" "run \`crew record … --rejected\`, which closes the card" \
  "set \`status: rejected\` with why, in the record's own words, and where the user said no" \
  "A kit's main moves only through sluice (\`state.3\`), so you never commit on it" "\`sluice submit main --no-wait --json\`" \
  "its main checkout is an anchor its host alone moves to GitHub's main, the fleet's timer or, on a runner host, the runner, which nobody else edits in or moves (\`plan.18\`)" \
  "each host's timer or runner brings its main checkout to them within minutes" \
  "WilldanGroup/willdan-blueprints's main checkout, \`$(space chuck-herdr-alpha willdan)/willdan-blueprints/main\`, in its folder \`$(space chuck-herdr-alpha willdan)/willdan-blueprints\`" \
  "in each kit's main checkout, with its folder, where your worktrees are cut: \`$(space chuck-herdr-alpha willdan)/atlas-kit/main\` (its folder \`$(space chuck-herdr-alpha willdan)/atlas-kit\`), " \
  "Name each checkout and folder by its path: the folder your session began in may be another." \
  "When \`sluice wait\` exits 0 your head landed: remove the worktree and its branch with \`wt -C <the kit's folder>/places/design-<topic> remove --foreground\`" \
  "<the kit's folder>/places/design-<topic> origin/main\`" "you level nothing" "then \`git merge origin/main\`" \
  "once its \`.config/sluice.toml\` names a policy for main" \
  "No checkout on chuck-herdr-alpha is a runner's clone, so you fetch from GitHub where this brief says." \
  "\`git -C <kit> fetch -q origin\`, none in a runner's clone, then \`origin/main\`, never the host's own \`main\`" \
  "in a worktree of your own, \`git -C <kit> fetch -q origin\`, none in a runner's clone, then \`git -C <kit> worktree add" \
  "in a runner's clone no fetch, merging \`origin/main\` once the runner's fetch, made at once on a landing, holds what you conflict with" \
  "so pull (\`git pull --rebase\`) before you commit there. Push only when the user says so." \
  "Run \`crew record … --proposed\` for each proposed record or amendment on your kits' main that has none open" \
  "At your start, once you have called \`whoami\` and \`list_pending\` as *Asking the user* says, read \`$CREW/plugin/bin/crew rail --label wldn\`" \
  "Never run \`npx pendingyou\` or \`pendingyou hold\`" "leave every other card alone" \
  "a choice of the user's alone in it is proposed until they accept it" "quotes the user's words as their decision" \
  "is told to them by number and commit, and goes to them on a card only for a choice that is theirs alone"; do
  has "$out" "$want"
done
lacks "$out" "wt submit"; lacks "$out" "branch -d design/<topic>"; lacks "$out" "this directory"
for gone in "record/<kit>/<number>/<commit>" "The record's card is the one card you post" "post a new card for the new version" \
  "Close the card with \`ack_answer\`" "Accept decision record <number>" "is committed as proposed and put to the user" \
  "The card is still asked" "is proposed until the user accepts it" \
  "record it with those words quoted as its deciders" "quotes those words as the user's decision" \
  "quoting any note they added in their own words" "with the user's words, and take out"; do
  lacks "$out" "$gone"
done
expect_ok crewpy brief wldn planner; lacks "$out" "record/<kit>"
ok "the design agent runs crew record at each turn of a record's status, which raises, changes and closes its one card, names a rule-decided choice, accepts a record only on the user's yes and queues nothing before; no brief posts a record card"

# A chore (plan.11): planned maintenance with no change, no construct and no review, its every commit carrying its trailer.
expect_ok crewpy brief wldn planner
for want in "**Unit, fix or chore.**" "chore add <chore> \"<what is done>\" --bolt <bolt>" "A chore is never split or amended" \
  "its words change by a proposal that drops it and adds it again" "A batch of chores" "chore by chore on the card" \
  "units and chores the proposal makes new to a bolt or the queue, each a box ticked as proposed" \
  "\`unit add\` or \`chore add\`"; do has "$out" "$want"; done
expect_ok crewpy brief wldn design
has "$out" "is queued the same way as a chore: \`$CREW/plugin/bin/crew chore add <chore> \"<what is done>\" --repo <kit>\`"
ok "the planner and the design agent each carry what a chore is to them"

# Every bolt's work runs through Flume (Decisions 1, 6 and 15 of the-team-machinery-leaves): its places' answers and
# fixes are the planner's, its landing carried to the runner on the user's send, the read of its refusal for a conflict with main
# launching its take-main fix, a forecast conflict a take-main fix ops starts, and a red main is a Flume fix place on
# main, sent on the user's word (state.3).
expect_ok crewpy brief wldn planner
for want in "## A bolt's work in Flume" "so \`bolt order\` is how you move one ahead" "keep chains short" \
  "**Plan writes reach its places by their approval.**" "naming drop and add as the way on, so propose the drop and the add" \
  "by your address \`wldn/planner\`" "answer <work> \"<the answer, in the words of whoever gave it>\"\`" \
  "when the place neither stopped short nor waits on its caller" \
  "as its runner last carried it, naming the host and when, so a wait Flume told you of since is answered again once \`$CREW/plugin/bin/crew bolts\` shows the place waiting" \
  "**Its fixes are yours to start.**" \
  "fix <bolt> <name> \"<what is wrong, in the words of whoever found it>\"\`" "fix <bolt> <name> --drop\`" \
  "is in a batch only once its place has merged into its bolt"; do has "$out" "$want"; done
expect_ok crewpy brief wldn main-ops
for want in "Every bolt is a base place of Flume's, and its units, chores and fixes are Flume places on its branch, taken by a runner whose configuration names the kit's repository" \
  "No agent drives a bolt's work, so a landing tells nobody but the user and the planner" \
  "crew records the forecast once and starts nothing for it" "start that fix yourself" \
  "take-main-<main's revision, seven characters> \"Take main into the bolt: merge origin/main into this place" \
  "crew's read of that refusal launches its take-main fix itself" "\`<bolt>--take-main-<main's revision>\`" "start nothing yourself" \
  "the fix having only taken main in: crew posts its land again on that send" "fix <bolt> <name> \"<the note>\" --label wldn\`" \
  "main fix <kit> <name> \"<the failure's words>\" --label wldn\`" "which you launch on reading main red" \
  "its submission held for the user's word" "\`fixes in flight\`" \
  "answer main--<name> \"<the answer>\" --label wldn\`" "\`fix main--<name>\` with the failure's first line" \
  "the user's send of that row is the one word that lands it: crew carries it to the runner as a land of the fix, ahead of the bolts the same send lands, with nothing for you to run" \
  "main fix <kit> <name> --drop --label wldn\`" \
  "who proposes it as a bolt of one chore, first among the planned"; do has "$out" "$want"; done
lacks "$out" "who decide which team builds it"; lacks "$out" "--team <team>"; lacks "$out" "main fix <kit> <name> --send"
ok "a bolt's places' answers and fixes are the planner's, its landing carried to the runner on the user's send, and a red main is a Flume fix place landed on the same send"

# Flume launches a bolt's landing fix where its base place names one (main-level "Main-level ops starts no fix that
# Flume's landing fix covers", its scenario "Flume's landing fix"; crews-bolt-kind-names-its-landing-fix, Decision 7): ops starts
# nothing where the row says Flume's landing fix covers it, starts the fix only where the row names none or says Flume
# ran its landing fixes, and past the bound starts one by hand or tells the planner and the user; a landing fix that
# asks is told to the user.
expect_ok crewpy brief wldn main-ops
for want in "Where its row says Flume's landing fix takes main in, or that Flume launches its landing fix, the fix is Flume's, launched on its own forecast: start nothing, and tell the user in one line" \
  "Only where its row names no landing fix of Flume's, or says Flume ran its landing fixes, start that fix yourself" \
  "Where its row says Flume's landing fix makes the failed checks pass, or that Flume launches its landing fix, the fix is Flume's: start nothing" \
  "Where its row names no landing fix of Flume's, tell the user Flume's words, the check that failed, and start a fix on the bolt with them" \
  "Flume's landing fix, a fix place on the bolt named \`<bolt>-<n>\`, takes main into the bolt" \
  "the bolt's row says Flume ran its landing fixes, or how its fix ended, and that it waits on ops, and crew asks you once in Flume's words, launching nothing" \
  "or, where you judge the bolt should not land, tell the planner and the user in one line" \
  "crew cannot answer a fix it did not launch, so tell the user in one line that it waits and on what" \
  "each take-main fix and each landing fix Flume runs on a bolt in flight"; do has "$out" "$want"; done
ok "main-level ops starts no fix Flume's landing fix covers, and one past its bound"

# A runner host's teams file names its kept repositories (record 0061; Decision 7 of
# a-kept-repositorys-folder-is-the-runners-container): built there, the design agent's brief names its blueprints
# checkout and each kit's at the runner's view with the runner's container as its folder, and the operator's names
# swancloud's, with no ~/Code/github_afterthought/swancloud; and neither has the agent fetch or pull in the runner's
# clone (drive-state "crew fetches nothing in the runner's clone"; boomdrivedev/boomdrive core.14).
blueprints afterthought/blueprints >/dev/null; blueprints agentplot/blueprints >/dev/null; crew state init madswan >/dev/null
crew bolt new crew-work "Work in crew." --repo crew --label madswan >/dev/null
r=/Users/chuck/.local/share/flywheel/repositories; v=/Users/chuck/Code/boomdrive
tf=$(home_of mac-studio)/.config/crew/teams.json
jq --arg r "$r" --arg v "$v" '.repositories = ({} | reduce ("afterthought/blueprints", "agentplot/crew", "afterthought/swancloud") as $a
  (.; .[$a] = {dir: "\($r)/\($a)", checkout: "\($v)/\($a)"}))' "$tf" > "$tf.new" && mv "$tf.new" "$tf"
expect_ok crewpy brief madswan design
for want in "afterthought/blueprints's main checkout, \`$v/afterthought/blueprints\`, in its folder \`$r/afterthought/blueprints\`" \
  "where your worktrees are cut: \`$v/agentplot/crew\` (its folder \`$r/agentplot/crew\`; the runner's clone, which only the runner fetches)." \
  "On mac-studio the runner keeps afterthought/blueprints and agentplot/crew: each is the runner's clone, which the runner alone fetches, every pass and at once on a landing (boomdrivedev/boomdrive \`core.14\`), so there you run no \`git fetch\` and no \`git pull\`, read GitHub's branches at \`origin/<branch>\` as the runner last fetched them, and when you need one fresher, wait for the runner's next fetch." \
  "Until then, its checkout on this host is the runner's view, which only the runner moves: commit on a branch of your own cut from \`origin/main\` as the runner last fetched it, in a worktree, \`git -C $v/afterthought/blueprints worktree add -b design/<topic> $r/afterthought/blueprints/places/design-<topic> origin/main\`, fetching and pulling nothing there, and tell the user the branch."; do has "$out" "$want"; done
lacks "$out" "$(space mac-studio madswan)"; lacks "$out" "git pull --rebase"
expect_ok crewpy brief madswan operator
for want in "on your main level's host, \`$v/afterthought/swancloud\`, in its folder \`$r/afterthought/swancloud\`" \
  "cut from GitHub's main, as the runner last fetched it, with no fetch of your own, since this host's runner alone fetches swancloud's clone: \`git -C $v/afterthought/swancloud worktree add -b crew-teams/<label> $r/afterthought/swancloud/places/crew-teams-<label> origin/main\`" \
  "\`wt -C $r/afterthought/swancloud/places/crew-teams-<label> remove --foreground\`"; do has "$out" "$want"; done
lacks "$out" "~/Code/github_afterthought/swancloud"; lacks "$out" "$(space mac-studio madswan)/swancloud"; lacks "$out" "fetch -q origin"
teams_json mac-studio > "$tf"
ok "on a runner host the design agent's and the operator's briefs name the teams file's checkouts with the folders it gives, and fetch nothing in the runner's clone"
