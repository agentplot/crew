# README, the crew skill and crew's usage name the same commands: every command in the README is in the usage,
# and none of the removed ones is in any of them. CLAUDE.md names how an agent runs crew's tools through the shell
# per command, and no role brief or crew skill does (tests.7); a landing pushes nothing and levels no host in each of
# them (docs.2, plan.18); a start launches the bolt's base place and makes no branch, a drop drops it last, and crew
# deletes no branch, a dropped bolt's kept by sluice while it holds work main lacks; a bolt lands on the user's send,
# which crew carries to the runner, `crew bolt submit` and `crew main fix --send` refused (Decision 11 of
# crew-lands-each-bolt-through-flumes-base-place); CLAUDE.md
# says a host loads crew live from crew/live/plugin or released at a tag swancloud pins, never from a checkout on main,
# which nobody pulls or levels (plan.18, plan.19); a checkout carries the .envrc a person's direnv enters the shell
# with, and ignores devenv's and direnv's working files and the tests' .venv. crew's openspec/config.yaml hands crew's
# construct and coder crew's conventions for its changes (docs.6): each task names its check, no proof list, tick a
# task once its check passes. The README and the opening comment of crew's .config/sluice.toml say crew readies no
# worktree, sluice equipping a place at Flume's asking, `sluice equip` (Flume's record 0036), and the comment cites no
# plan.17, which is retired. README's The flake says the module's drives are keyed by label and listed in label order,
# that another module can give a drive its machine and state, each written once, and what fails evaluation, with no
# label listed twice. README and the skill say a role's run's start takes the ends Flume holds for its role and its end
# asks the runners to confirm them, and README's requests.rec names a confirm. README and the skill say that crew
# drive set mends what it replaces in a file at crew's own version and refuses it only where a check still fails
# (record 0065, point 8). README, the skill and the usage say a piece's end is the runner's report alone, the record
# Flume holds for the runner among them, and name no landing commit as what makes a piece merged or a bolt landed
# (record 0062's stopgap retired; docs.2).
# Reads: README.md CLAUDE.md plugin/roles/ plugin/skills/ .envrc .gitignore openspec/config.yaml .config/sluice.toml
. "${TESTS:?run crew tests through tests/run, which puts stub herdr, ssh and claude first}/lib.sh" || exit 2
world
usage=$(crew 2>&1 || true)
readme=$(cat "$CREW/README.md"); skill=$(cat "$CREW/plugin/skills/crew/SKILL.md")
n=0
while read -r line; do
  words=${line#crew }; words=${words%%[<\[\"-]*}; set -- $words
  cmds=$1; subs=${2:-}
  for c in ${cmds//|/ }; do
    lines=$(grep -E "^ *crew +$c( |$)" <<<"$usage") || fail "README's crew $c is not in crew's usage"
    for sub in ${subs//|/ }; do
      grep -qE "(^| |\|)$sub( |\||$)" <<<"$lines" || fail "README's crew $c $sub is not in crew's usage"
      n=$((n + 1))
    done
    n=$((n + 1))
  done
done < <(grep -E '^crew ' "$CREW/README.md")
echo "$n commands checked"
(( n >= 100 )) || fail "too few commands read from the README"
ok "every command in the README is in crew's usage"

# the removed crew release <team> by its command: a release is otherwise crew's own, plugin/release.json and crew _release
for gone in assign "crew release" opsx fable explorer verifier coder-; do
  for doc in usage readme skill; do lacks "${!doc}" "$gone"; done
done
for gone in assign release opsx list status up rebuild close restart resume clear down _tidy _status _team; do
  expect_fail "every bolt, unit and chore of the plans" crew $gone swb-1
done
for doc in usage readme skill; do
  team=$(grep -oE '(^|[^a-z_])crew +(list|status|up|rebuild|close|restart|resume|clear|down)([^a-z]|$)' <<<"${!doc}" || true)
  [[ -z $team ]] || fail "the $doc names a team command:"$'\n'"$team"
  for gone in "<team or drive>" "(sent to <team" "SLUICE_BRANCH" "sluice_branch" "conductor fresh" "unit slot"; do
    lacks "${!doc}" "$gone"
  done
  has "${!doc}" 'crew send'; has "${!doc}" '<drive> "<text>"'
done
for doc in usage readme skill; do lacks "${!doc}" "unit approve"; lacks "${!doc}" "review/<unit>"; done
for doc in usage readme skill; do has "${!doc}" "crew review"; done
for gone in "unit run" "unit wait" "unit free" "chore run" "chore wait" "chore free" "crew needs" "fix <team>"; do
  for doc in usage readme skill; do lacks "${!doc}" "$gone"; done
done
for gone in "unit run a code" "unit wait a" "chore free c"; do expect_fail "invalid choice" crew $gone; done
expect_fail "crew: each drive's plan of bolts, its main level of agents in herdr" crew needs "what it needs"
ok "none of the removed commands or roles is in the README, the skill or the usage, a team command among them, crew drives no stage and waits on none, crew send names a drive alone, and each names crew review"

for doc in usage readme skill; do has "${!doc}" "crew ops offer <env>"; has "${!doc}" "[--notes <file>] [--steps <file>]"; has "${!doc}" "[--ticked <n>[,<n>...]]"; done
for doc in usage readme skill; do
  for gone in "crew plan card" "crew card post" "crew card change" "crew card close" "post|change" "propose|proposed|agree|card"; do
    lacks "${!doc}" "$gone"
  done
  has "${!doc}" "crew record"
done
for doc in usage readme; do has "${!doc}" "session|end <key>"; has "${!doc}" "read <key>"; lacks "${!doc}" "session|wait|end"; done
for want in "crew card session <key>" "crew card end <key>" "crew card read <key>"; do has "$skill" "$want"; done
lacks "$skill" "crew card wait <key>"
for doc in usage readme skill; do
  has "${!doc}" "crew card wait"; has "${!doc}" "refused at once, naming"
  has "${!doc}" "beside the run record"
done
for doc in usage readme skill; do has "${!doc}" "what an earlier send still lands, with or without a card open"; done
for doc in usage readme skill; do has "${!doc}" "preview <key> <thing> [--done]"; done
has "$skill" "crew card preview <key> <thing> [--done]"
expect_fail "invalid choice: 'post'" crew card post land/x
expect_fail "invalid choice: 'card'" crew plan card 1
ok "the README, the skill and the usage give crew ops offer's notes and steps and crew ops approve's ticked steps, crew record and crew card read, session, end and preview, crew card wait refused naming the read, crew card read land/<kit> with no card open, each landing as the runner reports it beside the run record, and no crew plan card or crew card post, change or close, which crew no longer has"

for doc in usage readme skill; do
  has "${!doc}" "pushes nothing and levels no host"; has "${!doc}" "origin/main"; lacks "${!doc}" "behind GitHub's"
done
ok "the README, the skill and the usage say a landing pushes nothing and levels no host, and a bolt is cut from origin/main"

for doc in usage readme skill; do
  for want in "base place" "crew/bolt" "holds work main lacks" "lands under the crew that started it" "crew carries"; do
    has "${!doc}" "$want"
  done
  for gone in "sluice branch create" "sluice branch delete" "0.20.0" "stays local until it lands" "while main lacks its tip" \
    "have sluice delete" "standing in sluice" "landing queued as" "submitted only once crew reads them" "wt submit main"; do
    lacks "${!doc}" "$gone"
  done
done
for doc in readme skill; do has "${!doc}" "origin/bolt/<bolt>"; done
has "$usage" "start, the user's or a proposal's, makes no branch and reads no host"
has "$usage" "drop drops each"; has "$usage" "last its base place's"
has "$usage" "refused at once, before it reads anything, with any arguments"; has "$usage" "refused at once, before it reads anything, naming the way: a fix of main lands on"
has "$readme" "and last the launch of its base place, which Flume refuses while a place on its branch is live"
has "$readme" "\`crew bolt submit\`, with any arguments, is refused at once, before it reads anything, naming the card's send as the way"
has "$readme" "\`crew main fix <kit> <name> --send\`, with or without \`--excerpt\`, is refused at once"
has "$skill" "crew deletes no bolt branch"; has "$skill" "\`crew bolt submit <bolt>...\` is refused at once, naming the card's send"
has "$skill" "\`crew main fix <kit> <name> --send\` is refused at once, naming the card's send"
claude=$(cat "$CREW/CLAUDE.md")
for want in "a bolt lands on the user's send of its row on its kit's landings card, and on nothing else" \
  "no agent runs \`crew bolt submit\`, which is refused" "crew's read of Flume's refusal launches a fix on the bolt"; do
  has "$claude" "$want"
done
lacks "$claude" "ops submits the bolt with"; lacks "$claude" "run in the background and waited on to its end"
ok "the README, the skill and the usage say a start launches the bolt's base place and makes no branch, a drop drops it last, crew deletes no branch, a dropped bolt's kept while it holds work main lacks, a bolt started before lands under its crew, and a bolt and a fix of main land on the user's send, which crew carries to the runner, crew bolt submit and crew main fix --send refused; CLAUDE.md says no agent runs a landing"

for doc in usage readme skill; do
  has "${!doc}" '<bolt> <name> "<what is wrong>"'; has "${!doc}" "start"; has "${!doc}" "started already"; has "${!doc}" "waits to land"
  for gone in "bolt give" "crew bolt give" "one more" "a give" "never refused for the bolts" "plan agree" "dispatch" "agreement"; do
    lacks "${!doc}" "$gone"
  done
  has "${!doc}" "bolt start"
done
expect_fail "unrecognized arguments: --merge" crew fix tenant-environments edge --merge
ok "the README, the skill and the usage say a bolt's work is started by crew bolt start, refused for one started already, and name no give, agreement or dispatcher, a proven bolt waits to land, and crew fix names its bolt, with no --merge or --wait"

for doc in usage readme skill; do
  for want in "version 6, which lists no team" "version 2, 3, 4 or 5 among them" 'its drives under `drives`' "in Flume stream" "Path: flume" "no team's conductor, ops or slot" \
    "requests.rec" "<label>/runner/<host>" "crew answer" "fix <kit> <name> --send"; do has "${!doc}" "$want"; done
  for gone in "due to cross" "due back" "however they went down" "closes what the hold left" "crossed team" "version 3 of the teams file" \
    "Version 3 of the teams file" "version-2 file" "version 4 names" "version 4 of the teams file" "at version 2 or 3" "versions 2 and 3" \
    "<team|label>" "version 5, which lists no team" "<partition>"; do lacks "${!doc}" "$gone"; done
done
ok "the README, the skill and the usage say the teams file is version 6, its drives under drives, and lists no team, an older one refused, that crew runs no team's agents, its launches in requests.rec and its runner's branch, crew answer and crew main fix, and no team due to cross or crossing"

# The README, the skill and the usage keep no team section, roles row or run-record act of the old path (Task 8.3 of
# the-team-machinery-leaves): the README's roles are the five main-level definitions, the acts an older crew wrote are
# entries from before, and the usage opens on the plan and the main level.
for gone in "## Teams" "Bolt teams of" "conductor.md" "construct.md" "coder.md" "verify.md" "dispatcher.md" "| ops, team and main level" \
  "such as \`unit.add\`, \`bolt.give\`" "\`team.up\` or" "on the host of the team holding" "on the team's host" "sent to their teams"; do
  lacks "$readme" "$gone"
done
for want in "## Bolts" "| main-level ops | \`main-ops.md\` |" "\`bolt.start\`" "in entries from before, acts crew writes no more" \
  "in entries from before, \`team/<team>\`"; do has "$readme" "$want"; done
for gone in "**A team**" "of the team holding" "on the team's host" "its team's fix"; do lacks "$skill" "$gone"; done
for doc in usage readme skill; do lacks "${!doc}" "bolt teams"; done
has "$(head -1 <<<"$usage")" "crew: each drive's plan of bolts, its main level of agents in herdr, and its bolts' work in Flume."
ok "the README, the skill and the usage keep no team section, roles row or old run-record act as current, and the usage opens on the plan and the main level"

for doc in usage readme skill; do
  for want in "runs as its kind" "every role stands" "asks.rec" "roles.rec" "crew-<role>--<label>" "end --report <path>" \
    "open <role>" "land <repo> <name> --brief-file <file>" "delivered [--label L]" "pendingyou watch -- crew _answered" \
    "ended at its next stop" "never restarted"; do has "${!doc}" "$want"; done
done
for doc in usage readme; do has "${!doc}" "turns/<role>.md"; done
for doc in readme skill; do
  for want in "the ends Flume holds for" "asks the runners to confirm each end"; do has "${!doc}" "$want"; done
done
has "$readme" "and a confirm, which a role's run's end appends for each launch whose place's ends its turn took"
ok "the README, the skill and the usage say a drive's flume, a role that runs as its kind, its asks in asks.rec and its record in roles.rec, crew role start, end, open and land, the ends a run takes and its end confirms, crew review delivered, the follower's notice of a card's change, and a standing agent of such a role ended at its stop"

for doc in usage readme skill; do
  for want in "piece's end is the runner's report alone" "the record Flume holds for the runner"; do has "${!doc}" "$want"; done
  for gone in "Sluice-From" "names its place's branch" "landed on its bolt at" "main holds its landing"; do lacks "${!doc}" "$gone"; done
  has "${!doc}" "no landing commit on its kit's main read for it"
done
ok "the README, the skill and the usage say a piece's end is the runner's report alone, the record Flume holds for the runner among them, name no landing commit as what makes a piece merged or a bolt landed, and read none on main for crew bolt land"

# The teams file may name its host's kept repositories (record 0061): README and the skill say what crew names there, and
# the drives' folders where it names none. It is the one file crew reads for a host's drives (record 0064): README, the
# skill and openspec/config.yaml name its hosts, each drive's folder, repos and accounts, and the host's consoles, and
# none names swancloud's hosts file (docs.2).
for doc in readme skill; do
  for want in "the file may name the kept repositories of the host it is written on, \`repositories\`" \
    "with exactly its \`dir\` and its \`checkout\`, each an absolute path" "the runner's container and view on a runner host" \
    "Where the file names none, a kit's folder and checkout are \`<folder>/<name>\` and \`<folder>/<name>/main\` in the folder of the first drive on that host whose \`repos\` lists it" \
    "\`repos\` is a drive's list of addresses, \`repositories\` the host's map of each address to its folder and checkout" \
    "The teams file is the one file crew reads for a host's drives and the hosts that serve them" \
    "\`hosts\`, each host crew reaches or reads, by the name \`hostname -s\` gives it, with exactly its \`ssh\` name and its \`kind\`, \`darwin\` or \`nixos\`" \
    "\`folder\`, the absolute folder of its herdr session on its machine" \
    "\`repos\`, the repositories that folder keeps there" "\`accounts\`, the Claude account each of its five main-level roles runs under" \
    "\`consoles\`, for the host it is written on, each drive whose console that host opens"; do
    has "${!doc}" "$want"
  done
done
config=$(cat "$CREW/openspec/config.yaml")
has "$config" "It is the one file crew reads for a host's drives"
for doc in readme skill config usage; do lacks "${!doc}" "herdr-hosts"; lacks "${!doc}" "hosts file"; done
ok "the README and the skill say the teams file is the one file crew reads for a host's drives, its hosts, each drive's folder, repos and accounts, and its consoles, that it may name its host's kept repositories, and the drives' folders where it names none, and nothing names swancloud's hosts file"

has "$(cat "$CREW/CLAUDE.md")" "devenv shell -- "
wrapped=$(grep -rlF -- 'devenv shell --' "$CREW/plugin/roles" "$CREW/plugin/skills" || true)
[[ -z $wrapped ]] || fail "these briefs or skills name the shell's wrap, which is CLAUDE.md's to say:"$'\n'"$wrapped"
ok "CLAUDE.md names the per-command form of crew's shell, and no brief or skill does"

claude=$(cat "$CREW/CLAUDE.md")
for want in "## How crew reaches a host" "crew/live/plugin" "release tags" "cut from \`origin/main\`"; do has "$claude" "$want"; done
for gone in "This checkout is live" "read-tree" "merge --ff-only" "git pull" "brings every host's checkout up"; do
  lacks "$claude" "$gone"
done
ok "CLAUDE.md says crew/main is an anchor, a host loads crew live from crew/live/plugin or released at a pinned tag, and work is cut from origin/main, with no pull or levelling of crew's checkout"

grep -qxF 'use devenv' "$CREW/.envrc" || fail ".envrc does not enter devenv"
for line in .devenv/ .direnv/ '!.envrc' tests/.venv/; do grep -qxF -- "$line" "$CREW/.gitignore" || fail ".gitignore lacks $line"; done
ok "a checkout carries the .envrc and ignores devenv's and direnv's working files and the tests' .venv"

has "$readme" "crew readies no worktree"; has "$readme" '`sluice equip`'
policy=$(awk '/^\[/ { exit } { print }' "$CREW/.config/sluice.toml")
has "$policy" "sluice equip"; lacks "$policy" "plan.17"
ok "the README says crew readies no worktree and names sluice equip, and the policy's opening comment names sluice equip and no plan.17"

config=$(cat "$CREW/openspec/config.yaml")
for want in "the check in crew's tiers that proves it" "tests/suite --affected" "*Task notes*" "no proof list of any name" \
  "*After deploy* lists only the steps no check can be code" "is a check this change adds" \
  "Tick a task only once the check it names passes"; do
  has "$config" "$want"
done
ok "crew's openspec/config.yaml says crew's conventions for its changes: each task names its check, no proof list, and a task is ticked once its check passes"

flake=$(awk '/^## The flake$/ { on = 1; next } /^## / { on = 0 } on' "$CREW/README.md")
for want in "every drive by its label" "listed in the order of their labels" "its \`label\` its name, which no host sets" \
  "can give a drive its \`machine\` and \`state\` by its label" "Each of the two is written once" "drives given as a list" \
  "a \`label\` the host sets" "no drive,"; do
  has "$flake" "$want"
done
lacks "$flake" "a label listed twice"
ok "the README's flake says the drives are keyed by label and listed in label order, another module gives a drive's machine and state, each written once, and what fails evaluation, with no label listed twice"

for doc in "$readme" "$skill"; do
  has "$doc" "mends what it replaces"; has "$doc" "a check still fails"
done
ok "README and the skill say crew drive set mends what it replaces in a file at crew's own version and refuses it only where a check still fails"
