# crew's specs pass openspec's strict validation (test-suite "crew's specs pass openspec's strict validation"):
# `openspec validate --specs --strict`, run in crew's checkout by the machine's openspec, which tests/run requires,
# passes every spec under openspec/specs/, so a requirement past openspec's 500 characters, or one with no SHALL, MUST
# or scenario, fails the suite at the merge of the change whose archive brought it. It first finds, in scratch specs of
# its own, a requirement of 501 characters refused and one of 500 taken, so an openspec that checks no length fails
# here rather than passing crew's specs unread. Open changes under openspec/changes/ are each change's own to
# validate, and outside it. openspec runs with its telemetry and update check off, so the test reaches no service.
# Reads: openspec/specs/ openspec/config.yaml
. "${TESTS:?run crew tests through tests/run, which puts stub herdr, ssh and claude first}/lib.sh" || exit 2
export DO_NOT_TRACK=1 OPENSPEC_TELEMETRY=0 OPENSPEC_NO_UPDATE_CHECK=1

# scratch <characters>: a project of its own under $T, its one spec's one requirement that many characters long as
# openspec counts them, with its SHALL and a scenario; prints the project's folder
scratch() {
  local d=$T/scratch-$1
  mkdir -p "$d/openspec/specs/x"; printf 'schema: spec-driven\n' > "$d/openspec/config.yaml"
  python3 - "$d/openspec/specs/x/spec.md" "$1" <<'EOF'
import sys
path, n = sys.argv[1], int(sys.argv[2])
text = "The scratch spec SHALL hold this one requirement"
while len(text) < n - 1:
    text += " word"
text = text[: n - 1] + "."
assert len(text) == n
open(path, "w", encoding="utf-8").write(
    f"# x Specification\n\n## Purpose\nA scratch spec whose one requirement is {n} characters long, as openspec counts them.\n\n"
    f"## Requirements\n\n### Requirement: One requirement of {n} characters\n{text}\n\n"
    f"#### Scenario: Read\n- **WHEN** openspec reads it\n- **THEN** it counts {n} characters\n")
EOF
  echo "$d"
}
strict() { (cd "$1" && openspec validate --specs --strict); }

d=$(scratch 500); expect_ok strict "$d"
d=$(scratch 501); expect_fail "1 failed" strict "$d"
ok "openspec's strict validation takes a requirement of 500 characters and refuses one of 501"

out=$(strict "$CREW" 2>&1) || fail "crew's specs fail openspec validate --specs --strict: split each requirement it names into requirements that together say the same, through a change"$'\n'"$out"
has "$out" " 0 failed"
ok "every spec of crew's passes openspec validate --specs --strict"
