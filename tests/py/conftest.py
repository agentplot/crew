"""The logic tier (tests.11): crew's decisions called in-process on plain facts. Nothing here starts a process: every
way Python starts one raises, so a decision that still reaches a tool fails its test, naming the call."""
import os
import pathlib
import subprocess
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "plugin" / "lib"))


@pytest.fixture(autouse=True)
def no_process(monkeypatch):
    def refuse(*args, **kwargs):
        raise AssertionError(f"a logic test starts no process, and this one ran {args[0] if args else kwargs!r}")
    for name in ("run", "Popen", "call", "check_call", "check_output", "getoutput", "getstatusoutput"):
        monkeypatch.setattr(subprocess, name, refuse)
    for name in ("system", "popen", "execv", "execvp", "execvpe", "spawnv", "spawnvp", "fork"):
        monkeypatch.setattr(os, name, refuse)


@pytest.fixture(autouse=True)
def no_run(monkeypatch):
    """A suite started in a Flume place carries FLUME_PLACE, which names a role's run to crew.caller: a case runs in
    no place but one it names."""
    monkeypatch.delenv("FLUME_PLACE", raising=False)


@pytest.fixture(autouse=True)
def scratch_record(monkeypatch, tmp_path_factory):
    """A case's run record is kept under a scratch folder, never the host's own under ~/.local/state/crew: a plan write
    appends the entries its commit carried to the host's file once its push is accepted, and a case that stands in
    land is such a push. A case that names its own folder for the record sets record.ROOT itself."""
    import record
    monkeypatch.setattr(record, "ROOT", tmp_path_factory.mktemp("record"))


@pytest.fixture(autouse=True)
def pushed(monkeypatch):
    """record.emit pushes each entry it writes through record.reach, which fetches and pushes the drive's branch:
    here reach stands for it, recording each label it was asked to push, so every case that emits still runs and one
    can say the push was asked (read.5)."""
    import record
    asked = []
    monkeypatch.setattr(record, "reach", lambda label, eid=None, said=False: asked.append(label) or 0)
    return asked


@pytest.fixture(autouse=True)
def no_main(monkeypatch):
    """A case reads no kit's main on GitHub unless it hands one in: plan.main_tip gives None, as the follower's read gives
    it for a repository its fetch has not brought (a-landed-bolt-is-closed-and-offered-no-more, Decision 7), so a started
    bolt reads as the runner's report gives it and nothing is fetched. A case that reads main sets plan.main_tip itself,
    and tests/py/test_landed_on_main.py's TestMainTip takes the real one back."""
    import plan
    monkeypatch.setattr(plan, "main_tip", lambda repo: None)
