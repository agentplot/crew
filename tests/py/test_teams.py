"""The main level and its agents (teams.2, teams.6, teams.7, teams.11, code.5): crew.load for the teams file at version
6, its drives alone, and each drive's Flume setting, crew.role_stream and
crew.kind_role_of for which of a drive's main-level roles run as their kinds, crew.greet_waits for one look of
a greeting's wait, crew.standing_greeting for what a main level's agent is greeted with, crew.operator_session for where an operator runs, crew.tab_holds for what an operator's tab holds,
crew.dead_said for a pane herdr lists with no terminal behind it and crew.opens_at for where a pane opens again,
crew.last_conversation for where a role resumes,
crew.brief_due and crew.brief_role for the brief a session herdr resumed is given back at a compaction,
crew.main_named and crew.identity_withheld for whether a main level's agent herdr resumed gets its identity back on this host,
and plan.kind_said for what crew main status says of a role that runs as its kind. Starting, greeting, reviving and
taking them down through the command are the main level's journey's (t-journey-main)."""
import builtins
import json
import os
import pathlib
import re

import pytest

import crew
import plan

BOX = "chuck-herdr-alpha"
FLEET = {"drives": {"wldn": {"label": "wldn", "machine": BOX, "session": "wldn-3"}},
         "hosts": {"mac-studio": {"ssh": "mac-studio", "kind": "darwin"}}, "consoles": {"wldn": "/w/willdan"}}
STANDING = {r: False for r in crew.KIND_ROLES}
HOSTS = {BOX: {"ssh": BOX, "kind": "nixos"}, "mac-studio": {"ssh": "mac-studio", "kind": "darwin"}}


def every(account):
    """A drive's `accounts`, every main-level role on one account."""
    return {r: account for r in crew.KIND_ROLES}


def loaded(tmp_path, monkeypatch, data, hosts_file=None):
    """crew.load over a teams file holding data, written in tmp_path; with hosts_file, swancloud's hosts file beside it
    in the home crew runs in, holding it, which crew reads nothing of (record 0064)."""
    (tmp_path / "teams.json").write_text(json.dumps(data))
    monkeypatch.setattr(crew, "TEAMS", tmp_path / "teams.json")
    if hosts_file is not None:
        swancloud = tmp_path / ".config/swancloud"
        swancloud.mkdir(parents=True, exist_ok=True)
        (swancloud / "herdr-hosts.json").write_text(json.dumps({"version": 1, "hosts": hosts_file}))
        monkeypatch.setattr(pathlib.Path, "home", classmethod(lambda cls: tmp_path))
    crew.load.cache_clear()
    try:
        return crew.load()
    finally:
        crew.load.cache_clear()


class TestLoad:
    """The teams file at version 6 holds drives alone, under `drives`, each named by its label, and every fact crew
    reads of a host's drives and of the hosts that serve them (main-level "Drives are declared in the teams file";
    Boomdrive record 0028; record 0064): no hosts file is read; the files' refusals by field are t-teams'."""

    def data(self, version=6, key="drives", **more):
        part = {"state": "afterthought/crew-state", "review": {"every": 5, "hours": 4}, "flume": STANDING}
        return dict({"version": version, "hosts": HOSTS,
                     key: [dict(part, label="wldn", blueprints=["WilldanGroup/willdan-blueprints"], machine=BOX, session="wldn-3",
                                folder="/box/willdan", repos=["WilldanGroup/switchboard-kit", "WilldanGroup/willdan-blueprints"],
                                accounts=every("ia")),
                           dict(part, label="madswan", blueprints=["afterthought/blueprints"], machine="mac-studio",
                                session="madswan-1", folder="/mac/madswan", repos=["afterthought/blueprints", "afterthought/crew"],
                                accounts=every("madswan"))]}, **more)

    def refused(self, tmp_path, monkeypatch, data, said):
        """The file refused, saying said, naming the teams file's writer as the fix."""
        with pytest.raises(crew.Refusal, match=said) as refused:
            loaded(tmp_path, monkeypatch, data)
        assert crew.WRITER in str(refused.value)
        return str(refused.value)

    def test_a_drives_main_level_folder_and_repos_come_from_its_entry_and_the_fleet_holds_no_teams(self, tmp_path, monkeypatch):
        """main-level, No hosts file: the file gives every key, and crew loads it with none present."""
        assert not hasattr(crew, "HOSTS") and not hasattr(crew, "read_hosts")
        fleet = loaded(tmp_path, monkeypatch, self.data())
        assert set(fleet) == {"hosts", "drives", "repositories", "consoles"} and list(fleet["drives"]) == ["wldn", "madswan"]
        assert fleet["hosts"] == HOSTS and fleet["consoles"] == {} and fleet["repositories"] == {}
        p = crew.drive_of(fleet, "wldn")
        assert (p["machine"], p["session"], p["ssh"], p["folder"]) == (BOX, "wldn-3", BOX, "/box/willdan")
        assert "teams" not in p and "dir" not in p
        assert p["checkout"] == "/box/willdan/willdan-blueprints/main" and p["accounts"] == every("ia")
        assert p["repos"] == ["WilldanGroup/switchboard-kit", "WilldanGroup/willdan-blueprints"]
        assert p["flume"] == STANDING and p["sessions"]["planner"] == "wldn-3"

    def test_clients_willdan_starts_in_its_folders_blueprints(self, tmp_path, monkeypatch):
        """main-level, clients/willdan: wldn on chuck-herdr-alpha in wldn-2, its folder /workspace and its repos naming
        willdan-blueprints, starts in /workspace/willdan-blueprints/main, and its plan is wldn/main of crew-state."""
        data = self.data()
        data["drives"][0].update(session="wldn-2", folder="/workspace", state="WilldanGroup/crew-state")
        fleet = loaded(tmp_path, monkeypatch, data)
        monkeypatch.setattr(crew, "definition", lambda role: ({"model": "opus", "effort": "high"}, ""))
        monkeypatch.setattr(crew, "kits_on", lambda fleet, label, host, fetch=False: [])
        assert crew.launch(fleet, "wldn", "operator")["cwd"] == "/workspace/willdan-blueprints/main"
        assert crew.place_of_agent(fleet, "wldn-operator") == (BOX, "wldn-2")
        assert crew.drive_of(fleet, "wldn")["state"] == "WilldanGroup/crew-state"

    @pytest.mark.parametrize("given", [
        {BOX: {"ssh": "box", "sessions": {"wldn-3": {"dir": "/elsewhere", "partition": "clients/willdan", "account": "credits",
                                                     "repos": ["WilldanGroup/atlas-kit"]}}}},
        {"mac-studio": {"ssh": "studio", "home": "/Users/chuck", "kind": "linux", "sessions": {}}},
        {}])
    def test_a_hosts_file_present_is_read_for_nothing(self, tmp_path, monkeypatch, given):
        """main-level, A session's `partition` in the hosts file: whatever swancloud's hosts file gives wldn's session, its
        partition, folder, account or ssh name, crew loads the teams file the same as with none, opening nothing of it."""
        bare = loaded(tmp_path, monkeypatch, self.data())
        opened = []
        real_read, real_open = pathlib.Path.read_text, builtins.open
        monkeypatch.setattr(pathlib.Path, "read_text", lambda self, *a, **k: opened.append(str(self)) or real_read(self, *a, **k))
        monkeypatch.setattr(builtins, "open", lambda f, *a, **k: opened.append(str(f)) or real_open(f, *a, **k))
        assert loaded(tmp_path, monkeypatch, self.data(), hosts_file=given) == bare
        assert not [f for f in opened if "swancloud" in f or "herdr-hosts" in f]

    @pytest.mark.parametrize("version", [1, 2, 3, 4, 5, 7, "6", True, None])
    def test_another_version_is_refused_naming_6_and_the_machines_configuration(self, tmp_path, monkeypatch, version):
        with pytest.raises(crew.Refusal, match=f"teams.json is version {json.dumps(version)}, "
                           "and crew reads only version 6. It must be regenerated by crew's own module, services.crew, "
                           "crew drive set, or the machine's configuration that writes it; crew has done nothing."):
            loaded(tmp_path, monkeypatch, self.data(version))

    def test_the_file_at_version_5_is_refused_naming_version_6(self, tmp_path, monkeypatch):
        """main-level, The file at version 5: its drives under `partitions`, each naming its `partition`, as deneb's file
        held them on 2026-11-08, refused by its version before anything else of it is read."""
        data = self.data(5, key="partitions")
        for entry, grouping in zip(data["partitions"], ("clients/willdan", "business")):
            entry["partition"] = grouping
        read = []
        monkeypatch.setattr(crew, "hosts_of", lambda data: read.append("hosts"))
        with pytest.raises(crew.Refusal, match="teams.json is version 5, and crew reads only version 6. It must be regenerated by "
                                               "crew's own module, services.crew, crew drive set, or the machine's configuration that writes it; crew has done nothing."):
            loaded(tmp_path, monkeypatch, data)
        assert read == []

    def test_a_version_6_file_whose_drives_are_under_partitions_lists_no_drives(self, tmp_path, monkeypatch):
        """main-level, A version-6 file whose drives are under `partitions`: no former key is read, so it lists no
        drives, as an empty `drives` does, and the fix is named."""
        for data in (self.data(key="partitions"), self.data(drives=[])):
            with pytest.raises(crew.Refusal, match="teams.json lists no drives: it must be regenerated by crew's own module, "
                                                   "services.crew, crew drive set, or the machine's configuration that writes it; crew has done nothing."):
                loaded(tmp_path, monkeypatch, data)

    @pytest.mark.parametrize("refused", ["version", "teams", "drives", "state", "review", "flume", "repositories", "hosts",
                                         "folder", "repos", "accounts", "consoles"])
    def test_every_refusal_of_the_file_names_crews_own_module_and_no_other_repositorys(self, tmp_path, monkeypatch, refused):
        """main-level, Every refusal of the file names crew's own fix: crew is the family's tool, not the fleet's, so the
        fix of a refused teams file is crew's own module, services.crew, crew drive set, or the machine's configuration that writes it,
        never swancloud's lib/crew-teams.nix (agentplot-design on batch 23 of crew-names-each-drive-once; code.5)."""
        data = self.data()
        if refused == "version":
            data["version"] = 5
        elif refused == "teams":
            data["teams"] = []
        elif refused == "drives":
            data["drives"] = []
        elif refused == "repositories":
            data["repositories"] = {"agentplot/crew": {"dir": "crew"}}
        elif refused == "hosts":
            del data["hosts"]
        elif refused == "consoles":
            data["consoles"] = {"wldn": "w"}
        else:
            del data["drives"][0][refused]
        with pytest.raises(crew.Refusal) as said:
            loaded(tmp_path, monkeypatch, data)
        assert crew.WRITER in str(said.value) and "services.crew" in crew.WRITER
        assert "swancloud" not in str(said.value) and "crew-teams.nix" not in str(said.value)

    def test_a_missing_file_is_refused_naming_its_four_writers(self, tmp_path, monkeypatch):
        """main-level, No teams file: refused naming the file and crew's own module, services.crew, crew drive set and the
        machine's configuration as its writers, with nothing done (design, Decision 13)."""
        monkeypatch.setattr(crew, "TEAMS", tmp_path / "teams.json")
        crew.load.cache_clear()
        with pytest.raises(crew.Refusal) as said:
            crew.load()
        assert str(said.value) == (f"{tmp_path}/teams.json is missing: it must be written by crew's own module, services.crew, "
                                   "crew drive set, or the machine's configuration that writes it; crew has done nothing.")

    @pytest.mark.parametrize("text, words", [("{\"version\": 6,", "Expecting property name enclosed in double quotes"),
                                             ("", "Expecting value: line 1 column 1"), ("version: 6", "Expecting value")])
    def test_a_file_that_is_no_json_is_refused_naming_it_and_the_parsers_words(self, tmp_path, monkeypatch, text, words):
        """main-level, A file that is no JSON: refused naming the file and the parser's words, a Refusal and never a
        traceback (code.2), naming the writer as every refusal of the file does."""
        (tmp_path / "teams.json").write_text(text)
        monkeypatch.setattr(crew, "TEAMS", tmp_path / "teams.json")
        crew.load.cache_clear()
        with pytest.raises(crew.Refusal) as said:
            crew.load()
        assert str(said.value).startswith(f"{tmp_path}/teams.json is no JSON (") and words in str(said.value)
        assert crew.WRITER in str(said.value)

    @pytest.mark.parametrize("data", [[], "drives", 6, None])
    def test_json_that_is_no_object_is_refused_naming_the_writer(self, tmp_path, monkeypatch, data):
        """A file whose JSON is no object is a teams file of no shape crew reads: refused, never a traceback."""
        with pytest.raises(crew.Refusal, match="not a teams file's object") as said:
            loaded(tmp_path, monkeypatch, data)
        assert crew.WRITER in str(said.value)

    def test_fleet_of_plain_data_answers_as_load_does_on_the_same_file(self, tmp_path, monkeypatch):
        """Decision 5: crew.load is a read of the file and crew.fleet_of(data, here), a function of the file's data and
        this host's name that starts no process, and answers the same fleet; here is read only where the file names
        kept repositories."""
        for data in (self.data(), self.data(repositories={"afterthought/crew": {"dir": "/r/crew", "checkout": "/v/crew"}})):
            monkeypatch.setattr(crew, "this_host", lambda: "mac-studio")
            assert crew.fleet_of(json.loads(json.dumps(data)), "mac-studio") == loaded(tmp_path, monkeypatch, data)
        asked = []
        assert crew.fleet_of(self.data(), lambda: asked.append(1))["repositories"] == {} and asked == []
        with pytest.raises(crew.Refusal, match="is version 5"):
            crew.fleet_of(self.data(5), "mac-studio")

    @pytest.mark.parametrize("field, said", [
        ("folder", "drive wldn in .*teams.json has no 'folder', the absolute folder of its herdr session on chuck-herdr-alpha"),
        ("repos", "drive wldn in .*teams.json has no 'repos', the repositories its folder keeps on chuck-herdr-alpha"),
        ("accounts", "drive wldn in .*teams.json has no 'accounts', which names the Claude account each of its roles, "
                     "design, planner, reviewer, ops, operator, runs under")])
    def test_a_drive_with_no_folder_repos_or_accounts_is_refused_naming_it_the_field_and_the_writer(self, tmp_path, monkeypatch, field, said):
        """main-level, A drive with no folder, repos or accounts."""
        data = self.data()
        del data["drives"][0][field]
        self.refused(tmp_path, monkeypatch, data, said)

    @pytest.mark.parametrize("folder", ["work/willdan", "", None, ["/w"]])
    def test_a_relative_folder_is_refused_naming_the_drive_and_its_folder(self, tmp_path, monkeypatch, folder):
        """main-level, A relative folder."""
        data = self.data()
        data["drives"][0]["folder"] = folder
        self.refused(tmp_path, monkeypatch, data, f"drive wldn in .*teams.json: 'folder' is the absolute folder of its herdr "
                                                  f"session on chuck-herdr-alpha, not {re.escape(json.dumps(folder))}")

    @pytest.mark.parametrize("repos, said", [
        ("WilldanGroup/willdan-blueprints", "'repos' lists the repositories its folder keeps on chuck-herdr-alpha, each <owner>/<name>, not"),
        (["willdan-blueprints"], "'repos' names \"willdan-blueprints\", which is no <owner>/<name>"),
        (["WilldanGroup/willdan-blueprints", 7], "'repos' names 7, which is no <owner>/<name>")])
    def test_a_repos_entry_that_is_no_address_is_refused(self, tmp_path, monkeypatch, repos, said):
        data = self.data()
        data["drives"][0]["repos"] = repos
        self.refused(tmp_path, monkeypatch, data, f"drive wldn in .*teams.json: {said}")

    @pytest.mark.parametrize("accounts, said", [
        ({r: "ia" for r in ("design", "planner", "ops", "operator")}, "'accounts' leaves out the reviewer"),
        (dict(every("ia"), dispatcher="ia"), "'accounts' names dispatcher, which is no main-level role"),
        (dict(every("ia"), planner="IA"), "accounts.planner is the Claude account it runs under, a name crew accepts, not \"IA\""),
        (dict(every("ia"), ops=None), "accounts.ops is the Claude account it runs under, a name crew accepts, not null"),
        ("ia", "'accounts' names each of its roles with its Claude account, not \"ia\"")])
    def test_an_account_left_out_or_named_wrongly_is_refused_naming_the_drive_and_the_role(self, tmp_path, monkeypatch, accounts, said):
        """main-level, An account left out: wldn's accounts naming no reviewer is refused, naming wldn and the reviewer."""
        data = self.data()
        data["drives"][0]["accounts"] = accounts
        self.refused(tmp_path, monkeypatch, data, f"drive wldn in .*teams.json: {said}")

    def test_two_accounts_in_one_session_are_refused_naming_the_drive_the_session_and_both(self, tmp_path, monkeypatch):
        """main-level, Two accounts in one session: wldn's design agent and ops run in wldn-2, the one on willdan-alex and
        the other on credits; a herdr session runs under one account."""
        data = self.data()
        data["drives"][0].update(session="wldn-2", roles={"planner": {"session": "wldn-1"}},
                                 accounts=dict(every("willdan-alex"), planner="ia", reviewer="ia", ops="credits"))
        said = self.refused(tmp_path, monkeypatch, data, "drive wldn's design \\(willdan-alex\\), ops \\(credits\\), operator "
                                                         "\\(willdan-alex\\) run in session wldn-2 under credits and willdan-alex, "
                                                         "and a herdr session runs under one account")
        assert "wldn-1" not in said
        data["drives"][0]["accounts"]["ops"] = "willdan-alex"
        p = crew.drive_of(loaded(tmp_path, monkeypatch, data), "wldn")
        assert p["sessions"] == {"design": "wldn-2", "planner": "wldn-1", "ops": "wldn-2", "operator": "wldn-2", "reviewer": "wldn-1"}

    def test_a_blueprints_repo_its_machine_does_not_keep_is_refused(self, tmp_path, monkeypatch):
        """main-level, A blueprints repo its machine does not keep: wldn's repos does not list willdan-blueprints and the
        box's file names it in no `repositories`."""
        data = self.data()
        data["drives"][0]["repos"] = ["WilldanGroup/switchboard-kit"]
        self.refused(tmp_path, monkeypatch, data, "drive wldn: chuck-herdr-alpha keeps no WilldanGroup/willdan-blueprints, its "
                                                  "first blueprints repo: .*teams.json lists it neither in the drive's 'repos' "
                                                  "nor in 'repositories' for chuck-herdr-alpha")
        named = {"WilldanGroup/willdan-blueprints": {"dir": "/r/willdan-blueprints", "checkout": "/v/willdan-blueprints"}}
        monkeypatch.setattr(crew, "this_host", lambda: "mac-studio")
        self.refused(tmp_path, monkeypatch, dict(data, repositories=named), "drive wldn: chuck-herdr-alpha keeps no")
        monkeypatch.setattr(crew, "this_host", lambda: BOX)
        assert crew.drive_of(loaded(tmp_path, monkeypatch, dict(data, repositories=named)), "wldn")["checkout"] == "/v/willdan-blueprints"

    def test_a_machine_the_file_gives_no_host_for_is_refused(self, tmp_path, monkeypatch):
        """main-level, A machine the file gives no host for: wldn runs on chuck-herdr-alpha and `hosts` names only deneb."""
        data = dict(self.data(), hosts={"deneb": {"ssh": "deneb", "kind": "darwin"}})
        self.refused(tmp_path, monkeypatch, data, "drive wldn runs on chuck-herdr-alpha, which .*teams.json's 'hosts' does not "
                                                  "name. hosts: deneb")

    def test_no_hosts_is_refused_naming_hosts_and_the_writer(self, tmp_path, monkeypatch):
        """main-level, No hosts."""
        data = self.data()
        del data["hosts"]
        self.refused(tmp_path, monkeypatch, data, "teams.json gives no 'hosts', the ssh name and kind of each host crew reaches or reads")

    @pytest.mark.parametrize("deneb, said", [
        ({"kind": "darwin"}, "host deneb in 'hosts' has no 'ssh'"),
        ({"ssh": "deneb"}, "host deneb in 'hosts' has no 'kind'"),
        ({"ssh": "deneb", "kind": "macos"}, "host deneb's 'kind' is darwin or nixos, not \"macos\""),
        ({"ssh": "deneb", "kind": "darwin", "home": "/Users/chuck"}, "host deneb in 'hosts' gives 'home', which crew has no place for"),
        ({"ssh": "", "kind": "darwin"}, "host deneb's 'ssh' is the name ssh reaches it by, not \"\""),
        ("deneb", "host deneb in 'hosts' gives exactly its 'ssh' and its 'kind', not \"deneb\"")])
    def test_a_host_named_wrongly_is_refused_naming_it_and_the_key(self, tmp_path, monkeypatch, deneb, said):
        """main-level, A host named wrongly: no ssh, a kind of macos, or a home beside its ssh and kind."""
        self.refused(tmp_path, monkeypatch, dict(self.data(), hosts=dict(HOSTS, deneb=deneb)), f"teams.json: {said}")

    @pytest.mark.parametrize("hosts, said", [
        ({"Deneb": {"ssh": "deneb", "kind": "darwin"}}, "'hosts' names \"Deneb\", which is no name crew accepts"),
        (["deneb"], "'hosts' names each host crew reaches or reads, by its name, with its 'ssh' and its 'kind', not")])
    def test_a_hosts_name_crew_does_not_accept_is_refused(self, tmp_path, monkeypatch, hosts, said):
        self.refused(tmp_path, monkeypatch, dict(self.data(), hosts=hosts if isinstance(hosts, list) else dict(HOSTS, **hosts)),
                     f"teams.json: {said}")

    def test_a_roles_session_of_another_drive_loads_as_the_file_names_it(self, tmp_path, monkeypatch):
        """main-level, A session of another drive: wldn's planner named madswan's session loads, checked against no list
        of sessions: herdr runs the session the file names."""
        data = self.data()
        data["drives"][0]["roles"] = {"planner": {"session": "madswan-1"}}
        fleet = loaded(tmp_path, monkeypatch, data)
        assert crew.place_of_agent(fleet, "wldn-planner") == (BOX, "madswan-1")
        assert crew.place_of_agent(fleet, "wldn-design") == (BOX, "wldn-3")

    def test_the_consoles_of_the_host_load_and_a_console_of_no_drive_is_refused(self, tmp_path, monkeypatch):
        """main-level, The consoles of the host and A console of no drive."""
        consoles = {"wldn": "/Users/chuck/Code/clients/github_willdan", "madswan": "/Users/chuck/Code/github_afterthought"}
        assert loaded(tmp_path, monkeypatch, self.data(consoles=consoles))["consoles"] == consoles
        self.refused(tmp_path, monkeypatch, self.data(consoles=dict(consoles, swancloud="/w")),
                     "teams.json: 'consoles' names swancloud, which is no drive the file lists. drives: wldn madswan")
        self.refused(tmp_path, monkeypatch, self.data(consoles={"wldn": "Code/clients/github_willdan"}),
                     "teams.json: consoles.wldn is the absolute folder its console's tabs open in, not \"Code/clients/github_willdan\"")
        self.refused(tmp_path, monkeypatch, self.data(consoles=["wldn"]), "teams.json: 'consoles' maps each drive whose console")

    def test_a_file_that_still_lists_teams_is_refused_at_version_4_5_or_6(self, tmp_path, monkeypatch):
        """main-level, The file before version 5, A version-5 file that lists teams and A version-6 file that lists teams:
        a version-4 or -5 file is refused by its version; nor does version 6 hold one, a teams list being no field of
        it, never read in order to be ignored (code.5)."""
        teams = [{"name": "swb-1", "system": "Switchboard", "machine": BOX, "session": "wldn-3", "units": 4,
                  "repos": ["switchboard-kit", "willdan-blueprints"], "flume": "wldn"}]
        for version in (4, 5):
            with pytest.raises(crew.Refusal, match=f"is version {version}, and crew reads only version 6.*crew's own module, services.crew"):
                loaded(tmp_path, monkeypatch, self.data(version, key="partitions", teams=teams))
        for listed in (teams, []):
            with pytest.raises(crew.Refusal, match="teams.json lists teams, which version 6 has no place for: crew runs no team. "
                                                   "It must be regenerated by crew's own module, services.crew, crew drive set, or the machine's configuration"):
                loaded(tmp_path, monkeypatch, self.data(teams=listed))

    def test_the_boxs_file_at_version_2_is_refused_by_its_version_with_nothing_further_read(self, tmp_path, monkeypatch):
        """main-level, The box's file at version 2: chuck-herdr-alpha's file for wldn's teams, its `partitions` with a
        team beside them as tests/lib.sh's teams_old writes it, is refused by its version alone, before its teams or its
        hosts are read (code.5)."""
        teams = [{"name": "swb-1", "system": "Switchboard", "machine": BOX, "session": "wldn-1", "units": 4,
                  "repos": ["switchboard-kit", "willdan-blueprints"], "flume": False}]
        read = []
        monkeypatch.setattr(crew, "hosts_of", lambda data: read.append("hosts"))
        with pytest.raises(crew.Refusal, match="teams.json is version 2, and crew reads only version 6. It must be regenerated by "
                                               "crew's own module, services.crew, crew drive set, or the machine's configuration that writes it; crew has done nothing."):
            loaded(tmp_path, monkeypatch, self.data(2, key="partitions", teams=teams))
        assert read == []


class TestReadable:
    """crew.readable: the data of a teams file crew can read at all, and the refusal of one it cannot, no JSON, no
    UTF-8, no object or at a version this crew does not read, in the words crew.load gives for the same file (record
    0065, point 6; a-drive-set-loses-no-drive-and-no-record, Decision 1). A file it gives the data of is at crew's own
    version, and fleet_of makes every later check."""

    def load_said(self, tmp_path, monkeypatch, raw):
        (tmp_path / "teams.json").write_bytes(raw)
        crew.load.cache_clear()
        try:
            with pytest.raises(crew.Refusal) as said:
                crew.load()
        finally:
            crew.load.cache_clear()
        return str(said.value)

    @pytest.mark.parametrize("raw", [b"{\"version\": 6,", b"version: 6", b"\xff\xfe{}", b"[]", b"{}", b"{\"version\":\"6\"}",
                                     b"{\"version\":true}", b"{\"version\":5}"])
    def test_a_file_crew_cannot_read_at_all_is_refused_in_loads_words(self, tmp_path, monkeypatch, raw):
        monkeypatch.setattr(crew, "TEAMS", tmp_path / "teams.json")
        with pytest.raises(crew.Refusal) as said:
            crew.readable(raw)
        assert str(said.value) == self.load_said(tmp_path, monkeypatch, raw)
        assert crew.WRITER in str(said.value)

    @pytest.mark.parametrize("data, refused", [({"version": 6, "drives": [], "hosts": {}}, "lists no drives"),
                                               ({"version": 6, "teams": []}, "lists teams, which version 6 has no place for")])
    def test_a_file_at_crews_own_version_is_read_and_fleet_of_refuses_it(self, tmp_path, monkeypatch, data, refused):
        monkeypatch.setattr(crew, "TEAMS", tmp_path / "teams.json")
        raw = json.dumps(data).encode()
        assert crew.readable(raw) == data and crew.readable(raw.decode()) == data
        with pytest.raises(crew.Refusal, match=refused) as said:
            crew.fleet_of(crew.readable(raw), "mac-studio")
        assert str(said.value) == self.load_said(tmp_path, monkeypatch, raw)


class TestKeptRepositories:
    """main-level, A runner host's kept repositories (record 0061; Decisions 3 and 4 of
    a-kept-repositorys-folder-is-the-runners-container): the teams file may name, for the host it is written on, each
    repository that host keeps, its `dir` and its `checkout`, checked whole at load; the fleet keeps them with that host."""

    CREW = {"dir": "/Users/chuck/.local/share/flywheel/repositories/agentplot/crew", "checkout": "/Users/chuck/Code/boomdrive/agentplot/crew"}

    def load(self, tmp_path, monkeypatch, **more):
        return loaded(tmp_path, monkeypatch, TestLoad().data(**more))

    def test_a_runner_hosts_kept_repositories_are_the_fleets_with_the_host_they_are_for(self, tmp_path, monkeypatch):
        monkeypatch.setattr(crew, "this_host", lambda: "deneb")
        fleet = self.load(tmp_path, monkeypatch, repositories={"agentplot/crew": self.CREW})
        assert fleet["repositories"] == {"host": "deneb", "named": {"agentplot/crew": self.CREW}}
        assert crew.kept_on(fleet, "deneb", "agentplot/crew") == self.CREW["checkout"]

    def test_a_file_that_names_none_names_no_repository_and_reads_no_host(self, tmp_path, monkeypatch):
        """main-level, A file that names no repository: the logic tier's fixture refuses any process, so no host is read;
        madswan's folder keeps crew, so mac-studio keeps it there."""
        fleet = self.load(tmp_path, monkeypatch)
        assert fleet["repositories"] == {}
        assert self.load(tmp_path, monkeypatch, repositories={})["repositories"] == {}
        assert crew.kit_kept(fleet, "mac-studio", "crew") == {"name": "crew", "repo": "afterthought/crew", "dir": "/mac/madswan/crew",
                                                             "main": "/mac/madswan/crew/main"}

    def test_a_repository_no_drive_of_the_host_lists_is_not_kept(self, tmp_path, monkeypatch):
        """main-level, A repository no drive of the host lists: mac-studio's drives list no atlas-kit, so it keeps none."""
        fleet = self.load(tmp_path, monkeypatch)
        assert crew.kit_kept(fleet, "mac-studio", "atlas-kit") is None
        assert crew.kept_on(fleet, "mac-studio", "WilldanGroup/atlas-kit") is None

    def test_a_drive_whose_blueprints_the_file_names_on_its_host_starts_in_the_files_checkout(self, tmp_path, monkeypatch):
        """Decision 6: madswan's main level runs on mac-studio, whose file names afterthought/blueprints, so its checkout,
        where its roles start, is the file's; wldn's, on the box, is its folder's as before."""
        monkeypatch.setattr(crew, "this_host", lambda: "mac-studio")
        named = {"afterthought/blueprints": {"dir": "/r/afterthought/blueprints", "checkout": "/v/afterthought/blueprints"}}
        fleet = self.load(tmp_path, monkeypatch, repositories=named)
        assert crew.drive_of(fleet, "madswan")["checkout"] == "/v/afterthought/blueprints"
        assert crew.drive_of(fleet, "wldn")["checkout"] == "/box/willdan/willdan-blueprints/main"
        monkeypatch.setattr(crew, "definition", lambda role: ({"model": "opus", "effort": "high"}, ""))
        monkeypatch.setattr(crew, "kits_on", lambda fleet, label, host, fetch=False: [])
        assert crew.launch(fleet, "madswan", "design")["cwd"] == "/v/afterthought/blueprints"
        monkeypatch.setattr(crew, "this_host", lambda: BOX)
        fleet = self.load(tmp_path, monkeypatch, repositories=named)
        assert crew.drive_of(fleet, "madswan")["checkout"] == "/mac/madswan/blueprints/main"

    @pytest.mark.parametrize("repositories, said", [
        ([], "'repositories' maps each kept repository, <owner>/<name>, to its 'dir' and 'checkout', not \\[\\]"),
        (None, "'repositories' maps each kept repository, <owner>/<name>, to its 'dir' and 'checkout', not null"),
        ({"crew": CREW}, "names kept repository \"crew\", which is no <owner>/<name>"),
        ({"agentplot/crew": {"dir": CREW["dir"]}}, "kept repository agentplot/crew gives exactly its 'dir' and its 'checkout'"),
        ({"agentplot/crew": dict(CREW, view="/v")}, "kept repository agentplot/crew gives exactly its 'dir' and its 'checkout'"),
        ({"agentplot/crew": "/r"}, "kept repository agentplot/crew gives exactly its 'dir' and its 'checkout', not \"/r\""),
        ({"agentplot/crew": dict(CREW, dir="repositories/agentplot/crew")},
         "kept repository agentplot/crew's 'dir' is an absolute path, not \"repositories/agentplot/crew\""),
        ({"agentplot/crew": dict(CREW, dir="")}, "kept repository agentplot/crew's 'dir' is an absolute path, not \"\""),
        ({"agentplot/crew": dict(CREW, checkout=7)}, "kept repository agentplot/crew's 'checkout' is an absolute path, not 7")])
    def test_a_kept_repository_named_wrongly_is_refused_naming_the_file_it_and_the_fix(self, tmp_path, monkeypatch, repositories, said):
        """main-level, A kept repository named wrongly: refused before anything else is read, the hosts among it."""
        read = []
        monkeypatch.setattr(crew, "hosts_of", lambda data: read.append("hosts"))
        with pytest.raises(crew.Refusal, match=said) as refused:
            self.load(tmp_path, monkeypatch, repositories=repositories)
        assert "teams.json" in str(refused.value) and crew.WRITER in str(refused.value)
        assert read == []


DENEB = {"deneb": {"ssh": "deneb", "kind": "darwin"}}


class TestRoleSettings:
    """A drive's Flume setting for each of its main-level roles (record 0047 move 6, the change
    roles-run-as-flume-kinds' Decision 3): `flume` on every drive, each of the five roles false while it stands or
    the stream its runs run in, and nothing else."""

    NONE = object()  # a drive that names no `flume`

    def load(self, tmp_path, monkeypatch, flume):
        part = {"blueprints": ["afterthought/blueprints"], "state": "afterthought/crew-state", "review": {"every": 5, "hours": 4},
                "machine": "deneb", "folder": "/deneb/madswan", "repos": ["afterthought/blueprints", "afterthought/crew"],
                "accounts": every("madswan")}
        madswan = dict(part, label="madswan", session="madswan-1", **({} if flume is self.NONE else {"flume": flume}))
        swancloud = dict(part, label="swancloud", session="swancloud-1", flume=STANDING)
        return loaded(tmp_path, monkeypatch, {"version": 6, "hosts": DENEB, "drives": [madswan, swancloud]})

    TWO = {"design": False, "planner": "madswan-roles", "reviewer": "madswan-roles", "ops": False, "operator": False}

    def test_each_drive_names_each_roles_stream_or_that_it_stands(self, tmp_path, monkeypatch):
        fleet = self.load(tmp_path, monkeypatch, self.TWO)
        assert crew.drive_of(fleet, "madswan")["flume"] == self.TWO
        assert crew.role_stream(fleet, "madswan", "planner") == "madswan-roles"
        assert crew.role_stream(fleet, "madswan", "ops") is False
        assert crew.role_stream(fleet, "swancloud", "planner") is False

    @pytest.mark.parametrize("flume, said", [
        (NONE, "drive madswan in .*teams.json has no 'flume', which names each of its roles, design, planner, reviewer, ops, operator"),
        ([], "drive madswan in .*teams.json: 'flume' names each of its roles, not \\[\\]"),
        (dict(TWO, dispatcher=False), "drive madswan in .*teams.json: 'flume' names dispatcher, which crew has no kind for"),
        ({r: False for r in ("design", "planner", "reviewer", "ops")}, "drive madswan in .*teams.json: 'flume' leaves out operator"),
        (dict(TWO, planner=True), "drive madswan in .*teams.json: flume.planner is false, or the name of a Flume stream its host declares, not true"),
        (dict(TWO, ops=None), "flume.ops is false, or the name of a Flume stream its host declares, not null"),
        (dict(TWO, design=""), "flume.design is false, or the name of a Flume stream its host declares, not \"\""),
        (dict(TWO, operator="Roles"), "flume.operator is false, or the name of a Flume stream its host declares, not \"Roles\""),
        (dict(TWO, reviewer=0), "flume.reviewer is false, or the name of a Flume stream its host declares, not 0")])
    def test_a_drive_without_a_good_setting_is_refused_naming_it_the_role_and_the_fix(self, tmp_path, monkeypatch, flume, said):
        with pytest.raises(crew.Refusal, match=said) as refused:
            self.load(tmp_path, monkeypatch, flume)
        assert crew.WRITER in str(refused.value)

    def test_an_agent_name_is_its_drive_and_role_only_where_the_role_runs_as_its_kind(self, tmp_path, monkeypatch):
        fleet = self.load(tmp_path, monkeypatch, self.TWO)
        assert crew.kind_role_of(fleet, "madswan-planner") == ("madswan", "planner")
        assert crew.kind_role_of(fleet, "madswan-reviewer") == ("madswan", "reviewer")
        for name in ("madswan-design", "madswan-ops", "swancloud-planner", "madswan-main-ops", "madswan-dispatch-deneb",
                     "crw-4-conductor", "madswan", "planner", "", None):
            assert crew.kind_role_of(fleet, name) is None, name

    def test_a_role_with_no_kind_is_refused(self, tmp_path, monkeypatch):
        fleet = self.load(tmp_path, monkeypatch, self.TWO)
        with pytest.raises(crew.Refusal, match="dispatcher is no main-level role that runs as a kind. roles: design planner reviewer ops operator"):
            crew.role_stream(fleet, "madswan", "dispatcher")
        with pytest.raises(crew.Refusal, match="no drive 'wldn'"):
            crew.role_stream(fleet, "wldn", "planner")


class TestRoleSessions:
    """A main-level role may run in a session of its own, named in its drive's roles (record 0035): so a
    drive's design agent and planner sit in two sessions on two Claude accounts, as the drive's `accounts` gives them."""

    def load(self, tmp_path, monkeypatch, roles, accounts=None):
        teams = {"version": 6, "hosts": DENEB, "drives": [{
            "label": "swancloud", "blueprints": ["afterthought/blueprints"], "state": "afterthought/crew-state",
            "review": {"every": 5, "hours": 4}, "machine": "deneb", "session": "swancloud-1", "folder": "/deneb/madswan",
            "repos": ["afterthought/blueprints", "afterthought/crew"], "roles": roles, "flume": STANDING,
            "accounts": accounts or (dict(every("madswan"), planner="madswan-2", reviewer="madswan-2")
                                     if (roles.get("planner") or {}).get("session") else every("madswan"))}]}
        return loaded(tmp_path, monkeypatch, teams)

    def test_a_role_named_a_session_runs_there_the_reviewer_beside_the_planner_and_the_rest_in_the_main_levels(self, tmp_path, monkeypatch):
        fleet = self.load(tmp_path, monkeypatch, {"planner": {"session": "swancloud-2", "effort": "max"}})
        p = crew.drive_of(fleet, "swancloud")
        assert p["sessions"] == {"design": "swancloud-1", "planner": "swancloud-2", "ops": "swancloud-1", "operator": "swancloud-1",
                                 "reviewer": "swancloud-2"}
        assert crew.place_of_agent(fleet, "swancloud-planner") == ("deneb", "swancloud-2")
        assert crew.place_of_agent(fleet, "swancloud-operator") == ("deneb", "swancloud-1")
        assert crew.main_sessions(p) == [("swancloud-1", ("design", "ops", "operator")), ("swancloud-2", ("planner",))]

    def test_with_none_named_every_role_is_in_the_main_levels_session(self, tmp_path, monkeypatch):
        p = crew.drive_of(self.load(tmp_path, monkeypatch, {}), "swancloud")
        assert crew.main_sessions(p) == [("swancloud-1", ("design", "planner", "ops", "operator"))]

    def test_a_role_that_runs_as_its_kind_stands_in_no_session_though_its_session_is_still_one(self, tmp_path, monkeypatch):
        """main-level, Two roles run as their kinds: no tab and no start for the planner; the session it was named
        stays one of the main level's, so a standing agent of it left there is ended (design Decision 14)."""
        fleet = self.load(tmp_path, monkeypatch, {"planner": {"session": "swancloud-2"}})
        p = dict(crew.drive_of(fleet, "swancloud"))
        p["flume"] = dict(p["flume"], planner="swancloud-main", ops="swancloud-main")
        assert crew.main_sessions(p) == [("swancloud-1", ("design", "operator")), ("swancloud-2", ())]

    NOW = plan.utc("2026-10-31T12:30:00Z")
    WAITING = [{"Ask": "3", "At": "2026-10-31T12:16:00Z"}, {"Ask": "5", "At": "2026-10-31T12:29:00Z"}]

    @pytest.mark.parametrize("run, said", [
        ({"live": False, "place": None, "words": None, "why": None}, "no run stands"),
        ({"live": False, "place": "/flume/places/crew-planner--madswan", "words": "flume refused: no stream madswan-main", "why": None},
         "no run stands (the runner could not launch its last: flume refused: no stream madswan-main)"),
        ({"live": True, "place": "/flume/places/crew-planner--madswan", "words": None, "why": None},
         "a run stands, the place /flume/places/crew-planner--madswan"),
        ({"live": None, "place": None, "words": None, "why": "no runner answers on mac-studio: madswan/runner/mac-studio does not exist"},
         "crew can't tell whether a run stands: no runner answers on mac-studio: madswan/runner/mac-studio does not exist")])
    def test_main_status_says_a_role_runs_as_its_kind_whether_a_run_stands_and_how_many_asks_wait(self, run, said):
        """main-level, Main status: the planner runs as its kind, its run as the runner's records show it, and two asks
        wait, with the oldest's age (design Decision 14; plan.kind_said)."""
        assert plan.kind_said("madswan-main", self.WAITING, run, self.NOW) == \
            f"runs as its kind in stream madswan-main; {said}; 2 asks wait, the oldest asked 14m ago"
        assert plan.kind_said("madswan-main", self.WAITING[1:], run, self.NOW).endswith("; 1 ask waits, the oldest asked 1m ago")
        assert plan.kind_said("madswan-main", [], run, self.NOW).endswith("; no ask waits")

    @pytest.mark.parametrize("roles, said", [
        ({"planner": {"session": ""}}, "roles.planner.session must name a session of the main level's machine"),
        ({"planner": {"seat": "x"}}, "roles.planner sets only 'model', 'effort' or 'session'")])
    def test_a_session_named_as_nothing_or_a_setting_crew_has_no_place_for_is_refused(self, tmp_path, monkeypatch, roles, said):
        with pytest.raises(crew.Refusal, match=said):
            self.load(tmp_path, monkeypatch, roles)

    def test_a_brief_names_where_each_main_level_role_runs_and_on_which_account(self, tmp_path, monkeypatch):
        import plan
        fleet = self.load(tmp_path, monkeypatch, {"planner": {"session": "swancloud-2"}})
        monkeypatch.setattr(crew, "this_host", lambda: "deneb")
        monkeypatch.setattr(plan, "kits_read", lambda fleet, label, fresh=True: ["crew", "agentplot/weir"])
        tok = crew.main_tokens(fleet, crew.drive_of(fleet, "swancloud"), "planner", "")
        assert tok["KIT_CHECKOUTS"] == "`/deneb/madswan/crew/main` (its folder `/deneb/madswan/crew`)"
        assert tok["CHECKOUT"] == "/deneb/madswan/blueprints/main" and tok["FOLDER"] == "/deneb/madswan/blueprints"
        assert (tok["SWANCLOUD_CHECKOUT"], tok["SWANCLOUD_FOLDER"]) == ("swancloud's checkout, which deneb does not keep",
                                                                       "its folder, which deneb does not keep")
        # the drive's kits, the repositories its plan and its landings name (Decision 3 of the-team-machinery-leaves),
        # and on its cards those its main level's host keeps, by forge address
        assert tok["KITS"] == "crew, weir" and tok["CARDS"].endswith("The kits: crew: afterthought/crew.")
        assert tok["MAIN_SESSIONS"] == (
            "`swancloud-design` in session swancloud-1 (account madswan); `swancloud-planner` in session swancloud-2 "
            "(account madswan-2); `swancloud-ops` in session swancloud-1 (account madswan); `swancloud-operator` in session "
            "swancloud-1 (account madswan); `swancloud-reviewer` in session swancloud-2 (account madswan-2)")
        assert tok["MAIN_SESSIONS"] in tok["ROSTER"] and "OPERATORS" not in tok

    def test_a_brief_names_each_kept_repositorys_checkout_and_folder_as_the_hosts_teams_file_gives_them(self, tmp_path, monkeypatch):
        """main-level, The design brief on a runner host and The operator's swancloud on a runner host (Decision 7 of
        a-kept-repositorys-folder-is-the-runners-container): deneb's file names the blueprints, crew and swancloud at
        the runner's containers and views, and the tokens name them; the kits it names none of are in their drive's folder."""
        monkeypatch.setattr(crew, "this_host", lambda: "deneb")
        r, v = "/Users/chuck/.local/share/flywheel/repositories", "/Users/chuck/Code/boomdrive"
        named = {a: {"dir": f"{r}/{a}", "checkout": f"{v}/{a}"} for a in ("afterthought/blueprints", "afterthought/crew", "afterthought/swancloud")}
        part = {"state": "afterthought/crew-state", "review": {"every": 5, "hours": 4}, "flume": STANDING}
        teams = {"version": 6, "repositories": named, "hosts": dict(DENEB, **{BOX: HOSTS[BOX]}), "drives": [
            dict(part, label="swancloud", blueprints=["afterthought/blueprints"], machine="deneb", session="swancloud-1",
                 folder="/deneb/madswan", repos=["afterthought/blueprints", "afterthought/crew", "agentplot/weir"],
                 accounts=every("madswan")),
            dict(part, label="wldn", blueprints=["WilldanGroup/willdan-blueprints"], machine=BOX, session="wldn-3",
                 folder="/box/willdan", repos=["WilldanGroup/willdan-blueprints"], accounts=every("ia"))]}
        fleet = loaded(tmp_path, monkeypatch, teams)
        monkeypatch.setattr(plan, "kits_read", lambda fleet, label, fresh=True: ["crew", "agentplot/weir"])
        tok = crew.main_tokens(fleet, crew.drive_of(fleet, "swancloud"), "design", "")
        assert (tok["CHECKOUT"], tok["FOLDER"]) == (f"{v}/afterthought/blueprints", f"{r}/afterthought/blueprints")
        assert tok["KIT_CHECKOUTS"] == (f"`{v}/afterthought/crew` (its folder `{r}/afterthought/crew`; the runner's clone, which "
                                        "only the runner fetches), "
                                        "`/deneb/madswan/weir/main` (its folder `/deneb/madswan/weir`)")
        assert (tok["SWANCLOUD_CHECKOUT"], tok["SWANCLOUD_FOLDER"]) == (f"{v}/afterthought/swancloud", f"{r}/afterthought/swancloud")
        assert tok["TEAMS_DOORS"] == "`swancloud`"
        # drive-state "crew fetches nothing in the runner's clone": the runner's repositories named, no fetch or pull there
        assert tok["FETCHING"].startswith("On deneb the runner keeps afterthought/blueprints and afterthought/crew: each is "
                                          "the runner's clone, which the runner alone fetches")
        assert tok["BLUEPRINTS_COMMIT"].startswith("Until then, its checkout on this host is the runner's view")
        assert tok["SWANCLOUD_FETCH"].startswith("as the runner last fetched it, with no fetch of your own")
        # main-level, A box's operator: the box keeps no swancloud, and its tokens say so in words (teams.10)
        tok = crew.main_tokens(fleet, crew.drive_of(fleet, "wldn"), "operator", "")
        assert (tok["SWANCLOUD_CHECKOUT"], tok["SWANCLOUD_FOLDER"]) == (f"swancloud's checkout, which {BOX} does not keep",
                                                                       f"its folder, which {BOX} does not keep")
        assert tok["KIT_CHECKOUTS"] == "none on this host"
        assert (tok["CHECKOUT"], tok["FOLDER"]) == ("/box/willdan/willdan-blueprints/main", "/box/willdan/willdan-blueprints")
        assert tok["FETCHING"] == f"No checkout on {BOX} is a runner's clone, so you fetch from GitHub where this brief says."
        assert "git pull --rebase" in tok["BLUEPRINTS_COMMIT"]
        assert tok["SWANCLOUD_FETCH"] == "`git -C {{SWANCLOUD_CHECKOUT}} fetch -q origin`, then "

    @pytest.mark.parametrize("role", ["dispatcher", "conductor", "coder"])
    def test_a_role_with_no_definition_is_refused_a_dispatcher_among_them(self, tmp_path, monkeypatch, role):
        """agent-models, A dispatcher's override: no drive role crew has no definition for, a team's least of all."""
        with pytest.raises(crew.Refusal, match=f"drive swancloud in .*teams.json overrides role '{role}', which it has no "
                                               "definition for. roles: design planner main-ops operator reviewer"):
            self.load(tmp_path, monkeypatch, {role: {"effort": "high"}})

    def test_a_brief_built_on_a_host_the_file_names_no_kind_for_is_refused(self, tmp_path, monkeypatch):
        """teams.10: whether the host crew runs on is a Mac is read from `hosts`; a host it does not name gives no token."""
        import plan
        fleet = self.load(tmp_path, monkeypatch, {})
        monkeypatch.setattr(crew, "this_host", lambda: "macbook-pro")
        monkeypatch.setattr(plan, "kits_read", lambda fleet, label, fresh=True: [])
        with pytest.raises(crew.Refusal, match="macbook-pro is no host .*teams.json's 'hosts' names, so crew can't tell whether "
                                               "it is a Mac for swancloud's brief"):
            crew.main_tokens(fleet, crew.drive_of(fleet, "swancloud"), "planner", "")
        monkeypatch.setattr(crew, "this_host", lambda: "deneb")
        assert crew.main_tokens(fleet, crew.drive_of(fleet, "swancloud"), "planner", "")["SHOWING"].startswith("deneb is a Mac")


class TestMoved:
    """A state folder's panes recorded in another session than its agents run in now name nothing there, so crew sets
    them aside rather than taking another agent at the same pane id for its own (teams.2; deneb, 2026-10-20: a stale
    swancloud-main panes file made crew main up take crw-5's agents for the design agent and planner)."""

    def test_a_folder_that_names_another_session_is_said_and_one_that_names_this_or_none_is_not(self):
        assert crew.moved_said("swancloud", "swancloud-2", "swancloud-1") == (
            "swancloud's panes were recorded in session swancloud-2, and it runs in swancloud-1 now; their ids name nothing here")
        assert crew.moved_said("swancloud", "swancloud-1", "swancloud-1") is None
        assert crew.moved_said("swancloud", "", "swancloud-1") is None


class TestGreetWaits:
    def look(self, status, asking=False, asked=False, out_of_time=False):
        return crew.greet_waits("wldn-planner", status, asking, asked, out_of_time, "crew main up wldn starts and greets it", "Read where wldn stands.")

    @pytest.mark.parametrize("status", ["idle", "done"])
    def test_an_agent_settled_with_no_question_is_greeted(self, status):
        assert self.look(status) == ("greet", None)

    def test_one_waiting_on_a_question_is_said_once_and_given_five_minutes(self):
        assert self.look("blocked", asking=True) == ("asking", "wldn-planner is waiting on a question in its pane; answer it there and it will be greeted")
        assert self.look("blocked", asking=True, asked=True) == (None, None)

    def test_one_never_ready_is_said_with_the_tell_that_would_greet_it_and_one_not_up_with_its_hint(self):
        assert self.look("working", out_of_time=True) == ("gave up", "wldn-planner was not ready to greet; once it is: crew tell wldn-planner 'Read where wldn stands.'")
        assert self.look(None, out_of_time=True) == ("gave up", "wldn-planner is not up: crew main up wldn starts and greets it")

    def test_else_it_looks_again(self):
        assert self.look("working") == (None, None)


class TestStandingGreeting:
    @pytest.mark.parametrize("name, says", [
        ("wldn-design", "curate the signals that have no move"), ("wldn-planner", "crew plan proposed"),
        ("wldn-ops", "land nothing until it comes"), ("wldn-operator", "what is moving and what waits on me")])
    def test_each_role_has_its_greeting(self, name, says):
        label, text, why, hint = crew.standing_greeting(FLEET, name)
        assert label == "wldn" and says in text

    def test_its_entry_and_its_hint_name_the_main_level_the_operators_among_it(self):
        assert crew.standing_greeting(FLEET, "wldn-design")[2:] == ("main(wldn): greet wldn-design", "crew main up wldn starts and greets it")
        assert crew.standing_greeting(FLEET, "wldn-operator")[2:] == (
            "main(wldn): greet wldn-operator", "crew main up wldn starts and greets it")

    @pytest.mark.parametrize("name, said", [
        ("swb-1-ops", "no agent swb-1-ops: crew starts none by that name"),
        ("wldn-reviewer", "wldn-reviewer is sent its batch as its prompt by crew review, and is not greeted"),
        ("nobody", "no agent nobody: crew starts none by that name")])
    def test_a_teams_agent_the_reviewer_and_an_unknown_name_are_refused(self, name, said):
        with pytest.raises(crew.Refusal, match=said):
            crew.standing_greeting(FLEET, name)


class TestPlaces:
    @pytest.mark.parametrize("name", ["swb-1-conductor", "swb-1-ops", "swb-1-unit-2"])
    def test_a_teams_agent_is_no_agent_crew_starts_so_a_tell_to_it_is_refused(self, name):
        """the-team-machinery-leaves Decision 10; main-level "Any agent crew starts is reached by name": crew tell finds
        a main level's agents alone, and a team's old name is no agent's."""
        with pytest.raises(crew.Refusal, match=f"no agent {name}: crew starts none by that name"):
            crew.place_of_agent(FLEET, name)
        assert crew.label_of_agent(FLEET, name) is None

    def test_an_operator_runs_in_the_folder_the_hosts_consoles_give_its_drive(self, monkeypatch):
        """operator-agent, A console the host names and A console the host does not name: the folder this host's
        `consoles` gives the drive; a drive it names no console of is refused, naming it, the host and `consoles`, and
        so is a label no drive has."""
        monkeypatch.setattr(crew, "this_host", lambda: "deneb")
        assert crew.operator_session(FLEET, "wldn", "deneb") == "/w/willdan"
        with pytest.raises(crew.Refusal, match=f"{BOX}'s teams file names no console of wldn in 'consoles', so no console of wldn opens here"):
            crew.operator_session(FLEET, "wldn", BOX)
        fleet = dict(FLEET, drives=dict(FLEET["drives"], madswan={"label": "madswan"}))
        with pytest.raises(crew.Refusal, match="deneb's teams file names no console of madswan in 'consoles'"):
            crew.operator_session(fleet, "madswan", "deneb")
        with pytest.raises(crew.Refusal, match="no drive 'madswan'. drives: wldn"):
            crew.operator_session(FLEET, "madswan", "deneb")


# herdr 0.9.3's pane process-info on mac-studio, 2026-10-18: swancloud's rail tab (w2:pF) as herdr brought it back after
# the host's restart of 2026-10-15, its shell alone, the loop that wrote the agents' views gone with the restart.
RESTORED = {"foreground_process_group_id": 2301, "pane_id": "w2:pF", "shell_pid": 2301,
            "foreground_processes": [{"argv": ["-zsh"], "argv0": "zsh", "cmdline": "-zsh", "cwd": "/Users/chuck", "name": "zsh", "pid": 2301}]}


def running(*argvs):
    return {"foreground_process_group_id": 9001, "pane_id": "w2:pF", "shell_pid": 2301,
            "foreground_processes": [{"argv": list(a), "pid": 9001 + i} for i, a in enumerate(argvs)]}


class TestOperatorTabs:
    """What crew console up finds in a tab's pane it opened before (crew.tab_holds, code.7): its loop running, the
    shell alone a restart left, which runs the loop again, or something else, which crew leaves (read.4)."""

    def test_a_pane_a_restart_left_holds_its_shell_alone_and_its_loop_runs_again(self):
        assert crew.tab_holds(RESTORED, ["_rail", "swancloud"]) == ("shell", None)

    def test_a_tabs_loop_runs_when_a_foreground_process_ends_with_its_words_and_the_bash_its_crew_execs_keeps_them(self):
        rail = running(["bash", "/c/plugin/bin/crew", "_rail", "swancloud"], ["python3", "/c/plugin/lib/record.py", "events", "--follow", "--label", "swancloud"])
        assert crew.tab_holds(rail, ["_rail", "swancloud"]) == ("running", None)
        flow = running(["python3", "/c/plugin/bin/../lib/record.py", "events", "--follow", "--label", "swancloud"])
        assert crew.tab_holds(flow, ["events", "--follow", "--label", "swancloud"]) == ("running", None)

    def test_anything_else_in_the_foreground_is_left_and_named(self):
        assert crew.tab_holds(running(["less", "notes"]), ["_board", "swancloud"]) == ("other", "less notes")
        assert crew.tab_holds(running(["bash", "/c/plugin/bin/crew", "_rail", "wldn"]), ["_rail", "swancloud"]) == ("other", "bash /c/plugin/bin/crew _rail wldn")
        assert crew.tab_holds(running(), ["_board", "swancloud"]) == ("other", "process group 9001")

    @pytest.mark.parametrize("info", [None, {}, {"shell_pid": 1, "foreground_process_group_id": "1", "foreground_processes": []},
                                      {"shell_pid": 1, "foreground_process_group_id": 1}])
    def test_an_answer_crew_cant_read_is_said_and_runs_nothing(self, info):
        assert crew.tab_holds(info, ["_rail", "swancloud"]) == (None, "herdr's process-info for it can't be read")


# herdr 0.9.3's pane list of swancloud's session on mac-studio, 2026-10-19: crw-3's w10:p6, which herdr could not bring
# back at its restart, its folder a worktree since removed, and crw-1's conductor pane, brought back with its shell.
DEAD = {"agent_status": "unknown", "cwd": "/c/crew.git/wt/trash/the-board-is-a-page-1791745030", "focused": False,
        "pane_id": "w10:p6", "restore_error": "Saved directory is unavailable. Restore the directory and restart this session.",
        "revision": 0, "tab_id": "w10:t1", "terminal_id": "term_65e35acc23da81a", "workspace_id": "w10"}
BACK = {"agent_status": "unknown", "cwd": "/c/bolts/curation-and-holds", "focused": False, "foreground_cwd": "/c/bolts/curation-and-holds",
        "pane_id": "w3:p1", "revision": 0, "scroll": {"max_offset_from_bottom": 0, "offset_from_bottom": 0, "viewport_rows": 77},
        "tab_id": "w3:t1", "terminal_id": "term_65e35acc0e86bf", "workspace_id": "w3"}


class TestDeadPanes:
    """A pane crew keeps that herdr lists with no terminal behind it, as crw-2's were when crew up did not bring its
    conductor back at test D (2026-10-18), is dead (crew.dead_said, teams.2); one an agent holds never is (read.4); and a
    pane not there opens again beside its tab's other pane, else in its workspace while that stands (crew.opens_at);
    crew revive opens again a pane brought back dead and picks up one brought back empty (crew.revived). Closing and
    opening them through crew up is the teams journey's, through crew revive and crew main up the main journey's."""

    def test_a_pane_herdr_could_not_bring_back_is_dead_said_with_its_folder_and_herdrs_words(self):
        assert crew.dead_said("crw-3", "conductor", DEAD, None) == (
            "crw-3's conductor pane w10:p6 is dead: herdr could not bring it back in /c/crew.git/wt/trash/the-board-is-a-page-1791745030 "
            "(Saved directory is unavailable. Restore the directory and restart this session.)")
        assert crew.dead_said("crw-3", "ops", {k: v for k, v in DEAD.items() if k != "cwd"}, None) == (
            "crw-3's ops pane w10:p6 is dead: herdr could not bring it back (Saved directory is unavailable. Restore the directory and "
            "restart this session.)")

    def test_a_pane_brought_back_with_its_shell_or_not_listed_is_not_dead(self):
        assert crew.dead_said("crw-1", "conductor", BACK, None) is None
        assert crew.dead_said("crw-1", "conductor", None, None) is None

    @pytest.mark.parametrize("status", ["idle", "working", "blocked", "done"])
    def test_a_pane_an_agent_holds_is_never_dead(self, status):
        assert crew.dead_said("crw-3", "conductor", DEAD, status) is None

    @pytest.mark.parametrize("err", ["", "  ", None, 1, ["Saved directory is unavailable."]])
    def test_a_restore_error_with_no_words_is_not_read_as_one(self, err):
        assert crew.dead_said("crw-3", "conductor", dict(DEAD, restore_error=err), None) is None

    def test_revive_opens_again_a_pane_brought_back_dead_and_picks_up_one_brought_back_empty(self):
        assert crew.revived(DEAD, None) == "dead"
        assert crew.revived(BACK, None) == "empty"

    @pytest.mark.parametrize("item, status", [(BACK, "idle"), (DEAD, "working"), (None, None)])
    def test_revive_leaves_a_pane_an_agent_holds_and_one_herdr_does_not_list(self, item, status):
        assert crew.revived(item, status) is None

    def test_a_pane_opens_beside_its_tabs_other_pane_else_in_its_workspace_while_it_stands_else_in_a_new_one(self):
        assert crew.opens_at("w2X:p2", "w2X") == ("split", "w2X:p2")
        assert crew.opens_at("", "w2X") == ("tab", "w2X")
        assert crew.opens_at("", "") == ("workspace", None)


class TestResume:
    @pytest.fixture
    def home(self, tmp_path, monkeypatch):
        monkeypatch.setenv("HOME", str(tmp_path))
        monkeypatch.setattr(crew, "SESSIONS", tmp_path / ".local/state/crew/sessions")
        crew.SESSIONS.mkdir(parents=True)
        return tmp_path

    def session(self, home, sid, agent, cwd=None, spoken=True, mtime=0, began=None):
        (crew.SESSIONS / sid).write_text(f"CREW_AGENT={agent}\nCREW_LABEL=wldn\n" + (f"CREW_CWD={cwd}\n" if cwd else ""))
        os.utime(crew.SESSIONS / sid, (mtime, mtime))
        if spoken:
            d = home / ".claude/projects/-work"
            d.mkdir(parents=True, exist_ok=True)
            (d / f"{sid}.jsonl").write_text(json.dumps({"type": "user", "cwd": began or cwd}) + "\n")

    def test_a_role_resumes_its_last_conversation_in_the_folder_it_began_in(self, home):
        (home / "kit").mkdir(); (home / "bolt").mkdir()
        self.session(home, "s1", "swb-1-conductor", str(home / "kit"), mtime=1)
        assert crew.last_conversation("swb-1-conductor") == ("s1", str(home / "kit"))
        self.session(home, "s2", "swb-1-conductor", str(home / "bolt"), mtime=2)
        assert crew.last_conversation("swb-1-conductor") == ("s2", str(home / "bolt"))

    def test_a_last_session_never_spoken_to_starts_fresh_not_the_one_before(self, home):
        (home / "kit").mkdir()
        self.session(home, "s1", "swb-1-conductor", str(home / "kit"), mtime=1)
        self.session(home, "s2", "swb-1-conductor", str(home / "kit"), spoken=False, mtime=2)
        assert crew.last_conversation("swb-1-conductor") is None

    def test_a_record_kept_before_the_folder_was_is_read_from_its_transcript(self, home):
        (home / "kit").mkdir()
        self.session(home, "old", "swb-1-ops", None, began=str(home / "kit"), mtime=1)
        assert crew.last_conversation("swb-1-ops") == ("old", str(home / "kit"))

    def test_a_folder_gone_is_not_resumed(self, home):
        self.session(home, "s1", "swb-1-ops", str(home / "gone"), mtime=1)
        assert crew.last_conversation("swb-1-ops") is None


class TestBriefBack:
    SAVED = {"CREW_AGENT": "wldn-planner", "CREW_LABEL": "wldn", "CREW_CWD": "/blueprints", "CREW_ROLE": "planner"}

    def test_a_compaction_of_a_session_herdr_resumed_gives_its_agents_brief_back(self):
        assert crew.brief_due("compact", False, self.SAVED) == "wldn-planner"

    @pytest.mark.parametrize("source", ["resume", "startup", "clear", "fork", None])
    def test_any_other_start_gives_none_a_resume_keeping_the_brief_in_its_transcript(self, source):
        assert crew.brief_due(source, False, self.SAVED) is None

    def test_a_session_crew_role_started_carries_its_brief_through_a_compaction_and_is_given_none(self):
        assert crew.brief_due("compact", True, self.SAVED) is None

    @pytest.mark.parametrize("saved", [{}, {"CREW_AGENT": ""}, {"CREW_LABEL": "wldn"}])
    def test_a_session_no_crew_agent_is_recorded_for_is_given_none(self, saved):
        assert crew.brief_due("compact", False, saved) is None

    @pytest.mark.parametrize("name, recorded, found", [
        ("wldn-planner", "planner", ("wldn", "planner")), ("wldn-ops", "main-ops", ("wldn", "main-ops"))])
    def test_the_brief_is_built_from_the_definition_crew_role_recorded(self, name, recorded, found):
        assert crew.brief_role(FLEET, name, recorded) == found

    @pytest.mark.parametrize("name, found", [
        ("wldn-design", ("wldn", "design")), ("wldn-planner", ("wldn", "planner")), ("wldn-ops", ("wldn", "main-ops")),
        ("wldn-reviewer", ("wldn", "reviewer")), ("wldn-operator", ("wldn", "operator"))])
    def test_a_session_recorded_before_crew_role_named_its_definition_is_given_the_one_its_name_gives(self, name, found):
        assert crew.brief_role(FLEET, name, "") == found
        assert crew.brief_role(FLEET, name, None) == found

    def test_a_dispatchers_name_is_no_agent_crew_starts(self):
        """main-level delta: no dispatcher is started, placed or named, so its name gives no brief."""
        with pytest.raises(crew.Refusal, match="no agent wldn-dispatch-chuck-herdr-alpha: crew starts none by that name"):
            crew.brief_role(FLEET, "wldn-dispatch-chuck-herdr-alpha", None)

    @pytest.mark.parametrize("name", ["swb-1-conductor", "swb-1-ops", "swb-1-unit-2"])
    def test_a_teams_agents_name_is_no_agent_crew_starts(self, name):
        """the-team-machinery-leaves Decision 10: crew starts no team's conductor, ops or slot, so a session recorded
        as one is given no brief."""
        with pytest.raises(crew.Refusal, match=f"no agent {name}: crew starts none by that name"):
            crew.brief_role(FLEET, name, "conductor")

    def test_a_name_crew_starts_no_agent_by_is_refused(self):
        with pytest.raises(crew.Refusal, match="no agent swb-9-conductor"):
            crew.brief_role(FLEET, "swb-9-conductor", "conductor")

    def test_the_brief_comes_back_whole_behind_a_line_saying_what_it_is_and_to_read_a_file_it_is_cut_to(self):
        said = crew.brief_back_said("wldn-planner", "You are wldn's planner.\n\nPlan the drive's bolts.")
        first, rest = said.split("\n\n", 1)
        assert first.startswith("[crew] This is your brief as wldn-planner") and "read that file whole now" in first
        assert rest == "You are wldn's planner.\n\nPlan the drive's bolts."


class TestIdentityOnItsHost:
    """A main level's agent herdr resumed gets its identity back only on its main level's host (main-level)."""

    @pytest.mark.parametrize("name, role", [("wldn-design", "design"), ("wldn-planner", "planner"), ("wldn-ops", "ops"),
                                            ("wldn-operator", "operator"), ("wldn-reviewer", "reviewer")])
    def test_a_main_levels_agent_is_told_from_its_record_alone(self, name, role):
        assert crew.main_named(name, "wldn") == role

    @pytest.mark.parametrize("name, label", [("swb-1-conductor", "wldn"), ("wldn-dispatch-chuck-herdr-alpha", "wldn"),
                                             ("madswan-planner", "wldn"), ("wldn-planner", ""), ("wldn-planner", None),
                                             ("", "wldn")])
    def test_a_teams_agent_a_dispatcher_another_drives_or_an_unlabelled_record_is_none(self, name, label):
        assert crew.main_named(name, label) is None

    def test_on_its_main_levels_host_nothing_is_withheld(self):
        assert crew.identity_withheld("wldn-planner", "wldn", BOX, BOX) is None

    def test_on_another_host_it_is_told_where_the_main_level_runs_and_that_it_is_no_agent_of_crews(self):
        said = crew.identity_withheld("wldn-planner", "wldn", "mac-studio", BOX)
        assert said.startswith("[crew] This session was wldn-planner, and crew gives it no identity here: ")
        assert crew.main_elsewhere_said("wldn-planner", "wldn", BOX, "mac-studio") in said
        assert "wldn's main level runs on chuck-herdr-alpha, not mac-studio, and crew starts wldn-planner only there" in said
        assert "no agent of crew's" in said and "run no crew command" in said and "wait for the user" in said

    def test_a_teams_file_crew_cant_read_withholds_it_and_says_why(self):
        said = crew.identity_withheld("wldn-planner", "wldn", BOX, None, unread="/h/.config/crew/teams.json is missing; the machine's configuration writes it")
        assert said.startswith("[crew] This session was wldn-planner, and crew gives it no identity here: it can't tell "
                               "where wldn's main level runs, /h/.config/crew/teams.json is missing; the machine's configuration writes it. ")
        assert "no agent of crew's" in said
        said = crew.identity_withheld("wldn-planner", "wldn", BOX, BOX, unread="crew has done nothing.")
        assert "runs, crew has done nothing. In this session" in said


def test_a_drive_crew_does_not_know_is_refused():
    with pytest.raises(crew.Refusal, match="no drive 'nope'. drives: wldn"):
        crew.drive_of(FLEET, "nope")


def test_a_greeting_never_taken_says_the_tell_that_would_send_it_once_the_agent_is_ready():
    again = "once it is ready: crew tell wldn-design 'Read where wldn stands.'"
    assert crew.untaken_said("wldn-design", "its greeting", "never", "sent twice", again) == (
        "wldn-design did not take its greeting, sent twice; nothing is left typed; " + again)
    assert crew.untaken_said("wldn-design", "its greeting", "unread", "it went to work") == (
        "crew could not tell whether wldn-design took its greeting: it went to work; nothing more was sent")
