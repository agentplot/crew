"""What crew bolts shows of a submission (bolt-teams "A submission's number is on its bolt's row from the submit",
teams.22): plan.bolts_data and plan.bolts_text show a piece's submission as the runner carries it and a bolt's landing
as the run record holds it and the runner reports it, never from sluice's queue, which crew reads nothing of (crew
record 0056 points 1 and 4; crew-lands-each-bolt-through-flumes-base-place, Decision 1), beside the rest of crew bolts
in test_rail.py and test_chores.py."""
import pytest

from facts import plan_text

import crew
import plan

# ------------------------------------------------------------------------------------------------- crew bolts

BOX = "chuck-herdr-alpha"
FLEET = {"partitions": {"wldn": {"label": "wldn", "machine": BOX}},
         "hosts": {BOX: {"ssh": BOX, "home": "/h/box"}}}


@pytest.fixture(autouse=True)
def here(monkeypatch):
    monkeypatch.setattr(crew, "this_host", lambda: "mac-studio")
    monkeypatch.setenv("CREW_AGENT", "chuck")


def bolts(at="code", carries=None, logs=None):
    """crew bolts of wldn's plan, its bolt y started and its work launched, taken by the runner on the box, which keeps
    switchboard-kit in /kit/main, its base place live with no land asked and a's place at the Flume 0.3.6 status fixture
    named (tests/py/flume-0.3.6/<at>.json),
    the kit read as the gather reads it, with no queue of sluice's, and wldn's run record the entries logs gives."""
    from facts import FactsWrite, ran
    import runner
    w = FactsWrite(plan_text(bolts=[("y", "switchboard-kit", "swb-1")],
                             units=[("a", "switchboard-kit", "y", []), ("b", "switchboard-kit", "y", []), ("bump", "switchboard-kit", "y", [], "chore")]))
    act, work, given = runner.bolt_launch(w.plan, "y", "wldn")  # y's base place, request 1, as a start launches it
    plan.request(w, act, work, **given)
    plan.reach_places(FLEET, w, "y")
    requests = plan.Plan(w.files.get("requests.rec") or runner.REQUESTS).recs("Request")
    kit = {"ok": True, "main": [], "fixes": [], "places": {}, "bolts": {"y": {"exists": True, "head": "d" * 40, "changes": [],
                                                                         **({"carries": carries} if carries else {})}}}
    sv = {BOX: {"ok": True, "kits": {"/kit/main": kit}}}
    return plan.bolts_data(FLEET, ["wldn"], [("wldn", "WilldanGroup/crew-state", "abcdef1" + "0" * 33, w.plan)], sv, {},
                           runs={"wldn": (requests, ran({1: "flume-0.17.0/bolt-submitted", 2: at}, host=BOX, label="wldn",
                                                         repository="/kit/main"))},
                           logs={"wldn": logs} if logs is not None else None)


def held(d):
    return d["partitions"][0]["plans"][0]["bolts"][0]


def test_crew_bolts_says_a_bolt_carrying_another_bolts_work_is_held_naming_it():
    """bolt-teams "crew bolts says a bolt carries another bolt's work" (plan.8): a bolt whose kit's read says it holds
    another bolt's landing main lacks shows it held on the line under its head, naming that bolt and its landing, and
    carries it in its JSON as carries; a bolt carrying none shows no such line."""
    d = bolts(carries={"x": ["f5e67f35" + "0" * 32]})
    assert held(d)["carries"] == {"x": ["f5e67f35" + "0" * 32]}
    assert plan.bolts_text(d).splitlines()[2] == (
        "  landing: held: carries bolt x's work, its landing f5e67f3, which main lacks; a bolt never carries another bolt's "
        "work to main, so it lands once main holds that work, by the landing of bolt x")
    assert held(bolts())["carries"] == {} and "carries" not in plan.bolts_text(bolts())


A_LINE = "  a                                        submitted #413 flume/change--teams-cross-to-flume-as-their-bolts-land"


def test_crew_bolts_shows_a_merge_under_test_on_its_line_and_the_landing_on_the_head_line():
    """bolt-teams "A unit's merge under test", "A bolt's landing queued on main" and "Read again after the session that
    submitted it ended": a's line says its submission as the runner carries Flume's status of its place, under test as
    #413, and y's head line its landing as the run record holds it, queued as #355; the JSON gives a's stage from the
    runner and no line a submission, nor the bolt a landing or a submissions error, read from sluice's queue."""
    queued = [dict(Act="bolt.submit", On=["bolt/y"], Outcome="queued", Submission="355", Head="d" * 40)]
    d = bolts(at="submitted", logs=queued)
    b = held(d)
    assert (b["units"][0]["flume"]["stage"], b["units"][0]["flume"]["submission"]) == ("submitted", "413")
    assert not any("submission" in x for x in b["units"] + b["fixes"]) and "submissions_error" not in b
    assert b["landing"] == {"outcome": "none"}  # its base place live with no land asked, as the runner reports it
    out = plan.bolts_text(d).splitlines()
    assert out[1] == f"y  switchboard-kit  @ {BOX}, in Flume stream wldn  active  landing queued as #355"
    assert A_LINE in out


def test_once_decided_no_line_shows_a_submission():
    """bolt-teams "Decided": the runner carries a's place landed, so a reads merged and its line names no number."""
    d = bolts(at="landed")
    assert held(d)["units"][0]["stage"] == "merged"
    assert "#" not in plan.bolts_text(d)


def test_sluices_record_cant_be_read_and_nothing_is_said_of_it():
    """bolt-teams "sluice's record can't be read": the kit's read carries nothing of sluice's queue, and none is asked;
    a's line still says its submission from the runner, and the head line says nothing of the queue."""
    out = plan.bolts_text(bolts(at="submitted")).splitlines()
    assert out[1] == f"y  switchboard-kit  @ {BOX}, in Flume stream wldn  active"
    assert A_LINE in out and not any("can't be read" in line for line in out)
