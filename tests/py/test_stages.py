"""A drop refused for work whose stage crew cannot tell (read.1); and a started bolt's work, its stage read from the
runner's records and never from a place in the kit (bolt-plan "A unit's stage is read from the runner, or from the plan
before its bolt starts"): plan.Stages."""
import pytest

from facts import FactsWrite, apply, crew_read, flume_plan, known, madswan_fleet, plan_text

import plan
import runner


def fresh():
    return FactsWrite(plan_text(bolts=[("tenant-environments", "switchboard-kit", "swb-1"), ("console-pages", "switchboard-kit", "swb-2")],
                                units=[("bump", "switchboard-kit", "tenant-environments", [], "chore"), ("b", "switchboard-kit", "tenant-environments", [])]))


def test_work_whose_stage_crew_cannot_tell_is_not_dropped():
    """bump's stage unknown, its host silent: the drop is refused naming why (read.1)."""
    w = fresh()
    ctx = known(w)
    ctx.of = lambda name: {"stage": "unknown", "worktree": None, "open": [], "head": None, "why": "its host did not answer"}
    with pytest.raises(plan.Refusal, match="cannot tell chore bump's stage: its host did not answer"):
        apply(w, 'chore drop bump "Not now."', ctx=ctx)


# ------------------------------------------------------------------------- a crossed team's work, from the runner's records

class TestCrossed:
    """bolt-plan "A started bolt's work reads its stage from the runner's records" and "A started place's stage is where
    Flume's status has it" (Decision 8 of teams-cross-to-flume-as-their-bolts-land): plan.Stages answers runner.stage_of
    for each unit and chore of a bolt marked Path: flume, from the runner that took its launch, never reading a place in
    the kit, and reads the kit where that runner reported it (the user's ruling of 2026-11-01)."""
    FLEET = madswan_fleet()

    @pytest.fixture(autouse=True)
    def writer(self, monkeypatch):
        monkeypatch.setenv("CREW_AGENT", "madswan-dispatch-deneb")

    def stages(self, runners, main=(), chores=(), runs=None, bolt=None):
        """Stages of x, started, holding a, b after a, and chore c, launched as requests 1 to 3, with the partition's runners
        as given (facts.ran, deneb's), and crew's kit as read on deneb holding main's changes and chores, and x's facts
        there as given (bolt, over crew_read's empty bolt)."""
        from facts import launched
        p, requests = launched(["x"], work=[("a", "x", [], "unit", []), ("b", "x", ["a"], "unit", []), ("c", "x", [], "chore", [])],
                               fleet=self.FLEET)
        return plan.Stages(self.FLEET, p, crew_read(main, chores, {"x": bolt or {}}),
                           runs={"madswan": runs if runs is not None else (requests, runners)}, label="madswan")

    def test_a_dependent_waits_on_the_work_it_comes_after(self):
        """bolt-plan "A dependent waits": b's launch answered held, a's place not yet landed."""
        from facts import ran
        s = self.stages(ran({1: "code"}, held=[2])).of("b")
        assert (s["stage"], s["flume"]["after"], s["worktree"]) == ("waiting", ["unit/a"], None)

    def test_the_runners_host_silent_reads_every_crossed_piece_unknown(self):
        """bolt-plan "The runner's host is silent": deneb's runner branch can't be read, so crew can't tell which runner
        took each launch; with no runner answering for the partition at all, nothing takes them (read.1)."""
        silent = {"deneb": runner.host_read("madswan", "deneb", "5e1f0c2a" + "0" * 32, {}, {"runner.rec": "recfix refused it"})}
        st = self.stages(silent)
        why = "deneb's runner can't be read: madswan/runner/deneb at 5e1f0c2: recfix refused it"
        assert [(st.of(n)["stage"], st.of(n)["why"]) for n in "abc"] == [
            ("unknown", f"no runner crew read has taken request {n}, and {why}") for n in (1, 2, 3)]
        assert st.unread(st.plan.bolt("x")) == ("deneb's runner", why)
        none = self.stages({})
        assert none.of("a")["why"] == "no runner answers for the partition: no <label>/runner/<host> branch exists, so nothing takes request 1"

    def test_requests_crew_cant_read_read_every_crossed_piece_unknown(self):
        st = self.stages(None, runs="could not fetch madswan/main of afterthought/crew-state over https: no network")
        assert st.of("a")["stage"] == "unknown"
        assert st.of("a")["why"] == ("crew can't read madswan's requests or runners: could not fetch madswan/main of "
                                     "afterthought/crew-state over https: no network")

    def test_a_unit_in_code_reads_its_tasks(self):
        """bolt-plan "A unit in code"."""
        from facts import ran
        s = self.stages(ran({1: "code"})).of("a")
        assert (s["stage"], s["tasks"]) == ("code", (6, 26))
        assert runner.piece_said(s["flume"]) == ("code 6/26", "")

    def test_a_worktree_of_crews_from_before_is_not_read(self):
        """bolt-plan "A worktree of crew's from before": a unit/a place in the kit with every task ticked reads nothing
        for a; its stage is the runner's."""
        from facts import ran
        st = self.stages(ran({1: "code"}))
        k = st.survey["deneb"]["kits"]["/crew/main"]
        k["places"]["a"] = {"path": "/crew/places/unit-a", "tasks": [5, 5], "planning": True, "open": [], "branch": "unit/a", "bolt": "x"}
        assert (st.of("a")["stage"], st.of("a")["tasks"]) == ("code", (6, 26))

    def test_a_bolt_not_started_reads_ready_or_waiting_from_the_plan(self):
        """bolt-plan "A bolt not started": a with no After ready, b after a waiting, and nothing of a runner read."""
        p = plan.Plan(flume_plan([("y", None, None)], [("a", "y", [], "unit", []), ("b", "y", ["a"], "unit", []), ("q", None, [], "unit", [])]))
        st = plan.Stages(self.FLEET, p, {}, runs={}, label="madswan")
        assert [st.of(n)["stage"] for n in ("a", "b", "q")] == ["ready", "waiting", "queued"]
        assert st.runs == {}

    def test_a_construct_that_asked_needs_an_answer_with_its_question(self):
        """bolt-plan "A construct that asked"."""
        from facts import ran
        s = self.stages(ran({1: "stopped-short"})).of("a")
        assert s["stage"] == "needs"
        assert runner.piece_said(s["flume"])[1].startswith("asks at code: Head 118ec46 is ready for your flume:live run (6.1).")

    def test_a_place_sent_back_by_sluice_reads_its_stage_with_sluices_words(self):
        """bolt-plan "Sent back by sluice"."""
        from facts import ran
        s = self.stages(ran({2: "sent-back"})).of("b")
        assert (s["stage"], s["flume"]["sent_back"]) == ("code", 1)
        assert runner.piece_said(s["flume"]) == ("code 26/26", "sent back by sluice: check-full failed on "
                                                 "bolt/crew-runs-its-work-through-flume with change/teams-cross-to-flume-as-"
                                                 "their-bolts-land merged: tests:logic (1 failed: tests/py/test_runner.py::"
                                                 "TestStageOf::test_a_crossed_piece_reads_its_stage)")

    def test_a_place_landed_on_its_bolt_reads_merged_and_landed_once_main_holds_it(self):
        """bolt-plan "Landed on the bolt": merged while x has not landed; landed once crew's main holds a's change, or c's
        trailer, as today's do."""
        from facts import ran
        runners = ran({1: "landed", 3: "landed"})
        assert [self.stages(runners).of(n)["stage"] for n in "ac"] == ["merged", "merged"]
        assert [self.stages(runners, main=["a"], chores=["c"]).of(n)["stage"] for n in "ac"] == ["landed", "landed"]

    def test_a_launch_the_runner_has_not_answered_is_launching_and_no_launch_is_unknown(self):
        from facts import ran
        assert self.stages(ran()).of("a")["stage"] == "launching"
        st = self.stages(None, runs=([], ran()))
        assert (st.of("a")["stage"], st.of("a")["why"]) == ("unknown", "unit/a has no launch in requests.rec")

    def with_tidy(self, runners, bolt=None):
        """Stages of x (stages) with its fix tidy launched as request 4 at 2026-11-08T04:00:00Z."""
        st = self.stages(runners, bolt=bolt)
        requests, _ = st.runs["madswan"]
        fix = plan.Rec("Request", [("Request", "4"), ("Act", "launch"), ("Work", "fix/x/tidy"), ("Name", "x--tidy"),
                                   ("Base", "bolt/x"), ("Kind", "fix"), ("Date", "2026-11-08T04:00:00Z")])
        st.runs["madswan"] = (requests + [fix], st.runs["madswan"][1])
        return st

    def test_a_crossed_bolts_fixes_read_their_stages_from_the_runner(self):
        """bolt-plan's requirement holds for a fix: fix/x/tidy, launched as request 4, read at code."""
        from facts import ran
        st = self.with_tidy(ran({4: "code"}))
        assert [(w, s["stage"]) for w, _, s in st.fixes(st.plan.bolt("x"))] == [("fix/x/tidy", "code")]

    def test_a_crossed_bolts_fix_held_for_the_runner_reads_merged(self):
        """bolt-plan "A fix the runner reports merged holds nothing": tidy's place landed on x and Flume tidied it,
        holding its record for the runner, which carries it as tidy's status (tests/py/flume-0.20.0/landed-held.json);
        it reads merged at the record's commit, as crew bolts and the board show it, with no word of a landing on its
        bolt; last carried at submitted, it reads submitted, whatever x's landing commits name."""
        from facts import ran
        st = self.with_tidy(ran({4: "flume-0.20.0/landed-held"}))
        [(w, _, s)] = st.fixes(st.plan.bolt("x"))
        assert (w, s["stage"], s["commit"]) == ("fix/x/tidy", "merged", HELD_AT)
        assert runner.piece_said(s) == ("merged", "")
        named = self.with_tidy(ran({4: "submitted"}), bolt={"landings": {"fix/x--tidy": {"commit": "4" * 40, "at": "2026-11-08T04:18:32Z"}}})
        assert [s["stage"] for _, _, s in named.fixes(named.plan.bolt("x"))] == ["submitted"]


# ------------------------------------------------------------------------ a place's end held for the runner

# The commit Flume landed the place of tests/py/flume-0.20.0/landed-held.json at, as its record held for the runner says.
HELD_AT = "f564d22041933732ee004aa33d1b629a97272cd9"


class TestEndsHeldForTheRunner:
    """bolt-plan "A launched place's stage is where Flume's status has it" (record 0062's stopgap retired; crew record 0056
    point 4; roles.5, roles.9): a piece's end is the runner's report alone, the record Flume holds for the runner after
    it tidies the place among them (tests/py/flume-0.20.0/), and no landing commit on its bolt or on main is read for it.
    x, a, b and c as TestCrossed has them."""
    FLEET = madswan_fleet()
    stages = TestCrossed.stages

    @pytest.fixture(autouse=True)
    def writer(self, monkeypatch):
        monkeypatch.setenv("CREW_AGENT", "madswan-dispatch-deneb")

    def test_a_place_landed_and_tidied_reads_merged_from_the_record_held_for_the_runner(self):
        """bolt-plan "A landing held for the runner": Flume landed a's place on x and tidied it, holding its record for
        the runner, which carries it as a's status; a reads merged at the record's commit, carried when the runner
        carried it, which a batch reads it at, and landed once main holds its change."""
        from facts import ran
        runners = ran({1: "flume-0.20.0/landed-held"})
        st = self.stages(runners, bolt={"archived": ["a"]})
        assert (st.of("a")["stage"], st.of("a")["flume"]["commit"], st.of("a")["carried"]) == ("merged", HELD_AT, "2026-10-31T12:02:00Z")
        assert plan.crossed_changes(st.plan, st) == {"a": (HELD_AT, "2026-10-31T12:02:00Z")}
        landed = self.stages(runners, main=["a"])
        assert (landed.of("a")["stage"], landed.of("a")["flume"]["commit"]) == ("landed", HELD_AT)

    def test_a_place_tidied_before_the_runner_carried_its_end_reads_as_last_carried(self):
        """bolt-plan "A place tidied before the runner carried its end": the runner last carried b's place at submitted,
        Flume tidied it holding no record for the runner, and x's facts give a landing commit naming change/b; b reads
        submitted, as last carried, and nothing reads that landing (design Decision 3)."""
        from facts import ran
        named = {"landings": {"change/b": {"commit": "2" * 40, "at": "2026-11-07T19:20:00Z"}}}
        st = self.stages(ran({2: "submitted"}), bolt=named)
        assert (st.of("b")["stage"], st.of("b")["flume"].get("commit"), st.of("b")["carried"]) == ("submitted", None, "2026-10-31T12:02:00Z")
        assert plan.crossed_changes(st.plan, st) == {}

    def test_a_launch_refused_for_a_change_its_bolt_holds_reads_refused(self):
        """bolt-plan "A launch refused for a change the bolt holds" (design Decision 4): the runner refused this
        partition's launch of a because the base bolt/x already holds a change named a, and x's facts give a landing
        commit naming change/a; a reads refused in the runner's words, and nothing of x's landing commits is read."""
        from facts import ran
        words = "the base bolt/x already holds a change named a"
        named = {"landings": {"change/a": {"commit": "1" * 40, "at": "2026-11-07T19:10:00Z"}}}
        s = self.stages(ran({2: "code"}, refused={1: words}), bolt=named).of("a")
        assert (s["stage"], s["flume"]) == ("refused", {"stage": "refused", "words": words})

    def test_a_head_held_for_the_runner_reads_green_and_one_only_a_landing_commit_names_reads_none(self):
        """merge-gate "A landing held for the runner": every piece of x carried landed and held for the runner at its
        commit, x's head the last, reads green naming the head as the runner reports it; and "A landing read from the
        bolt's own landings": b last carried at submitted, with x's facts giving a landing commit naming change/b at the
        head, reads none, so x is not offered for landing."""
        from facts import ran
        st = self.stages(ran({n: "flume-0.20.0/landed-held" for n in (1, 2, 3)}), bolt={"head": HELD_AT})
        assert st.verification(st.plan.bolt("x"), HELD_AT) == ("green", f"its head {HELD_AT[:7]} is a's landing, as the runner reports it")
        head = "2" * 40
        named = {"head": head, "landings": {"change/b": {"commit": head, "at": "2026-11-07T19:20:00Z"}}}
        st = self.stages(ran({1: "flume-0.20.0/landed-held", 2: "submitted"}), bolt=named)
        assert st.verification(st.plan.bolt("x"), head)[0] == "none"
        assert st.bolt_state(st.plan.bolt("x")) == "active"

    GONE = {"exists": False, "head": None, "head_at": None, "verdict": None}  # x's facts once GitHub deleted bolt/x

    def test_a_landed_bolt_whose_places_are_held_for_the_runner_closes(self):
        """bolt-teams "A landed bolt whose branch and places are gone": x landed on main, GitHub deleted bolt/x, Flume
        tidied each of x's places and the runner carries the record Flume holds for it of each, landed on bolt/x at a
        commit main holds; each piece reads merged at its record's commit, and x's close is refused for none of them."""
        from facts import ran
        st = self.stages(ran({n: "flume-0.20.0/landed-held" for n in (1, 2, 3)}), bolt=self.GONE)
        assert [(st.of(n)["stage"], st.of(n)["flume"]["commit"]) for n in "abc"] == [("merged", HELD_AT)] * 3
        assert plan.land_refusal("x", ["a", "b", "c"], st.of, [], "madswan", {HELD_AT: 0}, "crew") is None

    def test_a_piece_whose_end_the_runner_never_carried_keeps_the_bolt_open(self):
        """bolt-teams "A piece whose end the runner never carried": main holds x's landing, the runner last carried b's
        place at submitted, Flume having tidied it holding no record for the runner, and a landing commit on bolt/x names
        change/b; x's close is refused naming b."""
        from facts import ran
        named = dict(self.GONE, landings={"change/b": {"commit": "2" * 40, "at": "2026-11-07T19:20:00Z"}})
        st = self.stages(ran({1: "flume-0.20.0/landed-held", 2: "submitted", 3: "flume-0.20.0/landed-held"}), bolt=named)
        assert plan.land_refusal("x", ["a", "b", "c"], st.of, [], "madswan", {HELD_AT: 0, "2" * 40: 0}, "crew") == (
            "unit b has not merged into bolt/x: it is submitted")


class TestABoltWhoseLaunchesWereAllRefused:
    """bolt-plan "A launch refused for a change the bolt holds" and drive-state "A bolt whose every launch was
    refused": a bolt whose every launch the runner refused, as for changes the bolt already holds, has no place of its
    own; crew reads it where that runner reports keeping the kit, its stream none while the runner carries no place of
    it, or, where that runner reports no repositories, as its places of the kit's other work name it (plan.launched_at,
    kit_at), never another host's, so crew bolts never says where it runs can't be told for it."""
    FLEET = madswan_fleet()

    @pytest.fixture(autouse=True)
    def writer(self, monkeypatch):
        monkeypatch.setenv("CREW_AGENT", "madswan-dispatch-deneb")

    def launched(self):
        from facts import launched
        return launched(["x", "y"], work=[("a", "x", [], "unit", []), ("b", "y", [], "unit", [])], fleet=self.FLEET)

    def test_it_is_read_on_the_runners_host_in_the_kits_folder_there(self):
        from facts import ran
        p, requests = self.launched()
        runners = ran({2: "code"}, refused={1: "the base bolt/x already holds a change named a"})
        at = plan.bolt_at(self.FLEET, "madswan", p.bolt("x"), (requests, runners))
        assert (at["machine"], at["stream"], at["kit"]["main"]) == ("deneb", None, "/crew/main")
        st = plan.Stages(self.FLEET, p, crew_read(bolts={"x": {}, "y": {}}), runs={"madswan": (requests, runners)}, label="madswan")
        assert (st.unread(p.bolt("x")), st.of("a")["stage"]) == (None, "refused")

    def test_with_no_repositories_reported_it_is_read_where_the_runners_place_of_the_kits_other_work_names(self):
        from facts import ran
        p, requests = self.launched()
        runners = ran({2: "code"}, refused={1: "the base bolt/x already holds a change named a"}, keeps=None)
        at = plan.bolt_at(self.FLEET, "madswan", p.bolt("x"), (requests, runners))
        assert (at["machine"], at["stream"], at["kit"]["main"]) == ("deneb", "madswan", "/crew/main")

    def test_the_kits_folder_on_another_runners_host_is_not_taken(self):
        from facts import ran
        p, requests = self.launched()
        runners = {**ran(refused={1: "the base bolt/x already holds a change named a"}, keeps=None), **ran({2: "code"}, host="alpha")}
        with pytest.raises(plan.Refusal, match="^the runner on deneb took bolt x's work, reports no repositories it keeps and "
                                               "carries no place of crew's work naming its folder, so crew can't tell where "
                                               "it keeps crew there$"):
            plan.bolt_at(self.FLEET, "madswan", p.bolt("x"), (requests, runners))
