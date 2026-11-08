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

    def test_a_crossed_bolts_landed_fix_reads_merged_from_its_bolts_landing(self):
        """bolt-plan "A fix whose place's landing its bolt's branch holds is merged": tidy's place last carried at
        submitted and x's landing of fix/x--tidy after its launch, it reads merged there, as crew bolts and the board
        show it; with x's landings unread, or the landing made before its launch, it reads submitted (read.1)."""
        from facts import ran
        landed = {"fix/x--tidy": {"commit": "4" * 40, "at": "2026-11-08T04:18:32Z"}}
        st = self.with_tidy(ran({4: "submitted"}), bolt={"landings": landed})
        [(w, _, s)] = st.fixes(st.plan.bolt("x"))
        assert (w, s["stage"], s["commit"], s["landed"], s["on"], s["branch"]) == (
            "fix/x/tidy", "merged", "4" * 40, "2026-11-08T04:18:32Z", "bolt", "fix/x--tidy")
        assert runner.piece_said(s) == ("merged", "fix/x--tidy landed on its bolt at 4444444")
        unread = self.with_tidy(ran({4: "submitted"}), bolt={"landings_error": "git could not list the landings on origin/bolt/x"})
        assert [s["stage"] for _, _, s in unread.fixes(unread.plan.bolt("x"))] == ["submitted"]
        before = self.with_tidy(ran({4: "submitted"}), bolt={"landings": {"fix/x--tidy": dict(landed["fix/x--tidy"], at="2026-11-08T03:59:59Z")}})
        assert [s["stage"] for _, _, s in before.fixes(before.plan.bolt("x"))] == ["submitted"]


# ------------------------------------------------------------------- a unit whose work its bolt's branch already holds

# The landings sluice made on x, by the branch each names (gather.bolt_landings): a's, b's and chore c's places.
LANDED = {"change/a": {"commit": "1" * 40, "at": "2026-11-07T19:10:00Z"},
          "change/b": {"commit": "2" * 40, "at": "2026-11-07T19:20:00Z"},
          "chore/c": {"commit": "3" * 40, "at": "2026-11-07T19:30:00Z"}}


class TestBuiltOnItsBolt:
    """bolt-plan "A unit whose work its bolt's branch holds is built" (crew record 0056 decision 2: crew reads a bolt's
    places from what the work's tools hold; read.1, read.2): a piece whose place's branch a landing on its bolt names is
    merged at that landing, read from the bolt's branch as the kit was read, whatever the runner reports of its place and
    whichever partition's launch made it; no partition is mapped onto another (crew record 0055, rejected). x, a, b and
    c as TestCrossed has them."""
    FLEET = madswan_fleet()
    stages = TestCrossed.stages

    @pytest.fixture(autouse=True)
    def writer(self, monkeypatch):
        monkeypatch.setenv("CREW_AGENT", "madswan-dispatch-deneb")

    def test_places_landed_and_tidied_read_merged_from_the_bolts_landings_not_the_runners_stale_status(self):
        """agentplot-design, 2026-11-07: flume's two units on flume-names-each-repository-by-its-address and sluice's on
        sluices-own-module-writes-a-hosts-settings landed on their bolts and Flume tidied their places; the runner had
        carried one place never and another last at submitted, so crew read them launching and submitted and no batch
        came due. Here a's place was never carried and b's last at submitted: with x's landings read, a, b and chore c
        are merged at their landings, carried when each landed, a batch reads a and b, and a is landed once main holds
        its change."""
        from facts import ran
        runners = ran({2: "submitted"})
        assert [self.stages(runners).of(n)["stage"] for n in "abc"] == ["launching", "submitted", "launching"]
        st = self.stages(runners, bolt={"landings": LANDED, "archived": ["a", "b"]})
        got = [(st.of(n)["stage"], st.of(n)["flume"]["commit"], st.of(n)["carried"]) for n in "abc"]
        assert got == [("merged", "1" * 40, "2026-11-07T19:10:00Z"), ("merged", "2" * 40, "2026-11-07T19:20:00Z"),
                       ("merged", "3" * 40, "2026-11-07T19:30:00Z")]
        assert st.of("b")["flume"]["place"].endswith("change--teams-cross-to-flume-as-their-bolts-land")
        assert runner.piece_said(st.of("a")["flume"]) == ("merged", "change/a landed on its bolt at 1111111")
        assert plan.crossed_changes(st.plan, st) == {"a": ("1" * 40, "2026-11-07T19:10:00Z"), "b": ("2" * 40, "2026-11-07T19:20:00Z")}
        landed = self.stages(runners, main=["a"], bolt={"landings": LANDED})
        assert [landed.of(n)["stage"] for n in "ab"] == ["landed", "merged"]

    def test_every_piece_merged_on_a_bolt_sluice_passed_reads_it_proven(self):
        """bolt-plan "A unit whose work its bolt's branch holds is built": x's head is sluice's landing, passed, and
        every piece is read merged from x's landings, so x waits to land (teams.16); with the runner's records alone
        it stays active."""
        from facts import ran
        green = {"landings": LANDED, "verdict": "passed (35 run, 0 replayed)"}
        st = self.stages(ran({2: "submitted"}), bolt=green)
        assert st.bolt_state(st.plan.bolt("x")) == "waits"
        st = self.stages(ran({2: "submitted"}), bolt=dict(green, landings={}))
        assert st.bolt_state(st.plan.bolt("x")) == "active"

    def test_a_launch_refused_for_a_change_its_bolt_already_holds_reads_merged_and_asks_nothing(self):
        """The reading of 2026-11-07 (afterthought-planner on deneb; signal 2026-11-07-agentplot-planner-cbc41169/02):
        a's place ran as another partition's launch and landed on x; crew launched a again for this partition and the
        runner refused it because the base bolt already holds the change. With x's landing of change/a, a is merged
        there and nothing waits on it; without one, a stays refused with the runner's words, never guessed built."""
        from facts import ran
        words = "the base bolt/x already holds a change named a"
        runners = ran({2: "code"}, refused={1: words})
        assert self.stages(runners).of("a")["flume"] == {"stage": "refused", "words": words}
        s = self.stages(runners, bolt={"landings": LANDED}).of("a")
        assert (s["stage"], s["flume"]) == ("merged", {"stage": "merged", "commit": "1" * 40, "landed": "2026-11-07T19:10:00Z",
                                                        "on": "bolt", "branch": "change/a"})

    def test_a_unit_another_partitions_place_built_with_no_launch_here_is_merged_by_its_branch_alone(self):
        """Whichever partition's launch made a's place, its branch is change/a, the unit's own name: this partition
        holds no launch of a at all, so the runner's records give it none, and x's landing of change/a makes it merged;
        a landing naming another branch builds nothing, and a fix's work is read from the landing naming its own place's
        branch alone."""
        from facts import ran
        st = self.stages(ran({2: "code"}), bolt={"landings": LANDED})
        requests, reads = st.runs["madswan"]
        st.runs["madswan"] = ([r for r in requests if r.get("Work") != "unit/a"], reads)
        assert (st.of("a")["stage"], st.of("a")["flume"]["commit"]) == ("merged", "1" * 40)
        other = self.stages(ran({2: "code"}), bolt={"landings": {"change/ab": LANDED["change/a"], "unit/a": LANDED["change/a"]}})
        assert other.of("a")["stage"] == "launching"
        assert runner.built_on_bolt("fix/x/tidy", {"stage": "code"}, {"fix/x--tidy": LANDED["change/a"]})["stage"] == "merged"
        assert runner.built_on_bolt("fix/x/tidy", {"stage": "code"}, {"fix/x--gap": LANDED["change/a"]}) == {"stage": "code"}

    def test_landings_crew_could_not_read_leave_the_runners_reading(self):
        """read.1: x's landings unread (landings_error, no landings) build nothing; the runner's stage stands."""
        from facts import ran
        st = self.stages(ran({2: "submitted"}), bolt={"landings_error": "git could not list the landings on origin/bolt/x"})
        assert st.of("b")["stage"] == "submitted"

    def test_a_place_the_runner_reads_landed_keeps_flumes_commit(self):
        """A place Flume's status shows landed is merged at Flume's commit, sluice's landing on the bolt, as before."""
        from facts import ran
        flumes = self.stages(ran({1: "landed"})).of("a")["flume"]
        s = self.stages(ran({1: "landed"}), bolt={"landings": LANDED}).of("a")["flume"]
        assert (s, s["stage"], s.get("on")) == (flumes, "merged", None)
        assert s["commit"] and s["commit"] != "1" * 40


class TestABoltWhoseLaunchesWereAllRefused:
    """bolt-plan "A unit whose work its bolt's branch holds is built" and drive-state "A bolt whose every launch was
    refused": a bolt whose every launch the runner refused, as for changes the bolt already holds, has no place of its
    own; crew reads it where that runner reports keeping the kit (plan.launched_at; Decision 1 of
    a-bolts-landing-on-main-reads-landed), its stream none while the runner carries no place of it, never in a folder
    another place names, so crew bolts never says where it runs can't be told for it while the runner reports the kit."""
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
        st = plan.Stages(self.FLEET, p, crew_read(bolts={"x": {"landings": LANDED}, "y": {}}), runs={"madswan": (requests, runners)},
                         label="madswan")
        assert (st.unread(p.bolt("x")), st.of("a")["stage"]) == (None, "merged")

    def test_the_kits_folder_on_another_runners_host_is_not_taken(self):
        from facts import ran
        p, requests = self.launched()
        runners = {**ran(refused={1: "the base bolt/x already holds a change named a"}, keeps=None), **ran({2: "code"}, host="alpha")}
        with pytest.raises(plan.Refusal, match="^the runner on deneb took bolt x's work and reports no repositories it keeps, so "
                                               "crew can't tell where it keeps crew there$"):
            plan.bolt_at(self.FLEET, "madswan", p.bolt("x"), (requests, runners))


class TestABoltLandedOnMain:
    """bolt-plan "A landed bolt's pieces are read from its landing" and bolt-teams "A bolt whose landing main holds closes
    whatever the runner carried of its places" (Decision 3 of a-bolts-landing-on-main-reads-landed): x landed on main
    through a pull request and GitHub deleted bolt/x, so the kit's read gives x's facts with no branch, its landing on main
    and the landings on that landing's line (gather.kit); deneb's runner answered a's launch launched and carries no place
    of it, as deneb's runner carried none on 2026-11-08. a reads landed through its landing, x reads landed and its close
    passes; a piece the landing does not name keeps x open, named; a landing crew can't read builds nothing (read.1)."""
    FLEET = madswan_fleet()
    LANDING = {"commit": "4acecf09" + "0" * 32, "at": "2026-11-08T16:02:45Z", "base": "b45e0000" + "0" * 32, "head": "900527e9" + "0" * 32}
    A = {"change/a": {"commit": "1" * 40, "at": "2026-11-08T15:00:00Z"}}
    PLACES = {1: "/crew/main/places/change--a"}

    @pytest.fixture(autouse=True)
    def writer(self, monkeypatch):
        monkeypatch.setenv("CREW_AGENT", "madswan-dispatch-deneb")

    def launched(self, units):
        from facts import launched
        return launched(["x"], work=[(u, "x", [], "unit", []) for u in units], fleet=self.FLEET)

    def stages(self, units, runners, facts):
        """x of units, started and launched, crew's kit read on deneb holding a on main and x's facts as gather gives a
        bolt with no branch (gather.kit), over facts."""
        p, requests = self.launched(units)
        gone = {"exists": False, "head": None, "head_at": None, "verdict": None}
        return p, plan.Stages(self.FLEET, p, crew_read(main=["a"], bolts={"x": dict(gone, **facts)}),
                              runs={"madswan": (requests, runners)}, label="madswan")

    def test_a_landed_bolt_whose_branch_and_places_are_gone_reads_landed_and_closes(self):
        """bolt-plan "The landed unit of a bolt whose branch and places are gone"; bolt-teams "A landed bolt whose branch
        and places are gone"."""
        from facts import ran
        p, st = self.stages(["a"], ran(unplaced=self.PLACES), {"landed": self.LANDING, "landings": self.A})
        assert (st.of("a")["stage"], st.of("a")["flume"]["commit"]) == ("landed", "1" * 40)
        assert st.bolt_state(p.bolt("x")) == "landed"
        assert plan.land_refusal("x", ["a"], st.of, [], "madswan", {"1" * 40: 0}, "crew") is None

    def test_a_piece_its_landing_does_not_name_keeps_the_bolt_open_named(self):
        """bolt-teams "A piece its landing does not hold"; bolt-plan "A piece its landing does not name"."""
        from facts import ran
        p, st = self.stages(["a", "b"], ran({2: "code"}, unplaced=self.PLACES), {"landed": self.LANDING, "landings": self.A})
        assert (st.of("a")["stage"], st.of("b")["stage"]) == ("landed", "code")
        assert st.bolt_state(p.bolt("x")) != "landed"
        assert plan.land_refusal("x", ["a", "b"], st.of, [], "madswan", {"1" * 40: 0}, "crew") == (
            "unit b has not merged into bolt/x: it is code")

    def test_a_landing_crew_cant_read_builds_nothing(self):
        """bolt-plan "main's line can't be read"."""
        from facts import ran
        _, st = self.stages(["a"], ran(unplaced=self.PLACES),
                            {"landed_error": "git could not list main's first-parent line at origin/main since 2026-11-08T10:00:00Z: fatal"})
        assert st.of("a")["stage"] == "launching"

    def test_stages_for_seeks_each_started_bolts_landing_from_its_launch_and_the_heads_crew_submitted(self, monkeypatch):
        """stages_for asks the survey for x with seek, its first launch's Date and its bolt.submit's head
        (landing_sought), the survey faked as gather would answer it."""
        from facts import ran
        import record
        p, requests = self.launched(["a"])
        submits = record.acts_in(f"Id: 1\nAt: 2026-11-08T15:40:00Z\nAct: bolt.submit\nOn: bolt/x\nOutcome: queued\n"
                                 f"Head: {self.LANDING['head']}\n", "bolt.submit")
        asked = []
        monkeypatch.setattr(plan, "runner_facts", lambda fleet, label: (requests, ran(unplaced=self.PLACES)))
        monkeypatch.setattr(plan, "submits_read", lambda fleet, label: submits)
        monkeypatch.setattr(plan, "survey", lambda fleet, held, fetch=False: asked.extend(held) or crew_read(
            main=["a"], bolts={"x": {"exists": False, "head": None, "landed": self.LANDING, "landings": self.A}}))
        st = plan.stages_for(self.FLEET, "madswan", p, [p.bolt("x")])
        since = min(r.get("Date") for r in requests if r.get("Base") == "bolt/x")
        assert [(t["machine"], b, sought) for t, b, sought in asked] == [("deneb", "x", {"since": since, "heads": [self.LANDING["head"]]})]
        assert st.of("a")["stage"] == "landed"
