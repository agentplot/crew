# A host's tests run in its test slots (tests.9). With one slot, a second test waits while the first holds it and
# runs once it is let go; a test started inside another's slot, as t-suite's suites are, runs at once in it; a process
# a test leaves running holds no slot's file, the slot is free once the test has ended, and the process is ended with
# it, sent SIGKILL when it ignores SIGTERM, and the test's exit is the slot's; a signal sent to the slot ends its test
# and what that left; a slot whose holder was killed is free again, and its test and what that left end with it; a
# card's plannotator session, which crew starts in a session of its own, ends once its test's shell has; the slot
# count is CREW_TEST_SLOTS, and a count that is not one is refused; with none given, it is as many tests as the host's
# cores less two hold at what one test costs the host beside others, a core and a half, at least one.
# Reads: tests/slot tests/stubs/plannotator
. "${TESTS:?run crew tests through tests/run, which puts stub herdr, ssh and claude first}/lib.sh" || exit 2
# The stubs' sleep returns at once; the holders here wait with the real one.
zzz=$(type -a -P sleep | grep -vxF "$TESTS/stubs/sleep" | head -1)
[[ -x $zzz ]] || fail "no sleep on PATH but the stub's"
export CREW_TEST_SLOTS_DIR=$T/slots CREW_TEST_SLOTS=1
unset CREW_TEST_SLOT

# hold <name>: a test in a slot that marks itself started and holds its slot until $T/release-<name> exists
hold() {
  python3 "$TESTS/slot" bash -c 'echo "$CREW_TEST_SLOT" > "$1/started-$2"; while [ ! -e "$1/release-$2" ]; do "$3" 0.05; done' \
    _ "$T" "$1" "$zzz" &
}
# until_there <file>: wait for the file, with a limit that holds on a loaded host
until_there() { local _; for _ in $(seq 6000); do [[ -e $1 ]] && return; "$zzz" 0.05; done; fail "$1 never appeared"; }
# held: whether slot-0 is held by someone
held() { python3 -c 'import fcntl, os, sys
fd = os.open(sys.argv[1], os.O_RDWR)
try:
    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
except BlockingIOError:
    sys.exit(0)
sys.exit(1)' "$T/slots/slot-0"; }

hold first; first=$!
until_there "$T/started-first"
eq "$(cat "$T/started-first")" 0
held || fail "the first test does not hold slot-0"
hold second; second=$!
"$zzz" 0.5
[[ -e $T/started-second ]] && fail "the second test started while the first held the only slot"
kill -0 "$second" 2>/dev/null || fail "the second test ended instead of waiting for the slot"
touch "$T/release-first"; wait "$first"
until_there "$T/started-second"
touch "$T/release-second"; wait "$second"
held && fail "slot-0 is still held once both tests ended"
ok "with one slot, a second test waits while the first holds it, and runs once it is let go"

hold outer; outer=$!
until_there "$T/started-outer"
CREW_TEST_SLOT=0 python3 "$TESTS/slot" bash -c 'touch "$1/inner"' _ "$T" || fail "a test inside another's slot failed"
[[ -e $T/inner ]] || fail "a test inside another's slot did not run"
touch "$T/release-outer"; wait "$outer"
ok "a test started inside another's slot runs at once in it"

# A test that leaves a process running, as t-journey-board leaves crew's board follower when it fails before it ends
# it: the process reports whether any file it holds open is slot-0, then waits ten minutes; the test ends once it has
# reported, exiting 3.
# gone <pid>: whether the process has ended; ends <file>: wait until the process whose pid the file holds has ended
gone() { ! kill -0 "$1" 2>/dev/null; }
ends() { until_ok gone "$(cat "$1")" || fail "process $(cat "$1"), which $1 names, is still running"; }
leaves() {
  python3 "$TESTS/slot" bash -c 'python3 -c "import os, sys, time
slot = os.stat(sys.argv[1])
held = []
for fd in range(3, 256):
    try:
        st = os.fstat(fd)
    except OSError:
        continue
    held += [fd] if (st.st_dev, st.st_ino) == (slot.st_dev, slot.st_ino) else []
open(sys.argv[2], \"w\").write(\"holds slot-0\" if held else \"holds no slot\")
time.sleep(600)" "$1/slots/slot-0" "$1/report" & echo $! > "$1/left"
until [ -s "$1/report" ]; do "$2" 0.05; done; exit 3' _ "$T" "$zzz"
}
rc=0; leaves || rc=$?
eq "$rc" 3
eq "$(cat "$T/report")" "holds no slot"
held && fail "slot-0 is still held once its test ended"
ends "$T/left"
ok "a process a test leaves running holds no slot's file, the slot is free once the test has ended, the process is ended with it, and the test's exit is the slot's"

# A process left running that ignores SIGTERM is sent SIGKILL.
python3 "$TESTS/slot" bash -c '(trap "" TERM; exec "$2" 600) & echo $! > "$1/stubborn"' _ "$T" "$zzz" ||
  fail "the test that left a stubborn process failed"
held && fail "slot-0 is still held once the test that left a stubborn process ended"
ends "$T/stubborn"
ok "a process a test left running that ignores SIGTERM is killed"

# A signal sent to the slot ends its test and what the test left, and the slot exits as the test did.
python3 "$TESTS/slot" bash -c 'echo $$ > "$1/signalled"; "$2" 600 & echo $! > "$1/signalled-left"; wait' _ "$T" "$zzz" & sent=$!
until_ok test -s "$T/signalled-left" || fail "the test to be signalled never started"
kill -TERM "$sent"
rc=0; wait "$sent" || rc=$?
eq "$rc" 143
ends "$T/signalled"; ends "$T/signalled-left"
held && fail "slot-0 is still held once the signalled test ended"
ok "a signal sent to the slot ends its test and what the test left, and the slot exits as the test did"

python3 "$TESTS/slot" bash -c 'echo $$ > "$1/killed"; "$2" 600 & echo $! > "$1/killed-left"; wait' _ "$T" "$zzz" & killed=$!
until_ok test -s "$T/killed-left" || fail "the test to be killed never started"
held || fail "the test to be killed never took the slot"
kill -9 "$killed"; wait "$killed" 2>/dev/null || true
python3 "$TESTS/slot" bash -c 'touch "$1/after-kill"' _ "$T" || fail "no test ran after the holder was killed"
[[ -e $T/after-kill ]] || fail "the slot of a killed holder was not free again"
ends "$T/killed"; ends "$T/killed-left"
ok "a slot whose holder was killed is free again, and its test and what that left end with it"

# A card's session as crew starts it, plannotator in a session of its own, by a test that then ends: the stub ends
# once the test's shell has, with no decision written.
echo "# A document" > "$T/doc.md"
python3 "$TESTS/slot" bash -c 'export CREW_TEST_PID=$$
python3 -c "import subprocess, sys
print(subprocess.Popen(sys.argv[1:], start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).pid)" \
  plannotator annotate "$1/doc.md" --gate --json --result-file "$1/result.json" > "$1/session"
until [ -n "$(plannotator sessions --json | jq ".[] | select(.pid == $(cat "$1/session"))")" ]; do "$2" 0.05; done' _ "$T" "$zzz" ||
  fail "the test that started a card's session failed"
ends "$T/session"
[[ ! -e $T/result.json ]] || fail "the card's session wrote a result when its test ended: $(cat "$T/result.json")"
ok "a card's plannotator session, started in a session of its own, ends once its test's shell has"

expect_fail "CREW_TEST_SLOTS is 'none', not a number of slots" env CREW_TEST_SLOTS=none python3 "$TESTS/slot" true
ok "a slot count that is not a number is refused"

# With no count given, a host's slots are as many tests as its cores less two hold at what one test costs the host
# beside others, a core and a half, and at least one (tests.9): ten on deneb's eighteen cores, nine on the box's
# sixteen, five on ten, one on four or two; and this host's from its own cores.
count() { env -u CREW_TEST_SLOTS python3 -c 'import importlib.machinery, sys
slot = importlib.machinery.SourceFileLoader("slot", sys.argv[1]).load_module()
print(" ".join(str(slot.count(int(c))) for c in sys.argv[2:]) if sys.argv[2:] else slot.count())' "$TESTS/slot" "$@"; }
eq "$(count 18 16 10 4 2)" "10 9 5 1 1"
eq "$(count)" "$(count "$(python3 -c 'import os; print(os.cpu_count())')")"
ok "with no count given, a host's slots are as many tests as its cores less two hold at a core and a half each, at least one"
