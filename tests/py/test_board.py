"""The board of a drive's flow (the crew-board spec): board.board_data on one read of the plan, proposals, signals,
kits and run record, as plan.rail_read and board.signals give it, and board.board_text, board.frame_text and
board.stamp on what that makes. That crew board reads it all and writes nothing, and the host's follower's refresh writes the
frame the board tab draws, are the board journey's (t-journey-board)."""
import datetime
import json
import os
import pathlib
import re
import sys

import pytest

from facts import FLUME, LANDED, kits_of, plan_text

import board
import crew
import ops
import plan

BOX = "chuck-herdr-alpha"
KIT = {"name": "switchboard-kit", "main": "/kit/main", "dir": "/kit"}
FLEET = {"drives": {"wldn": {"label": "wldn", "machine": "mac-studio",
                                 "blueprints": ["WilldanGroup/willdan-blueprints"], "state": "WilldanGroup/crew-state",
                                 "folder": "/m", "repos": ["WilldanGroup/breadboard-kit", "WilldanGroup/switchboard-kit"],
                                 "accounts": {r: "madswan" for r in ("design", "planner", "reviewer", "ops", "operator")}}},
         "hosts": {BOX: {"kind": "nixos", "ssh": BOX}, "mac-studio": {"kind": "darwin", "ssh": "mac-studio"}},
         "consoles": {"wldn": "/m"}}
# Where work runs, as the runner that took it reported (plan.bolt_at), for a survey of the kits it runs in: two pieces
# of work in switchboard-kit and one in breadboard-kit on the box, and one in atlas-kit on mac-studio.
WHERE = {"a": {"label": "wldn", "machine": BOX, "stream": "wldn", "kit": KIT},
         "b": {"label": "wldn", "machine": BOX, "stream": "wldn", "kit": KIT},
         "c": {"label": "wldn", "machine": BOX, "stream": "wldn", "kit": {"name": "breadboard-kit", "main": "/b/main", "dir": "/b"}},
         "d": {"label": "wldn", "machine": "mac-studio", "stream": "wldn", "kit": {"name": "atlas-kit", "main": "/a/main", "dir": "/a"}}}
NOW = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)


def ago(minutes):
    return board.iso(NOW - datetime.timedelta(minutes=minutes))


def hm(minutes):
    """A time minutes before the board was read as a head line says when a holder began (plan.time_said)."""
    t = (NOW - datetime.timedelta(minutes=minutes)).astimezone()
    return f"{t:%H:%M}" if t.date() == NOW.astimezone().date() else f"{t:%Y-%m-%d %H:%M}"


# Each started bolt's start, the run record's entry that made its branch: tenant-environments 200 minutes before the
# board was read, and board-done 30; with nothing else of theirs recorded, each has been nobody's since (plan.20), with
# no word of a stall (teams.23 retires with the-team-machinery-leaves).
STARTS = [dict(Id=f"{ago(200)}-mac-studio-1-0", At=ago(200), Host="mac-studio", Act="bolt.start", On=["bolt/tenant-environments"]),
          dict(Id=f"{ago(30)}-mac-studio-1-0", At=ago(30), Host="mac-studio", Act="bolt.start", On=["bolt/board-done"])]
TE_TIME = f"3h 20m: nobody 3h 20m; nobody since {hm(200)}"
DONE_TIME = f"30m: nobody 30m; nobody since {hm(30)}"
NO_START = "its age can't be told: the run record of the last 60 days holds no start of it"


@pytest.fixture(autouse=True)
def here(monkeypatch):
    monkeypatch.setattr(crew, "this_host", lambda: "mac-studio")


def the_plan():
    return plan.Plan(plan_text(
        bolts=[("apex-zones", "switchboard-kit", None), ("tenant-environments", "switchboard-kit", True), ("board-done", "breadboard-kit", True)],
        units=[("zone-one", "switchboard-kit", "apex-zones", []), ("a", "switchboard-kit", "tenant-environments", []),
               ("b", "switchboard-kit", "tenant-environments", []), ("done-one", "breadboard-kit", "board-done", []),
               ("zone-two", "switchboard-kit", None, [])]).replace("Unit: zone-two\nRepo: switchboard-kit\n", "Unit: zone-two\nRepo: switchboard-kit\nSource: docs/zones.md\n"))


def kits(ok=True):
    """Each host's survey: the box, where the started bolts' work runs, and mac-studio, wldn's main-level host, whose
    checkout of switchboard-kit holds its explorations (plan.main_kit)."""
    swb = {"ok": True, "main": [], "places": {}, "reports": {},
           "bolts": {"tenant-environments": {"head": "d" * 40, "head_at": ago(200), "changes": [], "worktree": "/kit/bolts/tenant-environments"}},
           "sites": {}, "routes": [], "submissions": [], "decided": []}
    brd = {"ok": True, "main": ["done-one"], "places": {}, "reports": {}, "bolts": {"board-done": {"head": "e" * 40, "head_at": ago(10), "changes": []}},
           "fixes": [], "sites": {}, "routes": [], "submissions": [], "decided": []}
    mac = {"mac-studio": {"ok": True, "kits": {"/a/main": {"ok": True, "main": [], "places": {}, "reports": {}, "bolts": {}, "fixes": []},
                                               "/m/switchboard-kit/main": {"ok": True, "main": [], "places": {}, "reports": {}, "bolts": {},
                                                                           "explorations": [{"name": "command-cost",
                                                                                             "first": "Reading: what each crew command costs."}]}}}}
    return {BOX: {"ok": True, "kits": {"/kit/main": swb, "/b/main": brd}}, **mac} if ok else {BOX: {"ok": False, "error": "ssh: timed out"}, **mac}


# Where each started bolt's work stands in Flume, as the runner on its host carries it: a at code with one of its two
# tasks ticked, b at construct, and done-one's place landed on board-done, which breadboard-kit's main holds.
PLACED = {"a": ("code", (1, 2)), "b": ("construct", None), "done-one": ("landed", None)}


def flume_status(name, place, tasks=None, repository=None):
    """A flume 0.3.6 status fixture (facts.FLUME) of the place at path place, its tasks (ticked, in all) where given, in
    the kit's folder on its host (repository) where given."""
    s = json.loads((FLUME / f"{name}.json").read_text())
    p = s["status"]["places"][0]
    p["place"] = place + p["place"][len(p["place"].split("@")[0]):]
    if repository:
        p["repository"] = repository
    p["stream"] = {"name": "wldn", "from": "intent"}  # the stream the box's runner gives wldn's work
    if tasks:
        p["tasks"] = [{"text": f"1.{i + 1}", "ticked": i < tasks[0], "group": 0} for i in range(tasks[1])]
    return json.dumps(s)


# Each kit's folder on the box, as the box's runner reports it in its repositories.rec (runner.where; Decision 1 of
# a-bolts-landing-on-main-reads-landed), and as Flume's status of a place it took names it.
KEPT = {"switchboard-kit": "/kit/main", "breadboard-kit": "/b/main"}


def flume_runs(p, placed):
    """wldn's requests and runners as the board reads them (plan.runner_facts): a launch of each unit and chore of each
    started bolt in p, in the plan's order, in its bolt's repository, as a start writes them, then each bolt's base place,
    so it is a bolt of this crew's and not one started before bolts were base places, and the box's runner
    answering each launch of placed launched with its place at {unit: (fixture, tasks)} in the kit's folder there (KEPT),
    the rest unanswered, and reporting each kit of KEPT in its folder there."""
    import runner
    requests, answers, places = [], "", ""
    for b in p.bolts() if p else []:
        for u in p.work_of(b.name()) if plan.started(b) else []:
            n, k = len(requests) + 1, plan.kind_of(u)
            requests.append(plan.Rec("Request", [("Request", str(n)), ("Act", "launch"), ("Work", f"{k}/{u.name()}"),
                                                 ("Repo", b.get("Repo")), ("Kind", "change" if k == "unit" else "chore"), ("Name", u.name()),
                                                 ("Base", f"bolt/{b.name()}"), ("Priority", "1")]))
            if u.name() in placed:
                fixture, tasks = placed[u.name()]
                where = f"/flume/places/{u.name()}"
                answers += f"\nRequest: {n}\nOutcome: launched\nPlace: {where}\nAt: {ago(100)}\n"
                places += f"\nRequest: {n}\nPlace: {where}\nAt: {ago(90)}\nStatus: {flume_status(fixture, where, tasks, KEPT[b.get('Repo')])}\n"
    for b in p.bolts() if p else []:  # each started bolt's base place, after its pieces so their numbers stand, unanswered
        if plan.started(b):
            requests.append(plan.Rec("Request", [("Request", str(len(requests) + 1)), ("Act", "launch"), ("Work", f"bolt/{b.name()}"),
                                                 ("Repo", b.get("Repo")), ("Kind", "crew/bolt"), ("Name", b.name()), ("Base", "main"),
                                                 ("Priority", "1")]))
    files = {"runner.rec": plan.Plan(runner.RUNNER + f"\nHost: {BOX}\nVersion: 0.1.0\nSince: {ago(300)}\n"),
             "answers.rec": plan.Plan(runner.ANSWERS + answers), "places.rec": plan.Plan(runner.PLACES + places),
             "repositories.rec": plan.Plan(runner.REPOSITORIES + "".join(f"\nRepository: WilldanGroup/{k}\nFolder: {f}\n" for k, f in KEPT.items()))}
    return {"wldn": (requests, {BOX: runner.host_read("wldn", BOX, "5e1f0c2a" + "0" * 32, files, {})})}


def read(sv=None, signals=None, props=(), landings=(), rows=None, cards=(), errors=None, unread=None, pl=True, entries=(), logs=(),
         roles=None, placed=None):
    """The read the board is made from; entries are the drive's run record entries the operations are read from,
    whose rail rows join the plan's, as plan.rail_record makes them, logs every entry it read, roles what it read of
    the roles the drive runs as their kinds (board.roles_read), none by default, and placed where each started
    bolt's work stands on its host's runner (flume_runs), PLACED by default."""
    p = the_plan() if pl else None
    found = [("wldn", "WilldanGroup/crew-state", "tip0" if pl else None, p)]
    sv = sv or kits()
    runs = flume_runs(p, PLACED if placed is None else placed)
    ops_rows = [dict(r, at=plan.utc(r["at"]), doc=None) for r in ops.rows(FLEET, "wldn", list(entries))]
    return dict(found=found, sv=sv, props=list(props), cards=list(cards), unread=unread or {}, errors=errors or {}, kits=kits_of(found),
                landings=list(landings), signals={"wldn": (signals or [], {})}, ops={"wldn": list(entries)},
                logs={"wldn": STARTS + (list(logs) or list(entries))}, roles={"wldn": roles} if roles else {}, runs=runs,
                rows=rows if rows is not None else (plan.rail_rows(FLEET, found, sv, list(props), {}, None, runs) if p else []) + ops_rows)


def data(**kw):
    return board.board_data(FLEET, ["wldn"], read(**kw), NOW)


def lane(text, name):
    out, on = [], False
    for l in text.splitlines():
        if l == name:
            on = True
        elif l and l[0] not in " !✓✎":
            on = False
        elif on:
            out.append(l)
    return out


S1, S2 = "a" * 40, "b" * 40
N = iter(range(1, 1000))


def entry(act, minutes, env="mac-studio", **f):
    """A run-record entry on the drive's main level's host, minutes before the board was read."""
    on = [f"bolt/{f.pop('bolt')}"] if act == "bolt.land" else [f"env/{env}"]
    return dict(Id=f"{ago(minutes)}-mac-studio-1-{next(N)}", At=ago(minutes), Host="mac-studio", Act=act, On=on, From=[], Commit=[], **f)


# A deploy of atlas-kit to mac-studio approved and done, a newer one offered, an operation handed to main-level ops and
# one waiting on the user.
OPS = [entry("bolt.land", 95, bolt="atlas-maps", Repo="atlas-kit", Head=S1), entry("ops.offer", 90, Head=S1, Base="none"),
       entry("ops.approve", 70, Head=S1, By="wldn-ops"), entry("ops.deploy", 60, Head=S1, Base="none", Phase="start"),
       entry("ops.deploy", 50, Head=S1, Phase="end", Outcome="done"), entry("bolt.land", 45, bolt="atlas-zones", Repo="atlas-kit", Head=S2),
       entry("ops.offer", 40, Head=S2, Base=S1),
       entry("ops.step", 30, Head=S1, Key="restart-roles/1", State="handed", Doer="main-ops", Agent="wldn-ops"),
       entry("ops.step", 20, Key="rotate-key", State="waiting", Doer="user", Text="Rotate the key.")]
DEPLOY_CARD = dict(label="wldn", card="req_9", key="deploy/mac-studio", by="wldn-ops", host="mac-studio", at=NOW)
# The deploy's card, posted in wldn-ops's name when the offer was made, refused by Pending You (rail-cards "A row's card
# that Pending You refused is owed until it posts").
REFUSED_POST = entry("card.post", 39, Key="deploy/mac-studio", By="wldn-ops",
                     Refused="Pending You refused post_request: This is wldn-planner’s card; leave it.")


SIGS = [{"signal": "2026-10-01-planning/01-zones", "home": "blueprints", "captured_by": "wldn-planner", "at": "2026-10-01", "kind": "ask",
         "first": "Every apex should be a zone of its own."},
        {"signal": "2026-10-01-planning/02-tenants", "home": "blueprints", "captured_by": "wldn-planner", "at": "2026-10-01", "kind": "constraint",
         "first": "Tenants never share an environment."},
        {"signal": "2026-10-12-chuck/01-checked", "home": "branch", "captured_by": "chuck@mac-studio", "at": None, "kind": "ask",
         "first": "Plans should be checked before they run."}]


class TestText:
    def test_with_nothing_in_flight_each_lane_and_attention_say_none_plain_into_a_pipe(self):
        sv = {BOX: {"ok": True, "kits": {}}, "mac-studio": {"ok": True, "kits": {}}}
        empty = board.board_data(FLEET, ["wldn"], read(sv=sv, pl=False), NOW)
        out = board.board_text(empty)
        assert out.splitlines()[0].startswith("wldn board, as of ") and out.splitlines()[0].endswith(f"read from {BOX}, mac-studio")
        assert [l for l in out.splitlines()[1:] if l and l[0].isalpha()] == ["Inception", "Bolt plan", "Construction", "Operation", "attention"]
        assert "\033" not in out

    def test_inception_lists_unmoved_signals_by_who_captured_them_and_each_exploration(self):
        inc = lane(board.board_text(data(signals=SIGS)), "Inception")
        assert "  signals captured by wldn-planner  2 not moved, the oldest captured 2026-10-01" in inc
        assert "  signals captured by chuck@mac-studio  1 not moved" in inc
        assert "    ask  Every apex should be a zone of its own.  2026-10-01-planning/01-zones" in inc
        assert "  exploration  switchboard-kit command-cost  Reading: what each crew command costs." in inc

    def test_bolt_plan_lists_each_planned_bolt_with_its_units_and_the_queue_with_its_sources(self):
        bp = lane(board.board_text(data()), "Bolt plan")
        assert bp == ["  switchboard-kit apex-zones  Goal of apex-zones.", "    zone-one  ready", "  switchboard-kit zone-two  queued  docs/zones.md"]

    def test_construction_shows_a_started_bolt_as_a_ledger(self):
        """Each unit at its stage as its host's runner carries its place, with no server (a started bolt's work is
        Flume's)."""
        con = lane(board.board_text(data()), "Construction")
        assert con[:3] == [f"  switchboard-kit tenant-environments  on chuck-herdr-alpha  in Flume stream wldn  {TE_TIME}",
                           "    a  code 1/2", "    b  construct"]
        assert f"! breadboard-kit board-done  on chuck-herdr-alpha  in Flume stream wldn  landed  {DONE_TIME}" in con

    def test_a_started_bolt_every_unit_of_which_landed_is_named_for_attention(self):
        att = lane(board.board_text(data()), "attention")
        assert att == ["! bolt board-done: every unit has landed on main, and the bolt is still in the plan"]

    def test_a_rail_row_is_a_marker_on_its_object_with_its_card(self):
        props = [{"label": "wldn", "proposal": 1, "by": "chuck@mac-studio", "opened": "2026-10-12", "case": "The console gets a bolt.",
                  "changes": [{"do": 'bolt new console-two "x" --repo switchboard-kit', "bolts": ["console-two"]}]}]
        card = dict(label="wldn", card="req_1", key="proposal/1", by="wldn-planner", host="mac-studio", at=NOW)
        bp = lane(board.board_text(data(props=props, cards=[card])), "Bolt plan")
        assert bp[0] == "✓ proposal 1 by chuck@mac-studio  The console gets a bolt.  card open, asked by wldn-planner"

    def test_a_rewritten_proposals_marker_is_its_chains_card(self):
        props = [{"label": "wldn", "proposal": 2, "first": 1, "by": "wldn-planner", "opened": "2026-10-12", "case": "The console, again.",
                  "changes": [{"do": 'bolt new console-two "x" --repo switchboard-kit', "bolts": ["console-two"]}]}]
        card = dict(label="wldn", card="req_1", key="proposal/1", by="wldn-planner", host="mac-studio", at=NOW)
        bp = lane(board.board_text(data(props=props, cards=[card])), "Bolt plan")
        assert bp[0] == "✓ proposal 2 by wldn-planner  The console, again.  card open, asked by wldn-planner"

    def test_operation_lists_a_bolt_landed_this_week_and_not_one_landed_eight_days_ago(self):
        landings = [dict(label="wldn", bolt="atlas-maps", units=["map-one"], at=NOW - datetime.timedelta(hours=1), by="chuck@mac-studio", host="mac-studio"),
                    dict(label="wldn", bolt="old-maps", units=["old"], at=NOW - datetime.timedelta(days=8), by="wldn-ops", host="mac-studio")]
        op = lane(board.board_text(data(landings=landings)), "Operation")
        assert len(op) == 1 and op[0].startswith("  atlas-maps  landed ") and op[0].endswith(" by chuck@mac-studio  map-one")

    def test_operation_shows_each_environments_deploys_and_the_operations_waiting_with_their_markers(self):
        op = lane(board.board_text(data(entries=OPS, cards=[DEPLOY_CARD])), "Operation")
        assert op == [f"✓ mac-studio  deploy {S2[:7]} from {S1[:7]}  waits on the user's word  carrying atlas-zones  card open, asked by wldn-ops",
                      f"  mac-studio  deploy {S1[:7]} from nothing deployed  done {board.local(ago(50))}  approved by wldn-ops  carrying atlas-maps",
                      "  mac-studio  restart-roles/1  handed to wldn-ops",
                      "✓ mac-studio  rotate-key  waits on the user  Rotate the key.  no card open"]
        env, = data(entries=OPS)["drives"][0]["environments"]
        assert (sorted(env), [d["row"] for d in env["deploys"]], [w["row"] for w in env["waiting"]]) == (
            ["deploys", "env", "waiting"], ["deploy/mac-studio", None], [None, "op/mac-studio/2"])

    def test_a_deploy_whose_only_post_was_refused_owes_its_card_and_a_row_with_no_post_has_none_open(self):
        """crew-board "A row whose card post was refused": the row's last post under its key, refused, with no card
        open; the rotate-key step, never posted, has none open and says no more."""
        logs = OPS + [REFUSED_POST]
        op = lane(board.board_text(data(entries=OPS, logs=logs)), "Operation")
        assert op[0] == f"✓ mac-studio  deploy {S2[:7]} from {S1[:7]}  waits on the user's word  carrying atlas-zones  no card open, its post refused"
        assert op[-1] == "✓ mac-studio  rotate-key  waits on the user  Rotate the key.  no card open"
        env, = data(entries=OPS, logs=logs)["drives"][0]["environments"]
        assert env["deploys"][0]["markers"][0]["refused"] == REFUSED_POST["Refused"]
        assert env["waiting"][1]["markers"][0]["refused"] is None

    def test_a_card_posted_after_a_refused_post_is_open_and_owes_nothing(self):
        d = data(entries=OPS, logs=OPS + [REFUSED_POST], cards=[DEPLOY_CARD])
        assert d["drives"][0]["environments"][0]["deploys"][0]["markers"][0]["refused"] is None
        assert lane(board.board_text(d), "Operation")[0].endswith("card open, asked by wldn-ops")

    def test_a_deploy_that_failed_says_at_which_step_and_one_whose_commit_no_landing_holds_says_so(self):
        es = [entry("ops.deploy", 30, Head=S2, Base=S1, Phase="start"), entry("ops.deploy", 20, Head=S2, Phase="step", Step="machine", Outcome="failed"),
              entry("ops.deploy", 10, Head=S2, Phase="end", Outcome="failed")]
        assert lane(board.board_text(data(entries=es)), "Operation") == [
            f"  mac-studio  deploy {S2[:7]} from {S1[:7]}  failed {board.local(ago(10))} at the machine  carrying what can't be read: {S2[:7]} is no landing's commit in the record"]

    def test_a_host_that_does_not_answer_is_named_and_its_ledgers_bolts_are_unknown(self):
        """Its bolts' states can't be told, and their times are read from the run record alone; each unit's stage is the
        runner's, read from the branch, but a place merged on its bolt can't be told landed with main unread."""
        out = board.board_text(data(sv=kits(ok=False)))
        assert f"! {BOX} did not answer (its kits: ssh: timed out)" in lane(out, "attention")
        con = lane(out, "Construction")
        assert (f"  switchboard-kit tenant-environments  on {BOX}  in Flume stream wldn  unknown  {TE_TIME}") in con and "    a  code 1/2" in con \
            and "    done-one  merged" in con
        assert out.splitlines()[0].endswith("read from mac-studio")

    def test_an_operator_host_with_no_team_is_never_named_for_its_run_record(self):
        """crew-board, "An operator host asleep": the run record is read from the branch, so a host that runs no team
        is asked for nothing and named for nothing, and the landings and cards read from wldn/main are drawn whole."""
        fleet = dict(FLEET, hosts=dict(FLEET["hosts"], **{"macbook-pro": {"kind": "darwin", "ssh": "macbook-pro"}}))
        sv = dict(kits(), **{"macbook-pro": {"ok": False, "error": "ssh: connect to host macbook-pro port 22: Operation timed out"}})
        landed = [dict(label="wldn", bolt="tenant-environments", units=["a", "b"], at=plan.utc(ago(5)), by="wldn-ops", host="macbook-pro")]
        d = board.board_data(fleet, ["wldn"], read(sv=sv, unread={"wldn": {}}, landings=landed), NOW)
        p = d["drives"][0]
        assert "macbook-pro" not in p["hosts"] and "macbook-pro" not in json.dumps(p["attention"])
        assert [a for a in p["attention"] if a["what"] in ("host", "plan")] == []

    def test_a_branch_whose_run_record_cannot_be_read_is_named_as_the_plans(self):
        d = data(unread={"wldn": {"wldn/main": "could not fetch wldn/main of WilldanGroup/crew-state over https: timed out"}})
        assert [a for a in d["drives"][0]["attention"] if a["what"] in ("host", "plan")] == [
            {"what": "plan", "name": "wldn/main", "why": "its run record: could not fetch wldn/main of WilldanGroup/crew-state over https: timed out"}]
        assert ("! the plan, wldn/main: its run record: could not fetch wldn/main of WilldanGroup/crew-state over https: timed out"
                in lane(board.board_text(d), "attention"))
        assert sorted(d["drives"][0]["hosts"]) == [BOX, "mac-studio"]

    def test_a_plan_that_cannot_be_read_is_named_for_attention(self):
        d = board.board_data(FLEET, ["wldn"], read(pl=False, errors={"wldn/main of WilldanGroup/crew-state": "plan.rec fails recfix --check"}), NOW)
        assert "! the plan, wldn/main of WilldanGroup/crew-state: plan.rec fails recfix --check" in lane(board.board_text(d), "attention")


class TestData:
    def test_the_json_lists_no_teams_and_no_object_says_whose_team_it_is(self):
        """crew-board, the removed "The board's JSON lists each drive's teams" and "Each object in the board's JSON
        says whose it is": an object's drive and kit say whose it is (Decision 11 of the-team-machinery-leaves)."""
        landings = [dict(label="wldn", bolt="atlas-maps", units=["map-one"], at=NOW - datetime.timedelta(hours=1), by="wldn-ops", host="mac-studio")]
        props = [{"label": "wldn", "proposal": 2, "by": "chuck@mac-studio", "opened": "2026-10-12", "case": "Tenants get d.",
                  "changes": [{"do": 'unit add d "Unit d." --bolt tenant-environments', "bolts": ["tenant-environments"]}]}]
        p = data(signals=SIGS, props=props, entries=OPS, landings=landings)["drives"][0]

        def keys(x):
            """Every key of x's objects, a bolt's time left out, whose holders keep their names (plan.20)."""
            if isinstance(x, dict):
                return set(x) | {k for n, v in x.items() if n != "time" for k in keys(v)}
            return {k for v in x for k in keys(v)} if isinstance(x, list) else set()
        assert not {"teams", "team", "slot"} & keys(p)
        assert all(p[k] for k in ("construction", "operation", "environments")) and p["bolt_plan"]["proposals"] and p["inception"]["explorations"]

    def test_the_hosts_are_named_with_whether_they_answered(self):
        assert data()["drives"][0]["hosts"] == {BOX: True, "mac-studio": True}

    @pytest.mark.parametrize("at, held", [("2026-10-01", "2026-10-01"), ("2026-10-01T10:00:00", "2026-10-01T10:00:00Z"),
                                          ("2026-10-01T12:00:00+02:00", "2026-10-01T10:00:00Z"), ("not a time", None)])
    def test_a_captures_time_is_held_in_utc_and_a_date_as_it_is(self, at, held):
        assert board.stamp(at) == held


class TestFrame:
    def test_with_no_frame_the_board_tab_says_the_hosts_follower_writes_it(self):
        assert board.frame_text("wldn", None, None, False, NOW) == (
            "No board for wldn yet: the host's follower writes it each time it refreshes, swancloud's job or the console's rail tab, "
            "which crew console up wldn opens while no job runs.")

    def test_a_frame_read_five_minutes_ago_is_headed_with_its_age(self):
        d = data()
        d["read_at"] = board.iso(NOW - datetime.timedelta(minutes=5))
        assert "(5m ago: the host's follower has not refreshed it since)" in board.frame_text("wldn", d, None, False, NOW).splitlines()[0]
        d["read_at"] = board.iso(NOW)
        assert " ago" not in board.frame_text("wldn", d, None, False, NOW).splitlines()[0]


class TestFollower:
    """The host's one follower (the crew-board spec, A host has one follower): an OS lock on a file beside the frames,
    held for the follower's life and saying who holds it. Two open()s are two open file descriptions, so the lock
    conflicts between them in one process as between two processes."""

    def test_a_held_lock_refuses_a_second_try_and_says_the_tab_holds_it(self, tmp_path, monkeypatch):
        monkeypatch.setattr(board, "FRAMES", tmp_path)
        held = board.lock_follower("tab", "wldn", wait=False)
        assert held
        assert board.lock_follower("job", wait=False) is None and board.lock_follower("tab", "madswan", wait=False) is None
        assert board.lock_path().read_text().startswith("tab wldn ")
        assert board.follower_here() == "tab"
        held.close()
        assert board.follower_here() == "none"

    def test_the_job_holding_it_reads_as_the_job(self, tmp_path, monkeypatch):
        monkeypatch.setattr(board, "FRAMES", tmp_path)
        held = board.lock_follower("job", wait=False)
        assert board.lock_path().read_text().split()[0] == "job" and board.follower_here() == "job"
        held.close()

    def test_a_released_lock_is_free_and_taken_again_with_its_holder_written_anew(self, tmp_path, monkeypatch):
        monkeypatch.setattr(board, "FRAMES", tmp_path)
        board.lock_follower("job", wait=False).close()
        held = board.lock_follower("tab", "wldn", wait=False)
        assert held and len(board.lock_path().read_text().splitlines()) == 1 and board.follower_here() == "tab"
        held.close()

    @pytest.mark.parametrize("line, free, who", [("", False, "unknown"), (None, False, "unknown"), ("job 12 2026-10-28T10:00:00Z", False, "job"),
                                                 ("tab wldn 12 2026-10-28T10:00:00Z", False, "tab"), ("tab 12 2026-10-28T10:00:00Z", False, "unknown"),
                                                 ("someone else", False, "unknown"), ("job 12 2026-10-28T10:00:00Z", True, "none"), ("", True, "none")])
    def test_who_follows_is_read_from_the_lock_and_an_unreadable_holder_is_unknown(self, line, free, who):
        assert board.follower_of(line, free) == who

    def test_it_follows_the_drives_its_teams_files_consoles_name(self, monkeypatch):
        """operator-agent, The drives a host follows: deneb's `consoles` names afterthought, agentplot, madswan and wldn,
        and its teams file lists swancloud too, which it does not follow; the file names this host's consoles alone, so
        another host follows none of them, and a file that names none follows none (record 0064)."""
        monkeypatch.setattr(crew, "this_host", lambda: "deneb")
        fleet = {"drives": {"afterthought": {}, "agentplot": {}, "swancloud": {}, "madswan": {}, "wldn": {}},
                 "consoles": {"wldn": "/w", "madswan": "/a", "agentplot": "/p", "afterthought": "/a"}}
        assert board.labels_here(fleet, "deneb") == ["afterthought", "agentplot", "madswan", "wldn"]
        assert board.labels_here(fleet, "mac-studio") == [] and board.labels_here(fleet, BOX) == []
        assert board.labels_here(dict(fleet, consoles={}), "deneb") == []

    @pytest.mark.parametrize("m, kept, crew_read, how", [
        ({"crew": True, "read": True, "any": True}, False, True, "read"), ({"crew": True, "read": True, "any": True}, True, True, "update"),
        ({"crew": True, "read": True, "any": True}, True, False, "read"), ({"crew": False, "read": True, "any": True}, True, True, "read"),
        ({"crew": False, "read": False, "any": True}, True, True, "sweep"), ({"crew": False, "read": False, "any": False}, True, True, "render")])
    def test_a_refresh_reads_once_with_none_kept_hands_out_restarts_once_crew_moved_and_renders_when_nothing_moved(self, m, kept, crew_read, how):
        """A tip or a kit moved reads; only a readings folder or the cards moved sweeps; nothing moved renders."""
        assert board.refresh_plan(m, kept, crew_read) == how

    NOTHING = {"crew": False, "state": set(), "blueprints": set(), "kits": set(), "readings": set(), "cards": False, "read": False, "any": False}
    READINGS = {"mac-studio": ["wldn", "swancloud"], BOX: ["wldn"]}

    def test_after_only_a_hosts_readings_moved_its_card_sessions_alone_are_swept(self):
        """The card-sessions spec, A reading sent on one host."""
        assert board.sweeps_after(dict(self.NOTHING, readings={BOX}, any=True), self.READINGS, []) == {"cards": False, "sessions": {"wldn": {BOX}}}
        assert board.sweeps_after(dict(self.NOTHING, readings={"mac-studio"}, any=True), self.READINGS, []) == (
            {"cards": False, "sessions": {"wldn": {"mac-studio"}, "swancloud": {"mac-studio"}}})

    def test_after_only_the_cards_moved_the_card_sweep_alone_runs(self):
        assert board.sweeps_after(dict(self.NOTHING, cards=True, any=True), self.READINGS, []) == {"cards": True, "sessions": {}}

    def test_with_nothing_moved_only_the_hosts_the_last_could_not_check_are_swept_beside_what_moved(self):
        unchecked = [{"label": "wldn", "host": "mac-studio", "why": "did not answer (exit 255)"}]
        assert board.sweeps_after(self.NOTHING, self.READINGS, unchecked) == {"cards": False, "sessions": {"wldn": {"mac-studio"}}}
        assert board.sweeps_after(dict(self.NOTHING, readings={BOX}, any=True), self.READINGS, unchecked) == (
            {"cards": False, "sessions": {"wldn": {"mac-studio", BOX}}})

    @pytest.mark.parametrize("now, tick_at, seen, looked, how", [
        (100.0, 100.0, "a", "a", "tick"), (100.0, 0.0, "a", "b", "tick"), (100.0, 160.0, "a", "b", "refresh"), (100.0, 160.0, "a", "a", None)])
    def test_a_look_ticks_when_its_clock_is_due_refreshes_when_a_cache_moved_and_else_reads_nothing(self, now, tick_at, seen, looked, how):
        assert board.wake(now, tick_at, seen, looked) == how

    def test_the_clock_is_a_minute_a_frame_is_stale_after_three_and_sigusr1_makes_the_next_tick_now(self):
        assert board.PERIOD == 60 and board.STALE == 3 * board.PERIOD
        f = board.Follower(None)
        f.tick_at = 1e12
        assert board.wake(100.0, f.tick_at, "a", "a") is None
        f.tick_now()
        assert board.wake(100.0, f.tick_at, "a", "a") == "tick"


class TestInstalledCrew:
    """The follower watches the crew the host has installed (host-holds-and-updates "An install moves while an agent sits
    idle"): on a build its stamp is the installed command's real path, which an install moves, so the next refresh is an
    update, handed out and started again through the installed crew; on a checkout its commit, as before."""

    @pytest.fixture
    def build(self, tmp_path, monkeypatch):
        """crew run from a build in the store, no git, and a profile folder on its path whose crew links to a build."""
        store = tmp_path / "store"
        home = store / "abc-crew"
        (home / "bin").mkdir(parents=True)
        monkeypatch.setattr(crew, "HOME", home)
        monkeypatch.setattr(crew, "STORE", f"{store}/")
        profile = tmp_path / "profile/bin"
        profile.mkdir(parents=True)
        monkeypatch.setenv("PATH", str(profile))
        return store, home, profile

    def built(self, store, name):
        """A build's bin/crew in the store, made where it is missing."""
        (store / name / "bin").mkdir(parents=True, exist_ok=True)
        (store / name / "bin/crew").write_text("#!/bin/sh\n")
        (store / name / "bin/crew").chmod(0o755)
        return store / name / "bin/crew"

    def test_on_a_build_the_stamp_is_the_installed_commands_real_path_and_an_install_moves_it(self, build):
        store, home, profile = build
        (profile / "crew").symlink_to(self.built(store, "abc-crew"))
        was = board.crew_stamp()
        assert was == os.path.realpath(home / "bin/crew")
        (profile / "crew").unlink()
        (profile / "crew").symlink_to(self.built(store, "def-crew"))
        assert board.crew_stamp() == os.path.realpath(store / "def-crew/bin/crew") != was
        assert board.moved_at()[0] == board.crew_stamp()

    def test_on_a_checkout_the_stamp_is_its_commit(self, tmp_path, monkeypatch):
        (tmp_path / ".git").write_text("gitdir: /elsewhere\n")
        monkeypatch.setattr(crew, "HOME", tmp_path)
        monkeypatch.setattr(crew, "head_here", lambda root=None: "c" * 40)
        assert board.crew_stamp() == "c" * 40

    def test_with_no_installed_crew_the_stamp_is_unread_and_a_refresh_reads_and_hands_out_nothing(self, build):
        assert board.crew_stamp() is None
        kept = {"crew": ("c" * 40, b"{teams}"), "state": {}, "blueprints": {}, "kits": {}}
        now = dict(kept, crew=(board.crew_stamp(), b"{teams}"))
        m = board.moved(kept, now)
        assert m["crew"] and board.refresh_plan(m, True, None not in now["crew"]) == "read"

    def test_the_notice_runs_the_installed_crew(self, build):
        store, home, profile = build
        (profile / "crew").symlink_to(self.built(store, "def-crew"))
        assert board.notice_argv() == ["pendingyou", "watch", "--", "bash", str(profile / "crew"), "_answered"]

    def test_an_install_hands_out_the_restarts_and_starts_the_follower_again_through_the_installed_crew(self, build, tmp_path, monkeypatch):
        store, home, profile = build
        (profile / "crew").symlink_to(self.built(store, "def-crew"))
        ran, started = [], []
        monkeypatch.setattr(board.subprocess, "run", lambda argv, **kw: ran.append(argv) or
                            board.subprocess.CompletedProcess(argv, 0, "wldn-ops is due", ""))
        monkeypatch.setattr(board.os, "execvpe", lambda file, argv, env: started.append((file, argv, env["CREW_FOLLOWER_LOCK"])))
        monkeypatch.setattr(board.os, "execve", lambda file, argv, env: started.append((file, argv, env["CREW_FOLLOWER_LOCK"])))
        monkeypatch.setattr(board.sys, "argv", ["board.py", "_follow"])
        lock = open(tmp_path / "lock", "w")
        f = board.Follower(lock)
        f.labels = ["wldn"]
        f.again({})
        assert ran == [["bash", str(profile / "crew"), "_update", "--label", "wldn"]]
        assert started == [("bash", ["bash", str(profile / "crew"), "_follow"], str(lock.fileno()))]

    def test_on_a_checkout_the_follower_starts_again_as_its_own_board(self, tmp_path, monkeypatch):
        (tmp_path / ".git").write_text("gitdir: /elsewhere\n")
        monkeypatch.setattr(crew, "HOME", tmp_path)
        ran, started = [], []
        monkeypatch.setattr(board.subprocess, "run", lambda argv, **kw: ran.append(argv) or
                            board.subprocess.CompletedProcess(argv, 0, "", ""))
        monkeypatch.setattr(board.os, "execvpe", lambda file, argv, env: started.append(argv))
        monkeypatch.setattr(board.os, "execve", lambda file, argv, env: started.append(argv))
        monkeypatch.setattr(board.sys, "argv", ["board.py", "_follow"])
        f = board.Follower(open(tmp_path / "lock", "w"))
        f.labels = ["wldn"]
        f.again({})
        assert ran == [["bash", str(tmp_path / "plugin/bin/crew"), "_update", "--label", "wldn"]]
        assert started == [[sys.executable, str(board.LIB / "board.py"), "_follow"]]


class TestRefresh:
    """The host's follower's refresh (the crew-board spec, The rail and the board come from one read, A refresh after
    nothing moved reads nothing, A refresh after a change reads only what moved): one read for every drive with an
    operator session on the host, kept, and the frames written from it; each step around it stands in here, the read,
    the views and the stamps, so what is asked is what the case shows."""

    FLEET = {"drives": {"wldn": {"label": "wldn", "state": "o/state", "blueprints": ["o/bp"],
                                     "machine": "mac-studio", "runs": {r: "standing" for r in crew.KIND_ROLES}},
                            "swancloud": {"label": "swancloud", "state": "o/state", "blueprints": ["o/bp"],
                                          "machine": "mac-studio", "runs": {r: "standing" for r in crew.KIND_ROLES}}},
             "hosts": {"mac-studio": {"ssh": "mac-studio", "kind": "darwin"}}, "consoles": {"wldn": "/w", "swancloud": "/s"}}

    @pytest.fixture
    def follower(self, tmp_path, monkeypatch):
        monkeypatch.setattr(board, "FRAMES", tmp_path)
        monkeypatch.setattr(crew, "SESSIONS", tmp_path / "sessions")
        monkeypatch.setattr(crew, "HOLD", tmp_path / "hold")
        self.looks = {"crew": ("c" * 40, b"{teams}"), "state": {"wldn": "a" * 40, "swancloud": ""}, "blueprints": {"wldn": "b" * 40, "swancloud": "b" * 40}}
        self.stamps, self.reads, self.swept, self.again, self.unchecked = {(BOX, "/kit/main"): "s1"}, [], [], [], []
        self.readings, self.asked = {BOX: "r1", "mac-studio": "r2"}, []
        monkeypatch.setattr(board, "look", lambda fleet, labels: {k: dict(v) if isinstance(v, dict) else v for k, v in self.looks.items()})

        self.routes, self.routes_asked = {}, []

        def stamps_now(fleet, kits, readings, routes=(), hosts=None):
            asked = {h: ls for h, ls in readings.items() if hosts is None or h in hosts}
            self.asked.append(asked)
            self.routes_asked.append(sorted(routes))
            return {"kits": {k: v for k, v in self.stamps.items() if k[1] in kits.get(k[0], {}) and (hosts is None or k[0] in hosts)},
                    "readings": {h: self.readings[h] for h in asked},
                    "routes": {h: r for h, r in self.routes.items() if h in kits and h in routes}}
        monkeypatch.setattr(board, "stamps_now", stamps_now)
        monkeypatch.setattr(crew, "this_host", lambda: "mac-studio")

        self.req, self.found = {"main": "/kit/main"}, []

        def flow_read(fleet, labels, sweep=False):
            kept = plan.READ.follower
            self.reads.append((list(labels), sweep, plan.READ.tip("o/state", "wldn/main"), plan.READ.tip("o/state", "swancloud/main")))
            served = kept.served(BOX, "/kit/main", self.req)
            kept.use(BOX, "/kit/main", self.req, served or {"ok": True, "stamp": self.stamps[(BOX, "/kit/main")], "routes": []})
            if kept.cards is None:  # the tick's ask, which rail_read makes when the follower kept no read to ask from
                kept.cards = ({}, None)
            print("crew: a word the read said", file=sys.stderr)
            return {"found": list(self.found), "errors": {"wldn/main of o/state": "a plan it could not read"}, "signals": {}, "unchecked": list(self.unchecked),
                    "sv": {}, "rows": [], "cards": [], "unread": {}, "batched": {}, "served": served is not None, "kits": kits_of(self.found)}
        monkeypatch.setattr(board, "flow_read", flow_read)
        monkeypatch.setattr(board, "board_data", lambda fleet, labels, read, now: {"read_at": board.iso(now), "from": "mac-studio",
                                                                                   "drives": [{"label": labels[0]}], "unread": {}})
        monkeypatch.setattr(plan, "rail_text", lambda fleet, labels, read, now: f"rail of {labels[0]}" + (", served" if read["served"] else ""))
        monkeypatch.setattr(board, "here_read", lambda fleet, l: {"host": "mac-studio", "version": None, "held": None, "agents": {}})
        monkeypatch.setattr(board, "agent_views", lambda data: {"read_at": data["read_at"], "views": {}})
        monkeypatch.setattr(plan, "sweep_sessions", lambda fleet, found, sv, rows, cards, unread, batched, only=None, runs=None:
                            self.swept.append(only) or ([], []))
        # wldn's runner answers on the box, its branch in crew's cache (plan.runner_tips, read with no fetch), at a tip a
        # case moves when the box's runner reports a move of the places it runs
        self.runner = {BOX: "r" * 40}
        monkeypatch.setattr(plan, "runner_tips", lambda repo, label, fetch=True: dict(self.runner) if label == "wldn" else {})
        test = self

        class Here(board.Follower):
            def fleet(self):
                self.fleet_, self.labels = test.FLEET, board.labels_here(test.FLEET, "mac-studio")
                return test.FLEET

            def again(self, fleet):
                test.again.append(list(self.labels))
        return Here(None)

    def test_the_follower_runs_pending_yous_notice_while_a_role_here_runs_as_its_kind(self, tmp_path, monkeypatch):
        """role-runs "The follower hears Pending You's notice while a role here runs as its kind": started at a tick
        while a drive whose main level is here names a role on demand in its `runs`, once, started again when it ended, and
        ended once none does (design Decision 5 of roles-run-as-flume-kinds)."""
        started = []

        class Proc:
            def __init__(self, argv, **kw):
                self.argv, self.code, self.ended = argv, None, False
                started.append(self)

            def poll(self):
                return self.code

            def terminate(self):
                self.ended, self.code = True, -15

            def wait(self, timeout=None):
                return self.code
        monkeypatch.setattr(board.subprocess, "Popen", Proc)
        monkeypatch.setattr(board, "HEARD", tmp_path / "heard.log")
        monkeypatch.setattr(crew, "this_host", lambda: "deneb")
        stands = {r: "standing" for r in crew.KIND_ROLES}
        runs = {"drives": {"madswan": {"label": "madswan", "machine": "deneb", "runs": dict(stands, planner="on-demand")}}}
        f = board.Follower(None)
        f.hear(runs)
        f.hear(runs)
        assert [x.argv for x in started] == [board.notice_argv()]
        started[0].code = 1
        f.hear(runs)
        assert len(started) == 2, "a notice that ended was not started again"
        f.hear({"drives": {"madswan": dict(runs["drives"]["madswan"], runs=stands)}})
        assert started[1].ended and f.notice is None
        f.hear({"drives": {"madswan": dict(runs["drives"]["madswan"], machine="mac-studio")}})
        assert len(started) == 2, "a notice was run for a role whose main level is on another host"

    def frame(self, label, kind="rail"):
        return json.loads((board.FRAMES / f"{label}{'.' + kind if kind != 'board' else ''}.json").read_text())

    def test_one_read_writes_every_drives_frames_with_what_it_said(self, follower):
        follower.refresh()
        assert self.reads == [(["wldn", "swancloud"], True, "a" * 40, "")], "the read was not handed the tips the caches hold"
        assert self.frame("wldn")["text"] == "rail of wldn\ncrew: a word the read said\na plan it could not read"
        assert self.frame("swancloud")["text"] == "rail of swancloud\ncrew: a word the read said"
        assert self.frame("swancloud", "board")["drives"] == [{"label": "swancloud"}] and self.frame("wldn", "agents")["views"] == {}

    def test_a_refresh_with_nothing_moved_reads_nothing_sweeps_nothing_and_writes_the_frames_again(self, follower):
        follower.refresh()
        was = self.frame("wldn")["read_at"]
        follower.refresh()
        assert len(self.reads) == 1 and self.swept == []
        assert self.frame("wldn")["text"] == "rail of wldn\na plan it could not read" and self.frame("wldn")["read_at"] >= was

    def test_a_refresh_after_a_kit_moved_reads_again_with_the_rest_served(self, follower):
        follower.refresh()
        self.stamps[(BOX, "/kit/main")] = "s2"
        self.runner[BOX] = "q" * 40  # the box's runner reports a move of the place it runs
        follower.refresh()
        assert len(self.reads) == 2 and self.frame("wldn")["text"].startswith("rail of wldn\n")
        follower.refresh()
        assert len(self.reads) == 2, "a kit read at its new stamp was taken as moved again"
        self.looks["state"] = {"wldn": "d" * 40, "swancloud": ""}
        follower.refresh()
        assert len(self.reads) == 3 and self.frame("wldn")["text"].startswith("rail of wldn, served"), "an unmoved kit was not served"

    def test_its_check_stamps_the_readings_of_each_drives_hosts_with_its_kits(self, follower):
        """The card-sessions spec, A reading sent on one host: every host where a drive's card sessions are swept,
        its main machine and its runners', has its readings stamped at its first refresh; then this host's at each, in
        this process, and another's when something there could have moved (hosts_due)."""
        follower.refresh()
        follower.refresh()
        assert self.asked == [{"mac-studio": ["wldn", "swancloud"], BOX: ["wldn"]}, {"mac-studio": ["wldn", "swancloud"]}]

    def test_a_refresh_after_crew_moved_hands_out_the_restarts_and_starts_again(self, follower):
        follower.refresh()
        self.looks["crew"] = ("e" * 40, b"{teams}")
        follower.refresh()
        assert self.again == [["wldn", "swancloud"]]

    def test_the_clock_asks_pending_you_after_the_kept_reads_cards_when_they_could_have_moved_and_never_between(self, follower, monkeypatch):
        """The crew-board spec, The follower asks Pending You about cards when they could have moved: one bridge at a
        tick for the cards the kept read's sweep would act on that it has not answered, none on a tick when it names
        none or has answered them all, again ten minutes on, and none at a refresh between ticks."""
        bridges, test = [], self
        self.to_ask = []

        class Py:
            def __enter__(self):
                return self

            def __exit__(self, *exc):
                pass

            def answer(self, tool, args):
                return {"status": "pending"}, None

        class Acts:
            def __init__(self, fleet):
                pass

            def bridge(self, name, later, held=None):
                bridges.append(name)
                return Py()
        monkeypatch.setattr(plan, "SweepActs", Acts)
        monkeypatch.setattr(plan, "cards_asked", lambda fleet, read, here, now: list(test.to_ask))
        monkeypatch.setattr(plan, "sweep_cards", lambda fleet, read, acts=None, answers=None, listed=None: {"done": [], "unswept": []})
        monkeypatch.setattr(type(follower), "fetch", lambda self, fleet: None)
        follower.tick()
        follower.tick()
        assert bridges == [] and follower.kept.cards == ({}, None) and len(self.reads) == 1
        self.to_ask = ["req_p4"]
        follower.tick()
        assert bridges == ["crew"] and follower.kept.cards == ({"req_p4": ({"status": "pending"}, None)}, None)
        follower.refresh()
        follower.refresh()
        assert bridges == ["crew"], "a refresh between ticks asked Pending You"
        follower.tick()
        assert bridges == ["crew"], "a tick asked Pending You after a card it had answered, with nothing to say it moved"
        aged(follower)
        follower.tick()
        assert bridges == ["crew", "crew"], "ten minutes on, the tick did not ask Pending You again"

    def test_a_tick_after_nothing_moved_starts_nothing_but_its_fetch_of_each_repository(self, follower, monkeypatch):
        """The crew-board spec, An idle host (Decisions 1 to 3 of a-followers-tick-reads-nothing-while-nothing-moved):
        with every card answered, a bolt held in the box's kit and nothing moved, a tick fetches each repository once and
        asks nothing else: no host, no route, no Pending You and no herdr; reads nothing and starts no process."""
        fetched, bridges, listed = [], [], []
        monkeypatch.setattr(plan, "tips_of", lambda repo, refs: fetched.append((repo, list(refs))) or {r: "x" * 40 for r in refs})
        monkeypatch.setattr(plan, "cards_asked", lambda fleet, read, here, now: ["req_p4"])
        monkeypatch.setattr(plan, "askers_asked", lambda fleet, read, here, now: ["crw-3-conductor"])
        monkeypatch.setattr(plan, "cards_fetched", lambda fleet, cards: bridges.append(list(cards)) or ({c: ({"status": "pending"}, None) for c in cards}, None))
        monkeypatch.setattr(plan, "askers_listed", lambda fleet, names: listed.append(list(names)) or {n: (True, None) for n in names})
        monkeypatch.setattr(plan, "sweep_cards", lambda fleet, read, acts=None, answers=None, listed=None: {"done": [], "unswept": []})
        self.req = {"main": "/kit/main", "bolts": ["te"]}
        self.routes = {BOX: []}
        follower.tick()
        follower.tick()  # the first tick's read had no listing of the askers, so this one asks
        assert bridges == [["req_p4"]] and listed == [["crw-3-conductor"]]
        fetched.clear(), bridges.clear(), listed.clear()
        asked, routes, reads, started = len(self.asked), len(self.routes_asked), len(self.reads), []
        monkeypatch.setattr(board.subprocess, "Popen", lambda *a, **kw: started.append(a))
        monkeypatch.setattr(board.subprocess, "run", lambda *a, **kw: started.append(a))
        follower.tick()
        assert fetched == [("o/state", ["wldn/main", "swancloud/main"]), ("o/bp", ["main"])]
        assert self.asked[asked:] == [{"mac-studio": ["wldn", "swancloud"]}], "a host but this one was asked"
        assert self.routes_asked[routes:] == [[]] and bridges == listed == [] and started == []
        assert len(self.reads) == reads

    def test_another_host_is_asked_only_when_something_there_could_have_moved(self, follower):
        """Decision 1: the box, which holds wldn's kit and runs wldn's runner, is asked when its runner reports, when
        wldn's branch moves, when the last ask of it went unanswered, and ten minutes on; a move of swancloud, which has
        nothing on the box, asks it nothing."""
        follower.refresh()

        def box_asked():
            follower.refresh()
            return BOX in self.asked[-1]
        assert not box_asked()
        self.runner[BOX] = "q" * 40
        assert box_asked() and not box_asked()
        self.looks["state"] = {"wldn": "d" * 40, "swancloud": ""}
        assert box_asked() and not box_asked()
        self.looks["state"] = {"wldn": "d" * 40, "swancloud": "e" * 40}
        assert not box_asked(), "a move of a drive with nothing on the box asked it"
        self.readings[BOX], self.runner[BOX] = None, "p" * 40  # the box asked, and its readings can't be stamped
        assert box_asked() and box_asked(), "a host whose last answer could not be read was not asked again"
        self.readings[BOX] = "r1"
        assert box_asked() and not box_asked()
        aged(follower)
        assert box_asked() and not box_asked()

    def test_a_runners_report_with_no_move_of_its_drives_branch_reads_it_again(self, follower):
        """The crew-board spec, A runner's report: the look stamps the runners' branches, and one moved reads wldn again
        with its unmoved kit served."""
        self.looks["runners"] = {"wldn": {BOX: "r" * 40}, "swancloud": {}}
        follower.refresh()
        follower.refresh()
        assert len(self.reads) == 1
        self.looks["runners"] = {"wldn": {BOX: "q" * 40}, "swancloud": {}}
        follower.refresh()
        assert len(self.reads) == 2 and self.frame("wldn")["text"].startswith("rail of wldn, served")

    def test_a_card_the_sweep_left_is_tried_again_at_the_next_ask_and_not_at_each_tick(self, follower, monkeypatch):
        """The crew-board spec, A card the sweep left: Pending You refused the close of a gone row's card; the cards move
        again at the next ask, ten minutes on, and no tick before it sweeps them."""
        swept = []
        monkeypatch.setattr(type(follower), "fetch", lambda self, fleet: None)
        monkeypatch.setattr(plan, "cards_asked", lambda fleet, read, here, now: ["req_b17"])
        monkeypatch.setattr(plan, "askers_asked", lambda fleet, read, here, now: [])
        monkeypatch.setattr(plan, "cards_fetched", lambda fleet, cards: ({c: ({"status": "pending"}, None) for c in cards}, None))
        monkeypatch.setattr(plan, "askers_listed", lambda fleet, names: {})
        monkeypatch.setattr(plan, "sweep_cards", lambda fleet, read, acts=None, answers=None, listed=None: swept.append(answers) or {
            "done": [dict(label="wldn", key="batch/17", card="req_b17", by="wldn-planner", did="left", words="its close did not go through")],
            "unswept": []})
        follower.tick()
        follower.tick()  # the read's ask answered no card; this one asks after req_b17 and the sweep leaves it
        assert len(swept) == 1 and follower.left
        follower.tick()
        follower.tick()
        assert len(swept) == 1, "a card the sweep left was tried again at a tick that asked nothing"
        aged(follower)
        follower.tick()
        assert len(swept) == 2

    def test_a_submission_the_boxs_runner_reports_is_the_boxs_move_and_starts_no_sluice(self, follower, monkeypatch):
        """The crew-board spec, A merge moves in sluice's queue and A submission moved: a merge queued on the box moves
        nothing the follower reads until the box's runner reports it; its report moves the runner's branch, so the next
        refresh asks the box and reads wldn again, its unmoved kit served, and no refresh starts a process for sluice."""
        self.req = {"main": "/kit/main", "bolts": ["te"]}
        started = []
        monkeypatch.setattr(board.subprocess, "Popen", lambda *a, **kw: started.append(a))
        monkeypatch.setattr(board.subprocess, "run", lambda *a, **kw: started.append(a))
        follower.refresh()
        follower.refresh()
        assert BOX not in self.asked[-1] and len(self.reads) == 1
        self.looks["runners"] = {"wldn": {BOX: "r" * 40}, "swancloud": {}}
        follower.refresh()
        self.runner[BOX] = "q" * 40
        self.looks["runners"] = {"wldn": {BOX: "q" * 40}, "swancloud": {}}
        follower.refresh()
        assert BOX in self.asked[-1] and len(self.reads) == 3 and self.frame("wldn")["text"].startswith("rail of wldn, served")
        follower.refresh()
        assert BOX not in self.asked[-1] and len(self.reads) == 3
        assert started == [], "a refresh started a process"

    def test_a_refresh_after_only_a_hosts_readings_moved_sweeps_its_card_sessions_and_reads_nothing(self, follower):
        """The crew-board spec, A reading sent back: plannotator wrote the result in the box's readings folder, which
        the next refresh that asks the box finds, here once ten minutes have passed with nothing else moved."""
        follower.refresh()
        self.readings[BOX] = "r9"
        follower.refresh()
        assert self.swept == [], "the box was asked with nothing there moved"
        aged(follower)
        follower.refresh()
        assert len(self.reads) == 1 and self.swept == [{"wldn": {BOX}}]
        follower.refresh()
        assert len(self.reads) == 1 and self.swept == [{"wldn": {BOX}}], "a readings folder swept was taken as moved again"

    def test_a_refresh_after_only_the_cards_moved_runs_the_card_sweep_alone_against_the_kept_read(self, follower, monkeypatch):
        """The crew-board spec, A card lost between ticks: the tick's answers say proposal 4's card is lost."""
        swept = []
        monkeypatch.setattr(plan, "sweep_cards", lambda fleet, read, acts=None, answers=None, listed=None: swept.append((read["served"], answers)) or {
            "done": [dict(label="wldn", key="proposal/4", card="req_p4", by="wldn-planner", did="lost", words="posted again as req_p5", new="req_p5")],
            "unswept": []})
        follower.refresh()
        lost = ({"req_p4": (None, "Not found: request:req_p4.")}, None)
        follower.kept.cards, follower.cards = lost, board.cards_stamp(*lost, False, 2)
        follower.refresh()
        assert len(self.reads) == 1 and swept == [(False, lost)] and self.swept == []
        assert [c["card"] for c in follower.last["read"]["cards"]] == ["req_p5"]
        follower.refresh()
        assert swept == [(False, lost)], "the cards swept were taken as moved again before the next tick"

    def test_a_refresh_with_nothing_moved_sweeps_the_sessions_only_where_the_last_could_not(self, follower):
        """The card-sessions spec, A host the last sweep missed."""
        self.unchecked = [{"label": "wldn", "host": BOX, "why": "did not answer (exit 255)"}]
        follower.refresh()
        follower.refresh()
        assert self.swept == [{"wldn": {BOX}}] and len(self.reads) == 1
        follower.refresh()
        assert self.swept == [{"wldn": {BOX}}], "a host the sweep reached was asked again"


    def test_every_refresh_reckons_a_batch_from_the_kept_read_and_one_told_is_not_reckoned_again_at_that_tip(self, follower, monkeypatch):
        """The crew-board spec, A batch made due by the hours: nothing moves, and each refresh reckons from the kept read."""
        reckoned = []
        monkeypatch.setattr(plan, "reckon_batches", lambda fleet, found, read, skip=(): reckoned.append(set(skip)) or ({"wldn": True} if not skip else {}))
        self.found = [("wldn", "o/state", "a" * 40, None)]
        follower.refresh()
        follower.refresh()
        follower.refresh()
        assert len(self.reads) == 1 and reckoned == [set(), {"wldn"}]
        self.looks["state"] = {"wldn": "d" * 40, "swancloud": ""}
        self.found = [("wldn", "o/state", "d" * 40, None)]
        follower.refresh()
        follower.refresh()
        assert len(self.reads) == 2 and reckoned[-1] == set(), "a drive told at an older tip was not reckoned at the new one"

    def test_a_tell_that_did_not_go_through_is_tried_again_at_the_next_tick_and_not_between(self, follower, monkeypatch):
        """wldn's planner is not up: the tell starts herdr, so it is not made at every refresh."""
        reckoned = []
        monkeypatch.setattr(plan, "reckon_batches", lambda fleet, found, read, skip=(): reckoned.append(set(skip)) or ({} if skip else {"wldn": False}))
        monkeypatch.setattr(type(follower), "fetch", lambda self, fleet: None)
        monkeypatch.setattr(type(follower), "ask", lambda self, fleet: None)
        self.found = [("wldn", "o/state", "a" * 40, None)]
        follower.refresh()
        follower.refresh()
        follower.refresh()
        follower.tick()
        assert len(self.reads) == 1 and reckoned == [set(), {"wldn"}, set()]

    def test_a_dev_server_started_by_hand_is_drawn_after_the_next_tick_with_nothing_gathered(self, follower, monkeypatch):
        """The crew-board spec, A dev server started by hand: a tick that asks the box reads its portless routes again,
        here the first once ten minutes have passed with nothing there moved; no refresh between ticks reads them."""
        monkeypatch.setattr(type(follower), "fetch", lambda self, fleet: None)
        monkeypatch.setattr(type(follower), "ask", lambda self, fleet: None)
        follower.refresh()
        route = [{"url": "https://unit-a--switchboard-kit.local", "name": "unit-a--switchboard-kit"}]
        self.routes = {BOX: route}
        follower.refresh()
        assert follower.kept.kits[BOX]["/kit/main"][1]["routes"] == [], "routes were read between ticks"
        follower.tick()
        assert follower.kept.kits[BOX]["/kit/main"][1]["routes"] == [], "a tick with nothing moved on the box read its routes"
        aged(follower)
        follower.refresh()
        assert follower.kept.kits[BOX]["/kit/main"][1]["routes"] == [], "routes were read between ticks"
        follower.tick()
        assert len(self.reads) == 1 and follower.kept.kits[BOX]["/kit/main"][1]["routes"] == route
        follower.tick()
        assert len(self.reads) == 1 and self.swept == []

    def test_an_askers_pane_emptied_moves_the_cards_at_the_tick_and_the_sweep_judges_with_the_listing(self, follower, monkeypatch):
        """The crew-board spec, An asker's agent gone: herdr's listing is read at the tick beside Pending You's answers,
        and the card sweep between ticks judges with it."""
        listing, swept = {"crw-3-conductor": (True, None)}, []
        monkeypatch.setattr(type(follower), "fetch", lambda self, fleet: None)
        monkeypatch.setattr(plan, "cards_asked", lambda fleet, read, here, now: [])
        monkeypatch.setattr(plan, "askers_asked", lambda fleet, read, here, now: ["crw-3-conductor"])
        monkeypatch.setattr(plan, "askers_listed", lambda fleet, names: {n: listing[n] for n in names})
        monkeypatch.setattr(plan, "sweep_cards", lambda fleet, read, acts=None, answers=None, listed=None: swept.append(listed) or {"done": [], "unswept": []})
        follower.tick()
        follower.tick()  # the first tick read the kits and asked nothing of herdr, having no read to ask from
        swept.clear()
        follower.tick()
        assert swept == [] and follower.kept.listed == {"crw-3-conductor": (True, None)}, "the same listing moved the cards"
        listing["crw-3-conductor"] = (False, None)
        follower.refresh()
        follower.tick()
        assert swept == [], "herdr was read between ticks, or at a tick with nothing to say it could have moved"
        aged(follower)
        follower.tick()
        assert swept == [{"crw-3-conductor": (False, None)}] and len(self.reads) == 1


def aged(follower):
    """The follower as it stands DISCOVERY seconds on: every host and Pending You last asked that long ago."""
    for memo in (follower.asked, follower.asked_at_tick):
        memo.update({h: (b, at - board.DISCOVERY) for h, (b, at) in memo.items()})
    if follower.cards_at is not None:
        follower.cards_at -= board.DISCOVERY


def test_the_session_sweep_after_nothing_moved_asks_the_host_the_last_could_not_check_and_no_other(monkeypatch):
    """The card-sessions spec, A host the last sweep missed: unchecked {box} and nothing moved, the box alone is asked."""
    import subprocess
    asked = []
    monkeypatch.setattr(crew, "crew_argv", lambda fleet, h, *a: ["crew", *a])
    monkeypatch.setattr(crew, "on_machine", lambda fleet, h, argv, input=None: asked.append(h) or subprocess.CompletedProcess(argv, 0, "[]", ""))
    found = [("wldn", "WilldanGroup/crew-state", "a" * 40, the_plan())]
    only = plan.sessions_unchecked([{"label": "wldn", "host": BOX, "why": "did not answer (exit 255)"}])
    assert only == {"wldn": {BOX}}
    runs = {"wldn": ([], {BOX: runner_reading({}, BOX)})}  # wldn's runner answers on the box (plan.hosts_of)
    assert plan.sweep_sessions(FLEET, found, {}, [], [], {}, {}, only, runs) == ([], []) and asked == [BOX]
    asked.clear()
    plan.sweep_sessions(FLEET, found, {}, [], [], {}, {}, runs=runs)
    assert asked == [BOX, "mac-studio"], "a refresh after a change did not sweep every host"
    assert plan.sessions_unchecked([]) == {}


def test_the_check_asks_each_host_once_for_its_kits_and_its_readings(monkeypatch):
    """The crew-board spec, A refresh after nothing moved reads nothing: a host's kits and its card readings folders are
    stamped in one request to it, a host with no kit asked for its readings alone, and one that does not answer has
    every stamp of its None, which counts as moved (read.1)."""
    asked = []

    def stamped(fleet, host, kits, labels=(), routes=False):
        asked.append((host, [k["main"] for k in kits], list(labels)))
        return (None, "exit 255") if host == "macbook-pro" else ({"kits": {k["main"]: "s" for k in kits}, "readings": "r"}, None)
    monkeypatch.setattr(plan, "stamped", stamped)
    got = board.stamps_now({}, {BOX: {"/kit/main": ({"main": "/kit/main"}, {})}, "macbook-pro": {"/b/main": ({"main": "/b/main"}, {})}},
                           {BOX: ["wldn"], "mac-studio": ["wldn", "swancloud"], "macbook-pro": ["wldn"]})
    assert asked == [(BOX, ["/kit/main"], ["wldn"]), ("mac-studio", [], ["wldn", "swancloud"]), ("macbook-pro", ["/b/main"], ["wldn"])]
    assert got == {"kits": {(BOX, "/kit/main"): "s", ("macbook-pro", "/b/main"): None}, "readings": {BOX: "r", "mac-studio": "r", "macbook-pro": None},
                   "routes": {}}
    fleet = {"drives": {"wldn": {"machine": "mac-studio", "state": "o/state"}, "swancloud": {"machine": "mac-studio", "state": "o/state"}}}
    monkeypatch.setattr(plan, "runner_tips", lambda repo, label, fetch=True: {BOX: "r" * 40} if label == "wldn" and not fetch else {})
    assert board.readings_hosts(fleet, ["wldn", "swancloud"]) == {BOX: ["wldn"], "mac-studio": ["wldn", "swancloud"]}


class TestMoved:
    """The follower's check before it reads (the crew-board spec, A refresh after nothing moved reads nothing): what moved
    between the stamps its last read was made at and the stamps now."""

    KEPT = {"crew": ("c" * 40, b"{teams}"), "state": {"wldn": "a" * 40, "swancloud": ""}, "blueprints": {"wldn": "b" * 40, "swancloud": "b" * 40},
            "kits": {(BOX, "/kit/main"): "s1", ("mac-studio", "/a/main"): "s2"}, "readings": {BOX: "r1", "mac-studio": "r2"}}

    def now(self, **kw):
        return {k: ({**self.KEPT[k], **kw[k]} if k in kw and isinstance(self.KEPT[k], dict) else kw.get(k, self.KEPT[k])) for k in self.KEPT}

    def test_nothing_moved_names_nothing_and_a_branch_the_cache_lacks_stands(self):
        assert board.moved(self.KEPT, self.now()) == {"crew": False, "state": set(), "blueprints": set(), "kits": set(), "readings": set(),
                                                      "cards": False, "read": False, "any": False}

    def test_one_state_tip_moved_names_its_drive_alone(self):
        m = board.moved(self.KEPT, self.now(state={"wldn": "d" * 40}))
        assert m["state"] == {"wldn"} and not m["crew"] and m["blueprints"] == m["kits"] == set() and m["any"]

    def test_one_kit_moved_names_that_kit_on_its_host(self):
        m = board.moved(self.KEPT, self.now(kits={(BOX, "/kit/main"): "s9"}))
        assert m["kits"] == {(BOX, "/kit/main")} and m["state"] == set() and m["any"]

    def test_a_kit_whose_stamp_could_not_be_read_counts_as_moved(self):
        assert board.moved(self.KEPT, self.now(kits={(BOX, "/kit/main"): None}))["kits"] == {(BOX, "/kit/main")}
        assert board.moved(dict(self.KEPT, kits={(BOX, "/kit/main"): None}), dict(self.KEPT, kits={(BOX, "/kit/main"): None}))["kits"] == {(BOX, "/kit/main")}

    def test_a_kit_new_to_the_read_or_gone_from_it_counts_as_moved(self):
        m = board.moved(self.KEPT, dict(self.KEPT, kits={("mac-studio", "/a/main"): "s2", (BOX, "/b/main"): "s3"}))
        assert m["kits"] == {(BOX, "/kit/main"), (BOX, "/b/main")}

    def test_only_one_hosts_readings_moved_names_that_host_and_nothing_to_read(self):
        """The crew-board spec, A reading sent back: plannotator wrote a result in the box's readings folder."""
        m = board.moved(self.KEPT, self.now(readings={BOX: "r9"}))
        assert m["readings"] == {BOX} and m["kits"] == m["state"] == m["blueprints"] == set() and not m["crew"]
        assert m["any"] and not m["read"]

    def test_a_host_whose_readings_could_not_be_stamped_counts_as_moved(self):
        assert board.moved(self.KEPT, self.now(readings={BOX: None}))["readings"] == {BOX}

    FOUND = {"req_p4": ({"status": "pending", "version": 2}, None), "req_q1": (None, "This is wldn-ops's card; leave it.")}

    def test_the_same_answers_at_the_next_tick_leave_the_cards_and_one_card_now_lost_moves_them(self):
        """The crew-board spec, A card lost between ticks: Pending You answered alike, then no longer finds proposal 4's."""
        kept = dict(self.KEPT, cards=board.cards_stamp(self.FOUND, None, False, 1))
        assert not board.moved(kept, dict(kept, cards=board.cards_stamp(dict(self.FOUND), None, False, 2)))["any"]
        m = board.moved(kept, dict(kept, cards=board.cards_stamp(dict(self.FOUND, req_p4=(None, "Not found: request:req_p4.")), None, False, 2)))
        assert m["cards"] and m["any"] and not m["read"] and m["readings"] == m["kits"] == set()

    def test_a_failed_bridge_or_a_card_the_last_sweep_left_moves_the_cards_at_each_ask_and_only_then(self):
        """A card left because its act did not go through is tried again at the clock's next ask of Pending You
        (cards_due), not at every refresh, nor at a tick that asks nothing."""
        for why, left in (("Pending You did not answer whoami within 30 seconds.", False), (None, True)):
            at_tick = board.cards_stamp(self.FOUND, why, left, 2)
            assert board.moved(dict(self.KEPT, cards=board.cards_stamp(self.FOUND, None, False, 1)), dict(self.KEPT, cards=at_tick))["cards"]
            kept = dict(self.KEPT, cards=at_tick)
            assert not board.moved(kept, dict(kept))["cards"], "a refresh between ticks took the cards as moved again"
            assert board.moved(kept, dict(kept, cards=board.cards_stamp(self.FOUND, why, left, 3)))["cards"]

    def test_an_askers_pane_now_empty_at_the_tick_moves_the_cards(self):
        """The crew-board spec, An asker's agent gone: herdr's listing read at the tick beside Pending You's answers."""
        kept = dict(self.KEPT, cards=board.cards_stamp(self.FOUND, None, False, 1, {"crw-3-conductor": (True, None)}))
        assert not board.moved(kept, dict(kept, cards=board.cards_stamp(self.FOUND, None, False, 2, {"crw-3-conductor": (True, None)})))["any"]
        m = board.moved(kept, dict(kept, cards=board.cards_stamp(self.FOUND, None, False, 2, {"crw-3-conductor": (False, None)})))
        assert m["cards"] and not m["read"]

    def test_a_runners_branch_moved_reads_its_drive_again(self):
        """A runner's report of the places it runs arrives on its own branch, with no move of the drive's: the read
        rests on it as on the drive's branch, so it moves that drive's state, and its runner gone does too."""
        kept = dict(self.KEPT, runners={"wldn": {BOX: "r" * 40}, "swancloud": {}})
        assert not board.moved(kept, dict(kept))["any"]
        m = board.moved(kept, dict(kept, runners={"wldn": {BOX: "q" * 40}, "swancloud": {}}))
        assert m["state"] == {"wldn"} and m["read"]
        assert board.moved(kept, dict(kept, runners={"wldn": {}, "swancloud": {}}))["state"] == {"wldn"}
        assert not board.moved(self.KEPT, dict(self.KEPT))["any"], "a check from before runners were stamped took them as moved"

    def test_crews_head_or_the_teams_file_moved_or_unreadable_says_crew_moved(self):
        assert board.moved(self.KEPT, self.now(crew=("e" * 40, b"{teams}")))["crew"]
        assert board.moved(self.KEPT, self.now(crew=("c" * 40, b"{teams, again}")))["crew"]
        assert board.moved(self.KEPT, self.now(crew=(None, b"{teams}")))["crew"]

    def test_with_no_read_kept_everything_has_moved(self):
        m = board.moved(None, self.KEPT)
        assert m["crew"] and m["state"] == {"wldn", "swancloud"} and m["kits"] == set(self.KEPT["kits"]) and m["any"] and m["read"]
        assert m["readings"] == {BOX, "mac-studio"}


def test_no_asker_to_ask_after_reads_no_herdr_and_each_asker_named_is_listed_afresh(monkeypatch):
    """herdr's listing of the askers is read afresh at the tick, its sessions listed again (crew.herdr_fresh)."""
    fresh = []
    monkeypatch.setattr(crew, "herdr_fresh", lambda: fresh.append(1))
    assert plan.askers_listed(FLEET, []) == {} and fresh == []

    class Acts:
        def listed(self, name):
            return (name == "swb-1-conductor", None)
    assert plan.askers_listed(FLEET, ["swb-1-conductor", "crw-3-conductor"], Acts()) == {"swb-1-conductor": (True, None), "crw-3-conductor": (False, None)}
    assert fresh == [1]


def test_no_card_to_ask_after_starts_no_bridge_and_the_cards_asked_are_asked_in_one():
    """The crew-board spec, No card to ask about: no bridge at all (a logic test's subprocess raises); and the cards the
    clock's tick asks after are asked in one bridge in crew's own name."""
    assert plan.cards_fetched(FLEET, []) == ({}, None)
    opened = []

    class Py:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            pass

        def answer(self, tool, args):
            opened.append((tool, args["requestId"], args["name"]))
            return {"status": "pending"}, None

    class Acts:
        def bridge(self, name, later, held=None):
            opened.append(name)
            return Py()
    assert plan.cards_fetched(FLEET, ["req_1", "req_2"], Acts()) == ({"req_1": ({"status": "pending"}, None), "req_2": ({"status": "pending"}, None)}, None)
    assert opened == ["crew", ("get_request", "req_1", "crew"), ("get_request", "req_2", "crew")]


class TestAsking:
    """What the follower asks of another host, of Pending You and herdr, and of GitHub (the crew-board spec, A refresh
    after nothing moved reads nothing, The follower fetches on a one-minute clock, The follower asks Pending You about
    cards when they could have moved): only what something it reads with no process says could have moved, and each
    repository once a tick (Decisions 1 to 3 of a-followers-tick-reads-nothing-while-nothing-moved)."""

    def basis(self, tip="a" * 40, runner="r" * 40):
        return board.host_basis(BOX, ["wldn"], {"wldn": tip, "swancloud": "s" * 40}, {"wldn": {BOX: runner, "mac-studio": "m" * 40}})

    def test_a_hosts_basis_is_its_drives_branches_and_its_runners_and_no_queue(self):
        """A submission's move is in the host's runner's report, so a moved runner's branch is the host's move, and no
        queue of sluice's is in its basis (crew record 0056 points 1 and 4)."""
        b = self.basis()
        assert b == self.basis(), "a basis read twice with nothing moved differs"
        assert b != self.basis(tip="d" * 40) and b != self.basis(runner="q" * 40)
        assert json.loads(b) == [["wldn", "a" * 40, "r" * 40]]
        assert b == board.host_basis(BOX, ["wldn"], {"wldn": "a" * 40, "swancloud": "e" * 40}, {"wldn": {BOX: "r" * 40, "mac-studio": "n" * 40}}), (
            "a move of a drive the host does not serve, or of another host's runner, moved the host's basis")

    def test_a_host_is_asked_never_asked_moved_unanswered_or_ten_minutes_on_and_else_not(self):
        b, now = self.basis(), 1000.0
        assert board.hosts_due({BOX: b}, {}, now) == [BOX]
        assert board.hosts_due({BOX: b}, {BOX: (b, now - 1)}, now) == []
        assert board.hosts_due({BOX: self.basis(runner="q" * 40)}, {BOX: (b, now - 1)}, now) == [BOX]
        assert board.hosts_due({BOX: b}, {BOX: (b, now - board.DISCOVERY)}, now) == [BOX]
        assert board.DISCOVERY == plan.CARD_RETRY == 600

    def test_pending_you_is_asked_after_a_card_it_has_not_answered_a_failed_bridge_or_ten_minutes_and_never_with_none(self):
        found, now = ({"req_p4": ({"status": "pending"}, None)}, None), 1000.0
        listed = {"crw-3-conductor": (True, None)}
        assert not board.cards_due([], [], None, None, None, now), "nothing to ask after asked Pending You"
        assert board.cards_due(["req_p4"], [], None, None, None, now)
        assert not board.cards_due(["req_p4"], ["crw-3-conductor"], found, listed, now - 1, now)
        assert board.cards_due(["req_p4", "req_p5"], [], found, listed, now - 1, now)
        assert board.cards_due(["req_p4"], ["wldn-planner"], found, listed, now - 1, now)
        assert board.cards_due(["req_p4"], ["crw-3-conductor"], found, {"crw-3-conductor": (None, "herdr did not answer")}, now - 1, now)
        assert board.cards_due(["req_p4"], [], ({}, "Pending You did not answer whoami within 30 seconds."), listed, now - 1, now)
        assert board.cards_due(["req_p4"], [], found, listed, now - board.DISCOVERY, now)
        assert not board.cards_due(["req_p4"], [], found, listed, now - board.DISCOVERY + 1, now)

    def test_each_repository_is_fetched_once_with_every_branch_read_of_it(self):
        fleet = {"drives": {"wldn": {"label": "wldn", "state": "o/state", "blueprints": ["o/bp", "o/other"]},
                                "swancloud": {"label": "swancloud", "state": "o/state", "blueprints": ["s/bp"]},
                                "madswan": {"label": "madswan", "state": "m/state", "blueprints": ["o/bp"]}}}
        assert board.fetches(fleet, ["wldn", "swancloud", "madswan"]) == {
            "o/state": ["wldn/main", "swancloud/main"], "o/bp": ["main"], "s/bp": ["main"], "m/state": ["madswan/main"]}

    def test_the_same_routes_move_nothing_and_a_new_one_moves_its_host(self):
        """The crew-board spec, A dev server started by hand."""
        a = {"url": "https://unit-a--switchboard-kit.local", "name": "unit-a--switchboard-kit"}
        kits = {BOX: {"/kit/main": ({"main": "/kit/main"}, {"ok": True, "routes": [a]}), "/b/main": ({"main": "/b/main"}, {"ok": False})},
                "mac-studio": {"/a/main": ({"main": "/a/main"}, {"ok": True, "routes": None})}}
        assert board.routes_moved(kits, {BOX: [a], "mac-studio": None}) == set()
        assert board.routes_moved(kits, {BOX: [a, dict(a, name="unit-b--switchboard-kit")], "mac-studio": None}) == {BOX}
        assert board.routes_moved(kits, {"mac-studio": []}) == {"mac-studio"}


class TestKept:
    """What the host's follower keeps between its refreshes and serves while it has not moved (the crew-board spec, A
    refresh after a change reads only what moved; plan.12's reading of 2026-10-28)."""

    REQ = {"main": "/kit/main", "dir": "/kit", "bolts": []}
    ANSWER = {"ok": True, "main": [], "stamp": "s1"}

    def test_a_kit_is_served_only_at_the_stamp_and_request_it_was_read_at(self):
        kept = (self.REQ, self.ANSWER)
        assert plan.kit_served(kept, "s1", self.REQ) == self.ANSWER
        assert plan.kit_served(kept, "s2", self.REQ) is None, "a moved kit was served"
        assert plan.kit_served(kept, "s1", dict(self.REQ, bolts=["tenant-environments"])) is None, "a kit asked of anew was served"
        assert plan.kit_served(kept, None, self.REQ) is None, "a kit whose stamp could not be read was served"
        assert plan.kit_served((self.REQ, None), "s1", self.REQ) is None and plan.kit_served(None, "s1", self.REQ) is None

    def test_a_board_survey_asks_each_host_for_its_moved_kits_alone_and_keeps_what_it_read(self, monkeypatch):
        asked = []

        def gathered(fleet, host, req):
            asked.append((host, sorted(k["main"] for k in req["kits"]), req.get("stamped")))
            return {k["main"]: {"ok": True, "stamp": "new"} for k in req["kits"]}, None
        monkeypatch.setattr(plan, "gathered", gathered)
        held = [(w, None) for w in WHERE.values()]
        k = plan.Kept()
        monkeypatch.setattr(plan.READ, "follower", k)
        first = plan.survey(FLEET, held, board=True)
        assert sorted(asked) == [("chuck-herdr-alpha", ["/b/main", "/kit/main"], True), ("mac-studio", ["/a/main"], True)]
        k.settle()
        k.stamps = {(BOX, "/kit/main"): "new", (BOX, "/b/main"): "moved", ("mac-studio", "/a/main"): "new"}
        asked.clear()
        again = plan.survey(FLEET, held, board=True)
        assert asked == [(BOX, ["/b/main"], True)], "an unmoved kit was gathered again, or a moved one served"
        assert again[BOX]["kits"]["/kit/main"] == first[BOX]["kits"]["/kit/main"] and again["mac-studio"] == first["mac-studio"]
        assert set(k.used) == {BOX, "mac-studio"} and set(k.used[BOX]) == {"/kit/main", "/b/main"}

    def test_a_board_survey_hands_a_kit_no_queue(self, monkeypatch):
        """crew-board "A gather runs no sluice": the follower's gather of a kit is asked its bolts and nothing of sluice's
        queue, and the follower keeps no queue to hand it (crew record 0056 points 1 and 4)."""
        asked = []
        monkeypatch.setattr(plan, "gathered", lambda fleet, host, req: asked.append(req) or ({k["main"]: {"ok": True} for k in req["kits"]}, None))
        k = plan.Kept()
        monkeypatch.setattr(plan.READ, "follower", k)
        plan.survey(FLEET, [(WHERE["a"], "te")], board=True)
        assert [sorted(x) for x in asked[0]["kits"]] == [["bolts", "dir", "main"]]
        assert not hasattr(k, "queued") and not hasattr(k, "decided")

    def test_a_host_that_does_not_answer_is_kept_with_no_answer_so_its_kits_read_as_moved(self, monkeypatch):
        monkeypatch.setattr(plan, "gathered", lambda fleet, host, req: (None, "ssh: connect timed out") if host == BOX else
                            ({k["main"]: {"ok": True, "stamp": "s"} for k in req["kits"]}, None))
        k = plan.Kept()
        monkeypatch.setattr(plan.READ, "follower", k)
        sv = plan.survey(FLEET, [(w, None) for w in WHERE.values()], board=True)
        assert sv[BOX] == {"ok": False, "error": "ssh: connect timed out"}
        assert {m: a for m, (_, a) in k.used[BOX].items()} == {"/kit/main": None, "/b/main": None}

    def test_a_survey_of_any_other_command_is_served_nothing_the_follower_kept(self, monkeypatch):
        asked = []
        monkeypatch.setattr(plan, "gathered", lambda fleet, host, req: asked.append(host) or ({k["main"]: {"ok": True} for k in req["kits"]}, None))
        plan.survey(FLEET, [(WHERE["a"], None)], board=True)
        assert asked == [BOX] and plan.READ.follower is None

    def test_a_state_file_at_a_tip_already_listed_is_its_kept_blob_and_starts_no_git(self, monkeypatch):
        calls = []
        tip = "f" * 40
        monkeypatch.setattr(plan, "git", lambda repo, *args, **kw: calls.append(args[0]) or f"100644 blob {'1' * 40}\tplan.rec\n100644 blob {'2' * 40}\tsignals/c/01-x.md")
        monkeypatch.setattr(plan, "cat_file", lambda repo, names: calls.append("cat-file") or [f"text of {n}" for n in names])
        k = plan.Kept()
        monkeypatch.setattr(plan.READ, "follower", k)
        assert plan.show("o/state", tip, "plan.rec") == f"text of {'1' * 40}" and plan.show("o/state", tip, "moves.rec") is None
        assert plan.paths_at("o/state", tip, "signals/") == ["signals/c/01-x.md"]
        assert board.texts("o/state", tip, ["signals/c/01-x.md", "signals/c/capture.md"]) == {"signals/c/01-x.md": f"text of {'2' * 40}"}
        assert calls == ["ls-tree", "cat-file"], "a kept tip was listed again or a held blob read again"
        k.settle()
        assert plan.show("o/state", tip, "plan.rec") == f"text of {'1' * 40}" and calls == ["ls-tree", "cat-file"]
        k.settle()
        k.settle()
        assert k.listings == {} and k.blobs == {}, "a tip no refresh read kept its blobs"


class TestRailFrame:
    """The rail tab draws the rail frame the host's follower writes (the crew-board spec, The rail and the board come
    from one read)."""

    RAIL = {"read_at": board.iso(NOW), "from": "mac-studio", "text": "What waits on you (wldn), as of 10:00:00\n\nproposals\n  none", "updated": None}

    def test_a_fresh_frame_is_the_rail_as_its_round_printed_it(self):
        assert board.rail_frame_text("wldn", self.RAIL, NOW) == self.RAIL["text"]

    def test_what_handing_out_the_restarts_said_follows_the_rail(self):
        said = board.rail_frame_text("wldn", dict(self.RAIL, updated="wldn-planner is due a restart: crew _renew restarts it once idle"), NOW)
        assert said == self.RAIL["text"] + "\n\nwldn-planner is due a restart: crew _renew restarts it once idle"

    def test_a_frame_read_five_minutes_ago_is_headed_with_its_age(self):
        said = board.rail_frame_text("wldn", dict(self.RAIL, read_at=board.iso(NOW - datetime.timedelta(minutes=5))), NOW).splitlines()
        assert said[0].startswith("wldn's rail as read at ")
        assert said[0].endswith(", 5m ago: the host's follower on mac-studio has not refreshed it since")
        assert said[1:] == ["", *self.RAIL["text"].splitlines()]
        assert board.rail_frame_text("wldn", dict(self.RAIL, read_at=board.iso(NOW - datetime.timedelta(seconds=board.STALE - 5))), NOW) == self.RAIL["text"]

    def test_with_no_frame_the_rail_tab_says_the_hosts_follower_writes_it(self):
        assert board.rail_frame_text("wldn", None, NOW) == (
            "No rail for wldn yet: the host's follower writes it each time it refreshes, swancloud's job or the console's rail tab, "
            "which crew console up wldn opens while no job runs.")

    def test_the_rail_tab_draws_the_frame_once_and_follows_nothing(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setattr(board, "FRAMES", tmp_path)
        board.write_frame("wldn", self.RAIL, board.rail_path("wldn"))
        board.rail_follow("wldn", once=True)
        assert capsys.readouterr().out == self.RAIL["text"] + "\n" and board.follower_here() == "none"

    def test_the_rail_tab_draws_the_jobs_frames_and_follows_itself_once_the_job_ends(self, tmp_path, monkeypatch, capsys):
        """The host's job holds the lock: the tab draws and waits; once the job lets go, the tab takes the lock as a tab
        and makes the rounds itself."""
        monkeypatch.setattr(board, "FRAMES", tmp_path)
        board.write_frame("wldn", self.RAIL, board.rail_path("wldn"))
        job, slept, stepped = board.lock_follower("job", wait=False), [], []

        class Done(Exception):
            pass

        class Stepping:
            def __init__(self, lock):
                self.lock = lock

            def step(self, most):
                stepped.append((board.lock_path().read_text().split()[:2], most))
                raise Done

            def close(self):
                self.lock.close()

        def sleep(s):
            slept.append(s)
            job.close()
        monkeypatch.setattr(board, "Follower", Stepping)
        monkeypatch.setattr(board.time, "sleep", sleep)
        with pytest.raises(Done):
            board.rail_follow("wldn")
        assert slept == [1] and stepped == [(["tab", "wldn"], 1)] and board.follower_here() == "none"
        assert capsys.readouterr().out == self.RAIL["text"] + "\n"

    def test_half_a_rail_frame_or_one_with_no_text_reads_as_none(self, tmp_path, monkeypatch):
        monkeypatch.setattr(board, "FRAMES", tmp_path)
        assert board.read_rail("wldn") is None
        (tmp_path / "wldn.rail.json").write_text('{"read_at": ')
        assert board.read_rail("wldn") is None
        (tmp_path / "wldn.rail.json").write_text(json.dumps(dict(self.RAIL, text=None)))
        assert board.read_rail("wldn") is None
        board.write_frame("wldn", self.RAIL, board.rail_path("wldn"))
        assert board.read_rail("wldn") == self.RAIL and board.read_frame("wldn") is None
        assert sorted(p.name for p in tmp_path.iterdir()) == ["wldn.rail.json"]


class TestMore:
    def test_a_captures_age_is_said_from_its_time_and_a_date_as_it_is(self):
        sigs = [dict(SIGS[0], captured_by="otter", at=ago(5 * 60)), dict(SIGS[1], captured_by="otter", at=ago(3 * 60))]
        line = next(l for l in lane(board.board_text(data(signals=sigs)), "Inception") if "signals captured by otter" in l)
        assert "2 not moved, the oldest captured 5h" in line and line.endswith(" ago")

    def test_the_board_answers_nothing_it_offers_no_approving_or_telling_command(self):
        props = [{"label": "wldn", "proposal": 1, "by": "chuck@mac-studio", "opened": "2026-10-12", "case": "The console.",
                  "changes": [{"do": 'bolt new console-two "x" --repo switchboard-kit', "bolts": ["console-two"]}]}]
        out = board.board_text(data(props=props, signals=SIGS))
        for no in ("crew plan approve", "crew unit approve", "crew tell"):
            assert no not in out

    def test_the_json_holds_each_lanes_objects_and_the_ledgers_units_and_fixes(self):
        d = data(signals=SIGS)
        p = d["drives"][0]
        assert sorted(d) == ["drives", "from", "read_at", "unread"]
        assert sorted(p) == ["asking", "attention", "bolt_plan", "cards", "construction", "environments", "fixing", "hosts", "inception", "kits",
                             "label", "operation", "plan", "records", "runs"]
        assert p["kits"] == ["breadboard-kit", "switchboard-kit"]
        te = next(b for b in p["construction"] if b["bolt"] == "tenant-environments")
        assert sorted(te) == ["bolt", "fixes", "goal", "head", "host", "landing", "markers", "record", "repo", "state", "stream", "time",
                              "units", "url"]
        assert (te["host"], te["stream"]) == (BOX, "wldn")  # where the box's runner reported its work (plan.bolt_at)
        assert sorted(te["units"][0]) == ["flume", "kind", "stage", "tasks", "unit", "url", "worktree"]
        assert te["fixes"] == []  # a fix is a started bolt's Flume place alone (TestCrossed)

    def test_half_a_frame_or_one_with_no_time_reads_as_none(self, tmp_path, monkeypatch):
        monkeypatch.setattr(board, "FRAMES", tmp_path)
        assert board.read_frame("wldn") is None
        (tmp_path / "wldn.json").write_text('{"read_at": ')
        assert board.read_frame("wldn") is None
        (tmp_path / "wldn.json").write_text('{"drives": []}')
        assert board.read_frame("wldn") is None
        board.write_frame("wldn", dict(data(), read_at=board.iso(NOW)))
        assert board.read_frame("wldn")["drives"][0]["label"] == "wldn" and sorted(p.name for p in tmp_path.iterdir()) == ["wldn.json"]


def view(name, **kw):
    """An agent's view of the fixture's board, a line to a string as its mod draws it, styles left out."""
    return ["".join(s for s, _ in line) for line in board.agent_views(data(**kw))["views"][name]]


def ledger(name, bolt, **kw):
    """A bolt's ledger in an agent's view: its head line and the lines of its work under it."""
    lines = view(name, **kw)
    i = next(i for i, l in enumerate(lines) if f"  {bolt}  " in l and not l.startswith("    "))
    j = next((j for j in range(i + 1, len(lines)) if not lines[j].startswith("    ")), len(lines))
    return lines[i:j]


WAITS = [{"label": "wldn", "proposal": 2, "by": "wldn-planner", "opened": "2026-10-12", "case": "Tenants get d.",
          "changes": [{"do": 'unit add d "Unit d." --bolt tenant-environments', "bolts": ["tenant-environments"]}]}]


class TestViews:
    def test_the_planner_reads_each_bolt_in_flight_as_a_ledger_a_pip_to_each_unit_then_what_comes_next(self):
        """Ordering within a bolt, batches and amendments are the planner's (Decision 6 of the-team-machinery-leaves), so
        its band draws each started bolt as the ledger a conductor's did, product by product, no slot named."""
        assert view("wldn-planner") == [
            "wldn plan  2 in flight  1 planned  1 queued  0 proposals open",
            f"! breadboard-kit  ●  board-done  in Flume stream wldn  landed  1 of 1 merged  {DONE_TIME}", "    ●  done-one  landed",
            f"  switchboard-kit  ◑◔  tenant-environments  in Flume stream wldn  0 of 2 merged  {TE_TIME}", "    ◑  a  code 1/2", "    ◔  b  construct",
            "  switchboard-kit  next  apex-zones", "  queued  1 in switchboard-kit",
            "! bolt board-done: every unit has landed on main, and the bolt is still in the plan"]

    def test_a_started_bolt_that_waits_to_land_and_one_in_flight_of_one_kit_are_both_drawn(self, monkeypatch):
        """Two bolts of switchboard-kit started, doctor-rows proven, so it waits to land (teams.16), and ssh-fix at code:
        the planner's band and the Construction lane draw both, the proven one saying it waits to land."""
        two = plan.Plan(plan_text(bolts=[("doctor-rows", "switchboard-kit", True), ("ssh-fix", "switchboard-kit", True)],
                                  units=[("rows-one", "switchboard-kit", "doctor-rows", []), ("ssh-one", "switchboard-kit", "ssh-fix", [])]))
        monkeypatch.setitem(globals(), "the_plan", lambda: two)
        monkeypatch.setitem(globals(), "PLACED", {"rows-one": ("landed", None), "ssh-one": ("code", (1, 2))})
        sv = kits()
        swb = sv[BOX]["kits"]["/kit/main"]
        swb["bolts"].update({"doctor-rows": {"head": LANDED, "head_at": ago(30), "changes": ["rows-one"], "archived": ["rows-one"]},
                             "ssh-fix": {"head": "c" * 40, "head_at": ago(20), "changes": []}})
        mine = view("wldn-planner", sv=sv)
        assert mine[1:5] == [f"✓ switchboard-kit  ●  doctor-rows  in Flume stream wldn  waits to land  1 of 1 merged  {NO_START}  no card open", "    ●  rows-one  merged",
                             f"  switchboard-kit  ◑  ssh-fix  in Flume stream wldn  0 of 1 merged  {NO_START}", "    ◑  ssh-one  code 1/2"]
        assert lane(board.board_text(data(sv=sv)), "Construction") == [
            f"✓ switchboard-kit doctor-rows  on chuck-herdr-alpha  in Flume stream wldn  waits to land  {NO_START}  no card open", "    rows-one  merged",
            f"  switchboard-kit ssh-fix  on chuck-herdr-alpha  in Flume stream wldn  {NO_START}", "    ssh-one  code 1/2"]

    def test_each_bolt_is_marked_from_its_kits_landing_row_and_ops_band_draws_the_row_with_its_card(self, monkeypatch):
        """Two proven bolts of one kit are one landing row, land/<kit> (crew-rail "Two bolts of one kit"): each bolt's
        marker is that row's, its card main-level ops's, which ops's band draws, the row naming both, and the card above
        ops's prompt; the operator counts the row once (code.8)."""
        two = plan.Plan(plan_text(bolts=[("doctor-rows", "switchboard-kit", True), ("ssh-fix", "switchboard-kit", True)],
                                  units=[("rows-one", "switchboard-kit", "doctor-rows", []), ("ssh-one", "switchboard-kit", "ssh-fix", [])]))
        monkeypatch.setitem(globals(), "the_plan", lambda: two)
        monkeypatch.setitem(globals(), "PLACED", {"rows-one": ("landed", None), "ssh-one": ("landed", None)})
        sv = kits()
        sv[BOX]["kits"]["/kit/main"]["bolts"].update({
            "doctor-rows": {"head": LANDED, "head_at": ago(30), "changes": ["rows-one"], "archived": ["rows-one"]},
            "ssh-fix": {"head": LANDED, "head_at": ago(20), "changes": ["ssh-one"], "archived": ["ssh-one"]}})
        card = dict(label="wldn", card="req_k1", key="land/switchboard-kit", by="wldn-ops", host="mac-studio", at=NOW)
        d = data(sv=sv, cards=[card])
        ledgers = {b["bolt"]: b["markers"] for b in d["drives"][0]["construction"]}
        assert [m["key"] for m in ledgers["doctor-rows"]] == [m["key"] for m in ledgers["ssh-fix"]] == ["land/switchboard-kit"]
        assert ledgers["ssh-fix"][0]["card"]["by"] == "wldn-ops"
        assert "✓ land/switchboard-kit  doctor-rows, ssh-fix  wait to land  card open, asked by wldn-ops" in view("wldn-ops", sv=sv, cards=[card])
        v = board.agent_views(d)
        assert "".join(t for t, _ in v["cards"]["wldn-ops"][0]).startswith("  your card  land/switchboard-kit  req_k1")
        assert "✓ 1 to approve" in "\n".join(view("wldn-operator", sv=sv, cards=[card]))
        assert ledger("wldn-planner", "doctor-rows", sv=sv, cards=[card])[0].endswith(
            f"doctor-rows  in Flume stream wldn  waits to land  1 of 1 merged  {NO_START}  card open, asked by wldn-ops")

    def test_ops_answered_landings_card_says_the_landing_is_ops_own(self, monkeypatch):
        """crew-board "Ops's answered landings card": land/switchboard-kit's card, wldn-ops's, the user's answer on it
        recorded; ops's band shows the card answered and its land line says the landing is ops's, and the planner's
        ledger says the card waits on ops, as the rail's card line does (design Decision 3)."""
        two = plan.Plan(plan_text(bolts=[("doctor-rows", "switchboard-kit", True)], units=[("rows-one", "switchboard-kit", "doctor-rows", [])]))
        monkeypatch.setitem(globals(), "the_plan", lambda: two)
        monkeypatch.setitem(globals(), "PLACED", {"rows-one": ("landed", None)})
        sv = kits()
        sv[BOX]["kits"]["/kit/main"]["bolts"].update({
            "doctor-rows": {"head": LANDED, "head_at": ago(30), "changes": ["rows-one"], "archived": ["rows-one"]}})
        card = dict(label="wldn", card="req_k1", key="land/switchboard-kit", by="wldn-ops", host="mac-studio", at=NOW - datetime.timedelta(hours=1),
                    answered=dict(at=NOW - datetime.timedelta(minutes=5), answer="ticked doctor-rows", heads="doctor-rows@d185a87"))
        d = data(sv=sv, cards=[card])
        (m,) = d["drives"][0]["construction"][0]["markers"]
        assert m["card"]["answered"] == board.iso(NOW - datetime.timedelta(minutes=5))
        assert ("✓ land/switchboard-kit  doctor-rows  waits to land  answered: crew asks the runner to land what the user ticked  card answered, waits on wldn-ops"
                in view("wldn-ops", sv=sv, cards=[card]))
        assert ["".join(t for t, _ in l) for l in board.agent_views(d)["cards"]["wldn-ops"]] == [
            "  your card  land/switchboard-kit  req_k1  answered 5m ago, yours to act on"]
        assert ledger("wldn-planner", "doctor-rows", sv=sv, cards=[card])[0].endswith("card answered, waits on wldn-ops")
        waiting = dict(card, answered=None)
        assert "✓ land/switchboard-kit  doctor-rows  waits to land  card open, asked by wldn-ops" in view("wldn-ops", sv=sv, cards=[waiting])

    def test_a_unit_waits_on_no_answer_so_it_has_no_marker_even_with_an_old_verify_card_open(self):
        card = dict(label="wldn", card="req_2", key="verify/a/20261012-1200", by="swb-1-conductor", host="mac-studio", at=NOW)
        assert ledger("wldn-planner", "tenant-environments", cards=[card])[1] == "    ◑  a  code 1/2"

    def test_a_proposal_touching_a_started_bolt_waits_on_no_agreement(self):
        assert "✓ proposal 2 by wldn-planner  Tenants get d.  no card open" in view("wldn-planner", props=WAITS)

    def test_a_bolt_whose_host_does_not_answer_is_unknown_and_the_host_is_named_for_attention(self):
        """Its state can't be told, and its time is read from the run record alone; its units' stages are the runner's,
        read from the branch."""
        mine = view("wldn-planner", sv=kits(ok=False))
        assert ledger("wldn-planner", "tenant-environments", sv=kits(ok=False))[:2] == [
            f"  switchboard-kit  ◑◔  tenant-environments  in Flume stream wldn  unknown  0 of 2 merged  {TE_TIME}", "    ◑  a  code 1/2"]
        assert f"! {BOX} did not answer (its kits: ssh: timed out)" in mine

    QUEUED = [dict(entry("bolt.submit", 30, Outcome="queued", Submission="412", Head=S1), On=["bolt/tenant-environments"])]
    READY = "chore tidy-a has not landed on main: it is ready"
    UNCLOSED = [dict(entry("bolt.submit", 30, Outcome="landed", Submission="412", Head=S1), On=["bolt/tenant-environments"]),
                entry("bolt.land", 29, bolt="tenant-environments", Refused=READY, By="wldn-ops")]

    def test_a_landing_queued_is_said_on_its_bolts_head_line_with_sluices_number(self):
        """crew-board "A landing recorded queued that sluice no longer has standing": on the lane and in the planner's band."""
        assert ledger("wldn-planner", "tenant-environments", logs=self.QUEUED)[0] == (
            f"  switchboard-kit  ◑◔  tenant-environments  in Flume stream wldn  landing queued as #412  0 of 2 merged  {TE_TIME}")
        assert f"  switchboard-kit tenant-environments  on chuck-herdr-alpha  in Flume stream wldn  landing queued as #412  {TE_TIME}" in lane(
            board.board_text(data(logs=self.QUEUED)), "Construction")

    def test_a_close_refused_is_said_on_its_head_line_in_the_attention_gutter_to_the_planner_and_main_level_ops(self):
        """crew-board "A close refused": on the lane, in the planner's band and in main-level ops's band, in the words of
        its last refused close, which the planner's attention names too."""
        said = f"landed on main, not closed: {self.READY}"
        mine = view("wldn-planner", logs=self.UNCLOSED)
        head = f"! switchboard-kit  ◑◔  tenant-environments  in Flume stream wldn  {said}  0 of 2 merged  {TE_TIME}"
        assert head in mine and f"! bolt tenant-environments: it landed on main and was not closed: {self.READY}" in mine
        assert head in view("wldn-ops", logs=self.UNCLOSED)
        assert f"! switchboard-kit tenant-environments  on chuck-herdr-alpha  in Flume stream wldn  {said}  {TE_TIME}" in lane(board.board_text(data(logs=self.UNCLOSED)),
                                                                                                       "Construction")
        assert not [l for l in view("wldn-ops") if "not closed" in l]

    REJECTED = QUEUED + [dict(entry("bolt.submit", 25, Refused="#412 conflict: README.md", Submission="412", Head="d" * 40),
                              On=["bolt/tenant-environments"])]

    def test_a_landing_rejected_or_landing_again_is_said_on_its_head_line_as_a_state_of_its_own(self):
        """crew-board "A landing rejected" and "Landing again": rejected at its head now, the bolt open for work, in
        sluice's words; once submitted again, landing again after the rejection, with the record's number."""
        assert ledger("wldn-planner", "tenant-environments", logs=self.REJECTED)[0] == (
            "  switchboard-kit  ◑◔  tenant-environments  in Flume stream wldn  landing #412 rejected at ddddddd, open for work: "
            f"#412 conflict: README.md  0 of 2 merged  {TE_TIME}")
        again = self.REJECTED + [dict(entry("bolt.submit", 20, Outcome="queued", Submission="415", Head="e" * 40), On=["bolt/tenant-environments"])]
        assert ledger("wldn-planner", "tenant-environments", logs=again)[0] == (
            "  switchboard-kit  ◑◔  tenant-environments  in Flume stream wldn  landing again as #415, after #412 was rejected  "
            f"0 of 2 merged  {TE_TIME}")
        assert board.landing_of(again, "tenant-environments")["state"] == "again"

    def test_what_a_held_bolts_landing_is_read_from_the_run_record(self):
        """Decision 5 (board.landing_of): queued while its last bolt.submit is, unclosed while its last bolt.land since
        its landing is refused, and nothing once a close went through or before any landing."""
        b = "tenant-environments"
        assert board.landing_of(self.QUEUED, b) == {"state": "queued", "n": "412", "head": S1}
        assert board.landing_of(self.UNCLOSED, b) == {"state": "unclosed", "words": self.READY}
        assert board.landing_of(self.UNCLOSED + [entry("bolt.land", 20, bolt=b, Repo="switchboard-kit", Head=S2)], b) is None
        assert board.landing_of(self.UNCLOSED[:1], b) is None and board.landing_of([], b) is None
        refused_before = [entry("bolt.land", 40, bolt=b, Refused=self.READY)] + self.UNCLOSED[:1]
        assert board.landing_of(refused_before, b) is None
        assert board.landing_of(self.UNCLOSED, "ssh-fix") is None

    def test_the_planner_reads_the_plan_in_brief_each_bolt_in_flight_and_the_proposals(self):
        mine = view("wldn-planner", props=WAITS)
        assert mine[0] == "wldn plan  2 in flight  1 planned  1 queued  1 proposal open"
        assert mine[6:] == ["✓ proposal 2 by wldn-planner  Tenants get d.  no card open", "  switchboard-kit  next  apex-zones",
                            "  queued  1 in switchboard-kit", "! bolt board-done: every unit has landed on main, and the bolt is still in the plan"]

    def test_each_bolt_in_flight_or_planned_is_led_by_its_product_and_names_no_team(self):
        lines = board.agent_views(data())["views"]["wldn-planner"]
        flying = next(l for l in lines if "tenant-environments" in "".join(s for s, _ in l))
        assert flying[:4] == [("  ", None), ("switchboard-kit", None), ("  ", None), ("◑◔", None)]
        planned = next(l for l in lines if "apex-zones" in "".join(s for s, _ in l))
        assert planned[:4] == [("  ", None), ("switchboard-kit", None), ("  ", None), ("next", "dim")]

    def test_the_design_agent_reads_the_signals_by_who_captured_them_and_the_first_explorations(self, monkeypatch):
        monkeypatch.setattr(board, "SHOWN", 0)
        assert view("wldn-design", signals=SIGS) == ["wldn inception  3 signals not moved  1 exploration", "  signals captured by wldn-planner  2 not moved",
                                                     "  signals captured by chuck@mac-studio  1 not moved", "  and 1 more exploration"]
        monkeypatch.setattr(board, "SHOWN", 6)
        assert view("wldn-design")[1:] == ["  switchboard-kit command-cost  Reading: what each crew command costs."]

    def test_an_operator_reads_the_drives_board_in_brief_and_what_waits_on_the_user(self):
        mine = view("wldn-operator", props=WAITS, signals=SIGS)
        assert mine[:4] == [f"wldn board  read from {BOX}, mac-studio", "Inception  3 signals not moved  1 exploration",
                            "Bolt plan  1 proposal open  1 planned  1 queued", "Construction"]
        assert mine[4:7] == [f"! breadboard-kit  ●  board-done  in Flume stream wldn  landed  1 of 1 merged  {DONE_TIME}",
                             f"  switchboard-kit  ◑◔  tenant-environments  in Flume stream wldn  0 of 2 merged  {TE_TIME}",
                             "Operation  0 landed in seven days"]
        assert "Operation  0 landed in seven days" in mine and "waits on the user  ✓ 1 to approve" in mine

    def test_an_operator_reads_each_environment_with_a_deploy_or_an_operation_waiting_and_counts_their_cards(self):
        mine = view("wldn-operator", entries=OPS)
        at = mine.index("Operation  0 landed in seven days")
        assert mine[at + 1] == f"✓ mac-studio  deploy {S2[:7]}  waits on the user's word  2 operations waiting"
        assert "waits on the user  ✓ 2 to approve" in mine

    def test_main_level_ops_reads_each_deploy_waiting_on_the_word_or_running_and_each_operation_step_with_its_doer(self):
        running = entry("ops.deploy", 10, env="swancloud-srv", Head=S1, Base="none", Phase="start")
        assert view("wldn-ops", entries=OPS + [running], cards=[DEPLOY_CARD]) == [
            "wldn operations  1 deploy waits on the user's word  1 deploy running  2 operations waiting",
            f"✓ mac-studio  deploy {S2[:7]}  waits on the user's word  card open, asked by wldn-ops",
            f"  mac-studio  restart-roles/1  after {S1[:7]}  handed  doer main-ops, wldn-ops",
            "✓ mac-studio  rotate-key  waiting  doer user  no card open",
            f"  swancloud-srv  deploy {S1[:7]}  deploying since {board.local(ago(10))}"]

    def test_main_level_ops_reads_a_deploy_whose_card_post_was_refused_as_owing_its_card(self):
        """crew-board "A deploy whose card was refused", in main-level ops's view."""
        assert view("wldn-ops", entries=OPS, logs=OPS + [REFUSED_POST])[1] == (
            f"✓ mac-studio  deploy {S2[:7]}  waits on the user's word  no card open, its post refused")

    def test_a_step_held_for_the_users_word_is_marked_held_and_waits_on_its_card(self):
        held = entry("ops.step", 10, Head=S1, Key="restart-herdr/1", State="waiting", Doer="main-ops", Agent="wldn-ops", When="quiet held")
        assert view("wldn-ops", entries=OPS + [held])[-1] == (
            f"✓ mac-studio  restart-herdr/1  after {S1[:7]}  waiting  doer main-ops, wldn-ops, held for the user's word  no card open")
        assert lane(board.board_text(data(entries=OPS + [held])), "Operation")[-1] == (
            "✓ mac-studio  restart-herdr/1  held for the user's word, for wldn-ops  no card open")

    def test_a_deploy_waiting_at_its_gate_is_said_to_wait_there_for_the_user_and_main_level_ops_names_it_the_gate_of_its_commit(self):
        run = "https://github.com/WilldanGroup/switchboard-kit/actions/runs/38612817613"
        gate = entry("ops.step", 10, Head=S1, Key="gate-38612817613", State="waiting", Doer="user", Text=run)
        assert view("wldn-ops", entries=OPS + [gate])[-1] == f"✓ mac-studio  gate-38612817613  gate of {S1[:7]}  waiting  doer user  no card open"
        assert lane(board.board_text(data(entries=OPS + [gate])), "Operation")[-1] == (
            f"✓ mac-studio  gate-38612817613  waits at its gate for the user  {run}  no card open")
        bare = dict(gate, Head=None)
        assert view("wldn-ops", entries=OPS + [bare])[-1] == "✓ mac-studio  gate-38612817613  gate  waiting  doer user  no card open"

    def test_main_level_ops_with_nothing_waiting_reads_its_head_and_no_deploy_done_or_replaced(self):
        done = [entry("ops.offer", 30, Head=S1, Base="none"), entry("ops.offer", 20, Head=S2, Base="none"), entry("ops.approve", 15, Head=S2),
                entry("ops.deploy", 12, Head=S2, Phase="start"), entry("ops.deploy", 10, Head=S2, Phase="end", Outcome="done")]
        assert view("wldn-ops", entries=done) == ["wldn operations  0 deploys wait on the user's word  0 deploys running  0 operations waiting"]

    def test_an_approved_deploy_whose_word_went_to_a_newer_offer_leaves_main_level_opss_view_and_the_board_says_so(self):
        """mac-studio, 2026-10-15 to 18: 45eecf3 approved and never deployed, its word gone to 291a4e6, deployed since,
        stood as approved, not yet deployed in swancloud-ops's band."""
        moved = [entry("ops.offer", 30, Head=S1, Base="none"), entry("ops.approve", 25, Head=S1), entry("ops.offer", 20, Head=S2, Base=S1),
                 entry("ops.approve", 15, Head=S2), entry("ops.deploy", 12, Head=S2, Base=S1, Phase="start"),
                 entry("ops.deploy", 10, Head=S2, Phase="end", Outcome="done")]
        assert view("wldn-ops", entries=moved) == ["wldn operations  0 deploys wait on the user's word  0 deploys running  0 operations waiting"]
        assert lane(board.board_text(data(entries=moved)), "Operation")[-1].startswith(
            f"  mac-studio  deploy {S1[:7]} from nothing deployed  approved, then the word went to a newer offer  carrying")

    def test_an_approved_deploy_whose_word_a_newer_deploys_end_spent_leaves_main_level_opss_view_and_the_board_names_that_deploy(self):
        """macbook-pro, 2026-10-26 to 31: 3b12e8f approved and never deployed, 8651be6 started after its word and ended,
        stood as approved, not yet deployed (signal 2026-10-31-swancloud-ops-edced2f9/01)."""
        spent = [entry("ops.offer", 30, Head=S1, Base="none"), entry("ops.approve", 25, Head=S1), entry("ops.deploy", 12, Head=S2, Base=S1, Phase="start"),
                 entry("ops.deploy", 10, Head=S2, Phase="end", Outcome="done")]
        assert view("wldn-ops", entries=spent) == ["wldn operations  0 deploys wait on the user's word  0 deploys running  0 operations waiting"]
        assert lane(board.board_text(data(entries=spent)), "Operation")[-1].startswith(
            f"  mac-studio  deploy {S1[:7]} from nothing deployed  approved, then the deploy of {S2[:7]} ended first  carrying")

    def test_the_planner_the_design_agent_main_level_ops_and_the_operator_have_a_view_and_no_other_agent(self):
        """No conductor's, team ops's or dispatcher's view (Decision 11 of the-team-machinery-leaves)."""
        v = board.agent_views(data())
        assert sorted(v["views"]) == ["wldn-design", "wldn-operator", "wldn-ops", "wldn-planner"]
        assert v["read_at"] == data()["read_at"] and v["stale_after_ms"] == board.STALE * 1000
        assert v["stale"] == [(f"crew: the board was last read at {board.local(data()['read_at'])}, too long ago to show; crew's follower on mac-studio "
                               "has not refreshed it since", "dim")]
        # a day with it: a restart, or a follower that stopped, can leave it days old
        assert re.fullmatch(r"crew: the board was last read at [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}, .*", v["stale"][0][0])

    @pytest.mark.parametrize("stages, shown", [(["queued", "waiting", "ready"], "○○○"), (["amended", "construct", "planned"], "◔◔◔"),
                                               (["code", "verify"], "◑◕"), (["merged", "landed"], "●●"), (["unknown"], "?")])
    def test_a_units_pip_fills_as_its_stage_goes_and_one_crew_cannot_read_is_a_question(self, stages, shown):
        assert board.pips([{"stage": s} for s in stages]) == shown

    def test_the_rail_tabs_refresh_writes_the_views_whole_beside_the_frame(self, tmp_path, monkeypatch):
        monkeypatch.setattr(board, "FRAMES", tmp_path)
        board.write_frame("wldn", board.agent_views(data()), board.agents_path("wldn"))
        assert sorted(p.name for p in tmp_path.iterdir()) == ["wldn.agents.json"]
        assert board.read_frame("wldn") is None

    def test_the_views_file_holds_every_key_crews_mod_reads_in_the_form_it_draws(self):
        """code.8: plugin/hooks/status.js reads exactly these keys from the views file, finds its agent's view by name,
        and draws each line as (text, style) segments, bold, dim or plain; a change to the views' shape, or a key the
        mod reads that they lack, fails here."""
        mod = (pathlib.Path(board.__file__).resolve().parent.parent / "hooks/status.js").read_text()
        v = json.loads(json.dumps(board.agent_views(data(props=WAITS, signals=SIGS))))
        assert set(re.findall(r"live\.frame\.(\w+)", mod)) == set(v) == {"read_at", "stale_after_ms", "stale", "views", "cards"}
        assert "live.frame.views[live.agent]" in mod and "(live.frame.cards || {})[live.agent]" in mod and "Date.parse(live.frame.read_at)" in mod
        assert re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", v["read_at"]) and isinstance(v["stale_after_ms"], int)
        assert "home + '/.cache/crew/board/' + label + '.agents.json'" in mod and board.agents_path("wldn").parts[-4:] == (".cache", "crew", "board", "wldn.agents.json")
        assert re.findall(r"style === '(\w+)'", mod) == ["bold"] and "dimColor: true" in mod
        assert v["cards"] == {} and json.loads(json.dumps(board.agent_views(data(cards=[QUESTION]))))["cards"]["wldn-ops"]
        answered = dict(QUESTION, answered=dict(at=NOW - datetime.timedelta(minutes=5), answer="picked a", heads=None))  # an answered card's line
        lines = [l for lines in json.loads(json.dumps(board.agent_views(data(cards=[answered]))))["cards"].values() for l in lines]
        assert any("answered 5m ago, yours to act on" in t for l in lines for t, _ in l)
        standing = board.agent_views(data(placed=TestSubmissions.SUBMITTED))["views"]  # a submission the runner carries, drawn as plain segments
        lines += [v["stale"]] + [l for lines in v["views"].values() for l in lines] + [l for lines in board.agent_views(data(cards=[QUESTION]))["cards"].values() for l in lines]
        lines += [l for lines in standing.values() for l in lines]
        assert any("submitted #413" in t for l in standing["wldn-planner"] for t, _ in l)
        # a role's run's view, under its run's name, its lines of the same form (Decision 15 of roles-run-as-flume-kinds)
        ran = json.loads(json.dumps(board.agent_views(data(roles=roles({"planner": "wldn", "reviewer": "wldn"},
                                                                       [an_ask(1, 9), an_ask(2, 4)], [a_turn(1, ["ask/1"])])))))["views"]
        assert ran["wldn-planner"][0][0] == ["wldn-planner run", "bold"] and ran["wldn-reviewer"]
        lines += [l for lines in ran.values() for l in lines]
        assert all(isinstance(l, list) and all(isinstance(t, str) and len(seg) == 2 and style in (None, "bold", "dim") for seg in l for t, style in [seg])
                   for l in lines)


QUESTION = dict(label="wldn", card="req_q1", key=None, on="agent/wldn-ops", by="wldn-ops", host="mac-studio",
                at=NOW - datetime.timedelta(minutes=14))


# Merges and a landing standing in sluice's queue, as the gather reads them on the host its work runs on
# (gather.submissions_of).
STANDING_SUBS = [{"id": 41, "branch": "bolt/tenant-environments", "head": "a" * 40, "state": "testing", "worktree": "unit/a", "pull_head": None,
                  "submitted": ago(30), "started": ago(20)},
                 {"id": 43, "branch": "bolt/tenant-environments", "head": "c" * 40, "state": "queued", "worktree": "fix/tenant-environments/edge",
                  "pull_head": None, "submitted": ago(25), "started": None},
                 {"id": 355, "branch": "main", "head": "d" * 40, "state": "queued", "worktree": "pull/198", "pull_head": "bolt/tenant-environments",
                  "submitted": ago(10), "started": None}]


def queued(subs=(), error=None):
    sv = kits()
    sv[BOX]["kits"]["/kit/main"].update({"submissions": list(subs)} if error is None else {"submissions": None, "submissions_error": error})
    return sv


class TestSubmissions:
    """crew-board "Construction shows each bolt in flight as a ledger, with no server for a started bolt's work": each
    piece's submission on its line as the runner carries Flume's status of its place, and the bolt's landing on its
    head line as the run record holds it, in the lane and in the bands, nothing of sluice's queue read (crew record
    0056 points 1 and 4; code.8)."""
    SUBMITTED = dict(PLACED, a=("submitted", None))

    def test_a_submission_the_runner_carries_is_on_its_line_in_the_lane_and_the_planners_band(self):
        """crew-board "A submission moved": a's place submitted as #413, under test, as the box's runner carries it."""
        assert lane(board.board_text(data(placed=self.SUBMITTED)), "Construction")[1:3] == [
            "    a  submitted #413", "    b  construct"]
        assert ledger("wldn-planner", "tenant-environments", placed=self.SUBMITTED)[1:3] == [
            "    ◕  a  submitted #413", "    ◔  b  construct"]

    def test_a_landing_the_run_record_holds_queued_is_on_the_bolts_head_line_in_the_lane_and_the_bands(self):
        """bolt-teams "A bolt's landing queued on main": the lane, the planner's band and main-level ops's, with its number."""
        logs = TestViews.QUEUED
        assert lane(board.board_text(data(logs=logs)), "Construction")[0] == (
            f"  switchboard-kit tenant-environments  on chuck-herdr-alpha  in Flume stream wldn  landing queued as #412  {TE_TIME}")
        assert ledger("wldn-planner", "tenant-environments", logs=logs)[0] == (
            f"  switchboard-kit  ◑◔  tenant-environments  in Flume stream wldn  landing queued as #412  0 of 2 merged  {TE_TIME}")
        assert "  switchboard-kit  tenant-environments  landing queued as #412" in view("wldn-ops", logs=logs)

    def test_a_landing_on_ops_landing_row_is_named_with_its_bolt(self, monkeypatch):
        two = plan.Plan(plan_text(bolts=[("doctor-rows", "switchboard-kit", True)], units=[("rows-one", "switchboard-kit", "doctor-rows", [])]))
        monkeypatch.setitem(globals(), "the_plan", lambda: two)
        monkeypatch.setitem(globals(), "PLACED", {"rows-one": ("landed", None)})
        sv = kits()
        sv[BOX]["kits"]["/kit/main"]["bolts"]["doctor-rows"] = {"head": LANDED, "head_at": ago(30), "changes": ["rows-one"],
                                                                "archived": ["rows-one"]}
        logs = [dict(entry("bolt.submit", 10, Outcome="queued", Submission="355", Head=LANDED), On=["bolt/doctor-rows"])]
        card = dict(label="wldn", card="req_k1", key="land/switchboard-kit", by="wldn-ops", host="mac-studio", at=NOW)
        ops_ = view("wldn-ops", sv=sv, cards=[card], logs=logs)
        assert "✓ land/switchboard-kit  doctor-rows landing queued as #355  waits to land  card open, asked by wldn-ops" in ops_
        assert not [l for l in ops_ if l.startswith("  switchboard-kit  doctor-rows")]

    def test_nothing_standing_draws_nothing_new(self):
        assert view("wldn-planner", sv=queued([])) == view("wldn-planner")


class TestTime:
    """crew-board "A held bolt's head line shows its age and who held its time" (plan.20): each holder now as the lane,
    the JSON and the bands draw tenant-environments' head line, started 200 minutes before the board was read; its age
    runs from the run record's entry that made its branch (Decision 11 of the-team-machinery-leaves)."""

    @staticmethod
    def head(**kw):
        return lane(board.board_text(data(**kw)), "Construction")[0]

    def test_the_team_while_a_stage_runs(self):
        logs = [dict(Act="stage.start", On=["stage/a/code", "unit/a", "agent/swb-1-unit-1"], At=ago(50))]
        said = f"3h 20m: team 50m, nobody 2h 30m; team since {hm(50)}, code on a"
        assert self.head(logs=logs).endswith(f"on {BOX}  in Flume stream wldn  {said}")
        assert f"  switchboard-kit  ◑◔  tenant-environments  in Flume stream wldn  0 of 2 merged  {said}" in view("wldn-planner", logs=logs)
        assert f"  switchboard-kit  ◑◔  tenant-environments  in Flume stream wldn  0 of 2 merged  {said}" in view("wldn-operator", logs=logs)

    def test_a_submission_the_runner_reports_places_no_minute(self):
        """crew-board "A submission the runner reports": a's place submitted as #413 under test, as the box's runner
        carries it, with no stage, card or hold of the bolt's: none of its minutes are the kit's or the team's, and
        nobody holds it."""
        assert self.head(placed=TestSubmissions.SUBMITTED).endswith(TE_TIME)

    def test_the_user_while_a_card_of_the_bolts_is_open(self):
        logs = [dict(Act="card.post", On=["bolt/tenant-environments"], Card="req_l", Key="land/tenant-environments", By="wldn-ops", At=ago(40))]
        assert self.head(logs=logs).endswith(f"3h 20m: user 40m, nobody 2h 40m; user since {hm(40)}, land/tenant-environments")

    def test_a_hold_while_the_host_its_work_runs_on_is_held(self):
        logs = [dict(Act="host.hold", On=[f"host/{BOX}"], By="chuck", At=ago(15))]
        assert self.head(logs=logs).endswith(f"3h 20m: hold 15m, nobody 3h 05m; held since {hm(15)}: its host {BOX} is held by chuck")

    def test_nobody_however_long_and_never_stalled(self):
        """teams.23 retires with the-team-machinery-leaves: nobody's minutes are said as nobody's, never a stall."""
        assert self.head().endswith(TE_TIME) and "stalled" not in board.board_text(data())
        logs = [dict(Act="stage.start", On=["stage/a/code", "unit/a", "agent/swb-1-unit-1"], At=ago(50)),
                dict(Act="stage.end", On=["stage/a/code", "unit/a", "agent/swb-1-unit-1"], At=ago(2))]
        assert self.head(logs=logs).endswith(f"3h 20m: team 48m, nobody 2h 32m; nobody since {hm(2)}")

    def test_a_row_reads_nothing_of_sluices_queue(self):
        """crew-board "A row drawn from the overview": the kit's read holding #41 under test since twenty minutes ago and
        #40 decided, as an older gather gave them, places no minute: the head line is as with none."""
        sv = queued(STANDING_SUBS)
        sv[BOX]["kits"]["/kit/main"]["decided"] = [{"id": 40, "bolt": "tenant-environments", "branch": "bolt/tenant-environments", "worktree": "unit/a",
                                                    "pull_head": None, "submitted": ago(30), "started": None, "decided": ago(18), "event": "landed"}]
        assert self.head(sv=sv).endswith(f"on {BOX}  in Flume stream wldn  {TE_TIME}")
        assert data(sv=sv)["drives"][0]["construction"][0]["time"]["shares"] == data()["drives"][0]["construction"][0]["time"]["shares"]

    def test_an_age_that_cant_be_told_says_why_and_shows_no_share(self):
        unread = {"wldn": {"wldn/main of WilldanGroup/crew-state": "fetch failed"}}
        said = "its age can't be told: wldn/main of WilldanGroup/crew-state could not be read (fetch failed)"
        assert self.head(unread=unread).endswith(said)
        assert ledger("wldn-planner", "tenant-environments", unread=unread)[0].endswith(f"0 of 2 merged  {said}")

    def test_the_json_carries_the_age_the_shares_and_the_holder_now(self):
        logs = [dict(Act="stage.start", On=["stage/a/code", "unit/a", "agent/swb-1-unit-1"], At=ago(50))]
        te = data(logs=logs)["drives"][0]["construction"][0]
        assert te["time"] == {"age": 200, "shares": {"team": 50, "kit": 0, "team_or_kit": 0, "user": 0, "hold": 0, "nobody": 150},
                              "now": {"holder": "team", "what": "code on a", "since": ago(50)},
                              "said": f"3h 20m: team 50m, nobody 2h 30m; team since {hm(50)}, code on a"}
        assert json.loads(json.dumps(te))["time"] == te["time"]


class TestCards:
    def test_each_agent_sees_its_open_cards_its_questions_among_them_above_its_view(self):
        """code.8: the band crew's mod draws above an agent's prompt opens with the agent's open cards, oldest first."""
        p2 = dict(label="wldn", card="req_p2", key="proposal/2", by="wldn-planner", host="mac-studio", at=NOW - datetime.timedelta(hours=2, minutes=5))
        stray = dict(QUESTION, card="req_x", key="ask/wldn-reviewer/x", by="wldn-reviewer")
        v = board.agent_views(data(props=WAITS, cards=[p2, QUESTION, stray]))
        drawn = {a: ["".join(t for t, _ in l) for l in lines] for a, lines in v["cards"].items()}
        assert drawn == {"wldn-planner": ["  your card  proposal/2  req_p2  open 2h 05m"], "wldn-ops": ["  your question  req_q1  open 14m"]}
        assert ("req_q1", "dim") in v["cards"]["wldn-ops"][0]

    def test_the_planners_answered_proposal_card_says_it_was_answered_and_is_the_planners_to_act_on(self):
        """crew-board "The planner's answered proposal card": proposal/57's card, wldn-planner's, answered five minutes
        ago; the board's card carries when and what (design Decision 3)."""
        p57 = dict(label="wldn", card="req_57", key="proposal/57", by="wldn-planner", host="mac-studio", at=NOW - datetime.timedelta(hours=1),
                   answered=dict(at=NOW - datetime.timedelta(minutes=5), answer="approved", heads=None))
        v = board.agent_views(data(cards=[p57]))
        assert ["".join(t for t, _ in l) for l in v["cards"]["wldn-planner"]] == ["  your card  proposal/57  req_57  answered 5m ago, yours to act on"]
        (c,) = data(cards=[p57])["drives"][0]["cards"]
        assert (c["answered"], c["answer"]) == (board.iso(NOW - datetime.timedelta(minutes=5)), "approved")
        (c,) = data(cards=[dict(p57, answered=None)])["drives"][0]["cards"]
        assert (c["answered"], c["answer"]) == (None, None)

    def test_the_board_lists_each_open_card_with_what_it_is(self):
        rec = dict(QUESTION, card="req_r1", key="record/atlas-kit/0021", by="wldn-design")
        assert [(c["card"], c["kind"], c["by"]) for c in data(cards=[rec, QUESTION])["drives"][0]["cards"]] == [
            ("req_q1", "question", "wldn-ops"), ("req_r1", "record", "wldn-design")]

    def test_the_design_agent_sees_each_record_proposed_and_not_yet_accepted_or_rejected_with_its_card(self, monkeypatch):
        """The design band reads crew record's record.<status> entries: 0021 proposed and its card open, 0022 settled
        in the pane, 0023 proposed and then accepted, so gone."""
        monkeypatch.setattr(board, "SHOWN", 0)
        logs = [dict(Act="record.proposed", On=["record/atlas-kit/0021"], At=ago(60)), dict(Act="record.proposed", On=["record/atlas-kit/0022"], At=ago(50),
                                                                                            State="settled in the pane"),
                dict(Act="record.proposed", On=["record/atlas-kit/0023"], At=ago(40)), dict(Act="record.accepted", On=["record/atlas-kit/0023"], At=ago(30))]
        rec = dict(QUESTION, card="req_r1", key="record/atlas-kit/0021", by="wldn-design")
        assert [(r["kit"], r["number"], r["settled"], r["card"] and r["card"]["card"]) for r in data(logs=logs, cards=[rec])["drives"][0]["records"]] == [
            ("atlas-kit", "0021", False, "req_r1"), ("atlas-kit", "0022", True, None)]
        assert view("wldn-design", logs=logs, cards=[rec]) == [
            "wldn inception  0 signals not moved  2 records proposed  1 exploration",
            f"✓ atlas-kit record 0021  proposed {board.local(ago(60))}  card open, asked by wldn-design",
            f"  atlas-kit record 0022  proposed {board.local(ago(50))}  settled in the pane", "  and 1 more exploration"]
        assert board.agent_views(data(logs=logs, cards=[rec]))["cards"]["wldn-design"]


def test_a_chore_is_marked_in_a_ledger_a_planned_bolt_and_the_queue(monkeypatch):
    """A chore stands among the units in build order, its kind in the JSON and `chore` before its stage in the text
    (plan.11); a started bolt's chore at the stage its host's runner carries its place at, bump submitted."""
    import sys
    text = plan_text(bolts=[("apex-zones", "switchboard-kit", None), ("tenant-environments", "switchboard-kit", True)],
                     units=[("pin", "switchboard-kit", "apex-zones", [], "chore"), ("a", "switchboard-kit", "tenant-environments", []),
                            ("bump", "switchboard-kit", "tenant-environments", [], "chore"), ("tidy", "switchboard-kit", None, [], "chore")])
    monkeypatch.setattr(sys.modules[__name__], "the_plan", lambda: plan.Plan(text))
    monkeypatch.setitem(globals(), "PLACED", dict(PLACED, bump=("submitted", None)))
    sv = kits()
    d = data(sv=sv)
    ledger = next(b for b in d["drives"][0]["construction"] if b["bolt"] == "tenant-environments")
    assert [(u["unit"], u["kind"], u["stage"]) for u in ledger["units"]] == [("a", "unit", "code"), ("bump", "chore", "submitted")]
    out = board.board_text(d)
    assert "    bump  chore submitted #413" in lane(out, "Construction")
    assert lane(out, "Bolt plan") == ["  switchboard-kit apex-zones  Goal of apex-zones.", "    pin  chore ready", "  switchboard-kit tidy  chore queued"]
    # The planner's view, the mod's band, draws the chore in its ledger as the board does (code.8).
    mine = view("wldn-planner", sv=sv)
    assert mine[1:4] == [f"  switchboard-kit  ◑◕  tenant-environments  in Flume stream wldn  0 of 2 merged  {TE_TIME}", "    ◑  a  code 1/2", "    ◕  bump  chore submitted #413"]


class TestStarted:
    """crew-board "Construction shows a started bolt from the runner's records" and "The planner's and ops's bands show
    what places wait on them for" (code.8): x started, its work taken by deneb's runner in stream madswan, a launched as
    request 1 and b after a as request 2; y planned and not started; deneb's runner as each case gives it."""

    @pytest.fixture(autouse=True)
    def writer(self, monkeypatch):
        monkeypatch.setenv("CREW_AGENT", "madswan-dispatch-deneb")

    def data(self, runners, extra=(), kit=None, bolts=None):
        """The board of madswan, its runner as given and extra requests appended to those the start wrote; kit what deneb's
        read of crew holds beside, and bolts each bolt's facts there."""
        from facts import crew_read, launched, madswan_fleet
        fleet = madswan_fleet()
        fleet["drives"]["madswan"].update(machine="deneb", blueprints=["afterthought/blueprints"], state="afterthought/crew-state")
        p, requests = launched(["x"], work=[("a", "x", [], "unit", []), ("b", "x", ["a"], "unit", []), ("y1", "y", [], "unit", [])],
                               fleet=fleet, planned=["y"])
        runs = {"madswan": (requests + [plan.Rec("Request", list(f.items())) for f in extra], runners)}
        found, sv = [("madswan", "afterthought/crew-state", "tip0", p)], crew_read(bolts=bolts or {"x": {}, "y": {}})
        sv["deneb"]["kits"]["/crew/main"].update(kit or {})
        r = dict(found=found, sv=sv, props=[], cards=[], unread={}, errors={}, landings=[], signals={"madswan": ([], {})}, kits=kits_of(found),
                 ops={"madswan": []}, logs={"madswan": []}, runs=runs, rows=plan.rail_rows(fleet, found, sv, [], {}, None, runs))
        return board.board_data(fleet, ["madswan"], r, NOW)

    def views(self, runners, extra=()):
        return {a: ["".join(s for s, _ in line) for line in v] for a, v in board.agent_views(self.data(runners, extra))["views"].items()}

    def test_a_started_bolts_ledger(self):
        """crew-board "A started bolt's ledger": x on deneb in stream madswan, a at code, b waiting on a, and no slot line;
        the board's JSON gives the ledger its host and stream, and lists no teams."""
        from facts import ran
        d = self.data(ran({1: "code"}, held=[2]))
        assert lane(board.board_text(d), "Construction") == [
            "  crew x  on deneb  in Flume stream madswan  its age can't be told: the run record of the last 60 days holds no start of it",
            "    a  code 6/26", "    b  waiting  on a"]
        x = next(b for b in d["drives"][0]["construction"] if b["bolt"] == "x")
        assert (x["host"], x["stream"]) == ("deneb", "madswan") and "teams" not in d["drives"][0]
        assert [b["bolt"] for b in d["drives"][0]["bolt_plan"]["planned"]] == ["y"]

    def test_a_started_bolts_ledger_shows_no_server(self, monkeypatch):
        """crew-board "A started bolt's work shows no server": a server running in x's own worktree, as a bolt given before
        record 0026 had one, is drawn for no part of x, its places being Flume's until the runner reports a place's
        addresses."""
        from facts import ran
        monkeypatch.setattr(crew, "this_host", lambda: "deneb")
        site = {"here": "https://bolt--crew.local"}
        kit = dict(sites={"/crew/bolts/x": site}, routes=[{"name": "bolt--crew", "url": "https://bolt--crew.local"}])
        d = self.data(ran({1: "code"}, held=[2]), kit=kit, bolts={"x": {"worktree": "/crew/bolts/x"}})
        x = next(b for b in d["drives"][0]["construction"] if b["bolt"] == "x")
        assert x["url"] is None and {u["url"] for u in x["units"]} == {None}
        assert "server" not in "\n".join(lane(board.board_text(d), "Construction")[:3])

    def test_a_launch_the_runner_holds_with_no_after_is_on_its_runners_host_with_its_words(self):
        """drive-state "A place not carried yet" and bolt-plan "A claimed launch is not held for After work", in the
        board and the planner's band (code.8): deneb's runner holds a's launch, which names no After, with its claim's
        words, has carried no place of x's work and reports no repositories; the ledger names deneb, a's line says it is
        launching with the runner's words, and b, after a, waits on a."""
        from facts import ran
        claim = "claimed by deneb's runner; launching once no other runner has claimed it"
        d = self.data(ran(held={1: claim, 2: None}, keeps=None))
        x = next(b for b in d["drives"][0]["construction"] if b["bolt"] == "x")
        assert (x["host"], x["stream"]) == ("deneb", None)
        assert lane(board.board_text(d), "Construction")[1:] == [f"    a  launching  held by the runner: {claim}", "    b  waiting  on a"]
        assert lane(board.board_text(d), "Construction")[0].startswith("  crew x  on deneb  ")
        v = self.views(ran(held={1: claim, 2: None}, keeps=None))["madswan-planner"]
        assert any(f"a  launching  held by the runner: {claim}" in l for l in v) and not any("After work" in l for l in v)

    def test_a_question_in_the_planners_band(self):
        """crew-board "A question in the planner's band": a's construct stopped short asking."""
        from facts import ran
        v = self.views(ran({1: "stopped-short"}))["madswan-planner"]
        assert v[0].endswith("1 place waits on an answer")
        assert [l for l in v if "asks at" in l] == [next(l for l in v if l.startswith("    ◑  a  needs  asks at code: Head 118ec46 is ready for your flume:live run"))]

    def test_a_place_past_its_bound_in_the_planners_band(self):
        """crew-board "A place past its bound in the planner's band": the runner carries flume 0.17.0's status of a's
        place waiting on its caller to retry code past its bound, its verify delivered (tests/py/flume-0.17.0/
        past-bound.json); the planner's view counts it among the places waiting on an answer and lists it waiting on
        its caller at code with Flume's words, as the board's ledger does in the Construction lane, never at verify."""
        from facts import ran
        said = "waits on its caller at code: the submission conflicted with its base: [sluice] #24 conflicts on bolt/sluice-runs-one-host-process"
        v = self.views(ran({1: "flume-0.17.0/past-bound"}))["madswan-planner"]
        assert v[0].endswith("1 place waits on an answer")
        assert [l for l in v if "waits on its caller" in l] == [next(l for l in v if l.startswith(f"    ◑  a  waits  {said}"))]
        assert any(l.startswith(f"    a  waits  {said}") for l in lane(board.board_text(self.data(ran({1: "flume-0.17.0/past-bound"}))), "Construction"))
        assert not any("verify" in l for l in v if "  a  " in l)

    def test_a_fix_of_main_in_ops_band(self):
        """crew-board "A fix of main in ops's band": main--a-test-reads-its-fixture is in code."""
        from facts import ran
        fix = {"Request": "3", "Act": "launch", "Host": "deneb", "Work": "fix/main/crew/a-test-reads-its-fixture", "Repo": "afterthought/crew",
               "Kind": "fix", "Name": "main--a-test-reads-its-fixture", "Base": "main", "Hold": "submission"}
        v = self.views(ran({3: "code"}), extra=[fix])["madswan-ops"]
        assert v[0].endswith("1 fix in flight") and v[1] == "  crew  fix main--a-test-reads-its-fixture  code 6/26  on deneb"

    def test_a_take_main_fix_in_flight_is_in_ops_band_and_on_its_ledger(self):
        from facts import ran
        fix = {"Request": "3", "Act": "launch", "Host": "deneb", "Work": "fix/x/take-main-4d3d9be", "Repo": "afterthought/crew", "Kind": "fix",
               "Name": "x--take-main-4d3d9be", "Base": "bolt/x"}
        d = self.data(ran({3: "code"}), extra=[fix])
        assert "    fix/x/take-main-4d3d9be  fix code 6/26" in lane(board.board_text(d), "Construction")
        assert "  crew  fix x--take-main-4d3d9be  code 6/26  on deneb" in self.views(ran({3: "code"}), extra=[fix])["madswan-ops"]

    def test_a_landing_fix_in_ops_band(self):
        """crew-board "A landing fix in ops's band" (crews-bolt-kind-names-its-landing-fix, Decision 6): x's base place
        lists y-1 live for a conflict; ops's band lists it after the take-main fixes as a landing fix taking main in, and
        its head line counts one fix in flight."""
        from facts import ran
        v = self.views(ran({1: "code", 3: "flume-0.19.0/bolt-conflict-fixing"}))["madswan-ops"]
        assert v[0].endswith("1 fix in flight")
        assert "  crew  fix y-1  landing fix  Take main into the bolt: Flume's landing fix y-1 merges main at 9f1c2ab  on deneb" in v, v

    def test_a_runner_crew_cant_read_is_named_for_attention(self):
        import runner
        d = self.data({"deneb": runner.host_read("madswan", "deneb", "5e1f0c2a" + "0" * 32, {}, {"runner.rec": "recfix refused it"})})
        assert {"what": "runner", "name": "deneb's runner", "why": "deneb's runner can't be read: madswan/runner/deneb at 5e1f0c2: "
                "recfix refused it"} in d["drives"][0]["attention"]
        assert {"what": "runner", "name": "madswan's runners", "why": "no runner answers for madswan: its state repository holds no "
                "madswan/runner/<host>"} in self.data({})["drives"][0]["attention"]
        assert {u["stage"] for b in d["drives"][0]["construction"] if b["bolt"] == "x" for u in b["units"]} == {"unknown"}

    def test_a_crossed_pieces_pip_is_the_stage_it_waits_at(self):
        assert board.pips([{"stage": "needs", "flume": {"of": "code"}}, {"stage": "submitted"}, {"stage": "launching"}, {"stage": "refused"}]) == "◑◕○?"


# A role's run on wldn's main level's host, as the runner carries it (runner.RUNS): its place and Flume's status of it.
RUN = "/home/u/.local/state/flume/places/crew-{role}--wldn"


def run_status(role, waiting_on=None, words=None):
    """flume status --json of a role's run in its one stage, turn, as the runner carries it."""
    stage = {"name": "turn", "state": "ended" if waiting_on else "running", "end": {"words": words} if words else None}
    return json.dumps({"status": {"places": [{"place": RUN.format(role=role), "phase": "live", "current": "turn", "stages": [stage],
                                              "waiting_on": waiting_on, "stalled": False}]}})


def runner_reading(runs, host="mac-studio"):
    """The main level's host's runner as plan.runners reads it, its places.rec holding each role's run, {role: status}."""
    import runner
    recs = "".join(f"\nAddress: wldn/{r}\nPlace: {RUN.format(role=r)}\nAt: {ago(10)}\nStatus: {st}\n" for r, st in runs.items())
    files = {"runner.rec": plan.Plan(runner.RUNNER + f"\nHost: {host}\nVersion: 0.1.0\nSince: {ago(60)}\n"),
             "answers.rec": plan.Plan(runner.ANSWERS), "places.rec": plan.Plan(runner.PLACES + "\n" + runner.RUNS + recs)}
    return runner.host_read("wldn", host, "5e1f0c2a" + "0" * 32, files, {})


def asks_rec(asks_, turns):
    """asks.rec with these asks and turns, each a dict of its fields, a Took a list."""
    def rec(f):
        return "".join(f"{k}: {x}\n" for k, v in f.items() for x in (v if isinstance(v, list) else [v])) + "\n"
    return "%rec: Ask\n\n" + "".join(rec(a) for a in asks_) + "%rec: Turn\n\n" + "".join(rec(t) for t in turns)


def an_ask(n, minutes, role="planner", what="tell", frm="wldn-design", names=None):
    return dict(Id=str(n), Role=role, From=frm, What=what, **({"Names": names} if names else {}), At=ago(minutes))


def a_turn(n, took, role="planner", ended=False, superseded=None):
    t = dict(Turn=str(n), Role=role, Run=f"wldn-{role}", Place=f"crew-{role}--wldn", Host="mac-studio", Took=list(took), Began=ago(6))
    t.update(dict(Ended=ago(1), Said="done") if ended else {})
    t.update(dict(Superseded=str(superseded)) if superseded else {})
    return t


def roles(kinds, asks_=(), turns=(), runs=None, reading=None):
    """What the board read of wldn's roles that run as their kinds (board.roles_read)."""
    return {"kinds": kinds, "asks": asks_rec(list(asks_), list(turns)) if asks_ or turns else None, "host": "mac-studio",
            "reading": reading if reading is not None else runner_reading(runs or {})}


PLANNER = {"planner": "wldn"}
# What the fixture's board names for attention with no role's run in it: board-done, every unit of it landed.
ATTENDED = ["! bolt board-done: every unit has landed on main, and the bolt is still in the plan"]


def runs_named(r):
    """What the attention line names of the roles' runs in the board read with roles r."""
    return [a for a in data(roles=r)["drives"][0]["attention"] if a["what"] == "run"]


class TestRuns:
    """crew-board "A role that runs as its kind has its view" and "The attention line names a role's run that waits"
    (Decision 15 of roles-run-as-flume-kinds, code.8): wldn's planner, and in some cases its design agent and reviewer,
    run as their kinds in stream wldn, their runs on mac-studio, wldn's main level's host."""

    def test_a_run_with_an_ask_waiting(self):
        """A run with an ask waiting: the planner's run took two asks, and a third has waited four minutes."""
        r = roles(PLANNER, [an_ask(1, 9), an_ask(2, 7, what="landed", frm="crew", names="bolt/apex-zones"), an_ask(3, 4)],
                  [a_turn(1, ["ask/1", "ask/2"])], {"planner": run_status("planner")})
        mine = view("wldn-planner", roles=r)
        assert mine[:3] == ["wldn-planner run  in stream wldn  turn 1 took 2  1 ask waits, for 4m",
                            "  ask 1  tell from wldn-design", "  ask 2  landed from crew  on bolt/apex-zones"]
        # the planner's own view of the board follows its run's lines
        assert mine[3:] == view("wldn-planner")
        styled = board.agent_views(data(roles=r))["views"]["wldn-planner"][0]
        assert styled[0] == ("wldn-planner run", "bold")

    def test_nothing_waiting(self):
        """Nothing waiting: the planner's run took one ask and nothing else waits."""
        r = roles(PLANNER, [an_ask(1, 9)], [a_turn(1, ["ask/1"])])
        assert view("wldn-planner", roles=r)[:2] == ["wldn-planner run  in stream wldn  turn 1 took 1  nothing waits",
                                                      "  ask 1  tell from wldn-design"]

    def test_asks_that_wait_count_from_the_oldest_and_an_ended_turn_took_its_own(self):
        r = roles(PLANNER, [an_ask(1, 30), an_ask(2, 125), an_ask(3, 12)], [a_turn(1, ["ask/1"], ended=True)])
        assert view("wldn-planner", roles=r)[0] == "wldn-planner run  in stream wldn  turn 1 took 1, ended  2 asks wait, the oldest for 2h 05m"

    def test_a_run_with_no_turn_yet_and_the_reviewer_whose_run_has_no_other_view(self):
        r = roles({"planner": "wldn", "reviewer": "wldn"}, [an_ask(1, 3, role="reviewer", what="batch", frm="crew", names="batch/4")])
        v = {a: ["".join(t for t, _ in l) for l in ls] for a, ls in board.agent_views(data(roles=r))["views"].items()}
        assert v["wldn-reviewer"] == ["wldn-reviewer run  in stream wldn  no turn taken  1 ask waits, for 3m"]
        assert v["wldn-planner"][0] == "wldn-planner run  in stream wldn  no turn taken  nothing waits"
        # a role that stands keeps its view as it was, and no run's lines
        assert v["wldn-design"] == view("wldn-design") and v["wldn-ops"] == view("wldn-ops")

    def test_a_turns_ends_are_counted_on_its_head_line_and_listed_nowhere(self):
        """Ends counted: the planner's run took one ask and nine ends of three places, Flume holding them for wldn/planner
        (crew-board "A role that runs as its kind has its view"; design Decision 7 of crews-role-runs-confirm-what-they-collect)."""
        ends = [f"end/{n}/change--u{n}/0a1b2c3d/stage/{s}/1/delivered" for n in (12, 14, 15) for s in ("construct", "code", "verify")]
        r = roles(PLANNER, [an_ask(1, 9)], [a_turn(1, ["ask/1"] + ends)])
        mine = view("wldn-planner", roles=r)
        assert mine[:2] == ["wldn-planner run  in stream wldn  turn 1 took 1 and 9 ends  nothing waits", "  ask 1  tell from wldn-design"]
        assert mine[2:] == view("wldn-planner") and not any("end/" in l or "stage/" in l for l in mine)
        one = roles(PLANNER, [an_ask(1, 9)], [a_turn(1, ["ask/1", ends[0]], ended=True)])
        assert view("wldn-planner", roles=one)[0] == "wldn-planner run  in stream wldn  turn 1 took 1 and 1 end, ended  nothing waits"

    def test_a_superseded_turn_is_not_the_runs_and_its_asks_wait_again_until_the_next_takes_them(self):
        lost = roles(PLANNER, [an_ask(1, 20)], [a_turn(1, ["ask/1"], superseded=2)])
        assert view("wldn-planner", roles=lost)[0] == "wldn-planner run  in stream wldn  no turn taken  1 ask waits, for 20m"
        again = roles(PLANNER, [an_ask(1, 20)], [a_turn(1, ["ask/1"], superseded=2), a_turn(2, ["ask/1"])])
        assert view("wldn-planner", roles=again)[0] == "wldn-planner run  in stream wldn  turn 2 took 1  nothing waits"

    def test_a_lost_run(self):
        """A lost run: the runner's records show wldn's design run lost; the attention line names it, its place and its
        host, and prints no command."""
        lost = {"act": "retry", "stage": "turn", "why": "lost", "since": 1793440000, "words": None}
        r = roles({"design": "wldn"}, runs={"design": run_status("design", lost)})
        said = f"wldn's design run: lost, its place {RUN.format(role='design')} on mac-studio"
        assert lane(board.board_text(data()), "attention") == ATTENDED
        assert lane(board.board_text(data(roles=r)), "attention") == ATTENDED + [f"! {said}"]
        assert f"! {said}" in view("wldn-operator", roles=r) and f"! {said}" in view("wldn-planner", roles=r)
        a, = runs_named(r)
        assert (a["what"], a["run"], a["how"], a["place"], a["host"]) == ("run", "wldn-design", "lost", RUN.format(role="design"), "mac-studio")
        for no in ("flume retry", "crew "):
            assert no not in said

    def test_a_run_that_stopped_short_is_named_with_its_words(self):
        short = {"act": "retry", "stage": "turn", "why": "answer", "since": 1793440000, "words": None}
        r = roles(PLANNER, runs={"planner": run_status("planner", short, "Which bolt does proposal 12's chore belong in?\nIt names two.")})
        assert lane(board.board_text(data(roles=r)), "attention") == ATTENDED + [
            f"! wldn's planner run: stopped short, its place {RUN.format(role='planner')} on mac-studio: Which bolt does proposal 12's chore belong in?"]
        assert runs_named(r)[0]["words"] == "Which bolt does proposal 12's chore belong in?\nIt names two."

    def test_a_run_that_waits_on_nothing_or_stands_live_is_not_named(self):
        held = {"act": "retry", "stage": "turn", "why": "on_hold", "since": 1793440000, "words": "held for the user"}
        r = roles({"planner": "wldn", "design": "wldn"}, runs={"planner": run_status("planner"), "design": run_status("design", held)})
        assert runs_named(r) == []

    def test_a_runner_crew_cant_read_names_the_runs_it_cant_tell(self):
        import runner
        r = roles({"design": "wldn", "planner": "wldn", "operator": "wldn"}, reading=runner.of_host({}, "wldn", "mac-studio"))
        assert lane(board.board_text(data(roles=r)), "attention") == ATTENDED + [
            "! wldn's design, planner and operator runs: crew can't tell how they stand: no runner answers on mac-studio: wldn/runner/mac-studio "
            "does not exist"]
        bad = runner_reading({"design": "{not json", "planner": run_status("planner")})
        assert lane(board.board_text(data(roles=roles({"design": "wldn", "planner": "wldn"}, reading=bad))), "attention")[-1].startswith(
            "! wldn's design run: crew can't tell how it stands: wldn/runner/mac-studio at 5e1f0c2: places.rec's status of the run of wldn/design is no JSON (")
        # the runs still have their views from asks.rec
        assert view("wldn-design", roles=r)[0] == "wldn-design run  in stream wldn  no turn taken  nothing waits"

    def test_the_board_reads_the_roles_beside_the_plan_and_a_drive_running_none_reads_nothing_more(self, monkeypatch):
        shown, ran = [], []
        monkeypatch.setattr(plan, "show", lambda repo, tip, path: shown.append((repo, tip, path)) or "%rec: Ask\n")
        monkeypatch.setattr(plan, "runners", lambda repo, label: ran.append((repo, label)) or {})
        fleet = dict(FLEET, drives={"wldn": dict(FLEET["drives"]["wldn"], runs=dict(crew_standing(), planner="on-demand")),
                                        "madswan": dict(FLEET["drives"]["wldn"], label="madswan", runs=crew_standing())})
        got = board.roles_read(fleet, [("wldn", "WilldanGroup/crew-state", "tip0", None), ("madswan", "WilldanGroup/crew-state", "tip1", None)])
        assert list(got) == ["wldn"] and got["wldn"]["kinds"] == {"planner": "wldn"} and got["wldn"]["asks"] == "%rec: Ask\n"
        assert got["wldn"]["reading"]["why"] == "no runner answers on mac-studio: wldn/runner/mac-studio does not exist"
        assert (shown, ran) == ([("WilldanGroup/crew-state", "tip0", "asks.rec")], [("WilldanGroup/crew-state", "wldn")])
        assert board.roles_read(fleet, [("wldn", "WilldanGroup/crew-state", None, None)])["wldn"]["asks"] is None


def crew_standing():
    return {r: "standing" for r in crew.KIND_ROLES}


class TestLandingsUnderAnotherName:
    """bolt-plan "Landings under another name", on the board: a drive whose run record holds a landing under
    agentplot/tailrace and, after it, a kit.rename of tailrace to timber names agentplot/tailrace as written, its kits
    read as the rail's read reads them (plan.kits_at; the landings a tip holding both entries gives, which test_kits'
    TestRunsRead proves); and the agents' views keep the keys crew's mod reads (code.8), so plugin/hooks/status.js is
    untouched."""
    LANDED = {"Id": "20261104T100000Z-1-deneb-1-1", "At": "2026-11-04T10:00:00Z", "Act": "bolt.land", "On": ["bolt/ledger"],
              "From": [], "Commit": [], "Repo": "agentplot/tailrace", "Head": "a" * 40}

    def board(self, monkeypatch, landings):
        monkeypatch.setattr(plan, "landings_at", lambda repo, tip: landings)
        r = read()
        r["kits"] = {l: plan.kits_at(repo, tip, p) for l, repo, tip, p in r["found"]}
        return board.board_data(FLEET, ["wldn"], r, NOW)

    def test_the_board_names_the_kit_as_its_landing_wrote_it_and_the_views_keep_their_keys(self, monkeypatch):
        landed, before = self.board(monkeypatch, [self.LANDED]), self.board(monkeypatch, [])
        assert landed["drives"][0]["kits"] == ["agentplot/tailrace", "breadboard-kit", "switchboard-kit"]
        assert before["drives"][0]["kits"] == ["breadboard-kit", "switchboard-kit"]
        v, was = json.loads(json.dumps(board.agent_views(landed))), json.loads(json.dumps(board.agent_views(before)))
        assert set(v) == set(was) == {"read_at", "stale_after_ms", "stale", "views", "cards"}
        assert set(v["views"]) == set(was["views"])


class TestALandingFromTheRunnersReport:
    """crew-board "Construction shows each bolt in flight as a ledger, with no server for a started bolt's work"
    (crew-lands-each-bolt-through-flumes-base-place, Decision 10): a bolt's head line, the rail and ops's band say its
    landing as the runner reports it beside what the run record holds (plan.landing_line, board.head_said,
    board.record_landing), under the ledger's key landing, which the mod's view reads with the rest (code.8)."""
    ASKED = {"state": "asked", "n": "57", "head": "a" * 40}

    def ledger(self, landing=None, record=None, state="waits"):
        return {"bolt": "y", "head": "a" * 40, "state": state, "landing": landing, "record": record}

    def test_a_land_asked_says_its_request(self):
        b = self.ledger({"outcome": "asked", "request": 57}, self.ASKED)
        assert board.head_said(b) == "landing asked, request 57" and board.record_landing(b) == "landing asked, request 57"

    def test_a_submission_under_test_says_flumes_entry(self):
        b = self.ledger({"outcome": "submitted", "request": 57, "entry": "412", "state": "under_test"}, self.ASKED)
        assert board.head_said(b) == "landing #412 under test" and board.record_landing(b) == "landing #412 under test"

    FAILED = ("landing refused at aaaaaaa, a check failed, the bolt's, open for work: check-full failed: tests:logic; it waits "
              "for a fix on the bolt, which ops starts with Flume's words, crew fix y <name> \"check-full failed: tests:logic\", "
              "and lands again once that fix moves its head")

    def test_a_failed_check_says_its_head_open_for_work_and_ops_fix_recorded_or_not(self):
        """crew-board "A landing rejected" and bolt-teams "A check that ran and failed": the head its land was posted at,
        the bolt open for work, and the fix ops starts with Flume's words, before the record holds it and after; nothing
        once a fix has moved the head."""
        refused = {"outcome": "refused", "request": 57, "why": "failed", "words": "check-full failed: tests:logic"}
        rejected = dict(self.ASKED, state="rejected", words="landing refused, a check failed: check-full failed: tests:logic")
        assert board.head_said(self.ledger(refused, self.ASKED)) == self.FAILED == board.head_said(self.ledger(refused, rejected))
        assert board.head_said(self.ledger(refused, dict(rejected, head="b" * 40))) == "waits to land"
        assert board.record_landing(self.ledger(refused, rejected)) == ""

    def test_a_conflict_says_it_takes_main_first_recorded_or_not(self):
        """crew-board "A landing refused in conflict" and bolt-teams "A conflict is the bolt's": in Flume's words, that it
        takes main first by the fix crew launches, naming no team."""
        conflict = {"outcome": "refused", "request": 57, "why": "conflict", "words": "bolt/y conflicts with main on README.md",
                    "files": ["README.md"], "main": "4d3d9be" + "0" * 33}
        want = ("takes main first: its landing at aaaaaaa was refused in conflict with main at 4d3d9be: bolt/y conflicts with main "
                "on README.md; crew launches the fix that takes main into it, ops starting nothing, and it lands again once that "
                "fix moves its head")
        rejected = dict(self.ASKED, state="rejected", words="landing refused in conflict with main at 4d3d9be: bolt/y conflicts")
        assert board.head_said(self.ledger(conflict, self.ASKED)) == want == board.head_said(self.ledger(conflict, rejected))

    def test_a_stop_says_its_head_and_a_landing_its_commit(self):
        """crew-board "A landing stopped": at the head its land was posted at, in the runner's words."""
        stopped = {"outcome": "stopped", "request": 57, "by": "runner", "words": "flume refused it: a place on bolt/y is live"}
        recorded = {"state": "stopped", "n": None, "head": "a" * 40, "words": "flume refused it: a place on bolt/y is live"}
        want = "landing stopped at aaaaaaa, nothing of the bolt's: flume refused it: a place on bolt/y is live"
        assert board.head_said(self.ledger(stopped, self.ASKED)) == want == board.head_said(self.ledger(stopped, recorded))
        assert board.head_said(self.ledger({"outcome": "landed", "commit": "c" * 40})) == "landed at ccccccc"
        assert board.record_landing(self.ledger(stopped, recorded)) == ""

    def test_landing_again_says_nothing_of_the_refusal_while_asked_and_both_once_in_the_queue(self):
        """crew-board "Landing again": asked again as request 63, nothing of the refusal at its old head; bolt-teams
        "Landing again": once the runner carries it as #415 under test, that it lands again after #412 was refused, and
        work joining it is refused naming both."""
        again = dict(self.ASKED, n="63", rejected=("412", "b" * 40))
        assert board.head_said(self.ledger({"outcome": "asked", "request": 63}, again)) == "landing asked, request 63"
        b = self.ledger({"outcome": "submitted", "request": 63, "entry": "415", "state": "under_test"}, again)
        assert board.head_said(b) == board.record_landing(b) == "landing again as #415, under test, after #412 was refused"
        assert plan.landing_hold(dict(again, entry="415"), "y", "unit a").startswith(
            "bolt y is landing again as #415 (request 63), after #412 was refused, so unit a does not join it until its outcome is read")
        assert plan.landing_hold(dict(self.ASKED, entry="412"), "y", "unit a").startswith(
            "bolt y has its landing #412 in the merge queue (request 57), so unit a does not join it")

    def test_a_bolt_started_before_bolts_were_base_places_says_it_lands_under_the_crew_that_started_it(self):
        legacy = {"outcome": "legacy", "words": "y was started before bolts were base places and lands under the crew that started it"}
        assert board.head_said(self.ledger(legacy)) == legacy["words"]

    def test_a_runner_that_cant_be_read_says_its_landing_cant_be_told_and_why(self):
        """crew-board "A runner that can't be read": the land posted as request 57, the runner that took the work unread."""
        unknown = {"outcome": "unknown", "why": "the runner on deneb that took request 41 can't be read: fetch failed"}
        assert board.head_said(self.ledger(unknown, self.ASKED)) == (
            "can't tell its landing: the runner on deneb that took request 41 can't be read: fetch failed")

    def test_with_nothing_asked_the_head_line_says_its_state(self):
        assert board.head_said(self.ledger({"outcome": "none"})) == "waits to land"
        assert board.head_said(self.ledger({"outcome": "unlaunched", "refused": True, "words": "not locked"}, state="active")) == ""
        assert board.record_landing(self.ledger({"outcome": "none"})) == ""

    def flume_19(self, name):
        from test_runner import TestLandingFix
        return TestLandingFix().of(f"flume-0.19.0/{name}")

    def test_a_head_line_names_the_landing_fix_taking_main_in(self):
        """crew-board "A landing fix taking main in"."""
        assert board.head_said(self.ledger(self.flume_19("bolt-conflict-fixing"), self.ASKED)).endswith(
            "; Flume's landing fix y-1 takes main in")

    def test_a_head_line_names_the_bound_spent(self):
        """crew-board "The bound spent on the head line"."""
        got = board.head_said(self.ledger(self.flume_19("bolt-failed-spent"), self.ASKED))
        assert got.startswith("landing refused at aaaaaaa, a check failed") and got.endswith("Flume ran its 3 landing fixes, and it waits on ops")

    def test_ops_band_lists_a_landing_in_flight_with_its_request_or_entry(self):
        p = {"label": "wldn", "construction": [
            dict(self.ledger({"outcome": "asked", "request": 57}, self.ASKED), repo="crew", markers=[]),
            dict(self.ledger({"outcome": "submitted", "request": 58, "entry": "412", "state": "under_test"}), bolt="z", repo="crew",
                 markers=[])], "environments": [], "fixing": [], "attention": []}
        said = [" ".join(f for f, _ in r["fields"] if f) if isinstance(r, dict) and "fields" in r else str(r) for r in board.ops_view(p)]
        text = "\n".join(said)
        assert "landing asked, request 57" in text and "landing #412 under test" in text, text

    def test_ops_band_draws_the_head_line_of_a_bolt_started_before_bolts_were_base_places(self):
        """crew-board "A bolt started before bolts were base places": the words show in ops's band as in the lane."""
        legacy = {"outcome": "legacy", "words": "w was started before bolts were base places and lands under the crew that started it"}
        p = {"label": "wldn", "construction": [dict(self.ledger(legacy, state="active"), bolt="w", repo="crew", markers=[], units=[],
                                                    fixes=[], pips=[], stream=None, host="deneb")],
             "environments": [], "fixing": [], "attention": []}
        said = "\n".join(" ".join(f for f, _ in r["fields"] if f) if isinstance(r, dict) and "fields" in r else str(r)
                         for r in board.ops_view(p))
        assert legacy["words"] in said, said
