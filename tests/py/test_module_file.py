"""crew reads the teams file its flake's module writes (the crew-flake spec; record 0058, flake.3): the module's file
for deneb's partitions, pinned byte for byte as nix/tests/files/deneb.json, and with deneb's kept repositories as
nix/tests/files/runner.json (record 0061), which the project nix's test holds the module to, each loaded by crew.load
as its teams file, beside a hosts file naming those sessions."""
import json
import pathlib
import shutil

import crew

FILES = pathlib.Path(__file__).resolve().parents[2] / "nix/tests/files"
PINNED = FILES / "deneb.json"
DENEB, BOX = "deneb", "chuck-herdr-alpha"


def hosts(tmp_path):
    """deneb's sessions afterthought, agentplot and madswan, in partitions personal, agentplot and business, and the
    box's wldn-1 and wldn-2 in clients/willdan, each space keeping its partition's first blueprints repository."""
    def sess(space, partition, repo):
        return {"dir": f"{tmp_path}/{space}", "partition": partition, "repos": [repo]}
    willdan = "WilldanGroup/willdan-blueprints"
    return {DENEB: {"ssh": DENEB, "sessions": {"afterthought": sess("afterthought", "personal", "afterthought/blueprints"),
                                               "agentplot": sess("agentplot", "agentplot", "agentplot/blueprints"),
                                               "madswan": sess("madswan", "business", "afterthought/blueprints")}},
            BOX: {"ssh": BOX, "sessions": {"wldn-1": sess("willdan-1", "clients/willdan", willdan),
                                           "wldn-2": sess("willdan-2", "clients/willdan", willdan)}}}


def loaded(tmp_path, monkeypatch, pinned):
    """crew.load over the pinned file as its teams file, beside the hosts file."""
    (tmp_path / "herdr-hosts.json").write_text(json.dumps({"version": 1, "hosts": hosts(tmp_path)}))
    shutil.copyfile(pinned, tmp_path / "teams.json")
    monkeypatch.setattr(crew, "HOSTS", tmp_path / "herdr-hosts.json")
    monkeypatch.setattr(crew, "TEAMS", tmp_path / "teams.json")
    crew.load.cache_clear()
    try:
        return crew.load()
    finally:
        crew.load.cache_clear()


def test_crew_reads_the_file_the_module_writes(tmp_path, monkeypatch):
    fleet = loaded(tmp_path, monkeypatch, PINNED)
    assert fleet["repositories"] == {}
    parts = fleet["partitions"]
    assert list(parts) == ["afterthought", "agentplot", "madswan", "wldn"]
    assert parts["wldn"]["sessions"]["planner"] == "wldn-1"
    assert parts["wldn"]["sessions"]["reviewer"] == "wldn-1"
    for label, p in parts.items():
        assert all(p["flume"][role] is False for role in crew.KIND_ROLES), f"{label}'s roles do not all stand: {p['flume']}"


def test_crew_reads_the_kept_repositories_the_module_writes(tmp_path, monkeypatch):
    """crew-flake, crew reads the kept repositories the module writes: on deneb, crew's and swancloud's folder and
    checkout are the file's, whether or not a space lists them; the box's are its spaces' still."""
    monkeypatch.setattr(crew, "this_host", lambda: DENEB)
    fleet = loaded(tmp_path, monkeypatch, FILES / "runner.json")
    assert list(fleet["partitions"]) == ["afterthought", "agentplot", "madswan", "wldn"]
    r, v = "/Users/chuck/.local/share/flywheel/repositories", "/Users/chuck/Code/boomdrive"
    assert crew.kit_kept(fleet, DENEB, "crew") == {"name": "crew", "repo": "agentplot/crew", "dir": f"{r}/agentplot/crew",
                                                   "main": f"{v}/agentplot/crew"}
    assert crew.kit_kept(fleet, DENEB, "afterthought/swancloud") == {
        "name": "swancloud", "repo": "afterthought/swancloud", "dir": f"{r}/afterthought/swancloud", "main": f"{v}/afterthought/swancloud"}
    assert crew.kit_kept(fleet, BOX, "crew") is None
    assert fleet["partitions"]["madswan"]["checkout"] == f"{tmp_path}/madswan/blueprints/main"
