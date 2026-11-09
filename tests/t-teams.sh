# crew reads teams.json version 6 alone: drives under `drives`, each named by its label, with their main levels, role
# overrides, and errors for anything missing or inconsistent; a file at another version, version 5 and its
# `partitions` among them, or one listing teams, is refused naming crew's own module, services.crew, or the machine's
# configuration that writes it, and no swancloud module (main-level "Drives are declared in the teams file"). The
# teams file is the one file crew reads of a host's drives (record 0064): swancloud's hosts file, present or not, is
# read for nothing, and a drive with no folder, or whose machine keeps none of its first blueprints repo, is refused.
# What a drive's entry resolves its main level to is the logic tier's (tests/py/test_teams.py).
# Reads: plugin/roles/
. "${TESTS:?run crew tests through tests/run, which puts stub herdr, ssh and claude first}/lib.sh" || exit 2
world

expect_ok crewpy labels; eq "$out" $'wldn\nmadswan\nswancloud'

edit teams "$(part wldn)['roles'] = {'planner': {'effort': 'max'}, 'operator': {'model': 'claude-opus-5-5'}}"
expect_ok crewpy labels
ok "roles overrides on a drive"

edit teams "$(part wldn)['roles'] = {'conductor': {'effort': 'max'}}"
expect_fail "overrides role 'conductor', which it has no definition for" crewpy labels
edit teams "$(part wldn)['roles'] = {'dispatcher': {'effort': 'high'}}"
expect_fail "overrides role 'dispatcher', which it has no definition for. roles: design planner main-ops operator reviewer" crewpy labels
edit teams "$(part wldn)['roles'] = {'planner': {'effort': 'extreme'}}"
expect_fail "roles.planner.effort is 'extreme', which is no effort level" crewpy labels
edit teams "$(part wldn)['roles'] = {'fable': {'effort': 'high'}}"
expect_fail "overrides role 'fable'" crewpy labels
edit teams "$(part wldn)['roles'] = {}"
ok "an override naming a role crew has no definition for, the dispatcher's or a team's among them, or an unknown effort, is refused"

edit teams "del $(part madswan)['session']"
expect_fail "drive madswan in" crewpy labels; has "$out" "has no 'session'"
fixtures
ok "a missing field is an error"

edit teams "del $(part wldn)['state']"
expect_fail "drive wldn in" crewpy labels
has "$out" "names no state repository ('state')"; has "$out" "crew's own module, services.crew, or the machine's configuration that writes it"
fixtures
edit teams "$(part madswan)['state'] = 'crew-state'"
expect_fail "drive madswan: 'state' is its state repository as GitHub owner/name, not \"crew-state\"" crewpy labels
fixtures
expect_ok crewpy labels
ok "a drive without a state repository, or with one not named owner/name, is refused, naming the fix"

edit teams "del $(part wldn)['review']"
expect_fail "drive wldn in" crewpy labels
has "$out" "has no batch setting ('review', with 'every' and 'hours')"; has "$out" "crew's own module, services.crew, or the machine's configuration that writes it"
fixtures
edit teams "del $(part madswan)['review']['hours']"
expect_fail "drive madswan in" crewpy labels; has "$out" "has no batch setting ('review', with 'every' and 'hours')"
fixtures
edit teams "$(part madswan)['review']['every'] = 0"
expect_fail "drive madswan: 'review.every' is how many changes make a batch, a whole number of at least 1, not 0" crewpy labels
fixtures
edit teams "$(part swancloud)['review']['hours'] = '4'"
expect_fail "drive swancloud: 'review.hours' is how many hours make a batch due, a number above 0, not \"4\"" crewpy labels
fixtures
expect_ok crewpy labels
ok "a drive without its batch setting, or with one crew can't read, is refused, naming the field and the fix"

edit teams "del $(part swancloud)['flume']"
expect_fail "drive swancloud in" crewpy labels; has "$out" "has no 'flume'"; has "$out" "crew's own module, services.crew, or the machine's configuration that writes it"
fixtures
ok "a drive without its flume is refused, naming the field and the fix"

expect_ok crewpy brief wldn planner; brief=$out
for h in mac-studio chuck-herdr-alpha; do
  mkdir -p "$(home_of $h)/.config/swancloud"
  printf '{"version": 1, "hosts": {"chuck-herdr-alpha": {"ssh": "elsewhere", "kind": "darwin", "sessions": {"wldn-3": {"dir": "/nowhere", "account": "ia", "partition": "business", "repos": []}}}}}\n' \
    > "$(home_of $h)/.config/swancloud/herdr-hosts.json"
done
expect_ok crewpy labels; eq "$out" $'wldn\nmadswan\nswancloud'
expect_ok crewpy brief wldn planner; eq "$out" "$brief"
lacks "$out" "/nowhere"; lacks "$out" "account ia"
echo "not json" > "$(home_of mac-studio)/.config/swancloud/herdr-hosts.json"
expect_ok crewpy labels
for h in mac-studio chuck-herdr-alpha; do rm -r "$(home_of $h)/.config/swancloud"; done
ok "a hosts file present, whatever it gives a drive's session, is read for nothing"

edit teams "$(part wldn)['repos'].remove('WilldanGroup/willdan-blueprints')"
expect_fail "drive wldn: chuck-herdr-alpha keeps no WilldanGroup/willdan-blueprints, its first blueprints repo" crewpy labels
has "$out" "crew's own module, services.crew, or the machine's configuration that writes it"
fixtures
ok "a drive whose machine keeps none of its first blueprints repo is refused, naming the fix"

edit teams "del $(part madswan)['folder']"
expect_fail "drive madswan in" crewpy labels; has "$out" "has no 'folder', the absolute folder of its herdr session on mac-studio"
has "$out" "crew's own module, services.crew, or the machine's configuration that writes it"
fixtures
ok "a drive with no folder is refused, naming the field and the fix"

for v in 1 2 3 4 5; do
  fixtures $v
  expect_fail "teams.json is version $v, and crew reads only version 6" crewpy labels
  has "$out" "It must be regenerated by crew's own module, services.crew, or the machine's configuration that writes it; crew has done nothing."
done
expect_fail "must be regenerated" crew bolts
fixtures
edit teams "d['version'] = 5; d['partitions'] = [dict(p, partition='business') for p in d.pop('drives')]"
expect_fail "teams.json is version 5, and crew reads only version 6" crewpy labels
has "$out" "It must be regenerated by crew's own module, services.crew, or the machine's configuration that writes it; crew has done nothing."
fixtures
edit teams "d['partitions'] = d.pop('drives')"
expect_fail "teams.json lists no drives: it must be regenerated by crew's own module, services.crew, or the machine's configuration that writes it" crewpy labels
fixtures
edit teams "d['teams'] = []"
expect_fail "teams.json lists teams, which version 6 has no place for: crew runs no team" crewpy labels
has "$out" "crew's own module, services.crew, or the machine's configuration that writes it"
ok "a file at version 1 to 5, version 5's partitions among them, one at 6 with its drives under partitions, or one at 6 that lists teams, is refused with the fix named"
