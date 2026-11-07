# A test's waits start little (tests.8, tests.9): lib.sh's nap pauses, on macOS as anywhere, with no command on the
# path; until_ok looks at once and ends there when its command succeeds, and looks less often the longer it waits, its
# pauses doubling from a tenth of a second up to a second, so a wait of a few seconds runs its command a handful of
# times rather than ten a second; and the stub sluice's wait on a submission held undecided exits 5 only after a
# moment of about a second, so a landing's waiter calling it again while it is held calls about once a second.
. "${TESTS:?run crew tests through tests/run, which puts stub herdr, ssh and claude first}/lib.sh" || exit 2
# since <start>: the seconds since EPOCHREALTIME was <start>, to a millisecond
since() { python3 -c 'import sys, time; print(f"{time.time() - float(sys.argv[1]):.3f}")' "$1"; }
# at_least <seconds> <limit>: whether seconds is no less than limit
at_least() { python3 -c 'import sys; sys.exit(0 if float(sys.argv[1]) >= float(sys.argv[2]) else 1)' "$1" "$2"; }

mkdir -p "$T/empty"
t0=$EPOCHREALTIME
(PATH=$T/empty; nap 0.3) || fail "nap failed with no command on the path"
took=$(since "$t0")
at_least "$took" 0.3 || fail "nap 0.3 took $took seconds"
ok "nap pauses with no command on the path"

looks=0
at_once() { looks=$((looks + 1)); }
until_ok at_once || fail "until_ok failed on a command that succeeds"
eq "$looks" "1"
looks=0; t0=$EPOCHREALTIME
after() { looks=$((looks + 1)); at_least "$(since "$t0")" "$1"; }
until_ok after 3 || fail "until_ok never saw three seconds pass"
# Pauses of 0.1, 0.2, 0.4, 0.8, 1 and 1 seconds pass three seconds at the seventh look; a looser host only lengthens
# them, so it looks fewer times, never more.
(( looks <= 7 )) || fail "until_ok looked $looks times in three seconds"
ok "until_ok looks at once and ends there when its command succeeds, and looks less often the longer it waits"

# A submission the stub made, held undecided.
gitconfig "$HOME"
r=$T/kit; git init -q "$r"; git -C "$r" commit -q --allow-empty -m "chore: start"
common=$(git -C "$r" rev-parse --path-format=absolute --git-common-dir)
echo '{"schema": "sluice/submission@1", "id": 7, "branch": "main", "state": "landed", "rc": 0}' > "$common/stub-sluice-wait-7.json"
touch "$T/sluice-wait-holds"
t0=$EPOCHREALTIME; rc=0
out=$(cd "$r" && sluice wait 7 --timeout 9m --json) || rc=$?
took=$(since "$t0")
eq "$rc" "5"; eq "$(jq -r .state <<<"$out")" "testing"
at_least "$took" 0.9 || fail "a held wait exited 5 after $took seconds"
rm "$T/sluice-wait-holds"
rc=0; out=$(cd "$r" && sluice wait 7 --timeout 9m --json) || rc=$?
eq "$rc" "0"; eq "$(jq -r .state <<<"$out")" "landed"
ok "the stub sluice's wait on a submission held undecided exits 5 after about a second, and decides once the hold is lifted"
