"""What crew's own landing reads of sluice's queue and records, and what crew bolts shows of a submission (bolt-teams
"A submission's number is on its bolt's row from the submit", teams.22): the read of an overview's standing
submissions, gather.submissions_of, on sluice 0.51.3's own overview (tests/py/sluice-0.51.3/), every field guarded and
a document of another schema said, which the landing reads before it submits (plan.queue_read); sluice's record of
every submission a branch has had, gather.decided_of, as the landing reads it once, on its own `status --all`
documents;
whose line each submission is, plan.submission_rows, which crew's own landing reads; and that crew bolts,
plan.bolts_data and plan.bolts_text, shows a piece's submission as the runner carries it and a bolt's landing as the
run record holds it, never from sluice's queue (crew record 0056 points 1 and 4), beside the rest of crew bolts in
test_rail.py and test_chores.py."""
import json
import pathlib

import pytest

from facts import plan_text

import crew
import gather
import plan

RECORDED = pathlib.Path(__file__).parent / "sluice-0.51.3"


def overview():
    return json.loads((RECORDED / "overview-standing.json").read_text())


# ------------------------------------------------------------------------------------- the gather's read of the queue

def test_the_overview_gives_each_standing_submission_with_its_branch_state_and_where_it_came_from():
    assert gather.submissions_of(overview()) == ([
        {"id": 317, "branch": "bolt/crews-chores-of-the-24th-night", "head": "aa1a9c7fa2f7a64d505f4c6a99e0f76b5f948d2b",
         "state": "testing", "worktree": "chore/a-proven-bolts-batch-is-reckoned-at-once-wherever-it-lives", "pull_head": None,
         "submitted": "2026-10-28T00:01:43Z", "started": "2026-10-28T01:03:27Z"},
        {"id": 318, "branch": "bolt/crews-chores-of-the-24th-night", "head": "ed8e7a92d5f8385895c2cf99d277a4c147738e6f",
         "state": "queued", "worktree": "chore/a-stage-drives-a-browser-only-the-kits-way", "pull_head": None,
         "submitted": "2026-10-28T00:23:06Z", "started": None},
        {"id": 355, "branch": "main", "head": "b49230ce242d7a965174cc0f52589739ed97f375", "state": "queued",
         "worktree": "pull/198", "pull_head": "bolt/crew-opens-no-tab-the-user-does-not-use",
         "submitted": "2026-10-28T15:30:29Z", "started": None}], None)


def test_a_submission_under_test_takes_the_start_of_its_candidates_checks_and_a_candidate_only_formed_gives_none():
    """The design's Decision 2: a standing submission under test is the kit's from the start of its checks."""
    doc = overview()
    doc["branches"][0]["candidates"][0]["started"] = 7
    doc["branches"][0]["candidates"][1]["state"] = "testing"
    got, _ = gather.submissions_of(doc)
    assert [(s["id"], s["started"]) for s in got] == [(317, None), (318, None), (355, None)]
    del doc["branches"][0]["candidates"]
    assert gather.submissions_of(doc)[0][0]["started"] is None


def test_an_empty_queue_is_none_standing_and_not_a_failure():
    doc = dict(overview(), branches=[dict(b, submissions=[]) for b in overview()["branches"]])
    assert gather.submissions_of(doc) == ([], None)


def test_a_field_missing_or_mistyped_is_none_and_a_submission_with_no_number_or_branch_is_left_out():
    """read.2: a missing value never becomes text."""
    doc = overview()
    subs = doc["branches"][0]["submissions"]
    del subs[0]["state"], subs[0]["from"]
    subs[1]["id"] = "318"
    doc["branches"][1]["submissions"][0]["from"] = "pull/198"
    doc["branches"][1]["submissions"].append({"id": True, "branch": "main"})
    doc["branches"][1]["submissions"].append("#356")
    got, why = gather.submissions_of(doc)
    assert why is None and [(s["id"], s["state"], s["worktree"], s["pull_head"]) for s in got] == [
        (317, None, None, None), (355, "queued", None, None)]


def test_a_submission_with_no_branch_of_its_own_takes_its_branch_views():
    doc = overview()
    del doc["branches"][0]["submissions"][0]["branch"]
    assert gather.submissions_of(doc)[0][0]["branch"] == "bolt/crews-chores-of-the-24th-night"


@pytest.mark.parametrize("doc, why", [
    (dict(overview(), schema="sluice/overview@2"), "sluice overview printed sluice/overview@2, not the sluice/overview@1 crew reads"),
    ({"branches": []}, "sluice overview printed no schema, where crew reads sluice/overview@1"),
    ([], "sluice overview printed no schema, where crew reads sluice/overview@1"),
    (dict(overview(), branches=None), "sluice overview's sluice/overview@1 holds no list of branches")])
def test_a_document_of_another_schema_is_said_never_read_as_an_empty_queue(doc, why):
    assert gather.submissions_of(doc) == (None, why)


# ------------------------------------------------------------------------- sluice's record of every submission had

def recorded(name):
    return json.loads((RECORDED / name).read_text())


def test_a_branchs_record_gives_every_submission_it_had_with_when_it_was_submitted_and_told():
    """crew-board "A held bolt's decided merges": sluice 0.51.3's record of a bolt's branch, landed and withdrawn."""
    got, why = gather.decided_of(recorded("status-bolt-all.json"))
    assert why is None and [(s["id"], s["state"], s["worktree"], s["submitted"], s["told"]) for s in got] == [
        (356, "landed", "fix/crew-costs-an-idle-host-nothing/take-main-448c543", "2026-10-28T15:47:07Z", "2026-10-28T15:48:24Z"),
        (357, "landed", "chore/a-wait-ends-with-the-session-that-started-it", "2026-10-28T16:10:48Z", "2026-10-28T16:21:02Z"),
        (358, "withdrawn", "unit/crew-keeps-no-card-wait-and-a-row-carries-its-submission-number", "2026-10-28T17:47:07Z", "2026-10-28T17:47:13Z"),
        (359, "withdrawn", "unit/crew-keeps-no-card-wait-and-a-row-carries-its-submission-number", "2026-10-28T17:56:48Z", "2026-10-28T18:23:56Z"),
        (361, "landed", "unit/crew-keeps-no-card-wait-and-a-row-carries-its-submission-number", "2026-10-28T18:36:05Z", "2026-10-28T18:55:42Z"),
        (362, "landed", "unit/a-rail-refresh-after-no-change-reads-nothing", "2026-10-28T18:57:11Z", "2026-10-28T19:09:03Z")]
    assert (got[0]["branch"], got[0]["head"], got[0]["pull_head"]) == (
        "bolt/crew-costs-an-idle-host-nothing", "e79d32a4061c5a028dbd765d6c397458f249719b", None)


def test_mains_record_names_a_landing_by_its_pull_request_and_a_withdrawal_never_told_by_its_time():
    got, _ = gather.decided_of(recorded("status-main-all.json"))
    assert [(s["id"], s["state"], s["worktree"], s["pull_head"], s["told"]) for s in got] == [
        (305, "withdrawn", "pull/171", "design/bolt-cycle-time", "2026-10-27T18:34:17Z"),
        (363, "landed", "pull/200", "bolt/crew-costs-an-idle-host-nothing", "2026-10-28T19:13:46Z"),
        (364, "landed", "pull/201", "design/the-words", "2026-10-28T19:23:54Z")]


def test_a_record_field_missing_or_mistyped_is_none_and_one_with_no_number_is_left_out():
    """read.2."""
    doc = recorded("status-bolt-all.json")
    del doc["submissions"][0]["told"], doc["submissions"][0]["from"]
    doc["submissions"][1]["submitted"] = 1730000000
    doc["submissions"][2]["id"] = "358"
    del doc["submissions"][3]["branch"]
    doc["submissions"].append("#400")
    got, why = gather.decided_of(doc)
    assert why is None and [(s["id"], s["told"], s["worktree"], s["submitted"]) for s in got][:3] == [
        (356, None, None, "2026-10-28T15:47:07Z"), (357, "2026-10-28T16:21:02Z", "chore/a-wait-ends-with-the-session-that-started-it", None),
        (359, "2026-10-28T18:23:56Z", "unit/crew-keeps-no-card-wait-and-a-row-carries-its-submission-number", "2026-10-28T17:56:48Z")]
    assert got[2]["branch"] == "bolt/crew-costs-an-idle-host-nothing"


@pytest.mark.parametrize("doc, why", [
    ({"branch": "main"}, "sluice status printed no list of submissions"),
    ([], "sluice status printed no list of submissions"),
    ({"submissions": [{"schema": "sluice/submission@2", "id": 1, "branch": "main"}]},
     "sluice status printed a record of sluice/submission@2, not the sluice/submission@1 crew reads")])
def test_a_record_of_another_shape_is_said(doc, why):
    assert gather.decided_of(doc) == (None, why)


# --------------------------------------------------------------------------------------- whose line each one is

def sub(n, branch, worktree, state="queued", pull_head=None, head="a" * 40):
    return {"id": n, "branch": branch, "head": head, "state": state, "worktree": worktree, "pull_head": pull_head}


LINES = [("a", "unit"), ("bump", "chore"), ("fix/y/gap", "fix")]


def test_a_merge_into_the_bolt_is_its_lines_and_a_landing_on_main_the_bolts():
    """bolt-teams "A unit's merge under test" and "A bolt's landing queued on main"."""
    subs = [sub(41, "bolt/y", "unit/a", "testing"), sub(42, "bolt/y", "chore/bump"), sub(43, "bolt/y", "fix/y/gap", "passed"),
            sub(355, "main", "bolt/y", head="b" * 40)]
    assert plan.submission_rows(subs, "y", LINES) == (
        {"a": {"id": 41, "state": "testing"}, "bump": {"id": 42, "state": "queued"}, "fix/y/gap": {"id": 43, "state": "passed"}},
        {"id": 355, "state": "queued", "head": "b" * 40})


def test_a_flume_places_submission_is_its_lines():
    """bolt-teams "A unit's merge under test", for a started bolt's work: Flume submits a place from its own branch,
    change/<u>, chore/<c> or fix/<bolt>--<f>, as flume-0.3.6's status names it."""
    subs = [sub(41, "bolt/y", "change/a", "testing"), sub(42, "bolt/y", "chore/bump"), sub(43, "bolt/y", "fix/y--gap", "passed"),
            sub(44, "bolt/y", "change/bump")]
    assert plan.submission_rows(subs, "y", LINES)[0] == {
        "a": {"id": 41, "state": "testing"}, "bump": {"id": 42, "state": "queued"}, "fix/y/gap": {"id": 43, "state": "passed"}}


def test_a_landing_by_pull_request_is_the_bolts_it_was_opened_from():
    assert plan.submission_rows([sub(355, "main", "pull/198", pull_head="bolt/y")], "y", LINES)[1]["id"] == 355
    assert plan.submission_rows([sub(355, "main", "pull/198", pull_head="bolt/z")], "y", LINES) == ({}, None)


def test_another_bolts_submissions_and_a_hand_submission_are_no_line_of_this_one():
    subs = [sub(41, "bolt/z", "unit/a"), sub(44, "bolt/y", "unit/elsewhere"), sub(45, "bolt/y", "unit/a-b"), sub(46, "main", "bolt/z"),
            sub(47, "bolt/y", None)]
    assert plan.submission_rows(subs, "y", LINES) == ({}, None)


def test_the_newest_of_a_lines_two_is_its_own():
    subs = [sub(52, "bolt/y", "unit/a", "testing"), sub(50, "bolt/y", "unit/a", "passed")]
    assert plan.submission_rows(subs, "y", LINES)[0] == {"a": {"id": 52, "state": "testing"}}


def test_nothing_read_gives_no_line_a_submission():
    assert plan.submission_rows(None, "y", LINES) == ({}, None)


@pytest.mark.parametrize("state, said", [("testing", "#41 under test"), ("queued", "#41 queued"), ("passed", "#41 passed, to land next"),
                                         ("waiting", "#41 waiting on a submission it comes after"), ("landing", "#41 landing"),
                                         ("forming", "#41 forming"), (None, "#41")])
def test_a_standing_state_is_said_in_crews_words_and_sluices_own_for_one_crew_has_none_for(state, said):
    assert plan.standing_said({"id": 41, "state": state}) == said


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
    switchboard-kit in /kit/main, a's place at the Flume 0.3.6 status fixture named (tests/py/flume-0.3.6/<at>.json),
    the kit read as the gather reads it, with no queue of sluice's, and wldn's run record the entries logs gives."""
    from facts import FactsWrite, ran
    import runner
    w = FactsWrite(plan_text(bolts=[("y", "switchboard-kit", "swb-1")],
                             units=[("a", "switchboard-kit", "y", []), ("b", "switchboard-kit", "y", []), ("bump", "switchboard-kit", "y", [], "chore")]))
    plan.reach_places(FLEET, w, "y")
    requests = plan.Plan(w.files.get("requests.rec") or runner.REQUESTS).recs("Request")
    kit = {"ok": True, "main": [], "fixes": [], "places": {}, "bolts": {"y": {"exists": True, "head": "d" * 40, "changes": [],
                                                                         **({"carries": carries} if carries else {})}}}
    sv = {BOX: {"ok": True, "kits": {"/kit/main": kit}}}
    return plan.bolts_data(FLEET, ["wldn"], [("wldn", "WilldanGroup/crew-state", "abcdef1" + "0" * 33, w.plan)], sv, {},
                           runs={"wldn": (requests, ran({1: at}, host=BOX, label="wldn", repository="/kit/main", keeps=("WilldanGroup/switchboard-kit",)))},
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
    assert not any("submission" in x for x in b["units"] + b["fixes"]) and "landing" not in b and "submissions_error" not in b
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
