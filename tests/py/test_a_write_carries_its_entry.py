"""A write carries its entries (an-act-carries-its-entry-in-its-own-commit; plan.2, read.5, state.1, record.4): a plan
write's commit adds the entries of its act, its asks and its further acts to its host's day file in its own files, made
again on each replay, named in its trailers and naming no Commit, a day file the change replaced taking them on its
text; once its push is accepted the host's own file holds them and the host's kept entries are pushed after it, and a
refused write writes nothing of the host's. A write given no act is refused before it reads or pushes anything, and
every write crew makes names its act. plan.land is stood in to run make on tips in memory, with plan.show, plan.read
and record.reach stood in. A real write read whole once it returns is the contract tier's
(tests/contract/test_record.py); the commands' wiring, t-journey-state's and t-journey-plan's."""
import ast
import datetime
import pathlib

import pytest

from facts import FactsWrite, STANDING, keeping, known, plan_text

import crew
import plan
import record

REPO = "WilldanGroup/crew-state"
# wldn/main as read on 2026-11-07, newest first: 18883a31f approved proposal 1009 (18:01:26Z), e0d5a954b proposed 1010
# (17:47:23Z), 16f19a887 cleared a unit's mark naming an entry no act wrote (17:46:34Z), and below it the same process's
# stage.end, whose entry the branch holds.
APPROVE, PROPOSE, CLEARED, END = (s + "0" * 31 for s in ("18883a31f", "e0d5a954b", "16f19a887", "0c1d2e3f4"))
BELOW = "1" * 40
IDS = {APPROVE: "20261107T180126Z-120000-chuck-herdr-alpha-77-1", PROPOSE: "20261107T174723Z-110000-chuck-herdr-alpha-66-1",
       CLEARED: "20261107T174633Z-983370-chuck-herdr-alpha-2601180-2", END: "20261107T174623Z-500000-chuck-herdr-alpha-2601180-1"}
COMMITS = [(APPROVE, PROPOSE, [IDS[APPROVE]]), (PROPOSE, CLEARED, [IDS[PROPOSE]]), (CLEARED, END, [IDS[CLEARED]]), (END, BELOW, [IDS[END]])]
DAY = "runs/chuck-herdr-alpha/2026-11-07.rec"
SUBJECT = "plan(production-stands-stage-in-devs-account): the-copy-acting-for-a-class-is-one-declared-value constructed again, its mark cleared (swb-2-conductor)"
SAID = ("wldn/main was read at 0c1d2e3, below its tip 18883a3: the write 16f19a8 by swb-2-conductor is on the branch without its "
        "run-record entry yet, so nothing from 16f19a8 on was read (read.5)")


def held(*commits):
    """The day's run-record file at the tip, holding the entries of the commits named."""
    return {DAY: "".join(f"Id: {IDS[c]}\nAct: x\n\n" for c in commits)}


# ------------------------------------------------------------------------------------------- every write is an act

def test_a_write_given_no_act_is_refused_before_it_reads_or_pushes_anything(monkeypatch):
    """The reading of 2026-11-07: wldn/main's 16f19a887 named Crew-Entry 20261107T174633Z-983370-chuck-herdr-alpha-2601180-2,
    which no run record held, since the write that cleared the mark was given no act; every decision after it read the
    branch at its parent for sixteen minutes. A write with no act now writes nothing."""
    touched = []
    monkeypatch.setattr(plan, "state_of", lambda fleet, label: touched.append("read") or (REPO, f"{label}/main"))
    monkeypatch.setattr(plan, "land", lambda *a: touched.append("pushed"))
    with pytest.raises(crew.Refusal) as e:
        plan.write({}, "wldn", lambda w: [], "plan(b): u constructed again, its mark cleared")
    assert str(e.value) == ('crew does not write "plan(b): u constructed again, its mark cleared": a write names its act, whose '
                            "run-record entry its commit names and the write itself records, and this one names none (plan.2)")
    assert touched == []
    assert plan.unacted("unit.unmark", "plan(b): u constructed again, its mark cleared") is None


def test_every_plan_write_crew_makes_names_its_act():
    """plan.write's callers, read from plan.py itself: each names act=, so none is refused at run time and none commits an
    entry nothing writes. On crew main, the give of a bolt, a unit marked amended so its construct runs again, and that
    mark cleared were the three that named none; this line has none of the three."""
    tree = ast.parse(pathlib.Path(plan.__file__).read_text())
    # a plan write takes the fleet, the label, the change and the subject; a session's write() of its own takes none
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "write"
             and len(n.args) >= 4]
    assert len(calls) > 10
    assert [n.lineno for n in calls if not any(k.arg == "act" for k in n.keywords)] == []


# ---------------------------------------------------------------------------------- a write carries its entries

STATE = "afterthought/crew-state"
BOLT = "Bolt: b\nRepo: crew\nGoal: B is built.\n"
OTHER = "20261110T090000Z-000001-deneb-41-1"  # another command's entry of the same host and day


def other_entry(repo="crew"):
    return f"Id: {OTHER}\nAt: 2026-11-10T09:00:00Z\nHost: deneb\nBy: chuck@deneb\nAct: bolt.land\nOn: bolt/a\nRepo: {repo}\n"


class Branch:
    """madswan's branch in memory: each tip's files, the tips a write is applied to in turn (the last accepted, or
    refused when refuse is set), the commits made and record.reach's calls."""

    def __init__(self, monkeypatch, tmp_path, *tips, refuse=False):
        self.tips, self.order, self.refuse = {f"t{i}": dict(files) for i, files in enumerate(tips)}, [f"t{i}" for i in range(len(tips))], refuse
        self.made, self.reached = [], []
        self.here = tmp_path / "crew" / "madswan" / "runs" / "deneb"
        monkeypatch.setattr(record, "ROOT", tmp_path / "crew")
        monkeypatch.setattr(record, "_session", ...)
        monkeypatch.setenv("CREW_SESSION", "")
        monkeypatch.delenv("CREW_AGENT", raising=False)
        monkeypatch.setattr(crew, "this_host", lambda: "deneb")
        monkeypatch.setattr(plan, "agent", lambda: "madswan-planner")
        monkeypatch.setattr(plan, "state_of", lambda fleet, label: (STATE, f"{label}/main"))
        monkeypatch.setattr(plan, "read", lambda repo, ref, tip: plan.Plan(self.tips[tip]["plan.rec"]))
        monkeypatch.setattr(plan, "show", lambda repo, tip, path: self.tips[tip].get(path))
        monkeypatch.setattr(plan, "paths_at", lambda repo, tip, prefix: sorted(p for p in self.tips[tip] if p.startswith(prefix)))
        monkeypatch.setattr(plan, "cat_file", lambda repo, names: [self.tips[n.split(":", 1)[0]].get(n.split(":", 1)[1]) for n in names])
        monkeypatch.setattr(plan, "runners", lambda repo, label: {})
        monkeypatch.setattr(plan, "land", self.land)
        monkeypatch.setattr(record, "reach", lambda label, eid=None, said=False: self.reached.append((label, eid, said)) or 0)

    def land(self, repo, ref, path, make):
        for tip in self.order:
            self.made.append(make(tip))
        self.refuse and plan.fail(f"{ref} of {repo} kept moving")
        return "c" * 40

    def committed(self):
        """The last commit's files, its day file's entries as record.parse gives them, and the ids its trailers name."""
        files, msg = self.made[-1]
        day, = [p for p in files if p.startswith("runs/")]
        return files, day, record.parse(files[day]), [l.split(": ", 1)[1] for l in msg.splitlines() if l.startswith("Crew-Entry: ")]


def add_bolt(w):
    w.plan.insert(plan.Rec("Bolt", [("Bolt", "b"), ("Repo", "crew"), ("Goal", "B is built.")]))
    return []


def written(b, change=add_bolt, **kw):
    return plan.write({}, "madswan", change, "plan(b): add the bolt", act="bolt.new", on=["bolt/b"], **kw)


def test_a_writes_commit_holds_the_plan_and_its_hosts_day_file_with_its_entry(monkeypatch, tmp_path):
    b = Branch(monkeypatch, tmp_path, {"plan.rec": plan_text()})
    written(b)
    files, day, entries, eids = b.committed()
    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    assert sorted(files) == ["plan.rec", f"runs/deneb/{today}.rec"] and BOLT in files["plan.rec"]
    e, = entries
    assert files[day].startswith(record.DESCRIPTOR) and e["At"][:10] == today and [e["Id"]] == eids
    import getpass
    assert (e["Act"], e["On"], e["Host"], e["By"], e["Why"], e["Commit"]) == (
        "bolt.new", ["bolt/b"], "deneb", f"{getpass.getuser()}@deneb", "plan(b): add the bolt", [])
    assert b.made[-1][1].startswith("plan(b): add the bolt (madswan-planner)\n\nCrew-Entry: ")


def test_an_asks_and_a_further_acts_entries_are_carried_each_named_in_a_trailer(monkeypatch, tmp_path, capsys):
    b = Branch(monkeypatch, tmp_path, {"plan.rec": plan_text()})
    ask, move = record.new_id(), record.new_id()

    def change(w):
        add_bolt(w)
        w.asked.append((ask, plan.Rec("Ask", [("Role", "planner"), ("What", "landed"), ("Names", "bolt/b"), ("Words", "x" * 12)])))
        w.also.append((move, "signal.move", ["signals/s/01-c", "unit/u"], {"why": "signals(s/01-c): route to unit/u", "frm": ["proposal/7"]}))
        return []
    written(b, change)
    _, _, entries, eids = b.committed()
    assert eids[1:] == [ask, move] and sorted(e["Id"] for e in entries) == sorted(eids)
    by = {e["Id"]: e for e in entries}
    assert (by[ask]["Act"], by[ask]["On"], by[ask]["Why"], by[ask]["Chars"]) == ("ask", ["agent/madswan-planner", "bolt/b"],
                                                                                  "ask madswan-planner: landed", "12")
    assert (by[move]["Act"], by[move]["On"], by[move]["From"], by[move]["Why"]) == (
        "signal.move", ["signals/s/01-c", "unit/u"], ["proposal/7"], "signals(s/01-c): route to unit/u")
    assert by[eids[0]]["Why"] == "plan(b): add the bolt"
    assert all(e["Commit"] == [] for e in entries)
    assert "asked madswan-planner: landed on bolt/b" in capsys.readouterr().out


def test_a_replay_on_a_tip_whose_day_file_gained_another_entry_keeps_it(monkeypatch, tmp_path):
    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    path = f"runs/deneb/{today}.rec"
    b = Branch(monkeypatch, tmp_path, {"plan.rec": plan_text()}, {"plan.rec": plan_text(), path: record.DESCRIPTOR + other_entry()})
    written(b)
    (_, first), (files, last) = b.made
    assert first.split("Crew-Entry: ")[1] == last.split("Crew-Entry: ")[1]  # the act's id made once for the write
    _, day, entries, eids = b.committed()
    assert day == path and other_entry() in files[path] and [e["Id"] for e in entries] == sorted([OTHER, eids[0]])


def test_a_renames_day_file_has_its_entry_added_to_the_text_the_rename_left(monkeypatch, tmp_path):
    """crew kit rename tailrace timber on a tip whose runs/deneb/<day>.rec holds a bolt.land under tailrace, on deneb:
    the commit's file holds that entry under timber and the kit.rename entry beside it, From: kit/tailrace."""
    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    path = f"runs/deneb/{today}.rec"
    b = Branch(monkeypatch, tmp_path, {"plan.rec": plan_text(bolts=[("crew-bolt", "crew", False)]), path: record.DESCRIPTOR + other_entry("tailrace")})
    fleet = {"drives": {"madswan": dict({"label": "madswan", "machine": "deneb", "runs": STANDING}, **keeping("/d/agentplot", "agentplot/timber"))},
             "hosts": {"deneb": {"ssh": "deneb", "kind": "darwin"}}}
    op = plan.OPS[("kit", "rename")](known(FactsWrite(plan_text(), label="madswan"), fleet=fleet), plan.do_args("madswan", "kit rename tailrace timber"))
    plan.write(fleet, op.label, op.change, op.subject, op.body, act=op.act, on=op.on, frm=op.frm, fields=op.fields)
    files, day, entries, eids = b.committed()
    assert day == path and other_entry("timber") in files[path]
    rename, = [e for e in entries if e["Id"] == eids[0]]
    assert (rename["Act"], rename["On"], rename["From"], rename["Repo"], rename["Count"], rename["Commit"]) == (
        "kit.rename", ["kit/timber"], ["kit/tailrace"], "timber", "1", [])


def test_once_pushed_the_hosts_file_holds_the_entries_and_its_kept_entries_are_pushed_after(monkeypatch, tmp_path):
    b = Branch(monkeypatch, tmp_path, {"plan.rec": plan_text()})
    move = record.new_id()

    def change(w):
        add_bolt(w)
        w.also.append((move, "signal.move", ["signals/s/01-c", "bolt/b"], {}))
        return []
    written(b, change)
    files, day, entries, eids = b.committed()
    mine = (b.here / pathlib.PurePath(day).name).read_text()
    # appended one write each, the act's first, as the trailers name them
    assert mine.startswith(record.DESCRIPTOR) and [e["Id"] for e in record.parse(mine)] == eids
    assert sorted(record.parse(mine), key=lambda e: e["Id"]) == entries
    assert b.reached == [("madswan", None, True)]


def test_a_refused_write_leaves_the_hosts_file_as_it_was(monkeypatch, tmp_path):
    b = Branch(monkeypatch, tmp_path, {"plan.rec": plan_text()}, {"plan.rec": plan_text()}, refuse=True)
    with pytest.raises(crew.Refusal, match="kept moving"):
        written(b)
    assert len(b.made) == 2 and not b.here.exists() and b.reached == []


def test_a_state_init_steps_commit_carries_its_state_init_entry(monkeypatch, tmp_path):
    """Decision 3: crew state init's first step, on a branch not there yet, and a later one, each commit carrying its
    state.init entry naming no commit, the host's file holding it once pushed and its kept entries pushed after."""
    b = Branch(monkeypatch, tmp_path, {"plan.rec": plan.HEADER})
    b.order = [None]
    sha = plan.init_step(STATE, "madswan/main", "madswan", "state(madswan): start the drive's plan",
                         lambda tip, files: files.update({"plan.rec": plan.HEADER}))
    files, day, (e,), eids = b.committed()
    assert sha == "c" * 40 and sorted(files) == ["plan.rec", day] and day.startswith("runs/deneb/")
    assert (e["Act"], e["On"], e["Why"], e["Commit"], [e["Id"]]) == ("state.init", ["plan/madswan"], "state(madswan): start the drive's plan", [], eids)
    assert b.made[-1][1].startswith("state(madswan): start the drive's plan (madswan-planner)\n\nCrew-Entry: ")
    assert record.parse((b.here / pathlib.PurePath(day).name).read_text()) == [e] and b.reached == [("madswan", None, True)]
    b.order, b.tips["t0"][day] = ["t0"], files[day]  # the next step, on the tip the first left
    plan.init_step(STATE, "madswan/main", "madswan", "state(madswan): moves.rec", lambda tip, files: files.update({"moves.rec": plan.MOVES}))
    files, _, entries, eids = b.committed()
    assert [x["Id"] for x in entries] == sorted([e["Id"], eids[0]]) and sorted(files) == sorted([day, "moves.rec"])


# ------------------------------------------------------------------------------------- a read below the tip says so

def test_the_write_a_read_waits_on_is_the_oldest_in_flight_and_the_read_is_unchanged():
    """decision_at reads wldn/main below 16f19a887, as it did, and the write it waits on is 16f19a887 itself."""
    texts = held(APPROVE, PROPOSE, END)
    assert plan.decision_at(COMMITS, texts) == END
    assert plan.waited_on(COMMITS, texts) == CLEARED
    assert [c[0] for c in plan.in_flight(COMMITS, texts)] == [CLEARED]
    assert plan.decision_at(COMMITS, {}) == BELOW and plan.waited_on(COMMITS, {}) == END  # the oldest of all in flight
    whole = held(APPROVE, PROPOSE, CLEARED, END)
    assert plan.decision_at(COMMITS, whole) == APPROVE and plan.waited_on(COMMITS, whole) is None
    # a branch whose first commit is in flight is read at its tip, waiting on nothing; and no commits, nothing
    assert plan.decision_at([(CLEARED, None, [IDS[CLEARED]])], {}) == CLEARED and plan.waited_on([(CLEARED, None, [IDS[CLEARED]])], {}) is None
    assert plan.waited_on([], {}) is None


def test_a_writes_agent_is_its_subjects_and_a_subject_naming_none_says_so():
    assert plan.writer_of(SUBJECT) == "swb-2-conductor"
    assert plan.writer_of("runs(chuck-herdr-alpha): stage.end stage/u/construct (swb-2-conductor)") == "swb-2-conductor"
    assert plan.writer_of("plan: start") is None and plan.writer_of("") is None and plan.writer_of(None) is None
    assert plan.below_said("wldn/main", APPROVE, END, CLEARED, SUBJECT) == SAID
    assert plan.below_said("wldn/main", APPROVE, END, CLEARED, "plan: by hand") == (
        "wldn/main was read at 0c1d2e3, below its tip 18883a3: the write 16f19a8, whose subject names no agent, is on the "
        "branch without its run-record entry yet, so nothing from 16f19a8 on was read (read.5)")


def test_a_commands_latest_read_of_a_branch_is_what_it_says_and_a_read_at_the_tip_takes_it_back():
    r = plan.Reading()
    assert r.below() == []
    r.keep_below(REPO, "wldn/main", PROPOSE, END, (CLEARED, SUBJECT))
    r.keep_below(REPO, "wldn/main", APPROVE, END, (CLEARED, SUBJECT))  # read again, the tip moved, still below the write
    r.keep_below(REPO, "swancloud/main", "3" * 40, "4" * 40, ("5" * 40, "plan: x (swancloud-planner)"))
    assert r.below() == [dict(ref="wldn/main", tip=APPROVE, at=END, write=CLEARED, subject=SUBJECT),
                         dict(ref="swancloud/main", tip="3" * 40, at="4" * 40, write="5" * 40, subject="plan: x (swancloud-planner)")]
    r.keep_below(REPO, "wldn/main", "6" * 40, "6" * 40, None)  # read at its tip once the entry arrived
    r.keep_below(REPO, "swancloud/main", None, None, None)  # a branch not there
    assert r.below() == []


def test_a_refusal_after_a_read_below_the_tip_says_so_first_and_an_answer_says_so_on_standard_error(monkeypatch, capsys):
    """crew plan answer 1010 and crew plan proposed 1010 answered "no proposal 1010 in wldn/main" while proposals.rec held
    it open, read at e0d5a954b's grandparent; now the refusal says where the branch was read and what it waits on, its
    own words still its last line."""
    r = plan.Reading()
    monkeypatch.setattr(plan, "READ", r)
    assert plan.below_read("no proposal 1010 in wldn/main") == "no proposal 1010 in wldn/main"
    assert plan.below_read() == "" and capsys.readouterr().err == ""
    r.keep_below(REPO, "wldn/main", APPROVE, END, (CLEARED, SUBJECT))
    assert plan.below_read("no proposal 1010 in wldn/main") == f"{SAID}\nno proposal 1010 in wldn/main"
    assert plan.below_read() == ""
    out = capsys.readouterr()
    assert out.err == SAID + "\n" and out.out == ""
