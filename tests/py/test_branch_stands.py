"""A unit whose branch stands is refused at its proposal (bolt-plan "A name whose Flume branch stands is refused when it
is planned"; signal 2026-11-07-agentplot-planner-b2717722/01): Flume keeps a dropped place's branch while it holds work
and refuses a launch that would make it again (flume 3, 67), so crew reads whether the branch stands in the repository a
launch would be made in, as Flume reads it, and refuses the add, naming the branch, where it stands and the two ways on;
a drop says Flume keeps the branch and the name stays taken. Where the repository is, which branch a launch makes, what
stands and the refusal are decisions of facts; the add through a proposal's own reads (plan.Proposed) reads the runners
and git through plan.runner_facts and plan.branches_in, which a case gives. git's own reading of the branches is the
contract tier's (tests/contract/test_git.py)."""
import pytest

from facts import FactsWrite, apply, flume_plan, known, launched, madswan_fleet, ran
import plan
import record
import runner

FLEET = madswan_fleet()
SHA = "c0ffee" + "0" * 34
RE_ADD = "a-base-place-that-conflicts-with-its-base-launches-its-fix"


@pytest.fixture(autouse=True)
def writer(monkeypatch):
    """A write to a started bolt appends its launches, which name their writer."""
    monkeypatch.setenv("CREW_AGENT", "madswan-planner")


def unit(name, bolt="x", kind="unit"):
    return (name, bolt, [], kind, [])


def started(*work):
    """madswan's plan with bolt x started and its work launched as a start launches it (facts.launched), as a write,
    and requests.rec's records as it leaves them."""
    w = FactsWrite(flume_plan([("x", None, None)], list(work)), label="madswan")
    w.plan.bolt("x").set("Path", "flume")
    plan.reach_places(FLEET, w, "x")
    return w, plan.Plan(w.files["requests.rec"]).recs("Request")


class Reads(plan.Proposed):
    """A proposal's own reads (plan.Proposed), its free among them, each unit's stage given as ready."""

    def stage(self, label, p, name):
        return {"stage": "ready", "worktree": None, "why": None}


def keeping(host="deneb", **repos):
    """A host's runner that has taken nothing and reports keeping each repository (forge address) in its folder, as its
    repositories.rec says (runner.host_read)."""
    files = {"runner.rec": plan.Plan(runner.RUNNER + f"\nHost: {host}\nVersion: 0.1.0\nSince: 2026-10-31T11:00:00Z\n"),
             "repositories.rec": plan.Plan(runner.REPOSITORIES + "".join(
                 f"\nRepository: {a}\nFolder: {f}\n" for a, f in repos.items()))}
    return {host: runner.host_read("madswan", host, "5e1f0c2a" + "0" * 32, files, {})}


class TestTheBranch:
    def test_a_units_launch_makes_change_and_a_chores_makes_chore(self):
        assert runner.place_branch("unit/a") == "change/a"
        assert runner.place_branch("chore/c") == "chore/c"

    def test_what_stands_is_each_branch_named_exactly_and_not_one_below_it(self):
        out = f"{SHA} refs/heads/change/a\n{'d' * 40} refs/heads/change/b/old\n"
        assert runner.refs_standing(out, ["change/a", "change/b", "chore/c"]) == {"change/a": SHA}
        assert runner.refs_standing("", ["change/a"]) == {}


class TestWhereALaunchWouldBeMade:
    def test_where_the_runner_that_took_the_kits_work_keeps_it(self):
        _, requests = launched(["x"], work=[unit("a")])
        reads = ran({1: "code"}, repository="/r/crew")
        assert runner.launch_repositories(reads, runner.kit_launches(requests, "crew"), "crew") == (
            [{"host": "deneb", "dir": "/r/crew"}], None)

    def test_where_a_runner_reports_keeping_the_kit_though_it_took_none_of_its_work(self):
        reads = keeping(**{"afterthought/crew": "/r/afterthought/crew", "agentplot/flume": "/r/agentplot/flume"})
        assert runner.launch_repositories(reads, [], "crew") == ([{"host": "deneb", "dir": "/r/afterthought/crew"}], None)

    def test_nowhere_while_no_runner_has_taken_the_kits_work_and_none_reports_keeping_it(self):
        assert runner.launch_repositories(ran({}, keeps=None), [], "crew") == ([], None)
        assert runner.launch_repositories(ran({}, keeps=("agentplot/flume",)), [], "crew") == ([], None)

    def test_crew_cant_tell_where_when_the_runner_that_took_it_reports_no_repositories(self):
        """Its place's status names /r/crew, and its branch holds no repositories.rec: the place is no report of where
        the runner keeps crew (Decision 1 of a-bolts-landing-on-main-reads-landed)."""
        _, requests = launched(["x"], work=[unit("a")])
        reads = ran({1: "code"}, repository="/r/crew", keeps=None)
        assert runner.launch_repositories(reads, runner.kit_launches(requests, "crew"), "crew") == ([], (
            "the runner on deneb took crew's work and reports no repositories it keeps, so crew can't tell where it keeps "
            "crew there"))

    def test_crew_cant_tell_where_when_a_runner_keeps_two_repositories_by_the_kits_name(self):
        reads = keeping(**{"afterthought/crew": "/r/a/crew", "madswan/crew": "/r/m/crew"})
        assert runner.launch_repositories(reads, [], "crew") == ([], (
            "the runner on deneb keeps afterthought/crew and madswan/crew by the name crew, so crew can't tell which a "
            "launch of its work would be made in"))


class TestTheRefusal:
    FOUND = [{"host": "deneb", "dir": "/r/crew", "refs": {f"change/{RE_ADD}": SHA}}]

    def test_a_name_whose_branch_stands_is_refused_naming_the_branch_where_it_stands_and_the_ways_on(self):
        assert runner.branch_refusal("crew", "unit", [RE_ADD], self.FOUND) == (
            f"unit {RE_ADD} can't be planned in crew: Flume's branch change/{RE_ADD} stands in /r/crew on deneb, at "
            f"c0ffee0, where a launch of {RE_ADD} would make its place, and Flume refuses a launch that would make it again "
            "while it stands; propose the unit under a fresh name, or have the planner or the user remove the branch "
            f"first, which may hold work and which crew never removes (git -C /r/crew branch -D change/{RE_ADD}, on deneb)")

    def test_a_fresh_name_passes(self):
        assert runner.branch_refusal("crew", "unit", ["a-base-place-launches-its-fix"], self.FOUND) is None

    def test_a_chore_by_the_name_is_another_branch_and_passes(self):
        assert runner.branch_refusal("crew", "chore", [RE_ADD], self.FOUND) is None


class TestAtItsProposal:
    """The add as a proposal checks it (plan.check_ops, plan.apply_all): plan.Proposed's reads, the runners and git given."""

    def given(self, monkeypatch, refs, keeps=("afterthought/crew",)):
        w, requests = started(unit("a"))
        asked = []
        monkeypatch.setattr(plan, "name_free", lambda *a: None)  # main's changes and chores: test_unit_commands.py
        monkeypatch.setattr(plan, "runner_facts", lambda fleet, label: (requests, ran({1: "code"}, repository="/r/crew", keeps=keeps)))

        def branches_in(fleet, host, folder, branches):
            asked.append((host, folder, branches))
            return {b: refs[b] for b in branches if b in refs}
        monkeypatch.setattr(plan, "branches_in", branches_in)
        return w, asked

    def test_a_dropped_unit_added_again_under_its_name_is_refused_and_nothing_is_written(self, monkeypatch):
        w, asked = self.given(monkeypatch, {f"change/{RE_ADD}": SHA})
        before = w.plan.text()
        with pytest.raises(plan.Refusal) as e:
            apply(w, f'unit add {RE_ADD} "Build it again." --bolt x', ctx=Reads(FLEET, "madswan", w, 49))
        assert str(e.value).startswith(f"unit {RE_ADD} can't be planned in crew: Flume's branch change/{RE_ADD} stands in "
                                       "/r/crew on deneb, at c0ffee0")
        assert asked == [("deneb", "/r/crew", [f"change/{RE_ADD}"])]
        assert w.plan.text() == before

    def test_the_same_work_under_a_fresh_name_passes(self, monkeypatch):
        w, asked = self.given(monkeypatch, {f"change/{RE_ADD}": SHA})
        apply(w, 'unit add a-base-place-launches-its-fix "Build it again." --bolt x', ctx=Reads(FLEET, "madswan", w, 49))
        assert w.plan.unit("a-base-place-launches-its-fix").get("Bolt") == "x"
        assert asked == [("deneb", "/r/crew", ["change/a-base-place-launches-its-fix"])]

    def test_a_chore_reads_its_own_branch(self, monkeypatch):
        w, asked = self.given(monkeypatch, {"chore/bump": SHA})
        with pytest.raises(plan.Refusal, match="^chore bump can't be planned in crew: Flume's branch chore/bump stands"):
            apply(w, 'chore add bump "Bump it." --bolt x', ctx=Reads(FLEET, "madswan", w, 49))
        assert asked == [("deneb", "/r/crew", ["chore/bump"])]

    def test_a_split_reads_the_branch_of_each_name_it_adds(self, monkeypatch):
        w, asked = self.given(monkeypatch, {"change/a-rest": SHA})
        w.plan.bolt("x").drop("Path")  # a bolt not started, so a's split launches nothing
        with pytest.raises(plan.Refusal, match="^unit a-rest can't be planned in crew"):
            apply(w, 'unit split a "Build a." --into a-rest "The rest."', ctx=Reads(FLEET, "madswan", w, 49))
        assert asked == [("deneb", "/r/crew", ["change/a-rest"])]

    def test_where_crew_cant_tell_the_repository_the_add_is_refused_saying_why(self, monkeypatch):
        w, asked = self.given(monkeypatch, {}, keeps=None)
        with pytest.raises(plan.Refusal) as e:
            apply(w, 'unit add b "Build b." --bolt x', ctx=Reads(FLEET, "madswan", w, 49))
        assert str(e.value) == ("cannot check whether Flume's branch for unit b stands: the runner on deneb took crew's work "
                                "and reports no repositories it keeps, so crew can't tell where it keeps crew there")
        assert asked == []

    def test_a_card_drawn_reads_no_repository(self, monkeypatch):
        w, asked = self.given(monkeypatch, {f"change/{RE_ADD}": SHA})
        apply(w, f'unit add {RE_ADD} "Build it again." --bolt x', ctx=plan.Drawn(FLEET, "madswan", w, 49))
        assert asked == []


class TestTheDrop:
    def dropped(self, w, do):
        a = plan.do_args("madswan", do)
        op = plan.OPS[(a.cmd, a.sub)](known(w, n=1, fleet=FLEET), a)
        op.change(w)
        return op

    def test_a_launched_units_drop_says_flume_keeps_its_branch_and_the_name_stays_taken(self):
        w, _ = started(unit(RE_ADD), unit("b"))
        op = self.dropped(w, f'unit drop {RE_ADD} "Replaced."')
        assert op.fields["Note"] == (
            f"Flume keeps change/{RE_ADD} while it holds work bolt/x lacks, and the name {RE_ADD} stays taken while that "
            f"branch stands: a unit added as {RE_ADD} again is refused until the planner or the user removes it")

    def test_a_chores_drop_names_its_chore_branch(self):
        w, _ = started(unit("a"), unit("c", kind="chore"))
        assert self.dropped(w, 'chore drop c "Done by hand."').fields["Note"].startswith("Flume keeps chore/c while it holds work bolt/x lacks")

    def test_a_drop_of_work_never_launched_says_nothing_of_a_branch(self):
        w = FactsWrite(flume_plan([("y", None, None)], [unit("q", bolt="y")]), label="madswan")
        assert "Note" not in self.dropped(w, 'unit drop q "Not needed."').fields

    def test_the_entry_carries_the_note_and_a_trace_shows_it(self):
        note = runner.drop_kept_said("unit", "a", "bolt/x")
        e = {"Id": "1", "At": "2026-11-07T20:20:00Z", "Host": "deneb", "By": "madswan-planner", "Act": "unit.drop",
             "On": ["unit/a", "bolt/x"], "From": ["proposal/49"], "Commit": [], "Note": note}
        assert record.line(e).endswith(f"unit/a bolt/x ← proposal/49 ({note})")
        assert "Note" in record.EXTRA
