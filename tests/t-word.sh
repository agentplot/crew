# crew's word for a body of work is drive (Boomdrive record 0028; the design of crews-partition-is-a-drive, Decision
# 8): crew's command, plugin, module, README, CLAUDE.md, OpenSpec configuration and specs, the specs read as the
# archived change leaves them, hold "partition" in no case, but for a Python .partition( or .rpartition( call and a
# former key quoted as one, `partition` or `partitions`. It lists each offending file and line and fails once,
# having first found the word, and only the word, in a scratch file of its own. tests/, nix/tests/, the records, the
# rules, the explorations and openspec/changes/ are outside it: tests hold the former shapes on purpose, and the rest
# is dated or the design agent's.
# Reads: plugin/ nix/modules/ nix/packages/ flake.nix README.md CLAUDE.md openspec/config.yaml openspec/specs/
. "${TESTS:?run crew tests through tests/run, which puts stub herdr, ssh and claude first}/lib.sh" || exit 2

# said <path>...: how many files it read, on its first line, then each file:line holding the word, every allowed
# use taken out of the line first; a file that is not text is not read
said() {
  python3 - "$@" <<'EOF'
import os, re, sys
ALLOWED = re.compile(r"\.r?partition\(|`partitions?`")
WORD = re.compile("partition", re.I)
SKIP = {"__pycache__", "node_modules", ".venv"}

def files(top):
    if os.path.isfile(top):
        yield top
    for d, dirs, fs in os.walk(top):
        dirs[:] = sorted(x for x in dirs if x not in SKIP)
        yield from (os.path.join(d, f) for f in sorted(fs))

read, hits = 0, []
for top in sys.argv[1:]:
    for f in files(top):
        try:
            text = open(f, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        read += 1
        hits += [f"{f}:{n}: {line.strip()[:160]}" for n, line in enumerate(text.splitlines(), 1) if WORD.search(ALLOWED.sub("", line))]
print(read)
print("\n".join(hits))
EOF
}

# The check finds the word and nothing it allows: a line naming a partition, a str.partition call, an rpartition
# call and a former key quoted as one, of which only the first is named.
mkdir -p "$T/word"
printf '%s\n' 'A partition is a drive.' 'head, _, rest = line.partition(" ")' 'a, _, b = s.rpartition("/")' \
  'no `partitions` key and no `partition`' 'Partitions too.' > "$T/word/sample.md"
out=$(said "$T/word")
eq "$out" "1"$'\n'"$T/word/sample.md:1: A partition is a drive."$'\n'"$T/word/sample.md:5: Partitions too."
ok "the check names a line that holds the word in any case, and none that holds only a .partition( or .rpartition( call or a quoted former key"

cd "$CREW" || fail "no crew checkout at $CREW"
out=$(said plugin nix/modules nix/packages flake.nix README.md CLAUDE.md openspec/config.yaml openspec/specs)
n=$(head -n 1 <<<"$out"); hits=$(tail -n +2 <<<"$out")
(( n > 0 )) || fail "the check read no file of crew's"
[[ -z $hits ]] || fail "crew's text says partition where crew's word is drive (Boomdrive record 0028), at:"$'\n'"$hits"
ok "crew's command, plugin, module, README, CLAUDE.md, OpenSpec configuration and specs, $n files, say drive: no partition but a .partition( call and a former key quoted as one"
