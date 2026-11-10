"""crew run on another host is the crew that host installed (code.3, read.1): `crew` by its name, found on the host's
login path over ssh to the `ssh` name the teams file's `hosts` gives it, as the one asking, behind a guard that names a
host whose path finds none (crew_there, NO_CREW). crew looks for no checkout there and reads no address of its own to
find one, and a host the file gives no ssh name is refused with no ssh run. The reading, 2026-11-10: on the box, crew
0.41.11 at 13:57 refused a send to deneb's operator, "none of deneb's sessions keeps afterthought/crew", and on deneb
the teams file names no checkout of crew on chuck-herdr-alpha, so a send to wldn's operator was refused the same way;
each host has crew installed on its login path, `/etc/profiles/per-user/chuck/bin/crew`, which the other finds by ssh."""
import json
import pathlib
import re
import shlex
import types

import pytest

import crew
import record

ROOT = pathlib.Path(__file__).resolve().parents[2]
BOX = "chuck-herdr-alpha"
MANIFEST = ROOT / "plugin/.claude-plugin/plugin.json"


def fleet(*repos):
    """deneb's teams file with wldn on the box, its folder /workspace keeping repos there, as the hosts file had its
    sessions on 2026-11-07; the box reached as `box`."""
    wldn = {"label": "wldn", "machine": BOX, "session": "wldn-2", "folder": "/workspace", "repos": list(repos)}
    return {"hosts": {BOX: {"ssh": "box", "kind": "nixos"}, "deneb": {"ssh": "deneb", "kind": "darwin"}},
            "drives": {"wldn": wldn, "agentplot": {"label": "agentplot", "machine": "deneb", "folder": "/d", "repos": []}}}


KEPT = fleet("agentplot/crew", "WilldanGroup/atlas-kit", "WilldanGroup/willdan-blueprints")
NONE_KEPT = fleet("WilldanGroup/atlas-kit")


@pytest.fixture
def deneb(monkeypatch):
    """A command on deneb, asked by swancloud-planner of drive swancloud in Claude session deneb:s1."""
    monkeypatch.setattr(crew, "this_host", lambda: "deneb")
    monkeypatch.setenv("CREW_AGENT", "swancloud-planner")
    monkeypatch.setenv("CREW_LABEL", "swancloud")
    monkeypatch.setattr(record, "_session", "deneb:s1")


@pytest.fixture
def no_manifest(monkeypatch):
    """crew's manifest read by nothing: a read of it fails the case."""
    read = pathlib.Path.read_text

    def guarded(self, *a, **kw):
        if self.name == "plugin.json":
            pytest.fail(f"crew read its manifest {self}")
        return read(self, *a, **kw)
    monkeypatch.setattr(pathlib.Path, "read_text", guarded)


class TestCrewThere:
    def test_the_line_runs_crew_by_its_name_behind_the_guard_as_the_one_asking(self):
        """crew-command, A command forwarded to a main level's host."""
        assert crew.crew_there(BOX, "swancloud-planner", "wldn", "deneb:s1", ["main", "status", "wldn"]) == [
            "sh", "-c", crew.NO_CREW, BOX, "env", "CREW_AGENT=swancloud-planner", "CREW_LABEL=wldn",
            "CREW_SESSION=deneb:s1", "crew", "main", "status", "wldn"]

    def test_the_guard_names_the_host_by_its_first_argument_and_runs_the_rest(self):
        assert crew.NO_CREW == ("command -v crew >/dev/null 2>&1 || { printf '%s\\n' \"$0 has no crew on its login path, so "
                                "crew can't run there\" >&2; exit 127; }; exec \"$@\"")


class TestCrewArgv:
    @pytest.mark.parametrize("kept", [KEPT, NONE_KEPT], ids=["crew-in-repos", "crew-in-no-repos"])
    def test_another_host_runs_the_crew_it_installed_whatever_the_file_keeps_of_crew_there(self, deneb, no_manifest, kept):
        """crew-command, A send reaches another host's drive whatever the teams file keeps of crew there."""
        argv = crew.crew_argv(kept, BOX, "x")
        assert argv == crew.crew_there(BOX, "swancloud-planner", "swancloud", "deneb:s1", ("x",))
        assert argv[-2:] == ["crew", "x"]
        assert not [a for a in argv if "plugin/bin/crew" in a or "/workspace" in a]

    def test_this_host_runs_the_crew_this_host_installed(self, deneb, monkeypatch):
        monkeypatch.setattr(crew, "crew_command", lambda: "/etc/profiles/per-user/chuck/bin/crew")
        assert crew.crew_argv(KEPT, "deneb", "bolts") == [
            "env", "CREW_AGENT=swancloud-planner", "CREW_LABEL=swancloud", "CREW_SESSION=deneb:s1", "bash",
            "/etc/profiles/per-user/chuck/bin/crew", "bolts"]

    def test_reach_gives_bash_the_one_line_and_nothing_else(self, deneb, no_manifest):
        got = crew.reach(NONE_KEPT, BOX)
        assert list(got) == ["REMOTE_CREW"]
        assert shlex.split(got["REMOTE_CREW"]) == crew.crew_argv(NONE_KEPT, BOX)

    def test_reach_gives_nothing_for_this_host(self, deneb):
        assert crew.reach(KEPT, "deneb") == {}


class TestReadAgent:
    def test_an_agent_herdr_names_in_no_pane_is_asked_of_the_crew_the_host_installed(self, deneb, no_manifest, monkeypatch):
        """crew-command, A tell finds an agent herdr names in no pane through the crew installed there: one run on the
        box, herdr's agent get or else `crew _found`, and nothing refused before it for a host that keeps no crew."""
        ran = []
        a = {"pane_id": "w1:p1", "name": "wldn-planner", "agent_status": "idle"}

        def on_machine(fleet, host, argv, input=None):
            ran.append((host, argv))
            return types.SimpleNamespace(returncode=0, stdout=json.dumps({"result": {"agent": a}}), stderr="")
        monkeypatch.setattr(crew, "on_machine", on_machine)
        assert crew.read_agent(NONE_KEPT, "wldn-planner") == (a, None)
        [(host, argv)] = ran
        assert host == BOX and argv[:2] == ["sh", "-c"]
        get, found = argv[2].split(" || exec ", 1)
        assert get == "herdr --session wldn-2 agent get wldn-planner"
        assert shlex.split(found) == crew.crew_argv(NONE_KEPT, BOX, "_found", "wldn-planner")
        assert shlex.split(found)[-2:] == ["_found", "wldn-planner"]


def test_crews_code_writes_its_own_address_nowhere():
    """crew-command, crew's code names no address of its own: no module or command of crew's names the repository its
    manifest names."""
    m = re.fullmatch(r"(?:https://github\.com/|git@github\.com:)([\w.-]+)/([\w.-]+?)(?:\.git)?/?",
                     json.loads(MANIFEST.read_text())["repository"])
    own = f"{m[1]}/{m[2]}"
    named = re.compile(re.escape(own) + r"(?![\w-])")
    files = sorted((ROOT / "plugin/lib").glob("*.py")) + sorted(p for p in (ROOT / "plugin/bin").iterdir() if p.is_file())
    assert [str(p.relative_to(ROOT)) for p in files if named.search(p.read_text())] == []


class TestReach:
    """crew-command, A host the file gives no ssh name: crew reaches a host by the `ssh` name the teams file's `hosts`
    gives it, and refuses one it does not name before any ssh is run (crew.ssh_of, crew.on_machine, plan.forwarded,
    plan.opener, hold.fan)."""

    def test_a_host_is_reached_by_its_ssh_name(self, monkeypatch):
        import plan
        assert crew.ssh_of(KEPT, BOX) == "box"
        assert plan.opener(KEPT, BOX, "deneb", "/r/x.md") == "ssh -t box plannotator-tui " + shlex.quote(shlex.quote("/r/x.md"))
        ran = []
        monkeypatch.setattr(crew, "this_host", lambda: "deneb")
        monkeypatch.setattr(crew.subprocess, "run", lambda argv, **kw: ran.append(argv))
        crew.on_machine(KEPT, BOX, ["true"])
        assert ran == [["ssh", "-o", "BatchMode=yes", "box", "true"]]

    @pytest.mark.parametrize("act", ["ssh_of", "on_machine", "opener", "fan"])
    def test_a_host_the_file_does_not_name_is_refused_and_no_ssh_is_run(self, monkeypatch, act):
        import hold
        import plan
        ran = []
        monkeypatch.setattr(crew, "this_host", lambda: "deneb")
        monkeypatch.setattr(crew.subprocess, "run", lambda argv, **kw: ran.append(argv))
        monkeypatch.setattr(hold.subprocess, "Popen", lambda argv, **kw: ran.append(argv))
        monkeypatch.setattr(crew, "crew_argv", lambda fleet, host, *args: ["crew", *args])
        acts = {"ssh_of": lambda: crew.ssh_of(KEPT, "macbook-pro"),
                "on_machine": lambda: crew.on_machine(KEPT, "macbook-pro", ["true"]),
                "opener": lambda: plan.opener(KEPT, "macbook-pro", "deneb", "/r/x.md"),
                "fan": lambda: hold.fan(KEPT, ["macbook-pro"], "status")}
        with pytest.raises(crew.Refusal, match="^macbook-pro is no host .*teams.json's 'hosts' names, so crew can't reach it. "
                                               "hosts: chuck-herdr-alpha deneb$"):
            acts[act]()
        assert ran == []

    def test_forwarded_names_the_hosts_ssh_and_refuses_one_the_file_does_not_name(self, monkeypatch):
        import plan
        monkeypatch.setattr(crew, "this_host", lambda: "deneb")
        monkeypatch.setattr(crew, "reach", lambda fleet, machine: {})
        written = []
        monkeypatch.setattr(plan.os, "write", lambda fd, b: written.append((fd, b.decode())))
        with pytest.raises(plan.Stopped):
            plan.forwarded(KEPT, BOX)
        assert written == [(3, f"MACHINE={BOX}\nSSH_TARGET=box\n")]
        with pytest.raises(crew.Refusal, match="^macbook-pro is no host"):
            plan.forwarded(KEPT, "macbook-pro")
