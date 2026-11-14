"""One landings card per kit's main (rail-cards, record 0031 as amended 2026-10-23, plan.16): what a land/ key names,
a kit's or a bolt's, and the run record's object for it; a bolt refused a kit's name; the card's rows in the plan's
order, a bolt held for a fix or a landing sluice refused at its head; the conflicts forecast between each row and main
and each row above it; and the one decision of what the raise does with the kit's card. Each on plain facts (code.7);
the raise's act on a stand-in for what it reaches beyond them. Its wiring is t-journey-land's and t-cards'."""
import argparse
import base64
import contextlib
import fcntl
import json

import pytest

import cards
import crew
import plan

KITS = ("crew", "swancloud")
FLEET = {"drives": {"swancloud": {"label": "swancloud", "machine": "mac-studio"}}}
# Where each kit's work runs, as the runner that took it reported (plan.bolt_at, plan.kit_at): swancloud's on deneb,
# crew's on mac-studio, each in stream swancloud.
WHERE = {"swancloud": {"machine": "deneb", "stream": "swancloud",
                       "kit": {"name": "swancloud", "repo": "afterthought/swancloud", "main": "/s/main", "dir": "/s"}},
         "crew": {"machine": "mac-studio", "stream": "swancloud",
                  "kit": {"name": "crew", "repo": "afterthought/crew", "main": "/c/main", "dir": "/c"}}}


@pytest.fixture(autouse=True)
def kits(monkeypatch):
    """swancloud's kits as its plan and landings name them (plan.kits_read), with no branch read; and where each started
    bolt's and each kit's work runs as the runner that took it reported (plan.bolt_at, plan.kit_at), on the host and in
    the folder WHERE gives each kit, with no runner read."""
    monkeypatch.setattr(plan, "kits_read", lambda fleet, label: list(KITS))

    def kit_where(label, kit):
        w = WHERE.get((kit or "").split("/")[-1])
        return dict(w, label=label) if w else None
    monkeypatch.setattr(plan, "runner_facts", lambda fleet, label: ([], {}))
    monkeypatch.setattr(plan, "bolt_at", lambda fleet, label, b, run=None: kit_where(label, b.get("Repo")) if plan.started(b) else None)
    monkeypatch.setattr(plan, "bolt_taken", lambda fleet, label, b, run=None: (kit_where(label, b.get("Repo")), None))
    monkeypatch.setattr(plan, "kit_at", lambda fleet, label, kit, run=None: kit_where(label, kit) or plan.fail(
        f"no runner has reported taking {kit}'s work yet, so crew can't tell where it runs"))


# ------------------------------------------------------------------------------------- what a land/ key names

def test_a_kits_key_is_its_landings_card():
    assert plan.land_key("land/crew", KITS) == ("kit", "crew")


def test_any_other_land_key_is_a_bolts():
    assert plan.land_key("land/doctor-rows", KITS) == ("bolt", "doctor-rows")


def test_an_old_key_with_the_head_is_the_bolts_even_when_named_as_a_kit():
    assert plan.land_key("land/doctor-rows/abc1234", KITS) == ("bolt", "doctor-rows")
    assert plan.land_key("land/crew/abc1234", KITS) == ("bolt", "crew")


@pytest.mark.parametrize("key", ["batch/7", "land/", "land/Crew", "proposal/3", None])
def test_a_key_that_is_no_landings_names_nothing(key):
    assert plan.land_key(key, KITS) is None


def test_a_kits_card_is_on_the_kit_and_a_bolts_on_the_bolt_in_the_run_record():
    assert cards.row_object("land/crew", KITS) == "kit/crew"
    assert cards.row_object("land/doctor-rows", KITS) == "bolt/doctor-rows"
    assert cards.row_object("land/crew") == "bolt/crew"  # no kit named: as before, a bolt's


def test_a_bolt_named_as_a_kit_of_its_drive_is_refused():
    assert plan.kit_named("crew", KITS, "swancloud") == (
        "a bolt of swancloud may not be named crew: that is the name of a kit swancloud's plan or landings name, whose landings "
        "card is land/crew")
    assert plan.kit_named("doctor-rows", KITS, "swancloud") is None


def test_the_plan_write_that_adds_a_bolt_named_as_a_kit_refuses_it_writing_nothing():
    class Ctx:
        fleet = FLEET

        def kit(self, kit):
            return "swancloud"

        def kits(self, label):
            return KITS
    a = argparse.Namespace(repo="swancloud", bolt="crew", goal="x", source=[], before=None)
    with pytest.raises(crew.Refusal, match="may not be named crew"):
        plan.op_bolt_new(Ctx(), a)
    assert plan.op_bolt_new(Ctx(), argparse.Namespace(**dict(vars(a), bolt="doctor-rows"))).act == "bolt.new"


# ---------------------------------------------------------------------------------------------- the card's rows

def facts(bolt, head="a" * 40, fixes=None, **more):
    return dict(bolt=bolt, kit="crew", head=head, fixes=fixes or {}, **more)


def submitted(bolt, head, refused=None):
    return dict(Act="bolt.submit", On=[f"bolt/{bolt}"], Head=head, **({"Refused": refused} if refused else {}))


def test_the_rows_are_the_proven_bolts_in_the_plans_order_each_a_box():
    rows = plan.landing_rows(["w", "y", "x", "z"], {"z": facts("z"), "y": facts("y"), "w": facts("w")}, {})
    assert [(r["bolt"], r["box"]) for r in rows] == [("w", True), ("y", True), ("z", True)]


def test_a_fix_in_flight_holds_its_row_in_its_words_with_no_box():
    rows = plan.landing_rows(["y", "z"], {"y": facts("y", fixes={"fix/y/gap": "The zone list misses one zone."}),
                                          "z": facts("z", fixes={"fix/z/old": None})}, {})
    assert [(r["bolt"], r["box"], r["why"]) for r in rows] == [
        ("y", False, "held for a fix: The zone list misses one zone. (fix/y/gap)"),
        ("z", False, "held for fix/z/old until it merges or is dropped")]


def test_a_bolt_started_before_bolts_were_base_places_has_no_box_beside_one_that_can_land():
    """rail-cards "A bolt started before bolts were base places has no box", beside a bolt that can land (Decision 9):
    its row is held with no box in the words that say it lands under the crew that started it, and the card shows the
    other alone."""
    import runner
    rows = plan.landing_rows(["y", "z"], {"y": facts("y", legacy=runner.legacy_said("y")), "z": facts("z")}, {})
    assert [(r["bolt"], r["box"], r.get("why")) for r in rows] == [
        ("y", False, "y was started before bolts were base places and lands under the crew that started it"), ("z", True, None)]
    assert [r["bolt"] for r in plan.card_rows(rows)] == ["z"]


def test_a_landing_refused_at_the_bolts_present_head_holds_its_row():
    head = "d" * 40
    held = plan.refusals([submitted("y", "c" * 40), submitted("y", head, "bolt/y did not land: sluice found a conflict")])
    row, = plan.landing_rows(["y"], {"y": facts("y", head)}, held)
    assert (row["box"], row["why"]) == (False, "landing rejected at ddddddd, open for work: it waits for a fix on the "
                                               "bolt: bolt/y did not land: sluice found a conflict")
    assert plan.held_at(plan.refusals([submitted("y", head, "no")]), "y", head) == "no"


def test_a_submit_that_submitted_nothing_at_the_refused_head_leaves_the_row_held_for_its_fix():
    """The Willdan box's case (signal 2026-11-06-wldn-ops-ea539623/01; bolt-teams "No land is posted again until
    a fix moves the head sent back"): a stop an older crew recorded at the head sent back, of a submit that submitted nothing,
    leaves the row held for its fix, never given its box back as a stop of the runner's or Flume's."""
    head = "d" * 40
    entries = [dict(submitted("y", head, "#1474 failed: tests:logic on 41a7c09"), Submission="1474"),
               dict(submitted("y", head), Outcome="stopped", Why="sluice itself failed (it said nothing), and sluice records no submission")]
    row, = plan.landing_rows(["y"], {"y": facts("y", head)}, plan.refusals(entries), plan.stops(entries))
    assert (row["box"], row["why"]) == (False, "landing rejected at ddddddd, open for work: it waits for a fix on the bolt: #1474 "
                                               "failed: tests:logic on 41a7c09")


def test_a_refusal_at_an_older_head_holds_nothing_once_the_fix_moved_it():
    held = plan.refusals([submitted("y", "c" * 40, "bolt/y did not land")])
    row, = plan.landing_rows(["y"], {"y": facts("y", "d" * 40)}, held)
    assert row["box"]
    assert plan.held_at(plan.refusals([submitted("y", "c" * 40, "no")]), "y", "d" * 40) is None


def test_a_landing_after_a_refusal_holds_nothing():
    assert plan.refusals([submitted("y", "c" * 40, "no"), submitted("y", "c" * 40)]) == {}


def test_a_landing_stopped_at_the_bolts_present_head_keeps_its_box_saying_what_stopped_it():
    """rail-cards "A landing the runner or Flume stopped keeps its box": recorded stopped, its row a box whose facts
    carry the head it was stopped at and what stopped it; once its head moves, its row says nothing of it."""
    head = "d" * 40
    stop = dict(submitted("y", head), Why="check:dagger could not run: the Dagger engine did not answer", Outcome="stopped")
    entries = [submitted("y", "c" * 40, "bolt/y did not land: sluice found a conflict"), stop]
    row, = plan.landing_rows(["y"], {"y": facts("y", head)}, plan.refusals(entries), plan.stops(entries))
    assert (row["box"], row["facts"]["stopped"]) == (True, (head, "check:dagger could not run: the Dagger engine did not answer"))
    moved, = plan.landing_rows(["y"], {"y": facts("y", "e" * 40)}, plan.refusals(entries), plan.stops(entries))
    assert moved["box"] and "stopped" not in moved["facts"]
    assert "stopped" not in plan.landing_rows(["y"], {"y": facts("y", head)}, {})[0]["facts"]


def test_a_bolt_forecast_to_conflict_with_main_takes_main_first_with_no_box():
    """rail-cards "Main landed a change the bolt also made"."""
    rows = plan.landing_rows(["y", "z"], {"y": facts("y"), "z": facts("z")}, {},
                             takes_main={"y": ("e4f5a6b", ["openspec/specs/artifact-buckets/spec.md"])})
    assert [(r["bolt"], r["box"], r.get("why"), r.get("takes_main")) for r in rows] == [
        ("y", False, "takes main first: forecast to conflict with main on openspec/specs/artifact-buckets/spec.md at "
                     "e4f5a6b, until a fix taking main in moves its head", True),
        ("z", True, None, None)]


def test_a_conflict_a_wait_recorded_holds_the_row_when_the_cards_own_forecast_was_not_made():
    """rail-cards "Raised again at the same heads": the record's conflict at the bolt's present head (main_conflict)."""
    head = "d" * 40
    recorded = [dict(Act="forecast", On=["bolt/y"], Heads=f"bolt/y@{head[:7]} main@2222222", Paths="README.md", Reached="wait")]
    row, = plan.landing_rows(["y"], {"y": facts("y", head)}, {}, takes_main={"y": plan.main_conflict(recorded, "y", head)})
    assert (row["box"], row["why"], row["takes_main"]) == (
        False, "takes main first: forecast to conflict with main on README.md at 2222222, until a fix taking main in moves its head", True)


def test_a_conflict_only_with_a_row_above_holds_nothing():
    """rail-cards "Only a bolt above it": a forecast against a row above is said on the row, not held."""
    rows = plan.landing_rows(["y", "z"], {"y": facts("y"), "z": dict(facts("z"), forecast=[("y", ["plan.py"])])}, {}, takes_main={})
    assert [r["box"] for r in rows] == [True, True]


# The Willdan box's breadboard-kit on 2026-11-06 (signal 2026-11-07-wldn-ops-052d0a47/01): bolt deleting landed its
# unit as 214, f5e67f35, merging the unit's commits; the popover unit's coder rebased onto that landing, so the
# popover bolt's landing 216, b0fdceeb, holds 214 and every commit it merged, while main holds neither bolt.
UNITS_214 = ["6165532d" + "0" * 32, "c162f231" + "0" * 32, "56e28202" + "0" * 32]
L214, L216, POPOVER_UNIT = "f5e67f35" + "0" * 32, "b0fdceeb" + "0" * 32, ["d4a01a89" + "0" * 32, "8d11ad43" + "0" * 32]
DELETING_HOLDS = [L214] + UNITS_214
POPOVER_HOLDS = [L216] + POPOVER_UNIT + [L214] + UNITS_214
LINES = {"breadboard-shows-a-deleted-app-as-deleting": [L214], "breadboards-access-choice-is-one-popover": [L216]}


def test_a_bolt_holding_another_bolts_landing_carries_that_bolts_work_and_the_other_carries_nothing():
    """plan.8 (gather.carried_bolts): the popover bolt holds deleting's landing 214, on deleting's own first-parent line and
    not on its own, so it carries deleting's work; deleting holds nothing on the popover bolt's line, so the bolt
    whose work was carried is free to land, its own landing taking that work to main."""
    assert plan.gather.carried_bolts(POPOVER_HOLDS, LINES, "breadboards-access-choice-is-one-popover") == {
        "breadboard-shows-a-deleted-app-as-deleting": [L214]}
    assert plan.gather.carried_bolts(DELETING_HOLDS, LINES, "breadboard-shows-a-deleted-app-as-deleting") == {}


def test_a_commit_on_the_bolts_own_line_or_one_main_holds_is_carried_from_no_one():
    """plan.8: a landing on the bolt's own first-parent line is its own, whichever other line also lists it; and a
    commit main holds is in no bolt's holds beyond main, so once deleting lands the popover bolt carries nothing."""
    lines = dict(LINES, other=[L216])
    assert plan.gather.carried_bolts(POPOVER_HOLDS, lines, "breadboards-access-choice-is-one-popover") == {
        "breadboard-shows-a-deleted-app-as-deleting": [L214]}
    assert plan.gather.carried_bolts([L216] + POPOVER_UNIT, LINES, "breadboards-access-choice-is-one-popover") == {}


def test_a_bolt_carrying_another_bolts_work_is_held_with_no_box_naming_that_bolt_and_its_landing():
    """plan.8: held as a conflict holds it, whatever else holds it, a take-main fix in flight on it among them, so it is
    no row the user ticks and no card is raised for it; its words name the bolt whose work it carries and that bolt's
    landing it holds."""
    carried = {"breadboard-shows-a-deleted-app-as-deleting": [L214]}
    words = "Take main into the bolt: it is forecast to conflict on README.md"
    y, z = plan.landing_rows(["y", "z"], {"y": facts("y", carries=carried, fixes={"fix/y/take-main-e4f5a6b": words}), "z": facts("z")}, {},
                             takes_main={"y": ("e4f5a6b", ["README.md"])})
    assert (y["box"], y.get("takes_main"), y["why"]) == (False, None, (
        "held: carries bolt breadboard-shows-a-deleted-app-as-deleting's work, its landing f5e67f3, which main lacks; a bolt "
        "never carries another bolt's work to main, so it lands once main holds that work, by the landing of bolt "
        "breadboard-shows-a-deleted-app-as-deleting"))
    assert z["box"]


def test_a_bolt_whose_carried_work_cant_be_read_is_held_saying_why():
    """read.1: what a bolt carries that git could not list holds it too, saying why, never read as nothing."""
    row, = plan.landing_rows(["y"], {"y": facts("y", carries_error="git could not list bolt/z's own commits beyond main")}, {})
    assert (row["box"], row["why"]) == (False, "held: crew can't tell whether it carries another bolt's work, so it does not "
                                               "land: git could not list bolt/z's own commits beyond main")


def test_a_take_main_fix_in_flight_holds_its_row_as_taking_main_first_in_its_words():
    """rail-cards "The conductor started the fix"; any other fix holds the row in its words as ever."""
    words = "Take main into the bolt: it is forecast to conflict on README.md"
    y, z = plan.landing_rows(["y", "z"], {"y": facts("y", fixes={"fix/y/take-main-e4f5a6b": words}),
                                          "z": facts("z", fixes={"fix/z/take-main-e4f5a6b": words, "fix/z/gap": "A zone is missing."})}, {})
    assert (y["box"], y["why"], y["takes_main"]) == (False, f'takes main first: take-main-e4f5a6b taking main in: "{words}"', True)
    assert (z["box"], z.get("takes_main")) == (False, None)
    assert z["why"] == f'held for a fix: A zone is missing. (fix/z/gap); takes main first: take-main-e4f5a6b taking main in: "{words}"'


class TestALiveLandingFixHoldsItsRow:
    """bolt-teams "A live landing fix holds its bolt" and rail-cards "A row held by Flume's landing fix says so"
    (crews-bolt-kind-names-its-landing-fix, Decision 5): a live landing fix of a bolt's base place is a fix in flight on
    it (runner.fixes_in_flight), so its row has no box, takes main first or is held in its words, and no land is posted
    while it runs; once a fix that took main in has landed, the standing send lands the bolt."""

    def in_flight(self, fixture, status=None):
        import runner
        from facts import ran
        reads = ran({1: f"flume-0.19.0/{fixture}"}, label="swancloud")
        if status is not None:
            reads["deneb"]["places"][1]["status"] = status
        return runner.fixes_in_flight([], "y", TestLandsDue().requests(), reads)

    def test_a_conflicts_live_landing_fix_takes_main_first_beside_a_row_that_can_land(self):
        x, y = plan.landing_rows(["x", "y"], {"x": facts("x"), "y": facts("y", fixes=self.in_flight("bolt-conflict-fixing"))}, {})
        assert (x["box"], y["box"], y["takes_main"]) == (True, False, True)
        assert y["why"] == ('takes main first: y-1 taking main in: "Take main into the bolt: Flume\'s landing fix y-1 merges main '
                            'at 9f1c2ab"')
        assert [(r["bolt"], r["box"]) for r in plan.card_rows([x, y])] == [("x", True), ("y", False)]

    def test_a_forecasts_live_landing_fix_takes_main_first_and_the_raise_appends_no_request(self, monkeypatch):
        monkeypatch.setenv("CREW_AGENT", "swancloud-ops")
        (y,) = plan.landing_rows(["y"], {"y": facts("y", H1, fixes=self.in_flight("bolt-forecast-fixing"))}, {})
        assert (y["box"], y["takes_main"]) == (False, True) and "Flume's landing fix y-1 merges main at 9f1c2ab" in y["why"]
        w = TestTheRaisePostsTheLands().write()
        before = w.files["requests.rec"]
        from facts import ran
        with pytest.raises(plan.Unposted):
            plan.lands_change(w, "crew", [y], {"bolt/y": ("req_1", H1[:7])}, ran({1: "flume-0.19.0/bolt-forecast-fixing"}, label="swancloud"))
        assert w.files["requests.rec"] == before

    def test_a_failed_checks_live_landing_fix_holds_its_row_in_its_words(self):
        from facts import flume_fixture
        status = json.loads(flume_fixture("flume-0.19.0/bolt-failed-fix-due").read_text())
        status["status"]["places"][0]["fixes"] = [{"number": 1, "name": "y-1", "place": "fix--y-1", "launched": 1794176400,
                                                   "cause": {"failed": {"submission": "412"}}, "ended": "live"}]
        fixes = self.in_flight("bolt-failed-fix-due", status)
        (y,) = plan.landing_rows(["y"], {"y": facts("y", fixes=fixes)}, {})
        assert (y["box"], y.get("takes_main")) == (False, None)
        assert y["why"] == ("held for a fix: Flume's landing fix y-1 makes the failed checks pass: check-full failed: tests:logic "
                            "3 failed (tests/py/test_landing.py) (y-1)")

    def test_a_row_held_by_its_refusal_says_flume_launches_its_landing_fix(self):
        """rail-cards "Due": y's landing was refused for a failed check at its head and its landing fix is due; the run
        record's Refused, written by landing_said, holds the row saying Flume launches its landing fix."""
        import runner
        from facts import ran
        from test_runner import rec
        requests = TestLandsDue().requests(rec(5, "land", "bolt/y", Of=1))
        launch = requests[0]
        l = runner.landing_of(launch, runner.lands_of(requests, launch), ran({1: "flume-0.19.0/bolt-failed-fix-due"}, label="swancloud",
                                                                            unplaced={5: "-"}))
        (y,) = plan.landing_rows(["y"], {"y": facts("y", H1)}, {"y": (H1, runner.landing_said(l))})
        assert y["box"] is False and y["why"].endswith("; Flume launches its landing fix")
        assert y["why"].startswith("landing rejected at abc1234, open for work: it waits for a fix on the bolt: landing refused, a check failed")

    def test_no_land_is_posted_while_it_runs_and_one_once_the_fix_that_took_main_in_has_landed(self):
        from facts import ran
        from test_runner import rec
        requests = TestLandsDue().requests(rec(5, "land", "bolt/y", Of=1))
        posted = [dict(work="bolt/y", card="req_1", head=H1[:7], request=5)]
        sent = {"bolt/y": ("req_1", H1[:7])}
        import runner
        for fixture in ("bolt-conflict-fixing", "bolt-forecast-fixing"):
            reads = ran({1: f"flume-0.19.0/{fixture}"}, label="swancloud", unplaced={5: "-"})
            (y,) = plan.landing_rows(["y"], {"y": facts("y", H1, fixes=runner.fixes_in_flight([], "y", requests, reads))}, {})
            assert runner.lands_due([y], sent, requests, reads, posted) == []
        reads = ran({1: "flume-0.19.0/bolt-fixed-landed"}, label="swancloud", unplaced={5: "-"})
        assert runner.fixes_in_flight([], "y", requests, reads) == {}
        assert runner.lands_due([box("y", H2)], sent, requests, reads, posted, work={"y": work()}) == [("bolt/y", 1)]


class TestCrossedTakesMain:
    """A crossed team's landing refused for a conflict with main launches its take-main fix with sluice's words, once,
    and its row says it takes main first (Decision 10 of teams-cross-to-flume-as-their-bolts-land, plan.8)."""
    MAIN, WORDS = "4d3d9be" + "0" * 33, "#137 conflict: README.md, plugin/lib/plan.py"

    @pytest.fixture(autouse=True)
    def ops(self, monkeypatch):
        monkeypatch.setenv("CREW_AGENT", "madswan-ops")

    def launched(self):
        """x, started, its unit a launched as a start launches it."""
        from facts import FactsWrite, flume_plan, madswan_fleet
        w = FactsWrite(flume_plan([("x", None, "flume")], [("a", "x", [], "unit", [])]), label="madswan")
        plan.reach_places(madswan_fleet(), w, "x")
        return w, "madswan"

    def test_a_landing_refused_for_a_conflict_launches_one_take_main_fix_with_sluices_words(self):
        """crew's read of x's landing finds Flume refusing it for a conflict with main at 4d3d9be (landing_read)."""
        import runner
        w, t = self.launched()
        act, work, given = runner.take_main(w.plan, plan.requests_of(w).recs("Request"), "x", t, self.MAIN, self.WORDS)
        assert (act, work, given["Repo"], given["Kind"], given["Name"], given["Base"], given["Recipient"]) == (
            "launch", "fix/x/take-main-4d3d9be", "crew", "fix", "x--take-main-4d3d9be", "bolt/x", "madswan/planner")
        assert given["Brief"] == (
            "Take main into the bolt: merge origin/main, at 4d3d9be, into this place, cut from bolt/x, resolving each conflicting "
            "path keeping both intents, main's and the bolt's; the merge queue refused the bolt's landing for its conflict with main: "
            "#137 conflict: README.md, plugin/lib/plan.py")
        assert given["Brief"].startswith(plan.TAKE_MAIN)

    def test_read_twice_it_launches_nothing_more(self):
        """A later read of the same refusal finds x--take-main-4d3d9be standing."""
        import runner
        w, t = self.launched()
        act, work, given = runner.take_main(w.plan, plan.requests_of(w).recs("Request"), "x", t, self.MAIN, self.WORDS)
        plan.request(w, act, work, **given)
        assert runner.take_main(w.plan, plan.requests_of(w).recs("Request"), "x", t, self.MAIN, self.WORDS) is None

    def test_its_row_says_it_takes_main_first(self):
        import runner
        w, t = self.launched()
        brief = runner.take_main(w.plan, plan.requests_of(w).recs("Request"), "x", t, self.MAIN, self.WORDS)[2]["Brief"]
        held = plan.refusals([submitted("x", "a" * 40, "#137 conflict: README.md, plugin/lib/plan.py")])
        x, = plan.landing_rows(["x"], {"x": facts("x", fixes={"fix/x/take-main-4d3d9be": brief})}, held)
        assert (x["box"], x["takes_main"], x["why"]) == (False, True, f'takes main first: take-main-4d3d9be taking main in: "{brief}"')


def test_a_bolt_the_user_left_forecast_to_conflict_with_main_keeps_its_box_marked_that_it_would_take_main_first():
    """rail-cards "A bolt the user left" and "Left, and main conflicts with it": no fix is started for it, so it is not
    held taking main first."""
    rows = plan.landing_rows(["y", "z"], {"y": facts("y"), "z": facts("z")}, {}, takes_main={"z": ("e4f5a6b0", ["README.md"])},
                             left={"z"})
    assert [(r["bolt"], r["box"], r["facts"].get("would_main")) for r in rows] == [
        ("y", True, None), ("z", True, ("e4f5a6b", ["README.md"]))]
    # a left bolt forecast clean is a row as any
    assert plan.landing_rows(["z"], {"z": facts("z")}, {}, takes_main={}, left={"z"})[0] == dict(bolt="z", box=True, facts=facts("z"))


def test_a_left_bolt_whose_landing_was_stopped_keeps_both_marks():
    """A stop holds nothing (rail-cards "A landing the runner or Flume stopped keeps its box"), and a left bolt
    forecast to conflict with main keeps its box: its row says both."""
    head = "a" * 40
    entries = [dict(submitted("z", head), Why="sluice exited 3", Outcome="stopped")]
    row, = plan.landing_rows(["z"], {"z": facts("z", head)}, {}, plan.stops(entries),
                             takes_main={"z": ("e4f5a6b0", ["README.md"])}, left={"z"})
    assert row["box"] and row["facts"]["would_main"] == ("e4f5a6b", ["README.md"])
    assert row["facts"]["stopped"] == (head, "sluice exited 3")


def test_a_left_bolt_with_a_fix_in_flight_or_sluices_refusal_is_held_as_before():
    """Those hold whatever the user chose (Decision 2)."""
    takes = {"y": ("e4f5a6b", ["README.md"]), "z": ("e4f5a6b", ["README.md"])}
    held = plan.refusals([submitted("z", "a" * 40, "bolt/z did not land: sluice found a conflict")])
    y, z = plan.landing_rows(["y", "z"], {"y": facts("y", fixes={"fix/y/gap": "A zone is missing."}), "z": facts("z")}, held,
                             takes_main=takes, left={"y", "z"})
    assert (y["box"], y["why"]) == (False, "held for a fix: A zone is missing. (fix/y/gap)")
    assert (z["box"], z["why"]) == (False, "landing rejected at aaaaaaa, open for work: it waits for a fix on the bolt: "
                                           "bolt/z did not land: sluice found a conflict")


def test_a_new_head_with_no_conflict_forecast_has_its_box_again():
    """rail-cards "The fix merges": the record's conflict was at the head the fix moved the bolt from."""
    recorded = [dict(Act="forecast", On=["bolt/y"], Heads="bolt/y@ccccccc main@2222222", Paths="README.md", Reached="told")]
    takes = {b: c for b in ["y"] for c in [plan.main_conflict(recorded, b, "d" * 40)] if c}
    row, = plan.landing_rows(["y"], {"y": facts("y", "d" * 40)}, {}, takes_main=takes)
    assert row["box"] and "takes_main" not in row


# ---------------------------------------------------------------------------------------------- the forecasts

def test_two_bolts_on_one_file_the_lower_row_names_the_one_above():
    paths = {("z", "y"): ["plugin/lib/plan.py"]}
    got = plan.row_forecasts(["y", "z"], lambda ours, theirs: paths.get((ours, theirs), []))
    assert got == {"y": [], "z": [("y", ["plugin/lib/plan.py"])]}


def test_a_bolt_behind_main_names_main_first_and_alone():
    """A bolt forecast to conflict with main takes main first (landing_rows), so it is forecast against main alone and
    no row below is forecast against it."""
    paths = {("y", "main"): ["README.md"], ("z", "main"): ["a"], ("z", "y"): ["b"], ("w", "y"): ["c"], ("w", "x"): ["d"]}
    got = plan.row_forecasts(["y", "z", "x", "w"], lambda ours, theirs: paths.get((ours, theirs), []))
    assert got == {"y": [("main", ["README.md"])], "z": [("main", ["a"])], "x": [], "w": [("x", ["d"])]}


def test_a_bolt_the_record_holds_taking_main_first_is_forecast_against_main_alone():
    """rail-cards "Raised again at the same heads": a row the run record holds taking main first is no row above another."""
    asked = []
    got = plan.row_forecasts(["y", "z"], lambda ours, theirs: asked.append((ours, theirs)) or (["b"] if (ours, theirs) == ("z", "y") else []),
                             held=["y"])
    assert got == {"y": [], "z": []} and ("z", "y") not in asked


def test_a_forecast_git_could_not_tell_is_kept_as_not_made():
    got = plan.row_forecasts(["y", "z"], lambda ours, theirs: None if "y" in (ours, theirs) else [])
    assert got == {"y": [("main", None)], "z": [("y", None)]}


def test_merge_trees_words_are_read_as_its_paths():
    assert plan.tree_paths(0, "abc\n") == []
    assert plan.tree_paths(1, "abc\nREADME.md\nplan.py\nREADME.md\n") == ["README.md", "plan.py"]
    assert plan.tree_paths(128, "fatal") is None


def origin_fetches(monkeypatch, refused=None):
    """The kit's GitHub fetched where its work runs as one try (plan.origin_fetched: ORIGIN_FETCH through host_run on
    the kit's host), standing in for host_run: each fetch's (script, folder) recorded, and refused in host_run's words,
    on <host>: <git's>, where refused gives git's."""
    fetches = []

    def fetch(fleet, host, script, *args):
        fetches.append((script, *args))
        if refused:
            plan.fail(f"on {host}: {refused}")
        return ""
    monkeypatch.setattr(plan, "host_run", fetch)
    return fetches


def test_a_bolt_branch_crew_cannot_read_is_said_and_its_box_kept(monkeypatch):
    """rail-cards "A bolt branch crew cannot read": the row's forecast is said as not made, with why, and holds
    nothing, since the rows' boxes are landing_rows' alone."""
    calls = []

    def git(fleet, t, where, *args, ok=(0,)):
        calls.append(args)
        if args[:2] == ("rev-parse", "--verify"):
            return (0, "f" * 40) if "bolt/z" in args[3] or "/main^" in args[3] else (1, "")
        return (0, "tree\n") if args[0] == "merge-tree" else (0, "")
    monkeypatch.setattr(plan, "kit_git", git)
    fetches = origin_fetches(monkeypatch)
    got, why, at = plan.forecast_rows(FLEET, "swancloud", "crew", ["y", "z"])
    assert got == {"y": [("main", None)], "z": [("y", None)]}
    assert why == {"y": "bolt/y is on no branch crew can read in /c/main on mac-studio, GitHub's or the host's",
                   "z": "bolt/y is on no branch crew can read in /c/main on mac-studio, GitHub's or the host's"}
    assert fetches == [(plan.ORIGIN_FETCH, "/c/main")] and not [c for c in calls if c[0] == "fetch"]
    assert [r for r in plan.landing_rows(["y", "z"], {"y": facts("y"), "z": facts("z")}, {}) if r["box"]] != []


def where_read(monkeypatch, policy):
    """forecast_rows over bolt y, whose GitHub copy is at 1… and the host's at 2…, GitHub's copy holding policy (None
    for no policy file): the commit each merge-tree was given for y."""
    trees = []

    def git(fleet, t, where, *args, ok=(0,)):
        if args[:2] == ("rev-parse", "--verify"):
            return 0, ("1" if "refs/remotes/origin/" in args[3] else "2") * 40
        if args[0] == "show":
            return (128, "fatal: path does not exist") if policy is None else (0, policy)
        if args[0] == "merge-tree":
            trees.append(args[-1])
        return (0, "tree\n") if args[0] == "merge-tree" else (0, "")
    monkeypatch.setattr(plan, "kit_git", git)
    origin_fetches(monkeypatch)
    return plan.forecast_rows(FLEET, "swancloud", "crew", ["y"]), trees


def test_a_bolt_on_github_is_forecast_where_it_lives(monkeypatch):
    """bolt-plan "crew reads a bolt at GitHub's copy where its policy names a remote, and else at the host's own": GitHub's copy, whose policy names origin for the bolt, not
    the host's lagging copy."""
    (got, why, at), trees = where_read(monkeypatch, '[branches."bolt/*"]\nremote = "origin"\n')
    assert why == {} and trees == ["1" * 40]


def test_a_bolt_kept_on_its_host_is_forecast_at_the_hosts_branch(monkeypatch):
    """bolt-plan "A bolt kept on its host": GitHub's copy names no remote for the bolt, or has no policy."""
    for policy in ("[branches.main]\nremote = \"origin\"\n", None):
        (got, why, at), trees = where_read(monkeypatch, policy)
        assert why == {} and trees == ["2" * 40]


def test_a_policy_crew_cannot_read_at_githubs_copy_is_said_and_forecasts_nothing(monkeypatch):
    (got, why, at), trees = where_read(monkeypatch, "[branches\n")
    assert got == {"y": [("main", None)]} and trees == []
    assert why["y"].startswith(".config/sluice.toml at origin/bolt/y is not TOML, so crew can't read bolt y: ")


def test_the_forecast_hands_back_the_revision_of_main_it_forecast_against(monkeypatch):
    """rail-cards "Main moves under an open card": the commit origin/main names after the fetch, which the merge-trees
    are made onto and the raise keeps."""
    (got, why, at), trees = where_read(monkeypatch, None)
    assert at == {"main": "1" * 40}


def test_a_forecast_whose_fetch_or_read_of_main_failed_hands_back_no_revision(monkeypatch):
    monkeypatch.setattr(plan, "kit_git", lambda fleet, t, where, *args, ok=(0,): (0, ""))
    origin_fetches(monkeypatch, refused="fatal: could not read from remote")
    got, why, at = plan.forecast_rows(FLEET, "swancloud", "crew", ["y"])
    assert at is None and got == {"y": [("main", None)]} and why["y"] == "on mac-studio: fatal: could not read from remote"

    def no_main(fleet, t, where, *args, ok=(0,)):
        return (1, "") if args[0] == "rev-parse" else (0, "")
    monkeypatch.setattr(plan, "kit_git", no_main)
    origin_fetches(monkeypatch)
    got, why, at = plan.forecast_rows(FLEET, "swancloud", "crew", ["y"])
    assert at is None and why == {"y": "/c/main on mac-studio has no origin/main to forecast against"}
    assert plan.forecast_rows(FLEET, "swancloud", "atlas-kit", ["y"])[2] is None


# ------------------------------------------------------------------------------------ when main moved under a card

M1, M2 = "a1b2c3d" + "0" * 33, "e4f5a6b" + "0" * 33


def test_a_card_main_moved_under_is_due_a_raise_and_one_it_did_not_is_not():
    """rail-cards "Main moves under an open card" and "Main has not moved"."""
    cards_ = [("swancloud", "crew"), ("swancloud", "swancloud")]
    mains = {("swancloud", "crew"): M2, ("swancloud", "swancloud"): M1}
    assert plan.landings_moved(cards_, mains, {("swancloud", "crew"): M1, ("swancloud", "swancloud"): M1}) == (
        [("swancloud", "crew")], [])


def test_a_card_with_no_revision_kept_is_due_a_raise():
    """A lost note costs one more raise."""
    assert plan.landings_moved([("swancloud", "crew")], {("swancloud", "crew"): M1}, {}) == ([("swancloud", "crew")], [])


def test_a_kit_whose_read_names_no_revision_is_unread_and_not_judged_moved():
    """read.2: an older gather leaves main_at out, and a kit not read has none."""
    cards_ = [("swancloud", "crew"), ("swancloud", "swancloud")]
    assert plan.landings_moved(cards_, {("swancloud", "crew"): None}, {("swancloud", "crew"): M1}) == (
        [], [("swancloud", "crew"), ("swancloud", "swancloud")])


def test_no_open_card_is_nothing_due():
    assert plan.landings_moved([], {("swancloud", "crew"): M2}, {("swancloud", "crew"): M1}) == ([], [])


# ------------------------------------------------------------------- a bolt's own work between two heads

def work_read(monkeypatch, moves, fetch=0, known=("abc1234", "d" * 40, "e" * 40), logs=None):
    """bolt_work over moves, git answering where the kit's forecasts are made: the fetch (origin_fetches) refused when
    fetch is set, rev-parse finding the commits known and each bolt on GitHub at e…, and each log its lines in logs, by
    (from, not); the git calls made, each fetch among them as (ORIGIN_FETCH, folder)."""
    calls = []

    def git(fleet, t, where, *args, ok=(0,)):
        calls.append(args)
        if args[:2] == ("rev-parse", "--verify"):
            rev = args[3].split("^")[0]
            return (0, "e" * 40) if rev.startswith("refs/remotes/origin/bolt/") else (0, rev) if rev in known else (1, "")
        if args[0] == "show":
            return 0, '[branches."bolt/*"]\nremote = "origin"\n'
        if args[0] == "log":
            return 0, (logs or {}).get((args[3], args[4]), "")
        return 0, ""
    monkeypatch.setattr(plan, "kit_git", git)
    fetches = origin_fetches(monkeypatch, refused="fatal: unable to access GitHub" if fetch else None)
    got = plan.bolt_work(FLEET, "swancloud", "crew", moves)
    return got, calls + fetches


def test_a_bolts_own_work_is_its_non_merge_commits_main_lacks_gained_and_lost_between_the_heads(monkeypatch):
    """rail-cards "A ticked bolt's approval stands while its own work is unchanged", Decision 1: one fetch, main read
    at GitHub's, each log both ways."""
    logs = {("d" * 40, "^abc1234"): "1a2b3c4 fix: keep the lease\n", ("abc1234", "^" + "d" * 40): ""}
    got, calls = work_read(monkeypatch, {"z": ("abc1234", "d" * 40)}, logs=logs)
    assert got == {"z": dict(head="d" * 40, gained=[("1a2b3c4", "fix: keep the lease")], lost=[], why=None)}
    assert calls.count((plan.ORIGIN_FETCH, "/c/main")) == 1 and not [c for c in calls if c[0] == "fetch"]
    assert ("log", "--no-merges", "--format=%h %s", "d" * 40, "^abc1234", "^refs/remotes/origin/main") in calls
    # a head now not given is read where the bolt lives, GitHub's copy, as the forecasts read it
    got, _ = work_read(monkeypatch, {"z": ("abc1234", None)})
    assert got == {"z": dict(head="e" * 40, gained=[], lost=[], why=None)}


def test_a_kit_no_runner_has_reported_reads_no_work_and_says_why(monkeypatch):
    monkeypatch.setattr(plan, "kit_git", lambda *a, **k: plan.fail("no git"))
    assert plan.bolt_work(FLEET, "swancloud", "boomdrive", {"z": ("abc1234", "d" * 40)}) == {"z": dict(
        head="d" * 40, gained=[], lost=[], why="no runner has reported taking boomdrive's work yet, so crew can't tell where it runs")}


def test_a_fetch_refused_reads_no_work_in_gits_words(monkeypatch):
    """rail-cards "crew cannot compare the heads"."""
    got, calls = work_read(monkeypatch, {"z": ("abc1234", "d" * 40)}, fetch=1)
    assert got["z"]["why"] == "on mac-studio: fatal: unable to access GitHub"
    assert not [c for c in calls if c[0] == "log"]


def test_a_sent_head_that_names_no_one_commit_reads_no_work_and_says_so(monkeypatch):
    got, calls = work_read(monkeypatch, {"z": ("0f0f0f0", "d" * 40)})
    assert got == {"z": dict(head="d" * 40, gained=[], lost=[],
                             why="your send's head, 0f0f0f0, names no one commit in /c/main on mac-studio")}
    assert not [c for c in calls if c[0] == "log"]


# ------------------------------------------------------------------------------------- what the raise does

H1, H2 = "abc1234" + "0" * 33, "def5678" + "0" * 33
TIMER = " every host's folder follows by swancloud's timer within minutes."


def box(bolt, head=H1):
    return dict(bolt=bolt, box=True, facts=facts(bolt, head))


def hold(bolt, why="held for a fix: one zone is missing (fix/y/gap)", head=H1):
    return dict(bolt=bolt, box=False, why=why, facts=facts(bolt, head))


def held_card(status, heads):
    """A kit's landings card ops holds as kit_card_state reads it, from the Heads its last post or change recorded."""
    text = " ".join(heads)
    return {"status": status, "heads": plan.card_heads(text), "taking": plan.heads_taking(text), "next": plan.heads_next(text)}


def waiting(*heads):
    return held_card("waiting", heads)


def answered(*heads):
    return held_card("answered", heads)


def work(gained=(), lost=(), why=None, head=H2):
    """A bolt's own work between the head sent and its head now, as bolt_work reads it."""
    return dict(head=head, gained=list(gained), lost=list(lost), why=why)


LEASE = ("1a2b3c4", "fix: keep the lease")


def test_a_send_stands_at_the_head_sent_or_where_the_bolts_own_work_is_the_same():
    """rail-cards "A ticked bolt's approval stands while its own work is unchanged"."""
    assert plan.send_stands("abc1234", H1, None)
    assert plan.send_stands("abc1234", H2, work())
    assert not plan.send_stands("abc1234", H2, work([LEASE]))
    assert not plan.send_stands("abc1234", H2, work(lost=[LEASE]))
    assert not plan.send_stands("abc1234", H2, work(why="git log in /c/main on mac-studio failed: fatal: bad object"))
    assert not plan.send_stands("abc1234", H2, None)


def test_a_bolt_asked_again_is_said_with_the_work_it_gained_or_lost_or_why_crew_cant_tell():
    """rail-cards "A ticked bolt whose own work changed is asked again, saying what changed"."""
    assert plan.work_said("z", "abc1234", H2, work([LEASE])) == (
        "z's head is now def5678, with work of its own since your send at abc1234: fix: keep the lease")
    assert plan.work_said("z", "abc1234", H2, work(lost=[LEASE])) == (
        "z's head is now def5678, no longer holding work of its own your send at abc1234 held: fix: keep the lease")
    assert plan.work_said("z", "abc1234", H2, work([LEASE], [("9f8e7d6", "test: wait for the lock")])) == (
        "z's head is now def5678, with work of its own since your send at abc1234: fix: keep the lease, and no longer "
        "holding: test: wait for the lock")
    assert plan.work_said("z", "abc1234", H2, work(why="git fetch in /c/main on mac-studio failed: fatal: no route")) == (
        "z's head is now def5678, but crew could not tell whether z's own work changed since your send at abc1234: "
        "git fetch in /c/main on mac-studio failed: fatal: no route")


def test_a_bolt_asked_again_names_five_commits_of_each_list_and_how_many_more():
    six = [(f"{n}000000", f"fix: part {n}") for n in range(1, 7)]
    assert plan.work_said("z", "abc1234", H2, work(six)) == (
        "z's head is now def5678, with work of its own since your send at abc1234: fix: part 1; fix: part 2; "
        "fix: part 3; fix: part 4; fix: part 5; and 1 more")


def test_no_row_that_can_land_and_no_card_is_nothing():
    assert plan.landings_step([hold("y")], None, None, {"y"}) == ("none",)
    assert plan.landings_step([], None, None, set()) == ("none",)


def test_a_waiting_card_with_no_row_that_can_land_is_withdrawn_saying_why():
    assert plan.landings_step([hold("y")], waiting("y@abc1234"), None, {"y"}) == (
        "withdraw", "every bolt waiting to land is held: y, held for a fix: one zone is missing (fix/y/gap)")
    assert plan.landings_step([], waiting("y@abc1234"), None, set()) == ("withdraw", "no bolt waits to land on its main")


def test_rows_that_can_land_and_no_card_post_one():
    assert plan.landings_step([box("y"), hold("z")], None, None, {"y", "z"}) == ("post", [])


def test_a_waiting_card_whose_rows_head_moved_is_changed_in_place():
    step = plan.landings_step([box("y"), box("z", H2)], waiting("y@abc1234", "z@abc1234"), None, {"y", "z"})
    assert step == ("change", "z's head is now def5678", False, [])


def test_a_second_bolt_proven_changes_the_cards_form_so_it_is_followed():
    step = plan.landings_step([box("y"), box("z")], waiting("y@abc1234"), None, {"y", "z"})
    assert step == ("change", "z reads proven and joins the card", True, [])


def test_a_row_held_or_gone_is_named_and_the_events_own_note_comes_first():
    step = plan.landings_step([box("y"), hold("z")], waiting("y@abc1234", "z@abc1234", "w@abc1234"), None, {"y", "z"},
                              note=f"y: {plan.RELINKED}")
    assert step == ("change", f"y: {plan.RELINKED}; z is held for a fix: one zone is missing (fix/y/gap); "
                              "w no longer waits to land", True, [])


def test_a_waiting_card_nothing_changed_is_left():
    assert plan.landings_step([box("y")], waiting("y@abc1234"), None, {"y"}) == ("leave",)


def test_a_bolt_left_on_the_last_send_stays_unticked_while_its_head_stands():
    assert plan.landings_step([box("y"), box("z")], waiting("y@abc1234", "z@abc1234:left"), None, {"y", "z"},
                              note="x")[3] == ["z"]
    assert plan.landings_step([box("y"), box("z", H2)], waiting("y@abc1234", "z@abc1234:left"), None, {"y", "z"})[3] == []


def test_an_answered_card_is_left_while_a_ticked_bolt_is_still_in_the_plan_and_not_held():
    assert plan.landings_step([box("y"), box("z")], answered("y@abc1234", "z@abc1234"), ["y", "z"], {"y", "z"}) == ("leave",)
    assert plan.landings_step([box("z")], answered("y@abc1234", "z@abc1234"), ["y", "z"], {"z"}) == ("leave",)
    # z landed and not yet closed: in the plan, no row now, and still waited for
    assert plan.landings_step([hold("y")], answered("y@abc1234", "z@abc1234"), ["y", "z"], {"y", "z"}) == ("leave",)


def test_once_every_ticked_bolt_landed_it_is_closed_naming_where_and_nothing_follows():
    step = plan.landings_step([], answered("y@abc1234", "z@abc1234"), ["y", "z"], set(), landed={"y": "1" * 40, "z": "2" * 40})
    assert step == ("close", "Landed on GitHub's main: y at 1111111 and z at 2222222; every host's folder follows by "
                             "swancloud's timer within minutes.", None, [])


def test_one_left_out_is_closed_saying_so_and_a_new_card_follows_with_it_unticked():
    step = plan.landings_step([box("z")], answered("y@abc1234", "z@abc1234"), ["y"], {"z"}, landed={"y": "1" * 40})
    assert step == ("close", f"Landed on GitHub's main: y at 1111111;{TIMER} Left: z.", ["z"], [])


def test_a_bolt_still_in_the_plan_is_left_one_landed_is_closed_naming_where_and_one_gone_unlanded_left_the_plan():
    """read.5, plan.2 (an-act-carries-its-entry-in-its-own-commit): a landings card's close reads the branch at its tip,
    where bolt.land's write carries its entry in its own commit: a bolt still in the plan is still landing and its card
    left; one whose landing is recorded is closed saying where it landed; and one gone from the plan with no landing
    recorded is the one said to have landed or left the plan."""
    assert plan.landings_step([], answered("y@abc1234"), ["y"], {"y"}) == ("leave",)
    assert plan.landings_step([], answered("y@abc1234"), ["y"], set(), landed={"y": "1" * 40}) == (
        "close", f"Landed on GitHub's main: y at 1111111;{TIMER}", None, [])
    assert plan.landings_step([], answered("y@abc1234"), ["y"], set()) == ("close", "Landed or left the plan: y.", None, [])


STANDS = ("your send stands for it: it lands once a fix on it has only taken main in and it reads proven at its new head, "
          "with nothing asked.")
REFUSED = "landing rejected at abc1234, open for work: it waits for a fix on the bolt: x"


def test_a_ticked_bolt_sluice_refused_is_held_and_the_rest_close_the_card():
    """rail-cards "A ticked bolt held at the close": the close keeps the send for z, saying so."""
    step = plan.landings_step([hold("z", REFUSED)], answered("y@abc1234", "z@abc1234", "w@abc1234"), ["y", "z", "w"], {"z"},
                              landed={"y": "1" * 40, "w": "3" * 40})
    assert step == ("close", f"Landed on GitHub's main: y at 1111111 and w at 3333333;{TIMER} Held: z, {REFUSED}; {STANDS}",
                    None, [("z", "abc1234")])


def test_a_send_holding_only_a_held_bolt_closes_keeping_it_and_one_whose_work_changed_is_not_kept():
    step = plan.landings_step([hold("z", REFUSED)], answered("z@abc1234"), ["z"], {"z"})
    assert step == ("close", f"Held: z, {REFUSED}; {STANDS}", None, [("z", "abc1234")])
    held = "held for a fix: the lease (fix/z/lease)"
    step = plan.landings_step([hold("z", held, H2)], answered("z@abc1234"), ["z"], {"z"}, work={"z": work([LEASE])})
    assert step == ("close", f"Held: z, {held}; z's head is now def5678, with work of its own since your send at abc1234: "
                             "fix: keep the lease, so a card asks for it again once it reads proven.", None, [])
    # held at a new head its own work is the same at: kept
    step = plan.landings_step([hold("z", held, H2)], answered("z@abc1234"), ["z"], {"z"}, work={"z": work()})
    assert step[3] == [("z", "abc1234")]
    # followed while y still lands: the follow's send keeps the held z beside y
    step = plan.landings_step([box("y"), hold("z", REFUSED), box("w")], answered("y@abc1234", "z@abc1234"), ["y", "z"],
                              {"y", "z", "w"})
    assert (step[0], step[3]) == ("follow", [("y", "abc1234"), ("z", "abc1234")]) and f"Held: z, {REFUSED}; {STANDS}" in step[1]


def taking_main(bolt):
    return dict(hold(bolt, MAIN_FIRST), takes_main=True)


def test_a_row_taking_main_first_beside_one_that_can_land_is_a_row_of_the_card():
    """rail-cards "A row taking main first stays on the card": shown beside a row that can land, marked so, and held off
    the card with the rest while none can, or while an earlier send lands it."""
    rows = [box("y"), taking_main("z"), hold("w")]
    assert [r["bolt"] for r in plan.card_rows(rows)] == ["y", "z"]
    assert plan.card_rows([taking_main("z"), hold("w")]) == []
    assert [r["bolt"] for r in plan.card_rows([box("y"), dict(taking_main("z"), sent=True)])] == ["y"]


def test_a_row_coming_to_take_main_first_and_back_changes_the_card_in_place():
    """rail-cards "One of two" and "Taking main in and back, one card": the card's count stands, so its form does."""
    assert plan.landings_step([box("y"), taking_main("z")], waiting("y@abc1234", "z@abc1234"), None, {"y", "z"}) == (
        "change", f"z {MAIN_FIRST}", False, [])
    assert plan.landings_step([box("y"), taking_main("z")], waiting("y@abc1234", "z@abc1234:main"), None, {"y", "z"}) == ("leave",)
    assert plan.landings_step([box("y"), box("z", H2)], waiting("y@abc1234", "z@abc1234:main"), None, {"y", "z"}) == (
        "change", "z's head is now def5678; z can land again", False, [])
    # a bolt taking main first joins a card of one: its form changes, so it is followed
    assert plan.landings_step([box("y"), taking_main("z")], waiting("y@abc1234"), None, {"y", "z"}) == (
        "change", f"z joins the card and {MAIN_FIRST}", True, [])


def test_under_a_hold_a_close_says_the_send_stands_and_asks_nothing():
    """rail-cards "A send under a hold" (Decision 6 of a-proven-bolt-lands-on-proof): while a hold stands no land is asked,
    so an answered card that follows says the user's send stands for what it lands, landing it once the hold is lifted,
    never that it was asked of the runner."""
    card = answered("y@abc1234")
    step = plan.landings_step([box("y"), box("z")], card, ["y"], {"y", "z"}, hold="the hold on crew's landings")
    assert step == ("follow", "Your send stands for y: no land is asked while the hold on crew's landings stands, and crew asks the "
                              "runner to land it once it is lifted. Since your send, z reads proven, and the card that follows asks "
                              "for it.", [], [("y", "abc1234")])
    assert "Asked of the runner" not in step[1]


def test_a_row_shown_taking_main_first_and_left_unticked_is_no_bolt_the_user_left():
    """rail-cards "A row taking main first stays on the card": crew unticked it, not they."""
    card = answered("y@abc1234", "z@abc1234:main")
    assert plan.landings_step([box("y"), taking_main("z")], card, ["y"], {"y", "z"}) == ("leave",)
    step = plan.landings_step([taking_main("z")], card, ["y"], {"z"}, landed={"y": "1" * 40})
    assert step == ("close", f"Landed on GitHub's main: y at 1111111;{TIMER}", None, [])
    # back from taking main in while y still lands: a card follows asking for it
    step = plan.landings_step([box("y"), box("z")], card, ["y"], {"y", "z"})
    assert step == ("follow", "Asked of the runner as you ticked: y. Since your send, z reads proven, and the card that follows asks for it.",
                    [], [("y", "abc1234")])
    assert plan.left_now(card, ["y"], {"y": H1, "z": H1}, {}, []) == {}
    # ticked while it took main in: their send stands for it
    assert plan.landings_step([box("y"), box("z")], card, ["y", "z"], {"y", "z"}) == ("leave",)


def test_a_ticked_bolt_then_taking_main_first_leaves_the_card_its_send_standing():
    """rail-cards "Ticked, then forecast to conflict" and "Ticked beside one that lands"."""
    assert plan.landings_step([taking_main("y")], answered("y@abc1234"), ["y"], {"y"}) == ("leave",)
    assert plan.landings_step([taking_main("y")], answered("y@abc1234", "z@abc1234"), ["y", "z"], {"y"},
                              landed={"z": "2" * 40}) == ("leave",)


def test_a_ticked_bolt_taking_main_first_is_kept_on_the_send_when_a_new_card_follows():
    step = plan.landings_step([taking_main("y"), box("w")], answered("y@abc1234", "z@abc1234"), ["y", "z"], {"y", "z", "w"})
    assert step == ("follow", "Asked of the runner as you ticked: z. Taking main in first, your send standing for it: y. Since your "
                              "send, w reads proven, and the card that follows asks for it.", [], [("y", "abc1234"), ("z", "abc1234")])


def test_a_ticked_bolt_taking_main_first_whose_own_work_changed_keeps_no_send():
    """A send stands while the bolt takes main in only for the work the user sent (send_stands): one that gained work
    of its own is held, and asked for again once it reads proven."""
    y = dict(taking_main("y"), facts=facts("y", H2))
    work = {"y": dict(head=H2, gained=[("1a2b3c4", "fix: keep the lease")], lost=[], why=None)}
    step = plan.landings_step([y], answered("y@abc1234"), ["y"], {"y"}, work=work)
    assert step == ("close", f"Held: y, {MAIN_FIRST}; y's head is now def5678, with work of its own since your send at "
                             "abc1234: fix: keep the lease, so a card asks for it again once it reads proven.", None, [])


def test_a_ticked_bolt_held_for_any_other_fix_is_held_and_the_card_closed_keeping_its_send():
    """Only a bolt taking main in leaves the card; one held for another fix closes it, its send kept on the close."""
    step = plan.landings_step([hold("y")], answered("y@abc1234"), ["y"], {"y"})
    assert step == ("close", "Held: y, held for a fix: one zone is missing (fix/y/gap); your send stands for it: it lands "
                             "once a fix on it has only taken main in and it reads proven at its new head, with nothing asked.", None,
                    [("y", "abc1234")])


def test_a_waiting_card_no_row_of_which_can_land_is_withdrawn_whatever_note_the_event_carries():
    """No word in a pane lands a bolt (record 0056 point 5): a waiting card no row of which can land is withdrawn, never
    closed as answered in a pane."""
    assert plan.landings_step([], waiting("y@abc1234"), None, set(), note="Landed on the user's word") == (
        "withdraw", "no bolt waits to land on its main")


def test_a_bolt_proven_after_the_answer_is_no_row_of_it_and_a_new_card_follows_it_with_the_rest():
    step = plan.landings_step([box("y"), box("z"), box("w")], answered("y@abc1234", "z@abc1234"), ["y"], {"y", "z", "w"})
    assert step == ("follow", "Asked of the runner as you ticked: y. Left: z. Since your send, w reads proven, and the card that "
                              "follows asks for it.", ["z"], [("y", "abc1234")])


def test_a_rows_next_mark_is_read_as_a_row_with_no_box():
    """rail-cards "A landings card holds five boxes and the rest of its rows wait on its face": a row the card showed
    with no box is recorded :next, after :left or :main or alone, and read back so by the next raise."""
    text = "a@abc1234 b@abc1234:left:next c@abc1234:main:next d@abc1234:next"
    assert plan.card_heads(text) == [("a", "abc1234", False), ("b", "abc1234", True), ("c", "abc1234", False),
                                     ("d", "abc1234", False)]
    assert plan.heads_taking(text) == {"c"}
    assert plan.heads_next(text) == {"b", "c", "d"}
    assert plan.offered_boxes(text) == ["land:a"]
    assert plan.heads_taking("c@abc1234:main") == {"c"} and plan.heads_next("c@abc1234:main b@abc1234:left") == set()


EIGHT = [f"b{i}@abc1234" for i in range(1, 6)] + [f"b{i}@abc1234:next" for i in range(6, 9)]


def test_a_row_coming_to_a_box_changes_the_waiting_card_in_place():
    """rail-cards "A row coming to a box or losing one changes the waiting landings card in place": "A boxed row is held
    for a fix"."""
    rows = [box("b1"), hold("b2")] + [box(f"b{i}") for i in range(3, 9)]
    step = plan.landings_step(rows, waiting(*EIGHT), None, {f"b{i}" for i in range(1, 9)})
    assert step == ("change", "b2 is held for a fix: one zone is missing (fix/y/gap); b6 has a box now", False, [])
    # and back: b2 can land again, so b6 waits for a box once more
    back = waiting(*([f"b{i}@abc1234" for i in (1, 3, 4, 5, 6)] + ["b7@abc1234:next", "b8@abc1234:next"]))
    step = plan.landings_step([box(f"b{i}") for i in range(1, 9)], back, None, {f"b{i}" for i in range(1, 9)})
    assert step == ("change", "b2 reads proven and joins the card; b6 waits for a box", False, [])


def test_a_row_with_no_box_whose_head_moves_changes_the_card_and_keeps_it_with_no_box():
    """rail-cards "A row waiting for a box moves its head"."""
    rows = [box(f"b{i}") for i in range(1, 7)] + [box("b7", H2), box("b8")]
    step = plan.landings_step(rows, waiting(*EIGHT), None, {f"b{i}" for i in range(1, 9)})
    assert step == ("change", "b7's head is now def5678", False, [])
    assert plan.landings_step([box(f"b{i}") for i in range(1, 9)], waiting(*EIGHT), None, {f"b{i}" for i in range(1, 9)}) == ("leave",)


def test_a_send_with_rows_waiting_for_a_box_is_followed_at_once_by_a_card_asking_for_them():
    """rail-cards "A send with rows waiting for a box is followed at once by a card asking for them": "Five ticked, three
    waiting"."""
    ticked = [f"b{i}" for i in range(1, 6)]
    step = plan.landings_step([box(f"b{i}") for i in range(1, 9)], answered(*EIGHT), ticked, {f"b{i}" for i in range(1, 9)})
    assert step == ("follow", "Asked of the runner as you ticked: b1, b2, b3, b4 and b5. b6, b7 and b8 had no box on this "
                              "card, and the card that follows asks for them.", [], [(b, "abc1234") for b in ticked])
    assert "Left:" not in step[1]
    # beside a row proven since the send
    rows = [box(f"b{i}") for i in range(1, 9)] + [box("b9")]
    step = plan.landings_step(rows, answered(*EIGHT), ticked, {f"b{i}" for i in range(1, 10)})
    assert step[1].endswith("Since your send, b9 reads proven; b6, b7 and b8 had no box on this card, and the card that "
                            "follows asks for them.")


def test_a_left_row_waiting_for_a_box_stays_left():
    """rail-cards "A left row that waited for a box"."""
    heads = ["b1@abc1234:left:next"] + [f"b{i}@abc1234" for i in range(2, 7)] + ["b7@abc1234:next"]
    now = {f"b{i}": H1 for i in range(1, 8)}
    assert plan.left_now(answered(*heads), [f"b{i}" for i in range(2, 7)], now, {}, []) == {"b1": "abc1234"}
    # b7 waited for a box alone, unticked: not left
    assert "b7" not in plan.left_now(answered(*heads), [f"b{i}" for i in range(2, 7)], now, {}, [])
    # while the card waits, the mark alone says so
    assert plan.left_now(waiting(*heads), None, now, {}, []) == {"b1": "abc1234"}


STOP = "check:dagger could not run: the Dagger engine did not answer"


def stopped_box(bolt, head=H1, words=STOP):
    """A row that can land whose last landing at its head sluice or its host stopped (landing_rows)."""
    return dict(bolt=bolt, box=True, facts=dict(facts(bolt, head), stopped=(head, words)))


def test_an_answered_card_whose_ticked_bolts_landing_was_stopped_closes_naming_it_and_its_send_is_spent():
    """rail-cards "A stopped row on the same send" (crew-lands-each-bolt-through-flumes-base-place, Decision 7): the
    runner or Flume stopped z's land on the user's send, nothing of the bolt's; the send is spent, so the card they
    answered closes naming the stop, keeping no send, and the card that follows asks for z again with its box."""
    step = plan.landings_step([stopped_box("z")], answered("z@abc1234"), ["z"], {"z"})
    assert step == ("close", f"z's landing at abc1234 was stopped, nothing of the bolt's: {STOP}; your send of it is spent, and the "
                             "card that follows asks for it again.", [], [])


def test_a_stopped_bolt_beside_one_proven_since_closes_the_card_and_the_one_that_follows_asks_for_both():
    step = plan.landings_step([stopped_box("z"), box("w")], answered("z@abc1234"), ["z"], {"z", "w"})
    assert step == ("close", f"z's landing at abc1234 was stopped, nothing of the bolt's: {STOP}; your send of it is spent, and the "
                             "card that follows asks for it again. Since your send, w reads proven, and the card that follows asks "
                             "for it.", [], [])
    assert plan.rows_unsent([stopped_box("z"), box("w")], plan.landings_sent([], "land/crew", "swancloud-ops")) == (
        [stopped_box("z"), box("w")], [], [])


def test_crew_card_read_says_what_stopped_a_bolt_the_send_lands_naming_no_land_for_it():
    """rail-cards "A landing the runner or Flume stopped keeps its box", "The landings card's read prints the lands crew
    posted": crew card read land/crew says what stopped z's last landing and
    at which head, that it lands again only on the user's next send, and names no land of it, its land being spent; a
    bolt it does not land says nothing, nor does one whose last landing was not stopped."""
    sent = {"status": "answered", "turn": "agent", "answer": {"choiceIds": ["land:y", "land:z"]}}
    heads = plan.card_heads("y@abc1234 z@abc1234")
    stopped = plan.stops([dict(submitted("z", H2), Why=STOP, Outcome="stopped"), dict(submitted("w", H1), Why="x", Outcome="stopped"),
                          dict(submitted("y", H1), Why="x", Outcome="stopped"), submitted("y", H1, "sluice: y conflicts")])
    assert plan.landing_lines("swancloud", sent, heads, [], [], stopped) == [
        "  to land, in the card's order: y and z",
        f"  z's last landing at def5678 was stopped, nothing of the bolt's: {STOP}; it lands again only on the user's "
        "next send",
        "  y: no land is posted for it yet: crew's next raise of the card posts it"]
    assert plan.landing_lines("swancloud", sent, heads, [], [], stopped, posted={"y": "57", "z": "41"})[-1] == (
        "  y: asked of the runner to land, request 57")
    assert plan.landing_lines("swancloud", sent, heads) == plan.landing_lines("swancloud", sent, heads, [], [], {})
    assert plan.landing_lines("swancloud", {}, [], ["z"], [], stopped)[1].startswith("  z's last landing at def5678 was stopped")


def test_a_ticked_bolt_proven_again_at_a_new_head_is_asked_again_rather_than_waited_for():
    """rail-cards "A fix adds a commit": the card that follows asks for y, saying what it gained."""
    gained = {"y": work([LEASE])}
    step = plan.landings_step([box("y", H2), box("z")], answered("y@abc1234", "z@abc1234"), ["y", "z"], {"y", "z"}, work=gained)
    assert step == ("follow", "Asked of the runner as you ticked: z. Since your send, y's head is now def5678, with work of its own "
                              "since your send at abc1234: fix: keep the lease, and the card that follows asks for it.",
                    [], [("z", "abc1234")])
    step = plan.landings_step([box("y", H2)], answered("y@abc1234"), ["y"], {"y"}, work=gained)
    assert step == ("close", "Since your send, y's head is now def5678, with work of its own since your send at abc1234: "
                             "fix: keep the lease, and the card that follows asks for it.", [], [])


def test_a_ticked_bolt_that_only_took_main_in_is_waited_for_on_the_same_send():
    """rail-cards "The head moves by taking main in before the landing": the card is left as it is."""
    step = plan.landings_step([box("y"), box("z", H2)], answered("y@abc1234", "z@abc1234"), ["y", "z"], {"y", "z"},
                              work={"z": work()})
    assert step == ("leave",)
    # once y has landed and z is still to be submitted, the send still lands z: left too
    assert plan.landings_step([box("z", H2)], answered("y@abc1234", "z@abc1234"), ["y", "z"], {"z"},
                              work={"z": work()}) == ("leave",)
    # and once z lands too, the card closes, nothing asked again
    assert plan.landings_step([], answered("y@abc1234", "z@abc1234"), ["y", "z"], set(),
                              landed={"y": "1" * 40, "z": "2" * 40})[0] == "close"


def test_a_ticked_bolt_whose_work_crew_cannot_read_is_asked_again_saying_why():
    """rail-cards "crew cannot compare the heads"."""
    why = "git fetch -q origin in /c/main on mac-studio failed: fatal: unable to access GitHub"
    step = plan.landings_step([box("z", H2)], answered("z@abc1234"), ["z"], {"z"}, work={"z": work(why=why)})
    assert step == ("close", f"Since your send, z's head is now def5678, but crew could not tell whether z's own work "
                             f"changed since your send at abc1234: {why}, and the card that follows asks for it.", [], [])


def test_a_bolt_left_on_the_send_is_ticked_on_the_card_that_follows_once_its_head_moved():
    step = plan.landings_step([box("z", H2)], answered("y@abc1234", "z@abc1234"), ["y"], {"z"}, landed={"y": "1" * 40})
    assert step == ("close", f"Landed on GitHub's main: y at 1111111;{TIMER} Left: z. Since your send, z's head is now "
                             "def5678, and the card that follows asks for it.", [], [])


def test_the_bolts_a_followed_send_still_lands_are_no_row_of_any_card_after_it_while_their_head_stands():
    closes = [dict(Act="card.close", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234 z@abc1234"),
              dict(Act="card.close", Key="land/crew", By="swancloud-ops", Card="req_k2", Heads="z@def5678"),
              dict(Act="card.close", Key="land/crew", By="crw-1-conductor", Card="req_b1", Heads="w@abc1234"),
              dict(Act="card.close", Key="land/crew", By="swancloud-ops", Card="req_k3", Heads="w@abc1234", Refused="x")]
    sent = plan.landings_sent(closes, "land/crew", "swancloud-ops")
    assert sent == {"y": "abc1234", "z": "def5678"}
    rows = [box("y"), box("z"), hold("x"), box("w")]
    # z moved from the head sent with its own work unread, which holds no send (read.1); x is held, a row with no box
    unread = "but crew could not tell whether {b}'s own work changed since your send at {at}: crew read none of its work"
    assert plan.rows_unsent(rows, sent) == ([box("z"), hold("x"), box("w")], ["y"], [
        ("z", "z's head is now abc1234, " + unread.format(b="z", at="def5678"))])
    assert plan.rows_unsent([box("y", H2), hold("z")], sent) == ([box("y", H2), hold("z")], [], [
        ("y", "y's head is now def5678, " + unread.format(b="y", at="abc1234"))])
    assert plan.landings_sent([], "land/crew", "swancloud-ops") == {}


def test_a_sent_bolt_that_only_took_main_in_is_no_row_and_one_whose_work_changed_is_a_row_saying_so():
    """rail-cards "A refused bolt takes main in" and "A fix adds a commit"."""
    sent = {"y": "abc1234", "z": "abc1234"}
    rows = [box("y", H2), box("z", H2)]
    assert plan.rows_unsent(rows, sent, {"y": work(), "z": work([LEASE])}) == ([box("z", H2)], ["y"], [
        ("z", "z's head is now def5678, with work of its own since your send at abc1234: fix: keep the lease")])


def test_a_send_whose_card_followed_before_ops_read_it_is_read_beside_the_card_that_followed():
    """The card ops reads under land/<kit> is the one that followed: the send it closed still lands its bolts first."""
    waits = {"status": "pending", "turn": "you"}
    heads = plan.card_heads("w@abc1234")
    assert plan.landing_lines("swancloud", waits, heads, ["y"]) == [
        "  to land on the user's send of an earlier card: y", "  y: no land is posted for it yet: crew's next raise of the card posts it"]
    sent = {"status": "answered", "turn": "agent", "answer": {"approved": True}}
    assert plan.landing_lines("swancloud", sent, heads, ["y", "z"]) == [
        "  to land on the user's send of an earlier card: y and z", "  to land, in the card's order: w",
        "  y: no land is posted for it yet: crew's next raise of the card posts it", "  z: no land is posted for it yet: crew's next raise of the card posts it", "  w: no land is posted for it yet: crew's next raise of the card posts it"]
    none = {"status": "answered", "turn": "agent", "answer": {"choiceIds": []}}
    assert plan.landing_lines("swancloud", none, plan.card_heads("w@abc1234 v@abc1234"), ["y"]) == [
        "  to land on the user's send of an earlier card: y", "  no bolt ticked on this card: nothing of it lands",
        "  y: no land is posted for it yet: crew's next raise of the card posts it"]


def test_what_an_earlier_send_still_lands_leaves_out_the_landed_the_asked_again_and_the_refused_at_its_head():
    sent = {"y": "abc1234", "z": "abc1234", "x": "abc1234", "v": "abc1234", "u": "abc1234"}
    refused = {"x": ("abc1234" + "0" * 33, "sluice: conflict in a.py"), "u": ("def5678", "sluice: a check failed")}
    # v landed and left the plan, z's own work changed at its new head, x was refused at its head now, the head sent;
    # u's refusal was at another head, which holds nothing
    now = {"y": H1, "z": H2, "x": H1, "u": H1}
    assert plan.sent_left(sent, now, {"y", "z", "x", "u"}, refused, {"z": work([LEASE])}) == (["y", "u"], [])
    assert plan.sent_left({}, {}, {"y"}, {}) == ([], [])


def test_an_earlier_send_lands_a_refused_bolt_once_its_fix_only_took_main_in_and_names_one_it_cant_tell_of():
    """rail-cards "The landings card's read prints the lands crew posted", with no card open: an earlier send still
    lands a refused bolt once its fix only took main in, and a bolt whose head crew cannot read is named."""
    sent = {"z": "abc1234", "w": "abc1234", "q": "abc1234"}
    refused = {"z": ("abc1234" + "0" * 33, "sluice: conflict in plugin/lib/plan.py")}
    unread = "bolt/w is on no branch crew can read in /c/main on mac-studio, GitHub's or the host's"
    fetch = "git fetch -q origin in /c/main on mac-studio failed: fatal: unable to access GitHub"
    got = plan.sent_left(sent, {"z": H2, "w": None, "q": H2}, {"z", "w", "q"}, refused,
                         {"z": work(), "w": work(why=unread, head=None), "q": work(why=fetch)})
    assert got == (["z"], [("w", unread), ("q", fetch)])


class WorkActs:
    """A stand-in for the work read (CardActs.work): each bolt's head now and its own work as heads gives them, the
    moves it was asked for recorded."""

    def __init__(self, heads):
        self.heads, self.asked = heads, []

    def work(self, label, kit, moves):
        self.asked.append(moves)
        return {b: self.heads.get(b) or work(why=f"bolt/{b} is on no branch crew can read", head=None) for b in moves}


def test_the_read_of_an_earlier_send_reads_the_plan_only_when_one_stands_and_refuses_when_it_cant(monkeypatch):
    closes = [dict(Act="card.close", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234 q@abc1234")]
    read, acts = [], WorkActs({"y": work(head=H1)})
    monkeypatch.setattr(plan, "plan_of", lambda fleet, label: read.append(label))
    assert plan.landings_earlier(FLEET, "swancloud", "crew", "land/crew", "swancloud-ops", [], [], acts) == ([], []) and not read
    with pytest.raises(crew.Refusal, match="^swancloud/main could not be read, so what an earlier send on land/crew still lands"):
        plan.landings_earlier(FLEET, "swancloud", "crew", "land/crew", "swancloud-ops", closes, [], acts)
    bolts = [plan.Rec("Bolt", [("Bolt", "y"), ("Repo", "crew")]), plan.Rec("Bolt", [("Bolt", "q"), ("Repo", "swancloud")])]
    monkeypatch.setattr(plan, "plan_of", lambda fleet, label: argparse.Namespace(bolts=lambda: bolts))
    assert plan.landings_earlier(FLEET, "swancloud", "crew", "land/crew", "swancloud-ops", closes, [], acts) == (["y"], [])
    assert acts.asked == [{"y": ("abc1234", None)}]  # one read, of the sent bolts the plan holds of the kit
    # a bolt on a row of the card read now is that card's to ask for
    assert plan.landings_earlier(FLEET, "swancloud", "crew", "land/crew", "swancloud-ops", closes,
                                 plan.card_heads("y@def5678"), acts) == ([], [])


def read_unopened(monkeypatch, capsys, closes, works, json=False):
    """crew card read land/crew as swancloud-ops, who holds no card under it on this host, after closes, the plan
    holding y and z of crew, each bolt's head now and own work as works gives them: what it printed."""
    bolts = [plan.Rec("Bolt", [("Bolt", b), ("Repo", "crew")]) for b in ("y", "z")]
    monkeypatch.setattr(plan, "plan_of", lambda fleet, label: argparse.Namespace(bolts=lambda: bolts))
    monkeypatch.setattr(plan, "card_asker", lambda fleet, a: ("swancloud", "swancloud-ops"))
    monkeypatch.setattr(crew, "this_host", lambda: "mac-studio")
    monkeypatch.setattr(cards, "host_entries", lambda record, label, host: closes)
    monkeypatch.setattr(plan, "bolt_work", lambda fleet, label, kit, moves: WorkActs(works).work(label, kit, moves))
    plan.card_read(FLEET, argparse.Namespace(key="land/crew", label=None, json=json, sub="read"))
    return capsys.readouterr().out


def test_with_no_card_open_ops_reads_what_an_earlier_send_still_lands_and_the_command_that_lands_it(monkeypatch, capsys):
    """rail-cards "The landings card's read prints the lands crew posted", with no card open: refuses nothing, and
    names the land crew's next raise posts, no command."""
    closes = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234 z@abc1234"),
              dict(Act="card.close", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="z@abc1234")]
    assert read_unopened(monkeypatch, capsys, closes, {"z": work()}) == (
        "card land/crew: no landings card of crew is open\n"
        "  to land on the user's send of an earlier card: z\n"
        "  z: no land is posted for it yet: crew's next raise of the card posts it\n")


def test_with_no_card_open_a_sent_bolt_whose_head_crew_cant_read_is_named_and_left_out_of_the_command(monkeypatch, capsys):
    """rail-cards "The landings card's read prints the lands crew posted", with no card open: a sent bolt whose head
    crew cannot read is named and left out of what lands."""
    closes = [dict(Act="card.close", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234 z@abc1234")]
    assert read_unopened(monkeypatch, capsys, closes, {"y": work(head=H1)}) == (
        "card land/crew: no landings card of crew is open\n"
        "  can't tell whether the user's earlier send still lands z: bolt/z is on no branch crew can read\n"
        "  to land on the user's send of an earlier card: y\n"
        "  y: no land is posted for it yet: crew's next raise of the card posts it\n")
    assert json.loads(read_unopened(monkeypatch, capsys, closes, {"y": work(head=H1)}, json=True)) == {
        "key": "land/crew", "card": None, "earlier": ["y"], "unknown": {"z": "bolt/z is on no branch crew can read"}}
    # with no send standing, it says only that no card is open
    assert read_unopened(monkeypatch, capsys, [], {}) == "card land/crew: no landings card of crew is open\n"


class TestLandReadingRead:
    """crew card read land/<bolt>, main-level ops's on the host its bolt's work runs on (card-sessions "A landing's read
    gives its session's decision alone and leaves its card"): the reading's decision alone, its annotations as notes on the bolt's row,
    an approval as landing nothing, then set aside so crew card session starts it anew; the kit's card untouched."""
    S = {"pid": 42, "document": "/c/00-y.md", "url": "http://mac-studio:19432/y", "started": "2026-10-23T10:00:00Z"}

    def read(self, monkeypatch, tmp_path, result=None, session=True, who="swancloud-ops", kit="crew", key="land/y"):
        d = tmp_path / "swancloud" / key
        d.mkdir(parents=True, exist_ok=True)
        if session:
            (d / "session.json").write_text(json.dumps(self.S))
        if result:
            (d / "result.json").write_text(json.dumps(result))
        monkeypatch.setattr(plan, "CARDS", tmp_path)
        monkeypatch.setattr(plan, "card_asker", lambda fleet, a: ("swancloud", who))
        monkeypatch.setattr(crew, "this_host", lambda: "mac-studio")
        monkeypatch.setattr(plan, "land_held", lambda fleet, label, bolt: (None, plan.Rec("Bolt", [("Bolt", bolt), ("Repo", "crew")]),
                                                                           dict(WHERE[kit], label="swancloud") if kit else None))
        monkeypatch.setattr(cards, "host_entries", lambda record, label, host: [])
        monkeypatch.setattr(cards, "Bridge", lambda *a, **k: pytest.fail("the read of a bolt's reading reached Pending You"))
        plan.card_read(FLEET, argparse.Namespace(key=key, label=None, json=False, sub="read"))
        return d

    def test_annotations_print_word_for_word_as_notes_on_its_row_and_the_reading_is_set_aside(self, monkeypatch, tmp_path, capsys):
        """card-sessions "Annotated in a landing's session"."""
        d = self.read(monkeypatch, tmp_path, {"decision": "annotated", "feedback": "1. 03-y-diff.txt: this drops the retry\n",
                                              "annotationCount": 1})
        assert capsys.readouterr().out == (
            "land/y: notes from its reading, as notes on the landing card:\n1. 03-y-diff.txt: this drops the retry\n"
            "land/y: its card is left as it is; crew card session land/y opens its reading again\n")
        assert sorted(p.name for p in d.iterdir()) == [".lock", "result.20261023T100000Z.json"]

    def test_an_approval_lands_nothing(self, monkeypatch, tmp_path, capsys):
        """card-sessions "Approved in a landing's session"."""
        self.read(monkeypatch, tmp_path, {"decision": "approved", "annotationCount": 0})
        assert capsys.readouterr().out.splitlines()[0] == (
            "land/y: approved in its reading, which lands nothing: the card's approval is the word to land")

    def test_nothing_sent_waits_on_the_user_and_forgets_nothing(self, monkeypatch, tmp_path, capsys):
        """card-sessions "Nothing decided yet"."""
        d = self.read(monkeypatch, tmp_path)
        assert capsys.readouterr().out == "land/y: its reading waits on the user, who has sent nothing from it\n"
        assert sorted(p.name for p in d.iterdir()) == ["session.json"]
        self.read(monkeypatch, tmp_path / "none", session=False)
        assert capsys.readouterr().out == "land/y: no reading of it runs on this host: crew card session land/y starts it\n"

    def test_any_agent_but_ops_and_a_bolt_not_started_are_refused(self, monkeypatch, tmp_path):
        with pytest.raises(crew.Refusal, match="^land/y's reading is swancloud-ops's to read, not swancloud-planner's$"):
            self.read(monkeypatch, tmp_path, who="swancloud-planner")
        with pytest.raises(crew.Refusal, match="^bolt y is not started"):
            self.read(monkeypatch, tmp_path, kit=None)

    def test_an_old_card_of_the_bolts_own_under_its_head_is_still_read_as_a_card(self, monkeypatch):
        monkeypatch.setattr(plan, "card_asker", lambda fleet, a: ("swancloud", "crw-1-conductor"))
        monkeypatch.setattr(crew, "this_host", lambda: "mac-studio")
        monkeypatch.setattr(cards, "host_entries", lambda record, label, host: [])
        with pytest.raises(crew.Refusal, match="^crw-1-conductor holds no open card under land/y/abc1234 on mac-studio"):
            plan.card_read(FLEET, argparse.Namespace(key="land/y/abc1234", label=None, json=False, sub="read"))


def test_a_send_ticking_none_closes_it_at_once_landing_nothing():
    step = plan.landings_step([box("y"), box("z")], answered("y@abc1234", "z@abc1234"), [], {"y", "z"})
    assert step == ("close", "Sent with no bolt ticked, so nothing lands. Left: y and z.", ["y", "z"], [])


def test_the_ticked_bolts_are_read_in_the_cards_order_from_each_form_of_answer():
    heads = plan.card_heads("y@abc1234 z@abc1234:left w@def5678")
    assert heads == [("y", "abc1234", False), ("z", "abc1234", True), ("w", "def5678", False)]
    got = lambda answer: {"status": "answered", "turn": "agent", "answer": answer}
    assert plan.ticked_of(got({"choiceIds": ["land:w", "land:y"]}), heads) == ["y", "w"]
    assert plan.ticked_of(got({"answers": {"rows-1": {"choiceIds": ["land:z"]}, "rows-2": {"choiceIds": ["land:w"]}}}), heads) == ["z", "w"]
    assert plan.ticked_of(got({"approved": True}), heads[:1]) == ["y"]
    assert plan.ticked_of(got({"approved": False}), heads[:1]) == []
    assert plan.ticked_of({"status": "pending", "turn": "you"}, heads) is None


# ------------------------------------------------------------------------------------- which bolts are left

def left_set(heads, at="2026-10-24T10:00:00Z"):
    """A raise's record of the bolts the user left on land/crew, as landing.left."""
    return dict(Act="landing.left", On=["kit/crew"], Key="land/crew", At=at, **({"Heads": heads} if heads else {}))


def stop(bolt, head=H1):
    """main-level ops's record of the user's words stopping a bolt's landing, as bolt.leave."""
    return dict(Act="bolt.leave", On=[f"bolt/{bolt}"], Head=head, From=["session/s-1/u-7"], Chars=38)


def pane_landed(bolt):
    return dict(Act="bolt.submit", On=[f"bolt/{bolt}"], Head=H1, From=["session/s-1/u-9"], Chars=20)


NOW = {"y": H1, "z": H1}


class TestWhichBoltsAreLeft:
    """rail-cards "A bolt the user left stays left until they tick it" and "A bolt stopped in ops's pane is shown as
    left": plan.left_now at a raise, from the card held, the ticks, the heads and the run record; plan.left_of from the
    run record alone, as a conductor's wait and the rail read it."""

    def test_a_bolt_marked_left_on_a_waiting_card_is_left_at_its_head(self):
        assert plan.left_now(waiting("y@abc1234", "z@abc1234:left"), None, NOW, {}, []) == {"z": "abc1234"}

    def test_a_bolt_the_user_did_not_tick_on_an_answered_card_is_left(self):
        assert plan.left_now(answered("y@abc1234", "z@abc1234"), ["y"], NOW, {}, []) == {"z": "abc1234"}
        assert plan.left_now(answered("y@abc1234", "z@abc1234"), [], NOW, {}, []) == {"y": "abc1234", "z": "abc1234"}

    def test_a_left_bolt_stays_left_across_the_close_of_one_card_and_the_post_of_the_next(self):
        assert plan.left_now(None, None, NOW, {"z": "abc1234"}, []) == {"z": "abc1234"}
        assert plan.left_now(waiting("y@abc1234", "z@abc1234"), None, NOW, {"z": "abc1234"}, []) == {"z": "abc1234"}

    def test_a_stop_in_ops_pane_is_left(self):
        assert plan.left_now(waiting("y@abc1234", "z@abc1234"), None, NOW, {}, [("z", H1)]) == {"z": "abc1234"}
        assert plan.left_now(None, None, NOW, {}, [("z", H1)]) == {"z": "abc1234"}

    def test_a_tick_on_the_card_held_ends_it(self):
        assert plan.left_now(answered("y@abc1234", "z@abc1234"), ["y", "z"], NOW, {"z": "abc1234"}, [("y", H1)]) == {}

    def test_a_moved_head_ends_it(self):
        moved = {"y": H1, "z": H2}
        assert plan.left_now(waiting("y@abc1234", "z@abc1234:left"), None, moved, {"z": "abc1234"}, [("z", H1)]) == {}
        assert plan.left_now(answered("y@abc1234", "z@abc1234"), ["y"], moved, {}, []) == {}

    def test_a_bolt_that_is_no_row_now_is_not_left(self):
        assert plan.left_now(waiting("z@abc1234:left"), None, {"y": H1}, {"z": "abc1234"}, [("z", H1)]) == {}

    def test_the_record_gives_the_last_set_and_each_stop_since_at_the_bolts_head_now(self):
        entries = [left_set("y@abc1234"), stop("w"), left_set("z@abc1234"), stop("y"), stop("v", H2)]
        assert plan.left_marks(entries, "land/crew") == ({"z": "abc1234"}, [("y", H1), ("v", H2)])
        assert plan.left_of(entries, "land/crew", {"y": H1, "z": H1, "v": H1, "w": H1}) == {"z": "abc1234", "y": "abc1234"}
        assert plan.left_of(entries, "land/swancloud", {"y": H1, "z": H1}) == {"y": "abc1234"}

    def test_a_set_with_none_left_ends_every_one_before_it_and_a_refused_one_ends_none(self):
        assert plan.left_of([left_set("z@abc1234"), left_set("")], "land/crew", NOW) == {}
        assert plan.left_of([left_set("z@abc1234"), dict(left_set(""), Refused="no")], "land/crew", NOW) == {"z": "abc1234"}

    def test_an_older_crews_landing_on_the_users_words_in_ops_pane_ends_no_stop(self):
        """No word in a pane lands a bolt (record 0056 point 5): only the user's tick lifts a stop or a left mark."""
        assert plan.left_of([stop("z"), pane_landed("z")], "land/crew", NOW) == {"z": "abc1234"}
        assert plan.left_of([left_set("z@abc1234"), pane_landed("z")], "land/crew", NOW) == {"z": "abc1234"}


# ------------------------------------------------------------- the raise on the main machine, from each row's host

import json  # noqa: E402
import types  # noqa: E402

# y, w and z are marked to stay, so every case of the card's rows holds of rows the card asks about; PROVEN leaves y
# unmarked, a bolt that lands on proof (a-proven-bolt-lands-on-proof).
PLAN = ("%rec: Bolt\n\n" + "".join(f"Bolt: {b}\nRepo: {k}\nPath: flume\nStays: yes\n\n" for b, k in
                                    [("y", "crew"), ("w", "swancloud"), ("z", "crew")]) + "%rec: Unit\n\n")
PROVEN = PLAN.replace("Bolt: y\nRepo: crew\nPath: flume\nStays: yes\n", "Bolt: y\nRepo: crew\nPath: flume\n")


MAIN = "e4f5a6b" + "0" * 33


def row(bolt, head=H1, **more):
    return dict(bolt=bolt, box=True, facts=dict(dict(bolt=bolt, kit="crew", units=["a"], chores=[], batches={}, head=head, at=None,
                                                     moved=0, pr=None, preview=None,
                                                     link=f"http://mac-studio:19432/{bolt}"), **more))


class LandActs:
    """A stand-in for what the raise reaches (plan.CardActs) on the main machine: each bolt's row as its team's host
    gives it (rows, a missing one's host not answering), the forecasts, this host's run record (entries) and the
    drive's (drive), and Pending You's tools answered from answers."""

    def __init__(self, rows, entries=(), drive=(), answers=None, here="mac-studio", against_main=None, main=MAIN, works=None):
        self.rows, self.held, self.whole, self.answers, self.here = rows, list(entries), list(drive), dict(answers or {}), here
        self.calls, self.emitted, self.told, self.asked, self.works, self.worked = [], [], [], [], dict(works or {}), []
        # The forecast: each bolt's conflicts with main ({bolt: [("main", paths)]}) at the revision main (None, unread).
        self.against_main, self.main, self.forecasts, self.kept = dict(against_main or {}), main, [], {}
        # The kit's card's lock: each taking of it, and the kit it is held for while the raise is inside it.
        self.locked, self.holding = [], None

    @contextlib.contextmanager
    def raising(self, label, kit):
        self.locked.append((label, kit))
        self.holding = kit
        try:
            yield
        finally:
            self.holding = None

    def land_row(self, label, bolt, host):
        self.asked.append((bolt, host))
        got = self.rows.get(bolt)
        return (got, None) if got else (None, "ssh: connect to host deneb: timed out")

    def forecast(self, label, kit, bolts, held=()):
        self.forecasts.append((list(bolts), list(held)))
        return {b: self.against_main.get(b) or [] for b in bolts}, {}, self.main and {"main": self.main}

    def keep_main(self, label, kit, sha):
        self.kept[kit] = sha

    def read_landings(self, label, kit):
        """The kit's landings read from the runner's report before the card's lock (kit_landings_read): recorded."""
        self.landings_read = getattr(self, "landings_read", []) + [(label, kit)]

    def post_lands(self, label, kit, owner, rows, sent, reads, work, proof=False):
        """The lands the send makes due, or with proof those due on proof, as lands_change decides them on a write over
        requests.rec as given (requests) and the plan at the write's tip, the plan the raise read unless the case gives
        another (tip), recorded in posts; none while the case gives no requests."""
        self.posts = getattr(self, "posts", [])
        if getattr(self, "requests", None) is None:
            return []
        from facts import FactsWrite
        read = getattr(self, "tip", None) or plan.plan_of(FLEET, label)
        w = FactsWrite(read.text() if isinstance(read, plan.Plan) else "%rec: Bolt\n%key: Bolt\n", files={"requests.rec": self.requests},
                       entries=self.held)
        try:
            got = plan.lands_change(w, kit, rows, sent, reads, work, proof)
        except plan.Unposted:
            return []
        self.requests = w.files["requests.rec"]
        self.posts.append((w.subject, w.act, list(w.on), dict(w.fields), [(a, o, f) for _, a, o, f in w.also]))
        for _, a, o, f in [(None, w.act, w.on, w.fields)] + w.also:
            self.held.append(dict(f, Act=a, On=list(o)))
        return got

    def kept_main(self, label, kit):
        return self.kept.get(kit)

    def work(self, label, kit, moves):
        self.worked.append(moves)
        return {b: self.works.get(b) or work(why="git log in /c/main on mac-studio failed: fatal: bad object") for b in moves}

    def entries(self, label):
        return self.held

    def drive(self, label):
        return self.whole

    def bridge(self, name, later, held=None):
        acts = self

        class Py:
            def __enter__(self):
                return self

            def __exit__(self, *exc):
                pass

            def answer(self, tool, args):
                acts.calls.append((tool, args))
                got = acts.answers.get(tool, ({"ok": True}, None))
                return got(args) if callable(got) else got

            def call(self, tool, args):
                got, words = self.answer(tool, args)
                if words is not None:
                    raise crew.Refusal(f"Pending You refused {tool}: {words}")
                return got
        return Py()

    def emit(self, label, act, on, **fields):
        self.emitted.append(dict(fields, Act=act, On=on))
        self.held.append(dict(fields, Act=act, On=on, By=fields.get("by")))

    def tell(self, name, text):
        self.told.append((name, text))
        return True

    def put(self, url, data, kind):
        return None

    def host(self):
        return self.here

    def caller(self):
        return "crw-1-conductor"

    def kits(self, label):
        return KITS


POSTED = {"match_area": ({"decision": "use", "suggestions": [{"areaId": "prj_crew"}]}, None),
          "post_request": ({"requestId": "req_k1", "version": 1}, None)}


def raised(monkeypatch, acts, note=None):
    monkeypatch.setattr(plan, "plan_of", lambda fleet, label: plan.Plan(PLAN))
    return plan.raise_landings(FLEET, "swancloud", "crew", acts, note=note)


def test_two_proven_bolts_post_one_card_in_ops_name_with_two_boxes(monkeypatch, capsys):
    acts = LandActs({"y": row("y"), "z": row("z")}, answers=POSTED)
    assert raised(monkeypatch, acts) == "req_k1"
    assert acts.asked == [("y", "mac-studio"), ("z", "mac-studio")]  # w is swancloud's, no row of crew's card
    post = next(a for t, a in acts.calls if t == "post_request")
    assert (post["idempotencyKey"], post["session"]["label"], post["kind"], post["highStakes"]) == (
        "land/crew@swancloud", "swancloud-ops", "multi", True)
    assert [o["label"] for o in post["options"]] == ["1. y", "2. z"]
    assert acts.emitted == [dict(Act="card.post", On=["kit/crew"], by="swancloud-ops", Card="req_k1", Key="land/crew",
                                 Heads="y@abc1234 z@abc1234")]
    assert acts.told == [("swancloud-ops", "Your card land/crew is up for the user: call get_request (requestId req_k1, "
                                           "name swancloud-ops), to hear their answer.")]


# Pending You's refusal of a card of questions carrying highStakes, in its words and with its apostrophe: of the card's own
# on the Willdan box on 2026-11-10 (signals 2026-11-10-wldn-ops-6352d0d6/01 and 2026-11-10-wldn-operator-9599d7fa/01 on
# WilldanGroup/crew-state wldn/main), and of each question's on deneb from 2026-11-11T23:09Z, every post of boomdrive's
# landings card refused (signal 2026-11-12-agentplot-ops-6907cc32/01 on agentplot/main of afterthought/crew-state).
MARKED_WORDS = "With questions, each question carries its own highStakes; leave the card’s highStakes out."


def marked_post(args):
    """post_request as Pending You answers it: a card of questions carrying highStakes, on the card or on any question,
    refused in its words."""
    questions = args.get("questions") or []
    if questions and ("highStakes" in args or any("highStakes" in q for q in questions)):
        return None, MARKED_WORDS
    return POSTED["post_request"]


def test_eight_proven_bolts_post_one_list_of_five_boxes_and_nothing_is_refused(monkeypatch):
    """rail-cards "Eight bolts, and Pending You refuses questions carrying highStakes": boomdrive's eight proven bolts
    had no card on deneb from 2026-11-11T23:09Z, every post of its lists of questions refused; one list of five boxes
    carrying highStakes on the card posts, the other three waiting on its face, recorded :next."""
    eight = [f"b{i}" for i in range(1, 9)]
    monkeypatch.setattr(plan, "plan_of", lambda fleet, label: plan.Plan(
        "%rec: Bolt\n\n" + "".join(f"Bolt: {b}\nRepo: crew\nPath: flume\nStays: yes\n\n" for b in eight) + "%rec: Unit\n\n"))
    acts = LandActs({b: row(b) for b in eight}, answers=dict(POSTED, post_request=marked_post))
    assert plan.raise_landings(FLEET, "swancloud", "crew", acts) == "req_k1"
    post = next(a for t, a in acts.calls if t == "post_request")
    assert (post["kind"], post["highStakes"], "questions" in post, len(post["options"])) == ("multi", True, False, 5)
    assert [(e["Act"], e.get("refused"), e.get("Refused"), e["Card"]) for e in acts.emitted] == [("card.post", None, None, "req_k1")]
    assert acts.emitted[0]["Heads"].endswith("b6@abc1234:next b7@abc1234:next b8@abc1234:next")
    # the fake refuses what Pending You refused, a card of questions carrying highStakes anywhere, and takes one carrying none
    qs = [{"id": "rows-1", "kind": "multi", "options": []}, {"id": "rows-2", "kind": "multi", "options": []}]
    assert marked_post({"questions": qs, "highStakes": True}) == (None, MARKED_WORDS)
    assert marked_post({"questions": [dict(qs[0], highStakes=True), qs[1]]}) == (None, MARKED_WORDS)
    assert marked_post({"questions": qs}) == POSTED["post_request"]


def test_a_send_with_rows_waiting_for_a_box_posts_the_card_that_follows_asking_for_them(monkeypatch):
    """rail-cards "Five ticked, three waiting", through the raise: the card is closed, none of the three recorded left, and
    the card that follows asks for b6, b7 and b8 as ticked boxes."""
    eight = [f"b{i}" for i in range(1, 9)]
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads=" ".join(EIGHT))]
    answer = {"status": "answered", "turn": "agent", "version": 3, "answer": {"choiceIds": [f"land:b{i}" for i in range(1, 6)]}}
    answers = dict(POSTED, get_request=(answer, None), post_request=({"requestId": "req_k2", "version": 1}, None))
    monkeypatch.setattr(plan, "plan_of", lambda fleet, label: plan.Plan(
        "%rec: Bolt\n\n" + "".join(f"Bolt: {b}\nRepo: crew\nPath: flume\nStays: yes\n\n" for b in eight) + "%rec: Unit\n\n"))
    acts = LandActs({b: row(b) for b in eight}, held, answers=answers)
    assert plan.raise_landings(FLEET, "swancloud", "crew", acts) == "req_k2"
    close = next(e for e in acts.emitted if e["Act"] == "card.close")
    assert close["Outcome"] == ("Asked of the runner as you ticked: b1, b2, b3, b4 and b5. b6, b7 and b8 had no box on this "
                                "card, and the card that follows asks for them.")
    assert close["Answer"] == "ticked b1, b2, b3, b4 and b5"
    assert not [e for e in acts.emitted if e["Act"] == "landing.left"]
    post = next(a for t, a in acts.calls if t == "post_request")
    assert post["follows"] == "req_k1"
    assert [o["id"] for o in post["options"]] == ["land:b6", "land:b7", "land:b8"]
    assert post["recommendedIds"] == ["land:b6", "land:b7", "land:b8"]
    assert acts.emitted[-1]["Act"] == "card.post" and acts.emitted[-1]["Heads"] == "b6@abc1234 b7@abc1234 b8@abc1234"


def test_a_kits_card_is_raised_under_its_lock_every_read_and_act_inside_it(monkeypatch):
    """Two bolts landing at once each raise their kit's card as they close (t-journey-land, sluice's #402 on deneb,
    2026-10-30: both read the card open and closed it, the second recording "ended in Pending You already"): the raise
    holds the kit's lock over the plan, the rows, the record and Pending You, so the second reads the first's close."""
    acts = LandActs({"y": row("y"), "z": row("z")}, answers=POSTED)
    seen = []
    for name in ("land_row", "entries", "drive", "forecast", "bridge", "emit", "tell"):
        monkeypatch.setattr(acts, name, lambda *a, f=getattr(acts, name), n=name, **k: seen.append((n, acts.holding)) or f(*a, **k))
    monkeypatch.setattr(plan, "plan_of", lambda fleet, label: seen.append(("plan", acts.holding)) or plan.Plan(PLAN))
    assert plan.raise_landings(FLEET, "swancloud", "crew", acts) == "req_k1"
    assert acts.locked == [("swancloud", "crew")]
    assert {n for n, _ in seen} >= {"plan", "land_row", "entries", "drive", "bridge", "emit"}
    assert [(n, h) for n, h in seen if h != "crew"] == []


def test_the_kits_card_lock_is_held_by_one_raise_and_fetches_the_plan_afresh_under_it(monkeypatch, tmp_path):
    monkeypatch.setattr(plan, "CARDS", tmp_path)
    monkeypatch.setattr(plan, "state_of", lambda fleet, label: ("/state", f"{label}/main"))
    lock = plan.landings_lock("swancloud", "crew")
    fetched = []

    def fetch(repo, ref, fresh=False):
        with open(lock, "w") as other, pytest.raises(BlockingIOError):  # fetched with the lock held
            fcntl.flock(other, fcntl.LOCK_EX | fcntl.LOCK_NB)
        fetched.append((ref, fresh))
    monkeypatch.setattr(plan, "tip_of", fetch)
    with plan.CardActs(FLEET).raising("swancloud", "crew"):
        with open(lock, "w") as other, pytest.raises(BlockingIOError):  # a second raise of the kit's card waits
            fcntl.flock(other, fcntl.LOCK_EX | fcntl.LOCK_NB)
        with open(plan.landings_lock("swancloud", "swancloud"), "w") as other:  # another kit's card's does not
            fcntl.flock(other, fcntl.LOCK_EX | fcntl.LOCK_NB)
    with open(lock, "w") as other:  # and the kit's is free once the raise is done
        fcntl.flock(other, fcntl.LOCK_EX | fcntl.LOCK_NB)
    assert fetched == [("swancloud/main", True)]
    assert lock.parent == tmp_path / "swancloud" / "land" and not (tmp_path / "swancloud" / "land" / "crew").exists()


def test_a_rows_head_moved_changes_the_waiting_card_in_place_naming_it(monkeypatch):
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234 z@abc1234")]
    acts = LandActs({"y": row("y"), "z": row("z", H2)}, held,
                    answers={"get_request": ({"status": "pending", "turn": "you", "version": 2}, None)})
    assert raised(monkeypatch, acts) == "req_k1"
    change = next(a for t, a in acts.calls if t == "update_request")
    assert (change["requestId"], change["changeNote"], change["expectedVersion"]) == ("req_k1", "z's head is now def5678", 2)
    assert acts.emitted[-1]["Heads"] == "y@abc1234 z@def5678"


# ------------------------------------------------------------- a row's preview, from the runner's report alone
# rail-cards "A landing row carries what brings its bolt's preview up", "A preview is put away on the user's done
# and when its row leaves the landings card" and "A moved head releases the preview of the old one and asks for none" (Decisions 5 and 7
# of a-cards-preview-is-asked-of-the-runner): the raise on the main machine reads each row's preview from the runner's
# report and writes the done of each ask no row that can land carries, reading no kit's policy.

import runner  # noqa: E402
from facts import FactsWrite  # noqa: E402


def ask_rec(n, bolt="z", head=H1, done=False, host="mac-studio"):
    """A preview request of a landings row's bolt, as crew card preview writes it."""
    return plan.Rec("Request", runner.request_fields(n, "preview", f"bolt/{bolt}", runner.preview_fields(
        host, "crew", f"bolt/{bolt}", head, done), "2026-11-08T12:00:00Z", "swancloud-ops"))


def mac_studio(previews=""):
    """mac-studio's runner as crew reads it, with these previews answered."""
    files = {"runner.rec": plan.Plan(runner.RUNNER + "\nHost: mac-studio\nVersion: 0.6.0\nSince: 2026-11-08T11:00:00Z\n"),
             "previews.rec": plan.Plan(runner.PREVIEWS + previews)}
    return {"mac-studio": runner.host_read("swancloud", "mac-studio", "5e1f0c2a" + "0" * 32, files, {})}


HY = "1234567" + "0" * 33  # y's head, beside z's at H1
UP = {"name": "crew-z", "branch": "bolt/z", "revision": H1, "state": "up", "addresses": {"web": "http://mac-studio:4310"}}


class TestRowPreview:
    @pytest.fixture(autouse=True)
    def runner_and_writes(self, monkeypatch):
        """The drive's requests and runners as the case sets them (self.requests, self.reads); each plan write
        applied to requests.rec at a tip holding them; and no kit's policy read."""
        self.requests, self.reads, self.writes = [], mac_studio(), []
        monkeypatch.setattr(plan, "runner_facts", lambda fleet, label: (list(self.requests), dict(self.reads)))
        monkeypatch.setattr(plan, "kit_git", lambda *a, **k: pytest.fail("a row's preview reads no kit's policy"))
        monkeypatch.setenv("CREW_AGENT", "swancloud-ops")

        def write(fleet, label, change, subject, act=None, on=(), fields=None, **more):
            text = runner.REQUESTS + "".join("\n" + "\n".join(r.lines()) + "\n" for r in self.requests)
            w = FactsWrite("%rec: Bolt\n%key: Bolt\n", files={"requests.rec": text}, runners=self.reads, label=label)
            change(w)
            new = plan.Plan(w.files["requests.rec"]).recs("Request")[len(self.requests):]
            self.requests += new
            self.writes.append(dict(subject=subject, act=act, on=list(on), fields=fields,
                                    requests=[(r.get("Work"), r.get("Revision"), r.get("Done")) for r in new]))
        monkeypatch.setattr(plan, "write", write)

    def posted(self, monkeypatch, rows, held=(), answers=POSTED):
        acts = LandActs(rows, list(held), answers=answers)
        raised(monkeypatch, acts)
        post = next((a for t, a in acts.calls if t in ("post_request", "update_request")), None)
        return acts, "\n".join(post["artifacts"][0]["lines"]) if post else ""

    def test_a_row_that_can_land_carries_what_brings_its_preview_up_with_no_policy_read(self, monkeypatch, tmp_path):
        """rail-cards "A kit that declares a preview" and "A kit that declares none": no request written."""
        monkeypatch.setattr(plan, "CARDS", tmp_path)
        _, face = self.posted(monkeypatch, {"y": row("y", HY), "z": row("z")})
        assert ("Try it running from bolt/z at abc1234: write on this card to bring it up, and that you are done to put it "
                "away. It is not held while the card waits.") in face.split("**2. z**")[1]
        assert self.writes == []

    def test_a_row_whose_ask_stands_carries_the_runners_report_and_the_card_keeps_what_it_told(self, monkeypatch, tmp_path):
        """rail-cards "Brought up" and "Not answered yet"; Decision 8, what the card was told kept on posting it."""
        monkeypatch.setattr(plan, "CARDS", tmp_path)
        self.requests = [ask_rec(1, "y", HY), ask_rec(2, "z")]
        self.reads = mac_studio(f"\nRequest: 2\nOutcome: done\nStatus: {json.dumps(UP)}\nListed: yes\nAt: 2026-11-08T12:03:00Z\n")
        _, face = self.posted(monkeypatch, {"y": row("y", HY), "z": row("z")})
        y, z = face.split("**2. z**")
        assert "A preview of 1234567 is asked of the runner on mac-studio, which brings it up at its next pass" in y
        assert "[Preview web](http://mac-studio:4310)" in z
        assert self.writes == []
        assert plan.told_read("swancloud") == {"land/crew": {"1": "asked", "2": "up"}}

    def test_a_moved_head_writes_the_old_asks_done_says_so_and_asks_nothing_at_the_new_head(self, monkeypatch, tmp_path):
        """rail-cards "A row's head moves while the card waits" and "The head moves with a preview up"."""
        monkeypatch.setattr(plan, "CARDS", tmp_path)
        self.requests = [ask_rec(1, "z", H1)]
        held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@1234567 z@abc1234")]
        acts, face = self.posted(monkeypatch, {"y": row("y", HY), "z": row("z", H2)}, held,
                                 answers={"get_request": ({"status": "pending", "turn": "you", "version": 2}, None)})
        change = next(a for t, a in acts.calls if t == "update_request")
        assert change["changeNote"] == "z's head is now def5678"
        assert ("Try it running from bolt/z at def5678: write on this card to bring it up, and that you are done to put it "
                "away. It is not held while the card waits. Its preview of abc1234 was released as the head moved.") in face
        assert [(w["subject"], w["fields"], w["requests"]) for w in self.writes] == [
            ("plan(card): preview of z put away from land/crew", {"Key": "land/crew", "State": "done"}, [("bolt/z", H1, "yes")])]

    def test_a_held_row_writes_its_done(self, monkeypatch, tmp_path):
        """rail-cards "A fix holds the landing"."""
        monkeypatch.setattr(plan, "CARDS", tmp_path)
        self.requests = [ask_rec(1, "z", H1)]
        self.posted(monkeypatch, {"y": row("y", HY), "z": {"bolt": "z", "box": False, "why": "held for a fix: gap (fix/z/gap)", "facts": row("z")["facts"]}})
        assert [w["requests"] for w in self.writes] == [[("bolt/z", H1, "yes")]]

    def test_a_bolt_gone_from_the_plan_writes_its_done(self, monkeypatch, tmp_path):
        """rail-cards "The bolt lands with its preview up": the raise that follows its close."""
        monkeypatch.setattr(plan, "CARDS", tmp_path)
        self.requests = [ask_rec(1, "gone", "9abcdef" + "0" * 33)]
        self.posted(monkeypatch, {"y": row("y", HY), "z": row("z")})
        assert [w["requests"] for w in self.writes] == [[("bolt/gone", "9abcdef" + "0" * 33, "yes")]]

    def test_a_refused_ask_writes_no_done_and_its_row_says_why(self, monkeypatch, tmp_path):
        """rail-cards "A preview the runner refused" and "The runner refuses the preview"."""
        monkeypatch.setattr(plan, "CARDS", tmp_path)
        words = "its Act preview, which crew's implementation does not read"
        self.requests = [ask_rec(1, "z", H1), ask_rec(2, "gone", H1)]
        self.reads = mac_studio("".join(f"\nRequest: {n}\nOutcome: refused\nWords: {words}\nAt: 2026-11-08T12:03:00Z\n" for n in (1, 2)))
        _, face = self.posted(monkeypatch, {"y": row("y", HY), "z": row("z")})
        assert self.writes == []
        assert f"it could not be brought up on mac-studio: {words}. Nothing waits on it." in face.split("**2. z**")[1]


def test_a_host_that_does_not_answer_is_named_and_the_rest_raised(monkeypatch, capsys):
    acts = LandActs({"y": row("y")}, answers=POSTED)
    raised(monkeypatch, acts)
    assert "card land/crew: mac-studio did not answer for bolt z (ssh: connect to host deneb: timed out), so its row is left off" in capsys.readouterr().err
    post = next(a for t, a in acts.calls if t == "post_request")
    assert (post["kind"], post["title"]) == ("approve", "Land the bolt y on crew's main")


def test_off_the_drives_main_machine_the_raise_is_refused_naming_it(monkeypatch):
    with pytest.raises(crew.Refusal, match="crew's landings card is raised on mac-studio, where swancloud-ops's cards are"):
        raised(monkeypatch, LandActs({}, here="deneb"))


def test_an_answered_card_whose_ticked_bolts_all_landed_is_closed_naming_where_with_no_row_left(monkeypatch):
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234 z@abc1234")]
    landed = [dict(Act="bolt.land", On=["bolt/y"], Head="1" * 40), dict(Act="bolt.land", On=["bolt/z"], Head="2" * 40)]
    answer = {"status": "answered", "turn": "agent", "version": 3, "answer": {"choiceIds": ["land:y", "land:z"]}}
    acts = LandActs({}, held, landed, answers={"get_request": (answer, None)})
    monkeypatch.setattr(plan, "plan_of", lambda fleet, label: plan.Plan("%rec: Bolt\n\n%rec: Unit\n\n"))
    assert plan.raise_landings(FLEET, "swancloud", "crew", acts) == "req_k1"
    ack = next(a for t, a in acts.calls if t == "ack_answer")
    said = f"Landed on GitHub's main: y at 1111111 and z at 2222222;{TIMER}"
    assert ack["outcome"] == said
    assert acts.emitted[-1] == dict(Act="card.close", On=["kit/crew"], by="swancloud-ops", Card="req_k1", Key="land/crew",
                                    State="closed", Outcome=said, Rows="0", Answer="ticked y and z")
    assert not [t for t, _ in acts.calls if t == "post_request"]


def test_a_raise_reading_its_card_answered_records_the_answer_once_with_the_bolts_ticked(monkeypatch):
    """rail-cards "crew records the user's answer the first time it reads it", "A landings card's raise reads it
    answered": y ticked and z cleared, the card showing y@abc1234 z@abc1234; y still lands on the send, so the card is
    left, and a second raise records nothing more."""
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234 z@abc1234")]
    answer = {"status": "answered", "turn": "agent", "version": 3, "answer": {"choiceIds": ["land:y"]}}
    acts = LandActs({"y": row("y")}, held, answers={"get_request": (answer, None)})
    monkeypatch.setattr(plan, "plan_of", lambda fleet, label: plan.Plan("%rec: Bolt\n\nBolt: y\nRepo: crew\nPath: flume\nStays: yes\n\n%rec: Unit\n\n"))
    assert plan.raise_landings(FLEET, "swancloud", "crew", acts) == "req_k1"
    answers = [e for e in acts.emitted if e["Act"] == "card.answer"]
    assert answers == [dict(Act="card.answer", On=["kit/crew"], by="swancloud-ops", Card="req_k1", Key="land/crew",
                            Answer="ticked y, left z", Heads="y@abc1234")]
    plan.raise_landings(FLEET, "swancloud", "crew", acts)
    assert len([e for e in acts.emitted if e["Act"] == "card.answer"]) == 1


def test_an_answered_landings_card_the_sweep_closes_keeps_the_send_and_the_next_raise_has_no_row_for_it(monkeypatch):
    """rail-cards "The sweep closes an answered landings card" and "The next card": the user ticked y at abc1234 and
    the sweep closes the card with a reason alone, its row gone for a moment; the close is acked, recorded closed with
    Heads: y@abc1234, and the next raise, y standing at abc1234 beside z, posts a card with z's row alone."""
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234 z@abc1234")]
    answer = {"status": "answered", "turn": "agent", "version": 3, "answer": {"choiceIds": ["land:y"]}}
    acts = LandActs({"y": row("y"), "z": row("z")}, held, answers=dict(POSTED, get_request=(answer, None),
                                                                        post_request=({"requestId": "req_k2", "version": 1}, None)))
    plan.row_card_close(FLEET, "swancloud", "swancloud-ops", "land/crew", reason="nothing waits to land on crew's main", acts=acts)
    close = acts.emitted[-1]
    assert (close["Act"], close["State"], close["Answer"], close["Heads"]) == ("card.close", "closed", "ticked y, left z", "y@abc1234")
    assert next(a for t, a in acts.calls if t == "ack_answer")["outcome"] == "nothing waits to land on crew's main"
    acts.answers["get_request"] = ({"status": "pending", "turn": "you", "version": 1}, None)
    monkeypatch.setattr(plan, "plan_of", lambda fleet, label: plan.Plan(PLAN))
    assert plan.raise_landings(FLEET, "swancloud", "crew", acts) == "req_k2"
    assert acts.emitted[-1]["Act"] == "card.post" and acts.emitted[-1]["Heads"] == "z@abc1234"


def test_a_send_ops_acked_in_pending_you_read_resolved_at_a_raise_is_recorded_closed_with_its_answer_and_send(monkeypatch):
    """rail-cards "A send closed in Pending You by its owner": ops's session acked land/crew's answered card, and the
    raise reads it resolved: crew records it closed as ended there, its Answer and Heads kept, sends Pending You
    nothing for it, and posts with no row for y, whose send stands at its head."""
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234 z@abc1234")]
    resolved = {"status": "resolved", "turn": "agent", "version": 4, "answer": {"choiceIds": ["land:y"]}}
    acts = LandActs({"y": row("y"), "z": row("z")}, held, answers=dict(POSTED, get_request=(resolved, None),
                                                                        post_request=({"requestId": "req_k2", "version": 1}, None)))
    monkeypatch.setattr(plan, "plan_of", lambda fleet, label: plan.Plan(PLAN))
    assert plan.raise_landings(FLEET, "swancloud", "crew", acts) == "req_k2"
    close = next(e for e in acts.emitted if e["Act"] == "card.close")
    assert {k: close[k] for k in ("Card", "State", "Outcome", "Answer", "Heads")} == {
        "Card": "req_k1", "State": "closed", "Outcome": plan.ENDED_ELSEWHERE, "Answer": "ticked y, left z", "Heads": "y@abc1234"}
    assert not [t for t, _ in acts.calls if t in ("ack_answer", "cancel_request", "update_request")]
    assert acts.emitted[-1]["Act"] == "card.post" and acts.emitted[-1]["Heads"] == "z@abc1234"


def test_one_left_out_closes_the_card_and_a_new_one_follows_it_with_that_bolt_unticked(monkeypatch):
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234 z@abc1234")]
    answer = {"status": "answered", "turn": "agent", "version": 3, "answer": {"choiceIds": ["land:y"]}}
    answers = dict(POSTED, get_request=(answer, None), post_request=({"requestId": "req_k2", "version": 1}, None))
    acts = LandActs({"z": row("z")}, held, [dict(Act="bolt.land", On=["bolt/y"], Head="1" * 40)], answers)
    monkeypatch.setattr(plan, "plan_of", lambda fleet, label: plan.Plan("%rec: Bolt\n\nBolt: z\nRepo: crew\nPath: flume\nStays: yes\n\n%rec: Unit\n\n"))
    assert plan.raise_landings(FLEET, "swancloud", "crew", acts) == "req_k2"
    close = next(e for e in acts.emitted if e["Act"] == "card.close")
    assert (close["Outcome"], close["Rows"]) == (f"Landed on GitHub's main: y at 1111111;{TIMER} Left: z.", "1")
    post = next(a for t, a in acts.calls if t == "post_request")
    opening, said = post["summary"].split("\n\n")[:2]
    assert post["follows"] == "req_k1" and said.startswith("Left on your last send.")
    assert opening.startswith("You answered the card before this one") and opening.endswith(
        f": ticked y, left z. Since then: landed on GitHub's main: y at 1111111;{TIMER} Left: z. z, which you left, waits on this card.")
    assert acts.emitted[-1]["Heads"] == "z@abc1234:left"


def test_a_send_ticking_none_closes_the_card_and_the_card_that_follows_says_every_row_was_left(monkeypatch):
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234 z@abc1234")]
    answer = {"status": "answered", "turn": "agent", "version": 3, "answer": {"choiceIds": []}}
    answers = dict(POSTED, get_request=(answer, None), post_request=({"requestId": "req_k2", "version": 1}, None))
    acts = LandActs({"y": row("y"), "z": row("z")}, held, answers=answers)
    assert raised(monkeypatch, acts) == "req_k2"
    assert next(e for e in acts.emitted if e["Act"] == "card.close")["Answer"] == "ticked none, left y and z"
    post = next(a for t, a in acts.calls if t == "post_request")
    assert post["follows"] == "req_k1" and post["summary"].startswith(
        "You answered the card before this one: ticked none, left y and z. Since then: sent with no bolt ticked, so nothing lands. "
        "Left: y and z. y and z, which you left, wait on this card.")


def test_a_card_posted_after_the_kits_last_one_says_which_bolts_joined_moved_or_still_wait_since_the_send(monkeypatch):
    """The send's follow-on was refused by Pending You, so the next raise posts the kit's card afresh, following the
    card the user sent: y landed, z they left still waits, w reads proven since."""
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234 z@abc1234", At="2026-10-23T13:10:00Z"),
            dict(Act="card.close", Key="land/crew", By="swancloud-ops", Card="req_k1", State="closed", Rows="1", At="2026-10-23T14:02:00Z",
                 Answer="ticked y, left z")]
    acts = LandActs({"z": row("z"), "w": row("w", H2)}, held, [dict(Act="bolt.land", On=["bolt/y"], Head="1" * 40)], POSTED)
    monkeypatch.setattr(plan, "plan_of", lambda fleet, label: plan.Plan(
        "%rec: Bolt\n\n" + "".join(f"Bolt: {b}\nRepo: crew\nPath: flume\nStays: yes\n\n" for b in ("z", "w")) + "%rec: Unit\n\n"))
    assert plan.raise_landings(FLEET, "swancloud", "crew", acts) == "req_k1"
    post = next(a for t, a in acts.calls if t == "post_request")
    assert post["follows"] == "req_k1" and post["summary"].startswith(
        "You answered the card before this one, posted 2026-10-23 13:10 UTC, by 14:02 UTC: ticked y, left z. Since then: w reads proven and "
        "joins the card. z, which you left, waits on this card.\n\n")
    assert plan.landings_since(plan.card_heads("y@abc1234 z@abc1234"), [box("z"), box("w", H2)]) == [
        "w reads proven and joins the card.", "z, which you left, waits on this card."]
    assert plan.landings_since(plan.card_heads("z@abc1234"), [box("z", H2)]) == ["z's head is now def5678."]


def test_the_card_that_follows_says_the_rows_that_had_no_box_wait_on_it(monkeypatch):
    """rail-cards "A send with rows waiting for a box is followed at once by a card asking for them": the card that
    follows says which of its rows had no box on the last card, never that the user left them. Its follow-on was
    refused, so the next raise posts the kit's card afresh, following the card the user sent."""
    earlier = plan.card_heads(" ".join(EIGHT))
    assert plan.landings_since(earlier, [box("b6"), box("b7"), box("b8")], {"b6", "b7", "b8"}) == [
        "b6, b7 and b8, which had no box on your last card, wait on this card."]
    left = plan.card_heads("b1@abc1234:left:next b2@abc1234 b7@abc1234:next")
    assert plan.landings_since(left, [box("b1"), box("b7", H2), box("b9")], {"b1", "b7"}) == [
        "b9 reads proven and joins the card.", "b7's head is now def5678.", "b1, which had no box on your last card, waits on this card."]
    assert plan.landings_since(plan.card_heads("z@abc1234"), [box("z")]) == ["z, which you left, waits on this card."]
    eight = [f"b{i}" for i in range(1, 9)]
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads=" ".join(EIGHT), At="2026-10-23T13:10:00Z"),
            dict(Act="card.close", Key="land/crew", By="swancloud-ops", Card="req_k1", State="closed", Rows="3", At="2026-10-23T14:02:00Z",
                 Answer="ticked b1, b2, b3, b4 and b5", Heads=" ".join(f"b{i}@abc1234" for i in range(1, 6)))]
    monkeypatch.setattr(plan, "plan_of", lambda fleet, label: plan.Plan(
        "%rec: Bolt\n\n" + "".join(f"Bolt: {b}\nRepo: crew\nPath: flume\nStays: yes\n\n" for b in eight) + "%rec: Unit\n\n"))
    acts = LandActs({b: row(b) for b in eight}, held, answers=POSTED)
    assert plan.raise_landings(FLEET, "swancloud", "crew", acts) == "req_k1"
    post = next(a for t, a in acts.calls if t == "post_request")
    assert post["follows"] == "req_k1" and [o["id"] for o in post["options"]] == ["land:b6", "land:b7", "land:b8"]
    assert post["summary"].startswith(
        "You answered the card before this one, posted 2026-10-23 13:10 UTC, by 14:02 UTC: ticked b1, b2, b3, b4 and b5. "
        "Since then: b6, b7 and b8, which had no box on your last card, wait on this card.\n\n")
    assert "which you left" not in post["summary"]


def test_a_bolt_proven_after_the_answer_gets_a_new_card_following_it_and_the_send_still_lands_the_rest(monkeypatch, capsys):
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234")]
    answer = {"status": "answered", "turn": "agent", "version": 3, "answer": {"approved": True}}
    answers = dict(POSTED, get_request=(answer, None), post_request=({"requestId": "req_k2", "version": 1}, None))
    acts = LandActs({"y": row("y"), "z": row("z")}, held, answers=answers)
    assert raised(monkeypatch, acts) == "req_k2"
    said = "Asked of the runner as you ticked: y. Since your send, z reads proven, and the card that follows asks for it."
    assert next(a for t, a in acts.calls if t == "ack_answer")["outcome"] == said
    assert not [t for t, _ in acts.calls if t == "update_request"]
    close = next(e for e in acts.emitted if e["Act"] == "card.close")
    assert (close["Card"], close["Outcome"], close["Heads"], close["Rows"]) == ("req_k1", said, "y@abc1234", "1")
    post = next(a for t, a in acts.calls if t == "post_request")
    assert (post["follows"], post["title"]) == ("req_k1", "Land the bolt z on crew's main")
    assert acts.emitted[-1]["Heads"] == "z@abc1234"
    # y still lands on that send: the card that followed is left as it is, and y joins no card while its head stands
    again = LandActs({"y": row("y"), "z": row("z")}, acts.held,
                     answers={"get_request": ({"status": "pending", "turn": "you", "version": 1}, None)})
    assert raised(monkeypatch, again) == "req_k2"
    assert [t for t, _ in again.calls] == ["get_request"]
    assert "card land/crew: y lands on the user's send of an earlier card, so it is no row of this one" in capsys.readouterr().out


def card_of(shown, ticked=None):
    """The open card plan.unoffered reads, from the Heads its last post or change recorded (shown) and the bolts the
    user's answer ticked, None while it waits on them."""
    return dict(heads=plan.card_heads(shown), taking=plan.heads_taking(shown), next=plan.heads_next(shown), ticked=ticked)


def test_a_row_the_open_card_does_not_offer_as_it_stands_is_unoffered():
    """rail-cards "The rail's read raises a landings card that does not show a row as it stands": a row that can land,
    held by no send, is unoffered when the card shows it on no row, at another head, taking main first, or, once
    answered, with no box; a row the card shows as it stands is not, one the user left on their send among them."""
    # the user sent y; z reads proven since, on no row of the card: unoffered, while y, ticked, is held by the send
    assert plan.unoffered([("y", H1, False), ("z", H1, True)], card_of("y@abc1234", ["y"]), {}) == ["z"]
    assert plan.unoffered([("y", H1, True), ("z", H1, True)], card_of("y@abc1234", ["y"]), {}) == ["z"]
    # z left on the send at its head now changes nothing; at a new head it reads proven again
    assert plan.unoffered([("y", H1, False), ("z", H1, True)], card_of("y@abc1234 z@abc1234", ["y"]), {}) == []
    assert plan.unoffered([("y", H1, False), ("z", H2, True)], card_of("y@abc1234 z@abc1234", ["y"]), {}) == ["z"]
    # shown taking main first and back, or with no box on the card the user sent
    assert plan.unoffered([("z", H1, True)], card_of("y@abc1234 z@abc1234:main", ["y"]), {}) == ["z"]
    assert plan.unoffered([("z", H1, True)], card_of("y@abc1234 z@abc1234:next", ["y"]), {}) == ["z"]
    # sent with nothing ticked: a row it showed is left, a row it did not is unoffered
    assert plan.unoffered([("y", H1, True), ("z", H1, True)], card_of("y@abc1234", []), {}) == ["z"]
    # a send holds a row at the head it was sent at: a bolt it ticked that reads proven at a new head, its take-main fix
    # merged, is unoffered, for the raise to post its land on that send or ask for it again
    assert plan.unoffered([("y", H2, True)], card_of("y@abc1234", ["y"]), {}) == ["y"]
    assert plan.unoffered([("y", H2, True)], card_of("y@abc1234:main", ["y"]), {}) == ["y"]
    # a send kept on a closed card holds a row this card does not show, at that head; one this card shows is judged by it
    assert plan.unoffered([("z", H1, True)], card_of("y@abc1234", ["y"]), {"z": "abc1234"}) == []
    assert plan.unoffered([("z", H2, True)], card_of("y@abc1234", ["y"]), {"z": "abc1234"}) == ["z"]
    assert plan.unoffered([("z", H2, True)], card_of("z@abc1234", None), {"z": "abc1234"}) == ["z"]
    # a waiting card: a row joining it, at a new head or back from taking main first; one on its face with no box is offered
    assert plan.unoffered([("y", H1, True), ("z", H1, True)], card_of("y@abc1234", None), {}) == ["z"]
    assert plan.unoffered([("y", H2, True)], card_of("y@abc1234", None), {}) == ["y"]
    assert plan.unoffered([("y", H1, True), ("z", H1, True)], card_of("y@abc1234 z@abc1234:main", None), {}) == ["z"]
    assert plan.unoffered([("y", H1, True), ("z", H1, True)], card_of("y@abc1234 z@abc1234:next", None), {}) == []
    # a row that can't land is offered by none; a fix of main, read by its name, is unoffered on no row of the card
    assert plan.unoffered([("z", H1, False)], card_of("y@abc1234", ["y"]), {}) == []
    assert plan.unoffered([("main--a-test-reads-its-fixture", None, True)], card_of("y@abc1234", ["y"]), {}) == [
        "main--a-test-reads-its-fixture"]
    assert plan.unoffered([("main--a-test-reads-its-fixture", None, True)],
                          card_of("y@abc1234 main--a-test-reads-its-fixture@1111111", None), {}) == []
    assert plan.unoffered([("main--a-test-reads-its-fixture", None, True)],
                          card_of("main--a-test-reads-its-fixture@1111111", ["main--a-test-reads-its-fixture"]), {}) == []


class SweepActs:
    """A stand-in for what the rail read's raise of the kits' landings cards reaches (plan.SweepActs) on the main
    machine: main as the survey read it, the revision its rows were last forecast against, both MAIN, so main has not
    moved, and each card's raise made by plan.raise_landings on land, the stand-in for what that raise reaches, or,
    with none, recorded alone and answered with req_k2."""

    def __init__(self, land):
        self.land, self.raised = land, []

    def host(self):
        return "mac-studio"

    def main_at(self, label, kit, sv, runs):
        return MAIN, None

    def kept_main(self, label, kit):
        return MAIN

    def raise_kit(self, label, kit):
        self.raised.append(kit)
        return plan.raise_landings(FLEET, label, kit, self.land) if self.land else "req_k2"


def swept_read(card, shown, answer, bolts):
    """A rail read of swancloud on its main machine once its sweep acted: crew's landings card open in swancloud-ops's
    name, its last post or change recording shown, its answer as the run record holds it ({heads}, or None), and crew's
    land row naming bolts, [(bolt, head, can)]."""
    entries = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card=card, Heads=shown)]
    land = dict(label="swancloud", group="land", key="land/crew", fixes=[],
                bolts=[dict(bolt=b, host="mac-studio", can=can, head=h) for b, h, can in bolts])
    return dict(found=[("swancloud", "afterthought/crew-state", "tip", plan.Plan(PLAN))], kits={"swancloud": list(KITS)}, sv={},
                rows=[land], logs={"swancloud": entries}, swept={},
                cards=[dict(label="swancloud", card=card, key="land/crew", by="swancloud-ops", host="mac-studio",
                            **({"answered": dict(at=None, answer="approved", heads=answer)} if answer is not None else {}))])


def test_a_bolt_proven_between_a_send_and_its_landing_gets_its_card_in_the_same_sweep(monkeypatch):
    """rail-cards "The rail's read raises a landings card that does not show a row as it stands": the user sent
    land/crew ticking y, whose land the runner has not answered yet, and z reads proven, main not having moved. The
    rail's read raises the card in the same sweep: the card they sent is closed keeping their send for y, and a card
    following it asks for z (signal 2026-11-12-agentplot-planner-237b59c7/01: wldn's bolts proven overnight waited
    400 to 1055 minutes for a landings card)."""
    monkeypatch.setattr(plan, "plan_of", lambda fleet, label: plan.Plan(PLAN))
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234")]
    answer = {"status": "answered", "turn": "agent", "version": 3, "answer": {"approved": True}}
    land = LandActs({"y": row("y"), "z": row("z")}, held,
                    answers=dict(POSTED, get_request=(answer, None), post_request=({"requestId": "req_k2", "version": 1}, None)))
    acts = SweepActs(land)
    got = plan.sweep_moved(FLEET, swept_read("req_k1", "y@abc1234", "y@abc1234", [("y", H1, False), ("z", H1, True)]), acts)
    assert got == {"raised": [dict(label="swancloud", kit="crew", was=MAIN, now=MAIN, card="req_k2", said=None, sent=False,
                                   rows=["z"], proven=[])], "unread": []}
    close = next(e for e in land.emitted if e["Act"] == "card.close")
    assert (close["Card"], close["Heads"]) == ("req_k1", "y@abc1234")
    post = next(a for t, a in land.calls if t == "post_request")
    assert (post["follows"], post["title"]) == ("req_k1", "Land the bolt z on crew's main")
    # the next read finds the card that followed showing z as it stands, and y still landing on the send: no raise
    acts = SweepActs(land)
    assert plan.sweep_moved(FLEET, swept_read("req_k2", "z@abc1234", None, [("y", H1, False), ("z", H1, True)]), acts) == {
        "raised": [], "unread": []} and acts.raised == []


def test_a_bolt_proven_while_the_card_waits_raises_it_in_the_same_sweep():
    """rail-cards "The rail's read raises a landings card that does not show a row as it stands": land/crew waits on
    the user with y, main has not moved, and z reads proven, so the read raises the card for z; once the card shows z
    at its head, the next read raises none."""
    acts = SweepActs(None)
    got = plan.sweep_moved(FLEET, swept_read("req_k1", "y@abc1234", None, [("y", H1, True), ("z", H1, True)]), acts)
    assert acts.raised == ["crew"] and got["raised"][0]["rows"] == ["z"]
    acts = SweepActs(None)
    assert plan.sweep_moved(FLEET, swept_read("req_k2", "y@abc1234 z@abc1234", None, [("y", H1, True), ("z", H1, True)]),
                            acts) == {"raised": [], "unread": []} and acts.raised == []


def test_a_bolt_the_user_left_beside_a_send_still_landing_raises_no_card(monkeypatch):
    """rail-cards "The rail's read raises a landings card that does not show a row as it stands": the user sent
    land/crew ticking y and leaving z, and y has not landed yet; z can land at the head the card showed, so the read
    raises nothing, the card waiting on its own landings to close."""
    acts = SweepActs(None)
    assert plan.sweep_moved(FLEET, swept_read("req_k1", "y@abc1234 z@abc1234", "y@abc1234", [("y", H1, False), ("z", H1, True)]),
                            acts) == {"raised": [], "unread": []} and acts.raised == []


LEFT = dict(Act="landing.left", On=["kit/crew"], by="swancloud-ops", Key="land/crew", Heads="z@abc1234")


def test_the_bolts_the_user_left_are_recorded_once_and_not_again_while_unchanged(monkeypatch):
    """rail-cards "A bolt the user left stays left until they tick it": the raise records the kit's left set when it
    changes, and a raise that changes nothing writes nothing (state.1)."""
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234 z@abc1234:left")]
    acts = LandActs({"y": row("y"), "z": row("z")}, held, answers=dict(POSTED, **WAITING))
    assert raised(monkeypatch, acts) == "req_k1"
    assert acts.emitted == [LEFT]
    again = LandActs({"y": row("y"), "z": row("z")}, acts.held, answers=dict(POSTED, **WAITING))
    raised(monkeypatch, again)
    assert again.emitted == []


def test_a_bolt_left_on_a_closed_card_is_unticked_on_the_card_posted_after_it(monkeypatch):
    """rail-cards "Left again": the record carries what the user left across the close of one card and the post of
    the next."""
    acts = LandActs({"y": row("y"), "z": row("z")}, [LEFT], answers=POSTED)
    assert raised(monkeypatch, acts) == "req_k1"
    post = next(a for t, a in acts.calls if t == "post_request")
    assert post["recommendedIds"] == ["land:y"]
    assert [e["Act"] for e in acts.emitted] == ["card.post"] and acts.emitted[0]["Heads"] == "y@abc1234 z@abc1234:left"


def test_a_left_bolt_whose_host_did_not_answer_stays_left_as_recorded(monkeypatch):
    """read.1: a row crew could not read ends nothing the user left."""
    acts = LandActs({"y": row("y")}, [LEFT], answers=POSTED)
    raised(monkeypatch, acts)
    assert not [e for e in acts.emitted if e["Act"] == "landing.left"]


def test_a_bolt_left_whose_head_moved_is_left_no_more_and_recorded_so(monkeypatch):
    """rail-cards "Its head moves": the card asks for it as a row at its new head."""
    acts = LandActs({"y": row("y"), "z": row("z", H2)}, [LEFT], answers=POSTED)
    raised(monkeypatch, acts)
    assert [e for e in acts.emitted if e["Act"] == "landing.left"] == [dict(LEFT, Heads="")]  # none left: the run record writes no Heads
    post = next(a for t, a in acts.calls if t == "post_request")
    assert post["recommendedIds"] == ["land:y", "land:z"]


def test_a_stop_in_ops_pane_shows_the_bolt_unticked_on_the_waiting_card_and_is_recorded(monkeypatch):
    """rail-cards "A bolt stopped in ops's pane is shown as left": crew bolt leave's note changes the card in place."""
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234 z@abc1234")]
    acts = LandActs({"y": row("y"), "z": row("z")}, held, drive=[stop("z")], answers=dict(POSTED, **WAITING))
    assert raised(monkeypatch, acts, note="z was stopped on your words in swancloud-ops's pane") == "req_k1"
    change = next(a for t, a in acts.calls if t == "update_request")
    assert change["changeNote"] == "z was stopped on your words in swancloud-ops's pane"
    assert change["recommendedIds"] == ["land:y"]
    assert acts.emitted[0] == LEFT and acts.emitted[-1]["Heads"] == "y@abc1234 z@abc1234:left"


def test_a_tick_on_a_send_ends_what_the_user_left_and_is_recorded(monkeypatch):
    """rail-cards "Ticked after a stop": the answered card ticks z, and the raise records none left."""
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234 z@abc1234:left"), LEFT]
    answer = {"status": "answered", "turn": "agent", "version": 3, "answer": {"choiceIds": ["land:y", "land:z"]}}
    acts = LandActs({"y": row("y"), "z": row("z")}, held, answers={"get_request": (answer, None)})
    raised(monkeypatch, acts)
    assert [e for e in acts.emitted if e["Act"] == "landing.left"] == [dict(LEFT, Heads="")]  # none left: the run record writes no Heads


WAITING = {"get_request": ({"status": "pending", "turn": "you", "version": 2}, None)}
MAIN_FIRST = "takes main first: forecast to conflict with main on README.md at e4f5a6b, until a fix taking main in moves its head"


def test_main_moving_so_one_of_two_conflicts_changes_the_card_in_place_the_other_keeping_its_box_unticked(monkeypatch):
    """rail-cards "One of two": every row forecast against main first; z stays on the list, unticked, saying why."""
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234 z@abc1234")]
    acts = LandActs({"y": row("y"), "z": row("z")}, held, answers=dict(POSTED, **WAITING), against_main={"z": [("main", ["README.md"])]})
    assert raised(monkeypatch, acts) == "req_k1"
    assert acts.forecasts == [(["y", "z"], [])] and acts.kept == {"crew": MAIN}
    assert [t for t, _ in acts.calls] == ["get_request", "get_request", "update_request"]
    change = next(a for t, a in acts.calls if t == "update_request")
    assert (change["requestId"], change["changeNote"], change["recommendedIds"]) == ("req_k1", f"z {MAIN_FIRST}", ["land:y"])
    assert change["options"][1]["detail"].startswith(MAIN_FIRST[0].upper() + MAIN_FIRST[1:])
    assert acts.emitted[-1]["Heads"] == "y@abc1234 z@abc1234:main"


def test_main_moving_so_one_of_three_conflicts_changes_the_card_in_place_saying_why(monkeypatch):
    """rail-cards "One of three"."""
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234 z@abc1234 w@abc1234")]
    acts = LandActs({"y": row("y"), "z": row("z"), "w": row("w")}, held, answers=WAITING, against_main={"w": [("main", ["README.md"])]})
    monkeypatch.setattr(plan, "plan_of", lambda fleet, label: plan.Plan(PLAN.replace("Bolt: w\nRepo: swancloud\n", "Bolt: w\nRepo: crew\n")))
    assert plan.raise_landings(FLEET, "swancloud", "crew", acts) == "req_k1"
    change = next(a for t, a in acts.calls if t == "update_request")
    assert change["changeNote"] == f"w {MAIN_FIRST}"
    assert acts.emitted[-1]["Heads"] == "y@abc1234 w@abc1234:main z@abc1234"


TAKE_MAIN_FIX = 'takes main first: take-main-e4f5a6b taking main in: "Take main into the bolt: it is forecast to conflict on README.md"'


def test_a_forecast_that_flips_between_raises_holds_the_card_to_one_request_changed_in_place(monkeypatch):
    """rail-cards "Taking main in and back, one card": wldn's switchboard-kit on 2026-11-06, whose land/switchboard-kit
    was withdrawn and posted six times from 03:11Z to 04:10Z as identity-and-access-reads-as-the-locked-mockups took
    main in beside a-deploy-row-follows-its-stack-to-the-end, each time it came to take main first or came back from it
    (signal 2026-11-06-swancloud-operator-1e1b6c68/01). Here main moves under z, z's take-main fix runs and merges, and
    main moves under it again: the card is posted once and changed in place, never withdrawn."""
    acts = LandActs({"y": row("y"), "z": row("z")}, answers=dict(POSTED, **WAITING))
    assert raised(monkeypatch, acts) == "req_k1"  # both can land: posted
    acts.against_main = {"z": [("main", ["README.md"])]}  # main moves: z is forecast to conflict with it
    assert raised(monkeypatch, acts) == "req_k1"
    fixing = dict(row("z"), box=False, why=TAKE_MAIN_FIX, takes_main=True)
    acts.rows, acts.against_main = {"y": row("y"), "z": fixing}, {}  # its take-main fix in flight: nothing to say
    assert raised(monkeypatch, acts) == "req_k1"
    acts.rows = {"y": row("y"), "z": row("z", H2)}  # the fix merged: z reads proven at its new head
    assert raised(monkeypatch, acts) == "req_k1"
    acts.main, acts.against_main = "9" * 40, {"z": [("main", ["README.md"])]}  # main moves under it again
    assert raised(monkeypatch, acts) == "req_k1"
    tools = [t for t, _ in acts.calls]
    assert tools.count("post_request") == 1 and "cancel_request" not in tools
    assert [a["changeNote"] for t, a in acts.calls if t == "update_request"] == [
        f"z {MAIN_FIRST}", "z's head is now def5678; z can land again",
        "z takes main first: forecast to conflict with main on README.md at 9999999, until a fix taking main in moves its head"]
    assert [a["recommendedIds"] for t, a in acts.calls if t == "update_request"] == [["land:y"], ["land:y", "land:z"], ["land:y"]]
    assert [(e["Act"], e["Card"], e["Heads"]) for e in acts.emitted if e["Act"].startswith("card.")] == [
        ("card.post", "req_k1", "y@abc1234 z@abc1234"), ("card.update", "req_k1", "y@abc1234 z@abc1234:main"),
        ("card.update", "req_k1", "y@abc1234 z@def5678"), ("card.update", "req_k1", "y@abc1234 z@def5678:main")]


FOUR = ("%rec: Bolt\n\n" + "".join(f"Bolt: {b}\nRepo: crew\nPath: flume\nStays: yes\n\n" for b in ("a", "b", "c", "d")) + "%rec: Unit\n\n")
FOUR_POSTED = dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="a@abc1234 b@abc1234 c@abc1234 d@abc1234")


def offers_what_it_recommends(args):
    """What Pending You holds every card it takes to (afterthought-ops's signal card-update-recommends-removed-options,
    req_acf27442b1fa4ce4a278 on deneb, 2026-11-08: "Recommend from: land:a-boxs-build-engine-is-never-killed-at-its-cap,
    land:moons-store-…"): a list of boxes recommends only boxes it offers, and an approval only its approve."""
    if "options" in args:
        return set(args["recommendedIds"]) <= {o["id"] for o in args["options"]}
    return args["recommendedIds"] == ["approve"] and "approve" in args


def test_rows_turning_to_take_main_first_while_the_card_waits_change_it_in_place_recommending_only_what_it_offers(monkeypatch):
    """rail-cards "A row taking main first changes the card in place": afterthought's land/swancloud on deneb,
    2026-11-08, four bolts waiting when main moved under three of them, which then took main in. The card is changed in
    place, still four boxes, the three unticked saying they take main first, its recommended ids all among the options
    it sends; their take-main fixes starting change nothing it shows, so it is left as it is."""
    monkeypatch.setattr(plan, "plan_of", lambda fleet, label: plan.Plan(FOUR))
    rows = {b: row(b) for b in "abcd"}
    acts = LandActs(rows, [FOUR_POSTED], answers=dict(POSTED, **WAITING),
                    against_main={b: [("main", ["README.md"])] for b in "abc"})
    assert plan.raise_landings(FLEET, "swancloud", "crew", acts) == "req_k1"
    fixing = {b: dict(row(b), box=False, why=TAKE_MAIN_FIX, takes_main=True) for b in "abc"}
    acts.rows, acts.against_main = dict(fixing, d=row("d")), {}  # each take-main fix in flight
    assert plan.raise_landings(FLEET, "swancloud", "crew", acts) == "req_k1"
    tools = [t for t, _ in acts.calls]
    assert tools.count("update_request") == 1 and "cancel_request" not in tools and "post_request" not in tools
    change = next(a for t, a in acts.calls if t == "update_request")
    assert [o["id"] for o in change["options"]] == ["land:a", "land:b", "land:c", "land:d"]
    assert change["recommendedIds"] == ["land:d"] and offers_what_it_recommends(change)
    assert change["multi"] == {"min": 0, "max": 4}
    assert all(o["detail"].startswith(MAIN_FIRST[0].upper() + MAIN_FIRST[1:]) for o in change["options"][:3])
    assert change["changeNote"].startswith("a takes main first: forecast to conflict with main")  # cut to what Pending You takes
    assert [(e["Act"], e["Heads"]) for e in acts.emitted if e["Act"].startswith("card.")] == [
        ("card.update", "a@abc1234:main b@abc1234:main c@abc1234:main d@abc1234")]


def test_take_main_fixes_started_on_rows_the_card_shows_taking_main_first_change_it_in_place_as_four_boxes(monkeypatch):
    """The refused changes of 2026-11-08 themselves: land/swancloud posted with three rows marked :main and one that can
    land, then crew fix started a take-main fix on each of the three, each start raising the card with its note (crew
    fix's "<bolt> is held for a fix: <words>"). Each raise changes the card in place, its four rows as the post recorded
    them, the one that can land its only recommended id, every recommended id among the options it sends; the older crew
    read the post as one row and sent its approval, recommending "approve", in place over the four boxes, which Pending
    You refused."""
    monkeypatch.setattr(plan, "plan_of", lambda fleet, label: plan.Plan(FOUR))
    posted = dict(FOUR_POSTED, Heads="a@abc1234:main b@abc1234:main c@abc1234:main d@abc1234")
    fixing = {b: dict(row(b), box=False, why=TAKE_MAIN_FIX, takes_main=True) for b in "abc"}
    acts = LandActs(dict(fixing, d=row("d")), [posted], answers=dict(POSTED, **WAITING))
    for b in "abc":
        note = f"{b} is held for a fix: Take main into the bolt: merge origin/main into this place"
        assert plan.raise_landings(FLEET, "swancloud", "crew", acts, note=note) == "req_k1"
    tools = [t for t, _ in acts.calls]
    assert tools.count("update_request") == 3 and "cancel_request" not in tools and "post_request" not in tools
    for change in (a for t, a in acts.calls if t == "update_request"):
        assert [o["id"] for o in change["options"]] == ["land:a", "land:b", "land:c", "land:d"]
        assert change["recommendedIds"] == ["land:d"] and offers_what_it_recommends(change)
    assert [e["Heads"] for e in acts.emitted] == ["a@abc1234:main b@abc1234:main c@abc1234:main d@abc1234"] * 3


def test_rows_leaving_a_card_of_boxes_for_one_that_can_land_follow_it_with_an_approval_never_changed_in_place(monkeypatch):
    """rail-cards "A row taking main first changes the card in place", its other side: three of four rows held for a fix
    that takes no main in leave the card, so one row can land and the card's form moves from boxes to a hold-to-approve,
    which Pending You never changes (cards.landings_form). It is withdrawn and the approval follows it, so no change
    sends an approval's recommended id over boxes that offer none, as the refused changes of 2026-11-08 did."""
    monkeypatch.setattr(plan, "plan_of", lambda fleet, label: plan.Plan(FOUR))
    held = {b: dict(row(b), box=False, why="held for a fix: one zone is missing (fix/a/gap)") for b in "abc"}
    acts = LandActs(dict(held, d=row("d")), [FOUR_POSTED], answers=dict(POSTED, **WAITING))
    assert plan.raise_landings(FLEET, "swancloud", "crew", acts) == "req_k1"
    tools = [t for t, _ in acts.calls]
    assert "update_request" not in tools and tools.count("cancel_request") == 1 and tools.count("post_request") == 1
    post = next(a for t, a in acts.calls if t == "post_request")
    assert (post["kind"], post["recommendedIds"]) == ("approve", ["approve"]) and offers_what_it_recommends(post)
    assert [(e["Act"], e.get("Heads")) for e in acts.emitted if e["Act"].startswith("card.")] == [
        ("card.close", None), ("card.post", "d@abc1234")]


def test_a_conflict_the_record_holds_at_the_rows_head_holds_it_with_no_forecast_against_it(monkeypatch):
    """rail-cards "Raised again at the same heads": the row is handed to the forecast as held, and held taking main first in the
    recorded files though the card's own forecast says nothing of it."""
    recorded = [dict(Act="forecast", On=["bolt/y"], Heads="bolt/y@abc1234 main@2222222", Paths="docs/a.md", Reached="wait")]
    acts = LandActs({"y": row("y"), "z": row("z")}, drive=recorded, answers=POSTED, main=None)
    assert raised(monkeypatch, acts) == "req_k1"
    assert acts.forecasts == [(["y", "z"], ["y"])] and acts.kept == {}
    post = next(a for t, a in acts.calls if t == "post_request")
    assert (post["kind"], post["recommendedIds"]) == ("multi", ["land:z"])
    assert post["options"][0]["detail"].startswith(
        "Takes main first: forecast to conflict with main on docs/a.md at 2222222, until a fix taking main in moves its head")
    assert acts.emitted[-1]["Heads"] == "y@abc1234:main z@abc1234"


HELD = dict(Act="forecast", On=["bolt/z"], why="bolt(z): forecast to conflict with main", Heads="bolt/z@abc1234 main@e4f5a6b",
            Paths="README.md", Reached="held")


def test_a_row_newly_taking_main_first_is_recorded_held_once_and_nobody_is_told(monkeypatch):
    """rail-cards "A row forecast to conflict with main takes main first, recorded once and telling no one" (Task notes 2.2 of the-team-machinery-leaves):
    the raise holds z's forecast on its row and starts nothing, and raised again at the same heads records nothing more,
    z still held by the record and the forecast."""
    acts = LandActs({"y": row("y"), "z": row("z")}, answers=POSTED, against_main={"z": [("main", ["README.md"])]})
    raised(monkeypatch, acts)
    assert [n for n, _ in acts.told] == ["swancloud-ops"]  # the card's owner, told it is up; no one told of z
    assert [e for e in acts.emitted if e["Act"] == "forecast"] == [HELD]
    post = next(a for t, a in acts.calls if t == "post_request")
    assert post["recommendedIds"] == ["land:y"] and post["options"][1]["detail"].startswith(MAIN_FIRST[0].upper() + MAIN_FIRST[1:])
    again = LandActs({"y": row("y"), "z": row("z")}, drive=[HELD], answers=dict(POSTED, **WAITING),
                     against_main={"z": [("main", ["README.md"])]})
    raised(monkeypatch, again)
    assert {n for n, _ in again.told} == {"swancloud-ops"} and not [e for e in again.emitted if e["Act"] == "forecast"]
    assert again.forecasts == [(["y", "z"], ["z"])]


def test_a_forecast_recorded_first_at_the_same_heads_is_not_recorded_again(monkeypatch):
    """A forecast the record holds at the same bolt head and revision of main, a conductor's wait's from before among
    them, is not recorded again."""
    acts = LandActs({"y": row("y"), "z": row("z")}, drive=[dict(HELD, Reached="wait")], answers=POSTED,
                    against_main={"z": [("main", ["README.md"])]})
    raised(monkeypatch, acts)
    assert not [e for e in acts.emitted if e["Act"] == "forecast"] and [n for n, _ in acts.told] == ["swancloud-ops"]


WOULD = "z, which you left, would take main first: forecast to conflict with main on README.md at e4f5a6b"


def test_a_left_bolt_main_conflicts_with_is_told_nothing_and_the_waiting_card_says_so_once(monkeypatch):
    """bolt-teams "A left bolt"; rail-cards "Left, and main conflicts with it" and "Raised again at the same heads"."""
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234 z@abc1234:left")]
    acts = LandActs({"y": row("y"), "z": row("z")}, held, answers=dict(POSTED, **WAITING), against_main={"z": [("main", ["README.md"])]})
    assert raised(monkeypatch, acts) == "req_k1"
    assert acts.told == []
    assert [e for e in acts.emitted if e["Act"] == "forecast"] == [dict(HELD, Reached="left")]
    change = next(a for t, a in acts.calls if t == "update_request")
    assert change["changeNote"] == WOULD and change["recommendedIds"] == ["land:y"]
    assert change["options"][1]["consequence"].startswith("It would take main first if you tick it")
    assert acts.emitted[-1]["Heads"] == "y@abc1234 z@abc1234:left"
    again = LandActs({"y": row("y"), "z": row("z")}, acts.held, answers=dict(POSTED, **WAITING),
                     against_main={"z": [("main", ["README.md"])]})
    raised(monkeypatch, again)
    assert again.told == [] and again.emitted == [] and [t for t, _ in again.calls] == ["get_request"]


def test_a_left_bolt_ticked_at_the_same_heads_is_recorded_held_and_takes_main_first_nobody_told(monkeypatch):
    """rail-cards "Ticked after being left": the send stands for it, and nothing is started for it."""
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234 z@abc1234:left"), LEFT,
            dict(HELD, Reached="left")]
    answer = {"status": "answered", "turn": "agent", "version": 3, "answer": {"choiceIds": ["land:y", "land:z"]}}
    acts = LandActs({"y": row("y"), "z": row("z")}, held, answers={"get_request": (answer, None)},
                    against_main={"z": [("main", ["README.md"])]})
    assert raised(monkeypatch, acts) == "req_k1"
    assert acts.told == []
    assert [e for e in acts.emitted if e["Act"] == "forecast"] == [HELD]
    assert [t for t, _ in acts.calls] == ["get_request"]  # the card is left as it is, the send standing for z


ONLY_Z = "%rec: Bolt\n\nBolt: z\nRepo: crew\nPath: flume\nStays: yes\n\n%rec: Unit\n\n"


def refused_and_closed(monkeypatch):
    """The user sent land/crew with y and z ticked, y landed and sluice refused z at abc1234: the raise closes the
    card, keeping z's send; the run record's entries after it."""
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234 z@abc1234")]
    answer = {"status": "answered", "turn": "agent", "version": 3, "answer": {"choiceIds": ["land:y", "land:z"]}}
    z = dict(row("z"), box=False, why=REFUSED)
    acts = LandActs({"z": z}, held, [dict(Act="bolt.land", On=["bolt/y"], Head="1" * 40)], {"get_request": (answer, None)})
    monkeypatch.setattr(plan, "plan_of", lambda fleet, label: plan.Plan(ONLY_Z))
    assert plan.raise_landings(FLEET, "swancloud", "crew", acts) == "req_k1"
    close = acts.emitted[-1]
    assert (close["Act"], close["Heads"]) == ("card.close", "z@abc1234")
    assert close["Outcome"] == f"Landed on GitHub's main: y at 1111111;{TIMER} Held: z, {REFUSED}; {STANDS}"
    assert not [t for t, _ in acts.calls if t == "post_request"]
    return acts.held


def test_a_refused_bolt_whose_fix_only_took_main_in_lands_on_the_same_send_with_no_card(monkeypatch, capsys):
    """rail-cards "A refused bolt takes main in" and "The fix merges": z reads proven at def5678, its own work the
    same, and no card asks for it."""
    entries = refused_and_closed(monkeypatch)
    acts = LandActs({"z": row("z", H2)}, entries, answers=POSTED, works={"z": work()})
    assert plan.raise_landings(FLEET, "swancloud", "crew", acts) is None
    assert acts.worked == [{"z": ("abc1234", H2)}] and not acts.calls
    assert "card land/crew: z lands on the user's send of an earlier card, so it is no row of this one" in capsys.readouterr().out


def test_a_refused_bolt_whose_fix_committed_a_change_is_asked_again_on_a_card_naming_it(monkeypatch):
    """rail-cards "A fix that changes the bolt's work merges": z has a box again, the card naming the fix's commit."""
    entries = refused_and_closed(monkeypatch)
    acts = LandActs({"z": row("z", H2)}, entries, answers=POSTED, works={"z": work([LEASE])})
    assert plan.raise_landings(FLEET, "swancloud", "crew", acts) == "req_k1"
    post = next(a for t, a in acts.calls if t == "post_request")
    assert post["title"] == "Land the bolt z on crew's main"
    assert post["summary"].startswith("z's head is now def5678, with work of its own since your send at abc1234: fix: "
                                      "keep the lease.\n\n")
    assert acts.emitted[-1]["Heads"] == "z@def5678"


def test_a_card_following_the_users_send_says_what_changed_of_a_bolt_asked_again_once_in_its_opening(monkeypatch):
    """rail-cards "A follow-on card says what changed in the words its event gives" and "A ticked bolt whose own work changed is
    asked again, saying what changed": the user ticked y and z, y is landing, and a fix committed to z: the card that
    follows opens with what they answered and what changed of z's work, said there once."""
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234 z@abc1234")]
    answer = {"status": "answered", "turn": "agent", "version": 3, "answer": {"choiceIds": ["land:y", "land:z"]}}
    answers = dict(POSTED, get_request=(answer, None), post_request=({"requestId": "req_k2", "version": 1}, None))
    acts = LandActs({"y": row("y"), "z": row("z", H2)}, held, answers=answers, works={"z": work([LEASE])})
    assert raised(monkeypatch, acts) == "req_k2"
    changed = "z's head is now def5678, with work of its own since your send at abc1234: fix: keep the lease"
    post = next(a for t, a in acts.calls if t == "post_request")
    assert post["follows"] == "req_k1" and post["summary"].startswith(
        f"You answered the card before this one: ticked y and z. Since then: asked of the runner as you ticked: y. Since your send, {changed}, "
        "and the card that follows asks for it.\n\n")
    assert post["summary"].count(changed) == 1


def test_a_card_posted_after_the_users_send_opens_with_what_changed_of_a_bolt_asked_again_and_what_joined(monkeypatch):
    """The user's send kept z's yes as it closed, and a fix committed to z since: the kit's card posted afresh follows
    the card they sent, opening with what changed of z's work, once, and that w joined."""
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234 z@abc1234", At="2026-10-23T13:10:00Z"),
            dict(Act="card.close", Key="land/crew", By="swancloud-ops", Card="req_k1", State="closed", Rows="1", Heads="z@abc1234",
                 At="2026-10-23T14:02:00Z", Answer="ticked y and z")]
    acts = LandActs({"z": row("z", H2), "w": row("w")}, held, [dict(Act="bolt.land", On=["bolt/y"], Head="1" * 40)], POSTED,
                    works={"z": work([LEASE])})
    monkeypatch.setattr(plan, "plan_of", lambda fleet, label: plan.Plan(
        "%rec: Bolt\n\n" + "".join(f"Bolt: {b}\nRepo: crew\nPath: flume\nStays: yes\n\n" for b in ("z", "w")) + "%rec: Unit\n\n"))
    assert plan.raise_landings(FLEET, "swancloud", "crew", acts) == "req_k1"
    changed = "z's head is now def5678, with work of its own since your send at abc1234: fix: keep the lease"
    post = next(a for t, a in acts.calls if t == "post_request")
    assert post["follows"] == "req_k1" and post["summary"].startswith(
        f"You answered the card before this one, posted 2026-10-23 13:10 UTC, by 14:02 UTC: ticked y and z. Since then: {changed}. "
        "w reads proven and joins the card.\n\n")
    assert post["summary"].count(changed) == 1


def test_a_ticked_bolt_whose_head_moved_on_an_answered_card_is_read_once_and_waited_for_when_its_work_stands(monkeypatch, capsys):
    """rail-cards "The head moves by taking main in before the landing": the card the user answered is left."""
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234 z@abc1234")]
    answer = {"status": "answered", "turn": "agent", "version": 3, "answer": {"choiceIds": ["land:y", "land:z"]}}
    acts = LandActs({"y": row("y"), "z": row("z", H2)}, held, answers={"get_request": (answer, None)}, works={"z": work()})
    assert raised(monkeypatch, acts) == "req_k1"
    assert acts.worked == [{"z": ("abc1234", H2)}] and [t for t, _ in acts.calls] == ["get_request"]
    assert "card land/crew: req_k1 is left as it is, the user having answered it" in capsys.readouterr().out


def test_the_raise_is_handed_to_the_main_machine_as_the_one_asking(monkeypatch, capsys):
    ran = []
    monkeypatch.setattr(crew, "this_host", lambda: "deneb")
    monkeypatch.setattr(crew, "crew_argv", lambda fleet, host, *args: ["crew-on", host, *args])
    monkeypatch.setattr(crew, "on_machine", lambda fleet, host, argv: ran.append((host, argv)) or types.SimpleNamespace(
        returncode=1, stdout="card land/crew: req_k1 changed\n", stderr="ssh: refused\n"))
    plan.land_hand(FLEET, "swancloud", "crew", "y is held for a fix: x")
    assert ran == [("mac-studio", ["crew-on", "mac-studio", "_land-card", "swancloud", "crew", "--note", "y is held for a fix: x"])]
    out, err = capsys.readouterr()
    assert out == "card land/crew: req_k1 changed\n" and err.endswith("crew's landings card is not raised on mac-studio: ssh: refused\n")


def test_on_the_main_machine_the_raise_runs_in_this_process_and_a_refusal_refuses_nothing(monkeypatch, capsys):
    monkeypatch.setattr(crew, "this_host", lambda: "mac-studio")
    monkeypatch.setattr(plan, "raise_landings", lambda fleet, label, kit, note=None, pane=None: plan.fail(f"no plan, {note}"))
    plan.land_hand(FLEET, "swancloud", "crew", "x")
    assert capsys.readouterr().err == "crew's landings card is not raised: no plan, x\n"


def test_a_row_read_on_another_host_is_its_crew_land_row_and_one_crew_cannot_read_is_said(monkeypatch):
    acts = plan.CardActs(FLEET)
    monkeypatch.setattr(crew, "this_host", lambda: "mac-studio")
    monkeypatch.setattr(crew, "crew_argv", lambda fleet, host, *args: list(args))
    out = {"y": json.dumps(row("y")), "z": "not a row"}
    monkeypatch.setattr(crew, "on_machine", lambda fleet, host, argv: types.SimpleNamespace(
        returncode=0, stdout=f"{out[argv[2]]}\n", stderr=""))
    assert acts.land_row("swancloud", "y", "deneb") == (row("y"), None)
    assert acts.land_row("swancloud", "z", "deneb") == (None, "crew _land-row printed no row crew reads: not a row")


def test_crew_land_row_prints_the_row_as_one_line_of_json(monkeypatch, capsys):
    monkeypatch.setattr(plan, "land_row", lambda fleet, label, bolt: print("ended land/y's session") or dict(bolt=bolt, why="no"))
    plan.land_row_cmd(FLEET, argparse.Namespace(label="swancloud", bolt="y", json=True))
    out, err = capsys.readouterr()
    assert (out, err) == ('{"bolt": "y", "why": "no"}\n', "ended land/y's session\n")


# --------------------------------------------------------------------- a row's reading ends with its row, not a card

class OldCardActs(LandActs):
    """LandActs where a reading would end: each end asked, recorded."""

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.ended = []

    def end(self, label, key):
        self.ended.append(key)
        return f"ended {key}'s session"


@pytest.mark.parametrize("key", ["land/y", "land/y/abc1234"])
@pytest.mark.parametrize("answers", [{"get_request": ({"status": "pending", "version": 1}, None)},
                                     {"get_request": ({"status": "answered", "version": 2}, None)}])
def test_an_old_card_of_a_bolts_own_closed_ends_not_its_rows_reading(key, answers, capsys):
    """A closed card of the old per-bolt form is no word on the bolt's row: its reading ends with the row (land_end),
    whether crew withdrew the card waiting on the user or closed one they answered."""
    acts = OldCardActs({}, entries=[dict(Act="card.post", Key=key, By="crw-1-conductor", Card="req_l1", On=["bolt/y"])], answers=answers)
    assert plan.row_card_close(None, "swancloud", "crw-1-conductor", key, reason="y is now a row of crew's landings card", acts=acts) == "req_l1"
    assert acts.ended == []
    assert "ended" not in capsys.readouterr().out


def test_the_sweep_keeps_a_rows_reading_live_though_a_card_of_the_bolts_own_was_closed_under_its_key():
    """sweep_judgment: y is a row of crew's landings card and its old land/y card was withdrawn, no card open under it;
    a batch closed with no card open is still taken out, and so is a reading whose bolt is no row."""
    closed = {"closed": {"land/y", "land/w", "batch/3"}}
    assert plan.sweep_judgment("swancloud", {"land/crew", "land/y", "batch/3"}, [], None, closed, {"land/y"}) == {
        "live": ["land/crew", "land/y"], "blind": []}
    assert plan.sweep_judgment("swancloud", {"land/crew"}, [], None, closed, set())["live"] == ["land/crew"]


def test_a_wait_whose_reading_crew_ended_says_it_ended_with_its_row_or_crew_card_end():
    assert plan.land_waited("land/y", None, False) == (
        "land/y: crew ended its reading, as its row was held or left its kit's landings card, or crew card end was run")


# ------------------------------------------------------------------------------------------- a card left elsewhere

def test_the_sweeps_raise_of_a_kits_card_handed_an_older_copy_posts_it_saying_that_copy_is_dead(monkeypatch):
    """rail-cards "A landings card left on the host the main level left"."""
    monkeypatch.setattr(plan, "plan_of", lambda fleet, label: plan.Plan(PLAN))
    r = {"label": "swancloud", "key": "land/crew", "group": "land"}
    acts, plain = LandActs({"y": row("y")}, answers=POSTED), LandActs({"y": row("y")}, answers=POSTED)
    assert plan.raise_landings_row(FLEET, dict(r, dead="req_k0"), acts) == "req_k1"
    assert plan.raise_landings_row(FLEET, r, plain) == "req_k1"
    dead, bare = [next(a for t, a in x.calls if t == "post_request")["summary"] for x in (acts, plain)]
    assert dead == f"{cards.DEAD}\n\n{bare}"


# ------------------------------------------------------------------------- the lands a send makes due (runner.lands_due)

class TestLandsDue:
    """rail-cards "A landings row is due one land for each send and head" (crew-lands-each-bolt-through-flumes-base-place,
    Decisions 4 and 5): runner.lands_due over the card's rows, the sends standing for them, requests.rec and the runner's
    report, each row due one land of its launch per send and head, in the card's order with the fixes of main first."""
    FIX = "fix/main/crew/red"

    def requests(self, *more):
        """requests.rec: y's base place 1, z's 2, a unit of y 3, the fix of crew's main main--red 4, then more."""
        import runner
        from test_runner import BOLT, held, rec
        return held(rec(1, "launch", "bolt/y", **dict(BOLT, Name="y")), rec(2, "launch", "bolt/z", **dict(BOLT, Name="z")),
                    rec(3, "launch", "unit/a", Base="bolt/y"),
                    rec(4, "launch", self.FIX, Kind="fix", Name="main--red", Base="main", Hold="submission", Intent="swancloud/main/crew",
                        Recipient="swancloud/ops"), *more)

    def reads(self, **more):
        """The runner on deneb: y's, z's and the fix's places launched, live with nothing submitted (or as more gives)."""
        from facts import ran
        launched = {1: "flume-0.17.0/bolt-submitted", 2: "flume-0.17.0/bolt-submitted", 4: "held", **more.pop("launched", {})}
        return ran(launched, label="swancloud", **more)

    def rows(self, *bolts, fix=False):
        out = ([dict(bolt="main--red", work=self.FIX, box=True, facts=dict(head=H2))] if fix else []) + [box(b) for b in bolts]
        return out

    def due(self, rows, sent, requests=None, reads=None, posted=(), work=None):
        import runner
        requests = requests if requests is not None else self.requests()
        # none of the fixtures has submitted anything: a base place live with no land reads none (runner.landing_of)
        return runner.lands_due(rows, sent, requests, reads or self.reads(), posted, work)

    def test_two_rows_in_the_cards_order(self):
        assert self.due(self.rows("z", "y"), {"bolt/y": ("req_1", H1[:7]), "bolt/z": ("req_1", H1[:7])}) == [("bolt/z", 2), ("bolt/y", 1)]

    def test_a_fix_of_main_first(self):
        sent = {"bolt/y": ("req_1", H1[:7]), self.FIX: ("req_1", H2[:7])}
        assert self.due([box("y"), dict(bolt="main--red", work=self.FIX, box=True, facts=dict(head=H2))], sent) == [
            (self.FIX, 4), ("bolt/y", 1)]

    def test_a_send_read_twice_posts_once(self):
        """Once posted, at its head, nothing more: posted names it, and the land stands undecided."""
        import runner
        from test_runner import rec
        requests = self.requests(rec(5, "land", "bolt/y", Of=1))
        posted = [dict(work="bolt/y", card="req_1", head=H1[:7], request=5)]
        assert self.due([box("y")], {"bolt/y": ("req_1", H1[:7])}, requests, posted=posted) == []
        assert self.due([box("y")], {"bolt/y": ("req_1", H1[:7])}, requests) == []

    def test_a_row_taking_main_first_posts_nothing_then_once_at_its_new_head(self):
        """The user ticked y at abc1234 and its land conflicted; its take-main fix merged, y proven at def5678, its own
        work unchanged: nothing while it takes main in, then one land at the new head on the same send."""
        from test_runner import rec
        requests = self.requests(rec(5, "land", "bolt/y", Of=1))
        posted = [dict(work="bolt/y", card="req_1", head=H1[:7], request=5)]
        reads = self.reads(launched={1: "flume-0.17.0/bolt-conflict"}, unplaced={5: "-"})
        sent = {"bolt/y": ("req_1", H1[:7])}
        assert self.due([taking_main("y")], sent, requests, reads, posted) == []
        assert self.due([box("y", H2)], sent, requests, reads, posted, work={"y": work()}) == [("bolt/y", 1)]
        assert self.due([box("y", H2)], sent, requests, reads, posted + [dict(work="bolt/y", card="req_1", head=H2[:7], request=6)],
                        work={"y": work()}) == []

    def test_a_stopped_row_posts_nothing_on_the_same_send_and_once_on_a_new_one(self):
        from test_runner import rec
        requests = self.requests(rec(5, "land", "bolt/y", Of=1))
        posted = [dict(work="bolt/y", card="req_1", head=H1[:7], request=5)]
        reads = self.reads(refused={5: "flume refused the submission: a place on bolt/y is live"})
        assert self.due([box("y", H2)], {"bolt/y": ("req_1", H1[:7])}, requests, reads, posted, work={"y": work()}) == []
        assert self.due([box("y", H2)], {"bolt/y": ("req_2", H2[:7])}, requests, reads, posted) == [("bolt/y", 1)]

    def test_a_bolt_started_before_bolts_were_base_places_posts_nothing(self):
        """It has no launch of its own, and its row no box (rail-cards "A bolt started before bolts were base places has
        no box"); a box given it all the same posts nothing."""
        assert self.due([box("w")], {"bolt/w": ("req_1", H1[:7])}) == []

    def test_a_held_row_posts_nothing(self):
        """A bolt carrying another bolt's work, held with no box (landing_rows), and a bolt whose units wait on a batch
        the user has not answered, no row at all (land_facts): whatever send stands, nothing is posted."""
        sent = {"bolt/y": ("req_1", H1[:7]), "bolt/z": ("req_1", H1[:7])}
        assert self.due([hold("y", "held: carries bolt x's work, its landing 1a2b3c4, which main lacks")], sent) == []
        assert self.due([], sent) == []

    def test_no_land_while_a_batch_waits(self):
        """review-batches "No land while a batch waits": the user's send stands at y's head, and y's unit a's latest
        change is in batch 7, which the user has not answered: y's landing facts read no row (landing_facts), the row
        saying it lands once the user has answered batch 7 (batch_waits), so the raise's rows hold none of y and no land
        of y's launch is due, though its send stands."""
        work = [("a", "unit", "merged")]
        assert plan.landing_facts("y", "crew", work, H1, None, set(), {"a": 7}, {}, 0, None) is None
        assert plan.batch_waits(["a"], set(), {"a": 7}) == "the user has not answered batch 7"
        rows = [box(b) for b in ["z"] if plan.landing_facts(b, "crew", work, H1, None, set(), {}, {}, 0, None)]
        rows += [box("y")] if plan.landing_facts("y", "crew", work, H1, None, set(), {"a": 7}, {}, 0, None) else []
        assert self.due(rows, {"bolt/y": ("req_1", H1[:7]), "bolt/z": ("req_1", H1[:7])}) == [("bolt/z", 2)]

    def test_an_outcome_crew_cant_tell_posts_nothing_again_at_that_head(self):
        import runner
        from test_runner import rec
        requests = self.requests(rec(5, "land", "bolt/y", Of=1))
        unread = {"deneb": runner.host_read("swancloud", "deneb", "5e1f0c2a" + "0" * 32, {}, {"answers.rec": "recfix refused it"})}
        assert self.due([box("y")], {"bolt/y": ("req_1", H1[:7])}, requests, unread) == []
        assert self.due([box("y")], {"bolt/y": ("req_1", H1[:7])}, requests, unread,
                        [dict(work="bolt/y", card="req_1", head=H1[:7], request=5)]) == []

    def test_a_send_whose_bolts_own_work_changed_posts_nothing(self):
        assert self.due([box("y", H2)], {"bolt/y": ("req_1", H1[:7])}, work={"y": work([LEASE])}) == []


class TestTheRaisePostsTheLands:
    """rail-cards "The user's send on a kit's landings card posts one land for each row it lands" and "A landings row is
    due one land for each send and head" (crew-lands-each-bolt-through-flumes-base-place, Decision 4): the raise of a
    kit's landings card that reads the user's send posts its lands by one plan write (plan.lands_change), each land of
    its row's launch in the card's order with the fixes of main first, an entry for each row naming the card, the head
    and the land's request, marked asked; a write replayed on a tip that holds them writes nothing."""
    FIX = "fix/main/crew/red"

    @pytest.fixture(autouse=True)
    def here(self, monkeypatch):
        monkeypatch.setattr(crew, "this_host", lambda: "mac-studio")

    def write(self, requests=None, entries=()):
        import runner
        from facts import FactsWrite
        text = runner.REQUESTS + "".join("\n" + "\n".join(r.lines()) + "\n" for r in (requests or TestLandsDue().requests()))
        return FactsWrite("%rec: Bolt\n%key: Bolt\n", files={"requests.rec": text}, entries=entries, label="swancloud")

    def rows(self):
        return [box("y"), box("z"), dict(bolt="main--red", work=self.FIX, box=True, facts=dict(head=H2))]

    SENT = {"bolt/y": ("req_k1", H1[:7]), "bolt/z": ("req_k1", H1[:7]), FIX: ("req_k1", H2[:7])}

    def test_one_write_posts_a_land_of_each_row_in_the_cards_order_the_fix_of_main_first(self, monkeypatch):
        monkeypatch.setenv("CREW_AGENT", "swancloud-ops")
        w = self.write()
        got = plan.lands_change(w, "crew", self.rows(), self.SENT, TestLandsDue().reads())
        assert got == [(self.FIX, 5, H2), ("bolt/y", 6, H1), ("bolt/z", 7, H1)]
        lands = [(r.get("Request"), r.get("Act"), r.get("Work"), r.get("Of")) for r in plan.Plan(w.files["requests.rec"]).recs("Request")][4:]
        assert lands == [("5", "land", self.FIX, "4"), ("6", "land", "bolt/y", "1"), ("7", "land", "bolt/z", "2")]
        assert (w.act, w.on, w.fields) == ("fix.merge", [self.FIX], dict(Card="req_k1", Head=H2, Request="5", Outcome="asked"))
        assert [(a, o, f) for _, a, o, f in w.also] == [
            ("bolt.submit", ["bolt/y"], dict(Card="req_k1", Head=H1, Request="6", Outcome="asked")),
            ("bolt.submit", ["bolt/z"], dict(Card="req_k1", Head=H1, Request="7", Outcome="asked"))]
        assert w.subject == "plan(crew): land main--red, y and z on the user's send"

    def test_a_write_replayed_on_a_tip_that_holds_the_lands_writes_nothing(self, monkeypatch):
        monkeypatch.setenv("CREW_AGENT", "swancloud-ops")
        w = self.write()
        plan.lands_change(w, "crew", self.rows(), self.SENT, TestLandsDue().reads())
        entries = [dict(Act=a, On=o, **f) for _, a, o, f in [(None, w.act, w.on, w.fields)] + w.also]
        again = self.write(plan.Plan(w.files["requests.rec"]).recs("Request"), entries)
        with pytest.raises(plan.Unposted):
            plan.lands_change(again, "crew", self.rows(), self.SENT, TestLandsDue().reads())
        assert plan.lands_posted(entries) == [dict(work=self.FIX, card="req_k1", head=H2, request="5"),
                                              dict(work="bolt/y", card="req_k1", head=H1, request="6"),
                                              dict(work="bolt/z", card="req_k1", head=H1, request="7")]

    def test_the_sends_standing_are_the_answered_cards_ticks_and_an_earlier_cards_kept_heads(self):
        entries = [dict(Act="card.close", Key="land/crew", By="swancloud-ops", Card="req_k0", Heads="w@1111111 main--red@2222222")]
        shown = plan.card_heads("y@abc1234 z@abc1234")
        assert plan.lands_sent(entries, "land/crew", "swancloud-ops", "req_k1", shown, ["y"]) == {
            "bolt/w": ("req_k0", "1111111"), self.FIX: ("req_k0", "2222222"), "bolt/y": ("req_k1", "abc1234")}

    def test_a_raise_reading_the_send_posts_the_lands_of_the_ticked_rows_and_a_second_raise_none(self, monkeypatch, capsys):
        """rail-cards "Read with no session of ops's running" and "Two bolts sent": the user ticked y and z; the raise
        posts two lands in the card's order, says each, tells no agent and leaves the card while they land; the next
        raise posts none."""
        monkeypatch.setenv("CREW_AGENT", "swancloud-ops")
        requests = TestLandsDue().requests()[:3]  # y's and z's base places and y's unit, no fix of main
        monkeypatch.setattr(plan, "runner_facts", lambda fleet, label: (requests, TestLandsDue().reads()))
        monkeypatch.setattr(plan, "plan_of", lambda fleet, label: plan.Plan(PLAN))
        held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234 z@abc1234")]
        answer = {"status": "answered", "turn": "agent", "version": 3, "answer": {"choiceIds": ["land:y", "land:z"]}}
        acts = LandActs({"y": row("y"), "z": row("z")}, held, answers={"get_request": (answer, None)})
        acts.requests = self.write(requests).files["requests.rec"]
        assert plan.raise_landings(FLEET, "swancloud", "crew", acts) == "req_k1"
        (subject, act, on, fields, also), = acts.posts
        assert (act, on, fields["Request"], fields["Card"], [o for _, o, _ in also]) == ("bolt.submit", ["bolt/y"], "4", "req_k1", [["bolt/z"]])
        out = capsys.readouterr().out
        assert "card land/crew: y is asked of the runner to land at abc1234 (request 4), on the user's send" in out
        assert "card land/crew: z is asked of the runner to land at abc1234 (request 5), on the user's send" in out
        assert "card land/crew: req_k1 is left as it is, the user having answered it" in out
        assert acts.told == []
        plan.raise_landings(FLEET, "swancloud", "crew", acts)
        assert len(acts.posts) == 1 and acts.told == []


def test_a_landing_is_read_and_recorded_by_a_host_away_from_the_kits_with_every_ssh_refused(monkeypatch):
    """bolt-teams "A landing's record rests on the state repository alone", its scenario "Read away from the kit's host"
    (read.5; crew-lands-each-bolt-through-flumes-base-place, Decision 6): the runners' branches are the drive's
    state, so a host that is not the kit's reads y's landing from the runner's report and records it, reaching no
    host."""
    from test_landing import ASKED, base_run

    def refused(*a, **k):
        raise AssertionError("ssh: connect to host deneb: refused")
    monkeypatch.setattr(crew, "on_machine", refused)
    monkeypatch.setattr(plan, "host_run", refused)
    monkeypatch.setattr(crew, "this_host", lambda: "macbook-pro")
    from facts import writes_at
    emitted = writes_at(monkeypatch, [ASKED])
    monkeypatch.setattr(plan, "unlanded_ask", lambda *a, **k: None)
    landed, said = plan.landing_read({}, "swancloud", "y", base_run("bolt-failed"), [ASKED])
    assert (landed, said) == (False, "landing refused, a check failed: check-full failed: tests:logic 3 failed (tests/py/test_landing.py)")
    assert [(e["Act"], e["On"], e["refused"]) for e in emitted] == [("bolt.submit", ["bolt/y"], said)]


# boomdrive's a-boomdrive-release-reports-its-own-version as y (tests/py/test_landed_on_main.py): its head, main's commit
# that landed it, the commit its unit a's place landed at on bolt/y, and an older crew's entries for it, its landing
# queued as #154 and stopped at the head.
ON_MAIN_HEAD, ON_MAIN, ON_MAIN_UNIT = "62d2f06" + "0" * 33, "6cfc4ae" + "0" * 33, "896e642" + "0" * 33
ON_MAIN_ENTRIES = [{"Act": "bolt.start", "On": ["bolt/y"], "At": "2026-11-11T20:00:00Z"},
                   {"Act": "bolt.submit", "On": ["bolt/y"], "Outcome": "queued", "Submission": "154", "Head": ON_MAIN_HEAD},
                   {"Act": "bolt.submit", "On": ["bolt/y"], "Outcome": "stopped", "Head": ON_MAIN_HEAD, "Why": "no origin"}]


def on_main(monkeypatch, held=(ON_MAIN_HEAD, ON_MAIN_UNIT)):
    """GitHub's main of each kit, as crew's cache would answer it, holding the commits in held, landed by ON_MAIN; and
    the drive's run record ON_MAIN_ENTRIES."""
    monkeypatch.setattr(plan, "main_tip", lambda repo: "e" * 40)
    monkeypatch.setattr(plan, "main_holds", lambda repo, tip, commits: {c: 0 if c in held else 1 for c in commits})
    monkeypatch.setattr(plan, "landed_by", lambda repo, tip, commits: ON_MAIN)
    monkeypatch.setattr(plan, "drive_entries", lambda fleet, label: list(ON_MAIN_ENTRIES))


def started_y(launched=None, **ran_):
    """swancloud's plan with y started, its unit a launched as request 1 and z started beside it, its unit b launched as
    request 2, neither with a launch of its own, and deneb's runner as facts.ran gives it, a's place landed on bolt/y
    at ON_MAIN_UNIT unless launched says otherwise: (the plan, {swancloud: (requests, runners)})."""
    from facts import launched as launch, ran
    p, requests = launch(["y", "z"], work=[("a", "y", [], "unit", []), ("b", "z", [], "unit", [])], base=False)
    reads = ran(launched or {1: "flume-0.20.0/landed-held", 2: "code"}, label="swancloud", commits={1: ON_MAIN_UNIT}, **ran_)
    return p, {"swancloud": (requests, reads)}


class TestTheSweepClosesABoltOnMain:
    """bolt-teams "A bolt read landed on main is recorded and closed by the first act that reads it", its scenarios
    "Nobody runs anything" and "Its host can't be told" (a-landed-bolt-is-closed-and-offered-no-more, Decision 5): the
    sweep's judgment lists a bolt read landed on its kit's main, marked main, under its host or, where crew can't tell
    it, the drive's main-level host (plan.landings_judged), and its read reads it with no land posted
    (plan.reap_judged); a bolt neither posted nor read landed is read by nothing."""

    @pytest.fixture(autouse=True)
    def world(self, monkeypatch):
        monkeypatch.setenv("CREW_AGENT", "swancloud-planner")
        on_main(monkeypatch)
        self.read = []
        monkeypatch.setattr(plan, "landing_read", lambda fleet, label, bolt, run=None, entries=None, card=True: self.read.append(bolt))

    def test_a_bolt_read_landed_on_main_with_nothing_posted_is_read(self):
        p, runs = started_y()
        judged = plan.landings_judged(FLEET, "swancloud", p, {}, runs)
        assert judged == {"mac-studio": [dict(bolt="y", kit="crew", dir="/c", stages=["merged"], main=True)]}
        plan.reap_judged(FLEET, "swancloud", judged["mac-studio"], runs["swancloud"])
        assert self.read == ["y"]

    def test_with_its_host_unknown_it_is_listed_under_the_main_level_host(self):
        p, runs = started_y()
        p.bolt("y").set("Repo", "afterthought/boomdrive")  # a kit no runner's report places (WHERE)
        fleet = {"drives": {"swancloud": {"label": "swancloud", "machine": "deneb"}}}
        judged = plan.landings_judged(fleet, "swancloud", p, {}, runs)
        assert judged == {"deneb": [dict(bolt="y", kit=None, dir=None, stages=["merged"], main=True)]}
        plan.reap_judged(fleet, "swancloud", judged["deneb"], runs["swancloud"])
        assert self.read == ["y"]

    def test_a_bolt_neither_posted_nor_read_landed_is_not_read(self, monkeypatch):
        on_main(monkeypatch, held=(ON_MAIN_HEAD,))
        p, runs = started_y()
        assert plan.landings_judged(FLEET, "swancloud", p, {}, runs) == {}
        plan.reap_judged(FLEET, "swancloud", [dict(bolt="y", kit="crew", dir="/c", stages=["merged"]),
                                              dict(bolt="z", kit="crew", dir="/c", stages=["code"])], runs["swancloud"])
        assert self.read == []

    # deneb (agentplot)'s sweep failed on every rail read while a bolt read landed on main stood, its host unknown:
    # card_sweep took a landing as exactly {bolt, kit, dir, stages}, kit and dir strings, where the rail's
    # landings_judged gives it marked main with kit and dir null (signal 2026-11-13-agentplot-ops-4b4a402a/01).
    @pytest.mark.parametrize("fleet,host,repo", [
        ({"drives": {"swancloud": {"label": "swancloud", "machine": "deneb"}}}, "deneb", "afterthought/boomdrive"),
        (FLEET, "mac-studio", None)], ids=["its-host-unknown", "under-its-host"])
    def test_the_sweep_takes_the_rails_judgment_of_a_bolt_on_main_as_the_rail_sends_it(self, monkeypatch, tmp_path, capsys, fleet, host, repo):
        import io
        p, runs = started_y()
        repo and p.bolt("y").set("Repo", repo)
        judged = plan.landings_judged(fleet, "swancloud", p, {}, runs)[host]
        monkeypatch.setattr(plan, "CARDS", tmp_path)
        monkeypatch.setattr(plan, "runner_facts", lambda fleet, label: runs["swancloud"])
        monkeypatch.setattr(plan.sys, "stdin", io.StringIO(json.dumps(dict(live=[], blind=[], landings=judged))))
        plan.card_sweep(fleet, argparse.Namespace(key=None, unit=None, label="swancloud"), object())
        assert json.loads(capsys.readouterr().out) == [] and self.read == ["y"]


class TestTheSweepReadsTheRailsJudgment:
    """What crew card sweep takes on standard input (plan.sweep_read): the rail's judgment as sweep_sessions sends it,
    each landing as landings_judged gives it, and nothing else."""

    PLACED = dict(bolt="y", kit="crew", dir="/c", stages=["merged"])
    UNPLACED = dict(bolt="y", kit=None, dir=None, stages=["merged"], main=True)

    @pytest.mark.parametrize("landings", [None, [], [PLACED], [dict(PLACED, main=True)], [UNPLACED], [PLACED, UNPLACED]])
    def test_the_rails_judgment_is_taken(self, landings):
        j = dict(live=["land/crew"], blind=["batch/"], **({} if landings is None else dict(landings=landings)))
        assert plan.sweep_read(json.dumps(j)) == j

    @pytest.mark.parametrize("landing", [
        dict(UNPLACED, main=None), dict(UNPLACED, main=False), {k: v for k, v in UNPLACED.items() if k != "main"},
        dict(UNPLACED, dir="/c"), dict(PLACED, main=False), dict(PLACED, kit=3), dict(PLACED, stages=[1]),
        dict(PLACED, stages="merged"), dict(PLACED, extra=1), {k: v for k, v in PLACED.items() if k != "dir"}, "y"],
        ids=["main-null", "main-false", "unplaced-unmarked", "half-placed", "placed-main-false", "kit-not-text",
             "stage-not-text", "stages-not-a-list", "a-key-of-its-own", "no-dir", "not-an-object"])
    def test_a_landing_not_as_the_rail_gives_it_is_refused(self, landing):
        assert plan.sweep_read(json.dumps(dict(live=[], blind=[], landings=[landing]))) is None

    @pytest.mark.parametrize("text", ["", "not json", "[]", '{"live": []}', '{"live": [], "blind": [], "x": 1}',
                                      '{"live": [1], "blind": []}', '{"live": [], "blind": [], "landings": {}}'])
    def test_a_judgment_not_the_rails_is_refused(self, text):
        assert plan.sweep_read(text) is None


class TestABoltOnMainIsNoRow:
    """bolt-teams "A bolt read landed on main is offered no more" and rail-cards "A landing the runner or Flume stopped
    keeps its box", its scenario "A stopped landing that landed" (a-landed-bolt-is-closed-and-offered-no-more, Decision
    6): a bolt whose landing reads landed is no row of its kit's landings card (plan.land_facts, plan.land_read), so no
    land of it is posted on any send (runner.lands_due) and no stop of it is said; one whose kit's main does not hold
    its work keeps its box and its stop."""
    STOP = "flume refused it: a place on bolt/z is live"

    @pytest.fixture(autouse=True)
    def world(self, monkeypatch):
        monkeypatch.setenv("CREW_AGENT", "swancloud-planner")
        self.mp = monkeypatch

    def stages(self, p, runs):
        self.mp.setattr(plan, "stages_for", lambda fleet, label, plan_, bolts, fetch=False: plan.Stages(fleet, plan_, {}, runs, label))

    def z(self):
        """z started, its unit b launched as request 1 and landed on bolt/z at ON_MAIN_UNIT, its base place request 2,
        live, and its land request 3, which the runner refused, recorded stopped at H1: (the plan, runs, entries)."""
        from facts import launched, ran
        from test_runner import held, rec
        p, requests = launched(["z"], work=[("b", "z", [], "unit", [])], base=True)
        reads = ran({1: "flume-0.20.0/landed-held", 2: "flume-0.17.0/bolt-submitted"}, label="swancloud",
                    commits={1: ON_MAIN_UNIT}, refused={3: self.STOP})
        entries = [{"Act": "bolt.start", "On": ["bolt/z"], "At": "2026-11-11T20:00:00Z"},
                   {"Act": "bolt.submit", "On": ["bolt/z"], "Card": "req_1", "Head": H1, "Request": "3", "Outcome": "asked"},
                   {"Act": "bolt.submit", "On": ["bolt/z"], "Head": H1, "Request": "3", "Outcome": "stopped", "Why": self.STOP}]
        return p, {"swancloud": (requests + held(rec(3, "land", "bolt/z", Of=2)), reads)}, entries

    def test_a_bolt_read_landed_on_main_is_no_row_and_no_land_of_it_is_posted(self):
        import runner
        on_main(self.mp)
        p, runs = started_y()
        self.stages(p, runs)
        assert plan.land_read(FLEET, "swancloud", p, p.bolt("y"), dict(WHERE["crew"], label="swancloud")) == (
            None, "landed at 6cfc4ae: crew closes it at its next read")
        pz, runz, entries = self.z()
        on_main(self.mp, held=(H1, ON_MAIN_UNIT))
        self.mp.setattr(plan, "drive_entries", lambda fleet, label: list(entries))
        self.stages(pz, runz)
        assert plan.stops(entries)["z"] == (H1, self.STOP)
        assert plan.land_read(FLEET, "swancloud", pz, pz.bolt("z"), dict(WHERE["crew"], label="swancloud")) == (
            None, "landed at 6cfc4ae: crew closes it at its next read")
        rows = []  # the rows the raise reads: neither y nor z is one
        requests, reads = runz["swancloud"]
        assert runner.lands_due(rows, {"bolt/y": ("req_1", H1[:7]), "bolt/z": ("req_2", H1[:7])}, requests, reads) == []
        assert runner.lands_due([box("z")], {"bolt/z": ("req_2", H1[:7])}, requests, reads) == [("bolt/z", 2)]  # were it a row

    def test_a_stopped_bolt_main_does_not_hold_keeps_its_box_and_its_stop(self):
        pz, runz, entries = self.z()
        on_main(self.mp, held=(ON_MAIN_UNIT,))
        self.mp.setattr(plan, "drive_entries", lambda fleet, label: list(entries))
        self.stages(pz, runz)
        st = plan.stages_for(FLEET, "swancloud", pz, [pz.bolt("z")])
        assert st.landing(pz.bolt("z"))["outcome"] == "stopped"
        assert st.main_landing(pz.bolt("z"))[1] == "crew's main does not hold abc1234, the head bolt z's newest landing carried"
        with pytest.raises(plan.Refusal, match="^bolt z's kit could not be read"):  # read on past the landing, as today
            plan.land_read(FLEET, "swancloud", pz, pz.bolt("z"), dict(WHERE["crew"], label="swancloud"))
        (row,) = plan.landing_rows(["z"], {"z": facts("z", H1)}, {}, plan.stops(entries))
        assert row["box"] is True and row["facts"]["stopped"] == (H1, self.STOP)


# --------------------------------------------------------------- landing on proof (a-proven-bolt-lands-on-proof)

def test_how_each_row_lands():
    """Decision 1 of a-proven-bolt-lands-on-proof (plan.lands_by): a bolt not marked lands on proof; one marked to stay,
    one the user left and one whose land at its head now was stopped land on the user's send, a stop at an old head
    holding nothing; a fix of main lands on the send always; and a bolt that would land on proof reads held while a hold
    stands on its kit or its drive, the rest landing as they would."""
    stop = [dict(submitted("y", H1), Outcome="stopped", Why=STOP, Request="7")]
    at_now = plan.stopped_at(plan.stops(stop), "y", H1)
    at_old = plan.stopped_at(plan.stops(stop), "y", H2)
    fix = dict(bolt="main--red", work="fix/main/crew/red", box=True, facts=dict(bolt="main--red", fix=True, head=H1))
    cases = {"not marked": (box("y"), False, False, None), "marked": (box("y"), True, False, None),
             "left": (box("y"), False, True, None), "stopped now": (box("y"), False, False, at_now),
             "stopped at an old head": (box("y", H2), False, False, at_old), "a fix of main": (fix, False, False, None)}
    assert at_now == STOP and at_old is None
    assert {k: plan.lands_by(r, stays, left, stopped, None) for k, (r, stays, left, stopped) in cases.items()} == {
        "not marked": "proof", "marked": "send", "left": "send", "stopped now": "send", "stopped at an old head": "proof",
        "a fix of main": "send"}
    p = plan.Plan(PLAN + "%rec: Hold\n\nKit: crew\nWhy: Cutover\n")
    drive = plan.Plan(PLAN + "%rec: Hold\n\nWhy: Cutover\n")
    for held in (plan.hold_on(p, "crew"), plan.hold_on(drive, "crew")):
        assert held is not None
        assert {k: plan.lands_by(r, stays, left, stopped, held) for k, (r, stays, left, stopped) in cases.items()} == {
            "not marked": "hold", "marked": "send", "left": "send", "stopped now": "send", "stopped at an old head": "hold",
            "a fix of main": "send"}
    assert plan.hold_on(p, "swancloud") is None and plan.hold_on(drive, "swancloud") == dict(kit=None, why="Cutover")


def proof_acts(mp, rows, entries=(), answers=None, text=PROVEN, lands=(), reads=None, **more):
    """LandActs for a raise of crew's landings card on PROVEN, y not marked to stay and z marked, its requests y's and z's
    base places and y's unit, then lands, read from deneb's runner as TestLandsDue reads them unless reads says
    otherwise, every land posted on requests.rec."""
    requests = TestLandsDue().requests()[:3] + list(lands)
    mp.setattr(crew, "this_host", lambda: "mac-studio")
    mp.setenv("CREW_AGENT", "swancloud-ops")
    mp.setattr(plan, "runner_facts", lambda fleet, label: (requests, reads or TestLandsDue().reads()))
    mp.setattr(plan, "plan_of", lambda fleet, label: plan.Plan(text))
    acts = LandActs(rows, entries, answers=answers if answers is not None else POSTED, **more)
    acts.requests = TestTheRaisePostsTheLands().write(requests).files["requests.rec"]
    return acts


def posted_heads(acts):
    """The rows each card the raise posted or changed shows, as its entry records them (card_heads)."""
    return [plan.card_heads(e.get("Heads")) for e in acts.emitted if e["Act"] in ("card.post", "card.update")]


def test_the_card_asks_only_about_the_rows_a_send_must_land(monkeypatch):
    """rail-cards "A landings card asks only about the rows a send must land" (Decision 3 of a-proven-bolt-lands-on-proof):
    y is not marked to stay, z is."""
    # A bolt not marked beside one marked: the card is an approve naming z alone, and y lands on proof.
    acts = proof_acts(monkeypatch, {"y": row("y"), "z": row("z")})
    plan.raise_landings(FLEET, "swancloud", "crew", acts)
    post = next(a for t, a in acts.calls if t == "post_request")
    assert (post["kind"], posted_heads(acts)) == ("approve", [[("z", "abc1234", False)]])
    assert [on for _, _, on, _, _ in acts.posts] == [["bolt/y"]]
    # A land on proof stopped at y's head: asked with its box, in the runner's words, and no land of y posted there.
    stopped = [dict(Act="bolt.submit", On=["bolt/y"], Form="proof", Head=H1, Request="4", Outcome="asked"),
               dict(Act="bolt.submit", On=["bolt/y"], Head=H1, Request="4", Outcome="stopped", Why=STOP)]
    acts = proof_acts(monkeypatch, {"y": row("y", stopped=(H1, STOP))}, stopped, drive=stopped)
    plan.raise_landings(FLEET, "swancloud", "crew", acts)
    post = next(a for t, a in acts.calls if t == "post_request")
    assert posted_heads(acts) == [[("y", "abc1234", False)]] and STOP in json.dumps(post)
    assert "Its land on proof at abc1234 was stopped, nothing of the bolt's" in json.dumps(post) and "spent" not in json.dumps(post)
    assert getattr(acts, "posts", []) == []
    # A bolt the user left: shown unticked, and no land on proof posted while it is left.
    left = [dict(Act="landing.left", On=["kit/crew"], By="swancloud-ops", Key="land/crew", Heads="y@abc1234")]
    acts = proof_acts(monkeypatch, {"y": row("y"), "z": row("z")}, drive=left)
    plan.raise_landings(FLEET, "swancloud", "crew", acts)
    assert posted_heads(acts) == [[("y", "abc1234", True), ("z", "abc1234", False)]]
    assert getattr(acts, "posts", []) == []
    # A bolt not marked taking main first is no row: the card asks for z alone.
    acts = proof_acts(monkeypatch, {"y": row("y"), "z": row("z")}, against_main={"y": [("main", ["README.md"])]})
    plan.raise_landings(FLEET, "swancloud", "crew", acts)
    assert posted_heads(acts) == [[("z", "abc1234", False)]] and getattr(acts, "posts", []) == []


class TestLandOnProof:
    """rail-cards "A proven bolt not marked to stay lands on proof, its land posted by the card's raise" and run-record
    "A land crew posts on proof is one entry marked as on proof" (Decision 1 of a-proven-bolt-lands-on-proof): each raise
    of a kit's landings card posts, after its sends' lands and by one plan write in ops's name, a land of each bolt not
    marked to stay that can land, its forecast clear of main, its entry marked Form: proof with no Card; y is not
    marked, z is."""

    @pytest.fixture(autouse=True)
    def here(self, monkeypatch):
        monkeypatch.setattr(crew, "this_host", lambda: "mac-studio")
        monkeypatch.setenv("CREW_AGENT", "swancloud-ops")
        self.mp = monkeypatch

    def acts(self, rows, entries=(), answers=None, **more):
        return proof_acts(self.mp, rows, entries, answers, **more)

    def test_a_proven_bolt_lands_on_proof_at_the_raise(self, capsys):
        """rail-cards "Proven at night" and "Read again"."""
        acts = self.acts({"y": row("y")})
        plan.raise_landings(FLEET, "swancloud", "crew", acts)
        (subject, act, on, fields, also), = acts.posts
        assert (subject, act, on, fields, also) == ("plan(crew): land y on proof", "bolt.submit", ["bolt/y"],
                                                    dict(Form="proof", Head=H1, Request="4", Outcome="asked"), [])
        assert "Card" not in fields
        assert "card land/crew: y is asked of the runner to land at abc1234 (request 4), on proof" in capsys.readouterr().out
        plan.raise_landings(FLEET, "swancloud", "crew", acts)
        assert len(acts.posts) == 1

    def test_a_bolt_forecast_in_conflict_lands_on_no_proof(self):
        """rail-cards "Forecast to conflict with main": no land, the conflict recorded and y taking main first; proven at
        a new head forecast clear of main, the next raise posts its land on proof."""
        acts = self.acts({"y": row("y")}, against_main={"y": [("main", ["README.md"])]})
        plan.raise_landings(FLEET, "swancloud", "crew", acts)
        assert getattr(acts, "posts", []) == []
        assert [(e["Act"], e["On"], e["Heads"]) for e in acts.emitted if e["Act"] == "forecast"] == [
            ("forecast", ["bolt/y"], "bolt/y@abc1234 main@e4f5a6b")]
        acts.rows, acts.against_main = {"y": row("y", H2)}, {}
        plan.raise_landings(FLEET, "swancloud", "crew", acts)
        (_, act, on, fields, _), = acts.posts
        assert (act, on, fields["Form"], fields["Head"]) == ("bolt.submit", ["bolt/y"], "proof", H2)

    def test_a_send_lands_before_the_proof_lands_of_one_raise(self, capsys):
        """rail-cards "Beside a send": the user sent the card ticking z, marked to stay, and y, not marked, reads proven;
        one raise posts z's land on the send and then y's on proof, in one plan write each."""
        held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="z@abc1234")]
        answer = {"status": "answered", "turn": "agent", "version": 3, "answer": {"approved": True}}
        acts = self.acts({"y": row("y"), "z": row("z")}, held, answers=dict(POSTED, get_request=(answer, None)))
        plan.raise_landings(FLEET, "swancloud", "crew", acts)
        assert [(s, on, f.get("Card"), f.get("Form"), f["Request"]) for s, _, on, f, _ in acts.posts] == [
            ("plan(crew): land z on the user's send", ["bolt/z"], "req_k1", None, "4"),
            ("plan(crew): land y on proof", ["bolt/y"], None, "proof", "5")]
        out = capsys.readouterr().out
        assert out.index("z is asked of the runner to land at abc1234 (request 4), on the user's send") < out.index(
            "y is asked of the runner to land at abc1234 (request 5), on proof")


def test_the_users_send_lands_a_bolt_whose_land_on_proof_was_stopped(monkeypatch, capsys):
    """rail-cards "A land on proof stopped" and "A landings row is due one land for each send and head" as
    a-proven-bolt-lands-on-proof modifies it (Decision 3): y's land on proof at abc1234 (request 5) was refused by the
    runner, a place on bolt/y being live, so land/crew asks for y; the user's send of it posts y's land at that head on
    the send, the card left as answered and not closed as a send spent, and the next raise posts nothing more."""
    from test_runner import rec
    stop = "flume refused it: a place on bolt/y is live"
    stopped = [dict(Act="bolt.submit", On=["bolt/y"], Form="proof", Head=H1, Request="5", Outcome="asked"),
               dict(Act="bolt.submit", On=["bolt/y"], Head=H1, Request="5", Outcome="stopped", Why=stop)]
    card = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@abc1234")]
    answer = {"status": "answered", "turn": "agent", "version": 3, "answer": {"approved": True}}
    acts = proof_acts(monkeypatch, {"y": row("y", stopped=(H1, stop))}, stopped + card, answers=dict(POSTED, get_request=(answer, None)),
                      drive=stopped, lands=[rec(5, "land", "bolt/y", Of=1)], reads=TestLandsDue().reads(refused={5: stop}))
    got = plan.raise_landings(FLEET, "swancloud", "crew", acts)
    assert [(s, on, f.get("Card"), f.get("Form"), f["Head"], f["Request"]) for s, _, on, f, _ in acts.posts] == [
        ("plan(crew): land y on the user's send", ["bolt/y"], "req_k1", None, H1, "6")]
    out = capsys.readouterr().out
    assert "y is asked of the runner to land at abc1234 (request 6), on the user's send" in out
    assert got == "req_k1" and "req_k1 is left as it is, the user having answered it" in out and "spent" not in out
    # The next raise reads y's land asked on the send, its stop behind it: nothing more is posted, and the card is left.
    acts.rows = {"y": row("y")}
    assert plan.raise_landings(FLEET, "swancloud", "crew", acts) == "req_k1" and len(acts.posts) == 1
    # crew card read, before the raise: the stop was crew's land on proof, and the user's send lands it
    heads = plan.card_heads("y@abc1234")
    said = plan.landing_lines("swancloud", answer, heads, stopped={"y": (H1, stop)}, posted={"y": "5"}, on_proof={"y"})
    assert said == ["  to land, in the card's order: y",
                    f"  y's land on proof at abc1234 was stopped, nothing of the bolt's: {stop}; the user's send lands it",
                    "  y: no land is posted for it yet: crew's next raise of the card posts it"]
    # Under a hold, the send stands: no land is posted, and the card is left as answered, its send not spent.
    capsys.readouterr()
    acts = proof_acts(monkeypatch, {"y": row("y", stopped=(H1, stop))}, stopped + card, answers=dict(POSTED, get_request=(answer, None)),
                      drive=stopped, lands=[rec(5, "land", "bolt/y", Of=1)], reads=TestLandsDue().reads(refused={5: stop}),
                      text=PROVEN + "%rec: Hold\n\nKit: crew\nWhy: Cutover\n")
    assert plan.raise_landings(FLEET, "swancloud", "crew", acts) == "req_k1" and getattr(acts, "posts", []) == []
    out = capsys.readouterr().out
    assert "req_k1 is left as it is, the user having answered it" in out and "spent" not in out


def test_a_bolt_whose_forecast_could_not_be_made_lands_on_no_proof(monkeypatch, capsys):
    """rail-cards "A proven bolt not marked to stay lands on proof" (Decision 1 of a-proven-bolt-lands-on-proof; read.1):
    y reads clear of main only once a forecast found no conflict, so where git could not tell, no land on proof is
    posted and the raise says why; once the forecast is made and clear, the next raise posts it."""
    acts = proof_acts(monkeypatch, {"y": row("y")})
    made = acts.forecast
    acts.forecast = lambda label, kit, bolts, held=(): ({b: [("main", None)] for b in bolts},
                                                         {b: "git merge-tree could not tell in crew on mac-studio" for b in bolts},
                                                         {"main": MAIN})
    plan.raise_landings(FLEET, "swancloud", "crew", acts)
    assert getattr(acts, "posts", []) == [] and not any(t == "post_request" for t, _ in acts.calls)
    assert ("card land/crew: y's forecast against main could not be made (git merge-tree could not tell in crew on mac-studio), "
            "so no land on proof is posted for it until one is") in capsys.readouterr().out
    acts.forecast = made
    plan.raise_landings(FLEET, "swancloud", "crew", acts)
    assert [(on, f["Form"]) for _, _, on, f, _ in acts.posts] == [(["bolt/y"], "proof")]


def test_a_hold_or_a_drop_found_at_the_writes_tip_posts_no_land(monkeypatch):
    """plan.1 (Decision 6 of a-proven-bolt-lands-on-proof): lands_change re-checks at the tip it is applied to, so a hold
    on crew or on the drive put while the raise ran posts no land, on proof or on the send, and a bolt gone from the plan
    there, or marked to stay there, is posted no land on proof."""
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="z@abc1234")]
    answer = {"status": "answered", "turn": "agent", "version": 3, "answer": {"approved": True}}
    for tip in (PROVEN + "%rec: Hold\n\nKit: crew\nWhy: Cutover\n", PROVEN + "%rec: Hold\n\nWhy: Cutover\n"):
        acts = proof_acts(monkeypatch, {"y": row("y"), "z": row("z")}, held, answers=dict(POSTED, get_request=(answer, None)))
        acts.tip = plan.Plan(tip)
        plan.raise_landings(FLEET, "swancloud", "crew", acts)
        assert acts.posts == []
    for tip in (PLAN.replace("Bolt: y\nRepo: crew\nPath: flume\nStays: yes\n\n", ""), PLAN):
        acts = proof_acts(monkeypatch, {"y": row("y")})
        acts.tip = plan.Plan(tip)
        plan.raise_landings(FLEET, "swancloud", "crew", acts)
        assert acts.posts == []


Y_AT, W_AT = "9f1c2ab" + "0" * 33, "4d5e6f7" + "0" * 33


def landed_on_proof(bolt, commit, at, n):
    """The run record of a bolt of crew landed on proof: its land posted on proof, then its bolt.land at main's commit."""
    return [dict(Act="bolt.submit", On=[f"bolt/{bolt}"], Form="proof", Head=H1, Request=str(n), Outcome="asked", At=at),
            dict(Act="bolt.land", On=[f"bolt/{bolt}"], Repo="crew", Head=commit, At=at)]


Y_LANDED = landed_on_proof("y", Y_AT, "2026-11-13T03:12:40Z", 4)
W_LANDED = landed_on_proof("w", W_AT, "2026-11-13T04:40:02Z", 5)
# z alone in the plan, marked to stay, once y and w have landed and left it
ONLY_Z_STAYS = "%rec: Bolt\n\nBolt: z\nRepo: crew\nPath: flume\nStays: yes\n\n%rec: Unit\n\n"
PENDING = {"get_request": ({"status": "pending", "turn": "you", "version": 2}, None)}


def test_a_bolt_landed_on_proof_is_told_until_the_user_taps(monkeypatch):
    """rail-cards "A bolt that landed on proof is told on its kit's landings card" (Decision 4 of
    a-proven-bolt-lands-on-proof): y and w of crew landed on proof, z is marked to stay."""
    def raise_(rows, entries, answers):
        acts = proof_acts(monkeypatch, rows, entries, answers, text=ONLY_Z_STAYS, drive=[e for e in entries if e["Act"] != "card.post"])
        got = plan.raise_landings(FLEET, "swancloud", "crew", acts)
        return acts, got
    none = {"z": {"bolt": "z"}}  # z reads no row that can land

    # The notice: no row waits, so land/crew is a one-tap notice in ops's name naming y and its commit.
    acts, got = raise_(none, Y_LANDED, POSTED)
    post = next(a for t, a in acts.calls if t == "post_request")
    assert (got, post["kind"], post["intent"], post["title"]) == ("req_k1", "fyi", "tell", "Landed on crew's main: y")
    assert acts.emitted[-1]["Heads"] == "y@9f1c2ab:landed"

    # Another lands while it is open: the notice is changed in place, naming y and then w.
    notice = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="y@9f1c2ab:landed")]
    acts, got = raise_(none, Y_LANDED + W_LANDED + notice, PENDING)
    change = next(a for t, a in acts.calls if t == "update_request")
    assert (got, change["requestId"], change["changeNote"]) == ("req_k1", "req_k1", "w landed on proof at 4d5e6f7")
    assert acts.emitted[-1]["Heads"] == "y@9f1c2ab:landed w@4d5e6f7:landed"

    # The user taps it: recorded closed as Pending You ended it, and no later card tells y or w.
    both = [dict(notice[0], Heads="y@9f1c2ab:landed w@4d5e6f7:landed")]
    acts, got = raise_(none, Y_LANDED + W_LANDED + both, {"get_request": ({"status": "resolved", "version": 3}, None)})
    assert got is None and not any(t == "post_request" for t, _ in acts.calls)
    closed = acts.held
    assert plan.told_on(Y_LANDED + W_LANDED + closed, "land/crew", "swancloud-ops", "crew") == []
    acts, _ = raise_({"z": row("z")}, Y_LANDED + W_LANDED + closed, POSTED)
    assert acts.emitted[-1]["Act"] == "card.post" and acts.emitted[-1]["Heads"] == "z@abc1234"

    # A bolt marked to stay reads proven while the notice is open: a card following it asks for z, opening with y.
    acts, got = raise_({"z": row("z")}, Y_LANDED + notice, dict(POSTED, **PENDING, post_request=({"requestId": "req_k2", "version": 1}, None)))
    post = next(a for t, a in acts.calls if t == "post_request")
    assert (got, post["kind"], post["follows"]) == ("req_k2", "approve", "req_k1")
    assert post["summary"].startswith("Landed on proof since your last look: y at 9f1c2ab (2026-11-13 03:12Z).")
    assert acts.emitted[-1]["Heads"] == "z@abc1234 y@9f1c2ab:landed"

    # A card asking for z waits on the user and y lands on proof: it is changed in place, its note naming y.
    asking = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="z@abc1234")]
    acts, got = raise_({"z": row("z")}, Y_LANDED + asking, PENDING)
    change = next(a for t, a in acts.calls if t == "update_request")
    assert (got, change["changeNote"]) == ("req_k1", "y landed on proof at 9f1c2ab")
    assert acts.emitted[-1]["Heads"] == "z@abc1234 y@9f1c2ab:landed"

    # A card that told y followed or withdrawn before the user saw it: the next card still tells y.
    for state, outcome in (("closed", plan.FOLLOWED), ("withdrawn", "no bolt waits to land on its main")):
        gone = notice + [dict(Act="card.close", Key="land/crew", By="swancloud-ops", Card="req_k1", State=state, Outcome=outcome)]
        assert plan.told_on(Y_LANDED + gone, "land/crew", "swancloud-ops", "crew") == [("y", Y_AT, "2026-11-13T03:12:40Z")]
    answered = notice + [dict(Act="card.answer", Key="land/crew", By="swancloud-ops", Card="req_k1", Answer="approved")]
    assert plan.told_on(Y_LANDED + answered, "land/crew", "swancloud-ops", "crew") == []
    sent = [dict(e, Form=None) if e["Act"] == "bolt.submit" else e for e in Y_LANDED]  # landed on a send: told by none
    assert plan.told_on(sent, "land/crew", "swancloud-ops", "crew") == []


def test_a_hold_posts_no_land_and_its_lift_posts_what_came_due(monkeypatch, capsys):
    """rail-cards "A hold on the drive or the kit posts no land" (Decision 6 of a-proven-bolt-lands-on-proof): y, not
    marked to stay, reads proven, and the user sent land/crew ticking z, marked; under a hold on crew no land is posted,
    on the send or on proof, and crew card read says the send stands until the lift; the raise after the lift posts z's
    land on the send and then y's on proof; a hold on the drive outlasts the kit's lift."""
    held = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="z@abc1234")]
    answer = {"status": "answered", "turn": "agent", "version": 3, "answer": {"approved": True}}

    def raise_(text):
        acts = proof_acts(monkeypatch, {"y": row("y"), "z": row("z")}, held, dict(POSTED, get_request=(answer, None)), text=text)
        plan.raise_landings(FLEET, "swancloud", "crew", acts)
        return acts
    kit_held = PROVEN + "%rec: Hold\n\nKit: crew\nWhy: Cutover\n"
    acts = raise_(kit_held)
    assert getattr(acts, "posts", []) == []
    assert "card land/crew: no land is posted while the hold on crew's landings stands: Cutover" in capsys.readouterr().out
    heads = plan.card_heads("z@abc1234")
    assert plan.landing_lines("swancloud", answer, heads, hold=plan.hold_on(plan.Plan(kit_held), "crew"))[-1] == (
        "  z: no land is posted while the hold on crew stands; the user's send stands, and lands z once the hold is lifted")
    assert plan.landing_lines("swancloud", answer, heads)[-1] == (
        "  z: no land is posted for it yet: crew's next raise of the card posts it")
    acts = raise_(PROVEN)  # the hold lifted (crew plan go): the raise it hands
    assert [(s, f.get("Form")) for s, _, _, f, _ in acts.posts] == [("plan(crew): land z on the user's send", None),
                                                                    ("plan(crew): land y on proof", "proof")]
    drive_held = PROVEN + "%rec: Hold\n\nWhy: Cutover\n"
    acts = raise_(drive_held)
    assert getattr(acts, "posts", []) == []
    assert "no land is posted while the hold on the landings of swancloud's every kit stands: Cutover" in capsys.readouterr().out


def proof_read(bolts, lands, cards=(), logs=(), text=PROVEN):
    """A rail read of swancloud on its main machine once its sweep acted, crew's land row naming bolts, [(bolt, head,
    can)], each landing as lands says ({bolt: lands_by's word}), the cards open as given, each in swancloud-ops's name on
    mac-studio with its last post among logs, the drive's run record."""
    land = dict(label="swancloud", group="land", key="land/crew", fixes=[], lands=dict(lands),
                bolts=[dict(bolt=b, host="mac-studio", can=can, head=h) for b, h, can in bolts])
    return dict(found=[("swancloud", "afterthought/crew-state", "tip", plan.Plan(text))], kits={"swancloud": list(KITS)}, sv={},
                rows=[land], logs={"swancloud": list(logs)}, swept={},
                cards=[dict(label="swancloud", card=c, key="land/crew", by="swancloud-ops", host="mac-studio") for c in cards])


def test_the_rail_read_raises_a_kit_whose_bolt_is_due_a_land_on_proof(monkeypatch):
    """rail-cards "Proven since the last read" (Decision 2 of a-proven-bolt-lands-on-proof): y, not marked to stay,
    reads proven on the main level's host with no card of crew open; that read raises crew's card, whose raise posts y's
    land on proof and posts no card, and the next read raises none for y."""
    land = proof_acts(monkeypatch, {"y": row("y")})
    acts = SweepActs(land)
    got = plan.sweep_moved(FLEET, proof_read([("y", H1, True)], {"y": "proof"}), acts)
    assert got == {"raised": [dict(label="swancloud", kit="crew", was=None, now=None, card=None, said=None, sent=False, rows=[],
                                   proven=["y"])], "unread": []}
    assert [(on, f["Form"]) for _, _, on, f, _ in land.posts] == [(["bolt/y"], "proof")]
    assert not any(t == "post_request" for t, _ in land.calls)
    acts = SweepActs(land)
    assert plan.sweep_moved(FLEET, proof_read([("y", H1, True)], {"y": "proof"}, logs=land.held), acts) == {"raised": [], "unread": []}
    assert acts.raised == [] and len(land.posts) == 1
    assert ("landings cards raised for bolts due a land on proof:\n  land/crew (swancloud): y: raised, no card left open"
            in plan.rail_text(FLEET, ["swancloud"], dict(found=[], rows=[], cards=[], sv={}, unread={}, kits={}, runs={}, moved=got),
                              plan.utc("2026-11-13T04:00:00Z")))


def test_a_bolt_due_a_land_on_proof_beside_an_open_card_raises_it_once(monkeypatch):
    """rail-cards "Proven while a card asks for a bolt marked to stay": land/crew waits on the user with z, marked, and y,
    not marked, reads proven; the read raises the card once, for y alone, its raise posting y's land on proof and leaving
    the card's rows as they stand."""
    shown = [dict(Act="card.post", Key="land/crew", By="swancloud-ops", Card="req_k1", Heads="z@abc1234")]
    land = proof_acts(monkeypatch, {"y": row("y"), "z": row("z")}, shown, PENDING)
    acts = SweepActs(land)
    got = plan.sweep_moved(FLEET, proof_read([("y", H1, True), ("z", H1, True)], {"y": "proof", "z": "send"}, ["req_k1"], shown), acts)
    assert acts.raised == ["crew"] and [(m["rows"], m["proven"], m["card"]) for m in got["raised"]] == [([], ["y"], "req_k1")]
    assert [on for _, _, on, _, _ in land.posts] == [["bolt/y"]]
    assert not any(t in ("post_request", "update_request") for t, _ in land.calls)


def test_a_held_kit_is_raised_by_no_read(monkeypatch):
    """rail-cards "Under a hold": a hold on crew, or on the drive, stands and y reads proven: no read raises land/crew
    for y."""
    for hold in ("Kit: crew\n", ""):
        acts = SweepActs(None)
        read = proof_read([("y", H1, True)], {"y": "hold"}, text=PROVEN + f"%rec: Hold\n\n{hold}Why: Cutover\n")
        assert plan.sweep_moved(FLEET, read, acts) == {"raised": [], "unread": []} and acts.raised == []


def test_a_row_of_bolts_landing_on_proof_owes_no_card():
    """Decision 2 of a-proven-bolt-lands-on-proof (plan.sweep_judged): a land row whose card has no row to ask about and no
    bolt to tell (asks false) is owed no card by the sweep, so no read raises it changing nothing; one that asks is owed
    one."""
    owners = {"land/crew": ("swancloud-ops", "mac-studio")}
    now = plan.utc("2026-11-13T04:00:00Z")
    proven = dict(label="swancloud", group="land", key="land/crew", bolts=[dict(bolt="y", host="mac-studio", can=True, head=H1)],
                  fixes=[], asks=False, lands={"y": "proof"})
    assert plan.sweep_judged("mac-studio", [proven], [], [], owners, set(), set(), now)["none"] == []
    asks = dict(proven, asks=True, lands={"y": "send"})
    assert plan.sweep_judged("mac-studio", [asks], [], [], owners, set(), set(), now)["none"] == [asks]
