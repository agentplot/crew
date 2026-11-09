"""crew as a source of its host's Flume (the flume-source spec; record 0057, teams.25): source.entries for the standing
entry of each role that stands of each partition on the host, from the fleet crew.load gives of a teams file, and
source.text for the roles file's text, read back as Flume reads it, as TOML; source.keep for crew's bolt kind written
into the kinds folder beside it, whole and only when its bytes differ. That crew's follower and a main-level start write
the file, renamed over the old one, is t-flume-source's and t-journey-main's."""
import json
import os
import re
import tomllib

import pytest

import crew
import source

DENEB, BOX = "deneb", "chuck-herdr-alpha"
STANDING = {r: False for r in crew.KIND_ROLES}


def hosts(tmp_path):
    """deneb's sessions of agentplot, madswan and swancloud, and the box's wldn-1 and wldn-2, as read 2026-11-07."""
    def sess(space, partition, repos):
        return {"dir": f"{tmp_path}/{space}", "partition": partition, "repos": repos}
    afterthought = ["afterthought/blueprints", "afterthought/crew"]
    willdan = ["WilldanGroup/willdan-blueprints"]
    return {DENEB: {"ssh": DENEB, "sessions": {"agentplot": sess("agentplot", "agentplot", ["agentplot/blueprints"]),
                                               "madswan": sess("madswan", "business", afterthought),
                                               "swancloud": sess("swancloud", "personal", afterthought)}},
            BOX: {"ssh": BOX, "sessions": {"wldn-1": sess("willdan-1", "clients/willdan", willdan),
                                           "wldn-2": sess("willdan-2", "clients/willdan", willdan)}}}


def teams(flume=None):
    """deneb's teams file as read 2026-11-07 16:30Z: agentplot, madswan and swancloud on deneb in sessions of their
    labels' names, wldn on the box in wldn-2 with its planner in wldn-1, every role standing; flume gives a partition's
    setting in its place."""
    flume = flume or {}
    def part(label, partition, blueprints, machine, session, **more):
        return dict({"label": label, "partition": partition, "blueprints": [blueprints], "machine": machine,
                     "session": session, "state": "afterthought/crew-state", "review": {"every": 5, "hours": 4},
                     "flume": flume.get(label, STANDING)}, **more)
    return {"version": 5, "partitions": [
        part("agentplot", "agentplot", "agentplot/blueprints", DENEB, "agentplot"),
        part("madswan", "business", "afterthought/blueprints", DENEB, "madswan"),
        part("swancloud", "personal", "afterthought/blueprints", DENEB, "swancloud"),
        part("wldn", "clients/willdan", "WilldanGroup/willdan-blueprints", BOX, "wldn-2", roles={"planner": {"session": "wldn-1"}})]}


@pytest.fixture
def fleet(tmp_path, monkeypatch):
    """crew.load over deneb's teams file, or one whose partitions' `flume` the case gives, and the hosts file."""
    def loaded(flume=None):
        (tmp_path / "herdr-hosts.json").write_text(json.dumps({"version": 1, "hosts": hosts(tmp_path)}))
        (tmp_path / "teams.json").write_text(json.dumps(teams(flume)))
        monkeypatch.setattr(crew, "HOSTS", tmp_path / "herdr-hosts.json")
        monkeypatch.setattr(crew, "TEAMS", tmp_path / "teams.json")
        crew.load.cache_clear()
        try:
            return crew.load()
        finally:
            crew.load.cache_clear()
    return loaded


def declared(fleet, host):
    """The roles file's text on host, read as Flume reads it: its roles by address."""
    data = tomllib.loads(source.text(source.entries(fleet, host, crew.ASKS), host))
    assert set(data) <= {"roles"}
    return data.get("roles", {})


def test_the_roles_are_the_ones_a_partitions_flume_names():
    assert source.ROLES == crew.KIND_ROLES


class TestEachStandingRoleIsDeclaredAtItsAddressAsItsAgent:
    def test_deneb_holds_five_entries_for_each_of_its_three_partitions(self, fleet):
        roles = declared(fleet(), DENEB)
        assert list(roles) == [f"{label}/{role}" for label in ("agentplot", "madswan", "swancloud") for role in source.ROLES]
        assert roles["agentplot/planner"]["agent"] == "agentplot-planner" and roles["madswan/ops"]["agent"] == "madswan-ops"
        assert all(e["agent"] == a.replace("/", "-") for a, e in roles.items())


class TestAnEntryNamesTheSessionCrewOpensItsAgentIn:
    def test_sessions_of_the_partitions_names(self, fleet):
        roles = declared(fleet(), DENEB)
        assert {a: e["session"] for a, e in roles.items()} == {a: a.split("/")[0] for a in roles}

    def test_a_role_with_a_session_of_its_own_and_the_reviewer_beside_the_planner(self, fleet):
        roles = declared(fleet(), BOX)
        assert {a: e["session"] for a, e in roles.items()} == {
            "wldn/design": "wldn-2", "wldn/planner": "wldn-1", "wldn/reviewer": "wldn-1", "wldn/ops": "wldn-2", "wldn/operator": "wldn-2"}


class TestWhatARoleAnswersIsTheWordsCrewsBriefsGive:
    def test_the_design_agent_the_planner_and_ops_answer_their_words(self, fleet):
        roles = declared(fleet(), DENEB)
        assert roles["madswan/design"]["answers"] == "the design"
        assert roles["madswan/planner"]["answers"] == "the plan"
        assert roles["madswan/ops"]["answers"] == "a live system, a deploy or a landing"
        assert {r: crew.ASKS[r] for r in ("design", "planner", "ops")} == {
            r: roles[f"madswan/{r}"]["answers"] for r in ("design", "planner", "ops")}

    def test_the_briefs_sentence_on_whom_to_ask_gives_the_same_words(self):
        """The sentence the planner's, ops's and the design agent's briefs share (crew.brief needs the host and the
        partition's kits, so the whole brief is t-briefs')."""
        said = crew.cards_how("crew", "madswan", "none yet")
        assert ("ask the agent whose it is with `crew tell`: `madswan-design` for the design, `madswan-ops` for a live "
                "system, a deploy or a landing, `madswan-planner` for the plan.") in said
        assert all(f"`madswan-{r}` for {w}" in said for r, w in crew.ASKS.items())

    def test_the_operator_is_the_door_and_the_reviewer_answers_nothing(self, fleet):
        roles = declared(fleet(), DENEB)
        assert roles["madswan/operator"] == {"agent": "madswan-operator", "session": "madswan", "answerer": True}
        assert roles["madswan/reviewer"] == {"agent": "madswan-reviewer", "session": "madswan"}


class TestAnEntryGivesAStandingAgentsKeysAlone:
    @pytest.mark.parametrize("host", [DENEB, BOX])
    def test_read_as_flume_reads_it(self, fleet, host):
        data = tomllib.loads(source.text(source.entries(fleet(), host, crew.ASKS), host))
        assert list(data) == ["roles"]
        for address, entry in data["roles"].items():
            stream, role = address.split("/")
            assert crew.NAME.match(stream) and role in source.ROLES
            assert {"agent", "session"} <= set(entry) <= {"agent", "session", "answers", "answerer"}

    def test_the_same_fleet_gives_the_same_text(self, fleet):
        f = fleet()
        assert source.text(source.entries(f, DENEB, crew.ASKS), DENEB) == source.text(source.entries(fleet(), DENEB, crew.ASKS), DENEB)

    def test_the_text_says_whose_it_is_and_carries_no_clock(self, fleet):
        said = source.text(source.entries(fleet(), DENEB, crew.ASKS), DENEB)
        head = [l for l in said.splitlines() if l.startswith("#")]
        assert head and "deneb" in head[0] and any("by hand is lost" in l for l in head)
        assert "2026" not in said


class TestNoEntryForAPartitionOnAnotherHostOrARoleThatRunsAsItsKind:
    def test_wldn_on_deneb(self, fleet):
        assert not [a for a in declared(fleet(), DENEB) if a.startswith("wldn/")]

    def test_a_planner_that_runs_as_its_kind(self, fleet):
        roles = declared(fleet({"madswan": dict(STANDING, planner="madswan")}), DENEB)
        assert [a for a in roles if a.startswith("madswan/")] == ["madswan/design", "madswan/reviewer", "madswan/ops", "madswan/operator"]

    def test_a_host_that_is_no_partitions_machine_declares_nothing(self, fleet):
        assert source.entries(fleet(), "mac-studio", crew.ASKS) == []
        assert tomllib.loads(source.text([], "mac-studio")) == {}


# crew's bolt kind as it ships, byte for byte: a change to it fails here, since a version's bytes never change once
# released and a change to the kind is then bolt@2 beside it (the flume-source spec; crew-lands-each-bolt-through-
# flumes-base-place, Decision 2). bolt@1's first release names its landing fix (crews-bolt-kind-names-its-landing-fix,
# Decision 2).
BOLT_KIND = b"""# crew's bolt as a Flume base place, naming its landing fix (record 0056; crew-lands-each-bolt-through-flumes-base-place, Decision 2; crews-bolt-kind-names-its-landing-fix, Decision 2).
[kinds.bolt]
version = 1
branch = "bolt"
lands = true
stages = []
landing_fix = "flume/fix@1"
max_landing_fixes = 3
"""


class TestCrewsKindsFolderHoldsItsBoltKind:
    def kept(self, tmp_path, fleet, host=DENEB):
        roles, kinds = tmp_path / "state/roles.toml", tmp_path / "kinds/crew"
        source.keep(fleet, host, crew.ASKS, roles=roles, kinds=kinds)
        return roles, kinds, kinds / "bolt@1/kind.toml"

    def test_the_package_ships_as_pinned_and_is_a_base_place(self):
        (package, under), = source.KIND_PACKAGES
        assert package.read_bytes() == BOLT_KIND and under.as_posix() == "bolt@1/kind.toml"
        assert tomllib.loads(BOLT_KIND.decode()) == {"kinds": {"bolt": {
            "version": 1, "branch": "bolt", "lands": True, "stages": [],
            "landing_fix": "flume/fix@1", "max_landing_fixes": 3}}}

    def test_the_landing_fix_is_named_by_identity_and_bounded(self):
        (package, _), = source.KIND_PACKAGES
        bolt = tomllib.loads(package.read_text())["kinds"]["bolt"]
        assert re.fullmatch(r"[a-z0-9-]+/[a-z0-9-]+@[0-9]+", bolt["landing_fix"])
        assert bolt["landing_fix"].replace("@", "/").split("/") == ["flume", "fix", "1"]
        limit = bolt["max_landing_fixes"]
        assert isinstance(limit, int) and not isinstance(limit, bool) and limit > 0

    def test_written_once_with_an_entry_and_nothing_else_in_the_folder(self, tmp_path, fleet):
        _, kinds, kind = self.kept(tmp_path, fleet())
        assert kind.read_bytes() == BOLT_KIND
        assert sorted(p.relative_to(kinds).as_posix() for p in kinds.rglob("*")) == ["bolt@1", "bolt@1/kind.toml"]

    def test_not_written_again_with_the_same_bytes(self, tmp_path, fleet):
        f = fleet()
        _, _, kind = self.kept(tmp_path, f)
        os.utime(kind, ns=(1_000_000_000, 1_000_000_000))
        was = kind.stat()
        self.kept(tmp_path, f)
        assert (kind.stat().st_ino, kind.stat().st_mtime_ns) == (was.st_ino, was.st_mtime_ns)

    def test_written_over_when_the_bytes_differ_and_renamed_over_the_old(self, tmp_path, fleet):
        f = fleet()
        _, _, kind = self.kept(tmp_path, f)
        kind.write_bytes(b"[kinds.bolt]\nversion = 1\n")
        held = tmp_path / "held.toml"
        os.link(kind, held)
        self.kept(tmp_path, f)
        assert kind.read_bytes() == BOLT_KIND and held.read_bytes() == b"[kinds.bolt]\nversion = 1\n"

    def test_not_written_with_no_entry(self, tmp_path, fleet):
        roles, kinds, _ = self.kept(tmp_path, fleet(), host="mac-studio")
        assert not kinds.exists() and not roles.exists()

    def test_no_package_where_the_roles_file_is_written_with_no_entry(self, tmp_path, fleet):
        roles, kinds = tmp_path / "state/roles.toml", tmp_path / "kinds/crew"
        roles.parent.mkdir(parents=True)
        roles.write_text("# old\n")
        source.keep(fleet(), "mac-studio", crew.ASKS, roles=roles, kinds=kinds)
        assert not kinds.exists() and "roles" not in tomllib.loads(roles.read_text())
