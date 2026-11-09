"""crew reads the teams file its flake's module writes (the crew-flake spec; record 0058, flake.3): the module's file
for deneb's drives, pinned byte for byte as nix/tests/files/deneb.json, and with deneb's kept repositories as
nix/tests/files/runner.json (record 0061), which the project nix's test holds the module to, each loaded by crew.load
as its teams file with no hosts file, since the file gives every fact crew reads of the hosts (record 0064)."""
import pathlib
import shutil

import crew

FILES = pathlib.Path(__file__).resolve().parents[2] / "nix/tests/files"
PINNED = FILES / "deneb.json"
DENEB, BOX = "deneb", "chuck-herdr-alpha"
AFTERTHOUGHT, AGENTPLOT = "/Users/chuck/Code/github_afterthought", "/Users/chuck/Code/github_agentplot"


def loaded(tmp_path, monkeypatch, pinned):
    """crew.load over the pinned file as its teams file, and no other file."""
    shutil.copyfile(pinned, tmp_path / "teams.json")
    monkeypatch.setattr(crew, "TEAMS", tmp_path / "teams.json")
    crew.load.cache_clear()
    try:
        return crew.load()
    finally:
        crew.load.cache_clear()


def test_crew_reads_the_file_the_module_writes(tmp_path, monkeypatch):
    """crew-flake, crew reads the file the module writes: four drives, wldn's planner and reviewer in wldn-1 on account
    ia and its other roles on willdan-alex, every role of every drive standing, and the four consoles on deneb."""
    fleet = loaded(tmp_path, monkeypatch, PINNED)
    assert fleet["repositories"] == {}
    assert fleet["hosts"] == {DENEB: {"ssh": DENEB, "kind": "darwin"}, BOX: {"ssh": BOX, "kind": "nixos"}}
    parts = fleet["drives"]
    assert list(parts) == ["afterthought", "agentplot", "madswan", "wldn"]
    wldn = parts["wldn"]
    assert wldn["sessions"] == {"design": "wldn-2", "planner": "wldn-1", "ops": "wldn-2", "operator": "wldn-2", "reviewer": "wldn-1"}
    assert wldn["accounts"] == {"design": "willdan-alex", "planner": "ia", "reviewer": "ia", "ops": "willdan-alex",
                                "operator": "willdan-alex"}
    assert (wldn["folder"], wldn["checkout"]) == ("/workspace", "/workspace/willdan-blueprints/main")
    for label, p in parts.items():
        assert all(p["flume"][role] is False for role in crew.KIND_ROLES), f"{label}'s roles do not all stand: {p['flume']}"
    assert parts["madswan"]["checkout"] == f"{AFTERTHOUGHT}/blueprints/main"
    assert len(parts["agentplot"]["repos"]) == 24
    assert fleet["consoles"] == {"afterthought": AFTERTHOUGHT, "agentplot": AGENTPLOT, "madswan": AFTERTHOUGHT,
                                 "wldn": "/Users/chuck/Code/clients/github_willdan"}
    monkeypatch.setattr(crew, "this_host", lambda: DENEB)
    assert [crew.operator_session(fleet, l, DENEB) for l in parts] == [AFTERTHOUGHT, AGENTPLOT, AFTERTHOUGHT,
                                                                       "/Users/chuck/Code/clients/github_willdan"]
    assert crew.kit_kept(fleet, BOX, "crew")["main"] == "/workspace/crew/main"


def test_crew_reads_the_kept_repositories_the_module_writes(tmp_path, monkeypatch):
    """crew-flake, crew reads the kept repositories the module writes: on deneb, crew's and swancloud's folder and
    checkout are the file's, whether or not a drive lists them; the box's are wldn's folder's still."""
    monkeypatch.setattr(crew, "this_host", lambda: DENEB)
    fleet = loaded(tmp_path, monkeypatch, FILES / "runner.json")
    assert list(fleet["drives"]) == ["afterthought", "agentplot", "madswan", "wldn"]
    r, v = "/Users/chuck/.local/share/flywheel/repositories", "/Users/chuck/Code/boomdrive"
    assert crew.kit_kept(fleet, DENEB, "crew") == {"name": "crew", "repo": "agentplot/crew", "dir": f"{r}/agentplot/crew",
                                                   "main": f"{v}/agentplot/crew"}
    assert crew.kit_kept(fleet, DENEB, "afterthought/swancloud") == {
        "name": "swancloud", "repo": "afterthought/swancloud", "dir": f"{r}/afterthought/swancloud", "main": f"{v}/afterthought/swancloud"}
    assert crew.kit_kept(fleet, BOX, "crew")["main"] == "/workspace/crew/main"
    assert fleet["drives"]["madswan"]["checkout"] == f"{AFTERTHOUGHT}/blueprints/main"
