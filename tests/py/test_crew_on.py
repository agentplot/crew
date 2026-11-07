"""crew run on another host from the checkout of the repository crew is (code.3, read.1, plan.22): the repository read
from crew's own manifest, never from a name in crew's code, and found as the host's sessions keep it; a host that keeps
none refused naming the repository it looked for, a former address of crew's followed by no reader. The reading:
deneb, 2026-11-07, crew 0.41.0-unstable-2026-11-07, `crew send wldn ...` refused because crew looked on
chuck-herdr-alpha for afterthought/crew, a name written in crew_at, after crew moved to agentplot/crew."""
import pathlib
import re

import pytest

import crew

ROOT = pathlib.Path(__file__).resolve().parents[2]
BOX = "chuck-herdr-alpha"


def fleet(*repos):
    """The box's spaces as the hosts file has them on 2026-11-07, its willdan sessions keeping repos at /workspace."""
    sess = {"dir": "/workspace", "partition": "clients/willdan", "repos": list(repos)}
    return {"hosts": {BOX: {"sessions": {"wldn": sess, "wldn-3": dict(sess)}}, "deneb": {"sessions": {}}}, "partitions": {}}


KEPT = fleet("agentplot/crew", "WilldanGroup/atlas-kit", "WilldanGroup/willdan-blueprints")


class TestCrewOn:
    def test_crew_is_found_on_another_host_under_its_current_address(self):
        assert crew.crew_on(KEPT, BOX, "deneb", "agentplot/crew") == "/workspace/crew/main/plugin/bin/crew"

    def test_a_host_that_keeps_none_is_refused_naming_the_repository_it_looked_for(self):
        with pytest.raises(crew.Refusal, match=f"^none of {BOX}'s sessions keeps agentplot/crew, the repository crew is, "
                                               "so crew can't run there$"):
            crew.crew_on(fleet("WilldanGroup/atlas-kit"), BOX, "deneb", "agentplot/crew")

    def test_a_host_that_keeps_crew_only_under_a_former_address_is_refused_and_the_name_is_not_followed(self):
        """plan.22: no reader maps a former name, so a checkout kept as afterthought/crew is not crew's agentplot/crew."""
        with pytest.raises(crew.Refusal, match="keeps agentplot/crew, the repository crew is"):
            crew.crew_on(fleet("afterthought/crew"), BOX, "deneb", "agentplot/crew")

    def test_the_repository_is_whatever_crew_is_never_a_name_of_its_own(self):
        moved = fleet("someone/crew-next")
        assert crew.crew_on(moved, BOX, "deneb", "someone/crew-next") == "/workspace/crew-next/main/plugin/bin/crew"

    def test_on_this_host_it_is_this_crew_and_no_repository_is_asked(self):
        assert crew.crew_on(KEPT, "deneb", "deneb", None) == str(crew.HOME / "plugin/bin/crew")


class TestCrewAt:
    def test_crew_at_finds_crew_on_another_host_by_the_repository_its_own_manifest_names(self, monkeypatch):
        """The reading, reproduced: deneb runs `crew send wldn ...` for wldn's operator on the box, whose spaces keep
        agentplot/crew, and crew reaches it there."""
        monkeypatch.setattr(crew, "this_host", lambda: "deneb")
        assert crew.crew_at(KEPT, BOX) == "/workspace/crew/main/plugin/bin/crew"

    def test_crew_at_reads_no_manifest_for_this_host(self, monkeypatch):
        monkeypatch.setattr(crew, "this_host", lambda: "deneb")
        monkeypatch.setattr(crew, "crew_repository", lambda: pytest.fail("the manifest was read for this host"))
        assert crew.crew_at(KEPT, "deneb") == str(crew.HOME / "plugin/bin/crew")


class TestRepositoryNamed:
    def test_crews_own_manifest_names_its_current_address(self):
        assert crew.repository_named(crew.MANIFEST.read_text(), crew.MANIFEST) == "agentplot/crew"

    @pytest.mark.parametrize("given", ["https://github.com/agentplot/crew", "https://github.com/agentplot/crew.git",
                                       "https://github.com/agentplot/crew/", "git@github.com:agentplot/crew.git"])
    def test_a_github_address_gives_its_owner_and_name(self, given):
        assert crew.repository_named(f'{{"name": "crew", "repository": "{given}"}}', "m.json") == "agentplot/crew"

    @pytest.mark.parametrize("text, said", [
        ('{"name": "crew"}', "m.json names no GitHub repository as its 'repository' (null)"),
        ('{"repository": "https://gitlab.com/agentplot/crew"}', "m.json names no GitHub repository as its 'repository' (\"https://gitlab.com/agentplot/crew\")"),
        ('{"repository": {"url": "https://github.com/agentplot/crew"}}', "m.json names no GitHub repository"),
        ('{"repository": "https://github.com/agentplot"}', "m.json names no GitHub repository"),
        ("not json", "m.json is no JSON object"),
        ('["https://github.com/agentplot/crew"]', "m.json is no JSON object")])
    def test_a_manifest_that_names_no_repository_is_refused_naming_the_file(self, text, said):
        """read.1: crew can't tell where it is kept, so it says so rather than guess."""
        with pytest.raises(crew.Refusal, match=re.escape(said)):
            crew.repository_named(text, "m.json")


def test_crews_code_writes_its_own_address_nowhere():
    """The repository crew is comes from its manifest alone: no module or command of crew's names it."""
    own = crew.repository_named(crew.MANIFEST.read_text(), crew.MANIFEST)
    named = re.compile(re.escape(own) + r"(?![\w-])")
    files = sorted((ROOT / "plugin/lib").glob("*.py")) + sorted(p for p in (ROOT / "plugin/bin").iterdir() if p.is_file())
    assert [str(p.relative_to(ROOT)) for p in files if named.search(p.read_text())] == []
