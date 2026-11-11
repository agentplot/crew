"""What crew's tidy does on a kit's host (plan.9 as crew-lands-each-bolt-through-flumes-base-place, Decision 8, departs
from it): crew makes no worktree on a bolt's branch now, so the tidy removes none, runs no sluice, deletes no bolt
branch and reads no mark of crew's, and names each landing's place or legacy bolt worktree it finds with the commands
that remove it, the user's to run (plan.tidy, plan.leftover_said); and what a removal recorded reads as, and where a
place's bolt and a local bolt are read from. crew runs no wt remove, so worktrunk's is pinned by no contract case.""" 
import json

import pytest

import gather
import plan

KD = "/kit"


class TestTheTidy:
    """bolt-teams "crew removes no worktree, and names a landing's left from before" (Decision 8)."""

    @pytest.fixture
    def trees(self, monkeypatch):
        got = []
        monkeypatch.setattr(gather, "worktrees", lambda main: list(got))
        return got

    def test_a_landings_place_and_a_legacy_bolt_worktree_are_named_with_the_commands_that_remove_them(self, trees, capsys):
        trees += [{"path": f"{KD}/main", "branch": None}, {"path": f"{KD}/places/land-t", "branch": "bolt/t"},
                  {"path": f"{KD}/bolts/u", "branch": None}, {"path": f"{KD}/places/change--a", "branch": "change/a"},
                  {"path": "/elsewhere/x", "branch": "bolt/t"}]
        t = {"label": "wldn", "machine": "box", "kit": {"name": "k", "main": f"{KD}/main", "dir": KD}}
        assert plan.tidy({}, t, landed="t") == []
        assert capsys.readouterr().out.splitlines() == [
            f"{KD}/places/land-t is a landing's place of bolt t, which crew makes no more and removes no more: it is yours to "
            f"remove, with sluice release --worktree {KD}/places/land-t and then wt -C {KD}/main remove {KD}/places/land-t",
            f"{KD}/bolts/u is bolt u's worktree from before bolts lived on GitHub, which crew makes no more and removes no "
            f"more: it is yours to remove, with sluice release --worktree {KD}/bolts/u and then wt -C {KD}/main remove {KD}/bolts/u"]

    @pytest.mark.parametrize("path, branch", [("places/change--a", "change/a"), ("places/land-t", "bolt/other"),
                                              ("places/land-t", "chore/t"), ("main", None), ("wt/x", "bolt/t")])
    def test_a_place_of_flumes_and_every_other_worktree_are_left_unnamed(self, path, branch):
        assert plan.leftover_said(f"{KD}/{path}", branch or "", KD) is None


class TestRemovalRecorded:
    """plan.9: a slot.free crew wrote before it stopped freeing slots named the place its tidy removed in Paths, and
    crew events still reads it so; the sweep of a landing's place says it in its output alone."""

    def test_a_removal_reads_as_one_in_crew_events_and_a_forecast_still_as_its_conflict(self):
        import record
        e = {"At": "2026-10-29T10:00:00Z", "Act": "slot.free", "On": ["agent/t-unit-1", "unit/a"], "From": [], "Commit": [],
             "Paths": f"{KD}/places/a"}
        assert record.line(e).endswith(f"agent/t-unit-1 unit/a (removed {KD}/places/a)")
        assert record.line(dict(e, Act="forecast", Paths="a.txt", Reached="told")).endswith("(conflict on a.txt, told)")


@pytest.mark.parametrize("up, bolt", [
    ("bolt/b", "b"), ("origin/bolt/b", "b"), ("origin/bolt/tenant-environments", "tenant-environments"),
    ("", None), (None, None), ("main", None), ("origin/main", None), ("unit/x", None), ("bolt/", None), ("upstream/bolt/b", None)])
def test_a_places_bolt_is_read_from_either_upstream(up, bolt):
    """gather.bolt_of (plan.19): every read of a place's bolt from its upstream takes bolt/<bolt>, a bolt made before,
    and origin/bolt/<bolt>, a bolt on GitHub, alike."""
    import gather
    assert gather.bolt_of(up) == bolt


class TestBoltMadeBefore:
    """bolt-plan "A bolt made before stays local" (plan.19, record 0032's amendment): each read of a team holding a bolt
    on its host only, while the kit's main names a remote for its bolts, says once that it is local until it lands."""
    LINE = ("bolt/b is local until it lands: it was made before bolts were on GitHub, so its places are cut from the "
            "local branch, and its landing puts it on GitHub")

    def test_a_local_bolt_while_main_names_a_remote_is_said(self):
        assert plan.bolt_local_said("b", None, "origin") == self.LINE

    def test_a_bolt_on_github_is_not(self):
        assert plan.bolt_local_said("b", "origin", "origin") is None

    def test_a_local_bolt_while_main_names_none_is_not_since_every_bolt_is(self):
        assert plan.bolt_local_said("b", None, None) is None
